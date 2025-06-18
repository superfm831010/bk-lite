import json
import re
import time

import requests
from django.conf import settings
from django.http import StreamingHttpResponse

from apps.core.logger import opspilot_logger as logger
from apps.opspilot.bot_mgmt.utils import insert_skill_log
from apps.opspilot.enum import SkillTypeChoices
from apps.opspilot.model_provider_mgmt.models import LLMModel
from apps.opspilot.model_provider_mgmt.services.llm_service import llm_service
from apps.opspilot.quota_rule_mgmt.models import TeamTokenUseInfo
from apps.opspilot.utils.chat_server_helper import ChatServerHelper


def generate_stream_error(message):
    """通用的流式错误生成函数"""

    def generator():
        error_chunk = {
            "choices": [{"delta": {"content": message}, "index": 0, "finish_reason": "stop"}],
            "id": "error",
            "object": "chat.completion.chunk",
            "created": int(time.time()),
        }
        yield f"data: {json.dumps(error_chunk)}\n\n"

    response = StreamingHttpResponse(generator(), content_type="text/event-stream")
    # 添加必要的头信息以防止缓冲
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response


def _process_think_content(content_chunk, think_buffer, in_think_block, is_first_content, show_think, has_think_tags):
    """处理思考过程相关的内容过滤"""
    if show_think:
        # 显示思考过程，直接返回内容
        return content_chunk, think_buffer, in_think_block, False, has_think_tags

    # 如果是第一次接收内容，检查是否包含 <think> 标签
    if is_first_content:
        think_buffer += content_chunk
        # 检查整个缓冲区是否包含 <think> 标签
        if "<think>" not in think_buffer:
            # 如果没有 <think> 标签，直接返回内容，后续也不再检查
            return think_buffer, "", in_think_block, False, False
        else:
            # 有 <think> 标签，启用过滤机制
            has_think_tags = True
            # 检查是否以 <think> 开头
            if think_buffer.lstrip().startswith("<think>"):
                in_think_block = True
                think_start = think_buffer.find("<think>")
                think_buffer = think_buffer[think_start + 7 :]
                return "", think_buffer, in_think_block, False, has_think_tags

    # 如果确定没有 think 标签，直接返回内容
    if not has_think_tags:
        return content_chunk, think_buffer, in_think_block, False, has_think_tags

    # 隐藏思考过程的处理逻辑
    think_buffer += content_chunk
    output_chunks = []

    # 处理缓冲区内容
    while think_buffer:
        if not in_think_block:
            # 不在思考块中，查找 <think> 开始标签
            think_start_pos = think_buffer.find("<think>")
            if think_start_pos != -1:
                # 发送思考标签之前的内容
                before_think = think_buffer[:think_start_pos]
                if before_think:
                    output_chunks.append(before_think)
                # 进入思考块
                in_think_block = True
                think_buffer = think_buffer[think_start_pos + 7 :]
            else:
                # 没有找到 <think> 标签，保留一些字符以防标签被分割
                if len(think_buffer) > 8:
                    send_content = think_buffer[:-8]
                    think_buffer = think_buffer[-8:]
                    if send_content:
                        output_chunks.append(send_content)
                break
        else:
            # 在思考块中，查找 </think> 结束标签
            think_end_pos = think_buffer.find("</think>")
            if think_end_pos != -1:
                # 找到结束标签，退出思考块
                in_think_block = False
                think_buffer = think_buffer[think_end_pos + 8 :]
            else:
                # 还在思考块中，清空缓冲区（不发送内容）
                think_buffer = ""
                break

    return "".join(output_chunks), think_buffer, in_think_block, False, has_think_tags


def _create_stream_chunk(content, skill_name, finish_reason=None):
    """创建流式响应块"""
    return {
        "choices": [{"delta": {"content": content}, "index": 0, "finish_reason": finish_reason}],
        "id": skill_name,
        "object": "chat.completion.chunk",
        "created": int(time.time()),
    }


def _create_error_chunk(error_message, skill_name):
    """创建错误响应块"""
    return {
        "choices": [{"delta": {"content": error_message}, "index": 0, "finish_reason": "stop"}],
        "id": skill_name,
        "object": "chat.completion.chunk",
        "created": int(time.time()),
    }


def _process_sse_line(
    line,
    accumulated_content,
    prompt_tokens,
    completion_tokens,
    think_buffer,
    in_think_block,
    is_first_content,
    show_think,
    has_think_tags,
):
    """处理单行SSE数据"""
    if not line or not line.strip() or not line.startswith("data: "):
        return (
            accumulated_content,
            prompt_tokens,
            completion_tokens,
            think_buffer,
            in_think_block,
            is_first_content,
            None,
            has_think_tags,
        )

    data_str = line[6:]  # 移除 "data: " 前缀

    # 检查是否为结束标志
    if data_str.strip() == "[DONE]":
        return (
            accumulated_content,
            prompt_tokens,
            completion_tokens,
            think_buffer,
            in_think_block,
            is_first_content,
            "DONE",
            has_think_tags,
        )

    try:
        data = json.loads(data_str)
        output_content = ""

        # 收集token统计信息（在顶层）
        if "prompt_tokens" in data:
            prompt_tokens = data["prompt_tokens"]
        if "completion_tokens" in data:
            completion_tokens = data["completion_tokens"]

        # 检查是否有choices数组并且不为空
        if "choices" in data and data["choices"]:
            choice = data["choices"][0]

            # 检查是否结束
            if choice.get("finish_reason") == "stop":
                return (
                    accumulated_content,
                    prompt_tokens,
                    completion_tokens,
                    think_buffer,
                    in_think_block,
                    is_first_content,
                    "DONE",
                    has_think_tags,
                )

            # 处理内容增量
            if "delta" in choice and "content" in choice["delta"]:
                content_chunk = choice["delta"]["content"]
                if content_chunk:  # 只有非空内容才处理
                    accumulated_content += content_chunk

                    (
                        output_content,
                        think_buffer,
                        in_think_block,
                        is_first_content,
                        has_think_tags,
                    ) = _process_think_content(
                        content_chunk,
                        think_buffer,
                        in_think_block,
                        is_first_content,
                        show_think,
                        has_think_tags,
                    )

        return (
            accumulated_content,
            prompt_tokens,
            completion_tokens,
            think_buffer,
            in_think_block,
            is_first_content,
            output_content,
            has_think_tags,
        )

    except json.JSONDecodeError:
        # 忽略无效的JSON数据
        return (
            accumulated_content,
            prompt_tokens,
            completion_tokens,
            think_buffer,
            in_think_block,
            is_first_content,
            None,
            has_think_tags,
        )


def _generate_sse_stream(url, headers, chat_kwargs, skill_name, show_think):
    """生成SSE流式数据"""
    accumulated_content = ""
    prompt_tokens = 0
    completion_tokens = 0
    think_buffer = ""
    in_think_block = False
    is_first_content = True
    has_think_tags = True  # 默认假设有 think 标签，在第一次处理时会确定

    # 发起SSE请求
    res = requests.post(url, headers=headers, json=chat_kwargs, timeout=300, verify=False, stream=True)
    res.raise_for_status()

    for line in res.iter_lines(decode_unicode=True):
        result = _process_sse_line(
            line,
            accumulated_content,
            prompt_tokens,
            completion_tokens,
            think_buffer,
            in_think_block,
            is_first_content,
            show_think,
            has_think_tags,
        )
        (
            accumulated_content,
            prompt_tokens,
            completion_tokens,
            think_buffer,
            in_think_block,
            is_first_content,
            output,
            has_think_tags,
        ) = result

        if output == "DONE":
            break
        elif output and output != "":
            # 生成并发送流式响应块
            stream_chunk = _create_stream_chunk(output, skill_name)
            yield f"data: {json.dumps(stream_chunk)}\n\n"

    # 处理剩余的缓冲区内容
    if not show_think and not in_think_block and think_buffer:
        stream_chunk = _create_stream_chunk(think_buffer, skill_name)
        yield f"data: {json.dumps(stream_chunk)}\n\n"

    return accumulated_content, prompt_tokens, completion_tokens


def stream_chat(params, skill_name, kwargs, current_ip, user_message, skill_id=None):
    llm_model = LLMModel.objects.get(id=params["llm_model"])
    show_think = params.pop("show_think", True)
    group = params.pop("group", 0)
    # 处理用户消息和图片
    chat_kwargs, doc_map, title_map = llm_service.format_chat_server_kwargs(params, llm_model)
    # 选择正确的SSE端点
    url = f"{settings.METIS_SERVER_URL}/api/agent/invoke_chatbot_workflow_sse"
    if (
        params.get(
            "skill_type",
        )
        == SkillTypeChoices.BASIC_TOOL
    ):
        url = f"{settings.METIS_SERVER_URL}/api/agent/invoke_react_agent_sse"

    def generate_stream():
        try:
            headers = ChatServerHelper.get_chat_server_header()

            # 生成流式内容并收集最终数据
            stream_generator = _generate_sse_stream(url, headers, chat_kwargs, skill_name, show_think)
            accumulated_content = ""
            prompt_tokens = 0
            completion_tokens = 0

            # 处理流式数据
            for chunk in stream_generator:
                if isinstance(chunk, tuple):  # 最终返回的统计数据
                    accumulated_content, prompt_tokens, completion_tokens = chunk
                else:  # 流式响应块
                    yield chunk

            # 处理最终内容（移除思考过程）
            final_content = accumulated_content
            if not show_think:
                final_content = re.sub(r"<think>.*?</think>", "", accumulated_content, flags=re.DOTALL).strip()

            # 记录日志
            log_data = {
                "id": skill_name,
                "object": "chat.completion",
                "created": int(time.time()),
                "model": skill_name,
                "usage": {
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": prompt_tokens + completion_tokens,
                },
                "choices": [
                    {
                        "message": {"role": "assistant", "content": final_content},
                        "finish_reason": "stop",
                        "index": 0,
                    }
                ],
            }
            insert_skill_log(current_ip, skill_id, log_data, kwargs, user_message=user_message)
        except requests.exceptions.RequestException as e:
            logger.error(f"SSE request failed: {e}")
            error_chunk = _create_error_chunk(f"连接错误: {str(e)}", skill_name)
            yield f"data: {json.dumps(error_chunk)}\n\n"
            return

        except Exception as e:
            logger.error(f"Stream processing error: {e}")
            error_chunk = _create_error_chunk(f"处理错误: {str(e)}", skill_name)
            yield f"data: {json.dumps(error_chunk)}\n\n"
            return

        # 发送最终的完成标志
        final_chunk = _create_stream_chunk("", skill_name, "stop")
        yield f"data: {json.dumps(final_chunk)}\n\n"
        used_token = prompt_tokens + completion_tokens
        team_info, is_created = TeamTokenUseInfo.objects.get_or_create(
            group=group, llm_model=llm_model.name, defaults={"used_token": used_token}
        )
        if not is_created:
            team_info.used_token += used_token
            team_info.save()

    response = StreamingHttpResponse(generate_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response

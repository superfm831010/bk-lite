import datetime
import hashlib
import json
import re
import time

import requests
from django.conf import settings
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.http import FileResponse, JsonResponse, StreamingHttpResponse
from django_minio_backend import MinioBackend

from apps.base.models import UserAPISecret
from apps.core.logger import logger
from apps.core.utils.exempt import api_exempt
from apps.opspilot.bot_mgmt.services.skill_excute_service import SkillExecuteService
from apps.opspilot.bot_mgmt.utils import get_client_ip, insert_skill_log, set_time_range
from apps.opspilot.enum import SkillTypeChoices
from apps.opspilot.model_provider_mgmt.models import LLMModel
from apps.opspilot.model_provider_mgmt.services.llm_service import llm_service
from apps.opspilot.models import Bot, BotChannel, BotConversationHistory, LLMSkill, TokenConsumption
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


@api_exempt
def get_bot_detail(request, bot_id):
    api_token = request.META.get("HTTP_AUTHORIZATION").split("TOKEN")[-1].strip()
    if not api_token:
        return JsonResponse({})
    bot = Bot.objects.filter(id=bot_id, api_token=api_token).first()
    if not bot:
        return JsonResponse({})
    channels = BotChannel.objects.filter(bot_id=bot_id, enabled=True)
    return_data = {
        "channels": [
            {
                "id": i.id,
                "name": i.name,
                "channel_type": i.channel_type,
                "channel_config": i.decrypted_channel_config,
            }
            for i in channels
        ],
    }
    return JsonResponse(return_data)


@api_exempt
def model_download(request):
    bot_id = request.GET.get("bot_id")
    bot = Bot.objects.filter(id=bot_id).first()
    if not bot:
        return JsonResponse({})
    rasa_model = bot.rasa_model
    if not rasa_model:
        return JsonResponse({})
    storage = MinioBackend(bucket_name="munchkin-private")
    file = storage.open(rasa_model.model_file.name, "rb")

    # Calculate ETag
    data = file.read()
    etag = hashlib.md5(data).hexdigest()

    # Reset file pointer to start
    file.seek(0)

    response = FileResponse(file)
    response["ETag"] = etag

    return response


def validate_openai_token(token):
    """Validate the OpenAI API token"""
    if not token:
        return False, {"choices": [{"message": {"role": "assistant", "content": "No authorization"}}]}
    token = token.split("Bearer ")[-1]
    user = UserAPISecret.objects.filter(api_secret=token).first()
    if not user:
        return False, {"choices": [{"message": {"role": "assistant", "content": "No authorization"}}]}
    return True, user


def get_skill_and_params(kwargs, team):
    """Get skill object and prepare parameters for LLM invocation"""
    skill_id = kwargs.get("model")
    skill_obj = LLMSkill.objects.filter(name=skill_id, team__contains=int(team)).first()

    if not skill_obj:
        return None, None, {"choices": [{"message": {"role": "assistant", "content": "No skill"}}]}
    num = kwargs.get("conversation_window_size") or skill_obj.conversation_window_size
    chat_history = [{"message": i["content"], "event": i["role"]} for i in kwargs.get("messages", [])[-1 * num :]]

    params = {
        "llm_model": skill_obj.llm_model_id,
        "skill_prompt": kwargs.get("prompt", "") or skill_obj.skill_prompt,
        "temperature": kwargs.get("temperature") or skill_obj.temperature,
        "chat_history": chat_history,
        "user_message": chat_history[-1]["message"],
        "conversation_window_size": kwargs.get("conversation_window_size") or skill_obj.conversation_window_size,
        "enable_rag": kwargs.get("enable_rag") or skill_obj.enable_rag,
        "rag_score_threshold": [
            {"knowledge_base": int(key), "score": float(value)}
            for key, value in skill_obj.rag_score_threshold_map.items()
        ],
        "enable_rag_knowledge_source": skill_obj.enable_rag_knowledge_source,
        "show_think": skill_obj.show_think,
        "tools": skill_obj.tools,
        "skill_type": skill_obj.skill_type,
    }

    return skill_obj, params, None


def format_knowledge_sources(content, skill_obj, doc_map=None, title_map=None):
    """Format and append knowledge source references if enabled"""
    if skill_obj.enable_rag_knowledge_source:
        knowledge_titles = {doc_map.get(k, {}).get("name") for k in title_map.keys()}
        last_content = content.strip().split("\n")[-1]
        if "引用知识" not in last_content and knowledge_titles:
            content += f'\n引用知识: {", ".join(knowledge_titles)}'
    return content


def get_knowledge_sources(content, skill_obj, doc_map=None, title_map=None):
    if not skill_obj.enable_rag_knowledge_source:
        return ""
    knowledge_titles = {doc_map.get(k, {}).get("name") for k in title_map.keys()}
    last_content = content.strip().split("\n")[-1]
    if "引用知识" not in last_content and knowledge_titles:
        return f'\n引用知识: {", ".join(knowledge_titles)}'
    return ""


def invoke_chat(params, skill_obj, kwargs, current_ip, user_message):
    return_data, _ = get_chat_msg(current_ip, kwargs, params, skill_obj, user_message)
    return JsonResponse(return_data)


def get_chat_msg(current_ip, kwargs, params, skill_obj, user_message):
    data, doc_map, title_map = llm_service.invoke_chat(params)
    content = format_knowledge_sources(data["message"], skill_obj, doc_map, title_map)
    return_data = {
        "id": skill_obj.name,
        "object": "chat.completion",
        "created": int(time.time()),
        "model": kwargs["model"],
        "usage": {
            "prompt_tokens": data["prompt_tokens"],
            "completion_tokens": data["completion_tokens"],
            "total_tokens": data["prompt_tokens"] + data["completion_tokens"],
            "completion_tokens_details": {
                "reasoning_tokens": 0,
                "accepted_prediction_tokens": 0,
                "rejected_prediction_tokens": 0,
            },
        },
        "choices": [
            {
                "message": {"role": "assistant", "content": content},
                "logprobs": None,
                "finish_reason": "stop",
                "index": 0,
            }
        ],
    }
    insert_skill_log(current_ip, skill_obj.id, return_data, kwargs, user_message=user_message)
    return return_data, content


@api_exempt
def openai_completions(request):
    """Main entry point for OpenAI completions"""
    kwargs = json.loads(request.body)
    current_ip = get_client_ip(request)

    stream_mode = kwargs.get("stream", False)
    token = request.META.get("HTTP_AUTHORIZATION") or request.META.get(settings.API_TOKEN_HEADER_NAME)

    is_valid, msg = validate_openai_token(token)
    if not is_valid:
        if stream_mode:
            return generate_stream_error(msg["choices"][0]["message"]["content"])
        else:
            return JsonResponse(msg)
    user = msg
    skill_obj, params, error = get_skill_and_params(kwargs, user.team)
    if error:
        if skill_obj:
            user_message = params.get("user_message")
            insert_skill_log(current_ip, skill_obj.id, error, kwargs, False, user_message)
        if stream_mode:
            return generate_stream_error(error["choices"][0]["message"]["content"])
        else:
            return JsonResponse(error)
    params["user_id"] = user.username
    user_message = params.get("user_message")
    if not stream_mode:
        return invoke_chat(params, skill_obj, kwargs, current_ip, user_message)
    return stream_chat(params, skill_obj, kwargs, current_ip, user_message)


def _process_think_content(
    content_chunk, think_buffer, in_think_block, is_first_content, show_think, skill_obj, has_think_tags
):
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


def _create_stream_chunk(content, skill_obj, finish_reason=None):
    """创建流式响应块"""
    return {
        "choices": [{"delta": {"content": content}, "index": 0, "finish_reason": finish_reason}],
        "id": skill_obj.name,
        "object": "chat.completion.chunk",
        "created": int(time.time()),
    }


def _create_error_chunk(error_message, skill_obj):
    """创建错误响应块"""
    return {
        "choices": [{"delta": {"content": error_message}, "index": 0, "finish_reason": "stop"}],
        "id": skill_obj.name,
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
    skill_obj,
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
                        skill_obj,
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


def _generate_sse_stream(url, headers, chat_kwargs, skill_obj, show_think):
    """生成SSE流式数据"""
    accumulated_content = ""
    prompt_tokens = 0
    completion_tokens = 0
    think_buffer = ""
    in_think_block = False
    is_first_content = True
    has_think_tags = True  # 默认假设有 think 标签，在第一次处理时会确定

    # 发起SSE请求
    res = requests.post(url, headers=headers, json=chat_kwargs, timeout=300, verify=False)
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
            skill_obj,
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
            stream_chunk = _create_stream_chunk(output, skill_obj)
            yield f"data: {json.dumps(stream_chunk)}\n\n"

    # 处理剩余的缓冲区内容
    if not show_think and not in_think_block and think_buffer:
        stream_chunk = _create_stream_chunk(think_buffer, skill_obj)
        yield f"data: {json.dumps(stream_chunk)}\n\n"

    return accumulated_content, prompt_tokens, completion_tokens


def stream_chat(params, skill_obj, kwargs, current_ip, user_message):
    llm_model = LLMModel.objects.get(id=params["llm_model"])
    llm_service.validate_remaining_token(llm_model)
    show_think = params.pop("show_think", True)

    # 处理用户消息和图片
    chat_kwargs, doc_map, title_map = llm_service.format_chat_server_kwargs(params, llm_model)

    # 选择正确的SSE端点
    url = f"{settings.METIS_SERVER_URL}/api/agent/invoke_chatbot_workflow_sse"
    if params["skill_type"] == SkillTypeChoices.BASIC_TOOL:
        url = f"{settings.METIS_SERVER_URL}/api/agent/invoke_react_agent_sse"

    def generate_stream():
        try:
            headers = ChatServerHelper.get_chat_server_header()

            # 生成流式内容并收集最终数据
            stream_generator = _generate_sse_stream(url, headers, chat_kwargs, skill_obj, show_think)
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
            final_accumulated_content = accumulated_content
            if not show_think:
                final_accumulated_content = re.sub(
                    r"<think>.*?</think>", "", accumulated_content, flags=re.DOTALL
                ).strip()

            # 处理knowledge sources
            final_content = format_knowledge_sources(final_accumulated_content, skill_obj, doc_map, title_map)

            # 如果有额外的knowledge sources信息需要添加
            knowledge_sources = get_knowledge_sources(final_accumulated_content, skill_obj, doc_map, title_map)
            if knowledge_sources:
                stream_chunk = _create_stream_chunk(knowledge_sources, skill_obj)
                yield f"data: {json.dumps(stream_chunk)}\n\n"

            # 记录日志
            log_data = {
                "id": skill_obj.name,
                "object": "chat.completion",
                "created": int(time.time()),
                "model": kwargs["model"],
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
            insert_skill_log(current_ip, skill_obj.id, log_data, kwargs, user_message=user_message)

        except requests.exceptions.RequestException as e:
            logger.error(f"SSE request failed: {e}")
            error_chunk = _create_error_chunk(f"连接错误: {str(e)}", skill_obj)
            yield f"data: {json.dumps(error_chunk)}\n\n"
            return

        except Exception as e:
            logger.error(f"Stream processing error: {e}")
            error_chunk = _create_error_chunk(f"处理错误: {str(e)}", skill_obj)
            yield f"data: {json.dumps(error_chunk)}\n\n"
            return

        # 发送最终的完成标志
        final_chunk = _create_stream_chunk("", skill_obj, "stop")
        yield f"data: {json.dumps(final_chunk)}\n\n"
        group = llm_model.consumer_team or llm_model.team[0]
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


@api_exempt
def skill_execute(request):
    kwargs = json.loads(request.body)
    logger.info(f"skill_execute kwargs: {kwargs}")
    skill_id = kwargs.get("skill_id")
    user_message = kwargs.get("user_message")
    sender_id = kwargs.get("sender_id", "")
    chat_history = kwargs.get("chat_history", [])
    bot_id = kwargs.get("bot_id")
    channel = kwargs.get("channel", "socketio")
    if channel in ["socketio", "rest"]:
        channel = "web"
    return_data = get_skill_execute_result(
        bot_id, channel, chat_history, kwargs, request, sender_id, skill_id, user_message
    )
    return JsonResponse({"result": return_data})


def get_skill_execute_result(bot_id, channel, chat_history, kwargs, request, sender_id, skill_id, user_message):
    api_token = request.META.get("HTTP_AUTHORIZATION").split("TOKEN")[-1].strip()
    if not api_token:
        return {"content": "No authorization"}
    bot = Bot.objects.filter(id=bot_id, api_token=api_token).first()
    if not bot:
        logger.info(f"api_token: {api_token}")
        return {"content": "No bot found"}
    try:
        result = SkillExecuteService.execute_skill(bot, skill_id, user_message, chat_history, sender_id, channel)
    except Exception as e:
        logger.exception(e)
        result = {"content": str(e)}
    if getattr(request, "api_pass", False):
        current_ip = get_client_ip(request)
        insert_skill_log(current_ip, bot.llm_skills.first().id, result, kwargs, user_message=user_message)
    return result


# @HasRole("admin")
def get_total_token_consumption(request):
    start_time_str = request.GET.get("start_time")
    end_time_str = request.GET.get("end_time")
    end_time, start_time = set_time_range(end_time_str, start_time_str)
    total_tokens = TokenConsumption.objects.filter(
        created_at__range=[start_time, end_time],
        bot_id=request.GET.get("bot_id"),
    ).aggregate(total_input_tokens=Sum("input_tokens"), total_output_tokens=Sum("output_tokens"))
    input_tokens = total_tokens["total_input_tokens"] or 0
    output_tokens = total_tokens["total_output_tokens"] or 0
    total_combined_tokens = input_tokens + output_tokens
    return JsonResponse({"result": True, "data": total_combined_tokens})


# @HasRole("admin")
def get_token_consumption_overview(request):
    start_time_str = request.GET.get("start_time")
    end_time_str = request.GET.get("end_time")
    end_time, start_time = set_time_range(end_time_str, start_time_str)
    num_days = (end_time - start_time).days + 1
    all_dates = [start_time + datetime.timedelta(days=i) for i in range(num_days)]
    formatted_dates = {date.strftime("%Y-%m-%d"): 0 for date in all_dates}
    # 查询特定日期范围内的TokenConsumption，并按天分组统计input_tokens和output_tokens的总和
    queryset = (
        TokenConsumption.objects.filter(created_at__range=[start_time, end_time], bot_id=request.GET.get("bot_id"))
        .annotate(date=TruncDate("created_at"))
        .values("date")
        .annotate(input_tokens_sum=Sum("input_tokens"), output_tokens_sum=Sum("output_tokens"))
    )

    # 更新字典与查询结果
    for entry in queryset:
        date = entry["date"].strftime("%Y-%m-%d")
        input_tokens = entry["input_tokens_sum"] or 0
        output_tokens = entry["output_tokens_sum"] or 0
        formatted_dates[date] = input_tokens + output_tokens

    # 转换为所需的输出格式
    result = [{"time": date, "count": values} for date, values in sorted(formatted_dates.items())]
    return JsonResponse({"result": True, "data": result})


# @HasRole("admin")
def get_conversations_line_data(request):
    start_time_str = request.GET.get("start_time")
    end_time_str = request.GET.get("end_time")
    end_time, start_time = set_time_range(end_time_str, start_time_str)
    queryset = (
        BotConversationHistory.objects.filter(
            created_at__range=[start_time, end_time], bot_id=request.GET.get("bot_id"), conversation_role="bot"
        )
        .annotate(date=TruncDate("created_at"))
        .values("channel_user__channel_type", "date")
        .annotate(count=Count("id"))  # 不去重，按记录统计
    )
    # 生成日期范围内的所有日期
    result = set_channel_type_line(end_time, queryset, start_time)
    return JsonResponse({"result": True, "data": result})


# @HasRole("admin")
def get_active_users_line_data(request):
    start_time_str = request.GET.get("start_time")
    end_time_str = request.GET.get("end_time")
    end_time, start_time = set_time_range(end_time_str, start_time_str)
    queryset = (
        BotConversationHistory.objects.filter(
            created_at__range=[start_time, end_time], bot_id=request.GET.get("bot_id"), conversation_role="user"
        )
        .annotate(date=TruncDate("created_at"))
        .values("channel_user__channel_type", "date")
        .annotate(count=Count("channel_user", distinct=True))
    )
    # 生成日期范围内的所有日期
    result = set_channel_type_line(end_time, queryset, start_time)
    return JsonResponse({"result": True, "data": result})


def set_channel_type_line(end_time, queryset, start_time):
    num_days = (end_time - start_time).days + 1
    all_dates = [start_time + datetime.timedelta(days=i) for i in range(num_days)]
    formatted_dates = {date.strftime("%Y-%m-%d"): 0 for date in all_dates}
    known_channel_types = ["web", "ding_talk", "enterprise_wechat", "wechat_official_account"]
    result_dict = {channel_type: formatted_dates.copy() for channel_type in known_channel_types}
    total_user_count = formatted_dates.copy()
    # 更新字典与查询结果
    for entry in queryset:
        channel_type = entry["channel_user__channel_type"]
        date = entry["date"].strftime("%Y-%m-%d")
        user_count = entry["count"]
        result_dict[channel_type][date] = user_count
        total_user_count[date] += user_count
    # 转换为所需的输出格式
    result = {
        channel_type: [{"time": date, "count": user_count} for date, user_count in sorted(date_dict.items())]
        for channel_type, date_dict in result_dict.items()
    }
    result["total"] = [{"time": date, "count": user_count} for date, user_count in sorted(total_user_count.items())]
    return result

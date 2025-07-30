from langchain_mcp_adapters.client import MultiServerMCPClient
from sanic.log import logger
import json
from langchain_core.messages import HumanMessage, AIMessage
from src.tools.tools_loader import ToolsLoader
from src.core.node.basic_node import BasicNode
import json_repair
from typing import Type, TypeVar, Dict, List, Union, Any
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel
import copy

T = TypeVar('T', bound=BaseModel)


class ModelType:
    """模型类型常量"""
    GPT = "gpt"
    QWEN = "qwen"
    OTHER = "other"


class ModelDetector:
    """模型类型检测器"""

    @staticmethod
    def detect_model_type(llm) -> str:
        """
        检测模型类型

        Args:
            llm: LangChain LLM实例

        Returns:
            str: 模型类型 (gpt/qwen/other)
        """
        # 检查模型名称或类名
        model_name = getattr(llm, 'model_name', '').lower()
        model_class = llm.__class__.__name__.lower()

        # GPT模型检测
        if any(keyword in model_name for keyword in ['gpt', 'openai']) or \
           any(keyword in model_class for keyword in ['openai', 'chatgpt']):
            return ModelType.GPT

        # Qwen模型检测
        if any(keyword in model_name for keyword in ['qwen', 'tongyi']) or \
           any(keyword in model_class for keyword in ['qwen', 'tongyi']):
            return ModelType.QWEN

        return ModelType.OTHER


class StructuredOutputParser:
    """结构化输出解析器 - 支持多种模型类型"""

    def __init__(self, llm, max_retries: int = 3):
        self.llm = llm
        self.max_retries = max_retries
        self.model_type = ModelDetector.detect_model_type(llm)
        logger.info(f"检测到模型类型: {self.model_type}")

    def _generate_schema_prompt(self, pydantic_class: Type[T]) -> str:
        """生成包含 Pydantic 模型 schema 的提示"""
        schema = pydantic_class.model_json_schema()
        prompt = f"请以JSON格式返回结果，严格按照以下数据结构：\n\n模型名称: {pydantic_class.__name__}\n"

        if schema.get('description'):
            prompt += f"描述: {schema['description']}\n"

        prompt += "\nJSON Schema:\n"
        prompt += json.dumps(schema, indent=2, ensure_ascii=False)

        # 字段说明
        if 'properties' in schema:
            prompt += "\n\n字段说明:\n"
            for field_name, field_info in schema['properties'].items():
                field_type = field_info.get('type', 'unknown')
                field_desc = field_info.get('description', '无描述')
                required = field_name in schema.get('required', [])
                required_text = "(必填)" if required else "(可选)"
                prompt += f"- {field_name} ({field_type}) {required_text}: {field_desc}\n"

        prompt += f"\n请确保返回的JSON格式完全符合上述schema，并且可以被 {pydantic_class.__name__}.model_validate() 成功解析。"
        prompt += "\n只返回JSON内容，不要添加任何其他文字说明或markdown格式。"
        return prompt

    def _repair_and_parse_json(self, response_text: str, pydantic_class: Type[T]) -> T:
        """修复并解析JSON"""
        try:
            data = json_repair.loads(response_text)
            instance = pydantic_class.model_validate(data)
            return instance
        except Exception as e:
            logger.warning(f"JSON修复和解析失败: {e}")
            return None

    def _prepare_llm_for_chat_mode(self):
        """为聊天模式准备LLM配置"""
        if self.model_type == ModelType.QWEN:
            # Qwen模型需要关闭thinking模式
            if hasattr(self.llm, 'extra_body'):
                if isinstance(self.llm.extra_body, dict):
                    self.llm.extra_body["enable_thinking"] = False
                else:
                    self.llm.extra_body = {"enable_thinking": False}
            logger.debug("为Qwen模型设置enable_thinking=False")

    def _add_json_prompt_if_needed(self, messages: Union[Dict, List], content_key: str = "input") -> Union[Dict, List]:
        """如果需要，添加JSON提示到消息中"""
        patched_messages = copy.deepcopy(messages)
        json_prompt = "\n请以JSON格式返回结果。"

        if isinstance(patched_messages, dict):
            if content_key in patched_messages and "json" not in patched_messages[content_key]:
                patched_messages[content_key] += json_prompt
            elif "messages" in patched_messages and isinstance(patched_messages["messages"], list):
                if (patched_messages["messages"] and
                    hasattr(patched_messages["messages"][-1], "content") and
                        "json" not in patched_messages["messages"][-1].content):
                    patched_messages["messages"][-1].content += json_prompt
        elif isinstance(patched_messages, list) and patched_messages:
            if (hasattr(patched_messages[-1], "content") and
                    "json" not in patched_messages[-1].content):
                patched_messages[-1].content += json_prompt

        return patched_messages

    async def _parse_with_native_structured_output(self, prompt, messages: Union[Dict, List],
                                                   pydantic_class: Type[T]) -> T:
        """使用原生结构化输出解析 (适用于GPT等模型)"""
        planner = prompt | self.llm.with_structured_output(pydantic_class)

        # 准备调用参数
        invoke_args = messages if isinstance(messages, dict) else {
            "messages": messages}

        try:
            return await planner.ainvoke(invoke_args)
        except Exception as e:
            # 处理OpenAI response_format=json_object 的特殊情况
            err_msg = str(e)
            if (hasattr(self.llm, "kwargs") and
                self.llm.kwargs.get("response_format") == {"type": "json_object"} and
                    "must contain the word 'json'" in err_msg):

                logger.warning("检测到OpenAI JSON格式要求，自动添加json提示")
                patched_messages = self._add_json_prompt_if_needed(messages)
                patched_invoke_args = patched_messages if isinstance(
                    patched_messages, dict) else {"messages": patched_messages}
                return await planner.ainvoke(patched_invoke_args)
            else:
                raise

    async def _parse_with_chat_mode(self, messages: Union[Dict, List], pydantic_class: Type[T]) -> T:
        """使用聊天模式解析 (适用于不支持结构化输出的模型)"""
        self._prepare_llm_for_chat_mode()

        # 添加schema提示
        schema_prompt = self._generate_schema_prompt(pydantic_class)

        if messages and isinstance(messages[-1], HumanMessage):
            schema_msg = HumanMessage(
                content=messages[-1].content+schema_prompt)
        else:
            schema_msg = HumanMessage(content=schema_prompt)

        last_error = None

        for attempt in range(self.max_retries):
            try:
                response = await self.llm.ainvoke([schema_msg])
                response_text = getattr(response, 'content', str(response))
                logger.debug(
                    f"聊天模式尝试 {attempt + 1}: LLM响应: {response_text[:200]}...")

                result = self._repair_and_parse_json(
                    response_text, pydantic_class)
                if result is not None:
                    logger.info(f"成功解析为 {pydantic_class.__name__} 实例")
                    return result

                # 如果不是最后一次尝试，添加错误提示
                if attempt < self.max_retries - 1:
                    error_msg = f"""
上次的JSON格式不正确或不符合要求的schema。请重新生成，确保:
1. 返回有效的JSON格式
2. 包含所有必填字段
3. 字段类型正确
4. 只返回JSON内容，不要其他文字

之前的响应: {response_text[:200]}...
"""
                    messages.append(AIMessage(content=error_msg))

            except Exception as e:
                last_error = e
                logger.error(f"聊天模式尝试 {attempt + 1} 失败: {e}")
                if attempt < self.max_retries - 1:
                    error_msg = f"发生错误: {str(e)}。请重新生成正确的JSON格式。"
                    msg_list.append(HumanMessage(content=error_msg))

        # 所有尝试都失败了
        error_message = f"经过 {self.max_retries} 次尝试，无法解析为 {pydantic_class.__name__} 实例"
        if last_error:
            error_message += f"。最后一个错误: {last_error}"
        raise ValueError(error_message)

    async def parse_with_structured_output(self, prompt, messages: Union[Dict, List],
                                           pydantic_class: Type[T]) -> T:
        """
        根据模型类型选择合适的结构化输出解析方法

        Args:
            prompt: LangChain prompt模板
            messages: 消息内容 (dict或list格式)
            pydantic_class: 目标Pydantic模型类

        Returns:
            T: 解析后的Pydantic模型实例
        """
        if self.model_type == ModelType.GPT:
            # GPT模型使用原生结构化输出
            try:
                logger.debug("使用GPT原生结构化输出模式")
                return await self._parse_with_native_structured_output(prompt, messages, pydantic_class)
            except Exception as e:
                logger.warning(f"GPT结构化输出失败，降级到聊天模式: {e}")
                return await self._parse_with_chat_mode(messages, pydantic_class)
        else:
            # 其他模型 (包括Qwen) 直接使用聊天模式
            logger.debug(f"使用聊天模式处理 {self.model_type} 模型")
            return await self._parse_with_chat_mode(messages, pydantic_class)


class ToolsNodes(BasicNode):
    def __init__(self) -> None:
        self.tools = []
        self.mcp_client = None
        self.mcp_config = {}
        self.tools_prompt_tokens = 0
        self.tools_completions_tokens = 0

    async def call_with_structured_output(self, llm, prompt, pydantic_model,
                                          messages: Union[Dict, List], max_retries: int = 3):
        """
        通用结构化输出调用方法

        Args:
            llm: LangChain LLM实例
            prompt: LangChain prompt模板
            pydantic_model: 目标Pydantic模型类
            messages: 消息内容 (dict或list格式)
            max_retries: 最大重试次数

        Returns:
            解析后的Pydantic模型实例
        """
        parser = StructuredOutputParser(llm, max_retries=max_retries)
        return await parser.parse_with_structured_output(prompt, messages, pydantic_model)

    async def setup(self, request: BaseModel):
        """初始化工具节点"""
        # 初始化MCP客户端配置
        for server in request.tools_servers:
            if not server.url.startswith("langchain:"):
                self.mcp_config[server.name] = {
                    "url": server.url,
                    "transport": 'sse'
                }

        if self.mcp_config:
            self.mcp_client = MultiServerMCPClient(self.mcp_config)
            self.tools = await self.mcp_client.get_tools()

        # 初始化LangChain工具
        for server in request.tools_servers:
            if server.url.startswith("langchain:"):
                langchain_tools = ToolsLoader.load_tools(server)
                self.tools.extend(langchain_tools)

    async def build_tools_node(self) -> ToolNode:
        """构建工具节点"""
        try:
            if self.tools:
                tool_node = ToolNode(self.tools, handle_tool_errors=True)
                logger.info(f"成功构建工具节点，包含 {len(self.tools)} 个工具")
                return tool_node
            else:
                logger.info("未找到可用工具，返回空工具节点")
                return ToolNode([])
        except Exception as e:
            logger.error(f"构建工具节点失败: {e}")
            return ToolNode([])

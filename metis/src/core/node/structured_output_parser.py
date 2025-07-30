import json
from langchain_core.messages import HumanMessage
import json_repair
from typing import Type, TypeVar, Dict, List, Union
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

        # GPT模型检测
        if any(keyword in model_name for keyword in ['gpt', 'openai']):
            return ModelType.GPT

        # Qwen模型检测
        if any(keyword in model_name for keyword in ['qwen', 'tongyi']):
            return ModelType.QWEN

        return ModelType.OTHER


class StructuredOutputParser:
    """结构化输出解析器 - 支持多种模型类型"""

    def __init__(self, llm, max_retries: int = 3):
        self.llm = llm
        self.max_retries = max_retries
        self.model_type = ModelDetector.detect_model_type(llm)
        if self.model_type == ModelType.QWEN:
            if llm.extra_body is None:
                llm.extra_body = {}
            llm.extra_body["enable_thinking"] = False

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
            planner = prompt | self.llm.with_structured_output(
                pydantic_class)

            # 准备调用参数
            invoke_args = messages if isinstance(messages, dict) else {
                "messages": messages}
            result = await planner.ainvoke(invoke_args)
            return result

        else:
            schema_prompt = self._generate_schema_prompt(pydantic_class)
            schema_msg = HumanMessage(content=schema_prompt)
            response = await self.llm.ainvoke([schema_msg])
            response_text = response.content
            data = json_repair.loads(response_text)
            # 转换为 pydantic_class 类型实例
            return pydantic_class.model_validate(data)

import json
import copy
from typing import Type, TypeVar, Dict, List, Union

import json_repair
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from sanic.log import logger

from src.core.sanic_plus.utils.template_loader import TemplateLoader

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
        检测LLM模型类型

        Args:
            llm: LangChain LLM实例

        Returns:
            str: 模型类型 (gpt/qwen/other)
        """
        model_name = getattr(llm, 'model_name', '').lower()
        logger.info(f"检测到模型名称: {model_name}")

        # GPT模型检测
        if any(keyword in model_name for keyword in ['gpt', 'openai']):
            logger.info("检测到GPT模型类型")
            return ModelType.GPT

        # Qwen模型检测
        if any(keyword in model_name for keyword in ['qwen', 'tongyi']):
            logger.info("检测到Qwen模型类型")
            return ModelType.QWEN

        logger.info("检测到其他模型类型")
        return ModelType.OTHER


class PromptBuilder:
    """结构化输出的Prompt构建器"""

    def __init__(self):
        self.template_loader = TemplateLoader()

    def build_schema_prompt(self, pydantic_class: Type[T]) -> str:
        """
        构建包含Pydantic模型schema的提示

        Args:
            pydantic_class: Pydantic模型类

        Returns:
            str: 格式化的schema提示
        """
        try:
            schema = pydantic_class.model_json_schema()
            
            # 构建字段信息
            fields = {}
            if 'properties' in schema:
                required_fields = set(schema.get('required', []))
                for field_name, field_info in schema['properties'].items():
                    fields[field_name] = {
                        'type': field_info.get('type', 'unknown'),
                        'description': field_info.get('description', '无描述'),
                        'required': field_name in required_fields
                    }

            template_data = {
                'model_name': pydantic_class.__name__,
                'description': schema.get('description'),
                'schema_json': json.dumps(schema, indent=2, ensure_ascii=False),
                'fields': fields
            }

            prompt = self.template_loader.render_template('prompts/graph/structured_output_schema', template_data)
            logger.debug(f"生成schema提示，模型: {pydantic_class.__name__}")
            return prompt

        except Exception as e:
            logger.error(f"构建schema提示失败: {e}, 模型: {pydantic_class.__name__}")
            raise

    def add_json_format_prompt(self) -> str:
        """获取JSON格式提示"""
        return self.template_loader.render_template('prompts/graph/json_format_prompt')


class StructuredOutputParser:
    """结构化输出解析器 - 支持多种模型类型"""

    def __init__(self, llm, max_retries: int = 3):
        """
        初始化结构化输出解析器

        Args:
            llm: LangChain LLM实例
            max_retries: 最大重试次数
        """
        self.llm = llm
        self.max_retries = max_retries
        self.model_type = ModelDetector.detect_model_type(llm)
        self.prompt_builder = PromptBuilder()
        
        # 为Qwen模型禁用thinking模式
        if self.model_type == ModelType.QWEN:
            self._configure_qwen_model()

        logger.info(f"初始化结构化输出解析器，模型类型: {self.model_type}")

    def _configure_qwen_model(self):
        """配置Qwen模型特定设置"""
        if self.llm.extra_body is None:
            self.llm.extra_body = {}
        self.llm.extra_body["enable_thinking"] = False
        logger.debug("为Qwen模型禁用thinking模式")

    def _add_json_prompt_if_needed(self, messages: Union[Dict, List], content_key: str = "input") -> Union[Dict, List]:
        """
        如果需要，添加JSON提示到消息中

        Args:
            messages: 消息内容
            content_key: 内容键名

        Returns:
            添加提示后的消息
        """
        patched_messages = copy.deepcopy(messages)
        json_prompt = self.prompt_builder.add_json_format_prompt()

        try:
            if isinstance(patched_messages, dict):
                self._patch_dict_messages(patched_messages, json_prompt, content_key)
            elif isinstance(patched_messages, list) and patched_messages:
                self._patch_list_messages(patched_messages, json_prompt)
                
            logger.debug("成功添加JSON格式提示")
        except Exception as e:
            logger.warning(f"添加JSON提示失败: {e}")

        return patched_messages

    def _patch_dict_messages(self, messages: Dict, json_prompt: str, content_key: str):
        """为字典格式消息添加JSON提示"""
        if content_key in messages and "json" not in messages[content_key]:
            messages[content_key] += json_prompt
        elif "messages" in messages and isinstance(messages["messages"], list):
            if (messages["messages"] and
                hasattr(messages["messages"][-1], "content") and
                    "json" not in messages["messages"][-1].content):
                messages["messages"][-1].content += json_prompt

    def _patch_list_messages(self, messages: List, json_prompt: str):
        """为列表格式消息添加JSON提示"""
        if (hasattr(messages[-1], "content") and
                "json" not in messages[-1].content):
            messages[-1].content += json_prompt

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

        Raises:
            ValueError: 解析失败时抛出
        """
        logger.info(f"开始结构化输出解析，目标类型: {pydantic_class.__name__}")
        
        try:
            if self.model_type == ModelType.GPT:
                return await self._parse_with_gpt(prompt, messages, pydantic_class)
            else:
                return await self._parse_with_schema(pydantic_class)
        except Exception as e:
            logger.error(f"结构化输出解析失败: {e}, 目标类型: {pydantic_class.__name__}")
            raise ValueError(f"解析结构化输出失败: {e}")

    async def _parse_with_gpt(self, prompt, messages: Union[Dict, List], 
                             pydantic_class: Type[T]) -> T:
        """使用GPT的原生结构化输出功能"""
        planner = prompt | self.llm.with_structured_output(pydantic_class)
        
        # 准备调用参数
        invoke_args = messages if isinstance(messages, dict) else {"messages": messages}
        result = await planner.ainvoke(invoke_args)
        
        logger.info(f"GPT结构化输出解析成功，类型: {pydantic_class.__name__}")
        return result

    async def _parse_with_schema(self, pydantic_class: Type[T]) -> T:
        """使用schema提示进行解析"""
        schema_prompt = self.prompt_builder.build_schema_prompt(pydantic_class)
        schema_msg = HumanMessage(content=schema_prompt)
        
        response = await self.llm.ainvoke([schema_msg])
        response_text = response.content
        
        # 解析JSON响应
        try:
            data = json_repair.loads(response_text)
            result = pydantic_class.model_validate(data)
            logger.info(f"Schema解析成功，类型: {pydantic_class.__name__}")
            return result
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"JSON解析失败: {e}, 响应内容: {response_text[:200]}...")
            raise ValueError(f"JSON解析失败: {e}")

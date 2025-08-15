"""
测试结构化输出解析器的重构代码
"""
import pytest
from unittest.mock import Mock, AsyncMock
from pydantic import BaseModel, Field

from src.core.node.structured_output_parser import (
    ModelType,
    ModelDetector,
    PromptBuilder,
    StructuredOutputParser
)


class TestModel(BaseModel):
    """测试用的Pydantic模型"""
    name: str = Field(description="姓名")
    age: int = Field(description="年龄", ge=0)
    email: str = Field(description="邮箱地址", default="")


class TestModelDetector:
    """测试模型检测器"""

    def test_detect_gpt_model(self):
        """测试GPT模型检测"""
        llm = Mock()
        llm.model_name = "gpt-3.5-turbo"
        
        result = ModelDetector.detect_model_type(llm)
        assert result == ModelType.GPT

    def test_detect_qwen_model(self):
        """测试Qwen模型检测"""
        llm = Mock()
        llm.model_name = "qwen-turbo"
        
        result = ModelDetector.detect_model_type(llm)
        assert result == ModelType.QWEN

    def test_detect_other_model(self):
        """测试其他模型检测"""
        llm = Mock()
        llm.model_name = "llama-2"
        
        result = ModelDetector.detect_model_type(llm)
        assert result == ModelType.OTHER


class TestPromptBuilder:
    """测试Prompt构建器"""

    def test_build_schema_prompt(self):
        """测试schema提示构建"""
        builder = PromptBuilder()
        prompt = builder.build_schema_prompt(TestModel)
        
        assert "TestModel" in prompt
        assert "name" in prompt
        assert "age" in prompt
        assert "email" in prompt
        assert "JSON格式" in prompt

    def test_add_json_format_prompt(self):
        """测试JSON格式提示"""
        builder = PromptBuilder()
        prompt = builder.add_json_format_prompt()
        
        assert "JSON格式" in prompt


class TestStructuredOutputParser:
    """测试结构化输出解析器"""

    @pytest.fixture
    def mock_gpt_llm(self):
        """模拟GPT LLM"""
        llm = Mock()
        llm.model_name = "gpt-3.5-turbo"
        llm.with_structured_output = Mock()
        return llm

    @pytest.fixture
    def mock_qwen_llm(self):
        """模拟Qwen LLM"""
        llm = Mock()
        llm.model_name = "qwen-turbo"
        llm.extra_body = None
        llm.ainvoke = AsyncMock()
        return llm

    def test_init_with_gpt(self, mock_gpt_llm):
        """测试使用GPT初始化"""
        parser = StructuredOutputParser(mock_gpt_llm)
        
        assert parser.model_type == ModelType.GPT
        assert parser.llm == mock_gpt_llm

    def test_init_with_qwen(self, mock_qwen_llm):
        """测试使用Qwen初始化"""
        parser = StructuredOutputParser(mock_qwen_llm)
        
        assert parser.model_type == ModelType.QWEN
        assert mock_qwen_llm.extra_body["enable_thinking"] is False

    def test_patch_dict_messages(self, mock_gpt_llm):
        """测试字典消息补丁"""
        parser = StructuredOutputParser(mock_gpt_llm)
        messages = {"input": "test message"}
        
        result = parser._add_json_prompt_if_needed(messages)
        
        assert "JSON格式" in result["input"]

    def test_patch_list_messages(self, mock_gpt_llm):
        """测试列表消息补丁"""
        parser = StructuredOutputParser(mock_gpt_llm)
        
        mock_message = Mock()
        mock_message.content = "test message"
        messages = [mock_message]
        
        result = parser._add_json_prompt_if_needed(messages)
        
        assert "JSON格式" in result[0].content


if __name__ == "__main__":
    pytest.main([__file__])

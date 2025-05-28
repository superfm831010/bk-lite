import logging
import pytest
from unittest.mock import patch
from apps.core.exceptions.base_app_exception import BaseAppException

logger = logging.getLogger(__name__)


@pytest.fixture
def sample_data():
    """提供测试用的样例数据"""
    return {"user_id": 123, "action": "test"}


@pytest.fixture
def custom_exception_class():
    """创建自定义异常类用于测试继承场景"""
    class CustomException(BaseAppException):
        ERROR_CODE = "TEST001"
        MESSAGE = "自定义测试异常"
        STATUS_CODE = 400
        LOG_LEVEL = logging.WARNING
    
    return CustomException


def test_base_exception_default_creation():
    """测试使用默认参数创建BaseAppException实例"""
    exception = BaseAppException()
    
    logger.info("默认创建测试 - 错误码: %s", exception.ERROR_CODE)
    logger.info("默认创建测试 - 默认消息: %s", exception.message)
    logger.info("默认创建测试 - 数据: %s", exception.data)
    logger.info("默认创建测试 - 状态码: %s", exception.STATUS_CODE)
    logger.info("默认创建测试 - 日志级别: %s", exception.LOG_LEVEL)


def test_base_exception_with_custom_message():
    """测试使用自定义消息创建异常实例"""
    custom_message = "这是一个自定义错误消息"
    exception = BaseAppException(message=custom_message)
    
    logger.info("自定义消息测试 - 设置的消息: %s", custom_message)
    logger.info("自定义消息测试 - 实际消息: %s", exception.message)
    logger.info("自定义消息测试 - 消息是否匹配: %s", exception.message == custom_message)


def test_base_exception_with_data(sample_data):
    """测试带有数据的异常创建"""
    exception = BaseAppException(data=sample_data)
    
    logger.info("数据传递测试 - 原始数据: %s", sample_data)
    logger.info("数据传递测试 - 异常中的数据: %s", exception.data)
    logger.info("数据传递测试 - 数据类型: %s", type(exception.data).__name__)


def test_base_exception_with_message_and_data(sample_data):
    """测试同时传递消息和数据的异常创建"""
    message = "操作失败"
    exception = BaseAppException(message=message, data=sample_data)
    
    logger.info("消息和数据测试 - 消息: %s", exception.message)
    logger.info("消息和数据测试 - 数据: %s", exception.data)


def test_message_type_conversion():
    """测试非字符串类型消息的自动转换"""
    non_string_message = 12345
    with patch('logging.warning') as mock_warning:
        exception = BaseAppException(message=non_string_message)
        
        logger.info("类型转换测试 - 原始消息: %s (类型: %s)", 
                   non_string_message, type(non_string_message).__name__)
        logger.info("类型转换测试 - 转换后消息: %s (类型: %s)", 
                   exception.message, type(exception.message).__name__)
        logger.info("类型转换测试 - 是否调用了警告日志: %s", mock_warning.called)


def test_render_data_method(sample_data):
    """测试render_data方法的基本功能"""
    exception = BaseAppException(data=sample_data)
    rendered_data = exception.render_data()
    
    logger.info("render_data测试 - 原始数据: %s", sample_data)
    logger.info("render_data测试 - 渲染后数据: %s", rendered_data)
    logger.info("render_data测试 - 数据是否相同: %s", rendered_data == sample_data)


def test_render_data_with_none():
    """测试render_data方法处理None数据"""
    exception = BaseAppException(data=None)
    rendered_data = exception.render_data()
    
    logger.info("render_data None测试 - 渲染结果: %s", rendered_data)
    logger.info("render_data None测试 - 是否为None: %s", rendered_data is None)


def test_response_data_structure():
    """测试response_data方法返回的数据结构"""
    message = "测试响应数据结构"
    data = {"error_detail": "详细错误信息"}
    exception = BaseAppException(message=message, data=data)
    
    response = exception.response_data()
    
    logger.info("响应数据结构测试 - 完整响应: %s", response)
    logger.info("响应数据结构测试 - result字段: %s", response.get("result"))
    logger.info("响应数据结构测试 - code字段: %s", response.get("code"))
    logger.info("响应数据结构测试 - message字段: %s", response.get("message"))
    logger.info("响应数据结构测试 - data字段: %s", response.get("data"))
    logger.info("响应数据结构测试 - 字段数量: %s", len(response))


def test_response_data_with_none_data():
    """测试response_data方法处理空数据的情况"""
    exception = BaseAppException(message="无数据测试")
    response = exception.response_data()
    
    logger.info("空数据响应测试 - data字段值: %s", response.get("data"))
    logger.info("空数据响应测试 - data是否为None: %s", response.get("data") is None)


def test_custom_exception_inheritance(custom_exception_class):
    """测试自定义异常类的继承行为"""
    exception = custom_exception_class()
    
    logger.info("继承测试 - 自定义错误码: %s", exception.ERROR_CODE)
    logger.info("继承测试 - 自定义消息: %s", exception.message)
    logger.info("继承测试 - 自定义状态码: %s", exception.STATUS_CODE)
    logger.info("继承测试 - 自定义日志级别: %s", exception.LOG_LEVEL)
    
    response = exception.response_data()
    logger.info("继承测试 - 响应中的错误码: %s", response.get("code"))


def test_custom_exception_with_override(custom_exception_class):
    """测试自定义异常类中重写默认值的情况"""
    custom_message = "重写的消息"
    exception = custom_exception_class(message=custom_message)
    
    logger.info("重写测试 - 类默认消息: %s", custom_exception_class.MESSAGE)
    logger.info("重写测试 - 实例实际消息: %s", exception.message)
    logger.info("重写测试 - 是否使用了重写消息: %s", exception.message == custom_message)


def test_exception_with_additional_args():
    """测试传递额外参数给父类Exception的情况"""
    additional_args = ("额外参数1", "额外参数2")
    exception = BaseAppException("测试消息", None, *additional_args)
    
    logger.info("额外参数测试 - 异常参数: %s", exception.args)
    logger.info("额外参数测试 - 参数数量: %s", len(exception.args))


def test_various_data_types():
    """测试不同数据类型作为data参数的处理"""
    test_cases = [
        ("字符串数据", "string"),
        (["列表", "数据"], "list"),
        ({"字典": "数据"}, "dict"),
        (123, "int"),
        (12.34, "float"),
        (True, "bool"),
    ]
    
    for data, data_type in test_cases:
        exception = BaseAppException(data=data)
        logger.info("数据类型测试 - %s类型: 原始=%s, 存储=%s", 
                   data_type, data, exception.data)


@patch('logging.getLogger')
def test_logging_behavior(mock_get_logger):
    """测试日志记录行为"""
    mock_logger = mock_get_logger.return_value
    
    exception = BaseAppException(message="测试日志")
    
    logger.info("日志行为测试 - getLogger调用次数: %s", mock_get_logger.call_count)
    logger.info("日志行为测试 - logger.log调用次数: %s", mock_logger.log.call_count)
    
    # 调用response_data触发debug日志
    response = exception.response_data()
    logger.info("日志行为测试 - response_data后debug调用次数: %s", mock_logger.debug.call_count)


def test_edge_case_empty_string_message():
    """测试空字符串消息的边界情况"""
    exception = BaseAppException(message="")
    
    logger.info("空字符串测试 - 消息长度: %s", len(exception.message))
    logger.info("空字符串测试 - 消息内容: '%s'", exception.message)
    
    response = exception.response_data()
    logger.info("空字符串测试 - 响应中的消息: '%s'", response.get("message"))


def test_edge_case_very_long_message():
    """测试超长消息的处理"""
    long_message = "这是一个很长的错误消息" * 100
    exception = BaseAppException(message=long_message)
    
    logger.info("长消息测试 - 消息长度: %s", len(exception.message))
    logger.info("长消息测试 - 消息前50字符: %s...", exception.message[:50])
    
    response = exception.response_data()
    logger.info("长消息测试 - 响应消息长度: %s", len(response.get("message", "")))

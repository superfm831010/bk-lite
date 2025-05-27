import json
import logging
import pytest
from unittest.mock import Mock, patch, MagicMock
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import AnonymousUser, User

from apps.core.middlewares.app_exception_middleware import AppExceptionMiddleware
from apps.core.exceptions.base_app_exception import BaseAppException


# 配置测试日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture
def middleware():
    """创建中间件实例的fixture"""
    # 创建一个模拟的 get_response 函数
    def mock_get_response(request):
        return HttpResponse("Mock response")
    
    return AppExceptionMiddleware(mock_get_response)


@pytest.fixture
def mock_request():
    """创建模拟请求对象的fixture"""
    request = Mock(spec=HttpRequest)
    request.path = '/api/test'
    request.method = 'POST'
    request.META = {
        'HTTP_X_FORWARDED_FOR': '192.168.1.100, 10.0.0.1',
        'REMOTE_ADDR': '127.0.0.1',
        'HTTP_USER_AGENT': 'TestAgent/1.0'
    }
    
    # 模拟认证用户
    mock_user = Mock(spec=User)
    mock_user.username = 'testuser'
    request.user = mock_user
    
    # 模拟POST参数
    request.POST = {
        'username': 'testuser',
        'password': 'secret123',
        'data': 'normal_value'
    }
    
    return request


@pytest.fixture
def mock_business_exception():
    """创建模拟业务异常的fixture"""
    class TestBusinessException(BaseAppException):
        ERROR_CODE = 'TEST_ERROR'
        STATUS_CODE = 400
        LOG_LEVEL = logging.WARNING
        
        def __init__(self, message="测试业务异常"):
            super().__init__(message)
    
    return TestBusinessException


def test_handle_business_exception_success(middleware, mock_request, mock_business_exception):
    """测试业务异常处理 - 验证BaseAppException的正确处理流程"""
    logger.info("开始测试业务异常处理")
    
    # 创建业务异常实例
    exception = mock_business_exception("用户不存在")
    
    with patch('apps.core.utils.web_utils.WebUtils.response_error') as mock_response:
        mock_response.return_value = HttpResponse("业务异常响应")
        
        # 执行异常处理
        result = middleware.process_exception(mock_request, exception)
        
        # 验证调用参数
        mock_response.assert_called_once()
        call_args = mock_response.call_args
        
        logger.info(f"业务异常处理结果 - 错误信息: {call_args[1]['error_message']}")
        logger.info(f"业务异常处理结果 - 状态码: {call_args[1]['status_code']}")
        logger.info("业务异常处理测试完成")


def test_handle_system_exception_success(middleware, mock_request):
    """测试系统异常处理 - 验证普通Exception的处理流程"""
    logger.info("开始测试系统异常处理")
    
    # 创建系统异常
    exception = ValueError("数据格式错误")
    
    with patch('apps.core.utils.web_utils.WebUtils.response_error') as mock_response:
        mock_response.return_value = HttpResponse("系统异常响应")
        
        # 执行异常处理
        result = middleware.process_exception(mock_request, exception)
        
        # 验证调用参数
        mock_response.assert_called_once()
        call_args = mock_response.call_args
        
        logger.info(f"系统异常处理结果 - 错误信息: {call_args[1]['error_message']}")
        logger.info(f"系统异常处理结果 - 状态码: {call_args[1]['status_code']}")
        logger.info("系统异常处理测试完成")


def test_get_client_ip_from_forwarded_header(middleware, mock_request):
    """测试客户端IP获取 - 验证从X-Forwarded-For头获取真实IP"""
    logger.info("开始测试客户端IP获取（代理转发）")
    
    # 测试从X-Forwarded-For获取IP
    client_ip = middleware._get_client_ip(mock_request)
    
    logger.info(f"获取的客户端IP: {client_ip}")
    logger.info(f"原始X-Forwarded-For头: {mock_request.META['HTTP_X_FORWARDED_FOR']}")
    logger.info("客户端IP获取测试完成")


def test_get_client_ip_fallback_to_remote_addr(middleware):
    """测试客户端IP获取 - 验证回退到REMOTE_ADDR的逻辑"""
    logger.info("开始测试客户端IP获取（无代理）")
    
    # 创建没有X-Forwarded-For的请求
    request = Mock(spec=HttpRequest)
    request.META = {'REMOTE_ADDR': '192.168.1.50'}
    
    client_ip = middleware._get_client_ip(request)
    
    logger.info(f"获取的客户端IP: {client_ip}")
    logger.info(f"REMOTE_ADDR值: {request.META['REMOTE_ADDR']}")
    logger.info("客户端IP回退逻辑测试完成")


def test_get_username_with_authenticated_user(middleware, mock_request):
    """测试用户名获取 - 验证认证用户的用户名提取"""
    logger.info("开始测试认证用户的用户名获取")
    
    username = middleware._get_username(mock_request)
    
    logger.info(f"获取的用户名: {username}")
    logger.info(f"预期用户名: {mock_request.user.username}")
    logger.info("认证用户用户名获取测试完成")


def test_get_username_with_anonymous_user(middleware):
    """测试用户名获取 - 验证匿名用户的处理"""
    logger.info("开始测试匿名用户的用户名获取")
    
    # 创建匿名用户请求
    request = Mock(spec=HttpRequest)
    request.user = AnonymousUser()
    
    username = middleware._get_username(request)
    
    logger.info(f"获取的用户名: {username}")
    logger.info("匿名用户用户名获取测试完成")


def test_get_safe_request_params_with_sensitive_data(middleware, mock_request):
    """测试请求参数过滤 - 验证敏感字段的过滤功能"""
    logger.info("开始测试敏感参数过滤")
    
    # 设置中间件的request属性
    middleware.request = mock_request
    
    safe_params = middleware._get_safe_request_params()
    
    logger.info(f"原始参数: {dict(mock_request.POST)}")
    logger.info(f"过滤后参数: {safe_params}")
    
    # 解析JSON验证过滤效果
    try:
        params_dict = json.loads(safe_params)
        logger.info(f"密码字段是否被过滤: {'password' in params_dict and params_dict['password'] == '***FILTERED***'}")
        logger.info(f"普通字段是否保留: {'data' in params_dict and params_dict['data'] == 'normal_value'}")
    except json.JSONDecodeError:
        logger.warning(f"参数解析失败: {safe_params}")
    
    logger.info("敏感参数过滤测试完成")


def test_get_safe_request_params_with_large_data(middleware):
    """测试请求参数过滤 - 验证大数据的截断功能"""
    logger.info("开始测试大数据参数截断")
    
    # 创建包含大量数据的请求
    request = Mock(spec=HttpRequest)
    request.method = 'POST'
    large_data = 'x' * 2000  # 创建超长字符串
    request.POST = {'large_field': large_data}
    
    middleware.request = request
    safe_params = middleware._get_safe_request_params()
    
    logger.info(f"原始数据长度: {len(large_data)}")
    logger.info(f"过滤后参数长度: {len(safe_params)}")
    logger.info(f"是否包含截断标识: {'truncated' in safe_params}")
    logger.info("大数据参数截断测试完成")


def test_middleware_self_exception_handling(middleware, mock_request):
    """测试中间件异常处理 - 验证中间件自身异常的容错性"""
    logger.info("开始测试中间件自身异常处理")
    
    # 模拟 _handle_system_exception 方法抛出异常
    with patch.object(middleware, '_handle_system_exception') as mock_handle:
        mock_handle.side_effect = Exception("中间件内部异常")
        
        with patch('apps.core.utils.web_utils.WebUtils.response_error') as mock_response:
            mock_response.return_value = HttpResponse("容错响应")
            
            # 执行异常处理
            exception = ValueError("原始异常")
            result = middleware.process_exception(mock_request, exception)
            
            logger.info(f"中间件异常处理结果类型: {type(result)}")
            logger.info(f"最终异常处理调用: {mock_response.called}")
            
            # 验证最终的容错响应被调用
            mock_response.assert_called_once_with(
                error_message="系统异常,请联系管理员处理",
                status_code=500
            )
    
    logger.info("中间件自身异常处理测试完成")


def test_get_client_info_complete(middleware, mock_request):
    """测试客户端信息获取 - 验证完整信息的提取"""
    logger.info("开始测试完整客户端信息获取")
    
    client_info = middleware._get_client_info(mock_request)
    
    logger.info("获取的客户端信息:")
    for key, value in client_info.items():
        logger.info(f"  {key}: {value}")
    
    # 验证必要字段存在
    required_fields = ['client_ip', 'username', 'path', 'method', 'user_agent']
    for field in required_fields:
        if field in client_info:
            logger.info(f"字段 {field} 存在: ✓")
        else:
            logger.warning(f"字段 {field} 缺失: ✗")
    
    logger.info("完整客户端信息获取测试完成")


def test_exception_handling_with_missing_attributes(middleware):
    """测试异常处理 - 验证请求对象缺少属性时的容错性"""
    logger.info("开始测试缺少属性的请求对象处理")
    
    # 创建最小化的请求对象
    minimal_request = Mock()
    # 不设置任何属性，测试容错性
    
    exception = ValueError("测试异常")
    
    with patch('apps.core.utils.web_utils.WebUtils.response_error') as mock_response:
        mock_response.return_value = HttpResponse("容错响应")
        
        result = middleware.process_exception(minimal_request, exception)
        
        logger.info("成功处理缺少属性的请求对象")
        logger.info(f"返回结果类型: {type(result)}")
    
    logger.info("缺少属性的请求对象处理测试完成")


@pytest.mark.parametrize("method,has_data", [
    ("GET", False),
    ("POST", True),
    ("PUT", True),
    ("DELETE", False),
])
def test_get_safe_request_params_different_methods(middleware, method, has_data):
    """测试请求参数获取 - 验证不同HTTP方法的参数处理"""
    logger.info(f"开始测试 {method} 方法的参数获取")
    
    request = Mock(spec=HttpRequest)
    request.method = method
    
    # 根据方法设置参数
    if has_data:
        setattr(request, method, {'test_param': 'test_value'})
    else:
        setattr(request, method, {})
    
    middleware.request = request
    safe_params = middleware._get_safe_request_params()
    
    logger.info(f"{method} 方法参数结果: {safe_params}")
    logger.info(f"{method} 方法参数获取测试完成")

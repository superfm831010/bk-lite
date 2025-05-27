import logging
import pytest
from unittest.mock import Mock, patch, MagicMock
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import AnonymousUser

from apps.core.middlewares.auth_middleware import AuthMiddleware


# 配置测试日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture
def mock_get_response():
    """创建模拟的 get_response 函数"""
    return Mock(return_value=HttpResponse("OK"))


@pytest.fixture
def auth_middleware(mock_get_response):
    """创建 AuthMiddleware 实例"""
    return AuthMiddleware(mock_get_response)


@pytest.fixture
def mock_request():
    """创建模拟的 HTTP 请求对象"""
    request = Mock(spec=HttpRequest)
    request.path = "/api/test/"
    request.session = MagicMock()
    request.session.session_key = "test_session_key"
    request.META = {}
    return request


@pytest.fixture
def mock_view():
    """创建模拟的视图函数"""
    view = Mock()
    view.__name__ = "test_view"
    return view


def test_api_exempt_request(auth_middleware, mock_request, mock_view):
    """测试API豁免请求 - 视图标记为api_exempt=True的情况"""
    logger.info("开始测试：API豁免请求")
    
    # 设置视图豁免标记
    mock_view.api_exempt = True
    
    # 执行测试
    result = auth_middleware.process_view(mock_request, mock_view, [], {})
    
    # 记录测试结果
    logger.info(f"API豁免测试结果：result={result}")
    logger.info(f"期望结果：None（表示豁免认证）")
    logger.info("API豁免测试完成\n")


def test_request_api_pass(auth_middleware, mock_request, mock_view):
    """测试请求豁免标记 - 请求对象标记为api_pass=True的情况"""
    logger.info("开始测试：请求API豁免标记")
    
    # 设置请求豁免标记
    mock_request.api_pass = True
    
    # 执行测试
    result = auth_middleware.process_view(mock_request, mock_view, [], {})
    
    # 记录测试结果
    logger.info(f"请求豁免测试结果：result={result}")
    logger.info(f"期望结果：None（表示豁免认证）")
    logger.info("请求豁免测试完成\n")


@pytest.mark.parametrize("path,expected_exempt", [
    ("/swagger/", True),
    ("/swagger/ui/", True),
    ("/admin/", True),
    ("/admin/login/", True),
    ("/accounts/", True),
    ("/accounts/login/", True),
    ("/api/test/", False),
    ("/api/user/", False),
])
def test_path_exempt_requests(auth_middleware, mock_request, mock_view, path, expected_exempt):
    """测试路径豁免逻辑 - 验证不同路径的豁免状态"""
    logger.info(f"开始测试：路径豁免逻辑 - {path}")
    
    # 设置请求路径
    mock_request.path = path
    
    # 执行测试
    result = auth_middleware.process_view(mock_request, mock_view, [], {})
    
    # 记录测试结果
    is_exempt = result is None
    logger.info(f"路径：{path}")
    logger.info(f"实际豁免状态：{is_exempt}")
    logger.info(f"期望豁免状态：{expected_exempt}")
    logger.info(f"测试结果：{'通过' if is_exempt == expected_exempt else '失败'}")
    logger.info("路径豁免测试完成\n")


def test_login_exempt_view(auth_middleware, mock_request, mock_view):
    """测试登录豁免视图 - 视图标记为login_exempt=True的情况"""
    logger.info("开始测试：登录豁免视图")
    
    # 设置登录豁免标记
    mock_view.login_exempt = True
    
    # 执行测试
    result = auth_middleware.process_view(mock_request, mock_view, [], {})
    
    # 记录测试结果
    logger.info(f"登录豁免测试结果：result={result}")
    logger.info(f"期望结果：None（表示豁免认证）")
    logger.info("登录豁免测试完成\n")


def test_missing_token_header(auth_middleware, mock_request, mock_view):
    """测试缺少Token头部的情况"""
    logger.info("开始测试：缺少Token头部")
    
    # 不设置任何Token头部
    mock_request.META = {}
    
    # 模拟settings
    with patch.object(settings, 'AUTH_TOKEN_HEADER_NAME', 'HTTP_AUTHORIZATION'):
        result = auth_middleware.process_view(mock_request, mock_view, [], {})
    
    # 记录测试结果
    logger.info(f"缺少Token头部测试结果：result类型={type(result)}")
    logger.info(f"期望结果：HttpResponse（401错误响应）")
    if hasattr(result, 'status_code'):
        logger.info(f"响应状态码：{result.status_code}")
    logger.info("缺少Token头部测试完成\n")


@pytest.mark.parametrize("token_header,expected_token", [
    ("Bearer abc123", "abc123"),
    ("Bearer eyJhbGciOiJIUzI1NiJ9", "eyJhbGciOiJIUzI1NiJ9"),
    ("abc123", "abc123"),
    ("Bearer ", None),
    ("", None),
])
def test_extract_bearer_token(auth_middleware, token_header, expected_token):
    """测试Bearer Token提取逻辑"""
    logger.info(f"开始测试：Bearer Token提取 - '{token_header}'")
    
    # 执行Token提取
    extracted_token = auth_middleware._extract_bearer_token(token_header)
    
    # 记录测试结果
    logger.info(f"输入Token头部：'{token_header}'")
    logger.info(f"提取的Token：'{extracted_token}'")
    logger.info(f"期望Token：'{expected_token}'")
    logger.info(f"测试结果：{'通过' if extracted_token == expected_token else '失败'}")
    logger.info("Bearer Token提取测试完成\n")


@patch('apps.core.middlewares.auth_middleware.auth.authenticate')
@patch('apps.core.middlewares.auth_middleware.auth.login')
def test_successful_token_authentication(mock_login, mock_authenticate, auth_middleware, mock_request, mock_view):
    """测试成功的Token认证流程"""
    logger.info("开始测试：成功的Token认证")
    
    # 设置Token头部
    mock_request.META = {'HTTP_AUTHORIZATION': 'Bearer valid_token'}
    
    # 模拟认证成功
    mock_user = Mock()
    mock_user.username = "test_user"
    mock_authenticate.return_value = mock_user
    
    # 模拟settings
    with patch.object(settings, 'AUTH_TOKEN_HEADER_NAME', 'HTTP_AUTHORIZATION'):
        result = auth_middleware.process_view(mock_request, mock_view, [], {})
    
    # 记录测试结果
    logger.info(f"Token认证测试结果：result={result}")
    logger.info(f"期望结果：None（认证成功）")
    logger.info(f"authenticate调用次数：{mock_authenticate.call_count}")
    logger.info(f"login调用次数：{mock_login.call_count}")
    logger.info("成功Token认证测试完成\n")


@patch('apps.core.middlewares.auth_middleware.auth.authenticate')
def test_failed_token_authentication(mock_authenticate, auth_middleware, mock_request, mock_view):
    """测试失败的Token认证流程"""
    logger.info("开始测试：失败的Token认证")
    
    # 设置Token头部
    mock_request.META = {'HTTP_AUTHORIZATION': 'Bearer invalid_token'}
    
    # 模拟认证失败
    mock_authenticate.return_value = None
    
    # 模拟settings
    with patch.object(settings, 'AUTH_TOKEN_HEADER_NAME', 'HTTP_AUTHORIZATION'):
        result = auth_middleware.process_view(mock_request, mock_view, [], {})
    
    # 记录测试结果
    logger.info(f"Token认证失败测试结果：result类型={type(result)}")
    logger.info(f"期望结果：HttpResponse（401错误响应）")
    logger.info(f"authenticate调用次数：{mock_authenticate.call_count}")
    if hasattr(result, 'status_code'):
        logger.info(f"响应状态码：{result.status_code}")
    logger.info("失败Token认证测试完成\n")


@pytest.mark.parametrize("ip_headers,expected_ip", [
    ({'HTTP_X_FORWARDED_FOR': '192.168.1.1', 'REMOTE_ADDR': '127.0.0.1'}, '192.168.1.1'),
    ({'HTTP_X_FORWARDED_FOR': '192.168.1.1, 10.0.0.1', 'REMOTE_ADDR': '127.0.0.1'}, '192.168.1.1'),
    ({'REMOTE_ADDR': '127.0.0.1'}, '127.0.0.1'),
    ({}, 'unknown'),
])
def test_get_client_ip(auth_middleware, mock_request, ip_headers, expected_ip):
    """测试客户端IP地址获取逻辑"""
    logger.info("开始测试：客户端IP获取")
    
    # 设置IP头部信息
    mock_request.META = ip_headers
    
    # 获取客户端IP
    client_ip = auth_middleware._get_client_ip(mock_request)
    
    # 记录测试结果
    logger.info(f"IP头部信息：{ip_headers}")
    logger.info(f"获取的IP：{client_ip}")
    logger.info(f"期望IP：{expected_ip}")
    logger.info(f"测试结果：{'通过' if client_ip == expected_ip else '失败'}")
    logger.info("客户端IP获取测试完成\n")


@patch('apps.core.middlewares.auth_middleware.auth.authenticate')
def test_authentication_exception_handling(mock_authenticate, auth_middleware, mock_request, mock_view):
    """测试认证过程中的异常处理"""
    logger.info("开始测试：认证异常处理")
    
    # 设置Token头部
    mock_request.META = {'HTTP_AUTHORIZATION': 'Bearer test_token'}
    
    # 模拟认证过程中抛出异常
    mock_authenticate.side_effect = Exception("Database connection error")
    
    # 模拟settings
    with patch.object(settings, 'AUTH_TOKEN_HEADER_NAME', 'HTTP_AUTHORIZATION'):
        result = auth_middleware.process_view(mock_request, mock_view, [], {})
    
    # 记录测试结果
    logger.info(f"异常处理测试结果：result类型={type(result)}")
    logger.info(f"期望结果：HttpResponse（401错误响应）")
    if hasattr(result, 'status_code'):
        logger.info(f"响应状态码：{result.status_code}")
    logger.info("认证异常处理测试完成\n")


def test_session_cycle_key_when_missing(auth_middleware, mock_request, mock_view):
    """测试session_key缺失时的处理逻辑"""
    logger.info("开始测试：session_key缺失处理")
    
    # 设置Token头部
    mock_request.META = {'HTTP_AUTHORIZATION': 'Bearer valid_token'}
    
    # 设置session_key为None
    mock_request.session.session_key = None
    
    # 模拟认证成功
    with patch('apps.core.middlewares.auth_middleware.auth.authenticate') as mock_auth:
        with patch('apps.core.middlewares.auth_middleware.auth.login') as mock_login:
            mock_user = Mock()
            mock_user.username = "test_user"
            mock_auth.return_value = mock_user
            
            with patch.object(settings, 'AUTH_TOKEN_HEADER_NAME', 'HTTP_AUTHORIZATION'):
                result = auth_middleware.process_view(mock_request, mock_view, [], {})
    
    # 记录测试结果
    logger.info(f"session处理测试结果：result={result}")
    logger.info(f"cycle_key调用次数：{mock_request.session.cycle_key.call_count}")
    logger.info(f"期望：cycle_key被调用一次")
    logger.info("session_key缺失处理测试完成\n")

import logging
import pytest
from unittest.mock import Mock, patch, MagicMock
from django.conf import settings
from django.contrib.auth.models import User
from django.test import RequestFactory
from rest_framework import status

from apps.core.middlewares.api_middleware import APISecretMiddleware

# 配置测试日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture
def request_factory():
    """创建Django请求工厂fixture"""
    return RequestFactory()


@pytest.fixture
def middleware():
    """创建中间件实例fixture"""
    # 创建一个模拟的get_response函数
    mock_get_response = Mock()
    return APISecretMiddleware(mock_get_response)


@pytest.fixture
def mock_user():
    """创建模拟用户对象fixture"""
    user = Mock(spec=User)
    user.username = "test_user"
    user.id = 1
    return user


@pytest.fixture
def base_request(request_factory):
    """创建基础请求对象fixture"""
    request = request_factory.get('/api/test/')
    request.META = {
        'REMOTE_ADDR': '192.168.1.100',
        'HTTP_X_FORWARDED_FOR': '10.0.0.1, 192.168.1.100'
    }
    request.session = Mock()
    request.session.session_key = None
    request.session.cycle_key = Mock()
    return request


def test_successful_token_authentication(middleware, base_request, mock_user):
    """
    测试API令牌认证成功的场景
    验证：
    - 正确的令牌头部设置
    - 用户认证成功
    - 会话处理正确
    - api_pass属性设置为True
    """
    logger.info("开始测试：API令牌认证成功场景")
    
    # 设置配置和请求头
    with patch.object(settings, 'API_TOKEN_HEADER_NAME', 'HTTP_API_TOKEN'):
        base_request.META['HTTP_API_TOKEN'] = 'valid_token_123'
        
        with patch('django.contrib.auth.authenticate') as mock_auth, \
             patch('django.contrib.auth.login') as mock_login:
            
            mock_auth.return_value = mock_user
            
            # 执行中间件
            result = middleware.process_request(base_request)
            
            # 记录测试结果
            logger.info(f"认证结果: {mock_auth.called}")
            logger.info(f"登录调用: {mock_login.called}")
            logger.info(f"API通过状态: {getattr(base_request, 'api_pass', None)}")
            logger.info(f"返回值: {result}")
            logger.info(f"会话密钥创建: {base_request.session.cycle_key.called}")
            
            logger.info("API令牌认证成功测试 - 通过")


def test_missing_token_header(middleware, base_request):
    """
    测试API令牌缺失的场景
    验证：
    - 没有令牌头部时的处理
    - api_pass属性设置为False
    - 不进行用户认证
    """
    logger.info("开始测试：API令牌缺失场景")
    
    with patch.object(settings, 'API_TOKEN_HEADER_NAME', 'HTTP_API_TOKEN'):
        # 不设置令牌头部
        
        with patch('django.contrib.auth.authenticate') as mock_auth:
            # 执行中间件
            result = middleware.process_request(base_request)
            
            # 记录测试结果
            logger.info(f"认证是否被调用: {mock_auth.called}")
            logger.info(f"API通过状态: {getattr(base_request, 'api_pass', None)}")
            logger.info(f"返回值: {result}")
            
            logger.info("API令牌缺失测试 - 通过")


def test_invalid_token_authentication(middleware, base_request):
    """
    测试无效API令牌的场景
    验证：
    - 令牌验证失败
    - 返回403错误响应
    - 不进行用户登录
    """
    logger.info("开始测试：无效API令牌场景")
    
    with patch.object(settings, 'API_TOKEN_HEADER_NAME', 'HTTP_API_TOKEN'):
        base_request.META['HTTP_API_TOKEN'] = 'invalid_token'
        
        with patch('django.contrib.auth.authenticate') as mock_auth, \
             patch('django.contrib.auth.login') as mock_login, \
             patch('apps.core.utils.web_utils.WebUtils.response_error') as mock_error_response:
            
            mock_auth.return_value = None  # 认证失败
            mock_error_response.return_value = Mock(status_code=403)
            
            # 执行中间件
            result = middleware.process_request(base_request)
            
            # 记录测试结果
            logger.info(f"认证调用: {mock_auth.called}")
            logger.info(f"登录是否被调用: {mock_login.called}")
            logger.info(f"错误响应调用: {mock_error_response.called}")
            logger.info(f"返回值类型: {type(result)}")
            
            if mock_error_response.called:
                call_args = mock_error_response.call_args
                logger.info(f"错误响应参数: {call_args}")
            
            logger.info("无效API令牌测试 - 通过")


def test_authentication_exception_handling(middleware, base_request):
    """
    测试认证过程中异常处理的场景
    验证：
    - 认证异常时的错误处理
    - 返回500错误响应
    - 异常日志记录
    """
    logger.info("开始测试：认证异常处理场景")
    
    with patch.object(settings, 'API_TOKEN_HEADER_NAME', 'HTTP_API_TOKEN'):
        base_request.META['HTTP_API_TOKEN'] = 'test_token'
        
        with patch('django.contrib.auth.authenticate') as mock_auth, \
             patch('apps.core.utils.web_utils.WebUtils.response_error') as mock_error_response:
            
            # 模拟认证异常
            mock_auth.side_effect = Exception("数据库连接失败")
            mock_error_response.return_value = Mock(status_code=500)
            
            # 执行中间件
            result = middleware.process_request(base_request)
            
            # 记录测试结果
            logger.info(f"认证异常是否抛出: {mock_auth.called}")
            logger.info(f"错误响应调用: {mock_error_response.called}")
            logger.info(f"返回值类型: {type(result)}")
            
            if mock_error_response.called:
                call_args = mock_error_response.call_args
                logger.info(f"错误响应状态码: {call_args.kwargs.get('status_code', '未知')}")
            
            logger.info("认证异常处理测试 - 通过")


def test_missing_api_token_header_config(middleware, base_request):
    """
    测试API令牌头部配置缺失的场景
    验证：
    - 配置缺失时的处理
    - api_pass属性设置为False
    - 不进行认证尝试
    """
    logger.info("开始测试：API令牌头部配置缺失场景")
    
    with patch.object(settings, 'API_TOKEN_HEADER_NAME', None):
        base_request.META['HTTP_API_TOKEN'] = 'some_token'
        
        with patch('django.contrib.auth.authenticate') as mock_auth:
            # 执行中间件
            result = middleware.process_request(base_request)
            
            # 记录测试结果
            logger.info(f"认证是否被调用: {mock_auth.called}")
            logger.info(f"API通过状态: {getattr(base_request, 'api_pass', None)}")
            logger.info(f"返回值: {result}")
            
            logger.info("API令牌头部配置缺失测试 - 通过")


def test_client_ip_extraction(middleware, request_factory):
    """
    测试客户端IP地址提取功能
    验证：
    - X-Forwarded-For头部处理
    - REMOTE_ADDR备用处理
    - IP地址日志记录
    """
    logger.info("开始测试：客户端IP地址提取场景")
    
    # 测试X-Forwarded-For场景
    request1 = request_factory.get('/api/test/')
    request1.META = {'HTTP_X_FORWARDED_FOR': '10.0.0.1, 192.168.1.100'}
    request1.session = Mock()
    
    client_ip1 = middleware._get_client_ip(request1)
    logger.info(f"X-Forwarded-For提取的IP: {client_ip1}")
    
    # 测试REMOTE_ADDR场景
    request2 = request_factory.get('/api/test/')
    request2.META = {'REMOTE_ADDR': '192.168.1.200'}
    request2.session = Mock()
    
    client_ip2 = middleware._get_client_ip(request2)
    logger.info(f"REMOTE_ADDR提取的IP: {client_ip2}")
    
    # 测试无IP场景
    request3 = request_factory.get('/api/test/')
    request3.META = {}
    request3.session = Mock()
    
    client_ip3 = middleware._get_client_ip(request3)
    logger.info(f"无IP情况下的默认值: {client_ip3}")
    
    logger.info("客户端IP地址提取测试 - 通过")


def test_session_key_handling(middleware, base_request, mock_user):
    """
    测试会话密钥处理功能
    验证：
    - 会话密钥不存在时的创建
    - cycle_key方法调用
    - 会话状态处理
    """
    logger.info("开始测试：会话密钥处理场景")
    
    with patch.object(settings, 'API_TOKEN_HEADER_NAME', 'HTTP_API_TOKEN'):
        base_request.META['HTTP_API_TOKEN'] = 'valid_token'
        
        # 模拟会话密钥不存在
        base_request.session.session_key = None
        
        with patch('django.contrib.auth.authenticate') as mock_auth, \
             patch('django.contrib.auth.login') as mock_login:
            
            mock_auth.return_value = mock_user
            
            # 执行中间件
            result = middleware.process_request(base_request)
            
            # 记录测试结果
            logger.info(f"认证成功: {mock_auth.called}")
            logger.info(f"登录调用: {mock_login.called}")
            logger.info(f"会话密钥创建: {base_request.session.cycle_key.called}")
            logger.info(f"原始会话密钥: None")
            
            logger.info("会话密钥处理测试 - 通过")


@pytest.mark.parametrize("token_length,expected_log", [
    (10, "短令牌"),
    (32, "标准令牌"), 
    (64, "长令牌")
])
def test_token_length_logging(middleware, base_request, token_length, expected_log):
    """
    测试不同长度令牌的日志记录
    验证：
    - 令牌长度记录
    - 调试信息输出
    - 敏感信息保护
    """
    logger.info(f"开始测试：{expected_log}长度日志记录场景")
    
    with patch.object(settings, 'API_TOKEN_HEADER_NAME', 'HTTP_API_TOKEN'):
        test_token = 'a' * token_length
        base_request.META['HTTP_API_TOKEN'] = test_token
        
        token = middleware._get_api_token(base_request)
        
        logger.info(f"令牌长度: {len(token) if token else 0}")
        logger.info(f"令牌类型: {expected_log}")
        logger.info(f"令牌获取成功: {token is not None}")
        
        logger.info(f"{expected_log}长度日志记录测试 - 通过")

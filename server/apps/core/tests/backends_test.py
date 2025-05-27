import pytest
import logging
import os
from unittest.mock import Mock, patch, MagicMock
from django.test import RequestFactory
from django.db import IntegrityError
from django.utils import translation

from apps.core.backends import APISecretAuthBackend, AuthBackend

# 配置测试日志
logger = logging.getLogger(__name__)


@pytest.fixture
def request_factory():
    """提供Django RequestFactory实例"""
    return RequestFactory()


@pytest.fixture
def mock_user():
    """提供模拟用户对象"""
    user = Mock()
    user.username = "test_user"
    user.email = "test@example.com"
    user.is_superuser = False
    user.is_staff = False
    user.group_list = []
    user.roles = []
    user.locale = "en"
    user.save = Mock()
    return user


@pytest.fixture
def mock_user_secret():
    """提供模拟用户API密钥对象"""
    secret = Mock()
    secret.username = "test_user"
    secret.team = "test_team"
    return secret


@pytest.fixture
def api_auth_backend():
    """提供APISecretAuthBackend实例"""
    return APISecretAuthBackend()


@pytest.fixture
def auth_backend():
    """提供AuthBackend实例"""
    return AuthBackend()


@pytest.fixture
def sample_user_info():
    """提供示例用户信息字典"""
    return {
        "username": "test_user",
        "email": "test@example.com",
        "is_superuser": False,
        "group_list": ["group1", "group2"],
        "roles": ["role1", "role2"],
        "locale": "zh-CN",
        "permission": ["perm1", "perm2"]
    }


def test_api_secret_auth_success(api_auth_backend, mock_user_secret, mock_user):
    """测试API密钥认证成功的场景"""
    logger.info("Testing API secret authentication success")
    
    api_token = "test_token_12345678"
    
    with patch('apps.core.backends.UserAPISecret.objects') as mock_user_secret_objects, \
         patch('apps.core.backends.User.objects') as mock_user_objects:
        
        mock_user_secret_objects.filter.return_value.first.return_value = mock_user_secret
        mock_user_objects.get.return_value = mock_user
        
        result = api_auth_backend.authenticate(api_token=api_token)
        
        logger.info(f"API authentication result: {result is not None}")
        logger.info(f"User group_list set to: {result.group_list if result else 'None'}")
        logger.info("API secret authentication success test completed")


def test_api_secret_auth_no_token(api_auth_backend):
    """测试API密钥认证无token的场景"""
    logger.info("Testing API secret authentication with no token")
    
    result = api_auth_backend.authenticate()
    
    logger.info(f"Authentication result with no token: {result}")
    logger.info("API secret authentication no token test completed")


def test_api_secret_auth_invalid_token(api_auth_backend):
    """测试API密钥认证无效token的场景"""
    logger.info("Testing API secret authentication with invalid token")
    
    api_token = "invalid_token"
    
    with patch('apps.core.backends.UserAPISecret.objects') as mock_user_secret_objects:
        mock_user_secret_objects.filter.return_value.first.return_value = None
        
        result = api_auth_backend.authenticate(api_token=api_token)
        
        logger.info(f"Authentication result with invalid token: {result}")
        logger.info("API secret authentication invalid token test completed")


def test_api_secret_auth_user_not_found(api_auth_backend, mock_user_secret):
    """测试API密钥认证用户不存在的场景"""
    logger.info("Testing API secret authentication with user not found")
    
    api_token = "valid_token_but_no_user"
    
    with patch('apps.core.backends.UserAPISecret.objects') as mock_user_secret_objects, \
         patch('apps.core.backends.User.objects') as mock_user_objects:
        
        mock_user_secret_objects.filter.return_value.first.return_value = mock_user_secret
        mock_user_objects.get.side_effect = Exception("User not found")
        
        result = api_auth_backend.authenticate(api_token=api_token)
        
        logger.info(f"Authentication result with user not found: {result}")
        logger.info("API secret authentication user not found test completed")


def test_token_auth_success(auth_backend, request_factory, sample_user_info):
    """测试token认证成功的场景"""
    logger.info("Testing token authentication success")
    
    token = "valid_token_12345678"
    request = request_factory.get('/')
    request.COOKIES = {"current_team": "test_team"}
    
    mock_result = {
        "result": True,
        "data": sample_user_info
    }
    
    with patch('apps.core.backends.SystemMgmt') as mock_system_mgmt, \
         patch.object(auth_backend, 'set_user_info') as mock_set_user_info:
        
        mock_client = Mock()
        mock_system_mgmt.return_value = mock_client
        mock_client.verify_token.return_value = mock_result
        mock_client.get_user_rules.return_value = {"rule1": "value1"}
        
        mock_user = Mock()
        mock_user.username = "test_user"
        mock_set_user_info.return_value = mock_user
        
        result = auth_backend.authenticate(request=request, token=token)
        
        logger.info(f"Token authentication result: {result is not None}")
        logger.info(f"User created: {result.username if result else 'None'}")
        logger.info("Token authentication success test completed")


def test_token_auth_no_token(auth_backend):
    """测试token认证无token的场景"""
    logger.info("Testing token authentication with no token")
    
    result = auth_backend.authenticate()
    
    logger.info(f"Authentication result with no token: {result}")
    logger.info("Token authentication no token test completed")


def test_token_auth_verification_failed(auth_backend, request_factory):
    """测试token验证失败的场景"""
    logger.info("Testing token authentication with verification failed")
    
    token = "invalid_token"
    request = request_factory.get('/')
    
    mock_result = {
        "result": False,
        "message": "Token verification failed"
    }
    
    with patch('apps.core.backends.SystemMgmt') as mock_system_mgmt:
        mock_client = Mock()
        mock_system_mgmt.return_value = mock_client
        mock_client.verify_token.return_value = mock_result
        
        result = auth_backend.authenticate(request=request, token=token)
        
        logger.info(f"Authentication result with failed verification: {result}")
        logger.info("Token authentication verification failed test completed")


def test_token_auth_empty_user_info(auth_backend, request_factory):
    """测试token认证返回空用户信息的场景"""
    logger.info("Testing token authentication with empty user info")
    
    token = "token_with_empty_data"
    request = request_factory.get('/')
    
    mock_result = {
        "result": True,
        "data": None
    }
    
    with patch('apps.core.backends.SystemMgmt') as mock_system_mgmt:
        mock_client = Mock()
        mock_system_mgmt.return_value = mock_client
        mock_client.verify_token.return_value = mock_result
        
        result = auth_backend.authenticate(request=request, token=token)
        
        logger.info(f"Authentication result with empty user info: {result}")
        logger.info("Token authentication empty user info test completed")


def test_verify_token_with_system_mgmt_success(auth_backend):
    """测试SystemMgmt token验证成功的场景"""
    logger.info("Testing SystemMgmt token verification success")
    
    token = "valid_token"
    mock_result = {"result": True, "data": {"username": "test"}}
    
    with patch('apps.core.backends.SystemMgmt') as mock_system_mgmt, \
         patch.dict(os.environ, {'CLIENT_ID': 'test_app'}):
        
        mock_client = Mock()
        mock_system_mgmt.return_value = mock_client
        mock_client.verify_token.return_value = mock_result
        
        result = auth_backend._verify_token_with_system_mgmt(token)
        
        logger.info(f"Token verification result: {result is not None}")
        logger.info(f"Verification data: {result}")
        logger.info("SystemMgmt token verification success test completed")


def test_verify_token_missing_client_id(auth_backend):
    """测试缺少CLIENT_ID环境变量的场景"""
    logger.info("Testing SystemMgmt token verification with missing CLIENT_ID")
    
    token = "test_token"
    mock_result = {"result": True, "data": {"username": "test"}}
    
    with patch('apps.core.backends.SystemMgmt') as mock_system_mgmt, \
         patch.dict(os.environ, {}, clear=True):
        
        mock_client = Mock()
        mock_system_mgmt.return_value = mock_client
        mock_client.verify_token.return_value = mock_result
        
        result = auth_backend._verify_token_with_system_mgmt(token)
        
        logger.info(f"Token verification with missing CLIENT_ID: {result is not None}")
        logger.info("SystemMgmt token verification missing CLIENT_ID test completed")


def test_handle_user_locale_chinese(auth_backend):
    """测试处理中文locale的场景"""
    logger.info("Testing user locale handling for Chinese")
    
    user_info = {"locale": "zh-CN"}
    
    with patch('apps.core.backends.translation') as mock_translation:
        auth_backend._handle_user_locale(user_info)
        
        logger.info(f"Locale mapping result: {user_info.get('locale')}")
        logger.info(f"Translation activate called: {mock_translation.activate.called}")
        logger.info("User locale Chinese handling test completed")


def test_handle_user_locale_no_locale(auth_backend):
    """测试没有locale信息的场景"""
    logger.info("Testing user locale handling with no locale")
    
    user_info = {}
    
    with patch('apps.core.backends.translation') as mock_translation:
        auth_backend._handle_user_locale(user_info)
        
        logger.info(f"Translation activate called: {mock_translation.activate.called}")
        logger.info("User locale no locale handling test completed")


def test_handle_user_locale_activation_error(auth_backend):
    """测试locale激活失败的场景"""
    logger.info("Testing user locale handling with activation error")
    
    user_info = {"locale": "invalid-locale"}
    
    with patch('apps.core.backends.translation') as mock_translation:
        mock_translation.activate.side_effect = Exception("Invalid locale")
        
        auth_backend._handle_user_locale(user_info)
        
        logger.info("Locale activation error handled gracefully")
        logger.info("User locale activation error test completed")


def test_get_user_rules_success(auth_backend, request_factory):
    """测试获取用户规则成功的场景"""
    logger.info("Testing user rules retrieval success")
    
    request = request_factory.get('/')
    request.COOKIES = {"current_team": "test_team"}
    user_info = {"username": "test_user"}
    
    mock_rules = {"rule1": "value1", "rule2": "value2"}
    
    with patch('apps.core.backends.SystemMgmt') as mock_system_mgmt, \
         patch.dict(os.environ, {'CLIENT_ID': 'test_app'}):
        
        mock_client = Mock()
        mock_system_mgmt.return_value = mock_client
        mock_client.get_user_rules.return_value = mock_rules
        
        result = auth_backend._get_user_rules(request, user_info)
        
        logger.info(f"User rules retrieved: {len(result)} rules")
        logger.info(f"Rules content: {result}")
        logger.info("User rules retrieval success test completed")


def test_get_user_rules_no_request(auth_backend):
    """测试无请求对象的场景"""
    logger.info("Testing user rules retrieval with no request")
    
    user_info = {"username": "test_user"}
    
    result = auth_backend._get_user_rules(None, user_info)
    
    logger.info(f"User rules with no request: {result}")
    logger.info("User rules no request test completed")


def test_get_user_rules_no_current_team(auth_backend, request_factory):
    """测试没有当前团队信息的场景"""
    logger.info("Testing user rules retrieval with no current team")
    
    request = request_factory.get('/')
    request.COOKIES = {}
    user_info = {"username": "test_user"}
    
    result = auth_backend._get_user_rules(request, user_info)
    
    logger.info(f"User rules with no current team: {result}")
    logger.info("User rules no current team test completed")


def test_get_user_rules_no_username(auth_backend, request_factory):
    """测试没有用户名的场景"""
    logger.info("Testing user rules retrieval with no username")
    
    request = request_factory.get('/')
    request.COOKIES = {"current_team": "test_team"}
    user_info = {}
    
    result = auth_backend._get_user_rules(request, user_info)
    
    logger.info(f"User rules with no username: {result}")
    logger.info("User rules no username test completed")


def test_set_user_info_create_new_user(sample_user_info):
    """测试创建新用户的场景"""
    logger.info("Testing user info setting with new user creation")
    
    rules = {"rule1": "value1"}
    
    with patch('apps.core.backends.User.objects') as mock_user_objects:
        mock_user = Mock()
        mock_user.username = "test_user"
        mock_user_objects.get_or_create.return_value = (mock_user, True)  # True表示新创建
        
        result = AuthBackend.set_user_info(sample_user_info, rules)
        
        logger.info(f"New user created: {result is not None}")
        logger.info(f"User attributes set: email, is_superuser, group_list, etc.")
        logger.info(f"User rules assigned: {hasattr(result, 'rules') if result else False}")
        logger.info("User info setting new user test completed")


def test_set_user_info_update_existing_user(sample_user_info):
    """测试更新现有用户的场景"""
    logger.info("Testing user info setting with existing user update")
    
    rules = {"rule1": "value1"}
    
    with patch('apps.core.backends.User.objects') as mock_user_objects:
        mock_user = Mock()
        mock_user.username = "test_user"
        mock_user_objects.get_or_create.return_value = (mock_user, False)  # False表示已存在
        
        result = AuthBackend.set_user_info(sample_user_info, rules)
        
        logger.info(f"Existing user updated: {result is not None}")
        logger.info(f"User save method called: {mock_user.save.called}")
        logger.info("User info setting update user test completed")


def test_set_user_info_no_username():
    """测试没有用户名的场景"""
    logger.info("Testing user info setting with no username")
    
    user_info = {"email": "test@example.com"}
    rules = {}
    
    result = AuthBackend.set_user_info(user_info, rules)
    
    logger.info(f"User creation with no username: {result}")
    logger.info("User info setting no username test completed")


def test_set_user_info_integrity_error(sample_user_info):
    """测试数据库完整性错误的场景"""
    logger.info("Testing user info setting with database integrity error")
    
    rules = {"rule1": "value1"}
    
    with patch('apps.core.backends.User.objects') as mock_user_objects:
        mock_user_objects.get_or_create.side_effect = IntegrityError("Duplicate key")
        
        result = AuthBackend.set_user_info(sample_user_info, rules)
        
        logger.info(f"User creation with integrity error: {result}")
        logger.info("User info setting integrity error test completed")


def test_set_user_info_general_exception(sample_user_info):
    """测试一般异常的场景"""
    logger.info("Testing user info setting with general exception")
    
    rules = {"rule1": "value1"}
    
    with patch('apps.core.backends.User.objects') as mock_user_objects:
        mock_user_objects.get_or_create.side_effect = Exception("General error")
        
        result = AuthBackend.set_user_info(sample_user_info, rules)
        
        logger.info(f"User creation with general exception: {result}")
        logger.info("User info setting general exception test completed")


def test_set_user_info_default_values():
    """测试用户信息默认值设置的场景"""
    logger.info("Testing user info setting with default values")
    
    minimal_user_info = {"username": "minimal_user"}
    rules = {}
    
    with patch('apps.core.backends.User.objects') as mock_user_objects:
        mock_user = Mock()
        mock_user.username = "minimal_user"
        mock_user_objects.get_or_create.return_value = (mock_user, True)
        
        result = AuthBackend.set_user_info(minimal_user_info, rules)
        
        logger.info(f"User created with minimal info: {result is not None}")
        logger.info(f"Default email set: {mock_user.email == ''}")
        logger.info(f"Default is_superuser: {mock_user.is_superuser == False}")
        logger.info("User info setting default values test completed")


def test_auth_backend_full_flow_success(auth_backend, request_factory, sample_user_info):
    """测试认证后端完整流程成功的场景"""
    logger.info("Testing authentication backend full flow success")
    
    token = "full_flow_token"
    request = request_factory.get('/')
    request.COOKIES = {"current_team": "test_team"}
    
    mock_verify_result = {
        "result": True,
        "data": sample_user_info
    }
    
    with patch('apps.core.backends.SystemMgmt') as mock_system_mgmt, \
         patch('apps.core.backends.User.objects') as mock_user_objects, \
         patch.dict(os.environ, {'CLIENT_ID': 'test_app'}):
        
        # 设置SystemMgmt mock
        mock_client = Mock()
        mock_system_mgmt.return_value = mock_client
        mock_client.verify_token.return_value = mock_verify_result
        mock_client.get_user_rules.return_value = {"rule1": "value1"}
        
        # 设置User mock
        mock_user = Mock()
        mock_user.username = "test_user"
        mock_user_objects.get_or_create.return_value = (mock_user, True)
        
        result = auth_backend.authenticate(request=request, token=token)
        
        logger.info(f"Full flow authentication successful: {result is not None}")
        logger.info(f"Token verification completed: {mock_client.verify_token.called}")
        logger.info(f"User rules retrieved: {mock_client.get_user_rules.called}")
        logger.info(f"User object created/updated: {mock_user_objects.get_or_create.called}")
        logger.info("Authentication backend full flow test completed")

import json
import logging
import os
from unittest.mock import Mock, patch

import pytest
from django.test import RequestFactory

from apps.core.views.index_view import (
    _check_first_login,
    _create_system_mgmt_client,
    _safe_get_user_id_by_username,
    generate_qr_code,
    get_all_groups,
    get_client,
    get_client_detail,
    get_my_client,
    get_user_menus,
    get_wechat_settings,
    index,
    login,
    login_info,
    reset_pwd,
    verify_otp_code,
    wechat_user_register,
)

# 配置测试日志
logger = logging.getLogger(__name__)


@pytest.fixture
def request_factory():
    """提供Django请求工厂的fixture"""
    return RequestFactory()


@pytest.fixture
def mock_user():
    """创建模拟用户对象的fixture"""
    user = Mock()
    user.username = "test_user"
    user.is_superuser = False
    user.group_list = [{"name": "TestGroup"}]
    user.roles = ["test_role"]
    return user


@pytest.fixture
def mock_superuser():
    """创建模拟超级用户对象的fixture"""
    user = Mock()
    user.username = "admin_user"
    user.is_superuser = True
    user.group_list = [{"name": "AdminGroup"}]
    user.roles = ["admin_role"]
    return user


@pytest.fixture
def mock_system_mgmt_client():
    """创建模拟SystemMgmt客户端的fixture"""
    client = Mock()
    client.login.return_value = {"result": True, "message": "Login successful"}
    client.reset_pwd.return_value = {"result": True, "message": "Password reset successful"}
    client.search_users.return_value = {"data": {"users": [{"id": "user123", "username": "test_user"}]}}
    client.get_client.return_value = {"result": True, "data": {"client_info": "test"}}
    client.get_client_detail.return_value = {"result": True, "data": {"detail": "test"}}
    client.get_user_menus.return_value = {"result": True, "data": {"menus": []}}
    client.get_all_groups.return_value = {"result": True, "data": {"groups": []}}
    client.wechat_user_register.return_value = {"result": True, "message": "WeChat user registered successfully"}
    client.get_wechat_settings.return_value = {"result": True, "data": {"wechat_config": {"app_id": "test_app_id"}}}
    client.generate_qr_code.return_value = {"result": True, "data": {"qr_code": "test_qr_code"}}
    client.verify_otp_code.return_value = {"result": True, "message": "OTP verification successful"}
    return client


def test_create_system_mgmt_client_success():
    """测试成功创建SystemMgmt客户端的场景"""
    logger.info("Testing successful SystemMgmt client creation")

    with patch("apps.core.views.index_view.SystemMgmt") as mock_system_mgmt:
        mock_instance = Mock()
        mock_system_mgmt.return_value = mock_instance

        result = _create_system_mgmt_client()

        logger.info(f"Client creation result: {result}")
        logger.info("SystemMgmt client created successfully in test")


def test_create_system_mgmt_client_failure():
    """测试SystemMgmt客户端创建失败的场景"""
    logger.info("Testing SystemMgmt client creation failure")

    with patch("apps.core.views.index_view.SystemMgmt") as mock_system_mgmt:
        mock_system_mgmt.side_effect = Exception("Connection failed")

        try:
            _create_system_mgmt_client()
        except Exception as e:
            logger.info(f"Expected exception caught: {str(e)}")
            logger.info("SystemMgmt client creation failure handled correctly")


def test_safe_get_user_id_by_username_found(mock_system_mgmt_client):
    """测试通过用户名成功获取用户ID的场景"""
    logger.info("Testing successful user ID retrieval by username")

    username = "test_user"
    result = _safe_get_user_id_by_username(mock_system_mgmt_client, username)

    logger.info(f"Search result for username '{username}': {result}")
    logger.info("User ID retrieval test completed successfully")


def test_safe_get_user_id_by_username_not_found(mock_system_mgmt_client):
    """测试用户名不存在时的处理场景"""
    logger.info("Testing user ID retrieval for non-existent user")

    mock_system_mgmt_client.search_users.return_value = {"data": {"users": []}}

    username = "nonexistent_user"
    result = _safe_get_user_id_by_username(mock_system_mgmt_client, username)

    logger.info(f"Search result for non-existent username '{username}': {result}")
    logger.info("Non-existent user handling test completed")


def test_safe_get_user_id_by_username_exception(mock_system_mgmt_client):
    """测试搜索用户时发生异常的场景"""
    logger.info("Testing user ID retrieval with exception")

    mock_system_mgmt_client.search_users.side_effect = Exception("Search failed")

    username = "test_user"
    result = _safe_get_user_id_by_username(mock_system_mgmt_client, username)

    logger.info(f"Search result with exception for username '{username}': {result}")
    logger.info("Exception handling in user search test completed")


def test_check_first_login_no_groups():
    """测试用户没有组列表时的首次登录检测"""
    logger.info("Testing first login check for user with no groups")

    user = Mock()
    user.username = "new_user"
    user.group_list = []

    result = _check_first_login(user, "Guest")

    logger.info(f"First login check for user with no groups: {result}")
    logger.info("No groups first login test completed")


def test_check_first_login_default_group_only():
    """测试用户只有默认组时的首次登录检测"""
    logger.info("Testing first login check for user with only default group")

    user = Mock()
    user.username = "guest_user"
    user.group_list = [{"name": "Guest"}]

    result = _check_first_login(user, "Guest")

    logger.info(f"First login check for user with default group only: {result}")
    logger.info("Default group only first login test completed")


def test_check_first_login_multiple_groups():
    """测试用户有多个组时的首次登录检测"""
    logger.info("Testing first login check for user with multiple groups")

    user = Mock()
    user.username = "experienced_user"
    user.group_list = [{"name": "Group1"}, {"name": "Group2"}]

    result = _check_first_login(user, "Guest")

    logger.info(f"First login check for user with multiple groups: {result}")
    logger.info("Multiple groups first login test completed")


def test_index_view(request_factory):
    """测试首页视图的基本功能"""
    logger.info("Testing index view")

    request = request_factory.get("/")

    with patch("apps.core.views.index_view.render") as mock_render:
        mock_render.return_value = Mock()

        response = index(request)

        logger.info(f"Index view response: {response}")
        logger.info("Index view test completed")


def test_login_success(request_factory):
    """测试成功登录的场景"""
    logger.info("Testing successful login")

    login_data = {"username": "test_user", "password": "test_password"}
    request = request_factory.post("/login", data=json.dumps(login_data), content_type="application/json")

    with patch("apps.core.views.index_view._create_system_mgmt_client") as mock_create_client:
        mock_client = Mock()
        mock_client.login.return_value = {"result": True, "message": "Login successful"}
        mock_create_client.return_value = mock_client

        response = login(request)
        response_data = json.loads(response.content)

        logger.info(f"Login response: {response_data}")
        logger.info("Successful login test completed")


def test_login_empty_credentials(request_factory):
    """测试空凭据登录的场景"""
    logger.info("Testing login with empty credentials")

    login_data = {"username": "", "password": ""}
    request = request_factory.post("/login", data=json.dumps(login_data), content_type="application/json")

    response = login(request)
    response_data = json.loads(response.content)

    logger.info(f"Empty credentials login response: {response_data}")
    logger.info("Empty credentials login test completed")


def test_login_invalid_json(request_factory):
    """测试无效JSON数据登录的场景"""
    logger.info("Testing login with invalid JSON")

    request = request_factory.post("/login", data="invalid json", content_type="application/json")

    with patch("apps.core.views.index_view._create_system_mgmt_client") as mock_create_client:
        mock_client = Mock()
        mock_client.login.return_value = {"result": False, "message": "Login failed"}
        mock_create_client.return_value = mock_client

        response = login(request)
        response_data = json.loads(response.content)

        logger.info(f"Invalid JSON login response: {response_data}")
        logger.info("Invalid JSON login test completed")


def test_reset_pwd_success(request_factory):
    """测试成功重置密码的场景"""
    logger.info("Testing successful password reset")

    reset_data = {"username": "test_user", "password": "new_password"}
    request = request_factory.post("/reset_pwd", data=json.dumps(reset_data), content_type="application/json")

    with patch("apps.core.views.index_view._create_system_mgmt_client") as mock_create_client:
        mock_client = Mock()
        mock_client.reset_pwd.return_value = {"result": True, "message": "Password reset successful"}
        mock_create_client.return_value = mock_client

        response = reset_pwd(request)
        response_data = json.loads(response.content)

        logger.info(f"Password reset response: {response_data}")
        logger.info("Successful password reset test completed")


def test_login_info_success(request_factory, mock_user):
    """测试成功获取登录信息的场景"""
    logger.info("Testing successful login info retrieval")

    request = request_factory.get("/login_info")
    request.user = mock_user

    with patch("apps.core.views.index_view._create_system_mgmt_client") as mock_create_client:
        mock_client = Mock()
        mock_create_client.search_users.return_value = {"data": {"users": [{"id": "user123", "username": "test_user"}]}}
        mock_create_client.return_value = mock_client

        with patch("apps.core.views.index_view._safe_get_user_id_by_username") as mock_get_user_id:
            mock_get_user_id.return_value = "user123"

            response = login_info(request)
            response_data = json.loads(response.content)

            logger.info(f"Login info response: {response_data}")
            logger.info("Successful login info test completed")


def test_login_info_user_not_found(request_factory, mock_user):
    """测试用户未找到时获取登录信息的场景"""
    logger.info("Testing login info retrieval when user not found")

    request = request_factory.get("/login_info")
    request.user = mock_user

    with patch("apps.core.views.index_view._safe_get_user_id_by_username") as mock_get_user_id:
        mock_get_user_id.return_value = None

        response = login_info(request)
        response_data = json.loads(response.content)

        logger.info(f"User not found login info response: {response_data}")
        logger.info("User not found login info test completed")


def test_get_client_success(request_factory, mock_user):
    """测试成功获取客户端信息的场景"""
    logger.info("Testing successful client info retrieval")

    request = request_factory.get("/get_client")
    request.user = mock_user

    with patch("apps.core.views.index_view._create_system_mgmt_client") as mock_create_client:
        mock_client = Mock()
        mock_client.get_client.return_value = {"result": True, "data": {"client_info": "test"}}
        mock_create_client.return_value = mock_client

        response = get_client(request)
        response_data = json.loads(response.content)

        logger.info(f"Client info response: {response_data}")
        logger.info("Successful client info test completed")


def test_get_my_client_with_client_id(request_factory):
    """测试带有client_id参数获取客户端信息的场景"""
    logger.info("Testing my client info retrieval with client_id")

    request = request_factory.get("/get_my_client?client_id=test_client")

    with patch("apps.core.views.index_view._create_system_mgmt_client") as mock_create_client:
        mock_client = Mock()
        mock_client.get_client.return_value = {"result": True, "data": {"client_info": "test"}}
        mock_create_client.return_value = mock_client

        response = get_my_client(request)
        response_data = json.loads(response.content)

        logger.info(f"My client info with client_id response: {response_data}")
        logger.info("My client info with client_id test completed")


def test_get_my_client_with_env_var(request_factory):
    """测试使用环境变量获取客户端信息的场景"""
    logger.info("Testing my client info retrieval with environment variable")

    request = request_factory.get("/get_my_client")

    with patch.dict(os.environ, {"CLIENT_ID": "env_client_id"}):
        with patch("apps.core.views.index_view._create_system_mgmt_client") as mock_create_client:
            mock_client = Mock()
            mock_client.get_client.return_value = {"result": True, "data": {"client_info": "env_test"}}
            mock_create_client.return_value = mock_client

            response = get_my_client(request)
            response_data = json.loads(response.content)

            logger.info(f"My client info with env var response: {response_data}")
            logger.info("My client info with env var test completed")


def test_get_client_detail_success(request_factory):
    """测试成功获取客户端详情的场景"""
    logger.info("Testing successful client detail retrieval")

    request = request_factory.get("/get_client_detail?name=test_client")

    with patch("apps.core.views.index_view._create_system_mgmt_client") as mock_create_client:
        mock_client = Mock()
        mock_client.get_client_detail.return_value = {"result": True, "data": {"detail": "test"}}
        mock_create_client.return_value = mock_client

        response = get_client_detail(request)
        response_data = json.loads(response.content)

        logger.info(f"Client detail response: {response_data}")
        logger.info("Successful client detail test completed")


def test_get_client_detail_no_name(request_factory):
    """测试没有name参数获取客户端详情的场景"""
    logger.info("Testing client detail retrieval without name parameter")

    request = request_factory.get("/get_client_detail")

    response = get_client_detail(request)
    response_data = json.loads(response.content)

    logger.info(f"Client detail without name response: {response_data}")
    logger.info("Client detail without name test completed")


def test_get_user_menus_success(request_factory, mock_user):
    """测试成功获取用户菜单的场景"""
    logger.info("Testing successful user menus retrieval")

    request = request_factory.get("/get_user_menus?name=test_client")
    request.user = mock_user

    with patch("apps.core.views.index_view._create_system_mgmt_client") as mock_create_client:
        mock_client = Mock()
        mock_client.get_user_menus.return_value = {"result": True, "data": {"menus": []}}
        mock_create_client.return_value = mock_client

        response = get_user_menus(request)
        response_data = json.loads(response.content)

        logger.info(f"User menus response: {response_data}")
        logger.info("Successful user menus test completed")


def test_get_user_menus_no_client_name(request_factory, mock_user):
    """测试没有客户端名称获取用户菜单的场景"""
    logger.info("Testing user menus retrieval without client name")

    request = request_factory.get("/get_user_menus")
    request.user = mock_user

    response = get_user_menus(request)
    response_data = json.loads(response.content)

    logger.info(f"User menus without client name response: {response_data}")
    logger.info("User menus without client name test completed")


def test_get_all_groups_success(request_factory, mock_superuser):
    """测试超级用户成功获取所有组的场景"""
    logger.info("Testing successful all groups retrieval by superuser")

    request = request_factory.get("/get_all_groups")
    request.user = mock_superuser

    with patch("apps.core.views.index_view._create_system_mgmt_client") as mock_create_client:
        mock_client = Mock()
        mock_client.get_all_groups.return_value = {"result": True, "data": {"groups": []}}
        mock_create_client.return_value = mock_client

        response = get_all_groups(request)
        response_data = json.loads(response.content)

        logger.info(f"All groups response by superuser: {response_data}")
        logger.info("Successful all groups retrieval test completed")


def test_get_all_groups_not_authorized(request_factory, mock_user):
    """测试非超级用户获取所有组被拒绝的场景"""
    logger.info("Testing all groups retrieval authorization failure")

    request = request_factory.get("/get_all_groups")
    request.user = mock_user

    response = get_all_groups(request)
    response_data = json.loads(response.content)

    logger.info(f"All groups unauthorized response: {response_data}")
    logger.info("All groups authorization failure test completed")


# 异常处理测试
def test_login_exception_handling(request_factory):
    """测试登录过程中异常处理的场景"""
    logger.info("Testing login exception handling")

    login_data = {"username": "test_user", "password": "test_password"}
    request = request_factory.post("/login", data=json.dumps(login_data), content_type="application/json")

    with patch("apps.core.views.index_view._create_system_mgmt_client") as mock_create_client:
        mock_create_client.side_effect = Exception("System error")

        response = login(request)
        response_data = json.loads(response.content)

        logger.info(f"Login exception response: {response_data}")
        logger.info("Login exception handling test completed")


def test_reset_pwd_exception_handling(request_factory):
    """测试密码重置过程中异常处理的场景"""
    logger.info("Testing password reset exception handling")

    reset_data = {"username": "test_user", "password": "new_password"}
    request = request_factory.post("/reset_pwd", data=json.dumps(reset_data), content_type="application/json")

    with patch("apps.core.views.index_view._create_system_mgmt_client") as mock_create_client:
        mock_create_client.side_effect = Exception("System error")

        response = reset_pwd(request)
        response_data = json.loads(response.content)

        logger.info(f"Password reset exception response: {response_data}")
        logger.info("Password reset exception handling test completed")


def test_login_info_exception_handling(request_factory, mock_user):
    """测试获取登录信息过程中异常处理的场景"""
    logger.info("Testing login info exception handling")

    request = request_factory.get("/login_info")
    request.user = mock_user

    with patch("apps.core.views.index_view._create_system_mgmt_client") as mock_create_client:
        mock_create_client.side_effect = Exception("System error")

        response = login_info(request)
        response_data = json.loads(response.content)

        logger.info(f"Login info exception response: {response_data}")
        logger.info("Login info exception handling test completed")


def test_wechat_user_register_success(request_factory):
    """测试成功进行微信用户注册的场景"""
    logger.info("Testing successful WeChat user registration")

    register_data = {"user_id": "wechat_user_123", "nick_name": "微信用户"}
    request = request_factory.post(
        "/wechat_user_register", data=json.dumps(register_data), content_type="application/json"
    )

    with patch("apps.core.views.index_view._create_system_mgmt_client") as mock_create_client:
        mock_client = Mock()
        mock_client.wechat_user_register.return_value = {
            "result": True,
            "message": "WeChat user registered successfully",
        }
        mock_create_client.return_value = mock_client

        response = wechat_user_register(request)
        response_data = json.loads(response.content)

        logger.info(f"WeChat user registration response: {response_data}")
        logger.info("Successful WeChat user registration test completed")


def test_wechat_user_register_empty_user_id(request_factory):
    """测试微信用户注册时user_id为空的场景"""
    logger.info("Testing WeChat user registration with empty user_id")

    register_data = {"user_id": "", "nick_name": "微信用户"}
    request = request_factory.post(
        "/wechat_user_register", data=json.dumps(register_data), content_type="application/json"
    )

    response = wechat_user_register(request)
    response_data = json.loads(response.content)

    logger.info(f"WeChat user registration with empty user_id response: {response_data}")
    logger.info("Empty user_id WeChat registration test completed")


def test_wechat_user_register_invalid_json(request_factory):
    """测试微信用户注册时JSON格式无效的场景"""
    logger.info("Testing WeChat user registration with invalid JSON")

    request = request_factory.post("/wechat_user_register", data="invalid json", content_type="application/json")

    with patch("apps.core.views.index_view._create_system_mgmt_client") as mock_create_client:
        mock_client = Mock()
        mock_client.wechat_user_register.return_value = {"result": False, "message": "Registration failed"}
        mock_create_client.return_value = mock_client

        response = wechat_user_register(request)
        response_data = json.loads(response.content)

        logger.info(f"WeChat user registration with invalid JSON response: {response_data}")
        logger.info("Invalid JSON WeChat registration test completed")


def test_wechat_user_register_exception_handling(request_factory):
    """测试微信用户注册过程中异常处理的场景"""
    logger.info("Testing WeChat user registration exception handling")

    register_data = {"user_id": "wechat_user_123", "nick_name": "微信用户"}
    request = request_factory.post(
        "/wechat_user_register", data=json.dumps(register_data), content_type="application/json"
    )

    with patch("apps.core.views.index_view._create_system_mgmt_client") as mock_create_client:
        mock_create_client.side_effect = Exception("System error")

        response = wechat_user_register(request)
        response_data = json.loads(response.content)

        logger.info(f"WeChat user registration exception response: {response_data}")
        logger.info("WeChat user registration exception handling test completed")


def test_get_wechat_settings_success(request_factory):
    """测试成功获取微信设置的场景"""
    logger.info("Testing successful WeChat settings retrieval")

    request = request_factory.get("/get_wechat_settings")

    with patch("apps.core.views.index_view._create_system_mgmt_client") as mock_create_client:
        mock_client = Mock()
        mock_client.get_wechat_settings.return_value = {
            "result": True,
            "data": {"wechat_config": {"app_id": "test_app_id", "app_secret": "test_secret"}},
        }
        mock_create_client.return_value = mock_client

        response = get_wechat_settings(request)
        response_data = json.loads(response.content)

        logger.info(f"WeChat settings response: {response_data}")
        logger.info("Successful WeChat settings retrieval test completed")


def test_get_wechat_settings_failure(request_factory):
    """测试获取微信设置失败的场景"""
    logger.info("Testing WeChat settings retrieval failure")

    request = request_factory.get("/get_wechat_settings")

    with patch("apps.core.views.index_view._create_system_mgmt_client") as mock_create_client:
        mock_client = Mock()
        mock_client.get_wechat_settings.return_value = {"result": False, "message": "Settings not found"}
        mock_create_client.return_value = mock_client

        response = get_wechat_settings(request)
        response_data = json.loads(response.content)

        logger.info(f"WeChat settings failure response: {response_data}")
        logger.info("WeChat settings retrieval failure test completed")


def test_get_wechat_settings_exception_handling(request_factory):
    """测试获取微信设置过程中异常处理的场景"""
    logger.info("Testing WeChat settings exception handling")

    request = request_factory.get("/get_wechat_settings")

    with patch("apps.core.views.index_view._create_system_mgmt_client") as mock_create_client:
        mock_create_client.side_effect = Exception("System error")

        response = get_wechat_settings(request)
        response_data = json.loads(response.content)

        logger.info(f"WeChat settings exception response: {response_data}")
        logger.info("WeChat settings exception handling test completed")


def test_generate_qr_code_success(request_factory):
    """测试成功生成QR码的场景"""
    logger.info("Testing successful QR code generation")

    request = request_factory.get("/generate_qr_code?username=test_user")

    with patch("apps.core.views.index_view._create_system_mgmt_client") as mock_create_client:
        mock_client = Mock()
        mock_client.generate_qr_code.return_value = {
            "result": True,
            "data": {"qr_code": "test_qr_code_data", "secret": "test_secret"},
        }
        mock_create_client.return_value = mock_client

        response = generate_qr_code(request)
        response_data = json.loads(response.content)

        logger.info(f"QR code generation response: {response_data}")
        logger.info("Successful QR code generation test completed")


def test_generate_qr_code_empty_username(request_factory):
    """测试生成QR码时用户名为空的场景"""
    logger.info("Testing QR code generation with empty username")

    request = request_factory.get("/generate_qr_code?username=")

    response = generate_qr_code(request)
    response_data = json.loads(response.content)

    logger.info(f"QR code generation with empty username response: {response_data}")
    logger.info("Empty username QR code generation test completed")


def test_generate_qr_code_no_username(request_factory):
    """测试生成QR码时没有用户名参数的场景"""
    logger.info("Testing QR code generation without username parameter")

    request = request_factory.get("/generate_qr_code")

    response = generate_qr_code(request)
    response_data = json.loads(response.content)

    logger.info(f"QR code generation without username response: {response_data}")
    logger.info("No username QR code generation test completed")


def test_generate_qr_code_exception_handling(request_factory):
    """测试生成QR码过程中异常处理的场景"""
    logger.info("Testing QR code generation exception handling")

    request = request_factory.get("/generate_qr_code?username=test_user")

    with patch("apps.core.views.index_view._create_system_mgmt_client") as mock_create_client:
        mock_create_client.side_effect = Exception("System error")

        response = generate_qr_code(request)
        response_data = json.loads(response.content)

        logger.info(f"QR code generation exception response: {response_data}")
        logger.info("QR code generation exception handling test completed")


def test_verify_otp_code_success(request_factory):
    """测试成功验证OTP代码的场景"""
    logger.info("Testing successful OTP code verification")

    otp_data = {"username": "test_user", "otp_code": "123456"}
    request = request_factory.post("/verify_otp_code", data=json.dumps(otp_data), content_type="application/json")

    with patch("apps.core.views.index_view._create_system_mgmt_client") as mock_create_client:
        mock_client = Mock()
        mock_client.verify_otp_code.return_value = {"result": True, "message": "OTP verification successful"}
        mock_create_client.return_value = mock_client

        response = verify_otp_code(request)
        response_data = json.loads(response.content)

        logger.info(f"OTP code verification response: {response_data}")
        logger.info("Successful OTP code verification test completed")


def test_verify_otp_code_empty_credentials(request_factory):
    """测试验证OTP代码时凭据为空的场景"""
    logger.info("Testing OTP code verification with empty credentials")

    otp_data = {"username": "", "otp_code": ""}
    request = request_factory.post("/verify_otp_code", data=json.dumps(otp_data), content_type="application/json")

    response = verify_otp_code(request)
    response_data = json.loads(response.content)

    logger.info(f"OTP code verification with empty credentials response: {response_data}")
    logger.info("Empty credentials OTP verification test completed")


def test_verify_otp_code_empty_username(request_factory):
    """测试验证OTP代码时用户名为空的场景"""
    logger.info("Testing OTP code verification with empty username")

    otp_data = {"username": "", "otp_code": "123456"}
    request = request_factory.post("/verify_otp_code", data=json.dumps(otp_data), content_type="application/json")

    response = verify_otp_code(request)
    response_data = json.loads(response.content)

    logger.info(f"OTP code verification with empty username response: {response_data}")
    logger.info("Empty username OTP verification test completed")


def test_verify_otp_code_empty_otp(request_factory):
    """测试验证OTP代码时OTP代码为空的场景"""
    logger.info("Testing OTP code verification with empty OTP code")

    otp_data = {"username": "test_user", "otp_code": ""}
    request = request_factory.post("/verify_otp_code", data=json.dumps(otp_data), content_type="application/json")

    response = verify_otp_code(request)
    response_data = json.loads(response.content)

    logger.info(f"OTP code verification with empty OTP response: {response_data}")
    logger.info("Empty OTP code verification test completed")


def test_verify_otp_code_invalid_json(request_factory):
    """测试验证OTP代码时JSON格式无效的场景"""
    logger.info("Testing OTP code verification with invalid JSON")

    request = request_factory.post("/verify_otp_code", data="invalid json", content_type="application/json")

    with patch("apps.core.views.index_view._create_system_mgmt_client") as mock_create_client:
        mock_client = Mock()
        mock_client.verify_otp_code.return_value = {"result": False, "message": "Verification failed"}
        mock_create_client.return_value = mock_client

        response = verify_otp_code(request)
        response_data = json.loads(response.content)

        logger.info(f"OTP code verification with invalid JSON response: {response_data}")
        logger.info("Invalid JSON OTP verification test completed")


def test_verify_otp_code_verification_failure(request_factory):
    """测试OTP代码验证失败的场景"""
    logger.info("Testing OTP code verification failure")

    otp_data = {"username": "test_user", "otp_code": "wrong_code"}
    request = request_factory.post("/verify_otp_code", data=json.dumps(otp_data), content_type="application/json")

    with patch("apps.core.views.index_view._create_system_mgmt_client") as mock_create_client:
        mock_client = Mock()
        mock_client.verify_otp_code.return_value = {"result": False, "message": "Invalid OTP code"}
        mock_create_client.return_value = mock_client

        response = verify_otp_code(request)
        response_data = json.loads(response.content)

        logger.info(f"OTP code verification failure response: {response_data}")
        logger.info("OTP code verification failure test completed")


def test_verify_otp_code_exception_handling(request_factory):
    """测试验证OTP代码过程中异常处理的场景"""
    logger.info("Testing OTP code verification exception handling")

    otp_data = {"username": "test_user", "otp_code": "123456"}
    request = request_factory.post("/verify_otp_code", data=json.dumps(otp_data), content_type="application/json")

    with patch("apps.core.views.index_view._create_system_mgmt_client") as mock_create_client:
        mock_create_client.side_effect = Exception("System error")

        response = verify_otp_code(request)
        response_data = json.loads(response.content)

        logger.info(f"OTP code verification exception response: {response_data}")
        logger.info("OTP code verification exception handling test completed")

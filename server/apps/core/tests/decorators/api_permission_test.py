import logging
import pytest
from unittest.mock import patch
from apps.core.decorators.api_permission import HasRole, HasPermission

logger = logging.getLogger(__name__)


class DummyUser:
    def __init__(self, roles=None, permission=None, is_superuser=False):
        self.roles = roles or []
        self.permission = permission or set()
        self.is_superuser = is_superuser


class DummyRequest:
    def __init__(self, user, api_pass=False):
        self.user = user
        self.api_pass = api_pass


def dummy_task(request, *args, **kwargs):
    """模拟业务函数，用于测试装饰器"""
    logger.info("dummy_task called with args: %s, kwargs: %s", args, kwargs)
    return "task_executed"


@pytest.fixture
def admin_user():
    """创建具有admin角色的用户"""
    return DummyUser(roles=["admin"])


@pytest.fixture
def regular_user():
    """创建普通用户"""
    return DummyUser(roles=["user"])


@pytest.fixture
def user_with_permissions():
    """创建具有特定权限的用户"""
    return DummyUser(permission={"read", "write"})


@pytest.fixture
def superuser():
    """创建超级用户"""
    return DummyUser(is_superuser=True)


@pytest.fixture
def no_role_user():
    """创建没有角色的用户"""
    return DummyUser()


def test_has_role_admin_pass(admin_user):
    """测试admin角色用户能够通过HasRole("admin")装饰器验证"""
    request = DummyRequest(admin_user)
    decorated = HasRole("admin")(dummy_task)
    result = decorated(request)
    logger.info("HasRole admin test - result: %s", result)
    logger.info("HasRole admin test - user roles: %s", admin_user.roles)


def test_has_role_regular_user_fail(regular_user):
    """测试普通用户无法通过HasRole("admin")装饰器验证"""
    request = DummyRequest(regular_user)
    decorated = HasRole("admin")(dummy_task)
    result = decorated(request)
    logger.info("HasRole regular user fail test - result type: %s", type(result))
    logger.info("HasRole regular user fail test - user roles: %s", regular_user.roles)


def test_has_role_api_pass_bypass(no_role_user):
    """测试API通行证能够绕过角色验证"""
    request = DummyRequest(no_role_user, api_pass=True)
    decorated = HasRole("admin")(dummy_task)
    result = decorated(request)
    logger.info("HasRole api pass test - result: %s", result)
    logger.info("HasRole api pass test - api_pass: %s", request.api_pass)


def test_has_role_multiple_roles():
    """测试多角色验证场景"""
    user = DummyUser(roles=["user", "editor"])
    request = DummyRequest(user)
    decorated = HasRole(["admin", "editor"])(dummy_task)
    result = decorated(request)
    logger.info("HasRole multiple roles test - result: %s", result)
    logger.info("HasRole multiple roles test - user roles: %s, required: %s",
                user.roles, ["admin", "editor"])


def test_has_role_no_required_roles(no_role_user):
    """测试没有角色要求时的通过场景"""
    request = DummyRequest(no_role_user)
    decorated = HasRole(None)(dummy_task)
    result = decorated(request)
    logger.info("HasRole no requirements test - result: %s", result)


@patch.dict('os.environ', {'CLIENT_ID': 'test_client'})
def test_has_role_admin_with_client_id():
    """测试带CLIENT_ID环境变量的admin角色扩展"""
    user = DummyUser(roles=["test_client_admin"])
    request = DummyRequest(user)
    decorated = HasRole("admin")(dummy_task)
    result = decorated(request)
    logger.info("HasRole admin with client_id test - result: %s", result)
    logger.info("HasRole admin with client_id test - user roles: %s", user.roles)


def test_has_permission_read_pass(user_with_permissions):
    """测试用户具有read权限时能够通过HasPermission("read")验证"""
    request = DummyRequest(user_with_permissions)
    decorated = HasPermission("read")(dummy_task)
    result = decorated(request)
    logger.info("HasPermission read test - result: %s", result)
    logger.info("HasPermission read test - user permissions: %s", user_with_permissions.permission)


def test_has_permission_no_permission_fail(no_role_user):
    """测试用户没有权限时无法通过HasPermission验证"""
    request = DummyRequest(no_role_user)
    decorated = HasPermission("edit")(dummy_task)
    result = decorated(request)
    logger.info("HasPermission no permission test - result type: %s", type(result))
    logger.info("HasPermission no permission test - user permissions: %s", no_role_user.permission)


def test_has_permission_superuser_bypass(superuser):
    """测试超级用户能够绕过权限验证"""
    request = DummyRequest(superuser)
    decorated = HasPermission("edit")(dummy_task)
    result = decorated(request)
    logger.info("HasPermission superuser test - result: %s", result)
    logger.info("HasPermission superuser test - is_superuser: %s", superuser.is_superuser)


def test_has_permission_api_pass_bypass(no_role_user):
    """测试API通行证能够绕过权限验证"""
    request = DummyRequest(no_role_user, api_pass=True)
    decorated = HasPermission("edit")(dummy_task)
    result = decorated(request)
    logger.info("HasPermission api pass test - result: %s", result)
    logger.info("HasPermission api pass test - api_pass: %s", request.api_pass)


def test_has_permission_multiple_permissions():
    """测试多权限验证场景"""
    user = DummyUser(permission={"read", "write", "delete"})
    request = DummyRequest(user)
    decorated = HasPermission("write,edit")(dummy_task)
    result = decorated(request)
    logger.info("HasPermission multiple test - result: %s", result)
    logger.info("HasPermission multiple test - user permissions: %s, required: write,edit",
                user.permission)


def test_has_permission_partial_match():
    """测试部分权限匹配的场景"""
    user = DummyUser(permission={"read"})
    request = DummyRequest(user)
    decorated = HasPermission("read,write")(dummy_task)
    result = decorated(request)
    logger.info("HasPermission partial match test - result: %s", result)
    logger.info("HasPermission partial match test - matched permissions should include 'read'")


def test_error_handling_no_request():
    """测试没有request参数时的错误处理"""
    decorated = HasRole("admin")(dummy_task)
    result = decorated()
    logger.info("Error handling no request test - result type: %s", type(result))


def test_error_handling_user_without_roles():
    """测试用户对象没有roles属性时的错误处理"""

    class BadUser:
        pass

    request = DummyRequest(BadUser())
    decorated = HasRole("admin")(dummy_task)
    result = decorated(request)
    logger.info("Error handling no roles attr test - result type: %s", type(result))


def test_error_handling_user_without_permissions():
    """测试用户对象没有permission属性时的错误处理"""

    class BadUser:
        def __init__(self):
            self.is_superuser = False

    request = DummyRequest(BadUser())
    decorated = HasPermission("read")(dummy_task)
    result = decorated(request)
    logger.info("Error handling no permission attr test - result type: %s", type(result))


@pytest.mark.parametrize("role,expected_pass", [
    ("admin", True),
    ("user", False),
    ("editor", False),
])
def test_has_role_parametrized(role, expected_pass):
    """参数化测试不同角色的验证结果"""
    user = DummyUser(roles=[role])
    request = DummyRequest(user)
    decorated = HasRole("admin")(dummy_task)
    result = decorated(request)

    if expected_pass:
        logger.info("Parametrized test - role %s should pass: %s", role, result == "task_executed")
    else:
        logger.info("Parametrized test - role %s should fail: %s", role, result != "task_executed")


@pytest.mark.parametrize("permissions,required,should_pass", [
    ({"read"}, "read", True),
    ({"write"}, "read", False),
    ({"read", "write"}, "read,write", True),
    ({"read"}, "read,write", True),  # 部分匹配应该通过
    (set(), "read", False),
])
def test_has_permission_parametrized(permissions, required, should_pass):
    """参数化测试不同权限组合的验证结果"""
    user = DummyUser(permission=permissions)
    request = DummyRequest(user)
    decorated = HasPermission(required)(dummy_task)
    result = decorated(request)

    logger.info("Parametrized permission test - permissions: %s, required: %s, should_pass: %s, actual_result: %s",
                permissions, required, should_pass, result == "task_executed")

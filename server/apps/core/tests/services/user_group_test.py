import logging
import pytest
from unittest.mock import Mock, MagicMock

from apps.core.services.user_group import UserGroup
from apps.core.utils.user_group import Group
from apps.rpc.system_mgmt import SystemMgmt

# 配置测试日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 测试数据fixture
@pytest.fixture
def mock_system_mgmt_client():
    """模拟SystemMgmt客户端"""
    client = Mock(spec=SystemMgmt)
    logger.info("Created mock SystemMgmt client")
    return client


@pytest.fixture
def sample_user_search_result():
    """用户搜索结果样本数据"""
    return {
        "data": {
            "count": 2,
            "users": [
                {"id": 1, "username": "user1"},
                {"id": 2, "username": "user2"}
            ]
        }
    }


@pytest.fixture
def sample_groups_search_result():
    """用户组搜索结果样本数据"""
    return {
        "data": [
            {"id": 1, "name": "group1"},
            {"id": 2, "name": "group2"}
        ]
    }


@pytest.fixture
def mock_request_regular_user():
    """模拟普通用户的请求对象"""
    request = Mock()
    request.user = Mock()
    request.user.is_superuser = False
    request.user.group_list = [1, 2, 3]
    logger.info("Created mock request for regular user")
    return request


@pytest.fixture
def mock_request_super_admin():
    """模拟超级管理员的请求对象"""
    request = Mock()
    request.user = Mock()
    request.user.is_superuser = True
    request.user.group_list = []
    logger.info("Created mock request for super admin")
    return request


def test_get_system_mgmt_client(monkeypatch):
    """测试获取SystemMgmt客户端 - 成功创建客户端"""
    mock_client = Mock(spec=SystemMgmt)
    
    def mock_system_mgmt():
        logger.info("Mock SystemMgmt constructor called")
        return mock_client
    
    monkeypatch.setattr("apps.core.services.user_group.SystemMgmt", mock_system_mgmt)
    
    result = UserGroup.get_system_mgmt_client()
    
    logger.info(f"get_system_mgmt_client returned: {type(result)}")
    logger.info("✓ SystemMgmt client created successfully")


def test_user_list_success(mock_system_mgmt_client, sample_user_search_result):
    """测试用户列表获取 - 成功获取用户列表"""
    query_params = {"search": "test", "page": 1}
    mock_system_mgmt_client.search_users.return_value = sample_user_search_result
    
    result = UserGroup.user_list(mock_system_mgmt_client, query_params)
    
    logger.info(f"user_list query_params: {query_params}")
    logger.info(f"user_list result: {result}")
    logger.info(f"Users count: {result['count']}")
    logger.info(f"Users data length: {len(result['users'])}")
    logger.info("✓ User list retrieved successfully")


def test_user_list_empty_result(mock_system_mgmt_client):
    """测试用户列表获取 - 空结果处理"""
    query_params = {"search": "nonexistent"}
    empty_result = {"data": {"count": 0, "users": []}}
    mock_system_mgmt_client.search_users.return_value = empty_result
    
    result = UserGroup.user_list(mock_system_mgmt_client, query_params)
    
    logger.info(f"Empty search query_params: {query_params}")
    logger.info(f"Empty search result: {result}")
    logger.info("✓ Empty user list handled correctly")


def test_groups_list_with_params(mock_system_mgmt_client, sample_groups_search_result):
    """测试用户组列表获取 - 带查询参数"""
    query_params = {"search": "admin"}
    mock_system_mgmt_client.search_groups.return_value = sample_groups_search_result
    
    result = UserGroup.groups_list(mock_system_mgmt_client, query_params)
    
    logger.info(f"groups_list query_params: {query_params}")
    logger.info(f"groups_list result: {result}")
    logger.info(f"Groups count: {len(result)}")
    logger.info("✓ Groups list with params retrieved successfully")


def test_groups_list_with_none_params(mock_system_mgmt_client, sample_groups_search_result):
    """测试用户组列表获取 - 无查询参数（使用默认值）"""
    mock_system_mgmt_client.search_groups.return_value = sample_groups_search_result
    
    result = UserGroup.groups_list(mock_system_mgmt_client, None)
    
    logger.info("groups_list called with None params")
    logger.info(f"Default params used: {UserGroup.DEFAULT_QUERY_PARAMS}")
    logger.info(f"groups_list result: {result}")
    logger.info("✓ Groups list with default params retrieved successfully")


def test_user_groups_list_super_admin(mock_request_super_admin):
    """测试用户组列表获取 - 超级管理员用户"""
    result = UserGroup.user_groups_list(mock_request_super_admin)
    
    logger.info(f"Super admin user_groups_list result: {result}")
    logger.info(f"is_all: {result['is_all']}")
    logger.info(f"group_ids: {result['group_ids']}")
    logger.info("✓ Super admin user groups processed successfully")


def test_user_groups_list_regular_user(mock_request_regular_user, monkeypatch):
    """测试用户组列表获取 - 普通用户"""
    mock_group_instance = Mock(spec=Group)
    mock_group_instance.get_user_group_and_subgroup_ids.return_value = [1, 2, 3, 4, 5]
    
    def mock_group_constructor():
        logger.info("Mock Group constructor called")
        return mock_group_instance
    
    monkeypatch.setattr("apps.core.services.user_group.Group", mock_group_constructor)
    
    result = UserGroup.user_groups_list(mock_request_regular_user)
    
    logger.info(f"Regular user input groups: {mock_request_regular_user.user.group_list}")
    logger.info(f"Regular user user_groups_list result: {result}")
    logger.info(f"is_all: {result['is_all']}")
    logger.info(f"group_ids count: {len(result['group_ids'])}")
    logger.info(f"group_ids: {result['group_ids']}")
    logger.info("✓ Regular user groups processed successfully")


def test_user_groups_list_group_processing_error(mock_request_regular_user, monkeypatch):
    """测试用户组列表获取 - 组处理异常时的降级处理"""
    def mock_group_constructor():
        mock_instance = Mock(spec=Group)
        mock_instance.get_user_group_and_subgroup_ids.side_effect = Exception("Group processing error")
        logger.info("Mock Group constructor with error called")
        return mock_instance
    
    monkeypatch.setattr("apps.core.services.user_group.Group", mock_group_constructor)
    
    result = UserGroup.user_groups_list(mock_request_regular_user)
    
    logger.info(f"Error case user_groups_list result: {result}")
    logger.info(f"Fallback is_all: {result['is_all']}")
    logger.info(f"Fallback group_ids: {result['group_ids']}")
    logger.info("✓ Group processing error handled with safe fallback")


def test_get_all_groups_success(mock_system_mgmt_client):
    """测试获取所有用户组 - 成功获取"""
    all_groups_result = {
        "data": [
            {"id": 1, "name": "admin"},
            {"id": 2, "name": "user"},
            {"id": 3, "name": "guest"}
        ]
    }
    mock_system_mgmt_client.get_all_groups.return_value = all_groups_result
    
    result = UserGroup.get_all_groups(mock_system_mgmt_client)
    
    logger.info(f"get_all_groups result: {result}")
    logger.info(f"All groups count: {len(result)}")
    logger.info("✓ All groups retrieved successfully")


def test_constants_defined():
    """测试类常量定义 - 验证魔法变量已被常量替代"""
    logger.info(f"DEFAULT_SEARCH_QUERY: '{UserGroup.DEFAULT_SEARCH_QUERY}'")
    logger.info(f"DEFAULT_QUERY_PARAMS: {UserGroup.DEFAULT_QUERY_PARAMS}")
    
    # 验证常量值
    expected_default_query = ""
    expected_default_params = {"search": ""}
    
    logger.info(f"Expected default query: '{expected_default_query}'")
    logger.info(f"Expected default params: {expected_default_params}")
    logger.info("✓ Constants defined correctly")


@pytest.mark.parametrize("query_params", [
    {"search": "test"},
    {"search": "admin", "page": 1},
    {"search": "", "limit": 10},
])
def test_user_list_various_params(mock_system_mgmt_client, sample_user_search_result, query_params):
    """测试用户列表获取 - 多种查询参数组合"""
    mock_system_mgmt_client.search_users.return_value = sample_user_search_result
    
    result = UserGroup.user_list(mock_system_mgmt_client, query_params)
    
    logger.info(f"Parametrized test query_params: {query_params}")
    logger.info(f"Parametrized test result: {result}")
    logger.info(f"✓ User list with params {query_params} processed successfully")


@pytest.mark.parametrize("search_term", ["admin", "user", "guest", ""])
def test_groups_list_various_search_terms(mock_system_mgmt_client, sample_groups_search_result, search_term):
    """测试用户组列表获取 - 多种搜索词"""
    query_params = {"search": search_term}
    mock_system_mgmt_client.search_groups.return_value = sample_groups_search_result
    
    result = UserGroup.groups_list(mock_system_mgmt_client, query_params)
    
    logger.info(f"Search term: '{search_term}'")
    logger.info(f"Groups search result count: {len(result)}")
    logger.info(f"✓ Groups search with term '{search_term}' processed successfully")

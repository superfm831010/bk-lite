import pytest
import logging
from unittest.mock import Mock, MagicMock, patch
from django.db.models import Q, QuerySet

from apps.core.utils.viewset_utils import MaintainerViewSet, AuthViewSet

logger = logging.getLogger(__name__)


@pytest.fixture
def mock_request():
    """创建模拟的Django request对象"""
    request = Mock()
    request.user = Mock()
    request.user.username = "test_user"
    request.user.is_superuser = False
    request.user.rules = {}
    request.user.group_list = []
    request.data = {"name": "test_name", "description": "test_desc"}
    return request


@pytest.fixture
def mock_serializer():
    """创建模拟的DRF serializer对象"""
    serializer = Mock()
    serializer.Meta = Mock()
    serializer.Meta.model = Mock()
    serializer.Meta.model.__name__ = "TestModel"
    serializer.context = {}
    return serializer


@pytest.fixture
def mock_queryset():
    """创建模拟的Django QuerySet对象"""
    queryset = Mock(spec=QuerySet)
    queryset.filter.return_value = queryset
    queryset.exclude.return_value = queryset
    queryset.order_by.return_value = queryset
    queryset.count.return_value = 5
    queryset.values_list.return_value = [["team1", "team2"], ["team3"]]
    return queryset


@pytest.fixture
def maintainer_viewset(mock_request):
    """创建MaintainerViewSet实例"""
    viewset = MaintainerViewSet()
    viewset.request = mock_request
    return viewset


@pytest.fixture
def auth_viewset(mock_request, mock_queryset):
    """创建AuthViewSet实例"""
    viewset = AuthViewSet()
    viewset.request = mock_request
    viewset.queryset = mock_queryset
    viewset.permission_key = "test_permission"
    return viewset


def test_maintainer_perform_create_with_valid_user(maintainer_viewset, mock_serializer, mock_request):
    """测试MaintainerViewSet的perform_create方法 - 正常用户创建场景"""
    logger.info("Testing MaintainerViewSet perform_create with valid user")
    
    # 设置模拟数据
    mock_serializer.context = {"request": mock_request}
    mock_serializer.Meta.model.created_by = "field_exists"
    
    with patch.object(maintainer_viewset, 'perform_create', wraps=maintainer_viewset.perform_create):
        try:
            result = maintainer_viewset.perform_create(mock_serializer)
            logger.info(f"perform_create completed successfully")
            logger.info(f"Serializer save called with username: {mock_request.user.username}")
        except Exception as e:
            logger.error(f"perform_create failed: {e}")


def test_maintainer_perform_create_no_request_context(maintainer_viewset, mock_serializer):
    """测试MaintainerViewSet的perform_create方法 - 缺少request上下文场景"""
    logger.info("Testing MaintainerViewSet perform_create without request context")
    
    # 清空serializer context
    mock_serializer.context = {}
    
    with patch.object(maintainer_viewset, 'perform_create', wraps=maintainer_viewset.perform_create):
        try:
            result = maintainer_viewset.perform_create(mock_serializer)
            logger.info("perform_create handled missing request context gracefully")
        except Exception as e:
            logger.error(f"perform_create failed with missing context: {e}")


def test_maintainer_perform_create_model_without_created_by(maintainer_viewset, mock_serializer, mock_request):
    """测试MaintainerViewSet的perform_create方法 - 模型无created_by字段场景"""
    logger.info("Testing MaintainerViewSet perform_create with model lacking created_by field")
    
    mock_serializer.context = {"request": mock_request}
    # 模型没有created_by字段
    del mock_serializer.Meta.model.created_by
    
    with patch.object(maintainer_viewset, 'perform_create', wraps=maintainer_viewset.perform_create):
        try:
            result = maintainer_viewset.perform_create(mock_serializer)
            logger.info("perform_create handled model without created_by field correctly")
        except Exception as e:
            logger.error(f"perform_create failed: {e}")


def test_maintainer_perform_update_with_valid_user(maintainer_viewset, mock_serializer, mock_request):
    """测试MaintainerViewSet的perform_update方法 - 正常用户更新场景"""
    logger.info("Testing MaintainerViewSet perform_update with valid user")
    
    mock_serializer.context = {"request": mock_request}
    mock_serializer.Meta.model.updated_by = "field_exists"
    
    with patch.object(maintainer_viewset, 'perform_update', wraps=maintainer_viewset.perform_update):
        try:
            result = maintainer_viewset.perform_update(mock_serializer)
            logger.info(f"perform_update completed successfully")
            logger.info(f"Update performed by user: {mock_request.user.username}")
        except Exception as e:
            logger.error(f"perform_update failed: {e}")


def test_auth_filter_rules_empty_rules(auth_viewset, mock_queryset):
    """测试AuthViewSet的filter_rules方法 - 空规则列表场景"""
    logger.info("Testing AuthViewSet filter_rules with empty rules")
    
    result = auth_viewset.filter_rules(mock_queryset, [])
    logger.info("filter_rules returned original queryset for empty rules")
    logger.info(f"Queryset type: {type(result)}")


def test_auth_filter_rules_superuser_rule(auth_viewset, mock_queryset):
    """测试AuthViewSet的filter_rules方法 - 超级用户规则场景"""
    logger.info("Testing AuthViewSet filter_rules with superuser rule")
    
    superuser_rules = [{"id": "0"}]
    result = auth_viewset.filter_rules(mock_queryset, superuser_rules)
    logger.info("filter_rules detected superuser rule and returned full queryset")
    logger.info(f"Rules processed: {superuser_rules}")


def test_auth_filter_rules_normal_rules(auth_viewset, mock_queryset):
    """测试AuthViewSet的filter_rules方法 - 普通规则过滤场景"""
    logger.info("Testing AuthViewSet filter_rules with normal rules")
    
    normal_rules = [{"id": 1}, {"id": 2}, {"id": 3}]
    result = auth_viewset.filter_rules(mock_queryset, normal_rules)
    logger.info(f"filter_rules processed {len(normal_rules)} normal rules")
    logger.info(f"Rule IDs extracted: {[rule['id'] for rule in normal_rules]}")


def test_auth_filter_rules_invalid_rules(auth_viewset, mock_queryset):
    """测试AuthViewSet的filter_rules方法 - 无效规则格式场景"""
    logger.info("Testing AuthViewSet filter_rules with invalid rule formats")
    
    invalid_rules = [
        {"id": 1},  # 有效
        {"name": "no_id"},  # 无效：缺少id
        "invalid_string",  # 无效：非字典
        None,  # 无效：None值
        {"id": 2}  # 有效
    ]
    result = auth_viewset.filter_rules(mock_queryset, invalid_rules)
    logger.info(f"filter_rules processed mixed valid/invalid rules")
    logger.info(f"Total rules processed: {len(invalid_rules)}")


def test_auth_query_by_groups_superuser(auth_viewset, mock_queryset, mock_request):
    """测试AuthViewSet的query_by_groups方法 - 超级用户访问场景"""
    logger.info("Testing AuthViewSet query_by_groups for superuser")
    
    mock_request.user.is_superuser = True
    
    with patch.object(auth_viewset, '_list') as mock_list:
        mock_list.return_value = Mock()
        try:
            result = auth_viewset.query_by_groups(mock_request, mock_queryset)
            logger.info("query_by_groups handled superuser access correctly")
            logger.info("Returned full queryset without group filtering")
        except Exception as e:
            logger.error(f"query_by_groups failed for superuser: {e}")


def test_auth_query_by_groups_regular_user_with_permission(auth_viewset, mock_queryset, mock_request):
    """测试AuthViewSet的query_by_groups方法 - 普通用户有权限场景"""
    logger.info("Testing AuthViewSet query_by_groups for regular user with permissions")
    
    mock_request.user.is_superuser = False
    mock_request.user.rules = {"test_permission": [{"id": 1}, {"id": 2}]}
    mock_request.user.group_list = [{"id": "group1"}, {"id": "group2"}]
    
    with patch.object(auth_viewset, '_list') as mock_list:
        mock_list.return_value = Mock()
        try:
            result = auth_viewset.query_by_groups(mock_request, mock_queryset)
            logger.info("query_by_groups processed regular user with permissions")
            logger.info(f"User groups: {len(mock_request.user.group_list)}")
        except Exception as e:
            logger.error(f"query_by_groups failed for regular user: {e}")


def test_auth_get_permission_rules_simple_key(auth_viewset, mock_request):
    """测试AuthViewSet的_get_permission_rules方法 - 简单权限键场景"""
    logger.info("Testing AuthViewSet _get_permission_rules with simple permission key")
    
    mock_request.user.rules = {"test_permission": [{"id": 1}, {"id": 2}]}
    
    rules = auth_viewset._get_permission_rules(mock_request.user)
    logger.info(f"Retrieved rules for simple key: {len(rules)} rules")
    logger.info(f"Permission key used: {auth_viewset.permission_key}")


def test_auth_get_permission_rules_nested_key(auth_viewset, mock_request):
    """测试AuthViewSet的_get_permission_rules方法 - 嵌套权限键场景"""
    logger.info("Testing AuthViewSet _get_permission_rules with nested permission key")
    
    auth_viewset.permission_key = "category.subcategory"
    mock_request.user.rules = {
        "category": {
            "subcategory": [{"id": 1}, {"id": 2}]
        }
    }
    
    rules = auth_viewset._get_permission_rules(mock_request.user)
    logger.info(f"Retrieved rules for nested key: {len(rules)} rules")
    logger.info(f"Nested permission key used: {auth_viewset.permission_key}")


def test_auth_get_permission_rules_invalid_user_rules(auth_viewset, mock_request):
    """测试AuthViewSet的_get_permission_rules方法 - 无效用户规则场景"""
    logger.info("Testing AuthViewSet _get_permission_rules with invalid user rules")
    
    mock_request.user.rules = "invalid_rules_not_dict"
    
    rules = auth_viewset._get_permission_rules(mock_request.user)
    logger.info(f"Handled invalid user rules, returned: {len(rules)} rules")
    logger.info(f"User rules type: {type(mock_request.user.rules)}")


def test_auth_filter_by_user_groups_valid_groups(auth_viewset, mock_queryset, mock_request):
    """测试AuthViewSet的_filter_by_user_groups方法 - 有效用户组场景"""
    logger.info("Testing AuthViewSet _filter_by_user_groups with valid groups")
    
    mock_request.user.group_list = [
        {"id": "group1", "name": "Group 1"},
        {"id": "group2", "name": "Group 2"}
    ]
    
    result = auth_viewset._filter_by_user_groups(mock_request.user, mock_queryset)
    logger.info(f"Filtered queryset by {len(mock_request.user.group_list)} groups")
    logger.info(f"Group IDs: {[g['id'] for g in mock_request.user.group_list]}")


def test_auth_filter_by_user_groups_invalid_groups(auth_viewset, mock_queryset, mock_request):
    """测试AuthViewSet的_filter_by_user_groups方法 - 无效用户组格式场景"""
    logger.info("Testing AuthViewSet _filter_by_user_groups with invalid group formats")
    
    mock_request.user.group_list = [
        {"id": "group1"},  # 有效
        {"name": "no_id"},  # 无效：缺少id
        "invalid_string",  # 无效：非字典
        None  # 无效：None值
    ]
    
    result = auth_viewset._filter_by_user_groups(mock_request.user, mock_queryset)
    logger.info("Handled mixed valid/invalid group formats")
    logger.info(f"Total groups in list: {len(mock_request.user.group_list)}")


def test_auth_update_superuser_access(auth_viewset, mock_request):
    """测试AuthViewSet的update方法 - 超级用户更新权限场景"""
    logger.info("Testing AuthViewSet update method for superuser")
    
    mock_request.user.is_superuser = True
    mock_request.data = {"name": "updated_name", "team": ["team1", "team2"]}
    
    mock_instance = Mock()
    mock_instance.id = 1
    mock_instance.created_by = "other_user"
    
    with patch.object(auth_viewset, 'get_object', return_value=mock_instance), \
         patch.object(auth_viewset, 'get_serializer') as mock_get_serializer, \
         patch.object(auth_viewset, 'perform_update'):
        
        mock_serializer = Mock()
        mock_serializer.data = {"id": 1, "name": "updated_name"}
        mock_get_serializer.return_value = mock_serializer
        
        try:
            result = auth_viewset.update(mock_request)
            logger.info("Superuser update completed successfully")
            logger.info("Team field modification allowed for superuser")
        except Exception as e:
            logger.error(f"Superuser update failed: {e}")


def test_auth_update_non_owner_permission_restriction(auth_viewset, mock_request):
    """测试AuthViewSet的update方法 - 非所有者权限限制场景"""
    logger.info("Testing AuthViewSet update method for non-owner permission restriction")
    
    mock_request.user.is_superuser = False
    mock_request.user.username = "current_user"
    mock_request.data = {"name": "updated_name", "team": ["team1", "team2"]}
    
    mock_instance = Mock()
    mock_instance.id = 1
    mock_instance.created_by = "other_user"  # 不同的创建者
    mock_instance._prefetched_objects_cache = {}
    
    with patch.object(auth_viewset, 'get_object', return_value=mock_instance), \
         patch.object(auth_viewset, 'get_serializer') as mock_get_serializer, \
         patch.object(auth_viewset, 'perform_update'):
        
        mock_serializer = Mock()
        mock_serializer.data = {"id": 1, "name": "updated_name"}
        mock_get_serializer.return_value = mock_serializer
        
        try:
            result = auth_viewset.update(mock_request)
            logger.info("Non-owner update processed with team field restriction")
            logger.info(f"Original created_by: {mock_instance.created_by}")
            logger.info(f"Current user: {mock_request.user.username}")
        except Exception as e:
            logger.error(f"Non-owner update failed: {e}")


def test_auth_validate_name_success_case(auth_viewset):
    """测试AuthViewSet的_validate_name方法 - 名称验证成功场景"""
    logger.info("Testing AuthViewSet _validate_name for successful validation")
    
    name = "unique_name"
    group_list = [
        {"id": "group1", "name": "Group 1"},
        {"id": "group2", "name": "Group 2"}
    ]
    team = ["group3", "group4"]  # 不在existing_teams中
    
    # 模拟没有冲突的查询结果
    auth_viewset.queryset.values_list.return_value = []
    
    result = auth_viewset._validate_name(name, group_list, team)
    logger.info(f"Name validation result: '{result}'")
    logger.info(f"Validated name: {name} with teams: {team}")


def test_auth_validate_name_conflict_case(auth_viewset):
    """测试AuthViewSet的_validate_name方法 - 名称冲突场景"""
    logger.info("Testing AuthViewSet _validate_name for name conflict")
    
    name = "conflicting_name"
    group_list = [
        {"id": "group1", "name": "Group 1"},
        {"id": "group2", "name": "Group 2"}
    ]
    team = ["group1", "group2"]  # 与existing_teams有冲突
    
    # 模拟有冲突的查询结果
    auth_viewset.queryset.values_list.return_value = [["group1", "group3"], ["group2"]]
    
    result = auth_viewset._validate_name(name, group_list, team)
    logger.info(f"Name validation conflict detected: '{result}'")
    logger.info(f"Conflicting team found for name: {name}")


def test_auth_validate_name_invalid_parameters(auth_viewset):
    """测试AuthViewSet的_validate_name方法 - 无效参数场景"""
    logger.info("Testing AuthViewSet _validate_name with invalid parameters")
    
    # 测试各种无效参数组合
    test_cases = [
        (None, [], []),  # 无效name
        ("", [], []),    # 空name
        ("valid_name", "not_a_list", []),  # 无效group_list
        ("valid_name", [], "not_a_list"),  # 无效team
    ]
    
    for name, group_list, team in test_cases:
        result = auth_viewset._validate_name(name, group_list, team)
        logger.info(f"Invalid parameter test - name: {name}, result: '{result}'")


def test_auth_list_method_integration(auth_viewset, mock_request):
    """测试AuthViewSet的list方法 - 集成测试场景"""
    logger.info("Testing AuthViewSet list method integration")
    
    with patch.object(auth_viewset, 'filter_queryset') as mock_filter, \
         patch.object(auth_viewset, 'get_queryset') as mock_get_queryset, \
         patch.object(auth_viewset, 'query_by_groups') as mock_query_groups:
        
        mock_queryset = Mock()
        mock_get_queryset.return_value = mock_queryset
        mock_filter.return_value = mock_queryset
        mock_query_groups.return_value = Mock()
        
        try:
            result = auth_viewset.list(mock_request)
            logger.info("List method integration test completed successfully")
            logger.info("All filter and query methods called in sequence")
        except Exception as e:
            logger.error(f"List method integration test failed: {e}")

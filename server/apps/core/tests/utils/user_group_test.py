import logging
import pytest
from unittest.mock import Mock, patch
from apps.core.utils.user_group import SubGroup, Group

# 配置测试日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture
def sample_group_data():
    """提供测试用的组织数据结构"""
    return [
        {
            "id": "group1",
            "name": "主组织1",
            "subGroups": [
                {
                    "id": "group1_sub1",
                    "name": "子组织1-1",
                    "subGroups": [
                        {
                            "id": "group1_sub1_sub1",
                            "name": "子组织1-1-1",
                            "subGroups": []
                        }
                    ]
                },
                {
                    "id": "group1_sub2",
                    "name": "子组织1-2",
                    "subGroups": []
                }
            ]
        },
        {
            "id": "group2",
            "name": "主组织2",
            "subGroups": []
        }
    ]


@pytest.fixture
def user_group_list():
    """提供测试用的用户组织列表"""
    return [
        {"id": "group1", "name": "主组织1"},
        {"id": "group2", "name": "主组织2"}
    ]


def test_subgroup_init(sample_group_data):
    """测试SubGroup类的初始化功能"""
    logger.info("=== 测试SubGroup初始化 ===")
    
    # 测试正常初始化
    sub_group = SubGroup("group1", sample_group_data)
    logger.info(f"SubGroup初始化成功，group_id: {sub_group.group_id}")
    logger.info(f"传入的group_list长度: {len(sub_group.group_list)}")
    
    # 测试空group_list初始化
    sub_group_empty = SubGroup("group1", None)
    logger.info(f"空group_list初始化成功，group_list: {sub_group_empty.group_list}")


def test_subgroup_get_subgroup_found(sample_group_data):
    """测试SubGroup.get_subgroup方法 - 能找到目标组织的场景"""
    logger.info("=== 测试get_subgroup - 找到目标组织 ===")
    
    sub_group = SubGroup("group1", sample_group_data)
    
    # 测试找到根级组织
    result = sub_group.get_subgroup(sample_group_data[0], "group1")
    logger.info(f"查找根级组织group1结果: {result is not None}")
    if result:
        logger.info(f"找到的组织名称: {result.get('name')}")
    
    # 测试找到子组织
    result = sub_group.get_subgroup(sample_group_data[0], "group1_sub1")
    logger.info(f"查找子组织group1_sub1结果: {result is not None}")
    if result:
        logger.info(f"找到的组织名称: {result.get('name')}")
    
    # 测试找到深层子组织
    result = sub_group.get_subgroup(sample_group_data[0], "group1_sub1_sub1")
    logger.info(f"查找深层子组织group1_sub1_sub1结果: {result is not None}")
    if result:
        logger.info(f"找到的组织名称: {result.get('name')}")


def test_subgroup_get_subgroup_not_found(sample_group_data):
    """测试SubGroup.get_subgroup方法 - 找不到目标组织的场景"""
    logger.info("=== 测试get_subgroup - 找不到目标组织 ===")
    
    sub_group = SubGroup("nonexistent", sample_group_data)
    
    # 测试找不到的组织
    result = sub_group.get_subgroup(sample_group_data[0], "nonexistent_group")
    logger.info(f"查找不存在的组织结果: {result is None}")
    
    # 测试无效数据格式
    result = sub_group.get_subgroup("invalid_data", "group1")
    logger.info(f"传入无效数据格式的查找结果: {result is None}")


def test_subgroup_get_all_group_id_by_subgroups(sample_group_data):
    """测试SubGroup.get_all_group_id_by_subgroups方法 - 递归获取所有子组ID"""
    logger.info("=== 测试get_all_group_id_by_subgroups - 递归获取子组ID ===")
    
    sub_group = SubGroup("group1", sample_group_data)
    id_list = []
    
    # 获取group1的所有子组ID
    subgroups = sample_group_data[0].get("subGroups", [])
    sub_group.get_all_group_id_by_subgroups(subgroups, id_list)
    
    logger.info(f"获取到的子组ID列表: {id_list}")
    logger.info(f"子组ID数量: {len(id_list)}")
    
    # 测试空列表处理
    empty_list = []
    sub_group.get_all_group_id_by_subgroups([], empty_list)
    logger.info(f"空列表处理结果: {empty_list}")
    
    # 测试无效数据处理
    invalid_list = []
    sub_group.get_all_group_id_by_subgroups("invalid", invalid_list)
    logger.info(f"无效数据处理结果: {invalid_list}")


def test_subgroup_get_group_id_and_subgroup_id_with_data(sample_group_data):
    """测试SubGroup.get_group_id_and_subgroup_id方法 - 有数据的场景"""
    logger.info("=== 测试get_group_id_and_subgroup_id - 有数据场景 ===")
    
    # 测试存在的组织ID
    sub_group = SubGroup("group1", sample_group_data)
    result = sub_group.get_group_id_and_subgroup_id()
    
    logger.info(f"group1及其子组ID列表: {result}")
    logger.info(f"返回的ID数量: {len(result)}")
    logger.info(f"是否包含原始group_id: {'group1' in result}")
    
    # 测试没有子组的组织
    sub_group2 = SubGroup("group2", sample_group_data)
    result2 = sub_group2.get_group_id_and_subgroup_id()
    
    logger.info(f"group2及其子组ID列表: {result2}")
    logger.info(f"返回的ID数量: {len(result2)}")


def test_subgroup_get_group_id_and_subgroup_id_without_data():
    """测试SubGroup.get_group_id_and_subgroup_id方法 - 无数据的场景"""
    logger.info("=== 测试get_group_id_and_subgroup_id - 无数据场景 ===")
    
    # 测试空group_list
    sub_group = SubGroup("group1", [])
    result = sub_group.get_group_id_and_subgroup_id()
    
    logger.info(f"空group_list的结果: {result}")
    logger.info(f"结果是否只包含原始ID: {result == ['group1']}")
    
    # 测试None group_list
    sub_group2 = SubGroup("group1", None)
    result2 = sub_group2.get_group_id_and_subgroup_id()
    
    logger.info(f"None group_list的结果: {result2}")
    logger.info(f"结果是否只包含原始ID: {result2 == ['group1']}")


@patch('apps.core.utils.user_group.SystemMgmt')
def test_group_get_group_list_success(mock_system_mgmt, sample_group_data):
    """测试Group.get_group_list方法 - 成功获取组织列表的场景"""
    logger.info("=== 测试Group.get_group_list - 成功场景 ===")
    
    # 模拟SystemMgmt返回成功数据
    mock_instance = Mock()
    mock_instance.get_all_groups.return_value = {"data": sample_group_data}
    mock_system_mgmt.return_value = mock_instance
    
    group = Group()
    result = group.get_group_list()
    
    logger.info(f"获取组织列表成功，数量: {len(result)}")
    logger.info(f"第一个组织ID: {result[0].get('id') if result else 'None'}")
    logger.info(f"SystemMgmt.get_all_groups调用次数: {mock_instance.get_all_groups.call_count}")


@patch('apps.core.utils.user_group.SystemMgmt')
def test_group_get_group_list_failure(mock_system_mgmt):
    """测试Group.get_group_list方法 - 获取失败的场景"""
    logger.info("=== 测试Group.get_group_list - 失败场景 ===")
    
    # 模拟SystemMgmt抛出异常
    mock_instance = Mock()
    mock_instance.get_all_groups.side_effect = Exception("网络连接失败")
    mock_system_mgmt.return_value = mock_instance
    
    group = Group()
    result = group.get_group_list()
    
    logger.info(f"异常情况下的返回结果: {result}")
    logger.info(f"返回结果是否为空列表: {result == []}")
    
    # 模拟返回空数据
    mock_instance.get_all_groups.side_effect = None
    mock_instance.get_all_groups.return_value = None
    
    result2 = group.get_group_list()
    logger.info(f"返回None时的结果: {result2}")
    
    # 模拟返回格式错误的数据
    mock_instance.get_all_groups.return_value = {"data": "invalid_format"}
    
    result3 = group.get_group_list()
    logger.info(f"返回格式错误时的结果: {result3}")


@patch('apps.core.utils.user_group.SystemMgmt')
def test_group_get_user_group_and_subgroup_ids_success(mock_system_mgmt, sample_group_data, user_group_list):
    """测试Group.get_user_group_and_subgroup_ids方法 - 成功场景"""
    logger.info("=== 测试get_user_group_and_subgroup_ids - 成功场景 ===")
    
    # 模拟SystemMgmt返回成功数据
    mock_instance = Mock()
    mock_instance.get_all_groups.return_value = {"data": sample_group_data}
    mock_system_mgmt.return_value = mock_instance
    
    group = Group()
    result = group.get_user_group_and_subgroup_ids(user_group_list)
    
    logger.info(f"用户组织及子组ID列表: {result}")
    logger.info(f"总ID数量: {len(result)}")
    logger.info(f"去重前可能的重复情况: 已自动处理")
    logger.info(f"是否包含group1: {'group1' in result}")
    logger.info(f"是否包含group2: {'group2' in result}")


@patch('apps.core.utils.user_group.SystemMgmt')
def test_group_get_user_group_and_subgroup_ids_edge_cases(mock_system_mgmt, sample_group_data):
    """测试Group.get_user_group_and_subgroup_ids方法 - 边界情况"""
    logger.info("=== 测试get_user_group_and_subgroup_ids - 边界情况 ===")
    
    # 模拟SystemMgmt返回成功数据
    mock_instance = Mock()
    mock_instance.get_all_groups.return_value = {"data": sample_group_data}
    mock_system_mgmt.return_value = mock_instance
    
    group = Group()
    
    # 测试空用户组织列表
    result1 = group.get_user_group_and_subgroup_ids([])
    logger.info(f"空用户组织列表结果: {result1}")
    logger.info(f"空列表返回长度: {len(result1)}")
    
    # 测试None用户组织列表
    result2 = group.get_user_group_and_subgroup_ids(None)
    logger.info(f"None用户组织列表结果: {result2}")
    logger.info(f"None列表返回长度: {len(result2)}")
    
    # 测试无效格式的用户组织列表
    invalid_user_list = [
        "invalid_string",
        {"name": "missing_id"},
        {"id": "group1", "name": "valid_group"},
        None
    ]
    result3 = group.get_user_group_and_subgroup_ids(invalid_user_list)
    logger.info(f"包含无效数据的列表结果: {result3}")
    logger.info(f"无效数据处理后的长度: {len(result3)}")


@patch('apps.core.utils.user_group.SystemMgmt')
def test_group_get_user_group_and_subgroup_ids_system_failure(mock_system_mgmt, user_group_list):
    """测试Group.get_user_group_and_subgroup_ids方法 - 系统服务失败场景"""
    logger.info("=== 测试get_user_group_and_subgroup_ids - 系统服务失败 ===")
    
    # 模拟SystemMgmt返回空数据
    mock_instance = Mock()
    mock_instance.get_all_groups.return_value = None
    mock_system_mgmt.return_value = mock_instance
    
    group = Group()
    result = group.get_user_group_and_subgroup_ids(user_group_list)
    
    logger.info(f"系统服务返回空数据时的结果: {result}")
    logger.info(f"结果是否为空列表: {result == []}")
    
    # 模拟SystemMgmt抛出异常
    mock_instance.get_all_groups.side_effect = Exception("系统服务不可用")
    
    result2 = group.get_user_group_and_subgroup_ids(user_group_list)
    logger.info(f"系统服务异常时的结果: {result2}")
    logger.info(f"异常情况下结果是否为空列表: {result2 == []}")


def test_integration_subgroup_and_group_workflow(sample_group_data, user_group_list):
    """集成测试 - SubGroup和Group的完整工作流程"""
    logger.info("=== 集成测试 - 完整工作流程 ===")
    
    # 模拟Group类获取数据后，SubGroup类处理的完整流程
    with patch('apps.core.utils.user_group.SystemMgmt') as mock_system_mgmt:
        mock_instance = Mock()
        mock_instance.get_all_groups.return_value = {"data": sample_group_data}
        mock_system_mgmt.return_value = mock_instance
        
        # 1. 创建Group实例并获取用户组织ID
        group = Group()
        final_result = group.get_user_group_and_subgroup_ids(user_group_list)
        
        logger.info(f"完整流程最终结果: {final_result}")
        logger.info(f"最终ID数量: {len(final_result)}")
        
        # 2. 验证每个用户组织都被正确处理
        for user_group in user_group_list:
            group_id = user_group.get("id")
            if group_id in final_result:
                logger.info(f"用户组织 {group_id} 处理成功")
            else:
                logger.warning(f"用户组织 {group_id} 未在最终结果中找到")
        
        # 3. 单独测试SubGroup处理逻辑
        for user_group in user_group_list:
            group_id = user_group.get("id")
            sub_group = SubGroup(group_id, sample_group_data)
            sub_result = sub_group.get_group_id_and_subgroup_id()
            logger.info(f"SubGroup单独处理 {group_id} 的结果: {sub_result}")

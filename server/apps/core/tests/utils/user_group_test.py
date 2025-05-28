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
    assert sub_group.group_id == "group1"
    assert sub_group.group_list == sample_group_data
    logger.info(f"SubGroup初始化成功，group_id: {sub_group.group_id}")
    
    # 测试空group_list初始化
    sub_group_empty = SubGroup("group1", None)
    assert sub_group_empty.group_list == []  # 修正：None被转换为空列表
    logger.info("空group_list初始化成功")


def test_subgroup_get_subgroup_found(sample_group_data):
    """测试SubGroup.get_subgroup方法 - 能找到目标组织的场景"""
    logger.info("=== 测试get_subgroup - 找到目标组织 ===")
    
    sub_group = SubGroup("group1", sample_group_data)
    
    # 测试找到根级组织
    result = sub_group.get_subgroup(sample_group_data[0], "group1")
    assert result is not None
    assert result.get("id") == "group1"
    logger.info("查找根级组织group1成功")
    
    # 测试找到子组织
    result = sub_group.get_subgroup(sample_group_data[0], "group1_sub1")
    assert result is not None
    assert result.get("id") == "group1_sub1"
    logger.info("查找子组织group1_sub1成功")


def test_subgroup_get_subgroup_not_found(sample_group_data):
    """测试SubGroup.get_subgroup方法 - 找不到目标组织的场景"""
    logger.info("=== 测试get_subgroup - 找不到目标组织 ===")
    
    sub_group = SubGroup("nonexistent", sample_group_data)
    
    # 测试找不到的组织
    result = sub_group.get_subgroup(sample_group_data[0], "nonexistent_group")
    assert result is None
    logger.info("查找不存在的组织返回None，符合预期")
    
    # 测试无效数据格式
    result = sub_group.get_subgroup("invalid_data", "group1")
    assert result is None
    logger.info("传入无效数据格式返回None，符合预期")


def test_subgroup_get_all_group_id_by_subgroups(sample_group_data):
    """测试SubGroup.get_all_group_id_by_subgroups方法"""
    logger.info("=== 测试get_all_group_id_by_subgroups ===")
    
    sub_group = SubGroup("group1", sample_group_data)
    id_list = []
    
    # 获取group1的所有子组ID
    subgroups = sample_group_data[0].get("subGroups", [])
    sub_group.get_all_group_id_by_subgroups(subgroups, id_list)
    
    assert len(id_list) > 0
    assert "group1_sub1" in id_list
    assert "group1_sub2" in id_list
    logger.info(f"获取到的子组ID列表: {id_list}")


def test_subgroup_get_group_id_and_subgroup_id_with_data(sample_group_data):
    """测试SubGroup.get_group_id_and_subgroup_id方法 - 有数据的场景"""
    logger.info("=== 测试get_group_id_and_subgroup_id - 有数据场景 ===")
    
    # 测试存在的组织ID
    sub_group = SubGroup("group1", sample_group_data)
    result = sub_group.get_group_id_and_subgroup_id()
    
    assert isinstance(result, list)
    assert "group1" in result
    assert len(result) > 1  # 应包含子组织
    logger.info(f"group1及其子组ID列表: {result}")


def test_subgroup_get_group_id_and_subgroup_id_without_data():
    """测试SubGroup.get_group_id_and_subgroup_id方法 - 无数据的场景"""
    logger.info("=== 测试get_group_id_and_subgroup_id - 无数据场景 ===")
    
    # 测试空group_list
    sub_group = SubGroup("group1", [])
    result = sub_group.get_group_id_and_subgroup_id()
    
    assert result == ["group1"]
    logger.info("空group_list返回原始ID，符合预期")
    
    # 测试None group_list
    sub_group2 = SubGroup("group1", None)
    result2 = sub_group2.get_group_id_and_subgroup_id()
    
    assert result2 == ["group1"]
    logger.info("None group_list返回原始ID，符合预期")


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
    
    assert isinstance(result, list)
    assert len(result) == len(sample_group_data)
    logger.info(f"获取组织列表成功，数量: {len(result)}")


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
    
    assert result == []
    logger.info("异常情况下返回空列表，符合预期")


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
    
    assert isinstance(result, list)
    assert "group1" in result
    assert "group2" in result
    logger.info(f"用户组织及子组ID列表: {result}")


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
    assert result1 == []
    logger.info("空用户组织列表返回空列表，符合预期")
    
    # 测试None用户组织列表
    result2 = group.get_user_group_and_subgroup_ids(None)
    assert result2 == []
    logger.info("None用户组织列表返回空列表，符合预期")


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
    
    assert result == []
    logger.info("系统服务返回空数据时返回空列表，符合预期")


def test_integration_workflow(sample_group_data, user_group_list):
    """集成测试 - 完整工作流程"""
    logger.info("=== 集成测试 - 完整工作流程 ===")
    
    with patch('apps.core.utils.user_group.SystemMgmt') as mock_system_mgmt:
        mock_instance = Mock()
        mock_instance.get_all_groups.return_value = {"data": sample_group_data}
        mock_system_mgmt.return_value = mock_instance
        
        # 创建Group实例并获取用户组织ID
        group = Group()
        final_result = group.get_user_group_and_subgroup_ids(user_group_list)
        
        assert isinstance(final_result, list)
        assert len(final_result) > 0
        
        # 验证每个用户组织都被正确处理
        for user_group in user_group_list:
            group_id = user_group.get("id")
            assert group_id in final_result
            logger.info(f"用户组织 {group_id} 处理成功")
        
        logger.info(f"完整流程最终结果: {final_result}")

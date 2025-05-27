import logging
from apps.rpc.system_mgmt import SystemMgmt

logger = logging.getLogger(__name__)


class SubGroup:
    def __init__(self, group_id, group_list):
        self.group_id = group_id
        self.group_list = group_list or []

    def get_group_id_and_subgroup_id(self):
        """获取组织ID与子组ID的列表"""
        logger.info(f"开始获取组织ID {self.group_id} 及其子组ID列表")

        if not self.group_list:
            logger.warning(f"组织列表为空，只返回当前组织ID: {self.group_id}")
            return [self.group_id]

        sub_group = None
        for group in self.group_list:
            try:
                sub_group = self.get_subgroup(group, self.group_id)
                if sub_group:
                    logger.debug(f"找到目标组织: {self.group_id}")
                    break
            except Exception as e:
                logger.error(f"搜索组织时发生错误: {e}, 跳过当前组织")
                continue

        group_id_list = [self.group_id]

        if not sub_group:
            logger.warning(f"未找到组织ID {self.group_id} 对应的组织信息")
            return group_id_list

        try:
            subgroups = sub_group.get("subGroups", [])
            self.get_all_group_id_by_subgroups(subgroups, group_id_list)
            logger.info(f"成功获取组织ID {self.group_id} 及其子组，共 {len(group_id_list)} 个")
        except Exception as e:
            logger.error(f"获取子组ID时发生错误: {e}")

        return group_id_list

    def get_subgroup(self, group, target_id):
        """根据子组ID获取子组"""
        if not isinstance(group, dict):
            logger.warning("组织数据格式错误，不是字典类型")
            return None

        if group.get("id") == target_id:
            return group

        subgroups = group.get("subGroups", [])
        if not isinstance(subgroups, list):
            logger.warning("子组数据格式错误，不是列表类型")
            return None

        for subgroup in subgroups:
            if not isinstance(subgroup, dict):
                continue

            if subgroup.get("id") == target_id:
                return subgroup

            # 递归搜索子组的子组
            nested_subgroups = subgroup.get("subGroups", [])
            if nested_subgroups:
                result = self.get_subgroup(subgroup, target_id)
                if result:
                    return result

        return None

    def get_all_group_id_by_subgroups(self, subgroups, id_list):
        """取出所有子组ID"""
        if not isinstance(subgroups, list):
            logger.warning("子组数据不是列表类型，跳过处理")
            return

        for subgroup in subgroups:
            if not isinstance(subgroup, dict):
                logger.warning("子组数据格式错误，跳过该项")
                continue

            subgroup_id = subgroup.get("id")
            if subgroup_id is not None:
                id_list.append(subgroup_id)

            nested_subgroups = subgroup.get("subGroups", [])
            if nested_subgroups:
                self.get_all_group_id_by_subgroups(nested_subgroups, id_list)


class Group:
    def __init__(self):
        self.system_mgmt_client = SystemMgmt()

    def get_group_list(self):
        """获取组织列表"""
        try:
            logger.info("开始获取所有组织列表")
            groups = self.system_mgmt_client.get_all_groups()

            if not groups:
                logger.warning("系统管理服务返回空数据")
                return []

            group_data = groups.get("data", [])
            logger.info(f"成功获取组织列表，共 {len(group_data) if isinstance(group_data, list) else 0} 个组织")
            return group_data if isinstance(group_data, list) else []

        except Exception as e:
            logger.error(f"获取组织列表时发生错误: {e}")
            return []

    def get_user_group_and_subgroup_ids(self, user_group_list=None):
        """获取用户组织ID与子组ID的列表"""
        if user_group_list is None:
            user_group_list = []

        logger.info(f"开始处理用户组织列表，共 {len(user_group_list)} 个组织")

        # 获取所有组织列表
        all_groups = self.get_group_list()
        if not all_groups:
            logger.warning("无法获取组织列表，返回空结果")
            return []

        # 获取用户组织ID与子组ID的列表
        user_group_and_subgroup_ids = []

        for group_info in user_group_list:
            if not isinstance(group_info, dict):
                logger.warning(f"用户组织信息格式错误，跳过: {group_info}")
                continue

            group_id = group_info.get("id")
            if group_id is None:
                logger.warning(f"用户组织信息缺少ID字段，跳过: {group_info}")
                continue

            try:
                sub_group_processor = SubGroup(group_id, all_groups)
                group_ids = sub_group_processor.get_group_id_and_subgroup_id()
                user_group_and_subgroup_ids.extend(group_ids)
                logger.debug(f"处理组织ID {group_id}，获得 {len(group_ids)} 个相关组织ID")
            except Exception as e:
                logger.error(f"处理组织ID {group_id} 时发生错误: {e}")
                continue

        # ID去重
        user_group_and_subgroup_ids = list(set(user_group_and_subgroup_ids))
        logger.info(f"用户组织及子组ID处理完成，去重后共 {len(user_group_and_subgroup_ids)} 个ID")

        return user_group_and_subgroup_ids

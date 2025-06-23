from apps.core.logger import system_mgmt_logger as logger


class GroupUtils(object):
    @staticmethod
    def build_group_tree(groups, is_superuser=False, user_groups=None):
        """构建组的树状结构，只展示用户有权限的组及其父级组"""
        if user_groups is None:
            user_groups = []

        # 超级用户返回完整树结构
        if is_superuser:
            return GroupUtils._build_full_tree(groups, is_superuser, user_groups)

        # 构建组字典和父子关系映射
        group_dict, parent_child_map = GroupUtils._build_group_mappings(groups)

        # 获取需要展示的组ID集合（有权限的组及其所有父级）
        visible_group_ids = GroupUtils._get_visible_groups(group_dict, user_groups)

        # 构建过滤后的树结构
        return GroupUtils._build_filtered_tree(group_dict, visible_group_ids, user_groups)

    @staticmethod
    def _build_group_mappings(groups):
        """构建组字典和父子关系映射"""
        group_dict = {}
        parent_child_map = {}

        for group in groups:
            group_dict[group.id] = {
                "id": group.id,
                "name": group.name,
                "subGroupCount": 0,
                "subGroups": [],
                "hasAuth": False,
            }

            if hasattr(group, "parent_id") and group.parent_id:
                group_dict[group.id]["parentId"] = group.parent_id
                if group.parent_id not in parent_child_map:
                    parent_child_map[group.parent_id] = []
                parent_child_map[group.parent_id].append(group.id)

        return group_dict, parent_child_map

    @staticmethod
    def _get_visible_groups(group_dict, user_groups):
        """递归获取需要展示的组ID集合"""
        visible_ids = set(user_groups)

        # 递归向上查找父级组
        def add_parent_groups(group_id):
            if group_id in group_dict and "parentId" in group_dict[group_id]:
                parent_id = group_dict[group_id]["parentId"]
                if parent_id not in visible_ids:
                    visible_ids.add(parent_id)
                    add_parent_groups(parent_id)

        for group_id in user_groups:
            add_parent_groups(group_id)

        logger.info(f"可见组数量: {len(visible_ids)}, 用户权限组: {len(user_groups)}")
        return visible_ids

    @staticmethod
    def _build_filtered_tree(group_dict, visible_group_ids, user_groups):
        """构建过滤后的树结构"""
        filtered_dict = {}
        root_groups = []

        # 创建过滤后的组字典
        for group_id in visible_group_ids:
            if group_id in group_dict:
                group_data = group_dict[group_id].copy()
                group_data["hasAuth"] = group_id in user_groups
                group_data["subGroups"] = []
                group_data["subGroupCount"] = 0
                filtered_dict[group_id] = group_data

        # 构建父子关系
        for group_id, group_data in filtered_dict.items():
            if "parentId" in group_data and group_data["parentId"] in filtered_dict:
                parent_id = group_data["parentId"]
                filtered_dict[parent_id]["subGroups"].append(group_data)
                filtered_dict[parent_id]["subGroupCount"] += 1
            else:
                root_groups.append(group_data)

        return root_groups

    @staticmethod
    def _build_full_tree(groups, is_superuser, user_groups):
        """构建完整树结构（超级用户）"""
        group_dict = {}
        root_groups = []

        for group in groups:
            group_dict[group.id] = {
                "id": group.id,
                "name": group.name,
                "subGroupCount": 0,
                "subGroups": [],
                "hasAuth": is_superuser or group.id in user_groups,
            }

            if hasattr(group, "parent_id") and group.parent_id:
                group_dict[group.id]["parentId"] = group.parent_id

        for group_id, group_data in group_dict.items():
            if "parentId" in group_data and group_data["parentId"] in group_dict:
                parent_id = group_data["parentId"]
                group_dict[parent_id]["subGroups"].append(group_data)
                group_dict[parent_id]["subGroupCount"] += 1
            else:
                root_groups.append(group_data)

        return root_groups

class GroupUtils(object):
    @staticmethod
    def build_group_tree(groups, is_superuser=False, user_groups=None):
        """构建组的树状结构"""
        # 创建组的字典表示，方便后续查找
        group_dict = {}
        root_groups = []
        if user_groups is None:
            user_groups = []

        # 第一遍循环：创建所有组的基本信息
        for group in groups:
            group_dict[group.id] = {
                "id": group.id,
                "name": group.name,
                "subGroupCount": 0,
                "subGroups": [],
                "hasAuth": is_superuser or group.id in user_groups,
            }
            # 如果有parent_id字段，则添加到字典中，方便后续关联
            if hasattr(group, "parent_id") and group.parent_id:
                group_dict[group.id]["parentId"] = group.parent_id

        for group_id, group_data in group_dict.items():
            if "parentId" in group_data:
                parent_id = group_data["parentId"]
                if parent_id in group_dict:
                    group_dict[parent_id]["subGroups"].append(group_data)
                    group_dict[parent_id]["subGroupCount"] += 1
            else:
                # 没有父组的组被视为根组
                root_groups.append(group_data)

        return root_groups

from apps.cmdb.constants import ORGANIZATION
from apps.cmdb.graph.format_type import FORMAT_TYPE


class PermissionManage:
    def __init__(self, roles=[], user_groups=[]):
        self.roles = roles
        self.user_groups = user_groups

    def get_group_params(self):
        """获取组织条件，用于列表页查询"""
        group_ids = [group["id"] for group in self.user_groups]
        method = FORMAT_TYPE.get("list[]")
        params = method({"field": ORGANIZATION, "value": group_ids})
        return params

    def get_permission_params(self):
        """获取条件，用于列表页查询"""

        # 查询用户角色

        # 判断是否为超管, 超管返回空条件
        if "admin" in self.roles:
            return ""

        # 获取用户组织条件
        params = self.get_group_params()

        return params

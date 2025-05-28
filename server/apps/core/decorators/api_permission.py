import logging
import os
from functools import wraps
from typing import List, Union, Set, Any, Callable

from django.utils.translation import gettext as _
from django.views.generic.base import View

from apps.core.utils.web_utils import WebUtils

logger = logging.getLogger("app")


def _extract_request(args: tuple) -> Any:
    """从参数中提取请求对象"""
    request = args[0]
    if isinstance(request, View):
        return args[1] if len(args) > 1 else None
    return request


class HasRole(object):
    def __init__(self, roles: Union[str, List[str], None] = None):
        self.roles = self._normalize_roles(roles)

    def _normalize_roles(self, roles: Union[str, List[str], None]) -> List[str]:
        """标准化角色列表"""
        if roles is None:
            return []

        if isinstance(roles, str):
            if roles == "admin":
                client_id = os.getenv("CLIENT_ID", "")
                return ["admin", f"{client_id}_admin"] if client_id else ["admin"]
            return [roles]

        if isinstance(roles, list):
            return roles

        return []

    def __call__(self, task_definition: Callable) -> Callable:
        @wraps(task_definition)
        def wrapper(*args, **kwargs):
            request = _extract_request(args)
            if request is None:
                return WebUtils.response_403(_("insufficient permissions"))

            # 检查API通行证
            if getattr(request, "api_pass", False):
                return task_definition(*args, **kwargs)

            # 如果没有指定角色要求，直接通过
            if not self.roles:
                return task_definition(*args, **kwargs)

            # 获取用户角色并检查权限
            user_roles = getattr(request.user, 'roles', [])
            for role in user_roles:
                if role in self.roles:
                    return task_definition(*args, **kwargs)

            logger.warning(f"Access denied. Required roles: {self.roles}, user roles: {user_roles}")
            return WebUtils.response_403(_("insufficient permissions"))

        return wrapper


class HasPermission(object):
    def __init__(self, permission: str = ""):
        self.permission = self._parse_permissions(permission)

    def _parse_permissions(self, permission: str) -> Set[str]:
        """解析权限字符串为集合"""
        if not permission:
            return set()
        return {p.strip() for p in permission.split(",") if p.strip()}

    def __call__(self, task_definition: Callable) -> Callable:
        @wraps(task_definition)
        def wrapper(*args, **kwargs):
            request = _extract_request(args)
            if request is None:
                return WebUtils.response_403(_("insufficient permissions"))

            # 检查API通行证
            if getattr(request, "api_pass", False):
                return task_definition(*args, **kwargs)

            # 检查超级用户
            if getattr(request.user, 'is_superuser', False):
                return task_definition(*args, **kwargs)

            # 检查权限交集
            user_permissions = getattr(request.user, 'permission', set())
            if self.permission & user_permissions:
                return task_definition(*args, **kwargs)

            logger.warning(f"Access denied. Required permissions: {self.permission}, user permissions: {user_permissions}")
            return WebUtils.response_403(_("insufficient permissions"))

        return wrapper

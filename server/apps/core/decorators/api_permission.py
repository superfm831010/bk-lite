import logging
import os
from functools import wraps
from typing import List, Union, Set, Any, Callable

from django.utils.translation import gettext as _
from django.views.generic.base import View

from apps.core.utils.web_utils import WebUtils

logger = logging.getLogger("app")

# 常量定义
ADMIN_ROLE = "admin"
API_PASS_ATTR = "api_pass"
CLIENT_ID_ENV = "CLIENT_ID"
PERMISSION_DELIMITER = ","


class HasRole(object):
    def __init__(self, roles: Union[str, List[str], None] = None):
        self.roles = self._normalize_roles(roles)

    def _normalize_roles(self, roles: Union[str, List[str], None]) -> List[str]:
        """标准化角色列表"""
        if roles is None:
            return []

        if isinstance(roles, str):
            if roles == ADMIN_ROLE:
                client_id = os.getenv(CLIENT_ID_ENV, "")
                if not client_id:
                    logger.warning("CLIENT_ID environment variable is not set, using default admin role only")
                return [ADMIN_ROLE, f"{client_id}_admin"] if client_id else [ADMIN_ROLE]
            else:
                return [roles]

        if isinstance(roles, list):
            return roles

        logger.error(f"Invalid roles type: {type(roles)}, expected str or list")
        return []

    def _extract_request(self, args: tuple) -> Any:
        """从参数中提取请求对象"""
        try:
            request = args[0]
            if isinstance(request, View):
                if len(args) < 2:
                    logger.error("View instance found but no request object in second argument")
                    return None
                request = args[1]
            return request
        except (IndexError, AttributeError) as e:
            logger.error(f"Failed to extract request object: {e}")
            return None

    def _check_api_pass(self, request: Any) -> bool:
        """检查是否有API通行证"""
        return getattr(request, API_PASS_ATTR, False)

    def _get_user_roles(self, request: Any) -> List[str]:
        """获取用户角色列表"""
        try:
            user_info = request.user
            if not hasattr(user_info, 'roles'):
                logger.warning("User object does not have 'roles' attribute")
                return []

            roles = user_info.roles
            if not isinstance(roles, (list, tuple)):
                logger.warning(f"User roles is not a list/tuple, got: {type(roles)}")
                return []

            return list(roles)
        except AttributeError as e:
            logger.error(f"Failed to get user roles: {e}")
            return []

    def __call__(self, task_definition: Callable) -> Callable:
        @wraps(task_definition)
        def wrapper(*args, **kwargs):
            request = self._extract_request(args)
            if request is None:
                logger.error("Could not extract request object from arguments")
                return WebUtils.response_403(_("insufficient permissions"))

            # 检查API通行证
            if self._check_api_pass(request):
                logger.debug("API pass detected, skipping role check")
                return task_definition(*args, **kwargs)

            # 如果没有指定角色要求，直接通过
            if not self.roles:
                logger.debug("No roles required, allowing access")
                return task_definition(*args, **kwargs)

            # 获取用户角色
            user_roles = self._get_user_roles(request)
            if not user_roles:
                logger.warning("User has no roles, denying access")
                return WebUtils.response_403(_("insufficient permissions"))

            # 检查角色权限
            for role in user_roles:
                if role in self.roles:
                    logger.info(f"Access granted for role: {role}")
                    return task_definition(*args, **kwargs)

            logger.warning(f"Access denied. Required roles: {self.roles}, user roles: {user_roles}")
            return WebUtils.response_403(_("insufficient permissions"))

        return wrapper


class HasPermission(object):
    def __init__(self, permission: str = ""):
        self.permission = self._parse_permissions(permission)

    def _parse_permissions(self, permission: str) -> Set[str]:
        """解析权限字符串为集合"""
        if not permission or not isinstance(permission, str):
            return set()

        permissions = {p.strip() for p in permission.split(PERMISSION_DELIMITER) if p.strip()}
        return permissions

    def _extract_request(self, args: tuple) -> Any:
        """从参数中提取请求对象"""
        try:
            request = args[0]
            if isinstance(request, View):
                if len(args) < 2:
                    logger.error("View instance found but no request object in second argument")
                    return None
                request = args[1]
            return request
        except (IndexError, AttributeError) as e:
            logger.error(f"Failed to extract request object: {e}")
            return None

    def _check_api_pass(self, request: Any) -> bool:
        """检查是否有API通行证"""
        return getattr(request, API_PASS_ATTR, False)

    def _is_superuser(self, request: Any) -> bool:
        """检查是否为超级用户"""
        try:
            user = request.user
            if not hasattr(user, 'is_superuser'):
                logger.warning("User object does not have 'is_superuser' attribute")
                return False
            return bool(user.is_superuser)
        except AttributeError as e:
            logger.error(f"Failed to check superuser status: {e}")
            return False

    def _get_user_permissions(self, request: Any) -> Set[str]:
        """获取用户权限集合"""
        try:
            user = request.user
            if not hasattr(user, 'permission'):
                logger.warning("User object does not have 'permission' attribute")
                return set()

            user_permissions = user.permission
            if not isinstance(user_permissions, set):
                logger.warning(f"User permissions is not a set, got: {type(user_permissions)}")
                return set()

            return user_permissions
        except AttributeError as e:
            logger.error(f"Failed to get user permissions: {e}")
            return set()

    def __call__(self, task_definition: Callable) -> Callable:
        @wraps(task_definition)
        def wrapper(*args, **kwargs):
            request = self._extract_request(args)
            if request is None:
                logger.error("Could not extract request object from arguments")
                return WebUtils.response_403(_("insufficient permissions"))

            # 检查API通行证
            if self._check_api_pass(request):
                logger.debug("API pass detected, skipping permission check")
                return task_definition(*args, **kwargs)

            # 检查超级用户
            if self._is_superuser(request):
                logger.info("Superuser access granted")
                return task_definition(*args, **kwargs)

            # 获取用户权限
            user_permissions = self._get_user_permissions(request)

            # 检查权限交集
            if self.permission & user_permissions:
                matched_permissions = self.permission & user_permissions
                logger.info(f"Access granted with permissions: {matched_permissions}")
                return task_definition(*args, **kwargs)

            logger.warning(
                f"Access denied. Required permissions: {self.permission}, user permissions: {user_permissions}")
            return WebUtils.response_403(_("insufficient permissions"))

        return wrapper

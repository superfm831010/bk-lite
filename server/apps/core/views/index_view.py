import json
import os
import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from rest_framework.decorators import api_view

from apps.core.utils.exempt import api_exempt
from apps.rpc.system_mgmt import SystemMgmt

# 配置日志
logger = logging.getLogger(__name__)

# 常量定义
DEFAULT_GROUP_NAME_KEY = "DEFAULT_GROUP_NAME"
DEFAULT_GROUP_FALLBACK = "Guest"
CLIENT_ID_KEY = "CLIENT_ID"
EMPTY_STRING = ""

# 错误消息常量
ERROR_MSG_EMPTY_CREDENTIALS = _("Username or password cannot be empty")
ERROR_MSG_NOT_AUTHORIZED = _("Not Authorized")
ERROR_MSG_SYSTEM_ERROR = _("System error occurred")


def _create_system_mgmt_client():
    """创建SystemMgmt客户端的工厂方法"""
    try:
        client = SystemMgmt()
        logger.info("SystemMgmt client created successfully")
        return client
    except Exception as e:
        logger.error(f"Failed to create SystemMgmt client: {str(e)}")
        raise


def _safe_get_user_id_by_username(client, username):
    """安全获取用户ID"""
    try:
        logger.info(f"Searching for user: {username}")
        res = client.search_users({"search": username})

        users_data = res.get("data", {})
        users_list = users_data.get("users", [])

        if not users_list:
            logger.warning(f"No users found for username: {username}")
            return None

        # 查找匹配的用户
        matching_users = [user for user in users_list if user.get("username") == username]

        if not matching_users:
            logger.warning(f"No exact match found for username: {username}")
            return None

        user_id = matching_users[0].get("id")
        logger.info(f"Found user ID {user_id} for username: {username}")
        return user_id

    except Exception as e:
        logger.error(f"Error searching for user {username}: {str(e)}")
        return None


def _check_first_login(user, default_group):
    """检查是否为首次登录"""
    group_list = getattr(user, 'group_list', [])

    # 如果没有组列表，认为是首次登录
    if not group_list:
        logger.info(f"User {user.username} has no groups - first login")
        return True

    # 如果只有一个组且为默认组，认为是首次登录
    if len(group_list) == 1:
        first_group = group_list[0]
        group_name = first_group.get("name") if isinstance(first_group, dict) else str(first_group)
        if group_name == default_group:
            logger.info(f"User {user.username} only has default group - first login")
            return True

    logger.info(f"User {user.username} has {len(group_list)} groups - not first login")
    return False


@api_exempt
def index(request):
    logger.info("Index page requested")
    response = render(request, "index.html")
    return response


@api_exempt
def login(request):
    logger.info("Login attempt started")

    try:
        # 安全解析请求数据
        if hasattr(request, 'body') and request.body:
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                logger.warning("Invalid JSON in request body, falling back to POST data")
                data = request.POST.dict()
        else:
            data = request.POST.dict()

        username = data.get("username", EMPTY_STRING).strip()
        password = data.get("password", EMPTY_STRING)

        if not username or not password:
            logger.warning(f"Login failed: empty credentials for user '{username}'")
            return JsonResponse({"result": False, "message": ERROR_MSG_EMPTY_CREDENTIALS})

        logger.info(f"Processing login for user: {username}")
        client = _create_system_mgmt_client()
        res = client.login(username, password)

        if res.get("result"):
            logger.info(f"Login successful for user: {username}")
        else:
            logger.warning(f"Login failed for user: {username}")

        return JsonResponse(res)

    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return JsonResponse({"result": False, "message": ERROR_MSG_SYSTEM_ERROR})


@api_exempt
def reset_pwd(request):
    logger.info("Password reset attempt started")

    try:
        # 安全解析请求数据
        if hasattr(request, 'body') and request.body:
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                logger.warning("Invalid JSON in request body, falling back to POST data")
                data = request.POST.dict()
        else:
            data = request.POST.dict()

        username = data.get("username", EMPTY_STRING).strip()
        password = data.get("password", EMPTY_STRING)

        logger.info(f"Processing password reset for user: {username}")
        client = _create_system_mgmt_client()
        res = client.reset_pwd(username, password)

        if res.get("result"):
            logger.info(f"Password reset successful for user: {username}")
        else:
            logger.warning(f"Password reset failed for user: {username}")

        return JsonResponse(res)

    except Exception as e:
        logger.error(f"Password reset error: {str(e)}")
        return JsonResponse({"result": False, "message": ERROR_MSG_SYSTEM_ERROR})


@api_view(["GET"])
def login_info(request):
    logger.info(f"Login info requested for user: {request.user.username}")

    try:
        default_group = os.environ.get(DEFAULT_GROUP_NAME_KEY, DEFAULT_GROUP_FALLBACK)
        is_first_login = _check_first_login(request.user, default_group)

        client = _create_system_mgmt_client()
        user_id = _safe_get_user_id_by_username(client, request.user.username)

        if user_id is None:
            logger.error(f"Could not find user ID for: {request.user.username}")
            return JsonResponse({"result": False, "message": "User not found"})

        response_data = {
            "result": True,
            "data": {
                "user_id": user_id,
                "username": request.user.username,
                "is_superuser": getattr(request.user, 'is_superuser', False),
                "group_list": getattr(request.user, 'group_list', []),
                "roles": getattr(request.user, 'roles', []),
                "is_first_login": is_first_login,
            },
        }

        logger.info(f"Login info retrieved successfully for user: {request.user.username}")
        return JsonResponse(response_data)

    except Exception as e:
        logger.error(f"Error retrieving login info for {request.user.username}: {str(e)}")
        return JsonResponse({"result": False, "message": ERROR_MSG_SYSTEM_ERROR})


def get_client(request):
    logger.info(f"Client info requested by user: {request.user.username}")

    try:
        client = _create_system_mgmt_client()
        return_data = client.get_client(EMPTY_STRING, request.user.username)

        logger.info(f"Client info retrieved successfully for user: {request.user.username}")
        return JsonResponse(return_data)

    except Exception as e:
        logger.error(f"Error retrieving client info for {request.user.username}: {str(e)}")
        return JsonResponse({"result": False, "message": ERROR_MSG_SYSTEM_ERROR})


def get_my_client(request):
    logger.info("My client info requested")

    try:
        client = _create_system_mgmt_client()
        client_id = request.GET.get("client_id", EMPTY_STRING) or os.getenv(CLIENT_ID_KEY, EMPTY_STRING)

        logger.info(f"Retrieving client info for client_id: {client_id or 'default'}")
        return_data = client.get_client(client_id, EMPTY_STRING)

        logger.info("My client info retrieved successfully")
        return JsonResponse(return_data)

    except Exception as e:
        logger.error(f"Error retrieving my client info: {str(e)}")
        return JsonResponse({"result": False, "message": ERROR_MSG_SYSTEM_ERROR})


def get_client_detail(request):
    client_name = request.GET.get("name", EMPTY_STRING)
    logger.info(f"Client detail requested for: {client_name}")

    if not client_name:
        logger.warning("Client detail requested without name parameter")
        return JsonResponse({"result": False, "message": "Client name is required"})

    try:
        client = _create_system_mgmt_client()
        return_data = client.get_client_detail(client_id=client_name)

        logger.info(f"Client detail retrieved successfully for: {client_name}")
        return JsonResponse(return_data)

    except Exception as e:
        logger.error(f"Error retrieving client detail for {client_name}: {str(e)}")
        return JsonResponse({"result": False, "message": ERROR_MSG_SYSTEM_ERROR})


def get_user_menus(request):
    client_name = request.GET.get("name", EMPTY_STRING)
    logger.info(f"User menus requested for client: {client_name}, user: {request.user.username}")

    if not client_name:
        logger.warning("User menus requested without client name parameter")
        return JsonResponse({"result": False, "message": "Client name is required"})

    try:
        client = _create_system_mgmt_client()
        return_data = client.get_user_menus(
            client_id=client_name,
            roles=getattr(request.user, 'roles', []),
            username=request.user.username,
            is_superuser=getattr(request.user, 'is_superuser', False),
        )

        logger.info(f"User menus retrieved successfully for client: {client_name}, user: {request.user.username}")
        return JsonResponse(return_data)

    except Exception as e:
        logger.error(f"Error retrieving user menus for {client_name}: {str(e)}")
        return JsonResponse({"result": False, "message": ERROR_MSG_SYSTEM_ERROR})


def get_all_groups(request):
    logger.info(f"All groups requested by user: {request.user.username}")

    if not getattr(request.user, 'is_superuser', False):
        logger.warning(f"Non-superuser {request.user.username} attempted to access all groups")
        return JsonResponse({"result": False, "message": ERROR_MSG_NOT_AUTHORIZED})

    try:
        client = _create_system_mgmt_client()
        return_data = client.get_all_groups()

        logger.info(f"All groups retrieved successfully by superuser: {request.user.username}")
        return JsonResponse(return_data)

    except Exception as e:
        logger.error(f"Error retrieving all groups: {str(e)}")
        return JsonResponse({"result": False, "message": ERROR_MSG_SYSTEM_ERROR})

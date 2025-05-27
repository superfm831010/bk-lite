import json
import os

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from rest_framework.decorators import api_view

from apps.core.utils.exempt import api_exempt
from apps.rpc.system_mgmt import SystemMgmt


def index(request):
    data = {"STATIC_URL": "static/", "RUN_MODE": "PROD"}
    response = render(request, "index.prod.html", data)
    return response


@api_exempt
def login(request):
    data = json.loads(request.body) or request.POST.dict()
    username = data.get("username", "")
    password = data.get("password", "")
    if not username or not password:
        return JsonResponse({"result": False, "message": _("Username or password cannot be empty")})
    client = SystemMgmt()
    res = client.login(username, password)
    return JsonResponse(res)


@api_view
def wechat_user_register(request):
    data = json.loads(request.body) or request.POST.dict()
    user_id = data.get("user_id", "")
    nick_name = data.get("nick_name", "")
    if not user_id:
        return JsonResponse({"result": False, "message": _("user_id cannot be empty")})
    client = SystemMgmt()
    res = client.wechat_user_register(user_id, nick_name)
    return JsonResponse(res)


@api_view
def get_wechat_settings(request):
    client = SystemMgmt()
    res = client.get_wechat_settings()
    return JsonResponse(res)


@api_exempt
def reset_pwd(request):
    data = json.loads(request.body) or request.POST.dict()
    username = data.get("username", "")
    password = data.get("password", "")
    client = SystemMgmt()
    res = client.reset_pwd(username, password)
    return JsonResponse(res)


@api_view(["GET"])
def login_info(request):
    is_first_login = False
    default_group = os.environ.get("DEFAULT_GROUP_NAME", "Guest")
    if not request.user.group_list:
        is_first_login = True
    elif len(request.user.group_list) == 1 and request.user.group_list[0]["name"] == default_group:
        is_first_login = True
    client = SystemMgmt()
    res = client.search_users({"search": request.user.username})
    user_id = [i for i in res["data"]["users"] if i["username"] == request.user.username][0]["id"]
    return JsonResponse(
        {
            "result": True,
            "data": {
                "user_id": user_id,
                "username": request.user.username,
                "is_superuser": request.user.is_superuser,
                "group_list": request.user.group_list,
                "roles": request.user.roles,
                "is_first_login": is_first_login,
            },
        }
    )


@api_exempt
def generate_qr_code(request):
    username = request.GET.get("username")
    if not username:
        return JsonResponse({"result": False, "message": _("Username cannot be empty")})
    client = SystemMgmt()
    res = client.generate_qr_code(username)
    return JsonResponse(res)


@api_exempt
def verify_otp_code(request):
    kwargs = json.loads(request.body) or request.POST.dict()
    username = kwargs.get("username", "")
    otp_code = kwargs.get("otp_code", "")
    if not username or not otp_code:
        return JsonResponse({"result": False, "message": _("Username or OTP code cannot be empty")})
    client = SystemMgmt()
    res = client.verify_otp_code(username, otp_code)
    return JsonResponse(res)


def get_client(request):
    client = SystemMgmt()
    return_data = client.get_client("", request.user.username)
    return JsonResponse(return_data)


def get_my_client(request):
    client = SystemMgmt()
    client_id = request.GET.get("client_id", "") or os.getenv("CLIENT_ID", "")
    return_data = client.get_client(client_id, "")
    return JsonResponse(return_data)


def get_client_detail(request):
    client = SystemMgmt()
    return_data = client.get_client_detail(
        client_id=request.GET["name"],
    )
    return JsonResponse(return_data)


def get_user_menus(request):
    client = SystemMgmt()
    return_data = client.get_user_menus(
        client_id=request.GET["name"],
        roles=request.user.role_ids,
        username=request.user.username,
        is_superuser=request.user.is_superuser,
    )
    return JsonResponse(return_data)


def get_all_groups(request):
    if not request.user.is_superuser:
        return JsonResponse({"result": False, "message": _("Not Authorized")})
    client = SystemMgmt()
    return_data = client.get_all_groups()
    return JsonResponse(return_data)

import base64
import io
import os
import time

import jwt
import pyotp
import qrcode
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q

import nats_client
from apps.core.backends import cache
from apps.core.logger import system_mgmt_logger as logger
from apps.system_mgmt.models import (
    App,
    Channel,
    ChannelChoices,
    Group,
    GroupDataRule,
    LoginModule,
    Menu,
    Role,
    User,
    UserRule,
)
from apps.system_mgmt.models.system_settings import SystemSettings
from apps.system_mgmt.opspilot_menus import GUEST_MENUS
from apps.system_mgmt.services.role_manage import RoleManage
from apps.system_mgmt.utils.channel_utils import send_by_bot, send_email, send_wechat
from apps.system_mgmt.utils.group_utils import GroupUtils


@nats_client.register
def verify_token(token):
    if not token:
        return {"result": False, "message": "Token is missing"}
    token = token.split("Basic ")[-1]
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("JWT_ALGORITHM", "HS256")
    user_info = jwt.decode(token, key=secret_key, algorithms=algorithm)
    time_now = int(time.time())
    login_expired_time_set = SystemSettings.objects.filter(key="login_expired_time").first()
    login_expired_time = 3600 * 24
    if login_expired_time_set:
        login_expired_time = int(login_expired_time_set.value) * 3600

    if time_now - login_expired_time > user_info["login_time"]:
        return {"result": False, "message": "Token is invalid"}
    user = User.objects.filter(id=user_info["user_id"]).first()
    if not user:
        return {"result": False, "message": "User not found"}
    role_list = Role.objects.filter(id__in=user.role_list)
    role_names = [f"{role.app}--{role.name}" if role.app else role.name for role in role_list]
    is_superuser = "admin" in role_names or "system-manager--admin" in role_names
    group_list = Group.objects.all()
    if not is_superuser:
        group_list = group_list.filter(id__in=user.group_list)
    # groups = GroupUtils.build_group_tree(group_list)
    groups = list(group_list.values("id", "name", "parent_id"))
    queryset = Group.objects.all()

    # 构建嵌套组结构
    groups_data = GroupUtils.build_group_tree(queryset, is_superuser, [i["id"] for i in groups])
    menus = cache.get(f"menus-user:{user.id}")
    if not menus:
        menus = {}
        if not is_superuser:
            menu_list = role_list.values_list("menu_list", flat=True)
            menu_ids = []
            for i in menu_list:
                menu_ids.extend(i)
            menu_data = Menu.objects.filter(id__in=list(set(menu_ids))).values_list("app", "name")
            for app, name in menu_data:
                menus.setdefault(app, []).append(name)
        cache.set(f"menus-user:{user.id}", menus, 60 * 30)
    return {
        "result": True,
        "data": {
            "username": user.username,
            "display_name": user.display_name,
            "domain": user.domain,
            "email": user.email,
            "is_superuser": is_superuser,
            "group_list": groups,
            "group_tree": groups_data,
            "roles": role_names,
            "role_ids": user.role_list,
            "locale": user.locale,
            "permission": menus,
        },
    }


@nats_client.register
def get_user_menus(client_id, roles, username, is_superuser):
    client = RoleManage()
    client_id = client_id
    menus = []
    if not is_superuser:
        menu_ids = []
        role_menus = Role.objects.filter(app=client_id, id__in=roles).values_list("menu_list", flat=True)
        for i in role_menus:
            menu_ids.extend(i)
        menus = list(Menu.objects.filter(app=client_id, id__in=list(set(menu_ids))).values_list("name", flat=True))
    user_menus = client.get_all_menus(client_id, user_menus=menus, username=username, is_superuser=is_superuser)
    return {"result": True, "data": user_menus}


@nats_client.register
def get_client(client_id="", username="", domain="domain.com"):
    app_list = App.objects.all()
    if client_id:
        app_list = app_list.filter(name__in=client_id.split(";"))
    if username:
        user = User.objects.filter(username=username, domain=domain).first()
        if not user:
            return {"result": False, "message": "User not found"}
        app_name_list = list(Role.objects.filter(id__in=user.role_list).values_list("app", flat=True).distinct())
        if "" not in app_name_list:
            app_list = app_list.filter(name__in=app_name_list)
    return_data = list(app_list.order_by("name").values())
    return {"result": True, "data": return_data}


@nats_client.register
def get_client_detail(client_id):
    app_obj = App.objects.filter(name=client_id).first()
    if not app_obj:
        return {"result": False, "message": "Client not found"}
    return {
        "result": True,
        "data": {
            "id": app_obj.id,
            "name": app_obj.name,
            "description": app_obj.description,
            "description_cn": app_obj.description_cn,
        },
    }


@nats_client.register
def get_group_users(group):
    users = User.objects.filter(group_list__contains=int(group)).values("id", "username", "display_name")
    return {"result": True, "data": list(users)}


@nats_client.register
def get_all_users():
    data = User.objects.all().values(*User.display_fields())
    return {"result": True, "data": list(data)}


@nats_client.register
def search_groups(query_params):
    groups = Group.objects.filter(name__contains=query_params["search"]).values()
    return {"result": True, "data": list(groups)}


@nats_client.register
def search_users(query_params):
    page = int(query_params.get("page", 1))
    page_size = int(query_params.get("page_size", 10))
    search = query_params.get("search", "")
    queryset = User.objects.filter(
        Q(username__icontains=search) | Q(display_name__icontains=search) | Q(email__icontains=search)
    )
    start = (page - 1) * page_size
    end = page * page_size
    total = queryset.count()
    display_fields = User.display_fields() + ["group_list"]
    data = queryset.values(*display_fields)[start:end]
    return {"result": True, "data": {"count": total, "users": list(data)}}


@nats_client.register
def init_user_default_attributes(user_id, group_name, default_group_id):
    try:
        role_obj = Role.objects.get(name="guest", app="opspilot")
        normal_role = Role.objects.get(name="normal", app="opspilot")
        user = User.objects.get(id=user_id)
        top_group, _ = Group.objects.get_or_create(
            name=os.getenv("DEFAULT_GROUP_NAME", "Guest"), parent_id=0, defaults={"description": ""}
        )
        if Group.objects.filter(parent_id=top_group.id, name=group_name).exists():
            return {"result": False, "message": "Group already exists"}

        guest_group, _ = Group.objects.get_or_create(name="OpsPilotGuest", parent_id=0)
        group_obj = Group.objects.create(name=group_name, parent_id=top_group.id)
        user.locale = "zh-Hans"
        user.timezone = "Asia/Shanghai"
        if role_obj.id not in user.role_list:
            user.role_list.append(role_obj.id)
        if normal_role.id in user.role_list:
            user.role_list.remove(normal_role.id)
        user.group_list.remove(int(default_group_id))
        user.group_list.append(guest_group.id)
        user.group_list.append(group_obj.id)
        user.save()
        default_rule = GroupDataRule.objects.get(name="OpsPilot内置规则", group_id=guest_group.id)
        UserRule.objects.create(username=user.username, group_rule_id=default_rule.id)
        cache.delete(f"group_{user.username}")
        return {"result": True, "data": {"group_id": group_obj.id}}
    except Exception as e:
        logger.exception(e)
        return {"result": False, "message": str(e)}


@nats_client.register
def create_opspilot_guest_role():
    menus = dict(Menu.objects.filter(app="opspilot").values_list("id", "name"))
    guest_menus = GUEST_MENUS[:]
    menu_list = [k for k, v in menus.items() if v in guest_menus]
    Role.objects.update_or_create(name="guest", app="opspilot", defaults={"menu_list": menu_list})
    guest_group, _ = Group.objects.get_or_create(name="Guest", parent_id=0, defaults={"description": "Guest group"})
    opspilot_guest_group, _ = Group.objects.get_or_create(name="OpsPilotGuest", parent_id=0)
    return {"result": True, "data": {"group_id": opspilot_guest_group.id}}


@nats_client.register
def create_default_rule(llm_model, ocr_model, embed_model, rerank_model):
    guest_group = Group.objects.get(name="OpsPilotGuest", parent_id=0)
    GroupDataRule.objects.get_or_create(
        name="OpsPilot内置规则",
        app="opspilot",
        defaults=dict(
            group_id=guest_group.id,
            description="Guest组数据权限规则",
            group_name=guest_group.name,
            rules={
                "skill": [{"id": -1, "name": "All", "permission": ["View", "Operate"]}],
                "tools": [{"id": -1, "name": "All", "permission": ["View", "Operate"]}],
                "provider": {
                    "llm_model": [{"id": llm_model["id"], "name": llm_model["name"], "permission": ["View"]}],
                    "ocr_model": [{"id": i["id"], "name": i["name"], "permission": ["View"]} for i in ocr_model],
                    "embed_model": [{"id": i["id"], "name": i["name"], "permission": ["View"]} for i in embed_model],
                    "rerank_model": [{"id": rerank_model["id"], "name": rerank_model["name"], "permission": ["View"]}],
                },
                "knowledge": [{"id": -1, "name": "All", "permission": ["View", "Operate"]}],
            },
        ),
    )
    return {"result": True}


@nats_client.register
def get_all_groups():
    groups = Group.objects.all()
    return_data = GroupUtils.build_group_tree(groups, True)
    return {"result": True, "data": return_data}


@nats_client.register
def search_channel_list(channel_type):
    channels = Channel.objects.all()
    if channel_type:
        channels = channels.filter(channel_type=channel_type)
    return {"result": True, "data": [i for i in channels.values("id", "name", "channel_type")]}


@nats_client.register
def send_msg_with_channel(channel_id, title, content, receivers):
    channel_obj = Channel.objects.filter(id=channel_id).first()
    if not channel_obj:
        return {"result": False, "message": "Channel not found"}
    if channel_obj.channel_type == ChannelChoices.EMAIL:
        return send_email(channel_obj, title, content, receivers)
    elif channel_obj.channel_type == ChannelChoices.ENTERPRISE_WECHAT_BOT:
        return send_by_bot(channel_obj, content)
    return send_wechat(channel_obj, content, receivers)


@nats_client.register
def get_user_rules(group_id, username):
    rules = UserRule.objects.filter(username=username).filter(
        Q(group_rule__group_id=group_id) | Q(group_rule__group_name="OpsPilotGuest")
    )
    if not rules:
        return {}
    return {i.group_rule.app: i.group_rule.rules for i in rules}


@nats_client.register
def get_group_id(group_name):
    group = Group.objects.filter(name=group_name, parent_id=0).first()
    if not group:
        return {"result": False, "message": f"group named '{group_name}' not exists."}
    return {"result": True, "data": group.id}


@nats_client.register
def login(username, password):
    user = User.objects.filter(username=username, domain="domain.com").first()
    if not user:
        return {"result": False, "message": "Username or password is incorrect"}

    # 使用 check_password 验证密码是否匹配
    if not check_password(password, user.password):
        return {"result": False, "message": "Username or password is incorrect"}
    return get_user_login_token(user, username)


@nats_client.register
def reset_pwd(username, password):
    user = User.objects.filter(username=username).first()
    if not user:
        return {"result": False, "message": "Username not exists"}
    user.password = make_password(password)
    user.temporary_pwd = False
    user.save()
    return {"result": True}


@nats_client.register
def wechat_user_register(user_id, nick_name):
    user, is_first_login = User.objects.update_or_create(username=user_id, defaults={"display_name": nick_name})
    if not user.group_list:
        default_group = Group.objects.get(name="Default", parent_id=0)
        user.group_list = [default_group.id]
    if not user.role_list:
        default_role = list(
            Role.objects.filter(name="normal", app__in=["opspilot", "ops-console"]).values_list("id", flat=True)
        )
        user.role_list = default_role
    user.save()
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("JWT_ALGORITHM", "HS256")
    user_obj = {"user_id": user.id, "login_time": int(time.time())}
    token = jwt.encode(payload=user_obj, key=secret_key, algorithm=algorithm)
    return {
        "result": True,
        "data": {
            "id": user.id,
            "username": user.username,
            "display_name": user.display_name,
            "is_first_login": is_first_login,
            "locale": user.locale,
            "token": token,
        },
    }


@nats_client.register
def get_wechat_settings():
    login_module = LoginModule.objects.filter(source_type="wechat", enabled=True).first()
    if not login_module:
        return {"result": True, "data": {"enabled": False}}

    return {
        "result": True,
        "data": {
            "enabled": True,
            "app_id": login_module.app_id,
            "app_secret": login_module.decrypted_app_secret,
            "redirect_uri": login_module.other_config.get("redirect_uri", ""),
            "callback_url": login_module.other_config.get("callback_url", ""),
        },
    }


# 生成二维码
@nats_client.register
def generate_qr_code(username):
    # 查找用户
    user = User.objects.filter(username=username).first()
    if not user:
        return {"result": False, "message": "User not found"}
    user.otp_secret = pyotp.random_base32()
    user.save()
    totp = pyotp.TOTP(user.otp_secret)
    # 创建用于Authenticator应用的配置URL
    provisioning_uri = totp.provisioning_uri(name=username, issuer_name="WeopsX")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(provisioning_uri)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

    return {"result": True, "data": {"qr_code": qr_code_base64}}


# 验证OTP代码
@nats_client.register
def verify_otp_code(username, otp_code):
    user = User.objects.get(username=username)
    totp = pyotp.TOTP(user.otp_secret)
    if totp.verify(otp_code):
        return {"result": True, "message": "Verification successful"}
    return {"result": False, "message": "Invalid OTP code"}


@nats_client.register
def get_namespace_by_domain(domain):
    login_module = LoginModule.objects.filter(source_type="bk_lite", other_config__contains={"domain": domain}).first()
    if not login_module:
        return {"result": False, "message": "Login module not found"}
    namespace = login_module.other_config.get("namespace", "")
    return {"result": True, "data": namespace}


@nats_client.register
def bk_lite_user_login(username, domain):
    user = User.objects.filter(username=username, domain=domain).first()
    if not user:
        return {"result": False, "message": "Username or password is incorrect"}
    return get_user_login_token(user, username)


def get_user_login_token(user, username):
    if user.disabled:
        return {"result": False, "message": "User is disabled"}
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("JWT_ALGORITHM", "HS256")
    user_obj = {"user_id": user.id, "login_time": int(time.time())}
    token = jwt.encode(payload=user_obj, key=secret_key, algorithm=algorithm)
    enable_otp = SystemSettings.objects.filter(key="enable_otp").first()
    if not enable_otp:
        enable_otp = False
    else:
        enable_otp = enable_otp.value == "1"
    return {
        "result": True,
        "data": {
            "token": token,
            "username": username,
            "display_name": user.display_name,
            "id": user.id,
            "domain": user.domain,
            "locale": user.locale,
            "temporary_pwd": user.temporary_pwd,
            "enable_otp": enable_otp,
            "qrcode": user.otp_secret is None or user.otp_secret == "",
        },
    }


@nats_client.register
def get_login_module_domain_list():
    login_module_list = list(
        LoginModule.objects.filter(source_type="bk_lite").values_list("other_config__domain", flat=True)
    )
    login_module_list.insert(0, "domain.com")
    return {"result": True, "data": login_module_list}

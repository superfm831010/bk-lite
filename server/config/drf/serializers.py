from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.fields import empty

from apps.system_mgmt.models import User


class UsernameSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)
        self.user_map = dict(User.objects.all().values_list("username", "display_name"))

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if "created_by" in list(response.keys()):
            response["created_by"] = self.user_map.get(response["created_by"], response["created_by"])
        if "updated_by" in list(response.keys()):
            response["updated_by"] = self.user_map.get(response["updated_by"], response["updated_by"])
        return response


class I18nSerializer(UsernameSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        if "is_build_in" in list(response.keys()):
            for key in response.keys():
                if isinstance(response[key], str):
                    response[key] = _(response[key])
        return response


class TeamSerializer(I18nSerializer):
    team_name = serializers.SerializerMethodField()

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)
        request = self.context["request"]
        groups = request.user.group_list
        self.group_map = {i["id"]: i["name"] for i in groups}

    def get_team_name(self, instance):
        return [self.group_map.get(i) for i in instance.team if i in self.group_map]


class AuthSerializer(UsernameSerializer):
    permissions = serializers.SerializerMethodField()

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)
        request = self.context["request"]
        self.rule_map = {}

        # 获取当前应用名称
        app_name = self._get_app_name()

        if hasattr(self, "permission_key") and app_name:
            # 获取应用下的规则
            app_rules = request.user.rules.get(app_name, {})

            if "." in self.permission_key:
                keys = self.permission_key.split(".")
                rules = app_rules.get(keys[0], {}).get(keys[1], [])
            else:
                rules = app_rules.get(self.permission_key, [])
            self.rule_map = {int(i["id"]): i["permission"] for i in rules}

    def _get_app_name(self):
        """获取当前序列化器所属的应用名称"""
        module_path = self.__class__.__module__
        if "apps." in module_path:
            # 从模块路径中提取应用名称，如 apps.opspilot.serializers -> opspilot
            parts = module_path.split(".")
            if len(parts) >= 2 and parts[0] == "apps":
                return parts[1]
        return None

    def get_permissions(self, instance):
        return self.rule_map.get(instance.id, ["View", "Operate"])

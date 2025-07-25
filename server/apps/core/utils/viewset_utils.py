import logging

from django.db.models import Q
from django.http import JsonResponse
from django.utils.translation import gettext as _
from rest_framework import viewsets
from rest_framework.response import Response

from apps.core.utils.permission_utils import get_permission_rules

logger = logging.getLogger(__name__)


class MaintainerViewSet(viewsets.ModelViewSet):
    DEFAULT_USERNAME = "guest"

    def perform_create(self, serializer):
        """创建时补充基础Model中的字段"""
        try:
            request = serializer.context.get("request")
            if not request:
                return super().perform_create(serializer)

            user = getattr(request, "user", None)
            username = getattr(user, "username", self.DEFAULT_USERNAME)
            domain = getattr(user, "domain", "domain.com")
            model = serializer.Meta.model
            if hasattr(model, "created_by"):
                serializer.save(created_by=username, updated_by=username, domain=domain, updated_by_domain=domain)

        except Exception as e:
            logger.error(f"Error in perform_create: {e}")
            raise

        return super().perform_create(serializer)

    def perform_update(self, serializer):
        """更新时补充基础Model中的字段"""
        try:
            request = serializer.context.get("request")
            if not request:
                return super().perform_update(serializer)

            user = getattr(request, "user", None)
            username = getattr(user, "username", self.DEFAULT_USERNAME)
            domain = getattr(user, "domain", "domain.com")

            model = serializer.Meta.model
            if hasattr(model, "updated_by"):
                serializer.save(updated_by=username, updated_by_domain=domain)

        except Exception as e:
            logger.error(f"Error in perform_update: {e}")
            raise

        return super().perform_update(serializer)


class AuthViewSet(MaintainerViewSet):
    SUPERUSER_RULE_ID = ["0", "-1"]
    ORDERING_FIELD = "-id"

    def filter_rules(self, rules):
        """根据规则过滤查询集"""
        if not rules:
            return []

        if len(rules) == 1 and isinstance(rules[0], dict) and str(rules[0].get("id")) in self.SUPERUSER_RULE_ID:
            return []

        rule_ids = []
        for rule in rules:
            if isinstance(rule, dict) and "id" in rule:
                rule_ids.append(int(rule["id"]))
        if -1 in rule_ids or 0 in rule_ids:
            return []
        return rule_ids

    def list(self, request, *args, **kwargs):
        """重写列表方法以支持权限过滤"""
        try:
            queryset = self.filter_queryset(self.get_queryset())
            return self.query_by_groups(request, queryset)
        except Exception as e:
            logger.error(f"Error in list method: {e}")
            raise

    def query_by_groups(self, request, queryset):
        """根据用户组权限过滤查询结果"""
        try:
            user = getattr(request, "user", None)
            if not user:
                return self.value_error(_("User not found in request"))

            if getattr(user, "is_superuser", False):
                return self._list(queryset.order_by(self.ORDERING_FIELD))
            current_team = request.COOKIES.get("current_team", "0")
            fields = [i.name for i in queryset.model._meta.fields]
            if "created_by" in fields:
                query = Q(
                    team__contains=int(current_team), created_by=request.user.username, domain=request.user.domain
                )
            else:
                query = Q()

            if hasattr(self, "permission_key"):
                app_name = self._get_app_name()
                permission_data = get_permission_rules(user, current_team, app_name, self.permission_key)
                instance_ids = [i["id"] for i in permission_data.get("instance", [])]
                team = permission_data.get("team", [])
                if instance_ids:
                    query |= Q(id__in=instance_ids)
                for i in team:
                    query |= Q(team__contains=int(i))
            queryset = queryset.filter(query)
            return self._list(queryset.order_by(self.ORDERING_FIELD))

        except Exception as e:
            logger.error(f"Error in query_by_groups: {e}")
            raise

    def _filter_by_user_groups(self, queryset, current_team):
        """根据用户组过滤查询集"""
        query = Q()

        try:
            if not current_team:
                return query
            teams = [i.strip() for i in current_team.split(",") if i.strip()]
            for i in teams:
                query |= Q(team__contains=int(i))
            return query

        except Exception as e:
            logger.error(f"Error filtering by user groups: {e}")
            return query

    def _list(self, queryset):
        """统一的列表响应处理"""
        try:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        except Exception as e:
            logger.error(f"Error in _list method: {e}")
            raise

    def retrieve(self, request, *args, **kwargs):
        user = getattr(request, "user", None)
        instance = self.get_object()
        if getattr(user, "is_superuser", False):
            return super().retrieve(request, *args, **kwargs)
        if hasattr(self, "permission_key"):
            current_team = request.COOKIES.get("current_team", "0")
            has_permission = self.get_has_permission(user, instance, current_team, is_check=True)
            if not has_permission:
                return self.value_error(_("User does not have permission to view this instance"))
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @staticmethod
    def value_error(msg):
        return JsonResponse({"result": False, "message": msg})

    def destroy(self, request, *args, **kwargs):
        user = getattr(request, "user", None)
        instance = self.get_object()
        if getattr(user, "is_superuser", False):
            return super().destroy(request, *args, **kwargs)
        if hasattr(self, "permission_key"):
            current_team = request.COOKIES.get("current_team", "0")
            has_permission = self.get_has_permission(user, instance, current_team)
            if not has_permission:
                return self.value_error(_("User does not have permission to delete this instance"))
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """重写更新方法以支持权限控制"""
        try:
            user = getattr(request, "user", None)
            partial = kwargs.pop("partial", False)
            data = request.data
            instance = self.get_object()

            if getattr(user, "is_superuser", False):
                return super().update(request, *args, **kwargs)
            if "team" in data:
                data.pop("team", None)
            current_team = int(request.COOKIES.get("current_team", None))
            if current_team not in instance.team:
                return self.value_error(_("User does not have permission to update this instance"))
            if hasattr(self, "permission_key"):
                has_permission = self.get_has_permission(user, instance, current_team)
                if not has_permission:
                    return self.value_error(_("User does not have permission to update this instance"))
            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, "_prefetched_objects_cache", None):
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)

        except Exception as e:
            logger.error(f"Error in update method: {e}")
            raise

    def get_has_permission(self, user, instance, current_team, is_list=False, is_check=False):
        """获取规则实例ID"""
        user_groups = [int(i["id"]) for i in user.group_list]
        if is_list:
            instance_id = list(instance.values_list("id", flat=True))
            for i in instance:
                if hasattr(i, "team"):
                    # 判断两个集合是否有交集
                    if not set(i.team).intersection(set(user_groups)):
                        return False
        else:
            if hasattr(instance, "team"):
                if not set(instance.team).intersection(set(user_groups)):
                    return False
            instance_id = [instance.id]
        try:
            app_name = self._get_app_name()
            permission_rules = get_permission_rules(user, current_team, app_name, self.permission_key)
            if int(current_team) in permission_rules["team"]:
                return True

            operate = "View" if is_check else "Operate"
            instance_list = [int(i["id"]) for i in permission_rules["instance"] if operate in i["permission"]]
            return set(instance_id).issubset(set(instance_list))
        except Exception as e:
            logger.error(f"Error getting rule instances: {e}")
            return False

    def _validate_name(self, name, group_list, team, exclude_id=None):
        """验证名称在团队中的唯一性"""
        try:
            if not name or not isinstance(name, str):
                return ""

            if not isinstance(group_list, list) or not isinstance(team, list):
                return ""

            queryset = self.queryset.filter(name=name)
            if exclude_id:
                queryset = queryset.exclude(id=exclude_id)

            team_list = list(queryset.values_list("team", flat=True))
            existing_teams = []

            for team_data in team_list:
                if isinstance(team_data, list):
                    existing_teams.extend(team_data)

            team_name_map = {}
            for group in group_list:
                if isinstance(group, dict) and "id" in group and "name" in group:
                    team_name_map[group["id"]] = group["name"]

            for team_id in team:
                if team_id in existing_teams:
                    conflict_team_name = team_name_map.get(team_id, f"Team-{team_id}")
                    return conflict_team_name

            return ""

        except Exception as e:
            logger.error(f"Error in _validate_name: {e}")
            return ""

    def _get_app_name(self):
        """获取当前序列化器所属的应用名称"""
        module_path = self.__class__.__module__
        if "apps." in module_path:
            parts = module_path.split(".")
            if len(parts) >= 2 and parts[0] == "apps":
                return parts[1]
        return None

import logging

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response

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
                raise ValueError("User not found in request")

            if getattr(user, "is_superuser", False):
                return self._list(queryset.order_by(self.ORDERING_FIELD))
            query = Q()
            instance_ids = []
            if hasattr(self, "permission_key"):
                guest_rules, normal_rules = self._get_permission_rules(user)
                instance_ids = self.filter_rules(normal_rules)

                if guest_rules:
                    guest_instance_ids = self.filter_rules(guest_rules)
                    query |= Q(id__in=guest_instance_ids)
            group_query = self._filter_by_user_groups(user, queryset)
            if instance_ids:
                queryset = queryset.filter(id__in=instance_ids)
            queryset = queryset.filter(query | group_query)
            return self._list(queryset.order_by(self.ORDERING_FIELD))

        except Exception as e:
            logger.error(f"Error in query_by_groups: {e}")
            raise

    def _get_permission_rules(self, user):
        """获取用户权限规则"""
        try:
            app_name_map = {
                "system_mgmt": "system-manager",
                "node_mgmt": "node",
                "console_mgmt": "ops-console",
                "mlops": "mlops",
            }
            app_name = self._get_app_name()
            app_name = app_name_map.get(app_name, app_name)
            user_rules = getattr(user, "rules", {}).get(app_name, {})
            if not isinstance(user_rules, dict):
                return {}, {}
            guest_rules_map = user_rules.get("guest", {})
            normal_rules_map = user_rules.get("normal", {})
            if "." in self.permission_key:
                keys = self.permission_key.split(".", 1)
                guest_rules = guest_rules_map.get(keys[0], {})
                normal_rules = normal_rules_map.get(keys[0], {})
                if isinstance(guest_rules, dict) and len(keys) > 1:
                    guest_rules = guest_rules.get(keys[1], [])
                if isinstance(normal_rules, dict) and len(keys) > 1:
                    normal_rules = normal_rules.get(keys[1], [])
            else:
                guest_rules = guest_rules_map.get(self.permission_key, [])
                normal_rules = normal_rules_map.get(self.permission_key, [])

            return guest_rules, normal_rules

        except Exception as e:
            logger.error(f"Error getting permission rules: {e}")
            return {}, {}

    def _filter_by_user_groups(self, user, queryset):
        """根据用户组过滤查询集"""
        query = Q()

        try:
            group_list = getattr(user, "group_list", [])
            if not isinstance(group_list, list):
                return query

            team_ids = []
            for group in group_list:
                if isinstance(group, dict) and "id" in group:
                    team_ids.append(group["id"])

            if not team_ids:
                return query

            for team_id in team_ids:
                query |= Q(team__contains=team_id)

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

    def update(self, request, *args, **kwargs):
        """重写更新方法以支持权限控制"""
        try:
            partial = kwargs.pop("partial", False)
            data = request.data.copy() if hasattr(request.data, "copy") else dict(request.data)
            instance = self.get_object()

            user = getattr(request, "user", None)
            if not user:
                raise ValueError("User not found in request")

            if not getattr(user, "is_superuser", False) and getattr(instance, "created_by", None) != getattr(
                user, "username", None
            ):
                if "team" in data:
                    data.pop("team", None)

            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, "_prefetched_objects_cache", None):
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)

        except Exception as e:
            logger.error(f"Error in update method: {e}")
            raise

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

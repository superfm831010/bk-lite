import logging
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class MaintainerViewSet(viewsets.ModelViewSet):
    # 常量定义
    DEFAULT_USERNAME = "guest"
    
    def perform_create(self, serializer):
        """创建时补充基础Model中的字段"""
        try:
            request = serializer.context.get("request")
            if not request:
                logger.warning("No request found in serializer context")
                return super().perform_create(serializer)
                
            user = getattr(request, "user", None)
            username = getattr(user, "username", self.DEFAULT_USERNAME)
            
            model = serializer.Meta.model
            if hasattr(model, "created_by"):
                logger.info(f"Creating {model.__name__} instance by user: {username}")
                serializer.save(created_by=username, updated_by=username)
            else:
                logger.debug(f"Model {model.__name__} does not have created_by field")
                
        except Exception as e:
            logger.error(f"Error in perform_create: {e}")
            raise
            
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        """更新时补充基础Model中的字段"""
        try:
            request = serializer.context.get("request")
            if not request:
                logger.warning("No request found in serializer context")
                return super().perform_update(serializer)
                
            user = getattr(request, "user", None)
            username = getattr(user, "username", self.DEFAULT_USERNAME)
            
            model = serializer.Meta.model
            if hasattr(model, "updated_by"):
                logger.info(f"Updating {model.__name__} instance by user: {username}")
                serializer.save(updated_by=username)
            else:
                logger.debug(f"Model {model.__name__} does not have updated_by field")
                
        except Exception as e:
            logger.error(f"Error in perform_update: {e}")
            raise
            
        return super().perform_update(serializer)


class AuthViewSet(MaintainerViewSet):
    # 常量定义
    SUPERUSER_RULE_ID = "0"
    ORDERING_FIELD = "-id"
    
    def filter_rules(self, queryset, rules):
        """根据规则过滤查询集"""
        if not rules:
            logger.debug("No rules provided, returning original queryset")
            return queryset
            
        if (len(rules) == 1 and 
            isinstance(rules[0], dict) and 
            str(rules[0].get("id")) == self.SUPERUSER_RULE_ID):
            logger.debug("Superuser rule detected, returning full queryset")
            return queryset
            
        # 提取规则ID并验证
        rule_ids = []
        for rule in rules:
            if isinstance(rule, dict) and "id" in rule:
                rule_ids.append(rule["id"])
            else:
                logger.warning(f"Invalid rule format: {rule}")
                
        logger.info(f"Filtering queryset with rule IDs: {rule_ids}")
        return queryset.filter(id__in=rule_ids)

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
                logger.error("No user found in request")
                raise ValueError("User not found in request")
                
            if getattr(user, "is_superuser", False):
                logger.info("Superuser access detected, returning full queryset")
                return self._list(queryset.order_by(self.ORDERING_FIELD))
            
            # 处理权限规则
            if hasattr(self, "permission_key"):
                rules = self._get_permission_rules(user)
                queryset = self.filter_rules(queryset, rules)
            
            # 处理用户组过滤
            queryset = self._filter_by_user_groups(user, queryset)
            
            return self._list(queryset.order_by(self.ORDERING_FIELD))
            
        except Exception as e:
            logger.error(f"Error in query_by_groups: {e}")
            raise
    
    def _get_permission_rules(self, user):
        """获取用户权限规则"""
        try:
            user_rules = getattr(user, "rules", {})
            if not isinstance(user_rules, dict):
                logger.warning(f"User rules is not a dict: {type(user_rules)}")
                return []
                
            if "." in self.permission_key:
                keys = self.permission_key.split(".", 1)  # 限制分割次数
                rules = user_rules.get(keys[0], {})
                if isinstance(rules, dict) and len(keys) > 1:
                    rules = rules.get(keys[1], [])
            else:
                rules = user_rules.get(self.permission_key, [])
                
            logger.debug(f"Retrieved rules for permission_key {self.permission_key}: {len(rules) if isinstance(rules, list) else 'not a list'}")
            return rules if isinstance(rules, list) else []
            
        except Exception as e:
            logger.error(f"Error getting permission rules: {e}")
            return []
    
    def _filter_by_user_groups(self, user, queryset):
        """根据用户组过滤查询集"""
        try:
            group_list = getattr(user, "group_list", [])
            if not isinstance(group_list, list):
                logger.warning(f"User group_list is not a list: {type(group_list)}")
                return queryset
                
            team_ids = []
            for group in group_list:
                if isinstance(group, dict) and "id" in group:
                    team_ids.append(group["id"])
                else:
                    logger.warning(f"Invalid group format: {group}")
            
            if not team_ids:
                logger.warning("No valid team IDs found in user groups")
                return queryset
                
            logger.info(f"Filtering by team IDs: {team_ids}")
            query = Q()
            for team_id in team_ids:
                query |= Q(team__contains=team_id)
            
            return queryset.filter(query)
            
        except Exception as e:
            logger.error(f"Error filtering by user groups: {e}")
            return queryset

    def _list(self, queryset):
        """统一的列表响应处理"""
        try:
            page = self.paginate_queryset(queryset)
            if page is not None:
                logger.debug(f"Returning paginated response with {len(page)} items")
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            logger.debug(f"Returning non-paginated response with {queryset.count()} items")
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error in _list method: {e}")
            raise

    def update(self, request, *args, **kwargs):
        """重写更新方法以支持权限控制"""
        try:
            partial = kwargs.pop("partial", False)
            data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
            instance = self.get_object()
            
            user = getattr(request, "user", None)
            if not user:
                logger.error("No user found in request for update operation")
                raise ValueError("User not found in request")
            
            # 权限检查：非超级用户且非创建者不能修改团队信息
            if (not getattr(user, "is_superuser", False) and 
                getattr(instance, "created_by", None) != getattr(user, "username", None)):
                if "team" in data:
                    logger.warning(f"User {getattr(user, 'username', 'unknown')} attempted to modify team field without permission")
                    data.pop("team", None)
            
            logger.info(f"Updating instance {instance.id} by user {getattr(user, 'username', 'unknown')}")
            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            # 清除预取对象缓存
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
                logger.warning(f"Invalid name parameter: {name}")
                return ""
                
            if not isinstance(group_list, list):
                logger.warning(f"Invalid group_list parameter: {type(group_list)}")
                return ""
                
            if not isinstance(team, list):
                logger.warning(f"Invalid team parameter: {type(team)}")
                return ""
            
            queryset = self.queryset.filter(name=name)
            if exclude_id:
                queryset = queryset.exclude(id=exclude_id)
            
            team_list = list(queryset.values_list("team", flat=True))
            existing_teams = []
            
            for team_data in team_list:
                if isinstance(team_data, list):
                    existing_teams.extend(team_data)
                elif team_data is not None:
                    logger.warning(f"Unexpected team data format: {type(team_data)}")
            
            # 构建团队名称映射
            team_name_map = {}
            for group in group_list:
                if isinstance(group, dict) and "id" in group and "name" in group:
                    team_name_map[group["id"]] = group["name"]
                else:
                    logger.warning(f"Invalid group format in group_list: {group}")
            
            # 检查冲突
            for team_id in team:
                if team_id in existing_teams:
                    conflict_team_name = team_name_map.get(team_id, f"Team-{team_id}")
                    logger.warning(f"Name conflict detected for '{name}' in team '{conflict_team_name}'")
                    return conflict_team_name
            
            logger.debug(f"Name validation passed for '{name}'")
            return ""
            
        except Exception as e:
            logger.error(f"Error in _validate_name: {e}")
            return ""

import logging
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.core.services.user_group import UserGroup
from apps.core.utils.web_utils import WebUtils
from apps.rpc.system_mgmt import SystemMgmt

logger = logging.getLogger(__name__)


class UserGroupViewSet(viewsets.ViewSet):

    def __init__(self, *args, **kwargs):
        super(UserGroupViewSet, self).__init__(*args, **kwargs)
        self.system_mgmt_client = SystemMgmt()

    def get_first_and_max(self, params):
        """格式化page参数, 获取first与max"""
        try:
            page = max(1, int(params.get("page", 1)))
            page_size = max(1, min(100, int(params.get("page_size", 20))))  # 限制最大页面大小
            _first = (page - 1) * page_size
            _max = page_size
            return _first, _max
        except (ValueError, TypeError):
            logger.warning(f"Invalid pagination parameters: page={params.get('page')}, page_size={params.get('page_size')}")
            return 0, 20

    @swagger_auto_schema(
        operation_id="user_list",
        operation_description="查询用户列表",
        manual_parameters=[
            openapi.Parameter("page", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("page_size", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("search", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ],
    )
    @action(methods=["get"], detail=False)
    def user_list(self, request):
        try:
            _first, _max = self.get_first_and_max(request.query_params)
            search_term = request.query_params.get("search", "").strip()
            
            data = UserGroup().user_list(
                self.system_mgmt_client, 
                query_params={
                    "first": _first, 
                    "max": _max,
                    "search": search_term
                }
            )
            return WebUtils.response_success(data)
        except Exception as e:
            logger.error(f"Failed to fetch user list: {str(e)}")
            return WebUtils.response_error("获取用户列表失败")

    @swagger_auto_schema(
        operation_id="group_list",
        operation_description="组列表",
        manual_parameters=[
            openapi.Parameter("search", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ],
    )
    @action(methods=["get"], detail=False)
    def group_list(self, request):
        try:
            search_term = request.query_params.get("search", "").strip()
            
            data = UserGroup().groups_list(
                system_mgmt_client=self.system_mgmt_client,
                query_params=search_term
            )
            return WebUtils.response_success(data)
        except Exception as e:
            logger.error(f"Failed to fetch group list: {str(e)}")
            return WebUtils.response_error("获取组列表失败")

    @swagger_auto_schema(
        operation_id="user_groups",
        operation_description="用户组列表",
    )
    @action(methods=["get"], detail=False)
    def user_groups(self, request):
        try:
            data = UserGroup().user_groups_list(request)
            return WebUtils.response_success(data)
        except Exception as e:
            logger.error(f"Failed to fetch user groups: {str(e)}")
            return WebUtils.response_error("获取用户组列表失败")

import logging
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from django.utils.translation import gettext as _

from apps.core.services.user_group import UserGroup
from apps.core.utils.web_utils import WebUtils
from apps.rpc.system_mgmt import SystemMgmt

# 配置日志
logger = logging.getLogger(__name__)

# 常量定义
DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 20
MIN_PAGE = 1
MIN_PAGE_SIZE = 1
MAX_PAGE_SIZE = 100
EMPTY_STRING = ""

# 错误消息常量
ERROR_MSG_INVALID_PAGE = _("Invalid page parameter")
ERROR_MSG_INVALID_PAGE_SIZE = _("Invalid page_size parameter") 
ERROR_MSG_SYSTEM_ERROR = _("System error occurred")


class UserGroupViewSet(viewsets.ViewSet):

    def __init__(self, *args, **kwargs):
        super(UserGroupViewSet, self).__init__(*args, **kwargs)
        self.system_mgmt_client = self._create_system_mgmt_client()

    def _create_system_mgmt_client(self):
        """创建SystemMgmt客户端的工厂方法"""
        try:
            client = SystemMgmt()
            logger.info("SystemMgmt client created successfully in UserGroupViewSet")
            return client
        except Exception as e:
            logger.error(f"Failed to create SystemMgmt client in UserGroupViewSet: {str(e)}")
            raise

    def get_first_and_max(self, params):
        """格式化page参数, 获取first与max"""
        try:
            page = int(params.get("page", DEFAULT_PAGE))
            page_size = int(params.get("page_size", DEFAULT_PAGE_SIZE))
            
            # 参数验证
            if page < MIN_PAGE:
                logger.warning(f"Invalid page parameter: {page}, using default: {DEFAULT_PAGE}")
                page = DEFAULT_PAGE
                
            if page_size < MIN_PAGE_SIZE or page_size > MAX_PAGE_SIZE:
                logger.warning(f"Invalid page_size parameter: {page_size}, using default: {DEFAULT_PAGE_SIZE}")
                page_size = DEFAULT_PAGE_SIZE
            
            _first = (page - 1) * page_size
            _max = page_size
            
            logger.debug(f"Pagination calculated: page={page}, page_size={page_size}, first={_first}, max={_max}")
            return _first, _max
            
        except (ValueError, TypeError) as e:
            logger.warning(f"Error parsing pagination parameters: {str(e)}, using defaults")
            _first = (DEFAULT_PAGE - 1) * DEFAULT_PAGE_SIZE
            _max = DEFAULT_PAGE_SIZE
            return _first, _max

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
        logger.info(f"User list requested by user: {getattr(request.user, 'username', 'anonymous')}")
        
        try:
            _first, _max = self.get_first_and_max(request.query_params)
            search_term = request.query_params.get("search", EMPTY_STRING).strip()
            
            logger.info(f"Fetching user list with parameters: first={_first}, max={_max}, search='{search_term}'")
            
            query_params = {
                "first": _first,
                "max": _max,
                "search": search_term
            }
            
            data = UserGroup().user_list(self.system_mgmt_client, query_params=query_params)
            logger.info("User list retrieved successfully")
            
            return WebUtils.response_success(data)
            
        except Exception as e:
            logger.error(f"Error retrieving user list: {str(e)}")
            return WebUtils.response_error(ERROR_MSG_SYSTEM_ERROR)

    @swagger_auto_schema(
        operation_id="group_list",
        operation_description="组列表",
        manual_parameters=[
            openapi.Parameter("search", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ],
    )
    @action(methods=["get"], detail=False)
    def group_list(self, request):
        logger.info(f"Group list requested by user: {getattr(request.user, 'username', 'anonymous')}")
        
        try:
            search_term = request.GET.get("search", EMPTY_STRING).strip()
            logger.info(f"Fetching group list with search term: '{search_term}'")
            
            data = UserGroup().groups_list(
                system_mgmt_client=self.system_mgmt_client,
                query_params=search_term if search_term else None
            )
            logger.info("Group list retrieved successfully")
            
            return WebUtils.response_success(data)
            
        except Exception as e:
            logger.error(f"Error retrieving group list: {str(e)}")
            return WebUtils.response_error(ERROR_MSG_SYSTEM_ERROR)

    @swagger_auto_schema(
        operation_id="user_groups",
        operation_description="用户组列表",
    )
    @action(methods=["get"], detail=False)
    def user_groups(self, request):
        logger.info(f"User groups requested by user: {getattr(request.user, 'username', 'anonymous')}")
        
        try:
            data = UserGroup().user_groups_list(request)
            logger.info("User groups retrieved successfully")
            
            return WebUtils.response_success(data)
            
        except Exception as e:
            logger.error(f"Error retrieving user groups: {str(e)}")
            return WebUtils.response_error(ERROR_MSG_SYSTEM_ERROR)

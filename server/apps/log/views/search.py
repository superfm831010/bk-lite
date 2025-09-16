from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet, ModelViewSet

from apps.core.utils.web_utils import WebUtils
from apps.log.services.search import SearchService
from apps.log.utils.log_group import LogGroupQueryBuilder
from apps.log.models.log_group import SearchCondition
from apps.log.serializers.log_group import SearchConditionSerializer
from apps.log.filters.log_group import SearchConditionFilter


class LogSearchViewSet(ViewSet):

    @swagger_auto_schema(
        operation_description="search field_names",
        manual_parameters=[
            openapi.Parameter('filed', openapi.IN_QUERY, description="Search filed", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('start_time', openapi.IN_QUERY, description="Start time for the search", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('end_time', openapi.IN_QUERY, description="End time for the search", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('limit', openapi.IN_QUERY, description="Number of results to return", type=openapi.TYPE_INTEGER, default=100),
        ],
    )
    @action(methods=['get'], detail=False, url_path='field_names')
    def field_names(self, request):
        """
        Search available log field_names.
        """
        field = request.query_params.get('filed', '')
        start_time = request.query_params.get('start_time', '')
        end_time = request.query_params.get('end_time', '')
        limit = int(request.query_params.get('limit', 100))

        if not field:
            return WebUtils.response_error("Field parameter is required.")

        data = SearchService.field_names(field, start_time, end_time, limit)
        return WebUtils.response_success(data)

    @swagger_auto_schema(
        operation_description="Search logs",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "query": openapi.Schema(type=openapi.TYPE_STRING, description="Search query"),
                "start_time": openapi.Schema(type=openapi.TYPE_STRING, description="Start time for the search"),
                "end_time": openapi.Schema(type=openapi.TYPE_STRING, description="End time for the search"),
                "limit": openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of results to return", default=10),
                "log_groups": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING, description="Log group IDs"),
                    description="List of log group IDs to filter the search"
                ),
            },
            required=["query", "log_groups"]
        ),
        tags=['LogSearch']
    )
    @action(methods=['post'], detail=False, url_path='search')
    def search(self, request):
        """
        Search logs based on the provided query parameters.
        """
        query = request.data.get('query', '')
        start_time = request.data.get('start_time', '')
        end_time = request.data.get('end_time', '')
        limit = request.data.get('limit', 10)
        log_groups = request.data.get('log_groups', [])

        if not query:
            return WebUtils.response_error("Query parameter is required.")

        # 验证日志分组
        is_valid, error_msg, _ = LogGroupQueryBuilder.validate_log_groups(log_groups)
        if not is_valid:
            return WebUtils.response_error(error_msg)

        data = SearchService.search_logs(query, start_time, end_time, limit, log_groups)
        return WebUtils.response_success(data)

    @swagger_auto_schema(
        operation_description="Search hits",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "query": openapi.Schema(type=openapi.TYPE_STRING, description="Search query"),
                "start_time": openapi.Schema(type=openapi.TYPE_STRING, description="Start time for the search"),
                "end_time": openapi.Schema(type=openapi.TYPE_STRING, description="End time for the search"),
                "field": openapi.Schema(type=openapi.TYPE_STRING, description="Field to search hits in"),
                "fields_limit": openapi.Schema(type=openapi.TYPE_INTEGER, description="Limit of fields to return", default=5),
                "step": openapi.Schema(type=openapi.TYPE_STRING, description="Step interval for hits", default='5m'),
                "log_groups": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING, description="Log group IDs"),
                    description="List of log group IDs to filter the search"
                ),
            },
            required=["query", "field", "log_groups"]
        ),
        tags=['LogSearch']
    )
    @action(methods=['post'], detail=False, url_path='hits')
    def hits(self, request):
        """
        Search hits based on the provided query parameters.
        """
        query = request.data.get('query', '')
        start_time = request.data.get('start_time', '')
        end_time = request.data.get('end_time', '')
        field = request.data.get('field', '')
        fields_limit = request.data.get('fields_limit', 5)
        step = request.data.get('step', '5m')
        log_groups = request.data.get('log_groups', [])

        if not query or not field:
            return WebUtils.response_error("Query and field parameters are required.")

        # 验证日志分组
        is_valid, error_msg, _ = LogGroupQueryBuilder.validate_log_groups(log_groups)
        if not is_valid:
            return WebUtils.response_error(error_msg)

        data = SearchService.search_hits(query, start_time, end_time, field, fields_limit, step, log_groups)
        return WebUtils.response_success(data)

    @swagger_auto_schema(
        operation_description="Tail logs",
        manual_parameters=[
            openapi.Parameter('query', openapi.IN_QUERY, description="Query to filter logs", type=openapi.TYPE_STRING),
            openapi.Parameter('log_groups', openapi.IN_QUERY, description="Comma-separated log group IDs", type=openapi.TYPE_STRING)
        ],
        tags=['LogSearch']
    )
    @action(methods=['get'], detail=False, url_path='tail')
    def tail_logs(self, request):
        """
        实现长连接接口，用于实时获取日志数据
        """
        query = request.query_params.get("query", "")
        log_groups_param = request.query_params.get("log_groups", "")

        # 解析log_groups参数
        log_groups = []
        if log_groups_param:
            log_groups = [group.strip() for group in log_groups_param.split(',') if group.strip()]

        if not log_groups:
            return WebUtils.response_error("log_groups parameter is required.")

        if not query:
            return WebUtils.response_error("Query parameters are required.")

        # 验证日志分组
        is_valid, error_msg, _ = LogGroupQueryBuilder.validate_log_groups(log_groups)
        if not is_valid:
            return WebUtils.response_error(error_msg)

        return SearchService.tail(query, log_groups)

class SearchConditionViewSet(ModelViewSet):
    """搜索条件管理ViewSet"""
    queryset = SearchCondition.objects.all()
    serializer_class = SearchConditionSerializer
    filterset_class = SearchConditionFilter

    def get_queryset(self):
        """根据当前组织过滤查询集"""
        current_team = self.request.COOKIES.get("current_team")
        if current_team:
            return SearchCondition.objects.filter(organization=int(current_team))
        return SearchCondition.objects.none()

    @swagger_auto_schema(
        operation_description="创建搜索条件",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="搜索条件名称"),
                "condition": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="搜索条件配置",
                    example={
                        "query": "error",
                        "log_groups": ["log-group-1", "log-group-2"],
                        "time_range": {"start": "2024-01-01T00:00:00Z", "end": "2024-01-02T00:00:00Z"},
                        "filters": {"level": "error"}
                    }
                ),
            },
            required=["name", "condition"]
        ),
        tags=['SearchCondition']
    )
    def create(self, request, *args, **kwargs):
        """创建搜索条件"""
        current_team = request.COOKIES.get("current_team")
        if not current_team:
            return WebUtils.response_error("当前组织信息不存在，请重新登录")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 设置创建者和组织
        serializer.validated_data['created_by'] = request.user.username
        serializer.validated_data['organization'] = int(current_team)

        search_condition = serializer.save()

        return WebUtils.response_success({
            "id": search_condition.id,
            "name": search_condition.name,
            "message": "搜索条件创建成功"
        })

    @swagger_auto_schema(
        operation_description="获取搜索条件列表",
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, description="按名称过滤", type=openapi.TYPE_STRING),
            openapi.Parameter('created_by', openapi.IN_QUERY, description="按创建者过滤", type=openapi.TYPE_STRING),
        ],
        tags=['SearchCondition']
    )
    def list(self, request, *args, **kwargs):
        """获取搜索条件列表"""
        current_team = request.COOKIES.get("current_team")
        if not current_team:
            return WebUtils.response_error("当前组织信息不存在，请重新登录")

        queryset = self.filter_queryset(self.get_queryset())

        # 分页处理
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return WebUtils.response_success(serializer.data)

    @swagger_auto_schema(
        operation_description="获取搜索条件详情",
        tags=['SearchCondition']
    )
    def retrieve(self, request, *args, **kwargs):
        """获取搜索条件详情"""
        current_team = request.COOKIES.get("current_team")
        if not current_team:
            return WebUtils.response_error("当前组织信息不存在，请重新登录")

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return WebUtils.response_success(serializer.data)

    @swagger_auto_schema(
        operation_description="更新搜索条件",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="搜索条件名称"),
                "condition": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="搜索条件配置",
                    example={
                        "query": "error",
                        "log_groups": ["log-group-1", "log-group-2"],
                        "time_range": {"start": "2024-01-01T00:00:00Z", "end": "2024-01-02T00:00:00Z"},
                        "filters": {"level": "error"}
                    }
                ),
            }
        ),
        tags=['SearchCondition']
    )
    def update(self, request, *args, **kwargs):
        """更新搜索条件"""
        current_team = request.COOKIES.get("current_team")
        if not current_team:
            return WebUtils.response_error("当前组织信息不存在，请重新登录")

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # 设置更新者（不允许修改组织）
        serializer.validated_data['updated_by'] = request.user.username

        search_condition = serializer.save()

        return WebUtils.response_success({
            "id": search_condition.id,
            "name": search_condition.name,
            "message": "搜索条件更新成功"
        })

    @swagger_auto_schema(
        operation_description="部分更新搜索条件",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="搜索条件名称"),
                "condition": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="搜索条件配置"
                ),
            }
        ),
        tags=['SearchCondition']
    )
    def partial_update(self, request, *args, **kwargs):
        """部分更新搜索条件"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="删除搜索条件",
        tags=['SearchCondition']
    )
    def destroy(self, request, *args, **kwargs):
        """删除搜索条件"""
        current_team = request.COOKIES.get("current_team")
        if not current_team:
            return WebUtils.response_error("当前组织信息不存在，请重新登录")

        instance = self.get_object()
        search_condition_name = instance.name
        instance.delete()

        return WebUtils.response_success({
            "message": f"搜索条件 '{search_condition_name}' 删除成功"
        })

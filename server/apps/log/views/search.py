from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

from apps.core.utils.web_utils import WebUtils
from apps.log.services.search import SearchService


class LogSearchViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Search logs",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "query": openapi.Schema(type=openapi.TYPE_STRING, description="Search query"),
                "start_time": openapi.Schema(type=openapi.TYPE_STRING, description="Start time for the search"),
                "end_time": openapi.Schema(type=openapi.TYPE_STRING, description="End time for the search"),
                "limit": openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of results to return", default=10),
            },
            required=["query"]
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

        if not query:
            return WebUtils.response_error("Query parameter is required.")

        data = SearchService.search_logs(query, start_time, end_time, limit)
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
            },
            required=["query", "field"]
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

        if not query or not field:
            return WebUtils.response_error("Query and field parameters are required.")

        data = SearchService.search_hits(query, start_time, end_time, field, fields_limit, step)
        return WebUtils.response_success(data)

    @swagger_auto_schema(
        operation_description="Tail logs",
        manual_parameters=[
            openapi.Parameter('query', openapi.IN_QUERY, description="Query to filter logs", type=openapi.TYPE_STRING)
        ],
        tags=['LogSearch']
    )
    @action(methods=['get'], detail=False, url_path='tail')
    def tail_logs(self, request):
        """
        实现长连接接口，用于实时获取日志数据
        """
        query = request.query_params.get("query", "")
        if not query:
            return WebUtils.response_error("Query parameters are required.")

        return SearchService.tail(query)

from django.http import StreamingHttpResponse

from apps.log.utils.query_log import VictoriaMetricsAPI
from apps.log.utils.log_group import LogGroupQueryBuilder


class SearchService:
    @staticmethod
    def search_logs(query, start_time, end_time, limit=10, log_groups=None):
        """搜索日志，支持日志分组过滤

        Args:
            query: 用户查询语句
            start_time: 开始时间
            end_time: 结束时间
            limit: 返回结果限制
            log_groups: 日志分组ID列表
        """
        # 处理日志分组规则
        final_query, group_info = LogGroupQueryBuilder.build_query_with_groups(query, log_groups)

        # Create an instance of the VictoriaMetricsAPI
        vm_api = VictoriaMetricsAPI()

        # Perform the query
        response = vm_api.query(final_query, start_time, end_time, limit)

        # 添加分组信息到响应中（用于调试）
        if isinstance(response, dict) and group_info:
            response['_log_group_info'] = group_info

        return response

    @staticmethod
    def search_hits(query, start_time, end_time, field, fields_limit=5, step="5m", log_groups=None):
        """搜索命中统计，支持日志分组过滤"""
        # 处理日志分组规则
        final_query, group_info = LogGroupQueryBuilder.build_query_with_groups(query, log_groups)

        # Create an instance of the VictoriaMetricsAPI
        vm_api = VictoriaMetricsAPI()

        # Perform the hits query
        response = vm_api.hits(final_query, start_time, end_time, field, fields_limit, step)

        # 添加分组信息到响应中（用于调试）
        if isinstance(response, dict) and group_info:
            response['_log_group_info'] = group_info

        return response

    @staticmethod
    def tail(query, log_groups=None):
        """实时日志流，支持日志分组过滤"""
        # 处理日志分组规则
        final_query, group_info = LogGroupQueryBuilder.build_query_with_groups(query, log_groups)

        def event_stream():
            api = VictoriaMetricsAPI()
            try:
                # 首先发送分组信息（如果有的话）
                if group_info:
                    yield f"event: group_info\ndata: {group_info}\n\n"

                for line in api.tail(final_query):
                    yield f"data: {line}\n\n"  # 格式化为 Server-Sent Events (SSE)
            except Exception as e:
                yield f"error: {str(e)}\n\n"

        response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
        response['Cache-Control'] = 'no-cache'
        return response

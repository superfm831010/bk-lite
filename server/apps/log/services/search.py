from django.http import StreamingHttpResponse
import time
import json

from apps.log.utils.query_log import VictoriaMetricsAPI
from apps.log.utils.log_group import LogGroupQueryBuilder
from apps.core.logger import log_logger as logger


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

        async def async_event_stream():
            api = VictoriaMetricsAPI()

            try:
                # 发送连接建立事件
                yield f"event: connection\ndata: {json.dumps({'status': 'connected', 'timestamp': int(time.time())})}\n\n"

                # 首先发送分组信息（如果有的话）
                if group_info:
                    yield f"event: group_info\ndata: {json.dumps(group_info)}\n\n"

                # 使用异步tail方法
                last_heartbeat = time.time()
                heartbeat_interval = 30  # 30秒心跳间隔

                async for line in api.tail_async(final_query):
                    current_time = time.time()

                    # 发送心跳保持连接
                    if current_time - last_heartbeat > heartbeat_interval:
                        yield f"event: heartbeat\ndata: {json.dumps({'timestamp': int(current_time)})}\n\n"
                        last_heartbeat = current_time

                    yield f"data: {line}\n\n"

            except Exception as e:
                logger.error("SSE tail连接异常", extra={'error': str(e)})
                error_data = {
                    'type': 'error',
                    'message': str(e),
                    'timestamp': int(time.time())
                }
                yield f"event: error\ndata: {json.dumps(error_data)}\n\n"

        response = StreamingHttpResponse(async_event_stream(), content_type="text/event-stream")
        # 关键的防缓冲响应头
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'  # HTTP/1.0兼容
        response['Expires'] = '0'
        response['X-Accel-Buffering'] = 'no'  # 防止Nginx缓冲
        response['Connection'] = 'keep-alive'

        return response

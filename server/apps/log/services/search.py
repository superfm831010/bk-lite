from django.http import StreamingHttpResponse
import time

from apps.log.utils.query_log import VictoriaMetricsAPI
from apps.log.utils.log_group import LogGroupQueryBuilder
from apps.log.constants import SSE_MAX_CONNECTION_TIME, SSE_KEEPALIVE_INTERVAL
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

        def sync_event_stream():
            api = VictoriaMetricsAPI()
            connection_start_time = time.time()
            max_connection_time = SSE_MAX_CONNECTION_TIME
            data_count = 0  # 在开始就初始化，避免作用域问题

            try:
                last_data_time = time.time()
                keepalive_interval = SSE_KEEPALIVE_INTERVAL

                for line in api.tail(final_query):
                    current_time = time.time()

                    # 检查连接是否超过最大时间限制
                    if current_time - connection_start_time > max_connection_time:
                        logger.info("SSE tail连接达到最大时间限制，主动断开", extra={
                            'duration': current_time - connection_start_time,
                            'data_sent': data_count
                        })
                        break

                    # 检查是否需要发送保活信号（仅在长时间无数据时）
                    if current_time - last_data_time > keepalive_interval:
                        try:
                            yield ": keepalive\n\n"
                            last_data_time = current_time
                        except (BrokenPipeError, ConnectionResetError, OSError):
                            logger.info("检测到客户端连接断开，停止SSE流", extra={
                                'duration': current_time - connection_start_time,
                                'data_sent': data_count
                            })
                            break

                    try:
                        yield f"data: {line}\n\n"
                        data_count += 1
                        last_data_time = current_time
                    except (BrokenPipeError, ConnectionResetError, OSError):
                        logger.info("检测到客户端连接断开，停止SSE流", extra={
                            'duration': current_time - connection_start_time,
                            'data_sent': data_count
                        })
                        break

            except Exception as e:
                logger.error("SSE tail连接异常", extra={'error': str(e)})
            finally:
                connection_duration = time.time() - connection_start_time
                logger.info("SSE tail连接结束", extra={
                    'duration': connection_duration,
                    'data_sent': data_count
                })

        response = StreamingHttpResponse(sync_event_stream(), content_type="text/event-stream")
        # 关键的防缓冲响应头
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        response['X-Accel-Buffering'] = 'no'

        return response

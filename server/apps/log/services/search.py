from django.http import StreamingHttpResponse

from apps.log.utils.query_log import VictoriaMetricsAPI


class SearchService:
    @staticmethod
    def search_logs(query, start_time, end_time, limit=10):

        # Create an instance of the VictoriaMetricsAPI
        vm_api = VictoriaMetricsAPI()

        # Perform the query
        response = vm_api.query(query, start_time, end_time, limit)

        return response

    @staticmethod
    def search_hits(query, start_time, end_time, field, fields_limit=5, step="5m"):
        # Create an instance of the VictoriaMetricsAPI
        vm_api = VictoriaMetricsAPI()

        # Perform the hits query
        response = vm_api.hits(query, start_time, end_time, field, fields_limit, step)

        return response

    @staticmethod
    def tail(query):
        def event_stream():
            api = VictoriaMetricsAPI()
            try:
                for line in api.tail(query):
                    yield f"data: {line}\n\n"  # 格式化为 Server-Sent Events (SSE)
            except Exception as e:
                yield f"error: {str(e)}\n\n"

        response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
        response['Cache-Control'] = 'no-cache'
        return response

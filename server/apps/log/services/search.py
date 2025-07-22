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

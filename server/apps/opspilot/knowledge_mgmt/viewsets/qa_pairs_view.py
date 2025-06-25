from django.http import JsonResponse
from rest_framework.decorators import action

from apps.core.utils.viewset_utils import AuthViewSet
from apps.opspilot.knowledge_mgmt.models import QAPairs
from apps.opspilot.knowledge_mgmt.serializers.qa_pairs_serializers import QAPairsSerializer
from apps.opspilot.utils.chunk_helper import ChunkHelper


class QAPairsViewSet(AuthViewSet):
    queryset = QAPairs.objects.all()
    serializer_class = QAPairsSerializer
    ordering = ("-id",)
    search_fields = ("name",)

    @action(methods=["GET"], detail=True)
    def get_details(self, request, *args, **kwargs):
        instance: QAPairs = self.get_object()
        client = ChunkHelper()
        page = request.query_params.get("page", 1)
        page_size = request.query_params.get("page_size", 10)
        search_text = request.query_params.get("search_text", "")
        metadata_filter = {"qa_pairs_id": str(instance.id)}
        index_name = instance.knowledge_base.knowledge_index_name()

        res = client.get_document_es_chunk(index_name, page, page_size, search_text, metadata_filter)
        if res["status"] != "success":
            return JsonResponse({"result": False, "message": res.get("message", "Failed to retrieve data.")})
        return_data = [
            {"question": i["page_content"], "answer": i["metadata"]["qa_answer"], "id": i["metadata"]["chunk_id"]}
            for i in res.get("documents", [])
        ]
        return JsonResponse({"result": True, "data": return_data, "count": res["count"]})

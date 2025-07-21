import json

from django.http import JsonResponse
from django_filters import filters
from django_filters.rest_framework import FilterSet
from rest_framework.decorators import action

from apps.core.utils.viewset_utils import MaintainerViewSet
from apps.opspilot.knowledge_mgmt.models import QAPairs
from apps.opspilot.knowledge_mgmt.serializers.qa_pairs_serializers import QAPairsSerializer
from apps.opspilot.tasks import create_qa_pairs, create_qa_pairs_by_json
from apps.opspilot.utils.chunk_helper import ChunkHelper


class QAPairsFilter(FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    knowledge_base_id = filters.NumberFilter(field_name="knowledge_base_id", lookup_expr="exact")


class QAPairsViewSet(MaintainerViewSet):
    queryset = QAPairs.objects.all()
    serializer_class = QAPairsSerializer
    filterset_class = QAPairsFilter
    ordering = ("-id",)

    @action(methods=["POST"], detail=False)
    def create_qa_pairs(self, request):
        params = request.data
        document_list = params.get("document_list", [])
        qa_list = []
        for i in document_list:
            qa_list.append(
                QAPairs(
                    name=i.get("name", ""),
                    knowledge_base_id=params["knowledge_base_id"],
                    llm_model_id=params["llm_model_id"],
                    qa_count=params.get("qa_count", 0),
                    document_id=i.get("document_id", 0),
                    document_source=i.get("document_source", "file"),
                    created_by=request.user.username,
                    domain=request.user.domain,
                )
            )
        add_list = QAPairs.objects.bulk_create(qa_list, batch_size=100)
        create_qa_pairs.delay(
            [instance.id for instance in add_list],
            params["llm_model_id"],
            params["qa_count"],
            params["knowledge_base_id"],
        )
        return JsonResponse({"result": True})

    @action(methods=["POST"], detail=False)
    def import_qa_json(self, request):
        files = request.FILES.getlist("file")
        if not files:
            return JsonResponse({"result": False, "message": "No file provided."})
        file_data = {}
        for i in files:
            try:
                file_data.setdefault(i.name, []).extend(json.loads(i.read().decode("utf-8")))
            except json.JSONDecodeError:
                return JsonResponse({"result": False, "message": f"Invalid JSON file: {i.name}"})
        params = request.data
        create_qa_pairs_by_json.delay(
            file_data, params["knowledge_base_id"], request.user.username, request.user.domain
        )
        return JsonResponse({"result": True, "message": "QA pairs import started."})

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
        return_data = [
            {"question": i["page_content"], "answer": i["metadata"]["qa_answer"], "id": i["metadata"]["chunk_id"]}
            for i in res.get("documents", [])
        ]
        return JsonResponse({"result": True, "data": {"items": return_data, "count": res["count"]}})

    @action(methods=["GET"], detail=False)
    def get_chunk_qa_pairs(self, request):
        """
        Get chunk QA pairs
        """
        index_name = request.GET.get("index_name", "")
        chunk_id = request.GET.get("chunk_id")
        res = ChunkHelper.get_document_es_chunk(
            index_name,
            1,
            10000,
            metadata_filter={"base_chunk_id": str(chunk_id)},
        )
        if res["status"] != "success":
            return JsonResponse({"result": False, "message": res.get("message", "Failed to retrieve data.")})
        return_data = [
            {"question": i["page_content"], "answer": i["metadata"]["qa_answer"], "id": i["metadata"]["chunk_id"]}
            for i in res.get("documents", [])
        ]
        return JsonResponse({"result": True, "data": return_data})

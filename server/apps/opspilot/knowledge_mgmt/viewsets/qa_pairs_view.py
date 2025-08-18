import json
import os

from django.http import HttpResponse, JsonResponse
from django.utils.translation import gettext as _
from django_filters import filters
from django_filters.rest_framework import FilterSet
from rest_framework.decorators import action

from apps.core.utils.viewset_utils import GenericViewSetFun, MaintainerViewSet
from apps.opspilot.knowledge_mgmt.models import QAPairs
from apps.opspilot.knowledge_mgmt.models.knowledge_task import KnowledgeTask
from apps.opspilot.knowledge_mgmt.serializers.qa_pairs_serializers import QAPairsSerializer
from apps.opspilot.tasks import (
    create_qa_pairs,
    create_qa_pairs_by_chunk,
    create_qa_pairs_by_custom,
    create_qa_pairs_by_json,
)
from apps.opspilot.utils.chunk_helper import ChunkHelper


class QAPairsFilter(FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    knowledge_base_id = filters.NumberFilter(field_name="knowledge_base_id", lookup_expr="exact")


class QAPairsViewSet(MaintainerViewSet, GenericViewSetFun):
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
                    status="pending",
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
        try:
            file_data = self.set_file_data(files)
        except Exception as e:
            return JsonResponse({"result": False, "message": str(e)})
        params = request.data
        create_qa_pairs_by_json.delay(
            file_data, int(params["knowledge_base_id"]), request.user.username, request.user.domain
        )
        return JsonResponse({"result": True, "message": "QA pairs import started."})

    @staticmethod
    def set_file_data(files):
        file_data = {}
        # 验证文件格式
        allowed_extensions = [".json", ".csv"]
        for i in files:
            file_ext = os.path.splitext(i.name)[1].lower()
            if file_ext not in allowed_extensions:
                raise Exception(_(f"Invalid file format: {i.name}. Only .json and .csv files are allowed."))
            try:
                if file_ext == ".json":
                    file_data.setdefault(i.name, []).extend(json.loads(i.read().decode("utf-8")))
                else:
                    csv_content = i.read().decode("utf-8").split("\n")[1:]
                    content = []
                    for line in csv_content:
                        if "," not in line:
                            continue
                        q, a = line.strip().split(",", 1)
                        content.append({"instruction": q.strip(), "output": a.strip()})
                    file_data.setdefault(i.name, []).extend(content)
            except json.JSONDecodeError:
                raise Exception(_(f"Invalid JSON file: {i.name}"))
        return file_data

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
            {
                "question": i["page_content"],
                "answer": i["metadata"]["qa_answer"],
                "id": i["metadata"]["chunk_id"],
                "base_chunk_id": i["metadata"].get("base_chunk_id", ""),
            }
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
        if res.get("status", "fail") != "success":
            return JsonResponse({"result": False, "message": res.get("message", "Failed to retrieve data.")})
        return_data = [
            {
                "question": i["page_content"],
                "answer": i["metadata"]["qa_answer"],
                "id": i["metadata"]["chunk_id"],
                "base_chunk_id": i["metadata"].get("base_chunk_id", ""),
            }
            for i in res.get("documents", [])
        ]
        return JsonResponse({"result": True, "data": return_data})

    @action(methods=["POST"], detail=False)
    def update_qa_pairs(self, request):
        params = request.data
        qa_paris = QAPairs.objects.get(id=params["qa_pairs_id"])
        index_name = qa_paris.knowledge_base.knowledge_index_name()
        chunk_id = params["id"]
        question = params["question"]
        answer = params["answer"]
        result = ChunkHelper.update_qa_pairs(index_name, chunk_id, question, answer)
        if not result:
            return JsonResponse({"result": False, "message": _("Failed to update QA pair.")})
        return JsonResponse({"result": True})

    @action(methods=["POST"], detail=False)
    def create_one_qa_pairs(self, request):
        params = request.data
        qa_paris = QAPairs.objects.get(id=params["qa_pairs_id"])
        index_name = qa_paris.knowledge_base.knowledge_index_name()
        question = params["question"]
        answer = params["answer"]
        embed_config = qa_paris.knowledge_base.embed_model.decrypted_embed_config
        embed_model_name = qa_paris.knowledge_base.embed_model.name
        result = ChunkHelper.create_one_qa_pairs(
            embed_config, embed_model_name, index_name, params["qa_pairs_id"], params["knowledge_id"], question, answer
        )
        return JsonResponse(result)

    @action(methods=["POST"], detail=False)
    def delete_one_qa_pairs(self, request):
        params = request.data
        qa_paris = QAPairs.objects.get(id=params["qa_pairs_id"])
        index_name = qa_paris.knowledge_base.knowledge_index_name()
        chunk_id = params["id"]
        result = ChunkHelper.delete_chunk(index_name, chunk_id)
        if not result:
            return JsonResponse({"result": False, "message": _("Failed to delete QA pair.")})
        if params["base_chunk_id"]:
            ChunkHelper.update_document_qa_pairs_count(index_name, -1, params["base_chunk_id"])
        return JsonResponse({"result": True})

    @action(methods=["POST"], detail=False)
    def create_qa_pairs_by_custom(self, request):
        params = request.data
        qa_pairs = QAPairs.objects.create(
            name=params["name"],
            description=params.get("description", ""),
            knowledge_base_id=params["knowledge_base_id"],
            qa_count=len(params["qa_pairs"]),
            document_id=0,
            create_type="custom",
            status="pending",
            created_by=request.user.username,
            domain=request.user.domain,
        )
        create_qa_pairs_by_custom.delay(qa_pairs.id, params["qa_pairs"])
        return JsonResponse({"result": True})

    @action(methods=["POST"], detail=False)
    def create_qa_pairs_by_chunk(self, request):
        params = request.data
        qa_pairs, _ = QAPairs.objects.get_or_create(
            name=params["name"],
            knowledge_base_id=params["knowledge_base_id"],
            document_id=params["document_id"],
            document_source=params["document_source"],
            defaults={
                "created_by": request.user.username,
                "domain": request.user.domain,
                "description": params.get("description", ""),
                "qa_count": params["qa_count"],
                "llm_model_id": params["llm_model_id"],
                "status": "pending",
            },
        )
        create_qa_pairs_by_chunk.delay(qa_pairs.id, params["chunk_list"], params["llm_model_id"], params["qa_count"])
        return JsonResponse({"result": True, "data": {"qa_pairs_id": qa_pairs.id}})

    @action(methods=["GET"], detail=False)
    def get_qa_pairs_task_status(self, request):
        document_id = request.GET.get("document_id")
        qa_pairs_obj = QAPairs.objects.filter(
            document_id=document_id,
        ).first()
        if not qa_pairs_obj:
            return JsonResponse({"result": True, "data": []})
        task_list = KnowledgeTask.objects.filter(
            is_qa_task=True, task_name=qa_pairs_obj.name, knowledge_ids__contains=int(qa_pairs_obj.id)
        )
        if not task_list:
            return JsonResponse({"result": True, "data": []})
        return JsonResponse(
            {
                "result": True,
                "data": [
                    {"status": "generating", "process": f"{task_obj.completed_count}/{task_obj.total_count}"}
                    for task_obj in task_list
                ],
            }
        )

    @action(methods=["POST"], detail=False)
    def export_qa_pairs(self, request):
        instance_id = request.data.get("qa_pairs_id")
        instance = QAPairs.objects.get(id=instance_id)
        if not request.user.is_superuser:
            current_team = request.COOKIES.get("current_team", "0")
            has_permission = self.get_has_permission(request.user, instance.knowledge_base, current_team)
            if not has_permission:
                return JsonResponse(
                    {"result": False, "message": _("You do not have permission to update this instance")}
                )
        res = ChunkHelper.get_document_es_chunk(
            instance.knowledge_base.knowledge_index_name(),
            1,
            10000,
            metadata_filter={"qa_pairs_id": str(instance_id)},
            get_count=False,
        )
        export_data = [
            {"instruction": i["page_content"], "output": i["metadata"]["qa_answer"]} for i in res.get("documents", [])
        ]
        export_file_name = instance.name
        if not export_file_name.endswith(".json"):
            export_file_name = f"{export_file_name}.json"

        # 创建 JSON 文件响应
        response = HttpResponse(json.dumps(export_data, ensure_ascii=False, indent=2), content_type="application/json")
        response["Content-Disposition"] = f'attachment; filename="{export_file_name}"'
        return response

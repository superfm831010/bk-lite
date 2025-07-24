from django.db.transaction import atomic
from django.http import JsonResponse
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.decorators.api_permission import HasRole
from apps.core.utils.viewset_utils import AuthViewSet
from apps.opspilot.knowledge_mgmt.models.knowledge_document import DocumentStatus
from apps.opspilot.knowledge_mgmt.serializers import KnowledgeBaseSerializer
from apps.opspilot.models import EmbedProvider, KnowledgeBase, KnowledgeDocument
from apps.opspilot.tasks import retrain_all


class KnowledgeBaseViewSet(AuthViewSet):
    queryset = KnowledgeBase.objects.all()
    serializer_class = KnowledgeBaseSerializer
    ordering = ("-id",)
    search_fields = ("name",)
    permission_key = "knowledge"

    @HasRole()
    def create(self, request, *args, **kwargs):
        params = request.data
        if not params.get("team"):
            return JsonResponse({"result": False, "message": _("The team field is required.")})
        if "embed_model" not in params:
            params["embed_model"] = EmbedProvider.objects.get(name="FastEmbed(BAAI/bge-small-zh-v1.5)").id
        if KnowledgeBase.objects.filter(name=params["name"]).exists():
            return JsonResponse({"result": False, "message": _("The knowledge base name already exists.")})
        params["created_by"] = request.user.username
        if params.get("enable_rerank") is None:
            params["enable_rerank"] = False
        if params.get("rag_k") is None:
            params["rag_k"] = 10
        if params.get("rag_num_candidates") is None:
            params["rag_num_candidates"] = 50
        if not params.get("team"):
            params["team"] = [int(request.COOKIES.get("current_team"))]
        serializer = self.get_serializer(data=params)
        serializer.is_valid(raise_exception=True)
        with atomic():
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @HasRole()
    def update(self, request, *args, **kwargs):
        instance: KnowledgeBase = self.get_object()
        params = request.data
        if instance.embed_model_id != params["embed_model"]:
            if instance.knowledgedocument_set.filter(train_status=DocumentStatus.TRAINING).exists():
                return JsonResponse(
                    {"result": False, "message": _("The knowledge base is training and cannot be modified.")}
                )
            retrain_all.delay(instance.id, username=request.user.username, domain=request.user.domain)
        return super().update(request, *args, **kwargs)

    @action(methods=["POST"], detail=True)
    @HasRole()
    def update_settings(self, request, *args, **kwargs):
        instance: KnowledgeBase = self.get_object()
        if not request.user.is_superuser:
            current_team = request.COOKIES.get("current_team", "0")
            has_permission = self.get_has_permission(request.user, instance, current_team)
            if not has_permission:
                return JsonResponse(
                    {"result": False, "message": _("You do not have permission to update this instance")}
                )

        kwargs = request.data
        if kwargs.get("name"):
            if KnowledgeBase.objects.filter(name=kwargs["name"]).exclude(id=instance.id).exists():
                return JsonResponse({"result": False, "message": _("The knowledge base name already exists.")})
            instance.name = kwargs["name"]
        if kwargs.get("introduction"):
            instance.introduction = kwargs["introduction"]
        if kwargs.get("team"):
            instance.team = kwargs["team"]
        instance.enable_vector_search = kwargs["enable_vector_search"]
        instance.vector_search_weight = kwargs["vector_search_weight"]
        instance.enable_text_search = kwargs["enable_text_search"]
        instance.text_search_weight = kwargs["text_search_weight"]
        instance.enable_rerank = kwargs["enable_rerank"]
        instance.rerank_model_id = kwargs["rerank_model"]
        instance.text_search_mode = kwargs["text_search_mode"]
        instance.rag_k = kwargs["rag_k"]
        instance.rerank_top_k = kwargs.get("rerank_top_k", 10)
        instance.enable_naive_rag = kwargs["enable_naive_rag"]
        instance.enable_qa_rag = kwargs["enable_qa_rag"]
        instance.enable_graph_rag = kwargs["enable_graph_rag"]
        instance.rag_size = kwargs["rag_size"]
        instance.qa_size = kwargs["qa_size"]
        instance.graph_size = kwargs["graph_size"]
        instance.rag_num_candidates = kwargs["rag_num_candidates"]
        instance.save()
        return JsonResponse({"result": True})

    @HasRole()
    def destroy(self, request, *args, **kwargs):
        if KnowledgeDocument.objects.filter(knowledge_base_id=kwargs["pk"]).exists():
            return JsonResponse(
                {"result": False, "message": _("This knowledge base contains documents and cannot be deleted.")}
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=["GET"])
    @HasRole()
    def get_teams(self, request):
        groups = request.user.group_list
        return JsonResponse({"result": True, "data": groups})

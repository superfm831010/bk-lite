from django.http import JsonResponse
from django.utils.translation import gettext as _
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.opspilot.knowledge_mgmt.serializers import WebPageKnowledgeSerializer
from apps.opspilot.knowledge_mgmt.utils import KnowledgeDocumentUtils
from apps.opspilot.models import WebPageKnowledge


class WebPageKnowledgeViewSet(viewsets.ModelViewSet):
    queryset = WebPageKnowledge.objects.all()
    serializer_class = WebPageKnowledgeSerializer
    ordering = ("-id",)
    search_fields = ("name",)

    @action(methods=["POST"], detail=False)
    def create_web_page_knowledge(self, request):
        kwargs = request.data
        if not kwargs.get("url").strip():
            return JsonResponse({"result": False, "data": _("url is required")})
        kwargs["knowledge_source_type"] = "web_page"
        new_doc = KnowledgeDocumentUtils.get_new_document(kwargs, request.user.username, request.user.domain)
        knowledge_obj = WebPageKnowledge.objects.create(
            knowledge_document_id=new_doc.id,
            url=kwargs.get("url", "").strip(),
            max_depth=kwargs.get("max_depth", 1),
            sync_enabled=kwargs.get("sync_enabled", False),
            sync_time=kwargs.get("sync_time", "00:00"),
        )
        if knowledge_obj.sync_enabled:
            knowledge_obj.create_sync_periodic_task()
        return JsonResponse({"result": True, "data": knowledge_obj.knowledge_document_id})

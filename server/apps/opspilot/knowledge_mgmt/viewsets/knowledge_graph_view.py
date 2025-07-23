from django.http import JsonResponse
from django_filters import filters
from django_filters.rest_framework import FilterSet
from rest_framework.decorators import action

from apps.core.utils.viewset_utils import MaintainerViewSet
from apps.opspilot.knowledge_mgmt.models import KnowledgeGraph
from apps.opspilot.knowledge_mgmt.serializers.knowledge_graph_serializers import KnowledgeGraphSerializer
from apps.opspilot.tasks import rebuild_graph_community_by_instance
from apps.opspilot.utils.graph_utils import GraphUtils


class KnowledgeGraphFilter(FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    knowledge_base_id = filters.NumberFilter(field_name="knowledge_base_id", lookup_expr="exact")


class KnowledgeGraphViewSet(MaintainerViewSet):
    queryset = KnowledgeGraph.objects.all()
    serializer_class = KnowledgeGraphSerializer
    filterset_class = KnowledgeGraphFilter
    ordering = ("-id",)

    @action(methods=["GET"], detail=False)
    def get_details(self, request):
        knowledge_base_id = request.query_params.get("knowledge_base_id")
        obj = KnowledgeGraph.objects.filter(knowledge_base_id=knowledge_base_id).first()
        if not obj:
            return JsonResponse({"result": True, "data": {"is_exists": False}})
        res = GraphUtils.get_graph(obj.id)
        if not res["result"]:
            return JsonResponse(res)
        return_data = {"graph": res["data"], "graph_id": obj.id, "is_exists": True}
        return JsonResponse({"result": True, "data": return_data})

    @action(methods=["POST"], detail=False)
    def delete_graph(self, request):
        instance = KnowledgeGraph.objects.get(knowledge_base_id=request.data.get("knowledge_base_id"))
        try:
            GraphUtils.delete_graph(instance)
        except Exception as e:
            return JsonResponse({"result": False, "message": str(e)}, status=500)
        instance.delete()
        return JsonResponse({"result": True})

    @action(methods=["POST"], detail=False)
    def rebuild_graph_community(self, request):
        knowledge_base_id = request.data.get("knowledge_base_id")
        graph_obj = KnowledgeGraph.objects.filter(knowledge_base_id=knowledge_base_id).first()
        if not graph_obj:
            return JsonResponse({"result": False, "message": "Knowledge graph not found."}, status=404)
        try:
            rebuild_graph_community_by_instance.delay(graph_obj.id)
            return JsonResponse({"result": True})
        except Exception as e:
            return JsonResponse({"result": False, "message": str(e)})

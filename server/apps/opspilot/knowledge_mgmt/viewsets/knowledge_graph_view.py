from django.http import JsonResponse
from django_filters import filters
from django_filters.rest_framework import FilterSet
from rest_framework.decorators import action

from apps.core.utils.viewset_utils import MaintainerViewSet
from apps.opspilot.knowledge_mgmt.models import KnowledgeGraph
from apps.opspilot.knowledge_mgmt.serializers.knowledge_graph_serializers import KnowledgeGraphSerializer
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
            return JsonResponse({"result": False})
        index_name = obj.knowledge_base.knowledge_index_name()
        res = GraphUtils.get_graph(index_name)
        return JsonResponse({"result": True, "data": res})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            GraphUtils.delete_graph(instance)
        except Exception as e:
            return JsonResponse({"result": False, "message": str(e)}, status=500)
        instance.delete()
        return JsonResponse({"result": True})

    @action(methods=["POST"], detail=False)
    def delete_graph_chunk(self, request):
        params = request.data
        chunk_ids = params["chunk_ids"]
        try:
            GraphUtils.delete_graph_chunk(chunk_ids)
        except Exception as e:
            return JsonResponse({"result": False, "message": str(e)}, status=500)
        return JsonResponse({"result": True})

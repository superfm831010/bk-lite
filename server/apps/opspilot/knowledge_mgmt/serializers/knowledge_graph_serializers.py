from apps.opspilot.knowledge_mgmt.models import KnowledgeGraph
from apps.opspilot.utils.graph_utils import GraphUtils
from config.drf.serializers import AuthSerializer


class KnowledgeGraphSerializer(AuthSerializer):
    class Meta:
        model = KnowledgeGraph
        fields = "__all__"

    def create(self, validated_data):
        instance = super().create(validated_data)
        res = GraphUtils.create_graph(instance)
        if not res["result"]:
            instance.delete()
            raise Exception(res["message"])
        return instance

    def update(self, instance, validated_data):
        old_doc_list = instance.doc_list[:]
        instance = super().update(instance, validated_data)
        res = GraphUtils.update_graph(instance, old_doc_list)
        if not res["result"]:
            raise Exception(res["message"])
        return instance

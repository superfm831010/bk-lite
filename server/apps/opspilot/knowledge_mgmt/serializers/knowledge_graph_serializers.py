from apps.opspilot.knowledge_mgmt.models import KnowledgeGraph
from apps.opspilot.utils.graph_utils import GraphUtils
from config.drf.serializers import AuthSerializer


class KnowledgeGraphSerializer(AuthSerializer):
    class Meta:
        model = KnowledgeGraph
        fields = "__all__"

    def create(self, validated_data):
        instance = super().create(validated_data)
        GraphUtils.create_graph(instance)
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        # GraphUtils.create_graph(instance)
        return instance

from apps.opspilot.knowledge_mgmt.models import QAPairs
from apps.opspilot.tasks import create_qa_pairs
from config.drf.serializers import AuthSerializer


class QAPairsSerializer(AuthSerializer):
    class Meta:
        model = QAPairs
        fields = "__all__"

    def create(self, validated_data):
        instance = super().create(validated_data)
        create_qa_pairs.delay(instance.id)
        return instance

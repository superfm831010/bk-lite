from apps.opspilot.knowledge_mgmt.models import QAPairs
from config.drf.serializers import AuthSerializer


class QAPairsSerializer(AuthSerializer):
    class Meta:
        model = QAPairs
        fields = "__all__"

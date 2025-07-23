from apps.core.utils.serializers import AuthSerializer
from apps.opspilot.knowledge_mgmt.models import QAPairs


class QAPairsSerializer(AuthSerializer):
    class Meta:
        model = QAPairs
        fields = "__all__"

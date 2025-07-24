from apps.core.utils.serializers import UsernameSerializer
from apps.opspilot.knowledge_mgmt.models import QAPairs


class QAPairsSerializer(UsernameSerializer):
    class Meta:
        model = QAPairs
        fields = "__all__"

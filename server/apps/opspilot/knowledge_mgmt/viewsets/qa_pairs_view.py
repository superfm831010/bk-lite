from apps.core.utils.viewset_utils import AuthViewSet
from apps.opspilot.knowledge_mgmt.models import QAPairs
from apps.opspilot.knowledge_mgmt.serializers.qa_pairs_serializers import QAPairsSerializer


class QAPairsViewSet(AuthViewSet):
    queryset = QAPairs.objects.all()
    serializer_class = QAPairsSerializer
    ordering = ("-id",)
    search_fields = ("name",)

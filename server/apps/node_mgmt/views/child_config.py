from rest_framework.viewsets import ModelViewSet

from apps.node_mgmt.filters.child_config import ChildConfigFilter
from apps.node_mgmt.models import ChildConfig
from apps.node_mgmt.serializers.child_config import ChildConfigSerializer


class ChildConfigViewSet(ModelViewSet):

    queryset = ChildConfig.objects.all()
    serializer_class = ChildConfigSerializer
    filterset_class = ChildConfigFilter

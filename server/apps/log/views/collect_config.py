from rest_framework.viewsets import ModelViewSet
from apps.log.models.collect_config import CollectType, CollectInstance, CollectConfig
from apps.log.serializers.collect_config import CollectTypeSerializer, CollectInstanceSerializer, CollectConfigSerializer
from apps.log.filters.collect_config import CollectTypeFilter, CollectInstanceFilter, CollectConfigFilter


class CollectTypeViewSet(ModelViewSet):
    queryset = CollectType.objects.all()
    serializer_class = CollectTypeSerializer
    filterset_class = CollectTypeFilter


class CollectInstanceViewSet(ModelViewSet):
    queryset = CollectInstance.objects.all()
    serializer_class = CollectInstanceSerializer
    filterset_class = CollectInstanceFilter


class CollectConfigViewSet(ModelViewSet):
    queryset = CollectConfig.objects.all()
    serializer_class = CollectConfigSerializer
    filterset_class = CollectConfigFilter
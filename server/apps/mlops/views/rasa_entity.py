from config.drf.pagination import CustomPageNumberPagination
from apps.core.decorators.api_permission import HasPermission

from config.drf.viewsets import ModelViewSet

from apps.mlops.models.rasa_entity import RasaEntity
from apps.mlops.filters.rasa_entity import RasaEntityFilter
from apps.mlops.serializers.rasa_entity import RasaEntitySerializer

class RasaEntityViewSet(ModelViewSet):
    filterset_class = RasaEntityFilter
    ordering = ('-id',)
    pagination_class = CustomPageNumberPagination
    permission_key = 'dataset.rasa_entity'
    queryset = RasaEntity.objects.all()
    serializer_class = RasaEntitySerializer



from config.drf.viewsets import ModelViewSet
from config.drf.pagination import CustomPageNumberPagination
from apps.core.decorators.api_permission import HasPermission

from apps.mlops.models.rasa_response import RasaResponse
from apps.mlops.filters.rasa_response import RasaResponseFilter
from apps.mlops.serializers.rasa_response import RasaResponseSerializer

class RasaResponseViewSet(ModelViewSet):
    filterset_class = RasaResponseFilter
    ordering = ('-id',)
    pagination_class = CustomPageNumberPagination
    permission_key = 'dataset.rasa_response'
    queryset = RasaResponse.objects.all()
    serializer_class = RasaResponseSerializer

from config.drf.viewsets import ModelViewSet
from config.drf.pagination import CustomPageNumberPagination

from apps.mlops.models.rasa_action import RasaAction
from apps.mlops.serializers.rasa_action import RasaActionSerializer
from apps.mlops.filters.rasa_action import RasaActionFilter

class RasaActionViewSet(ModelViewSet):
    queryset = RasaAction.objects.all()
    serializer_class = RasaActionSerializer
    filterset_class = RasaActionFilter
    pagination_class = CustomPageNumberPagination
    permission_key = 'dataset.rasa_action'
    ordering = ('-id',)
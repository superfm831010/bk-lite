from config.drf.viewsets import ModelViewSet
from config.drf.pagination import CustomPageNumberPagination
from apps.core.decorators.api_permission import HasPermission

from apps.mlops.models.rasa_slot import RasaSlot
from apps.mlops.serializers.rasa_slot import RasaSlotSerializer
from apps.mlops.filters.rasa_slot import RasaSlotFilter

class RasaSlotViewSet(ModelViewSet):
    filterset_class = RasaSlotFilter
    ordering = ('-id',)
    pagination_class = CustomPageNumberPagination
    permission_key = 'dataset.rasa_slot'
    queryset = RasaSlot.objects.all()
    serializer_class = RasaSlotSerializer

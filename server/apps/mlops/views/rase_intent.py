from config.drf.viewsets import ModelViewSet
from config.drf.pagination import CustomPageNumberPagination

from apps.mlops.models.rasa_intent import RasaIntent
from apps.mlops.serializers.rasa_intent import RasaIntentSerializer
from apps.mlops.filters.rase_intent import RasaIntentFilter

class RasaIntentViewSet(ModelViewSet):
    queryset = RasaIntent.objects.all()
    serializer_class = RasaIntentSerializer
    filterset_class = RasaIntentFilter
    pagination_class = CustomPageNumberPagination
    permission_key = 'dataset.rasa_intent'
    ordering = ('-id',)
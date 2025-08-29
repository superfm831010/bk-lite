from config.drf.viewsets import ModelViewSet
from config.drf.pagination import CustomPageNumberPagination
from apps.core.decorators.api_permission import HasPermission

from apps.mlops.models.rasa_form import RasaForm
from apps.mlops.serializers.rasa_form import RasaFormSerializer
from apps.mlops.filters.rasa_form import RasaFormFilter

class RasaFormViewSet(ModelViewSet):
    filterset_class = RasaFormFilter
    ordering = ('-id',)
    pagination_class = CustomPageNumberPagination
    permission_key = 'dataset.rasa_form'
    queryset = RasaForm.objects.all()
    serializer_class = RasaFormSerializer

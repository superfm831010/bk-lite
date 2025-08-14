from config.drf.viewsets import ModelViewSet
from apps.mlops.models.rasa_dataset import RasaDatasets
from apps.mlops.serializers.rasa_dataset import RasaDatasetSerializer
from apps.mlops.filters.rasa_dataset import RasaDatasetFilter
from config.drf.pagination import CustomPageNumberPagination
from apps.core.decorators.api_permission import HasPermission

class RasaDatasetViewSet(ModelViewSet):
    filterset_class = RasaDatasetFilter
    ordering = ("-id",)
    pagination_class = CustomPageNumberPagination
    permission_key = "dataset.rasa_dataset"
    queryset = RasaDatasets.objects.all()
    serializer_class = RasaDatasetSerializer
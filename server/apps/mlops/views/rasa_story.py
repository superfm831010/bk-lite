from config.drf.viewsets import ModelViewSet
from config.drf.pagination import CustomPageNumberPagination
from apps.core.decorators.api_permission import HasPermission

from apps.mlops.models.rasa_story import RasaStory
from apps.mlops.serializers.rasa_story import RasaStorySerializer
from apps.mlops.filters.rasa_story import RasaStoryFilter

class RasaStoryViewSet(ModelViewSet):
    filterset_class = RasaStoryFilter
    pagination_class = CustomPageNumberPagination
    permission_key = "dataset.rasa_story"
    queryset = RasaStory.objects.all()
    serializer_class = RasaStorySerializer
    ordering = ("-id",)

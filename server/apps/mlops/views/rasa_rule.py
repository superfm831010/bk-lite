from config.drf.viewsets import ModelViewSet
from config.drf.pagination import CustomPageNumberPagination
from apps.core.decorators.api_permission import HasPermission

from apps.mlops.models.rasa_rule import RasaRule
from apps.mlops.filters.rasa_rule import RasaRuleFilter
from apps.mlops.serializers.rasa_rule import RasaRuleSerializer

class RasaRuleViewSet(ModelViewSet):
    filterset_class = RasaRuleFilter
    ordering = ('-id',)
    pagination_class = CustomPageNumberPagination
    permission_key = 'dataset.rasa_rule'
    queryset = RasaRule.objects.all()
    serializer_class = RasaRuleSerializer
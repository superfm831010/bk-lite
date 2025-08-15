from django_filters.rest_framework import FilterSet
from apps.mlops.models.rasa_response import RasaResponse

class RasaResponseFilter(FilterSet):
    """
    Rasa机器人响应过滤器
    """
    class Meta:
        model = RasaResponse
        fields = {
            "dataset": ["exact"],
            "name": ["exact", "icontains"],
        }

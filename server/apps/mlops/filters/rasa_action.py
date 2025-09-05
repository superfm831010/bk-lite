from django_filters.rest_framework import FilterSet
from apps.mlops.models.rasa_action import RasaAction

class RasaActionFilter(FilterSet):
    class Meta:
        model = RasaAction
        fields = {
            "dataset": ["exact"],
            "name": ["exact", "icontains"],
        }
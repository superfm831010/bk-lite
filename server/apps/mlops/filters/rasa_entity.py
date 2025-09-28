from django_filters.rest_framework import FilterSet
from apps.mlops.models.rasa_entity import RasaEntity

class RasaEntityFilter(FilterSet):
    class Meta:
        model = RasaEntity
        fields = {
            "dataset": ["exact"],
            "name": ["exact", "icontains"],
            "entity_type": ["exact"],
        }
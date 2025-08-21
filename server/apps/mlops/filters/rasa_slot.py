from django_filters.rest_framework import FilterSet
from apps.mlops.models.rasa_slot import RasaSlot

class RasaSlotFilter(FilterSet):
    class Meta:
        model = RasaSlot
        fields = {
            "dataset": ["exact"],
            "name": ["exact", "icontains"],
        }
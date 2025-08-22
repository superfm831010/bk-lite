from django_filters.rest_framework import FilterSet
from apps.mlops.models.rasa_intent import RasaIntent

class RasaIntentFilter(FilterSet):
    class Meta:
        model = RasaIntent
        fields = {
            "dataset": ["exact"],
            "name": ["exact", "icontains"],
        }
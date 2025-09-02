from django_filters.rest_framework import FilterSet
from apps.mlops.models.rasa_form import RasaForm


class RasaFormFilter(FilterSet):
    class Meta:
        model = RasaForm
        fields = {
            "dataset": ["exact"],
            "name": ["exact", "icontains"],
        }
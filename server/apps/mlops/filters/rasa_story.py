from django_filters.rest_framework import FilterSet
from apps.mlops.models.rasa_story import RasaStory

class RasaStoryFilter(FilterSet):
    class Meta:
        model = RasaStory
        fields = {
            "dataset": ["exact"],
            "name": ["exact", "icontains"],
        }
from apps.mlops.models.rasa_dataset import RasaDatasets
from django_filters.rest_framework import FilterSet

class RasaDatasetFilter(FilterSet):
    """Rasa机器人数据集"""

    class Meta:
        model = RasaDatasets
        fields = {
            "name": ["exact", "icontains"],
        }
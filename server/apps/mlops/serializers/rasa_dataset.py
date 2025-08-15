from apps.core.utils.serializers import AuthSerializer
from apps.mlops.models.rasa_dataset import RasaDatasets

class RasaDatasetSerializer(AuthSerializer):
    """Rasa机器人数据集"""
    permission_key = "dataset.rasa_dataset"

    class Meta:
        model = RasaDatasets
        fields = "__all__"
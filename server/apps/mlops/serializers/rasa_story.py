from apps.core.utils.serializers import AuthSerializer
from apps.mlops.models.rasa_story import RasaStory

class RasaStorySerializer(AuthSerializer):

    permission_key = "dataset.rasa_story"

    class Meta:
        model = RasaStory
        fields = "__all__"
        extra_kwargs = {
            'name': {'required': False},
            'steps': {'required': False},
            'dataset': {'required': False},
        }
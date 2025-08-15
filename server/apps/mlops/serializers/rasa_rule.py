from apps.core.utils.serializers import AuthSerializer
from apps.mlops.models.rasa_rule import RasaRule

class RasaRuleSerializer(AuthSerializer):
    permission_key = "dataset.rasa_rule"

    class Meta:
        model = RasaRule
        fields = "__all__"
        extra_kwargs = {
            'name': {'required': False},
            'steps': {'required': False},
            'dataset': {'required': False},
        }
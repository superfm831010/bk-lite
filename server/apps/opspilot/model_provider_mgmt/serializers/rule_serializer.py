from apps.opspilot.models import SkillRule
from config.drf.serializers import UsernameSerializer


class RuleSerializer(UsernameSerializer):
    class Meta:
        model = SkillRule
        fields = "__all__"

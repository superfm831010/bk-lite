from apps.core.utils.serializers import AuthSerializer, TeamSerializer
from apps.opspilot.models import Bot


class BotSerializer(TeamSerializer, AuthSerializer):
    permission_key = "bot"

    class Meta:
        model = Bot
        fields = "__all__"

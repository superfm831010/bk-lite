from apps.opspilot.models import Channel
from config.drf.serializers import UsernameSerializer


class ChannelSerializer(UsernameSerializer):
    class Meta:
        model = Channel
        fields = "__all__"

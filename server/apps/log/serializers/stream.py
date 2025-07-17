from rest_framework import serializers
from apps.log.models.stream import Stream


class StreamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stream
        fields = ["id", "name", "rule", "collect_type", "created_by", "created_at"]
from apps.core.utils.serializers import AuthSerializer
from apps.mlops.models.rasa_response import RasaResponse
from rest_framework import serializers


class RasaResponseSerializer(AuthSerializer):
    permission_key = "dataset.rasa_response"

    example_count = serializers.SerializerMethodField(read_only=True,help_text="响应示例数量")

    class Meta:
        model = RasaResponse
        fields = "__all__"
        extra_kwargs = {
            'name': {'required': False},
            'example': {'required': False},
            'dataset': {'required': False},
        }

    def get_example_count(self, obj):
        """
        计算 example 字段的长度
        """
        if isinstance(obj.example, list):
            return len(obj.example)
        return 0
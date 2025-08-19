from apps.core.utils.serializers import AuthSerializer
from apps.mlops.models.rasa_entity import RasaEntity
from rest_framework import serializers

class RasaEntitySerializer(AuthSerializer):
    permission_key = "dataset.rasa_entity"

    # 使用 SerializerMethodField 来动态计算 example_count
    example_count = serializers.SerializerMethodField(read_only=True, help_text="实体示例数量")

    class Meta:
        model = RasaEntity
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
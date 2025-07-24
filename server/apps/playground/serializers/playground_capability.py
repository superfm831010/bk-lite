from rest_framework import serializers
from apps.playground.models.playground_capability import PlayGroundCapability
from apps.core.utils.serializers import AuthSerializer

class PlayGroundCapabilitySerializer(AuthSerializer):
    """
    PlayGroundCapability 的序列化器，支持所有字段的序列化。
    关键业务逻辑：category 字段序列化为嵌套对象。
    """
    category = serializers.SerializerMethodField()

    class Meta:
        model = PlayGroundCapability
        fields = "__all__"

    def get_category(self, obj):
        # 返回分类的详细信息
        from apps.playground.serializers.playground_category import PlayGroundCategorySerializer
        return PlayGroundCategorySerializer(obj.category).data if obj.category else None

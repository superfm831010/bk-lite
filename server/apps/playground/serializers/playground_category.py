from rest_framework import serializers
from apps.playground.models.playground_category import PlayGroundCategory
from apps.core.utils.serializers import AuthSerializer

class PlayGroundCategorySerializer(AuthSerializer):
    """
    PlayGroundCategory 的序列化器，支持所有字段的序列化。
    关键业务逻辑：支持树形结构的父子分类展示。
    """
    class Meta:
        model = PlayGroundCategory
        fields = "__all__"

    def to_representation(self, instance):
        # 支持树形结构展示
        representation = super().to_representation(instance)
        if hasattr(instance, 'children'):
            representation['children'] = PlayGroundCategorySerializer(instance.children.all(), many=True, context=self.context).data
        return representation

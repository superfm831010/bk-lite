from apps.core.utils.viewset_utils import AuthViewSet
from apps.playground.models.playground_capability import PlayGroundCapability
from apps.playground.serializers.playground_capability import PlayGroundCapabilitySerializer
from apps.playground.filters.playground_capability import PlayGroundCapabilityFilter

class PlayGroundCapabilityViewSet(AuthViewSet):
    """
    PlayGroundCapability 的视图集，支持增删改查和过滤。
    关键业务逻辑：category 字段嵌套展示，支持按分类、启用状态过滤。
    """
    queryset = PlayGroundCapability.objects.all()
    serializer_class = PlayGroundCapabilitySerializer
    filterset_class = PlayGroundCapabilityFilter
    search_fields = ['name']
    ordering_fields = ['id', 'name', 'is_active']
    ordering = ['id']
    permission_key = "playground.playground_capability"

    def get_queryset(self):
        # 可根据需求自定义查询集
        queryset = super().get_queryset()
        return queryset

from apps.core.utils.viewset_utils import AuthViewSet
from apps.playground.models.playground_category import PlayGroundCategory
from apps.playground.serializers.playground_category import PlayGroundCategorySerializer
from apps.playground.filters.playground_category import PlayGroundCategoryFilter

class PlayGroundCategoryViewSet(AuthViewSet):
    """
    PlayGroundCategory 的视图集，支持增删改查和过滤。
    关键业务逻辑：支持树形结构展示和过滤。
    """
    queryset = PlayGroundCategory.objects.all()
    serializer_class = PlayGroundCategorySerializer
    filterset_class = PlayGroundCategoryFilter
    search_fields = ['name']
    ordering_fields = ['id', 'name']
    ordering = ['id']
    permission_key = "playground.playground_category"

    def get_queryset(self):
        # 可根据需求自定义查询集，如只展示根节点等
        queryset = super().get_queryset()
        return queryset

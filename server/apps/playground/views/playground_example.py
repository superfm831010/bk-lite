from config.drf.viewsets import ModelViewSet
from apps.playground.models.playground_example import PlayGroundFile
from apps.playground.filters.playground_example import PlayGroundExampleFilter
from apps.playground.serializers.playground_example import PlayGroundFileSerializer
from apps.core.decorators.api_permission import HasPermission

class PlayGroundFileViewSet(ModelViewSet):
    """
    PlayGroundFileViewSet 视图集
    关键业务逻辑：serving 嵌套对象
    """
    queryset = PlayGroundFile.objects.all()
    serializer_class = PlayGroundFileSerializer
    filterset_class = PlayGroundExampleFilter
    search_fields = ['name']
    ordering_fields = ['id','name','is_active']
    ordering = ['id']
    permission_key = 'playground.playground_example'

    def get_queryset(self):
        # 可根据需求自定义查询集
        queryset = super().get_queryset()

    @HasPermission('example-View')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @HasPermission('example-Add')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @HasPermission('example-Edit')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @HasPermission('example-Delete')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @HasPermission('example-View')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
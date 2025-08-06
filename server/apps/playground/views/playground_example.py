from config.drf.viewsets import ModelViewSet
from apps.playground.models.playground_example import PlaygroundAnomalyDetectionExample
from apps.playground.filters.playground_example import PlaygroundAnomalyDetectionExampleFilter
from apps.playground.serializers.playground_example import PlaygroundAnomalyDetectionExampleSerializer
from apps.core.decorators.api_permission import HasPermission

class PlayGroundAnomalyDetectionExampleViewSet(ModelViewSet):
    """
    PlaygroundAnomalyDetectionExample 视图集
    只支持异常检测样本文件的增删改查
    """
    queryset = PlaygroundAnomalyDetectionExample.objects.all()
    serializer_class = PlaygroundAnomalyDetectionExampleSerializer
    filterset_class = PlaygroundAnomalyDetectionExampleFilter
    search_fields = ['name']
    ordering_fields = ['id','name','is_active']
    ordering = ['id']
    permission_key = 'playground.playground_example'

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
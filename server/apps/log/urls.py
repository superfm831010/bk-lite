from rest_framework import routers

from apps.log.views.node import NodeViewSet
from apps.log.views.search import LogSearchViewSet
from apps.log.views.stream import StreamViewSet

from apps.log.views.collect_config import (
    CollectTypeViewSet,
    CollectInstanceViewSet,
    CollectConfigViewSet
)

router = routers.DefaultRouter()

router.register(r'collect_types', CollectTypeViewSet, basename='collect_type')
router.register(r'collect_instances', CollectInstanceViewSet, basename='collect_instance')
router.register(r'collect_configs', CollectConfigViewSet, basename='collect_config')
router.register(r'node_mgmt', NodeViewSet, basename='node_mgmt')
router.register(r'streams', StreamViewSet, basename='stream')
router.register(r'search', LogSearchViewSet, basename='log_search')

urlpatterns = router.urls

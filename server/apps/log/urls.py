from rest_framework import routers

router = routers.DefaultRouter()
from apps.log.views.collect_config import (
    CollectTypeViewSet,
    CollectInstanceViewSet,
    CollectConfigViewSet,
)
router.register(r'collect_types', CollectTypeViewSet, basename='collect_type')
router.register(r'collect_instances', CollectInstanceViewSet, basename='collect_instance')
router.register(r'collect_configs', CollectConfigViewSet, basename='collect_config')
urlpatterns = router.urls

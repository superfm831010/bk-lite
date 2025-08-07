from rest_framework import routers
from apps.playground.views import PlayGroundCategoryViewSet, PlayGroundCapabilityViewSet,PlayGroundAnomalyDetectionExampleViewSet

router = routers.DefaultRouter()
router.register(r'category', PlayGroundCategoryViewSet, basename='playground-category')
router.register(r'capability', PlayGroundCapabilityViewSet, basename='playground-capability')
router.register(r'example',PlayGroundAnomalyDetectionExampleViewSet,basename='playground-example')

urlpatterns = router.urls

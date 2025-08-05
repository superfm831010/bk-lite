from rest_framework import routers
from apps.playground.views import PlayGroundCategoryViewSet, PlayGroundCapabilityViewSet,PlayGroundFileViewSet

router = routers.DefaultRouter()
router.register(r'category', PlayGroundCategoryViewSet, basename='playground-category')
router.register(r'capability', PlayGroundCapabilityViewSet, basename='playground-capability')
router.register(r'example',PlayGroundFileViewSet,basename='playground-example')

urlpatterns = router.urls

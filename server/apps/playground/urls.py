from rest_framework import routers
from apps.playground.views import PlayGroundCategoryViewSet, PlayGroundCapabilityViewSet

router = routers.DefaultRouter()
router.register(r'category', PlayGroundCategoryViewSet, basename='playground-category')
router.register(r'capability', PlayGroundCapabilityViewSet, basename='playground-capability')

urlpatterns = router.urls

from rest_framework import routers

from apps.system_mgmt.viewset import (
    AppViewSet,
    ChannelViewSet,
    GroupDataRuleViewSet,
    GroupViewSet,
    RoleViewSet,
    SystemSettingsViewSet,
    UserViewSet,
)

router = routers.DefaultRouter()
router.register(r"group", GroupViewSet, basename="group_mgmt")
router.register(r"user", UserViewSet, basename="user_mgmt")
router.register(r"role", RoleViewSet, basename="role_mgmt")
router.register(r"channel", ChannelViewSet)
router.register(r"group_data_rule", GroupDataRuleViewSet)
router.register(r"system_settings", SystemSettingsViewSet)
router.register(r"app", AppViewSet)
urlpatterns = router.urls

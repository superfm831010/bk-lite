# -- coding: utf-8 --
# @File: urls.py
# @Time: 2025/7/14 16:35
# @Author: windyzhao

from rest_framework import routers

from apps.operation_analysis.views.view import DataSourceAPIModelViewSet, DashboardModelViewSet, DirectoryModelViewSet, \
    TopologyModelViewSet, NameSpaceModelViewSet

router = routers.DefaultRouter()
router.register(r"api/data_source", DataSourceAPIModelViewSet, basename="data_source")
router.register(r"api/dashboard", DashboardModelViewSet, basename="dashboard")
router.register(r"api/directory", DirectoryModelViewSet, basename="directory")
router.register(r"api/topology", TopologyModelViewSet, basename="topology")
router.register(r"api/namespace", NameSpaceModelViewSet, basename="namespace")

urlpatterns = [
    # path("api/test/", request_test),
]

urlpatterns += router.urls

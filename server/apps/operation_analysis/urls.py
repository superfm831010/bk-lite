# -- coding: utf-8 --
# @File: urls.py
# @Time: 2025/7/14 16:35
# @Author: windyzhao

from django.urls import path
from rest_framework import routers

from apps.operation_analysis.views.view import request_test, DataSourceAPIModelViewSet

router = routers.DefaultRouter()
router.register(r"api/data_source", DataSourceAPIModelViewSet, basename="data_source")

urlpatterns = [
    path("api/test/", request_test),
]

urlpatterns += router.urls

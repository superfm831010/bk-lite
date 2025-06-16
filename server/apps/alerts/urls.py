# -- coding: utf-8 --
# @File: urls.py
# @Time: 2025/5/9 14:57
# @Author: windyzhao
from django.urls import path
from rest_framework import routers

from apps.alerts.views.assignment_shield import AlertAssignmentModelViewSet, AlertShieldModelViewSet
from apps.alerts.views.view import request_test, AlterModelViewSet, EventModelViewSet, LevelModelViewSet
from apps.alerts.views.source import receiver_data
from apps.alerts.views.view import AlertSourceModelViewSet

urlpatterns = [
    path("api/test/", request_test),
    path("api/receiver_data/", receiver_data),
]

router = routers.DefaultRouter()
router.register(r"api/alert_source", AlertSourceModelViewSet, basename="alert_source")
router.register(r"api/alerts", AlterModelViewSet, basename="alerts")
router.register(r"api/events", EventModelViewSet, basename="events")
router.register(r"api/level", LevelModelViewSet, basename="level")
router.register(r"api/assignment", AlertAssignmentModelViewSet, basename="assignment")
router.register(r"api/shield", AlertShieldModelViewSet, basename="shield")

urlpatterns += router.urls

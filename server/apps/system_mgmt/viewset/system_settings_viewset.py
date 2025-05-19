from rest_framework import viewsets

from apps.system_mgmt.models.system_settings import SystemSettings
from apps.system_mgmt.serializers.system_settings_serializer import SystemSettingsSerializer


class SystemSettingsViewSet(viewsets.ModelViewSet):
    queryset = SystemSettings.objects.all()
    serializer_class = SystemSettingsSerializer

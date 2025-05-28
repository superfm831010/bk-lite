from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.system_mgmt.models.system_settings import SystemSettings
from apps.system_mgmt.serializers.system_settings_serializer import SystemSettingsSerializer


class SystemSettingsViewSet(viewsets.ModelViewSet):
    queryset = SystemSettings.objects.all()
    serializer_class = SystemSettingsSerializer

    @action(methods=["GET"], detail=False)
    def get_sys_set(self, request):
        sys_settings = SystemSettings.objects.all().values_list("key", "value")
        return JsonResponse({"result": True, "data": dict(sys_settings)})

    @action(methods=["POST"], detail=False)
    def update_sys_set(self, request):
        kwargs = request.data
        sys_set = list(SystemSettings.objects.filter(key__in=list(kwargs.keys())))
        for i in sys_set:
            i.value = kwargs.get(i.key, i.value)
        SystemSettings.objects.bulk_update(sys_set, ["value"])
        return JsonResponse({"result": True})

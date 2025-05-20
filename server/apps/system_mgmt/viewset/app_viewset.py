from django.http import JsonResponse
from django.utils.translation import gettext as _
from rest_framework import viewsets

from apps.system_mgmt.models import App
from apps.system_mgmt.serializers.app_serializer import AppSerializer


class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.is_build_in:
            return JsonResponse({"result": False, "message": _("Cannot delete built-in application")})
        return super().destroy(request, *args, **kwargs)

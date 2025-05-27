from rest_framework import viewsets

from apps.system_mgmt.models import LoginModule
from apps.system_mgmt.serializers.login_module_serializer import LoginModuleSerializer


class LoginModuleViewSet(viewsets.ModelViewSet):
    queryset = LoginModule.objects.all()
    serializer_class = LoginModuleSerializer

    def list(self, request, *args, **kwargs):
        """
        List all login modules.
        """
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Create a new login module.
        """
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update an existing login module.
        """
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a login module.
        """
        return super().destroy(request, *args, **kwargs)

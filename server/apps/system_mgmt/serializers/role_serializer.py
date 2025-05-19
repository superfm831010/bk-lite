from rest_framework import serializers

from apps.system_mgmt.models import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

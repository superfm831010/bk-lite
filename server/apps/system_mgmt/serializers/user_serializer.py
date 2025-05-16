from rest_framework import serializers

from apps.system_mgmt.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

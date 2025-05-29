from rest_framework import serializers

from apps.system_mgmt.models import App


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = "__all__"

    def create(self, validated_data):
        validated_data["is_build_in"] = False
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("is_build_in", None)
        return super().update(instance, validated_data)

from rest_framework import serializers
from rest_framework.fields import empty

from apps.opspilot.models import ModelType


class ProviderModelTypeSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()
    model_type_name = serializers.SerializerMethodField()

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)
        type_list = ModelType.objects.all().values("id", "icon", "display_name")
        self.type_map = {}
        for i in type_list:
            self.type_map[i["id"]] = {"icon": i["icon"], "display_name": i["display_name"]}

    def get_icon(self, instance):
        if instance.model_type:
            return self.type_map.get(instance.model_type_id, {}).get("icon", "")
        return ""

    def get_model_type_name(self, instance):
        if instance.model_type:
            return self.type_map.get(instance.model_type_id, {}).get("display_name", "")
        return ""


class ModelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelType
        fields = "__all__"

    def create(self, validated_data):
        last_obj = ModelType.objects.order_by("-index").first()
        if last_obj:
            last_index = last_obj.index + 1
        else:
            last_obj = 0
        validated_data["index"] = last_index
        instance = super().create(validated_data)
        return instance

from django.http import JsonResponse
from django_filters import filters
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.core.decorators.api_permission import HasPermission
from apps.system_mgmt.models import Channel
from apps.system_mgmt.serializers import ChannelSerializer


class ChannelFilter(FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    channel_type = filters.CharFilter(field_name="channel_type", lookup_expr="exact")


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    filterset_class = ChannelFilter

    @HasPermission("Channel_list-View")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @HasPermission("Channel_list-Add")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @HasPermission("Channel_list-Delete")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(methods=["POST"], detail=True)
    @HasPermission("Channel_list-Edit")
    def update_settings(self, request, *args, **kwargs):
        obj: Channel = self.get_object()
        config = request.data["config"]
        if obj.channel_type == "email":
            obj.encrypt_field("smtp_pwd", config)
            config.setdefault("smtp_pwd", obj.config["smtp_pwd"])
        elif obj.channel_type == "enterprise_wechat":
            obj.encrypt_field("secret", config)
            obj.encrypt_field("token", config)
            obj.encrypt_field("aes_key", config)
            config.setdefault("secret", obj.config["secret"])
            config.setdefault("token", obj.config["token"])
            config.setdefault("aes_key", obj.config["aes_key"])
        elif obj.channel_type == "enterprise_wechat_bot":
            obj.encrypt_field("bot_key", config)
            config.setdefault("bot_key", obj.config["bot_key"])
        obj.config = config
        obj.save()
        return JsonResponse({"result": True})


class TemplateFilter(FilterSet):
    channel_type = filters.CharFilter(field_name="channel_type", lookup_expr="exact")
    name = filters.CharFilter(field_name="name", lookup_expr="lte")

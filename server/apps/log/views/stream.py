from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet
from apps.core.utils.web_utils import WebUtils
from apps.log.models.stream import Stream, StreamOrganization
from apps.log.serializers.stream import StreamSerializer
from apps.log.filters.stream import StreamFilter


class StreamViewSet(ModelViewSet):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    filterset_class = StreamFilter

    @swagger_auto_schema(
        operation_description="创建数据流",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_STRING, description="Stream ID"),
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="Stream Name"),
                "collect_type_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Collect Type ID"),
                "rule": openapi.Schema(type=openapi.TYPE_OBJECT, description="Stream Rule"),
                "organizations": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER, description="Organization ID")),
            },
            required=["id", "name", "collect_type_id", "rule", "organizations"]
        )
    )
    def create(self, request, *args, **kwargs):
        obj = Stream.objects.create(
            id=request.data.get("id"),
            name=request.data.get("name"),
            collect_type_id=request.data.get("collect_type_id"),
            rule=request.data.get("rule", {}),
            created_by=request.user.username
        )
        # 创建组织关联
        StreamOrganization.objects.bulk_create(
            [StreamOrganization(stream_id=obj.id, organization=org_id) for org_id in request.data.get("organizations", [])],
            ignore_conflicts=True
        )

        return WebUtils.response_success(request.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(streamorganization__organization=request.COOKIES.get("current_team")).distinct("id")
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        data = serializer.data
        # 添加组织信息
        org_map = {}
        asso_objs = StreamOrganization.objects.filter(
            stream_id__in=[item["id"] for item in data]).values_list("stream_id", "organization")
        for stream_id, organization in asso_objs:
            org_map.setdefault(stream_id, []).append(organization)
        for item in data:
            item["organizations"] = org_map.get(item["id"], [])
        return self.get_paginated_response(data)

    @swagger_auto_schema(
        operation_description="修改数据流",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="Stream Name"),
                "collect_type_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Collect Type ID"),
                "rule": openapi.Schema(type=openapi.TYPE_OBJECT, description="Stream Rule"),
                "organizations": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER, description="Organization ID")),
            },
            required=["name", "collect_type_id", "rule", "organizations"]
        )
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.name = request.data.get("name", instance.name)
        instance.collect_type_id = request.data.get("collect_type_id", instance.collect_type_id)
        instance.rule = request.data.get("rule", instance.rule)
        instance.updated_by = request.user.username
        instance.save()
        # 更新组织关联
        organizations = request.data.get("organizations", [])
        # 清除旧的组织关联
        StreamOrganization.objects.filter(stream=instance).delete()
        # 添加新的组织关联
        StreamOrganization.objects.bulk_create(
            [StreamOrganization(stream=instance, organization=org_id) for org_id in organizations],
            ignore_conflicts=True
        )
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return WebUtils.response_success(dict(id=instance.id, **request.data))

    # @swagger_auto_schema(
    #     operation_description="查询节点列表",
    #     request_body=openapi.Schema(
    #         type=openapi.TYPE_OBJECT,
    #         properties={
    #             "organizations": openapi.Schema(type=openapi.TYPE_ARRAY,
    #                 items=openapi.Schema(type=openapi.TYPE_INTEGER, description="Organization ID")),
    #         },
    #         required=["organizations"]
    #     )
    # )
    # @action(methods=["post"], detail=True, url_path="set_organizations")
    # def set_organizations(self, request, pk=None):
    #     """Set organizations for a specific stream."""
    #     stream = self.get_object()
    #     organizations = request.data.get("organizations", [])
    #     if not isinstance(organizations, list):
    #         return Response({"error": "Invalid organizations format"}, status=400)
    #
    #     # Clear existing organizations
    #     StreamOrganization.objects.filter(stream=stream).delete()
    #
    #     # Add new organizations
    #     for org_id in organizations:
    #         StreamOrganization.objects.create(stream=stream, organization=org_id)
    #
    #     return Response({"message": "Organizations updated successfully"})

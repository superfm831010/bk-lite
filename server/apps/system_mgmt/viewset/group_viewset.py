from django.http import JsonResponse
from django.utils.translation import gettext as _
from rest_framework.decorators import action

from apps.system_mgmt.models import Group, User
from apps.system_mgmt.serializers.group_serializer import GroupSerializer
from apps.system_mgmt.utils.group_utils import GroupUtils
from apps.system_mgmt.utils.viewset_utils import ViewSetUtils


class GroupViewSet(ViewSetUtils):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    @action(detail=False, methods=["GET"])
    def search_group_list(self, request):
        queryset = Group.objects.all()
        # 构建嵌套组结构
        groups_data = GroupUtils.build_group_tree(queryset)
        return JsonResponse({"result": True, "data": groups_data})

    @action(detail=False, methods=["GET"])
    def get_detail(self, request):
        group = Group.objects.get(id=request.GET["group_id"])
        return JsonResponse(
            {"result": True, "data": {"name": group.name, "id": group.id, "parent_id": group.parent_id}}
        )

    @action(detail=False, methods=["POST"])
    def create_group(self, request):
        params = request.data
        group = Group.objects.create(
            parent_id=params.get("parent_group_id", 0),
            name=params["group_name"],
        )
        data = {"id": group.id, "name": group.name, "parent_id": group.parent_id, "subGroupCount": 0, "subGroups": []}
        return JsonResponse({"result": True, "data": data})

    @action(detail=False, methods=["POST"])
    def update_group(self, request):
        Group.objects.filter(id=request.data.get("group_id")).update(name=request.data.get("group_name"))
        return JsonResponse({"result": True})

    @action(detail=False, methods=["POST"])
    def delete_groups(self, request):
        kwargs = request.data
        users = User.objects.filter(group_list__contains=int(kwargs["id"]))
        if users:
            return JsonResponse(
                {"result": False, "message": _("This group or sub groups has users, please remove the users first!")}
            )
        Group.objects.filter(id=int(kwargs["id"])).delete()
        return JsonResponse({"result": True})

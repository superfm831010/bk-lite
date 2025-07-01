from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.cmdb.services.instance import InstanceManage
from apps.core.decorators.api_permission import HasPermission
from apps.core.utils.web_utils import WebUtils
from apps.rpc.node_mgmt import NodeMgmt


class InstanceViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_id="instance_list",
        operation_description="实例列表",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "query_list": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_OBJECT, description="查询条件"),
                    description="查询条件列表",
                ),
                "page": openapi.Schema(type=openapi.TYPE_INTEGER, description="第几页"),
                "page_size": openapi.Schema(type=openapi.TYPE_INTEGER, description="每页条目数"),
                "order": openapi.Schema(type=openapi.TYPE_STRING, description="排序"),
                "model_id": openapi.Schema(type=openapi.TYPE_STRING, description="模型ID"),
                "role": openapi.Schema(type=openapi.TYPE_STRING, description="角色"),
            },
            required=["model_id"],
        ),
    )
    @HasPermission("asset_list-View")
    @action(methods=["post"], detail=False)
    def search(self, request):
        """
        TODO 搜索存在问题
        query_list [{field: "inst_name", type: "str*", value: "allure(weops-prod)"}] 搜索失败
        query_list [{field: "inst_name", type: "str=", value: "allure(weops-prod)"}] 搜索成果
        """
        page, page_size = int(request.data.get("page", 1)), int(request.data.get("page_size", 10))
        insts, count = InstanceManage.instance_list(
            request.user.group_list,
            request.user.roles,
            request.data["model_id"],
            request.data.get("query_list", []),
            page,
            page_size,
            request.data.get("order", ""),
        )
        return WebUtils.response_success(dict(insts=insts, count=count))

    @swagger_auto_schema(
        operation_id="instance_detail",
        operation_description="查询实例信息",
        manual_parameters=[
            openapi.Parameter("id", openapi.IN_PATH, description="实例ID", type=openapi.TYPE_INTEGER),
        ],
    )
    @HasPermission("asset_basic_information-View")
    def retrieve(self, request, pk: str):
        data = InstanceManage.query_entity_by_id(int(pk))
        return WebUtils.response_success(data)

    @swagger_auto_schema(
        operation_id="instance_create",
        operation_description="创建实例",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "model_id": openapi.Schema(type=openapi.TYPE_STRING, description="模型ID"),
                "instance_info": openapi.Schema(type=openapi.TYPE_OBJECT, description="实例信息"),
            },
            required=["model_id", "instance_info"],
        ),
    )
    @HasPermission("asset_list-Add")
    def create(self, request):
        inst = InstanceManage.instance_create(
            request.data.get("model_id"),
            request.data.get("instance_info"),
            request.user.username,
        )
        return WebUtils.response_success(inst)

    @swagger_auto_schema(
        operation_id="instance_delete",
        operation_description="删除实例",
        manual_parameters=[openapi.Parameter("id", openapi.IN_PATH, description="实例ID", type=openapi.TYPE_INTEGER)],
    )
    @HasPermission("asset_list-Delete")
    def destroy(self, request, pk: int):
        InstanceManage.instance_batch_delete(
            request.user.group_list,
            request.user.roles,
            [int(pk)],
            request.user.username,
        )
        return WebUtils.response_success()

    @swagger_auto_schema(
        operation_id="instance_batch_delete",
        operation_description="批量删除实例",
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_INTEGER, description="实例ID"),
        ),
    )
    @HasPermission("asset_list-Delete")
    @action(detail=False, methods=["post"], url_path="batch_delete")
    def instance_batch_delete(self, request):
        InstanceManage.instance_batch_delete(
            request.user.group_list,
            request.user.roles,
            request.data,
            request.user.username,
        )
        return WebUtils.response_success()

    @swagger_auto_schema(
        operation_id="instance_update",
        operation_description="更新实例属性",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description="实例信息",
        ),
    )
    @HasPermission("asset_list-Edit,asset_basic_information-Edit")
    def partial_update(self, request, pk: int):
        inst = InstanceManage.instance_update(
            request.user.group_list,
            request.user.roles,
            int(pk),
            request.data,
            request.user.username,
        )
        return WebUtils.response_success(inst)

    @swagger_auto_schema(
        operation_id="instance_batch_update",
        operation_description="批量更新实例属性",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "inst_ids": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER, description="实例ID"),
                ),
                "update_data": openapi.Schema(type=openapi.TYPE_OBJECT, description="要更新的数据"),
            },
            required=["inst_ids", "update_data"],
        ),
    )
    @HasPermission("asset_list-Edit")
    @action(detail=False, methods=["post"], url_path="batch_update")
    def instance_batch_update(self, request):
        InstanceManage.batch_instance_update(
            request.user.group_list,
            request.user.roles,
            request.data["inst_ids"],
            request.data["update_data"],
            request.user.username,
        )
        return WebUtils.response_success()

    @swagger_auto_schema(
        operation_id="instance_association_create",
        operation_description="创建实例关联",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "model_asst_id": openapi.Schema(type=openapi.TYPE_STRING, description="模型关联关系"),
                "src_model_id": openapi.Schema(type=openapi.TYPE_STRING, description="源模型ID"),
                "dst_model_id": openapi.Schema(type=openapi.TYPE_STRING, description="目标模型ID"),
                "src_inst_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="源模型实例ID"),
                "dst_inst_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="目标模型实例ID"),
                "asst_id": openapi.Schema(type=openapi.TYPE_STRING, description="目标模型实例ID"),
            },
            required=[
                "model_asst_id",
                "src_model_id",
                "src_inst_id",
                "dst_model_id",
                "dst_inst_id",
                "asst_id",
            ],
        ),
    )
    @HasPermission("asset_list-Add,asset_relationships-Add")
    @action(detail=False, methods=["post"], url_path="association")
    def instance_association_create(self, request):
        asso = InstanceManage.instance_association_create(request.data, request.user.username)
        return WebUtils.response_success(asso)

    @swagger_auto_schema(
        operation_id="instance_association_delete",
        operation_description="删除实例关联",
        manual_parameters=[
            openapi.Parameter("id", openapi.IN_PATH, description="实例关联ID", type=openapi.TYPE_INTEGER)],
    )
    @HasPermission("asset_list-Delete,asset_relationships-Delete")
    @action(detail=False, methods=["delete"], url_path="association/(?P<id>.+?)")
    def instance_association_delete(self, request, id: int):
        InstanceManage.instance_association_delete(int(id), request.user.username)
        return WebUtils.response_success()

    @swagger_auto_schema(
        operation_id="instance_association_instance_list",
        operation_description="查询某个实例的所有关联实例",
        manual_parameters=[
            openapi.Parameter(
                "model_id",
                openapi.IN_PATH,
                description="模型ID",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter("inst_id", openapi.IN_PATH, description="实例ID", type=openapi.TYPE_NUMBER),
        ],
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="association_instance_list/(?P<model_id>.+?)/(?P<inst_id>.+?)",
    )
    @HasPermission("asset_list-View,asset_relationships-View")
    def instance_association_instance_list(self, request, model_id: str, inst_id: int):
        asso_insts = InstanceManage.instance_association_instance_list(model_id, int(inst_id))
        return WebUtils.response_success(asso_insts)

    @swagger_auto_schema(
        operation_id="instance_association",
        operation_description="查询某个实例的所有关联",
        manual_parameters=[
            openapi.Parameter(
                "model_id",
                openapi.IN_PATH,
                description="模型ID",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="instance_association/(?P<model_id>.+?)/(?P<inst_id>.+?)",
    )
    @HasPermission("asset_relationships-View,asset_list-View")
    def instance_association(self, request, model_id: str, inst_id: int):
        asso_insts = InstanceManage.instance_association(model_id, int(inst_id))
        return WebUtils.response_success(asso_insts)

    @swagger_auto_schema(
        operation_id="download_template",
        operation_description="下载模型实例导入模板",
        manual_parameters=[
            openapi.Parameter(
                "model_id",
                openapi.IN_PATH,
                description="模型ID",
                type=openapi.TYPE_STRING,
            )
        ],
    )
    @HasPermission("asset_list-Add")
    @action(methods=["get"], detail=False, url_path=r"(?P<model_id>.+?)/download_template")
    def download_template(self, request, model_id):
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = f"attachment;filename={f'{model_id}_import_template.xlsx'}"
        response.write(InstanceManage.download_import_template(model_id).read())
        return response

    @swagger_auto_schema(
        operation_id="inst_import",
        operation_description="实例导入",
        manual_parameters=[
            openapi.Parameter(
                "model_id",
                openapi.IN_PATH,
                description="模型ID",
                type=openapi.TYPE_STRING,
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "file": openapi.Schema(
                    type=openapi.TYPE_FILE,
                    format=openapi.FORMAT_BINARY,
                    description="文件",
                ),
            },
            required=["file"],
        ),
    )
    @HasPermission("asset_list-Add")
    @action(methods=["post"], detail=False, url_path=r"(?P<model_id>.+?)/inst_import")
    def inst_import(self, request, model_id):
        result = InstanceManage.inst_import(
            model_id,
            request.data.get("file").file,
            request.user.username,
        )
        return WebUtils.response_success(result)

    @swagger_auto_schema(
        operation_id="inst_import_support_edit",
        operation_description="实例导入支持编辑",
        manual_parameters=[
            openapi.Parameter(
                "model_id",
                openapi.IN_PATH,
                description="模型ID",
                type=openapi.TYPE_STRING,
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "file": openapi.Schema(
                    type=openapi.TYPE_FILE,
                    format=openapi.FORMAT_BINARY,
                    description="文件",
                ),
            },
            required=["file"],
        ),
    )
    @HasPermission("asset_list-Add")
    @action(methods=["post"], detail=False, url_path=r"(?P<model_id>.+?)/inst_import_support_edit")
    def inst_import_support_edit(self, request, model_id):
        add_result, update_result = InstanceManage.inst_import_support_edit(
            model_id,
            request.data.get("file").file,
            request.user.username,
        )
        return WebUtils.response_success({
            "add_result": add_result,
            "update_result": update_result,
        })

    @swagger_auto_schema(
        operation_id="inst_export",
        operation_description="实例导出",
        manual_parameters=[
            openapi.Parameter(
                "model_id",
                openapi.IN_PATH,
                description="模型ID",
                type=openapi.TYPE_STRING,
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_INTEGER, description="实例ID"),
        ),
    )
    @HasPermission("asset_list-View")
    @action(methods=["post"], detail=False, url_path=r"(?P<model_id>.+?)/inst_export")
    def inst_export(self, request, model_id):
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = f"attachment;filename={f'{model_id}_import_template.xlsx'}"
        response.write(InstanceManage.inst_export(model_id, request.data).read())
        return response

    @swagger_auto_schema(
        operation_id="instance_fulltext_search",
        operation_description="实例全文检索",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "search": openapi.Schema(type=openapi.TYPE_STRING, description="检索内容"),
                "model_id": openapi.Schema(type=openapi.TYPE_STRING, description="模型ID"),
            },
            required=["search"],
        ),
    )
    @HasPermission("search-View")
    @action(methods=["post"], detail=False)
    def fulltext_search(self, request):
        result = InstanceManage.fulltext_search(
            request.user.group_list,
            request.user.roles,
            request.data.get("search", "")
        )
        return WebUtils.response_success(result)

    @swagger_auto_schema(
        operation_id="topo_search",
        operation_description="实例拓扑查询",
        manual_parameters=[
            openapi.Parameter(
                "model_id",
                openapi.IN_PATH,
                description="模型ID",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter("inst_id", openapi.IN_PATH, description="实例ID", type=openapi.TYPE_NUMBER),
        ],
    )
    @action(
        detail=False,
        methods=["get"],
        url_path=r"topo_search/(?P<model_id>.+?)/(?P<inst_id>.+?)",
    )
    @HasPermission("asset_list-View,asset_basic_information-View,asset_relationships-View")
    def topo_search(self, request, model_id: str, inst_id: int):
        result = InstanceManage.topo_search(int(inst_id))
        return WebUtils.response_success(result)

    @swagger_auto_schema(
        operation_id="show_field_settings",
        operation_description="展示字段设置",
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_STRING, description="模型属性ID"),
        ),
    )
    @action(
        methods=["post"],
        detail=False,
        url_path=r"(?P<model_id>.+?)/show_field/settings",
    )
    @HasPermission("asset_list-View")
    def create_or_update(self, request, model_id):
        data = dict(
            model_id=model_id,
            created_by=request.user.username,
            show_fields=request.data,
        )
        result = InstanceManage.create_or_update(data)
        return WebUtils.response_success(result)

    @action(methods=["get"], detail=False, url_path=r"(?P<model_id>.+?)/show_field/detail")
    @HasPermission("asset_list-View")
    def get_info(self, request, model_id):
        result = InstanceManage.get_info(model_id, request.user.username)
        return WebUtils.response_success(result)

    @swagger_auto_schema(
        operation_id="model_inst_count",
        operation_description="模型实例数量",
    )
    @action(methods=["get"], detail=False, url_path=r"model_inst_count")
    @HasPermission("asset_list-View,view_list-View")
    def model_inst_count(self, request):
        result = InstanceManage.model_inst_count(user_groups=request.user.group_list, roles=request.user.roles)
        return WebUtils.response_success(result)

    @action(methods=["GET"], detail=False)
    @HasPermission("asset_list-View")
    def list_proxys(self, requests, *args, **kwargs):
        """
        查询云区域数据
        TODO 等节点管理开放接口后再对接接口
        """
        node_mgmt = NodeMgmt()
        data = node_mgmt.cloud_region_list()
        _data = [{"proxy_id": i['id'], "proxy_name": i['name']} for i in data]
        return WebUtils.response_success(_data)

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action

from apps.cmdb.constants import ASSOCIATION_TYPE, OPERATOR_MODEL, PERMISSION_MODEL, OPERATE, VIEW
from apps.cmdb.language.service import SettingLanguage
from apps.cmdb.models import DELETE_INST, UPDATE_INST
from apps.cmdb.services.model import ModelManage
from apps.cmdb.utils.base import get_cmdb_rules, get_default_group_id
from apps.cmdb.utils.change_record import create_change_record
from apps.cmdb.utils.permisssion_util import CmdbRulesFormatUtil
from apps.core.decorators.api_permission import HasPermission
from apps.core.utils.web_utils import WebUtils


class ModelViewSet(viewsets.ViewSet):

    @HasPermission("model_management-View")
    @action(detail=False, methods=["get"], url_path="get_model_info/(?P<model_id>.+?)")
    def get_model_info(self, request, model_id: str):
        model_info = ModelManage.search_model_info(model_id)
        if not model_info:
            return WebUtils.response_error("模型不存在", status_code=status.HTTP_404_NOT_FOUND)

        # TODO 如果使用了这个接口 补充上 默认group为default的判断 全部人都可以查看
        model_id = model_info["model_id"]
        classification_id = model_info["classification_id"]
        rules = get_cmdb_rules(request=request, permission_key=PERMISSION_MODEL)
        has_permission = CmdbRulesFormatUtil.has_object_permission(rules=rules, obj_type=PERMISSION_MODEL,
                                                                   classification_id=classification_id,
                                                                   model_id=model_id, operator=VIEW)
        if not has_permission:
            return WebUtils.response_error("抱歉！您没有此模型的权限", status_code=status.HTTP_403_FORBIDDEN)

        model_id_list, classification_id_list = CmdbRulesFormatUtil.get_rules_classification_id_list(rules=rules,
                                                                                                     classification_id=classification_id)
        if not rules or classification_id in classification_id_list or model_id in model_id_list:
            model_permission = [OPERATE, VIEW]
        else:
            if not model_id_list and not classification_id_list:
                model_permission = [OPERATE, VIEW]
            else:
                model_permission = []
        model_info['permission'] = model_permission

        return WebUtils.response_success(model_info)

    @swagger_auto_schema(
        operation_id="model_create",
        operation_description="创建模型",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "classification_id": openapi.Schema(type=openapi.TYPE_STRING, description="模型分类ID"),
                "model_id": openapi.Schema(type=openapi.TYPE_STRING, description="模型ID"),
                "model_name": openapi.Schema(type=openapi.TYPE_STRING, description="模型名称"),
                "icn": openapi.Schema(type=openapi.TYPE_STRING, description="图标"),
            },
            required=["classification_id", "model_id", "model_name", "icn"],
        ),
    )
    @HasPermission("model_management-Add Model")
    def create(self, request):
        result = ModelManage.create_model(request.data, username=request.user.username)
        return WebUtils.response_success(result)

    @swagger_auto_schema(
        operation_id="model_list",
        operation_description="查询模型",
    )
    @HasPermission("model_management-View")
    def list(self, request):
        current_team = request.COOKIES.get("current_team")
        rules = get_cmdb_rules(request=request, permission_key=PERMISSION_MODEL)
        default_group = get_default_group_id()
        if default_group:
            # 补充上查询自己组织的模型
            default_group.append(int(current_team))
        else:
            default_group = [int(current_team)]
        model_id_list, classification_id_list = CmdbRulesFormatUtil.get_rules_classification_id_list(rules)
        result = ModelManage.search_model(language=request.user.locale, classification_ids=classification_id_list,
                                          model_list=model_id_list, group_list=default_group)
        for model in result:
            model_id = model['model_id']
            cls_id = model['classification_id']
            if not rules or cls_id in classification_id_list or model_id in model_id_list:
                model_permission = [OPERATE, VIEW]
            else:
                model_permission = []
            model['permission'] = model_permission
        return WebUtils.response_success(result)

    @swagger_auto_schema(
        operation_id="model_delete",
        operation_description="删除模型",
        manual_parameters=[openapi.Parameter("id", openapi.IN_PATH, description="模型ID", type=openapi.TYPE_STRING)],
    )
    @HasPermission("model_management-Delete Model")
    def destroy(self, request, pk: str):
        model_id = pk
        model_info = ModelManage.search_model_info(pk)
        classification_id = model_info.get("classification_id")
        rules = get_cmdb_rules(request=request, permission_key=PERMISSION_MODEL)
        has_permission = CmdbRulesFormatUtil.has_object_permission(rules=rules, obj_type="model",
                                                                   classification_id=classification_id,
                                                                   model_id=model_id, operator=OPERATE)
        if not has_permission:
            return WebUtils.response_error(response_data=[], error_message="抱歉！您没有此模的权限",
                                           status_code=status.HTTP_403_FORBIDDEN)

        # 校验模型是否存在关联
        ModelManage.check_model_exist_association(pk)
        # 校验模型是否存在实例
        ModelManage.check_model_exist_inst(pk)
        # 执行删除
        model_info = ModelManage.search_model_info(pk)
        ModelManage.delete_model(model_info.get("_id"))

        create_change_record(operator=request.user.username, model_id=model_info["model_id"], label="模型管理",
                             _type=DELETE_INST, message=f"删除模型. 模型名称: {model_info['model_name']}",
                             inst_id=model_info['_id'], model_object=OPERATOR_MODEL)
        return WebUtils.response_success()

    @swagger_auto_schema(
        operation_id="model_update",
        operation_description="更改模型信息",
        manual_parameters=[openapi.Parameter("id", openapi.IN_PATH, description="模型ID", type=openapi.TYPE_STRING)],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "classification_id": openapi.Schema(type=openapi.TYPE_STRING, description="模型分类ID"),
                "model_name": openapi.Schema(type=openapi.TYPE_STRING, description="模型名称"),
                "icn": openapi.Schema(type=openapi.TYPE_STRING, description="图标"),
            },
        ),
    )
    @HasPermission("model_management-Edit Model")
    def update(self, request, pk: str):
        model_id = pk
        model_info = ModelManage.search_model_info(pk)
        classification_id = model_info.get("classification_id")
        rules = get_cmdb_rules(request=request, permission_key=PERMISSION_MODEL)
        has_permission = CmdbRulesFormatUtil.has_object_permission(rules=rules, obj_type="model",
                                                                   classification_id=classification_id,
                                                                   model_id=model_id, operator=OPERATE)
        if not has_permission:
            return WebUtils.response_error(response_data=[], error_message="抱歉！您没有此模的权限",
                                           status_code=status.HTTP_403_FORBIDDEN)

        data = ModelManage.update_model(model_info.get("_id"), request.data)
        create_change_record(operator=request.user.username, model_id=model_info["model_id"], label="模型管理",
                             _type=UPDATE_INST, message=f"修改模型. 模型名称: {model_info['model_name']}",
                             inst_id=model_info['_id'], model_object=OPERATOR_MODEL)
        return WebUtils.response_success(data)

    @swagger_auto_schema(
        operation_id="model_association_create",
        operation_description="创建模型关联",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "asst_id": openapi.Schema(type=openapi.TYPE_STRING, description="关联关系"),
                "src_model_id": openapi.Schema(type=openapi.TYPE_STRING, description="源模型ID"),
                "dst_model_id": openapi.Schema(type=openapi.TYPE_STRING, description="目标模型ID"),
                "mapping": openapi.Schema(type=openapi.TYPE_STRING, description="约束"),
            },
            required=[
                "asst_id",
                "src_model_id",
                "dst_model_id",
                "mapping",
            ],
        ),
    )
    @HasPermission("model_management-Add Model")
    @action(detail=False, methods=["post"], url_path="association")
    def model_association_create(self, request):
        rules = get_cmdb_rules(request=request, permission_key=PERMISSION_MODEL)
        src_model_id = request.data["src_model_id"]
        dst_model_id = request.data["dst_model_id"]
        src_model_info = ModelManage.search_model_info(src_model_id)
        src_classification_id = src_model_info.get("classification_id")
        src_has_permission = CmdbRulesFormatUtil.has_object_permission(rules=rules, obj_type="model",
                                                                       classification_id=src_classification_id,
                                                                       model_id=src_model_id, operator=OPERATE)
        if not src_has_permission:
            return WebUtils.response_error("抱歉！您没有源模型的权限", status_code=status.HTTP_403_FORBIDDEN)

        dst_model_info = ModelManage.search_model_info(dst_model_id)
        dst_classification_id = dst_model_info.get("classification_id")
        dst_has_permission = CmdbRulesFormatUtil.has_object_permission(rules=rules, obj_type="model",
                                                                       classification_id=dst_classification_id,
                                                                       model_id=dst_model_id, operator=OPERATE)
        if not dst_has_permission:
            return WebUtils.response_error("抱歉！您没有目标模型的权限", status_code=status.HTTP_403_FORBIDDEN)

        model_asst_id = f'{src_model_id}_{request.data["asst_id"]}_{dst_model_id}'
        result = ModelManage.model_association_create(
            src_id=src_model_info["_id"], dst_id=dst_model_info["_id"], model_asst_id=model_asst_id, **request.data
        )
        return WebUtils.response_success(result)

    @swagger_auto_schema(
        operation_id="model_association_delete",
        operation_description="删除模型关联",
        manual_parameters=[
            openapi.Parameter(
                "model_asst_id",
                openapi.IN_PATH,
                description="模型关联ID",
                type=openapi.TYPE_STRING,
            )
        ],
    )
    @HasPermission("model_management-Delete Model")
    @action(detail=False, methods=["delete"], url_path="association/(?P<model_asst_id>.+?)")
    def model_association_delete(self, request, model_asst_id: str):
        rules = get_cmdb_rules(request=request, permission_key=PERMISSION_MODEL)
        association_info = ModelManage.model_association_info_search(model_asst_id)
        src_model_id = association_info['src_model_id']
        dst_model_id = association_info['dst_model_id']
        src_model_info = ModelManage.search_model_info(src_model_id)
        src_classification_id = src_model_info.get("classification_id")
        src_has_permission = CmdbRulesFormatUtil.has_object_permission(rules=rules, obj_type="model",
                                                                       classification_id=src_classification_id,
                                                                       model_id=src_model_id, operator=OPERATE)
        if not src_has_permission:
            return WebUtils.response_error("抱歉！您没有源模型的权限", status_code=status.HTTP_403_FORBIDDEN)

        dst_model_info = ModelManage.search_model_info(dst_model_id)
        dst_classification_id = dst_model_info.get("classification_id")
        dst_has_permission = CmdbRulesFormatUtil.has_object_permission(rules=rules, obj_type="model",
                                                                       classification_id=dst_classification_id,
                                                                       model_id=dst_model_id, operator=OPERATE)
        if not dst_has_permission:
            return WebUtils.response_error("抱歉！您没有目标模型的权限", status_code=status.HTTP_403_FORBIDDEN)

        ModelManage.model_association_delete(association_info.get("_id"))
        return WebUtils.response_success()

    @swagger_auto_schema(
        operation_id="model_association_list",
        operation_description="查询模型关联",
        manual_parameters=[
            openapi.Parameter(
                "model_id",
                openapi.IN_PATH,
                description="模型ID",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    @HasPermission("model_management-View")
    @action(detail=False, methods=["get"], url_path="(?P<model_id>.+?)/association")
    def model_association_list(self, request, model_id: str):
        model_info = ModelManage.search_model_info(model_id)
        classification_id = model_info.get("classification_id")
        rules = get_cmdb_rules(request=request, permission_key=PERMISSION_MODEL)
        has_permission = CmdbRulesFormatUtil.has_object_permission(rules=rules, obj_type="model",
                                                                   classification_id=classification_id,
                                                                   model_id=model_id, operator=OPERATE)
        if not has_permission:
            return WebUtils.response_error(response_data=[], error_message="抱歉！您没有此模的权限",
                                           status_code=status.HTTP_403_FORBIDDEN)

        result = ModelManage.model_association_search(model_id)
        return WebUtils.response_success(result)

    @swagger_auto_schema(
        operation_id="model_attr_create",
        operation_description="创建模型属性",
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
                "attr_id": openapi.Schema(type=openapi.TYPE_STRING, description="属性ID"),
                "attr_name": openapi.Schema(type=openapi.TYPE_STRING, description="属性名称"),
                "attr_type": openapi.Schema(type=openapi.TYPE_STRING, description="属性类型"),
                "is_only": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="是否唯一"),
                "is_required": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="必填项"),
                "editable": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="可编辑"),
                "option": openapi.Schema(
                    type=openapi.TYPE_ARRAY, description="选项", items=openapi.Schema(type=openapi.TYPE_STRING)
                ),
                "attr_group": openapi.Schema(type=openapi.TYPE_STRING, description="属性分组"),
            },
        ),
    )
    @HasPermission("model_management-Add Model")
    @action(detail=False, methods=["post"], url_path="(?P<model_id>.+?)/attr")
    def model_attr_create(self, request, model_id):
        model_info = ModelManage.search_model_info(model_id)
        classification_id = model_info.get("classification_id")
        rules = get_cmdb_rules(request=request, permission_key=PERMISSION_MODEL)
        has_permission = CmdbRulesFormatUtil.has_object_permission(rules=rules, obj_type="model",
                                                                   classification_id=classification_id,
                                                                   model_id=model_id, operator=OPERATE)
        if not has_permission:
            return WebUtils.response_error(response_data=[], error_message="抱歉！您没有此模的权限",
                                           status_code=status.HTTP_403_FORBIDDEN)

        result = ModelManage.create_model_attr(model_id, request.data, username=request.user.username)
        return WebUtils.response_success(result)

    @swagger_auto_schema(
        operation_id="model_attr_update",
        operation_description="更新模型属性信息",
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
                "attr_id": openapi.Schema(type=openapi.TYPE_STRING, description="属性ID"),
                "attr_name": openapi.Schema(type=openapi.TYPE_STRING, description="属性名称"),
                "attr_type": openapi.Schema(type=openapi.TYPE_STRING, description="属性类型"),
                "is_only": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="是否唯一"),
                "is_required": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="必填项"),
                "editable": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="可编辑"),
                "option": openapi.Schema(type=openapi.TYPE_STRING, description="选项"),
                "attr_group": openapi.Schema(type=openapi.TYPE_STRING, description="属性分组"),
            },
        ),
    )
    @HasPermission("model_management-Edit Model")
    @action(detail=False, methods=["put"], url_path="(?P<model_id>.+?)/attr_update")
    def model_attr_update(self, request, model_id):
        model_info = ModelManage.search_model_info(model_id)
        classification_id = model_info.get("classification_id")
        rules = get_cmdb_rules(request=request, permission_key=PERMISSION_MODEL)
        has_permission = CmdbRulesFormatUtil.has_object_permission(rules=rules, obj_type="model",
                                                                   classification_id=classification_id,
                                                                   model_id=model_id, operator=OPERATE)
        if not has_permission:
            return WebUtils.response_error(response_data=[], error_message="抱歉！您没有此模的权限",
                                           status_code=status.HTTP_403_FORBIDDEN)

        result = ModelManage.update_model_attr(model_id, request.data, username=request.user.username)
        return WebUtils.response_success(result)

    @swagger_auto_schema(
        operation_id="model_attr_delete",
        operation_description="删除模型属性",
        manual_parameters=[
            openapi.Parameter(
                "model_id",
                openapi.IN_PATH,
                description="模型ID",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "attr_id",
                openapi.IN_PATH,
                description="模型属性ID",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    @HasPermission("model_management-Delete Model")
    @action(
        detail=False,
        methods=["delete"],
        url_path="(?P<model_id>.+?)/attr/(?P<attr_id>.+?)",
    )
    def model_attr_delete(self, request, model_id: str, attr_id: str):
        model_info = ModelManage.search_model_info(model_id)
        classification_id = model_info.get("classification_id")
        rules = get_cmdb_rules(request=request, permission_key=PERMISSION_MODEL)
        has_permission = CmdbRulesFormatUtil.has_object_permission(rules=rules, obj_type="model",
                                                                   classification_id=classification_id,
                                                                   model_id=model_id, operator=OPERATE)
        if not has_permission:
            return WebUtils.response_error(response_data=[], error_message="抱歉！您没有此模的权限",
                                           status_code=status.HTTP_403_FORBIDDEN)

        result = ModelManage.delete_model_attr(model_id, attr_id, username=request.user.username)
        return WebUtils.response_success(result)

    @swagger_auto_schema(
        operation_id="model_attr_list",
        operation_description="查询模型属性",
        manual_parameters=[
            openapi.Parameter(
                "model_id",
                openapi.IN_PATH,
                description="模型ID",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    @HasPermission("model_management-View")
    @action(detail=False, methods=["get"], url_path="(?P<model_id>.+?)/attr_list")
    def model_attr_list(self, request, model_id: str):
        model_info = ModelManage.search_model_info(model_id)
        classification_id = model_info.get("classification_id")
        rules = get_cmdb_rules(request=request, permission_key=PERMISSION_MODEL)
        has_permission = CmdbRulesFormatUtil.has_object_permission(rules=rules, obj_type="model",
                                                                   classification_id=classification_id,
                                                                   model_id=model_id, operator=OPERATE)
        if not has_permission:
            return WebUtils.response_error(response_data=[], error_message="抱歉！您没有此模的权限",
                                           status_code=status.HTTP_403_FORBIDDEN)

        result = ModelManage.search_model_attr(model_id, request.user.locale)
        return WebUtils.response_success(result)

    @swagger_auto_schema(
        operation_id="model_association_type",
        operation_description="查询模型关联类型",
    )
    @HasPermission("model_management-View")
    @action(detail=False, methods=["get"], url_path="model_association_type")
    def model_association_type(self, request):
        lan = SettingLanguage(request.user.locale)
        result = []
        for asso in ASSOCIATION_TYPE:
            result.append(
                {
                    "asst_id": asso["asst_id"],
                    "asst_name": lan.get_val("ASSOCIATION_TYPE", asso["asst_id"]) or asso["asst_name"],
                    "is_pre": asso["is_pre"],
                }
            )

        return WebUtils.response_success(result)

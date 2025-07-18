from apps.cmdb.constants import PERMISSION_MODEL,PERMISSION_INSTANCES
from apps.cmdb.services.model import ModelManage


class CmdbRulesFormatUtil:
    @staticmethod
    def format_rules(module, child_module, rules, cls_id = None):
        rule_items = []
        if module == PERMISSION_MODEL:
            rule_items = rules.get(module, {}).get(child_module, {})
        elif module == PERMISSION_INSTANCES:
            rule_items = rules.get(module,{}).get(cls_id,{}).get(child_module,{})
        instance_permission_map = {i["id"]: i["permission"] for i in rule_items}
        if "0" in instance_permission_map or "-1" in instance_permission_map or not instance_permission_map:
            return None
        return instance_permission_map

    @staticmethod
    def get_can_view_insts(module,child_module,rules, cls_id=None):
        # 获取可查看的实例名称集合
        instance_permission_map = CmdbRulesFormatUtil.format_rules(module,child_module,rules,cls_id)
        inst_names = []
        for inst_name,permission in instance_permission_map.items():
            if "View" in permission:
                inst_names.append(inst_name)
        return inst_names

    @staticmethod
    def has_single_permission(module,children_module,rules,inst_name,can_do,cls_id=None):
        # module为instance时，children_module为model_id, inst_name为实例名称
        #module为model时，children_module为classification，inst_name为model_id
        permission_map = CmdbRulesFormatUtil.format_rules(module,children_module,rules,cls_id)
        if permission_map is None:
            return True
        else:
            return inst_name in permission_map and can_do in permission_map[inst_name]

    @staticmethod
    def has_btch_permission(module,children_module,rules,inst_names: list,can_do,cls_id = None):
        # 批量权限验证，如果选中的其中某个实例没有operate权限则不能执行批量操作
        for inst_name in inst_names:
            if not CmdbRulesFormatUtil.has_single_permission(module,children_module,rules,inst_name,can_do,cls_id):
                return False
        return True

    @staticmethod
    def has_single_asso_permission(module,src_dict: dict,dst_dict: dict,rules,can_do):
        dst_model_id = list(dst_dict.keys())[0]
        dst_cls_id = ModelManage.search_model_info(dst_model_id)["classification_id"]
        src_model_id = list(src_dict.keys())[0]
        src_cls_id = ModelManage.search_model_info(src_model_id)["classification_id"]
        dst_inst_name = dst_dict[dst_model_id]
        src_inst_name = src_dict[src_model_id]
        dst_permission = CmdbRulesFormatUtil.has_single_permission(module,dst_model_id,rules,dst_inst_name,can_do,dst_cls_id)
        src_permission = CmdbRulesFormatUtil.has_single_permission(module,src_model_id,rules,src_inst_name,can_do,src_cls_id)
        return dst_permission and src_permission

    @staticmethod
    def has_bath_asso_permission(module,asso_list: list,rules,inst_name,can_do):
        #判断每个关联的两个模型的权限是否都包含can_do
        for asso in asso_list:
            src_model_id = asso['src_model_id']
            src_cls_id = ModelManage.search_model_info(src_model_id)["classification_id"]
            dst_model_id = asso['dst_model_id']
            dst_cls_id = ModelManage.search_model_info(dst_model_id)["classification_id"]
            inst_list = asso['inst_list']
            src_permission = CmdbRulesFormatUtil.has_single_permission(module,src_model_id,rules,inst_name,can_do,src_cls_id)
            for dst_inst in inst_list:
                dst_inst_name = dst_inst['inst_name']
                dst_permission = CmdbRulesFormatUtil.has_single_permission(module,dst_model_id,rules,dst_inst_name,can_do,dst_cls_id)
                if not dst_permission and src_permission:
                    inst_list.remove(dst_inst)
        return asso_list

    @staticmethod
    def has_model_list(module,src_model_list: list,rules,can_do):
        #查询所有模型时，根据权限过滤模型
        for model in src_model_list:
            cls_id = model["classification_id"]
            model_id = model["model_id"]
            model_permission = CmdbRulesFormatUtil.has_single_permission(module,cls_id,rules,model_id,can_do)
            if not model_permission:
                src_model_list.remove(model)
        return src_model_list

    @staticmethod
    def has_model_permission(module,children_module,rules,can_do):
        rule_items = rules.get(module, {})
        for model_list in rule_items.values():
            for model in model_list:
                model_id = model['id']
                model_permission = model['permission']
                if model_id == children_module and can_do in model_permission:
                    return True
        return False

    @staticmethod
    def get_permission_list(module,children_module,rules,inst_name,cls_id = None):
        # 获取权限列表，如果module为model时，children_module为cls_id，inst_name为model_id
        # module为instance时，children_module为model_id, inst_name为inst_name
        permission_list = []
        permission_map = CmdbRulesFormatUtil.format_rules(module,children_module, rules,cls_id)
        if permission_map is None:
            permission_list.append("Operate")
            permission_list.append("View")
        else:
            permission_list = permission_map[inst_name]
        return permission_list







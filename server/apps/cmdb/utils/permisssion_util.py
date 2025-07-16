from apps.cmdb.constants import PERMISSION_MODEL,PERMISSION_INSTANCES

class CmdbRulesFormatUtil:
    @staticmethod
    def format_rules(module, child_module, rules):
        rule_items = []
        if module == PERMISSION_MODEL:
            rule_items = rules.get(module, {}).get(child_module, {})
        elif module == PERMISSION_INSTANCES:
            all_instance = rules.get(module,{})
            for _,instance in all_instance.values():
                for model_id,rule in instance.items():
                    if model_id == child_module:
                        rule_items.append(rule[0])
        instance_permission_map = {i["id"]: i["permission"] for i in rule_items}
        if "0" in instance_permission_map or "-1" in instance_permission_map or not instance_permission_map:
            return None
        return instance_permission_map

    @staticmethod
    def has_single_permission(module,children_module,rules,inst_name,can_do):
        permission_map = CmdbRulesFormatUtil.format_rules(module,children_module,rules)
        if permission_map is None:
            return True
        else:
            return can_do in permission_map[inst_name]

    @staticmethod
    def has_btch_permission(module,children_module,rules,inst_names: list,can_do):
        for inst_name in inst_names:
            if not CmdbRulesFormatUtil.has_single_permission(module,children_module,rules,inst_name,can_do):
                return False
        return True

    @staticmethod
    def has_single_asso_permission(module,src_dict: dict,dst_dict: dict,rules,can_do):
        dst_model_id = list(dst_dict.keys())[0]
        src_model_id = list(src_dict.keys())[0]
        dst_inst_name = dst_dict[dst_model_id]
        src_inst_name = src_dict[src_model_id]
        dst_permission = CmdbRulesFormatUtil.has_single_permission(module,dst_model_id,rules,dst_inst_name,can_do)
        src_permission = CmdbRulesFormatUtil.has_single_permission(module,src_model_id,rules,src_inst_name,can_do)
        return dst_permission and src_permission

    @staticmethod
    def has_bath_asso_permission(module,asso_list: list,rules,can_do):
        #判断每个关联的两个模型的权限是否都包含can_do
        for asso in asso_list:
            src_model_id = asso.get("src_model_id")
            dst_model_id = asso.get("dst_model_id")
            src_permission = CmdbRulesFormatUtil.format_rules(module,src_model_id,rules)
            dst_permission = CmdbRulesFormatUtil.format_rules(module,dst_model_id,rules)
            if src_permission is not None and dst_permission is not None:
                for _,value in src_permission.items():
                    if can_do not in value:
                        asso_list.remove(asso)
                for _,value in dst_permission.items():
                    if can_do not in value:
                        asso_list.remove(asso)
        return asso_list







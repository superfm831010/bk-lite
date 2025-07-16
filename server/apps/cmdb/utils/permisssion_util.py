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
        permission = CmdbRulesFormatUtil.format_rules(module,children_module,rules)
        if permission is None:
            return True
        else:
            return can_do in permission[inst_name]

    @staticmethod
    def has_btch_permission(module,children_module,rules,inst_names: list,can_do):
        for inst_name in inst_names:
            if not CmdbRulesFormatUtil.has_single_permission(module,children_module,rules,inst_name,can_do):
                return False
        return True










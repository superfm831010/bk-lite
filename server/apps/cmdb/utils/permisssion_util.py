from apps.cmdb.constants import PERMISSION_MODEL, PERMISSION_INSTANCES, OPERATE, VIEW
from apps.cmdb.services.model import ModelManage


class CmdbRulesFormatUtil:

    @staticmethod
    def get_rules_classification_id_list(rules, classification_id=None):
        permission_map = CmdbRulesFormatUtil.format_permission_map(rules, classification_id)
        model_list = []
        classification_id_list = []
        for _classification_id, _permission_map in permission_map.items():
            if _permission_map["select_all"]:
                classification_id_list.append(_classification_id)
            else:
                for model_id, permission in _permission_map["permission_map"].items():
                    if VIEW in permission:
                        model_list.append(model_id)

        return model_list, classification_id_list

    @staticmethod
    def has_object_permission(rules, model_id, classification_id, obj_type, operator, instance_name=None):
        """
        检查用户是否有权限操作对象
        :param rules: 权限规则
        :param model_id: 模型id
        :param classification_id: 分类id
        :param obj_type: 对象类型，例如 "model" 或 "instance"
        :param operator: 操作类型
        :param instance_name: 实例名称（仅在obj_type为"instances"时使用）
        :return: 是否有权限
        """
        if obj_type == "model":
            permission_map = CmdbRulesFormatUtil.format_permission_map(rules=rules,
                                                                       _classification_id=classification_id)
            if not permission_map:
                # 没有权限规则时，默认有权限
                return True
            classification_permission = permission_map.get(classification_id, {})
            permission_map_data = classification_permission.get("permission_map")
            if classification_permission.get("select_all"):
                # 当是select_all时，permission_map_data为list
                return operator in permission_map_data
            # 当非select_all时，permission_map_data为dict
            return operator in permission_map_data.get(model_id, [])
        elif obj_type == "instances":
            permission_map = CmdbRulesFormatUtil.format_permission_map(rules=rules, model_id=model_id)
            if not permission_map:
                # 没有权限规则时，默认有权限
                return True
            model_permission = permission_map.get(model_id, {})
            permission_map_data = model_permission.get("permission_map")
            if model_permission.get("select_all"):
                # 当是select_all时，permission_map_data为list
                return operator in permission_map_data
            # 当非select_all时，permission_map_data为dict
            return operator in permission_map_data.get(instance_name, [])

        return False

    @staticmethod
    def format_permission_map(rules, _classification_id=None, model_id=None):
        permission_map = {}
        for classification_id, permission_data in rules.items():
            if _classification_id and classification_id != _classification_id:
                continue
            _map_data = {"select_all": False, "permission_map": {}}
            if not model_id:
                for data in permission_data:
                    if data["id"] in ["0", "-1"]:
                        _map_data["select_all"] = True
                        _map_data["permission_map"] = data["permission"]
                        permission_map[classification_id] = _map_data
                        break
                    _map_data["permission_map"][data["id"]] = data["permission"]
                    permission_map[classification_id] = _map_data

            else:
                for _model_id, _permission_data in permission_data.items():
                    if _model_id != model_id:
                        continue
                    _map_data = {"select_all": False, "permission_map": {}}
                    for _model_data in _permission_data:
                        if _model_data["id"] in ["0", "-1"]:
                            _map_data["select_all"] = True
                            _map_data["permission_map"] = _model_data["permission"]
                            permission_map[model_id] = _map_data
                            break
                        _map_data["permission_map"][_model_data["id"]] = _model_data["permission"]
                    permission_map[model_id] = _map_data
        return permission_map

    @staticmethod
    def format_rules(module: str, child_module, rules, cls_id=None):
        rule_items = []
        if module == PERMISSION_MODEL:
            rule_items = rules.get('cmdb', {}).get('normal', {}).get(module, {}).get(child_module, [])
        elif module == PERMISSION_INSTANCES:
            rule_items = rules.get('cmdb', {}).get('normal', {}).get(module, {}).get(cls_id, {}).get(child_module, [])
        instance_permission_map = {i["id"]: i["permission"] for i in rule_items}
        if "0" in instance_permission_map or "-1" in instance_permission_map or not instance_permission_map:
            return None
        return instance_permission_map

    @staticmethod
    def get_can_view_insts(rules):
        # 获取可查看的实例名称集合
        instance_permission_map = rules
        inst_names = []
        for inst_name, permission in instance_permission_map.items():
            if VIEW in permission:
                inst_names.append(inst_name)
        return inst_names

    @staticmethod
    def has_single_permission(module, children_module, rules, inst_name, can_do, cls_id=None):
        # module为instance时，children_module为model_id, inst_name为实例名称
        # module为model时，children_module为classification，inst_name为model_id
        permission_map = CmdbRulesFormatUtil.format_rules(module, children_module, rules, cls_id)
        if permission_map is None:
            return True
        else:
            return inst_name in permission_map and can_do in permission_map[inst_name]

    @staticmethod
    def has_btch_permission(module, children_module, rules, inst_names: list, can_do, cls_id=None):
        # 批量权限验证，如果选中的其中某个实例没有operate权限则不能执行批量操作
        for inst_name in inst_names:
            if not CmdbRulesFormatUtil.has_single_permission(module, children_module, rules, inst_name, can_do, cls_id):
                return False
        return True

    @staticmethod
    def has_single_asso_permission(module, src_dict: dict, dst_dict: dict, rules, can_do):
        dst_model_id = list(dst_dict.keys())[0]
        dst_cls_id = ModelManage.search_model_info(dst_model_id)["classification_id"]
        src_model_id = list(src_dict.keys())[0]
        src_cls_id = ModelManage.search_model_info(src_model_id)["classification_id"]
        dst_inst_name = dst_dict[dst_model_id]
        src_inst_name = src_dict[src_model_id]
        dst_permission = CmdbRulesFormatUtil.has_single_permission(module, dst_model_id, rules, dst_inst_name, can_do,
                                                                   dst_cls_id)
        src_permission = CmdbRulesFormatUtil.has_single_permission(module, src_model_id, rules, src_inst_name, can_do,
                                                                   src_cls_id)
        return dst_permission and src_permission

    @staticmethod
    def has_bath_asso_permission(module, asso_list: list, rules, inst_name, can_do):
        # 判断每个关联的两个模型的权限是否都包含can_do
        for asso in asso_list:
            src_model_id = asso['src_model_id']
            src_cls_id = ModelManage.search_model_info(src_model_id)["classification_id"]
            dst_model_id = asso['dst_model_id']
            dst_cls_id = ModelManage.search_model_info(dst_model_id)["classification_id"]
            if module == PERMISSION_INSTANCES:
                src_permission = CmdbRulesFormatUtil.has_single_permission(module, src_model_id, rules, inst_name,
                                                                           can_do,
                                                                           src_cls_id)
                inst_list = asso['inst_list']
                for dst_inst in inst_list:
                    dst_inst_name = dst_inst['inst_name']
                    dst_permission = CmdbRulesFormatUtil.has_single_permission(module, dst_model_id, rules,
                                                                               dst_inst_name,
                                                                               can_do, dst_cls_id)
                    if not dst_permission or not src_permission:
                        inst_list.remove(dst_inst)
            else:
                src_permission = CmdbRulesFormatUtil.has_single_permission(module, src_cls_id, rules, inst_name, can_do)
                dst_permission = CmdbRulesFormatUtil.has_single_permission(module, dst_cls_id, rules, inst_name, can_do)
                if not src_permission or not dst_permission:
                    asso_list.remove(asso)
        return asso_list

    @staticmethod
    def has_model_list(module, src_model_list: list, rules, can_do):
        # 查询所有模型时，根据权限过滤模型
        for model in src_model_list:
            cls_id = model["classification_id"]
            model_id = model["model_id"]
            model_permission = CmdbRulesFormatUtil.has_single_permission(module, cls_id, rules, model_id, can_do)
            if not model_permission:
                src_model_list.remove(model)
        return src_model_list

    @staticmethod
    def has_model_permission(module, children_module, rules, can_do):
        cls_id = ModelManage.search_model_info(children_module)["classification_id"]
        permission = CmdbRulesFormatUtil.has_single_permission(module, cls_id, rules, children_module, can_do)
        return permission

    @staticmethod
    def get_permission_list(module, children_module, rules, inst_name, cls_id=None):
        # 获取权限列表，如果module为model时，children_module为cls_id，inst_name为model_id
        # module为instance时，children_module为model_id, inst_name为inst_name
        permission_map = CmdbRulesFormatUtil.format_rules(module, children_module, rules, cls_id)
        if permission_map is None:
            permission_list = [OPERATE, VIEW]
        else:
            permission_list = permission_map.get(inst_name, [])  # 你百分百确定inst_name
        return permission_list

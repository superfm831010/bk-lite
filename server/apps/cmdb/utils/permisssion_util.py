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
                    if data["id"] in ["0"]:
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
                        if _model_data["id"] in ["0"]:
                            _map_data["select_all"] = True
                            _map_data["permission_map"] = _model_data["permission"]
                            permission_map[model_id] = _map_data
                            break
                        _map_data["permission_map"][_model_data["id"]] = _model_data["permission"]
                    permission_map[model_id] = _map_data
        return permission_map

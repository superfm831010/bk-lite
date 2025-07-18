from apps.rpc.system_mgmt import SystemMgmt


class SystemMgmtUtils:

    @staticmethod
    def get_user_all():
        result = SystemMgmt().get_all_users()
        return result["data"]

    @staticmethod
    def search_channel_list(channel_type=""):
        """email、enterprise_wechat"""
        result = SystemMgmt().search_channel_list(channel_type)
        return result["data"]

    @staticmethod
    def send_msg_with_channel(channel_id, title, content, receivers):
        result = SystemMgmt().send_msg_with_channel(channel_id, title, content, receivers)
        return result

    @staticmethod
    def format_rules(module, child_module, rules):
        rule = rules.get("monitor", {}).get("normal", {})
        map = {}
        for j in [i for i in rule.get(module, {}).values()]:
            map.update(**j)
        rule_items = map.get(child_module, [])
        instance_permission_map = {i["id"]: i["permission"] for i in rule_items}
        if "0" in instance_permission_map or "-1" in instance_permission_map or not instance_permission_map:
            return None
        return instance_permission_map

    @staticmethod
    def format_rules_v2(module, rules):
        all_permission_objs = set()
        instance_map = {}

        rule = rules.get("monitor", {}).get("normal", {})
        map = {}
        for j in [i for i in rule.get(module, {}).values()]:
            map.update(**j)

        for obj, instance_rules in map.items():
            for instance_rule in instance_rules:
                if instance_rule["id"] in {"0", "-1"}:
                    all_permission_objs.add(obj)
                    continue
                instance_map[instance_rule["id"]] = instance_rule["permission"]

        return all_permission_objs, instance_map

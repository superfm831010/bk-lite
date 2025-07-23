from apps.rpc.system_mgmt import SystemMgmt


def get_permission_rules(user, current_team, app_name, permission_key):
    """获取用户权限规则"""
    app_name_map = {
        "system_mgmt": "system-manager",
        "node_mgmt": "node",
        "console_mgmt": "ops-console",
        "mlops": "mlops",
    }
    client = SystemMgmt()
    try:
        app_name = app_name_map.get(app_name, app_name)
        user_rules = getattr(user, "rules", {}).get(app_name, {})
        if not isinstance(user_rules, dict):
            return {}, {}
        module = permission_key
        child_module = ""
        if "." in permission_key:
            module, child_module = permission_key.split(".")
        permission_data = client.get_user_rules_by_app(int(current_team), user.username, app_name, module, child_module)
        return permission_data
    except Exception:
        return {}

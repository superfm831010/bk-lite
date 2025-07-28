from django.db.models import Q

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
        module = permission_key
        child_module = ""
        if "." in permission_key:
            module, child_module = permission_key.split(".")
        permission_data = client.get_user_rules_by_app(
            int(current_team), user.username, app_name, module, child_module, user.domain
        )
        return permission_data
    except Exception:
        return {}


def permission_filter(model, permission, team_key="teams__id__in", id_key="id__in"):
    """
        模型权限过滤（单对象查询）
        model: Django model to filter.
        permission: {
            "instance":[{"id": 1, permission: ["view", "Operate"]}],
            "team":[1, 2, 3]
        }
    """

    qs = model.objects.all()

    per_instance_ids = [i["id"] for i in permission.get("instance", [])]
    per_team_ids = permission.get("team", [])

    if not per_instance_ids and not per_team_ids:
        return qs

    # 实例权限过滤
    if per_team_ids and not per_instance_ids:
        qs = qs.filter(Q(**{team_key: per_team_ids}) | Q(**{id_key: per_instance_ids}))
    elif per_instance_ids and not per_team_ids:
        qs = qs.filter(**{id_key: per_instance_ids})
    else:
        qs = qs.filter(Q(**{team_key: per_team_ids}) | Q(**{id_key: per_instance_ids}))

    return qs

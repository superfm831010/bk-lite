# -- coding: utf-8 --
# @File: base.py
# @Time: 2025/7/21 14:00
# @Author: windyzhao
from apps.core.logger import cmdb_logger as logger


def get_cmdb_rules(request) -> dict:
    """
    获取cmdb的权限规则
    :param request:
    :return: cmdb的权限规则
    """
    try:
        rules = request.user.rules.get("cmdb", {}).get("normal", {}).get("task", {})
    except Exception as err:
        rules = {}
        logger.error(f"获取cmdb权限规则失败: {err}")
    return rules

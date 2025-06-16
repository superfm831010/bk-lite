# -- coding: utf-8 --
# @File: constants.py
# @Time: 2025/5/9 14:57
# @Author: windyzhao


class AlertAccessType:
    """告警源接入类型"""
    BUILT_IN = "built_in"
    CUSTOMIZE = "customize"
    CHOICES = (
        (BUILT_IN, "内置"),
        (CUSTOMIZE, "自定义"),
    )


class AlertsSourceTypes:
    """告警源类型"""
    PROMETHEUS = "prometheus"
    ZABBIX = "zabbix"
    WEBHOOK = "webhook"
    LOG = "log"
    MONITOR = "monitor"
    CLOUD = "cloud"
    NATS = "nats"
    RESTFUL = "restful"
    CHOICES = (
        (PROMETHEUS, 'Prometheus'),
        (ZABBIX, 'Zabbix'),
        (WEBHOOK, 'Webhook'),
        (LOG, '日志'),
        (MONITOR, '监控'),
        (CLOUD, '云监控'),
        (NATS, 'NATS'),
        (RESTFUL, 'RESTFul'),
    )


class EventLevel:
    """事件级别"""
    REMAIN = "remain"
    WARNING = "warning"
    SEVERITY = "severity"
    FATAL = "fatal"

    CHOICES = (
        (REMAIN, "提醒"),
        (WARNING, "预警"),
        (SEVERITY, "严重"),
        (FATAL, "致命")
    )


class EventStatus:
    """事件状态"""
    PENDING = "pending"
    RESOLVED = "resolved"
    PROCESSING = "processing"
    CLOSED = "closed"
    SHIELD = "shield"

    CHOICES = (
        (PENDING, "待响应"),
        (PROCESSING, "处理中"),
        (RESOLVED, "已处理"),
        (CLOSED, "已关闭"),
        (SHIELD, "已屏蔽"),
    )


class EventAction:
    """告警类型"""
    CREATED = "created"
    CLOSED = "closed"

    CHOICES = (
        (CREATED, "产生"),
        (CLOSED, "关闭"),
    )


class AlertLevel:
    """告警级别"""
    WARNING = "warning"
    SEVERITY = "severity"
    FATAL = "fatal"

    CHOICES = (
        (WARNING, "预警"),
        (SEVERITY, "严重"),
        (FATAL, "致命")
    )


class AlertStatus:
    """告警状态"""
    PENDING = "pending"
    RESOLVED = "resolved"
    PROCESSING = "processing"
    CLOSED = "closed"
    UNASSIGNED = "unassigned"

    CHOICES = (
        (PENDING, "待响应"),
        (PROCESSING, "处理中"),
        (RESOLVED, "已处理"),
        (CLOSED, "已关闭"),
        (UNASSIGNED, "未分派"),
    )
    ACTIVATE_STATUS = (PENDING, PROCESSING, UNASSIGNED)


class AlertOperate:
    """告警操作"""
    ACKNOWLEDGE = "acknowledge"
    CLOSE = "close"
    REASSIGN = "reassign"
    Assign = "assign"

    CHOICES = (
        (ACKNOWLEDGE, "认领"),
        (CLOSE, "关闭"),
        (REASSIGN, "转派"),
        (Assign, "分派"),
    )


# ===
class LevelType:
    """级别类型"""
    EVENT = "event"
    ALERT = "alert"
    INCIDENT = "incident"

    CHOICES = (
        (EVENT, "事件"),
        (ALERT, "告警"),
        (INCIDENT, "事故"),
    )


DEFAULT_LEVEL = [
    {
        "level_type": LevelType.EVENT,
        "level_id": 0,
        "level_name": "Critical",
        "level_display_name": "致命",
        "color": "#F43B2C",
        "icon": "huoyanhuodongtuijian",
        "description": "",
    },
    {
        "level_type": LevelType.EVENT,
        "level_id": 1,
        "level_name": "Error",
        "level_display_name": "错误",
        "color": "#D97007",
        "icon": "weiwangguanicon-defuben-",
        "description": "",
    },
    {
        "level_type": LevelType.EVENT,
        "level_id": 2,
        "level_name": "Warning",
        "level_display_name": "预警",
        "color": "#FFAD42",
        "icon": "gantanhao1",
        "description": "",
    },
    {
        "level_type": LevelType.EVENT,
        "level_id": 3,
        "level_name": "Info",
        "level_display_name": "提醒",
        "color": "#FBBF24",
        "icon": "tixing",
        "description": "",
    },

    {
        "level_type": LevelType.ALERT,
        "level_id": 0,
        "level_name": "Critical",
        "level_display_name": "致命",
        "color": "#F43B2C",
        "icon": "huoyanhuodongtuijian",
        "description": "",
    },
    {
        "level_type": LevelType.ALERT,
        "level_id": 1,
        "level_name": "Error",
        "level_display_name": "错误",
        "color": "#D97007",
        "icon": "weiwangguanicon-defuben-",
        "description": "",
    },
    {
        "level_type": LevelType.ALERT,
        "level_id": 2,
        "level_name": "Warning",
        "level_display_name": "预警",
        "color": "#FFAD42",
        "icon": "gantanhao1",
        "description": "",
    },
    {
        "level_type": LevelType.INCIDENT,
        "level_id": 0,
        "level_name": "Critical",
        "level_display_name": "致命",
        "color": "#F43B2C",
        "icon": "huoyanhuodongtuijian",
        "description": "",
    },
    {
        "level_type": LevelType.INCIDENT,
        "level_id": 1,
        "level_name": "Error",
        "level_display_name": "错误",
        "color": "#D97007",
        "icon": "weiwangguanicon-defuben-",
        "description": "",
    },
    {
        "level_type": LevelType.INCIDENT,
        "level_id": 2,
        "level_name": "Warning",
        "level_display_name": "预警",
        "color": "#FFAD42",
        "icon": "gantanhao1",
        "description": "",
    }

]


class AlertAssignmentMatchType:
    """告警分派匹配类型"""
    ALL = "all"
    FILTER = "filter"

    CHOICES = (
        (ALL, "全部匹配"),
        (FILTER, "过滤匹配"),
    )


class AlertAssignmentNotifyChannels:
    """告警分派通知渠道"""
    EMAIL = "email"
    ENTERPRISE_WECHAT = "enterprise_wechat"

    CHOICES = (
        (EMAIL, "邮件"),
        (ENTERPRISE_WECHAT, "企业微信"),
    )


class AlertAssignmentNotificationScenario:
    """ 告警分派通知场景 """

    ASSIGNMENT = "assignment"
    RECOVERED = "recovered"

    CHOICES = (
        (ASSIGNMENT, "分派"),
        (RECOVERED, "恢复"),
    )


class AlertShieldMatchType:
    """告警屏蔽匹配类型"""
    ALL = "all"
    FILTER = "filter"

    CHOICES = (
        (ALL, "全部匹配"),
        (FILTER, "过滤匹配"),
    )

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
    CHOICES = (
        (PROMETHEUS, 'Prometheus'),
        (ZABBIX, 'Zabbix'),
        (WEBHOOK, 'Webhook'),
        (LOG, '日志'),
        (MONITOR, '监控'),
        (CLOUD, '云监控'),
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

    CHOICES = (
        (PENDING, "待响应"),
        (PROCESSING, "处理中"),
        (RESOLVED, "已处理"),
        (CLOSED, "已关闭"),
    )


class EventAction:
    """告警类型"""
    CREATED = "created"
    CLOSED = "closed"

    CHOICES = (
        (CREATED, "创建"),
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

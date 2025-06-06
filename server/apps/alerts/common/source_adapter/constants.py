# -- coding: utf-8 --
# @File: constants.py
# @Time: 2025/5/14 13:49
# @Author: windyzhao

DEFAULT_SOURCE_CONFIG = {
    "url": "/alerts/api/receiver_data/",
    "headers": {"SECRET": "your_source_secret"},
    "params": {
        "source_type": "",
        "source_id": "",
        "events": []
    },
    "content_type": "application/json",
    "method": "POST",
    "timeout": 30,
    "auth": {
        "type": "",
        "token": "your_token_here",
        "username": "user",
        "password": "pass",
        "secret_key": "your_secret"
    },
    "event_fields_mapping": {
        "title": "title",
        "description": "description",
        "level": "level",
        "item": "item",
        "start_time": "start_time",
        "end_time": "end_time",
        "labels": "labels",
        "rule_id": "rule_id",
        "external_id": "external_id",
        "resource_id": "resource_id",
        "resource_name": "resource_name",
        "resource_type": "resource_type",
        "value": "value",
        "action": "action",

    },
    "event_fields_desc_mapping": {
        "title": "事件标题, 类型字符串",
        "item": "事件指标, 类型字符串",
        "description": "事件描述，类型字符串",
        "external_id": "事件ID，类型字符串",
        "value": "事件值，float类型",
        "action": "事件类型，类型字符串，可选值为：{'created':'创建', 'closed':'关闭'}",
        "level": "事件级别，类型字符串，可选值为：{'3': '提醒', '2': '预警', '1': '严重', '0': '致命'}",
        "start_time": "事件开始时间(时间戳，毫秒级)",
        "end_time": "事件开始时间(时间戳，毫秒级)",
        "labels": "标签，格式为字典，可选，可以包含其他的所有冗余字段，如关联的资产实例",
        "rule_id": "事件规则ID，类型字符串，可选",
        "resource_id": "资源ID，类型字符串，可选",
        "resource_name": "资源实例名称，类型字符串，可选",
        "resource_type": "资源类型，类型字符串，可选",
    }
}

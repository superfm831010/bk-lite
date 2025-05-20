# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import datetime
import time

from common.cmp.cloud_apis.cloud_constant import DiskChargeType, EipStatus
from common.cmp.cloud_apis.constant import DiskCategory, SubnetStatus


def handle_time_str(time_str):
    """
    :param time_str: eg. 2018-09-28T14:48:41Z
        aliyun: 2019-09-09T04:04Z  缺少SS
    :return:
    """
    if time_str:
        time_str = time_str.replace("T", " ")
        if "Z" in time_str:
            time_str = time_str.replace("Z", "")
            try:
                time_datetime = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=8)
            except ValueError:
                time_datetime = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M") + datetime.timedelta(hours=8)
            time_str = time_datetime.strftime("%Y-%m-%d %H:%M:%S")
        return time_str
    else:
        return ""


def handle_time_stamp(time_stamp):
    """
    将时间戳转为日期
    :param time_stamp:
    :return:
    """
    try:
        ret = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_stamp))
    except OSError:
        time_stamp = time_stamp // 1000
        ret = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_stamp))
    return ret


def handle_eip_status(status):
    eip_status_dict = {
        EipStatus.CREATING.value: "创建中",
        EipStatus.BINDING.value: "绑定中",
        EipStatus.BIND.value: "已绑定",
        EipStatus.UNBINDING.value: "解绑中",
        EipStatus.UNBIND.value: "未绑定",
    }
    return eip_status_dict.get(status, "未知")


def handle_subnet_status(status):
    subnet_status_dict = {
        SubnetStatus.PENDING.value: "配置中",
        SubnetStatus.AVAILABLE.value: "可用",
        SubnetStatus.ERROR.value: "错误",
    }
    return subnet_status_dict.get(status, "配置中")


def handle_disk_category(category):
    disk_category_dict = {
        DiskCategory.CLOUD_BASIC.value: "普通云盘",
        DiskCategory.CLOUD_EFFICIENCY.value: "高效云盘",
        DiskCategory.CLOUD_SSD.value: "SSD云盘",
        DiskCategory.CLOUD_ESSD.value: "ESSD云盘",
        DiskCategory.CLOUD_UNKNOWN.value: "未知云盘",
    }
    return disk_category_dict.get(category, "未知云盘")


def handle_disk_paid_modal(disk_charge_type):
    """
    根据传入计费类型value获取对应中文显示值
    Args:
        disk_charge_type (str): 计费类型value

    Returns:

    """
    paid_modal_dict = {
        DiskChargeType.PREPAID.value: "包年包月",
        DiskChargeType.POSTPAID_BY_HOUR.value: "按量计费",
    }
    return paid_modal_dict.get(disk_charge_type, "未知计费类型")


def get_value_in_dit(value_name, dit):
    if value_name in dit:
        return dit.get(value_name)
    return ""


def check_required_params(list_params, kwargs):
    for i in list_params:
        if i not in kwargs:
            raise ValueError("missing param {}".format(i))


def set_optional_params(list_params, kwargs, obj):
    for i in list_params:
        if i in kwargs:
            obj.update({i: kwargs.get(i)})
    return obj


def fail(message=""):
    return {"result": False, "message": message}


def success(data=""):
    return {"result": True, "data": data}


def set_optional_params_huawei(list_params, kwargs, obj):
    for i in list_params:
        if i in kwargs:
            setattr(obj, i, kwargs[i])
    return obj


def init_name(name):
    """
    初始化命名
    :param name:
    :return:
    """
    new_name = name
    if name == "" or name is None:
        new_name = "未命名"
    return new_name


def init_value(list_params, object_json, value_type="str"):
    d = object_json
    value = ""
    if value_type == "list":
        value = []
    elif value_type == "dict":
        value = {}
    elif value_type == "int":
        value = 0
    for i in list_params:
        if d.get(i):
            d = d.get(i)
            value = d
        else:
            if value_type == "list":
                value = []
            elif value_type == "dict":
                value = {}
            elif value_type == "int":
                value = 0
            else:
                value = ""
            break
    return value

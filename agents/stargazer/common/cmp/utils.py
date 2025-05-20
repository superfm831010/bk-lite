# 统一管理CMP的Utils


def convert_param_to_list(param):
    """
    将传入的未定格式的参数转换成列表
    Args:
        param (all): 未确定类型参数

    Returns:

    """
    if not param and param != 0:
        return []
    if not isinstance(param, (str, list, int)):
        raise Exception("传入参数不为空时，类型仅支持str和list。请修改！")
    return param if isinstance(param, list) else [param]


import random
import time
from enum import Enum


# 公共参数
class AliChargeMode(Enum):
    SubscriptionOrder = "预付订单"
    PayAsYouGoBill = "后付账单"
    Refund = "退款"
    Adjustment = "调账"


class PublicCloudResourceType(Enum):
    QCloud = {
        "vm": {"condition": "equal", "keywords": "云服务器CVM"},
        "disk": {"condition": "equal", "keywords": "云硬盘CBS"},
        "snapshot": {"condition": "equal", "keywords": "云硬盘快照Snapshot"},
        "mysql": {"condition": "icontains", "keywords": "mysql"},
        "tdsql": {"condition": "icontains", "keywords": "tdsql"},
        "redis": {"condition": "icontains", "keywords": "redis"},
        "mongodb": {"condition": "icontains", "keywords": "mongodb"},
        "bucket": {"condition": "contains", "keywords": "对象存储"},
        "eip": {"condition": "contains", "keywords": "弹性公网"},
    }
    Aliyun = {
        "vm": {"condition": "contains", "keywords": "云服务器 ECS"},
        "disk": {"condition": "contains", "keywords": "硬盘"},
        "snapshot": {"condition": "contains", "keywords": "快照"},
        "mysql": {"condition": "icontains", "keywords": "mysql"},
        "tdsql": {"condition": "icontains", "keywords": "tdsql"},
        "redis": {"condition": "icontains", "keywords": "redis"},
        "mongodb": {"condition": "icontains", "keywords": "mongodb"},
        "bucket": {"condition": "contains", "keywords": "对象存储"},
        "eip": {"condition": "contains", "keywords": "弹性公网"},
    }
    HuaweiCloud = {
        "vm": {"condition": "equal", "keywords": "hws.resource.type.vm"},
        "disk": {"condition": "equal", "keywords": "hws.resource.type.volume"},
        "snapshot": {"condition": "", "keywords": ""},
        "mysql": {"condition": "equal", "keywords": "hws.resource.type.taurus.vm"},
        "tdsql": {"condition": "", "keywords": ""},
        "redis": {"condition": "", "keywords": ""},
        "mongodb": {"condition": "", "keywords": ""},
        "bucket": {"condition": "equal", "keywords": "hws.resource.type.obs"},
        "eip": {"condition": "equal", "keywords": "hws.resource.type.ip"},
    }


# 生成唯一流水号
def generate_serial_number(number):
    return (
        int(time.time() * 1000)
        + int(time.clock() * random.randint(1000000, 9999999))
        + int(number * int("".join(random.sample("123456789", 7))))
    )


def set_dir_size(dir_object, object_lists, cloud_type="aliyun"):
    next_objects = [item for item in object_lists if item.parent == dir_object.name]
    file_objects_sum = sum([item.size for item in next_objects if item.type == "FILE"])
    dir_objects_list = [item for item in next_objects if item.type == "DIR"]
    if dir_objects_list:
        for item in dir_objects_list:
            set_dir_size(item, object_lists)
    size = sum([item.size for item in dir_objects_list]) + file_objects_sum
    dir_object.size = round(size / 1024 / 1024, 2)
    if cloud_type == "fusioncloud":
        dir_object["dir_size"] = round(size / 1024 / 1024, 2)


def set_dir_size_qcloud(dir_object, object_lists):
    next_objects = [item for item in object_lists if item["parent"] == dir_object["name"]]
    file_objects_sum = sum([int(item["Size"]) for item in next_objects if item["type"] == "FILE"])
    dir_objects_list = [item for item in next_objects if item["type"] == "DIR"]
    if dir_objects_list:
        for item in dir_objects_list:
            set_dir_size(item, object_lists)
    size = sum([int(item["Size"]) for item in dir_objects_list]) + file_objects_sum
    dir_object["size"] = round(size / 1024 / 1024, 2)


def format_huawei_bill_charge_mode(charge_mode):
    charge_mode_dict = {"1": "包年/包月", "2": "按需", "3": "预留实例"}
    return charge_mode_dict.get(charge_mode, "未知模式")


def format_ali_bill_charge_mode(charge_mode):
    return AliChargeMode[charge_mode].value


def format_public_cloud_resource_type(cloud_type, resource_type):
    for key, value in PublicCloudResourceType[cloud_type].value.items():
        if value["condition"] == "equal":
            if value["keywords"] == resource_type:
                return key
        elif value["condition"] == "contains":
            if value["keywords"] in resource_type:
                return key
        elif value["condition"] == "icontains":
            if value["keywords"] in resource_type.lower():
                return key


def get_compute_price_module(cloud_type, account, region=None, zone=None):
    """获取计算价格模型，公有云返回价格模型，私有云返回规格价格模型"""
    pass
    # module = None
    # if cloud_type in CloudPlatform.CLOUD or cloud_type == "TCE":
    #     price_module = PriceModule.objects.filter(
    #         account__config_name=account, region_id=region, zone_id=zone).first()
    #     if price_module:
    #         compute_price_module_queryset = ComputePriceModule.objects.filter(price_module=price_module)
    #         spec_list = [
    #             (i.display_name, i.cpu, i.mem, iRegionInfo.price_per_day, i.name)
    #             for i in ComputePriceModuleDetail.objects.filter(
    #                 compute_price_module__in=compute_price_module_queryset)
    #         ]
    #         return price_module, spec_list
    #     else:
    #         return module, []
    # else:
    #     if ComputePriceModuleResource.objects.filter(account_name=account).exists():
    #         module = ComputePriceModuleResource.objects.filter(account_name=account).first()
    #     if ComputePriceModuleResource.objects.filter(account_name=account, region=region).exists():
    #         module = ComputePriceModuleResource.objects.filter(account_name=account, region=region).first()
    #     if ComputePriceModuleResource.objects.filter(account_name=account, region=region, zone=zone).exists():
    #         module = ComputePriceModuleResource.objects.filter(
    #             account_name=account, region=region, zone=zone
    #         ).first()
    #     if module:
    #         com_module = module.compute_price_module
    #         spec_list = [
    #             (i.display_name, i.cpu, i.mem, i.price_per_day, "")
    #             for i in ComputePriceModuleDetail.objects.filter(compute_price_module=com_module)
    #         ]
    #         return com_module, spec_list
    #     else:
    #         module = PriceModule.objects.filter(account__config_name=account).first()
    #         if module:
    #             com_module = ComputePriceModule.objects.filter(price_module=module)
    #             spec_list = [
    #                 (i.display_name, i.cpu, i.mem, i.price_per_day, "")
    #                 for i in ComputePriceModuleDetail.objects.filter(compute_price_module__in=com_module)
    #             ]
    #             return com_module.first(), spec_list
    #         return module, []


def get_storage_pricemodule(cloud_type, account_config_name, region_id=None, zone_id=None, disk_category=None):
    pass
    # try:
    #     module = None
    #     if cloud_type in CloudPlatform.CLOUD or cloud_type == "TCE":
    #         price_module = PriceModule.objects.filter(
    #             account__config_name=account_config_name, region_id=region_id, zone_id=zone_id).first()
    #         if price_module:
    #             storage_module = StoragePriceModule.objects.filter(
    #                 price_module=price_module).filter(name=disk_category).first()
    #             if storage_module:
    #                 return storage_module, (
    #                     storage_module.display_name,
    #                     storage_module.price_per_day,
    #                     storage_module.price_per_month
    #                 )
    #             else:
    #                 return None, ()
    #         else:
    #             return None, ()
    #     else:
    #         queryset = StoragePriceModuleResource.objects.filter(account_name=account_config_name, region="", zone="")
    #         if queryset.exists():
    #             module = queryset.first().storage_price_module
    #         queryset = StoragePriceModuleResource.objects.filter(
    #             account_name=account_config_name, region=region_id, zone="")
    #         if queryset.exists():
    #             module = queryset.first().storage_price_module
    #         queryset = StoragePriceModuleResource.objects.filter(account_name=account_config_name, region=region_id,
    #                                                              zone=zone_id)
    #         if queryset.exists():
    #             module = queryset.first().storage_price_module
    #         if module:
    #             # storage_price = (module.display_name, module.price_per_day)
    #             storage_price = (module.display_name, float("%.4f" % (module.price_per_month / 30)))
    #         else:
    #             storage_price = ()
    #         return module, storage_price
    # except Exception:
    #     logger.exception("get_storage_pricemodule error")
    #     return None, ()


def list_dict_duplicate_removal(data, resource_type):
    """
    数据根据resource_id去重,磁盘需要根据resource_id和server_id联合去重
    """
    pass
    # distinct_list = []
    # for ins in data:
    #     if resource_type == CloudResourceType.DISK.value:
    #         distinct_result = any(
    #             distinct["resource_id"] == ins["resource_id"] and distinct["server_id"] == ins["server_id"]
    #             for distinct in distinct_list
    #         )
    #     else:
    #         distinct_result = any(distinct["resource_id"] == ins["resource_id"] for distinct in distinct_list)
    #     if not distinct_result:
    #         distinct_list.append(ins)
    # return distinct_list

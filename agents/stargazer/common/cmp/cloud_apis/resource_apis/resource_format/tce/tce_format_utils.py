# -*- coding: utf-8 -*-
"""tce资源属性格式转换方法"""
from common.cmp.cloud_apis.cloud_constant import VMChargeType
from common.cmp.cloud_apis.resource_apis.resource_format.tce.tce_constant import TCEVmChargeType


# ******************************************** 实例 vm
def format_tce_vm_charge_type(charge_type):
    charge_type_dict = {
        TCEVmChargeType.PREPAID.value: VMChargeType.PREPAID.value,
        TCEVmChargeType.CDHPAID.value: VMChargeType.PREPAID.value,
        TCEVmChargeType.POSTPAID_BY_HOUR.value: VMChargeType.POSTPAID_BY_HOUR.value,
    }
    if charge_type not in charge_type_dict:
        raise Exception("主机实例付费模式{}未纳入本地TCE，请检查".format(charge_type))
    return charge_type_dict[charge_type]


# k8s
def format_tce_k8s_tag(tags):
    return [{tag.Key: tag.Value} for tag in [i.Tags for i in tags if i.Tags]]


# ************* tdsql
def format_tce_shared_detail(detail):
    if not all([detail, isinstance(detail, list)]):
        return []
    return [
        {
            "status": cur_shared_detail.Status,
            "shard_ins_id": cur_shared_detail.ShardInstanceId,
            "shard_serial_id": cur_shared_detail.ShardSerialId,
            "storage": cur_shared_detail.Storage,
            "shard_id": cur_shared_detail.ShardId,
            "mem": cur_shared_detail.Memory,
            "node_count": cur_shared_detail.NodeCount,
            "created_time": cur_shared_detail.Createtime,
        }
        for cur_shared_detail in detail
    ]


# ******************************************** bms **********************
def format_bms_status(status):
    # 多种状态映射到Failed
    return 1 if status in [1, 3, 7, 10, 11] else status


# ****************************************** ckafka
def format_ckafka_tags(tags):
    """
    格式化ckafka的tag
    :param tags:
        [tagKey, tagValue]
    :return:
    """
    if not tags:
        return []
    return [{i.TagKey: i.TagValue} for i in tags]

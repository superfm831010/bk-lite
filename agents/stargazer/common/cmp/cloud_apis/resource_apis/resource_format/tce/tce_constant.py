# -*- coding: utf-8 -*-
"""tce属性枚举"""
from enum import Enum


# ******************************************** 实例 vm
class TCEVmChargeType(Enum):
    PREPAID = "PREPAID"  # 包年包月
    POSTPAID_BY_HOUR = "POSTPAID_BY_HOUR"  # 按量计费
    CDHPAID = "CDHPAID"  # CDH计费 只对CDH计费，不对CDH上的实例计费


# ***************************************** K8S
class TCEK8SStatus(Enum):
    RUNNING = "Running"
    CREATING = "Creating"
    ABNORMAL = "Abnormal"


# ************************************** mariadb
class MariadbStatus(Enum):
    CREATING = 0  # 创建中
    PROCESSING = 1  # 流程处理中
    RUNNING = 2  # 运行中
    UNINITIALIZED = 3  # 未初始化
    QUARANTINED = -1  # 已隔离
    DELETED = -2  # 已删除


class MariadbWanIpStatus(Enum):
    """外网开通状态"""

    NONACTIVATED = 0  # 未开通
    ACTIVATED = 1  # 已开通
    SHUTDOWN = 2  # 关闭
    OPENING = 3  # 开通中


tce_disk_cn_dict = {
    "CLOUD_BASIC": "普通云硬盘",
    "CLOUD_PREMIUM": "高性能云硬盘",
    "CLOUD_SSD": "SSD云硬盘",
}

tce_bucket_cn_dict = {
    "STANDARD": "标准存储",
    "STANDARD_IA": "低频存储",
    "ARCHIVE": "归档存储",
}

REDISTYPENAME = {
    "REDIS_MASTER_SLAVE_V28": "Redis2.8主从版",
    "REDIS_MASTER_SLAVE_V32": "Redis3.2主从版(CKV主从版)",
    "REDIS_CLUSTER_V32": "Redis3.2集群版(CKV集群版)",
    "REDIS_STANDALONE_V28": "Redis2.8单机版",
    "REDIS_MASTER_SLAVE_V40": "Redis4.0主从版",
    "REDIS_CLUSTER_V40": "Redis4.0集群版",
    "REDIS_MASTER_SLAVE_V50": "Redis5.0主从版",
    "REDIS_CLUSTER_V50": "Redis5.0集群版",
}


class RedisType(Enum):
    REDIS_MASTER_SLAVE_V28 = 2
    REDIS_MASTER_SLAVE_V32 = 3
    REDIS_CLUSTER_V32 = 4
    REDIS_STANDALONE_V28 = 5
    REDIS_MASTER_SLAVE_V40 = 6
    REDIS_CLUSTER_V40 = 7
    REDIS_MASTER_SLAVE_V50 = 8
    REDIS_CLUSTER_V50 = 9

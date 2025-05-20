# -*- coding: utf-8 -*-
"""阿里云各种状态和Model中的状态双向映射"""
from enum import Enum


# ***************** 通用枚举 ***************************
class AliyunChargeType(Enum):
    PREPAID = "PrePaid"  # 包年包月
    POSTPAID = "PostPaid"  # 按需付费


class AliyunOsType(Enum):
    WINDOWS = "windows"
    LINUX = "linux"


class AliyunRegionStatus(Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "soldOut"


class AliyunInstanceStatus(Enum):
    RUNNING = "Running"
    STARTING = "Starting"
    STOPPING = "Stopping"
    STOP = "Stopped"


class AliyunInstanceChargeType(Enum):
    PREPAID = "PrePaid"  # 包年包月
    POSTPAID = "PostPaid"  # 按需付费


class AliyunDiskStatus(Enum):
    CREATING = "Creating"
    AVAILABLE = "Available"
    IN_USE = "In_use"
    REINITING = "ReIniting"
    ATTACHING = "Attaching"
    DETACHING = "Detaching"


class AliyunDiskType(Enum):
    SYSTEM = "system"
    DATA = "data"


class AliyunDiskCategory(Enum):
    CLOUD = "cloud"  # 普通云盘
    CLOUD_EFFICIENCY = "cloud_efficiency"  # 高效云盘
    CLOUD_SSD = "cloud_ssd"  # SSD盘
    CLOUD_ESSD = "cloud_essd"  # ESSD云盘
    LOCAL_SSD_PRO = "local_ssd_pro"  # I/O密集型本地盘
    LOCAL_HDD_PRO = "local_hdd_pro"  # 吞吐密集型本地盘
    EPHEMERAL = "ephemeral"  # 本地盘 已停售
    EPHEMERAL_SSD = "ephemeral_ssd"  # 本地SSD盘 已停售


class AliyunDiskChargeType(Enum):
    PREPAID = "PrePaid"
    POSTPAID = "PostPaid"


class ALiyunSnapshotStatus(Enum):
    PROGRESSING = "progressing"  # 创建中
    ACCOMPLISHED = "accomplished"  # 创建成功
    FAILED = "failed"  # 创建失败
    ALL = "all"


# ***************************** 镜像image
class AliyunImageType(Enum):
    SYSTEM = "system"
    SELF = "self"
    OTHERS = "others"
    MARKETPLACE = "marketplace"


class AliyunImageStatus(Enum):
    CREATING = "Creating"
    WAITING = "Waiting"
    AVAILABLE = "Available"
    UNAVAILABLE = "UnAvailable"
    CREATEFAILED = "CreateFailed"


# *************************** VPC
class AliyunVPCStatus(Enum):
    PENDING = "Pending"
    AVAILABLE = "Available"


# ************************* 子网 subnet
class AliyunSubnetStatus(Enum):
    PENDING = "Pending"
    AVAILABLE = "Available"


# ************************* 弹性公网 eip
class AliyunEipStatus(Enum):
    ASSOCIATING = "Associating"
    UNASSOCIATING = "Unassociating"
    INUSE = "InUse"
    AVAILABLE = "Available"


# *************************** 安全组规则 SecurityGroupRule
class AliyunSecurityGroupRuleDirection(Enum):
    INGRESS = "ingress"
    EGRESS = "egress"
    ALL = "all"


# *************************** 私有存储 PrivateStorage
class AliyunPrivateStorageStatus(Enum):
    pass


# *************************** 标签 tag
class AliyunTagType(Enum):
    pass


# *************************** 对象（桶）存储 bucket
class AliyunBucketType(Enum):
    STANDARD = "Standard"  # 标准存储
    IA = "IA"  # 低频访问
    ARCHIVE = "Archive"  # 归档存储
    COLD_ARCHIVE = "Cold_Archive"  # 冷归档存储

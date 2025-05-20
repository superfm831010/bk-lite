# -*- coding: utf-8 -*-
# @Time : 2021-01-21 10:32
from enum import Enum


class HwCloudDiskType(Enum):
    GPSSD = "GPSSD"
    GPSSD_cn = "通用型SSD云盘"

    SAS = "SAS"
    SAS_cn = "高IO云盘"

    SSD = "SSD"
    SSD_cn = "超高IO云盘"

    ESSD = "ESSD"
    ESSD_cn = "极速型SSD"


huaweicloud_disk_cn_dict = {
    "ESSD": "极速型SSD",
    "GPSSD": "通用型SSD云盘",
    "DESS_SAS": "DESS_SAS",
    "SSD": "超高IO云硬盘",
    "SAS": "高IO云盘",
    "SATA": "普通IO云硬盘",
}

huaweicloud_bucket_cn_dict = {
    "STANDARD": "标准存储",
    "WARM": "低频访问存储",
    "COLD": "归档存储",
}


class HwCloudEipChargeType(Enum):
    BANDWIDTH = "bandwidth"  # 按带宽计费
    TRAFFIC = "traffic"  # 按流量计费


class HwCloudEipStatus(Enum):
    FREEZED = "FREEZED"  # 冻结
    BIND_ERROR = "BIND_ERROR"  # 绑定失败
    BINDING = "BINDING"  # 绑定中
    PENDING_DELETE = "PENDING_DELETE"  # 释放中
    PENDING_CREATE = "PENDING_CREATE"  # 创建中
    PENDING_UPDATE = "PENDING_UPDATE"  # 更新中
    DOWN = "DOWN"  # 未绑定
    ACTIVE = "ACTIVE"  # 绑定
    ELB = "ELB"  # 绑定ELB
    ERROR = "ERROR"  # 异常失败


class HwCloudSubnetStatus(Enum):
    ERROR = "ERROR"  # 故障
    ACTIVE = "ACTIVE"  # 表示子网已挂载到ROUTER上
    UNKNOWN = "UNKNOWN"  # 表示子网还未挂载到ROUTER上


class HwCloudBucketType(Enum):
    STANDARD = "STANDARD"  # 标准存储
    WARM = "WARM"  # 低频访问存储
    COLD = "COLD"  # 归档存储


class HwCloudImageStatus(Enum):
    ACTIVE = "active"  # 镜像可以正常使用
    KILLED = "killed"  # 镜像上传错误
    DELETED = "deleted"  # 镜像已经删除
    SAVING = "saving"  # 镜像正在上传文件到后端存储
    QUEUED = "queued"  # 镜像元数据已经创建成功，等待上传镜像文件


class HwCloudImageType(Enum):
    GOLD = "gold"  # 公共镜像
    PRIVATE = "private"  # 私有镜像
    SHARED = "shared"  # 共享镜像
    MARKET = "market"  # 市场镜像


class HwCloudNetworkStatus(Enum):
    CREATING = "CREATING"  # 创建中
    OK = "OK"  # 创建成功
    ERROR = "ERROR"  # 故障


class HwCloudSnapshotStatus(Enum):
    CREATING = "creating"
    AVAILABLE = "available"
    ERROR = "error"
    DELETING = "deleting"
    ERROR_DELETING = "error_deleting"
    ROLLBACKING = "rollbacking"
    BACKING_UP = "backing-up"


class HwCloudVMStatus(Enum):
    ACTIVE = "ACTIVE"
    BUILD = "BUILD"
    DELETED = "DELETED"
    ERROR = "ERROR"
    HARD_REBOOT = "HARD_REBOOT"
    MIGRATING = "MIGRATING"
    PAUSED = "PAUSED"
    REBOOT = "REBOOT"
    REBUILD = "REBUILD"
    RESIZE = "RESIZE"
    REVERT_RESIZE = "REVERT_RESIZE"
    SHUTOFF = "SHUTOFF"
    SHELVED = "SHELVED"
    SHELVED_OFFLOADED = "SHELVED_OFFLOADED"
    SOFT_DELETED = "SOFT_DELETED"
    SUSPENDED = "SUSPENDED"
    VERIFY_RESIZE = "VERIFY_RESIZE"


class HwCloudVolumeStatus(Enum):
    CREATING = "creating"
    AVAILABLE = "available"
    IN_USE = "in-use"
    ERROR = "error"
    ATTACHING = "attaching"
    DETACHING = "detaching"
    RESTORING_BACKUP = "restoring-backup"
    BACKING_UP = "backing-up"
    ERROR_RESTORING = "error_restoring"
    UPLOADING = "uploading"
    DOWNLOADING = "downloading"
    EXTENDING = "extending"
    ERROR_EXTENDING = "error_extending"
    DELETING = "deleting"
    ERROR_DELETING = "error_deleting"
    ROLLBACKING = "rollbacking"
    ERROR_ROLLBACKING = "error_rollbacking"
    AWAITING_TRANSFER = "awaiting-transfer"


class HwCloudPaidModal(Enum):
    PREPAID = "prePaid"  # 包年包月
    POSTPAID = "postPaid"  # 按需

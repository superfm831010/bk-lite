# -*- coding: UTF-8 -*-
from enum import Enum


class AliyunVmStatus(Enum):
    RUNNING = "Running"
    STARTING = "Starting"
    STOPPING = "Stopping"
    STOPPED = "Stopped"


class QcloudVmStatus(Enum):
    PENDING = "PENDING"
    LAUNCH_FAILED = "LAUNCH_FAILED"
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    STARTING = "STARTING"
    STOPPING = "STOPPING"
    REBOOTING = "REBOOTING"
    SHUTDOWN = "SHUTDOWN"
    TERMINATING = "TERMINATING"


class AliyunVolumeStatus(Enum):
    CREATING = "Creating"
    AVAILABLE = "Available"
    IN_USE = "In_use"
    REINITING = "ReIniting"
    ATTACHING = "Attaching"
    DETACHING = "Detaching"


class QcloudVolumeStatus(Enum):
    UNATTACHED = "UNATTACHED"  # 未挂载
    ATTACHING = "ATTACHING"  # 挂载中
    ATTACHED = "ATTACHED"  # 已挂载
    DETACHING = "DETACHING"  # 解挂中
    EXPANDING = "EXPANDING"  # 扩容中
    ROLLBACKING = "ROLLBACKING"  # 回滚中
    TORECYCLE = "TORECYCLE"  # 待回收
    DUMPING = "DUMPING"  # 拷贝硬盘中


class AliyunNetworkStatus(Enum):
    PENGING = "Pending"  # 配置中
    AVAILABLE = "Available"  # 可用


class AliyunSnapshotStatus(Enum):
    PROGRESSING = "progressing"
    ACCOMPLISHED = "accomplished"
    FAILED = "failed"


class QcloudSnapshotStatus(Enum):
    NORMAL = "NORMAL"  # 正常
    CREATING = "CREATING"  # 创建中
    ROLLBACKING = "ROLLBACKING"  # 回滚中
    COPYING_FROM_REMOTE = "COPYING_FROM_REMOTE"  # 跨地域复制快照拷贝中


# image type
class AliyunImageType(Enum):
    SYSTEM = "system"
    SELF = "self"
    OTHERS = "others"
    MARKETPLACE = "marketplace"


class QcloudImageType(Enum):
    PUBLIC_IMAGE = "PUBLIC_IMAGE"
    PRIVATE_IMAGE = "PRIVATE_IMAGE"
    SHARED_IMAGE = "SHARED_IMAGE"


class AliyunImageStatus(Enum):
    CREATING = "Creating"
    WAITING = "Waiting"
    AVAILABLE = "Available"
    UNAVAILABLE = "UnAvailable"
    CREATEFAILED = "CreateFailed"


class QcloudImageStatus(Enum):
    CREATING = "CREATING"  # 创建中
    NORMAL = "NORMAL"  # 正常
    CREATEFAILED = "CREATEFAILED"  # 创建失败
    USING = "USING"  # 使用中
    SYNCING = "SYNCING"  # 同步中
    IMPORTING = "IMPORTING"  # 导入中
    IMPORTFAILED = "IMPORTFAILED"  # 导入失败


FusionComputeSiteStatus = {
    "joining": "Joining",
    "joining_cn": "加入域中",
    "exiting": "Exiting",
    "exiting_cn": "退出域中",
    "normal": "Normal",
    "normal_cn": "正常",
    "fault": "Fault",
    "fault_cn": "故障",
}


class FCVMStatus(Enum):
    RUNNING = "running"  # 运行中
    STOPPED = "stopped"  # 已停止
    UNKNOWN = "unknown"  # 未知状态
    HIBERNATED = "hibernated"  # 已休眠
    CREATING = "creating"  # 创建中
    SHUTTING_DOWN = "shutting-down"  # 删除中
    MIGRATING = "migrating"  # 迁移中
    FAULT_RESUMING = "fault-resuming"  # 故障恢复中
    STARTING = "starting"  # 启动中
    STOPPING = "stopping"  # 停止中
    HIBERNATING = "hibernating"  # 休眠中
    PAUSE = "pause"  # 已暂停
    RECYCLING = "recycling"  # 回收中


FusionComputeDiskType = {"normal": "Normal", "normal_cn": "普通", "share": "Share", "share_cn": "共享"}


class FCDiskStatus(Enum):
    CREATING = "CREATING"  # 创建中
    DELETING = "DELETING"  # 删除中
    USE = "USE"  # 可用的
    RESTORING = "RESTORING"  # 恢复中
    SNAPSHOTING = "SNAPSHOTING"  # 正在做快照
    FORMATING = "FORMATING"  # 正在格式化
    FORMATFAILED = "FORMATFAILED"  # 格式化失败
    COPYING = "COPYING"  # 拷贝中
    COPYFAILED = "COPYFAILED"  # 拷贝失败
    MAGRATING = "MAGRATING"  # 迁移中
    RESIZING = "RESIZING"  # 扩容中
    SHRINKING = "SHRINKING"  # 磁盘容量回收中


FusionComputeSnapshotType = {
    "normal": "Normal",
    "normal_cn": "普通快照",
    "backup": "Backup",
    "backup_cn": "备份点快照",
    "CBTbackup": "CBTbackup",
    "CBTbackup_cn": "CBT快照",
}


class FCSnapshotStatus(Enum):
    CREATING = "creating"  # 创建中
    RESUMING = "resuming"  # 恢复虚拟机中
    READY = "ready"  # 创建成功
    DELETING = "deleting"  # 删除中
    FAILED = "failed"  # 删除失败


# eip status
class AliyunEipStatus(Enum):
    ASSOCIATING = "Associating"  # 绑定中
    UNASSOCIATING = "Unassociating"  # 解绑中
    INUSE = "InUse"  # 已分配
    AVAILABLE = "Available"  # 可用


class QcloudEipStatus(Enum):
    CREATING = "CREATING"  # 创建中
    BINDING = "BINDING"  # 绑定中
    BIND = "BIND"  # 已绑定
    UNBINDING = "UNBINDING"  # 解绑中
    UNBIND = "UNBIND"  # 已解绑
    OFFLINING = "OFFLINING"  # 释放中
    BIND_ENI = "BIND_ENI"  # 绑定悬空弹性网卡


# 子网
class AliyunSubnetStatus(Enum):
    AVAILABLE = "Available"  # 可用
    PENDING = "Pending"  # 配置中


class AliyunDiskType(object):
    cloud = "cloud"
    cloud_cn = "普通云盘"

    cloud_efficiency = "cloud_efficiency"
    cloud_efficiency_cn = "高效云盘"

    cloud_ssd = "cloud_ssd"
    cloud_ssd_cn = "SSD云盘"

    cloud_essd = "cloud_essd"
    cloud_essd_cn = "ESSD云盘"


class QcloudDiskType(object):
    # 已无法购买
    # CLOUD_BASIC = "cloud"
    # CLOUD_BASIC_cn = "普通云盘"

    CLOUD_PREMIUM = "cloud_efficiency"
    CLOUD_PREMIUM_cn = "高效云盘"

    CLOUD_SSD = "cloud_ssd"
    CLOUD_SSD_cn = "SSD云盘"


class VmwareVirtualMachineStatus(object):
    poweredOn = "Running"
    poweredOn_cn = "运行中"

    poweredOff = "Stopped"
    poweredOff_cn = "已停止"

    suspended = "Suspended"
    suspended_cn = "挂起"


class AliyunDiskCategory(Enum):
    CLOUD = "cloud"  # 普通云盘
    CLOUD_EFFICIENCY = "cloud_efficiency"  # 高效云盘
    CLOUD_SSD = "cloud_ssd"  # SSD盘
    CLOUD_ESSD = "cloud_essd"  # ESSD云盘
    LOCAL_SSD_PRO = "local_ssd_pro"  # I/O密集型本地盘
    LOCAL_HDD_PRO = "local_hdd_pro"  # 吞吐密集型本地盘
    EPHEMERAL = "ephemeral"  # 本地盘
    EPHEMERAL_SSD = "ephemeral_ssd"  # 本地SSD盘


# 阿里云创建磁盘时使用，根据接口只支持这四种
class AliyunDiskCategoryCreate(Enum):
    CLOUD_EFFICIENCY = "cloud_efficiency"  # 高效云盘
    CLOUD_SSD = "cloud_ssd"  # SSD盘
    CLOUD_ESSD = "cloud_essd"  # ESSD云盘


class QcloudDiskCategory(Enum):
    # CLOUD_BASIC = "CLOUD_BASIC"  # 普通云硬盘  腾讯云已停用
    CLOUD_PREMIUM = "CLOUD_PREMIUM"  # 高性能云硬盘
    CLOUD_SSD = "CLOUD_SSD"  # SSD云硬盘
    CLOUD_HSSD = "CLOUD_HSSD"  # 增强型SSD云硬盘


class FCDiskCategory(Enum):
    NORMAL = "Normal"  # 普通
    SHARE = "Share"  # 共享


class VMwareDiskCategory(Enum):
    LAZY = "Lazy"  # 厚置备延迟置零
    EAGER = "Eager"  # 厚置备快速置零
    THIN = "Thin"  # 精简置备


class AliyunEipChargeType(Enum):
    PAYBYBANSWIDTH = "PayByBandwidth"  # 按带宽计费
    PAYBYTRAFFIC = "PayByTraffic"  # 按流量计费


class QCloudSnapShotType(Enum):
    PRIVATE_SNAPSHOT = "PRIVATE_SNAPSHOT"
    SHARED_SNAPSHOT = "SHARED_SNAPSHOT"


# 计费类型 私有云没有
class AliyunPaidModal(Enum):
    PREPAID = "PrePaid"  # 包年包月
    POSTPAID = "PostPaid"  # 按需付费


class QCloudPaidModal(Enum):
    PREPAID = "PREPAID"  # 包年包月
    POSTPAID_BY_HOUR = "POSTPAID_BY_HOUR"  # 按小时付费

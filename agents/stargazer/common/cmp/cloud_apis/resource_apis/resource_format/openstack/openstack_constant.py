# -*- coding: utf-8 -*-
# @Time : 2021-01-21 10:44
from enum import Enum

OpenStackVMPowerState = [
    {"es": "no state", "cn": "无状态"},
    {"es": "Running", "cn": "运行中"},
    {"es": "Paused", "cn": "暂停"},
    {"es": "Shutdown", "cn": "关机"},
    {"es": "Crashed", "cn": "崩溃"},
    {"es": "Suspended", "cn": "挂起"},
]


# vm status
class OpenStackVMStatus(Enum):
    ACTIVE = "ACTIVE"  # 运行中
    SHUTOFF = "SHUTOFF"  # 已停止
    BUILD = "BUILD"  # 创建中
    DELETED = "DELETED"  # 已删除
    VERIFY_RESIZE = "VERIFY_RESIZE"  # 确认是否调整
    REVERT_RESIZE = "REVERT_RESIZE"  # 放弃调整
    RESIZE = "RESIZE"  # 调整中
    ERROR = "ERROR"  # 错误


# volume status
class OpenStackVolumeStatus(Enum):
    CREATING = "creating"  # 创建中
    AVAILABLE = "available"  # 可用
    RESERVED = "reserved"  # 保留
    ATTACHING = "attaching"  # 挂载中
    DETACHING = "detaching"  # 卸载中
    IN_USE = "in-use"  # 使用中
    MAINTENANCE = "maintenance"  # 维护中
    DELETING = "deleting"  # 删除中
    TRANSFER = "awaiting-transfer"  # 等待转移
    ERROR = "error"  # 错误
    ERROR_DELETING = "error_deleting"  # 删除出错
    BACKING_UP = "backing-up"  # 备份中
    RESTORE_BACKUP = "restoring-backup"  # 恢复备份中
    ERROR_BACKUP = "error_backing-up"  # 备份出错
    ERROR_RESTORING = "error_restoring"  # 恢复出错
    ERROR_EXTEND = "error_extending"  # 扩展出错
    DOWNLOADING = "downloading"  # 下载中
    UPLOADING = "uploading"  # 上传中
    RETYPING = "retyping"  # 修改类型中
    EXTENDING = "extending"  # 扩展中


# network status
class OpenStackNetworkStatus(Enum):
    ACTIVE = "ACTIVE"  # 运行中
    DOWN = "DOWN"  # 停止
    BUILD = "BUILD"  # 创建中
    ERROR = "ERROR"  # 错误


# snapshot status
class OpenStackSnapshotStatus(Enum):
    CREATING = "creating"  # 创建中
    AVAILABLE = "available"  # 可用
    BACKING_UP = "backing-up"  # 备份中
    DELETING = "deleting"  # 删除中
    ERROR = "error"  # 错误
    DELETED = "deleted"  # 已删除
    UNMANAGING = "unmanaging"  # 未管理
    RESTORING = "restoring"  # 还原
    ERROR_DELETE = "error_deleting"  # 删除出错


# image status
class OpenStackImageStatus(Enum):
    QUEUED = "queued"
    SAVING = "saving"
    ACTIVE = "active"
    KILLED = "killed"
    DELETED = "deleted"
    PENDING_DELETE = "pending_delete"
    DEACTICATED = "deactivated"
    UPLOADING = "uploading"
    IMPORTING = "uploading"

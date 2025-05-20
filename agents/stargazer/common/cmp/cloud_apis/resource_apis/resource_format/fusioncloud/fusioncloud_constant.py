# -*- coding: utf-8 -*-
# @Time : 2021-01-22 17:20
from enum import Enum


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

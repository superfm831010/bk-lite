# -*- coding: utf-8 -*-
from common.cmp.cloud_apis.resource_apis.resource_format.vmware.vmware_constant import (
    VmwareDiskStatus,
    VmwareDiskType,
    VmwareImageStatus,
    VmwareImageType,
    VmwareInstanceStatus,
    VmwareSnapshotStatus,
    VmwareSnapshotType,
    VmwareStatus,
    VmwareSubnetStatus,
    VmwareVPCStatus,
)


def format_image_status():
    return VmwareImageStatus.AVAILABLE.value


def format_image_type():
    return VmwareImageType.PUBLIC.value


def format_disk_status():
    return VmwareDiskStatus.ATTACHED.value


def format_disk_type(unit_number):
    if unit_number == 0:
        return VmwareDiskType.SYSTEM_DISK.value
    else:
        return VmwareDiskType.DATA_DISK.value


def format_snapshot_status():
    return VmwareSnapshotStatus.AVAILABLE.value


def format_snapshot_type():
    return VmwareSnapshotType.VM_SNAPSHOT.value


def format_subnet_status():
    return VmwareSubnetStatus.AVAILABLE.value


def format_vpc_status():
    return VmwareVPCStatus.AVAILABLE.value


def format_instance_status(status):
    if status == VmwareInstanceStatus.RUNNING.value:
        return VmwareStatus.RUNNING.value
    elif status == VmwareInstanceStatus.STOPPING.value:
        return VmwareStatus.STOP.value
    elif status == VmwareInstanceStatus.SUSPEND.value:
        return VmwareStatus.PENDING.value
    else:
        # 返回状态不合法
        raise Exception("获取到未纳入本地的VmWare实例状态{}，无法归类，请查看并修改".format(status))

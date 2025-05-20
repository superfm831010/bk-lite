# -*- coding: utf-8 -*-
# @Time : 2021-01-21 10:29
from common.cmp.cloud_apis.cloud_constant import DiskStatus, ImageStatus, SnapshotStatus, VMStatus, VPCStatus
from common.cmp.cloud_apis.resource_apis.resource_format.openstack.openstack_constant import (
    OpenStackImageStatus,
    OpenStackNetworkStatus,
    OpenStackSnapshotStatus,
    OpenStackVMStatus,
    OpenStackVolumeStatus,
)


def handle_snapshot_status(status):
    snapshot_status_dict = {
        OpenStackSnapshotStatus.AVAILABLE.value: SnapshotStatus.NORMAL.value,
        OpenStackSnapshotStatus.CREATING.value: SnapshotStatus.CREATING.value,
        OpenStackSnapshotStatus.ERROR.value: SnapshotStatus.ERROR.value,
    }
    return snapshot_status_dict.get(status, SnapshotStatus.UNKNOWN.value)


def handle_vm_status(status):
    vm_status_dict = {
        OpenStackVMStatus.ACTIVE.value: VMStatus.RUNNING.value,
        OpenStackVMStatus.SHUTOFF.value: VMStatus.STOP.value,
        OpenStackVMStatus.ERROR.value: VMStatus.ERROR.value,
        OpenStackVMStatus.BUILD.value: VMStatus.BUILD.value,
    }
    return vm_status_dict.get(status, VMStatus.PENDING.value)


def handle_volume_status(status):
    volume_status_dict = {
        OpenStackVolumeStatus.AVAILABLE.value: DiskStatus.UNATTACHED.value,
        OpenStackVolumeStatus.IN_USE.value: DiskStatus.ATTACHED.value,
        OpenStackVolumeStatus.CREATING.value: DiskStatus.PENDING.value,
        OpenStackVolumeStatus.ERROR.value: DiskStatus.ERROR.value,
    }
    return volume_status_dict.get(
        status,
        DiskStatus.PENDING.value,
    )


def handle_network_status(status):
    network_status_dict = {
        OpenStackNetworkStatus.ACTIVE.value: VPCStatus.AVAILABLE.value,
        OpenStackNetworkStatus.ERROR.value: VPCStatus.ERROR.value,
        OpenStackNetworkStatus.BUILD.value: VPCStatus.PENDING.value,
        OpenStackNetworkStatus.DOWN.value: VPCStatus.ERROR.value,
    }
    return network_status_dict.get(
        status,
        VPCStatus.PENDING.value,
    )


def handle_image_status(image_status):
    image_status_dict = {
        OpenStackImageStatus.ACTIVE.value: ImageStatus.AVAILABLE.value,
        OpenStackImageStatus.KILLED.value: ImageStatus.UNAVAILABLE.value,
        OpenStackImageStatus.SAVING.value: ImageStatus.UNAVAILABLE.value,
    }
    return image_status_dict.get(image_status, ImageStatus.UNAVAILABLE.value)

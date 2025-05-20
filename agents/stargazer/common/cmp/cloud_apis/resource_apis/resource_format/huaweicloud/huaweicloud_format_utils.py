# -*- coding: utf-8 -*-
# @Time : 2021-01-18 19:52
from common.cmp.cloud_apis.cloud_constant import (
    BucketType,
    DiskCategory,
    DiskStatus,
    EipChargeType,
    EipStatus,
    ImageStatus,
    ImageType,
    SnapshotStatus,
    SubnetStatus,
    VMChargeType,
    VMStatus,
    VPCStatus,
)
from common.cmp.cloud_apis.resource_apis.resource_format.huaweicloud.huaweicloud_constant import (
    HwCloudBucketType,
    HwCloudDiskType,
    HwCloudEipChargeType,
    HwCloudEipStatus,
    HwCloudImageStatus,
    HwCloudImageType,
    HwCloudNetworkStatus,
    HwCloudSnapshotStatus,
    HwCloudSubnetStatus,
    HwCloudVMStatus,
    HwCloudVolumeStatus,
)


def handle_vm_status(status):
    vm_status_dict = {
        HwCloudVMStatus.ACTIVE.value: VMStatus.RUNNING.value,
        HwCloudVMStatus.ERROR.value: VMStatus.ERROR.value,
        HwCloudVMStatus.BUILD.value: VMStatus.BUILD.value,
        HwCloudVMStatus.SHUTOFF.value: VMStatus.STOP.value,
    }
    return vm_status_dict.get(status, VMStatus.PENDING.value)


def handle_volume_status(status):
    volume_status_dict = {
        HwCloudVolumeStatus.AVAILABLE.value: DiskStatus.UNATTACHED.value,
        HwCloudVolumeStatus.IN_USE.value: DiskStatus.ATTACHED.value,
        HwCloudVolumeStatus.CREATING.value: DiskStatus.PENDING.value,
        HwCloudVolumeStatus.ERROR.value: DiskStatus.ERROR.value,
    }
    return volume_status_dict.get(status, DiskStatus.PENDING)


def handle_volume_category(category):
    volume_category_dict = {
        HwCloudDiskType.SAS.value: DiskCategory.CLOUD_BASIC.value,
        HwCloudDiskType.GPSSD: DiskCategory.CLOUD_EFFICIENCY.value,
        HwCloudDiskType.SSD.value: DiskCategory.CLOUD_SSD.value,
        HwCloudDiskType.ESSD.value: DiskCategory.CLOUD_ESSD.value,
    }
    return volume_category_dict.get(category, DiskCategory.CLOUD_UNKNOWN.value)


def handle_vpc_status(status):
    vpc_status_dict = {
        HwCloudNetworkStatus.OK.value: VPCStatus.AVAILABLE.value,
        HwCloudNetworkStatus.CREATING.value: VPCStatus.PENDING.value,
        HwCloudNetworkStatus.ERROR.value: VPCStatus.ERROR.value,
    }
    return vpc_status_dict.get(status, VPCStatus.PENDING.value)


def handle_subnet_status(status):
    subnet_status_dict = {
        HwCloudSubnetStatus.ACTIVE.value: SubnetStatus.AVAILABLE.value,
        HwCloudSubnetStatus.ERROR.value: VPCStatus.ERROR.value,
        HwCloudSubnetStatus.UNKNOWN.value: VPCStatus.PENDING.value,
    }
    return subnet_status_dict.get(status, VPCStatus.PENDING.value)


def handle_eip_status(status):
    eip_status_dict = {
        HwCloudEipStatus.PENDING_CREATE.value: EipStatus.CREATING.value,
        HwCloudEipStatus.BINDING.value: EipStatus.BINDING.value,
        HwCloudEipStatus.DOWN.value: EipStatus.UNBIND.value,
        HwCloudEipStatus.ACTIVE.value: EipStatus.BIND.value,
    }
    return eip_status_dict.get(status, EipStatus.UNKNOWN.value)


def handle_snapshot_status(status):
    snapshot_status_dict = {
        HwCloudSnapshotStatus.AVAILABLE.value: SnapshotStatus.NORMAL.value,
        HwCloudSnapshotStatus.CREATING.value: SnapshotStatus.CREATING.value,
        HwCloudSnapshotStatus.ERROR.value: SnapshotStatus.ERROR.value,
    }
    return snapshot_status_dict.get(status, SnapshotStatus.UNKNOWN.value)


def handle_charge_type(charge_type):
    charge_type_dict = {
        "0": VMChargeType.POSTPAID_BY_HOUR.value,
        "1": VMChargeType.PREPAID.value,
    }
    return charge_type_dict.get(charge_type, VMChargeType.UNKNOWN.value)


def handle_image_type(image_type):
    image_type_dict = {
        HwCloudImageType.GOLD.value: ImageType.PUBLIC.value,
        HwCloudImageType.PRIVATE.value: ImageType.PRIVATE.value,
        HwCloudImageType.MARKET.value: ImageType.MARKETPLACE.value,
        HwCloudImageType.SHARED.value: ImageType.OTHERS.value,
    }
    return image_type_dict.get(image_type, ImageType.OTHERS.value)


def handle_image_status(image_status):
    image_status_dict = {
        HwCloudImageStatus.ACTIVE.value: ImageStatus.AVAILABLE.value,
        HwCloudImageStatus.KILLED.value: ImageStatus.ERROR.value,
        HwCloudImageStatus.SAVING.value: ImageStatus.UNAVAILABLE.value,
        HwCloudImageStatus.QUEUED.value: ImageStatus.ERROR.value,
    }
    return image_status_dict.get(image_status, ImageStatus.UNAVAILABLE.value)


def handle_bucket_type(bucket_type):
    bucket_type_dict = {
        HwCloudBucketType.STANDARD.value: BucketType.STANDARD.value,
        HwCloudBucketType.WARM.value: BucketType.IA.value,
        HwCloudBucketType.COLD: BucketType.ARCHIVE.value,
    }
    return bucket_type_dict.get(bucket_type, BucketType.UNKNOWN.value)


def handle_eip_charge_type(charge_type):
    eip_charge_type_dict = {
        HwCloudEipChargeType.BANDWIDTH.value: EipChargeType.PREPAID.value,
        HwCloudEipChargeType.TRAFFIC.value: EipChargeType.POSTPAID_BY_HOUR.value,
    }
    return eip_charge_type_dict.get(charge_type, EipChargeType.UNKNOWN_PAID.value)

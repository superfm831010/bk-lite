import datetime

from common.cmp.cloud_apis.cloud_constant import (
    DiskCategory,
    DiskStatus,
    ImageStatus,
    RegionStatus,
    SecurityGroupRuleDirection,
    SnapshotStatus,
    SubnetStatus,
    VMStatus,
    VPCStatus,
)
from common.cmp.cloud_apis.resource_apis.resource_format.amazonaws.amazonaws_constant import (
    AmazonAwsImageState,
    AmazonAwsRegionStatus,
    AmazonAwsSnapshotStatus,
    AmazonAwsSubnetState,
    AmazonAwsVMStatus,
    AmazonAwsVolumeStatus,
    AmazonAwsVolumeType,
    AmazonAwsVpcState,
    AwsSecurityGroupRuleDirection,
    AwsSecurityGroupRuleProtocol,
)


def format_region_status(status):
    region_status_dict = {
        AmazonAwsRegionStatus.OPT_IN_NOT_REQUIRED.value: RegionStatus.AVAILABLE.value,
        AmazonAwsRegionStatus.OPTED_IN.value: RegionStatus.AVAILABLE.value,
        AmazonAwsRegionStatus.NOT_OPTED_IN.value: RegionStatus.UNAVAILABLE.value,
    }
    return region_status_dict.get(status, RegionStatus.UNAVAILABLE.value)


def format_vm_status(status):
    vm_status_dict = {
        AmazonAwsVMStatus.RUNNING.value: VMStatus.RUNNING.value,
        AmazonAwsVMStatus.STOPPED.value: VMStatus.STOP.value,
        AmazonAwsVMStatus.STOPPING.value: VMStatus.PENDING.value,
        AmazonAwsVMStatus.TERMINATED.value: VMStatus.STOP.value,
        AmazonAwsVMStatus.SHUTTING_DOWN.value: VMStatus.STOP.value,
        AmazonAwsVMStatus.PENDING.value: VMStatus.PENDING.value,
    }
    return vm_status_dict.get(status, VMStatus.PENDING.value)


def format_volume_status(status):
    volume_status_dict = {
        AmazonAwsVolumeStatus.AVAILABLE.value: DiskStatus.UNATTACHED.value,
        AmazonAwsVolumeStatus.DELETING.value: DiskStatus.PENDING.value,
        AmazonAwsVolumeStatus.DELETED.value: DiskStatus.PENDING.value,
        AmazonAwsVolumeStatus.IN_USE.value: DiskStatus.ATTACHED.value,
        AmazonAwsVolumeStatus.CREATING.value: DiskStatus.PENDING.value,
        AmazonAwsVolumeStatus.ERROR.value: DiskStatus.ERROR.value,
    }
    return volume_status_dict.get(status, DiskStatus.PENDING)


def format_volume_category(category):
    volume_category_dict = {
        AmazonAwsVolumeType.STANDARD.value: DiskCategory.CLOUD_BASIC.value,
        AmazonAwsVolumeType.SC1.value: DiskCategory.CLOUD_EFFICIENCY.value,
        AmazonAwsVolumeType.ST1.value: DiskCategory.CLOUD_EFFICIENCY.value,
        AmazonAwsVolumeType.GP2.value: DiskCategory.CLOUD_SSD.value,
        AmazonAwsVolumeType.GP3.value: DiskCategory.CLOUD_SSD.value,
        AmazonAwsVolumeType.IO1: DiskCategory.CLOUD_ESSD.value,
        AmazonAwsVolumeType.IO2.value: DiskCategory.CLOUD_ESSD.value,
    }
    return volume_category_dict.get(category, DiskCategory.CLOUD_UNKNOWN.value)


def format_vpc_status(status):
    vpc_status_dict = {
        AmazonAwsVpcState.PENDING.value: VPCStatus.PENDING.value,
        AmazonAwsVpcState.AVAILABLE.value: VPCStatus.AVAILABLE.value,
    }
    return vpc_status_dict.get(status, VPCStatus.PENDING.value)


def format_subnet_status(status):
    subnet_status_dict = {
        AmazonAwsSubnetState.PENDING.value: SubnetStatus.PENDING.value,
        AmazonAwsSubnetState.AVAILABLE.value: SubnetStatus.AVAILABLE.value,
    }
    return subnet_status_dict.get(status, SubnetStatus.PENDING.value)


def format_is_attached(status):
    return status == AmazonAwsVolumeStatus.IN_USE.value


def format_snapshot_status(status):
    snapshot_status_dict = {
        AmazonAwsSnapshotStatus.PENDING.value: SnapshotStatus.CREATING.value,
        AmazonAwsSnapshotStatus.COMPLETED.value: SnapshotStatus.NORMAL.value,
        AmazonAwsSnapshotStatus.ERROR.value: SnapshotStatus.ERROR.value,
        AmazonAwsSnapshotStatus.RECOVERABLE.value: SnapshotStatus.NORMAL.value,
        AmazonAwsSnapshotStatus.RECOVERING.value: SnapshotStatus.ROLLBACKING.value,
        AmazonAwsSnapshotStatus.AVAILABLE.value: SnapshotStatus.NORMAL.value,
    }
    return snapshot_status_dict.get(status, SnapshotStatus.UNKNOWN.value)


def format_image_state(status):
    image_status_dict = {
        AmazonAwsImageState.PENDING.value: ImageStatus.CREATING.value,
        AmazonAwsImageState.AVAILABLE.value: ImageStatus.AVAILABLE.value,
        AmazonAwsImageState.INVALID.value: ImageStatus.UNAVAILABLE.value,
        AmazonAwsImageState.DEREGISTERED.value: ImageStatus.UNAVAILABLE.value,
        AmazonAwsImageState.TRANSIENT.value: ImageStatus.AVAILABLE.value,
        AmazonAwsImageState.FAILED.value: ImageStatus.ERROR.value,
        AmazonAwsImageState.ERROR.value: ImageStatus.ERROR.value,
    }
    return image_status_dict.get(status, ImageStatus.ERROR.value)


def format_rule_direction(direction):
    direction_dict = {
        AwsSecurityGroupRuleDirection.INGRESS.value: SecurityGroupRuleDirection.INGRESS.value,
        AwsSecurityGroupRuleDirection.EGRESS.value: SecurityGroupRuleDirection.EGRESS.value,
    }
    return direction_dict.get(direction, "")


def format_rule_protocol(protocol):
    protocol_dict = {
        AwsSecurityGroupRuleProtocol.TCP.value: "TCP",
        AwsSecurityGroupRuleProtocol.UDP.value: "UDP",
        AwsSecurityGroupRuleProtocol.Imonitor.cmp.value: "ICMP",
        AwsSecurityGroupRuleProtocol.ICMPv6.value: "ICMPv6",
        AwsSecurityGroupRuleProtocol.ALL.value: "ALL",
    }
    return protocol_dict.get(protocol, AwsSecurityGroupRuleProtocol.ALL.value)


# *********************** Common ***********************
def format_tag(tags):
    if not tags:
        return []
    object_item = tags["item"]
    if type(object_item) is not list:
        object_item = [object_item]
    return ["{}:{}".format(cur_kv["key"], cur_kv["value"]) for cur_kv in object_item]


def handle_time_str(time_str):
    """
    :param time_str: eg. 2018-09-28T14:48:41.000Z
    :return:
    """
    if time_str:
        time_str = time_str.replace("T", " ")
        if "Z" in time_str:
            time_str = time_str.replace("Z", "")
            try:
                time_datetime = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f") + datetime.timedelta(
                    hours=8
                )
            except ValueError:
                time_datetime = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M") + datetime.timedelta(hours=8)
            time_str = time_datetime.strftime("%Y-%m-%d %H:%M:%S")
        return time_str
    else:
        return ""

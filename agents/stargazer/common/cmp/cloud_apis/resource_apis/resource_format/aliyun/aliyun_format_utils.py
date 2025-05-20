# -*- coding: utf-8 -*-
"""阿里云转换数据格式时的工具方法"""
from common.cmp.cloud_apis.cloud_constant import (
    BucketType,
    DiskCategory,
    DiskChargeType,
    DiskStatus,
    DiskType,
    EipStatus,
    ImageStatus,
    ImageType,
    OSType,
    PrivateStorageStatus,
    RegionStatus,
    SecurityGroupRuleDirection,
    SnapshotStatus,
    SubnetStatus,
    TagType,
    VMChargeType,
    VMStatus,
    VPCStatus,
)
from common.cmp.cloud_apis.resource_apis.resource_format.aliyun.aliyun_constant import (
    AliyunBucketType,
    AliyunChargeType,
    AliyunDiskCategory,
    AliyunDiskStatus,
    AliyunDiskType,
    AliyunEipStatus,
    AliyunImageStatus,
    AliyunImageType,
    AliyunInstanceStatus,
    AliyunOsType,
    AliyunPrivateStorageStatus,
    AliyunRegionStatus,
    AliyunSecurityGroupRuleDirection,
    ALiyunSnapshotStatus,
    AliyunSubnetStatus,
    AliyunTagType,
    AliyunVPCStatus,
)


# *********************** 公用 ***********************
def format_tag(tags):
    if not tags:
        return []
    return ["{}:{}".format(cur_kv["TagKey"], cur_kv["TagValue"]) for cur_kv in tags["Tag"]]


def format_charge_type(charge_type):
    if charge_type == AliyunChargeType.POSTPAID.value:
        return VMChargeType.POSTPAID_BY_HOUR.value
    elif charge_type == AliyunChargeType.PREPAID.value:
        return VMChargeType.PREPAID.value
    else:
        raise Exception("获取到未纳入本地的阿里云付费类型{}，请检查。".format(charge_type))


# ********************** 区域
def format_region_status(status):
    """
    转换区域状态
    Args:
        status ():

    Returns:

    """
    if status == AliyunRegionStatus.AVAILABLE.value:
        return RegionStatus.AVAILABLE.value
    elif status == AliyunRegionStatus.UNAVAILABLE.value:
        return RegionStatus.UNAVAILABLE.value
    else:
        # 返回状态不合法
        raise Exception("获取到未纳入本地的阿里云区域状态{}，无法归类，请修改".format(status))


def format_instance_status(status):
    if status in {AliyunInstanceStatus.STARTING.value, AliyunInstanceStatus.RUNNING.value}:
        return VMStatus.RUNNING.value
    elif status in {AliyunInstanceStatus.STOPPING.value, AliyunInstanceStatus.STOP.value}:
        return VMStatus.STOP.value
    else:
        # 返回状态不合法
        raise Exception("获取到未纳入本地的阿里云实例状态{}，无法归类，请查看并修改".format(status))


def format_instance_charge_type(charge_type):
    if charge_type == AliyunChargeType.POSTPAID.value:
        return VMChargeType.POSTPAID_BY_HOUR.value
    elif charge_type == AliyunChargeType.PREPAID.value:
        return VMChargeType.PREPAID.value
    else:
        raise Exception("获取到未纳入本地的阿里云实例付费类型{}，请检查。".format(charge_type))


def format_disk_status(status):
    if status in [
        AliyunDiskStatus.ATTACHING.value,
        AliyunDiskStatus.DETACHING.value,
        AliyunDiskStatus.CREATING.value,
        AliyunDiskStatus.REINITING.value,
    ]:
        return DiskStatus.PENDING.value
    elif status == AliyunDiskStatus.AVAILABLE.value:
        return DiskStatus.UNATTACHED.value
    elif status == AliyunDiskStatus.IN_USE.value:
        return DiskStatus.ATTACHED.value
    else:
        return DiskStatus.ERROR.value


def format_disk_type(disk_type):
    disk_type_dict = {
        AliyunDiskType.SYSTEM.value: DiskType.SYSTEM_DISK.value,
        AliyunDiskType.DATA.value: DiskType.DATA_DISK.value,
    }
    if disk_type not in disk_type_dict:
        raise Exception("获取到未纳入本地的阿里云磁盘类型{}，无法处理".format(disk_type))
    return disk_type_dict[disk_type]


def format_disk_category(category):
    if category in {
        AliyunDiskCategory.CLOUD.value,
        AliyunDiskCategory.EPHEMERAL.value,
        AliyunDiskCategory.LOCAL_HDD_PRO.value,
    }:
        return DiskCategory.CLOUD_BASIC.value
    elif category == AliyunDiskCategory.CLOUD_EFFICIENCY.value:
        return DiskCategory.CLOUD_EFFICIENCY.value
    elif category in {
        AliyunDiskCategory.CLOUD_SSD.value,
        AliyunDiskCategory.LOCAL_SSD_PRO,
        AliyunDiskCategory.EPHEMERAL_SSD.value,
    }:
        return DiskCategory.CLOUD_SSD.value
    elif category == AliyunDiskCategory.CLOUD_ESSD.value:
        return DiskCategory.CLOUD_ESSD.value
    else:
        raise Exception("获取到未纳入本地的阿里云磁盘类型{}，请检查".format(category))


def format_disk_charge_type(charge_type):
    disk_charge_type_dict = {
        AliyunChargeType.PREPAID.value: DiskChargeType.PREPAID.value,
        AliyunChargeType.POSTPAID.value: DiskChargeType.POSTPAID_BY_HOUR.value,
    }
    if charge_type not in disk_charge_type_dict:
        raise Exception("获取到未纳入本地的阿里云磁盘类型{}，无法处理".format(charge_type))
    return disk_charge_type_dict[charge_type]


def format_is_attached(status):
    return status == AliyunDiskStatus.IN_USE.value


def format_server_id(status, instance_id):
    return instance_id if status == AliyunDiskStatus.IN_USE.value else ""


# ********************* 快照 snapshot ******************
def format_snapshot_status(status):
    if status == ALiyunSnapshotStatus.PROGRESSING.value:
        return SnapshotStatus.CREATING.value
    elif status == ALiyunSnapshotStatus.ACCOMPLISHED.value:
        return SnapshotStatus.NORMAL.value
    elif status == ALiyunSnapshotStatus.FAILED.value:
        return SnapshotStatus.ERROR.value
    else:
        raise Exception("获取到未纳入本地的阿里云快照状态{}，无法处理".format(status))


# ************************ 镜像 image
def format_image_type(image_type):
    image_type_dict = {
        AliyunImageType.SYSTEM.value: ImageType.PUBLIC.value,
        AliyunImageType.SELF.value: ImageType.PRIVATE.value,
        AliyunImageType.MARKETPLACE.value: ImageType.MARKETPLACE.value,
        AliyunImageType.OTHERS.value: ImageType.OTHERS.value,
    }
    if image_type not in image_type_dict:
        raise Exception("获取到未纳入本地的阿里云快照类型{}，无法处理".format(image_type))
    return image_type_dict[image_type]


def format_os_type(os_type):
    os_type_dict = {
        AliyunOsType.WINDOWS.value: OSType.WINDOWS.value,
        AliyunOsType.LINUX.value: OSType.LINUX.value,
    }
    return os_type_dict.get(os_type, OSType.UNKNOWN.value)


def format_image_status(status):
    image_status_dict = {
        AliyunImageStatus.UNAVAILABLE.value: ImageStatus.UNAVAILABLE.value,
        AliyunImageStatus.AVAILABLE.value: ImageStatus.AVAILABLE.value,
        AliyunImageStatus.CREATING.value: ImageStatus.CREATING.value,
        AliyunImageStatus.CREATEFAILED.value: ImageStatus.ERROR.value,
    }
    if status not in image_status_dict:
        raise Exception("获取到未纳入本地的阿里云镜像状态{}，无法处理".format(status))
    return image_status_dict[status]


# **************************** vpc
def format_vpc_status(status):
    vpc_status_dict = {
        AliyunVPCStatus.PENDING.value: VPCStatus.PENDING.value,
        AliyunVPCStatus.AVAILABLE.value: VPCStatus.AVAILABLE.value,
    }
    return vpc_status_dict.get(status, VPCStatus.ERROR.value)


# **************************** 子网subnet
def format_subnet_status(status):
    subnet_status_dict = {
        AliyunSubnetStatus.PENDING.value: SubnetStatus.PENDING.value,
        AliyunSubnetStatus.AVAILABLE.value: SubnetStatus.AVAILABLE.value,
    }
    return subnet_status_dict.get(status, SubnetStatus.ERROR.value)


# **************************** 弹性公网 eip
def format_eip_status(status):
    eip_status_dict = {
        AliyunEipStatus.ASSOCIATING.value: EipStatus.BINDING.value,
        AliyunEipStatus.UNASSOCIATING.value: EipStatus.UNBINDING.value,
        AliyunEipStatus.INUSE.value: EipStatus.BIND.value,
        AliyunEipStatus.AVAILABLE.value: EipStatus.UNBIND.value,
    }
    return eip_status_dict.get(status, EipStatus.UNKNOWN.value)


# **************************** 安全组规则 SecurityGroupRule
def format_rule_direction(direction):
    direction_dict = {
        AliyunSecurityGroupRuleDirection.INGRESS.value: SecurityGroupRuleDirection.INGRESS.value,
        AliyunSecurityGroupRuleDirection.EGRESS.value: SecurityGroupRuleDirection.EGRESS.value,
        AliyunSecurityGroupRuleDirection.ALL.value: SecurityGroupRuleDirection.ALL.value,
    }
    return direction_dict.get(direction, SecurityGroupRuleDirection.ALL.value)


# **************************** 私有存储 PrivateStorage
def format_private_storage_status(status):
    status_dict = {
        AliyunPrivateStorageStatus.ASSOCIATING.value: PrivateStorageStatus.AVAILABLE.value,
        AliyunPrivateStorageStatus.UNASSOCIATING.value: PrivateStorageStatus.PENDING.value,
    }
    return status_dict.get(status, PrivateStorageStatus.ERROR.value)


# **************************** 标签 tag
def format_tag_type(tag_type):
    tag_type_dict = {
        AliyunTagType.ASSOCIATING.value: TagType.BUILD_IN.value,
        AliyunTagType.UNASSOCIATING.value: TagType.SELF_DEFINE.value,
    }
    if tag_type not in tag_type_dict:
        raise Exception("获取到未纳入本地的阿里云标签类型{}，无法处理".format(tag_type))
    return tag_type_dict[tag_type]


# ****************************** 桶存储 bucket
def format_bucket_type(bucket_type):
    if not bucket_type:
        return bucket_type
    bucket_type_dict = {
        AliyunBucketType.STANDARD.value: BucketType.STANDARD.value,
        AliyunBucketType.IA.value: BucketType.IA.value,
        AliyunBucketType.ARCHIVE.value: BucketType.ARCHIVE.value,
    }
    if bucket_type not in bucket_type_dict:
        raise Exception("获取到未纳入本地的阿里云桶存储类型【{}】，无法处理".format(bucket_type))
    return bucket_type_dict[bucket_type]


# ****************************** 负载均衡监听详情 Listener
def format_listen_config(object_json):
    """
    HTTPListenerConfig:健康检查协议//端口/域名/路径/响应超时时间/间隔时间/健康阈值/不健康阈值/状态返回码，是否开启健康检查
    HTTPSListenerConfig 比HTTP多证书ID，
    TCPListenerConfig  协议 端口 响应超时时间/间隔时间/健康阈值/不健康阈值
    UDPListenerConfig  协议 端口 响应超时时间/间隔时间/健康阈值/不健康阈值 请求 返回结果
    :param object_json:
    :return:
    """
    listener_protocol = object_json.get("ListenerProtocol")
    if not listener_protocol:
        return {}
    configs = {
        "band_width": object_json.get("Bandwidth", ""),
        "scheduler": object_json.get("Scheduler", ""),
        "acl_status": object_json.get("AclStatus", ""),
        "un_threshold": object_json.get("UnHealthyThreshold", ""),
    }
    if listener_protocol.lower() == "udp":
        object_json_u = object_json.get("UDPListenerConfig")
        configs.update(
            {
                "protocol": object_json.get("ListenerProtocol", "udp"),
                "port": object_json_u.get("HealthCheckConnectPort"),
                "timeout": object_json_u.get("HealthCheckConnectTimeout"),
                "interval": object_json_u.get("HealthCheckInterval"),
                "threshold": object_json_u.get("HealthyThreshold"),
                "request": object_json_u.get("HealthCheckReq", ""),
                "response": object_json_u.get("HealthCheckExp", ""),
                "established_timeout": object_json_u.get("EstablishedTimeout", ""),
            }
        )
        return configs
    elif listener_protocol.lower() == "tcp":
        object_json_t = object_json.get("TCPListenerConfig")
        configs.update(
            {
                "protocol": object_json.get("ListenerProtocol", "tcp"),
                "port": object_json_t.get("HealthCheckConnectPort"),
                "timeout": object_json_t.get("HealthCheckConnectTimeout"),
                "interval": object_json_t.get("HealthCheckInterval"),
                "threshold": object_json_t.get("HealthyThreshold"),
                "sticky": object_json_t.get("StickySession", ""),
                "established_timeout": object_json_t.get("EstablishedTimeout", ""),
            }
        )
        return configs
    elif listener_protocol.lower() == "http":
        object_json_h = object_json.get("HTTPListenerConfig")
        configs.update(
            {
                "protocol": object_json_h.get("HealthCheckHttpVersion", "http"),
                "port": object_json_h.get("HealthCheckConnectPort"),
                "domain": object_json_h.get("HealthCheckDomain"),
                "path": object_json_h.get("HealthCheckURI"),
                "timeout": object_json_h.get("HealthCheckTimeout"),
                "interval": object_json_h.get("HealthCheckInterval"),
                "threshold": object_json_h.get("HealthyThreshold"),
                "code": object_json_h.get("HealthCheckHttpCode"),
                "check": object_json_h.get("HealthCheck"),
                "sticky": object_json_h.get("StickySession", ""),
                "established_timeout": object_json_h.get("EstablishedTimeout", ""),
            }
        )
        return configs
    elif listener_protocol.lower() == "https":
        object_json_hs = object_json.get("HTTPSListenerConfig")
        configs.update(
            {
                "protocol": object_json_hs.get("HealthCheckHttpVersion", "http"),
                "port": object_json_hs.get("HealthCheckConnectPort"),
                "domain": object_json_hs.get("HealthCheckDomain"),
                "path": object_json_hs.get("HealthCheckURI"),
                "timeout": object_json_hs.get("HealthCheckTimeout"),
                "interval": object_json_hs.get("HealthCheckInterval"),
                "threshold": object_json_hs.get("HealthyThreshold"),
                "code": object_json_hs.get("HealthCheckHttpCode"),
                "check": object_json_hs.get("HealthCheck"),
                "certificate": object_json_hs.get("ServerCertificateId"),
                "sticky": object_json_hs.get("StickySession", ""),
                "established_timeout": object_json_hs.get("EstablishedTimeout", ""),
            }
        )
        return configs
    else:
        raise ValueError("No support {} listener protocol".format(listener_protocol))

# -*- coding: utf-8 -*-
"""腾讯云数据格式转换"""
import hashlib
import threading

from common.cmp.cloud_apis.cloud_object.base import (
    VM,
    VPC,
    Balance,
    Bucket,
    BucketFile,
    Disk,
    Eip,
    Image,
    InstanceType,
    InstanceTypeFamily,
    LoadBalancer,
    LoadBalancerListener,
    Region,
    RelayRule,
    RouteEntry,
    RouteTable,
    SecurityGroup,
    SecurityGroupRule,
    Snapshot,
    SnapshotPolicy,
    Subnet,
    Tag,
    Transactions,
    Zone,
)
from common.cmp.cloud_apis.resource_apis.resource_format.qcloud.qcloud_format_utils import (
    format_bucket_type,
    format_qcloud_disk_charge_type,
    format_qcloud_disk_status,
    format_qcloud_disk_type,
    format_qcloud_eip_status,
    format_qcloud_image_status,
    format_qcloud_image_type,
    format_qcloud_restrict_state,
    format_qcloud_security_group_rule_direction,
    format_qcloud_snapshot_status,
    format_qcloud_status,
    format_qcloud_tag,
    format_qcloud_vm_charge_type,
    format_qcloud_vm_status,
    get_qcloud_eip_charge_type,
    get_qcloud_subnet_status,
    get_qcloud_vpc_status,
)
from common.cmp.cloud_apis.resource_apis.utils import handle_time_str


class QCloudResourceFormat:
    """格式化资源数据"""

    _instance_lock = threading.Lock()

    def __init__(self, account_id="", cloud_type="", region_id="", zone_id=""):
        self.account_id = account_id
        self.cloud_type = cloud_type
        self.region_id = region_id
        self.zone_id = zone_id

    def format_region(self, object_json, **kwargs):
        return Region(
            resource_id=object_json.Region,
            resource_name=object_json.RegionName,
            cloud_type=self.cloud_type,
            status=format_qcloud_status(object_json.RegionState),
        ).to_dict()

    def format_zone(self, object_json, **kwargs):
        return Zone(
            region=self.region_id,
            resource_id=object_json.Zone,
            resource_name=object_json.ZoneName,
            cloud_type=self.cloud_type,
            status=format_qcloud_status(object_json.ZoneState),
        ).to_dict()

    def format_instance_type_family(self, object_json, **kwargs):
        return InstanceTypeFamily(
            resource_id=object_json.InstanceFamily,
            resource_name=object_json.InstanceFamilyName,
            cloud_type=self.cloud_type,
        ).to_dict()

    def format_instance_type(self, object_json, **kwargs):
        return InstanceType(
            resource_id=object_json.InstanceType,
            resource_name=object_json.InstanceType,
            cloud_type=self.cloud_type,
            vcpus=object_json.CPU,
            memory=object_json.Memory * 1024,
            instance_family=object_json.InstanceFamily,
            zone=object_json.Zone,
            region=self.region_id,
        ).to_dict()

    def format_vm(self, object_json, **kwargs):
        # 腾讯云内置对象，无法json序列化。先转换
        system_disk = (
            {
                "id": object_json.SystemDisk.DiskId,
                "disk_size": object_json.SystemDisk.DiskSize,
                "disk_type": object_json.SystemDisk.DiskType,
            }
            if object_json.SystemDisk
            else {}
        )
        data_disk = (
            [
                {
                    "disk_size": getattr(i, "DiskSize", 0),
                    "disk_type": getattr(i, "DiskType", ""),
                    "id": getattr(i, "DiskId", ""),
                    "delete_with_instance": getattr(i, "DeleteWithInstance", ""),
                    "snapshot_id": getattr(i, "SnapshotId", ""),
                    "encrypt": getattr(i, "Encrypt", False),
                    "through_put_performance": getattr(i, "ThroughputPerformance", ""),
                }
                for i in object_json.DataDisks
                if i
            ]
            if object_json.DataDisks
            else []
        )
        internet_accessible_obj = object_json.InternetAccessible
        internet_accessible = (
            {
                "bandwidth_package_id": getattr(internet_accessible_obj, "BandwidthPackageId", "") or "",
                "internet_charge_type": getattr(internet_accessible_obj, "InternetChargeType", "") or "",
                "internet_max_bandwidth_out": getattr(internet_accessible_obj, "InternetMaxBandwidthOut", "") or "",
                "publicIp_assigned": getattr(internet_accessible_obj, "PublicIpAssigned", "") or "",
            }
            if internet_accessible_obj
            else {}
        )
        login_setting_obj = object_json.LoginSettings
        login_setting = (
            {
                "password": getattr(login_setting_obj, "Password") or "",
                "key_ids": getattr(login_setting_obj, "KeyIds") or "",
                "keep_image_login": getattr(login_setting_obj, "KeepImageLogin") or "",
            }
            if login_setting_obj
            else {}
        )
        return VM(
            resource_id=object_json.InstanceId,
            resource_name=object_json.InstanceName,
            instance_type=object_json.InstanceType,
            vcpus=object_json.CPU,
            cloud_type=self.cloud_type,
            memory=int(object_json.Memory) * 1024,
            image=object_json.ImageId or "",
            os_name=object_json.OsName or "",
            restrict_state=format_qcloud_restrict_state(object_json.RestrictState),
            status=format_qcloud_vm_status(object_json.InstanceState),
            inner_ip=object_json.PrivateIpAddresses or [],
            public_ip=object_json.PublicIpAddresses or [],
            system_disk=system_disk or {},
            data_disk=data_disk or {},
            charge_type=format_qcloud_vm_charge_type(object_json.InstanceChargeType),
            internet_accessible=internet_accessible,
            vpc=object_json.VirtualPrivateCloud.VpcId or "",
            subnet=object_json.VirtualPrivateCloud.SubnetId or "",
            security_group=object_json.SecurityGroupIds or [],
            zone=object_json.Placement.Zone or "",
            project=object_json.Placement.ProjectId or "",
            region=self.region_id,
            login_settings=login_setting,
            create_time=handle_time_str(object_json.CreatedTime),
            expired_time=handle_time_str(object_json.ExpiredTime),
            uuid=object_json.Uuid or "",
            tag=format_qcloud_tag(object_json.Tags),
            extra={},
        ).to_dict()

    def format_disk(self, object_json, **kwargs):
        category_dict = {"CLOUD_PREMIUM": "CLOUD_EFFICIENCY", "CLOUD_HDDS": "CLOUD_ESSD"}
        return Disk(
            cloud_type=self.cloud_type,
            resource_id=object_json.DiskId,
            resource_name=object_json.DiskName or "未命名",
            disk_type=format_qcloud_disk_type(object_json.DiskUsage),
            disk_size=object_json.DiskSize,
            charge_type=format_qcloud_disk_charge_type(object_json.DiskChargeType),
            portable=object_json.Portable,
            snapshot_ability=object_json.SnapshotAbility,
            status=format_qcloud_disk_status(object_json.DiskState),
            category=category_dict.get(object_json.DiskType, object_json.DiskType),
            is_attached=object_json.Attached,
            server_id=object_json.InstanceId,
            create_time=handle_time_str(object_json.CreateTime),
            expired_time=object_json.DeadlineTime,
            encrypt=object_json.Encrypt,
            delete_with_instance=object_json.DeleteWithInstance,
            project=object_json.Placement.ProjectId,
            zone=object_json.Placement.Zone,
            region=self.region_id,
            snapshot_policy=object_json.AutoSnapshotPolicyIds or "",
            extra={
                "Shareable": object_json.Shareable,
                "DeleteWithInstance": object_json.DeleteWithInstance,
                "RenewFlag": object_json.RenewFlag,
            },
        ).to_dict()

    def format_snapshot(self, object_json, **kwargs):
        return Snapshot(
            resource_id=object_json.SnapshotId,
            resource_name=object_json.SnapshotName or "未命名",
            cloud_type=self.cloud_type,
            disk_id=object_json.DiskId,
            disk_type=format_qcloud_disk_type(object_json.DiskUsage),
            disk_size=object_json.DiskSize,
            status=format_qcloud_snapshot_status(object_json.SnapshotState),
            encrypt=object_json.Encrypt,
            create_time=handle_time_str(object_json.CreateTime),
            expired_time=handle_time_str(object_json.DeadlineTime),
            is_permanent=object_json.IsPermanent,
            zone=object_json.Placement.Zone,
            project=object_json.Placement.ProjectId,
            region=self.region_id,
        ).to_dict()

    def format_auto_snapshot_policy(self, object_json, **kwargs):
        time_points = repeat_week = []
        if object_json.Policy:
            time_points = object_json.Policy[0].Hour
            repeat_week = object_json.Policy[0].DayOfWeek
        return SnapshotPolicy(
            resource_id=object_json.AutoSnapshotPolicyId,
            resource_name=object_json.AutoSnapshotPolicyName,
            status="AVAILABLE" if object_json.AutoSnapshotPolicyState == "NORMAL" else "ERROR",
            retention_days=object_json.RetentionDays,
            disk_nums=len(object_json.DiskIdSet),
            create_time=object_json.CreateTime,
            zone=self.zone_id,
            cloud_type=self.cloud_type,
            region=self.region_id,
            time_points=time_points,
            repeat_week=repeat_week,
        ).to_dict()

    def format_image(self, object_json, **kwargs):
        return Image(
            resource_id=object_json.ImageId,
            resource_name=object_json.ImageName or "未命名",
            cloud_type=self.cloud_type,
            desc=object_json.ImageDescription,
            create_time=handle_time_str(object_json.CreatedTime),
            arch=object_json.Architecture,
            image_type=format_qcloud_image_type(object_json.ImageType),
            os_name_en=object_json.OsName,
            size=object_json.ImageSize,
            status=format_qcloud_image_status(object_json.ImageState),
            platform=object_json.Platform,
        ).to_dict()

    def format_vpc(self, object_json, **kwargs):
        return VPC(
            resource_id=object_json.VpcId,
            resource_name=object_json.VpcName or "未命名",
            cloud_type=self.cloud_type,
            status=get_qcloud_vpc_status(),
            cidr=object_json.CidrBlock,
            cidr_v6=object_json.Ipv6CidrBlock,
            is_default=object_json.IsDefault,
            create_time=handle_time_str(object_json.CreatedTime),
            dns=object_json.DnsServerSet,
            region=self.region_id,
            tag=format_qcloud_tag(object_json.TagSet),
            extra={
                "DnsServerSet": object_json.DnsServerSet,
                "DomainName": ",".join(object_json.DomainName),
                "Ipv6CidrBlock": object_json.Ipv6CidrBlock,
            },
        ).to_dict()

    def format_subnet(self, object_json, **kwargs):
        return Subnet(
            resource_id=object_json.SubnetId,
            resource_name=object_json.SubnetName or "未命名",
            vpc=object_json.VpcId,
            cloud_type=self.cloud_type,
            status=get_qcloud_subnet_status(),
            cidr=object_json.CidrBlock,
            cidr_v6=object_json.Ipv6CidrBlock,
            create_time=handle_time_str(object_json.CreatedTime),
            router_table_id=object_json.RouteTableId,
            is_default=object_json.IsDefault,
            tag=format_qcloud_tag(object_json.TagSet),
            region=self.region_id,
            zone=object_json.Zone,
            extra={
                "AvailableIpAddressCount": object_json.AvailableIpAddressCount,
                "Ipv6CidrBlock": object_json.Ipv6CidrBlock,
                "NetworkAclId": object_json.NetworkAclId,
                "IsRemoteVpcSnat": object_json.IsRemoteVpcSnat,
                "TotalIpAddressCount": object_json.TotalIpAddressCount,
            },
        ).to_dict()

    def format_eip(self, object_json, **kwargs):
        return Eip(
            resource_id=object_json.AddressId,
            resource_name=object_json.AddressName or "未命名",
            cloud_type=self.cloud_type,
            status=format_qcloud_eip_status(object_json.AddressStatus),
            ip_addr=object_json.AddressIp,
            instance_id=object_json.InstanceId or "",
            create_time=handle_time_str(object_json.CreatedTime),
            nic_id=object_json.NetworkInterfaceId or "",
            private_ip_addr=object_json.PrivateAddressIp or "",
            is_attached=bool(object_json.InstanceId),
            bandwidth=getattr(object_json, "Bandwidth", 0) or 0,
            charge_type=get_qcloud_eip_charge_type(),
            # 返回值包括 "CMCC","CTCC","CUCC","BGP"
            provider=getattr(object_json, "InternetServiceProvider", ""),
            region=self.region_id,
            extra={
                "IsArrears": object_json.IsArrears,
                "IsBlocked": object_json.IsBlocked,
                "IsEipDirectConnection": object_json.IsEipDirectConnection,
                "AddressType": object_json.AddressType,
                "CascadeRelease": object_json.CascadeRelease,
            },
        ).to_dict()

    def format_security_group(self, object_json, **kwargs):
        return SecurityGroup(
            resource_id=object_json.SecurityGroupId,
            resource_name=object_json.SecurityGroupName or "未命名",
            cloud_type=self.cloud_type,
            desc=object_json.SecurityGroupDesc,
            tag=format_qcloud_tag(object_json.TagSet),
            is_default=object_json.IsDefault,
            create_time=handle_time_str(object_json.CreatedTime),
            region=self.region_id,
        ).to_dict()

    def format_security_group_rule(self, object_json, **kwargs):
        resource_id = "{}-{}-{}-{}-{}-{}-{}-{}".format(
            kwargs["security_group_id"],
            object_json.CidrBlock,
            object_json.PolicyDescription,
            object_json.PolicyIndex,
            object_json.Port,
            object_json.Protocol,
            object_json.PolicyDescription,
            object_json.ModifyTime,
        )
        return SecurityGroupRule(
            resource_id=hashlib.md5(resource_id.encode()).hexdigest()[:20],
            resource_name=object_json.PolicyIndex,
            cloud_type=self.cloud_type,
            direction=format_qcloud_security_group_rule_direction(kwargs["direction"]),
            source_cidr=object_json.CidrBlock,
            modify_time=object_json.ModifyTime,
            protocol=object_json.Protocol,
            port_range=object_json.Port,
            security_group=object_json.SecurityGroupId or kwargs["security_group_id"],
            action=object_json.Action,
            desc=object_json.PolicyDescription,
            region=self.region_id,
        ).to_dict()

    def format_tag(self, object_json, **kwargs):
        return Tag(
            key=object_json.TagKey,
            value=object_json.TagValue,
            cloud_type=self.cloud_type,
        ).to_dict()

    def format_bucket(self, object_json, **kwargs):
        return Bucket(
            resource_id=object_json.get("Name", ""),
            resource_name=object_json.get("Name", "未命名"),
            cloud_type=self.cloud_type,
            bucket_type=format_bucket_type(kwargs["bucket_type"]),
            create_time=object_json.get("CreationDate"),
            extra={"size": kwargs["size"]},
            region=object_json.get("Location"),
        ).to_dict()

    def format_bucket_file(self, object_json, **kwargs):
        bucket = kwargs.pop("bucket")
        modify_time = ""
        if object_json.get("LastModified"):
            time_data = object_json.get("LastModified").replace("T", "").replace("Z", "")[:-4]
            modify_time = f"{time_data[:10]} {time_data[10:]}"
        return BucketFile(
            modify_time=modify_time if object_json.get("LastModified") else "",
            size=object_json.get("Size", "0"),
            parent=object_json.get("parent") or "/",
            bucket=bucket,
            resource_id="{}<>{}".format(bucket, object_json.get("Key")),
            resource_name=object_json.get("Key", "未命名"),
            cloud_type=self.cloud_type,
            file_type=object_json.get("type"),
            extra={"location": kwargs.get("location")},
        ).to_dict()

    def format_balance(self, object_json, **kwargs):
        return Balance(amount=float(object_json.Balance) / 100, currency="CNY", unit="元").to_dict()

    def format_transactions(self, object_json, **kwargs):
        return Transactions(
            amount=float(object_json.Amount / 100),
            transaction_time=object_json.OperationTime,
            currency="CNY",
            unit="元",
            extra={},
        ).to_dict()

    def format_load_balancer(self, object_json, **kwargs):
        return LoadBalancer(
            cloud_type=self.cloud_type,
            resource_id=object_json.LoadBalancerId,
            resource_name=object_json.LoadBalancerName,
            net_type=object_json.LoadBalancerType,
            lb_type=object_json.Forward,
            domain=object_json.Domain,
            vips=object_json.LoadBalancerVips,
            status=object_json.Status,
            create_time=object_json.CreateTime,
            status_time=object_json.StatusTime,
            project=object_json.ProjectId,
            vpc=object_json.VpcId,
            ip_version=object_json.AddressIPVersion,
            expire_time=object_json.ExpireTime,
            charge_type=object_json.ChargeType,
            ipv6_addr=object_json.AddressIPv6,
            region=self.region_id,
        ).to_dict()

    def format_listener(self, object_json, **kwargs):
        return LoadBalancerListener(
            front_version=object_json.Protocol.lower(),
            backend_version=object_json.Protocol.lower(),
            front_port=object_json.Port,
            load_balancer=kwargs.get("LoadBalancerId", ""),
            create_time=kwargs.get("CreateTime", ""),
            cloud_type=self.cloud_type,
            zone=self.zone_id,
            region=self.region_id,
            resource_id=object_json.ListenerId,
            resource_name=object_json.ListenerName,
        ).to_dict()

    def format_rule(self, object_json, **kwargs):
        return RelayRule(
            url=object_json.Url,
            domain=object_json.Domain,
            load_balancer=kwargs.get("LoadBalancerId", ""),
            create_time=object_json.CreateTime,
            cloud_type=self.cloud_type,
            region=self.region_id,
            zone=self.zone_id,
            resource_id=object_json.LocationId,
            protocal=object_json.ForwardType,
            extra={
                "Certificate": object_json.Certificate,
                "ListenerId": object_json.ListenerId,
                "DefaultServer": object_json.DefaultServer,
            },
        ).to_dict()

    def format_route_table(self, object_json, **kwargs):
        subnets = [item.SubnetId for item in object_json.AssociationSet]
        return RouteTable(
            vpc=object_json.VpcId,
            resource_id=object_json.RouteTableId,
            resource_name=object_json.RouteTableName or "未命名",
            create_time=object_json.CreatedTime,
            subnets=subnets,
            cloud_type=self.cloud_type,
            region=self.region_id,
            zone=self.zone_id,
            is_system=object_json.Main,
            status="AVAILABLE",
        ).to_dict()

    def format_route_entry(self, object_json, **kwargs):
        return RouteEntry(
            route_table=kwargs.get("RouteTableIds")[0],
            cidr_block=object_json.DestinationCidrBlock,
            next_hops={
                "NextHop": [
                    {
                        "NextHopId": "",
                        "NextHopType": object_json.GatewayType,
                        "GatewayId": object_json.GatewayId,
                        "NextHopRelatedInfo": {},
                    }
                ]
            },
            resource_id=object_json.RouteId,
            resource_name=getattr(object_json, "RouteTableName", "未命名"),
            create_time=getattr(object_json, "CreateTime", ""),
            desc=object_json.RouteDescription,
            cloud_type=self.cloud_type,
            region=self.region_id,
            zone=self.zone_id,
            status="PENDING" if object_json.Enabled else "AVAILABLE",
            extra={
                "Enabled": object_json.Enabled,
                "RouteType": object_json.RouteType,
                "PublishedToVbc": getattr(object_json, "PublishedToVbc", False),
            },
        ).to_dict()

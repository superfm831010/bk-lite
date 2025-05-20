# -*- coding: utf-8 -*-
"""阿里云资源数据格式转换类"""
import hashlib
import json
import threading

from common.cmp.cloud_apis.cloud_object.base import (
    VM,
    VPC,
    Balance,
    Bucket,
    BucketFile,
    Disk,
    Eip,
    FileSystem,
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
    ServerCertificate,
    Snapshot,
    SnapshotPolicy,
    Subnet,
    Tag,
    Transactions,
    VServerGroup,
    Zone,
)
from common.cmp.cloud_apis.resource_apis.resource_format.aliyun.aliyun_format_utils import (
    format_bucket_type,
    format_charge_type,
    format_disk_category,
    format_disk_charge_type,
    format_disk_status,
    format_disk_type,
    format_eip_status,
    format_image_status,
    format_image_type,
    format_instance_charge_type,
    format_instance_status,
    format_is_attached,
    format_listen_config,
    format_region_status,
    format_rule_direction,
    format_server_id,
    format_snapshot_status,
    format_subnet_status,
    format_tag,
    format_vpc_status,
)
from common.cmp.cloud_apis.resource_apis.utils import handle_time_stamp, handle_time_str, init_value


class AliyunResourceFormat:
    """格式化资源数据"""

    _instance_lock = threading.Lock()

    def __init__(self, account_id="", cloud_type="", region_id="", zone_id="", **kwargs):
        self.account_id = account_id
        self.cloud_type = cloud_type
        self.region_id = region_id
        self.zone_id = zone_id

    def __new__(cls, *args, **kwargs):
        """
        支持多线程的单例模式
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        """
        if not hasattr(AliyunResourceFormat, "_instance"):
            with AliyunResourceFormat._instance_lock:
                if not hasattr(AliyunResourceFormat, "_instance"):
                    AliyunResourceFormat._instance = object.__new__(cls)
        return AliyunResourceFormat._instance

    def format_region(self, object_json, **kwargs):
        # 状态值可能没有
        return Region(
            status=format_region_status(object_json.get("status", "available")),
            resource_id=object_json["RegionId"],
            resource_name=object_json["LocalName"] or object_json["RegionId"],
            cloud_type=self.cloud_type,
            extra={"RegionEndpoint": object_json.get("RegionEndpoint", "")},
        ).to_dict()

    def format_zone(self, object_json, **kwargs):
        # 可用区无状态值
        # region_id
        return Zone(
            region=self.region_id,
            status="",
            resource_id=object_json["ZoneId"],
            cloud_type=self.cloud_type,
            resource_name=object_json["LocalName"],
        ).to_dict()

    def format_instance_type_family(self, object_json, **kwargs):
        return InstanceTypeFamily(
            resource_id=object_json["InstanceTypeFamilyId"],
            resource_name="",
            cloud_type=self.cloud_type,
            desc=object_json["Generation"],
        ).to_dict()

    def format_instance_type(self, object_json, **kwargs):
        return InstanceType(
            cloud_type=self.cloud_type,
            vcpus=object_json["CpuCoreCount"],
            memory=object_json["MemorySize"] * 1024,
            disk=object_json.get("LocalStorageCapacity", 0),
            instance_family=object_json["InstanceTypeFamily"],
            resource_id=object_json["InstanceTypeId"],
            resource_name=object_json["InstanceTypeId"],
            region=self.region_id,
            zone=self.zone_id,
            extra={
                "InstanceTypeFamily": object_json.get("InstanceTypeFamily", ""),
                "EniQuantity": object_json.get("EniQuantity", ""),
                "InstanceFamilyLevel": object_json.get("InstanceFamilyLevel", ""),
                "GPUSpec": object_json.get("GPUSpec", ""),
                "GPUAmount": object_json.get("GPUAmount", ""),
            },
        ).to_dict()

    def format_vm(self, object_json, **kwargs):
        security_group_ids = object_json["SecurityGroupIds"].get("SecurityGroupId", [])
        eip_address = object_json["EipAddress"]["IpAddress"]
        if not eip_address:
            eip_address = []
        else:
            eip_address = [eip_address]
        public_ip = object_json["PublicIpAddress"].get("IpAddress", []) or eip_address

        interface_id = ""
        if object_json["NetworkInterfaces"]["NetworkInterface"]:
            interface_id = object_json["NetworkInterfaces"]["NetworkInterface"][0]["NetworkInterfaceId"]

        return VM(
            cloud_type=self.cloud_type,
            resource_id=object_json["InstanceId"],
            resource_name=object_json.get("InstanceName", "未命名"),
            status=format_instance_status(object_json.get("Status", "Running")),
            vcpus=object_json.get("Cpu", 0),
            memory=object_json.get("Memory", 0),
            instance_type=object_json.get("InstanceType", ""),
            image=object_json.get("ImageId", ""),
            os_name=object_json.get("OSName", ""),
            inner_ip=object_json["VpcAttributes"]["PrivateIpAddress"].get("IpAddress", []),
            public_ip=public_ip,
            charge_type=format_instance_charge_type(object_json["InstanceChargeType"]),
            internet_accessible=object_json.get("InternetChargeType"),
            vpc=object_json["VpcAttributes"].get("VpcId", ""),
            subnet=object_json["VpcAttributes"].get("VSwitchId", ""),
            security_group=security_group_ids,
            tag=format_tag(object_json.get("Tags", "")),
            zone=object_json.get("ZoneId", self.zone_id),
            region=object_json.get("RegionId", self.region_id),
            create_time=handle_time_str(object_json.get("CreationTime", "")),
            expired_time=handle_time_str(object_json.get("ExpiredTime", "")),
            extra={
                "HostName": object_json.get("HostName", ""),
                "ImageId": object_json.get("ImageId", ""),
                "InstanceNetworkType": object_json.get("InstanceNetworkType", ""),
                "InstanceType": object_json.get("InstanceType", ""),
                "InstanceTypeFamily": object_json.get("InstanceTypeFamily", ""),
                "InternetMaxBandwidthIn": object_json.get("InternetMaxBandwidthIn", ""),
                "InternetMaxBandwidthOut": object_json.get("InternetMaxBandwidthOut", ""),
                "SerialNumber": object_json.get("SerialNumber", ""),
                "EipAddress": object_json["EipAddress"].get("IpAddress", ""),
                "NetworkInterfaceId": interface_id,
            },
        ).to_dict()

    def format_disk(self, object_json, **kwargs):
        return Disk(
            cloud_type=self.cloud_type,
            resource_id=object_json.get("DiskId", ""),
            resource_name=object_json.get("DiskName", "未命名"),
            desc=object_json.get("Description", ""),
            tag=format_tag(object_json.get("Tags", "")),
            disk_type=format_disk_type(object_json.get("Type", "")),
            disk_size=object_json.get("Size", ""),
            charge_type=format_disk_charge_type(object_json.get("DiskChargeType", "")),
            portable=object_json.get("Portable", True),
            status=format_disk_status(object_json.get("Status", "")),
            category=format_disk_category(object_json.get("Category", "")),
            is_attached=format_is_attached(object_json.get("Status", "")),
            server_id=format_server_id(object_json.get("Status", ""), object_json.get("InstanceId", "")),
            create_time=handle_time_str(object_json.get("CreationTime", "")),
            expired_time=handle_time_str(object_json.get("ExpiredTime", "")),
            encrypt=object_json.get("Encrypted", True),
            delete_with_instance=object_json.get("DeleteWithInstance", True),
            serial_number=object_json.get("SerialNumber", ""),
            storage=object_json.get("StorageSetId", ""),
            zone=object_json.get("ZoneId", self.zone_id),
            region=object_json.get("RegionId", self.region_id),
            snapshot_policy=object_json.get("AutoSnapshotPolicyId", ""),
            extra={
                "DeleteAutoSnapshot": object_json.get("DeleteAutoSnapshot", ""),
                "PerformanceLevel": object_json.get("PerformanceLevel", ""),
                "ResourceGroupId": object_json.get("ResourceGroupId", ""),
            },
        ).to_dict()

    def format_snapshot(self, object_json, **kwargs):
        return Snapshot(
            cloud_type=self.cloud_type,
            resource_id=object_json.get("SnapshotId", ""),
            resource_name=object_json.get("SnapshotName", "未命名"),
            desc=object_json.get("Description", ""),
            tag=format_tag(object_json.get("Tags", "")),
            disk_id=object_json.get("SourceDiskId", ""),
            disk_size=object_json.get("SourceDiskSize", 0),
            status=format_snapshot_status(object_json.get("Status", "")),
            disk_type=format_disk_type(object_json.get("SourceDiskType", "")),
            create_time=handle_time_str(object_json.get("CreationTime", "")),
            # todo 阿里云有自动快照保留天数 手动如何计算
            # expired_time=handle_time_str(object_json.get("CreationTime", "")),
            region=self.region_id,
            zone=self.zone_id,
            encrypt=object_json.get("Encrypted", False),
            extra={"Progress": object_json.get("Progress", ""), "Usage": "none"},
        ).to_dict()

    def format_auto_snapshot_policy(self, object_json, **kwargs):
        return SnapshotPolicy(
            time_points=object_json.get("TimePoints"),
            status="AVAILABLE" if object_json.get("Status") == "Normal" else "ERROR",
            retention_days=object_json.get("RetentionDays"),
            repeat_week=json.loads(object_json.get("RepeatWeekdays")),
            disk_nums=object_json.get("DiskNums"),
            create_time=object_json.get("CreationTime"),
            zone=self.zone_id,
            cloud_type=self.cloud_type,
            region=object_json.get("RegionId") or self.region_id,
            resource_id=object_json.get("AutoSnapshotPolicyId", ""),
            resource_name=object_json.get("AutoSnapshotPolicyName", "未命名"),
            desc=object_json.get("Description", ""),
            tag=format_tag(object_json.get("Tags", "")),
        ).to_dict()

    def format_image(self, object_json, **kwargs):
        return Image(
            cloud_type=self.cloud_type,
            resource_id=object_json.get("ImageId", ""),
            resource_name=object_json.get("ImageName", "未命名"),
            desc=object_json.get("Description", ""),
            tag=format_tag(object_json.get("Tags")),
            size=object_json.get("Size", ""),
            status=format_image_status(object_json.get("Status", "")),
            create_time=handle_time_str(object_json.get("CreationTime", "")),
            platform=object_json.get("Platform", ""),
            image_type=format_image_type(object_json.get("ImageOwnerAlias", "")),
            arch=object_json.get("Architecture", ""),
            image_family=object_json.get("ImageFamily", ""),
            image_version=object_json.get("ImageVersion", ""),
            os_type=object_json.get("OSType", ""),
            os_name=object_json.get("OSName", ""),
            os_name_en=object_json.get("OSNameEn", ""),
            extra={
                "ImageOwnerAlias": object_json.get("ImageOwnerAlias", ""),
                "IsCopied": object_json.get("IsCopied", ""),
                "Progress": object_json.get("Progress", ""),
                "Usage": object_json.get("Status", ""),
            },
        ).to_dict()

    def format_vpc(self, object_json, **kwargs):
        router_tables = (
            object_json.get("RouterTableIds").get("RouterTableIds", [])
            if isinstance(object_json.get("RouterTableIds"), dict)
            else []
        )
        return VPC(
            cloud_type=self.cloud_type,
            resource_id=object_json.get("VpcId", ""),
            resource_name=object_json.get("VpcName", "未命名"),
            status=format_vpc_status(object_json.get("Status", "")),
            router=object_json.get("VRouterId", ""),
            router_tables=router_tables,
            resource_group=object_json.get("ResourceGroupId", ""),
            is_default=object_json.get("IsDefault", ""),
            create_time=handle_time_str(object_json.get("CreationTime", "")),
            cidr=object_json.get("CidrBlock", ""),
            cidr_v6=object_json.get("Ipv6CidrBlock", ""),
            region=object_json.get("RegionId", self.region_id),
            zone=self.zone_id,
            desc=object_json.get("Description", ""),
            tag=format_tag(object_json.get("Tags", "")),
            extra={
                "UserCidrs": ",".join(object_json.get("UserCidrs", [])),
                "SecondaryCidrBlocks": ",".join(object_json.get("SecondaryCidrBlocks", [])),
                "NatGatewayIds": ",".join(object_json.get("NatGatewayIds", [])),
                "Ipv6CidrBlock": object_json.get("Ipv6CidrBlock", ""),
                "VRouterId": object_json.get("VRouterId", ""),
            },
        ).to_dict()

    def format_subnet(self, object_json, **kwargs):
        return Subnet(
            cloud_type=self.cloud_type,
            resource_id=object_json.get("VSwitchId", ""),
            resource_name=object_json.get("VSwitchName", "未命名"),
            vpc=object_json.get("VpcId", ""),
            status=format_subnet_status(object_json.get("Status", "")),
            cidr=object_json.get("CidrBlock", ""),
            cidr_v6=object_json.get("Ipv6CidrBlock", ""),
            create_time=handle_time_str(object_json.get("CreationTime", "")),
            router_table_id=object_json["RouteTable"].get("RouteTableId", ""),
            is_default=object_json.get("IsDefault", False),
            resource_group=object_json.get("ResourceGroupId", ""),
            tag=format_tag(object_json.get("Tags", "")),
            desc=object_json.get("Description", ""),
            region=self.region_id,
            zone=object_json.get("ZoneId", self.zone_id),
            extra={
                "AvailableIpAddressCount": object_json.get("AvailableIpAddressCount", ""),
                "Ipv6CidrBlock": object_json.get("Ipv6CidrBlock", ""),
                "ResourceGroupId": object_json.get("ResourceGroupId", ""),
                "IsDefault": object_json.get("IsDefault", ""),
            },
        ).to_dict()

    def format_eip(self, object_json, **kwargs):
        return Eip(
            cloud_type=self.cloud_type,
            resource_id=object_json.get("AllocationId", ""),
            resource_name=object_json.get("Name", "未命名"),
            status=format_eip_status(object_json.get("Status", "")),
            ip_addr=object_json.get("IpAddress", ""),
            instance_id=object_json.get("InstanceId", ""),
            create_time=handle_time_str(object_json.get("AllocationTime", "")),
            # private_ip_addr=object_json.get(),
            is_attached=True if object_json.get("InstanceId") else False,
            bandwidth=object_json.get("Bandwidth", ""),
            desc=object_json.get("Descritpion", ""),
            resource_group=object_json.get("ResourceGroupId", ""),
            charge_type=format_charge_type(object_json.get("ChargeType", "")),
            expired_time=handle_time_str(object_json.get("ExpiredTime", "")),
            zone=self.zone_id,
            region=object_json.get("RegionId", self.region_id),
            extra={
                "BandwidthPackageBandwidth": object_json.get("BandwidthPackageBandwidth", ""),
                "BandwidthPackageId": object_json.get("BandwidthPackageId", ""),
                "ResourceGroupId": object_json.get("ResourceGroupId", ""),
                "ExpiredTime": object_json.get("ExpiredTime", ""),
                "EipBandInstanceId": object_json.get("InstanceId", ""),
                "InstanceRegionId": object_json.get("InstanceRegionId", ""),
                "EipBandInstanceType": object_json.get("InstanceType", ""),
            },
        ).to_dict()

    def format_security_group_rule(self, object_json, **kwargs):
        resource_id = "{}-{}-{}-{}-{}-{}-{}".format(
            kwargs["SecurityGroupId"],
            object_json["Direction"],
            object_json["Priority"],
            object_json["IpProtocol"],
            object_json["PortRange"],
            object_json["SourceCidrIp"],
            object_json["DestCidrIp"],
        )
        return SecurityGroupRule(
            cloud_type=self.cloud_type,
            resource_id=hashlib.md5(resource_id.encode()).hexdigest()[:20],
            resource_name=object_json.get("DestGroupName", "未命名"),
            direction=format_rule_direction(object_json.get("Direction", "ERROR").lower()),
            protocol=object_json.get("IpProtocol", ""),
            action=object_json.get("Policy", "Accept"),
            security_group=kwargs.get("SecurityGroupId", ""),
            dest_cidr=object_json.get("DestCidrIp", ""),
            dest_group_id=kwargs.get("DestGroupId", ""),
            source_cidr=object_json.get("SourceCidrIp", ""),
            source_group_id=kwargs.get("SourceGroupId", ""),
            create_time=handle_time_str(object_json.get("CreateTime", "")),
            priority=object_json.get("Priority", ""),
            desc=object_json.get("Description", ""),
            nic_type=object_json.get("NicType", ""),
            port_range=object_json.get("PortRange", ""),
            tag=format_tag(object_json.get("Tags", "")),
            region=object_json.get("RegionId", self.region_id),
            zone=object_json.get("ZoneId", self.zone_id),
            extra={
                "NicType": object_json.get("NicType", ""),
                "Policy": object_json.get("Policy", ""),
            },
        ).to_dict()

    def format_security_group(self, object_json, **kwargs):
        return SecurityGroup(
            cloud_type=self.cloud_type,
            resource_id=object_json.get("SecurityGroupId", ""),
            resource_name=object_json.get("SecurityGroupName", "未命名"),
            desc=object_json.get("Description", ""),
            tag=format_tag(object_json.get("Tags", "")),
            vpc=object_json.get("VpcId", ""),
            resource_group=object_json.get("ResourceGroupId", ""),
            region=object_json.get("RegionId", self.region_id),
            zone=self.zone_id,
            create_time=handle_time_str(object_json.get("CreationTime", "")),
            extra={
                "ResourceGroupId": object_json.get("ResourceGroupId", ""),
                "SecurityGroupType": object_json.get("SecurityGroupType", ""),
            },
        ).to_dict()

    def format_bucket(self, object_json, **kwargs):
        return Bucket(
            cloud_type=self.cloud_type,
            resource_id=object_json.name,
            resource_name=object_json.name,
            bucket_type=format_bucket_type(kwargs.get("bucket_type", "")),
            extra={"size": kwargs.get("size", 0)},
            region=object_json.location.split("-", 1)[-1],
        ).to_dict()

    def format_bucket_file(self, file_object, **kwargs):
        bucket = kwargs.pop("bucket")
        return BucketFile(
            modify_time=handle_time_stamp(file_object.last_modified)
            if isinstance(file_object.last_modified, int)
            else "",
            size=file_object.size,
            file_type=file_object.type,
            parent=file_object.parent or "/",
            bucket=bucket,
            resource_id="{}<>{}".format(bucket, file_object.key),
            cloud_type=self.cloud_type,
            extra={"location": kwargs.get("location", "")},
        ).to_dict()

    def format_load_balancer(self, object_json, **kwargs):
        return LoadBalancer(
            cloud_type=self.cloud_type,
            resource_id=object_json.get("LoadBalancerId", "未命名"),
            resource_name=object_json.get("LoadBalancerName", "未命名"),
            net_type=object_json.get("AddressType"),
            lb_type=object_json.get("NetworkType") == "vpc",
            region=object_json.get("RegionIdAlias"),
            status=object_json.get("LoadBalancerStatus") == "active",
            vpc=object_json.get("VpcId"),
            ip_version=object_json.get("AddressIPVersion"),
            charge_type=object_json.get("PayType"),
            tag=format_tag(object_json.get("Tags", "")),
            desc=object_json.get("Description", ""),
        ).to_dict()

    def format_listener(self, object_json, **kwargs):
        return LoadBalancerListener(
            front_version=object_json.get("ListenerProtocol"),
            front_port=object_json.get("ListenerPort"),
            backend_version=object_json.get("ListenerProtocol"),
            backend_port=object_json.get("BackendServerPort", ""),
            status="RUNNING" if object_json.get("Status") == "running" else "STOPPING",
            listen_config=format_listen_config(object_json),
            server_group=object_json.get("VServerGroupId", ""),
            create_time="",
            load_balancer=object_json.get("LoadBalancerId", ""),
            cloud_type=self.cloud_type,
            zone=self.zone_id,
            region=object_json.get("RegionId", self.region_id),
            resource_id="{}-{}-{}".format(
                object_json.get("LoadBalancerId"), object_json.get("ListenerProtocol"), object_json.get("ListenerPort")
            ),
            resource_name=object_json.get("Description", "未命名"),
            desc=object_json.get("Description", ""),
            tag=format_tag(object_json.get("Tags", "")),
        ).to_dict()

    def format_route_table(self, object_json, **kwargs):
        subnets = (
            object_json.get("VSwitchIds").get("VSwitchId", [])
            if isinstance(object_json.get("VSwitchIds"), dict)
            else []
        )
        return RouteTable(
            status="AVAILABLE" if object_json.get("Status") == "Available" else "ERROR",
            vpc=object_json.get("VpcId"),
            vrouter=object_json.get("RouterId"),
            subnets=subnets,
            is_system=object_json.get("RouteTableType") == "System",
            create_time=handle_time_str(object_json.get("CreationTime", "")),
            cloud_type=self.cloud_type,
            zone=self.zone_id,
            region=object_json.get("RegionId", self.region_id),
            resource_id=object_json.get("RouteTableId", ""),
            resource_name=object_json.get("RouteTableName", "未命名"),
            desc=object_json.get("Description", ""),
            tag=format_tag(object_json.get("Tags", "")),
        ).to_dict()

    def format_route_entry(self, object_json, **kwargs):
        resource_id = "{}-{}".format(object_json.get("DestinationCidrBlock"), object_json.get("RouteTableId"))
        return RouteEntry(
            status=object_json.get("Status"),
            route_table=object_json.get("RouteTableId"),
            cidr_block=object_json.get("DestinationCidrBlock"),
            next_hops=object_json.get("NextHops", {}),
            is_system=object_json.get("Type") == "System",
            create_time="",
            cloud_type=self.cloud_type,
            zone=self.zone_id,
            region=object_json.get("RegionId", self.region_id),
            resource_id=object_json.get("RouteEntryId") if object_json.get("RouteEntryId") else resource_id,
            resource_name=object_json.get("RouteEntryName", "未命名"),
            desc=object_json.get("Description", ""),
            tag=format_tag(object_json.get("Tags", "")),
        ).to_dict()

    def format_vserver_groups(self, object_json, **kwargs):
        return VServerGroup(
            backend_servers=[],
            load_balancer="",
            listens=object_json["AssociatedObjects"]["Listeners"]["Listener"],
            rules=object_json["AssociatedObjects"]["Rules"]["Rule"],
            create_time="",
            cloud_type=self.cloud_type,
            region=object_json.get("RegionId", self.region_id),
            zone=self.zone_id,
            resource_id=object_json.get("VServerGroupId", ""),
            resource_name=object_json.get("VServerGroupName", "未命名"),
            desc=object_json.get("Description", ""),
            tag=format_tag(object_json.get("Tags", "")),
        ).to_dict()

    def format_server_certificate(self, object_json, **kwargs):
        return ServerCertificate(
            finger_print=object_json.get("Fingerprint", ""),
            upload_time=handle_time_stamp(object_json.get("CreateTimeStamp"))
            if object_json.get("CreateTimeStamp")
            else "",
            expired_time=handle_time_stamp(object_json.get("ExpireTimeStamp"))
            if object_json.get("ExpireTimeStamp")
            else "",
            create_time=handle_time_stamp(object_json.get("CreateTimeStamp"))
            if object_json.get("CreateTimeStamp")
            else "",
            region=object_json.get("RegionId", self.region_id),
            cloud_type=self.cloud_type,
            zone=self.zone_id,
            resource_id=object_json.get("ServerCertificateId", ""),
            resource_name=object_json.get("AliCloudCertificateName", "未命名"),
            desc=object_json.get("Description", ""),
            tag=format_tag(object_json.get("Tags", "")),
        ).to_dict()

    def format_file_system(self, object_json, **kwargs):
        return FileSystem(
            vpc="",
            protocol=object_json.get("ProtocolType"),
            status="AVAILABLE" if object_json.get("Status") == "Running" else "PENDING",
            used_capacity=object_json.get("MeteredSize") / 1024 / 1024
            if isinstance(object_json.get("MeteredSize"), int)
            else 0,
            max_size=object_json.get("Capacity") * 1024 if isinstance(object_json.get("Capacity"), int) else 0,
            storage_type=object_json.get("StorageType", ""),
            pgroup={},
            create_time=handle_time_str(object_json.get("CreateTime", "")),
            encrypt=object_json.get("EncryptType") != 0,
            cloud_type=self.cloud_type,
            zone=object_json.get("ZoneId", self.zone_id),
            ip_addr="",
            key=object_json.get("KMSKeyId", ""),
            # region=object_json.get("RegionId", self.region_id),
            resource_id=object_json.get("FileSystemId", ""),
            resource_name=object_json.get("Description") or object_json.get("FileSystemId", ""),
            desc=object_json.get("Description", ""),
            tag=format_tag(object_json.get("Tags", "")),
            mount_info=object_json["MountTargets"]["MountTarget"]
            if isinstance(object_json.get("MountTargets"), dict)
            else [],
        ).to_dict()

    def format_rule(self, object_json, **kwargs):
        return RelayRule(
            url=object_json.get("Url", ""),
            domain=object_json.get("Domain", ""),
            server_group=object_json.get("VServerGroupId"),
            load_balancer=kwargs.get("LoadBalancerId", ""),
            create_time="",
            cloud_type=self.cloud_type,
            region=object_json.get("RegionId", self.region_id),
            zone=object_json.get("ZoneId", self.zone_id),
            resource_id=object_json.get("RuleId", ""),
            resource_name=object_json.get("RuleName", "未命名"),
            desc=object_json.get("Description", ""),
            tag=format_tag(object_json.get("Tags", "")),
            port=kwargs.get("ListenerPort"),
            protocal=kwargs.get("ListenerProtocol", ""),
        ).to_dict()

    @staticmethod
    def format_balance(object_json, **kwargs):
        return Balance(
            amount=float(init_value(["Data", "AvailableAmount"], object_json).replace(",", "")),
            currency=init_value(["Data", "Currency"], object_json),
            unit="元",
            extra={
                "AvailableCashAmount": init_value(["Data", "AvailableCashAmount"], object_json),
                "CreditAmount": init_value(["Data", "CreditAmount"], object_json),
                "MybankCreditAmount": init_value(["Data", "MybankCreditAmount"], object_json),
            },
        ).to_dict()

    @staticmethod
    def format_transactions(object_json, **kwargs):
        return Transactions(
            amount=float(object_json["Amount"]),
            transaction_time=object_json.get("TransactionTime", ""),
            currency="CNY",
            unit="元",
            extra={
                "Balance": object_json.get("Balance", ""),
                "BillingCycle": object_json.get("BillingCycle", ""),
                "FundType": object_json.get("FundType", ""),
                "RecordID": object_json.get("RecordID", ""),
                "Remarks": object_json.get("Remarks", ""),
                "TransactionAccount": object_json.get("TransactionAccount", ""),
                "TransactionChannel": object_json.get("TransactionChannel", ""),
                "TransactionChannelSN": object_json.get("TransactionChannelSN", ""),
                "TransactionFlow": object_json.get("TransactionFlow", ""),
                "TransactionNumber": object_json.get("TransactionNumber", ""),
                "TransactionType": object_json.get("TransactionType", ""),
                "AccountName": kwargs.get("AccountName", ""),
            },
        ).to_dict()

    @staticmethod
    def format_tag(object_json, **kwargs):
        """
        转换标签
        Args:
            object_json ():
            **kwargs ():

        Returns:

        """
        return Tag(
            key=object_json["TagKey"],
            value=object_json["TagValue"],
            tag_type=object_json["ResourceType"],
        )

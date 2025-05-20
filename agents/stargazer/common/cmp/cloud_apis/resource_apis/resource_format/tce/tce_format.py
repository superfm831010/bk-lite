# -*- coding: utf-8 -*-
"""tce格式化"""
import json
import threading

from common.cmp.cloud_apis.cloud_object.base import (
    BMS,
    TDSQL,
    TKE,
    VM,
    VPC,
    Bucket,
    CKafka,
    FileSystem,
    InstanceType,
    InstanceTypeFamily,
    LoadBalancer,
    Mariadb,
    MongoDB,
    PrivateBucket,
    Redis,
    Region,
    SecurityGroup,
    SecurityGroupRule,
    TKEInstance,
    Zone,
    ZoneInstanceConfig,
)
from common.cmp.cloud_apis.resource_apis.resource_format.qcloud.qcloud_format import QCloudResourceFormat
from common.cmp.cloud_apis.resource_apis.resource_format.qcloud.qcloud_format_utils import (
    format_qcloud_restrict_state,
    format_qcloud_tag,
    format_qcloud_vm_status,
)
from common.cmp.cloud_apis.resource_apis.resource_format.tce.tce_format_utils import (
    format_ckafka_tags,
    format_tce_k8s_tag,
    format_tce_shared_detail,
    format_tce_vm_charge_type,
)
from common.cmp.cloud_apis.resource_apis.utils import handle_time_str


class TCEResourceFormat(QCloudResourceFormat):
    """
    Data normalization
    """

    zone_cache = None

    _instance_lock = threading.Lock()

    def __init__(self, account_id="", cloud_type="", region_id="", zone_id="", **kwargs):
        self.account_id = account_id
        self.cloud_type = cloud_type
        self.region_id = region_id
        self.zone_id = zone_id
        self.extra_params = kwargs

    def __new__(cls, *args, **kwargs):
        """
        支持多线程的单例模式
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        """
        if not hasattr(TCEResourceFormat, "_instance"):
            with TCEResourceFormat._instance_lock:
                if not hasattr(TCEResourceFormat, "_instance"):
                    TCEResourceFormat._instance = object.__new__(cls)
        return TCEResourceFormat._instance

    def format_region(self, object_json, **kwargs):
        return Region(
            resource_id=object_json.Region,
            resource_name=object_json.RegionName,
            cloud_type=self.cloud_type,
            status=object_json.RegionState,
        ).to_dict()

    def format_zone(self, object_json, **kwargs):
        return Zone(
            resource_id=object_json.Zone,
            resource_name=object_json.ZoneName,
            cloud_type=self.cloud_type,
            status=object_json.ZoneState,
            tce_zone_id=object_json.ZoneId,
            region=kwargs.get("region_id", ""),
        ).to_dict()

    def format_instance_type_family(self, object_json, **kwargs):
        return InstanceTypeFamily(
            resource_id=object_json.InstanceFamily,
            resource_name=object_json.InstanceFamilyName or "未命名",
            cloud_type=self.cloud_type,
        ).to_dict()

    def format_instance_type(self, object_json, **kwargs):
        return InstanceType(
            resource_id=object_json.InstanceType,
            resource_name=object_json.InstanceType,
            cloud_type=self.cloud_type,
            vcpus=object_json.CPU,
            memory=object_json.Memory * 1024,
            zone=object_json.Zone,
            instance_family=object_json.InstanceFamily,
            project="",
            region=kwargs.get("region_id", ""),
        ).to_dict()

    def format_vm(self, object_json, **kwargs):
        system_disk = (
            {
                "id": object_json.SystemDisk.DiskId,
                "disk_size": object_json.SystemDisk.DiskSize,
                "disk_type": object_json.SystemDisk.DiskType,
                "storage_pool_group": object_json.SystemDisk.DiskStoragePoolGroup,
            }
            if object_json.SystemDisk
            else {}
        )
        data_disk = (
            [
                {
                    "disk_size": i.DiskSize,
                    "disk_type": i.DiskType,
                    "id": i.DiskId,
                    "delete_with_instance": i.DeleteWithInstance,
                    "storage_pool_group": i.DiskStoragePoolGroup,
                }
                for i in object_json.DataDisks
                if i
            ]
            if object_json.DataDisks
            else []
        )
        internet_accessiable = (
            {
                "internet_charge_type": object_json.InternetAccessible.InternetChargeType,
                "internet_max_bandwidth_out": object_json.InternetAccessible.InternetMaxBandwidthOut,
                "publicIp_assigned": object_json.InternetAccessible.PublicIpAssigned,
            }
            if object_json.InternetAccessible
            else {}
        )
        login_settings = (
            {
                "password": object_json.LoginSettings.Password,
                "key_ids": object_json.LoginSettings.KeyIds,
                "keep_image_login": object_json.LoginSettings.KeepImageLogin,
            }
            if object_json.LoginSettings
            else {}
        )
        return VM(
            resource_id=object_json.InstanceId,
            resource_name=object_json.InstanceName,
            cloud_type=self.cloud_type,
            instance_type=object_json.InstanceType,
            vcpus=object_json.CPU,
            memory=int(object_json.Memory) * 1024,
            image=object_json.ImageId,
            # tce和qcloud主机状态等数一致
            restrict_state=format_qcloud_restrict_state(object_json.RestrictState),
            status=format_qcloud_vm_status(object_json.InstanceState),
            inner_ip=object_json.PrivateIpAddresses or [],
            public_ip=object_json.PublicIpAddresses or [],
            system_disk=system_disk,
            data_disk=data_disk,
            charge_type=format_tce_vm_charge_type(object_json.InstanceChargeType),
            internet_accessible=internet_accessiable,
            vpc=object_json.VirtualPrivateCloud.VpcId,
            subnet=object_json.VirtualPrivateCloud.SubnetId,
            security_group=object_json.SecurityGroupIds if object_json.SecurityGroupIds else [],
            zone=object_json.Placement.Zone,
            project=object_json.Placement.ProjectId,
            region=self.region_id,
            login_settings=login_settings,
            create_time=handle_time_str(object_json.CreatedTime),
            expired_time=handle_time_str(object_json.ExpiredTime),
            # tag=format_qcloud_tag(object_json.Tags),
            os_name=object_json.OsName,
        ).to_dict()

    def format_vpc(self, object_json, **kwargs):
        return VPC(
            resource_id=object_json.VpcId,
            resource_name=object_json.VpcName or "未命名",
            cloud_type=self.cloud_type,
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
            # project=object_json.ProjectId,
            create_time=handle_time_str(object_json.CreatedTime),
            region=self.region_id,
        ).to_dict()

    def format_security_group_rule(self, object_json, **kwargs):
        direction = kwargs.get("direction")
        version = kwargs.get("version")
        # access_ipaddr = object_json.CidrBlock if object_json.CidrBlock else "::/0"
        resource_id = kwargs["security_group_id"] + direction + str(object_json.PolicyIndex)
        return SecurityGroupRule(
            resource_id=resource_id,
            resource_name=object_json.PolicyIndex,
            cloud_type=self.cloud_type,
            direction=direction,
            source_cidr=object_json.CidrBlock,
            modify_time=object_json.ModifyTime,
            protocol=object_json.Protocol,
            port_range=object_json.Port,
            # security_group=object_json.SecurityGroupId,
            security_group=kwargs.get("security_group_id", ""),
            action=object_json.Action,
            desc=object_json.PolicyDescription,
            region=self.region_id,
            extra={"version": version},
        ).to_dict()

    def format_file_system(self, object_json, **kwargs):
        pgroup = (
            {"pgroup_id": object_json.PGroup.PGroupId, "name": object_json.PGroup.Name} if object_json.PGroup else {}
        )
        return FileSystem(
            resource_id=object_json.FileSystemId,
            resource_name=object_json.FsName,
            cloud_type=self.cloud_type,
            vpc=object_json.VpcId,
            protocol=object_json.Protocol,
            status="AVAILABLE" if object_json.LifeCycleState == "available" else "PENDING",
            used_capacity=object_json.SizeByte,
            max_size=object_json.SizeLimit,
            capacity_limit=object_json.SizeLimitMax,
            zone=object_json.Zone,
            create_time=object_json.CreationTime,
            pgroup=pgroup,
            storage_type=object_json.StorageType,
            ip_addr=object_json.IpAddress,
            allocated_capacity=object_json.AllocedSpace,
            encrypt=object_json.Encrypted,
            key=object_json.KmsKeyId,
        ).to_dict()

    def format_private_bucket(self, object_json, **kwargs):
        return PrivateBucket(
            resource_id=object_json["Name"],
            resource_name=object_json["Name"],
            cloud_type=self.cloud_type,
            region=self.region_id,
        ).to_dict()

    def format_bucket(self, object_json, **kwargs):
        return Bucket(
            cloud_type=self.cloud_type,
            resource_id=object_json.get("Name"),
            resource_name=object_json.get("Name"),
            bucket_type="STANDARD",
            extra={"size": kwargs.get("size", 0)},
            region=self.region_id,
        ).to_dict()

    def format_dcdb(self, object_json, **kwargs):
        return TDSQL(
            resource_id=object_json.InstanceId,
            resource_name=object_json.InstanceName,
            cloud_type=self.cloud_type,
            region=object_json.Region,
            zone=object_json.Zone,
            # project=object_json.ProjectId,
            vpc=object_json.UniqueVpcId,
            subnet=object_json.UniqueSubnetId,
            inner_ip=object_json.Vip,
            status=object_json.Status,
            inner_port=object_json.Vport,
            create_time=object_json.CreateTime,
            auto_renew_flag=object_json.AutoRenewFlag,
            memory=object_json.Memory,
            storage=object_json.Storage,
            shard_count=object_json.ShardCount,
            period_end_time=object_json.PeriodEndTime,
            isolated_time_stamp=object_json.IsolatedTimestamp,
            shard_detail=format_tce_shared_detail(object_json.ShardDetail),
            node_count=object_json.NodeCount,
            excluster_id=object_json.ExclusterId,
            wan_domain=object_json.WanDomain,
            wan_ip=object_json.WanVip,
            update_time=object_json.UpdateTime,
            engine=object_json.DbEngine,
            version=object_json.DbVersion,
            pay_mode=object_json.Paymode,
            wan_status=object_json.WanStatus,
            extra={
                "vpc_id": object_json.VpcId,
                "subnet_id": object_json.SubnetId,
            },
        ).to_dict()

    def format_dcdb_shard(self, data, **kwargs):
        # Status: 状态：0 创建中，1 流程处理中， 2 运行中，3 分片未初始化
        return {
            "status": data.Status,
            "status_cn": data.StatusDesc,
            "storage_usage": data.StorageUsage,
            "vpc_id": data.VpcId,
            "shard_ins_id": data.ShardInstanceId,
            "shard_serial_id": data.ShardSerialId,
            "ins_id": data.InstanceId,
            "project_id": data.ProjectId,
            "region_id": data.Region,
            "storage": data.Storage,
            "mem_usage": data.MemoryUsage,
            "zone_id": data.Zone,
            "period_end_time": data.PeriodEndTime,
            "mem": data.Memory,
            "node_count": data.NodeCount,
            "subnet_id": data.SubnetId,
            "proxy_version": data.ProxyVersion,
            "create_time": data.CreateTime,
        }

    def format_mariadb(self, object_json, **kwargs):
        return Mariadb(
            resource_id=object_json.InstanceId,
            resource_name=object_json.InstanceName,
            cloud_type=self.cloud_type,
            region=object_json.Region,
            zone=object_json.Zone,
            charge_type=object_json.Paymode,
            create_time=object_json.CreateTime,
            machine=object_json.Machine,
            memory=object_json.Memory,
            node_count=object_json.NodeCount,
            qps=object_json.Qps,
            status=object_json.Status,
            inner_ip=object_json.Vip,
            storage=object_json.Storage,
            vpc=object_json.UniqueVpcId,
            subnet=object_json.UniqueSubnetId,
            update_time=object_json.UpdateTime,
            inner_port=object_json.Vport,
            wan_domain=object_json.WanDomain,
            wan_status=object_json.WanStatus,
            wan_ip=object_json.WanVip,
        ).to_dict()

    def format_redis(self, object_json, **kwargs):
        return Redis(
            resource_id=object_json.InstanceId,
            resource_name=object_json.InstanceName,
            cloud_type=self.cloud_type,
            # project=object_json.ProjectId,
            region=object_json.RegionId,
            zone=object_json.ZoneId,
            vpc=object_json.UniqVpcId,
            subnet=object_json.UniqSubnetId,
            status=object_json.Status,
            vip=object_json.WanIp,
            port=object_json.Port,
            create_time=object_json.Createtime,
            size=object_json.Size,
            used_size=object_json.SizeUsed,
            instance_type=object_json.Type,
            billing_mode=object_json.BillingMode,
            auto_renew_flag=object_json.AutoRenewFlag,
            offline_time=object_json.OfflineTime,
            engine=object_json.Engine,
            product_type=object_json.ProductType,
            instance_node=object_json.InstanceNode,
            shard_size=object_json.RedisShardSize,
            shard_num=object_json.RedisShardNum,
            replicas_num=object_json.RedisReplicasNum,
            close_time=object_json.CloseTime,
            slave_read_weight=object_json.SlaveReadWeight,
            project_name=object_json.ProjectName,
            tag=format_qcloud_tag(object_json.InstanceTags),
        ).to_dict()

    def format_mongodb(self, object_json, **kwargs):
        charge_type = ""
        if object_json.PayMode == 0:
            charge_type = "按量计费"
        elif object_json.PayMode == 1:
            charge_type = "包年包月，"
        elif object_json.PayMode == -1:
            charge_type = "按量计费+包年包月"
        return MongoDB(
            resource_id=object_json.InstanceId,
            resource_name=object_json.InstanceName,
            cloud_type=self.cloud_type,
            region=object_json.Region,
            zone=object_json.Zone,
            vpc=object_json.VpcId,
            subnet=object_json.SubnetId,
            status=object_json.Status,
            inner_port=object_json.Vport,
            create_time=object_json.CreateTime,
            memory=int(object_json.Memory / 1024),
            node_count=0,
            inner_ip=object_json.Vip,
            charge_type=charge_type,
            storage=int(object_json.Volume / 1024),
            machine=object_json.MachineType,
            cluster_type=object_json.ClusterType,
            mongo_version=object_json.MongoVersion,
            extra={"vpc_id": object_json.VpcId, "subnet_id": object_json.SubnetId},
        ).to_dict()

    def format_load_balancer(self, object_json, **kwargs):
        return LoadBalancer(
            resource_id=object_json.LoadBalancerId,
            resource_name=object_json.LoadBalancerName,
            cloud_type=self.cloud_type,
            net_type=object_json.LoadBalancerType,
            lb_type=object_json.Forward,
            domain=object_json.Domain,
            vips=object_json.LoadBalancerVips,
            status=object_json.Status,
            create_time=object_json.CreateTime,
            status_time=object_json.StatusTime,
            # project=object_json.ProjectId,
            # tag=object_json.Tags,
            vpc=object_json.TargetRegionInfo.VpcId if object_json.TargetRegionInfo else "",
            region=object_json.TargetRegionInfo.Region if object_json.TargetRegionInfo else "",
            ip_version=object_json.AddressIPVersion,
            expire_time=object_json.ExpireTime,
            charge_type=object_json.ChargeType,
            ipv6_addr=object_json.AddressIPv6,
        ).to_dict()

    def format_tke(self, object_json, **kwargs):
        return TKE(
            resource_id=object_json.ClusterId,
            resource_name=object_json.ClusterName,
            cloud_type=self.cloud_type,
            cluster_type=object_json.ClusterType,
            version=object_json.ClusterVersion,
            desc=object_json.ClusterDescription,
            os=object_json.ClusterOs,
            network_settings={
                "cluster_cidr": object_json.ClusterNetworkSettings.ClusterCIDR,
                "ingnor_cluster_cidr_conflict": object_json.ClusterNetworkSettings.IgnoreClusterCIDRConflict,
                "max_node_pod_num": object_json.ClusterNetworkSettings.MaxNodePodNum,
                "max_cluster_service_num": object_json.ClusterNetworkSettings.MaxClusterServiceNum,
                "ipvs": object_json.ClusterNetworkSettings.Ipvs,
                "vpc_id": object_json.ClusterNetworkSettings.VpcId,
                "cni": object_json.ClusterNetworkSettings.Cni,
            }
            if object_json.ClusterNetworkSettings
            else {},
            node_num=object_json.ClusterNodeNum,
            # project=object_json.ProjectId,
            tag=format_tce_k8s_tag(object_json.TagSpecification or []),
            status=object_json.ClusterStatus,
            cluster_property=object_json.Property,
            master_node_num=object_json.ClusterMaterNodeNum or 0,
            image=object_json.ImageId or "",
            os_customize_type=object_json.OsCustomizeType or "",
            container_runtime=object_json.ContainerRuntime or "",
            create_time=handle_time_str(object_json.CreatedTime),
            project=object_json.ProjectId,
        ).to_dict()

    def format_tke_instance(self, obj, **kwargs):
        advance_settings = {
            "data_disk": [],
            "docker_graph_path": "",
            "labels": [],
            "extra_args": "",
            "target": "",
            "user_script": "",
            "unschedulable": 0,
        }
        if obj.InstanceAdvancedSettings:
            data = obj.InstanceAdvancedSettings
            advance_settings["data_disk"] = (
                [
                    {
                        "disk_type": data_disk.DiskType,
                        "file_system": data_disk.FileSystem,
                        "disk_size": data_disk.DiskSize,
                        "auto_format_and_mount": data_disk.AutoFormatAndMount,
                        "mount_target": data_disk.MountTarget,
                    }
                    for data_disk in data.DataDisks
                ]
                if data.DataDisks
                else []
            )
            advance_settings["mount_target"] = data.MountTarget or ""
            advance_settings["docker_graph_path"] = data.DockerGraphPath or ""
            advance_settings["user_script"] = data.UserScript or ""
            advance_settings["unschedulable"] = data.Unschedulable
            advance_settings["labels"] = (
                [{"name": label.Name, "value": label.Value} for label in data.Labels] if data.Labels else []
            )
            advance_settings["extra_args"] = (data.ExtraArgs.Kubelet or "") if data.ExtraArgs else ""
        return TKEInstance(
            cluster=self.extra_params["cluster_id"],
            resource_id=obj.InstanceId,
            resource_name=obj.InstanceId or "",
            cloud_type=self.cloud_type,
            role=obj.InstanceRole,
            failed_reason=obj.FailedReason,
            status=obj.InstanceState,
            drain_status=obj.DrainStatus or "",
            create_time=handle_time_str(obj.CreatedTime),
            data_disk=advance_settings["data_disk"],
            docker_graph_path=advance_settings["docker_graph_path"],
            extra_args=advance_settings["extra_args"],
            labels=advance_settings["labels"],
            target=advance_settings["target"],
            unschedulable=advance_settings["unschedulable"],
            user_script=advance_settings["user_script"],
        ).to_dict()

    @staticmethod
    def format_instance_config(object_json, **kwargs):
        return ZoneInstanceConfig(
            zone=object_json.Zone,
            status=object_json.Status,
            type_name=object_json.TypeName,
            price=object_json.Price,
            instance_family=object_json.InstanceFamily,
            cpu=object_json.Cpu,
            memory=object_json.Memory,
            instance_type=object_json.InstanceType,
            instance_charge_type=object_json.InstanceChargeType,
        ).to_dict()

    def format_bms(self, object_json, **kwargs):
        return BMS(
            cloud_type=self.cloud_type,
            region=self.region_id,
            resource_id=object_json.InstanceId,
            resource_name=object_json.InstanceName or "未命名",
            uuid=object_json.Uuid,
            raid_type=object_json.RaidType,
            os_type=object_json.OperatingSystemType,
            os_version=object_json.OperatingSystem,
            private_ip=json.dumps(object_json.PrivateIpAddresses),
            flavor=object_json.FlavorId,
            create_time=object_json.CreatedTime,
            status=object_json.Status,
            app_id=object_json.AppId,
            zone=object_json.Placement.Zone,
            vpc=object_json.VirtualPrivateCloud.VpcId,
            subnet=object_json.VirtualPrivateCloud.SubnetId,
        ).to_dict()

    def format_ckafka(self, ckafka_obj, **kwargs):
        return CKafka(
            cloud_type=self.cloud_type,
            region=self.region_id,
            zone=self.zone_id,
            resource_id=ckafka_obj.InstanceId,
            resource_name=ckafka_obj.InstanceName,
            vip=ckafka_obj.Vip,
            v_port=ckafka_obj.Vport,
            ip=json.dumps([i.Vip for i in ckafka_obj.VipList]),
            status=ckafka_obj.Status,
            bandwidth=ckafka_obj.Bandwidth,
            disk_size=ckafka_obj.DiskSize,
            tce_zone_id=ckafka_obj.ZoneId,
            vpc=ckafka_obj.VpcId,
            subnet=ckafka_obj.SubnetId,
            renew_flag=ckafka_obj.RenewFlag,
            healthy=ckafka_obj.Healthy,
            healthy_message=ckafka_obj.HealthyMessage,
            create_time=ckafka_obj.CreateTime,
            expire_time=ckafka_obj.ExpireTime,
            is_internal=ckafka_obj.IsInternal,
            topic_num=ckafka_obj.TopicNum,
            tag=format_ckafka_tags(ckafka_obj.Tags),
            version=ckafka_obj.Version,
            tce_zone_ids=json.dumps(ckafka_obj.ZoneIds or []),
            cvm=ckafka_obj.Cvm or 0,
        ).to_dict()

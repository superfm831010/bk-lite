# -*- coding: utf-8 -*-
# @Time : 2021-01-21 10:30
from __future__ import absolute_import, unicode_literals

from common.cmp.cloud_apis.cloud_constant import (
    DiskCategory,
    DiskChargeType,
    EipChargeType,
    ImageStatus,
    ImageType,
    SubnetStatus,
    VMChargeType,
    ZoneStatus,
)
from common.cmp.cloud_apis.cloud_object.base import (
    VM,
    VPC,
    Disk,
    Domain,
    Eip,
    HostMachine,
    Image,
    InstanceType,
    Project,
    Region,
    SecurityGroup,
    SecurityGroupRule,
    Snapshot,
    Subnet,
    Zone,
)
from common.cmp.cloud_apis.resource_apis.resource_format.common.common_format import FormatResource
from common.cmp.cloud_apis.resource_apis.resource_format.openstack.openstack_format_utils import (
    handle_network_status,
    handle_snapshot_status,
    handle_vm_status,
    handle_volume_status,
)
from common.cmp.cloud_apis.resource_apis.utils import init_value


class OpenStackFormatResource(FormatResource):
    def __init__(self, project_id="", region_id="", cloud_type=""):
        self.project_id = project_id
        self.region_id = region_id
        self.cloud_type = cloud_type

    def __new__(cls, *args, **kwargs):
        return super(OpenStackFormatResource, cls).__new__(cls, *args, **kwargs)

    def format_domain(self, obj, **kwargs):
        """
        区域格式转换
        """
        return Domain(
            cloud_type=self.cloud_type,
            resource_id=obj.id,
            resource_name=obj.name,
            enabled=obj.enabled,
            desc=obj.description,
            tag=[],
        ).to_dict()

    def format_project(self, obj, **kwargs):
        """
        区域格式转换
        """
        return Project(
            cloud_type=self.cloud_type,
            resource_id=obj.id,
            resource_name=obj.name,
            enabled=obj.enabled,
            desc=obj.description,
            extra={"domain_info": kwargs["domain_obj"]},
            tag=[],
        ).to_dict()

    def format_region(self, obj, **kwargs):
        """
        区域格式转换
        """
        return Region(
            cloud_type=self.cloud_type,
            resource_id=obj.id,
            resource_name=obj.id,
            desc=obj.description,
        ).to_dict()

    def format_zone(self, obj, **kwargs):
        """
        可用区格式转换
        """
        return Zone(
            region=self.region_id,  # todo
            cloud_type=self.cloud_type,
            resource_id=obj.zoneName,
            resource_name=obj.zoneName,
            status=ZoneStatus.AVAILABLE.value if obj.zoneState.get("available") else ZoneStatus.UNAVAILABLE.value,
        ).to_dict()

    def format_instance_type(self, obj, **kwargs):
        """
        规格格式转换
        """
        return InstanceType(
            resource_id=obj.id,
            resource_name=obj.name,
            vcpus=int(obj.vcpus),
            memory=int(obj.ram),
            disk=int(obj.disk),
            instance_family="",
            project=self.project_id,
            region=self.region_id,
            extra={
                "swap": obj.swap,
                "rxtx_factor": obj.rxtx_factor,
                "os-flavor-access:is_public": obj.rxtx_factor,
                "ephemeral": obj.ephemeral,
            },
        ).to_dict()

    def format_vm(self, obj, **kwargs):
        """
        虚拟机格式转换
        """
        return VM(
            cloud_type=self.cloud_type,
            resource_id=obj.id,
            resource_name=obj.name,
            uuid=obj.id,
            desc="",
            instance_type=kwargs["flavor_obj"]["resource_id"],
            vcpus=int(kwargs["flavor_obj"]["vcpus"]),
            memory=int(kwargs["flavor_obj"]["memory"]),
            image=kwargs["image_id"],
            os_name="",
            status=handle_vm_status(obj.status),
            inner_ip=kwargs["inner_ip_list"],
            public_ip=kwargs["out_ip_list"],
            system_disk=kwargs["system_disk"],
            data_disk=kwargs["disk_list"],
            charge_type=VMChargeType.UNKNOWN.value,
            internet_accessible={},
            vpc="",  # 底层sdk无法获取
            subnet="",  # 底层sdk无法获取
            security_group=kwargs["security_group_info"],
            project=self.project_id,
            zone=getattr(obj, "OS-EXT-AZ:availability_zone"),
            region=self.region_id,
            login_settings={},
            create_time=obj.created[:19].replace("T", " "),
            expired_time="",
            peak_period=None,
            tag=[],
            extra={
                "OS-EXT-SRV-ATTR:instance_name": getattr(obj, "OS-EXT-SRV-ATTR:instance_name"),
                "OS-SRV-USG:launched_at": (getattr(obj, "OS-SRV-USG:launched_at", "") or "")[:19].replace("T", " "),
            },
        ).to_dict()

    def format_disk(self, obj, **kwargs):
        """
        磁盘格式转换
        """
        return Disk(
            cloud_type=self.cloud_type,
            resource_id=obj.id,
            resource_name=obj.name if obj.name else "",
            desc=obj.description if obj.description else "",
            disk_type=kwargs["cur_disk_dict"]["disk_type"],
            disk_size=obj.size,
            charge_type=DiskChargeType.UNKNOWN.value,
            portable=True,
            snapshot_ability=True,
            status=handle_volume_status(obj.status),
            category=DiskCategory.CLOUD_UNKNOWN.value,
            is_attached=kwargs["cur_disk_dict"]["is_attached"],
            server_id=init_value(["cur_disk_dict", "vm_id"], kwargs),
            create_time=obj.created_at[:19].replace("T", " "),
            expired_time="",
            encrypt=obj.encrypted,
            delete_with_instance=True,
            serial_number="",
            storage="",
            project=self.project_id,
            zone="",
            region=self.region_id,
            tag=[],
            extra={"bootable": obj.bootable, "attached_mode": obj.metadata.get("attached_mode", "")},
        ).to_dict()

    def format_snapshot(self, obj, **kwargs):
        """
        快照格式转换
        """
        return Snapshot(
            cloud_type=self.cloud_type,
            resource_id=obj.id,
            resource_name=obj.name,
            desc=obj.description if obj.description else "",
            disk_type="",
            disk_id=kwargs["disk_id"],
            disk_size=0,
            status=handle_snapshot_status(obj.status),
            create_time=obj.created_at[:19].replace("T", " "),
            expired_time="",
            encrypt=False,
            is_permanent=True,
            server_id="",
            project=self.project_id,
            zone="",
            region=self.region_id,
            tag=[],
            extra={"progress": obj.progress},
        ).to_dict()

    def format_image(self, obj, **kwargs):
        """
        镜像格式转换
        """
        return Image(
            cloud_type=self.cloud_type,
            resource_id=obj.id,
            resource_name=obj.name,
            desc="",
            tag=obj.tags,
            create_time=obj.created_at[:19].replace("T", " "),
            image_family="",
            arch="",
            image_type=ImageType.PRIVATE.value,
            image_version="",
            os_name="",
            os_name_en="",
            os_type="",
            size=float(obj.size or 0) / 1024 / 1024 / 1024,
            status=ImageStatus.AVAILABLE.value,
            image_format=obj.disk_format,
            platform="",
            project=self.project_id,
            extra={"min_disk": obj.min_disk, "min_ram": obj.min_ram},
        ).to_dict()

    def format_vpc(self, obj, **kwargs):
        """
        VPC格式转换
        """
        return VPC(
            cloud_type=self.cloud_type,
            resource_id=obj["id"],
            resource_name=obj["name"],
            desc=init_value(["description"], obj),
            tag=obj.get("tags", []),
            extra={
                "mtu": init_value(["mtu"], obj),
                "shared": "是" if obj.get("shared") else "否",
                "admin_state_up": "开启" if obj.get("admin_state_up") else "关闭",
            },
            status=handle_network_status(obj["status"]),
            cidr="",
            cidr_v6="",
            router="",
            router_tables=[],
            resource_group="",
            is_default=False,
            create_time=obj.get("updated_at")[:19].replace("T", " "),
            dns=[],
            host="",
            project=self.project_id,
            zone=kwargs["zone_id"],
            region=self.region_id,
        ).to_dict()

    def format_subnet(self, obj, **kwargs):
        """
        子网格式转换
        """
        return Subnet(
            cloud_type=self.cloud_type,
            resource_id=obj["id"],
            resource_name=obj["name"],
            desc=init_value(["description"], obj),
            tag=[],
            extra={"dns": obj.get("dns_nameservers", [])},
            status=SubnetStatus.AVAILABLE.value,
            gateway=init_value(["gateway_ip"], obj),
            cidr=obj["cidr"],
            cidr_v6="",
            vpc=obj["network_id"],
            create_time=obj.get("created_at")[:19].replace("T", " "),
            router_table_id="",
            is_default=False,
            resource_group="",
            project=self.project_id,
            zone=init_value(["availability_zone"], obj),
            region=self.region_id,
        ).to_dict()

    def format_security_group(self, obj, **kwargs):
        """
        安全组格式转换
        """
        return SecurityGroup(
            cloud_type=self.cloud_type,
            resource_id=obj["id"],
            resource_name=obj["name"],
            desc=init_value(["description"], obj),
            tag=init_value(["tags"], obj, list),
            extra={},
            is_default=False,
            create_time=obj.get("created_at")[:19].replace("T", " "),
            resource_group="",
            vpc="",
            project=self.project_id,
            zone="",
            region=self.region_id,
        ).to_dict()

    def format_security_group_rule(self, obj, **kwargs):
        """
        安全组规则格式转换
        """
        return SecurityGroupRule(
            cloud_type=self.cloud_type,
            resource_id=obj["id"],
            resource_name=obj["id"],
            desc=init_value(["description"], obj),
            tag=[],
            extra={},
            direction="INGRESS" if obj["direction"] == "ingress" else "EGRESS",
            dest_cidr=init_value(["remote_ip_prefix"], obj),
            dest_group_id="",
            source_cidr=init_value(["remote_ip_prefix"], obj),
            source_group_id="",  # 源安全组id
            create_time="",
            modify_time="",
            nic_type="",
            protocol=obj["protocol"] if obj.get("protocol") else "ALL",
            port_range=[init_value(["port_range_min"], obj), init_value(["port_range_max"], obj)],
            priority="",
            security_group=obj["security_group_id"],
            action="",
            project=self.project_id,
            zone="",
            region=self.region_id,
        ).to_dict()

    def format_eip(self, obj, **kwargs):
        """
        eip格式转换
        """
        return Eip(
            cloud_type=self.cloud_type,
            resource_id=obj["id"],
            resource_name=obj["floating_ip_address"],
            desc=init_value(["description"], obj),
            tag=[],
            status=obj["status"],
            ip_addr=obj["floating_ip_address"],
            instance_id="",
            create_time=obj["created_at"],
            nic_id="",
            private_ip_addr=obj["fixed_ip_address"],
            is_attached=False,
            bandwidth="",
            charge_type=EipChargeType.UNKNOWN_PAID.value,
            expired_time="",
            provider="",
            resource_group="",
            project=self.project_id,
            zone="",
            region=self.region_id,
            extra={},
        ).to_dict()

    def format_hypervisor(self, obj, **kwargs):
        """
        hypervisor格式转换
        """
        return HostMachine(
            cloud_type=self.cloud_type,
            resource_id=obj.id,
            resource_name=obj.hypervisor_hostname,
            desc="",
            tag=[],
            extra={},
            status="开启" if obj.status == "enabled" else "关闭",
            cpu=obj.vcpus,
            memory=obj.memory_mb,
            local_storage=obj.local_gb,
            memory_usage=obj.memory_mb_used,
            cpu_usage="",
            local_storage_usage=obj.local_gb_used,
            memory_free=obj.free_ram_mb,
            cpu_free="",
            local_storage_free="",
            running_instances=obj.running_vms,
            total_instances="",
            project=self.project_id,
            zone="",
            region=self.region_id,
        ).to_dict()

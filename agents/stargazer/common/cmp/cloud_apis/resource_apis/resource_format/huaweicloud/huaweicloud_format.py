# -*- coding: utf-8 -*-
# @Time : 2021-01-18 19:14
from __future__ import absolute_import, unicode_literals

from common.cmp.cloud_apis.cloud_constant import DiskChargeType, DiskType, ZoneStatus
from common.cmp.cloud_apis.cloud_object.base import (
    VM,
    VPC,
    Bucket,
    BucketFile,
    Disk,
    Domain,
    Eip,
    Image,
    InstanceType,
    InstanceTypeFamily,
    LoadBalancer,
    LoadBalancerListener,
    Project,
    Region,
    RelayRule,
    RouteEntry,
    RouteTable,
    SecurityGroup,
    SecurityGroupRule,
    Snapshot,
    Subnet,
    VServerGroup,
    Zone,
)
from common.cmp.cloud_apis.resource_apis.resource_format.common.common_format import FormatResource
from common.cmp.cloud_apis.resource_apis.resource_format.huaweicloud.huaweicloud_format_utils import (
    handle_bucket_type,
    handle_charge_type,
    handle_eip_charge_type,
    handle_eip_status,
    handle_image_status,
    handle_image_type,
    handle_snapshot_status,
    handle_subnet_status,
    handle_vm_status,
    handle_volume_category,
    handle_volume_status,
    handle_vpc_status,
)
from common.cmp.cloud_apis.resource_apis.utils import handle_time_stamp, handle_time_str, init_value


class HuaweicloudFormatResource(FormatResource):
    def __init__(self, region_id="", project_id="", cloud_type=""):
        self.region_id = region_id
        self.project_id = project_id
        self.cloud_type = cloud_type

    def __new__(cls, *args, **kwargs):
        return super(HuaweicloudFormatResource, cls).__new__(cls, *args, **kwargs)

    def format_domain(self, object_json, **kwargs):
        """
        区域格式转换
        """
        return Domain(
            cloud_type=self.cloud_type,
            resource_id=object_json["id"],
            resource_name=object_json["name"],
            enabled=object_json["enabled"],
        ).to_dict()

    def format_project(self, object_json, **kwargs):
        """
        区域格式转换
        """
        return Project(
            cloud_type=self.cloud_type,
            resource_id=object_json["id"],
            resource_name=object_json["name"],
            enabled=object_json["enabled"],
            desc=object_json["description"],
        ).to_dict()

    def format_region(self, object_json, **kwargs):
        """
        区域格式转换
        """
        return Region(
            cloud_type=self.cloud_type,
            resource_id=object_json["id"],
            resource_name=object_json["locales"]["zh_cn"],
            desc=object_json["description"],
        ).to_dict()

    def format_zone(self, object_json, **kwargs):
        """
        可用区格式转换
        """
        return Zone(
            region=self.region_id,
            cloud_type=self.cloud_type,
            resource_id=object_json["zone_name"],
            resource_name=object_json["zone_name"],
            status=ZoneStatus.AVAILABLE.value
            if object_json["zone_state"].get("available")
            else ZoneStatus.UNAVAILABLE.value,
        ).to_dict()

    def format_instance_type_family(self, object_json, **kwargs):
        """
        规格族格式转换
        """
        return InstanceTypeFamily(
            cloud_type=self.cloud_type,
            resource_id=object_json["id"],
            resource_name=object_json["name"],
        ).to_dict()

    def format_instance_type(self, object_json, **kwargs):
        """
        规格格式转换
        """
        return InstanceType(
            resource_id=object_json["id"],
            resource_name=object_json["name"],
            vcpus=int(object_json["vcpus"]),
            memory=int(object_json["ram"]),
            disk=object_json["disk"],
            instance_family=object_json["id"].split(".")[0],
            project=self.project_id,
            region=self.region_id,
        ).to_dict()

    def format_vm(self, object_json, **kwargs):
        """
        虚拟机格式转换
        """
        inner_ip = []
        public_ip = []
        disk_list = object_json.get("os_extended_volumesvolumes_attached", [])
        system_disk = {}
        port_id = ""
        if "addresses" in object_json:
            for j in list(object_json["addresses"].values())[0]:
                if not port_id:
                    port_id = j.os_ext_ip_sport_id
                if j.os_ext_ip_stype == "fixed":
                    inner_ip.append(j.addr)
                if j.os_ext_ip_stype == "floating":
                    public_ip.append(j.addr)
        data_disk_list = []
        for disk in disk_list:
            if disk["boot_index"] == "0":
                system_disk["id"] = disk["id"]
            else:
                data_disk_list.append(disk["id"])
        security_group_list = []
        for security_group in object_json.get("security_groups", []):
            security_group_list.append(security_group["id"])
        return VM(
            cloud_type=self.cloud_type,
            resource_id=object_json["id"],
            resource_name=object_json["name"],
            uuid=object_json["host_id"],
            desc=init_value(["description"], object_json),
            instance_type=object_json["flavor"]["id"],
            vcpus=int(object_json["flavor"]["vcpus"]),
            memory=int(object_json["flavor"]["ram"]),
            image=init_value(["image", "id"], object_json),
            os_name=object_json["metadata"].get("image_name", ""),
            status=handle_vm_status(object_json["status"]),
            inner_ip=inner_ip,
            public_ip=public_ip,
            system_disk=system_disk,
            data_disk=data_disk_list,
            charge_type=handle_charge_type(object_json["metadata"]["charging_mode"]),
            internet_accessible={},
            vpc=object_json["metadata"]["vpc_id"],
            subnet=object_json["subnet_id"],
            security_group=security_group_list,
            project=self.project_id,
            zone=init_value(["os_ext_a_zavailability_zone"], object_json),
            region=self.region_id,
            login_settings={},
            create_time=handle_time_str(object_json["created"]),
            expired_time="",
            peak_period=None,
            tag=object_json.get("tags"),
            extra={"port_id": port_id},
        ).to_dict()

    def format_disk(self, object_json, **kwargs):
        """
        磁盘格式转换
        """
        is_attached = False
        tags = []
        host_id = ""
        if "tags" in object_json:
            for k, v in object_json["tags"].items():
                tags.append({k: v})
        if len(object_json["attachments"]) > 0:
            host_id = object_json["attachments"][0]["server_id"]
            is_attached = True
        return Disk(
            cloud_type=self.cloud_type,
            resource_id=object_json["id"],
            resource_name=object_json["name"],
            desc=object_json.get("description", ""),
            disk_type=DiskType.SYSTEM_DISK.value if object_json["bootable"] == "true" else DiskType.DATA_DISK.value,
            disk_size=object_json["size"],
            charge_type=DiskChargeType.PREPAID.value
            if object_json["metadata"]["order_id"]
            else DiskChargeType.POSTPAID_BY_HOUR.value,
            portable=True,
            snapshot_ability=True,
            status=handle_volume_status(object_json["status"]),
            category=handle_volume_category(object_json["volume_type"]),
            is_attached=is_attached,
            server_id=host_id,
            create_time=handle_time_str(object_json["created_at"]),
            expired_time="",
            encrypt=object_json.get("encrypted", False),
            delete_with_instance=True,
            serial_number="",
            storage="",
            project=self.project_id,
            zone=object_json["availability_zone"],
            region=self.region_id,
            tag=[],
            extra={},
        ).to_dict()

    def format_snapshot(self, object_json, **kwargs):
        """
        快照格式转换
        """
        return Snapshot(
            cloud_type=self.cloud_type,
            resource_id=object_json["id"],
            resource_name=object_json["name"],
            desc=init_value(["description"], object_json),
            disk_type="",
            disk_id=object_json["volume_id"],
            disk_size=object_json["size"],
            status=handle_snapshot_status(object_json["status"]),
            create_time=handle_time_str(object_json["created_at"]),
            expired_time="",
            encrypt=False,
            is_permanent=True,
            server_id="",
            project=self.project_id,
            zone="",
            region=self.region_id,
            tag=[],
            extra={},
        ).to_dict()

    def format_image(self, object_json, **kwargs):
        """
        镜像格式转换
        """
        return Image(
            cloud_type=self.cloud_type,
            resource_id=object_json["id"],
            resource_name=object_json["name"],
            desc=init_value(["description"], object_json),
            tag=[],
            extra={},
            create_time=handle_time_str(object_json["created_at"]),
            image_family="",
            arch=init_value(["architecture"], object_json),
            image_type=handle_image_type(object_json.get("imagetype")),
            image_version="",
            os_name=init_value(["os_version"], object_json),
            os_name_en="",
            os_type=init_value(["os_type"], object_json),
            size=float(object_json["image_size"]) / 1024 / 1024 / 1024 if object_json.get("image_size") else 0,
            status=handle_image_status(object_json["status"]),
            image_format=init_value(["disk_format"], object_json),
            platform=init_value(["platform"], object_json),
            project=self.project_id,
        ).to_dict()

    def format_vpc(self, object_json, **kwargs):
        """
        VPC格式转换
        """
        return VPC(
            cloud_type=self.cloud_type,
            resource_id=object_json["id"],
            resource_name=object_json["name"],
            desc=init_value(["description"], object_json),
            tag=[],
            extra={},
            status=handle_vpc_status(object_json["status"]),
            cidr=object_json["cidr"],
            cidr_v6="",
            router="",
            router_tables=[],
            resource_group="",
            is_default=True if "vpc-default" in object_json.get("description", "") else False,
            create_time="",
            dns=[],
            host="",
            project=self.project_id,
            zone="",
            region=self.region_id,
        ).to_dict()

    def format_subnet(self, object_json, **kwargs):
        """
        子网格式转换
        """
        return Subnet(
            cloud_type=self.cloud_type,
            resource_id=object_json["id"],
            resource_name=object_json["name"],
            desc=init_value(["description"], object_json),
            tag=[],
            extra={"dns": object_json.get("dns_list", [])},
            status=handle_subnet_status(object_json["status"]),
            gateway=object_json["gateway_ip"],
            cidr=object_json["cidr"],
            cidr_v6=init_value(["cidr_v6"], object_json),
            vpc=object_json["vpc_id"],
            create_time="",
            router_table_id="",
            is_default=False,
            resource_group="",
            project=self.project_id,
            zone=init_value(["availability_zone"], object_json),
            region=self.region_id,
        ).to_dict()

    def format_eip(self, object_json, **kwargs):
        """
        弹性公网IP格式转换
        """
        return Eip(
            cloud_type=self.cloud_type,
            resource_id=object_json["id"],
            resource_name=object_json.get("name") or "未命名",
            desc=init_value(["description"], object_json),
            tag=[],
            status=handle_eip_status(object_json["status"]),
            ip_addr=init_value(["public_ip_address"], object_json),
            instance_id="",
            create_time=object_json["create_time"].strftime("%Y-%m-%d %H:%M:%S"),
            nic_id="",
            private_ip_addr=init_value(["public_ip_address"], object_json),
            is_attached=True if object_json.get("port_id") else False,
            bandwidth=init_value(["bandwidth_size"], object_json),
            charge_type=handle_eip_charge_type(object_json["charge_type"]),
            expired_time="",
            provider="",
            resource_group="",
            project=self.project_id,
            zone="",
            region=self.region_id,
            extra={"port_id": init_value(["port_id"], object_json)},
        ).to_dict()

    def format_security_group(self, object_json, **kwargs):
        """
        安全组格式转换
        """
        return SecurityGroup(
            cloud_type=self.cloud_type,
            resource_id=object_json["id"],
            resource_name=object_json["name"],
            desc=init_value(["description"], object_json),
            tag=[],
            extra={},
            is_default=False,
            create_time="",
            resource_group="",
            vpc=init_value(["vpc_id"], object_json),
            project=self.project_id,
            zone="",
            region=self.region_id,
        ).to_dict()

    def format_security_group_rule(self, object_json, **kwargs):
        """
        安全组规则格式转换
        """
        return SecurityGroupRule(
            cloud_type=self.cloud_type,
            resource_id=object_json["id"],
            resource_name=object_json["name"] if object_json.get("name") else "未命名",
            desc=init_value(["description"], object_json),
            tag=[],
            extra={},
            direction=object_json["direction"].upper(),
            dest_cidr="",
            dest_group_id="",
            source_cidr="",
            source_group_id="",  # 源安全组id
            create_time="",
            modify_time="",
            nic_type="",
            protocol=object_json["protocol"] or "ALL",
            port_range=[init_value(["port_range_min"], object_json), init_value(["port_range_max"], object_json)],
            priority="",
            security_group=object_json["security_group_id"],
            action="",
            project=self.project_id,
            zone="",
            region=self.region_id,
        ).to_dict()

    def format_bucket(self, object_json, **kwargs):
        """
        存储桶格式转换
        """
        return Bucket(
            cloud_type=self.cloud_type,
            resource_id=object_json["name"],
            resource_name=object_json["name"],
            desc=object_json["description"] if object_json.get("description") else "",
            tag=[],
            region=self.region_id,
            extra={
                "capacity": init_value(["capacity"], object_json, "int"),
                "object_num": init_value(["object_num"], object_json, "int"),
                "size": object_json["capacity"],
            },
            bucket_type=handle_bucket_type(init_value(["bucket_type"], object_json)),
            create_time="",
            modify_time="",
        ).to_dict()

    def format_load_balancer(self, object_json, **kwargs):
        return LoadBalancer(
            resource_id=object_json.get("id"),
            resource_name=object_json.get("name"),
            desc=object_json.get("description") or "",
            project=object_json.get("project"),
            vpc=object_json.get("vpc_id"),
            status=object_json.get("provisioning_status") == "ACTIVE",
            create_time=object_json.get("created_at"),
            ipv6_addr=object_json.get("ipv6_vip_address"),
            backend_servers=[{"ServerId": i.get("id")} for i in object_json.get("pools", [])],
            cloud_type=self.cloud_type,
            region=self.region_id,
            extra={"publicips": object_json.get("publicips"), "listeners": object_json.get("listeners")},
        ).to_dict()

    def format_listener(self, object_json, **kwargs):
        return LoadBalancerListener(
            cloud_type=self.cloud_type,
            region=self.region_id,
            resource_id=object_json.get("id"),
            resource_name=object_json.get("name"),
            front_version=object_json.get("protocol"),
            front_port=object_json.get("protocol_port"),
            desc=object_json.get("description") or "",
            load_balancer=object_json["loadbalancers"][0].get("id") if object_json.get("loadbalancers") else "",
            create_time=object_json.get("created_at"),
            server_group=object_json.get("default_pool_id") or "",
        ).to_dict()

    def format_rule(self, object_json, **kwargs):
        return RelayRule(
            cloud_type=self.cloud_type,
            region=self.region_id,
            resource_id=object_json.get("id"),
            url=object_json.get("value"),
        ).to_dict()

    def format_backend_server_group(self, object_json, **kwargs):
        load_balancer = object_json["loadbalancers"][0].get("id", "") if object_json.get("loadbalancers") else ""
        members = []
        listens = []
        if object_json.get("members"):
            members = [{"ServerId": item.get("id")} for item in object_json["members"]]
        if object_json.get("listens"):
            listens = [item.get("id", "") for item in object_json["listens"]]
        return VServerGroup(
            cloud_type=self.cloud_type,
            region=self.region_id,
            resource_id=object_json.get("id"),
            resource_name=object_json.get("name"),
            backend_servers=members,
            listens=listens,
            load_balancer=load_balancer,
            extra={"protocol": object_json.get("protocol"), "healthmonitor_id": object_json.get("healthmonitor_id")},
        ).to_dict()

    def format_route_tables(self, object_json, **kwargs):
        subnets = [item.get("id") for item in object_json.get("subnets")]
        return RouteTable(
            cloud_type=self.cloud_type,
            region=self.region_id,
            resource_id=object_json.get("id"),
            resource_name=object_json.get("name"),
            vpc=object_json.get("vpc_id"),
            desc=object_json.get("description") or "",
            subnets=subnets,
        ).to_dict()

    def format_route(self, object_json, **kwargs):
        return RouteEntry(
            cloud_type=self.cloud_type,
            region=self.region_id,
            resource_id=object_json.get("id"),
            next_hops={"nexthop": object_json.get("nexthop"), "type": object_json.get("type")},
            cidr_block=object_json.get("destination"),
            extra={"vpc_id": object_json.get("vpc_id")},
        ).to_dict()

    def format_relay_rule(self, object_json, **kwargs):
        return RelayRule(
            cloud_type=self.cloud_type,
            region=self.region_id,
            resource_id=object_json.get("id"),
            resource_name=object_json.get("name"),
        ).to_dict()

    def format_bucket_file(self, file_object, **kwargs):
        return BucketFile(
            modify_time=handle_time_stamp(file_object.last_modified)
            if isinstance(file_object.last_modified, int)
            else "",
            size=file_object.size,
            file_type=file_object.type,
            parent=file_object.parent or "/",
            bucket=file_object.bucket,
            resource_id="{}<>{}".format(file_object.bucket, file_object.key),
            cloud_type=self.cloud_type,
            extra={"location": file_object.location},
        ).to_dict()

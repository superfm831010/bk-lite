# -*- coding: utf-8 -*-
# @Time : 2021-01-22 17:29

from common.cmp.cloud_apis.cloud_constant import (
    DiskCategory,
    DiskChargeType,
    DiskType,
    ImageStatus,
    ImageType,
    SubnetStatus,
    VMChargeType,
    VPCStatus,
    ZoneStatus,
)
from common.cmp.cloud_apis.cloud_object.base import (
    VM,
    VPC,
    Bucket,
    BucketFile,
    Disk,
    Domain,
    Eip,
    FusionCloudDiskType,
    Image,
    InstanceType,
    LoadBalancer,
    LoadBalancerListener,
    Project,
    Region,
    RelayRule,
    RouteEntry,
    SecurityGroup,
    SecurityGroupRule,
    Snapshot,
    Subnet,
    VServerGroup,
    Zone,
)
from common.cmp.cloud_apis.resource_apis.resource_format.common.common_format import FormatResource
from common.cmp.cloud_apis.resource_apis.resource_format.openstack.openstack_format_utils import (
    handle_snapshot_status,
    handle_vm_status,
    handle_volume_status,
)
from common.cmp.cloud_apis.resource_apis.utils import handle_time_str


class FusionCloudFormatResource(FormatResource):
    def __init__(self, region_id="", project_id="", cloud_type=""):
        self.region_id = region_id
        self.project_id = project_id
        self.cloud_type = cloud_type

    def __new__(cls, *args, **kwargs):
        return super(FusionCloudFormatResource, cls).__new__(cls, *args, **kwargs)

    def format_domain(self, object_json, **kwargs):
        """
        区域格式转换
        """
        return Domain(
            cloud_type=self.cloud_type,
            resource_id=object_json["id"],
            resource_name=object_json.get("name", "未命名"),
            enabled=object_json.get("enabled", True),
            desc=object_json.get("description", "") or "",
        ).to_dict()

    def format_project(self, object_json, **kwargs):
        """
        区域格式转换
        """
        return Project(
            cloud_type=self.cloud_type,
            resource_id=object_json["id"],
            resource_name=object_json.get("name", "未命名"),
            enabled=object_json.get("enabled", True),
            desc=object_json.get("description", "") or "",
        ).to_dict()

    def format_region(self, object_json, **kwargs):
        """
        区域格式转换
        """
        return Region(
            cloud_type=self.cloud_type,
            resource_id=object_json["id"],
            resource_name=object_json["locales"]["zh-cn"],
            desc="",
        ).to_dict()

    def format_zone(self, object_json, **kwargs):
        """
        可用区格式转换
        """
        return Zone(
            region=kwargs.get("region", ""),
            cloud_type=self.cloud_type,
            resource_id=object_json["zoneName"],
            resource_name=object_json["zoneName"],
            status=ZoneStatus.AVAILABLE.value,
        ).to_dict()

    def format_instance_type(self, object_json, **kwargs):
        """
        规格格式转换
        """
        return InstanceType(
            resource_id=object_json["id"],
            resource_name=object_json.get("name", "未命名"),
            project=self.project_id,
            region=kwargs.get("region", ""),
        ).to_dict()

    def format_server(self, object_json, **kwargs):
        """8.0.3虚拟机格式转换"""
        return self.format_vm(object_json, **kwargs)

    def format_vm(self, object_json, **kwargs):
        """
        虚拟机格式转换
        """
        flavor_id = ""
        if object_json.get("flavor"):
            flavor_id = object_json["flavor"].get("id")
        image_id = ""
        if object_json.get("image"):
            image_id = object_json["image"].get("id")

        nic_list = []
        inner_ip_list = []
        out_ip_list = []
        for k, v in object_json.get("addresses").items():
            nic_obj = {"name": k}
            for n in v:
                nic_obj.update(
                    {
                        "type": n["OS-EXT-IPS:type"],
                        "version": n["version"],
                        "ip": n["addr"],
                        "mac": n["OS-EXT-IPS-MAC:mac_addr"],
                    }
                )
                if n["OS-EXT-IPS:type"] == "fixed":
                    inner_ip_list.append(n["addr"])
                else:
                    out_ip_list.append(n["floating"])
            nic_list.append(nic_obj)
        mem = 0
        vcpus = 0
        vm_config = object_json.get("metadata").get("cascaded.instance_extrainfo").split(",")
        for i in vm_config:
            detail = i.split(":")
            if detail[0] == "current_mem":
                mem = int(detail[1])
            if detail[0] == "current_cpu":
                vcpus = int(detail[1])
        return VM(
            cloud_type=self.cloud_type,
            resource_id=object_json["id"],
            resource_name=object_json.get("name", "未命名"),
            uuid=object_json["id"],
            desc=object_json.get("description", "") or "",
            instance_type=flavor_id,
            vcpus=vcpus,
            memory=mem,
            image=image_id,
            os_name="",
            status=handle_vm_status(object_json["status"]),
            inner_ip=inner_ip_list,
            public_ip=out_ip_list,
            system_disk={},
            data_disk=object_json.get("os-extended-volumes:volumes_attached", []),
            charge_type=VMChargeType.UNKNOWN.value,
            internet_accessible={},
            vpc="",
            subnet="",
            security_group=[],
            project=self.project_id,
            zone=object_json.get("OS-EXT-AZ:availability_zone", ""),
            region=kwargs.get("region"),
            login_settings={},
            create_time=object_json["created"][:19].replace("T", " "),
            # 有server_expiry取过期时间，没有此字段按照不限时间处理
            expired_time=object_json.get("metadata").get("server_expiry", "0") or "0",
            peak_period=None,
            tag=[],
            extra={"security_group_name": object_json.get("security_groups", [])},  # 目前只能获取到安全组name列表
        ).to_dict()

    def format_disk(self, object_json, **kwargs):
        """
        磁盘格式转换
        """
        is_attached = False
        server_id = ""
        attachments = object_json.get("attachments")
        if len(attachments) > 0:
            is_attached = True
            server_id = attachments[0].get("server_id")
        return Disk(
            cloud_type=self.cloud_type,
            resource_id=object_json["id"],
            resource_name=object_json.get("name", "未命名"),
            desc=object_json.get("description") or "",
            disk_type=DiskType.SYSTEM_DISK.value if object_json.get("bootable") == "true" else DiskType.DATA_DISK.value,
            disk_size=object_json.get("size", 0),
            charge_type=DiskChargeType.UNKNOWN.value,
            portable=True,
            snapshot_ability=True,
            status=handle_volume_status(object_json["status"]),
            category=DiskCategory.CLOUD_UNKNOWN.value,
            is_attached=is_attached,
            server_id=server_id,
            create_time=object_json["created_at"][:19].replace("T", " "),
            expired_time="",
            encrypt=object_json.get("encrypted", False),
            delete_with_instance=True,
            serial_number="",
            storage="",
            project=self.project_id,
            zone=object_json.get("availability_zone", ""),
            region=kwargs.get("region", ""),
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
            resource_name=object_json.get("name", "未命名"),
            desc=object_json.get("description", "") or "",
            disk_type="",
            disk_id=object_json.get("volume_id", ""),
            disk_size=0,
            status=handle_snapshot_status(object_json["status"]),
            create_time=object_json.get("created_at")[:19].replace("T", " "),
            expired_time="",
            encrypt=False,
            is_permanent=True,
            server_id="",
            project=self.project_id,
            zone="",
            region=kwargs.get("region", ""),
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
            resource_name=object_json.get("name", "未命名"),
            desc=object_json.get("describe", "") or "",
            tag=object_json.get("tags", []),
            extra={},
            create_time=object_json["created_at"][:19].replace("T", " "),
            image_family="",
            arch="",
            image_type=ImageType.PRIVATE.value,
            image_version="",
            os_name=object_json.get("os_version", ""),
            os_name_en="",
            os_type=object_json.get("__os_type", ""),
            size=float(round(object_json.get("size", 0) / 1073741824, 2)),
            status=ImageStatus.AVAILABLE.value,
            image_format="",
            platform=object_json.get("__os_version", ""),
            project=self.project_id,
        ).to_dict()

    def format_vpc(self, object_json, **kwargs):
        """
        VPC格式转换
        """
        return VPC(
            cloud_type=self.cloud_type,
            resource_id=object_json["id"],
            resource_name=object_json.get("name", "未命名"),
            desc=object_json.get("description", "") or "",
            tag=[],
            extra={},
            status=VPCStatus.AVAILABLE.value,
            cidr="",
            cidr_v6="",
            router="",
            router_tables=[],
            resource_group="",
            is_default=False,
            create_time="",
            dns=[],
            host="",
            project=self.project_id,
            zone="",
            region=kwargs.get("region"),
        ).to_dict()

    def format_subnet(self, object_json, **kwargs):
        """
        子网格式转换
        """
        if object_json.get("status") == "UNKNOWN":
            return
        return Subnet(
            cloud_type=self.cloud_type,
            resource_id=object_json["id"],
            resource_name=object_json.get("name", "未命名"),
            desc="",
            tag=[],
            extra={"neutron_subnet_id": object_json.get("neutron_subnet_id")},
            status=SubnetStatus.AVAILABLE.value,
            gateway=object_json.get("gateway_ip", ""),
            cidr=object_json.get("cidr", ""),
            cidr_v6=object_json.get("cidr_v6", ""),
            vpc=object_json.get("vpc_id", ""),
            # create_time=object_json["created_at"][:19].replace("T", " ") if object_json.get("created_at") else "",
            router_table_id="",
            is_default=False,
            resource_group="",
            project=self.project_id,
            zone=object_json.get("availability_zone", ""),
            region=kwargs.get("region"),
        ).to_dict()

    def format_eip(self, object_json, **kwargs):
        status_map = {
            "ACTIVE": "BIND",
            "DOWN": "UNBIND",
            "ERROR": "UNKNOWN",
        }
        return Eip(
            resource_id=object_json.get("id"),
            status=status_map.get(object_json.get("status"), object_json.get("status")),
            ip_addr=object_json.get("floating_ip_address", "") or "",
            private_ip_addr=object_json.get("fixed_ip_address", "") or "",
            create_time=object_json.get("created_at")[:19].replace("T", " "),
            bandwidth=0,
            project=object_json.get("project_id", "") or "",
            is_attached=True if object_json.get("port_id") else False,
            cloud_type=self.cloud_type,
            extra={
                "router_id": object_json.get("router_id", "") or "",
                "tenant_id": object_json.get("tenant_id", "") or "",
                "qos_policy_id": object_json.get("qos_policy_id", "") or "",
                "port_id": object_json.get("port_id", "") or "",
                "updated_at": object_json.get("updated_at", "") or "",
            },
        ).to_dict()

    def format_security_group(self, object_json, **kwargs):
        """
        安全组格式转换
        """
        return SecurityGroup(
            cloud_type=self.cloud_type,
            resource_id=object_json.get("id"),
            resource_name=object_json.get("name", "未命名"),
            desc=object_json.get("description", "") or "",
            tag=[],
            extra={},
            is_default=False,
            create_time=handle_time_str(object_json.get("create_at", "")),
            resource_group="",
            vpc="",
            project=self.project_id,
            zone="",
            region=kwargs.get("region", ""),
        ).to_dict()

    def format_security_group_rule(self, object_json, **kwargs):
        """
        安全组规则格式转换
        """
        direction_map = {"ingress": "INGRESS", "egress": "EGRESS"}
        return SecurityGroupRule(
            cloud_type=self.cloud_type,
            resource_id=object_json.get("id"),
            resource_name=object_json.get("name", "未命名"),
            desc=object_json.get("description", "") or "",
            tag=[],
            extra={},
            direction=direction_map.get(object_json["direction"], object_json["direction"]),
            dest_cidr=object_json.get("remote_ip_prefix", "ANY"),
            dest_group_id="",
            source_cidr="",
            source_group_id="",  # 源安全组id
            create_time=handle_time_str(object_json.get("create_at", "")),
            modify_time="",
            nic_type="",
            protocol=object_json["protocol"] if object_json.get("protocol") else "ALL",
            port_range=[object_json.get("port_range_min", ""), object_json.get("port_range_max", "")],
            priority="",
            security_group=object_json.get("security_group_id"),
            action="ACCEPT",
            project=self.project_id,
            zone="",
            region=kwargs.get("region", ""),
        ).to_dict()

    def format_volume_type(self, object_json, **kwargs):
        return FusionCloudDiskType(
            extra={
                "volume_backend_name": object_json.get("volume_backend_name"),
                "availability-zone": object_json.get("availability-zone"),
            },
            cloud_type=self.cloud_type,
            resource_name=object_json.get("name", "未命名"),
            qos_specs_id=object_json.get("qos_specs_id", ""),
            resource_id=object_json.get("id"),
            is_public=object_json.get("is_public", True),
            desc=object_json.get("description", "") or "",
            project=self.project_id,
            region=kwargs.get("region", ""),
        ).to_dict()

    def format_rule(self, object_json, **kwargs):
        if object_json["listener_id"] in kwargs["listener_ids"]:
            return RelayRule(
                url=object_json.get("redirect_url", "") or "",
                domain=object_json.get("Domain", ""),
                server_group=object_json.get("redirect_pool_id"),
                load_balancer=kwargs.get("load_balancer", ""),
                cloud_type=self.cloud_type,
                region=kwargs.get("region"),
                # zone=object_json.get("ZoneId", self.zone_id),
                resource_id=object_json.get("id", ""),
                resource_name=object_json.get("name", "未命名"),
                desc=object_json.get("description", "") or "",
                # port=kwargs.get("ListenerPort"),
                # protocal=kwargs.get("ListenerProtocol", ""),
                extra={
                    "listener_id": object_json.get("listener_id"),
                    "redirect_pool_id": object_json.get("redirect_pool_id"),
                },
            ).to_dict()

    def format_load_balancer(self, object_json, **kwargs):
        return LoadBalancer(
            desc=object_json.get("description") or "",
            resource_id=object_json.get("id"),
            resource_name=object_json.get("name"),
            lb_type=0,
            # project=obj.get("tenant_id"),
            status=True if object_json.get("operating_status") == "ONLINE" else False,
            # create_time=object_json.get("created_at")[:19].replace("T", " "),
            # status_time=object_json.get("updated_at")[:19].replace("T", " "),
            vips=[object_json.get("vip_address")],
            cloud_type=self.cloud_type,
            region=kwargs.get("region"),
            extra={
                "tenant_id": object_json.get("tenant_id"),
                "vip_subnet_id": object_json.get("vip_subnet_id"),
                "vip_port_id": object_json.get("vip_port_id"),
                "provisioning_status": object_json.get("provisioning_status"),
                "pools": [i["id"] for i in object_json.get("pools", [])],
                "listener_ids": [i["id"] for i in object_json.get("listeners", [])],
            },
        ).to_dict()

    def format_pool(self, object_json, **kwargs):
        """后端服务器组"""
        backend_servers_list = [item["id"] for item in object_json.get("members", [])]
        load_balancer_list = [item["id"] for item in object_json.get("loadbalancers", [])]
        listen_list = [item["id"] for item in object_json.get("listeners", [])]
        return VServerGroup(
            backend_servers=backend_servers_list,
            load_balancer=load_balancer_list,
            listens=listen_list,
            rules=[],
            resource_id=object_json["id"],
            resource_name=object_json["name"],
            desc=object_json["description"] or "",
            cloud_type=self.cloud_type,
            project=self.project_id,
            region=kwargs.get("region", ""),
        ).to_dict()

    def format_number(self, object_json, **kwargs):
        """后端服务器"""
        return VM(
            uuid=object_json.get("id"),
            resource_id=object_json.get("id"),
            resource_name=object_json.get("name"),
            public_ip=object_json.get("address"),
            subnet=object_json.get("subnet_id"),
            cloud_type=self.cloud_type,
            project=self.project_id,
            region=kwargs.get("region", ""),
            extra={"protocol_port": object_json.get("protocol_port"), "weight": object_json.get("weight")},
        ).to_dict()

    def format_listener(self, object_json, **kwargs):
        return LoadBalancerListener(
            status="RUNNING",
            backend_version=object_json.get("protocol").lower(),
            backend_port=object_json.get("protocol_port"),
            front_version=object_json.get("protocol").lower(),
            front_port=object_json.get("protocol_port"),
            desc=object_json.get("description") or "",
            resource_id=object_json.get("id"),
            resource_name=object_json.get("name"),
            load_balancer=object_json.get("loadbalancers")[0].get("id", "") if object_json.get("loadbalancers") else "",
            cloud_type=self.cloud_type,
            region=kwargs.get("region", self.region_id),
            extra={"default_pool_id": object_json.get("default_pool_id")},
        ).to_dict()

    def format_router(self, object_json, **kwargs):
        status = "AVAILABLE" if object_json.get("status") == "ACTIVE" else "ERROR"
        # nexthop = object_json.get('routes')[0]['nexthop'] if object_json.get('routes') else ""
        nexthop = object_json.get("route_info", {}).get("nexthop")
        cidr_block = object_json.get("route_info", {}).get("destination")
        # nexthops = {"NextHop": [{"NextHopId": "", "NextHopType": "service", "NextHopRelatedInfo": {}}]}
        return RouteEntry(
            resource_id=object_json.get("id") + nexthop,
            resource_name=object_json.get("name") + nexthop,
            status=status,
            desc=object_json.get("description") or "",
            next_hops={"nexthop": nexthop},
            cidr_block=cidr_block,
            create_time=object_json.get("created_at"),
            cloud_type=self.cloud_type,
            region=kwargs.get("region_id"),
            extra={"vpc": object_json.get("id")},
        ).to_dict()

    def format_bucket(self, item, size, obj_list):
        return Bucket(
            resource_id=item.name,
            resource_name=item.name,
            region=item.location,
            extra={"size": size, "obj_list": obj_list},
            create_time=item.create_date,
            cloud_type="FusionCloud",
        ).to_dict()

    def format_bucket_file(self, file_object, **kwargs):
        bucket = kwargs.pop("bucket")
        return BucketFile(
            modify_time=file_object.lastModified,
            size=file_object.size or file_object.get("dir_size", 0),
            file_type=file_object.get("type"),
            parent=file_object.get("parent", "/"),
            bucket=bucket,
            resource_id="{}<>{}".format(bucket, file_object.key),
            cloud_type="FusionCloud",
            extra={"location": kwargs.get("location", "")},
        ).to_dict()

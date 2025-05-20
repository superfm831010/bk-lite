from common.cmp.cloud_apis.cloud_constant import DiskCategory, DiskStatus, ImageStatus, ImageType, VPCStatus
from common.cmp.cloud_apis.cloud_object.base import (
    VM,
    VPC,
    Disk,
    Image,
    LoadBalancer,
    LoadBalancerListener,
    Mariadb,
    Redis,
    Region,
    SecurityGroup,
    SecurityGroupRule,
    Subnet,
    Zone,
)
from common.cmp.cloud_apis.constant import VMStatusType
from common.cmp.cloud_apis.resource_apis.resource_format.common.common_format import FormatResource
from common.cmp.cloud_apis.resource_apis.resource_format.qingcloud.qingcloud_constant import QingCloudDiskStatus
from common.cmp.cloud_apis.resource_apis.utils import handle_time_str


def handle_vm_status(status):
    vm_status_map = {
        "running": VMStatusType.RUNNING.value,
        "pending": VMStatusType.PENDING.value,
        "stopped": VMStatusType.STOP.value,
    }
    return vm_status_map.get(status, VMStatusType.PENDING.value)


def handle_disk_status(status):
    status_map = {
        QingCloudDiskStatus.AVAILABLE.value: DiskStatus.UNATTACHED.value,
        QingCloudDiskStatus.RUNNING.value: DiskStatus.ATTACHED.value,
        QingCloudDiskStatus.PENDING.value: DiskStatus.PENDING.value,
    }
    return status_map.get(status, DiskStatus.ERROR.value)


def handle_vpc_status(status):
    vpc_status_map = {
        "pending": VPCStatus.PENDING.value,
        "active": VPCStatus.AVAILABLE.value,
    }
    return vpc_status_map.get(status, VPCStatus.ERROR.value)


def handle_loadbalancer_status(status):
    return True if status == "active" else False


def handle_region_status(status):
    return "AVAILABLE" if status == "active" else "UNAVAILABLE"


def handle_region_name(region_id):
    region_name_dict = {"pek3": "北京三区", "gd2": "广东二区", "sh1": "上海一区", "jinan1": "济南一区", "ap3": "亚太三区"}
    return region_name_dict.get(region_id, region_id)


def handle_image_status(status):
    image_status_map = {
        "available": ImageStatus.AVAILABLE.value,
        "pending": ImageStatus.CREATING.value,
    }
    return image_status_map.get(status, ImageStatus.UNAVAILABLE.value)


def handle_image_type(visibility):
    return ImageType.PUBLIC.value if visibility == "public" else ImageType.PRIVATE.value


def handle_redis_status(status):
    redis_status_map = {"active": 2, "deleted": -3, "ceased": 2, "stopped": 2}
    return redis_status_map.get(status, 0)


def handle_mysql_status(status):
    mysql_status_map = {
        "active": 2,
        "deleted": -2,
    }
    return mysql_status_map.get(status, 0)


class QingCloudFormatResource(FormatResource):
    def __init__(self, region_id="", project_id="", cloud_type=""):
        self.region_id = region_id
        self.project_id = project_id
        self.cloud_type = cloud_type

    def __new__(cls, *args, **kwargs):
        return super(QingCloudFormatResource, cls).__new__(cls, *args, **kwargs)

    def format_vm(self, object_json, **kwargs):
        """
        虚拟机格式转换
        """

        return VM(
            cloud_type=self.cloud_type,
            resource_id=object_json.get("instance_id"),
            resource_name=object_json.get("instance_name", "未命名") or "未命名",
            desc=object_json.get("description") or "",
            instance_type=object_json.get("instance_type"),
            vcpus=object_json.get("vcpus_current"),
            memory=object_json.get("memory_current"),
            image=object_json["image"].get("image_id"),
            # public_ip=(object_json.get("eip"))['eip_addr'],
            status=handle_vm_status(object_json.get("status")),
            inner_ip="",
            system_disk={},
            data_disk=object_json.get("os-extended-volumes:volumes_attached", []),
            internet_accessible={},
            security_group=object_json.get("security_group", []),  #
            project=self.project_id,
            zone=object_json.get("zone_id", ""),
            region=self.region_id,
            create_time=handle_time_str(object_json["create_time"]),
            expired_time="",
        ).to_dict()

    def format_disk(self, object_json, **kwargs):
        return Disk(
            resource_id=object_json.get("volume_id", ""),
            resource_name=object_json.get("volume_name", "未命名") or "未命名",
            desc=object_json.get("description", "") or "",
            disk_size=object_json.get("size", ""),
            status=handle_disk_status(object_json.get("status", "")),
            create_time=handle_time_str(object_json["create_time"]),
            server_id=object_json.get("instance", "").get("instance_id"),
            category=DiskCategory.CLOUD_BASIC.value,
            cloud_type=self.cloud_type,
            disk_type="DATA_DISK",
            zone=object_json.get("zone_id"),
        ).to_dict()

    def format_vpc(self, object_json, **kwargs):
        return VPC(
            resource_id=object_json.get("router_id", "") or "",
            resource_name=object_json.get("router_name", ""),
            desc=object_json.get("description", "") or "",
            status=handle_vpc_status(object_json.get("status", "")),
            cloud_type=self.cloud_type,
            router_tables=[],
            project=self.project_id,
            region=self.region_id,
        ).to_dict()

    def format_subnet(self, object_json, **kwargs):
        return Subnet(
            resource_id=object_json.get("vxnet_id"),
            resource_name=object_json.get("vxnet_name", "未命名"),
            vpc=object_json.get("vpc_router_id"),
            cloud_type=self.cloud_type,
            create_time=handle_time_str(object_json["create_time"]),
            desc=object_json.get("description", "") or "",
            region=self.region_id,
            zone=object_json.get("region_id", "") or "",
        ).to_dict()

    def format_security_group(self, object_json, **kwargs):
        return SecurityGroup(
            resource_id=object_json.get("security_group_id"),
            resource_name=object_json.get("security_group_name") or "未命名",
            cloud_type=self.cloud_type,
            desc=object_json.get("description") or "",
            is_default=object_json.get("is_default"),
            create_time=handle_time_str(object_json["create_time"]),
            region=self.region_id,
        ).to_dict()

    def format_security_group_rule(self, object_json, **kwargs):
        return SecurityGroupRule(
            resource_id=object_json.get("security_group_rule_id"),
            cloud_type=self.cloud_type,
            priority=object_json.get("priority"),
            security_group=object_json.get("security_group_id") or kwargs["security_group_id"],
            action=object_json.get("action"),
            region=self.region_id,
        ).to_dict()

    def format_load_balancer(self, object_json, **kwargs):
        return LoadBalancer(
            cloud_type=self.cloud_type,
            resource_id=object_json.get("loadbalancer_id"),
            resource_name=object_json.get("loadbalancer_name"),
            desc=object_json.get("description") or "",
            status=handle_loadbalancer_status(object_json.get("status")),
            create_time=handle_time_str(object_json["create_time"]),
            status_time=object_json.get("status_time"),
            region=self.region_id,
        ).to_dict()

    def format_listener(self, object_json, **kwargs):
        return LoadBalancerListener(
            create_time=handle_time_str(object_json["create_time"]),
            cloud_type=self.cloud_type,
            region=self.region_id,
            resource_id=object_json.get("loadbalancer_listener_id"),
            resource_name=object_json.get("loadbalancer_listener_name"),
        ).to_dict()

    def format_region(self, object_json, **kwargs):
        return Region(
            cloud_type=self.cloud_type,
            resource_id=object_json.get("region_id", object_json.get("zone_id")) or "",
            resource_name=handle_region_name(object_json.get("region_id", object_json.get("zone_id"))) or "",
            status=handle_region_status(object_json.get("status")) or "",
        ).to_dict()

    def format_zone(self, object_json, **kwargs):
        return Zone(
            cloud_type=self.cloud_type,
            resource_id=object_json.get("zone_id"),
            region=object_json.get("region_id", self.region_id),
            resource_name=handle_region_name(object_json.get("region_id", self.region_id)),
            status=handle_region_status(object_json.get("status")),
        ).to_dict()

    def format_redis(self, object_json, **kwargs):
        return Redis(
            cloud_type=self.cloud_type,
            resource_id=object_json.get("cluster_id"),
            resource_name=object_json.get("name"),
            vpc=object_json.get("vxnet")["vxnet_id"],
            create_time=handle_time_str(object_json["create_time"]),
            instance_type=1,
            product_type="cluster28",
            status=handle_redis_status(object_json.get("status")),
        ).to_dict()

    def format_mysql(self, object_json, **kwargs):
        return Mariadb(
            cloud_type=self.cloud_type,
            resource_id=object_json.get("cluster_id"),
            resource_name=object_json.get("name"),
            vpc=object_json.get("vxnet")["vxnet_id"],
            create_time=handle_time_str(object_json["create_time"]),
            memory=object_json.get("cpu_asgn"),
            storage=object_json.get("storage_asgn"),
            region=object_json.get("zone_id"),
            status=handle_mysql_status(object_json.get("status")),
        ).to_dict()

    def format_image(self, object_json, **kwargs):
        return Image(
            cloud_type=self.cloud_type,
            size=object_json.get("size"),
            resource_id=object_json.get("image_id"),
            resource_name=object_json.get("image_name"),
            desc=object_json.get("description") or "",
            os_type=object_json.get("platform"),
            create_time=handle_time_str(object_json["create_time"]),
            status=handle_image_status(object_json.get("status")),
            image_type=handle_image_type(object_json.get("visibility")),
        ).to_dict()

# -*- coding: utf-8 -*-
import json

from common.cmp.cloud_apis.cloud_constant import VMChargeType
from common.cmp.cloud_apis.cloud_object.base import VM
from common.cmp.cloud_apis.resource_apis.resource_format.common.common_format import FormatResource
from common.cmp.cloud_apis.resource_apis.resource_format.openstack.openstack_format_utils import handle_vm_status


class EasyStackFormatResource(FormatResource):
    def __init__(self, region_id="", project_id="", cloud_type=""):
        self.region_id = region_id
        self.project_id = project_id
        self.cloud_type = cloud_type

    def __new__(cls, *args, **kwargs):
        return super(EasyStackFormatResource, cls).__new__(cls, *args, **kwargs)

    def format_vm(self, object_json, **kwargs):
        """
        虚拟机格式转换
        """
        if isinstance(object_json, str):
            object_json = json.loads(object_json)
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
                    out_ip_list.append(n.get("addr", ""))
            nic_list.append(nic_obj)
        mem = 0
        vcpus = 0
        vm_config = object_json.get("metadata").get("cascaded.instance_extrainfo", "").split(",")
        for i in vm_config:
            detail = i.split(":")
            if detail[0] == "current_mem":
                mem = int(detail[1])
            if detail[0] == "current_cpu":
                vcpus = int(detail[1])
        return VM(
            cloud_type=self.cloud_type,
            resource_id=object_json.get("id"),
            resource_name=object_json.get("name"),
            uuid="",
            desc="",
            instance_type=flavor_id,
            vcpus=vcpus,
            memory=mem,  # "OS-EXT-SRV-ATTR:ramdisk_id": ""
            image=image_id,
            os_name="",
            status=handle_vm_status(object_json.get("status")),
            inner_ip=inner_ip_list,  # "accessIPv4"
            public_ip=out_ip_list,  #
            system_disk={},
            data_disk=object_json.get("os-extended-volumes:volumes_attached", []),
            charge_type=VMChargeType.UNKNOWN.value,
            internet_accessible={},
            vpc="",
            subnet="",
            security_group=object_json.get("security_groups", []),  #
            project=self.project_id,
            zone=object_json.get("OS-EXT-AZ:availability_zone", ""),
            region=self.region_id,
            login_settings={},
            create_time=object_json["created"][:19].replace("T", " "),  #
            expired_time="",
            peak_period=None,
            tag=[],
            extra={"security_group_name": object_json.get("security_groups", [])},  # 目前只能获取到安全组name列表
        ).to_dict()

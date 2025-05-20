# -*- coding: utf-8 -*-
import json

from common.cmp.cloud_apis.cloud_constant import VMStatus
from common.cmp.cloud_apis.cloud_object.base import VM
from common.cmp.cloud_apis.resource_apis.resource_format.common.common_format import FormatResource


class CasFormatResource(FormatResource):
    def __init__(self, region_id="", project_id="", cloud_type=""):
        self.region_id = region_id
        self.project_id = project_id
        self.cloud_type = cloud_type

    def __new__(cls, *args, **kwargs):
        return super(CasFormatResource, cls).__new__(cls, *args, **kwargs)

    @staticmethod
    def handle_vm_status(status):
        """虚拟机状态处理"""
        vm_status_dict = {
            "running": VMStatus.RUNNING.value,
            "shutOff": VMStatus.STOP.value,
        }
        return vm_status_dict.get(status, VMStatus.BUILD.value)

    def format_vm(self, object_json, **kwargs):
        """
        虚拟机格式转换
        """
        if isinstance(object_json, str):
            object_json = json.loads(object_json)

        system = object_json.get("system")
        system_map = {
            "0": "Windows",
            "1": "Linux",
            "2": "BSD",
        }
        os_system = system_map.get(str(system))
        if isinstance(object_json.get("ipv4Attribute", {}).get("ipv4"), dict):
            ip = object_json.get("ipv4Attribute", {}).get("ipv4", {}).get("ipAddress")
        else:
            ip_list = object_json.get("ipv4Attribute", {}).get("ipv4")
            ip = ip_list[0].get("ipAddress") if ip_list else ""
        inner_ip_list = [ip] if ip else []
        out_ip_list = []
        return VM(
            cloud_type=self.cloud_type,
            resource_id=object_json.get("id"),
            resource_name=object_json.get("name"),
            uuid=object_json.get("uuid"),
            desc=object_json.get("description"),
            instance_type="",
            vcpus=object_json.get("cpu"),
            memory=object_json.get("memory"),
            image="",
            os_name=os_system,
            status=self.handle_vm_status(object_json["vmStatus"]),
            inner_ip=inner_ip_list,  # "accessIPv4"
            public_ip=out_ip_list,  # 没找到
            system_disk={},  # 不确定
            data_disk=[],  # 不确定
            charge_type="",  # 无
            internet_accessible="",  # 没转换
            vpc=object_json.get("network", {}).get("vsName"),
            subnet="",
            security_group="",  # 没找到
            project=self.project_id,
            zone="",
            region=self.region_id,
            login_settings={},
            create_time=object_json["createDate"][:10].replace("T", " "),  #
            expired_time="",
            peak_period=None,
            tag=[],
            extra={},
        ).to_dict()

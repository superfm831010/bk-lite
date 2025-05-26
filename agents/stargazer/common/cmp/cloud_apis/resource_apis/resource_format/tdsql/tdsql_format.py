# -*- coding: utf-8 -*-
"""TDSQL数据格式转换"""
import threading

from common.cmp.cloud_apis.cloud_object.base import TDSQL

# from common.cmp.cloud_apis.resource_apis.constant import VmwareVirtualMachineStatus
from common.cmp.cloud_apis.resource_apis.resource_format.tdsql.tdsql_format_utils import (
    format_instance_status,
    format_readonly_status,
)


class TDSQLResourceFormat:
    _instance_lock = threading.Lock()

    def __init__(self, account_id="", cloud_type="", region_id=""):
        self.account_id = account_id
        self.cloud_type = cloud_type
        self.region_id = region_id

    def get_sync_tpye(self, sync_num):
        """
        同步异步类型
        """
        if sync_num == 0:
            return "异步"
        elif sync_num == 1:
            return "强同步"
        elif sync_num == 2:
            return "跨IDC强同步"
        else:
            return "未知"

    def get_instance_status(self, status):
        """
        实例状态
        """
        if status == 0:
            return "运行中"
        elif status == 1:
            return "已隔离"
        elif status == 2:
            return "未初始化"
        else:
            return "未知"

    def format_noshard_instance(self, object_json, **kwargs):
        if not object_json:
            return None

        instance_info = object_json.get("tdsql")
        detail_info = {
            "fenceid": instance_info.get("fenceid", None),
            "set_id": instance_info.get("id"),
            "set_status": self.get_instance_status(instance_info.get("status")),
            "cpu": "%.1f" % (float(instance_info["cpu"]) / 100),
            "memory": "%.2f" % (float(instance_info["memory"]) / 1024),
            "log_disk": "%.2f" % (float(instance_info["log_disk"]) / 1024),
            "data_disk": "%.2f" % (float(instance_info["data_disk"]) / 1024),
            "cluster_name": instance_info["cluster_name"],
            "db": instance_info["db"],
            "is_degrade": instance_info["degrade_flag"] == 1,
            "machine": instance_info["machine"],
            "is_dumper": instance_info["mydumper"] == 1,
            "read_only": format_readonly_status(instance_info["read_only"]),
            "is_xtrabackup": instance_info["xtrabackup"] == "1",
            "user": instance_info["user"],
            "pwd": instance_info["pwd"],
            "dctokafka": instance_info.get("dctokafka") == 1,
            "node_num": "1主{}备".format(instance_info["nodeNum"] - 1),
            "sync_type": self.get_sync_tpye(instance_info["sqlasyn"]),
            "master_zone": instance_info.get("master_zone"),
            "slave_zones": instance_info.get("slave_zones"),
            "xtrabackup": instance_info.get("xtrabackup"),
            "mydumper": instance_info.get("mydumper"),
            "sbackuptime": instance_info.get("sbackuptime"),
            "ebackuptime": instance_info.get("ebackuptime"),
        }

        return TDSQL(
            cloud_type=self.cloud_type,
            resource_id=object_json["set_name"],
            resource_name=object_json["set_name"],
            instance_type="NOSHARD",
            status=format_instance_status(instance_info["status"]),
            # memory="%.2f" % (float(instance_info["memory"]) / 1024),
            shard_count=0,
            version=object_json["version"],
            node_count=instance_info["nodeNum"],
            excluster_id="" if instance_info["fenceid"] == "none" else instance_info["fenceid"],
            shard_detail=[detail_info],
            extra={
                "proxy_group": object_json.get("group_id"),
                "proxy_host": object_json.get("proxy_host"),
                "proxy_port": object_json.get("proxy_port"),
                "dctokafka": object_json.get("dctokafka"),
                "available_proxy_host": object_json.get("available_proxy_host"),
            },
        ).to_dict()

    def format_group_instance(self, object_json, **kwargs):
        if not object_json:
            return None

        set_info = object_json.get("instances", [])
        shared_list = []
        for instance_info in set_info:
            shared_list.append(
                {
                    "fenceid": instance_info.get("fenceid", None),
                    "set_id": instance_info.get("id"),
                    "set_status": self.get_instance_status(instance_info.get("status")),
                    "cpu": "%.1f" % (float(instance_info["cpu"]) / 100),
                    "memory": "%.2f" % (float(instance_info["memory"]) / 1024),
                    "log_disk": "%.2f" % (float(instance_info["log_disk"]) / 1024),
                    "data_disk": "%.2f" % (float(instance_info["data_disk"]) / 1024),
                    "cluster_name": instance_info["cluster_name"],
                    "db": instance_info["db"],
                    "is_degrade": instance_info["degrade_flag"] == 1,
                    "machine": instance_info["machine"],
                    "is_dumper": instance_info["mydumper"] == 1,
                    "read_only": format_readonly_status(instance_info["read_only"]),
                    "is_xtrabackup": instance_info["xtrabackup"] == "1",
                    "user": instance_info["user"],
                    "pwd": instance_info["pwd"],
                    "dctokafka": instance_info.get("dctokafka") == 1,
                    "node_num": "1主{}备".format(instance_info["nodeNum"] - 1),
                    "sync_type": self.get_sync_tpye(instance_info["sqlasyn"]),
                    "master_zone": instance_info.get("master_zone"),
                    "slave_zones": instance_info.get("slave_zones"),
                    "xtrabackup": instance_info.get("xtrabackup"),
                    "mydumper": instance_info.get("mydumper"),
                    "sbackuptime": instance_info.get("sbackuptime"),
                    "ebackuptime": instance_info.get("ebackuptime"),
                }
            )

        return TDSQL(
            cloud_type=self.cloud_type,
            resource_id=object_json["groupid"],
            resource_name=object_json["groupid"],
            instance_type="GROUP",
            status=format_instance_status(object_json["status"]),
            # memory="%.2f" % (float(instance_info["memory"]) / 1024),
            shard_count=object_json.get("total_slice", -1),
            version=object_json.get("version", "N/A"),
            node_count=len(set_info),
            excluster_id="" if object_json["fenceid"] == "none" else object_json["fenceid"],
            shard_detail=shared_list,
            extra={
                "proxy_host": object_json.get("proxy_host"),
                "proxy_port": object_json.get("proxy_port"),
                "dctokafka": object_json.get("dctokafka"),
                "available_proxy_host": object_json.get("available_proxy_host"),
            },
        ).to_dict()

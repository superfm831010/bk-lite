# -*- coding: utf-8 -*-
# @File：qcloud_info.py.py
# @Time：2025/6/16 15:14
# @Author：bennie
import logging
from functools import cached_property

from tencentcloud.common import credential
from tencentcloud.common.common_client import CommonClient
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from typing import List, Dict

from plugins.base import BasePlugin
from plugins.base_utils import convert_to_prometheus_format
from plugins.constains import client_version_map, mysql_pay_type_map, redis_region_map, mongodb_status_map, \
    pgsql_status_map, pulsar_status_map, pgsql_pay_type_map, mysql_status_map, redis_status_map, redis_sub_status_map, \
    redis_type_map, mongodb_inst_type_map, mongodb_pay_type_map, pulsar_pay_type_map, cmq_status_map, \
    cmq_topic_status_map, cmq_topic_filter_type_map, clb_status_map, clb_net_type_map, clb_isp_map, clb_pay_type_map, \
    eip_status_map, eip_res_type_map, eip_isp_map, cfs_status_map, cfs_storage_type_map, domain_status_map, \
    eip_type_map, eip_pay_type_map
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

logger = logging.getLogger(__name__)


class TencentClientProxy(object):
    """
    腾讯云客户端代理类（非网络代理）
    """

    def __init__(self, credential: credential.Credential, region: str, profile: ClientProfile):
        self.credential = credential
        self.region = region
        self.profile = profile

    def get_client(self, service_name, version=None):
        if version is None:
            version = client_version_map.get(service_name)
            assert version is not None, "version is not supported"
        assert service_name in client_version_map, "service_name is not supported"
        return CommonClient(service_name, version, self.credential, self.region, self.profile)

    def __getattr__(self, item):
        # 支持client_xxmethod格式的直接调用
        if '_' in item:
            parts = item.split('_', 1)
            if len(parts) == 2:
                service_name, method_name = parts
                client = self.get_client(service_name)
                return getattr(client, method_name)
        # 支持client.xxmethod的链式调用
        return self.get_client(item)


class TencentCloudManager(BasePlugin):
    def __init__(self, params: dict):
        # 需要提供有全面只读权限的云账号，并允许进行编程访问
        self.params = params
        self.secret_id = params.get("secret_id")
        self.secret_key = params.get("secret_key")
        ssl = params.get("ssl", "false")
        self.protocol = "https" if ssl.lower() == "true" else "http"

    def get_tencent_client(self, region="ap-guangzhou") -> TencentClientProxy:
        """
        params:
            region: 地域
        return: TencentClientProxy
        """
        httpProfile = HttpProfile()
        httpProfile.protocol = self.protocol
        client_profile = ClientProfile()
        client_profile.httpProfile = httpProfile
        cred = self.get_credentials()
        return TencentClientProxy(credential=cred, region=region, profile=client_profile)

    def get_tencent_cos_client(self, region):
        return CosS3Client(CosConfig(SecretId=self.secret_id, SecretKey=self.secret_key, Region=region))

    def get_credentials(self) -> credential.Credential:
        return credential.Credential(self.secret_id, self.secret_key)

    def get_qcloud(self) -> List[Dict]:
        organization_api_info = self.get_tencent_client("").organization.call_json("DescribeOrganization", {})
        organization_info = organization_api_info.get("Response", {})

        return [{"inst_name": f"{organization_info.get('NickName', '')}_{organization_info.get('OrgId')}",
                 "organization": organization_info.get("NickName", "")}]

    def get_qcloud_region(self) -> List[Dict]:
        """获取腾讯云区域信息"""
        return self.get_tencent_client(region="").cvm.call_json("DescribeRegions", {}).get("Response", {}).get(
            "RegionSet", [])

    def get_qcloud_zones(self, region) -> List[Dict]:
        """获取腾讯云可用区信息"""
        return self.get_tencent_client(region=region).cvm.call_json("DescribeZones", {}).get("Response", {}).get(
            "ZoneSet", [])

    @cached_property
    def available_region_list(self):
        return [region.get("Region") for region in self.get_qcloud_region() if region.get("RegionState") == "AVAILABLE"]

    @cached_property
    def zone_id_zone_map(self) -> Dict:
        """获取腾讯云可用区信息"""
        result = {}
        for region in self.available_region_list:
            for zone in self.get_qcloud_zones(region):
                result[zone.get("ZoneId")] = zone.get("Zone")
        return result

    def get_qcloud_cvm(self) -> List[Dict]:
        """获取所有区域的CVM的资源名、资源ID、内网IP、公网IP、地域、可用区、VPC、状态、规格、操作系统名称、vCPU数、内存容量(MB)、付费类型
        doc: https://cloud.tencent.com/document/api/213/15753#Instance
        """
        result = []
        for region in self.available_region_list:
            cvm_info = self.get_tencent_client(region=region).cvm.call_json("DescribeInstances", {})
            instances = cvm_info.get("Response", {}).get("InstanceSet", [])
            result.extend([{
                "inst_name": instance.get("InstanceName"),
                "inst_id": instance.get("InstanceId"),
                "inner_ip": instance.get("PrivateIpAddresses") or [],  # 内网IP
                "outer_ip": instance.get("PublicIpAddresses") or [],  # 公网IP
                "region": region,  # 地域
                "zone": instance.get("Placement", {}).get("Zone"),  # 可用区
                "vpc": instance.get("VirtualPrivateCloud", {}),  # 虚拟私有网 VPC
                "status": instance.get("InstanceState"),  # 状态
                "spec": instance.get("InstanceType"),  # 规格
                "os_name": instance.get("OsName"),
                "vcpu": instance.get("CPU"),  # vCPU数" 核
                "memory": instance.get("Memory", 0) * 1024,  # 内存容量(MB)
                "pay_type": instance.get("InstanceChargeType"),
            } for instance in instances])

        return result

    def get_qcloud_rocketmq(self) -> List[Dict]:
        """资源名、资源ID、地域、可用区、状态、Topic 总数量、已用Topic 数量、集群 TPS 数量、命名空间数量、Group 数量"""
        result = []
        for region in self.available_region_list:
            rocketmq_info = self.get_tencent_client(region=region).tdmq.call_json("DescribeRocketMQClusters", {})
            clusters = rocketmq_info.get("Response", {}).get("ClusterList", [])
            result.extend([{
                "inst_name": cluster.get("Info", {}).get("ClusterName"),
                "inst_id": cluster.get("Info", {}).get("ClusterId"),
                "region": region,  # 地域
                "zone": self.zone_id_zone_map.get(cluster.get("Info").get("ZoneId")),
                "status": cluster.get("Status"),
                "topic_total": cluster.get("Config").get("MaxTopicNum"),  # Topic 总数量
                "topic_used": cluster.get("Config").get("UsedTopicNum"),
                "tps_total": cluster.get("Config").get("MaxTpsLimit"),  # 集群 TPS 数量
                "ns_total": cluster.get("Config").get("MaxNamespaceNum"),  # 命名空间数量
                "ns_used": cluster.get("Config").get("UsedNamespaceNum"),  # 已用命名空间数量"
                "group_total": cluster.get("Config").get("MaxGroupNum"),  # Group 数量
                "group_used": cluster.get("Config").get("UsedGroupNum"),  # 已用Group 数量
            } for cluster in clusters])
        return result

    def get_qcloud_mysql(self):
        """资源名、资源ID、IP、地域、可用区、状态、硬盘大小(GB)、内存容量(MB)、付费类型"""
        result = []
        for region in self.available_region_list:
            mysql_info = self.get_tencent_client(region=region).cdb.call_json("DescribeDBInstances", {})
            instances = mysql_info.get("Response", {}).get("Items", [])
            result.extend([{
                "inst_name": instance.get("InstanceName"),
                "inst_id": instance.get("InstanceId"),
                "ip": instance.get("Vip"),
                "region": region,  # 地域
                "zone": instance.get("Zone"),
                "status": mysql_status_map.get(instance.get("Status"), "未知"),
                "disk": instance.get("Volume"),
                "memory": instance.get("Memory"),
                "pay_type": mysql_pay_type_map.get(instance.get("PayType"), "未知"),
            }] for instance in instances)
        return result

    def get_qcloud_redis_product_conf(self, region="ap-guangzhou"):
        """获取售卖的Redis产品信息,
        参数region即使指定具体地域，也返回所有地域的售卖信息。
        """
        product_info = self.get_tencent_client(region=region).redis.call_json("DescribeProductInfo", {})
        return product_info.get("Response", {}).get("RegionSet", [])

    def get_qcloud_redis(self):
        """资源名、资源ID、IP、VPC、地域、可用区、端口号、外网地址、实例状态、读写状态、
         产品版本、兼容版本、架构版本、内存容量(MB)、分片大小、分片数量、副本数量、最大连接数、最大网络吞吐(Mb/s)
        """

        result = []
        for region in self.available_region_list:
            redis_info = self.get_tencent_client(region=region).redis.call_json("DescribeInstances", {})
            instances = redis_info.get("Response", {}).get("InstanceSet", [])
            result.extend([{
                "inst_name": instance.get("InstanceName"),
                "inst_id": instance.get("InstanceId"),
                "ip": instance.get("WanIp"),
                "vpc": instance.get("VpcId"),
                "region": redis_region_map.get(instance.get("RegionId")),  # 地域
                "zone": self.zone_id_zone_map.get(instance.get("ZoneId")),
                "port": instance.get("Port"),
                "outer_addr": instance.get("WanAddress"),  # 外网地址
                "status": redis_status_map.get(instance.get("Status"), "未知"),  # 实例状态
                "sub_status": redis_sub_status_map.get(instance.get("SubStatus"), "未知"),  # 流程中的实例返回的子状态
                "product_version": instance.get("ProductType"),  # 产品版本/产品类型
                "version": instance.get("CurrentRedisVersion"),  # 兼容版本
                "arch": redis_type_map.get(instance.get("Type")),  # 架构版本
                "memory": instance.get("Size"),
                "shard_size": instance.get("RedisShardSize"),  # 分片大小
                "shard_num": instance.get("RedisShardNum"),  # 分片数量
                "replica_num": instance.get("RedisReplicasNum"),  # 副本数量
                "max_conn": instance.get("ClientLimit"),  # 最大连接数
                "max_net": instance.get("NetLimit"),  # 最大网络吞吐(Mb/s)
            } for instance in instances])
        return result

    def get_qcloud_mongodb(self):
        """资源名、资源ID、IP、标签、项目ID、VPC、地域、可用区、端口号、实例状态、实例类型、配置类型、版本与引擎、实例CPU核数、
        实例内存规格(MB)、实例磁盘容量(MB)、实例从节点数、Mongod节点CPU核数、Mongod节点内存规格(MB)、Mongod节点数、付费类型"""
        result = []
        for region in self.available_region_list:
            mongodb_info = self.get_tencent_client(region=region).mongodb.call_json("DescribeDBInstances", {})
            instances = mongodb_info.get("Response", {}).get("InstanceDetails", [])
            result.extend([{
                "inst_name": instance.get("InstanceName"),
                "inst_id": instance.get("InstanceId"),
                "ip": instance.get("Vip"),
                "tags": instance.get("Tags"),
                "project_id": instance.get("ProjectId"),
                "vpc": instance.get("VpcId"),
                "region": instance.get("Region"),
                "zone": instance.get("Zone"),
                "port": instance.get("Vport"),
                "status": mongodb_status_map.get(instance.get("Status"), "未知"),
                "inst_type": mongodb_inst_type_map.get(instance.get("InstanceType"), "未知"),
                "machine_type": instance.get("MachineType"),  # 配置类型
                "version": instance.get("MongoVersion"),  # 版本与引擎
                "cpu": instance.get("CpuNum"),
                "memory": instance.get("Memory"),
                "disk": instance.get("Volume"),
                "slave_num": instance.get("SecondaryNum"),
                "mongo_cpu": instance.get("MongosCpuNum"),
                "mongo_memory": instance.get("MongosMemory"),
                "mongo_node_num": instance.get("MongosNodeNum"),
                "pay_type": mongodb_pay_type_map.get(instance.get("PayMode"), "未知"),
            } for instance in instances])
        return result

    def get_qcloud_pgsql(self):
        """
        资源名、资源ID、标签、项目ID、VPC、地域、可用区、实例状态、字符集、数据库引擎、架构、数据库版本、内核版本、
        实例CPU核数、实例内存规格(MB)、实例磁盘容量(MB)、付费类型
        """
        result = []
        for region in self.available_region_list:
            pgsql_info = self.get_tencent_client(region=region).postgres.call_json("DescribeDBInstances", {})
            instances = pgsql_info.get("Response", {}).get("DBInstanceSet", [])
            result.extend([{
                "inst_name": instance.get("DBInstanceName"),
                "inst_id": instance.get("DBInstanceId"),
                "tags": instance.get("TagList"),
                "project_id": instance.get("ProjectId"),
                "vpc": instance.get("VpcId"),
                "region": instance.get("Region"),
                "zone": instance.get("Zone"),
                "status": pgsql_status_map.get(instance.get("DBInstanceStatus"), "未知"),
                "charset": instance.get("DBCharset"),  # 字符集
                "engine": instance.get("DBEngine"),
                "arch": instance.get("DBInstanceType"),
                "version": instance.get("DBVersion"),
                "kernel_version": instance.get("DBKernelVersion"),
                "cpu": instance.get("DBInstanceCpu"),
                "memory": instance.get("DBInstanceMemory"),
                "disk": instance.get("DBInstanceStorage"),
                "pay_type": pgsql_pay_type_map.get(instance.get("PayType"), "未知"),
            } for instance in instances])
        return result

    def get_qcloud_pulsar_cluster(self):
        """资源名、资源ID、标签、项目ID、地域、状态、版本、内网接入地址、公网接入地址、最大命名空间数、最大Topic数、
        最大QPS、最大消息保留时间(s)、最大存储容量(MB)、最长消息延迟(s)、付费类型"""
        result = []
        for region in self.available_region_list:
            pulsar_info = self.get_tencent_client(region=region).tdmq.call_json("DescribeClusters", {})
            instances = pulsar_info.get("Response", {}).get("Instances", [])
            result.extend([{
                "inst_name": instance.get("ClusterName"),
                "inst_id": instance.get("ClusterId"),
                "tags": instance.get("Tags"),
                "project_id": instance.get("ProjectId"),
                "region": region,
                "status": pulsar_status_map.get(instance.get("Status"), "未知"),
                "version": instance.get("Version"),
                "inner_addr": instance.get("VpcEndPoint"),  # 内网接入地址
                "outer_addr": instance.get("PublicEndPoint"),  # 公网接入地址
                "ns_total": instance.get("MaxNamespaceNum"),  # 最大命名空间数
                "topic_total": instance.get("MaxTopicNum"),  # 最大Topic数
                "qps": instance.get("MaxQps"),
                "msg_rtt": instance.get("MessageRetentionTime"),  # 最大消息保留时间(s)
                "storage": instance.get("MaxStorageCapacity"),
                "max_delay": instance.get("MaxMessageDelayInSeconds"),  # 最长消息延迟(s)
                "pay_type": pulsar_pay_type_map.get(instance.get("PayMode"), "未知"),
            } for instance in instances])
        return result

    def get_qcloud_cmq(self):
        """资源名、资源ID、标签、地域、状态、消息最大未确认时间(s)、消息接收长轮询等待时间(s)、取出消息隐藏时长(s)、消息最大长度(B)、QPS限制"""
        result = []
        for region in self.available_region_list:
            cmq_info = self.get_tencent_client(region=region).cmq.call_json("DescribeQueueDetail", {})
            instances = cmq_info.get("Response", {}).get("QueueSet", [])
            result.extend([{
                "inst_name": instance.get("QueueName"),
                "inst_id": instance.get("QueueId"),
                "tags": instance.get("Tags"),
                "region": region,
                "status": cmq_status_map.get(instance.get("Migrate"), "未知"),
                "max_unack_time": instance.get("msgRetentionSeconds"),  # 消息最大未确认时间(s)
                "msg_receive_wait": instance.get("PollingWaitSeconds"),  # 消息接收长轮询等待时间(s)
                "msg_hidden_time": instance.get("visibilityTimeout"),  # 取出消息隐藏时长(s)
                "msg_max_len": instance.get("maxMsgSize"),  # 消息最大长度(B)
                "qps": instance.get("Qps"),  # QPS限制
            } for instance in instances])
        return result

    def get_qcloud_cmq_topic(self):
        """资源名、资源ID、标签、地域、状态、消息生命周期、消息最大长度(B)、消息过滤类型、QPS限制"""
        result = []
        for region in self.available_region_list:
            topic_info = self.get_tencent_client(region=region).cmq.call_json("DescribeTopicDetail", {})
            instances = topic_info.get("Response", {}).get("TopicSet", [])
            result.extend([{
                "inst_name": instance.get("TopicName"),
                "inst_id": instance.get("TopicId"),
                "tags": instance.get("Tags"),
                "region": region,
                "status": cmq_topic_status_map.get(instance.get("Migrate"), "未知"),
                "msg_life": instance.get("MsgRetentionSeconds"),  # 消息生命周期
                "msg_max_len": instance.get("MaxMsgSize"),  # 消息最大长度(B)
                "msg_filter_type": cmq_topic_filter_type_map.get(instance.get("FilterType"), "未知"),  # 消息过滤类型
                "qps": instance.get("Qps"),  # QPS限制
            } for instance in instances])
        return result

    def get_qcloud_clb(self):
        """资源名、资源ID、标签、项目ID、安全组ID、VPC、地域、主可用区、备可用区、状态、域名、VIP、网络类型、运营商、付费类型"""
        result = []
        for region in self.available_region_list:
            clb_info = self.get_tencent_client(region=region).clb.call_json("DescribeLoadBalancers", {})
            instances = clb_info.get("Response", {}).get("LoadBalancerSet", [])
            result.extend([{
                "inst_name": instance.get("LoadBalancerName"),
                "inst_id": instance.get("LoadBalancerId"),
                "tags": instance.get("Tags"),
                "project_id": instance.get("ProjectId"),
                "sg_id_list": instance.get("SecurityGroup"),
                "vpc_id": instance.get("VpcId"),
                "region": region,
                "master_zone": instance.get("MasterZone"),
                "backup_zone_list": instance.get("BackupZoneSet"),
                "status": clb_status_map.get(instance.get("Status"), "未知"),
                "domain": instance.get("Domain"),
                "vip_list": instance.get("LoadBalancerVips"),
                "net_type": clb_net_type_map.get(instance.get("LoadBalancerType"), "未知"),
                "isp": clb_isp_map.get(instance.get("LoadBalancerType"), "未知"),
                "pay_type": clb_pay_type_map.get(instance.get("PrepaidAttributes", {}).get("RenewFlag"), "未知"),
            } for instance in instances])
        return result

    def get_qcloud_eip(self):
        """资源名、资源ID、标签、地域、状态、类型、公网IP地址、绑定资源类型、绑定资源ID、线路类型、付费类型"""
        result = []
        for region in self.available_region_list:
            eip_info = self.get_tencent_client(region=region).vpc.call_json("DescribeAddresses", {})
            instances = eip_info.get("Response", {}).get("AddressSet", [])
            result.extend([{
                "inst_name": instance.get("AddressName"),
                "inst_id": instance.get("AddressId"),
                "tags": instance.get("TagSet"),
                "region": region,
                "status": eip_status_map.get(instance.get("AddressStatus"), "未知"),
                "type": eip_type_map.get(instance.get("AddressType"), "未知"),
                "public_ip": instance.get("AddressIp"),  # 公网IP地址
                "res_type": eip_res_type_map.get(instance.get("InstanceType"), "未知"),
                "res_id": instance.get("InstanceId"),
                "isp_type": eip_isp_map.get(instance.get("InternetServiceProvider"), "未知"),  # 线路类型
                "pay_type": eip_pay_type_map.get(instance.get("InternetChargeType"), "未知"),
            } for instance in instances])
        return result

    def get_qcloud_bucket(self):
        """资源名、资源ID、地域"""
        result = []
        for region in self.available_region_list:
            buckets = self.get_tencent_cos_client(region=region).list_buckets().get("Buckets",{}).get("Bucket")
            for bucket in buckets:
                result.append({
                    "inst_name": bucket.get("Name"),
                    "inst_id": bucket.get("Name"),
                    "region": bucket.get("Location"),
                })
        return result

    def get_qcloud_filesystem(self):
        """资源名、资源ID、标签、地域、可用区、状态、文件系统协议、存储类型、吞吐上限(MiB/s)、总容量(GiB)"""
        result = []
        for region in self.available_region_list:
            cfs_info = self.get_tencent_client(region=region).cfs.call_json("DescribeCfsFileSystems", {})
            instances = cfs_info.get("Response", {}).get("FileSystems", [])
            result.extend([{
                "inst_name": instance.get("FsName"),
                "inst_id": instance.get("FileSystemId"),
                "tags": instance.get("Tags"),
                "region": region,
                "zone": instance.get("Zone"),
                "status": cfs_status_map.get(instance.get("LifeCycleState"), "未知"),
                "protocol": instance.get("Protocol"),
                "storage_type": cfs_storage_type_map.get(instance.get("StorageType"), "未知"),
                "throughput": instance.get("BandwidthLimit"),  # 吞吐上限(MiB/s)
                "capacity": instance.get("Capacity"),
            } for instance in instances])
        return result

    def get_qcloud_domain(self):
        """资源名、资源ID、域名后缀、状态、到期时间"""
        domain_info = self.get_tencent_client("").domain.call_json("DescribeDomainNameList", {})
        return [{
            "inst_name": instance.get("DomainName"),
            "inst_id": instance.get("DomainId"),
            "domain_suffix": instance.get("CodeTld"),  # 域名后缀
            "status": domain_status_map.get(instance.get("BuyStatus"), "未知"),
            "expire_time": instance.get("ExpirationDate"),  # 到期时间
        } for instance in domain_info.get("DomainList", [])]

    def exec_script(self):
        return {
            "qcloud": self.get_qcloud(),
            "qcloud_cvm": self.get_qcloud_cvm(),
            "qcloud_rocketmq": self.get_qcloud_rocketmq(),
            "qcloud_mysql": self.get_qcloud_mysql(),
            "qcloud_redis": self.get_qcloud_redis(),
            "qcloud_mongodb": self.get_qcloud_mongodb(),
            "qcloud_pgsql": self.get_qcloud_pgsql(),
            "qcloud_pulsar_cluster": self.get_qcloud_pulsar_cluster(),
            "qcloud_cmq": self.get_qcloud_cmq(),
            "qcloud_cmq_topic": self.get_qcloud_cmq_topic(),
            "qcloud_clb": self.get_qcloud_clb(),
            "qcloud_eip": self.get_qcloud_eip(),
            "qcloud_bucket": self.get_qcloud_bucket(),
            "qcloud_filesystem": self.get_qcloud_filesystem(),
            "qcloud_domain": self.get_qcloud_domain()
        }

    def list_all_resources(self):
        try:
            result = self.exec_script()
        except Exception as err:
            import traceback
            logger.error(f"{self.__class__.__name__} main error! {traceback.format_exc()}")
            result = {}
        return convert_to_prometheus_format(result)

    def test_connection(self):
        """
        Test connection to Tencent Cloud Api
        : return  True if connection is successful, False otherwise
        """
        try:
            self.get_qcloud_region()
            return True
        except Exception as err:
            import traceback
            logger.error(f"{self.__class__.__name__} test_connection error! {traceback.format_exc()}")
            return False


if __name__ == '__main__':
    import os

    params = {
        "secret_id": os.getenv("qcloud_secret_id"),
        "secret_key": os.getenv("qcloud_secret_key"),
    }
    manager = TencentCloudManager(params)
    client = manager.get_tencent_client("")

    # print(manager.get_qcloud_cvm())
    print(manager.get_qcloud_bucket())
    # print(client.organization.call_json("DescribeOrganization",{}))

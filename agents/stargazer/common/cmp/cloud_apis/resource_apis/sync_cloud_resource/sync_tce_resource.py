# -*- coding: utf-8 -*-
"""同步tce资源"""
from common.cmp.cloud_apis.constant import CloudResourceType
from common.cmp.cloud_apis.resource_apis.sync_cloud_resource.cloud_resource import SyncPrivateCloudResource
from common.cmp.exceptions import SyncResourceDataError
from common.cmp.models import (
    BMS,
    TDSQL,
    TKE,
    Bucket,
    CKafka,
    FileSystem,
    LoadBalancer,
    LoadBalancerListener,
    Mariadb,
    Mongodb,
    Redis,
    TKEInstance,
)


class SyncTCEResource(SyncPrivateCloudResource):
    def __init__(self, client, account):
        super().__init__(client, account)
        self.resource_list.extend(
            [
                CloudResourceType.REDIS.value,
                CloudResourceType.FILE_SYSTEM.value,
                CloudResourceType.LOAD_BALANCER.value,
                CloudResourceType.BUCKET.value,
                CloudResourceType.TDSQL.value,
                CloudResourceType.MARIADB.value,
                CloudResourceType.MONGODB.value,
                CloudResourceType.INSTANCE_TYPE.value,
                CloudResourceType.INSTANCE_TYPE_FAMILY.value,
                CloudResourceType.BMS.value,
                CloudResourceType.CKafka.value,
                CloudResourceType.TKE.value,
                CloudResourceType.EIP.value,
            ]
        )

    def sync_file_system(self, ids=None):
        rs = self.client.list_file_systems(ids)
        if not rs["result"]:
            raise SyncResourceDataError(
                "同步文件系统FileSystem数据失败[{}: {}]".format(self.account.config_name, rs.get("message"))
            )
        self.sync_resource(FileSystem, self.account, rs["data"])

    def sync_bucket(self):
        rs = self.client.list_buckets()
        if not rs["result"]:
            raise SyncResourceDataError("同步Bucket数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(Bucket, self.account, rs["data"])

    def sync_tdsql(self, ids=None):
        rs = self.client.list_tdsql_instances(ids)
        if not rs["result"]:
            raise SyncResourceDataError("同步TDSQL数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(TDSQL, self.account, rs["data"])

    def sync_mariadb(self, ids=None):
        rs = self.client.list_mariadb_instances(ids)
        if not rs["result"]:
            raise SyncResourceDataError("同步Mariadb数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(Mariadb, self.account, rs["data"])

    def sync_redis(self, ids=None):
        rs = self.client.list_redis_instances(ids)
        if not rs["result"]:
            raise SyncResourceDataError("同步Redis数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(Redis, self.account, rs["data"])

    def sync_load_balancer(self, ids=None):
        rs = self.client.list_load_balancers(ids)
        if not rs["result"]:
            raise SyncResourceDataError("同步负载均衡数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(LoadBalancer, self.account, rs["data"])
        load_balancer_ids = [item["resource_id"] for item in rs["data"]]
        for load_balancer_id in load_balancer_ids:
            self.sync_listener(load_balancer_id, rs["data"][0]["cloud_type"])

    def sync_listener(self, load_balancer_id=None, cloud_type=None):
        rs = self.client.list_listeners(LoadBalancerId=load_balancer_id)
        if not rs["result"]:
            raise SyncResourceDataError("同步负载均衡监听表数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(LoadBalancerListener, self.account, rs["data"])

    def sync_mongodb(self):
        rs = self.client.list_mongodbs()
        if not rs["result"]:
            raise SyncResourceDataError("同步MongodDB数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(Mongodb, self.account, rs["data"])

    def sync_bms(self):
        res = self.client.list_bmss()
        if not res["result"]:
            raise SyncResourceDataError("同步裸金属BMS数据失败[{}: {}]".format(self.account.config_name, res["message"]))
        self.sync_resource(BMS, self.account, res["data"])

    def sync_ckafka(self):
        res = self.client.list_ckafkas()
        if not res["result"]:
            raise SyncResourceDataError("同步CKafka数据失败[{}: {}]".format(self.account.config_name, res["message"]))
        self.sync_resource(CKafka, self.account, res["data"])

    def sync_tke(self):
        res = self.client.list_tke_clusters()
        if not res["result"]:
            raise SyncResourceDataError("同步TKE集群数据失败[{}: {}]".format(self.account.config_name, res["message"]))
        self.sync_resource(TKE, self.account, res["data"])
        self.sync_tke_instance([i["resource_id"] for i in res["data"]])

    def sync_tke_instance(self, cluster_ids):
        res_data = []
        for cluster_id in cluster_ids:
            res = self.client.list_tke_cluster_instances(cluster_id)
            if not res["result"]:
                raise SyncResourceDataError("同步tke集群下实例数据失败[{}: {}]".format(self.account.config_name, res["message"]))
            res_data.extend(res["data"])
        self.sync_resource(TKEInstance, self.account, res_data)

# -*- coding: utf-8 -*-
from common.cmp.cloud_apis.cloud_constant import CloudPlatform
from common.cmp.cloud_apis.constant import CloudResourceType
from common.cmp.cloud_apis.resource_apis.cw_tke_cloud import CwTKECloud
from common.cmp.cloud_apis.resource_apis.sync_cloud_resource.base import SyncBaseResource
from common.cmp.exceptions import SyncResourceDataError
from common.cmp.models import (
    VM,
    VPC,
    Bucket,
    Disk,
    LoadBalancer,
    LoadBalancerListener,
    Mariadb,
    Redis,
    RelayRule,
    RouteEntry,
    SecurityGroup,
    SecurityGroupRule,
    Snapshot,
    Subnet,
    TKECloudCluster,
    TKECloudNodeList,
)
from common.cmp.utils import list_dict_duplicate_removal


class SyncPublicCloudResource(SyncBaseResource):
    def __init__(self, client, account):
        super().__init__(client, account)
        self.resource_list = [
            CloudResourceType.REGION.value,
            CloudResourceType.ZONE.value,
            CloudResourceType.VM.value,
            CloudResourceType.DISK.value,
            CloudResourceType.SNAPSHOT.value,
            CloudResourceType.IMAGE.value,
            CloudResourceType.VPC.value,
            CloudResourceType.SUBNET.value,
            CloudResourceType.EIP.value,
            CloudResourceType.SECURITY_GROUP.value,
            CloudResourceType.BUCKET.value,
            CloudResourceType.INSTANCE_TYPE_FAMILY.value,
            CloudResourceType.FILE_SYSTEM.value,
            CloudResourceType.INSTANCE_TYPE.value,
            CloudResourceType.SNAPSHOT_POLICY.value,
            CloudResourceType.ROUTE_TABLE.value,
            CloudResourceType.LISTENER.value,
            CloudResourceType.SERVER_CERTIFICATE.value,
            CloudResourceType.LOAD_BALANCER.value,
        ]


class SyncPrivateCloudResource(SyncBaseResource):
    def __init__(self, client, account):
        super().__init__(client, account)
        self.resource_list = [
            CloudResourceType.REGION.value,
            CloudResourceType.ZONE.value,
            CloudResourceType.VM.value,
            CloudResourceType.DISK.value,
            CloudResourceType.SNAPSHOT.value,
            CloudResourceType.IMAGE.value,
            CloudResourceType.VPC.value,
            CloudResourceType.SUBNET.value,
            CloudResourceType.SECURITY_GROUP.value,
        ]


class SyncAliyunResource(SyncPublicCloudResource):
    pass


class SyncApsaraResource(SyncPublicCloudResource):
    def __init__(self, client, account):
        super().__init__(client, account)
        self.resource_list = [
            CloudResourceType.REGION.value,
            CloudResourceType.ZONE.value,
            CloudResourceType.VM.value,
            CloudResourceType.DISK.value,
            CloudResourceType.SNAPSHOT.value,
            CloudResourceType.IMAGE.value,
            CloudResourceType.VPC.value,
            CloudResourceType.SUBNET.value,
            # CloudResourceType.EIP.value,
            CloudResourceType.SECURITY_GROUP.value,
            CloudResourceType.BUCKET.value,
            CloudResourceType.INSTANCE_TYPE_FAMILY.value,
            # CloudResourceType.FILE_SYSTEM.value,
            CloudResourceType.INSTANCE_TYPE.value,
            # CloudResourceType.SNAPSHOT_POLICY.value,
            # CloudResourceType.ROUTE_TABLE.value,
            # CloudResourceType.LISTENER.value,
            # CloudResourceType.SERVER_CERTIFICATE.value,
            # CloudResourceType.LOAD_BALANCER.value,
        ]


class SyncQCloudResource(SyncPublicCloudResource):
    def __init__(self, client, account):
        super().__init__(client, account)
        self.resource_list = [
            CloudResourceType.REGION.value,
            CloudResourceType.ZONE.value,
            CloudResourceType.VM.value,
            CloudResourceType.DISK.value,
            CloudResourceType.SNAPSHOT.value,
            CloudResourceType.IMAGE.value,
            CloudResourceType.VPC.value,
            CloudResourceType.SUBNET.value,
            CloudResourceType.EIP.value,
            CloudResourceType.SECURITY_GROUP.value,
            # CloudResourceType.BUCKET.value,
            CloudResourceType.INSTANCE_TYPE_FAMILY.value,
            # CloudResourceType.FILE_SYSTEM.value,
            CloudResourceType.INSTANCE_TYPE.value,
            CloudResourceType.SNAPSHOT_POLICY.value,
            CloudResourceType.ROUTE_TABLE.value,
            # CloudResourceType.LISTENER.value,
            CloudResourceType.SERVER_CERTIFICATE.value,
            # CloudResourceType.LOAD_BALANCER.value,
        ]

    def get_security_group_vpc(self):
        """腾讯云获取安全组关联实例的VPC"""
        vm_objs = VM.objects.filter(account_id=self.account.id).values("security_group", "vpc")
        if not vm_objs:
            return []
        vm_list = [{"security_group": i["security_group"], "vpc": i["vpc"]} for i in vm_objs]
        return vm_list

    def sync_security_group(self, ids=None):
        rs = self.client.list_security_groups(ids)
        if not rs["result"]:
            raise SyncResourceDataError("同步安全组数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        vm_list = self.get_security_group_vpc()
        for i in rs["data"]:
            for j in vm_list:
                if i["resource_id"] in j["security_group"]:
                    i["vpc"] = j["vpc"]
        self.sync_resource(SecurityGroup, self.account, rs["data"])
        # 同步安全组规则必须有安全组id
        self.sync_security_group_rule([i["resource_id"] for i in rs["data"]])

    def sync_load_balancer(self):
        rs = self.client.list_load_balancers()
        if not rs["result"]:
            raise SyncResourceDataError("同步负载均衡表数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(LoadBalancer, self.account, rs["data"])
        self.sync_vserver_groups([item["resource_id"] for item in rs["data"]])
        self.sync_rule(rs["data"])
        load_balancer_ids = [item["resource_id"] for item in rs["data"]]
        for load_balancer_id in load_balancer_ids:
            self.sync_listener(load_balancer_id, rs["data"][0]["cloud_type"])

    def sync_listener(self, load_balancer_id=None, cloud_type=None):
        rs = self.client.list_listeners(LoadBalancerId=load_balancer_id)
        if not rs["result"]:
            raise SyncResourceDataError("同步负载均衡监听表数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(LoadBalancerListener, self.account, rs["data"])


class SyncHuaweiCloudResource(SyncPublicCloudResource):
    def __init__(self, client, account):
        super().__init__(client, account)
        self.resource_list.extend(
            [
                CloudResourceType.DOMAIN.value,
                # CloudResourceType.PROJECT.value
            ]
        )


class SyncOpenStackResource(SyncPrivateCloudResource):
    def __init__(self, client, account):
        super().__init__(client, account)
        self.resource_list.extend(
            [
                CloudResourceType.DOMAIN.value,
                # CloudResourceType.PROJECT.value,
                CloudResourceType.EIP.value,
                CloudResourceType.INSTANCE_TYPE.value,
            ]
        )


class SyncVMwareResource(SyncPrivateCloudResource):
    def __init__(self, client, account):
        self.client = client
        self.account = account
        self.resource_list = [
            CloudResourceType.REGION.value,
            CloudResourceType.ZONE.value,
            CloudResourceType.VM.value,
            CloudResourceType.IMAGE.value,
            CloudResourceType.VPC.value,
            CloudResourceType.SUBNET.value,
            CloudResourceType.CLUSTER.value,
            CloudResourceType.HOST.value,
            CloudResourceType.PRIVATE_STORAGE.value,
        ]

    def sync_vm(self):
        rs = self.client.list_vms()

        if not rs["result"]:
            raise SyncResourceDataError("同步虚拟机数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        rs["data"]["list_vms"] = list_dict_duplicate_removal(rs["data"]["list_vms"], CloudResourceType.VM.value)
        rs["data"]["list_disks"] = list_dict_duplicate_removal(rs["data"]["list_disks"], CloudResourceType.DISK.value)
        rs["data"]["list_snapshots"] = list_dict_duplicate_removal(
            rs["data"]["list_snapshots"], CloudResourceType.SNAPSHOT.value
        )
        self.sync_resource(VM, self.account, rs["data"]["list_vms"])
        self.sync_resource(Disk, self.account, rs["data"]["list_disks"])
        self.sync_resource(Snapshot, self.account, rs["data"]["list_snapshots"])
        # 重新组装虚拟机磁盘数据
        disk_lists = list(
            Disk.objects.filter(account=self.account, cloud_type=CloudPlatform.VMware).values(
                "resource_id", "server_id", "disk_type"
            )
        )
        vm_query = VM.objects.filter(account=self.account, cloud_type=CloudPlatform.VMware)
        for disk in disk_lists:
            vm_obj = vm_query.filter(resource_id=disk["server_id"]).first()
            if not vm_obj:
                continue
            if disk["disk_type"] == "SYSTEM_DISK":
                if not vm_obj.system_disk:
                    vm_obj.system_disk = {"id": disk["resource_id"]}
            else:
                data_disks = vm_obj.data_disk
                data_disks = list(set(data_disks))
                if disk["resource_id"] in data_disks:
                    continue
                data_disks.append(disk["resource_id"])
                vm_obj.data_disk = data_disks
            vm_obj.save()

    def sync_subnet(self):
        rs = self.client.list_subnets()
        if not rs["result"]:
            raise SyncResourceDataError("同步Subnet数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))

        resource_objs = Subnet.objects.filter(account_id=self.account, cloud_type=CloudPlatform.VMware).values(
            "resource_id", "resource_name"
        )
        resource_tuple_list = [(i["resource_id"], i["resource_name"]) for i in resource_objs]

        new_resource_list, update_list = [], []
        for cur_data in rs["data"]:
            if (cur_data["resource_id"], cur_data["resource_name"]) in resource_tuple_list:
                subnet_obj = Subnet.objects.get(
                    resource_id=cur_data["resource_id"], resource_name=cur_data["resource_name"]
                )
                update_list.append(subnet_obj)
            else:
                new_resource_list.append(cur_data)
        self._update_subnet(update_list)
        self.sync_resource(Subnet, self.account, new_resource_list, False)
        return new_resource_list

    def _update_subnet(self, data):
        update_fields = [
            f.name
            for f in Subnet._meta.fields
            if f.name not in ["id", "resource_id", "resource_name", "account", "resource_infos"]
        ]
        Subnet.objects.bulk_update(data, update_fields, batch_size=200)


class SyncFusionCloudResource(SyncPrivateCloudResource):
    def __init__(self, client, account):
        super().__init__(client, account)
        self.resource_list = [
            CloudResourceType.REGION.value,
            CloudResourceType.ZONE.value,
            CloudResourceType.VM.value,
            CloudResourceType.DISK.value,
            CloudResourceType.SNAPSHOT.value,
            CloudResourceType.IMAGE.value,
            CloudResourceType.VPC.value,
            CloudResourceType.SUBNET.value,
            CloudResourceType.SECURITY_GROUP.value,
            CloudResourceType.INSTANCE_TYPE.value,
            # CloudResourceType.ROUTE_TABLE.value,
            # CloudResourceType.DOMAIN.value,
            # CloudResourceType.PROJECT.value,
            CloudResourceType.EIP.value,
            # CloudResourceType.LOAD_BALANCER.value,
            # CloudResourceType.LISTENER.value,
            # CloudResourceType.BUCKET.value,
        ]

    def sync_load_balancer(self):
        rs = self.client.list_load_balancers()
        if not rs["result"]:
            raise SyncResourceDataError("同步负载均衡表数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(LoadBalancer, self.account, rs["data"])
        # self.sync_vserver_groups([item["resource_id"] for item in rs["data"]])
        self.sync_rule(rs["data"])

    def sync_rule(self, load_balancers):
        res_data = []
        for load_balancer in load_balancers:
            # 负载均衡下有监听，监听下有规则，查询的规则只有监听ID，查询监听的接口才有对应负载均衡ID
            # ports = load_balancer.get("port", [])
            # for port in ports:
            #     kwargs = {"LoadBalancerId": load_balancer["resource_id"], "ListenerPort": port.get("ListenerPort"),
            #               "ListenerProtocal": port.get("ListenerProtocal")}
            kwargs = {
                "load_balancer": load_balancer["resource_id"],
                "listener_ids": load_balancer["extra"]["listener_ids"],
            }
            rs = self.client.list_rules(**kwargs)
            if not rs["result"]:
                raise SyncResourceDataError("同步转发规则表数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
            res_data.extend(rs["data"])
        self.sync_resource(RelayRule, self.account, res_data)

    def sync_route_tables(self):
        # FusionCloud的路由表就是路由
        rs = self.client.list_routers()
        if not rs["result"]:
            raise SyncResourceDataError("同步路由策略表数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(RouteEntry, self.account, rs["data"])


class SyncCwFusionComputeResource(SyncBaseResource):
    def __init__(self, client, account):
        super().__init__(client, account)
        self.resource_list = [
            CloudResourceType.REGION.value,
            CloudResourceType.ZONE.value,
            CloudResourceType.VM.value,
            CloudResourceType.DISK.value,
            # CloudResourceType.SNAPSHOT.value,
            CloudResourceType.IMAGE.value,
            CloudResourceType.VPC.value,
            CloudResourceType.SECURITY_GROUP.value,
            CloudResourceType.BUCKET.value,
            # CloudResourceType.EIP.value,
        ]

    def sync_vm(self, ids=None):
        rs = self.client.list_vms(ids)
        if not rs["result"]:
            raise SyncResourceDataError("同步虚拟机数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(VM, self.account, rs["data"])
        # 同步虚拟机下的快照
        self.sync_snapshot(i["resource_id"] for i in rs["data"])

    def sync_snapshot(self, server_ids):
        rs = self.client.list_snapshots(server_ids)
        if not rs["result"]:
            raise SyncResourceDataError("同步快照数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(Snapshot, self.account, rs["data"])

    def sync_vpc(self, ids=None):
        rs = self.client.list_vpcs(ids)
        if not rs["result"]:
            raise SyncResourceDataError("同步VPC数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(VPC, self.account, rs["data"])
        # 同步 VPC 下的子网
        self.sync_subnet(i["resource_id"] for i in rs["data"])

    def sync_subnet(self, vpc_ids):
        res_data = []
        for vpc_id in vpc_ids:
            rs = self.client.list_subnets(vpc_id)
            if not rs["result"]:
                raise SyncResourceDataError("同步Subnet数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
            res_data.extend(rs["data"])
        self.sync_resource(Subnet, self.account, res_data)

    def sync_bucket(self):
        rs = self.client.list_buckets()
        if not rs["result"]:
            raise SyncResourceDataError("同步存储桶数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(Bucket, self.account, rs["data"])


class SyncTKECloudResource(SyncPrivateCloudResource):
    def __init__(self):
        self.resource_list = []

    def sync_node_list(self):
        node_list = CwTKECloud().node_list()
        update_fields = [
            "generate_name",
            "self_link",
            "finalizers",
            "cluster_name",
            "type",
            "ip",
            "port",
            "username",
            "phase",
        ]
        self._create_update_delete_func(node_list, TKECloudNodeList, update_fields)

    @staticmethod
    def sync_node_details(self):
        node = CwTKECloud.node_details()
        return node

    def sync_cluster(self):
        clusters = CwTKECloud().clusters()
        update_fields = [
            "self_link",
            "labels",
            "finalizers",
            "tenant_id",
            "display_name",
            "type",
            "version",
            "network_device",
            "clusterCIDR",
            "serviceCIDR",
            "dns_domain",
            "public_alternative_names",
            "features",
            "properties",
            "machines",
            "kubelet_extra_args",
            "cluster_credential_ref",
            "etcd",
        ]
        self._create_update_delete_func(clusters, TKECloudCluster, update_fields)

    @staticmethod
    def _create_update_delete_func(datas, model_class, update_fields):
        old_name_list = set(model_class.objects.values_list("name", flat=True))
        new_name_list = {item["name"] for item in datas}

        need_create = new_name_list - old_name_list
        need_update = new_name_list & old_name_list
        need_delete = old_name_list - new_name_list

        need_create_obj = [item for item in datas if item["name"] in need_create]
        need_update_obj_dict = {item["name"]: item for item in datas if item["name"] in need_update}

        # 删除没查询到的节点
        model_class.objects.filter(name__in=need_delete).delete()

        # 更新已存在的对象
        exist_need_update_objs = model_class.objects.filter(name__in=need_update)

        need_update_obj = []
        for obj in exist_need_update_objs:
            for field in update_fields:
                setattr(obj, field, need_update_obj_dict[obj.name][field])
                # obj.generate_name = need_update_obj_dict[obj.name]['generate_name']
            need_update_obj.append(obj)
        model_class.objects.bulk_update(need_update_obj, fields=update_fields, batch_size=200)
        _need_create_obj = [model_class(**item) for item in need_create_obj]
        # 批量创建不存在的
        model_class.objects.bulk_create(_need_create_obj, batch_size=200)


class SyncEasyStackResource(SyncPrivateCloudResource):
    def __init__(self, client, account):
        super().__init__(client, account)
        self.resource_list = [
            CloudResourceType.VM.value,
        ]


class SyncCasResource(SyncPrivateCloudResource):
    def __init__(self, client, account):
        super().__init__(client, account)
        self.resource_list = [
            CloudResourceType.VM.value,
        ]


class SyncQingCloudResource(SyncPrivateCloudResource):
    def __init__(self, client, account):
        super().__init__(client, account)
        self.resource_list = [
            CloudResourceType.VM.value,
            CloudResourceType.REGION.value,
            CloudResourceType.ZONE.value,
            CloudResourceType.IMAGE.value,
            CloudResourceType.DISK.value,
            CloudResourceType.VPC.value,
            CloudResourceType.SUBNET.value,
            CloudResourceType.SECURITY_GROUP.value,
            CloudResourceType.SECURITY_GROUP_RULE.value,
            CloudResourceType.MARIADB.value,
            CloudResourceType.REDIS.value,
            CloudResourceType.LOAD_BALANCER.value,
            CloudResourceType.LISTENER.value,
        ]

    def sync_security_group(self):
        rs = self.client.list_security_groups()
        if not rs["result"]:
            raise SyncResourceDataError("同步安全组数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(SecurityGroup, self.account, rs["data"])

    def sync_security_group_rule(self):
        rs = self.client.list_security_group_rules()
        if not rs["result"]:
            raise SyncResourceDataError("同步安全组规则数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(SecurityGroupRule, self.account, rs["data"])

    def sync_load_balancer(self):
        rs = self.client.list_load_balancers()
        if not rs["result"]:
            raise SyncResourceDataError("同步负载均衡数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(LoadBalancer, self.account, rs["data"])

    def sync_listener(self):
        rs = self.client.list_listeners()
        if not rs["result"]:
            raise SyncResourceDataError("同步负载均衡监听数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(LoadBalancerListener, self.account, rs["data"])

    def sync_redis(self):
        rs = self.client.list_rediss()
        if not rs["result"]:
            raise SyncResourceDataError("同步负载均衡监听数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(Redis, self.account, rs["data"])

    def sync_mariadb(self):
        rs = self.client.list_mariadbs()
        if not rs["result"]:
            raise SyncResourceDataError("同步负载均衡监听数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(Mariadb, self.account, rs["data"])


class SyncTSFResource(SyncPrivateCloudResource):
    def __init__(self, client, account):
        super().__init__(client, account)
        self.resource_list = [
            CloudResourceType.APPLICATION.value,
        ]


class SyncAmazonAwsResource(SyncPublicCloudResource):
    def __init__(self, client, account):
        super().__init__(client, account)
        self.resource_list = [
            CloudResourceType.REGION.value,
            CloudResourceType.ZONE.value,
            CloudResourceType.VM.value,
            CloudResourceType.DISK.value,
            CloudResourceType.VPC.value,
            CloudResourceType.SUBNET.value,
            CloudResourceType.SECURITY_GROUP.value,
            CloudResourceType.SNAPSHOT.value,
            CloudResourceType.IMAGE.value,
        ]

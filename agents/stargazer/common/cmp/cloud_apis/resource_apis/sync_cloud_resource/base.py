# -*- coding: utf-8 -*-
from loguru import logger

from common.cmp.exceptions import SyncResourceDataError
from common.cmp.models import (
    VM,
    VPC,
    AccountConfig,
    Application,
    Bucket,
    BucketFile,
    Cluster,
    Disk,
    Domain,
    Eip,
    FileSystem,
    HostMachine,
    Image,
    InstanceFamily,
    InstanceType,
    LoadBalancer,
    LoadBalancerListener,
    PrivateStorage,
    ProjectInfo,
    RegionInfo,
    RelayRule,
    ResourceInfos,
    RouteEntry,
    RouteTable,
    SecurityGroup,
    SecurityGroupRule,
    ServerCertificate,
    ServerGroup,
    Snapshot,
    SnapshotPolicy,
    Subnet,
    ZoneInfo,
)


class SyncBaseResource:
    def __init__(self, client, account):
        self.client = client
        self.account = account

    def sync_all_resource(self):
        error_list = []
        for resource_name in getattr(self, "resource_list", []):
            try:
                getattr(self, "sync_{}".format(resource_name))()
            except SyncResourceDataError as sync_resource_error:
                error_list.append(sync_resource_error.message)
            except Exception as method_error:
                message = "同步资源{}出错{}".format(resource_name, method_error.__str__())
                logger.exception(message)
                error_list.append(message)
        return error_list

    @staticmethod
    def sync_resource(resource_model, account, data, is_auto=True):
        resource_objs = [
            cur_id for cur_id in resource_model.objects.filter(account=account).values("resource_id", "resource_name")
        ]
        if resource_model._meta.object_name in {"InstanceType"}:
            # 类似腾讯云的规格，resource_id可能是重复的，所以用resource_id + zone 确定唯一的规格
            resource_objs = [
                cur_id
                for cur_id in resource_model.objects.filter(account=account).values(
                    "resource_id", "resource_name", "zone"
                )
            ]
            resource_ids = {(i["resource_id"], i["zone"]) for i in resource_objs}
            existed_obj_mapping = {}
            new_resource_list = []
            # extra_data = []
            for cur_data in data:
                if not cur_data:
                    logger.error("Data is None:" + resource_model._meta.object_name)
                    continue
                if (cur_data["resource_id"], cur_data.get("zone", "")) in resource_ids:
                    existed_obj_mapping[(cur_data["resource_id"], cur_data.get("zone", ""))] = cur_data
                    resource_ids.remove((cur_data["resource_id"], cur_data.get("zone", "")))
                else:
                    new_resource_list.append(cur_data)
        else:
            resource_ids = {i["resource_id"] for i in resource_objs}

            existed_obj_mapping = {}
            new_resource_list = []
            # extra_data = []
            for cur_data in data:
                if not cur_data:
                    logger.error("Data is None:" + resource_model._meta.object_name)
                    continue
                if cur_data["resource_id"] in resource_ids:
                    existed_obj_mapping[cur_data["resource_id"]] = cur_data
                    resource_ids.remove(cur_data["resource_id"])
                else:
                    new_resource_list.append(cur_data)

        # resource_names = {i["resource_name"] for i in resource_objs}
        # bulk update resource
        updated_existed_objs = []
        update_fields = []
        for existed_obj in resource_model.objects.filter(account=account, resource_id__in=existed_obj_mapping.keys()):
            cur_resource = existed_obj_mapping[existed_obj.resource_id]
            update_fields = cur_resource.keys()
            for obj_attr in update_fields:
                setattr(existed_obj, obj_attr, cur_resource[obj_attr])
            updated_existed_objs.append(existed_obj)
        if update_fields:
            resource_model.objects.bulk_update(updated_existed_objs, update_fields, batch_size=200)

        # bulk create resource
        if resource_model._meta.object_name in {"Bucket"}:
            account_objs = AccountConfig.objects.filter(config_name=account.config_name)
            resource_id_list = list(
                resource_model.objects.filter(account__in=account_objs).values_list("resource_id", flat=True)
            )
            new_objs = [
                resource_model(account=account, resource_infos=ResourceInfos.objects.create(), **cur_resource)
                for cur_resource in new_resource_list
                if cur_resource["resource_id"] not in resource_id_list
            ]
        else:
            new_objs = [
                resource_model(account=account, resource_infos=ResourceInfos.objects.create(), **cur_resource)
                for cur_resource in new_resource_list
            ]
        resource_model.objects.bulk_create(new_objs, batch_size=200)

        # bulk delete resource
        if is_auto:
            resource_model.objects.filter(account=account, resource_id__in=resource_ids).delete(is_log=True)

        return new_resource_list

    def sync_region(self):
        rs = self.client.list_regions()
        if not rs["result"]:
            raise SyncResourceDataError("同步Region数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(RegionInfo, self.account, rs["data"])

    def sync_zone(self):
        rs = self.client.list_zones()
        if not rs["result"]:
            raise SyncResourceDataError("同步可用区数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(ZoneInfo, self.account, rs["data"])

    def sync_project(self):
        rs = self.client.list_projects()
        if not rs["result"]:
            raise SyncResourceDataError("同步项目数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(ProjectInfo, self.account, rs["data"])

    def sync_domain(self):
        rs = self.client.list_domains()
        if not rs["result"]:
            raise SyncResourceDataError("同步域数据失败[{}: {}]".format(self.account.cloud_type, self.account.config_name))
        self.sync_resource(Domain, self.account, rs["data"])

    def sync_instance_type_family(self):
        rs = self.client.list_instance_type_families()
        if not rs["result"]:
            raise SyncResourceDataError(
                "同步数据InstanceFamily失败[{}: {}]".format(self.account.config_name, rs.get("message"))
            )
        self.sync_resource(InstanceFamily, self.account, rs["data"])

    def sync_instance_type(self):
        rs = self.client.list_instance_types()
        if not rs["result"]:
            raise SyncResourceDataError(
                "同步数据InstanceType失败[{}: {}]".format(self.account.config_name, rs.get("message"))
            )
        self.sync_resource(InstanceType, self.account, rs["data"])

    def sync_vm(self, ids=None):
        rs = self.client.list_vms(ids)
        if not rs["result"]:
            raise SyncResourceDataError("同步虚拟机数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(VM, self.account, rs["data"])

    def sync_cluster(self, ids=None):
        rs = self.client.list_clusters(ids)
        if not rs["result"]:
            raise SyncResourceDataError("同步虚拟机集群失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(Cluster, self.account, rs["data"])

    def sync_disk(self, ids=None):
        rs = self.client.list_disks(ids)
        if not rs["result"]:
            raise SyncResourceDataError("同步磁盘数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(Disk, self.account, rs["data"])

    def sync_snapshot(self, ids=None):
        rs = self.client.list_snapshots(ids)
        if not rs["result"]:
            raise SyncResourceDataError("同步快照数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(Snapshot, self.account, rs["data"])

    def sync_image(self, ids=None):
        rs = self.client.list_images(ids)
        if not rs["result"]:
            raise SyncResourceDataError("同步镜像数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(Image, self.account, rs["data"])

    def sync_vpc(self, ids=None):
        rs = self.client.list_vpcs(ids)
        if not rs["result"]:
            raise SyncResourceDataError("同步VPC数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(VPC, self.account, rs["data"])

    def sync_subnet(self, ids=None):
        rs = self.client.list_subnets(ids)
        if not rs["result"]:
            raise SyncResourceDataError("同步Subnet数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(Subnet, self.account, rs["data"])

    def sync_eip(self, ids=None):
        rs = self.client.list_eips(ids)
        if not rs["result"]:
            raise SyncResourceDataError("同步EIP数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(Eip, self.account, rs["data"])

    def sync_host(self):
        rs = self.client.list_hosts()
        if not rs["result"]:
            raise SyncResourceDataError("同步主机数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(HostMachine, self.account, rs["data"])

    def sync_security_group(self, ids=None):
        rs = self.client.list_security_groups(ids)
        if not rs["result"]:
            raise SyncResourceDataError("同步安全组数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(SecurityGroup, self.account, rs["data"])
        # 同步安全组规则必须有安全组id
        self.sync_security_group_rule([i["resource_id"] for i in rs["data"]])

    def sync_security_group_rule(self, security_group_ids):
        res_data = []
        for i in security_group_ids:
            rs = self.client.list_security_group_rules(i)
            if not rs["result"]:
                raise SyncResourceDataError("同步安全组规则数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
            res_data.extend(rs["data"])
        self.sync_resource(SecurityGroupRule, self.account, res_data)

    def sync_private_storage(self):
        rs = self.client.list_private_storages()
        if not rs["result"]:
            raise SyncResourceDataError("同步本地存储数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(PrivateStorage, self.account, rs["data"])

    def sync_bucket(self):
        rs = self.client.list_buckets()
        if not rs["result"]:
            raise SyncResourceDataError("同步存储桶数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(Bucket, self.account, rs["data"])
        self.sync_bucket_file([(item["resource_name"], item["region"]) for item in rs["data"]])

    def sync_bucket_file(self, bucket_list):
        res_data = []
        for bucket_tuple in bucket_list:
            rs = self.client.list_bucket_file(bucket_name=bucket_tuple[0], location=bucket_tuple[1])
            if not rs["result"]:
                raise SyncResourceDataError("同步存储桶文件表数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
            res_data.extend(rs["data"])
        self.sync_resource(BucketFile, self.account, res_data)

    def sync_auto_snapshot_policy(self):
        rs = self.client.list_auto_snapshot_policy()
        if not rs["result"]:
            raise SyncResourceDataError("同步快照数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(SnapshotPolicy, self.account, rs["data"])

    def sync_route_tables(self):
        rs = self.client.list_route_tables()
        if not rs["result"]:
            raise SyncResourceDataError("同步路由表数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(RouteTable, self.account, rs["data"])
        self.sync_route_entry([item["resource_id"] for item in rs["data"]])

    def sync_route_entry(self, route_table_ids):
        res_data = []
        for i in route_table_ids:
            rs = self.client.list_route_entry(RouteTableId=i)
            if not rs["result"]:
                raise SyncResourceDataError("同步路由策略表数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
            res_data.extend(rs["data"])
        self.sync_resource(RouteEntry, self.account, res_data)

    def sync_load_balancer(self):
        rs = self.client.list_load_balancers()
        if not rs["result"]:
            raise SyncResourceDataError("同步负载均衡表数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(LoadBalancer, self.account, rs["data"])
        self.sync_vserver_groups([item["resource_id"] for item in rs["data"]])
        self.sync_rule(rs["data"])

    def sync_listener(self, load_balancer_id=None, cloud_type=None):
        rs = self.client.list_listeners()
        if not rs["result"]:
            raise SyncResourceDataError("同步负载均衡监听表数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(LoadBalancerListener, self.account, rs["data"])

    def sync_vserver_groups(self, load_balancer_ids):
        ret_data = []
        for i in load_balancer_ids:
            rs = self.client.list_vserver_groups(load_balancer_id=i)
            if not rs["result"]:
                raise SyncResourceDataError("同步虚拟服务器组数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
            ret_data.extend(rs["data"])
        self.sync_resource(ServerGroup, self.account, ret_data)

    def sync_rule(self, load_balancers):
        res_data = []
        for load_balancer in load_balancers:
            ports = load_balancer.get("port", [])
            for port in ports:
                kwargs = {
                    "LoadBalancerId": load_balancer["resource_id"],
                    "ListenerPort": port.get("ListenerPort"),
                    "ListenerProtocal": port.get("ListenerProtocal"),
                }
                rs = self.client.list_rules(**kwargs)
                if not rs["result"]:
                    raise SyncResourceDataError(
                        "同步转发规则表数据失败[{}: {}]".format(self.account.config_name, rs.get("message"))
                    )
                res_data.extend(rs["data"])
        self.sync_resource(RelayRule, self.account, res_data)

    def sync_server_certificates(self):
        rs = self.client.list_server_certificates()
        if not rs["result"]:
            raise SyncResourceDataError("同步服务器证书表数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(ServerCertificate, self.account, rs["data"])

    def sync_file_system(self):
        rs = self.client.list_file_system()
        if not rs["result"]:
            raise SyncResourceDataError("同步文件存储表数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(FileSystem, self.account, rs["data"])

    def sync_application(self):
        rs = self.client.list_applications()
        if not rs["result"]:
            raise SyncResourceDataError("同步文件存储表数据失败[{}: {}]".format(self.account.config_name, rs.get("message")))
        self.sync_resource(Application, self.account, rs["data"])

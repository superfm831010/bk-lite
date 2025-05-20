# -*- coding: utf-8 -*-
"""同步tdsql资源"""
from common.cmp.cloud_apis.constant import CloudResourceType
from common.cmp.cloud_apis.resource_apis.sync_cloud_resource.cloud_resource import SyncPrivateCloudResource
from common.cmp.exceptions import SyncResourceDataError
from common.cmp.models import TDSQL


class SyncTDSQLResource(SyncPrivateCloudResource):
    def __init__(self, client, account):
        super().__init__(client, account)
        self.resource_list = [CloudResourceType.TDSQL.value]
        # self.resource_list.extend([
        #     CloudResourceType.TDSQL.value
        #     # 实例 —— 分布式、非分布式
        #     # CloudResourceType.REDIS.value,
        #     # CloudResourceType.FILE_SYSTEM.value,
        #     # CloudResourceType.LOAD_BALANCER.value,
        #     # # CloudResourceType.PRIVATE_BUCKET.value,
        #     # CloudResourceType.TDSQL.value,
        #     # CloudResourceType.MARIADB.value,
        #     # CloudResourceType.INSTANCE_TYPE.value,
        #     # CloudResourceType.INSTANCE_TYPE_FAMILY.value,
        # ])

    def sync_tdsql(self, ids=None):
        instance_data = []
        # 非分布式
        rs = self.client.list_noshard(instance_array=ids)  # 非分布式
        if not rs["result"]:
            raise SyncResourceDataError(
                "同步TDSQL(非分布式实例)数据失败[{}: {}]".format(self.account.config_name, rs.get("message"))
            )
        instance_data.extend(rs["data"])
        # 分布式
        rs = self.client.list_groupshard(groups_array=ids)
        if not rs["result"]:
            raise SyncResourceDataError(
                "同步TDSQL(分布式实例)数据失败[{}: {}]".format(self.account.config_name, rs.get("message"))
            )
        instance_data.extend(rs["data"])
        # 同步数据至数据库中
        self.sync_resource(TDSQL, self.account, instance_data)

    # 测试用
    # def get_db_params(self, group_id="", set_id=""):
    #     res = self.client.list_config()
    #
    # def set_db_params(self, config=[], group_id="", set_id=""):
    #     config = [
    #         {"param":"auto_increment_increment",  "value": "100"}
    #     ]
    #     set_id = "set_1622084502_83"
    #     res = self.client.modify_config(config, group_id, set_id)
    #     print(res)

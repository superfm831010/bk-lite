# -*- coding: utf-8 -*-
from common.cmp.cloud_apis.resource_apis.resource_format.tdsql.tdsql_constant import (
    TDSQLInstanceStatus,
    TDSQLReadStatus,
    TDSQLStatus,
)


def format_instance_status(status):
    if status == TDSQLInstanceStatus.RUNNING.value:
        return TDSQLStatus.RUNNING.value
    elif status == TDSQLInstanceStatus.QUARANTINED.value:
        return TDSQLStatus.QUARANTINED.value
    elif status == TDSQLInstanceStatus.UNINITIALIZED.value:
        return TDSQLStatus.UNINITIALIZED.value
    else:
        # 返回状态不合法
        # raise Exception("获取到未纳入本地的TDSQL实例状态{}，无法归类，请查看并修改".format(status))
        return TDSQLStatus.UNKNOWN.value


def format_readonly_status(flag):
    if flag == TDSQLReadStatus.READ_WRITE.value:
        return "读写状态"
    else:
        return "只读"

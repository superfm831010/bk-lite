# -*- coding: utf-8 -*-
"""TDSQL各种状态和Model中的状态双向映射"""
from enum import Enum

from common.cmp.models import TDSQL


class TDSQLStatus(Enum):
    # (CREATING, "创建中"),
    # (PROCESSING, "流程处理中"),
    # (RUNNING, "运行中"),
    # (UNINITIALIZED, "未初始化"),
    # (QUARANTINED, "已隔离"),
    # (DELETED, "已删除"),
    RUNNING = TDSQL.RUNNING
    QUARANTINED = TDSQL.QUARANTINED
    UNINITIALIZED = TDSQL.UNINITIALIZED
    UNKNOWN = TDSQL.UNKNOWN


class TDSQLInstanceStatus(Enum):
    RUNNING = 0
    QUARANTINED = 1
    UNINITIALIZED = 2


class TDSQLReadStatus(Enum):
    READ_WRITE = "0"
    READ_ONLY = "1"

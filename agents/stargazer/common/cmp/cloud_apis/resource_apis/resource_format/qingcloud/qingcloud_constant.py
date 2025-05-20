"""青云属性枚举"""
from enum import Enum


class QingCloudDiskStatus(Enum):
    AVAILABLE = "available"
    RUNNING = "in-use"
    PENDING = "pending"
    SUSPENDED = "suspended"
    DELETED = "deleted"
    CEASED = "ceased"

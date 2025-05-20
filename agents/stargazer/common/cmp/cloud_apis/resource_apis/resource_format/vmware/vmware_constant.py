# -*- coding: utf-8 -*-
"""VmWare各种状态和Model中的状态双向映射"""
from enum import Enum

from common.cmp.models import VPC, Disk, Image, Snapshot, Subnet


class VmwareImageStatus(Enum):
    AVAILABLE = Image.AVAILABLE


class VmwareImageType(Enum):
    PRIVATE = Image.PRIVATE
    PUBLIC = Image.PUBLIC


class VmwareDiskStatus(Enum):
    ATTACHED = Disk.ATTACHED


class VmwareDiskType(Enum):
    SYSTEM_DISK = Disk.SYSTEM_DISK
    DATA_DISK = Disk.DATA_DISK


class VmwareSnapshotStatus(Enum):
    AVAILABLE = Snapshot.AVAILABLE


class VmwareSnapshotType(Enum):
    VM_SNAPSHOT = Snapshot.VM_SNAPSHOT


class VmwareSubnetStatus(Enum):
    AVAILABLE = Subnet.AVAILABLE


class VmwareVPCStatus(Enum):
    AVAILABLE = VPC.AVAILABLE


class VmwareInstanceStatus(Enum):
    RUNNING = "poweredOn"
    STOPPING = "poweredOff"
    SUSPEND = "suspended"


class VmwareStatus(Enum):
    RUNNING = "RUNNING"
    STOP = "STOP"
    PENDING = "PENDING"

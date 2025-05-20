from enum import Enum


class AmazonAwsRegionStatus(Enum):
    OPT_IN_NOT_REQUIRED = "opt-in-not-required"
    OPTED_IN = "opted-in"
    NOT_OPTED_IN = "not-opted-in"


class AmazonAwsZoneState(Enum):
    AVAILABLE = "available"
    INFORMATION = "information"
    IMPAIRED = "impaired"
    UNAVAILABLE = "unavailable"


class AmazonAwsVMStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SHUTTING_DOWN = "shutting-down"
    TERMINATED = "terminated"
    STOPPING = "stopping"
    STOPPED = "stopped"


class AmazonAwsVolumeStatus(Enum):
    CREATING = "creating"
    AVAILABLE = "available"
    IN_USE = "in-use"
    DELETING = "deleting"
    DELETED = "deleted"
    ERROR = "error"


class AmazonAwsAttachStatus(Enum):
    ATTACHING = "attaching"
    ATTACHED = "attached"
    DETACHING = "detaching"
    DETACHED = "detached"
    BUSY = "busy"


class AmazonAwsVolumeType(Enum):
    STANDARD = "standard"  # 上一代卷类型，所有类别中性能最差
    STANDARD_cn = "最低性能过代磁盘"

    IO1 = "io1"  # 高性能 SSD 持久性低于 io2
    IO1_cn = "EBS 预置 IOPS SSD"

    IO2 = "io2"  # 高性能 SSD
    IO2_cn = "EBS 预置 IOPS SSD(pro)"

    GP2 = "gp2"  # 通用型 SSD 吞吐量小于gp3
    GP2_cn = "EBS 通用型 SSD"

    GP3 = "gp3"  # 通用型 SSD
    GP3_cn = "EBS 最低成本型 SSD"

    SC1 = "sc1"  # Cold HDD – 适用于访问频率较低的工作负载的最低成本 HDD。
    SC1_cn = "冷存储HDD"

    ST1 = "st1"  # 吞吐量优化型 HDD – 适用于访问频率较高的吞吐量密集型工作负载的低成本 HDD。
    ST1_cn = "吞吐量优化型HDD"


class AmazonAwsVpcState(Enum):
    PENDING = "pending"
    AVAILABLE = "available"


class AmazonAwsSubnetState(Enum):
    PENDING = "pending"
    AVAILABLE = "available"


class AmazonAwsSnapshotStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    ERROR = "error"
    RECOVERABLE = "recoverable"
    RECOVERING = "recovering"
    AVAILABLE = "available"


class AmazonAwsImageState(Enum):
    PENDING = "pending"
    AVAILABLE = "available"
    INVALID = "invalid"
    DEREGISTERED = "deregistered"
    TRANSIENT = "transient"
    FAILED = "failed"
    ERROR = "error"


class AmazonAwsImageType(Enum):
    MACHINE = "machine"
    KERNEL = "kernel"
    RAMDISK = "ramdisk"


class AwsSecurityGroupRuleDirection(Enum):
    INGRESS = "true"
    EGRESS = "false"


class AwsSecurityGroupRuleProtocol(Enum):
    TCP = "6"
    UDP = "17"
    ICMP = "1"
    ICMPv6 = "58"
    ALL = "-1"

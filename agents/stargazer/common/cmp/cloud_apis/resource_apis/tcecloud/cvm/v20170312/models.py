# -*- coding: utf8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from common.cmp.cloud_apis.resource_apis.tcecloud.common.abstract_model import AbstractModel


class ActionTimer(AbstractModel):
    """定时任务"""

    def __init__(self):
        """
        :param Externals: 扩展数据
        :type Externals: :class:`tcecloud.cvm.v20170312.models.Externals`
        :param TimerAction: 定时器
        :type TimerAction: str
        :param ActionTime: 执行时间
        :type ActionTime: str
        """
        self.Externals = None
        self.TimerAction = None
        self.ActionTime = None

    def _deserialize(self, params):
        if params.get("Externals") is not None:
            self.Externals = Externals()
            self.Externals._deserialize(params.get("Externals"))
        self.TimerAction = params.get("TimerAction")
        self.ActionTime = params.get("ActionTime")


class Address(AbstractModel):
    """描述 EIP 信息"""

    def __init__(self):
        """
        :param AddressId: `EIP`的`ID`，是`EIP`的唯一标识。
        :type AddressId: str
        :param AddressName: `EIP`名称。
        :type AddressName: str
        :param AddressState: `EIP`状态。
        :type AddressState: str
        :param AddressIp: 弹性外网IP
        :type AddressIp: str
        :param BindedResourceId: 绑定的资源实例`ID`。可能是一个`CVM`，`NAT`，或是弹性网卡。
        :type BindedResourceId: str
        :param CreatedTime: 创建时间。按照`ISO8601`标准表示，并且使用`UTC`时间。格式为：`YYYY-MM-DDThh:mm:ssZ`。
        :type CreatedTime: str
        """
        self.AddressId = None
        self.AddressName = None
        self.AddressState = None
        self.AddressIp = None
        self.BindedResourceId = None
        self.CreatedTime = None

    def _deserialize(self, params):
        self.AddressId = params.get("AddressId")
        self.AddressName = params.get("AddressName")
        self.AddressState = params.get("AddressState")
        self.AddressIp = params.get("AddressIp")
        self.BindedResourceId = params.get("BindedResourceId")
        self.CreatedTime = params.get("CreatedTime")


class AddressChargePrepaid(AbstractModel):
    """用于描述弹性公网IP的费用对象"""

    def __init__(self):
        """
        :param Period: 购买实例的时长
        :type Period: int
        :param RenewFlag: 自动续费标志
        :type RenewFlag: str
        """
        self.Period = None
        self.RenewFlag = None

    def _deserialize(self, params):
        self.Period = params.get("Period")
        self.RenewFlag = params.get("RenewFlag")


class AllocateAddressesRequest(AbstractModel):
    """AllocateAddresses请求参数结构体"""

    def __init__(self):
        """
        :param AddressCount: 1
        :type AddressCount: int
        :param IspId: 1
        :type IspId: int
        :param IspName: 1
        :type IspName: str
        :param VipSet: 1
        :type VipSet: list of str
        :param TgwGroup: 1
        :type TgwGroup: str
        :param ApplySilence: 1
        :type ApplySilence: int
        :param InternetChargeType: 1
        :type InternetChargeType: str
        :param InternetMaxBandwidthOut: 1
        :type InternetMaxBandwidthOut: int
        :param AddressChargePrepaid: 1
        :type AddressChargePrepaid: :class:`tcecloud.cvm.v20170312.models.AddressChargePrepaid`
        :param DealId: 1
        :type DealId: str
        """
        self.AddressCount = None
        self.IspId = None
        self.IspName = None
        self.VipSet = None
        self.TgwGroup = None
        self.ApplySilence = None
        self.InternetChargeType = None
        self.InternetMaxBandwidthOut = None
        self.AddressChargePrepaid = None
        self.DealId = None

    def _deserialize(self, params):
        self.AddressCount = params.get("AddressCount")
        self.IspId = params.get("IspId")
        self.IspName = params.get("IspName")
        self.VipSet = params.get("VipSet")
        self.TgwGroup = params.get("TgwGroup")
        self.ApplySilence = params.get("ApplySilence")
        self.InternetChargeType = params.get("InternetChargeType")
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        if params.get("AddressChargePrepaid") is not None:
            self.AddressChargePrepaid = AddressChargePrepaid()
            self.AddressChargePrepaid._deserialize(params.get("AddressChargePrepaid"))
        self.DealId = params.get("DealId")


class AllocateAddressesResponse(AbstractModel):
    """AllocateAddresses返回参数结构体"""

    def __init__(self):
        """
        :param AddressSet: 申请到的 EIP 的唯一 ID 列表。
        :type AddressSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AddressSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.AddressSet = params.get("AddressSet")
        self.RequestId = params.get("RequestId")


class AllocateHostsRequest(AbstractModel):
    """AllocateHosts请求参数结构体"""

    def __init__(self):
        """
        :param Placement: 实例所在的位置。通过该参数可以指定实例所属可用区，所属项目等属性。
        :type Placement: :class:`tcecloud.cvm.v20170312.models.Placement`
        :param ClientToken: 用于保证请求幂等性的字符串
        :type ClientToken: str
        :param HostChargePrepaid: 预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月实例的购买时长、是否设置自动续费等属性。若指定实例的付费模式为预付费则该参数必传。
        :type HostChargePrepaid: :class:`tcecloud.cvm.v20170312.models.ChargePrepaid`
        :param HostChargeType: 实例计费类型。目前仅支持：PREPAID（预付费，即包年包月模式）。
        :type HostChargeType: str
        :param HostType: CDH实例机型
        :type HostType: str
        :param HostCount: 购买CDH实例数量
        :type HostCount: int
        :param DryRun: 是否跳过实际执行逻辑
        :type DryRun: bool
        :param PurchaseSource: 购买来源
        :type PurchaseSource: str
        """
        self.Placement = None
        self.ClientToken = None
        self.HostChargePrepaid = None
        self.HostChargeType = None
        self.HostType = None
        self.HostCount = None
        self.DryRun = None
        self.PurchaseSource = None

    def _deserialize(self, params):
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        self.ClientToken = params.get("ClientToken")
        if params.get("HostChargePrepaid") is not None:
            self.HostChargePrepaid = ChargePrepaid()
            self.HostChargePrepaid._deserialize(params.get("HostChargePrepaid"))
        self.HostChargeType = params.get("HostChargeType")
        self.HostType = params.get("HostType")
        self.HostCount = params.get("HostCount")
        self.DryRun = params.get("DryRun")
        self.PurchaseSource = params.get("PurchaseSource")


class AllocateHostsResponse(AbstractModel):
    """AllocateHosts返回参数结构体"""

    def __init__(self):
        """
        :param HostIdSet: 新创建云子机的实例id列表。
        :type HostIdSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.HostIdSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.HostIdSet = params.get("HostIdSet")
        self.RequestId = params.get("RequestId")


class AssociateAddressRequest(AbstractModel):
    """AssociateAddress请求参数结构体"""

    def __init__(self):
        """
        :param AddressId: 1
        :type AddressId: str
        :param InstanceId: 1
        :type InstanceId: str
        :param NetworkInterfaceId: 1
        :type NetworkInterfaceId: str
        :param PrivateIpAddress: 1
        :type PrivateIpAddress: str
        """
        self.AddressId = None
        self.InstanceId = None
        self.NetworkInterfaceId = None
        self.PrivateIpAddress = None

    def _deserialize(self, params):
        self.AddressId = params.get("AddressId")
        self.InstanceId = params.get("InstanceId")
        self.NetworkInterfaceId = params.get("NetworkInterfaceId")
        self.PrivateIpAddress = params.get("PrivateIpAddress")


class AssociateAddressResponse(AbstractModel):
    """AssociateAddress返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AssociateInstancesKeyPairsRequest(AbstractModel):
    """AssociateInstancesKeyPairs请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 一个或多个待操作的实例ID，每次请求批量实例的上限为100。<br><br>可以通过以下方式获取可用的实例ID：<br><li>通过登录控制台查询实例ID。<br><li>通过调用接口 DescribeInstances ，取返回信息中的`InstanceId`获取实例ID。
        :type InstanceIds: list of str
        :param KeyIds: 一个或多个待操作的密钥对ID，每次请求批量密钥对的上限为100。密钥对ID形如：`skey-11112222`。<br><br>可以通过以下方式获取可用的密钥ID：<br><li>通过登录控制台查询密钥ID。<br><li>通过调用接口 DescribeKeyPairs ，取返回信息中的`KeyId`获取密钥对ID。
        :type KeyIds: list of str
        :param ForceStop: 是否对运行中的实例选择强制关机。建议对运行中的实例先手动关机，然后再重置用户密码。取值范围：<br><li>TRUE：表示在正常关机失败后进行强制关机。<br><li>FALSE：表示在正常关机失败后不进行强制关机。<br><br>默认取值：FALSE。
        :type ForceStop: bool
        """
        self.InstanceIds = None
        self.KeyIds = None
        self.ForceStop = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.KeyIds = params.get("KeyIds")
        self.ForceStop = params.get("ForceStop")


class AssociateInstancesKeyPairsResponse(AbstractModel):
    """AssociateInstancesKeyPairs返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AssociateSecurityGroupsRequest(AbstractModel):
    """AssociateSecurityGroups请求参数结构体"""

    def __init__(self):
        """
        :param SecurityGroupIds: 1
        :type SecurityGroupIds: list of str
        :param InstanceIds: 1
        :type InstanceIds: list of str
        """
        self.SecurityGroupIds = None
        self.InstanceIds = None

    def _deserialize(self, params):
        self.SecurityGroupIds = params.get("SecurityGroupIds")
        self.InstanceIds = params.get("InstanceIds")


class AssociateSecurityGroupsResponse(AbstractModel):
    """AssociateSecurityGroups返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AuditMarketImageRequest(AbstractModel):
    """AuditMarketImage请求参数结构体"""

    def __init__(self):
        """
        :param ItemId: 1
        :type ItemId: int
        :param ImageId: 1
        :type ImageId: str
        """
        self.ItemId = None
        self.ImageId = None

    def _deserialize(self, params):
        self.ItemId = params.get("ItemId")
        self.ImageId = params.get("ImageId")


class AuditMarketImageResponse(AbstractModel):
    """AuditMarketImage返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CancelAuditMarketImageRequest(AbstractModel):
    """CancelAuditMarketImage请求参数结构体"""

    def __init__(self):
        """
        :param ItemId: 1
        :type ItemId: int
        :param ImageId: 1
        :type ImageId: str
        """
        self.ItemId = None
        self.ImageId = None

    def _deserialize(self, params):
        self.ItemId = params.get("ItemId")
        self.ImageId = params.get("ImageId")


class CancelAuditMarketImageResponse(AbstractModel):
    """CancelAuditMarketImage返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ChargePrepaid(AbstractModel):
    """描述预付费模式，即包年包月相关参数。包括购买时长和自动续费逻辑等。"""

    def __init__(self):
        """
        :param Period: 购买实例的时长，单位：月。取值范围：1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 24, 36。
        :type Period: int
        :param RenewFlag: 自动续费标识。取值范围：<br><li>NOTIFY_AND_AUTO_RENEW：通知过期且自动续费<br><li>NOTIFY_AND_MANUAL_RENEW：通知过期不自动续费<br><li>DISABLE_NOTIFY_AND_MANUAL_RENEW：不通知过期不自动续费<br><br>默认取值：NOTIFY_AND_AUTO_RENEW。若该参数指定为NOTIFY_AND_AUTO_RENEW，在账户余额充足的情况下，实例到期后将按月自动续费。
        :type RenewFlag: str
        """
        self.Period = None
        self.RenewFlag = None

    def _deserialize(self, params):
        self.Period = params.get("Period")
        self.RenewFlag = params.get("RenewFlag")


class CheckInstancesConnectivityRequest(AbstractModel):
    """CheckInstancesConnectivity请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 1
        :type InstanceIds: list of str
        """
        self.InstanceIds = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")


class CheckInstancesConnectivityResponse(AbstractModel):
    """CheckInstancesConnectivity返回参数结构体"""

    def __init__(self):
        """
        :param InstanceConnectivitySet: 实例连通性结果集合。
        :type InstanceConnectivitySet: list of InstanceConnectivity
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceConnectivitySet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("InstanceConnectivitySet") is not None:
            self.InstanceConnectivitySet = []
            for item in params.get("InstanceConnectivitySet"):
                obj = InstanceConnectivity()
                obj._deserialize(item)
                self.InstanceConnectivitySet.append(obj)
        self.RequestId = params.get("RequestId")


class ClientSysInfo(AbstractModel):
    """用于热迁移时传递客户端系统信息。"""

    def __init__(self):
        """
        :param OsType: 操作系统
        :type OsType: str
        :param OsVersion: 操作系统版本
        :type OsVersion: str
        :param DiskSize: 需要导入的系统盘数据盘信息
        :type DiskSize: list of int non-negative
        :param ExtraInfo: 额外信息
        :type ExtraInfo: str
        """
        self.OsType = None
        self.OsVersion = None
        self.DiskSize = None
        self.ExtraInfo = None

    def _deserialize(self, params):
        self.OsType = params.get("OsType")
        self.OsVersion = params.get("OsVersion")
        self.DiskSize = params.get("DiskSize")
        self.ExtraInfo = params.get("ExtraInfo")


class ColdMigrateInstanceRequest(AbstractModel):
    """ColdMigrateInstance请求参数结构体"""

    def __init__(self):
        """
        :param ImageUrl: 迁移的系统盘镜像COS链接
        :type ImageUrl: str
        :param InstanceId: 迁移目的实例ID。迁移完成后，该实例将运行迁入的操作系统。
        :type InstanceId: str
        :param JobName: 任务名称，用于在控制台展示。
        :type JobName: str
        :param DryRun: 用于测试参数合法性。默认为`false`
        :type DryRun: bool
        """
        self.ImageUrl = None
        self.InstanceId = None
        self.JobName = None
        self.DryRun = None

    def _deserialize(self, params):
        self.ImageUrl = params.get("ImageUrl")
        self.InstanceId = params.get("InstanceId")
        self.JobName = params.get("JobName")
        self.DryRun = params.get("DryRun")


class ColdMigrateInstanceResponse(AbstractModel):
    """ColdMigrateInstance返回参数结构体"""

    def __init__(self):
        """
        :param JobId: 任务ID，用于查询任务状态、进度。
        :type JobId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.JobId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.JobId = params.get("JobId")
        self.RequestId = params.get("RequestId")


class ColdMigrateRequest(AbstractModel):
    """ColdMigrate请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 待迁移的实例Id如："ins-38d920cd"
        :type InstanceId: str
        :param HostIps: 目标母机数组
        :type HostIps: list of str
        :param SoldPool: 要嵌入的售卖池，默认不变更
        :type SoldPool: str
        :param Zones: 需要跨可用迁移，可传入可用区列表
        :type Zones: list of str
        :param MaxBandwidth: 最大迁移带宽
        :type MaxBandwidth: int
        :param MaxTimeout: 最大迁移超时
        :type MaxTimeout: int
        :param HostNameReserved: 是否保留hostname
        :type HostNameReserved: bool
        """
        self.InstanceId = None
        self.HostIps = None
        self.SoldPool = None
        self.Zones = None
        self.MaxBandwidth = None
        self.MaxTimeout = None
        self.HostNameReserved = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.HostIps = params.get("HostIps")
        self.SoldPool = params.get("SoldPool")
        self.Zones = params.get("Zones")
        self.MaxBandwidth = params.get("MaxBandwidth")
        self.MaxTimeout = params.get("MaxTimeout")
        self.HostNameReserved = params.get("HostNameReserved")


class ColdMigrateResponse(AbstractModel):
    """ColdMigrate返回参数结构体"""

    def __init__(self):
        """
        :param TaskId: 任务Id
        :type TaskId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class CopyInstanceDiskRequest(AbstractModel):
    """CopyInstanceDisk请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 1
        :type InstanceId: str
        :param DestinationDiskId: 1
        :type DestinationDiskId: str
        :param SourceDiskId: 1
        :type SourceDiskId: str
        """
        self.InstanceId = None
        self.DestinationDiskId = None
        self.SourceDiskId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.DestinationDiskId = params.get("DestinationDiskId")
        self.SourceDiskId = params.get("SourceDiskId")


class CopyInstanceDiskResponse(AbstractModel):
    """CopyInstanceDisk返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateDisasterRecoverGroupRequest(AbstractModel):
    """CreateDisasterRecoverGroup请求参数结构体"""

    def __init__(self):
        """
        :param Name: 分散置放群组名称，长度1-60个字符，支持中、英文。
        :type Name: str
        :param Type: 分散置放群组类型，取值范围：<br><li>HOST：物理机<br><li>SW：交换机<br><li>RACK：机架
        :type Type: str
        """
        self.Name = None
        self.Type = None

    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Type = params.get("Type")


class CreateDisasterRecoverGroupResponse(AbstractModel):
    """CreateDisasterRecoverGroup返回参数结构体"""

    def __init__(self):
        """
        :param DisasterRecoverGroupId: 容灾组id。
        :type DisasterRecoverGroupId: str
        :param Type: 容灾组类型，与入参一致。
        :type Type: str
        :param Name: 分散置放群组名称，长度1-60个字符，支持中、英文。
        :type Name: str
        :param CvmQuotaTotal: 置放群组内可容纳的云服务器数量。
        :type CvmQuotaTotal: int
        :param CurrentNum: 置放群组内已有的云服务器数量。
        :type CurrentNum: int
        :param CreateTime: 置放群组创建时间。
        :type CreateTime: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DisasterRecoverGroupId = None
        self.Type = None
        self.Name = None
        self.CvmQuotaTotal = None
        self.CurrentNum = None
        self.CreateTime = None
        self.RequestId = None

    def _deserialize(self, params):
        self.DisasterRecoverGroupId = params.get("DisasterRecoverGroupId")
        self.Type = params.get("Type")
        self.Name = params.get("Name")
        self.CvmQuotaTotal = params.get("CvmQuotaTotal")
        self.CurrentNum = params.get("CurrentNum")
        self.CreateTime = params.get("CreateTime")
        self.RequestId = params.get("RequestId")


class CreateImageRequest(AbstractModel):
    """CreateImage请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 需要制作镜像的实例ID
        :type InstanceId: str
        :param ImageName: 镜像名称
        :type ImageName: str
        :param ImageDescription: 镜像描述
        :type ImageDescription: str
        :param ForcePoweroff: 软关机失败时是否执行强制关机以制作镜像
        :type ForcePoweroff: str
        :param Sysprep: 创建Windows镜像时是否启用Sysprep
        :type Sysprep: str
        :param Reboot: 实例处于运行中时，是否允许关机执行制作镜像任务。
        :type Reboot: str
        """
        self.InstanceId = None
        self.ImageName = None
        self.ImageDescription = None
        self.ForcePoweroff = None
        self.Sysprep = None
        self.Reboot = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.ImageName = params.get("ImageName")
        self.ImageDescription = params.get("ImageDescription")
        self.ForcePoweroff = params.get("ForcePoweroff")
        self.Sysprep = params.get("Sysprep")
        self.Reboot = params.get("Reboot")


class CreateImageResponse(AbstractModel):
    """CreateImage返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateKeyPairRequest(AbstractModel):
    """CreateKeyPair请求参数结构体"""

    def __init__(self):
        """
        :param KeyName: 密钥对名称，可由数字，字母和下划线组成，长度不超过25个字符。
        :type KeyName: str
        :param ProjectId: 密钥对创建后所属的项目ID。<br><br>可以通过以下方式获取项目ID：<br><li>通过项目列表查询项目ID。<br><li>通过调用接口 DescribeProject ，取返回信息中的`projectId `获取项目ID。
        :type ProjectId: int
        """
        self.KeyName = None
        self.ProjectId = None

    def _deserialize(self, params):
        self.KeyName = params.get("KeyName")
        self.ProjectId = params.get("ProjectId")


class CreateKeyPairResponse(AbstractModel):
    """CreateKeyPair返回参数结构体"""

    def __init__(self):
        """
        :param KeyPair: 密钥对信息。
        :type KeyPair: :class:`tcecloud.cvm.v20170312.models.KeyPair`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.KeyPair = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("KeyPair") is not None:
            self.KeyPair = KeyPair()
            self.KeyPair._deserialize(params.get("KeyPair"))
        self.RequestId = params.get("RequestId")


class DataDisk(AbstractModel):
    """描述了数据盘的信息"""

    def __init__(self):
        """
                :param DiskSize: 数据盘大小，单位：GB。最小调整步长为10G，不同数据盘类型取值范围不同，具体限制详见：CVM实例配置。默认值为0，表示不购买数据盘。更多限制详见产品文档。
                :type DiskSize: int
                :param DiskType: 数据盘类型。数据盘类型限制详见CVM实例配置。取值范围：<br><li>LOCAL_BASIC：本地硬盘<br><li>LOCAL_SSD：本地SSD硬盘<br><li>CLOUD_BASIC：普通云硬盘<br><li>CLOUD_PREMIUM：高性能云硬盘<br><li>CLOUD_SSD：SSD云硬盘<br><br>默认取值：LOCAL_BASIC。<br><br>该参数对`ResizeInstanceDisk`接口无效。
                :type DiskType: str
                :param DiskId: 系统盘ID。LOCAL_BASIC 和 LOCAL_SSD 类型没有ID。暂时不支持该参数。
                :type DiskId: str
                :param DeleteWithInstance: 数据盘是否随子机销毁。取值范围：
        <li>TRUE：子机销毁时，销毁数据盘，只支持按小时后付费云盘
        <li>FALSE：子机销毁时，保留数据盘<br>
        默认取值：TRUE<br>
        该参数目前仅用于 `RunInstances` 接口。
        注意：此字段可能返回 null，表示取不到有效值。
                :type DeleteWithInstance: bool
                :param DiskStoragePoolGroup: 数据盘指定的存储池。
        注意：此字段可能返回 null，表示取不到有效值。
                :type DiskStoragePoolGroup: str
        """
        self.DiskSize = None
        self.DiskType = None
        self.DiskId = None
        self.DeleteWithInstance = None
        self.DiskStoragePoolGroup = None

    def _deserialize(self, params):
        self.DiskSize = params.get("DiskSize")
        self.DiskType = params.get("DiskType")
        self.DiskId = params.get("DiskId")
        self.DeleteWithInstance = params.get("DeleteWithInstance")
        self.DiskStoragePoolGroup = params.get("DiskStoragePoolGroup")


class DataDisks(AbstractModel):
    """数据盘镜像描述，包括镜像cos url，数据盘大小，数据盘设备名(DiskId)；"""

    def __init__(self):
        """
        :param ImageUrl: 数据盘镜像cos url
        :type ImageUrl: str
        :param Size: 数据盘大小
        :type Size: int
        :param Device: 数据盘对应设备名，目前是DiskId
        :type Device: str
        """
        self.ImageUrl = None
        self.Size = None
        self.Device = None

    def _deserialize(self, params):
        self.ImageUrl = params.get("ImageUrl")
        self.Size = params.get("Size")
        self.Device = params.get("Device")


class DeleteDisasterRecoverGroupRequest(AbstractModel):
    """DeleteDisasterRecoverGroup请求参数结构体"""

    def __init__(self):
        """
        :param DisasterRecoverGroupIds: 容灾组id列表，可通过DescribeDisasterRecoverGroups接口查询。
        :type DisasterRecoverGroupIds: list of str
        """
        self.DisasterRecoverGroupIds = None

    def _deserialize(self, params):
        self.DisasterRecoverGroupIds = params.get("DisasterRecoverGroupIds")


class DeleteDisasterRecoverGroupResponse(AbstractModel):
    """DeleteDisasterRecoverGroup返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteDisasterRecoverGroupsRequest(AbstractModel):
    """DeleteDisasterRecoverGroups请求参数结构体"""

    def __init__(self):
        """
        :param DisasterRecoverGroupIds: 分散置放群组ID列表，可通过DescribeDisasterRecoverGroups接口获取。每次请求允许操作的分散置放群组数量上限是100。
        :type DisasterRecoverGroupIds: list of str
        """
        self.DisasterRecoverGroupIds = None

    def _deserialize(self, params):
        self.DisasterRecoverGroupIds = params.get("DisasterRecoverGroupIds")


class DeleteDisasterRecoverGroupsResponse(AbstractModel):
    """DeleteDisasterRecoverGroups返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteImagesRequest(AbstractModel):
    """DeleteImages请求参数结构体"""

    def __init__(self):
        """
        :param ImageIds: 准备删除的镜像Id列表
        :type ImageIds: list of str
        """
        self.ImageIds = None

    def _deserialize(self, params):
        self.ImageIds = params.get("ImageIds")


class DeleteImagesResponse(AbstractModel):
    """DeleteImages返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteInstancesActionTimerRequest(AbstractModel):
    """DeleteInstancesActionTimer请求参数结构体"""

    def __init__(self):
        """
        :param ActionTimerIds: 1
        :type ActionTimerIds: list of str
        """
        self.ActionTimerIds = None

    def _deserialize(self, params):
        self.ActionTimerIds = params.get("ActionTimerIds")


class DeleteInstancesActionTimerResponse(AbstractModel):
    """DeleteInstancesActionTimer返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteKeyPairsRequest(AbstractModel):
    """DeleteKeyPairs请求参数结构体"""

    def __init__(self):
        """
        :param KeyIds: 一个或多个待操作的密钥对ID。每次请求批量密钥对的上限为100。<br><br>可以通过以下方式获取可用的密钥ID：<br><li>通过登录控制台查询密钥ID。<br><li>通过调用接口 DescribeKeyPairs ，取返回信息中的 `KeyId` 获取密钥对ID。
        :type KeyIds: list of str
        """
        self.KeyIds = None

    def _deserialize(self, params):
        self.KeyIds = params.get("KeyIds")


class DeleteKeyPairsResponse(AbstractModel):
    """DeleteKeyPairs返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeAccountAttributesRequest(AbstractModel):
    """DescribeAccountAttributes请求参数结构体"""

    def __init__(self):
        """
        :param AttributeName: 1
        :type AttributeName: list of str
        """
        self.AttributeName = None

    def _deserialize(self, params):
        self.AttributeName = params.get("AttributeName")


class DescribeAccountAttributesResponse(AbstractModel):
    """DescribeAccountAttributes返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeAddressBandwidthConfigsRequest(AbstractModel):
    """DescribeAddressBandwidthConfigs请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 1
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class DescribeAddressBandwidthConfigsResponse(AbstractModel):
    """DescribeAddressBandwidthConfigs返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeAddressQuotaRequest(AbstractModel):
    """DescribeAddressQuota请求参数结构体"""


class DescribeAddressQuotaResponse(AbstractModel):
    """DescribeAddressQuota返回参数结构体"""

    def __init__(self):
        """
        :param QuotaSet: 账户 EIP 配额信息。
        :type QuotaSet: list of Quota
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.QuotaSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("QuotaSet") is not None:
            self.QuotaSet = []
            for item in params.get("QuotaSet"):
                obj = Quota()
                obj._deserialize(item)
                self.QuotaSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeAddressesRequest(AbstractModel):
    """DescribeAddresses请求参数结构体"""

    def __init__(self):
        """
        :param AddressIds: 1
        :type AddressIds: list of str
        :param Filters: 1
        :type Filters: list of Filter
        :param Offset: 1
        :type Offset: int
        :param Limit: 1
        :type Limit: int
        """
        self.AddressIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.AddressIds = params.get("AddressIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeAddressesResponse(AbstractModel):
    """DescribeAddresses返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的 EIP 数量。
        :type TotalCount: int
        :param AddressSet: EIP 详细信息列表。
        :type AddressSet: list of Address
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.AddressSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("AddressSet") is not None:
            self.AddressSet = []
            for item in params.get("AddressSet"):
                obj = Address()
                obj._deserialize(item)
                self.AddressSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDisasterRecoverGroupQuotaRequest(AbstractModel):
    """DescribeDisasterRecoverGroupQuota请求参数结构体"""


class DescribeDisasterRecoverGroupQuotaResponse(AbstractModel):
    """DescribeDisasterRecoverGroupQuota返回参数结构体"""

    def __init__(self):
        """
        :param GroupQuota: 可创建置放群组数量的上限。
        :type GroupQuota: int
        :param CurrentNum: 当前用户已经创建的置放群组数量。
        :type CurrentNum: int
        :param CvmInHostGroupQuota: 物理机类型容灾组内实例的配额数。
        :type CvmInHostGroupQuota: int
        :param CvmInSwGroupQuota: 交换机类型容灾组内实例的配额数。
        :type CvmInSwGroupQuota: int
        :param CvmInRackGroupQuota: 机架类型容灾组内实例的配额数。
        :type CvmInRackGroupQuota: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.GroupQuota = None
        self.CurrentNum = None
        self.CvmInHostGroupQuota = None
        self.CvmInSwGroupQuota = None
        self.CvmInRackGroupQuota = None
        self.RequestId = None

    def _deserialize(self, params):
        self.GroupQuota = params.get("GroupQuota")
        self.CurrentNum = params.get("CurrentNum")
        self.CvmInHostGroupQuota = params.get("CvmInHostGroupQuota")
        self.CvmInSwGroupQuota = params.get("CvmInSwGroupQuota")
        self.CvmInRackGroupQuota = params.get("CvmInRackGroupQuota")
        self.RequestId = params.get("RequestId")


class DescribeDisasterRecoverGroupsRequest(AbstractModel):
    """DescribeDisasterRecoverGroups请求参数结构体"""

    def __init__(self):
        """
        :param DisasterRecoverGroupIds: 容灾组id列表。
        :type DisasterRecoverGroupIds: list of str
        :param Name: 容灾组名称，支持模糊匹配。
        :type Name: str
        :param Offset: 偏移量，默认为0。关于`Offset`的更进一步介绍请参考 API 简介中的相关小节。
        :type Offset: int
        :param Limit: 返回数量，默认为20，最大值为100。关于`Limit`的更进一步介绍请参考 API 简介中的相关小节。
        :type Limit: int
        """
        self.DisasterRecoverGroupIds = None
        self.Name = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.DisasterRecoverGroupIds = params.get("DisasterRecoverGroupIds")
        self.Name = params.get("Name")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeDisasterRecoverGroupsResponse(AbstractModel):
    """DescribeDisasterRecoverGroups返回参数结构体"""

    def __init__(self):
        """
        :param DisasterRecoverGroupSet: 容灾组信息列表
        :type DisasterRecoverGroupSet: list of DisasterRecoverGroup
        :param TotalCount: 用户置放群组总量。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DisasterRecoverGroupSet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("DisasterRecoverGroupSet") is not None:
            self.DisasterRecoverGroupSet = []
            for item in params.get("DisasterRecoverGroupSet"):
                obj = DisasterRecoverGroup()
                obj._deserialize(item)
                self.DisasterRecoverGroupSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeHostsRequest(AbstractModel):
    """DescribeHosts请求参数结构体"""

    def __init__(self):
        """
        :param Filters: 过滤条件。
        :type Filters: list of Filter
        :param Offset: 偏移量，默认为0。
        :type Offset: int
        :param Limit: 返回数量，默认为20，最大值为100。
        :type Limit: int
        """
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeHostsResponse(AbstractModel):
    """DescribeHosts返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合查询条件的cdh实例总数
        :type TotalCount: int
        :param HostSet: cdh实例详细信息列表
        :type HostSet: list of HostItem
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.HostSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("HostSet") is not None:
            self.HostSet = []
            for item in params.get("HostSet"):
                obj = HostItem()
                obj._deserialize(item)
                self.HostSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeImageQuotaRequest(AbstractModel):
    """DescribeImageQuota请求参数结构体"""


class DescribeImageQuotaResponse(AbstractModel):
    """DescribeImageQuota返回参数结构体"""

    def __init__(self):
        """
        :param ImageNumQuota: 账户的镜像配额
        :type ImageNumQuota: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ImageNumQuota = None
        self.RequestId = None

    def _deserialize(self, params):
        self.ImageNumQuota = params.get("ImageNumQuota")
        self.RequestId = params.get("RequestId")


class DescribeImageSharePermissionRequest(AbstractModel):
    """DescribeImageSharePermission请求参数结构体"""

    def __init__(self):
        """
        :param ImageId: 需要共享的镜像Id
        :type ImageId: str
        """
        self.ImageId = None

    def _deserialize(self, params):
        self.ImageId = params.get("ImageId")


class DescribeImageSharePermissionResponse(AbstractModel):
    """DescribeImageSharePermission返回参数结构体"""

    def __init__(self):
        """
        :param SharePermissionSet: 镜像共享信息
        :type SharePermissionSet: list of SharePermission
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SharePermissionSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("SharePermissionSet") is not None:
            self.SharePermissionSet = []
            for item in params.get("SharePermissionSet"):
                obj = SharePermission()
                obj._deserialize(item)
                self.SharePermissionSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeImageSnapshotStatusRequest(AbstractModel):
    """DescribeImageSnapshotStatus请求参数结构体"""

    def __init__(self):
        """
        :param ImageId: 需要查看的镜像Id
        :type ImageId: str
        """
        self.ImageId = None

    def _deserialize(self, params):
        self.ImageId = params.get("ImageId")


class DescribeImageSnapshotStatusResponse(AbstractModel):
    """DescribeImageSnapshotStatus返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeImagesAttributeRequest(AbstractModel):
    """DescribeImagesAttribute请求参数结构体"""

    def __init__(self):
        """
        :param ImageIds: 1
        :type ImageIds: list of str
        """
        self.ImageIds = None

    def _deserialize(self, params):
        self.ImageIds = params.get("ImageIds")


class DescribeImagesAttributeResponse(AbstractModel):
    """DescribeImagesAttribute返回参数结构体"""

    def __init__(self):
        """
        :param ImageAttributeSet: unImgId到deviceImageId的映射的数组
        :type ImageAttributeSet: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ImageAttributeSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.ImageAttributeSet = params.get("ImageAttributeSet")
        self.RequestId = params.get("RequestId")


class DescribeImagesRequest(AbstractModel):
    """DescribeImages请求参数结构体"""

    def __init__(self):
        """
        :param ImageIds: 镜像ID列表 。镜像ID如：`img-gvbnzy6f`。array型参数的格式可以参考API简介。镜像ID可以通过如下方式获取：<br><li>通过DescribeImages接口返回的`ImageId`获取。<br><li>通过镜像控制台获取。
        :type ImageIds: list of str
        :param Filters: 过滤条件。其中Filters的上限为10，Filters.Values的上限为5。 注意：不可以同时指定ImageIds和Filters。可选值包括 `image-id`, `image-type`。
        :type Filters: list of Filter
        :param Offset: 偏移量，默认为0。关于Offset详见API简介。
        :type Offset: int
        :param Limit: 数量限制，默认为20，最大值为100。关于Limit详见API简介。
        :type Limit: int
        :param InstanceType: 实例类型，如 `S1.SMALL1`
        :type InstanceType: str
        :param IsInner: 内部参数
        :type IsInner: str
        """
        self.ImageIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None
        self.InstanceType = None
        self.IsInner = None

    def _deserialize(self, params):
        self.ImageIds = params.get("ImageIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.InstanceType = params.get("InstanceType")
        self.IsInner = params.get("IsInner")


class DescribeImagesResponse(AbstractModel):
    """DescribeImages返回参数结构体"""

    def __init__(self):
        """
        :param ImageSet: 一个关于镜像详细信息的结构体，主要包括镜像的主要状态与属性。
        :type ImageSet: list of Image
        :param TotalCount: 符合要求的镜像数量。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ImageSet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("ImageSet") is not None:
            self.ImageSet = []
            for item in params.get("ImageSet"):
                obj = Image()
                obj._deserialize(item)
                self.ImageSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeImportImageOsRequest(AbstractModel):
    """DescribeImportImageOs请求参数结构体"""


class DescribeImportImageOsResponse(AbstractModel):
    """DescribeImportImageOs返回参数结构体"""

    def __init__(self):
        """
        :param ImportImageOsListSupported: 支持的导入镜像的操作系统类型
        :type ImportImageOsListSupported: list of str
        :param ImportImageOsVersionSupported: 支持的导入镜像的操作系统版本
        :type ImportImageOsVersionSupported: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ImportImageOsListSupported = None
        self.ImportImageOsVersionSupported = None
        self.RequestId = None

    def _deserialize(self, params):
        self.ImportImageOsListSupported = params.get("ImportImageOsListSupported")
        self.ImportImageOsVersionSupported = params.get("ImportImageOsVersionSupported")
        self.RequestId = params.get("RequestId")


class DescribeImportSnapshotTaskRequest(AbstractModel):
    """DescribeImportSnapshotTask请求参数结构体"""

    def __init__(self):
        """
        :param TaskId: 1
        :type TaskId: str
        """
        self.TaskId = None

    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")


class DescribeImportSnapshotTaskResponse(AbstractModel):
    """DescribeImportSnapshotTask返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeInstanceAttachedDevicesRequest(AbstractModel):
    """DescribeInstanceAttachedDevices请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 1
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class DescribeInstanceAttachedDevicesResponse(AbstractModel):
    """DescribeInstanceAttachedDevices返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeInstanceChargeTypeConfigsRequest(AbstractModel):
    """DescribeInstanceChargeTypeConfigs请求参数结构体"""


class DescribeInstanceChargeTypeConfigsResponse(AbstractModel):
    """DescribeInstanceChargeTypeConfigs返回参数结构体"""

    def __init__(self):
        """
        :param InstanceChargeTypeConfigSet: 计费类型配置
        :type InstanceChargeTypeConfigSet: list of InstanceChargeTypeConfig
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceChargeTypeConfigSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("InstanceChargeTypeConfigSet") is not None:
            self.InstanceChargeTypeConfigSet = []
            for item in params.get("InstanceChargeTypeConfigSet"):
                obj = InstanceChargeTypeConfig()
                obj._deserialize(item)
                self.InstanceChargeTypeConfigSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInstanceConfigInfosRequest(AbstractModel):
    """DescribeInstanceConfigInfos请求参数结构体"""

    def __init__(self):
        """
        :param Filters: 1
        :type Filters: list of Filter
        """
        self.Filters = None

    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)


class DescribeInstanceConfigInfosResponse(AbstractModel):
    """DescribeInstanceConfigInfos返回参数结构体"""

    def __init__(self):
        """
        :param InstanceConfigInfos: 实例静态配置信息列表。
        :type InstanceConfigInfos: list of InstanceConfigInfoItem
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceConfigInfos = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("InstanceConfigInfos") is not None:
            self.InstanceConfigInfos = []
            for item in params.get("InstanceConfigInfos"):
                obj = InstanceConfigInfoItem()
                obj._deserialize(item)
                self.InstanceConfigInfos.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInstanceFamilyConfigsRequest(AbstractModel):
    """DescribeInstanceFamilyConfigs请求参数结构体"""


class DescribeInstanceFamilyConfigsResponse(AbstractModel):
    """DescribeInstanceFamilyConfigs返回参数结构体"""

    def __init__(self):
        """
        :param InstanceFamilyConfigSet: 实例机型组配置的列表信息
        :type InstanceFamilyConfigSet: list of InstanceFamilyConfig
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceFamilyConfigSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("InstanceFamilyConfigSet") is not None:
            self.InstanceFamilyConfigSet = []
            for item in params.get("InstanceFamilyConfigSet"):
                obj = InstanceFamilyConfig()
                obj._deserialize(item)
                self.InstanceFamilyConfigSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInstanceInternetBandwidthConfigsRequest(AbstractModel):
    """DescribeInstanceInternetBandwidthConfigs请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 待操作的实例ID。可通过`DescribeInstances`接口返回值中的`InstanceId`获取。
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class DescribeInstanceInternetBandwidthConfigsResponse(AbstractModel):
    """DescribeInstanceInternetBandwidthConfigs返回参数结构体"""

    def __init__(self):
        """
        :param InternetBandwidthConfigSet: 带宽配置信息列表。
        :type InternetBandwidthConfigSet: list of InternetBandwidthConfig
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InternetBandwidthConfigSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("InternetBandwidthConfigSet") is not None:
            self.InternetBandwidthConfigSet = []
            for item in params.get("InternetBandwidthConfigSet"):
                obj = InternetBandwidthConfig()
                obj._deserialize(item)
                self.InternetBandwidthConfigSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInstanceOperationLogsRequest(AbstractModel):
    """DescribeInstanceOperationLogs请求参数结构体"""

    def __init__(self):
        """
        :param Filters: 1
        :type Filters: list of Filter
        """
        self.Filters = None

    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)


class DescribeInstanceOperationLogsResponse(AbstractModel):
    """DescribeInstanceOperationLogs返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeInstanceStatisticsRequest(AbstractModel):
    """DescribeInstanceStatistics请求参数结构体"""

    def __init__(self):
        """
        :param Filters: 1
        :type Filters: list of Filter
        """
        self.Filters = None

    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)


class DescribeInstanceStatisticsResponse(AbstractModel):
    """DescribeInstanceStatistics返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeInstanceTypeConfigsRequest(AbstractModel):
    """DescribeInstanceTypeConfigs请求参数结构体"""

    def __init__(self):
        """
        :param Filters: 过滤条件，详见下表：实例过滤条件表。每次请求的`Filters`的上限为10，`Filter.Values`的上限为1。
        :type Filters: list of Filter
        """
        self.Filters = None

    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)


class DescribeInstanceTypeConfigsResponse(AbstractModel):
    """DescribeInstanceTypeConfigs返回参数结构体"""

    def __init__(self):
        """
        :param InstanceTypeConfigSet: 实例机型配置列表。
        :type InstanceTypeConfigSet: list of InstanceTypeConfig
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceTypeConfigSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("InstanceTypeConfigSet") is not None:
            self.InstanceTypeConfigSet = []
            for item in params.get("InstanceTypeConfigSet"):
                obj = InstanceTypeConfig()
                obj._deserialize(item)
                self.InstanceTypeConfigSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInstanceTypeNameConfigsRequest(AbstractModel):
    """DescribeInstanceTypeNameConfigs请求参数结构体"""


class DescribeInstanceTypeNameConfigsResponse(AbstractModel):
    """DescribeInstanceTypeNameConfigs返回参数结构体"""

    def __init__(self):
        """
        :param InstanceTypeNameConfigSet: 实例类型名称列表。
        :type InstanceTypeNameConfigSet: list of InstanceTypeNameConfig
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceTypeNameConfigSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("InstanceTypeNameConfigSet") is not None:
            self.InstanceTypeNameConfigSet = []
            for item in params.get("InstanceTypeNameConfigSet"):
                obj = InstanceTypeNameConfig()
                obj._deserialize(item)
                self.InstanceTypeNameConfigSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInstanceTypeQuotaRequest(AbstractModel):
    """DescribeInstanceTypeQuota请求参数结构体"""

    def __init__(self):
        """
        :param Filters: 1
        :type Filters: list of Filter
        """
        self.Filters = None

    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)


class DescribeInstanceTypeQuotaResponse(AbstractModel):
    """DescribeInstanceTypeQuota返回参数结构体"""

    def __init__(self):
        """
        :param InstanceTypeQuotaSet: 实例机型配额列表。
        :type InstanceTypeQuotaSet: list of InstanceTypeQuota
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceTypeQuotaSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("InstanceTypeQuotaSet") is not None:
            self.InstanceTypeQuotaSet = []
            for item in params.get("InstanceTypeQuotaSet"):
                obj = InstanceTypeQuota()
                obj._deserialize(item)
                self.InstanceTypeQuotaSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInstanceVncUrlRequest(AbstractModel):
    """DescribeInstanceVncUrl请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 查询的实例id, 如ins-38dk3j
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class DescribeInstanceVncUrlResponse(AbstractModel):
    """DescribeInstanceVncUrl返回参数结构体"""

    def __init__(self):
        """
        :param InstanceVncUrl: 用户的VNC连接串
        :type InstanceVncUrl: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceVncUrl = None
        self.RequestId = None

    def _deserialize(self, params):
        self.InstanceVncUrl = params.get("InstanceVncUrl")
        self.RequestId = params.get("RequestId")


class DescribeInstancesActionTimerRequest(AbstractModel):
    """DescribeInstancesActionTimer请求参数结构体"""

    def __init__(self):
        """
        :param ActionTimerIds: 定时器id数组
        :type ActionTimerIds: list of str
        :param InstanceIds: 实例id数组
        :type InstanceIds: list of str
        :param TimerAction: 定时任务执行之间，格式如：2018-05-01 19:00:00，必须大于当前时间5分钟。
        :type TimerAction: str
        :param EndActionTime: 执行时间的结束范围，用于条件筛选，格式如2018-05-01 19:00:00。
        :type EndActionTime: str
        :param StartActionTime: 执行时间的开始范围，用于条件筛选，格式如2018-05-01 19:00:00。
        :type StartActionTime: str
        :param StatusList: 定时器状态列表数组，可选值为：UNDO（未执行）， DOING（正在执行i），DONE（执行完成）。
        :type StatusList: list of str
        """
        self.ActionTimerIds = None
        self.InstanceIds = None
        self.TimerAction = None
        self.EndActionTime = None
        self.StartActionTime = None
        self.StatusList = None

    def _deserialize(self, params):
        self.ActionTimerIds = params.get("ActionTimerIds")
        self.InstanceIds = params.get("InstanceIds")
        self.TimerAction = params.get("TimerAction")
        self.EndActionTime = params.get("EndActionTime")
        self.StartActionTime = params.get("StartActionTime")
        self.StatusList = params.get("StatusList")


class DescribeInstancesActionTimerResponse(AbstractModel):
    """DescribeInstancesActionTimer返回参数结构体"""

    def __init__(self):
        """
        :param ActionTimers: 定时器数组
        :type ActionTimers: list of ActionTimer
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ActionTimers = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("ActionTimers") is not None:
            self.ActionTimers = []
            for item in params.get("ActionTimers"):
                obj = ActionTimer()
                obj._deserialize(item)
                self.ActionTimers.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInstancesAttributeRequest(AbstractModel):
    """DescribeInstancesAttribute请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 1
        :type InstanceIds: list of str
        :param Offset: 1
        :type Offset: int
        :param Limit: 1
        :type Limit: int
        """
        self.InstanceIds = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeInstancesAttributeResponse(AbstractModel):
    """DescribeInstancesAttribute返回参数结构体"""

    def __init__(self):
        """
        :param InstanceAttributeSet: 实例属性列表，标识实例id，实例订单Id。
        :type InstanceAttributeSet: list of KeyPair
        :param TotalCount: 拉取实例的个数。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceAttributeSet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("InstanceAttributeSet") is not None:
            self.InstanceAttributeSet = []
            for item in params.get("InstanceAttributeSet"):
                obj = KeyPair()
                obj._deserialize(item)
                self.InstanceAttributeSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeInstancesCreateImageAttributesRequest(AbstractModel):
    """DescribeInstancesCreateImageAttributes请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 实例ID
        :type InstanceIds: list of str
        """
        self.InstanceIds = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")


class DescribeInstancesCreateImageAttributesResponse(AbstractModel):
    """DescribeInstancesCreateImageAttributes返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeInstancesOperationLimitRequest(AbstractModel):
    """DescribeInstancesOperationLimit请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 1
        :type InstanceIds: list of str
        :param Operation: 1
        :type Operation: str
        """
        self.InstanceIds = None
        self.Operation = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.Operation = params.get("Operation")


class DescribeInstancesOperationLimitResponse(AbstractModel):
    """DescribeInstancesOperationLimit返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeInstancesRecentFailedOperationRequest(AbstractModel):
    """DescribeInstancesRecentFailedOperation请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 1
        :type InstanceIds: list of str
        :param Offset: 1
        :type Offset: int
        :param Limit: 1
        :type Limit: int
        """
        self.InstanceIds = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeInstancesRecentFailedOperationResponse(AbstractModel):
    """DescribeInstancesRecentFailedOperation返回参数结构体"""

    def __init__(self):
        """
        :param InstancesRecentFailedOperationSet: 最近失败操作详情列表。
        :type InstancesRecentFailedOperationSet: list of InstancesRecentFailedOperationSet
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstancesRecentFailedOperationSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("InstancesRecentFailedOperationSet") is not None:
            self.InstancesRecentFailedOperationSet = []
            for item in params.get("InstancesRecentFailedOperationSet"):
                obj = InstancesRecentFailedOperationSet()
                obj._deserialize(item)
                self.InstancesRecentFailedOperationSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInstancesRequest(AbstractModel):
    """DescribeInstances请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 按照一个或者多个实例ID查询。实例ID形如：`ins-11112222`。此参数的具体格式可参考API简介的`id.N`一节）。每次请求的实例的上限为100。参数不支持同时指定`InstanceIds`和`Filters`。
        :type InstanceIds: list of str
        :param Filters: 过滤条件，详见下表：实例过滤条件表。每次请求的`Filters`的上限为10，`Filter.Values`的上限为5。参数不支持同时指定`InstanceIds`和`Filters`。
        :type Filters: list of Filter
        :param Offset: 偏移量，默认为0。关于`Offset`的更进一步介绍请参考 API 简介中的相关小节。
        :type Offset: int
        :param Limit: 返回数量，默认为20，最大值为100。关于`Limit`的更进一步介绍请参考 API 简介中的相关小节。
        :type Limit: int
        :param InnerVpcIds: 内部参数，数字型vpcId列表 。
        :type InnerVpcIds: list of int
        :param InnerSubnetIds: 内部参数，数字型subnetId列表。
        :type InnerSubnetIds: list of int
        :param IpAddresses: 内部参数，精确内外网IP列表。
        :type IpAddresses: list of str
        :param VagueIpAddress: 内部参数，模糊内外网IP。
        :type VagueIpAddress: str
        :param VagueInstanceName: 内部参数，模糊实例别名。
        :type VagueInstanceName: str
        """
        self.InstanceIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None
        self.InnerVpcIds = None
        self.InnerSubnetIds = None
        self.IpAddresses = None
        self.VagueIpAddress = None
        self.VagueInstanceName = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.InnerVpcIds = params.get("InnerVpcIds")
        self.InnerSubnetIds = params.get("InnerSubnetIds")
        self.IpAddresses = params.get("IpAddresses")
        self.VagueIpAddress = params.get("VagueIpAddress")
        self.VagueInstanceName = params.get("VagueInstanceName")


class DescribeInstancesResponse(AbstractModel):
    """DescribeInstances返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param InstanceSet: 实例详细信息列表。
        :type InstanceSet: list of Instance
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.InstanceSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("InstanceSet") is not None:
            self.InstanceSet = []
            for item in params.get("InstanceSet"):
                obj = Instance()
                obj._deserialize(item)
                self.InstanceSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInstancesReturnableRequest(AbstractModel):
    """DescribeInstancesReturnable请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 1
        :type InstanceIds: list of str
        :param Offset: 1
        :type Offset: int
        :param Limit: 1
        :type Limit: int
        """
        self.InstanceIds = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeInstancesReturnableResponse(AbstractModel):
    """DescribeInstancesReturnable返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param InstanceReturnableSet: 可退还实例详细信息列表。
        :type InstanceReturnableSet: list of InstanceReturnable
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.InstanceReturnableSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("InstanceReturnableSet") is not None:
            self.InstanceReturnableSet = []
            for item in params.get("InstanceReturnableSet"):
                obj = InstanceReturnable()
                obj._deserialize(item)
                self.InstanceReturnableSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInstancesStatusRequest(AbstractModel):
    """DescribeInstancesStatus请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 按照一个或者多个实例ID查询。实例ID形如：`ins-11112222`。此参数的具体格式可参考API简介的`id.N`一节）。每次请求的实例的上限为100。
        :type InstanceIds: list of str
        :param Offset: 偏移量，默认为0。关于`Offset`的更进一步介绍请参考 API 简介中的相关小节。
        :type Offset: int
        :param Limit: 返回数量，默认为20，最大值为100。关于`Limit`的更进一步介绍请参考 API 简介中的相关小节。
        :type Limit: int
        """
        self.InstanceIds = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeInstancesStatusResponse(AbstractModel):
    """DescribeInstancesStatus返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的实例状态数量。
        :type TotalCount: int
        :param InstanceStatusSet: 实例状态 列表。
        :type InstanceStatusSet: list of InstanceStatus
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.InstanceStatusSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("InstanceStatusSet") is not None:
            self.InstanceStatusSet = []
            for item in params.get("InstanceStatusSet"):
                obj = InstanceStatus()
                obj._deserialize(item)
                self.InstanceStatusSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInternetChargeTypeConfigsRequest(AbstractModel):
    """DescribeInternetChargeTypeConfigs请求参数结构体"""


class DescribeInternetChargeTypeConfigsResponse(AbstractModel):
    """DescribeInternetChargeTypeConfigs返回参数结构体"""

    def __init__(self):
        """
        :param InternetChargeTypeConfigSet: 网络计费类型配置。
        :type InternetChargeTypeConfigSet: list of InternetChargeTypeConfig
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InternetChargeTypeConfigSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("InternetChargeTypeConfigSet") is not None:
            self.InternetChargeTypeConfigSet = []
            for item in params.get("InternetChargeTypeConfigSet"):
                obj = InternetChargeTypeConfig()
                obj._deserialize(item)
                self.InternetChargeTypeConfigSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeKeyPairsAttributeRequest(AbstractModel):
    """DescribeKeyPairsAttribute请求参数结构体"""

    def __init__(self):
        """
        :param KeyIds: 1
        :type KeyIds: list of str
        :param Offset: 1
        :type Offset: int
        :param Limit: 1
        :type Limit: int
        """
        self.KeyIds = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.KeyIds = params.get("KeyIds")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeKeyPairsAttributeResponse(AbstractModel):
    """DescribeKeyPairsAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeKeyPairsRequest(AbstractModel):
    """DescribeKeyPairs请求参数结构体"""

    def __init__(self):
        """
        :param KeyIds: 密钥对ID，密钥对ID形如：`skey-11112222`（此接口支持同时传入多个ID进行过滤。此参数的具体格式可参考 API 简介的 `id.N` 一节）。参数不支持同时指定 `KeyIds` 和 `Filters`。<br> 密钥对ID可以通过登录控制台查询。
        :type KeyIds: list of str
        :param Filters: 过滤条件，详见密钥对过滤条件表。参数不支持同时指定 `KeyIds` 和 `Filters`。
        :type Filters: list of Filter
        :param Offset: 偏移量，默认为0。关于 `Offset` 的更进一步介绍请参考 API 简介中的相关小节。
        :type Offset: int
        :param Limit: 返回数量，默认为20，最大值为100。关于 `Limit` 的更进一步介绍请参考 API 简介中的相关小节。
        :type Limit: int
        """
        self.KeyIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.KeyIds = params.get("KeyIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeKeyPairsResponse(AbstractModel):
    """DescribeKeyPairs返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的密钥对数量。
        :type TotalCount: int
        :param KeyPairSet: 密钥对详细信息列表。
        :type KeyPairSet: list of KeyPair
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.KeyPairSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("KeyPairSet") is not None:
            self.KeyPairSet = []
            for item in params.get("KeyPairSet"):
                obj = KeyPair()
                obj._deserialize(item)
                self.KeyPairSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeMarketImagesRequest(AbstractModel):
    """DescribeMarketImages请求参数结构体"""

    def __init__(self):
        """
        :param ImageIds: 需要查询的市场镜像的镜像Id
        :type ImageIds: list of str
        :param Filters: 过滤条件。只支持按镜像Id过滤
        :type Filters: list of Filter
        :param Offset: 偏移值，用于分页
        :type Offset: str
        :param Limit: 返回镜像的数量。
        :type Limit: str
        :param IsInner: 内部用户
        :type IsInner: str
        """
        self.ImageIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None
        self.IsInner = None

    def _deserialize(self, params):
        self.ImageIds = params.get("ImageIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.IsInner = params.get("IsInner")


class DescribeMarketImagesResponse(AbstractModel):
    """DescribeMarketImages返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeMigrateTaskStatusRequest(AbstractModel):
    """DescribeMigrateTaskStatus请求参数结构体"""

    def __init__(self):
        """
        :param JobId: 服务迁移任务taskId
        :type JobId: str
        :param IsInner: 控制台参数，用于返回额外信息
        :type IsInner: str
        """
        self.JobId = None
        self.IsInner = None

    def _deserialize(self, params):
        self.JobId = params.get("JobId")
        self.IsInner = params.get("IsInner")


class DescribeMigrateTaskStatusResponse(AbstractModel):
    """DescribeMigrateTaskStatus返回参数结构体"""

    def __init__(self):
        """
        :param Progress: 迁移进度。
        :type Progress: float
        :param Status: 任务状态。
        :type Status: str
        :param JobName: 任务名称。
        :type JobName: str
        :param JobId: 任务ID。
        :type JobId: str
        :param AppId: 用户AppId。
        :type AppId: int
        :param Uin: 账户ID。
        :type Uin: str
        :param Uuid: CVM子机uuid。
        :type Uuid: str
        :param InstanceId: 实例ID。
        :type InstanceId: str
        :param ImageUrl: 镜像COS链接。
        :type ImageUrl: str
        :param DataSize: 镜像大小。
        :type DataSize: int
        :param Region: 地域信息。
        :type Region: str
        :param CreateTime: 任务创建时间。
        :type CreateTime: str
        :param EndTime: 任务结束时间。
        :type EndTime: str
        :param Action: 任务类型。
        :type Action: str
        :param ErrorMessage: 任务失败的错误原因
        :type ErrorMessage: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Progress = None
        self.Status = None
        self.JobName = None
        self.JobId = None
        self.AppId = None
        self.Uin = None
        self.Uuid = None
        self.InstanceId = None
        self.ImageUrl = None
        self.DataSize = None
        self.Region = None
        self.CreateTime = None
        self.EndTime = None
        self.Action = None
        self.ErrorMessage = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Progress = params.get("Progress")
        self.Status = params.get("Status")
        self.JobName = params.get("JobName")
        self.JobId = params.get("JobId")
        self.AppId = params.get("AppId")
        self.Uin = params.get("Uin")
        self.Uuid = params.get("Uuid")
        self.InstanceId = params.get("InstanceId")
        self.ImageUrl = params.get("ImageUrl")
        self.DataSize = params.get("DataSize")
        self.Region = params.get("Region")
        self.CreateTime = params.get("CreateTime")
        self.EndTime = params.get("EndTime")
        self.Action = params.get("Action")
        self.ErrorMessage = params.get("ErrorMessage")
        self.RequestId = params.get("RequestId")


class DescribeNetworkSharingGroupsRequest(AbstractModel):
    """DescribeNetworkSharingGroups请求参数结构体"""


class DescribeNetworkSharingGroupsResponse(AbstractModel):
    """DescribeNetworkSharingGroups返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeRecomendedZonesRequest(AbstractModel):
    """DescribeRecomendedZones请求参数结构体"""

    def __init__(self):
        """
                :param InstanceType: 实例机型。不同实例机型指定了不同的资源规格。
        <br><li>对于付费模式为PREPAID或POSTPAID_BY_HOUR的子机创建，具体取值可通过调用接口DescribeInstanceTypeConfigs来获得最新的规格表或参见实例类型描述。若不指定该参数，则默认机型为S1.SMALL1。<br><li>对于付费模式为CDHPAID的子机创建，该参数以"CDH_"为前缀，根据cpu和内存配置生成，具体形式为：CDH_XCXG，例如对于创建cpu为1核，内存为1G大小的专用宿主机的子机，该参数应该为CDH_1C1G。
                :type InstanceType: str
                :param InstanceChargeType: 实例计费类型。<br><li>PREPAID：预付费，即包年包月<br><li>POSTPAID_BY_HOUR：按小时后付费<br><li>CDHPAID：独享母机付费（基于专用宿主机创建，宿主机部分的资源不收费）<br>默认值：POSTPAID_BY_HOUR。
                :type InstanceChargeType: str
        """
        self.InstanceType = None
        self.InstanceChargeType = None

    def _deserialize(self, params):
        self.InstanceType = params.get("InstanceType")
        self.InstanceChargeType = params.get("InstanceChargeType")


class DescribeRecomendedZonesResponse(AbstractModel):
    """DescribeRecomendedZones返回参数结构体"""

    def __init__(self):
        """
        :param PostPaidZoneSet: 按照实例可购买配额，从高到低排序的按量计费可用区列表。
        :type PostPaidZoneSet: list of str
        :param PrePaidZoneSet: 按照实例可购买配额，从高到低排序的包年包月可用区列表。
        :type PrePaidZoneSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.PostPaidZoneSet = None
        self.PrePaidZoneSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.PostPaidZoneSet = params.get("PostPaidZoneSet")
        self.PrePaidZoneSet = params.get("PrePaidZoneSet")
        self.RequestId = params.get("RequestId")


class DescribeRecommendedZonesRequest(AbstractModel):
    """DescribeRecommendedZones请求参数结构体"""

    def __init__(self):
        """
                :param InstanceType: 实例机型。不同实例机型指定了不同的资源规格。
        <br><li>对于付费模式为PREPAID或POSTPAID_BY_HOUR的子机创建，具体取值可通过调用接口DescribeInstanceTypeConfigs来获得最新的规格表或参见实例类型描述。若不指定该参数，则默认机型为S1.SMALL1。<br><li>对于付费模式为CDHPAID的子机创建，该参数以"CDH_"为前缀，根据cpu和内存配置生成，具体形式为：CDH_XCXG，例如对于创建cpu为1核，内存为1G大小的专用宿主机的子机，该参数应该为CDH_1C1G。
                :type InstanceType: str
                :param InstanceChargeType: 实例计费类型。<br><li>PREPAID：预付费，即包年包月<br><li>POSTPAID_BY_HOUR：按小时后付费<br><li>CDHPAID：独享母机付费（基于专用宿主机创建，宿主机部分的资源不收费）<br>默认值：POSTPAID_BY_HOUR。
                :type InstanceChargeType: str
        """
        self.InstanceType = None
        self.InstanceChargeType = None

    def _deserialize(self, params):
        self.InstanceType = params.get("InstanceType")
        self.InstanceChargeType = params.get("InstanceChargeType")


class DescribeRecommendedZonesResponse(AbstractModel):
    """DescribeRecommendedZones返回参数结构体"""

    def __init__(self):
        """
        :param PostPaidZoneSet: 按照实例可购买配额，从高到低排序的按量计费可用区列表。
        :type PostPaidZoneSet: list of str
        :param PrePaidZoneSet: 按照实例可购买配额，从高到低排序的包年包月可用区列表。
        :type PrePaidZoneSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.PostPaidZoneSet = None
        self.PrePaidZoneSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.PostPaidZoneSet = params.get("PostPaidZoneSet")
        self.PrePaidZoneSet = params.get("PrePaidZoneSet")
        self.RequestId = params.get("RequestId")


class DescribeRegionsRequest(AbstractModel):
    """DescribeRegions请求参数结构体"""


class DescribeRegionsResponse(AbstractModel):
    """DescribeRegions返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 地域数量
        :type TotalCount: int
        :param RegionSet: 地域列表信息
        :type RegionSet: list of RegionInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.RegionSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("RegionSet") is not None:
            self.RegionSet = []
            for item in params.get("RegionSet"):
                obj = RegionInfo()
                obj._deserialize(item)
                self.RegionSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeResourcesOverviewRequest(AbstractModel):
    """DescribeResourcesOverview请求参数结构体"""


class DescribeResourcesOverviewResponse(AbstractModel):
    """DescribeResourcesOverview返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeTaskRequest(AbstractModel):
    """DescribeTask请求参数结构体"""

    def __init__(self):
        """
        :param FlowId: des或者allinone的taskid
        :type FlowId: int
        """
        self.FlowId = None

    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")


class DescribeTaskResponse(AbstractModel):
    """DescribeTask返回参数结构体"""

    def __init__(self):
        """
        :param Status: 字符串状态
        :type Status: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Status = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class DescribeUserAvailableZonesRequest(AbstractModel):
    """DescribeUserAvailableZones请求参数结构体"""

    def __init__(self):
        """
        :param Filters: 1
        :type Filters: list of Filter
        """
        self.Filters = None

    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)


class DescribeUserAvailableZonesResponse(AbstractModel):
    """DescribeUserAvailableZones返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeUserGlobalConfigsRequest(AbstractModel):
    """DescribeUserGlobalConfigs请求参数结构体"""

    def __init__(self):
        """
        :param Names: 全局配置名称列表。
        :type Names: list of str
        """
        self.Names = None

    def _deserialize(self, params):
        self.Names = params.get("Names")


class DescribeUserGlobalConfigsResponse(AbstractModel):
    """DescribeUserGlobalConfigs返回参数结构体"""

    def __init__(self):
        """
        :param ConfigSet: 用户全局配置列表。
        :type ConfigSet: list of KvType
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ConfigSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("ConfigSet") is not None:
            self.ConfigSet = []
            for item in params.get("ConfigSet"):
                obj = KvType()
                obj._deserialize(item)
                self.ConfigSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeUserInstanceQuotaRequest(AbstractModel):
    """DescribeUserInstanceQuota请求参数结构体"""

    def __init__(self):
        """
        :param Filters: 1
        :type Filters: list of Filter
        """
        self.Filters = None

    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)


class DescribeUserInstanceQuotaResponse(AbstractModel):
    """DescribeUserInstanceQuota返回参数结构体"""

    def __init__(self):
        """
        :param DescribeUserInstanceQuota: 用于标识用户在可用区下包年包月、按量计费配额。
        :type DescribeUserInstanceQuota: list of KeyPair
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DescribeUserInstanceQuota = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("DescribeUserInstanceQuota") is not None:
            self.DescribeUserInstanceQuota = []
            for item in params.get("DescribeUserInstanceQuota"):
                obj = KeyPair()
                obj._deserialize(item)
                self.DescribeUserInstanceQuota.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeUserMigrateTasksRequest(AbstractModel):
    """DescribeUserMigrateTasks请求参数结构体"""

    def __init__(self):
        """
        :param MigrateTaskType: 查询的迁移任务类型，可选`ColdMigrateInstance`，`ImportCbs`和`OfflineMigrate`，其中`OfflineMigrate`代表两种离线迁移任务一起查询。
        :type MigrateTaskType: str
        :param Filters: 过滤条件，可选instance-id，job-name，job-id。
        :type Filters: list of Filter
        :param Limit: 任务数量限制，用于分页。
        :type Limit: int
        :param Offset: 任务起始数，用于分页。
        :type Offset: int
        """
        self.MigrateTaskType = None
        self.Filters = None
        self.Limit = None
        self.Offset = None

    def _deserialize(self, params):
        self.MigrateTaskType = params.get("MigrateTaskType")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")


class DescribeUserMigrateTasksResponse(AbstractModel):
    """DescribeUserMigrateTasks返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeUserZoneStatusRequest(AbstractModel):
    """DescribeUserZoneStatus请求参数结构体"""

    def __init__(self):
        """
        :param Filters: 1
        :type Filters: list of Filter
        """
        self.Filters = None

    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)


class DescribeUserZoneStatusResponse(AbstractModel):
    """DescribeUserZoneStatus返回参数结构体"""

    def __init__(self):
        """
        :param UserZoneStatus: 可用区计费类型状态列表。
        :type UserZoneStatus: list of UserZoneStatusItem
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.UserZoneStatus = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("UserZoneStatus") is not None:
            self.UserZoneStatus = []
            for item in params.get("UserZoneStatus"):
                obj = UserZoneStatusItem()
                obj._deserialize(item)
                self.UserZoneStatus.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeZoneCdhInstanceConfigInfosRequest(AbstractModel):
    """DescribeZoneCdhInstanceConfigInfos请求参数结构体"""

    def __init__(self):
        """
        :param Filters: 可用区
        :type Filters: :class:`tcecloud.cvm.v20170312.models.Filter`
        """
        self.Filters = None

    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = Filter()
            self.Filters._deserialize(params.get("Filters"))


class DescribeZoneCdhInstanceConfigInfosResponse(AbstractModel):
    """DescribeZoneCdhInstanceConfigInfos返回参数结构体"""

    def __init__(self):
        """
        :param HostTypeQuotaSet: 专用宿主机机型配置信息列表
        :type HostTypeQuotaSet: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.HostTypeQuotaSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.HostTypeQuotaSet = params.get("HostTypeQuotaSet")
        self.RequestId = params.get("RequestId")


class DescribeZoneCpuQuotaRequest(AbstractModel):
    """DescribeZoneCpuQuota请求参数结构体"""

    def __init__(self):
        """
        :param Filters: 1
        :type Filters: list of Filter
        """
        self.Filters = None

    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)


class DescribeZoneCpuQuotaResponse(AbstractModel):
    """DescribeZoneCpuQuota返回参数结构体"""

    def __init__(self):
        """
        :param ZoneCpuQuotaSet: 可用区 CPU 配额信息。
        :type ZoneCpuQuotaSet: list of ZoneCpuQuota
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ZoneCpuQuotaSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("ZoneCpuQuotaSet") is not None:
            self.ZoneCpuQuotaSet = []
            for item in params.get("ZoneCpuQuotaSet"):
                obj = ZoneCpuQuota()
                obj._deserialize(item)
                self.ZoneCpuQuotaSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeZoneHostConfigInfosRequest(AbstractModel):
    """DescribeZoneHostConfigInfos请求参数结构体"""

    def __init__(self):
        """
        :param Filters: 可用区过滤条件
        :type Filters: :class:`tcecloud.cvm.v20170312.models.Filter`
        """
        self.Filters = None

    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = Filter()
            self.Filters._deserialize(params.get("Filters"))


class DescribeZoneHostConfigInfosResponse(AbstractModel):
    """DescribeZoneHostConfigInfos返回参数结构体"""

    def __init__(self):
        """
        :param HostTypeQuotaSet: 专用宿主机机型配置信息列表
        :type HostTypeQuotaSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.HostTypeQuotaSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.HostTypeQuotaSet = params.get("HostTypeQuotaSet")
        self.RequestId = params.get("RequestId")


class DescribeZoneHostForSellStatusRequest(AbstractModel):
    """DescribeZoneHostForSellStatus请求参数结构体"""

    def __init__(self):
        """
        :param Filters: 过滤条件
        :type Filters: :class:`tcecloud.cvm.v20170312.models.Filter`
        """
        self.Filters = None

    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = Filter()
            self.Filters._deserialize(params.get("Filters"))


class DescribeZoneHostForSellStatusResponse(AbstractModel):
    """DescribeZoneHostForSellStatus返回参数结构体"""

    def __init__(self):
        """
        :param HostForSellZoneStatus: 专用宿主机可用区售罄状态
        :type HostForSellZoneStatus: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.HostForSellZoneStatus = None
        self.RequestId = None

    def _deserialize(self, params):
        self.HostForSellZoneStatus = params.get("HostForSellZoneStatus")
        self.RequestId = params.get("RequestId")


class DescribeZoneInstanceConfigInfosRequest(AbstractModel):
    """DescribeZoneInstanceConfigInfos请求参数结构体"""

    def __init__(self):
        """
        :param Filters: 1
        :type Filters: list of Filter
        """
        self.Filters = None

    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)


class DescribeZoneInstanceConfigInfosResponse(AbstractModel):
    """DescribeZoneInstanceConfigInfos返回参数结构体"""

    def __init__(self):
        """
        :param InstanceTypeQuotaSet: 可用区机型配置列表。
        :type InstanceTypeQuotaSet: :class:`tcecloud.cvm.v20170312.models.InstanceTypeQuota`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceTypeQuotaSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("InstanceTypeQuotaSet") is not None:
            self.InstanceTypeQuotaSet = InstanceTypeQuota()
            # 20201130 下方data值是列表时(获取实例规格接口)需要额外处理 龚仪
            instance_quota_set = params.get("InstanceTypeQuotaSet")
            if isinstance(instance_quota_set, list):
                self.InstanceTypeQuotaSet = []
                for item in instance_quota_set:
                    obj = InstanceTypeQuota()
                    obj._deserialize(item)
                    self.InstanceTypeQuotaSet.append(obj)
            else:
                self.InstanceTypeQuotaSet._deserialize(params.get("InstanceTypeQuotaSet"))

        self.RequestId = params.get("RequestId")


class DescribeZonesRequest(AbstractModel):
    """DescribeZones请求参数结构体"""


class DescribeZonesResponse(AbstractModel):
    """DescribeZones返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 可用区数量
        :type TotalCount: int
        :param ZoneSet: 可用区列表信息
        :type ZoneSet: list of ZoneInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.ZoneSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("ZoneSet") is not None:
            self.ZoneSet = []
            for item in params.get("ZoneSet"):
                obj = ZoneInfo()
                obj._deserialize(item)
                self.ZoneSet.append(obj)
        self.RequestId = params.get("RequestId")


class DisassociateAddressRequest(AbstractModel):
    """DisassociateAddress请求参数结构体"""

    def __init__(self):
        """
        :param AddressId: 1
        :type AddressId: str
        :param KeepAddressIdBindWithEniPip: 1
        :type KeepAddressIdBindWithEniPip: bool
        :param ReallocateNormalPublicIp: 1
        :type ReallocateNormalPublicIp: bool
        """
        self.AddressId = None
        self.KeepAddressIdBindWithEniPip = None
        self.ReallocateNormalPublicIp = None

    def _deserialize(self, params):
        self.AddressId = params.get("AddressId")
        self.KeepAddressIdBindWithEniPip = params.get("KeepAddressIdBindWithEniPip")
        self.ReallocateNormalPublicIp = params.get("ReallocateNormalPublicIp")


class DisassociateAddressResponse(AbstractModel):
    """DisassociateAddress返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DisassociateInstancesKeyPairsRequest(AbstractModel):
    """DisassociateInstancesKeyPairs请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 一个或多个待操作的实例ID，每次请求批量实例的上限为100。<br><br>可以通过以下方式获取可用的实例ID：<br><li>通过登录控制台查询实例ID。<br><li>通过调用接口 DescribeInstances ，取返回信息中的 `InstanceId` 获取密钥对ID。
        :type InstanceIds: list of str
        :param KeyIds: 密钥对ID列表，每次请求批量密钥对的上限为100。密钥对ID形如：`skey-11112222`。<br><br>可以通过以下方式获取可用的密钥ID：<br><li>通过登录控制台查询密钥ID。<br><li>通过调用接口 DescribeKeyPairs ，取返回信息中的 `KeyId` 获取密钥对ID。
        :type KeyIds: list of str
        :param ForceStop: 是否对运行中的实例选择强制关机。建议对运行中的实例先手动关机，然后再重置用户密码。取值范围：<br><li>TRUE：表示在正常关机失败后进行强制关机。<br><li>FALSE：表示在正常关机失败后不进行强制关机。<br><br>默认取值：FALSE。
        :type ForceStop: bool
        """
        self.InstanceIds = None
        self.KeyIds = None
        self.ForceStop = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.KeyIds = params.get("KeyIds")
        self.ForceStop = params.get("ForceStop")


class DisassociateInstancesKeyPairsResponse(AbstractModel):
    """DisassociateInstancesKeyPairs返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DisassociateSecurityGroupsRequest(AbstractModel):
    """DisassociateSecurityGroups请求参数结构体"""

    def __init__(self):
        """
        :param SecurityGroupIds: 1
        :type SecurityGroupIds: list of str
        :param InstanceIds: 1
        :type InstanceIds: list of str
        """
        self.SecurityGroupIds = None
        self.InstanceIds = None

    def _deserialize(self, params):
        self.SecurityGroupIds = params.get("SecurityGroupIds")
        self.InstanceIds = params.get("InstanceIds")


class DisassociateSecurityGroupsResponse(AbstractModel):
    """DisassociateSecurityGroups返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DisasterRecoverGroup(AbstractModel):
    """容灾组信息"""

    def __init__(self):
        """
                :param DisasterRecoverGroupId: 分散置放群组id。
                :type DisasterRecoverGroupId: str
                :param Name: 分散置放群组名称，长度1-60个字符。
                :type Name: str
                :param Type: 分散置放群组类型，取值范围：<br><li>HOST：物理机<br><li>SW：交换机<br><li>RACK：机架
                :type Type: str
                :param CvmQuotaTotal: 分散置放群组内最大容纳云服务器数量。
                :type CvmQuotaTotal: int
                :param CurrentNum: 分散置放群组内云服务器当前数量。
                :type CurrentNum: int
                :param InstanceIds: 分散置放群组内，云服务器id列表。
        注意：此字段可能返回 null，表示取不到有效值。
                :type InstanceIds: list of str
                :param CreateTime: 分散置放群组创建时间。
        注意：此字段可能返回 null，表示取不到有效值。
                :type CreateTime: str
        """
        self.DisasterRecoverGroupId = None
        self.Name = None
        self.Type = None
        self.CvmQuotaTotal = None
        self.CurrentNum = None
        self.InstanceIds = None
        self.CreateTime = None

    def _deserialize(self, params):
        self.DisasterRecoverGroupId = params.get("DisasterRecoverGroupId")
        self.Name = params.get("Name")
        self.Type = params.get("Type")
        self.CvmQuotaTotal = params.get("CvmQuotaTotal")
        self.CurrentNum = params.get("CurrentNum")
        self.InstanceIds = params.get("InstanceIds")
        self.CreateTime = params.get("CreateTime")


class EnhancedService(AbstractModel):
    """描述了实例的增强服务启用情况与其设置，如云安全，云监控等实例 Agent"""

    def __init__(self):
        """
        :param SecurityService: 开启云安全服务。若不指定该参数，则默认开启云安全服务。
        :type SecurityService: :class:`tcecloud.cvm.v20170312.models.RunSecurityServiceEnabled`
        :param MonitorService: 开启云安全服务。若不指定该参数，则默认开启云监控服务。
        :type MonitorService: :class:`tcecloud.cvm.v20170312.models.RunMonitorServiceEnabled`
        """
        self.SecurityService = None
        self.MonitorService = None

    def _deserialize(self, params):
        if params.get("SecurityService") is not None:
            self.SecurityService = RunSecurityServiceEnabled()
            self.SecurityService._deserialize(params.get("SecurityService"))
        if params.get("MonitorService") is not None:
            self.MonitorService = RunMonitorServiceEnabled()
            self.MonitorService._deserialize(params.get("MonitorService"))


class ExitLiveMigrateInstanceRequest(AbstractModel):
    """ExitLiveMigrateInstance请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 需要退出服务热迁移的实例ID。
        :type InstanceId: str
        :param MigrateResult: 服务迁移是否成功。
        :type MigrateResult: str
        """
        self.InstanceId = None
        self.MigrateResult = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.MigrateResult = params.get("MigrateResult")


class ExitLiveMigrateInstanceResponse(AbstractModel):
    """ExitLiveMigrateInstance返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ExportImageRequest(AbstractModel):
    """ExportImage请求参数结构体"""

    def __init__(self):
        """
        :param ImageId: 镜像ID
        :type ImageId: str
        :param BucketName: COS Bucket名称
        :type BucketName: str
        """
        self.ImageId = None
        self.BucketName = None

    def _deserialize(self, params):
        self.ImageId = params.get("ImageId")
        self.BucketName = params.get("BucketName")


class ExportImageResponse(AbstractModel):
    """ExportImage返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class Externals(AbstractModel):
    """扩展数据"""

    def __init__(self):
        """
        :param ReleaseAddress: 释放地址
        :type ReleaseAddress: bool
        """
        self.ReleaseAddress = None

    def _deserialize(self, params):
        self.ReleaseAddress = params.get("ReleaseAddress")


class FailoverMigrateRequest(AbstractModel):
    """FailoverMigrate请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 需要迁移的实例id
        :type InstanceId: str
        :param LossyLocal: lossy参数
        :type LossyLocal: bool
        :param HostIps: 可指定母机迁移
        :type HostIps: list of str
        """
        self.InstanceId = None
        self.LossyLocal = None
        self.HostIps = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.LossyLocal = params.get("LossyLocal")
        self.HostIps = params.get("HostIps")


class FailoverMigrateResponse(AbstractModel):
    """FailoverMigrate返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class Filter(AbstractModel):
    """>描述键值对过滤器，用于条件过滤查询。例如过滤ID、名称、状态等
    > * 若存在多个`Filter`时，`Filter`间的关系为逻辑与（`AND`）关系。
    > * 若同一个`Filter`存在多个`Values`，同一`Filter`下`Values`间的关系为逻辑或（`OR`）关系。
    >
    > 以DescribeInstances接口的`Filter`为例。若我们需要查询可用区（`zone`）为广州一区 ***并且*** 实例计费模式（`instance-charge-type`）为包年包月 ***或者*** 按量计费的实例时，可如下实现：
    ```
    Filters.1.Name=zone
    &Filters.1.Values.1=ap-guangzhou-1
    &Filters.2.Name=instance-charge-type
    &Filters.2.Values.1=PREPAID
    &Filters.3.Values.2=POSTPAID_BY_HOUR
    ```

    """

    def __init__(self):
        """
        :param Name: 需要过滤的字段。
        :type Name: str
        :param Values: 字段的过滤值。
        :type Values: list of str
        """
        self.Name = None
        self.Values = None

    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Values = params.get("Values")


class HostGoodsDetailItem(AbstractModel):
    """cdh发货实例详细信息"""

    def __init__(self):
        """
        :param transactionId: 请求事务id
        :type transactionId: str
        :param action: 操作名称
        :type action: str
        :param autoRenewFlag: 自动续费标记
        :type autoRenewFlag: int
        :param pid: pid
        :type pid: int
        :param timeSpan: 购买或续费时长
        :type timeSpan: int
        :param timeUnit: 时间单位
        :type timeUnit: str
        :param resourceId: 资源id
        :type resourceId: str
        :param curDeadline: 当前到期时间
        :type curDeadline: str
        :param signature: 数字签名
        :type signature: str
        :param productInfo: 产品信息项列表
        :type productInfo: list of ProductInfoItem
        """
        self.transactionId = None
        self.action = None
        self.autoRenewFlag = None
        self.pid = None
        self.timeSpan = None
        self.timeUnit = None
        self.resourceId = None
        self.curDeadline = None
        self.signature = None
        self.productInfo = None

    def _deserialize(self, params):
        self.transactionId = params.get("transactionId")
        self.action = params.get("action")
        self.autoRenewFlag = params.get("autoRenewFlag")
        self.pid = params.get("pid")
        self.timeSpan = params.get("timeSpan")
        self.timeUnit = params.get("timeUnit")
        self.resourceId = params.get("resourceId")
        self.curDeadline = params.get("curDeadline")
        self.signature = params.get("signature")
        if params.get("productInfo") is not None:
            self.productInfo = []
            for item in params.get("productInfo"):
                obj = ProductInfoItem()
                obj._deserialize(item)
                self.productInfo.append(obj)


class HostGoodsItem(AbstractModel):
    """cdh发货实例的详细信息"""

    def __init__(self):
        """
        :param goodsCategoryId: goodsCategoryId
        :type goodsCategoryId: int
        :param payMode: 实例付费模式
        :type payMode: int
        :param goodsNum: 发货的实例个数
        :type goodsNum: int
        :param regionId: 地域id
        :type regionId: int
        :param uin: 发起发货的用户uin
        :type uin: str
        :param ownerUin: 发起发货帐号的所有者uin
        :type ownerUin: str
        :param appId: 发起发货帐号对应的appId
        :type appId: int
        :param projectId: 项目id
        :type projectId: int
        :param zoneId: 可用区id
        :type zoneId: int
        :param goodsDetail: cdh实例详细信息
        :type goodsDetail: :class:`tcecloud.cvm.v20170312.models.HostGoodsDetailItem`
        """
        self.goodsCategoryId = None
        self.payMode = None
        self.goodsNum = None
        self.regionId = None
        self.uin = None
        self.ownerUin = None
        self.appId = None
        self.projectId = None
        self.zoneId = None
        self.goodsDetail = None

    def _deserialize(self, params):
        self.goodsCategoryId = params.get("goodsCategoryId")
        self.payMode = params.get("payMode")
        self.goodsNum = params.get("goodsNum")
        self.regionId = params.get("regionId")
        self.uin = params.get("uin")
        self.ownerUin = params.get("ownerUin")
        self.appId = params.get("appId")
        self.projectId = params.get("projectId")
        self.zoneId = params.get("zoneId")
        if params.get("goodsDetail") is not None:
            self.goodsDetail = HostGoodsDetailItem()
            self.goodsDetail._deserialize(params.get("goodsDetail"))


class HostItem(AbstractModel):
    """cdh实例详细信息"""

    def __init__(self):
        """
        :param Placement: cdh实例所在的位置。通过该参数可以指定实例所属可用区，所属项目等属性。
        :type Placement: :class:`tcecloud.cvm.v20170312.models.Placement`
        :param HostId: cdh实例id
        :type HostId: str
        :param HostType: cdh实例类型
        :type HostType: str
        :param HostName: cdh实例名称
        :type HostName: str
        :param HostChargeType: cdh实例付费模式
        :type HostChargeType: str
        :param RenewFlag: cdh实例自动续费标记
        :type RenewFlag: str
        :param CreatedTime: cdh实例创建时间
        :type CreatedTime: str
        :param ExpiredTime: cdh实例过期时间
        :type ExpiredTime: str
        :param InstanceIds: cdh实例上已创建云子机的实例id列表
        :type InstanceIds: str
        :param HostState: cdh实例状态
        :type HostState: str
        :param HostIp: cdh实例ip
        :type HostIp: str
        :param HostResource: cdh实例资源信息
        :type HostResource: :class:`tcecloud.cvm.v20170312.models.HostResource`
        """
        self.Placement = None
        self.HostId = None
        self.HostType = None
        self.HostName = None
        self.HostChargeType = None
        self.RenewFlag = None
        self.CreatedTime = None
        self.ExpiredTime = None
        self.InstanceIds = None
        self.HostState = None
        self.HostIp = None
        self.HostResource = None

    def _deserialize(self, params):
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        self.HostId = params.get("HostId")
        self.HostType = params.get("HostType")
        self.HostName = params.get("HostName")
        self.HostChargeType = params.get("HostChargeType")
        self.RenewFlag = params.get("RenewFlag")
        self.CreatedTime = params.get("CreatedTime")
        self.ExpiredTime = params.get("ExpiredTime")
        self.InstanceIds = params.get("InstanceIds")
        self.HostState = params.get("HostState")
        self.HostIp = params.get("HostIp")
        if params.get("HostResource") is not None:
            self.HostResource = HostResource()
            self.HostResource._deserialize(params.get("HostResource"))


class HostOrder(AbstractModel):
    """cdh实例相关的订单信息"""

    def __init__(self):
        """
        :param appId: 订单所属帐号的应用id
        :type appId: int
        :param uin: 创建订单的帐号uin
        :type uin: str
        :param ownerUin: 订单所属帐号的所有者uin
        :type ownerUin: str
        :param goods: 订单发货的资源信息列表
        :type goods: list of HostGoodsItem
        """
        self.appId = None
        self.uin = None
        self.ownerUin = None
        self.goods = None

    def _deserialize(self, params):
        self.appId = params.get("appId")
        self.uin = params.get("uin")
        self.ownerUin = params.get("ownerUin")
        if params.get("goods") is not None:
            self.goods = []
            for item in params.get("goods"):
                obj = HostGoodsItem()
                obj._deserialize(item)
                self.goods.append(obj)


class HostPrice(AbstractModel):
    """cdh相关价格信息"""

    def __init__(self):
        """
        :param HostPrice: 描述了cdh实例相关的价格信息
        :type HostPrice: :class:`tcecloud.cvm.v20170312.models.ItemPrice`
        """
        self.HostPrice = None

    def _deserialize(self, params):
        if params.get("HostPrice") is not None:
            self.HostPrice = ItemPrice()
            self.HostPrice._deserialize(params.get("HostPrice"))


class HostResource(AbstractModel):
    """cdh实例的资源信息"""

    def __init__(self):
        """
        :param CpuTotal: cdh实例总cpu核数
        :type CpuTotal: int
        :param CpuAvailable: cdh实例可用cpu核数
        :type CpuAvailable: int
        :param MemTotal: cdh实例总内存大小（单位为:GiB）
        :type MemTotal: float
        :param MemAvailable: cdh实例可用内存大小（单位为:GiB）
        :type MemAvailable: float
        :param DiskTotal: cdh实例总磁盘大小（单位为:GiB）
        :type DiskTotal: int
        :param DiskAvailable: cdh实例可用磁盘大小（单位为:GiB）
        :type DiskAvailable: int
        """
        self.CpuTotal = None
        self.CpuAvailable = None
        self.MemTotal = None
        self.MemAvailable = None
        self.DiskTotal = None
        self.DiskAvailable = None

    def _deserialize(self, params):
        self.CpuTotal = params.get("CpuTotal")
        self.CpuAvailable = params.get("CpuAvailable")
        self.MemTotal = params.get("MemTotal")
        self.MemAvailable = params.get("MemAvailable")
        self.DiskTotal = params.get("DiskTotal")
        self.DiskAvailable = params.get("DiskAvailable")


class Image(AbstractModel):
    """一个关于镜像详细信息的结构体，主要包括镜像的主要状态与属性。"""

    def __init__(self):
        """
        :param ImageId: 镜像ID
        :type ImageId: str
        :param OsName: 镜像操作系统
        :type OsName: str
        :param ImageType: 镜像类型
        :type ImageType: str
        :param CreatedTime: 镜像创建时间
        :type CreatedTime: str
        :param ImageName: 镜像名称
        :type ImageName: str
        :param ImageDescription: 镜像描述
        :type ImageDescription: str
        :param ImageSize: 镜像大小
        :type ImageSize: int
        :param Architecture: 镜像架构
        :type Architecture: str
        :param ImageState: 镜像状态
        :type ImageState: str
        :param Platform: 镜像来源平台
        :type Platform: str
        :param ImageCreator: 镜像创建者
        :type ImageCreator: str
        :param ImageSource: 镜像来源
        :type ImageSource: str
        """
        self.ImageId = None
        self.OsName = None
        self.ImageType = None
        self.CreatedTime = None
        self.ImageName = None
        self.ImageDescription = None
        self.ImageSize = None
        self.Architecture = None
        self.ImageState = None
        self.Platform = None
        self.ImageCreator = None
        self.ImageSource = None

    def _deserialize(self, params):
        self.ImageId = params.get("ImageId")
        self.OsName = params.get("OsName")
        self.ImageType = params.get("ImageType")
        self.CreatedTime = params.get("CreatedTime")
        self.ImageName = params.get("ImageName")
        self.ImageDescription = params.get("ImageDescription")
        self.ImageSize = params.get("ImageSize")
        self.Architecture = params.get("Architecture")
        self.ImageState = params.get("ImageState")
        self.Platform = params.get("Platform")
        self.ImageCreator = params.get("ImageCreator")
        self.ImageSource = params.get("ImageSource")


class ImportCbsRequest(AbstractModel):
    """ImportCbs请求参数结构体"""

    def __init__(self):
        """
        :param SnapshotUrl: 用户需要导入的数据盘镜像存放的COS链接。
        :type SnapshotUrl: str
        :param DiskId: 导入目的云盘的ID。
        :type DiskId: str
        :param DryRun: 用于测试参数合法性。
        :type DryRun: bool
        :param JobName: 任务名称，用于控制台展示。
        :type JobName: str
        """
        self.SnapshotUrl = None
        self.DiskId = None
        self.DryRun = None
        self.JobName = None

    def _deserialize(self, params):
        self.SnapshotUrl = params.get("SnapshotUrl")
        self.DiskId = params.get("DiskId")
        self.DryRun = params.get("DryRun")
        self.JobName = params.get("JobName")


class ImportCbsResponse(AbstractModel):
    """ImportCbs返回参数结构体"""

    def __init__(self):
        """
        :param JobId: 导入数据盘的任务ID，用于查询任务状态、进度。
        :type JobId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.JobId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.JobId = params.get("JobId")
        self.RequestId = params.get("RequestId")


class ImportFullCvmImageRequest(AbstractModel):
    """ImportFullCvmImage请求参数结构体"""

    def __init__(self):
        """
        :param JobName: 导入任务名称，不超过60个字符。
        :type JobName: str
        :param InstanceId: 导入镜像的目标子机实例ID。
        :type InstanceId: str
        :param ImageUrl: 系统盘镜像cos url，cos地域需要跟子机所在地域保持一致。
        :type ImageUrl: str
        :param ImageName: 镜像名称，IsCreate为`TRUE`则为必填，不超过20个字符。
        :type ImageName: str
        :param ImageDescription: 镜像描述，不超过60个字符。
        :type ImageDescription: str
        :param DataDisks: 数据盘镜像数组，最多4个数据盘镜像，传入的数据盘数量必须等于子机上挂载的盘的数量。
        :type DataDisks: list of DataDisks
        :param DryRun: 用于测试参数合法性，默认为`FALSE`。
        :type DryRun: bool
        :param IsCreate: 是否制作整机镜像，默认为`FALSE`。
        :type IsCreate: bool
        """
        self.JobName = None
        self.InstanceId = None
        self.ImageUrl = None
        self.ImageName = None
        self.ImageDescription = None
        self.DataDisks = None
        self.DryRun = None
        self.IsCreate = None

    def _deserialize(self, params):
        self.JobName = params.get("JobName")
        self.InstanceId = params.get("InstanceId")
        self.ImageUrl = params.get("ImageUrl")
        self.ImageName = params.get("ImageName")
        self.ImageDescription = params.get("ImageDescription")
        if params.get("DataDisks") is not None:
            self.DataDisks = []
            for item in params.get("DataDisks"):
                obj = DataDisks()
                obj._deserialize(item)
                self.DataDisks.append(obj)
        self.DryRun = params.get("DryRun")
        self.IsCreate = params.get("IsCreate")


class ImportFullCvmImageResponse(AbstractModel):
    """ImportFullCvmImage返回参数结构体"""

    def __init__(self):
        """
        :param JobId: 任务ID，可利用该ID查询任务状态。
        :type JobId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.JobId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.JobId = params.get("JobId")
        self.RequestId = params.get("RequestId")


class ImportImageRequest(AbstractModel):
    """ImportImage请求参数结构体"""

    def __init__(self):
        """
        :param Architecture: 导入镜像的操作系统架构，`x86_64` 或 `i386`
        :type Architecture: str
        :param OsType: 导入镜像的操作系统类型，通过`DescribeImportImageOs`获取
        :type OsType: str
        :param OsVersion: 导入镜像的操作系统版本，通过`DescribeImportImageOs`获取
        :type OsVersion: str
        :param ImageUrl: 导入镜像存放的cos地址
        :type ImageUrl: str
        :param ImageName: 镜像名称
        :type ImageName: str
        :param ImageDescription: 镜像描述
        :type ImageDescription: str
        :param DryRun: 只检查参数，不执行任务
        :type DryRun: str
        :param Force: 是否强制导入，参考强制导入镜像
        :type Force: str
        """
        self.Architecture = None
        self.OsType = None
        self.OsVersion = None
        self.ImageUrl = None
        self.ImageName = None
        self.ImageDescription = None
        self.DryRun = None
        self.Force = None

    def _deserialize(self, params):
        self.Architecture = params.get("Architecture")
        self.OsType = params.get("OsType")
        self.OsVersion = params.get("OsVersion")
        self.ImageUrl = params.get("ImageUrl")
        self.ImageName = params.get("ImageName")
        self.ImageDescription = params.get("ImageDescription")
        self.DryRun = params.get("DryRun")
        self.Force = params.get("Force")


class ImportImageResponse(AbstractModel):
    """ImportImage返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ImportInstancesActionTimerRequest(AbstractModel):
    """ImportInstancesActionTimer请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 1
        :type InstanceIds: list of str
        :param ActionTimer: 1
        :type ActionTimer: :class:`tcecloud.cvm.v20170312.models.ActionTimer`
        """
        self.InstanceIds = None
        self.ActionTimer = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        if params.get("ActionTimer") is not None:
            self.ActionTimer = ActionTimer()
            self.ActionTimer._deserialize(params.get("ActionTimer"))


class ImportInstancesActionTimerResponse(AbstractModel):
    """ImportInstancesActionTimer返回参数结构体"""

    def __init__(self):
        """
        :param ActionTimerIds: 定时器id列表
        :type ActionTimerIds: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ActionTimerIds = None
        self.RequestId = None

    def _deserialize(self, params):
        self.ActionTimerIds = params.get("ActionTimerIds")
        self.RequestId = params.get("RequestId")


class ImportKeyPairRequest(AbstractModel):
    """ImportKeyPair请求参数结构体"""

    def __init__(self):
        """
        :param KeyName: 密钥对名称，可由数字，字母和下划线组成，长度不超过25个字符。
        :type KeyName: str
        :param ProjectId: 密钥对创建后所属的项目ID。<br><br>可以通过以下方式获取项目ID：<br><li>通过项目列表查询项目ID。<br><li>通过调用接口 DescribeProject，取返回信息中的 `projectId ` 获取项目ID。
        :type ProjectId: int
        :param PublicKey: 密钥对的公钥内容，`OpenSSH RSA` 格式。
        :type PublicKey: str
        """
        self.KeyName = None
        self.ProjectId = None
        self.PublicKey = None

    def _deserialize(self, params):
        self.KeyName = params.get("KeyName")
        self.ProjectId = params.get("ProjectId")
        self.PublicKey = params.get("PublicKey")


class ImportKeyPairResponse(AbstractModel):
    """ImportKeyPair返回参数结构体"""

    def __init__(self):
        """
        :param KeyId: 密钥对ID。
        :type KeyId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.KeyId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.KeyId = params.get("KeyId")
        self.RequestId = params.get("RequestId")


class ImportSnapshotRequest(AbstractModel):
    """ImportSnapshot请求参数结构体"""

    def __init__(self):
        """
        :param SnapshotName: 制作的快照名称
        :type SnapshotName: str
        :param SnapshotUrl: 数据盘镜像COS链接
        :type SnapshotUrl: str
        :param SnapshotSize: 制作的快照大小
        :type SnapshotSize: int
        :param SnapshotDescription: 制作的快照描述
        :type SnapshotDescription: str
        :param DryRun: true为仅检查参数，默认为false
        :type DryRun: bool
        """
        self.SnapshotName = None
        self.SnapshotUrl = None
        self.SnapshotSize = None
        self.SnapshotDescription = None
        self.DryRun = None

    def _deserialize(self, params):
        self.SnapshotName = params.get("SnapshotName")
        self.SnapshotUrl = params.get("SnapshotUrl")
        self.SnapshotSize = params.get("SnapshotSize")
        self.SnapshotDescription = params.get("SnapshotDescription")
        self.DryRun = params.get("DryRun")


class ImportSnapshotResponse(AbstractModel):
    """ImportSnapshot返回参数结构体"""

    def __init__(self):
        """
        :param TaskId: 任务ID，可以用于查询任务状态
        :type TaskId: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class InquiryPriceAllocateAddressesRequest(AbstractModel):
    """InquiryPriceAllocateAddresses请求参数结构体"""

    def __init__(self):
        """
        :param AddressCount: 1
        :type AddressCount: int
        :param IspId: 1
        :type IspId: int
        :param IspName: 1
        :type IspName: str
        :param VipSet: 1
        :type VipSet: list of str
        :param TgwGroup: 1
        :type TgwGroup: str
        :param ApplySilence: 1
        :type ApplySilence: int
        :param InternetChargeType: 1
        :type InternetChargeType: str
        :param InternetMaxBandwidthOut: 1
        :type InternetMaxBandwidthOut: int
        :param AddressChargePrepaid: 1
        :type AddressChargePrepaid: :class:`tcecloud.cvm.v20170312.models.AddressChargePrepaid`
        :param DealId: 1
        :type DealId: str
        """
        self.AddressCount = None
        self.IspId = None
        self.IspName = None
        self.VipSet = None
        self.TgwGroup = None
        self.ApplySilence = None
        self.InternetChargeType = None
        self.InternetMaxBandwidthOut = None
        self.AddressChargePrepaid = None
        self.DealId = None

    def _deserialize(self, params):
        self.AddressCount = params.get("AddressCount")
        self.IspId = params.get("IspId")
        self.IspName = params.get("IspName")
        self.VipSet = params.get("VipSet")
        self.TgwGroup = params.get("TgwGroup")
        self.ApplySilence = params.get("ApplySilence")
        self.InternetChargeType = params.get("InternetChargeType")
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        if params.get("AddressChargePrepaid") is not None:
            self.AddressChargePrepaid = AddressChargePrepaid()
            self.AddressChargePrepaid._deserialize(params.get("AddressChargePrepaid"))
        self.DealId = params.get("DealId")


class InquiryPriceAllocateAddressesResponse(AbstractModel):
    """InquiryPriceAllocateAddresses返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class InquiryPriceAllocateHostsRequest(AbstractModel):
    """InquiryPriceAllocateHosts请求参数结构体"""

    def __init__(self):
        """
        :param Placement: 实例所在的位置。通过该参数可以指定实例所属可用区，所属项目等属性。
        :type Placement: :class:`tcecloud.cvm.v20170312.models.Placement`
        :param ClientToken: 用于保证请求幂等性的字符串。
        :type ClientToken: str
        :param HostChargePrepaid: 预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月实例的购买时长、是否设置自动续费等属性。若指定实例的付费模式为预付费则该参数必传。
        :type HostChargePrepaid: :class:`tcecloud.cvm.v20170312.models.ChargePrepaid`
        :param HostChargeType: 实例计费类型。目前仅支持：PREPAID（预付费，即包年包月模式）。
        :type HostChargeType: str
        :param HostType: CDH实例机型。
        :type HostType: str
        :param HostCount: 购买CDH实例数量。
        :type HostCount: int
        :param DryRun: 是否跳过实际执行逻辑
        :type DryRun: bool
        :param PurchaseSource: 购买来源
        :type PurchaseSource: str
        """
        self.Placement = None
        self.ClientToken = None
        self.HostChargePrepaid = None
        self.HostChargeType = None
        self.HostType = None
        self.HostCount = None
        self.DryRun = None
        self.PurchaseSource = None

    def _deserialize(self, params):
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        self.ClientToken = params.get("ClientToken")
        if params.get("HostChargePrepaid") is not None:
            self.HostChargePrepaid = ChargePrepaid()
            self.HostChargePrepaid._deserialize(params.get("HostChargePrepaid"))
        self.HostChargeType = params.get("HostChargeType")
        self.HostType = params.get("HostType")
        self.HostCount = params.get("HostCount")
        self.DryRun = params.get("DryRun")
        self.PurchaseSource = params.get("PurchaseSource")


class InquiryPriceAllocateHostsResponse(AbstractModel):
    """InquiryPriceAllocateHosts返回参数结构体"""

    def __init__(self):
        """
        :param Price: CDH实例创建价格信息
        :type Price: :class:`tcecloud.cvm.v20170312.models.HostPrice`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Price = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Price") is not None:
            self.Price = HostPrice()
            self.Price._deserialize(params.get("Price"))
        self.RequestId = params.get("RequestId")


class InquiryPriceCreateDisasterRecoverGroupRequest(AbstractModel):
    """InquiryPriceCreateDisasterRecoverGroup请求参数结构体"""

    def __init__(self):
        """
        :param Name: 1
        :type Name: str
        :param Type: 1
        :type Type: str
        """
        self.Name = None
        self.Type = None

    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Type = params.get("Type")


class InquiryPriceCreateDisasterRecoverGroupResponse(AbstractModel):
    """InquiryPriceCreateDisasterRecoverGroup返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class InquiryPriceDeleteDisasterRecoverGroupRequest(AbstractModel):
    """InquiryPriceDeleteDisasterRecoverGroup请求参数结构体"""

    def __init__(self):
        """
        :param DisasterRecoverGroupIds: 1
        :type DisasterRecoverGroupIds: list of str
        """
        self.DisasterRecoverGroupIds = None

    def _deserialize(self, params):
        self.DisasterRecoverGroupIds = params.get("DisasterRecoverGroupIds")


class InquiryPriceDeleteDisasterRecoverGroupResponse(AbstractModel):
    """InquiryPriceDeleteDisasterRecoverGroup返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class InquiryPriceModifyAddressesBandwidthRequest(AbstractModel):
    """InquiryPriceModifyAddressesBandwidth请求参数结构体"""

    def __init__(self):
        """
        :param AddressIds: 1
        :type AddressIds: list of str
        :param InternetMaxBandwidthOut: 1
        :type InternetMaxBandwidthOut: int
        :param DealId: 1
        :type DealId: str
        """
        self.AddressIds = None
        self.InternetMaxBandwidthOut = None
        self.DealId = None

    def _deserialize(self, params):
        self.AddressIds = params.get("AddressIds")
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        self.DealId = params.get("DealId")


class InquiryPriceModifyAddressesBandwidthResponse(AbstractModel):
    """InquiryPriceModifyAddressesBandwidth返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class InquiryPriceModifyInstanceInternetChargeTypeRequest(AbstractModel):
    """InquiryPriceModifyInstanceInternetChargeType请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 1
        :type InstanceId: str
        :param InternetAccessible: 1
        :type InternetAccessible: :class:`tcecloud.cvm.v20170312.models.InternetAccessibleModifyChargeType`
        :param DryRun: 1
        :type DryRun: bool
        """
        self.InstanceId = None
        self.InternetAccessible = None
        self.DryRun = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("InternetAccessible") is not None:
            self.InternetAccessible = InternetAccessibleModifyChargeType()
            self.InternetAccessible._deserialize(params.get("InternetAccessible"))
        self.DryRun = params.get("DryRun")


class InquiryPriceModifyInstanceInternetChargeTypeResponse(AbstractModel):
    """InquiryPriceModifyInstanceInternetChargeType返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class InquiryPriceModifyInstancesChargeTypeRequest(AbstractModel):
    """InquiryPriceModifyInstancesChargeType请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 1
        :type InstanceIds: list of str
        :param InstanceChargeType: 1
        :type InstanceChargeType: str
        :param InstanceChargePrepaid: 1
        :type InstanceChargePrepaid: :class:`tcecloud.cvm.v20170312.models.InstanceChargePrepaid`
        :param DryRun: 1
        :type DryRun: bool
        :param ModifyPortableDataDisk: 1
        :type ModifyPortableDataDisk: bool
        """
        self.InstanceIds = None
        self.InstanceChargeType = None
        self.InstanceChargePrepaid = None
        self.DryRun = None
        self.ModifyPortableDataDisk = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.InstanceChargeType = params.get("InstanceChargeType")
        if params.get("InstanceChargePrepaid") is not None:
            self.InstanceChargePrepaid = InstanceChargePrepaid()
            self.InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))
        self.DryRun = params.get("DryRun")
        self.ModifyPortableDataDisk = params.get("ModifyPortableDataDisk")


class InquiryPriceModifyInstancesChargeTypeResponse(AbstractModel):
    """InquiryPriceModifyInstancesChargeType返回参数结构体"""

    def __init__(self):
        """
        :param Price: 1
        :type Price: :class:`tcecloud.cvm.v20170312.models.Price`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Price = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Price") is not None:
            self.Price = Price()
            self.Price._deserialize(params.get("Price"))
        self.RequestId = params.get("RequestId")


class InquiryPriceQueryDisasterRecoverGroupRequest(AbstractModel):
    """InquiryPriceQueryDisasterRecoverGroup请求参数结构体"""

    def __init__(self):
        """
        :param DisasterRecoverGroupIds: 1
        :type DisasterRecoverGroupIds: list of str
        """
        self.DisasterRecoverGroupIds = None

    def _deserialize(self, params):
        self.DisasterRecoverGroupIds = params.get("DisasterRecoverGroupIds")


class InquiryPriceQueryDisasterRecoverGroupResponse(AbstractModel):
    """InquiryPriceQueryDisasterRecoverGroup返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class InquiryPriceRenewAddressesRequest(AbstractModel):
    """InquiryPriceRenewAddresses请求参数结构体"""

    def __init__(self):
        """
        :param AddressIds: 1
        :type AddressIds: str
        :param AddressChargePrepaid: 1
        :type AddressChargePrepaid: :class:`tcecloud.cvm.v20170312.models.AddressChargePrepaid`
        :param DealId: 1
        :type DealId: str
        :param CurrentDeadline: 1
        :type CurrentDeadline: str
        """
        self.AddressIds = None
        self.AddressChargePrepaid = None
        self.DealId = None
        self.CurrentDeadline = None

    def _deserialize(self, params):
        self.AddressIds = params.get("AddressIds")
        if params.get("AddressChargePrepaid") is not None:
            self.AddressChargePrepaid = AddressChargePrepaid()
            self.AddressChargePrepaid._deserialize(params.get("AddressChargePrepaid"))
        self.DealId = params.get("DealId")
        self.CurrentDeadline = params.get("CurrentDeadline")


class InquiryPriceRenewAddressesResponse(AbstractModel):
    """InquiryPriceRenewAddresses返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class InquiryPriceRenewHostsRequest(AbstractModel):
    """InquiryPriceRenewHosts请求参数结构体"""

    def __init__(self):
        """
        :param HostIds: 一个或多个待操作的CDH实例ID。
        :type HostIds: list of str
        :param HostChargePrepaid: 预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月实例的购买时长、是否设置自动续费等属性。若指定实例的付费模式为预付费则该参数必传。
        :type HostChargePrepaid: :class:`tcecloud.cvm.v20170312.models.ChargePrepaid`
        :param DryRun: 是否跳过实际执行逻辑。
        :type DryRun: bool
        """
        self.HostIds = None
        self.HostChargePrepaid = None
        self.DryRun = None

    def _deserialize(self, params):
        self.HostIds = params.get("HostIds")
        if params.get("HostChargePrepaid") is not None:
            self.HostChargePrepaid = ChargePrepaid()
            self.HostChargePrepaid._deserialize(params.get("HostChargePrepaid"))
        self.DryRun = params.get("DryRun")


class InquiryPriceRenewHostsResponse(AbstractModel):
    """InquiryPriceRenewHosts返回参数结构体"""

    def __init__(self):
        """
        :param Price: CDH实例续费价格信息
        :type Price: :class:`tcecloud.cvm.v20170312.models.HostPrice`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Price = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Price") is not None:
            self.Price = HostPrice()
            self.Price._deserialize(params.get("Price"))
        self.RequestId = params.get("RequestId")


class InquiryPriceRenewInstancesRequest(AbstractModel):
    """InquiryPriceRenewInstances请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 一个或多个待操作的实例ID。可通过`DescribeInstances`接口返回值中的`InstanceId`获取。每次请求批量实例的上限为100。
        :type InstanceIds: list of str
        :param InstanceChargePrepaid: 预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月实例的续费时长、是否设置自动续费等属性。
        :type InstanceChargePrepaid: :class:`tcecloud.cvm.v20170312.models.InstanceChargePrepaid`
        :param InternetAccessible: 内部参数，公网带宽相关信息设置。
        :type InternetAccessible: list of InternetAccessible
        :param DryRun: 试运行。
        :type DryRun: bool
        :param RenewPortableDataDisk: 内部参数，续费弹性数据盘。
        :type RenewPortableDataDisk: bool
        """
        self.InstanceIds = None
        self.InstanceChargePrepaid = None
        self.InternetAccessible = None
        self.DryRun = None
        self.RenewPortableDataDisk = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        if params.get("InstanceChargePrepaid") is not None:
            self.InstanceChargePrepaid = InstanceChargePrepaid()
            self.InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))
        if params.get("InternetAccessible") is not None:
            self.InternetAccessible = []
            for item in params.get("InternetAccessible"):
                obj = InternetAccessible()
                obj._deserialize(item)
                self.InternetAccessible.append(obj)
        self.DryRun = params.get("DryRun")
        self.RenewPortableDataDisk = params.get("RenewPortableDataDisk")


class InquiryPriceRenewInstancesResponse(AbstractModel):
    """InquiryPriceRenewInstances返回参数结构体"""

    def __init__(self):
        """
        :param Price: 该参数表示对应配置实例的价格。
        :type Price: :class:`tcecloud.cvm.v20170312.models.Price`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Price = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Price") is not None:
            self.Price = Price()
            self.Price._deserialize(params.get("Price"))
        self.RequestId = params.get("RequestId")


class InquiryPriceResetInstanceRequest(AbstractModel):
    """InquiryPriceResetInstance请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID。可通过 DescribeInstances API返回值中的`InstanceId`获取。
        :type InstanceId: str
        :param ImageId: 指定有效的镜像ID，格式形如`img-xxx`。镜像类型分为四种：<br/><li>公共镜像</li><li>自定义镜像</li><li>共享镜像</li><li>服务市场镜像</li><br/>可通过以下方式获取可用的镜像ID：<br/><li>`公共镜像`、`自定义镜像`、`共享镜像`的镜像ID可通过登录控制台查询；`服务镜像市场`的镜像ID可通过云市场查询。</li><li>通过调用接口 DescribeImages ，取返回信息中的`ImageId`字段。</li>
        :type ImageId: str
        :param SystemDisk: 实例系统盘配置信息。系统盘为云盘的实例可以通过该参数指定重装后的系统盘大小来实现对系统盘的扩容操作，若不指定则默认系统盘大小保持不变。系统盘大小只支持扩容不支持缩容；重装只支持修改系统盘的大小，不能修改系统盘的类型。
        :type SystemDisk: :class:`tcecloud.cvm.v20170312.models.SystemDisk`
        :param LoginSettings: 实例登录设置。通过该参数可以设置实例的登录方式密码、密钥或保持镜像的原始登录设置。默认情况下会随机生成密码，并以站内信方式知会到用户。
        :type LoginSettings: :class:`tcecloud.cvm.v20170312.models.LoginSettings`
        :param EnhancedService: 增强服务。通过该参数可以指定是否开启云安全、云监控等服务。若不指定该参数，则默认开启云监控、云安全服务。
        :type EnhancedService: :class:`tcecloud.cvm.v20170312.models.EnhancedService`
        """
        self.InstanceId = None
        self.ImageId = None
        self.SystemDisk = None
        self.LoginSettings = None
        self.EnhancedService = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.ImageId = params.get("ImageId")
        if params.get("SystemDisk") is not None:
            self.SystemDisk = SystemDisk()
            self.SystemDisk._deserialize(params.get("SystemDisk"))
        if params.get("LoginSettings") is not None:
            self.LoginSettings = LoginSettings()
            self.LoginSettings._deserialize(params.get("LoginSettings"))
        if params.get("EnhancedService") is not None:
            self.EnhancedService = EnhancedService()
            self.EnhancedService._deserialize(params.get("EnhancedService"))


class InquiryPriceResetInstanceResponse(AbstractModel):
    """InquiryPriceResetInstance返回参数结构体"""

    def __init__(self):
        """
        :param Price: 该参数表示重装成对应配置实例的价格。
        :type Price: :class:`tcecloud.cvm.v20170312.models.Price`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Price = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Price") is not None:
            self.Price = Price()
            self.Price._deserialize(params.get("Price"))
        self.RequestId = params.get("RequestId")


class InquiryPriceResetInstancesInternetMaxBandwidthRequest(AbstractModel):
    """InquiryPriceResetInstancesInternetMaxBandwidth请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 一个或多个待操作的实例ID。可通过`DescribeInstances`接口返回值中的`InstanceId`获取。每次请求批量实例的上限为100。
        :type InstanceIds: list of str
        :param InternetAccessible: 公网出带宽配置。不同机型带宽上限范围不一致，具体限制详见带宽限制对账表。暂时只支持`InternetMaxBandwidthOut`参数。
        :type InternetAccessible: :class:`tcecloud.cvm.v20170312.models.InternetAccessible`
        :param StartTime: 带宽生效的起始时间。格式：`YYYY-MM-DD`，例如：`2016-10-30`。起始时间不能早于当前时间。如果起始时间是今天则新设置的带宽立即生效。该参数只对包年包月带宽有效，其他模式带宽不支持该参数，否则接口会以相应错误码返回。
        :type StartTime: str
        :param EndTime: 带宽生效的终止时间。格式：`YYYY-MM-DD`，例如：`2016-10-30`。新设置的带宽的有效期包含终止时间此日期。终止时间不能晚于包年包月实例的到期时间。实例的到期时间可通过`DescribeInstances`接口返回值中的`ExpiredTime`获取。该参数只对包年包月带宽有效，其他模式带宽不支持该参数，否则接口会以相应错误码返回。
        :type EndTime: str
        """
        self.InstanceIds = None
        self.InternetAccessible = None
        self.StartTime = None
        self.EndTime = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        if params.get("InternetAccessible") is not None:
            self.InternetAccessible = InternetAccessible()
            self.InternetAccessible._deserialize(params.get("InternetAccessible"))
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")


class InquiryPriceResetInstancesInternetMaxBandwidthResponse(AbstractModel):
    """InquiryPriceResetInstancesInternetMaxBandwidth返回参数结构体"""

    def __init__(self):
        """
        :param Price: 该参数表示带宽调整为对应大小之后的价格。
        :type Price: :class:`tcecloud.cvm.v20170312.models.Price`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Price = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Price") is not None:
            self.Price = Price()
            self.Price._deserialize(params.get("Price"))
        self.RequestId = params.get("RequestId")


class InquiryPriceResetInstancesTypeRequest(AbstractModel):
    """InquiryPriceResetInstancesType请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 一个或多个待操作的实例ID。可通过`DescribeInstances`接口返回值中的`InstanceId`获取。每次请求批量实例的上限为1。
        :type InstanceIds: list of str
        :param InstanceType: 实例机型。不同实例机型指定了不同的资源规格，具体取值可参见附表实例资源规格对照表，也可以调用查询实例资源规格列表接口获得最新的规格表。
        :type InstanceType: str
        :param ForceStop: 是否对运行中的实例选择强制关机。建议对运行中的实例先手动关机，然后再重置用户密码。取值范围：<br><li>TRUE：表示在正常关机失败后进行强制关机<br><li>FALSE：表示在正常关机失败后不进行强制关机<br><br>默认取值：FALSE。<br><br>强制关机的效果等同于关闭物理计算机的电源开关。强制关机可能会导致数据丢失或文件系统损坏，请仅在服务器不能正常关机时使用。
        :type ForceStop: bool
        """
        self.InstanceIds = None
        self.InstanceType = None
        self.ForceStop = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.InstanceType = params.get("InstanceType")
        self.ForceStop = params.get("ForceStop")


class InquiryPriceResetInstancesTypeResponse(AbstractModel):
    """InquiryPriceResetInstancesType返回参数结构体"""

    def __init__(self):
        """
        :param Price: 该参数表示调整成对应机型实例的价格。
        :type Price: :class:`tcecloud.cvm.v20170312.models.Price`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Price = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Price") is not None:
            self.Price = Price()
            self.Price._deserialize(params.get("Price"))
        self.RequestId = params.get("RequestId")


class InquiryPriceResizeInstanceDisksRequest(AbstractModel):
    """InquiryPriceResizeInstanceDisks请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 待操作的实例ID。可通过`DescribeInstances`接口返回值中的`InstanceId`获取。
        :type InstanceId: str
        :param DataDisks: 待扩容的数据盘配置信息。只支持扩容随实例购买的数据盘，且数据盘类型为：`CLOUD_BASIC`、`CLOUD_PREMIUM`、`CLOUD_SSD`。数据盘容量单位：GB。最小扩容步长：10G。关于数据盘类型的选择请参考硬盘产品简介。可选数据盘类型受到实例类型`InstanceType`限制。另外允许扩容的最大容量也因数据盘类型的不同而有所差异。
        :type DataDisks: list of DataDisk
        :param ForceStop: 是否对运行中的实例选择强制关机。建议对运行中的实例先手动关机，然后再重置用户密码。取值范围：<br><li>TRUE：表示在正常关机失败后进行强制关机<br><li>FALSE：表示在正常关机失败后不进行强制关机<br><br>默认取值：FALSE。<br><br>强制关机的效果等同于关闭物理计算机的电源开关。强制关机可能会导致数据丢失或文件系统损坏，请仅在服务器不能正常关机时使用。
        :type ForceStop: bool
        """
        self.InstanceId = None
        self.DataDisks = None
        self.ForceStop = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("DataDisks") is not None:
            self.DataDisks = []
            for item in params.get("DataDisks"):
                obj = DataDisk()
                obj._deserialize(item)
                self.DataDisks.append(obj)
        self.ForceStop = params.get("ForceStop")


class InquiryPriceResizeInstanceDisksResponse(AbstractModel):
    """InquiryPriceResizeInstanceDisks返回参数结构体"""

    def __init__(self):
        """
        :param Price: 该参数表示磁盘扩容成对应配置的价格。
        :type Price: :class:`tcecloud.cvm.v20170312.models.Price`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Price = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Price") is not None:
            self.Price = Price()
            self.Price._deserialize(params.get("Price"))
        self.RequestId = params.get("RequestId")


class InquiryPriceRunInstancesRequest(AbstractModel):
    """InquiryPriceRunInstances请求参数结构体"""

    def __init__(self):
        """
        :param Placement: 实例所在的位置。通过该参数可以指定实例所属可用区，所属项目等属性。
        :type Placement: :class:`tcecloud.cvm.v20170312.models.Placement`
        :param ImageId: 指定有效的镜像ID，格式形如`img-xxx`。镜像类型分为四种：<br/><li>公共镜像</li><li>自定义镜像</li><li>共享镜像</li><li>服务市场镜像</li><br/>可通过以下方式获取可用的镜像ID：<br/><li>`公共镜像`、`自定义镜像`、`共享镜像`的镜像ID可通过登录控制台查询；`服务镜像市场`的镜像ID可通过云市场查询。</li><li>通过调用接口 DescribeImages ，取返回信息中的`ImageId`字段。</li>
        :type ImageId: str
        :param InstanceChargeType: 实例计费类型。<br><li>PREPAID：预付费，即包年包月<br><li>POSTPAID_BY_HOUR：按小时后付费<br>默认值：POSTPAID_BY_HOUR。
        :type InstanceChargeType: str
        :param InstanceChargePrepaid: 预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月实例的购买时长、是否设置自动续费等属性。若指定实例的付费模式为预付费则该参数必传。
        :type InstanceChargePrepaid: :class:`tcecloud.cvm.v20170312.models.InstanceChargePrepaid`
        :param InstanceType: 实例机型。不同实例机型指定了不同的资源规格，具体取值可通过调用接口DescribeInstanceTypeConfigs来获得最新的规格表或参见CVM实例配置描述。若不指定该参数，则默认机型为S1.SMALL1。
        :type InstanceType: str
        :param SystemDisk: 实例系统盘配置信息。若不指定该参数，则按照系统默认值进行分配。
        :type SystemDisk: :class:`tcecloud.cvm.v20170312.models.SystemDisk`
        :param DataDisks: 实例数据盘配置信息。若不指定该参数，则默认不购买数据盘，当前仅支持购买的时候指定一个数据盘。
        :type DataDisks: list of DataDisk
        :param VirtualPrivateCloud: 私有网络相关信息配置。通过该参数可以指定私有网络的ID，子网ID等信息。若不指定该参数，则默认使用基础网络。若在此参数中指定了私有网络ip，那么InstanceCount参数只能为1。
        :type VirtualPrivateCloud: :class:`tcecloud.cvm.v20170312.models.VirtualPrivateCloud`
        :param InternetAccessible: 公网带宽相关信息设置。若不指定该参数，则默认公网带宽为0Mbps。
        :type InternetAccessible: :class:`tcecloud.cvm.v20170312.models.InternetAccessible`
        :param InstanceCount: 购买实例数量。取值范围：1，100]。默认取值：1。指定购买实例的数量不能超过用户所能购买的剩余配额数量，具体配额相关限制详见[CVM实例购买限制。
        :type InstanceCount: int
        :param InstanceName: 实例显示名称。如果不指定则默认显示
        :type InstanceName: str
        :param LoginSettings: 实例登录设置。通过该参数可以设置实例的登录方式密码、密钥或保持镜像的原始登录设置。默认情况下会随机生成密码，并以站内信方式知会到用户。
        :type LoginSettings: :class:`tcecloud.cvm.v20170312.models.LoginSettings`
        :param SecurityGroupIds: 实例所属安全组。该参数可以通过调用DescribeSecurityGroups的返回值中的sgId字段来获取。若不指定该参数，则默认不绑定安全组<font style=
        :type SecurityGroupIds: list of str
        :param EnhancedService: 增强服务。通过该参数可以指定是否开启云安全、云监控等服务。若不指定该参数，则默认开启云监控、云安全服务。
        :type EnhancedService: :class:`tcecloud.cvm.v20170312.models.EnhancedService`
        :param ClientToken: 用于保证请求幂等性的字符串。该字符串由客户生成，需保证不同请求之间唯一，最大值不超过64个ASCII字符。若不指定该参数，则无法保证请求的幂等性。<br>更多详细信息请参阅：如何保证幂等性。
        :type ClientToken: str
        :param PurchaseSource: 内部参数，购买来源。
        :type PurchaseSource: str
        """
        self.Placement = None
        self.ImageId = None
        self.InstanceChargeType = None
        self.InstanceChargePrepaid = None
        self.InstanceType = None
        self.SystemDisk = None
        self.DataDisks = None
        self.VirtualPrivateCloud = None
        self.InternetAccessible = None
        self.InstanceCount = None
        self.InstanceName = None
        self.LoginSettings = None
        self.SecurityGroupIds = None
        self.EnhancedService = None
        self.ClientToken = None
        self.PurchaseSource = None

    def _deserialize(self, params):
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        self.ImageId = params.get("ImageId")
        self.InstanceChargeType = params.get("InstanceChargeType")
        if params.get("InstanceChargePrepaid") is not None:
            self.InstanceChargePrepaid = InstanceChargePrepaid()
            self.InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))
        self.InstanceType = params.get("InstanceType")
        if params.get("SystemDisk") is not None:
            self.SystemDisk = SystemDisk()
            self.SystemDisk._deserialize(params.get("SystemDisk"))
        if params.get("DataDisks") is not None:
            self.DataDisks = []
            for item in params.get("DataDisks"):
                obj = DataDisk()
                obj._deserialize(item)
                self.DataDisks.append(obj)
        if params.get("VirtualPrivateCloud") is not None:
            self.VirtualPrivateCloud = VirtualPrivateCloud()
            self.VirtualPrivateCloud._deserialize(params.get("VirtualPrivateCloud"))
        if params.get("InternetAccessible") is not None:
            self.InternetAccessible = InternetAccessible()
            self.InternetAccessible._deserialize(params.get("InternetAccessible"))
        self.InstanceCount = params.get("InstanceCount")
        self.InstanceName = params.get("InstanceName")
        if params.get("LoginSettings") is not None:
            self.LoginSettings = LoginSettings()
            self.LoginSettings._deserialize(params.get("LoginSettings"))
        self.SecurityGroupIds = params.get("SecurityGroupIds")
        if params.get("EnhancedService") is not None:
            self.EnhancedService = EnhancedService()
            self.EnhancedService._deserialize(params.get("EnhancedService"))
        self.ClientToken = params.get("ClientToken")
        self.PurchaseSource = params.get("PurchaseSource")


class InquiryPriceRunInstancesResponse(AbstractModel):
    """InquiryPriceRunInstances返回参数结构体"""

    def __init__(self):
        """
        :param Price: 该参数表示对应配置实例的价格。
        :type Price: :class:`tcecloud.cvm.v20170312.models.Price`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Price = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Price") is not None:
            self.Price = Price()
            self.Price._deserialize(params.get("Price"))
        self.RequestId = params.get("RequestId")


class InquiryPriceTerminateInstancesRequest(AbstractModel):
    """InquiryPriceTerminateInstances请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 1
        :type InstanceIds: list of str
        :param ReleaseAddress: 1
        :type ReleaseAddress: bool
        :param DryRun: 1
        :type DryRun: bool
        """
        self.InstanceIds = None
        self.ReleaseAddress = None
        self.DryRun = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.ReleaseAddress = params.get("ReleaseAddress")
        self.DryRun = params.get("DryRun")


class InquiryPriceTerminateInstancesResponse(AbstractModel):
    """InquiryPriceTerminateInstances返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class InquiryPriceUpdateDisasterRecoverGroupRequest(AbstractModel):
    """InquiryPriceUpdateDisasterRecoverGroup请求参数结构体"""

    def __init__(self):
        """
        :param DisasterRecoverGroupId: 1
        :type DisasterRecoverGroupId: str
        :param Name: 1
        :type Name: str
        """
        self.DisasterRecoverGroupId = None
        self.Name = None

    def _deserialize(self, params):
        self.DisasterRecoverGroupId = params.get("DisasterRecoverGroupId")
        self.Name = params.get("Name")


class InquiryPriceUpdateDisasterRecoverGroupResponse(AbstractModel):
    """InquiryPriceUpdateDisasterRecoverGroup返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class Instance(AbstractModel):
    """描述实例的信息"""

    def __init__(self):
        """
                :param Placement: 实例所在的位置。
                :type Placement: :class:`tcecloud.cvm.v20170312.models.Placement`
                :param InstanceId: 实例`ID`。
                :type InstanceId: str
                :param InstanceType: 实例机型。
                :type InstanceType: str
                :param CPU: 实例的CPU核数，单位：核。
                :type CPU: int
                :param Memory: 实例内存容量，单位：`GB`。
                :type Memory: int
                :param RestrictState: 实例业务状态。取值范围：<br><li>NORMAL：表示正常状态的实例<br><li>EXPIRED：表示过期的实例<br><li>PROTECTIVELY_ISOLATED：表示被安全隔离的实例。
                :type RestrictState: str
                :param InstanceName: 实例名称。
                :type InstanceName: str
                :param InstanceChargeType: 实例计费模式。取值范围：<br><li>`PREPAID`：表示预付费，即包年包月<br><li>`POSTPAID_BY_HOUR`：表示后付费，即按量计费<br><li>`CDHPAID`：`CDH`付费，即只对`CDH`计费，不对`CDH`上的实例计费。
                :type InstanceChargeType: str
                :param SystemDisk: 实例系统盘信息。
                :type SystemDisk: :class:`tcecloud.cvm.v20170312.models.SystemDisk`
                :param DataDisks: 实例数据盘信息。只包含随实例购买的数据盘。
                :type DataDisks: list of DataDisk
                :param PrivateIpAddresses: 实例主网卡的内网`IP`列表。
                :type PrivateIpAddresses: list of str
                :param PublicIpAddresses: 实例主网卡的公网`IP`列表。
                :type PublicIpAddresses: list of str
                :param InternetAccessible: 实例带宽信息。
                :type InternetAccessible: :class:`tcecloud.cvm.v20170312.models.InternetAccessible`
                :param VirtualPrivateCloud: 实例所属虚拟私有网络信息。
                :type VirtualPrivateCloud: :class:`tcecloud.cvm.v20170312.models.VirtualPrivateCloud`
                :param ImageId: 生产实例所使用的镜像`ID`。
                :type ImageId: str
                :param RenewFlag: 自动续费标识。取值范围：<br><li>`NOTIFY_AND_MANUAL_RENEW`：表示通知即将过期，但不自动续费<br><li>`NOTIFY_AND_AUTO_RENEW`：表示通知即将过期，而且自动续费<br><li>`DISABLE_NOTIFY_AND_MANUAL_RENEW`：表示不通知即将过期，也不自动续费。
                :type RenewFlag: str
                :param CreatedTime: 创建时间。按照`ISO8601`标准表示，并且使用`UTC`时间。格式为：`YYYY-MM-DDThh:mm:ssZ`。
                :type CreatedTime: str
                :param ExpiredTime: 到期时间。按照`ISO8601`标准表示，并且使用`UTC`时间。格式为：`YYYY-MM-DDThh:mm:ssZ`。
                :type ExpiredTime: str
                :param InstanceState: 实例状态。取值范围：<br><li>PENDING：表示创建中<br></li><li>LAUNCH_FAILED：表示创建失败<br></li><li>RUNNING：表示运行中<br></li><li>STOPPED：表示关机<br></li><li>STARTING：表示开机中<br></li><li>STOPPING：表示关机中<br></li><li>REBOOTING：表示重启中<br></li><li>SHUTDOWN：表示停止待销毁<br></li><li>TERMINATING：表示销毁中。<br></li>
        注意：此字段可能返回 null，表示取不到有效值。
                :type InstanceState: str
                :param LatestOperation: 实例的最新操作。例：StopInstances、ResetInstance。
        注意：此字段可能返回 null，表示取不到有效值。
                :type LatestOperation: str
                :param LatestOperationState: 实例的最新操作状态。取值范围：<br><li>SUCCESS：表示操作成功<br><li>OPERATING：表示操作执行中<br><li>FAILED：表示操作失败
        注意：此字段可能返回 null，表示取不到有效值。
                :type LatestOperationState: str
                :param LatestOperationRequestId: 实例最新操作的唯一请求 ID。
        注意：此字段可能返回 null，表示取不到有效值。
                :type LatestOperationRequestId: str
                :param SecurityGroupIds: 实例所属安全组。该参数可以通过调用 DescribeSecurityGroups 的返回值中的sgId字段来获取。
        注意：此字段可能返回 null，表示取不到有效值。
                :type SecurityGroupIds: list of str
                :param LoginSettings: 实例登录设置。目前只返回实例所关联的密钥。
        注意：此字段可能返回 null，表示取不到有效值。
                :type LoginSettings: :class:`tcecloud.cvm.v20170312.models.LoginSettings`
                :param DisasterRecoverGroupId: 分散置放群组ID。
        注意：此字段可能返回 null，表示取不到有效值。
                :type DisasterRecoverGroupId: str
                :param Tags: 实例关联的标签列表。
        注意：此字段可能返回 null，表示取不到有效值。
                :type Tags: list of Tag
        """
        self.Placement = None
        self.InstanceId = None
        self.InstanceType = None
        self.CPU = None
        self.Memory = None
        self.RestrictState = None
        self.InstanceName = None
        self.InstanceChargeType = None
        self.SystemDisk = None
        self.DataDisks = None
        self.PrivateIpAddresses = None
        self.PublicIpAddresses = None
        self.InternetAccessible = None
        self.VirtualPrivateCloud = None
        self.ImageId = None
        self.RenewFlag = None
        self.CreatedTime = None
        self.ExpiredTime = None
        self.InstanceState = None
        self.LatestOperation = None
        self.LatestOperationState = None
        self.LatestOperationRequestId = None
        self.SecurityGroupIds = None
        self.LoginSettings = None
        self.DisasterRecoverGroupId = None
        self.Tags = None
        self.OsName = None

    def _deserialize(self, params):
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        self.InstanceId = params.get("InstanceId")
        self.InstanceType = params.get("InstanceType")
        self.CPU = params.get("CPU")
        self.Memory = params.get("Memory")
        self.RestrictState = params.get("RestrictState")
        self.InstanceName = params.get("InstanceName")
        self.InstanceChargeType = params.get("InstanceChargeType")
        if params.get("SystemDisk") is not None:
            self.SystemDisk = SystemDisk()
            self.SystemDisk._deserialize(params.get("SystemDisk"))
        if params.get("DataDisks") is not None:
            self.DataDisks = []
            for item in params.get("DataDisks"):
                obj = DataDisk()
                obj._deserialize(item)
                self.DataDisks.append(obj)
        self.PrivateIpAddresses = params.get("PrivateIpAddresses")
        self.PublicIpAddresses = params.get("PublicIpAddresses")
        if params.get("InternetAccessible") is not None:
            self.InternetAccessible = InternetAccessible()
            self.InternetAccessible._deserialize(params.get("InternetAccessible"))
        if params.get("VirtualPrivateCloud") is not None:
            self.VirtualPrivateCloud = VirtualPrivateCloud()
            self.VirtualPrivateCloud._deserialize(params.get("VirtualPrivateCloud"))
        self.ImageId = params.get("ImageId")
        self.RenewFlag = params.get("RenewFlag")
        self.CreatedTime = params.get("CreatedTime")
        self.ExpiredTime = params.get("ExpiredTime")
        self.InstanceState = params.get("InstanceState")
        self.LatestOperation = params.get("LatestOperation")
        self.LatestOperationState = params.get("LatestOperationState")
        self.LatestOperationRequestId = params.get("LatestOperationRequestId")
        self.SecurityGroupIds = params.get("SecurityGroupIds")
        if params.get("LoginSettings") is not None:
            self.LoginSettings = LoginSettings()
            self.LoginSettings._deserialize(params.get("LoginSettings"))
        self.DisasterRecoverGroupId = params.get("DisasterRecoverGroupId")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.OsName = params.get("OsName")


class InstanceChargePrepaid(AbstractModel):
    """描述了实例的计费模式"""

    def __init__(self):
        """
        :param Period: 购买实例的时长，单位：月。取值范围：1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 24, 36。
        :type Period: int
        :param RenewFlag: 自动续费标识。取值范围：<br><li>NOTIFY_AND_AUTO_RENEW：通知过期且自动续费<br><li>NOTIFY_AND_MANUAL_RENEW：通知过期不自动续费<br><li>DISABLE_NOTIFY_AND_MANUAL_RENEW：不通知过期不自动续费<br><br>默认取值：NOTIFY_AND_AUTO_RENEW。若该参数指定为NOTIFY_AND_AUTO_RENEW，在账户余额充足的情况下，实例到期后将按月自动续费。
        :type RenewFlag: str
        """
        self.Period = None
        self.RenewFlag = None

    def _deserialize(self, params):
        self.Period = params.get("Period")
        self.RenewFlag = params.get("RenewFlag")


class InstanceChargeTypeConfig(AbstractModel):
    """计费类型配置信息"""

    def __init__(self):
        """
        :param InstanceChargeType: 实例计费类型
        :type InstanceChargeType: str
        :param Description: 实例计费类型描述
        :type Description: str
        """
        self.InstanceChargeType = None
        self.Description = None

    def _deserialize(self, params):
        self.InstanceChargeType = params.get("InstanceChargeType")
        self.Description = params.get("Description")


class InstanceConfigInfoItem(AbstractModel):
    """实例静态配置信息。"""

    def __init__(self):
        """
        :param type: 实例规格。
        :type type: str
        :param typeName: 实例规格名称。
        :type typeName: str
        :param order: 优先级。
        :type order: int
        :param instanceFamilies: 实例族信息列表。
        :type instanceFamilies: list of InstanceFamilyItem
        """
        self.type = None
        self.typeName = None
        self.order = None
        self.instanceFamilies = None

    def _deserialize(self, params):
        self.type = params.get("type")
        self.typeName = params.get("typeName")
        self.order = params.get("order")
        if params.get("instanceFamilies") is not None:
            self.instanceFamilies = []
            for item in params.get("instanceFamilies"):
                obj = InstanceFamilyItem()
                obj._deserialize(item)
                self.instanceFamilies.append(obj)


class InstanceConnectivity(AbstractModel):
    """实例端口连通性状态，用于表示实例默认远程登录端口和ICMP端口的连通性。"""

    def __init__(self):
        """
        :param InstanceId: 实例`ID`
        :type InstanceId: str
        :param DefaultLoginPortConnectivity: 默认远程登录端口连通性状态
        :type DefaultLoginPortConnectivity: bool
        :param ICMPConnectivity: ping包是否可达
        :type ICMPConnectivity: bool
        """
        self.InstanceId = None
        self.DefaultLoginPortConnectivity = None
        self.ICMPConnectivity = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.DefaultLoginPortConnectivity = params.get("DefaultLoginPortConnectivity")
        self.ICMPConnectivity = params.get("ICMPConnectivity")


class InstanceFamilyConfig(AbstractModel):
    """描述实例的机型族配置信息
    形如：{'InstanceFamilyName': '标准型S1', 'InstanceFamily': 'S1'}、{'InstanceFamilyName': '网络优化型N1', 'InstanceFamily': 'N1'}、{'InstanceFamilyName': '高IO型I1', 'InstanceFamily': 'I1'}等。

    """

    def __init__(self):
        """
        :param InstanceFamilyName: 机型族名称的中文全称。
        :type InstanceFamilyName: str
        :param InstanceFamily: 机型族名称的英文简称。
        :type InstanceFamily: str
        """
        self.InstanceFamilyName = None
        self.InstanceFamily = None

    def _deserialize(self, params):
        self.InstanceFamilyName = params.get("InstanceFamilyName")
        self.InstanceFamily = params.get("InstanceFamily")


class InstanceFamilyItem(AbstractModel):
    """实例族信息。"""

    def __init__(self):
        """
        :param instanceFamily: 实例族。
        :type instanceFamily: str
        :param order: 优先级。
        :type order: int
        :param instanceTypes: 实例类型信息列表。
        :type instanceTypes: list of InstanceTypeItem
        """
        self.instanceFamily = None
        self.order = None
        self.instanceTypes = None

    def _deserialize(self, params):
        self.instanceFamily = params.get("instanceFamily")
        self.order = params.get("order")
        if params.get("instanceTypes") is not None:
            self.instanceTypes = []
            for item in params.get("instanceTypes"):
                obj = InstanceTypeItem()
                obj._deserialize(item)
                self.instanceTypes.append(obj)


class InstanceOrder(AbstractModel):
    """实例订单详情信息。"""


class InstanceReturnable(AbstractModel):
    """实例可退还信息。"""

    def __init__(self):
        """
        :param InstanceId: 实例`ID`。
        :type InstanceId: str
        :param IsReturnable: 实例是否可退还。
        :type IsReturnable: bool
        :param ReturnFailCode: 实例退还失败错误码。
        :type ReturnFailCode: int
        :param ReturnFailMessage: 实例退还失败错误信息。
        :type ReturnFailMessage: str
        """
        self.InstanceId = None
        self.IsReturnable = None
        self.ReturnFailCode = None
        self.ReturnFailMessage = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.IsReturnable = params.get("IsReturnable")
        self.ReturnFailCode = params.get("ReturnFailCode")
        self.ReturnFailMessage = params.get("ReturnFailMessage")


class InstanceStatus(AbstractModel):
    """描述实例的状态。状态类型详见实例状态表"""

    def __init__(self):
        """
                :param InstanceId: 实例`ID`。
                :type InstanceId: str
                :param InstanceState: 实例状态。
                :type InstanceState: str
                :param LatestOperation: 实例的最新操作。例：StopInstances、ResetInstance。
        注意：此字段可能返回 null，表示取不到有效值。
                :type LatestOperation: str
                :param LatestOperationState: 实例的最新操作状态。取值范围：<br><li>SUCCESS：表示操作成功<br><li>OPERATING：表示操作执行中<br><li>FAILED：表示操作失败
        注意：此字段可能返回 null，表示取不到有效值。
                :type LatestOperationState: str
                :param LatestOperationRequestId: 实例最新操作的唯一请求 ID。
        注意：此字段可能返回 null，表示取不到有效值。
                :type LatestOperationRequestId: str
        """
        self.InstanceId = None
        self.InstanceState = None
        self.LatestOperation = None
        self.LatestOperationState = None
        self.LatestOperationRequestId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.InstanceState = params.get("InstanceState")
        self.LatestOperation = params.get("LatestOperation")
        self.LatestOperationState = params.get("LatestOperationState")
        self.LatestOperationRequestId = params.get("LatestOperationRequestId")


class InstanceTypeConfig(AbstractModel):
    """描述实例机型配置信息"""

    def __init__(self):
        """
        :param Zone: 可用区。
        :type Zone: str
        :param InstanceType: 实例机型。
        :type InstanceType: str
        :param InstanceFamily: 实例机型系列。
        :type InstanceFamily: str
        :param GPU: GPU核数，单位：核。
        :type GPU: int
        :param CPU: CPU核数，单位：核。
        :type CPU: int
        :param Memory: 内存容量，单位：`GB`。
        :type Memory: int
        :param CbsSupport: 是否支持云硬盘。取值范围：<br><li>`TRUE`：表示支持云硬盘；<br><li>`FALSE`：表示不支持云硬盘。
        :type CbsSupport: str
        :param InstanceTypeState: 机型状态。取值范围：<br><li>`AVAILABLE`：表示机型可用；<br><li>`UNAVAILABLE`：表示机型不可用。
        :type InstanceTypeState: str
        """
        self.Zone = None
        self.InstanceType = None
        self.InstanceFamily = None
        self.GPU = None
        self.CPU = None
        self.Memory = None
        self.CbsSupport = None
        self.InstanceTypeState = None

    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.InstanceType = params.get("InstanceType")
        self.InstanceFamily = params.get("InstanceFamily")
        self.GPU = params.get("GPU")
        self.CPU = params.get("CPU")
        self.Memory = params.get("Memory")
        self.CbsSupport = params.get("CbsSupport")
        self.InstanceTypeState = params.get("InstanceTypeState")


class InstanceTypeItem(AbstractModel):
    """实例类型信息。"""

    def __init__(self):
        """
        :param InstanceType: 实例类型。
        :type InstanceType: str
        :param Cpu: CPU核数。
        :type Cpu: int
        :param Memory: 内存大小。
        :type Memory: int
        :param Gpu: GPU核数。
        :type Gpu: int
        :param Fpga: FPGA核数。
        :type Fpga: int
        :param StorageBlock: 存储块数。
        :type StorageBlock: int
        :param NetworkCard: 网卡数。
        :type NetworkCard: int
        :param MaxBandwidth: 最大带宽。
        :type MaxBandwidth: float
        :param Frequency: 主频。
        :type Frequency: str
        :param CpuModelName: CPU型号名称。
        :type CpuModelName: str
        :param Pps: 包转发率。
        :type Pps: int
        :param Externals: 外部信息。
        :type Externals: :class:`tcecloud.cvm.v20170312.models.Externals`
        :param Remark: 备注信息。
        :type Remark: str
        """
        self.InstanceType = None
        self.Cpu = None
        self.Memory = None
        self.Gpu = None
        self.Fpga = None
        self.StorageBlock = None
        self.NetworkCard = None
        self.MaxBandwidth = None
        self.Frequency = None
        self.CpuModelName = None
        self.Pps = None
        self.Externals = None
        self.Remark = None

    def _deserialize(self, params):
        self.InstanceType = params.get("InstanceType")
        self.Cpu = params.get("Cpu")
        self.Memory = params.get("Memory")
        self.Gpu = params.get("Gpu")
        self.Fpga = params.get("Fpga")
        self.StorageBlock = params.get("StorageBlock")
        self.NetworkCard = params.get("NetworkCard")
        self.MaxBandwidth = params.get("MaxBandwidth")
        self.Frequency = params.get("Frequency")
        self.CpuModelName = params.get("CpuModelName")
        self.Pps = params.get("Pps")
        if params.get("Externals") is not None:
            self.Externals = Externals()
            self.Externals._deserialize(params.get("Externals"))
        self.Remark = params.get("Remark")


class InstanceTypeNameConfig(AbstractModel):
    """实例类型名称配置"""

    def __init__(self):
        """
        :param ShowInMenu: 是否显示到实例类型列表
        :type ShowInMenu: bool
        :param InstanceFamilyName: 实例类型中文名
        :type InstanceFamilyName: str
        :param InstanceFamily: 实例类型
        :type InstanceFamily: str
        """
        self.ShowInMenu = None
        self.InstanceFamilyName = None
        self.InstanceFamily = None

    def _deserialize(self, params):
        self.ShowInMenu = params.get("ShowInMenu")
        self.InstanceFamilyName = params.get("InstanceFamilyName")
        self.InstanceFamily = params.get("InstanceFamily")


class InstanceTypeQuota(AbstractModel):
    """描述实例机型配额信息"""

    def __init__(self):
        """
        :param Zone: 可用区。
        :type Zone: str
        :param InstanceType: 实例机型。
        :type InstanceType: str
        :param InstanceQuota: 实例机型配额。
        :type InstanceQuota: int
        :param InstanceChargeType: 实例计费模式。取值范围： <br>*`PREPAID`：表示预付费，即包年包月 <br>* `POSTPAID_BY_HOUR`：表示后付费，即按量计费 * `CDHPAID`：CDH付费，即只对CDH计费，不对CDH上的实例计费。
        :type InstanceChargeType: str
        :param DeviceClass: 实例类型。
        :type DeviceClass: str
        :param CPU: 实例的CPU核数，单位：核。
        :type CPU: int
        :param Memory: 实例内存容量，单位：`GB`。
        :type Memory: int
        :param GPU: 实例的GPU核数，单位：核。
        :type GPU: int
        """
        self.Zone = None
        self.Status = None
        self.InstanceType = None
        self.InstanceQuota = None
        self.InstanceChargeType = None
        self.DeviceClass = None
        self.TypeName = None
        self.Price = None
        self.InstanceFamily = None
        self.Cpu = None
        self.Memory = None
        self.GPU = None

    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.Status = params.get("Status")
        self.InstanceType = params.get("InstanceType")
        self.InstanceQuota = params.get("InstanceQuota")
        self.InstanceChargeType = params.get("InstanceChargeType")
        self.DeviceClass = params.get("DeviceClass")
        self.TypeName = params.get("TypeName")
        self.Price = params.get("Price")
        self.InstanceFamily = params.get("InstanceFamily")
        self.Cpu = params.get("Cpu")
        self.Memory = params.get("Memory")
        self.GPU = params.get("GPU")


class InstancesRecentFailedOperationSet(AbstractModel):
    """实例最新失败操作"""

    def __init__(self):
        """
        :param InstanceId: 实例ID
        :type InstanceId: str
        :param EventType: 操作事件类型
        :type EventType: str
        :param CreateTime: 操作事件发生时间
        :type CreateTime: str
        """
        self.InstanceId = None
        self.EventType = None
        self.CreateTime = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.EventType = params.get("EventType")
        self.CreateTime = params.get("CreateTime")


class InternetAccessible(AbstractModel):
    """描述了实例的公网可访问性，声明了实例的公网使用计费模式，最大带宽等"""

    def __init__(self):
        """
        :param InternetChargeType: 网络计费类型。取值范围：<br><li>BANDWIDTH_PREPAID：预付费按带宽结算<br><li>TRAFFIC_POSTPAID_BY_HOUR：流量按小时后付费<br><li>BANDWIDTH_POSTPAID_BY_HOUR：带宽按小时后付费<br><li>BANDWIDTH_PACKAGE：带宽包用户<br>默认取值：TRAFFIC_POSTPAID_BY_HOUR。
        :type InternetChargeType: str
        :param InternetMaxBandwidthOut: 公网出带宽上限，单位：Mbps。默认值：0Mbps。不同机型带宽上限范围不一致，具体限制详见购买网络带宽。
        :type InternetMaxBandwidthOut: int
        :param PublicIpAssigned: 是否分配公网IP。取值范围：<br><li>TRUE：表示分配公网IP<br><li>FALSE：表示不分配公网IP<br><br>当公网带宽大于0Mbps时，可自由选择开通与否，默认开通公网IP；当公网带宽为0，则不允许分配公网IP。
        :type PublicIpAssigned: bool
        """
        self.InternetChargeType = None
        self.InternetMaxBandwidthOut = None
        self.PublicIpAssigned = None

    def _deserialize(self, params):
        self.InternetChargeType = params.get("InternetChargeType")
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        self.PublicIpAssigned = params.get("PublicIpAssigned")


class InternetAccessibleModifyChargeType(AbstractModel):
    """描述了网络计费"""

    def __init__(self):
        """
        :param InternetChargeType: 网络付费模式
        :type InternetChargeType: str
        :param InternetMaxBandwidthOut: 外网出带宽值
        :type InternetMaxBandwidthOut: int
        """
        self.InternetChargeType = None
        self.InternetMaxBandwidthOut = None

    def _deserialize(self, params):
        self.InternetChargeType = params.get("InternetChargeType")
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")


class InternetBandwidthConfig(AbstractModel):
    """描述了按带宽计费的相关信息"""

    def __init__(self):
        """
        :param StartTime: 开始时间。按照`ISO8601`标准表示，并且使用`UTC`时间。格式为：`YYYY-MM-DDThh:mm:ssZ`。
        :type StartTime: str
        :param EndTime: 结束时间。按照`ISO8601`标准表示，并且使用`UTC`时间。格式为：`YYYY-MM-DDThh:mm:ssZ`。
        :type EndTime: str
        :param InternetAccessible: 实例带宽信息。
        :type InternetAccessible: :class:`tcecloud.cvm.v20170312.models.InternetAccessible`
        """
        self.StartTime = None
        self.EndTime = None
        self.InternetAccessible = None

    def _deserialize(self, params):
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        if params.get("InternetAccessible") is not None:
            self.InternetAccessible = InternetAccessible()
            self.InternetAccessible._deserialize(params.get("InternetAccessible"))


class InternetChargeTypeConfig(AbstractModel):
    """描述了网络计费"""

    def __init__(self):
        """
        :param InternetChargeType: 网络计费模式。
        :type InternetChargeType: str
        :param Description: 网络计费模式描述信息。
        :type Description: str
        """
        self.InternetChargeType = None
        self.Description = None

    def _deserialize(self, params):
        self.InternetChargeType = params.get("InternetChargeType")
        self.Description = params.get("Description")


class ItemPrice(AbstractModel):
    """描述了单项的价格信息"""

    def __init__(self):
        """
        :param UnitPrice: 后续单价，单位：元。
        :type UnitPrice: float
        :param ChargeUnit: 后续计价单元，可取值范围： <br><li>HOUR：表示计价单元是按每小时来计算。当前涉及该计价单元的场景有：实例按小时后付费（POSTPAID_BY_HOUR）、带宽按小时后付费（BANDWIDTH_POSTPAID_BY_HOUR）：<br><li>GB：表示计价单元是按每GB来计算。当前涉及该计价单元的场景有：流量按小时后付费（TRAFFIC_POSTPAID_BY_HOUR）。
        :type ChargeUnit: str
        :param OriginalPrice: 预支费用的原价，单位：元。
        :type OriginalPrice: float
        :param DiscountPrice: 预支费用的折扣价，单位：元。
        :type DiscountPrice: float
        """
        self.UnitPrice = None
        self.ChargeUnit = None
        self.OriginalPrice = None
        self.DiscountPrice = None

    def _deserialize(self, params):
        self.UnitPrice = params.get("UnitPrice")
        self.ChargeUnit = params.get("ChargeUnit")
        self.OriginalPrice = params.get("OriginalPrice")
        self.DiscountPrice = params.get("DiscountPrice")


class KeyPair(AbstractModel):
    """描述密钥对信息"""

    def __init__(self):
        """
        :param KeyId: 密钥对的`ID`，是密钥对的唯一标识。
        :type KeyId: str
        :param KeyName: 密钥对名称。
        :type KeyName: str
        :param ProjectId: 密钥对所属的项目`ID`。
        :type ProjectId: str
        :param Description: 密钥对描述信息。
        :type Description: str
        :param PublicKey: 密钥对的纯文本公钥。
        :type PublicKey: str
        :param PrivateKey: 密钥对的纯文本私钥。Tce不会保管私钥，请用户自行妥善保存。
        :type PrivateKey: str
        :param AssociatedInstanceIds: 密钥关联的实例`ID`列表。
        :type AssociatedInstanceIds: list of str
        :param CreatedTime: 创建时间。按照`ISO8601`标准表示，并且使用`UTC`时间。格式为：`YYYY-MM-DDThh:mm:ssZ`。
        :type CreatedTime: str
        """
        self.KeyId = None
        self.KeyName = None
        self.ProjectId = None
        self.Description = None
        self.PublicKey = None
        self.PrivateKey = None
        self.AssociatedInstanceIds = None
        self.CreatedTime = None

    def _deserialize(self, params):
        self.KeyId = params.get("KeyId")
        self.KeyName = params.get("KeyName")
        self.ProjectId = params.get("ProjectId")
        self.Description = params.get("Description")
        self.PublicKey = params.get("PublicKey")
        self.PrivateKey = params.get("PrivateKey")
        self.AssociatedInstanceIds = params.get("AssociatedInstanceIds")
        self.CreatedTime = params.get("CreatedTime")


class KvType(AbstractModel):
    """键值类型"""

    def __init__(self):
        """
        :param Name: 键的名称
        :type Name: str
        :param Value: 键所对应的值
        :type Value: str
        """
        self.Name = None
        self.Value = None

    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Value = params.get("Value")


class LiveMigrateInstanceRequest(AbstractModel):
    """LiveMigrateInstance请求参数结构体"""

    def __init__(self):
        """
        :param ClientVersion: 客户端版本。
        :type ClientVersion: str
        :param InstanceId: 迁移目的实例ID。
        :type InstanceId: str
        :param SysInfo: 迁移源实例系统信息。
        :type SysInfo: :class:`tcecloud.cvm.v20170312.models.ClientSysInfo`
        :param IgnoreCheckNetworkConnectivity: 是否忽略网络连通性检查
        :type IgnoreCheckNetworkConnectivity: bool
        """
        self.ClientVersion = None
        self.InstanceId = None
        self.SysInfo = None
        self.IgnoreCheckNetworkConnectivity = None

    def _deserialize(self, params):
        self.ClientVersion = params.get("ClientVersion")
        self.InstanceId = params.get("InstanceId")
        if params.get("SysInfo") is not None:
            self.SysInfo = ClientSysInfo()
            self.SysInfo._deserialize(params.get("SysInfo"))
        self.IgnoreCheckNetworkConnectivity = params.get("IgnoreCheckNetworkConnectivity")


class LiveMigrateInstanceResponse(AbstractModel):
    """LiveMigrateInstance返回参数结构体"""

    def __init__(self):
        """
        :param Ip: 目的实例外网IP。
        :type Ip: str
        :param Password: 目的子机密码。
        :type Password: str
        :param LanIp: 目的实例内网IP。
        :type LanIp: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Ip = None
        self.Password = None
        self.LanIp = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Ip = params.get("Ip")
        self.Password = params.get("Password")
        self.LanIp = params.get("LanIp")
        self.RequestId = params.get("RequestId")


class LiveMigrateRequest(AbstractModel):
    """LiveMigrate请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 待迁移实例Id
        :type InstanceId: str
        :param HostIps: 指定母机迁移
        :type HostIps: list of str
        :param SoldPool: 要迁入的售卖池， PLAIN, OVERSOLD等
        :type SoldPool: str
        :param Zones: 跨可用区迁移，要传入可用区表
        :type Zones: list of str
        :param MaxBandwidth: 最大迁移带宽
        :type MaxBandwidth: int
        :param MaxTimeout: 最大迁移超时
        :type MaxTimeout: int
        """
        self.InstanceId = None
        self.HostIps = None
        self.SoldPool = None
        self.Zones = None
        self.MaxBandwidth = None
        self.MaxTimeout = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.HostIps = params.get("HostIps")
        self.SoldPool = params.get("SoldPool")
        self.Zones = params.get("Zones")
        self.MaxBandwidth = params.get("MaxBandwidth")
        self.MaxTimeout = params.get("MaxTimeout")


class LiveMigrateResponse(AbstractModel):
    """LiveMigrate返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class LoginSettings(AbstractModel):
    """描述了实例登录相关配置与信息。"""

    def __init__(self):
        """
        :param Password: 实例登录密码。不同操作系统类型密码复杂度限制不一样，具体如下：<br><li>Linux实例密码必须8到16位，至少包括两项[a-z，A-Z]、[0-9] 和 [( ) ` ~ ! @ # $ % ^ & * - + = | { } [ ] : ; ' , . ? / ]中的特殊符号。<br><li>Windows实例密码必须12到16位，至少包括三项[a-z]，[A-Z]，[0-9] 和 [( ) ` ~ ! @ # $ % ^ & * - + = { } [ ] : ; ' , . ? /]中的特殊符号。<br><br>若不指定该参数，则由系统随机生成密码，并通过站内信方式通知到用户。
        :type Password: str
        :param KeyIds: 密钥ID列表。关联密钥后，就可以通过对应的私钥来访问实例；KeyId可通过接口DescribeKeyPairs获取，密钥与密码不能同时指定，同时Windows操作系统不支持指定密钥。当前仅支持购买的时候指定一个密钥。
        :type KeyIds: list of str
        :param KeepImageLogin: 保持镜像的原始设置。该参数与Password或KeyIds.N不能同时指定。只有使用自定义镜像、共享镜像或外部导入镜像创建实例时才能指定该参数为TRUE。取值范围：<br><li>TRUE：表示保持镜像的登录设置<br><li>FALSE：表示不保持镜像的登录设置<br><br>默认取值：FALSE。
        :type KeepImageLogin: str
        """
        self.Password = None
        self.KeyIds = None
        self.KeepImageLogin = None

    def _deserialize(self, params):
        self.Password = params.get("Password")
        self.KeyIds = params.get("KeyIds")
        self.KeepImageLogin = params.get("KeepImageLogin")


class ModifyAddressAttributeRequest(AbstractModel):
    """ModifyAddressAttribute请求参数结构体"""

    def __init__(self):
        """
        :param AddressId: 1
        :type AddressId: str
        :param AddressName: 1
        :type AddressName: str
        :param EipDirectConnection: 1
        :type EipDirectConnection: str
        """
        self.AddressId = None
        self.AddressName = None
        self.EipDirectConnection = None

    def _deserialize(self, params):
        self.AddressId = params.get("AddressId")
        self.AddressName = params.get("AddressName")
        self.EipDirectConnection = params.get("EipDirectConnection")


class ModifyAddressAttributeResponse(AbstractModel):
    """ModifyAddressAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyAddressesBandwidthRequest(AbstractModel):
    """ModifyAddressesBandwidth请求参数结构体"""

    def __init__(self):
        """
        :param AddressIds: 1
        :type AddressIds: list of str
        :param InternetMaxBandwidthOut: 1
        :type InternetMaxBandwidthOut: int
        :param DealId: 1
        :type DealId: str
        """
        self.AddressIds = None
        self.InternetMaxBandwidthOut = None
        self.DealId = None

    def _deserialize(self, params):
        self.AddressIds = params.get("AddressIds")
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        self.DealId = params.get("DealId")


class ModifyAddressesBandwidthResponse(AbstractModel):
    """ModifyAddressesBandwidth返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDisasterRecoverGroupAttributeRequest(AbstractModel):
    """ModifyDisasterRecoverGroupAttribute请求参数结构体"""

    def __init__(self):
        """
        :param DisasterRecoverGroupId: 分散置放群组ID，可使用DescribeDisasterRecoverGroups接口获取。
        :type DisasterRecoverGroupId: str
        :param Name: 分散置放群组名称，长度1-60个字符，支持中、英文。
        :type Name: str
        """
        self.DisasterRecoverGroupId = None
        self.Name = None

    def _deserialize(self, params):
        self.DisasterRecoverGroupId = params.get("DisasterRecoverGroupId")
        self.Name = params.get("Name")


class ModifyDisasterRecoverGroupAttributeResponse(AbstractModel):
    """ModifyDisasterRecoverGroupAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDisasterRecoverGroupRequest(AbstractModel):
    """ModifyDisasterRecoverGroup请求参数结构体"""

    def __init__(self):
        """
        :param DisasterRecoverGroupId: 容灾组id，可使用DescribeDisasterRecoverGroups接口查询。
        :type DisasterRecoverGroupId: str
        :param Name: 容灾组名称，最长128个字符。
        :type Name: str
        """
        self.DisasterRecoverGroupId = None
        self.Name = None

    def _deserialize(self, params):
        self.DisasterRecoverGroupId = params.get("DisasterRecoverGroupId")
        self.Name = params.get("Name")


class ModifyDisasterRecoverGroupResponse(AbstractModel):
    """ModifyDisasterRecoverGroup返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyHostsAttributeRequest(AbstractModel):
    """ModifyHostsAttribute请求参数结构体"""

    def __init__(self):
        """
        :param HostIds: 一个或多个待操作的CDH实例ID。
        :type HostIds: list of str
        :param HostName: CDH实例显示名称。可任意命名，但不得超过60个字符。
        :type HostName: str
        :param RenewFlag: 自动续费标识。
        :type RenewFlag: str
        """
        self.HostIds = None
        self.HostName = None
        self.RenewFlag = None

    def _deserialize(self, params):
        self.HostIds = params.get("HostIds")
        self.HostName = params.get("HostName")
        self.RenewFlag = params.get("RenewFlag")


class ModifyHostsAttributeResponse(AbstractModel):
    """ModifyHostsAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyImageAttributeRequest(AbstractModel):
    """ModifyImageAttribute请求参数结构体"""

    def __init__(self):
        """
        :param ImageId: 镜像ID，形如`img-gvbnzy6f`。镜像ID可以通过如下方式获取：<br><li>通过DescribeImages接口返回的`ImageId`获取。<br><li>通过镜像控制台获取。
        :type ImageId: str
        :param ImageName: 设置新的镜像名称；必须满足下列限制：<br> <li> 不得超过20个字符。<br> <li> 镜像名称不能与已有镜像重复。
        :type ImageName: str
        :param ImageDescription: 设置新的镜像描述；必须满足下列限制：<br> <li> 不得超过60个字符。
        :type ImageDescription: str
        """
        self.ImageId = None
        self.ImageName = None
        self.ImageDescription = None

    def _deserialize(self, params):
        self.ImageId = params.get("ImageId")
        self.ImageName = params.get("ImageName")
        self.ImageDescription = params.get("ImageDescription")


class ModifyImageAttributeResponse(AbstractModel):
    """ModifyImageAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyImageSharePermissionRequest(AbstractModel):
    """ModifyImageSharePermission请求参数结构体"""

    def __init__(self):
        """
        :param ImageId: 镜像ID，形如`img-gvbnzy6f`。镜像Id可以通过如下方式获取：<br><li>通过DescribeImages接口返回的`ImageId`获取。<br><li>通过镜像控制台获取。 <br>镜像ID必须指定为状态为`NORMAL`的镜像。镜像状态请参考镜像数据表。
        :type ImageId: str
        :param AccountIds: 接收分享镜像的账号Id列表，array型参数的格式可以参考API简介。帐号ID不同于QQ号，查询用户帐号ID请查看帐号信息中的帐号ID栏。
        :type AccountIds: list of str
        :param Permission: 操作，包括 `SHARE`，`CANCEL`。其中`SHARE`代表分享操作，`CANCEL`代表取消分享操作。
        :type Permission: str
        """
        self.ImageId = None
        self.AccountIds = None
        self.Permission = None

    def _deserialize(self, params):
        self.ImageId = params.get("ImageId")
        self.AccountIds = params.get("AccountIds")
        self.Permission = params.get("Permission")


class ModifyImageSharePermissionResponse(AbstractModel):
    """ModifyImageSharePermission返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyInstanceInternetChargeTypeRequest(AbstractModel):
    """ModifyInstanceInternetChargeType请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 1
        :type InstanceId: str
        :param InternetAccessible: 1
        :type InternetAccessible: :class:`tcecloud.cvm.v20170312.models.InternetAccessibleModifyChargeType`
        :param DryRun: 1
        :type DryRun: bool
        """
        self.InstanceId = None
        self.InternetAccessible = None
        self.DryRun = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("InternetAccessible") is not None:
            self.InternetAccessible = InternetAccessibleModifyChargeType()
            self.InternetAccessible._deserialize(params.get("InternetAccessible"))
        self.DryRun = params.get("DryRun")


class ModifyInstanceInternetChargeTypeResponse(AbstractModel):
    """ModifyInstanceInternetChargeType返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyInstancesActionTimerRequest(AbstractModel):
    """ModifyInstancesActionTimer请求参数结构体"""

    def __init__(self):
        """
        :param ActionTimer: 指定具体的定时器信息
        :type ActionTimer: :class:`tcecloud.cvm.v20170312.models.ActionTimer`
        :param ActionTimerIds: 定时器id列表，可以通过DescribeInstancesActionTimer接口查询。
        :type ActionTimerIds: list of str
        """
        self.ActionTimer = None
        self.ActionTimerIds = None

    def _deserialize(self, params):
        if params.get("ActionTimer") is not None:
            self.ActionTimer = ActionTimer()
            self.ActionTimer._deserialize(params.get("ActionTimer"))
        self.ActionTimerIds = params.get("ActionTimerIds")


class ModifyInstancesActionTimerResponse(AbstractModel):
    """ModifyInstancesActionTimer返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyInstancesAttributeRequest(AbstractModel):
    """ModifyInstancesAttribute请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 一个或多个待操作的实例ID。可通过`DescribeInstances` API返回值中的`InstanceId`获取。每次请求允许操作的实例数量上限是100。
        :type InstanceIds: list of str
        :param InstanceName: 实例显示名称。可任意命名，但不得超过60个字符。
        :type InstanceName: str
        :param UserData: 内部参数，用户数据。
        :type UserData: str
        :param SecurityGroups: 内部参数，安全组Id列表。
        :type SecurityGroups: list of str
        :param ResetNewCreationIdentify: 内部参数，未知。
        :type ResetNewCreationIdentify: bool
        """
        self.InstanceIds = None
        self.InstanceName = None
        self.UserData = None
        self.SecurityGroups = None
        self.ResetNewCreationIdentify = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.InstanceName = params.get("InstanceName")
        self.UserData = params.get("UserData")
        self.SecurityGroups = params.get("SecurityGroups")
        self.ResetNewCreationIdentify = params.get("ResetNewCreationIdentify")


class ModifyInstancesAttributeResponse(AbstractModel):
    """ModifyInstancesAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyInstancesChargeTypeRequest(AbstractModel):
    """ModifyInstancesChargeType请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 1
        :type InstanceIds: list of str
        :param InstanceChargeType: 1
        :type InstanceChargeType: str
        :param InstanceChargePrepaid: 1
        :type InstanceChargePrepaid: :class:`tcecloud.cvm.v20170312.models.InstanceChargePrepaid`
        :param DryRun: 1
        :type DryRun: bool
        :param ModifyPortableDataDisk: 1
        :type ModifyPortableDataDisk: bool
        """
        self.InstanceIds = None
        self.InstanceChargeType = None
        self.InstanceChargePrepaid = None
        self.DryRun = None
        self.ModifyPortableDataDisk = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.InstanceChargeType = params.get("InstanceChargeType")
        if params.get("InstanceChargePrepaid") is not None:
            self.InstanceChargePrepaid = InstanceChargePrepaid()
            self.InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))
        self.DryRun = params.get("DryRun")
        self.ModifyPortableDataDisk = params.get("ModifyPortableDataDisk")


class ModifyInstancesChargeTypeResponse(AbstractModel):
    """ModifyInstancesChargeType返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyInstancesProjectRequest(AbstractModel):
    """ModifyInstancesProject请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 一个或多个待操作的实例ID。可通过`DescribeInstances` API返回值中的`InstanceId`获取。每次请求允许操作的实例数量上限是100。
        :type InstanceIds: list of str
        :param ProjectId: 项目ID。项目可以使用AddProject接口创建。后续使用DescribeInstances接口查询实例时，项目ID可用于过滤结果。
        :type ProjectId: int
        """
        self.InstanceIds = None
        self.ProjectId = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.ProjectId = params.get("ProjectId")


class ModifyInstancesProjectResponse(AbstractModel):
    """ModifyInstancesProject返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyInstancesRenewFlagRequest(AbstractModel):
    """ModifyInstancesRenewFlag请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 一个或多个待操作的实例ID。可通过`DescribeInstances` API返回值中的`InstanceId`获取。每次请求允许操作的实例数量上限是100。
        :type InstanceIds: list of str
        :param RenewFlag: 自动续费标识。取值范围：<br><li>NOTIFY_AND_AUTO_RENEW：通知过期且自动续费<br><li>NOTIFY_AND_MANUAL_RENEW：通知过期不自动续费<br><li>DISABLE_NOTIFY_AND_MANUAL_RENEW：不通知过期不自动续费<br><br>若该参数指定为NOTIFY_AND_AUTO_RENEW，在账户余额充足的情况下，实例到期后将按月自动续费。
        :type RenewFlag: str
        """
        self.InstanceIds = None
        self.RenewFlag = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.RenewFlag = params.get("RenewFlag")


class ModifyInstancesRenewFlagResponse(AbstractModel):
    """ModifyInstancesRenewFlag返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyInstancesVpcAttributeRequest(AbstractModel):
    """ModifyInstancesVpcAttribute请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 待操作的实例ID数组。可通过`DescribeInstances`接口返回值中的`InstanceId`获取。
        :type InstanceIds: list of str
        :param VirtualPrivateCloud: 私有网络相关信息配置，通过该参数指定私有网络的ID，子网ID，私有网络ip等信息。<br><li>当指定私有网络ID和子网ID（子网必须在实例所在的可用区）与指定实例所在私有网络不一致时，会将实例迁移至指定的私有网络的子网下。<br><li>可通过`PrivateIpAddresses`指定私有网络子网IP，若需指定则所有已指定的实例均需要指定子网IP，此时`InstanceIds`与`PrivateIpAddresses`一一对应。<br><li>不指定`PrivateIpAddresses`时随机分配私有网络子网IP。
        :type VirtualPrivateCloud: :class:`tcecloud.cvm.v20170312.models.VirtualPrivateCloud`
        :param ForceStop: 是否对运行中的实例选择强制关机。默认为TRUE。
        :type ForceStop: bool
        :param ReserveHostName: 是否保留主机名。默认为FALSE。
        :type ReserveHostName: bool
        """
        self.InstanceIds = None
        self.VirtualPrivateCloud = None
        self.ForceStop = None
        self.ReserveHostName = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        if params.get("VirtualPrivateCloud") is not None:
            self.VirtualPrivateCloud = VirtualPrivateCloud()
            self.VirtualPrivateCloud._deserialize(params.get("VirtualPrivateCloud"))
        self.ForceStop = params.get("ForceStop")
        self.ReserveHostName = params.get("ReserveHostName")


class ModifyInstancesVpcAttributeResponse(AbstractModel):
    """ModifyInstancesVpcAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyKeyPairAttributeRequest(AbstractModel):
    """ModifyKeyPairAttribute请求参数结构体"""

    def __init__(self):
        """
        :param KeyId: 密钥对ID，密钥对ID形如：`skey-11112222`。<br><br>可以通过以下方式获取可用的密钥 ID：<br><li>通过登录控制台查询密钥 ID。<br><li>通过调用接口 DescribeKeyPairs ，取返回信息中的 `KeyId` 获取密钥对 ID。
        :type KeyId: str
        :param KeyName: 修改后的密钥对名称，可由数字，字母和下划线组成，长度不超过25个字符。
        :type KeyName: str
        :param Description: 修改后的密钥对描述信息。可任意命名，但不得超过60个字符。
        :type Description: str
        """
        self.KeyId = None
        self.KeyName = None
        self.Description = None

    def _deserialize(self, params):
        self.KeyId = params.get("KeyId")
        self.KeyName = params.get("KeyName")
        self.Description = params.get("Description")


class ModifyKeyPairAttributeResponse(AbstractModel):
    """ModifyKeyPairAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyUserGlobalConfigsRequest(AbstractModel):
    """ModifyUserGlobalConfigs请求参数结构体"""

    def __init__(self):
        """
        :param Configs: 用户全局配置列表，目前配置仅支持StoppedMode一个key值，表示用户默认关机不收费配置，KEEP_CHARGING为关机收费，STOP_CHARGING为关机不收费，默认为KEEP_CHARGING。
        :type Configs: list of KvType
        """
        self.Configs = None

    def _deserialize(self, params):
        if params.get("Configs") is not None:
            self.Configs = []
            for item in params.get("Configs"):
                obj = KvType()
                obj._deserialize(item)
                self.Configs.append(obj)


class ModifyUserGlobalConfigsResponse(AbstractModel):
    """ModifyUserGlobalConfigs返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class Placement(AbstractModel):
    """描述了实例的抽象位置，包括其所在的可用区，所属的项目，宿主机等（仅CDH产品可用）"""

    def __init__(self):
        """
        :param Zone: 实例所属的可用区ID。该参数也可以通过调用  DescribeZones 的返回值中的Zone字段来获取。
        :type Zone: str
        :param ProjectId: 实例所属项目ID。该参数可以通过调用 DescribeProject 的返回值中的 projectId 字段来获取。不填为默认项目。
        :type ProjectId: int
        :param HostIds: 实例所属的专用宿主机ID列表。如果您有购买专用宿主机并且指定了该参数，则您购买的实例就会随机的部署在这些专用宿主机上。当前暂不支持。
        :type HostIds: list of str
        """
        self.Zone = None
        self.ProjectId = None
        self.HostIds = None

    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.ProjectId = params.get("ProjectId")
        self.HostIds = params.get("HostIds")


class Price(AbstractModel):
    """价格"""

    def __init__(self):
        """
        :param InstancePrice: 描述了实例价格。
        :type InstancePrice: :class:`tcecloud.cvm.v20170312.models.ItemPrice`
        :param BandwidthPrice: 描述了网络价格。
        :type BandwidthPrice: :class:`tcecloud.cvm.v20170312.models.ItemPrice`
        """
        self.InstancePrice = None
        self.BandwidthPrice = None

    def _deserialize(self, params):
        if params.get("InstancePrice") is not None:
            self.InstancePrice = ItemPrice()
            self.InstancePrice._deserialize(params.get("InstancePrice"))
        if params.get("BandwidthPrice") is not None:
            self.BandwidthPrice = ItemPrice()
            self.BandwidthPrice._deserialize(params.get("BandwidthPrice"))


class ProductInfoItem(AbstractModel):
    """产品描述信息项"""

    def __init__(self):
        """
        :param name: 信息项名称
        :type name: str
        :param value: 信息项对应的值
        :type value: str
        """
        self.name = None
        self.value = None

    def _deserialize(self, params):
        self.name = params.get("name")
        self.value = params.get("value")


class QueryDataDisk(AbstractModel):
    """数据盘"""

    def __init__(self):
        """
        :param DiskSize: 数据盘大小
        :type DiskSize: int
        :param DiskType: 系统盘类型：LOCAL_BASIC、CLOUD_BASIC、LOCAL_SSD、CLOUD_SSD、CLOUD_PREMIUM、CLOUD_ENHANCEDSSD
        :type DiskType: str
        """
        self.DiskSize = None
        self.DiskType = None

    def _deserialize(self, params):
        self.DiskSize = params.get("DiskSize")
        self.DiskType = params.get("DiskType")


class QueryDisasterRecoverGroupRequest(AbstractModel):
    """QueryDisasterRecoverGroup请求参数结构体"""

    def __init__(self):
        """
        :param DisasterRecoverGroupIds: 1
        :type DisasterRecoverGroupIds: list of str
        """
        self.DisasterRecoverGroupIds = None

    def _deserialize(self, params):
        self.DisasterRecoverGroupIds = params.get("DisasterRecoverGroupIds")


class QueryDisasterRecoverGroupResponse(AbstractModel):
    """QueryDisasterRecoverGroup返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class QueryFlowLogsRequest(AbstractModel):
    """QueryFlowLogs请求参数结构体"""

    def __init__(self):
        """
        :param StartTime: 查询日志范围的起始时间；例：2019-07-05 00:00:00
        :type StartTime: str
        :param EndTime: 查询日志范围的截止时间；例：2019-07-05 23:59:59
        :type EndTime: str
        :param Filters: 过滤条件，详见下表：实例过滤条件表。每次请求的`Filters`的上限为10，`Filter.Values`的上限为5。参数不支持同时指定`InstanceIds`和`Filters`。
        :type Filters: list of Filter
        :param Offset: 偏移量，默认为0。关于`Offset`的更进一步介绍请参考 API 简介中的相关小节。
        :type Offset: int
        :param Limit: 返回数量，默认为20，最大值为100。关于`Limit`的更进一步介绍请参考 API 简介中的相关小节。
        :type Limit: int
        """
        self.StartTime = None
        self.EndTime = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class QueryFlowLogsResponse(AbstractModel):
    """QueryFlowLogs返回参数结构体"""

    def __init__(self):
        """
        :param FlowLogSet: 日志流水信息。
        :type FlowLogSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FlowLogSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.FlowLogSet = params.get("FlowLogSet")
        self.RequestId = params.get("RequestId")


class QueryHostsRequest(AbstractModel):
    """QueryHosts请求参数结构体"""


class QueryHostsResponse(AbstractModel):
    """QueryHosts返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 租户端云服务器实例总数
        :type TotalCount: int
        :param Hosts: 租户端云服务器主机列表
        :type Hosts: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.Hosts = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        self.Hosts = params.get("Hosts")
        self.RequestId = params.get("RequestId")


class QueryInstance(AbstractModel):
    """查询接口Instance列表"""

    def __init__(self):
        """
                :param Placement: Placement结构
                :type Placement: :class:`tcecloud.cvm.v20170312.models.QueryPlacement`
                :param Memory: 内存大小
                :type Memory: int
                :param CPU: cpu核数
                :type CPU: int
                :param CreatedTime: 创建时间
                :type CreatedTime: str
                :param InstanceId: 实例ID
                :type InstanceId: str
                :param AppId: 实例拥有者AppId
                :type AppId: int
                :param InstanceName: 实例Id
                :type InstanceName: str
                :param Uuid: 实例Uuid
                :type Uuid: str
                :param PrivateIp: 内网Ip
                :type PrivateIp: str
                :param PublicIp: 公网Ip
        注意：此字段可能返回 null，表示取不到有效值。
                :type PublicIp: str
                :param HostIp: 所在宿主机ip
                :type HostIp: str
                :param IPv6Addresses: Ipv6地址
                :type IPv6Addresses: list of str
                :param InstanceStatus: 当前状态
                :type InstanceStatus: str
                :param InstanceState: 当前状态
                :type InstanceState: str
                :param Uin: 所有者ownerUin
                :type Uin: str
                :param InstanceType: 子机机型规格
                :type InstanceType: str
                :param InstanceFamily: 子机机型类型
                :type InstanceFamily: str
                :param NodeQuota: Quota使用情况
                :type NodeQuota: list of int
                :param SystemDisk: 系统盘详情
                :type SystemDisk: :class:`tcecloud.cvm.v20170312.models.QuerySystemDisk`
                :param DataDisks: 数据盘详情
                :type DataDisks: list of QueryDataDisk
        """
        self.Placement = None
        self.Memory = None
        self.CPU = None
        self.CreatedTime = None
        self.InstanceId = None
        self.AppId = None
        self.InstanceName = None
        self.Uuid = None
        self.PrivateIp = None
        self.PublicIp = None
        self.HostIp = None
        self.IPv6Addresses = None
        self.InstanceStatus = None
        self.InstanceState = None
        self.Uin = None
        self.InstanceType = None
        self.InstanceFamily = None
        self.NodeQuota = None
        self.SystemDisk = None
        self.DataDisks = None

    def _deserialize(self, params):
        if params.get("Placement") is not None:
            self.Placement = QueryPlacement()
            self.Placement._deserialize(params.get("Placement"))
        self.Memory = params.get("Memory")
        self.CPU = params.get("CPU")
        self.CreatedTime = params.get("CreatedTime")
        self.InstanceId = params.get("InstanceId")
        self.AppId = params.get("AppId")
        self.InstanceName = params.get("InstanceName")
        self.Uuid = params.get("Uuid")
        self.PrivateIp = params.get("PrivateIp")
        self.PublicIp = params.get("PublicIp")
        self.HostIp = params.get("HostIp")
        self.IPv6Addresses = params.get("IPv6Addresses")
        self.InstanceStatus = params.get("InstanceStatus")
        self.InstanceState = params.get("InstanceState")
        self.Uin = params.get("Uin")
        self.InstanceType = params.get("InstanceType")
        self.InstanceFamily = params.get("InstanceFamily")
        self.NodeQuota = params.get("NodeQuota")
        if params.get("SystemDisk") is not None:
            self.SystemDisk = QuerySystemDisk()
            self.SystemDisk._deserialize(params.get("SystemDisk"))
        if params.get("DataDisks") is not None:
            self.DataDisks = []
            for item in params.get("DataDisks"):
                obj = QueryDataDisk()
                obj._deserialize(item)
                self.DataDisks.append(obj)


class QueryInstancesActionTimerRequest(AbstractModel):
    """QueryInstancesActionTimer请求参数结构体"""

    def __init__(self):
        """
        :param ActionTimerIds: 1
        :type ActionTimerIds: list of str
        :param InstanceIds: 1
        :type InstanceIds: list of str
        :param TimerAction: 1
        :type TimerAction: str
        :param EndActionTime: 1
        :type EndActionTime: str
        :param StartActionTime: 1
        :type StartActionTime: str
        :param StatusList: 1
        :type StatusList: list of str
        """
        self.ActionTimerIds = None
        self.InstanceIds = None
        self.TimerAction = None
        self.EndActionTime = None
        self.StartActionTime = None
        self.StatusList = None

    def _deserialize(self, params):
        self.ActionTimerIds = params.get("ActionTimerIds")
        self.InstanceIds = params.get("InstanceIds")
        self.TimerAction = params.get("TimerAction")
        self.EndActionTime = params.get("EndActionTime")
        self.StartActionTime = params.get("StartActionTime")
        self.StatusList = params.get("StatusList")


class QueryInstancesActionTimerResponse(AbstractModel):
    """QueryInstancesActionTimer返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class QueryInstancesRequest(AbstractModel):
    """QueryInstances请求参数结构体"""

    def __init__(self):
        """
                :param Offset: 查询开始位置
                :type Offset: int
                :param Limit: 查询个数
                :type Limit: int
                :param Filters: 可填列表:
        uuid：实例uuid过滤
        private-ip：实例内网ip
        vpc-id：实例vpc-id
        public-ip：实例公网ip
        appid：实例appId
        zone：实例zoneId
        instance-id：实例id,
        host-ip：实例所在宿主机ip
        ipv6-address：实例ipv6地址
        instance-status：实例状态
                :type Filters: list of Filter
        """
        self.Offset = None
        self.Limit = None
        self.Filters = None

    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)


class QueryInstancesResponse(AbstractModel):
    """QueryInstances返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 租户端云服务器实例总数
        :type TotalCount: int
        :param Instances: 租户端云服务器实例列表
        :type Instances: list of QueryInstance
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.Instances = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Instances") is not None:
            self.Instances = []
            for item in params.get("Instances"):
                obj = QueryInstance()
                obj._deserialize(item)
                self.Instances.append(obj)
        self.RequestId = params.get("RequestId")


class QueryMigrateTaskRequest(AbstractModel):
    """QueryMigrateTask请求参数结构体"""

    def __init__(self):
        """
        :param TaskId: 任务Id
        :type TaskId: str
        """
        self.TaskId = None

    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")


class QueryMigrateTaskResponse(AbstractModel):
    """QueryMigrateTask返回参数结构体"""

    def __init__(self):
        """
        :param Status: 任务状态
        :type Status: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Status = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class QueryPlacement(AbstractModel):
    """查询的地址"""

    def __init__(self):
        """
        :param Zone: 可用区名称
        :type Zone: int
        :param VpcId: VpcId
        :type VpcId: int
        :param SubnetId: 子网Id
        :type SubnetId: int
        :param SubnetName: 子网名称
        :type SubnetName: str
        :param VpcName: Vpc名称
        :type VpcName: str
        """
        self.Zone = None
        self.VpcId = None
        self.SubnetId = None
        self.SubnetName = None
        self.VpcName = None

    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.SubnetName = params.get("SubnetName")
        self.VpcName = params.get("VpcName")


class QuerySystemDisk(AbstractModel):
    """查询的系统盘"""

    def __init__(self):
        """
        :param DiskSize: 系统盘大小
        :type DiskSize: int
        :param DiskType: 系统盘类型：LOCAL_BASIC、CLOUD_BASIC、LOCAL_SSD、CLOUD_SSD、CLOUD_PREMIUM、CLOUD_ENHANCEDSSD
        :type DiskType: str
        """
        self.DiskSize = None
        self.DiskType = None

    def _deserialize(self, params):
        self.DiskSize = params.get("DiskSize")
        self.DiskType = params.get("DiskType")


class Quota(AbstractModel):
    """描述了配额信息"""

    def __init__(self):
        """
        :param QuotaId: 配额名称，取值范围：<br><li>`TOTAL_EIP_QUOTA`：用户当前地域下EIP的配额数；<br><li>`DAILY_EIP_APPLY`：用户当前地域下今日申购次数；<br><li>`DAILY_PUBLIC_IP_ASSIGN`：用户当前地域下，重新分配公网 IP次数。
        :type QuotaId: str
        :param QuotaCurrent: 当前数量
        :type QuotaCurrent: int
        :param QuotaLimit: 配额数量
        :type QuotaLimit: int
        """
        self.QuotaId = None
        self.QuotaCurrent = None
        self.QuotaLimit = None

    def _deserialize(self, params):
        self.QuotaId = params.get("QuotaId")
        self.QuotaCurrent = params.get("QuotaCurrent")
        self.QuotaLimit = params.get("QuotaLimit")


class RebootInstancesRequest(AbstractModel):
    """RebootInstances请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 一个或多个待操作的实例ID。可通过`DescribeInstances`接口返回值中的`InstanceId`获取。每次请求批量实例的上限为100。
        :type InstanceIds: list of str
        :param ForceReboot: 是否在正常重启失败后选择强制重启实例。取值范围：<br><li>TRUE：表示在正常重启失败后进行强制重启<br><li>FALSE：表示在正常重启失败后不进行强制重启<br><br>默认取值：FALSE。
        :type ForceReboot: bool
        """
        self.InstanceIds = None
        self.ForceReboot = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.ForceReboot = params.get("ForceReboot")


class RebootInstancesResponse(AbstractModel):
    """RebootInstances返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class RefreshInternalUserEnvironmentRequest(AbstractModel):
    """RefreshInternalUserEnvironment请求参数结构体"""


class RefreshInternalUserEnvironmentResponse(AbstractModel):
    """RefreshInternalUserEnvironment返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class RegionInfo(AbstractModel):
    """地域信息"""

    def __init__(self):
        """
        :param Region: 地域名称，例如，ap-guangzhou
        :type Region: str
        :param RegionName: 地域描述，例如，华南地区(广州)
        :type RegionName: str
        :param RegionState: 地域是否可用状态
        :type RegionState: str
        """
        self.Region = None
        self.RegionName = None
        self.RegionState = None

    def _deserialize(self, params):
        self.Region = params.get("Region")
        self.RegionName = params.get("RegionName")
        self.RegionState = params.get("RegionState")


class ReleaseAddressesRequest(AbstractModel):
    """ReleaseAddresses请求参数结构体"""

    def __init__(self):
        """
        :param AddressIds: 1
        :type AddressIds: list of str
        """
        self.AddressIds = None

    def _deserialize(self, params):
        self.AddressIds = params.get("AddressIds")


class ReleaseAddressesResponse(AbstractModel):
    """ReleaseAddresses返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class RenewAddressesRequest(AbstractModel):
    """RenewAddresses请求参数结构体"""

    def __init__(self):
        """
        :param AddressIds: 1
        :type AddressIds: list of str
        :param AddressChargePrepaid: 1
        :type AddressChargePrepaid: :class:`tcecloud.cvm.v20170312.models.AddressChargePrepaid`
        :param DealId: 1
        :type DealId: str
        :param CurrentDeadline: 1
        :type CurrentDeadline: str
        """
        self.AddressIds = None
        self.AddressChargePrepaid = None
        self.DealId = None
        self.CurrentDeadline = None

    def _deserialize(self, params):
        self.AddressIds = params.get("AddressIds")
        if params.get("AddressChargePrepaid") is not None:
            self.AddressChargePrepaid = AddressChargePrepaid()
            self.AddressChargePrepaid._deserialize(params.get("AddressChargePrepaid"))
        self.DealId = params.get("DealId")
        self.CurrentDeadline = params.get("CurrentDeadline")


class RenewAddressesResponse(AbstractModel):
    """RenewAddresses返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class RenewHostsRequest(AbstractModel):
    """RenewHosts请求参数结构体"""

    def __init__(self):
        """
        :param HostIds: 一个或多个待操作的CDH实例ID。
        :type HostIds: list of str
        :param HostChargePrepaid: 预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月实例的购买时长、是否设置自动续费等属性。若指定实例的付费模式为预付费则该参数必传。
        :type HostChargePrepaid: :class:`tcecloud.cvm.v20170312.models.ChargePrepaid`
        :param DryRun: 是否跳过实际执行逻辑。
        :type DryRun: bool
        """
        self.HostIds = None
        self.HostChargePrepaid = None
        self.DryRun = None

    def _deserialize(self, params):
        self.HostIds = params.get("HostIds")
        if params.get("HostChargePrepaid") is not None:
            self.HostChargePrepaid = ChargePrepaid()
            self.HostChargePrepaid._deserialize(params.get("HostChargePrepaid"))
        self.DryRun = params.get("DryRun")


class RenewHostsResponse(AbstractModel):
    """RenewHosts返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class RenewInstancesRequest(AbstractModel):
    """RenewInstances请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 一个或多个待操作的实例ID。可通过`DescribeInstances`接口返回值中的`InstanceId`获取。每次请求批量实例的上限为100。
        :type InstanceIds: list of str
        :param InstanceChargePrepaid: 预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月实例的续费时长、是否设置自动续费等属性。
        :type InstanceChargePrepaid: :class:`tcecloud.cvm.v20170312.models.InstanceChargePrepaid`
        :param InternetAccessible: 内部参数，公网带宽相关信息设置。
        :type InternetAccessible: list of InternetAccessible
        :param DryRun: 试运行。
        :type DryRun: bool
        :param RenewPortableDataDisk: 内部参数，续费弹性数据盘。
        :type RenewPortableDataDisk: bool
        """
        self.InstanceIds = None
        self.InstanceChargePrepaid = None
        self.InternetAccessible = None
        self.DryRun = None
        self.RenewPortableDataDisk = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        if params.get("InstanceChargePrepaid") is not None:
            self.InstanceChargePrepaid = InstanceChargePrepaid()
            self.InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))
        if params.get("InternetAccessible") is not None:
            self.InternetAccessible = []
            for item in params.get("InternetAccessible"):
                obj = InternetAccessible()
                obj._deserialize(item)
                self.InternetAccessible.append(obj)
        self.DryRun = params.get("DryRun")
        self.RenewPortableDataDisk = params.get("RenewPortableDataDisk")


class RenewInstancesResponse(AbstractModel):
    """RenewInstances返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ResetInstanceRequest(AbstractModel):
    """ResetInstance请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID。可通过 DescribeInstances API返回值中的`InstanceId`获取。
        :type InstanceId: str
        :param ImageId: 指定有效的镜像ID，格式形如`img-xxx`。镜像类型分为四种：<br/><li>公共镜像</li><li>自定义镜像</li><li>共享镜像</li><li>服务市场镜像</li><br/>可通过以下方式获取可用的镜像ID：<br/><li>`公共镜像`、`自定义镜像`、`共享镜像`的镜像ID可通过登录控制台查询；`服务镜像市场`的镜像ID可通过云市场查询。</li><li>通过调用接口 DescribeImages ，取返回信息中的`ImageId`字段。</li>
        :type ImageId: str
        :param SystemDisk: 实例系统盘配置信息。系统盘为云盘的实例可以通过该参数指定重装后的系统盘大小来实现对系统盘的扩容操作，若不指定则默认系统盘大小保持不变。系统盘大小只支持扩容不支持缩容；重装只支持修改系统盘的大小，不能修改系统盘的类型。
        :type SystemDisk: :class:`tcecloud.cvm.v20170312.models.SystemDisk`
        :param LoginSettings: 实例登录设置。通过该参数可以设置实例的登录方式密码、密钥或保持镜像的原始登录设置。默认情况下会随机生成密码，并以站内信方式知会到用户。
        :type LoginSettings: :class:`tcecloud.cvm.v20170312.models.LoginSettings`
        :param EnhancedService: 增强服务。通过该参数可以指定是否开启云安全、云监控等服务。若不指定该参数，则默认开启云监控、云安全服务。
        :type EnhancedService: :class:`tcecloud.cvm.v20170312.models.EnhancedService`
        """
        self.InstanceId = None
        self.ImageId = None
        self.SystemDisk = None
        self.LoginSettings = None
        self.EnhancedService = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.ImageId = params.get("ImageId")
        if params.get("SystemDisk") is not None:
            self.SystemDisk = SystemDisk()
            self.SystemDisk._deserialize(params.get("SystemDisk"))
        if params.get("LoginSettings") is not None:
            self.LoginSettings = LoginSettings()
            self.LoginSettings._deserialize(params.get("LoginSettings"))
        if params.get("EnhancedService") is not None:
            self.EnhancedService = EnhancedService()
            self.EnhancedService._deserialize(params.get("EnhancedService"))


class ResetInstanceResponse(AbstractModel):
    """ResetInstance返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ResetInstancesInternetMaxBandwidthRequest(AbstractModel):
    """ResetInstancesInternetMaxBandwidth请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 一个或多个待操作的实例ID。可通过`DescribeInstances`接口返回值中的 `InstanceId` 获取。 每次请求批量实例的上限为100。
        :type InstanceIds: list of str
        :param InternetAccessible: 公网出带宽配置。不同机型带宽上限范围不一致，具体限制详见带宽限制对账表。暂时只支持 `InternetMaxBandwidthOut` 参数。
        :type InternetAccessible: :class:`tcecloud.cvm.v20170312.models.InternetAccessible`
        :param StartTime: 带宽生效的起始时间。格式：`YYYY-MM-DD`，例如：`2016-10-30`。起始时间不能早于当前时间。如果起始时间是今天则新设置的带宽立即生效。该参数只对包年包月带宽有效，其他模式带宽不支持该参数，否则接口会以相应错误码返回。
        :type StartTime: str
        :param EndTime: 带宽生效的终止时间。格式： `YYYY-MM-DD` ，例如：`2016-10-30` 。新设置的带宽的有效期包含终止时间此日期。终止时间不能晚于包年包月实例的到期时间。实例的到期时间可通过 `DescribeInstances`接口返回值中的`ExpiredTime`获取。该参数只对包年包月带宽有效，其他模式带宽不支持该参数，否则接口会以相应错误码返回。
        :type EndTime: str
        """
        self.InstanceIds = None
        self.InternetAccessible = None
        self.StartTime = None
        self.EndTime = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        if params.get("InternetAccessible") is not None:
            self.InternetAccessible = InternetAccessible()
            self.InternetAccessible._deserialize(params.get("InternetAccessible"))
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")


class ResetInstancesInternetMaxBandwidthResponse(AbstractModel):
    """ResetInstancesInternetMaxBandwidth返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ResetInstancesPasswordRequest(AbstractModel):
    """ResetInstancesPassword请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 一个或多个待操作的实例ID。可通过`DescribeInstances` API返回值中的`InstanceId`获取。每次请求允许操作的实例数量上限是100。
        :type InstanceIds: list of str
        :param Password: 实例登录密码。不同操作系统类型密码复杂度限制不一样，具体如下：<br><li>`Linux`实例密码必须8到16位，至少包括两项`[a-z，A-Z]、[0-9]`和`[( ) ~ ~ ! @ # $ % ^ & * - + = _ | { } [ ] : ; ' < > , . ? /]`中的符号。密码不允许以`/`符号开头。<br><li>`Windows`实例密码必须12到16位，至少包括三项`[a-z]，[A-Z]，[0-9]`和`[( ) ~ ~ ! @ # $ % ^ & * - + = _ | { } [ ] : ; ' < > , . ? /]`中的符号。密码不允许以`/`符号开头。<br><li>如果实例即包含`Linux`实例又包含`Windows`实例，则密码复杂度限制按照`Windows`实例的限制。
        :type Password: str
        :param UserName: 待重置密码的实例操作系统用户名。不得超过64个字符。
        :type UserName: str
        :param ForceStop: 是否对运行中的实例选择强制关机。建议对运行中的实例先手动关机，然后再重置用户密码。取值范围：<br><li>TRUE：表示在正常关机失败后进行强制关机<br><li>FALSE：表示在正常关机失败后不进行强制关机<br><br>默认取值：FALSE。<br><br>强制关机的效果等同于关闭物理计算机的电源开关。强制关机可能会导致数据丢失或文件系统损坏，请仅在服务器不能正常关机时使用。
        :type ForceStop: bool
        """
        self.InstanceIds = None
        self.Password = None
        self.UserName = None
        self.ForceStop = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.Password = params.get("Password")
        self.UserName = params.get("UserName")
        self.ForceStop = params.get("ForceStop")


class ResetInstancesPasswordResponse(AbstractModel):
    """ResetInstancesPassword返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ResetInstancesTypeRequest(AbstractModel):
    """ResetInstancesType请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 一个或多个待操作的实例ID。可通过`DescribeInstances`接口返回值中的`InstanceId`获取。每次请求批量实例的上限为1。
        :type InstanceIds: list of str
        :param InstanceType: 实例机型。不同实例机型指定了不同的资源规格，具体取值可参见附表实例资源规格对照表，也可以调用查询实例资源规格列表接口获得最新的规格表。
        :type InstanceType: str
        :param ForceStop: 是否对运行中的实例选择强制关机。建议对运行中的实例先手动关机，然后再重置用户密码。取值范围：<br><li>TRUE：表示在正常关机失败后进行强制关机<br><li>FALSE：表示在正常关机失败后不进行强制关机<br><br>默认取值：FALSE。<br><br>强制关机的效果等同于关闭物理计算机的电源开关。强制关机可能会导致数据丢失或文件系统损坏，请仅在服务器不能正常关机时使用。
        :type ForceStop: bool
        """
        self.InstanceIds = None
        self.InstanceType = None
        self.ForceStop = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.InstanceType = params.get("InstanceType")
        self.ForceStop = params.get("ForceStop")


class ResetInstancesTypeResponse(AbstractModel):
    """ResetInstancesType返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ResizeInstanceDisksRequest(AbstractModel):
    """ResizeInstanceDisks请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 待操作的实例ID。可通过`DescribeInstances`接口返回值中的`InstanceId`获取。
        :type InstanceId: str
        :param DataDisks: 待扩容的数据盘配置信息。只支持扩容随实例购买的数据盘，且数据盘类型为：`CLOUD_BASIC`、`CLOUD_PREMIUM`、`CLOUD_SSD`。数据盘容量单位：GB。最小扩容步长：10G。关于数据盘类型的选择请参考硬盘产品简介。可选数据盘类型受到实例类型`InstanceType`限制。另外允许扩容的最大容量也因数据盘类型的不同而有所差异。
        :type DataDisks: list of DataDisk
        :param ForceStop: 是否对运行中的实例选择强制关机。建议对运行中的实例先手动关机，然后再重置用户密码。取值范围：<br><li>TRUE：表示在正常关机失败后进行强制关机<br><li>FALSE：表示在正常关机失败后不进行强制关机<br><br>默认取值：FALSE。<br><br>强制关机的效果等同于关闭物理计算机的电源开关。强制关机可能会导致数据丢失或文件系统损坏，请仅在服务器不能正常关机时使用。
        :type ForceStop: bool
        """
        self.InstanceId = None
        self.DataDisks = None
        self.ForceStop = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("DataDisks") is not None:
            self.DataDisks = []
            for item in params.get("DataDisks"):
                obj = DataDisk()
                obj._deserialize(item)
                self.DataDisks.append(obj)
        self.ForceStop = params.get("ForceStop")


class ResizeInstanceDisksResponse(AbstractModel):
    """ResizeInstanceDisks返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ResumeInstancesRequest(AbstractModel):
    """ResumeInstances请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 无
        :type InstanceIds: list of str
        """
        self.InstanceIds = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")


class ResumeInstancesResponse(AbstractModel):
    """ResumeInstances返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ReturnAddressesRequest(AbstractModel):
    """ReturnAddresses请求参数结构体"""

    def __init__(self):
        """
        :param AddressIds: 1
        :type AddressIds: list of str
        """
        self.AddressIds = None

    def _deserialize(self, params):
        self.AddressIds = params.get("AddressIds")


class ReturnAddressesResponse(AbstractModel):
    """ReturnAddresses返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ReturnNormalAddressesRequest(AbstractModel):
    """ReturnNormalAddresses请求参数结构体"""

    def __init__(self):
        """
        :param AddressIps: 1
        :type AddressIps: list of str
        """
        self.AddressIps = None

    def _deserialize(self, params):
        self.AddressIps = params.get("AddressIps")


class ReturnNormalAddressesResponse(AbstractModel):
    """ReturnNormalAddresses返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class RunInstancesRequest(AbstractModel):
    """RunInstances请求参数结构体"""

    def __init__(self):
        """
                :param Placement: 实例所在的位置。通过该参数可以指定实例所属可用区，所属项目，专用宿主机（对于独享母机付费模式的子机创建）等属性。
                :type Placement: :class:`tcecloud.cvm.v20170312.models.Placement`
                :param ImageId: 指定有效的镜像ID，格式形如`img-xxx`。镜像类型分为四种：<br/><li>公共镜像</li><li>自定义镜像</li><li>共享镜像</li><li>服务市场镜像</li><br/>可通过以下方式获取可用的镜像ID：<br/><li>`公共镜像`、`自定义镜像`、`共享镜像`的镜像ID可通过登录控制台查询；`服务镜像市场`的镜像ID可通过云市场查询。</li><li>通过调用接口 DescribeImages ，取返回信息中的`ImageId`字段。</li>
                :type ImageId: str
                :param InstanceChargeType: 实例计费类型。<br><li>PREPAID：预付费，即包年包月<br><li>POSTPAID_BY_HOUR：按小时后付费<br><li>CDHPAID：独享母机付费（基于专用宿主机创建，宿主机部分的资源不收费）<br>默认值：POSTPAID_BY_HOUR。
                :type InstanceChargeType: str
                :param InstanceChargePrepaid: 预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月实例的购买时长、是否设置自动续费等属性。若指定实例的付费模式为预付费则该参数必传。
                :type InstanceChargePrepaid: :class:`tcecloud.cvm.v20170312.models.InstanceChargePrepaid`
                :param InstanceType: 实例机型。不同实例机型指定了不同的资源规格。
        <br><li>对于付费模式为PREPAID或POSTPAID_BY_HOUR的子机创建，具体取值可通过调用接口DescribeInstanceTypeConfigs来获得最新的规格表或参见实例类型描述。若不指定该参数，则默认机型为S1.SMALL1。<br><li>对于付费模式为CDHPAID的子机创建，该参数以"CDH_"为前缀，根据cpu和内存配置生成，具体形式为：CDH_XCXG，例如对于创建cpu为1核，内存为1G大小的专用宿主机的子机，该参数应该为CDH_1C1G。
                :type InstanceType: str
                :param SystemDisk: 实例系统盘配置信息。若不指定该参数，则按照系统默认值进行分配。
                :type SystemDisk: :class:`tcecloud.cvm.v20170312.models.SystemDisk`
                :param DataDisks: 实例数据盘配置信息。若不指定该参数，则默认不购买数据盘，当前仅支持购买的时候指定一个数据盘。
                :type DataDisks: list of DataDisk
                :param VirtualPrivateCloud: 私有网络相关信息配置。通过该参数可以指定私有网络的ID，子网ID等信息。若不指定该参数，则默认使用基础网络。若在此参数中指定了私有网络ip，那么InstanceCount参数只能为1。
                :type VirtualPrivateCloud: :class:`tcecloud.cvm.v20170312.models.VirtualPrivateCloud`
                :param InternetAccessible: 公网带宽相关信息设置。若不指定该参数，则默认公网带宽为0Mbps。
                :type InternetAccessible: :class:`tcecloud.cvm.v20170312.models.InternetAccessible`
                :param InstanceCount: 购买实例数量。取值范围：1，100]。默认取值：1。指定购买实例的数量不能超过用户所能购买的剩余配额数量，具体配额相关限制详见[CVM实例购买限制。
                :type InstanceCount: int
                :param InstanceName: 实例显示名称。如果不指定则默认显示
                :type InstanceName: str
                :param LoginSettings: 实例登录设置。通过该参数可以设置实例的登录方式密码、密钥或保持镜像的原始登录设置。默认情况下会随机生成密码，并以站内信方式知会到用户。
                :type LoginSettings: :class:`tcecloud.cvm.v20170312.models.LoginSettings`
                :param SecurityGroupIds: 实例所属安全组。该参数可以通过调用 DescribeSecurityGroups 的返回值中的sgId字段来获取。若不指定该参数，则默认不绑定安全组。
                :type SecurityGroupIds: list of str
                :param EnhancedService: 增强服务。通过该参数可以指定是否开启云安全、云监控等服务。若不指定该参数，则默认开启云监控、云安全服务。
                :type EnhancedService: :class:`tcecloud.cvm.v20170312.models.EnhancedService`
                :param ClientToken: 用于保证请求幂等性的字符串。该字符串由客户生成，需保证不同请求之间唯一，最大值不超过64个ASCII字符。若不指定该参数，则无法保证请求的幂等性。<br>更多详细信息请参阅：如何保证幂等性。
                :type ClientToken: str
                :param SpotPrice: 用于指定价格生产，当前主要用于竞价实例
                :type SpotPrice: str
                :param HostName: 云服务器的主机名。<br><li>点号（.）和短横线（-）不能作为 HostName 的首尾字符，不能连续使用。<br><li>Windows 实例：名字符长度为[2, 15]，允许字母（不限制大小写）、数字和短横线（-）组成，不支持点号（.），不能全是数字。<br><li>其他类型（Linux 等）实例：字符长度为[2, 30]，允许支持多个点号，点之间为一段，每段允许字母（不限制大小写）、数字和短横线（-）组成。
                :type HostName: str
                :param UserData: 提供给实例使用的用户数据，需要以 base64 方式编码，支持的最大数据大小为 16KB。关于获取此参数的详细介绍，请参阅Windows和Linux启动时运行命令。
                :type UserData: str
                :param DisasterRecoverGroupIds: 置放群组id，仅支持指定一个。
                :type DisasterRecoverGroupIds: list of str
                :param TagSpecification: 标签描述列表。通过指定该参数可以同时绑定标签到相应的资源实例，当前仅支持绑定标签到云服务器实例。
                :type TagSpecification: list of TagSpecification
        """
        self.Placement = None
        self.ImageId = None
        self.InstanceChargeType = None
        self.InstanceChargePrepaid = None
        self.InstanceType = None
        self.SystemDisk = None
        self.DataDisks = None
        self.VirtualPrivateCloud = None
        self.InternetAccessible = None
        self.InstanceCount = None
        self.InstanceName = None
        self.LoginSettings = None
        self.SecurityGroupIds = None
        self.EnhancedService = None
        self.ClientToken = None
        self.SpotPrice = None
        self.HostName = None
        self.UserData = None
        self.DisasterRecoverGroupIds = None
        self.TagSpecification = None

    def _deserialize(self, params):
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        self.ImageId = params.get("ImageId")
        self.InstanceChargeType = params.get("InstanceChargeType")
        if params.get("InstanceChargePrepaid") is not None:
            self.InstanceChargePrepaid = InstanceChargePrepaid()
            self.InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))
        self.InstanceType = params.get("InstanceType")
        if params.get("SystemDisk") is not None:
            self.SystemDisk = SystemDisk()
            self.SystemDisk._deserialize(params.get("SystemDisk"))
        if params.get("DataDisks") is not None:
            self.DataDisks = []
            for item in params.get("DataDisks"):
                obj = DataDisk()
                obj._deserialize(item)
                self.DataDisks.append(obj)
        if params.get("VirtualPrivateCloud") is not None:
            self.VirtualPrivateCloud = VirtualPrivateCloud()
            self.VirtualPrivateCloud._deserialize(params.get("VirtualPrivateCloud"))
        if params.get("InternetAccessible") is not None:
            self.InternetAccessible = InternetAccessible()
            self.InternetAccessible._deserialize(params.get("InternetAccessible"))
        self.InstanceCount = params.get("InstanceCount")
        self.InstanceName = params.get("InstanceName")
        if params.get("LoginSettings") is not None:
            self.LoginSettings = LoginSettings()
            self.LoginSettings._deserialize(params.get("LoginSettings"))
        self.SecurityGroupIds = params.get("SecurityGroupIds")
        if params.get("EnhancedService") is not None:
            self.EnhancedService = EnhancedService()
            self.EnhancedService._deserialize(params.get("EnhancedService"))
        self.ClientToken = params.get("ClientToken")
        self.SpotPrice = params.get("SpotPrice")
        self.HostName = params.get("HostName")
        self.UserData = params.get("UserData")
        self.DisasterRecoverGroupIds = params.get("DisasterRecoverGroupIds")
        if params.get("TagSpecification") is not None:
            self.TagSpecification = []
            for item in params.get("TagSpecification"):
                obj = TagSpecification()
                obj._deserialize(item)
                self.TagSpecification.append(obj)


class RunInstancesResponse(AbstractModel):
    """RunInstances返回参数结构体"""

    def __init__(self):
        """
        :param InstanceIdSet: 当通过本接口来创建实例时会返回该参数，表示一个或多个实例`ID`。返回实例`ID`列表并不代表实例创建成功，可根据 DescribeInstancesStatus 接口查询返回的InstancesSet中对应实例的`ID`的状态来判断创建是否完成；如果实例状态由“准备中”变为“正在运行”，则为创建成功。
        :type InstanceIdSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceIdSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.InstanceIdSet = params.get("InstanceIdSet")
        self.RequestId = params.get("RequestId")


class RunMonitorServiceEnabled(AbstractModel):
    """描述了 “云监控” 服务相关的信息"""

    def __init__(self):
        """
        :param Enabled: 是否开启云监控服务。取值范围：<br><li>TRUE：表示开启云监控服务<br><li>FALSE：表示不开启云监控服务<br><br>默认取值：TRUE。
        :type Enabled: bool
        """
        self.Enabled = None

    def _deserialize(self, params):
        self.Enabled = params.get("Enabled")


class RunSecurityServiceEnabled(AbstractModel):
    """描述了 “云安全” 服务相关的信息"""

    def __init__(self):
        """
        :param Enabled: 是否开启云安全服务。取值范围：<br><li>TRUE：表示开启云安全服务<br><li>FALSE：表示不开启云安全服务<br><br>默认取值：TRUE。
        :type Enabled: bool
        """
        self.Enabled = None

    def _deserialize(self, params):
        self.Enabled = params.get("Enabled")


class SearchUserInstanceRequest(AbstractModel):
    """SearchUserInstance请求参数结构体"""

    def __init__(self):
        """
        :param Keyword: 1
        :type Keyword: str
        :param Offset: 1
        :type Offset: int
        :param Limit: 1
        :type Limit: int
        """
        self.Keyword = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.Keyword = params.get("Keyword")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class SearchUserInstanceResponse(AbstractModel):
    """SearchUserInstance返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class SharePermission(AbstractModel):
    """镜像分享信息结构"""

    def __init__(self):
        """
        :param CreateTime: 镜像分享时间
        :type CreateTime: str
        :param Account: 镜像分享的账户ID
        :type Account: str
        """
        self.CreateTime = None
        self.Account = None

    def _deserialize(self, params):
        self.CreateTime = params.get("CreateTime")
        self.Account = params.get("Account")


class StartInstancesRequest(AbstractModel):
    """StartInstances请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 一个或多个待操作的实例ID。可通过`DescribeInstances`接口返回值中的`InstanceId`获取。每次请求批量实例的上限为100。
        :type InstanceIds: list of str
        """
        self.InstanceIds = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")


class StartInstancesResponse(AbstractModel):
    """StartInstances返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class StopInstancesRequest(AbstractModel):
    """StopInstances请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 一个或多个待操作的实例ID。可通过`DescribeInstances`接口返回值中的`InstanceId`获取。每次请求批量实例的上限为100。
        :type InstanceIds: list of str
        :param ForceStop: 是否在正常关闭失败后选择强制关闭实例。取值范围：<br><li>TRUE：表示在正常关闭失败后进行强制关闭<br><li>FALSE：表示在正常关闭失败后不进行强制关闭<br><br>默认取值：FALSE。
        :type ForceStop: bool
        """
        self.InstanceIds = None
        self.ForceStop = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.ForceStop = params.get("ForceStop")


class StopInstancesResponse(AbstractModel):
    """StopInstances返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class SuspendInstancesRequest(AbstractModel):
    """SuspendInstances请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 无
        :type InstanceIds: list of str
        :param OperationType: 无
        :type OperationType: str
        """
        self.InstanceIds = None
        self.OperationType = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.OperationType = params.get("OperationType")


class SuspendInstancesResponse(AbstractModel):
    """SuspendInstances返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class SwitchParameterAllocateHostsRequest(AbstractModel):
    """SwitchParameterAllocateHosts请求参数结构体"""

    def __init__(self):
        """
        :param Placement: 实例所在的位置。通过该参数可以指定实例所属可用区，所属项目等属性。
        :type Placement: :class:`tcecloud.cvm.v20170312.models.Placement`
        :param ClientToken: 用于保证请求幂等性的字符串。
        :type ClientToken: str
        :param HostChargePrepaid: 预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月实例的购买时长、是否设置自动续费等属性。若指定实例的付费模式为预付费则该参数必传。
        :type HostChargePrepaid: :class:`tcecloud.cvm.v20170312.models.ChargePrepaid`
        :param HostChargeType: 实例计费类型。目前仅支持：PREPAID（预付费，即包年包月模式）。
        :type HostChargeType: str
        :param HostType: CDH实例机型。
        :type HostType: str
        :param HostCount: 购买CDH实例数量。
        :type HostCount: int
        :param DryRun: 是否跳过实际执行逻辑
        :type DryRun: bool
        :param PurchaseSource: 购买来源
        :type PurchaseSource: str
        """
        self.Placement = None
        self.ClientToken = None
        self.HostChargePrepaid = None
        self.HostChargeType = None
        self.HostType = None
        self.HostCount = None
        self.DryRun = None
        self.PurchaseSource = None

    def _deserialize(self, params):
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        self.ClientToken = params.get("ClientToken")
        if params.get("HostChargePrepaid") is not None:
            self.HostChargePrepaid = ChargePrepaid()
            self.HostChargePrepaid._deserialize(params.get("HostChargePrepaid"))
        self.HostChargeType = params.get("HostChargeType")
        self.HostType = params.get("HostType")
        self.HostCount = params.get("HostCount")
        self.DryRun = params.get("DryRun")
        self.PurchaseSource = params.get("PurchaseSource")


class SwitchParameterAllocateHostsResponse(AbstractModel):
    """SwitchParameterAllocateHosts返回参数结构体"""

    def __init__(self):
        """
        :param InstanceOrder: cdh订单详细信息
        :type InstanceOrder: :class:`tcecloud.cvm.v20170312.models.HostOrder`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceOrder = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("InstanceOrder") is not None:
            self.InstanceOrder = HostOrder()
            self.InstanceOrder._deserialize(params.get("InstanceOrder"))
        self.RequestId = params.get("RequestId")


class SwitchParameterModifyInstanceInternetChargeTypeRequest(AbstractModel):
    """SwitchParameterModifyInstanceInternetChargeType请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 1
        :type InstanceId: str
        :param InternetAccessible: 1
        :type InternetAccessible: :class:`tcecloud.cvm.v20170312.models.InternetAccessibleModifyChargeType`
        :param DryRun: 1
        :type DryRun: bool
        """
        self.InstanceId = None
        self.InternetAccessible = None
        self.DryRun = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("InternetAccessible") is not None:
            self.InternetAccessible = InternetAccessibleModifyChargeType()
            self.InternetAccessible._deserialize(params.get("InternetAccessible"))
        self.DryRun = params.get("DryRun")


class SwitchParameterModifyInstanceInternetChargeTypeResponse(AbstractModel):
    """SwitchParameterModifyInstanceInternetChargeType返回参数结构体"""

    def __init__(self):
        """
        :param InstanceOrder: 实例订单详情信息。
        :type InstanceOrder: :class:`tcecloud.cvm.v20170312.models.InstanceOrder`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceOrder = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("InstanceOrder") is not None:
            self.InstanceOrder = InstanceOrder()
            self.InstanceOrder._deserialize(params.get("InstanceOrder"))
        self.RequestId = params.get("RequestId")


class SwitchParameterModifyInstancesChargeTypeRequest(AbstractModel):
    """SwitchParameterModifyInstancesChargeType请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 1
        :type InstanceIds: list of str
        :param InstanceChargeType: 1
        :type InstanceChargeType: str
        :param InstanceChargePrepaid: 1
        :type InstanceChargePrepaid: :class:`tcecloud.cvm.v20170312.models.InstanceChargePrepaid`
        :param DryRun: 1
        :type DryRun: bool
        :param ModifyPortableDataDisk: 1
        :type ModifyPortableDataDisk: bool
        """
        self.InstanceIds = None
        self.InstanceChargeType = None
        self.InstanceChargePrepaid = None
        self.DryRun = None
        self.ModifyPortableDataDisk = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.InstanceChargeType = params.get("InstanceChargeType")
        if params.get("InstanceChargePrepaid") is not None:
            self.InstanceChargePrepaid = InstanceChargePrepaid()
            self.InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))
        self.DryRun = params.get("DryRun")
        self.ModifyPortableDataDisk = params.get("ModifyPortableDataDisk")


class SwitchParameterModifyInstancesChargeTypeResponse(AbstractModel):
    """SwitchParameterModifyInstancesChargeType返回参数结构体"""

    def __init__(self):
        """
        :param InstanceOrder: 实例订单详情信息。
        :type InstanceOrder: :class:`tcecloud.cvm.v20170312.models.InstanceOrder`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceOrder = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("InstanceOrder") is not None:
            self.InstanceOrder = InstanceOrder()
            self.InstanceOrder._deserialize(params.get("InstanceOrder"))
        self.RequestId = params.get("RequestId")


class SwitchParameterRenewHostsRequest(AbstractModel):
    """SwitchParameterRenewHosts请求参数结构体"""

    def __init__(self):
        """
        :param HostIds: 一个或多个待操作的CDH实例ID。
        :type HostIds: list of str
        :param HostChargePrepaid: 预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月实例的购买时长、是否设置自动续费等属性。若指定实例的付费模式为预付费则该参数必传。
        :type HostChargePrepaid: :class:`tcecloud.cvm.v20170312.models.ChargePrepaid`
        :param DryRun: 是否跳过实际执行逻辑。
        :type DryRun: bool
        """
        self.HostIds = None
        self.HostChargePrepaid = None
        self.DryRun = None

    def _deserialize(self, params):
        self.HostIds = params.get("HostIds")
        if params.get("HostChargePrepaid") is not None:
            self.HostChargePrepaid = ChargePrepaid()
            self.HostChargePrepaid._deserialize(params.get("HostChargePrepaid"))
        self.DryRun = params.get("DryRun")


class SwitchParameterRenewHostsResponse(AbstractModel):
    """SwitchParameterRenewHosts返回参数结构体"""

    def __init__(self):
        """
        :param InstanceOrder: cdh订单详细信息
        :type InstanceOrder: :class:`tcecloud.cvm.v20170312.models.HostOrder`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceOrder = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("InstanceOrder") is not None:
            self.InstanceOrder = HostOrder()
            self.InstanceOrder._deserialize(params.get("InstanceOrder"))
        self.RequestId = params.get("RequestId")


class SwitchParameterRenewInstancesRequest(AbstractModel):
    """SwitchParameterRenewInstances请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 1
        :type InstanceIds: list of str
        :param InstanceChargePrepaid: 1
        :type InstanceChargePrepaid: :class:`tcecloud.cvm.v20170312.models.InstanceChargePrepaid`
        :param InternetAccessible: 1
        :type InternetAccessible: :class:`tcecloud.cvm.v20170312.models.InternetAccessible`
        :param DryRun: 1
        :type DryRun: bool
        :param RenewPortableDataDisk: 1
        :type RenewPortableDataDisk: bool
        """
        self.InstanceIds = None
        self.InstanceChargePrepaid = None
        self.InternetAccessible = None
        self.DryRun = None
        self.RenewPortableDataDisk = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        if params.get("InstanceChargePrepaid") is not None:
            self.InstanceChargePrepaid = InstanceChargePrepaid()
            self.InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))
        if params.get("InternetAccessible") is not None:
            self.InternetAccessible = InternetAccessible()
            self.InternetAccessible._deserialize(params.get("InternetAccessible"))
        self.DryRun = params.get("DryRun")
        self.RenewPortableDataDisk = params.get("RenewPortableDataDisk")


class SwitchParameterRenewInstancesResponse(AbstractModel):
    """SwitchParameterRenewInstances返回参数结构体"""

    def __init__(self):
        """
        :param InstanceOrder: 实例订单详情信息。
        :type InstanceOrder: :class:`tcecloud.cvm.v20170312.models.InstanceOrder`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceOrder = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("InstanceOrder") is not None:
            self.InstanceOrder = InstanceOrder()
            self.InstanceOrder._deserialize(params.get("InstanceOrder"))
        self.RequestId = params.get("RequestId")


class SwitchParameterResetInstanceRequest(AbstractModel):
    """SwitchParameterResetInstance请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 1
        :type InstanceId: str
        :param ImageId: 1
        :type ImageId: str
        :param SystemDisk: 1
        :type SystemDisk: :class:`tcecloud.cvm.v20170312.models.SystemDisk`
        :param LoginSettings: 1
        :type LoginSettings: :class:`tcecloud.cvm.v20170312.models.LoginSettings`
        :param EnhancedService: 1
        :type EnhancedService: :class:`tcecloud.cvm.v20170312.models.EnhancedService`
        :param DryRun: 1
        :type DryRun: bool
        """
        self.InstanceId = None
        self.ImageId = None
        self.SystemDisk = None
        self.LoginSettings = None
        self.EnhancedService = None
        self.DryRun = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.ImageId = params.get("ImageId")
        if params.get("SystemDisk") is not None:
            self.SystemDisk = SystemDisk()
            self.SystemDisk._deserialize(params.get("SystemDisk"))
        if params.get("LoginSettings") is not None:
            self.LoginSettings = LoginSettings()
            self.LoginSettings._deserialize(params.get("LoginSettings"))
        if params.get("EnhancedService") is not None:
            self.EnhancedService = EnhancedService()
            self.EnhancedService._deserialize(params.get("EnhancedService"))
        self.DryRun = params.get("DryRun")


class SwitchParameterResetInstanceResponse(AbstractModel):
    """SwitchParameterResetInstance返回参数结构体"""

    def __init__(self):
        """
        :param InstanceOrder: 实例订单详情信息。
        :type InstanceOrder: :class:`tcecloud.cvm.v20170312.models.InstanceOrder`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceOrder = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("InstanceOrder") is not None:
            self.InstanceOrder = InstanceOrder()
            self.InstanceOrder._deserialize(params.get("InstanceOrder"))
        self.RequestId = params.get("RequestId")


class SwitchParameterResetInstancesInternetMaxBandwidthRequest(AbstractModel):
    """SwitchParameterResetInstancesInternetMaxBandwidth请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 1
        :type InstanceIds: list of str
        :param InternetAccessible: 1
        :type InternetAccessible: :class:`tcecloud.cvm.v20170312.models.InternetAccessible`
        :param StartTime: 1
        :type StartTime: str
        :param EndTime: 1
        :type EndTime: str
        :param DryRun: 1
        :type DryRun: bool
        """
        self.InstanceIds = None
        self.InternetAccessible = None
        self.StartTime = None
        self.EndTime = None
        self.DryRun = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        if params.get("InternetAccessible") is not None:
            self.InternetAccessible = InternetAccessible()
            self.InternetAccessible._deserialize(params.get("InternetAccessible"))
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.DryRun = params.get("DryRun")


class SwitchParameterResetInstancesInternetMaxBandwidthResponse(AbstractModel):
    """SwitchParameterResetInstancesInternetMaxBandwidth返回参数结构体"""

    def __init__(self):
        """
        :param InstanceOrder: 实例订单详情信息。
        :type InstanceOrder: :class:`tcecloud.cvm.v20170312.models.InstanceOrder`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceOrder = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("InstanceOrder") is not None:
            self.InstanceOrder = InstanceOrder()
            self.InstanceOrder._deserialize(params.get("InstanceOrder"))
        self.RequestId = params.get("RequestId")


class SwitchParameterResetInstancesTypeRequest(AbstractModel):
    """SwitchParameterResetInstancesType请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 1
        :type InstanceIds: list of str
        :param InstanceType: 1
        :type InstanceType: str
        :param ForceStop: 1
        :type ForceStop: bool
        :param DryRun: 1
        :type DryRun: bool
        """
        self.InstanceIds = None
        self.InstanceType = None
        self.ForceStop = None
        self.DryRun = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.InstanceType = params.get("InstanceType")
        self.ForceStop = params.get("ForceStop")
        self.DryRun = params.get("DryRun")


class SwitchParameterResetInstancesTypeResponse(AbstractModel):
    """SwitchParameterResetInstancesType返回参数结构体"""

    def __init__(self):
        """
        :param InstanceOrder: 实例订单详情信息。
        :type InstanceOrder: :class:`tcecloud.cvm.v20170312.models.InstanceOrder`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceOrder = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("InstanceOrder") is not None:
            self.InstanceOrder = InstanceOrder()
            self.InstanceOrder._deserialize(params.get("InstanceOrder"))
        self.RequestId = params.get("RequestId")


class SwitchParameterResizeInstanceDisksRequest(AbstractModel):
    """SwitchParameterResizeInstanceDisks请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 1
        :type InstanceId: str
        :param DataDisks: 1
        :type DataDisks: list of DataDisk
        :param ForceStop: 1
        :type ForceStop: bool
        :param DryRun: 1
        :type DryRun: bool
        """
        self.InstanceId = None
        self.DataDisks = None
        self.ForceStop = None
        self.DryRun = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("DataDisks") is not None:
            self.DataDisks = []
            for item in params.get("DataDisks"):
                obj = DataDisk()
                obj._deserialize(item)
                self.DataDisks.append(obj)
        self.ForceStop = params.get("ForceStop")
        self.DryRun = params.get("DryRun")


class SwitchParameterResizeInstanceDisksResponse(AbstractModel):
    """SwitchParameterResizeInstanceDisks返回参数结构体"""

    def __init__(self):
        """
        :param InstanceOrder: 实例订单详情信息。
        :type InstanceOrder: :class:`tcecloud.cvm.v20170312.models.InstanceOrder`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceOrder = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("InstanceOrder") is not None:
            self.InstanceOrder = InstanceOrder()
            self.InstanceOrder._deserialize(params.get("InstanceOrder"))
        self.RequestId = params.get("RequestId")


class SwitchParameterRunInstancesRequest(AbstractModel):
    """SwitchParameterRunInstances请求参数结构体"""

    def __init__(self):
        """
        :param Placement: 1
        :type Placement: :class:`tcecloud.cvm.v20170312.models.Placement`
        :param ImageId: 1
        :type ImageId: str
        :param HostName: 1
        :type HostName: str
        :param ClientToken: 1
        :type ClientToken: str
        :param InstanceChargePrepaid: 1
        :type InstanceChargePrepaid: :class:`tcecloud.cvm.v20170312.models.InstanceChargePrepaid`
        :param InstanceChargeType: 1
        :type InstanceChargeType: str
        :param InstanceType: 1
        :type InstanceType: str
        :param SystemDisk: 1
        :type SystemDisk: :class:`tcecloud.cvm.v20170312.models.SystemDisk`
        :param DataDisks: 1
        :type DataDisks: list of DataDisk
        :param VirtualPrivateCloud: 1
        :type VirtualPrivateCloud: :class:`tcecloud.cvm.v20170312.models.VirtualPrivateCloud`
        :param InternetAccessible: 1
        :type InternetAccessible: :class:`tcecloud.cvm.v20170312.models.InternetAccessible`
        :param InstanceCount: 1
        :type InstanceCount: int
        :param InstanceName: 1
        :type InstanceName: str
        :param LoginSettings: 1
        :type LoginSettings: :class:`tcecloud.cvm.v20170312.models.LoginSettings`
        :param SecurityGroupIds: 1
        :type SecurityGroupIds: list of str
        :param EnhancedService: 1
        :type EnhancedService: :class:`tcecloud.cvm.v20170312.models.EnhancedService`
        :param DryRun: 1
        :type DryRun: bool
        :param UserData: 1
        :type UserData: str
        :param AvailableZone: 1
        :type AvailableZone: str
        :param PurchaseSource: 内部参数，购买来源
        :type PurchaseSource: str
        :param DisasterRecoverGroupIds: 1
        :type DisasterRecoverGroupIds: list of str
        :param DesAction: 1
        :type DesAction: str
        :param ActionTimer: 1
        :type ActionTimer: :class:`tcecloud.cvm.v20170312.models.ActionTimer`
        :param PurchaseSource: 内部参数，购买来源
        :type PurchaseSource: str
        """
        self.Placement = None
        self.ImageId = None
        self.HostName = None
        self.ClientToken = None
        self.InstanceChargePrepaid = None
        self.InstanceChargeType = None
        self.InstanceType = None
        self.SystemDisk = None
        self.DataDisks = None
        self.VirtualPrivateCloud = None
        self.InternetAccessible = None
        self.InstanceCount = None
        self.InstanceName = None
        self.LoginSettings = None
        self.SecurityGroupIds = None
        self.EnhancedService = None
        self.DryRun = None
        self.UserData = None
        self.AvailableZone = None
        self.PurchaseSource = None
        self.DisasterRecoverGroupIds = None
        self.DesAction = None
        self.ActionTimer = None
        self.PurchaseSource = None

    def _deserialize(self, params):
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        self.ImageId = params.get("ImageId")
        self.HostName = params.get("HostName")
        self.ClientToken = params.get("ClientToken")
        if params.get("InstanceChargePrepaid") is not None:
            self.InstanceChargePrepaid = InstanceChargePrepaid()
            self.InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))
        self.InstanceChargeType = params.get("InstanceChargeType")
        self.InstanceType = params.get("InstanceType")
        if params.get("SystemDisk") is not None:
            self.SystemDisk = SystemDisk()
            self.SystemDisk._deserialize(params.get("SystemDisk"))
        if params.get("DataDisks") is not None:
            self.DataDisks = []
            for item in params.get("DataDisks"):
                obj = DataDisk()
                obj._deserialize(item)
                self.DataDisks.append(obj)
        if params.get("VirtualPrivateCloud") is not None:
            self.VirtualPrivateCloud = VirtualPrivateCloud()
            self.VirtualPrivateCloud._deserialize(params.get("VirtualPrivateCloud"))
        if params.get("InternetAccessible") is not None:
            self.InternetAccessible = InternetAccessible()
            self.InternetAccessible._deserialize(params.get("InternetAccessible"))
        self.InstanceCount = params.get("InstanceCount")
        self.InstanceName = params.get("InstanceName")
        if params.get("LoginSettings") is not None:
            self.LoginSettings = LoginSettings()
            self.LoginSettings._deserialize(params.get("LoginSettings"))
        self.SecurityGroupIds = params.get("SecurityGroupIds")
        if params.get("EnhancedService") is not None:
            self.EnhancedService = EnhancedService()
            self.EnhancedService._deserialize(params.get("EnhancedService"))
        self.DryRun = params.get("DryRun")
        self.UserData = params.get("UserData")
        self.AvailableZone = params.get("AvailableZone")
        self.PurchaseSource = params.get("PurchaseSource")
        self.DisasterRecoverGroupIds = params.get("DisasterRecoverGroupIds")
        self.DesAction = params.get("DesAction")
        if params.get("ActionTimer") is not None:
            self.ActionTimer = ActionTimer()
            self.ActionTimer._deserialize(params.get("ActionTimer"))
        self.PurchaseSource = params.get("PurchaseSource")


class SwitchParameterRunInstancesResponse(AbstractModel):
    """SwitchParameterRunInstances返回参数结构体"""

    def __init__(self):
        """
        :param InstanceOrder: 实例订单详情信息。
        :type InstanceOrder: :class:`tcecloud.cvm.v20170312.models.InstanceOrder`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceOrder = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("InstanceOrder") is not None:
            self.InstanceOrder = InstanceOrder()
            self.InstanceOrder._deserialize(params.get("InstanceOrder"))
        self.RequestId = params.get("RequestId")


class SyncImagesRequest(AbstractModel):
    """SyncImages请求参数结构体"""

    def __init__(self):
        """
        :param ImageIds: 镜像ID列表 ，镜像ID可以通过如下方式获取：<br><li>通过DescribeImages接口返回的`ImageId`获取。<br><li>通过镜像控制台获取。<br>镜像ID必须满足限制：<br><li>镜像ID对应的镜像状态必须为`NORMAL`。<br><li>镜像大小小于50GB。<br>镜像状态请参考镜像数据表。
        :type ImageIds: list of str
        :param DestinationRegions: 目的同步地域列表；必须满足限制：<br><li>不能为源地域，<br><li>必须是一个合法的Region。<br><li>暂不支持部分地域同步。<br>具体地域参数请参考Region。
        :type DestinationRegions: list of str
        """
        self.ImageIds = None
        self.DestinationRegions = None

    def _deserialize(self, params):
        self.ImageIds = params.get("ImageIds")
        self.DestinationRegions = params.get("DestinationRegions")


class SyncImagesResponse(AbstractModel):
    """SyncImages返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class SystemDisk(AbstractModel):
    """描述了操作系统所在块设备即系统盘的信息"""

    def __init__(self):
        """
        :param DiskType: 系统盘类型。系统盘类型限制详见CVM实例配置。取值范围：<br><li>LOCAL_BASIC：本地硬盘<br><li>LOCAL_SSD：本地SSD硬盘<br><li>CLOUD_BASIC：普通云硬盘<br><li>CLOUD_SSD：SSD云硬盘<br><br>默认取值：LOCAL_BASIC。
        :type DiskType: str
        :param DiskId: 系统盘ID。LOCAL_BASIC 和 LOCAL_SSD 类型没有ID。暂时不支持该参数。
        :type DiskId: str
        :param DiskSize: 系统盘大小，单位：GB。默认值为 50
        :type DiskSize: int
        :param DiskStoragePoolGroup: 系统盘指定的存储池。
        :type DiskStoragePoolGroup: str
        """
        self.DiskType = None
        self.DiskId = None
        self.DiskSize = None
        self.DiskStoragePoolGroup = None

    def _deserialize(self, params):
        self.DiskType = params.get("DiskType")
        self.DiskId = params.get("DiskId")
        self.DiskSize = params.get("DiskSize")
        self.DiskStoragePoolGroup = params.get("DiskStoragePoolGroup")


class Tag(AbstractModel):
    """标签键值对"""

    def __init__(self):
        """
        :param Key: 标签键
        :type Key: str
        :param Value: 标签值
        :type Value: str
        """
        self.Key = None
        self.Value = None

    def _deserialize(self, params):
        self.Key = params.get("Key")
        self.Value = params.get("Value")


class TagSpecification(AbstractModel):
    """创建云主机实例时同时绑定的标签对说明"""

    def __init__(self):
        """
        :param ResourceType: 标签绑定的资源类型
        :type ResourceType: str
        :param Tags: 标签对列表
        :type Tags: list of Tag
        """
        self.ResourceType = None
        self.Tags = None

    def _deserialize(self, params):
        self.ResourceType = params.get("ResourceType")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)


class TerminateInstancesRequest(AbstractModel):
    """TerminateInstances请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 一个或多个待操作的实例ID。可通过`DescribeInstances`接口返回值中的`InstanceId`获取。每次请求批量实例的上限为100。
        :type InstanceIds: list of str
        :param ReleaseAddress: 内部参数，释放弹性IP。
        :type ReleaseAddress: bool
        :param DryRun: 试运行。
        :type DryRun: bool
        """
        self.InstanceIds = None
        self.ReleaseAddress = None
        self.DryRun = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.ReleaseAddress = params.get("ReleaseAddress")
        self.DryRun = params.get("DryRun")


class TerminateInstancesResponse(AbstractModel):
    """TerminateInstances返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class TransformAddressRequest(AbstractModel):
    """TransformAddress请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 1
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class TransformAddressResponse(AbstractModel):
    """TransformAddress返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpdateDisasterRecoverGroupRequest(AbstractModel):
    """UpdateDisasterRecoverGroup请求参数结构体"""

    def __init__(self):
        """
        :param DisasterRecoverGroupId: 1
        :type DisasterRecoverGroupId: str
        :param Name: 1
        :type Name: str
        """
        self.DisasterRecoverGroupId = None
        self.Name = None

    def _deserialize(self, params):
        self.DisasterRecoverGroupId = params.get("DisasterRecoverGroupId")
        self.Name = params.get("Name")


class UpdateDisasterRecoverGroupResponse(AbstractModel):
    """UpdateDisasterRecoverGroup返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpdateInstanceVpcConfigRequest(AbstractModel):
    """UpdateInstanceVpcConfig请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 待操作的实例ID。可通过`DescribeInstances`接口返回值中的`InstanceId`获取。
        :type InstanceId: str
        :param VirtualPrivateCloud: 私有网络相关信息配置。通过该参数指定私有网络的ID，子网ID，私有网络ip等信息。
        :type VirtualPrivateCloud: :class:`tcecloud.cvm.v20170312.models.VirtualPrivateCloud`
        :param ForceStop: 是否对运行中的实例选择强制关机。默认为TRUE。
        :type ForceStop: bool
        """
        self.InstanceId = None
        self.VirtualPrivateCloud = None
        self.ForceStop = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("VirtualPrivateCloud") is not None:
            self.VirtualPrivateCloud = VirtualPrivateCloud()
            self.VirtualPrivateCloud._deserialize(params.get("VirtualPrivateCloud"))
        self.ForceStop = params.get("ForceStop")


class UpdateInstanceVpcConfigResponse(AbstractModel):
    """UpdateInstanceVpcConfig返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpdateInstancesActionTimerRequest(AbstractModel):
    """UpdateInstancesActionTimer请求参数结构体"""

    def __init__(self):
        """
        :param ActionTimerIds: 1
        :type ActionTimerIds: list of str
        :param ActionTimer: 1
        :type ActionTimer: :class:`tcecloud.cvm.v20170312.models.ActionTimer`
        """
        self.ActionTimerIds = None
        self.ActionTimer = None

    def _deserialize(self, params):
        self.ActionTimerIds = params.get("ActionTimerIds")
        if params.get("ActionTimer") is not None:
            self.ActionTimer = ActionTimer()
            self.ActionTimer._deserialize(params.get("ActionTimer"))


class UpdateInstancesActionTimerResponse(AbstractModel):
    """UpdateInstancesActionTimer返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UserZoneStatusItem(AbstractModel):
    """可用区实例计费类型状态。"""

    def __init__(self):
        """
        :param Zone: 可用区
        :type Zone: str
        :param InstanceChargeType: 计费类型
        :type InstanceChargeType: str
        :param Status: 售卖状态
        :type Status: str
        """
        self.Zone = None
        self.InstanceChargeType = None
        self.Status = None

    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.InstanceChargeType = params.get("InstanceChargeType")
        self.Status = params.get("Status")


class VirtualPrivateCloud(AbstractModel):
    """描述了VPC相关信息，包括子网，IP信息等"""

    def __init__(self):
        """
        :param VpcId: 私有网络ID，形如`vpc-xxx`。有效的VpcId可通过登录控制台查询；也可以调用接口 DescribeVpcEx ，从接口返回中的`unVpcId`字段获取。
        :type VpcId: str
        :param SubnetId: 私有网络子网ID，形如`subnet-xxx`。有效的私有网络子网ID可通过登录控制台查询；也可以调用接口  DescribeSubnetEx ，从接口返回中的`unSubnetId`字段获取。
        :type SubnetId: str
        :param AsVpcGateway: 是否用作公网网关。公网网关只有在实例拥有公网IP以及处于私有网络下时才能正常使用。取值范围：<br><li>TRUE：表示用作公网网关<br><li>FALSE：表示不用作公网网关<br><br>默认取值：FALSE。
        :type AsVpcGateway: bool
        :param PrivateIpAddresses: 私有网络子网 IP 数组，在创建实例、修改实例vpc属性操作中可使用此参数。当前仅批量创建多台实例时支持传入相同子网的多个 IP。
        :type PrivateIpAddresses: list of str
        :param Ipv6AddressCount: 为弹性网卡指定随机生成的 IPv6 地址数量。
        :type Ipv6AddressCount: int
        """
        self.VpcId = None
        self.SubnetId = None
        self.AsVpcGateway = None
        self.PrivateIpAddresses = None
        self.Ipv6AddressCount = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.AsVpcGateway = params.get("AsVpcGateway")
        self.PrivateIpAddresses = params.get("PrivateIpAddresses")
        self.Ipv6AddressCount = params.get("Ipv6AddressCount")


class ZoneCpuQuota(AbstractModel):
    """可用区CPU配额信息"""

    def __init__(self):
        """
        :param Zone: 可用区。
        :type Zone: str
        :param InstanceChargeType: 实例计费模式 (PREPAID：表示预付费，即包年包月 | POSTPAID_BY_HOUR：表示后付费，即按量计费 | CDHPAID：表示CDH付费，即只对CDH计费，不对CDH上的实例计费。 )
        :type InstanceChargeType: str
        :param cpuQuota: 可用CPU配额。
        :type cpuQuota: int
        """
        self.Zone = None
        self.InstanceChargeType = None
        self.cpuQuota = None

    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.InstanceChargeType = params.get("InstanceChargeType")
        self.cpuQuota = params.get("cpuQuota")


class ZoneInfo(AbstractModel):
    """可用区信息"""

    def __init__(self):
        """
        :param Zone: 可用区名称，例如，ap-guangzhou-3
        :type Zone: str
        :param ZoneName: 可用区描述，例如，广州三区
        :type ZoneName: str
        :param ZoneId: 可用区ID
        :type ZoneId: str
        :param ZoneState: 可用区状态
        :type ZoneState: str
        """
        self.Zone = None
        self.ZoneName = None
        self.ZoneId = None
        self.ZoneState = None

    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.ZoneName = params.get("ZoneName")
        self.ZoneId = params.get("ZoneId")
        self.ZoneState = params.get("ZoneState")

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
        :type Externals: :class:`tcecloud.bms.v20180813.models.Externals`
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


class DescribeDisksRequest(AbstractModel):
    """DescribeDisks请求参数结构体"""

    def __init__(self):
        """
        :param DiskIds: 按照一个或者多个云硬盘ID查询。云硬盘ID形如：`disk-11112222`，此参数的具体格式可参考API简介的ids.N一节）。参数不支持同时指定`DiskIds`和`Filters`。
        :type DiskIds: list of str
        :param Filters: 过滤条件。参数不支持同时指定`DiskIds`和`Filters`。<br><li>disk-id - Array of String - 是否必填：否 -（过滤条件）按照云硬盘ID过滤。云盘ID形如：`disk-11112222`。<br><li>instance-id - Array of String - 是否必填：否 -（过滤条件）按照云盘挂载的云主机实例ID过滤。可根据此参数查询挂载在指定云主机下的云硬盘。<br><li>zone - Array of String - 是否必填：否 -（过滤条件）按照[可用区]过滤。
        :type Filters: list of Filter
        :param Offset: API简介中的相关小节。
        :type Offset: int
        :param Limit: 返回数量，默认为20，最大值为100。关于`Limit`的更进一步介绍请参考 API 简介中的相关小节。
        :type Limit: int
        """
        self.DiskIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeDisksResponse(AbstractModel):
    """DescribeDisks返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的云硬盘数量。
        :type TotalCount: int
        :param DiskSet: 云硬盘的详细信息列表。
        :type DiskSet: list of Disk
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.DiskSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("DiskSet") is not None:
            self.DiskSet = []
            for item in params.get("DiskSet"):
                obj = Disk()
                obj._deserialize(item)
                self.DiskSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeFlavorsRequest(AbstractModel):
    """DescribeFlavors请求参数结构体"""

    def __init__(self):
        """
                :param FlavorIds: 按照一个或者多个实例ID查询。实例ID形如：`flavor-11112222`,每次请求的实例的上限为100。参数不支持同时指定`FlavorIds`和`Filters`。
                :type FlavorIds: list of str
                :param Filters: 过滤条件。
        <li> zone - String - 是否必填：否 -（过滤条件）按照可用区过滤。</li>
        <li> flavor-id - String - 是否必填：否 - （过滤条件）按照实例ID过滤。实例ID形如：flavor-11112222。</li>
        <li> flavor-name - String - 是否必填：否 - （过滤条件）按照实例名称过滤。</li>
        每次请求的`Filters`的上限为10，`Filter.Values`的上限为5。参数不支持同时指定`FlavorIds`和`Filters`。
                :type Filters: list of Filter
                :param Offset: 过滤条件。
        <li> zone - String - 是否必填：否 -（过滤条件）按照可用区过滤。</li>
        <li> flavor-id - String - 是否必填：否 - （过滤条件）按照实例ID过滤。实例ID形如：flavor-11112222。</li>
        <li> flavor-name - String - 是否必填：否 - （过滤条件）按照实例名称过滤。</li>
        每次请求的`Filters`的上限为10，`Filter.Values`的上限为5。参数不支持同时指定`FlavorIds`和`Filters`。
                :type Offset: int
                :param Limit: 返回数量，默认为20，最大值为100。关于`Limit`的更进一步介绍请参考 API 简介中的相关小节。
                :type Limit: int
        """
        self.FlavorIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.FlavorIds = params.get("FlavorIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeFlavorsResponse(AbstractModel):
    """DescribeFlavors返回参数结构体"""

    def __init__(self):
        """
        :param FlavorSet: 套餐详情列表
        :type FlavorSet: list of Flavor
        :param TotalCount: 套餐总数
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FlavorSet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("FlavorSet") is not None:
            self.FlavorSet = []
            for item in params.get("FlavorSet"):
                obj = Flavor()
                obj._deserialize(item)
                self.FlavorSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeInstancesRequest(AbstractModel):
    """DescribeInstances请求参数结构体"""

    def __init__(self):
        """
                :param InstanceIds: 按照一个或者多个实例ID查询。实例ID形如：`bms-11112222`。（此参数的具体格式可参考API简介的`id.N`一节）。每次请求的实例的上限为100。参数不支持同时指定`InstanceIds`和`Filters`。
                :type InstanceIds: list of str
                :param Filters: 过滤条件。
        <li> zone - String - 是否必填：否 -（过滤条件）按照可用区过滤。</li>
        <li> uuid- String - 是否必填：否 - （过滤条件）按照实例UUID过滤。</li>
        <li> instance-id - String - 是否必填：否 - （过滤条件）按照实例ID过滤。实例ID形如：ins-11112222。</li>
        <li> instance-name - String - 是否必填：否 - （过滤条件）按照实例名称过滤。</li>
        <li> instance-state - String - 是否必填：否 -（过滤条件）按照实例的状态过滤 </li>
        <li> private-ip-address - String - 是否必填：否 - （过滤条件）按照实例主网卡的内网IP过滤。</li>
        <li> vpc-id - String - 是否必填：否 - （过滤条件）按照实例所属的vpcid进行过滤 </li>
        <li> subnet-id - String - 是否必填：否 - （过滤条件）按照实例所属的子网id进行过滤。</li>
        每次请求的`Filters`的上限为10，`Filter.Values`的上限为5。参数不支持同时指定`InstanceIds`和`Filters`。
                :type Filters: list of Filter
                :param Offset: 偏移量，默认为0。关于`Offset`的更进一步介绍请参考 API 简介中的相关小节。
                :type Offset: int
                :param Limit: 返回数量，默认为20，最大值为100。关于`Limit`的更进一步介绍请参考 API 简介中的相关小节。
                :type Limit: int
        """
        self.InstanceIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

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


class DescribeInstancesResponse(AbstractModel):
    """DescribeInstances返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 实例总数量
        :type TotalCount: int
        :param InstanceSet: 实例的详细信息列表
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


class Disk(AbstractModel):
    """描述了BMS硬盘的详细信息"""

    def __init__(self):
        """
        :param DiskId: 硬盘ID。
        :type DiskId: str
        :param Placement: 硬盘所在的位置。
        :type Placement: :class:`tcecloud.bms.v20180813.models.Placement`
        :param DiskName: 硬盘名称。
        :type DiskName: str
        :param DiskSize: 硬盘大小。
        :type DiskSize: str
        :param InstanceId: 硬盘挂载的云主机ID。
        :type InstanceId: str
        :param DiskType: 云盘介质类型。取值范围：<br><li>CLOUD_BASIC：表示普通云硬<br><li>CLOUD_PREMIUM：表示高性能云硬盘<br><li>CLOUD_SSD：SSD表示SSD云硬盘。
        :type DiskType: str
        :param CreatedTime: 硬盘的创建时间。
        :type CreatedTime: str
        """
        self.DiskId = None
        self.Placement = None
        self.DiskName = None
        self.DiskSize = None
        self.InstanceId = None
        self.DiskType = None
        self.CreatedTime = None

    def _deserialize(self, params):
        self.DiskId = params.get("DiskId")
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        self.DiskName = params.get("DiskName")
        self.DiskSize = params.get("DiskSize")
        self.InstanceId = params.get("InstanceId")
        self.DiskType = params.get("DiskType")
        self.CreatedTime = params.get("CreatedTime")


class EnhancedService(AbstractModel):
    """描述了实例的增强服务启用情况与其设置，如云安全，云监控等实例 Agent"""

    def __init__(self):
        """
        :param SecurityService: 开启云安全服务。若不指定该参数，则默认
        :type SecurityService: bool
        :param MonitorService: 开启云安全服务。若不指定该参数，则默认开启云监控服务。
        :type MonitorService: bool
        """
        self.SecurityService = None
        self.MonitorService = None

    def _deserialize(self, params):
        self.SecurityService = params.get("SecurityService")
        self.MonitorService = params.get("MonitorService")


class Externals(AbstractModel):
    """扩展数据"""


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


class Flavor(AbstractModel):
    """套餐详情"""

    def __init__(self):
        """
        :param FlavorId: 套餐ID。
        :type FlavorId: str
        :param FlavorName: 套餐名称。
        :type FlavorName: str
        :param Placement: 实例所在的位置。
        :type Placement: :class:`tcecloud.bms.v20180813.models.Placement`
        :param RaidType: 支持的Raid类型。
        :type RaidType: list of str
        :param OperatingSystem: 支持的系统列表。
        :type OperatingSystem: :class:`tcecloud.bms.v20180813.models.OperatingSystem`
        :param Cpu: cpu信息。
        :type Cpu: str
        :param Memory: 内存信息。
        :type Memory: str
        :param SystemDisk: 硬盘信息。
        :type SystemDisk: str
        :param NetSpeed: 网卡信息
        :type NetSpeed: str
        :param CreatedTime: 创建时间。按照`ISO8601`标准表示，并且使用`UTC`时间。格式为：`YYYY-MM-DDThh:mm:ssZ`。
        :type CreatedTime: str
        :param UserDefined: 用户自定义
        :type UserDefined: int
        :param Soldout: 是否已售卖
        :type Soldout: int
        """
        self.FlavorId = None
        self.FlavorName = None
        self.Placement = None
        self.RaidType = None
        self.OperatingSystem = None
        self.Cpu = None
        self.Memory = None
        self.SystemDisk = None
        self.NetSpeed = None
        self.CreatedTime = None
        self.UserDefined = None
        self.Soldout = None

    def _deserialize(self, params):
        self.FlavorId = params.get("FlavorId")
        self.FlavorName = params.get("FlavorName")
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        self.RaidType = params.get("RaidType")
        if params.get("OperatingSystem") is not None:
            self.OperatingSystem = OperatingSystem()
            self.OperatingSystem._deserialize(params.get("OperatingSystem"))
        self.Cpu = params.get("Cpu")
        self.Memory = params.get("Memory")
        self.SystemDisk = params.get("SystemDisk")
        self.NetSpeed = params.get("NetSpeed")
        self.CreatedTime = params.get("CreatedTime")
        self.UserDefined = params.get("UserDefined")
        self.Soldout = params.get("Soldout")


class GetInstancesByTaskIdRequest(AbstractModel):
    """GetInstancesByTaskId请求参数结构体"""

    def __init__(self):
        """
        :param TaskIds: 任务ID列表
        :type TaskIds: list of int
        """
        self.TaskIds = None

    def _deserialize(self, params):
        self.TaskIds = params.get("TaskIds")


class GetInstancesByTaskIdResponse(AbstractModel):
    """GetInstancesByTaskId返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class InquiryPriceBmsInstanceForTradeRequest(AbstractModel):
    """InquiryPriceBmsInstanceForTrade请求参数结构体"""

    def __init__(self):
        """
        :param Zone: 可用区
        :type Zone: str
        :param ProductCode: 产品编码
        :type ProductCode: str
        :param SubProductCode: 子产品编码
        :type SubProductCode: str
        :param BmsFlavor: 计费机型
        :type BmsFlavor: str
        """
        self.Zone = None
        self.ProductCode = None
        self.SubProductCode = None
        self.BmsFlavor = None

    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.ProductCode = params.get("ProductCode")
        self.SubProductCode = params.get("SubProductCode")
        self.BmsFlavor = params.get("BmsFlavor")


class InquiryPriceBmsInstanceForTradeResponse(AbstractModel):
    """InquiryPriceBmsInstanceForTrade返回参数结构体"""

    def __init__(self):
        """
        :param UnitPrice: 单价
        :type UnitPrice: int
        :param ChargeUnit: 商品的时间单位
        :type ChargeUnit: str
        :param OriginalPrice: 总费用
        :type OriginalPrice: int
        :param DiscountPrice: 优惠后总价
        :type DiscountPrice: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.UnitPrice = None
        self.ChargeUnit = None
        self.OriginalPrice = None
        self.DiscountPrice = None
        self.RequestId = None

    def _deserialize(self, params):
        self.UnitPrice = params.get("UnitPrice")
        self.ChargeUnit = params.get("ChargeUnit")
        self.OriginalPrice = params.get("OriginalPrice")
        self.DiscountPrice = params.get("DiscountPrice")
        self.RequestId = params.get("RequestId")


class Instance(AbstractModel):
    """描述实例的信息"""

    def __init__(self):
        """
        :param Placement: 实例所在的位置。
        :type Placement: :class:`tcecloud.bms.v20180813.models.Placement`
        :param InstanceId: 实例`ID`。
        :type InstanceId: str
        :param InstanceName: 实例名称。
        :type InstanceName: str
        :param RaidType: Raid类型。
        :type RaidType: str
        :param OperatingSystemType: 操作系统类型。
        :type OperatingSystemType: str
        :param OperatingSystem: 操作系统发行版本
        :type OperatingSystem: str
        :param PrivateIpAddresses: 实例主网卡的内网`IP`列表。
        :type PrivateIpAddresses: list of str
        :param VirtualPrivateCloud: 实例所属虚拟私有网络信息。
        :type VirtualPrivateCloud: :class:`tcecloud.bms.v20180813.models.VirtualPrivateCloud`
        :param FlavorId: 套餐信息。
        :type FlavorId: str
        :param CreatedTime: 创建时间。按照`ISO8601`标准表示，并且使用`UTC`时间。格式为：`YYYY-MM-DDThh:mm:ssZ`。
        :type CreatedTime: str
        :param Status: 实例状态
        :type Status: str
        :param Uuid: Uuid
        :type Uuid: str
        :param UserDefined: 用户自定义
        :type UserDefined: int
        :param AppId: AppId
        :type AppId: str
        """
        self.Placement = None
        self.InstanceId = None
        self.InstanceName = None
        self.RaidType = None
        self.OperatingSystemType = None
        self.OperatingSystem = None
        self.PrivateIpAddresses = None
        self.VirtualPrivateCloud = None
        self.FlavorId = None
        self.CreatedTime = None
        self.Status = None
        self.Uuid = None
        self.UserDefined = None
        self.AppId = None

    def _deserialize(self, params):
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.RaidType = params.get("RaidType")
        self.OperatingSystemType = params.get("OperatingSystemType")
        self.OperatingSystem = params.get("OperatingSystem")
        self.PrivateIpAddresses = params.get("PrivateIpAddresses")
        if params.get("VirtualPrivateCloud") is not None:
            self.VirtualPrivateCloud = VirtualPrivateCloud()
            self.VirtualPrivateCloud._deserialize(params.get("VirtualPrivateCloud"))
        self.FlavorId = params.get("FlavorId")
        self.CreatedTime = params.get("CreatedTime")
        self.Status = params.get("Status")
        self.Uuid = params.get("Uuid")
        self.UserDefined = params.get("UserDefined")
        self.AppId = params.get("AppId")


class InternetAccessible(AbstractModel):
    """描述了实例的公网可访问性，声明了实例的公网使用计费模式，最大带宽等"""

    def __init__(self):
        """
        :param InternetMaxBandwidthOut: 公网出带宽上限，单位：Mbps。默认值：0Mbps。不同机型带宽上限范围不一致，具体限制详见购买网络带宽。
        :type InternetMaxBandwidthOut: int
        :param PublicIpAssigned: 是否分配公网IP。取值范围：<br><li>TRUE：表示分配公网IP<br><li>FALSE：表示不分配公网IP<br><br>当公网带宽大于0Mbps时，可自由选择开通与否，默认开通公网IP；当公网带宽为0，则不允许分配公网IP。
        :type PublicIpAssigned: bool
        """
        self.InternetMaxBandwidthOut = None
        self.PublicIpAssigned = None

    def _deserialize(self, params):
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        self.PublicIpAssigned = params.get("PublicIpAssigned")


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


class ModifyInstancesAttributeRequest(AbstractModel):
    """ModifyInstancesAttribute请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 一个或多个待操作的实例ID。可通过`DescribeInstances` API返回值中的`InstanceId`获取。每次请求允许操作的实例数量上限是100。
        :type InstanceIds: list of str
        :param InstanceName: 实例名称。可任意命名，但不得超过60个字符。
        :type InstanceName: str
        """
        self.InstanceIds = None
        self.InstanceName = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.InstanceName = params.get("InstanceName")


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


class OperatingSystem(AbstractModel):
    """操作系统信息"""

    def __init__(self):
        """
        :param Linux: 支持的linux系统列表
        :type Linux: list of str
        :param Windows: 支持的windows系统列表
        :type Windows: list of str
        """
        self.Linux = None
        self.Windows = None

    def _deserialize(self, params):
        self.Linux = params.get("Linux")
        self.Windows = params.get("Windows")


class Placement(AbstractModel):
    """描述了实例的抽象位置，包括其所在的可用区，所属的项目等"""

    def __init__(self):
        """
        :param Zone: 实例所属的可用区ID。该参数也可以通过调用  DescribeZones 的返回值中的Zone字段来获取。
        :type Zone: str
        :param ProjectId: 实例所属项目ID。该参数可以通过调用 DescribeProject 的返回值中的 projectId 字段来获取。不填为默认项目。
        :type ProjectId: int
        """
        self.Zone = None
        self.ProjectId = None

    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.ProjectId = params.get("ProjectId")


class QueryTaskRequest(AbstractModel):
    """QueryTask请求参数结构体"""

    def __init__(self):
        """
        :param TaskId: 异步任务请求返回的TaskId。
        :type TaskId: str
        """
        self.TaskId = None

    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")


class QueryTaskResponse(AbstractModel):
    """QueryTask返回参数结构体"""

    def __init__(self):
        """
        :param Status: 异步任务执行结果
        :type Status: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Status = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class RebootInstancesRequest(AbstractModel):
    """RebootInstances请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 一个或多个待操作的实例ID。可通过`DescribeInstances`接口返回值中的`InstanceId`获取。每次请求批量实例的上限为100。
        :type InstanceIds: list of str
        """
        self.InstanceIds = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")


class RebootInstancesResponse(AbstractModel):
    """RebootInstances返回参数结构体"""

    def __init__(self):
        """
        :param TaskId: 返回任务的taskid,可通过taskid查询任务运行情况
        :type TaskId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class ResetInstanceRequest(AbstractModel):
    """ResetInstance请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID。可通过 [DescribeInstances]
        :type InstanceId: str
        :param RaidType: raid类型
        :type RaidType: str
        :param OperatingSystemType: 操作系统类型
        :type OperatingSystemType: str
        :param OperatingSystem: 操作系统发行版本
        :type OperatingSystem: str
        :param LoginSettings: 实例登录设置。
        :type LoginSettings: :class:`tcecloud.bms.v20180813.models.LoginSettings`
        :param EnhancedService: 增强服务。通过该参数可以指定是否开启云安全、云监控等服务。若不指定该参数，则关闭开启云监控、云安全服务。
        :type EnhancedService: :class:`tcecloud.bms.v20180813.models.EnhancedService`
        """
        self.InstanceId = None
        self.RaidType = None
        self.OperatingSystemType = None
        self.OperatingSystem = None
        self.LoginSettings = None
        self.EnhancedService = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.RaidType = params.get("RaidType")
        self.OperatingSystemType = params.get("OperatingSystemType")
        self.OperatingSystem = params.get("OperatingSystem")
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
        :param TaskId: 返回任务的taskid,可通过taskid查询任务运行情况
        :type TaskId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class RunInstancesRequest(AbstractModel):
    """RunInstances请求参数结构体"""

    def __init__(self):
        """
                :param Placement: 实例所在的位置。通过该参数可以指定实例所属可用区，所属项目，专用宿主机（对于独享母机付费模式的子机创建）等属性。
                :type Placement: :class:`tcecloud.bms.v20180813.models.Placement`
                :param FlavorId: 套餐id
                :type FlavorId: str
                :param OperatingSystemType: 系统类型
                :type OperatingSystemType: str
                :param OperatingSystem: 系统的发行版本号
                :type OperatingSystem: str
                :param VirtualPrivateCloud: 私有网络相关信息配置。通过该参数可以指定私有网络的ID，子网ID等信息。若不指定该参数，则默认使用基础网络。若在此参数中指定了私有网络ip，表示每个实例的主网卡ip，而且InstanceCount参数必须与私有网络ip的个数一致。
                :type VirtualPrivateCloud: :class:`tcecloud.bms.v20180813.models.VirtualPrivateCloud`
                :param LoginSettings: 实例登录设置。通过该参数可以设置实例的登录方式密码、密钥或保持镜像的原始登录设置。默认情况下会随机生成密码，并以站内信方式知会到用户。
                :type LoginSettings: :class:`tcecloud.bms.v20180813.models.LoginSettings`
                :param RaidType: raid类型
                :type RaidType: str
                :param HostName: 云服务器的主机名。<br><li>点号（.）和短横线（-）不能作为 HostName 的首尾字符，不能连续使用。<br><li>Windows 实例：名字符长度为[2, 15]，允许字母（不限制大小写）、数字和短横线（-）组成，不支持点号（.），不能全是数字。<br><li>其他类型（Linux 等）实例：字符长度为[2, 30]，允许支持多个点号，点之间为一段，每段允许字母（不限制大小写）、数字和短横线（-）组成。
                :type HostName: str
                :param ClientToken: 用于保证请求幂等性的字符串。该字符串由客户生成，需保证不同请求之间唯一，最大值不超过64个ASCII字符。若不指定该参数，则无法保证请求的幂等性。<br>更多详细信息请参阅：如何保证幂等性。
                :type ClientToken: str
                :param InternetAccessible: 公网带宽相关信息设置。若不指定该参数，则默认公网带宽为0Mbps。
                :type InternetAccessible: :class:`tcecloud.bms.v20180813.models.InternetAccessible`
                :param InstanceCount: 实例数量。
                :type InstanceCount: int
                :param InstanceName: 实例显示名称。<br><li>不指定实例显示名称则默认显示‘未命名’。</li><li>购买多台实例，如果指定模式串`{R:x}`，表示生成数字`[x, x+n-1]`，其中`n`表示购买实例的数量，例如`server_{R:3}`，购买1台时，实例显示名称为`server_3`；购买2台时，实例显示名称分别为`server_3`，`server_4`。支持指定多个模式串`{R:x}`。</li><li>购买多台实例，如果不指定模式串，则在实例显示名称添加后缀`1、2...n`，其中`n`表示购买实例的数量，例如`server_`，购买2台时，实例显示名称分别为`server_1`，`server_2`。
                :type InstanceName: str
                :param EnhancedService: 增强服务。通过该参数可以指定是否开启云安全、云监控等服务。若不指定该参数，则默认开启云监控、云安全服务。
                :type EnhancedService: :class:`tcecloud.bms.v20180813.models.EnhancedService`
                :param UserData: 提供给实例使用的用户数据，需要以 base64 方式编码，支持的最大数据大小为 16KB。关于获取此参数的详细介绍，请参阅[Windows](https://cloud.tencent.com/document/product/213/17526
        )和Linux启动时运行命令。
                :type UserData: str
                :param ActionTimer: 定时任务。通过该参数可以为实例指定定时任务，目前仅支持定时销毁。
                :type ActionTimer: :class:`tcecloud.bms.v20180813.models.ActionTimer`
                :param TagSpecification: 标签描述列表。通过指定该参数可以同时绑定标签到相应的资源实例，当前仅支持绑定标签到云主机实例。
                :type TagSpecification: :class:`tcecloud.bms.v20180813.models.TagSpecification`
        """
        self.Placement = None
        self.FlavorId = None
        self.OperatingSystemType = None
        self.OperatingSystem = None
        self.VirtualPrivateCloud = None
        self.LoginSettings = None
        self.RaidType = None
        self.HostName = None
        self.ClientToken = None
        self.InternetAccessible = None
        self.InstanceCount = None
        self.InstanceName = None
        self.EnhancedService = None
        self.UserData = None
        self.ActionTimer = None
        self.TagSpecification = None

    def _deserialize(self, params):
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        self.FlavorId = params.get("FlavorId")
        self.OperatingSystemType = params.get("OperatingSystemType")
        self.OperatingSystem = params.get("OperatingSystem")
        if params.get("VirtualPrivateCloud") is not None:
            self.VirtualPrivateCloud = VirtualPrivateCloud()
            self.VirtualPrivateCloud._deserialize(params.get("VirtualPrivateCloud"))
        if params.get("LoginSettings") is not None:
            self.LoginSettings = LoginSettings()
            self.LoginSettings._deserialize(params.get("LoginSettings"))
        self.RaidType = params.get("RaidType")
        self.HostName = params.get("HostName")
        self.ClientToken = params.get("ClientToken")
        if params.get("InternetAccessible") is not None:
            self.InternetAccessible = InternetAccessible()
            self.InternetAccessible._deserialize(params.get("InternetAccessible"))
        self.InstanceCount = params.get("InstanceCount")
        self.InstanceName = params.get("InstanceName")
        if params.get("EnhancedService") is not None:
            self.EnhancedService = EnhancedService()
            self.EnhancedService._deserialize(params.get("EnhancedService"))
        self.UserData = params.get("UserData")
        if params.get("ActionTimer") is not None:
            self.ActionTimer = ActionTimer()
            self.ActionTimer._deserialize(params.get("ActionTimer"))
        if params.get("TagSpecification") is not None:
            self.TagSpecification = TagSpecification()
            self.TagSpecification._deserialize(params.get("TagSpecification"))


class RunInstancesResponse(AbstractModel):
    """RunInstances返回参数结构体"""

    def __init__(self):
        """
        :param TaskId: 返回改任务的taskid,可通过taskid查询任务运行情况
        :type TaskId: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


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
        :param TaskId: 返回任务的taskid,可通过taskid查询任务运行情况
        :type TaskId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class StopInstancesRequest(AbstractModel):
    """StopInstances请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 一个或多个待操作的实例ID。可通过`DescribeInstances`接口返回值中的`InstanceId`获取。每次请求批量实例的上限为100。
        :type InstanceIds: list of str
        """
        self.InstanceIds = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")


class StopInstancesResponse(AbstractModel):
    """StopInstances返回参数结构体"""

    def __init__(self):
        """
        :param TaskId: 返回任务的taskid,可通过taskid查询任务运行情况
        :type TaskId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


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
        :param TaskId: 返回任务的taskid,可通过taskid查询任务运行情况
        :type TaskId: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


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
        """
        self.VpcId = None
        self.SubnetId = None
        self.AsVpcGateway = None
        self.PrivateIpAddresses = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.AsVpcGateway = params.get("AsVpcGateway")
        self.PrivateIpAddresses = params.get("PrivateIpAddresses")

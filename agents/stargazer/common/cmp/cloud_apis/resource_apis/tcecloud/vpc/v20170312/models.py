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


class AcceptAttachCcnInstancesRequest(AbstractModel):
    """AcceptAttachCcnInstances请求参数结构体"""

    def __init__(self):
        """
        :param CcnId: CCN实例ID。形如：ccn-f49l6u0z。
        :type CcnId: str
        :param Instances: 接受关联实例列表。
        :type Instances: list of CcnInstance
        """
        self.CcnId = None
        self.Instances = None

    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")
        if params.get("Instances") is not None:
            self.Instances = []
            for item in params.get("Instances"):
                obj = CcnInstance()
                obj._deserialize(item)
                self.Instances.append(obj)


class AcceptAttachCcnInstancesResponse(AbstractModel):
    """AcceptAttachCcnInstances返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AccountAttribute(AbstractModel):
    """账户属性对象"""

    def __init__(self):
        """
        :param AttributeName: 属性名
        :type AttributeName: str
        :param AttributeValues: 属性值
        :type AttributeValues: list of str
        """
        self.AttributeName = None
        self.AttributeValues = None

    def _deserialize(self, params):
        self.AttributeName = params.get("AttributeName")
        self.AttributeValues = params.get("AttributeValues")


class AclRuleId(AbstractModel):
    """本端IP转换ACL规则ID复杂类型"""

    def __init__(self):
        """
        :param RuleId: 规则ID
        :type RuleId: int
        """
        self.RuleId = None

    def _deserialize(self, params):
        self.RuleId = params.get("RuleId")


class AclRuleIdType(AbstractModel):
    """本端IP转换ACL规则ID复杂类型"""

    def __init__(self):
        """
        :param AclRuleId: 规则ID
        :type AclRuleId: int
        """
        self.AclRuleId = None

    def _deserialize(self, params):
        self.AclRuleId = params.get("AclRuleId")


class AddBandwidthPackageResourcesRequest(AbstractModel):
    """AddBandwidthPackageResources请求参数结构体"""

    def __init__(self):
        """
        :param ResourceIds: 资源唯一ID，当前支持EIP资源和LB资源，形如'eip-xxxx', 'lb-xxxx'
        :type ResourceIds: list of str
        :param BandwidthPackageId: 带宽包唯一标识ID，形如'bwp-xxxx'
        :type BandwidthPackageId: str
        :param NetworkType: 带宽包类型，当前支持'BGP'类型，表示内部资源是BGP IP。
        :type NetworkType: str
        :param ResourceType: 资源类型，包括'Address', 'LoadBalance'
        :type ResourceType: str
        :param Protocol: 带宽包协议类型。当前支持'ipv4'和'ipv6'协议类型。
        :type Protocol: str
        """
        self.ResourceIds = None
        self.BandwidthPackageId = None
        self.NetworkType = None
        self.ResourceType = None
        self.Protocol = None

    def _deserialize(self, params):
        self.ResourceIds = params.get("ResourceIds")
        self.BandwidthPackageId = params.get("BandwidthPackageId")
        self.NetworkType = params.get("NetworkType")
        self.ResourceType = params.get("ResourceType")
        self.Protocol = params.get("Protocol")


class AddBandwidthPackageResourcesResponse(AbstractModel):
    """AddBandwidthPackageResources返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AddIp6RulesRequest(AbstractModel):
    """AddIp6Rules请求参数结构体"""

    def __init__(self):
        """
        :param Ip6TranslatorId: IPV6转换实例唯一ID，形如ip6-xxxxxxxx
        :type Ip6TranslatorId: str
        :param Ip6RuleInfos: IPV6转换规则信息
        :type Ip6RuleInfos: list of Ip6RuleInfo
        :param Ip6RuleName: IPV6转换规则名称
        :type Ip6RuleName: str
        """
        self.Ip6TranslatorId = None
        self.Ip6RuleInfos = None
        self.Ip6RuleName = None

    def _deserialize(self, params):
        self.Ip6TranslatorId = params.get("Ip6TranslatorId")
        if params.get("Ip6RuleInfos") is not None:
            self.Ip6RuleInfos = []
            for item in params.get("Ip6RuleInfos"):
                obj = Ip6RuleInfo()
                obj._deserialize(item)
                self.Ip6RuleInfos.append(obj)
        self.Ip6RuleName = params.get("Ip6RuleName")


class AddIp6RulesResponse(AbstractModel):
    """AddIp6Rules返回参数结构体"""

    def __init__(self):
        """
        :param Ip6RuleSet: IPV6转换规则唯一ID数组，形如rule6-xxxxxxxx
        :type Ip6RuleSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Ip6RuleSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Ip6RuleSet = params.get("Ip6RuleSet")
        self.RequestId = params.get("RequestId")


class Address(AbstractModel):
    """描述 EIP 信息"""

    def __init__(self):
        """
        :param AddressId: `EIP`的`ID`，是`EIP`的唯一标识。
        :type AddressId: str
        :param AddressName: `EIP`名称。
        :type AddressName: str
        :param AddressStatus: `EIP`状态，包含'CREATING'(创建中),'BINDING'(绑定中),'BIND'(已绑定),'UNBINDING'(解绑中),'UNBIND'(已解绑),'OFFLINING'(释放中),'BIND_ENI'(绑定悬空弹性网卡)
        :type AddressStatus: str
        :param AddressIp: 外网IP地址
        :type AddressIp: str
        :param InstanceId: 绑定的资源实例`ID`。可能是一个`CVM`，`NAT`。
        :type InstanceId: str
        :param CreatedTime: 创建时间。按照`ISO8601`标准表示，并且使用`UTC`时间。格式为：`YYYY-MM-DDThh:mm:ssZ`。
        :type CreatedTime: str
        :param NetworkInterfaceId: 绑定的弹性网卡ID
        :type NetworkInterfaceId: str
        :param PrivateAddressIp: 绑定的资源内网ip
        :type PrivateAddressIp: str
        :param IsArrears: 资源隔离状态。true表示eip处于隔离状态，false表示资源处于未隔离状态
        :type IsArrears: bool
        :param Bandwidth: 带宽
        :type Bandwidth: integer
        :param PayMode: 付费模式
        :type PayMode: str
        :param IsBlocked: 资源封堵状态。true表示eip处于封堵状态，false表示eip处于未封堵状态
        :type IsBlocked: bool
        :param IsEipDirectConnection: eip是否支持直通模式。true表示eip支持直通模式，false表示资源不支持直通模式
        :type IsEipDirectConnection: bool
        :param AddressType: eip资源类型，包括"CalcIP","WanIP","EIP","AnycastEIP"。其中"CalcIP"表示设备ip，“WanIP”表示普通公网ip，“EIP”表示弹性公网ip，“AnycastEip”表示加速EIP
        :type AddressType: str
        :param CascadeRelease: eip是否在解绑后自动释放。true表示eip将会在解绑后自动释放，false表示eip在解绑后不会自动释放
        :type CascadeRelease: bool
        :param EipAlgType: EIP ALG开启的协议类型。
        :type EipAlgType: :class:`tcecloud.vpc.v20170312.models.AlgType`
        :param InternetServiceProvider: 弹性公网IP的运营商信息，当前可能返回值包括"CMCC","CTCC","CUCC","BGP"
        :type InternetServiceProvider: str
        """
        self.AddressId = None
        self.AddressName = None
        self.AddressStatus = None
        self.AddressIp = None
        self.InstanceId = None
        self.CreatedTime = None
        self.NetworkInterfaceId = None
        self.PrivateAddressIp = None
        self.IsArrears = None
        self.Bandwidth = None
        self.PayMode = None
        self.IsBlocked = None
        self.IsEipDirectConnection = None
        self.AddressType = None
        self.CascadeRelease = None
        self.EipAlgType = None
        self.InternetServiceProvider = None

    def _deserialize(self, params):
        self.AddressId = params.get("AddressId")
        self.AddressName = params.get("AddressName")
        self.AddressStatus = params.get("AddressStatus")
        self.AddressIp = params.get("AddressIp")
        self.InstanceId = params.get("InstanceId")
        self.CreatedTime = params.get("CreatedTime")
        self.NetworkInterfaceId = params.get("NetworkInterfaceId")
        self.PrivateAddressIp = params.get("PrivateAddressIp")
        self.IsArrears = params.get("IsArrears")
        self.Bandwidth = params.get("Bandwidth")
        self.PayMode = params.get("PayMode")
        self.IsBlocked = params.get("IsBlocked")
        self.IsEipDirectConnection = params.get("IsEipDirectConnection")
        self.AddressType = params.get("AddressType")
        self.CascadeRelease = params.get("CascadeRelease")
        if params.get("EipAlgType") is not None:
            self.EipAlgType = AlgType()
            self.EipAlgType._deserialize(params.get("EipAlgType"))
        self.InternetServiceProvider = params.get("InternetServiceProvider")


class AddressBase(AbstractModel):
    """弹性公网IP基础信息"""

    def __init__(self):
        """
        :param InternetServiceProvider: 运营商信息，包括移动，联通，电信，腾讯CAP
        :type InternetServiceProvider: str
        :param SetName: 弹性公网IP集群名称
        :type SetName: str
        :param SetId: 弹性公网IP集群唯一Id
        :type SetId: int
        :param AddressIp: 弹性公网IP地址
        :type AddressIp: str
        :param IsDpdk: 弹性公网IP是否支持DPDK
        :type IsDpdk: bool
        :param Status: 弹性公网IP是否可用
        :type Status: str
        """
        self.InternetServiceProvider = None
        self.SetName = None
        self.SetId = None
        self.AddressIp = None
        self.IsDpdk = None
        self.Status = None

    def _deserialize(self, params):
        self.InternetServiceProvider = params.get("InternetServiceProvider")
        self.SetName = params.get("SetName")
        self.SetId = params.get("SetId")
        self.AddressIp = params.get("AddressIp")
        self.IsDpdk = params.get("IsDpdk")
        self.Status = params.get("Status")


class AddressBasic(AbstractModel):
    """EIP基本信息"""

    def __init__(self):
        """
                :param AddressIp: 外网IP地址
                :type AddressIp: str
                :param AddressId: `EIP`的`ID`，是`EIP`的唯一标识。
                :type AddressId: str
                :param AddressType: eip资源类型，包括"CalcIP","WanIP","EIP","AnycastEIP"。其中"CalcIP"表示设备ip，“WanIP”表示普通公网ip，“EIP”表示弹性公网ip，“AnycastEip”表示加速EIP
                :type AddressType: str
                :param InternetServiceProvider: EIP运营商信息，包括"CMCC","CTCC","CUCC","BGP"，其中"CMCC"表示移动运营商，"CTCC"表示电信运营商，"CUCC"表示联通运营商，"BGP"表示BGP对接运营商
                :type InternetServiceProvider: str
                :param Status: EIP使用状态，"used"表示该ip地址在当前地域已被占用，"unused"表示该ip地址在当前地域未被占用
                :type Status: str
                :param AnycastZone: Anycast 发布域是加速 IP 地址发布的地域，即 Anycast CLB 的 VIP 所发布的 POP 接入点，客户端接入最近的 POP 接入点。目前 Anycast CLB 支持以下发布域：
        发布域 A(ANYCAST_ZONE_A)：主要是中国和欧美地区，VIP 将同时在在北京、上海、广州、中国香港、多伦多、硅谷、法兰克福、弗吉尼亚和莫斯科发布。
        发布域 B(ANYCAST_ZONE_B)：主要是中国和东南亚地区，VIP 将同时在北京、上海、广州、中国香港、新加坡、首尔、孟买、曼谷和东京发布。
                :type AnycastZone: str
        """
        self.AddressIp = None
        self.AddressId = None
        self.AddressType = None
        self.InternetServiceProvider = None
        self.Status = None
        self.AnycastZone = None

    def _deserialize(self, params):
        self.AddressIp = params.get("AddressIp")
        self.AddressId = params.get("AddressId")
        self.AddressType = params.get("AddressType")
        self.InternetServiceProvider = params.get("InternetServiceProvider")
        self.Status = params.get("Status")
        self.AnycastZone = params.get("AnycastZone")


class AddressChangeQuota(AbstractModel):
    """描述实例更换公网IP地址的配额信息"""

    def __init__(self):
        """
        :param QuotaId: 配额名称，取值：INSTANCE_ADDRESS_CHANGE
        :type QuotaId: str
        :param InstanceId: 实例ID
        :type InstanceId: str
        :param QuotaCurrent: 剩余配额
        :type QuotaCurrent: int
        :param QuotaLimit: 配额上限
        :type QuotaLimit: int
        """
        self.QuotaId = None
        self.InstanceId = None
        self.QuotaCurrent = None
        self.QuotaLimit = None

    def _deserialize(self, params):
        self.QuotaId = params.get("QuotaId")
        self.InstanceId = params.get("InstanceId")
        self.QuotaCurrent = params.get("QuotaCurrent")
        self.QuotaLimit = params.get("QuotaLimit")


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


class AddressLibInfo(AbstractModel):
    """IP地址库信息"""

    def __init__(self):
        """
        :param Country: 国家信息
        :type Country: str
        :param Province: 省、州、郡一级行政区域信息
        :type Province: str
        :param City: 市一级行政区域信息
        :type City: str
        :param Region: 市内区域信息
        :type Region: str
        :param Isp: 接入运营商信息
        :type Isp: str
        :param AddressIp: 查询IP地址
        :type AddressIp: str
        :param AsName: 骨干运营商信息
        :type AsName: str
        :param AsId: 运营商As号
        :type AsId: str
        :param Comment: 注释信息。目前的填充值为移动接入用户的APN值，如无APN属性则为空
        :type Comment: str
        :param InternetServiceProvider: 同Isp，废弃
        :type InternetServiceProvider: str
        """
        self.Country = None
        self.Province = None
        self.City = None
        self.Region = None
        self.Isp = None
        self.AddressIp = None
        self.AsName = None
        self.AsId = None
        self.Comment = None
        self.InternetServiceProvider = None

    def _deserialize(self, params):
        self.Country = params.get("Country")
        self.Province = params.get("Province")
        self.City = params.get("City")
        self.Region = params.get("Region")
        self.Isp = params.get("Isp")
        self.AddressIp = params.get("AddressIp")
        self.AsName = params.get("AsName")
        self.AsId = params.get("AsId")
        self.Comment = params.get("Comment")
        self.InternetServiceProvider = params.get("InternetServiceProvider")


class AddressTemplate(AbstractModel):
    """IP地址模板"""

    def __init__(self):
        """
        :param AddressTemplateName: IP地址模板名称。
        :type AddressTemplateName: str
        :param AddressTemplateId: IP地址模板实例唯一ID。
        :type AddressTemplateId: str
        :param AddressSet: IP地址信息。
        :type AddressSet: list of str
        :param CreatedTime: 创建时间。
        :type CreatedTime: str
        """
        self.AddressTemplateName = None
        self.AddressTemplateId = None
        self.AddressSet = None
        self.CreatedTime = None

    def _deserialize(self, params):
        self.AddressTemplateName = params.get("AddressTemplateName")
        self.AddressTemplateId = params.get("AddressTemplateId")
        self.AddressSet = params.get("AddressSet")
        self.CreatedTime = params.get("CreatedTime")


class AddressTemplateGroup(AbstractModel):
    """IP地址模板集合"""

    def __init__(self):
        """
        :param AddressTemplateGroupName: IP地址模板集合名称。
        :type AddressTemplateGroupName: str
        :param AddressTemplateGroupId: IP地址模板集合实例ID，例如：ipmg-dih8xdbq。
        :type AddressTemplateGroupId: str
        :param AddressTemplateIdSet: IP地址模板ID。
        :type AddressTemplateIdSet: list of str
        :param CreatedTime: 创建时间。
        :type CreatedTime: str
        :param AddressTemplateSet: IP地址模板实例。
        :type AddressTemplateSet: list of AddressTemplateItem
        """
        self.AddressTemplateGroupName = None
        self.AddressTemplateGroupId = None
        self.AddressTemplateIdSet = None
        self.CreatedTime = None
        self.AddressTemplateSet = None

    def _deserialize(self, params):
        self.AddressTemplateGroupName = params.get("AddressTemplateGroupName")
        self.AddressTemplateGroupId = params.get("AddressTemplateGroupId")
        self.AddressTemplateIdSet = params.get("AddressTemplateIdSet")
        self.CreatedTime = params.get("CreatedTime")
        if params.get("AddressTemplateSet") is not None:
            self.AddressTemplateSet = []
            for item in params.get("AddressTemplateSet"):
                obj = AddressTemplateItem()
                obj._deserialize(item)
                self.AddressTemplateSet.append(obj)


class AddressTemplateItem(AbstractModel):
    """地址信息"""

    def __init__(self):
        """
        :param From: 起始地址。
        :type From: str
        :param To: 结束地址。
        :type To: str
        """
        self.From = None
        self.To = None

    def _deserialize(self, params):
        self.From = params.get("From")
        self.To = params.get("To")


class AddressTemplateSpecification(AbstractModel):
    """IP地址模版"""

    def __init__(self):
        """
        :param AddressId: IP地址ID，例如：ipm-2uw6ujo6。
        :type AddressId: str
        :param AddressGroupId: IP地址组ID，例如：ipmg-2uw6ujo6。
        :type AddressGroupId: str
        """
        self.AddressId = None
        self.AddressGroupId = None

    def _deserialize(self, params):
        self.AddressId = params.get("AddressId")
        self.AddressGroupId = params.get("AddressGroupId")


class AdjustPublicAddressRequest(AbstractModel):
    """AdjustPublicAddress请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 需要更换公网IP的实例ID
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class AdjustPublicAddressResponse(AbstractModel):
    """AdjustPublicAddress返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AlgType(AbstractModel):
    """ALG协议类型"""

    def __init__(self):
        """
        :param Ftp: Ftp协议Alg功能是否开启
        :type Ftp: bool
        :param Sip: Sip协议Alg功能是否开启
        :type Sip: bool
        """
        self.Ftp = None
        self.Sip = None

    def _deserialize(self, params):
        self.Ftp = params.get("Ftp")
        self.Sip = params.get("Sip")


class AllocateAddressesRequest(AbstractModel):
    """AllocateAddresses请求参数结构体"""

    def __init__(self):
        """
                :param AddressCount: EIP数量。默认值：1。
                :type AddressCount: int
                :param InternetServiceProvider: EIP线路类型。默认值：BGP。
        <ul style="margin:0"><li>已开通静态单线IP白名单的用户，可选值：<ul><li>CMCC：中国移动</li>
        <li>CTCC：中国电信</li>
        <li>CUCC：中国联通</li></ul>注意：仅部分地域支持静态单线IP。</li></ul>
                :type InternetServiceProvider: str
                :param TgwGroup: 内部参数，用于指定集群申请EIP。
                :type TgwGroup: str
                :param ApplySilence: 内部参数。
                :type ApplySilence: int
                :param InternetChargeType: EIP计费方式。
        <ul style="margin:0"><li>已开通带宽上移白名单的用户，可选值：<ul><li>BANDWIDTH_PACKAGE：共享带宽包付费（需额外开通共享带宽包白名单）</li>
        <li>BANDWIDTH_POSTPAID_BY_HOUR：带宽按小时后付费</li>
        <li>TRAFFIC_POSTPAID_BY_HOUR：流量按小时后付费</li></ul>默认值：TRAFFIC_POSTPAID_BY_HOUR。</li>
        <li>未开通带宽上移白名单的用户，EIP计费方式与其绑定的实例的计费方式一致，无需传递此参数。</li></ul>
                :type InternetChargeType: str
                :param InternetMaxBandwidthOut: EIP出带宽上限，单位：Mbps。
        <ul style="margin:0"><li>已开通带宽上移白名单的用户，可选值范围取决于EIP计费方式：<ul><li>BANDWIDTH_PACKAGE：1 Mbps 至 1000 Mbps</li>
        <li>BANDWIDTH_POSTPAID_BY_HOUR：1 Mbps 至 100 Mbps</li>
        <li>TRAFFIC_POSTPAID_BY_HOUR：1 Mbps 至 100 Mbps</li></ul>默认值：1 Mbps。</li>
        <li>未开通带宽上移白名单的用户，EIP出带宽上限取决于与其绑定的实例的公网出带宽上限，无需传递此参数。</li></ul>
                :type InternetMaxBandwidthOut: int
                :param AddressChargePrepaid: 计费周期，预付费需要传递。
                :type AddressChargePrepaid: :class:`tcecloud.vpc.v20170312.models.AddressChargePrepaid`
                :param DealId: 订单ID，内部参数。
                :type DealId: str
                :param AddressType: EIP类型。默认值：EIP。
        <ul style="margin:0"><li>已开通Anycast公网加速白名单的用户，可选值：<ul><li>AnycastEIP：加速IP，可参见 Anycast 公网加速</li></ul>注意：仅部分地域支持加速IP。</li></ul>
                :type AddressType: str
                :param AnycastZone: Anycast发布域。
        <ul style="margin:0"><li>已开通Anycast公网加速白名单的用户，可选值：<ul><li>ANYCAST_ZONE_GLOBAL：全球发布域（需要额外开通Anycast全球加速白名单）</li><li>ANYCAST_ZONE_OVERSEAS：境外发布域</li><li><b>[已废弃]</b> ANYCAST_ZONE_A：发布域A（已更新为全球发布域）</li><li><b>[已废弃]</b> ANYCAST_ZONE_B：发布域B（已更新为全球发布域）</li></ul>默认值：ANYCAST_ZONE_OVERSEAS。</li></ul>
                :type AnycastZone: str
                :param Zone: EIP可用区，用于指定可用区申请EIP。
                :type Zone: str
                :param VipCluster: 指定IP地址申请EIP，每个账户每个月只有三次配额
                :type VipCluster: list of str
                :param VipSet: [Deprecated] 该字段无实际功能，废弃
                :type VipSet: list of str
                :param ApplicableForCLB: <b>[已废弃]</b> AnycastEIP不再区分是否负载均衡。原参数说明如下：
        AnycastEIP是否用于绑定负载均衡。
        <ul style="margin:0"><li>已开通Anycast公网加速白名单的用户，可选值：<ul><li>TRUE：AnycastEIP可绑定对象为负载均衡</li>
        <li>FALSE：AnycastEIP可绑定对象为云服务器、NAT网关、高可用虚拟IP等</li></ul>默认值：FALSE。</li></ul>
                :type ApplicableForCLB: bool
                :param Tags: 需要关联的标签列表。
                :type Tags: list of Tag
                :param SetId: TGW集群ID，用于指定集群ID申请弹性公网IP。注意，anycast EIP不支持指定集群ID申请，静态单线EIP指定集群ID申请时，InternetServiceProvider参数必须和集群ID的运营商属性一致。
                :type SetId: int
                :param Restrictive: 是否是本地带宽IP。默认值：否
                :type Restrictive: bool
                :param BandwidthPackageId: BGP带宽包唯一ID参数。设定该参数且InternetChargeType为BANDWIDTH_PACKAGE，则表示创建的EIP加入该BGP带宽包并采用带宽包计费
                :type BandwidthPackageId: str
        """
        self.AddressCount = None
        self.InternetServiceProvider = None
        self.TgwGroup = None
        self.ApplySilence = None
        self.InternetChargeType = None
        self.InternetMaxBandwidthOut = None
        self.AddressChargePrepaid = None
        self.DealId = None
        self.AddressType = None
        self.AnycastZone = None
        self.Zone = None
        self.VipCluster = None
        self.VipSet = None
        self.ApplicableForCLB = None
        self.Tags = None
        self.SetId = None
        self.Restrictive = None
        self.BandwidthPackageId = None

    def _deserialize(self, params):
        self.AddressCount = params.get("AddressCount")
        self.InternetServiceProvider = params.get("InternetServiceProvider")
        self.TgwGroup = params.get("TgwGroup")
        self.ApplySilence = params.get("ApplySilence")
        self.InternetChargeType = params.get("InternetChargeType")
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        if params.get("AddressChargePrepaid") is not None:
            self.AddressChargePrepaid = AddressChargePrepaid()
            self.AddressChargePrepaid._deserialize(params.get("AddressChargePrepaid"))
        self.DealId = params.get("DealId")
        self.AddressType = params.get("AddressType")
        self.AnycastZone = params.get("AnycastZone")
        self.Zone = params.get("Zone")
        self.VipCluster = params.get("VipCluster")
        self.VipSet = params.get("VipSet")
        self.ApplicableForCLB = params.get("ApplicableForCLB")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.SetId = params.get("SetId")
        self.Restrictive = params.get("Restrictive")
        self.BandwidthPackageId = params.get("BandwidthPackageId")


class AllocateAddressesResponse(AbstractModel):
    """AllocateAddresses返回参数结构体"""

    def __init__(self):
        """
        :param AddressSet: 申请到的 EIP 的唯一 ID 列表。
        :type AddressSet: list of str
        :param TaskId: 异步任务TaskId。可以使用DescribeTaskResult接口查询任务状态。
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AddressSet = None
        self.TaskId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.AddressSet = params.get("AddressSet")
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class AllocateIp6AddressesBandwidthRequest(AbstractModel):
    """AllocateIp6AddressesBandwidth请求参数结构体"""

    def __init__(self):
        """
        :param Ip6Addresses: 需要开通公网访问能力的IPV6地址
        :type Ip6Addresses: list of str
        :param InternetMaxBandwidthOut: 带宽，单位Mbps。默认是1Mbps
        :type InternetMaxBandwidthOut: int
        :param InternetChargeType: 网络计费模式。IPV6当前支持"TRAFFIC_POSTPAID_BY_HOUR"，默认是"TRAFFIC_POSTPAID_BY_HOUR"。
        :type InternetChargeType: str
        """
        self.Ip6Addresses = None
        self.InternetMaxBandwidthOut = None
        self.InternetChargeType = None

    def _deserialize(self, params):
        self.Ip6Addresses = params.get("Ip6Addresses")
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        self.InternetChargeType = params.get("InternetChargeType")


class AllocateIp6AddressesBandwidthResponse(AbstractModel):
    """AllocateIp6AddressesBandwidth返回参数结构体"""

    def __init__(self):
        """
        :param AddressSet: 弹性公网 IPV6 的唯一 ID 列表。
        :type AddressSet: list of str
        :param TaskId: 异步任务TaskId。可以使用DescribeTaskResult接口查询任务状态。
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AddressSet = None
        self.TaskId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.AddressSet = params.get("AddressSet")
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class AnycastRegionInfo(AbstractModel):
    """支持AnycastEIP的地域的信息"""

    def __init__(self):
        """
        :param Region: 地域
        :type Region: str
        :param RegionName: 地域中文名称
        :type RegionName: str
        :param RegionState: 地域当前状态
        :type RegionState: str
        :param AnycastZone: AnycastEIP发布域
        :type AnycastZone: str
        """
        self.Region = None
        self.RegionName = None
        self.RegionState = None
        self.AnycastZone = None

    def _deserialize(self, params):
        self.Region = params.get("Region")
        self.RegionName = params.get("RegionName")
        self.RegionState = params.get("RegionState")
        self.AnycastZone = params.get("AnycastZone")


class AssignIpv6AddressesRequest(AbstractModel):
    """AssignIpv6Addresses请求参数结构体"""

    def __init__(self):
        """
        :param NetworkInterfaceId: 弹性网卡实例`ID`，形如：`eni-m6dyj72l`。
        :type NetworkInterfaceId: str
        :param Ipv6Addresses: 指定的`IPv6`地址列表，单次最多指定10个。与入参`Ipv6AddressCount`合并计算配额。与Ipv6AddressCount必填一个。
        :type Ipv6Addresses: list of Ipv6Address
        :param Ipv6AddressCount: 自动分配`IPv6`地址个数，内网IP地址个数总和不能超过配数。与入参`Ipv6Addresses`合并计算配额。与Ipv6Addresses必填一个。
        :type Ipv6AddressCount: int
        """
        self.NetworkInterfaceId = None
        self.Ipv6Addresses = None
        self.Ipv6AddressCount = None

    def _deserialize(self, params):
        self.NetworkInterfaceId = params.get("NetworkInterfaceId")
        if params.get("Ipv6Addresses") is not None:
            self.Ipv6Addresses = []
            for item in params.get("Ipv6Addresses"):
                obj = Ipv6Address()
                obj._deserialize(item)
                self.Ipv6Addresses.append(obj)
        self.Ipv6AddressCount = params.get("Ipv6AddressCount")


class AssignIpv6AddressesResponse(AbstractModel):
    """AssignIpv6Addresses返回参数结构体"""

    def __init__(self):
        """
        :param Ipv6AddressSet: 分配给弹性网卡的`IPv6`地址列表。
        :type Ipv6AddressSet: list of Ipv6Address
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Ipv6AddressSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Ipv6AddressSet") is not None:
            self.Ipv6AddressSet = []
            for item in params.get("Ipv6AddressSet"):
                obj = Ipv6Address()
                obj._deserialize(item)
                self.Ipv6AddressSet.append(obj)
        self.RequestId = params.get("RequestId")


class AssignIpv6CidrBlockRequest(AbstractModel):
    """AssignIpv6CidrBlock请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: `VPC`实例`ID`，形如：`vpc-f49l6u0z`。
        :type VpcId: str
        """
        self.VpcId = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")


class AssignIpv6CidrBlockResponse(AbstractModel):
    """AssignIpv6CidrBlock返回参数结构体"""

    def __init__(self):
        """
        :param Ipv6CidrBlock: 分配的 `IPv6` 网段。形如：`3402:4e00:20:1000::/56`
        :type Ipv6CidrBlock: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Ipv6CidrBlock = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Ipv6CidrBlock = params.get("Ipv6CidrBlock")
        self.RequestId = params.get("RequestId")


class AssignIpv6SubnetCidrBlockRequest(AbstractModel):
    """AssignIpv6SubnetCidrBlock请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: 子网所在私有网络`ID`。形如：`vpc-f49l6u0z`。
        :type VpcId: str
        :param Ipv6SubnetCidrBlocks: 分配 `IPv6` 子网段列表。
        :type Ipv6SubnetCidrBlocks: list of Ipv6SubnetCidrBlock
        """
        self.VpcId = None
        self.Ipv6SubnetCidrBlocks = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        if params.get("Ipv6SubnetCidrBlocks") is not None:
            self.Ipv6SubnetCidrBlocks = []
            for item in params.get("Ipv6SubnetCidrBlocks"):
                obj = Ipv6SubnetCidrBlock()
                obj._deserialize(item)
                self.Ipv6SubnetCidrBlocks.append(obj)


class AssignIpv6SubnetCidrBlockResponse(AbstractModel):
    """AssignIpv6SubnetCidrBlock返回参数结构体"""

    def __init__(self):
        """
        :param Ipv6SubnetCidrBlockSet: 分配 `IPv6` 子网段列表。
        :type Ipv6SubnetCidrBlockSet: list of Ipv6SubnetCidrBlock
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Ipv6SubnetCidrBlockSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Ipv6SubnetCidrBlockSet") is not None:
            self.Ipv6SubnetCidrBlockSet = []
            for item in params.get("Ipv6SubnetCidrBlockSet"):
                obj = Ipv6SubnetCidrBlock()
                obj._deserialize(item)
                self.Ipv6SubnetCidrBlockSet.append(obj)
        self.RequestId = params.get("RequestId")


class AssignPrivateIpAddressesRequest(AbstractModel):
    """AssignPrivateIpAddresses请求参数结构体"""

    def __init__(self):
        """
        :param NetworkInterfaceId: 弹性网卡实例ID，例如：eni-m6dyj72l。
        :type NetworkInterfaceId: str
        :param PrivateIpAddresses: 指定的内网IP信息，单次最多指定10个。与SecondaryPrivateIpAddressCount至少提供一个。
        :type PrivateIpAddresses: list of PrivateIpAddressSpecification
        :param SecondaryPrivateIpAddressCount: 新申请的内网IP地址个数，与PrivateIpAddresses至少提供一个。内网IP地址个数总和不能超过配额数，详见弹性网卡使用限制。
        :type SecondaryPrivateIpAddressCount: int
        """
        self.NetworkInterfaceId = None
        self.PrivateIpAddresses = None
        self.SecondaryPrivateIpAddressCount = None

    def _deserialize(self, params):
        self.NetworkInterfaceId = params.get("NetworkInterfaceId")
        if params.get("PrivateIpAddresses") is not None:
            self.PrivateIpAddresses = []
            for item in params.get("PrivateIpAddresses"):
                obj = PrivateIpAddressSpecification()
                obj._deserialize(item)
                self.PrivateIpAddresses.append(obj)
        self.SecondaryPrivateIpAddressCount = params.get("SecondaryPrivateIpAddressCount")


class AssignPrivateIpAddressesResponse(AbstractModel):
    """AssignPrivateIpAddresses返回参数结构体"""

    def __init__(self):
        """
        :param PrivateIpAddressSet: 内网IP详细信息。
        :type PrivateIpAddressSet: list of PrivateIpAddressSpecification
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.PrivateIpAddressSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("PrivateIpAddressSet") is not None:
            self.PrivateIpAddressSet = []
            for item in params.get("PrivateIpAddressSet"):
                obj = PrivateIpAddressSpecification()
                obj._deserialize(item)
                self.PrivateIpAddressSet.append(obj)
        self.RequestId = params.get("RequestId")


class AssistantCidr(AbstractModel):
    """VPC辅助CIDR信息。"""

    def __init__(self):
        """
                :param VpcId: `VPC`实例`ID`。形如：`vpc-6v2ht8q5`
                :type VpcId: str
                :param CidrBlock: 辅助CIDR。形如：`172.16.0.0/16`
                :type CidrBlock: str
                :param AssistantType: 辅助CIDR类型（0：普通辅助CIDR，1：容器辅助CIDR），默认都是0。
                :type AssistantType: int
                :param SubnetSet: 辅助CIDR拆分的子网。
        注意：此字段可能返回 null，表示取不到有效值。
                :type SubnetSet: list of Subnet
        """
        self.VpcId = None
        self.CidrBlock = None
        self.AssistantType = None
        self.SubnetSet = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.CidrBlock = params.get("CidrBlock")
        self.AssistantType = params.get("AssistantType")
        if params.get("SubnetSet") is not None:
            self.SubnetSet = []
            for item in params.get("SubnetSet"):
                obj = Subnet()
                obj._deserialize(item)
                self.SubnetSet.append(obj)


class AssociateAddressRequest(AbstractModel):
    """AssociateAddress请求参数结构体"""

    def __init__(self):
        """
        :param AddressId: 标识 EIP 的唯一 ID。EIP 唯一 ID 形如：`eip-11112222`。
        :type AddressId: str
        :param InstanceId: 要绑定的实例 ID。实例 ID 形如：`ins-11112222`。可通过登录控制台查询，也可通过 DescribeInstances 接口返回值中的`InstanceId`获取。
        :type InstanceId: str
        :param NetworkInterfaceId: 要绑定的弹性网卡 ID。 弹性网卡 ID 形如：`eni-11112222`。`NetworkInterfaceId` 与 `InstanceId` 不可同时指定。弹性网卡 ID 可通过登录控制台查询，也可通过DescribeNetworkInterfaces接口返回值中的`networkInterfaceId`获取。
        :type NetworkInterfaceId: str
        :param PrivateIpAddress: 要绑定的内网 IP。如果指定了 `NetworkInterfaceId` 则也必须指定 `PrivateIpAddress` ，表示将 EIP 绑定到指定弹性网卡的指定内网 IP 上。同时要确保指定的 `PrivateIpAddress` 是指定的 `NetworkInterfaceId` 上的一个内网 IP。指定弹性网卡的内网 IP 可通过登录控制台查询，也可通过DescribeNetworkInterfaces接口返回值中的`privateIpAddress`获取。
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
        :param TaskId: 异步任务TaskId。可以使用DescribeTaskResult接口查询任务状态。
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class AssociateNatGatewayAddressRequest(AbstractModel):
    """AssociateNatGatewayAddress请求参数结构体"""

    def __init__(self):
        """
        :param NatGatewayId: NAT网关的ID，形如：`nat-df45454`。
        :type NatGatewayId: str
        :param AddressCount: 需要申请的弹性IP个数，系统会按您的要求生产N个弹性IP, 其中AddressCount和PublicAddresses至少传递一个。
        :type AddressCount: int
        :param PublicIpAddresses: 绑定NAT网关的弹性IP数组，其中AddressCount和PublicAddresses至少传递一个。。
        :type PublicIpAddresses: list of str
        :param Zone: 弹性IP可以区，自动分配弹性IP时传递。
        :type Zone: str
        """
        self.NatGatewayId = None
        self.AddressCount = None
        self.PublicIpAddresses = None
        self.Zone = None

    def _deserialize(self, params):
        self.NatGatewayId = params.get("NatGatewayId")
        self.AddressCount = params.get("AddressCount")
        self.PublicIpAddresses = params.get("PublicIpAddresses")
        self.Zone = params.get("Zone")


class AssociateNatGatewayAddressResponse(AbstractModel):
    """AssociateNatGatewayAddress返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AssociateNetworkAclSubnetsRequest(AbstractModel):
    """AssociateNetworkAclSubnets请求参数结构体"""

    def __init__(self):
        """
        :param NetworkAclId: 网络ACL实例ID。例如：acl-12345678。
        :type NetworkAclId: str
        :param SubnetIds: 子网实例ID数组。例如：[subnet-12345678]
        :type SubnetIds: list of str
        """
        self.NetworkAclId = None
        self.SubnetIds = None

    def _deserialize(self, params):
        self.NetworkAclId = params.get("NetworkAclId")
        self.SubnetIds = params.get("SubnetIds")


class AssociateNetworkAclSubnetsResponse(AbstractModel):
    """AssociateNetworkAclSubnets返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AssociateNetworkInterfaceSecurityGroupsRequest(AbstractModel):
    """AssociateNetworkInterfaceSecurityGroups请求参数结构体"""

    def __init__(self):
        """
        :param NetworkInterfaceIds: 弹性网卡实例ID。形如：eni-pxir56ns。每次请求的实例的上限为100。
        :type NetworkInterfaceIds: list of str
        :param SecurityGroupIds: 安全组实例ID，例如：sg-33ocnj9n，可通过DescribeSecurityGroups获取。每次请求的实例的上限为100。
        :type SecurityGroupIds: list of str
        """
        self.NetworkInterfaceIds = None
        self.SecurityGroupIds = None

    def _deserialize(self, params):
        self.NetworkInterfaceIds = params.get("NetworkInterfaceIds")
        self.SecurityGroupIds = params.get("SecurityGroupIds")


class AssociateNetworkInterfaceSecurityGroupsResponse(AbstractModel):
    """AssociateNetworkInterfaceSecurityGroups返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AttachCcnInstancesRequest(AbstractModel):
    """AttachCcnInstances请求参数结构体"""

    def __init__(self):
        """
        :param CcnId: CCN实例ID。形如：ccn-f49l6u0z。
        :type CcnId: str
        :param Instances: 关联网络实例列表
        :type Instances: list of CcnInstance
        :param CcnUin: CCN所属UIN（根账号），默认当前账号所属UIN
        :type CcnUin: str
        """
        self.CcnId = None
        self.Instances = None
        self.CcnUin = None

    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")
        if params.get("Instances") is not None:
            self.Instances = []
            for item in params.get("Instances"):
                obj = CcnInstance()
                obj._deserialize(item)
                self.Instances.append(obj)
        self.CcnUin = params.get("CcnUin")


class AttachCcnInstancesResponse(AbstractModel):
    """AttachCcnInstances返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AttachClassicLinkVpcRequest(AbstractModel):
    """AttachClassicLinkVpc请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: VPC实例ID
        :type VpcId: str
        :param InstanceIds: CVM实例ID
        :type InstanceIds: list of str
        """
        self.VpcId = None
        self.InstanceIds = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.InstanceIds = params.get("InstanceIds")


class AttachClassicLinkVpcResponse(AbstractModel):
    """AttachClassicLinkVpc返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AttachNetworkInterfaceRequest(AbstractModel):
    """AttachNetworkInterface请求参数结构体"""

    def __init__(self):
        """
        :param NetworkInterfaceId: 弹性网卡实例ID，例如：eni-m6dyj72l。
        :type NetworkInterfaceId: str
        :param InstanceId: CVM实例ID。形如：ins-r8hr2upy。
        :type InstanceId: str
        """
        self.NetworkInterfaceId = None
        self.InstanceId = None

    def _deserialize(self, params):
        self.NetworkInterfaceId = params.get("NetworkInterfaceId")
        self.InstanceId = params.get("InstanceId")


class AttachNetworkInterfaceResponse(AbstractModel):
    """AttachNetworkInterface返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AvailableZone(AbstractModel):
    """可用区属性"""

    def __init__(self):
        """
        :param Zone: 可用区ID，如：ap-guangzhou-2。
        :type Zone: str
        :param ZoneId: 可用区数字ID。
        :type ZoneId: int
        :param Name: 可用区名称，如：广州二区。
        :type Name: str
        :param Products: 可用网络产品列表。
        :type Products: list of str
        :param WhiteListKey: 白名单`key`列表。
        :type WhiteListKey: list of str
        """
        self.Zone = None
        self.ZoneId = None
        self.Name = None
        self.Products = None
        self.WhiteListKey = None

    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.ZoneId = params.get("ZoneId")
        self.Name = params.get("Name")
        self.Products = params.get("Products")
        self.WhiteListKey = params.get("WhiteListKey")


class BandwidthAttribute(AbstractModel):
    """带宽属性"""

    def __init__(self):
        """
                :param NetworkPayMode: 网络计费模式列表，取值包括
        'BANDWIDTH_POSTPAID_BY_MONTH',
        'BANDWIDTH_PREPAID_BY_MONTH',
        'TRAFFIC_POSTPAID_BY_HOUR',
        'BANDWIDTH_POSTPAID_BY_HOUR',
        'BANDWIDTH_PACKAGE'
        注意：此字段可能返回 null，表示取不到有效值。
                :type NetworkPayMode: list of str
                :param CvmPayMode: cvm实例计费模式列表，取值包括"PREPAID","POSTPAID_BY_HOUR","CDHPAID"。
        注意：此字段可能返回 null，表示取不到有效值。
                :type CvmPayMode: list of str
                :param Cpu: cpu核数范围，前闭后闭区间。如[9,23]表示9 <= cpu核心数 <= 23。空区间表示任意cpu核心数都支持。
        注意：此字段可能返回 null，表示取不到有效值。
                :type Cpu: list of int
                :param ZoneId: 可用区ID列表。空列表表示任意可用区Id都支持。
        注意：此字段可能返回 null，表示取不到有效值。
                :type ZoneId: list of int
                :param BandwidthUpper: 带宽最大值
                :type BandwidthUpper: int
                :param BandwidthLimit: 带宽是否必须有上限。1表示有上限，0表示无上限
                :type BandwidthLimit: int
                :param ResourceIds: 资源唯一ID列表，可以是云服务器InstanceId，或者弹性公网IP唯一ID
                :type ResourceIds: str
        """
        self.NetworkPayMode = None
        self.CvmPayMode = None
        self.Cpu = None
        self.ZoneId = None
        self.BandwidthUpper = None
        self.BandwidthLimit = None
        self.ResourceIds = None

    def _deserialize(self, params):
        self.NetworkPayMode = params.get("NetworkPayMode")
        self.CvmPayMode = params.get("CvmPayMode")
        self.Cpu = params.get("Cpu")
        self.ZoneId = params.get("ZoneId")
        self.BandwidthUpper = params.get("BandwidthUpper")
        self.BandwidthLimit = params.get("BandwidthLimit")
        self.ResourceIds = params.get("ResourceIds")


class BandwidthLimitForCcnAlarmOnly(AbstractModel):
    """云联网（CCN）地域出带宽上限"""

    def __init__(self):
        """
        :param Region: 地域，例如：ap-guangzhou。
        :type Region: str
        :param BandwidthLimit: 出带宽上限，单位：Mbps。
        :type BandwidthLimit: int
        :param VbcId: 整型ID。
        :type VbcId: int
        :param CcnId: 实例ID。
        :type CcnId: str
        """
        self.Region = None
        self.BandwidthLimit = None
        self.VbcId = None
        self.CcnId = None

    def _deserialize(self, params):
        self.Region = params.get("Region")
        self.BandwidthLimit = params.get("BandwidthLimit")
        self.VbcId = params.get("VbcId")
        self.CcnId = params.get("CcnId")


class BandwidthLimitForCcnAlarmOnlyRequest(AbstractModel):
    """BandwidthLimitForCcnAlarmOnly请求参数结构体"""

    def __init__(self):
        """
        :param CcnId: CCN实例ID。形如：ccn-f49l6u0z
        :type CcnId: str
        :param Filters: 过滤条件
        :type Filters: list of Filter
        """
        self.CcnId = None
        self.Filters = None

    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)


class BandwidthLimitForCcnAlarmOnlyResponse(AbstractModel):
    """BandwidthLimitForCcnAlarmOnly返回参数结构体"""

    def __init__(self):
        """
        :param CcnRegionBandwidthLimitSet: 云联网（CCN）各地域出带宽上限
        :type CcnRegionBandwidthLimitSet: list of BandwidthLimitForCcnAlarmOnly
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.CcnRegionBandwidthLimitSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("CcnRegionBandwidthLimitSet") is not None:
            self.CcnRegionBandwidthLimitSet = []
            for item in params.get("CcnRegionBandwidthLimitSet"):
                obj = BandwidthLimitForCcnAlarmOnly()
                obj._deserialize(item)
                self.CcnRegionBandwidthLimitSet.append(obj)
        self.RequestId = params.get("RequestId")


class BandwidthPackage(AbstractModel):
    """描述带宽包信息的结构"""

    def __init__(self):
        """
        :param BandwidthPackageId: 带宽包唯一标识Id
        :type BandwidthPackageId: str
        :param NetworkType: 带宽包类型，包括'BGP','SINGLEISP','ANYCAST'
        :type NetworkType: str
        :param ChargeType: 带宽包计费类型，包括'TOP5_POSTPAID_BY_MONTH'和'PERCENT95_POSTPAID_BY_MONTH'
        :type ChargeType: str
        :param BandwidthPackageName: 带宽包名称
        :type BandwidthPackageName: str
        :param CreatedTime: 带宽包创建时间。按照`ISO8601`标准表示，并且使用`UTC`时间。格式为：`YYYY-MM-DDThh:mm:ssZ`。
        :type CreatedTime: str
        :param Status: 带宽包状态，包括'CREATING','CREATED','DELETING','DELETED'
        :type Status: str
        :param ResourceSet: 带宽包资源信息
        :type ResourceSet: list of Resource
        :param Bandwidth: 带宽包限速大小。单位：Mbps，-1表示不限速。
        :type Bandwidth: int
        """
        self.BandwidthPackageId = None
        self.NetworkType = None
        self.ChargeType = None
        self.BandwidthPackageName = None
        self.CreatedTime = None
        self.Status = None
        self.ResourceSet = None
        self.Bandwidth = None

    def _deserialize(self, params):
        self.BandwidthPackageId = params.get("BandwidthPackageId")
        self.NetworkType = params.get("NetworkType")
        self.ChargeType = params.get("ChargeType")
        self.BandwidthPackageName = params.get("BandwidthPackageName")
        self.CreatedTime = params.get("CreatedTime")
        self.Status = params.get("Status")
        if params.get("ResourceSet") is not None:
            self.ResourceSet = []
            for item in params.get("ResourceSet"):
                obj = Resource()
                obj._deserialize(item)
                self.ResourceSet.append(obj)
        self.Bandwidth = params.get("Bandwidth")


class CCN(AbstractModel):
    """云联网（CCN）对象"""

    def __init__(self):
        """
                :param CcnId: 云联网唯一ID
                :type CcnId: str
                :param CcnName: 云联网名称
                :type CcnName: str
                :param CcnDescription: 云联网描述信息
                :type CcnDescription: str
                :param InstanceCount: 关联实例数量
                :type InstanceCount: int
                :param CreateTime: 创建时间
                :type CreateTime: str
                :param State: 实例状态， 'ISOLATED': 隔离中（欠费停服），'AVAILABLE'：运行中。
                :type State: str
                :param QosLevel: 实例服务质量，’PT’：白金，'AU'：金，'AG'：银。
                :type QosLevel: str
                :param InstanceChargeType: 付费类型，PREPAID为预付费，POSTPAID为后付费。
        注意：此字段可能返回 null，表示取不到有效值。
                :type InstanceChargeType: str
                :param BandwidthLimitType: 限速类型，INTER_REGION_LIMIT为地域间限速；OUTER_REGION_LIMIT为地域出口限速。
        注意：此字段可能返回 null，表示取不到有效值。
                :type BandwidthLimitType: str
                :param TagSet: 标签键值对。
                :type TagSet: list of Tag
        """
        self.CcnId = None
        self.CcnName = None
        self.CcnDescription = None
        self.InstanceCount = None
        self.CreateTime = None
        self.State = None
        self.QosLevel = None
        self.InstanceChargeType = None
        self.BandwidthLimitType = None
        self.TagSet = None

    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")
        self.CcnName = params.get("CcnName")
        self.CcnDescription = params.get("CcnDescription")
        self.InstanceCount = params.get("InstanceCount")
        self.CreateTime = params.get("CreateTime")
        self.State = params.get("State")
        self.QosLevel = params.get("QosLevel")
        self.InstanceChargeType = params.get("InstanceChargeType")
        self.BandwidthLimitType = params.get("BandwidthLimitType")
        if params.get("TagSet") is not None:
            self.TagSet = []
            for item in params.get("TagSet"):
                obj = Tag()
                obj._deserialize(item)
                self.TagSet.append(obj)


class CcnAttachedInstance(AbstractModel):
    """云联网（CCN）关联实例（Instance）对象"""

    def __init__(self):
        """
                :param CcnId: 云联网实例ID。
                :type CcnId: str
                :param InstanceType: 关联实例类型：
        <li>`VPC`：私有网络</li>
        <li>`DIRECTCONNECT`：专线网关</li>
        <li>`BMVPC`：黑石私有网络</li>
                :type InstanceType: str
                :param InstanceId: 关联实例ID。
                :type InstanceId: str
                :param InstanceName: 关联实例名称。
                :type InstanceName: str
                :param InstanceRegion: 关联实例所属大区，例如：ap-guangzhou。
                :type InstanceRegion: str
                :param InstanceUin: 关联实例所属UIN（根账号）。
                :type InstanceUin: str
                :param CidrBlock: 关联实例CIDR。
                :type CidrBlock: list of str
                :param State: 关联实例状态：
        <li>`PENDING`：申请中</li>
        <li>`ACTIVE`：已连接</li>
        <li>`EXPIRED`：已过期</li>
        <li>`REJECTED`：已拒绝</li>
        <li>`DELETED`：已删除</li>
        <li>`FAILED`：失败的（2小时后将异步强制解关联）</li>
        <li>`ATTACHING`：关联中</li>
        <li>`DETACHING`：解关联中</li>
        <li>`DETACHFAILED`：解关联失败（2小时后将异步强制解关联）</li>
                :type State: str
                :param AttachedTime: 关联时间。
                :type AttachedTime: str
                :param CcnUin: 云联网所属UIN（根账号）。
                :type CcnUin: str
        """
        self.CcnId = None
        self.InstanceType = None
        self.InstanceId = None
        self.InstanceName = None
        self.InstanceRegion = None
        self.InstanceUin = None
        self.CidrBlock = None
        self.State = None
        self.AttachedTime = None
        self.CcnUin = None

    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")
        self.InstanceType = params.get("InstanceType")
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.InstanceRegion = params.get("InstanceRegion")
        self.InstanceUin = params.get("InstanceUin")
        self.CidrBlock = params.get("CidrBlock")
        self.State = params.get("State")
        self.AttachedTime = params.get("AttachedTime")
        self.CcnUin = params.get("CcnUin")


class CcnBandwidthInfo(AbstractModel):
    """用于描述云联网地域间限速带宽实例的信息"""

    def __init__(self):
        """
                :param CcnId: 带宽所属的云联网ID。
        注意：此字段可能返回 null，表示取不到有效值。
                :type CcnId: str
                :param CreatedTime: 实例的创建时间。
        注意：此字段可能返回 null，表示取不到有效值。
                :type CreatedTime: str
                :param ExpiredTime: 实例的过期时间
        注意：此字段可能返回 null，表示取不到有效值。
                :type ExpiredTime: str
                :param RegionFlowControlId: 带宽实例的唯一ID。
        注意：此字段可能返回 null，表示取不到有效值。
                :type RegionFlowControlId: str
                :param RenewFlag: 带宽是否自动续费的标记。
        注意：此字段可能返回 null，表示取不到有效值。
                :type RenewFlag: str
                :param CcnRegionBandwidthLimit: 描述带宽的地域和限速上限信息。
        注意：此字段可能返回 null，表示取不到有效值。
                :type CcnRegionBandwidthLimit: :class:`tcecloud.vpc.v20170312.models.CcnRegionBandwidthLimit`
        """
        self.CcnId = None
        self.CreatedTime = None
        self.ExpiredTime = None
        self.RegionFlowControlId = None
        self.RenewFlag = None
        self.CcnRegionBandwidthLimit = None

    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")
        self.CreatedTime = params.get("CreatedTime")
        self.ExpiredTime = params.get("ExpiredTime")
        self.RegionFlowControlId = params.get("RegionFlowControlId")
        self.RenewFlag = params.get("RenewFlag")
        if params.get("CcnRegionBandwidthLimit") is not None:
            self.CcnRegionBandwidthLimit = CcnRegionBandwidthLimit()
            self.CcnRegionBandwidthLimit._deserialize(params.get("CcnRegionBandwidthLimit"))


class CcnInstance(AbstractModel):
    """云联网（CCN）关联实例（Instance）对象。"""

    def __init__(self):
        """
                :param InstanceId: 关联实例ID。
                :type InstanceId: str
                :param InstanceRegion: 关联实例ID所属大区，例如：ap-guangzhou。
                :type InstanceRegion: str
                :param InstanceType: 关联实例类型，可选值：
        <li>`VPC`：私有网络</li>
        <li>`DIRECTCONNECT`：专线网关</li>
        <li>`BMVPC`：黑石私有网络</li>
                :type InstanceType: str
        """
        self.InstanceId = None
        self.InstanceRegion = None
        self.InstanceType = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.InstanceRegion = params.get("InstanceRegion")
        self.InstanceType = params.get("InstanceType")


class CcnLimit(AbstractModel):
    """云联网配额"""

    def __init__(self):
        """
        :param Type: 云联网配额类型
        :type Type: str
        :param Value: 云联网配额数值
        :type Value: int
        """
        self.Type = None
        self.Value = None

    def _deserialize(self, params):
        self.Type = params.get("Type")
        self.Value = params.get("Value")


class CcnRegionBandwidthLimit(AbstractModel):
    """云联网（CCN）地域出带宽上限"""

    def __init__(self):
        """
                :param Region: 地域，例如：ap-guangzhou
                :type Region: str
                :param BandwidthLimit: 出带宽上限，单位：Mbps
                :type BandwidthLimit: int
                :param IsBm: 是否黑石地域，默认`false`。
                :type IsBm: bool
                :param DstRegion: 目的地域，例如：ap-shanghai
        注意：此字段可能返回 null，表示取不到有效值。
                :type DstRegion: str
                :param DstIsBm: 目的地域是否为黑石地域，默认`false`。
                :type DstIsBm: bool
        """
        self.Region = None
        self.BandwidthLimit = None
        self.IsBm = None
        self.DstRegion = None
        self.DstIsBm = None

    def _deserialize(self, params):
        self.Region = params.get("Region")
        self.BandwidthLimit = params.get("BandwidthLimit")
        self.IsBm = params.get("IsBm")
        self.DstRegion = params.get("DstRegion")
        self.DstIsBm = params.get("DstIsBm")


class CcnRoute(AbstractModel):
    """CCN路由策略对象"""

    def __init__(self):
        """
        :param RouteId: 路由策略ID
        :type RouteId: str
        :param DestinationCidrBlock: 目的端
        :type DestinationCidrBlock: str
        :param InstanceType: 下一跳类型（关联实例类型），所有类型：VPC、DIRECTCONNECT
        :type InstanceType: str
        :param InstanceId: 下一跳（关联实例）
        :type InstanceId: str
        :param InstanceName: 下一跳名称（关联实例名称）
        :type InstanceName: str
        :param InstanceRegion: 下一跳所属地域（关联实例所属地域）
        :type InstanceRegion: str
        :param UpdateTime: 更新时间
        :type UpdateTime: str
        :param Enabled: 路由是否启用
        :type Enabled: bool
        :param InstanceUin: 关联实例所属UIN（根账号）
        :type InstanceUin: str
        """
        self.RouteId = None
        self.DestinationCidrBlock = None
        self.InstanceType = None
        self.InstanceId = None
        self.InstanceName = None
        self.InstanceRegion = None
        self.UpdateTime = None
        self.Enabled = None
        self.InstanceUin = None

    def _deserialize(self, params):
        self.RouteId = params.get("RouteId")
        self.DestinationCidrBlock = params.get("DestinationCidrBlock")
        self.InstanceType = params.get("InstanceType")
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.InstanceRegion = params.get("InstanceRegion")
        self.UpdateTime = params.get("UpdateTime")
        self.Enabled = params.get("Enabled")
        self.InstanceUin = params.get("InstanceUin")


class CheckAssistantCidrRequest(AbstractModel):
    """CheckAssistantCidr请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: `VPC`实例`ID`。形如：`vpc-6v2ht8q5`
        :type VpcId: str
        :param NewCidrBlocks: 待添加的负载CIDR。CIDR数组，格式如["10.0.0.0/16", "172.16.0.0/16"]
        :type NewCidrBlocks: list of str
        :param OldCidrBlocks: 待删除的负载CIDR。CIDR数组，格式如["10.0.0.0/16", "172.16.0.0/16"]
        :type OldCidrBlocks: list of str
        """
        self.VpcId = None
        self.NewCidrBlocks = None
        self.OldCidrBlocks = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.NewCidrBlocks = params.get("NewCidrBlocks")
        self.OldCidrBlocks = params.get("OldCidrBlocks")


class CheckAssistantCidrResponse(AbstractModel):
    """CheckAssistantCidr返回参数结构体"""

    def __init__(self):
        """
        :param ConflictSourceSet: 冲突资源信息数组。
        :type ConflictSourceSet: list of ConflictSource
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ConflictSourceSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("ConflictSourceSet") is not None:
            self.ConflictSourceSet = []
            for item in params.get("ConflictSourceSet"):
                obj = ConflictSource()
                obj._deserialize(item)
                self.ConflictSourceSet.append(obj)
        self.RequestId = params.get("RequestId")


class CheckBandwidthPackageRequest(AbstractModel):
    """CheckBandwidthPackage请求参数结构体"""


class CheckBandwidthPackageResponse(AbstractModel):
    """CheckBandwidthPackage返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CheckDefaultSubnetRequest(AbstractModel):
    """CheckDefaultSubnet请求参数结构体"""

    def __init__(self):
        """
        :param Zone: 子网所在的可用区ID，不同子网选择不同可用区可以做跨可用区灾备。
        :type Zone: str
        """
        self.Zone = None

    def _deserialize(self, params):
        self.Zone = params.get("Zone")


class CheckDefaultSubnetResponse(AbstractModel):
    """CheckDefaultSubnet返回参数结构体"""

    def __init__(self):
        """
        :param Result: 检查结果。true为可以创建默认子网，false为不可以创建默认子网。
        :type Result: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Result = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Result = params.get("Result")
        self.RequestId = params.get("RequestId")


class CheckGatewayFlowMonitorRequest(AbstractModel):
    """CheckGatewayFlowMonitor请求参数结构体"""

    def __init__(self):
        """
                :param GatewayId: 网关实例ID，目前我们支持的网关实例类型有，
        专线网关实例ID，形如，`dcg-ltjahce6`；
        Nat网关实例ID，形如，`nat-ltjahce6`；
        VPN网关实例ID，形如，`vpn-ltjahce6`。
                :type GatewayId: str
        """
        self.GatewayId = None

    def _deserialize(self, params):
        self.GatewayId = params.get("GatewayId")


class CheckGatewayFlowMonitorResponse(AbstractModel):
    """CheckGatewayFlowMonitor返回参数结构体"""

    def __init__(self):
        """
        :param Enabled: 网关是否启用了流控。true为启用，false未启用。
        :type Enabled: bool
        :param Bandwidth: 网关的带宽。
        :type Bandwidth: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Enabled = None
        self.Bandwidth = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Enabled = params.get("Enabled")
        self.Bandwidth = params.get("Bandwidth")
        self.RequestId = params.get("RequestId")


class CheckNetDetectStateRequest(AbstractModel):
    """CheckNetDetectState请求参数结构体"""

    def __init__(self):
        """
                :param DetectDestinationIp: 探测目的IPv4地址数组，最多两个。
                :type DetectDestinationIp: list of str
                :param NextHopType: 下一跳类型，目前我们支持的类型有：
        VPN：VPN网关；
        DIRECTCONNECT：专线网关；
        PEERCONNECTION：对等连接；
        NAT：NAT网关；
        NORMAL_CVM：普通云服务器；
                :type NextHopType: str
                :param NextHopDestination: 下一跳目的网关，取值与“下一跳类型”相关：
        下一跳类型为VPN，取值VPN网关ID，形如：vpngw-12345678；
        下一跳类型为DIRECTCONNECT，取值专线网关ID，形如：dcg-12345678；
        下一跳类型为PEERCONNECTION，取值对等连接ID，形如：pcx-12345678；
        下一跳类型为NAT，取值Nat网关，形如：nat-12345678；
        下一跳类型为NORMAL_CVM，取值云服务器IPv4地址，形如：10.0.0.12；
                :type NextHopDestination: str
                :param NetDetectId: 网络探测实例ID。形如：netd-12345678。该参数与（VpcId，SubnetId，NetDetectName），至少要有一个。当NetDetectId存在时，使用NetDetectId。
                :type NetDetectId: str
                :param VpcId: `VPC`实例`ID`。形如：`vpc-12345678`。该参数与（SubnetId，NetDetectName）配合使用，与NetDetectId至少要有一个。当NetDetectId存在时，使用NetDetectId。
                :type VpcId: str
                :param SubnetId: 子网实例ID。形如：subnet-12345678。该参数与（VpcId，NetDetectName）配合使用，与NetDetectId至少要有一个。当NetDetectId存在时，使用NetDetectId。
                :type SubnetId: str
                :param NetDetectName: 网络探测名称，最大长度不能超过60个字节。该参数与（VpcId，SubnetId）配合使用，与NetDetectId至少要有一个。当NetDetectId存在时，使用NetDetectId。
                :type NetDetectName: str
        """
        self.DetectDestinationIp = None
        self.NextHopType = None
        self.NextHopDestination = None
        self.NetDetectId = None
        self.VpcId = None
        self.SubnetId = None
        self.NetDetectName = None

    def _deserialize(self, params):
        self.DetectDestinationIp = params.get("DetectDestinationIp")
        self.NextHopType = params.get("NextHopType")
        self.NextHopDestination = params.get("NextHopDestination")
        self.NetDetectId = params.get("NetDetectId")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.NetDetectName = params.get("NetDetectName")


class CheckNetDetectStateResponse(AbstractModel):
    """CheckNetDetectState返回参数结构体"""

    def __init__(self):
        """
        :param NetDetectIpStateSet: 网络探测验证结果对象数组。
        :type NetDetectIpStateSet: list of NetDetectIpState
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.NetDetectIpStateSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("NetDetectIpStateSet") is not None:
            self.NetDetectIpStateSet = []
            for item in params.get("NetDetectIpStateSet"):
                obj = NetDetectIpState()
                obj._deserialize(item)
                self.NetDetectIpStateSet.append(obj)
        self.RequestId = params.get("RequestId")


class CheckSameCityRequest(AbstractModel):
    """CheckSameCity请求参数结构体"""

    def __init__(self):
        """
        :param Regions: 地域列表，最多两个。参数取值参考地域列表。
        :type Regions: list of str
        """
        self.Regions = None

    def _deserialize(self, params):
        self.Regions = params.get("Regions")


class CheckSameCityResponse(AbstractModel):
    """CheckSameCity返回参数结构体"""

    def __init__(self):
        """
        :param SameCity: 取值为true时，表示为同城；否则为非同城。
        :type SameCity: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SameCity = None
        self.RequestId = None

    def _deserialize(self, params):
        self.SameCity = params.get("SameCity")
        self.RequestId = params.get("RequestId")


class CheckSecurityGroupPoliciesRequest(AbstractModel):
    """CheckSecurityGroupPolicies请求参数结构体"""

    def __init__(self):
        """
        :param InstanceUUid: CVM主机的服务器ID
        :type InstanceUUid: str
        """
        self.InstanceUUid = None

    def _deserialize(self, params):
        self.InstanceUUid = params.get("InstanceUUid")


class CheckSecurityGroupPoliciesResponse(AbstractModel):
    """CheckSecurityGroupPolicies返回参数结构体"""

    def __init__(self):
        """
        :param SecurityGroupPolicyCheckInfoSet: 安全组策略检测结果集合
        :type SecurityGroupPolicyCheckInfoSet: list of SecurityGroupPolicyCheckInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SecurityGroupPolicyCheckInfoSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("SecurityGroupPolicyCheckInfoSet") is not None:
            self.SecurityGroupPolicyCheckInfoSet = []
            for item in params.get("SecurityGroupPolicyCheckInfoSet"):
                obj = SecurityGroupPolicyCheckInfo()
                obj._deserialize(item)
                self.SecurityGroupPolicyCheckInfoSet.append(obj)
        self.RequestId = params.get("RequestId")


class ClassicLinkInstance(AbstractModel):
    """私有网络和基础网络互通设备"""

    def __init__(self):
        """
        :param VpcId: VPC实例ID
        :type VpcId: str
        :param InstanceId: 云服务器实例唯一ID
        :type InstanceId: str
        """
        self.VpcId = None
        self.InstanceId = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.InstanceId = params.get("InstanceId")


class CloneSecurityGroupRequest(AbstractModel):
    """CloneSecurityGroup请求参数结构体"""

    def __init__(self):
        """
        :param SecurityGroupId: 安全组实例ID，例如sg-33ocnj9n，可通过DescribeSecurityGroups获取。
        :type SecurityGroupId: str
        :param GroupName: 安全组名称，可任意命名，但不得超过60个字符。未提供参数时，克隆后的安全组名称和SecurityGroupId对应的安全组名称相同。
        :type GroupName: str
        :param GroupDescription: 安全组备注，最多100个字符。未提供参数时，克隆后的安全组备注和SecurityGroupId对应的安全组备注相同。
        :type GroupDescription: str
        :param ProjectId: 项目ID，默认0。可在qcloud控制台项目管理页面查询到。
        :type ProjectId: str
        """
        self.SecurityGroupId = None
        self.GroupName = None
        self.GroupDescription = None
        self.ProjectId = None

    def _deserialize(self, params):
        self.SecurityGroupId = params.get("SecurityGroupId")
        self.GroupName = params.get("GroupName")
        self.GroupDescription = params.get("GroupDescription")
        self.ProjectId = params.get("ProjectId")


class CloneSecurityGroupResponse(AbstractModel):
    """CloneSecurityGroup返回参数结构体"""

    def __init__(self):
        """
        :param SecurityGroup: 安全组对象。
        :type SecurityGroup: :class:`tcecloud.vpc.v20170312.models.SecurityGroup`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SecurityGroup = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("SecurityGroup") is not None:
            self.SecurityGroup = SecurityGroup()
            self.SecurityGroup._deserialize(params.get("SecurityGroup"))
        self.RequestId = params.get("RequestId")


class ConflictItem(AbstractModel):
    """冲突资源条目信息。"""

    def __init__(self):
        """
        :param ConfilctId: 冲突资源的ID
        :type ConfilctId: str
        :param DestinationItem: 冲突目的资源
        :type DestinationItem: str
        """
        self.ConfilctId = None
        self.DestinationItem = None

    def _deserialize(self, params):
        self.ConfilctId = params.get("ConfilctId")
        self.DestinationItem = params.get("DestinationItem")


class ConflictSource(AbstractModel):
    """冲突资源信息。"""

    def __init__(self):
        """
        :param ConflictSourceId: 冲突资源ID
        :type ConflictSourceId: str
        :param SourceItem: 冲突资源
        :type SourceItem: str
        :param ConflictItemSet: 冲突资源条目信息
        :type ConflictItemSet: list of ConflictItem
        """
        self.ConflictSourceId = None
        self.SourceItem = None
        self.ConflictItemSet = None

    def _deserialize(self, params):
        self.ConflictSourceId = params.get("ConflictSourceId")
        self.SourceItem = params.get("SourceItem")
        if params.get("ConflictItemSet") is not None:
            self.ConflictItemSet = []
            for item in params.get("ConflictItemSet"):
                obj = ConflictItem()
                obj._deserialize(item)
                self.ConflictItemSet.append(obj)


class CreateAddressTemplateGroupRequest(AbstractModel):
    """CreateAddressTemplateGroup请求参数结构体"""

    def __init__(self):
        """
        :param AddressTemplateGroupName: IP地址模版集合名称。
        :type AddressTemplateGroupName: str
        :param AddressTemplateIds: IP地址模版实例ID，例如：ipm-mdunqeb6。
        :type AddressTemplateIds: list of str
        """
        self.AddressTemplateGroupName = None
        self.AddressTemplateIds = None

    def _deserialize(self, params):
        self.AddressTemplateGroupName = params.get("AddressTemplateGroupName")
        self.AddressTemplateIds = params.get("AddressTemplateIds")


class CreateAddressTemplateGroupResponse(AbstractModel):
    """CreateAddressTemplateGroup返回参数结构体"""

    def __init__(self):
        """
        :param AddressTemplateGroup: IP地址模板集合对象。
        :type AddressTemplateGroup: :class:`tcecloud.vpc.v20170312.models.AddressTemplateGroup`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AddressTemplateGroup = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("AddressTemplateGroup") is not None:
            self.AddressTemplateGroup = AddressTemplateGroup()
            self.AddressTemplateGroup._deserialize(params.get("AddressTemplateGroup"))
        self.RequestId = params.get("RequestId")


class CreateAddressTemplateRequest(AbstractModel):
    """CreateAddressTemplate请求参数结构体"""

    def __init__(self):
        """
        :param AddressTemplateName: IP地址模版名称
        :type AddressTemplateName: str
        :param Addresses: 地址信息，支持 IP、CIDR、IP 范围。
        :type Addresses: list of str
        """
        self.AddressTemplateName = None
        self.Addresses = None

    def _deserialize(self, params):
        self.AddressTemplateName = params.get("AddressTemplateName")
        self.Addresses = params.get("Addresses")


class CreateAddressTemplateResponse(AbstractModel):
    """CreateAddressTemplate返回参数结构体"""

    def __init__(self):
        """
        :param AddressTemplate: IP地址模板对象。
        :type AddressTemplate: :class:`tcecloud.vpc.v20170312.models.AddressTemplate`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AddressTemplate = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("AddressTemplate") is not None:
            self.AddressTemplate = AddressTemplate()
            self.AddressTemplate._deserialize(params.get("AddressTemplate"))
        self.RequestId = params.get("RequestId")


class CreateAndAttachNetworkInterfaceRequest(AbstractModel):
    """CreateAndAttachNetworkInterface请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: VPC实例ID。可通过DescribeVpcs接口返回值中的VpcId获取。
        :type VpcId: str
        :param NetworkInterfaceName: 弹性网卡名称，最大长度不能超过60个字节。
        :type NetworkInterfaceName: str
        :param SubnetId: 弹性网卡所在的子网实例ID，例如：subnet-0ap8nwca。
        :type SubnetId: str
        :param InstanceId: 云主机实例ID。
        :type InstanceId: str
        :param PrivateIpAddresses: 指定的内网IP信息，单次最多指定10个。
        :type PrivateIpAddresses: list of PrivateIpAddressSpecification
        :param SecondaryPrivateIpAddressCount: 新申请的内网IP地址个数，内网IP地址个数总和不能超过配数。
        :type SecondaryPrivateIpAddressCount: int
        :param SecurityGroupIds: 指定绑定的安全组，例如：['sg-1dd51d']。
        :type SecurityGroupIds: list of str
        :param NetworkInterfaceDescription: 弹性网卡描述，可任意命名，但不得超过60个字符。
        :type NetworkInterfaceDescription: str
        :param Tags: 指定绑定的标签列表，例如：[{"Key": "city", "Value": "shanghai"}]
        :type Tags: list of Tag
        """
        self.VpcId = None
        self.NetworkInterfaceName = None
        self.SubnetId = None
        self.InstanceId = None
        self.PrivateIpAddresses = None
        self.SecondaryPrivateIpAddressCount = None
        self.SecurityGroupIds = None
        self.NetworkInterfaceDescription = None
        self.Tags = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.NetworkInterfaceName = params.get("NetworkInterfaceName")
        self.SubnetId = params.get("SubnetId")
        self.InstanceId = params.get("InstanceId")
        if params.get("PrivateIpAddresses") is not None:
            self.PrivateIpAddresses = []
            for item in params.get("PrivateIpAddresses"):
                obj = PrivateIpAddressSpecification()
                obj._deserialize(item)
                self.PrivateIpAddresses.append(obj)
        self.SecondaryPrivateIpAddressCount = params.get("SecondaryPrivateIpAddressCount")
        self.SecurityGroupIds = params.get("SecurityGroupIds")
        self.NetworkInterfaceDescription = params.get("NetworkInterfaceDescription")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)


class CreateAndAttachNetworkInterfaceResponse(AbstractModel):
    """CreateAndAttachNetworkInterface返回参数结构体"""

    def __init__(self):
        """
        :param NetworkInterface: 弹性网卡实例。
        :type NetworkInterface: :class:`tcecloud.vpc.v20170312.models.NetworkInterface`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.NetworkInterface = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("NetworkInterface") is not None:
            self.NetworkInterface = NetworkInterface()
            self.NetworkInterface._deserialize(params.get("NetworkInterface"))
        self.RequestId = params.get("RequestId")


class CreateAssistantCidrRequest(AbstractModel):
    """CreateAssistantCidr请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: `VPC`实例`ID`。形如：`vpc-6v2ht8q5`
        :type VpcId: str
        :param CidrBlocks: CIDR数组，格式如["10.0.0.0/16", "172.16.0.0/16"]
        :type CidrBlocks: list of str
        """
        self.VpcId = None
        self.CidrBlocks = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.CidrBlocks = params.get("CidrBlocks")


class CreateAssistantCidrResponse(AbstractModel):
    """CreateAssistantCidr返回参数结构体"""

    def __init__(self):
        """
        :param AssistantCidrSet: 辅助CIDR数组。
        :type AssistantCidrSet: list of AssistantCidr
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AssistantCidrSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("AssistantCidrSet") is not None:
            self.AssistantCidrSet = []
            for item in params.get("AssistantCidrSet"):
                obj = AssistantCidr()
                obj._deserialize(item)
                self.AssistantCidrSet.append(obj)
        self.RequestId = params.get("RequestId")


class CreateBandwidthPackageRequest(AbstractModel):
    """CreateBandwidthPackage请求参数结构体"""

    def __init__(self):
        """
        :param NetworkType: 带宽包类型，包括'BGP'，'SINGLEISP'，'ANYCAST'
        :type NetworkType: str
        :param ChargeType: 带宽包计费类型，包括‘TOP5_POSTPAID_BY_MONTH’，‘PERCENT95_POSTPAID_BY_MONTH’
        :type ChargeType: str
        :param BandwidthPackageName: 带宽包名字
        :type BandwidthPackageName: str
        :param BandwidthPackageCount: 带宽包数量(非上移账户只能填1)
        :type BandwidthPackageCount: int
        :param InternetMaxBandwidth: 带宽包限速大小。单位：Mbps，-1表示不限速。
        :type InternetMaxBandwidth: int
        :param Tags: 需要关联的标签列表。
        :type Tags: list of Tag
        :param Protocol: 带宽包协议类型。当前支持'ipv4'和'ipv6'协议带宽包，默认值是'ipv4'。
        :type Protocol: str
        """
        self.NetworkType = None
        self.ChargeType = None
        self.BandwidthPackageName = None
        self.BandwidthPackageCount = None
        self.InternetMaxBandwidth = None
        self.Tags = None
        self.Protocol = None

    def _deserialize(self, params):
        self.NetworkType = params.get("NetworkType")
        self.ChargeType = params.get("ChargeType")
        self.BandwidthPackageName = params.get("BandwidthPackageName")
        self.BandwidthPackageCount = params.get("BandwidthPackageCount")
        self.InternetMaxBandwidth = params.get("InternetMaxBandwidth")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.Protocol = params.get("Protocol")


class CreateBandwidthPackageResponse(AbstractModel):
    """CreateBandwidthPackage返回参数结构体"""

    def __init__(self):
        """
        :param BandwidthPackageId: 带宽包唯一ID
        :type BandwidthPackageId: str
        :param BandwidthPackageIds: 带宽包唯一ID列表(申请数量大于1时有效)
        :type BandwidthPackageIds: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.BandwidthPackageId = None
        self.BandwidthPackageIds = None
        self.RequestId = None

    def _deserialize(self, params):
        self.BandwidthPackageId = params.get("BandwidthPackageId")
        self.BandwidthPackageIds = params.get("BandwidthPackageIds")
        self.RequestId = params.get("RequestId")


class CreateCcnBandwidthRequest(AbstractModel):
    """CreateCcnBandwidth请求参数结构体"""

    def __init__(self):
        """
        :param CcnId: CCN实例ID。
        :type CcnId: str
        :param InstanceChargePrepaid: 预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月实例的购买时长、是否设置自动续费等属性。若指定实例的付费模式为预付费则该参数必传。
        :type InstanceChargePrepaid: :class:`tcecloud.vpc.v20170312.models.InstanceChargePrepaid`
        :param CcnRegionBandwidthLimits: 云联网（CCN）各地域带宽上限。
        :type CcnRegionBandwidthLimits: list of CcnRegionBandwidthLimit
        """
        self.CcnId = None
        self.InstanceChargePrepaid = None
        self.CcnRegionBandwidthLimits = None

    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")
        if params.get("InstanceChargePrepaid") is not None:
            self.InstanceChargePrepaid = InstanceChargePrepaid()
            self.InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))
        if params.get("CcnRegionBandwidthLimits") is not None:
            self.CcnRegionBandwidthLimits = []
            for item in params.get("CcnRegionBandwidthLimits"):
                obj = CcnRegionBandwidthLimit()
                obj._deserialize(item)
                self.CcnRegionBandwidthLimits.append(obj)


class CreateCcnBandwidthResponse(AbstractModel):
    """CreateCcnBandwidth返回参数结构体"""

    def __init__(self):
        """
        :param CcnBandwidth: 云联网（CNN）地域带宽详情。
        :type CcnBandwidth: :class:`tcecloud.vpc.v20170312.models.CcnBandwidthInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.CcnBandwidth = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("CcnBandwidth") is not None:
            self.CcnBandwidth = CcnBandwidthInfo()
            self.CcnBandwidth._deserialize(params.get("CcnBandwidth"))
        self.RequestId = params.get("RequestId")


class CreateCcnRequest(AbstractModel):
    """CreateCcn请求参数结构体"""

    def __init__(self):
        """
        :param CcnName: CCN名称，最大长度不能超过60个字节。
        :type CcnName: str
        :param CcnDescription: CCN描述信息，最大长度不能超过100个字节。
        :type CcnDescription: str
        :param QosLevel: CCN服务质量，'PT'：白金，'AU'：金，'AG'：银，默认为‘AU’。
        :type QosLevel: str
        :param InstanceChargeType: 计费模式，PREPAID：表示预付费，即包年包月，POSTPAID：表示后付费，即按量计费。默认：POSTPAID。
        :type InstanceChargeType: str
        :param BandwidthLimitType: 限速类型，OUTER_REGION_LIMIT表示地域出口限速，INTER_REGION_LIMIT为地域间限速，默认为OUTER_REGION_LIMIT
        :type BandwidthLimitType: str
        :param Tags: 指定绑定的标签列表，例如：[{"Key": "city", "Value": "shanghai"}]
        :type Tags: list of Tag
        """
        self.CcnName = None
        self.CcnDescription = None
        self.QosLevel = None
        self.InstanceChargeType = None
        self.BandwidthLimitType = None
        self.Tags = None

    def _deserialize(self, params):
        self.CcnName = params.get("CcnName")
        self.CcnDescription = params.get("CcnDescription")
        self.QosLevel = params.get("QosLevel")
        self.InstanceChargeType = params.get("InstanceChargeType")
        self.BandwidthLimitType = params.get("BandwidthLimitType")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)


class CreateCcnResponse(AbstractModel):
    """CreateCcn返回参数结构体"""

    def __init__(self):
        """
        :param Ccn: 云联网（CCN）对象。
        :type Ccn: :class:`tcecloud.vpc.v20170312.models.CCN`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Ccn = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Ccn") is not None:
            self.Ccn = CCN()
            self.Ccn._deserialize(params.get("Ccn"))
        self.RequestId = params.get("RequestId")


class CreateCustomerGatewayRequest(AbstractModel):
    """CreateCustomerGateway请求参数结构体"""

    def __init__(self):
        """
        :param CustomerGatewayName: 对端网关名称，可任意命名，但不得超过60个字符。
        :type CustomerGatewayName: str
        :param IpAddress: 对端网关公网IP。
        :type IpAddress: str
        """
        self.CustomerGatewayName = None
        self.IpAddress = None

    def _deserialize(self, params):
        self.CustomerGatewayName = params.get("CustomerGatewayName")
        self.IpAddress = params.get("IpAddress")


class CreateCustomerGatewayResponse(AbstractModel):
    """CreateCustomerGateway返回参数结构体"""

    def __init__(self):
        """
        :param CustomerGateway: 对端网关对象
        :type CustomerGateway: :class:`tcecloud.vpc.v20170312.models.CustomerGateway`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.CustomerGateway = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("CustomerGateway") is not None:
            self.CustomerGateway = CustomerGateway()
            self.CustomerGateway._deserialize(params.get("CustomerGateway"))
        self.RequestId = params.get("RequestId")


class CreateDefaultSecurityGroupRequest(AbstractModel):
    """CreateDefaultSecurityGroup请求参数结构体"""

    def __init__(self):
        """
        :param ProjectId: 项目ID，默认0。可在qcloud控制台项目管理页面查询到。
        :type ProjectId: str
        """
        self.ProjectId = None

    def _deserialize(self, params):
        self.ProjectId = params.get("ProjectId")


class CreateDefaultSecurityGroupResponse(AbstractModel):
    """CreateDefaultSecurityGroup返回参数结构体"""

    def __init__(self):
        """
        :param SecurityGroup: 安全组对象。
        :type SecurityGroup: :class:`tcecloud.vpc.v20170312.models.SecurityGroup`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SecurityGroup = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("SecurityGroup") is not None:
            self.SecurityGroup = SecurityGroup()
            self.SecurityGroup._deserialize(params.get("SecurityGroup"))
        self.RequestId = params.get("RequestId")


class CreateDefaultVpcRequest(AbstractModel):
    """CreateDefaultVpc请求参数结构体"""

    def __init__(self):
        """
        :param Zone: 子网所在的可用区ID，不指定将随机选择可用区
        :type Zone: str
        :param Force: 是否强制返回默认VPC
        :type Force: bool
        """
        self.Zone = None
        self.Force = None

    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.Force = params.get("Force")


class CreateDefaultVpcResponse(AbstractModel):
    """CreateDefaultVpc返回参数结构体"""

    def __init__(self):
        """
        :param Vpc: 默认VPC和子网ID
        :type Vpc: :class:`tcecloud.vpc.v20170312.models.DefaultVpcSubnet`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Vpc = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Vpc") is not None:
            self.Vpc = DefaultVpcSubnet()
            self.Vpc._deserialize(params.get("Vpc"))
        self.RequestId = params.get("RequestId")


class CreateDirectConnectGatewayCcnRoutesRequest(AbstractModel):
    """CreateDirectConnectGatewayCcnRoutes请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID，形如：dcg-prpqlmg1
        :type DirectConnectGatewayId: str
        :param Routes: 需要连通的IDC网段列表
        :type Routes: list of DirectConnectGatewayCcnRoute
        """
        self.DirectConnectGatewayId = None
        self.Routes = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        if params.get("Routes") is not None:
            self.Routes = []
            for item in params.get("Routes"):
                obj = DirectConnectGatewayCcnRoute()
                obj._deserialize(item)
                self.Routes.append(obj)


class CreateDirectConnectGatewayCcnRoutesResponse(AbstractModel):
    """CreateDirectConnectGatewayCcnRoutes返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateDirectConnectGatewayRequest(AbstractModel):
    """CreateDirectConnectGateway请求参数结构体"""

    def __init__(self):
        """
                :param DirectConnectGatewayName: 专线网关名称
                :type DirectConnectGatewayName: str
                :param NetworkType: 关联网络类型，可选值：
        <li>VPC - 私有网络</li>
        <li>CCN - 云联网</li>
                :type NetworkType: str
                :param NetworkInstanceId: <li>NetworkType 为 VPC 时，这里传值为私有网络实例ID</li>
        <li>NetworkType 为 CCN 时，这里传值为云联网实例ID</li>
                :type NetworkInstanceId: str
                :param GatewayType: 网关类型，可选值：
        <li>NORMAL - （默认）标准型，注：云联网只支持标准型</li>
        <li>NAT - NAT型</li>NAT类型支持网络地址转换配置，类型确定后不能修改；一个私有网络可以创建一个NAT类型的专线网关和一个非NAT类型的专线网关
                :type GatewayType: str
        """
        self.DirectConnectGatewayName = None
        self.NetworkType = None
        self.NetworkInstanceId = None
        self.GatewayType = None

    def _deserialize(self, params):
        self.DirectConnectGatewayName = params.get("DirectConnectGatewayName")
        self.NetworkType = params.get("NetworkType")
        self.NetworkInstanceId = params.get("NetworkInstanceId")
        self.GatewayType = params.get("GatewayType")


class CreateDirectConnectGatewayResponse(AbstractModel):
    """CreateDirectConnectGateway返回参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGateway: 专线网关对象。
        :type DirectConnectGateway: :class:`tcecloud.vpc.v20170312.models.DirectConnectGateway`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DirectConnectGateway = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("DirectConnectGateway") is not None:
            self.DirectConnectGateway = DirectConnectGateway()
            self.DirectConnectGateway._deserialize(params.get("DirectConnectGateway"))
        self.RequestId = params.get("RequestId")


class CreateFlowLogRequest(AbstractModel):
    """CreateFlowLog请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: 私用网络ID或者统一ID，建议使用统一ID
        :type VpcId: str
        :param FlowLogName: 流日志实例名字
        :type FlowLogName: str
        :param ResourceType: 流日志所属资源类型，VPC|SUBNET|NETWORKINTERFACE
        :type ResourceType: str
        :param ResourceId: 资源唯一ID
        :type ResourceId: str
        :param TrafficType: 流日志采集类型，ACCEPT|REJECT|ALL
        :type TrafficType: str
        :param CloudLogId: 流日志存储ID
        :type CloudLogId: str
        :param FlowLogDescription: 流日志实例描述
        :type FlowLogDescription: str
        """
        self.VpcId = None
        self.FlowLogName = None
        self.ResourceType = None
        self.ResourceId = None
        self.TrafficType = None
        self.CloudLogId = None
        self.FlowLogDescription = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.FlowLogName = params.get("FlowLogName")
        self.ResourceType = params.get("ResourceType")
        self.ResourceId = params.get("ResourceId")
        self.TrafficType = params.get("TrafficType")
        self.CloudLogId = params.get("CloudLogId")
        self.FlowLogDescription = params.get("FlowLogDescription")


class CreateFlowLogResponse(AbstractModel):
    """CreateFlowLog返回参数结构体"""

    def __init__(self):
        """
        :param FlowLog: 创建的流日志信息
        :type FlowLog: list of FlowLog
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FlowLog = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("FlowLog") is not None:
            self.FlowLog = []
            for item in params.get("FlowLog"):
                obj = FlowLog()
                obj._deserialize(item)
                self.FlowLog.append(obj)
        self.RequestId = params.get("RequestId")


class CreateHaVipRequest(AbstractModel):
    """CreateHaVip请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: `HAVIP`所在私有网络`ID`。
        :type VpcId: str
        :param SubnetId: `HAVIP`所在子网`ID`。
        :type SubnetId: str
        :param HaVipName: `HAVIP`名称。
        :type HaVipName: str
        :param Vip: 指定虚拟IP地址，必须在`VPC`网段内且未被占用。不指定则自动分配。
        :type Vip: str
        """
        self.VpcId = None
        self.SubnetId = None
        self.HaVipName = None
        self.Vip = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.HaVipName = params.get("HaVipName")
        self.Vip = params.get("Vip")


class CreateHaVipResponse(AbstractModel):
    """CreateHaVip返回参数结构体"""

    def __init__(self):
        """
        :param HaVip: `HAVIP`对象。
        :type HaVip: :class:`tcecloud.vpc.v20170312.models.HaVip`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.HaVip = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("HaVip") is not None:
            self.HaVip = HaVip()
            self.HaVip._deserialize(params.get("HaVip"))
        self.RequestId = params.get("RequestId")


class CreateIp6TranslatorsRequest(AbstractModel):
    """CreateIp6Translators请求参数结构体"""

    def __init__(self):
        """
        :param IdcList: 创建转换实例所属IDC
        :type IdcList: list of str
        :param Ip6TranslatorName: 转换实例名称
        :type Ip6TranslatorName: str
        :param Ip6TranslatorCount: 创建转换实例数量，默认是1个
        :type Ip6TranslatorCount: int
        :param Ip6InternetServiceProvider: 转换实例运营商属性，可取"CMCC","CTCC","CUCC","BGP"
        :type Ip6InternetServiceProvider: str
        """
        self.IdcList = None
        self.Ip6TranslatorName = None
        self.Ip6TranslatorCount = None
        self.Ip6InternetServiceProvider = None

    def _deserialize(self, params):
        self.IdcList = params.get("IdcList")
        self.Ip6TranslatorName = params.get("Ip6TranslatorName")
        self.Ip6TranslatorCount = params.get("Ip6TranslatorCount")
        self.Ip6InternetServiceProvider = params.get("Ip6InternetServiceProvider")


class CreateIp6TranslatorsResponse(AbstractModel):
    """CreateIp6Translators返回参数结构体"""

    def __init__(self):
        """
        :param Ip6TranslatorSet: 转换实例的唯一ID数组，形如"ip6-xxxxxxxx"
        :type Ip6TranslatorSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Ip6TranslatorSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Ip6TranslatorSet = params.get("Ip6TranslatorSet")
        self.RequestId = params.get("RequestId")


class CreateLocalDestinationIpPortTranslationNatRuleRequest(AbstractModel):
    """CreateLocalDestinationIpPortTranslationNatRule请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID
        :type DirectConnectGatewayId: str
        :param VpcId: 字符型VPCID
        :type VpcId: str
        :param LocalDestinationIpPortTranslationNatRuleSet: 本端目的IP端口转换
        :type LocalDestinationIpPortTranslationNatRuleSet: list of LocalDestinationIpPortTranslationNatRule
        """
        self.DirectConnectGatewayId = None
        self.VpcId = None
        self.LocalDestinationIpPortTranslationNatRuleSet = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.VpcId = params.get("VpcId")
        if params.get("LocalDestinationIpPortTranslationNatRuleSet") is not None:
            self.LocalDestinationIpPortTranslationNatRuleSet = []
            for item in params.get("LocalDestinationIpPortTranslationNatRuleSet"):
                obj = LocalDestinationIpPortTranslationNatRule()
                obj._deserialize(item)
                self.LocalDestinationIpPortTranslationNatRuleSet.append(obj)


class CreateLocalDestinationIpPortTranslationNatRuleResponse(AbstractModel):
    """CreateLocalDestinationIpPortTranslationNatRule返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateLocalIpTranslationAclRuleRequest(AbstractModel):
    """CreateLocalIpTranslationAclRule请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID
        :type DirectConnectGatewayId: str
        :param VpcId: 字符型VPCID
        :type VpcId: str
        :param OriginalIp: 原始IP
        :type OriginalIp: str
        :param TranslationIp: 映射IP
        :type TranslationIp: str
        :param LocalIpTranslationAclRuleSet: 本端IP转换列表ACL列表
        :type LocalIpTranslationAclRuleSet: list of LocalIpTranslationAclRule
        """
        self.DirectConnectGatewayId = None
        self.VpcId = None
        self.OriginalIp = None
        self.TranslationIp = None
        self.LocalIpTranslationAclRuleSet = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.VpcId = params.get("VpcId")
        self.OriginalIp = params.get("OriginalIp")
        self.TranslationIp = params.get("TranslationIp")
        if params.get("LocalIpTranslationAclRuleSet") is not None:
            self.LocalIpTranslationAclRuleSet = []
            for item in params.get("LocalIpTranslationAclRuleSet"):
                obj = LocalIpTranslationAclRule()
                obj._deserialize(item)
                self.LocalIpTranslationAclRuleSet.append(obj)


class CreateLocalIpTranslationAclRuleResponse(AbstractModel):
    """CreateLocalIpTranslationAclRule返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateLocalIpTranslationNatRuleRequest(AbstractModel):
    """CreateLocalIpTranslationNatRule请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID
        :type DirectConnectGatewayId: str
        :param VpcId: 字符型VPCID
        :type VpcId: str
        :param LocalIpTranslationNatRuleSet: 本端IP转换列表
        :type LocalIpTranslationNatRuleSet: list of LocalIpTranslationNatRule
        """
        self.DirectConnectGatewayId = None
        self.VpcId = None
        self.LocalIpTranslationNatRuleSet = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.VpcId = params.get("VpcId")
        if params.get("LocalIpTranslationNatRuleSet") is not None:
            self.LocalIpTranslationNatRuleSet = []
            for item in params.get("LocalIpTranslationNatRuleSet"):
                obj = LocalIpTranslationNatRule()
                obj._deserialize(item)
                self.LocalIpTranslationNatRuleSet.append(obj)


class CreateLocalIpTranslationNatRuleResponse(AbstractModel):
    """CreateLocalIpTranslationNatRule返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateLocalSourceIpPortTranslationAclRuleRequest(AbstractModel):
    """CreateLocalSourceIpPortTranslationAclRule请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID
        :type DirectConnectGatewayId: str
        :param VpcId: 字符型VPCID
        :type VpcId: str
        :param TranslationIpPool: IP池
        :type TranslationIpPool: str
        :param LocalSourceIpPortTranslationAclRuleSet: 本端源IP端口转换ACL列表
        :type LocalSourceIpPortTranslationAclRuleSet: list of LocalSourceIpPortTranslationAclRule
        """
        self.DirectConnectGatewayId = None
        self.VpcId = None
        self.TranslationIpPool = None
        self.LocalSourceIpPortTranslationAclRuleSet = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.VpcId = params.get("VpcId")
        self.TranslationIpPool = params.get("TranslationIpPool")
        if params.get("LocalSourceIpPortTranslationAclRuleSet") is not None:
            self.LocalSourceIpPortTranslationAclRuleSet = []
            for item in params.get("LocalSourceIpPortTranslationAclRuleSet"):
                obj = LocalSourceIpPortTranslationAclRule()
                obj._deserialize(item)
                self.LocalSourceIpPortTranslationAclRuleSet.append(obj)


class CreateLocalSourceIpPortTranslationAclRuleResponse(AbstractModel):
    """CreateLocalSourceIpPortTranslationAclRule返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateLocalSourceIpPortTranslationNatRuleRequest(AbstractModel):
    """CreateLocalSourceIpPortTranslationNatRule请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID
        :type DirectConnectGatewayId: str
        :param VpcId: 字符型VPCID
        :type VpcId: str
        :param LocalSourceIpPortTranslationNatRuleSet: 本端源IP端口转换列表
        :type LocalSourceIpPortTranslationNatRuleSet: list of LocalSourceIpPortTranslationNatRule
        """
        self.DirectConnectGatewayId = None
        self.VpcId = None
        self.LocalSourceIpPortTranslationNatRuleSet = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.VpcId = params.get("VpcId")
        if params.get("LocalSourceIpPortTranslationNatRuleSet") is not None:
            self.LocalSourceIpPortTranslationNatRuleSet = []
            for item in params.get("LocalSourceIpPortTranslationNatRuleSet"):
                obj = LocalSourceIpPortTranslationNatRule()
                obj._deserialize(item)
                self.LocalSourceIpPortTranslationNatRuleSet.append(obj)


class CreateLocalSourceIpPortTranslationNatRuleResponse(AbstractModel):
    """CreateLocalSourceIpPortTranslationNatRule返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateNatGatewayDestinationIpPortTranslationNatRuleRequest(AbstractModel):
    """CreateNatGatewayDestinationIpPortTranslationNatRule请求参数结构体"""

    def __init__(self):
        """
        :param NatGatewayId: NAT网关的ID，形如：`nat-df45454`。
        :type NatGatewayId: str
        :param DestinationIpPortTranslationNatRules: NAT网关的端口转换规则。
        :type DestinationIpPortTranslationNatRules: list of DestinationIpPortTranslationNatRule
        """
        self.NatGatewayId = None
        self.DestinationIpPortTranslationNatRules = None

    def _deserialize(self, params):
        self.NatGatewayId = params.get("NatGatewayId")
        if params.get("DestinationIpPortTranslationNatRules") is not None:
            self.DestinationIpPortTranslationNatRules = []
            for item in params.get("DestinationIpPortTranslationNatRules"):
                obj = DestinationIpPortTranslationNatRule()
                obj._deserialize(item)
                self.DestinationIpPortTranslationNatRules.append(obj)


class CreateNatGatewayDestinationIpPortTranslationNatRuleResponse(AbstractModel):
    """CreateNatGatewayDestinationIpPortTranslationNatRule返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateNatGatewayRequest(AbstractModel):
    """CreateNatGateway请求参数结构体"""

    def __init__(self):
        """
        :param NatGatewayName: NAT网关名称
        :type NatGatewayName: str
        :param VpcId: VPC实例ID。可通过DescribeVpcs接口返回值中的VpcId获取。
        :type VpcId: str
        :param InternetMaxBandwidthOut: NAT网关最大外网出带宽(单位:Mbps)，支持的参数值：`20, 50, 100, 200, 500, 1000, 2000, 5000`，默认: `100Mbps`。
        :type InternetMaxBandwidthOut: int
        :param MaxConcurrentConnection: NAT网关并发连接上限，支持参数值：`1000000、3000000、10000000`，默认值为`100000`。
        :type MaxConcurrentConnection: int
        :param AddressCount: 需要申请的弹性IP个数，系统会按您的要求生产N个弹性IP，其中AddressCount和PublicAddresses至少传递一个。
        :type AddressCount: int
        :param PublicIpAddresses: 绑定NAT网关的弹性IP数组，其中AddressCount和PublicAddresses至少传递一个。
        :type PublicIpAddresses: list of str
        :param Zone: 可用区，形如：`ap-guangzhou-1`。
        :type Zone: str
        :param Tags: 指定绑定的标签列表，例如：[{"Key": "city", "Value": "shanghai"}]
        :type Tags: list of Tag
        """
        self.NatGatewayName = None
        self.VpcId = None
        self.InternetMaxBandwidthOut = None
        self.MaxConcurrentConnection = None
        self.AddressCount = None
        self.PublicIpAddresses = None
        self.Zone = None
        self.Tags = None

    def _deserialize(self, params):
        self.NatGatewayName = params.get("NatGatewayName")
        self.VpcId = params.get("VpcId")
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        self.MaxConcurrentConnection = params.get("MaxConcurrentConnection")
        self.AddressCount = params.get("AddressCount")
        self.PublicIpAddresses = params.get("PublicIpAddresses")
        self.Zone = params.get("Zone")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)


class CreateNatGatewayResponse(AbstractModel):
    """CreateNatGateway返回参数结构体"""

    def __init__(self):
        """
        :param NatGatewaySet: NAT网关对象数组。
        :type NatGatewaySet: list of NatGateway
        :param TotalCount: 符合条件的 NAT网关对象数量。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.NatGatewaySet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("NatGatewaySet") is not None:
            self.NatGatewaySet = []
            for item in params.get("NatGatewaySet"):
                obj = NatGateway()
                obj._deserialize(item)
                self.NatGatewaySet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class CreateNetDetectRequest(AbstractModel):
    """CreateNetDetect请求参数结构体"""

    def __init__(self):
        """
                :param VpcId: `VPC`实例`ID`。形如：`vpc-12345678`
                :type VpcId: str
                :param SubnetId: 子网实例ID。形如：subnet-12345678。
                :type SubnetId: str
                :param NetDetectName: 网络探测名称，最大长度不能超过60个字节。
                :type NetDetectName: str
                :param DetectDestinationIp: 探测目的IPv4地址数组。最多两个。
                :type DetectDestinationIp: list of str
                :param NextHopType: 下一跳类型，目前我们支持的类型有：
        VPN：VPN网关；
        DIRECTCONNECT：专线网关；
        PEERCONNECTION：对等连接；
        NAT：NAT网关；
        NORMAL_CVM：普通云服务器；
                :type NextHopType: str
                :param NextHopDestination: 下一跳目的网关，取值与“下一跳类型”相关：
        下一跳类型为VPN，取值VPN网关ID，形如：vpngw-12345678；
        下一跳类型为DIRECTCONNECT，取值专线网关ID，形如：dcg-12345678；
        下一跳类型为PEERCONNECTION，取值对等连接ID，形如：pcx-12345678；
        下一跳类型为NAT，取值Nat网关，形如：nat-12345678；
        下一跳类型为NORMAL_CVM，取值云服务器IPv4地址，形如：10.0.0.12；
                :type NextHopDestination: str
                :param NetDetectDescription: 网络探测描述。
                :type NetDetectDescription: str
        """
        self.VpcId = None
        self.SubnetId = None
        self.NetDetectName = None
        self.DetectDestinationIp = None
        self.NextHopType = None
        self.NextHopDestination = None
        self.NetDetectDescription = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.NetDetectName = params.get("NetDetectName")
        self.DetectDestinationIp = params.get("DetectDestinationIp")
        self.NextHopType = params.get("NextHopType")
        self.NextHopDestination = params.get("NextHopDestination")
        self.NetDetectDescription = params.get("NetDetectDescription")


class CreateNetDetectResponse(AbstractModel):
    """CreateNetDetect返回参数结构体"""

    def __init__(self):
        """
        :param NetDetect: 网络探测（NetDetect）对象。
        :type NetDetect: :class:`tcecloud.vpc.v20170312.models.NetDetect`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.NetDetect = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("NetDetect") is not None:
            self.NetDetect = NetDetect()
            self.NetDetect._deserialize(params.get("NetDetect"))
        self.RequestId = params.get("RequestId")


class CreateNetworkAclRequest(AbstractModel):
    """CreateNetworkAcl请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: VPC实例ID。可通过DescribeVpcs接口返回值中的VpcId获取。
        :type VpcId: str
        :param NetworkAclName: 网络ACL名称，最大长度不能超过60个字节。
        :type NetworkAclName: str
        """
        self.VpcId = None
        self.NetworkAclName = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.NetworkAclName = params.get("NetworkAclName")


class CreateNetworkAclResponse(AbstractModel):
    """CreateNetworkAcl返回参数结构体"""

    def __init__(self):
        """
        :param NetworkAcl: 网络ACL实例。
        :type NetworkAcl: :class:`tcecloud.vpc.v20170312.models.NetworkAcl`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.NetworkAcl = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("NetworkAcl") is not None:
            self.NetworkAcl = NetworkAcl()
            self.NetworkAcl._deserialize(params.get("NetworkAcl"))
        self.RequestId = params.get("RequestId")


class CreateNetworkInterfaceExRequest(AbstractModel):
    """CreateNetworkInterfaceEx请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: VPC实例ID。可通过DescribeVpcs接口返回值中的VpcId获取。
        :type VpcId: str
        :param NetworkInterfaceName: 弹性网卡名称，最大长度不能超过60个字节。
        :type NetworkInterfaceName: str
        :param InstanceId: 云服务实例ID。
        :type InstanceId: str
        :param NetworkInterfaceDescription: 弹性网卡描述，可任意命名，但不得超过60个字符。
        :type NetworkInterfaceDescription: str
        :param IsReservedAddress: 是否保留网段分配IP，默认为true；当ReservedAddress=false时，需要指定SubnetId。
        :type IsReservedAddress: bool
        :param SubnetId: 弹性网卡所在的子网实例ID，例如：subnet-0ap8nwca。
        :type SubnetId: str
        :param Business: 业务标识，默认为dockerMaster。
        :type Business: str
        :param BusinessOwner: 业务所属项目，默认为Docker。
        :type BusinessOwner: str
        :param IsCrossTenant: 是否跨租户创建网卡。默认为true。
        :type IsCrossTenant: bool
        :param PrivateIpAddresses: 指定的内网IP信息，单次最多指定10个。
        :type PrivateIpAddresses: list of PrivateIpAddressSpecification
        """
        self.VpcId = None
        self.NetworkInterfaceName = None
        self.InstanceId = None
        self.NetworkInterfaceDescription = None
        self.IsReservedAddress = None
        self.SubnetId = None
        self.Business = None
        self.BusinessOwner = None
        self.IsCrossTenant = None
        self.PrivateIpAddresses = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.NetworkInterfaceName = params.get("NetworkInterfaceName")
        self.InstanceId = params.get("InstanceId")
        self.NetworkInterfaceDescription = params.get("NetworkInterfaceDescription")
        self.IsReservedAddress = params.get("IsReservedAddress")
        self.SubnetId = params.get("SubnetId")
        self.Business = params.get("Business")
        self.BusinessOwner = params.get("BusinessOwner")
        self.IsCrossTenant = params.get("IsCrossTenant")
        if params.get("PrivateIpAddresses") is not None:
            self.PrivateIpAddresses = []
            for item in params.get("PrivateIpAddresses"):
                obj = PrivateIpAddressSpecification()
                obj._deserialize(item)
                self.PrivateIpAddresses.append(obj)


class CreateNetworkInterfaceExResponse(AbstractModel):
    """CreateNetworkInterfaceEx返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateNetworkInterfaceRequest(AbstractModel):
    """CreateNetworkInterface请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: VPC实例ID。可通过DescribeVpcs接口返回值中的VpcId获取。
        :type VpcId: str
        :param NetworkInterfaceName: 弹性网卡名称，最大长度不能超过60个字节。
        :type NetworkInterfaceName: str
        :param SubnetId: 弹性网卡所在的子网实例ID，例如：subnet-0ap8nwca。
        :type SubnetId: str
        :param NetworkInterfaceDescription: 弹性网卡描述，可任意命名，但不得超过60个字符。
        :type NetworkInterfaceDescription: str
        :param SecondaryPrivateIpAddressCount: 新申请的内网IP地址个数，内网IP地址个数总和不能超过配数。
        :type SecondaryPrivateIpAddressCount: int
        :param SecurityGroupIds: 指定绑定的安全组，例如：['sg-1dd51d']。
        :type SecurityGroupIds: list of str
        :param PrivateIpAddresses: 指定的内网IP信息，单次最多指定10个。
        :type PrivateIpAddresses: list of PrivateIpAddressSpecification
        :param Tags: 指定绑定的标签列表，例如：[{"Key": "city", "Value": "shanghai"}]
        :type Tags: list of Tag
        """
        self.VpcId = None
        self.NetworkInterfaceName = None
        self.SubnetId = None
        self.NetworkInterfaceDescription = None
        self.SecondaryPrivateIpAddressCount = None
        self.SecurityGroupIds = None
        self.PrivateIpAddresses = None
        self.Tags = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.NetworkInterfaceName = params.get("NetworkInterfaceName")
        self.SubnetId = params.get("SubnetId")
        self.NetworkInterfaceDescription = params.get("NetworkInterfaceDescription")
        self.SecondaryPrivateIpAddressCount = params.get("SecondaryPrivateIpAddressCount")
        self.SecurityGroupIds = params.get("SecurityGroupIds")
        if params.get("PrivateIpAddresses") is not None:
            self.PrivateIpAddresses = []
            for item in params.get("PrivateIpAddresses"):
                obj = PrivateIpAddressSpecification()
                obj._deserialize(item)
                self.PrivateIpAddresses.append(obj)
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)


class CreateNetworkInterfaceResponse(AbstractModel):
    """CreateNetworkInterface返回参数结构体"""

    def __init__(self):
        """
        :param NetworkInterface: 弹性网卡实例。
        :type NetworkInterface: :class:`tcecloud.vpc.v20170312.models.NetworkInterface`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.NetworkInterface = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("NetworkInterface") is not None:
            self.NetworkInterface = NetworkInterface()
            self.NetworkInterface._deserialize(params.get("NetworkInterface"))
        self.RequestId = params.get("RequestId")


class CreatePeerIpTranslationNatRuleRequest(AbstractModel):
    """CreatePeerIpTranslationNatRule请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID
        :type DirectConnectGatewayId: str
        :param VpcId: 字符型VPCID
        :type VpcId: str
        :param PeerIpTranslationNatRuleSet: 对端IP转换列表
        :type PeerIpTranslationNatRuleSet: list of LocalIpTranslationNatRule
        """
        self.DirectConnectGatewayId = None
        self.VpcId = None
        self.PeerIpTranslationNatRuleSet = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.VpcId = params.get("VpcId")
        if params.get("PeerIpTranslationNatRuleSet") is not None:
            self.PeerIpTranslationNatRuleSet = []
            for item in params.get("PeerIpTranslationNatRuleSet"):
                obj = LocalIpTranslationNatRule()
                obj._deserialize(item)
                self.PeerIpTranslationNatRuleSet.append(obj)


class CreatePeerIpTranslationNatRuleResponse(AbstractModel):
    """CreatePeerIpTranslationNatRule返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateRouteTableRequest(AbstractModel):
    """CreateRouteTable请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: 待操作的VPC实例ID。可通过DescribeVpcs接口返回值中的VpcId获取。
        :type VpcId: str
        :param RouteTableName: 路由表名称，最大长度不能超过60个字节。
        :type RouteTableName: str
        :param Tags: 指定绑定的标签列表，例如：[{"Key": "city", "Value": "shanghai"}]
        :type Tags: list of Tag
        """
        self.VpcId = None
        self.RouteTableName = None
        self.Tags = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.RouteTableName = params.get("RouteTableName")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)


class CreateRouteTableResponse(AbstractModel):
    """CreateRouteTable返回参数结构体"""

    def __init__(self):
        """
        :param RouteTable: 路由表对象。
        :type RouteTable: :class:`tcecloud.vpc.v20170312.models.RouteTable`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RouteTable = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("RouteTable") is not None:
            self.RouteTable = RouteTable()
            self.RouteTable._deserialize(params.get("RouteTable"))
        self.RequestId = params.get("RequestId")


class CreateRoutesRequest(AbstractModel):
    """CreateRoutes请求参数结构体"""

    def __init__(self):
        """
        :param RouteTableId: 路由表实例ID。
        :type RouteTableId: str
        :param Routes: 路由策略对象。
        :type Routes: list of Route
        """
        self.RouteTableId = None
        self.Routes = None

    def _deserialize(self, params):
        self.RouteTableId = params.get("RouteTableId")
        if params.get("Routes") is not None:
            self.Routes = []
            for item in params.get("Routes"):
                obj = Route()
                obj._deserialize(item)
                self.Routes.append(obj)


class CreateRoutesResponse(AbstractModel):
    """CreateRoutes返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 新增的实例个数。
        :type TotalCount: int
        :param RouteTableSet: 路由表对象。
        :type RouteTableSet: list of RouteTable
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.RouteTableSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("RouteTableSet") is not None:
            self.RouteTableSet = []
            for item in params.get("RouteTableSet"):
                obj = RouteTable()
                obj._deserialize(item)
                self.RouteTableSet.append(obj)
        self.RequestId = params.get("RequestId")


class CreateSecurityGroupPoliciesRequest(AbstractModel):
    """CreateSecurityGroupPolicies请求参数结构体"""

    def __init__(self):
        """
        :param SecurityGroupId: 安全组实例ID，例如sg-33ocnj9n，可通过DescribeSecurityGroups获取。
        :type SecurityGroupId: str
        :param SecurityGroupPolicySet: 安全组规则集合。
        :type SecurityGroupPolicySet: :class:`tcecloud.vpc.v20170312.models.SecurityGroupPolicySet`
        """
        self.SecurityGroupId = None
        self.SecurityGroupPolicySet = None

    def _deserialize(self, params):
        self.SecurityGroupId = params.get("SecurityGroupId")
        if params.get("SecurityGroupPolicySet") is not None:
            self.SecurityGroupPolicySet = SecurityGroupPolicySet()
            self.SecurityGroupPolicySet._deserialize(params.get("SecurityGroupPolicySet"))


class CreateSecurityGroupPoliciesResponse(AbstractModel):
    """CreateSecurityGroupPolicies返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateSecurityGroupRequest(AbstractModel):
    """CreateSecurityGroup请求参数结构体"""

    def __init__(self):
        """
        :param GroupName: 安全组名称，可任意命名，但不得超过60个字符。
        :type GroupName: str
        :param GroupDescription: 安全组备注，最多100个字符。
        :type GroupDescription: str
        :param ProjectId: 项目ID，默认0。可在qcloud控制台项目管理页面查询到。
        :type ProjectId: str
        :param Tags: 指定绑定的标签列表，例如：[{"Key": "city", "Value": "shanghai"}]
        :type Tags: list of Tag
        """
        self.GroupName = None
        self.GroupDescription = None
        self.ProjectId = None
        self.Tags = None

    def _deserialize(self, params):
        self.GroupName = params.get("GroupName")
        self.GroupDescription = params.get("GroupDescription")
        self.ProjectId = params.get("ProjectId")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)


class CreateSecurityGroupResponse(AbstractModel):
    """CreateSecurityGroup返回参数结构体"""

    def __init__(self):
        """
        :param SecurityGroup: 安全组对象。
        :type SecurityGroup: :class:`tcecloud.vpc.v20170312.models.SecurityGroup`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SecurityGroup = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("SecurityGroup") is not None:
            self.SecurityGroup = SecurityGroup()
            self.SecurityGroup._deserialize(params.get("SecurityGroup"))
        self.RequestId = params.get("RequestId")


class CreateSecurityGroupWithPoliciesRequest(AbstractModel):
    """CreateSecurityGroupWithPolicies请求参数结构体"""

    def __init__(self):
        """
        :param GroupName: 安全组名称，可任意命名，但不得超过60个字符。
        :type GroupName: str
        :param GroupDescription: 安全组备注，最多100个字符。
        :type GroupDescription: str
        :param ProjectId: 项目ID，默认0。可在qcloud控制台项目管理页面查询到。
        :type ProjectId: str
        :param SecurityGroupPolicySet: 安全组规则集合。
        :type SecurityGroupPolicySet: :class:`tcecloud.vpc.v20170312.models.SecurityGroupPolicySet`
        """
        self.GroupName = None
        self.GroupDescription = None
        self.ProjectId = None
        self.SecurityGroupPolicySet = None

    def _deserialize(self, params):
        self.GroupName = params.get("GroupName")
        self.GroupDescription = params.get("GroupDescription")
        self.ProjectId = params.get("ProjectId")
        if params.get("SecurityGroupPolicySet") is not None:
            self.SecurityGroupPolicySet = SecurityGroupPolicySet()
            self.SecurityGroupPolicySet._deserialize(params.get("SecurityGroupPolicySet"))


class CreateSecurityGroupWithPoliciesResponse(AbstractModel):
    """CreateSecurityGroupWithPolicies返回参数结构体"""

    def __init__(self):
        """
        :param SecurityGroup: 安全组对象。
        :type SecurityGroup: :class:`tcecloud.vpc.v20170312.models.SecurityGroup`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SecurityGroup = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("SecurityGroup") is not None:
            self.SecurityGroup = SecurityGroup()
            self.SecurityGroup._deserialize(params.get("SecurityGroup"))
        self.RequestId = params.get("RequestId")


class CreateServiceTemplateGroupRequest(AbstractModel):
    """CreateServiceTemplateGroup请求参数结构体"""

    def __init__(self):
        """
        :param ServiceTemplateGroupName: 协议端口模板集合名称
        :type ServiceTemplateGroupName: str
        :param ServiceTemplateIds: 协议端口模板实例ID，例如：ppm-4dw6agho。
        :type ServiceTemplateIds: list of str
        """
        self.ServiceTemplateGroupName = None
        self.ServiceTemplateIds = None

    def _deserialize(self, params):
        self.ServiceTemplateGroupName = params.get("ServiceTemplateGroupName")
        self.ServiceTemplateIds = params.get("ServiceTemplateIds")


class CreateServiceTemplateGroupResponse(AbstractModel):
    """CreateServiceTemplateGroup返回参数结构体"""

    def __init__(self):
        """
        :param ServiceTemplateGroup: 协议端口模板集合对象。
        :type ServiceTemplateGroup: :class:`tcecloud.vpc.v20170312.models.ServiceTemplateGroup`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ServiceTemplateGroup = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("ServiceTemplateGroup") is not None:
            self.ServiceTemplateGroup = ServiceTemplateGroup()
            self.ServiceTemplateGroup._deserialize(params.get("ServiceTemplateGroup"))
        self.RequestId = params.get("RequestId")


class CreateServiceTemplateRequest(AbstractModel):
    """CreateServiceTemplate请求参数结构体"""

    def __init__(self):
        """
        :param ServiceTemplateName: 协议端口模板名称
        :type ServiceTemplateName: str
        :param Services: 支持单个端口、多个端口、连续端口及所有端口，协议支持：TCP、UDP、ICMP、GRE 协议。
        :type Services: list of str
        """
        self.ServiceTemplateName = None
        self.Services = None

    def _deserialize(self, params):
        self.ServiceTemplateName = params.get("ServiceTemplateName")
        self.Services = params.get("Services")


class CreateServiceTemplateResponse(AbstractModel):
    """CreateServiceTemplate返回参数结构体"""

    def __init__(self):
        """
        :param ServiceTemplate: 协议端口模板对象。
        :type ServiceTemplate: :class:`tcecloud.vpc.v20170312.models.ServiceTemplate`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ServiceTemplate = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("ServiceTemplate") is not None:
            self.ServiceTemplate = ServiceTemplate()
            self.ServiceTemplate._deserialize(params.get("ServiceTemplate"))
        self.RequestId = params.get("RequestId")


class CreateSubnetRequest(AbstractModel):
    """CreateSubnet请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: 待操作的VPC实例ID。可通过DescribeVpcs接口返回值中的VpcId获取。
        :type VpcId: str
        :param SubnetName: 子网名称，最大长度不能超过60个字节。
        :type SubnetName: str
        :param CidrBlock: 子网网段，子网网段必须在VPC网段内，相同VPC内子网网段不能重叠。
        :type CidrBlock: str
        :param Zone: 子网所在的可用区ID，不同子网选择不同可用区可以做跨可用区灾备。
        :type Zone: str
        :param Tags: 指定绑定的标签列表，例如：[{"Key": "city", "Value": "shanghai"}]
        :type Tags: list of Tag
        """
        self.VpcId = None
        self.SubnetName = None
        self.CidrBlock = None
        self.Zone = None
        self.Tags = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.SubnetName = params.get("SubnetName")
        self.CidrBlock = params.get("CidrBlock")
        self.Zone = params.get("Zone")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)


class CreateSubnetResponse(AbstractModel):
    """CreateSubnet返回参数结构体"""

    def __init__(self):
        """
        :param Subnet: 子网对象。
        :type Subnet: :class:`tcecloud.vpc.v20170312.models.Subnet`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Subnet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Subnet") is not None:
            self.Subnet = Subnet()
            self.Subnet._deserialize(params.get("Subnet"))
        self.RequestId = params.get("RequestId")


class CreateSubnetsRequest(AbstractModel):
    """CreateSubnets请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: `VPC`实例`ID`。形如：`vpc-6v2ht8q5`
        :type VpcId: str
        :param Subnets: 子网对象列表。
        :type Subnets: list of SubnetInput
        :param Tags: 指定绑定的标签列表，注意这里的标签集合为列表中所有子网对象所共享，不能为每个子网对象单独指定标签，例如：[{"Key": "city", "Value": "shanghai"}]
        :type Tags: list of Tag
        """
        self.VpcId = None
        self.Subnets = None
        self.Tags = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        if params.get("Subnets") is not None:
            self.Subnets = []
            for item in params.get("Subnets"):
                obj = SubnetInput()
                obj._deserialize(item)
                self.Subnets.append(obj)
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)


class CreateSubnetsResponse(AbstractModel):
    """CreateSubnets返回参数结构体"""

    def __init__(self):
        """
        :param SubnetSet: 新创建的子网列表。
        :type SubnetSet: list of Subnet
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SubnetSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("SubnetSet") is not None:
            self.SubnetSet = []
            for item in params.get("SubnetSet"):
                obj = Subnet()
                obj._deserialize(item)
                self.SubnetSet.append(obj)
        self.RequestId = params.get("RequestId")


class CreateTrafficMirrorRequest(AbstractModel):
    """CreateTrafficMirror请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: VPC实例ID
        :type VpcId: str
        :param TrafficMirrorName: 流量镜像名字
        :type TrafficMirrorName: str
        :param Direction: 流量镜像采集方向，支持EGRESS/INGRESS/ALL
        :type Direction: str
        :param CollectorTarget: 流量镜像的目的地址
        :type CollectorTarget: :class:`tcecloud.vpc.v20170312.models.TrafficMirrorTarget`
        :param TrafficMirrorDescribe: 流量镜像描述
        :type TrafficMirrorDescribe: str
        :param State: 流量镜像状态, 支持RUNNING/STOPED
        :type State: str
        :param CollectorSrcs: 流量镜像的采集对象，支持vpc_xxxx, subnet_xxxx, eni_xxxx
        :type CollectorSrcs: list of str
        :param NatId: 流量镜像过滤的natgw实例
        :type NatId: str
        :param CollectorNormalFilters: 需要过滤的五元组规则
        :type CollectorNormalFilters: list of TrafficMirrorFilter
        """
        self.VpcId = None
        self.TrafficMirrorName = None
        self.Direction = None
        self.CollectorTarget = None
        self.TrafficMirrorDescribe = None
        self.State = None
        self.CollectorSrcs = None
        self.NatId = None
        self.CollectorNormalFilters = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.TrafficMirrorName = params.get("TrafficMirrorName")
        self.Direction = params.get("Direction")
        if params.get("CollectorTarget") is not None:
            self.CollectorTarget = TrafficMirrorTarget()
            self.CollectorTarget._deserialize(params.get("CollectorTarget"))
        self.TrafficMirrorDescribe = params.get("TrafficMirrorDescribe")
        self.State = params.get("State")
        self.CollectorSrcs = params.get("CollectorSrcs")
        self.NatId = params.get("NatId")
        if params.get("CollectorNormalFilters") is not None:
            self.CollectorNormalFilters = []
            for item in params.get("CollectorNormalFilters"):
                obj = TrafficMirrorFilter()
                obj._deserialize(item)
                self.CollectorNormalFilters.append(obj)


class CreateTrafficMirrorResponse(AbstractModel):
    """CreateTrafficMirror返回参数结构体"""

    def __init__(self):
        """
        :param TrafficMirror: 流量镜像实例
        :type TrafficMirror: :class:`tcecloud.vpc.v20170312.models.TrafficMirror`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TrafficMirror = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("TrafficMirror") is not None:
            self.TrafficMirror = TrafficMirror()
            self.TrafficMirror._deserialize(params.get("TrafficMirror"))
        self.RequestId = params.get("RequestId")


class CreateTrafficPackagesRequest(AbstractModel):
    """CreateTrafficPackages请求参数结构体"""

    def __init__(self):
        """
        :param TrafficAmount: 流量包规格。
        :type TrafficAmount: int
        :param TrafficPackageCount: 流量包数量。
        :type TrafficPackageCount: int
        """
        self.TrafficAmount = None
        self.TrafficPackageCount = None

    def _deserialize(self, params):
        self.TrafficAmount = params.get("TrafficAmount")
        self.TrafficPackageCount = params.get("TrafficPackageCount")


class CreateTrafficPackagesResponse(AbstractModel):
    """CreateTrafficPackages返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateVpcRequest(AbstractModel):
    """CreateVpc请求参数结构体"""

    def __init__(self):
        """
        :param VpcName: vpc名称，最大长度不能超过60个字节。
        :type VpcName: str
        :param CidrBlock: vpc的cidr，只能为10.0.0.0/16，172.16.0.0/16，192.168.0.0/16这三个内网网段内。
        :type CidrBlock: str
        :param EnableMulticast: 是否开启组播。true: 开启, false: 不开启。
        :type EnableMulticast: str
        :param DnsServers: DNS地址，最多支持4个
        :type DnsServers: list of str
        :param DomainName: 域名
        :type DomainName: str
        :param Tags: 指定绑定的标签列表，例如：[{"Key": "city", "Value": "shanghai"}]
        :type Tags: list of Tag
        """
        self.VpcName = None
        self.CidrBlock = None
        self.EnableMulticast = None
        self.DnsServers = None
        self.DomainName = None
        self.Tags = None

    def _deserialize(self, params):
        self.VpcName = params.get("VpcName")
        self.CidrBlock = params.get("CidrBlock")
        self.EnableMulticast = params.get("EnableMulticast")
        self.DnsServers = params.get("DnsServers")
        self.DomainName = params.get("DomainName")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)


class CreateVpcResponse(AbstractModel):
    """CreateVpc返回参数结构体"""

    def __init__(self):
        """
        :param Vpc: Vpc对象。
        :type Vpc: :class:`tcecloud.vpc.v20170312.models.Vpc`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Vpc = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Vpc") is not None:
            self.Vpc = Vpc()
            self.Vpc._deserialize(params.get("Vpc"))
        self.RequestId = params.get("RequestId")


class CreateVpnConnectionRequest(AbstractModel):
    """CreateVpnConnection请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: VPC实例ID。可通过DescribeVpcs接口返回值中的VpcId获取。
        :type VpcId: str
        :param VpnGatewayId: VPN网关实例ID。
        :type VpnGatewayId: str
        :param CustomerGatewayId: 对端网关ID，例如：cgw-2wqq41m9，可通过DescribeCustomerGateways接口查询对端网关。
        :type CustomerGatewayId: str
        :param VpnConnectionName: 通道名称，可任意命名，但不得超过60个字符。
        :type VpnConnectionName: str
        :param PreShareKey: 预共享密钥。
        :type PreShareKey: str
        :param SecurityPolicyDatabases: SPD策略组，例如：{"10.0.0.5/24":["172.123.10.5/16"]}，10.0.0.5/24是vpc内网段172.123.10.5/16是IDC网段。用户指定VPC内哪些网段可以和您IDC中哪些网段通信。
        :type SecurityPolicyDatabases: list of SecurityPolicyDatabase
        :param IKEOptionsSpecification: IKE配置（Internet Key Exchange，因特网密钥交换），IKE具有一套自我保护机制，用户配置网络安全协议
        :type IKEOptionsSpecification: :class:`tcecloud.vpc.v20170312.models.IKEOptionsSpecification`
        :param IPSECOptionsSpecification: IPSec配置，Tce提供IPSec安全会话设置
        :type IPSECOptionsSpecification: :class:`tcecloud.vpc.v20170312.models.IPSECOptionsSpecification`
        """
        self.VpcId = None
        self.VpnGatewayId = None
        self.CustomerGatewayId = None
        self.VpnConnectionName = None
        self.PreShareKey = None
        self.SecurityPolicyDatabases = None
        self.IKEOptionsSpecification = None
        self.IPSECOptionsSpecification = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.VpnGatewayId = params.get("VpnGatewayId")
        self.CustomerGatewayId = params.get("CustomerGatewayId")
        self.VpnConnectionName = params.get("VpnConnectionName")
        self.PreShareKey = params.get("PreShareKey")
        if params.get("SecurityPolicyDatabases") is not None:
            self.SecurityPolicyDatabases = []
            for item in params.get("SecurityPolicyDatabases"):
                obj = SecurityPolicyDatabase()
                obj._deserialize(item)
                self.SecurityPolicyDatabases.append(obj)
        if params.get("IKEOptionsSpecification") is not None:
            self.IKEOptionsSpecification = IKEOptionsSpecification()
            self.IKEOptionsSpecification._deserialize(params.get("IKEOptionsSpecification"))
        if params.get("IPSECOptionsSpecification") is not None:
            self.IPSECOptionsSpecification = IPSECOptionsSpecification()
            self.IPSECOptionsSpecification._deserialize(params.get("IPSECOptionsSpecification"))


class CreateVpnConnectionResponse(AbstractModel):
    """CreateVpnConnection返回参数结构体"""

    def __init__(self):
        """
        :param VpnConnection: 通道实例对象。
        :type VpnConnection: :class:`tcecloud.vpc.v20170312.models.VpnConnection`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.VpnConnection = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("VpnConnection") is not None:
            self.VpnConnection = VpnConnection()
            self.VpnConnection._deserialize(params.get("VpnConnection"))
        self.RequestId = params.get("RequestId")


class CreateVpnGatewayRequest(AbstractModel):
    """CreateVpnGateway请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: VPC实例ID。可通过DescribeVpcs接口返回值中的VpcId获取。
        :type VpcId: str
        :param VpnGatewayName: VPN网关名称，最大长度不能超过60个字节。
        :type VpnGatewayName: str
        :param InternetMaxBandwidthOut: 公网带宽设置。可选带宽规格：5, 10, 20, 50, 100；单位：Mbps
        :type InternetMaxBandwidthOut: int
        :param InstanceChargeType: VPN网关计费模式，PREPAID：表示预付费，即包年包月，POSTPAID_BY_HOUR：表示后付费，即按量计费。默认：POSTPAID_BY_HOUR，如果指定预付费模式，参数InstanceChargePrepaid必填。
        :type InstanceChargeType: str
        :param InstanceChargePrepaid: 预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月实例的购买时长、是否设置自动续费等属性。若指定实例的付费模式为预付费则该参数必传。
        :type InstanceChargePrepaid: :class:`tcecloud.vpc.v20170312.models.InstanceChargePrepaid`
        :param Zone: 可用区，如：ap-guangzhou-2。
        :type Zone: str
        :param Type: VPN网关类型。值“CCN”云联网类型VPN网关
        :type Type: str
        """
        self.VpcId = None
        self.VpnGatewayName = None
        self.InternetMaxBandwidthOut = None
        self.InstanceChargeType = None
        self.InstanceChargePrepaid = None
        self.Zone = None
        self.Type = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.VpnGatewayName = params.get("VpnGatewayName")
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        self.InstanceChargeType = params.get("InstanceChargeType")
        if params.get("InstanceChargePrepaid") is not None:
            self.InstanceChargePrepaid = InstanceChargePrepaid()
            self.InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))
        self.Zone = params.get("Zone")
        self.Type = params.get("Type")


class CreateVpnGatewayResponse(AbstractModel):
    """CreateVpnGateway返回参数结构体"""

    def __init__(self):
        """
        :param VpnGateway: VPN网关对象
        :type VpnGateway: :class:`tcecloud.vpc.v20170312.models.VpnGateway`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.VpnGateway = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("VpnGateway") is not None:
            self.VpnGateway = VpnGateway()
            self.VpnGateway._deserialize(params.get("VpnGateway"))
        self.RequestId = params.get("RequestId")


class CustomerGateway(AbstractModel):
    """对端网关"""

    def __init__(self):
        """
        :param CustomerGatewayId: 用户网关唯一ID
        :type CustomerGatewayId: str
        :param CustomerGatewayName: 网关名称
        :type CustomerGatewayName: str
        :param IpAddress: 公网地址
        :type IpAddress: str
        :param CreatedTime: 创建时间
        :type CreatedTime: str
        """
        self.CustomerGatewayId = None
        self.CustomerGatewayName = None
        self.IpAddress = None
        self.CreatedTime = None

    def _deserialize(self, params):
        self.CustomerGatewayId = params.get("CustomerGatewayId")
        self.CustomerGatewayName = params.get("CustomerGatewayName")
        self.IpAddress = params.get("IpAddress")
        self.CreatedTime = params.get("CreatedTime")


class CustomerGatewayVendor(AbstractModel):
    """对端网关厂商信息对象。"""

    def __init__(self):
        """
        :param Platform: 平台。
        :type Platform: str
        :param SoftwareVersion: 软件版本。
        :type SoftwareVersion: str
        :param VendorName: 供应商名称。
        :type VendorName: str
        """
        self.Platform = None
        self.SoftwareVersion = None
        self.VendorName = None

    def _deserialize(self, params):
        self.Platform = params.get("Platform")
        self.SoftwareVersion = params.get("SoftwareVersion")
        self.VendorName = params.get("VendorName")


class CvmInstance(AbstractModel):
    """云主机实例信息。"""

    def __init__(self):
        """
        :param VpcId: VPC实例ID。
        :type VpcId: str
        :param SubnetId: 子网实例ID。
        :type SubnetId: str
        :param InstanceId: 云主机实例ID
        :type InstanceId: str
        :param InstanceName: 云主机名称。
        :type InstanceName: str
        :param InstanceState: 云主机状态。
        :type InstanceState: str
        :param CPU: 实例的CPU核数，单位：核。
        :type CPU: int
        :param Memory: 实例内存容量，单位：GB。
        :type Memory: int
        :param CreatedTime: 创建时间。
        :type CreatedTime: str
        :param InstanceType: 实例机型。
        :type InstanceType: str
        :param EniLimit: 实例弹性网卡配额（包含主网卡）。
        :type EniLimit: int
        :param EniIpLimit: 实例弹性网卡内网IP配额（包含主网卡）。
        :type EniIpLimit: int
        :param InstanceEniCount: 实例已绑定弹性网卡的个数（包含主网卡）。
        :type InstanceEniCount: int
        """
        self.VpcId = None
        self.SubnetId = None
        self.InstanceId = None
        self.InstanceName = None
        self.InstanceState = None
        self.CPU = None
        self.Memory = None
        self.CreatedTime = None
        self.InstanceType = None
        self.EniLimit = None
        self.EniIpLimit = None
        self.InstanceEniCount = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.InstanceState = params.get("InstanceState")
        self.CPU = params.get("CPU")
        self.Memory = params.get("Memory")
        self.CreatedTime = params.get("CreatedTime")
        self.InstanceType = params.get("InstanceType")
        self.EniLimit = params.get("EniLimit")
        self.EniIpLimit = params.get("EniIpLimit")
        self.InstanceEniCount = params.get("InstanceEniCount")


class DefaultVpcSubnet(AbstractModel):
    """默认VPC和子网"""

    def __init__(self):
        """
        :param VpcId: 默认VpcId
        :type VpcId: str
        :param SubnetId: 默认SubnetId
        :type SubnetId: str
        """
        self.VpcId = None
        self.SubnetId = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")


class DeleteAddressTemplateGroupRequest(AbstractModel):
    """DeleteAddressTemplateGroup请求参数结构体"""

    def __init__(self):
        """
        :param AddressTemplateGroupId: IP地址模板集合实例ID，例如：ipmg-90cex8mq。
        :type AddressTemplateGroupId: str
        """
        self.AddressTemplateGroupId = None

    def _deserialize(self, params):
        self.AddressTemplateGroupId = params.get("AddressTemplateGroupId")


class DeleteAddressTemplateGroupResponse(AbstractModel):
    """DeleteAddressTemplateGroup返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteAddressTemplateRequest(AbstractModel):
    """DeleteAddressTemplate请求参数结构体"""

    def __init__(self):
        """
        :param AddressTemplateId: IP地址模板实例ID，例如：ipm-09o5m8kc。
        :type AddressTemplateId: str
        """
        self.AddressTemplateId = None

    def _deserialize(self, params):
        self.AddressTemplateId = params.get("AddressTemplateId")


class DeleteAddressTemplateResponse(AbstractModel):
    """DeleteAddressTemplate返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteAssistantCidrRequest(AbstractModel):
    """DeleteAssistantCidr请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: `VPC`实例`ID`。形如：`vpc-6v2ht8q5`
        :type VpcId: str
        :param CidrBlocks: CIDR数组，格式如["10.0.0.0/16", "172.16.0.0/16"]
        :type CidrBlocks: list of str
        """
        self.VpcId = None
        self.CidrBlocks = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.CidrBlocks = params.get("CidrBlocks")


class DeleteAssistantCidrResponse(AbstractModel):
    """DeleteAssistantCidr返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteBandwidthPackageRequest(AbstractModel):
    """DeleteBandwidthPackage请求参数结构体"""

    def __init__(self):
        """
        :param BandwidthPackageId: 待删除带宽包唯一ID
        :type BandwidthPackageId: str
        """
        self.BandwidthPackageId = None

    def _deserialize(self, params):
        self.BandwidthPackageId = params.get("BandwidthPackageId")


class DeleteBandwidthPackageResponse(AbstractModel):
    """DeleteBandwidthPackage返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteCcnRegionBandwidthLimitsRequest(AbstractModel):
    """DeleteCcnRegionBandwidthLimits请求参数结构体"""

    def __init__(self):
        """
        :param RegionFlowControlIds: 限速实例的ID。
        :type RegionFlowControlIds: list of str
        """
        self.RegionFlowControlIds = None

    def _deserialize(self, params):
        self.RegionFlowControlIds = params.get("RegionFlowControlIds")


class DeleteCcnRegionBandwidthLimitsResponse(AbstractModel):
    """DeleteCcnRegionBandwidthLimits返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteCcnRequest(AbstractModel):
    """DeleteCcn请求参数结构体"""

    def __init__(self):
        """
        :param CcnId: CCN实例ID。形如：ccn-f49l6u0z。
        :type CcnId: str
        """
        self.CcnId = None

    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")


class DeleteCcnResponse(AbstractModel):
    """DeleteCcn返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteCustomerGatewayRequest(AbstractModel):
    """DeleteCustomerGateway请求参数结构体"""

    def __init__(self):
        """
        :param CustomerGatewayId: 对端网关ID，例如：cgw-2wqq41m9，可通过DescribeCustomerGateways接口查询对端网关。
        :type CustomerGatewayId: str
        """
        self.CustomerGatewayId = None

    def _deserialize(self, params):
        self.CustomerGatewayId = params.get("CustomerGatewayId")


class DeleteCustomerGatewayResponse(AbstractModel):
    """DeleteCustomerGateway返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteDirectConnectGatewayCcnRoutesRequest(AbstractModel):
    """DeleteDirectConnectGatewayCcnRoutes请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID，形如：dcg-prpqlmg1
        :type DirectConnectGatewayId: str
        :param RouteIds: 路由ID。形如：ccnr-f49l6u0z。
        :type RouteIds: list of str
        """
        self.DirectConnectGatewayId = None
        self.RouteIds = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.RouteIds = params.get("RouteIds")


class DeleteDirectConnectGatewayCcnRoutesResponse(AbstractModel):
    """DeleteDirectConnectGatewayCcnRoutes返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteDirectConnectGatewayRequest(AbstractModel):
    """DeleteDirectConnectGateway请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关唯一`ID`，形如：`dcg-9o233uri`。
        :type DirectConnectGatewayId: str
        """
        self.DirectConnectGatewayId = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")


class DeleteDirectConnectGatewayResponse(AbstractModel):
    """DeleteDirectConnectGateway返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteFlowLogRequest(AbstractModel):
    """DeleteFlowLog请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: 私用网络ID或者统一ID，建议使用统一ID
        :type VpcId: str
        :param FlowLogId: 流日志唯一ID
        :type FlowLogId: str
        """
        self.VpcId = None
        self.FlowLogId = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.FlowLogId = params.get("FlowLogId")


class DeleteFlowLogResponse(AbstractModel):
    """DeleteFlowLog返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteHaVipRequest(AbstractModel):
    """DeleteHaVip请求参数结构体"""

    def __init__(self):
        """
        :param HaVipId: `HAVIP`唯一`ID`，形如：`havip-9o233uri`。
        :type HaVipId: str
        """
        self.HaVipId = None

    def _deserialize(self, params):
        self.HaVipId = params.get("HaVipId")


class DeleteHaVipResponse(AbstractModel):
    """DeleteHaVip返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteInstanceNetworkInterfaceRequest(AbstractModel):
    """DeleteInstanceNetworkInterface请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 云主机实例ID。
        :type InstanceId: str
        :param InstanceTerminated: 子机销毁同事释放相关资源，默认为false。比如EIP。
        :type InstanceTerminated: bool
        """
        self.InstanceId = None
        self.InstanceTerminated = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.InstanceTerminated = params.get("InstanceTerminated")


class DeleteInstanceNetworkInterfaceResponse(AbstractModel):
    """DeleteInstanceNetworkInterface返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteIp6TranslatorsRequest(AbstractModel):
    """DeleteIp6Translators请求参数结构体"""

    def __init__(self):
        """
        :param Ip6TranslatorIds: 待释放的IPV6转换实例的唯一ID，形如‘ip6-xxxxxxxx’
        :type Ip6TranslatorIds: list of str
        """
        self.Ip6TranslatorIds = None

    def _deserialize(self, params):
        self.Ip6TranslatorIds = params.get("Ip6TranslatorIds")


class DeleteIp6TranslatorsResponse(AbstractModel):
    """DeleteIp6Translators返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteLocalDestinationIpPortTranslationNatRuleRequest(AbstractModel):
    """DeleteLocalDestinationIpPortTranslationNatRule请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID
        :type DirectConnectGatewayId: str
        :param VpcId: 字符型VPCID
        :type VpcId: str
        :param LocalDestinationIpPortTranslationNatRuleSet: 对端IP转换列表
        :type LocalDestinationIpPortTranslationNatRuleSet: list of LocalDestinationIpPortTranslationNatRule
        """
        self.DirectConnectGatewayId = None
        self.VpcId = None
        self.LocalDestinationIpPortTranslationNatRuleSet = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.VpcId = params.get("VpcId")
        if params.get("LocalDestinationIpPortTranslationNatRuleSet") is not None:
            self.LocalDestinationIpPortTranslationNatRuleSet = []
            for item in params.get("LocalDestinationIpPortTranslationNatRuleSet"):
                obj = LocalDestinationIpPortTranslationNatRule()
                obj._deserialize(item)
                self.LocalDestinationIpPortTranslationNatRuleSet.append(obj)


class DeleteLocalDestinationIpPortTranslationNatRuleResponse(AbstractModel):
    """DeleteLocalDestinationIpPortTranslationNatRule返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteLocalIpTranslationAclRuleRequest(AbstractModel):
    """DeleteLocalIpTranslationAclRule请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID
        :type DirectConnectGatewayId: str
        :param VpcId: 字符型VPCID
        :type VpcId: str
        :param OriginalIp: 原始IP
        :type OriginalIp: str
        :param TranslationIp: 映射IP
        :type TranslationIp: str
        :param LocalIpTranslationAclRuleSet: 本端IP转换列表ACL列表
        :type LocalIpTranslationAclRuleSet: list of AclRuleId
        """
        self.DirectConnectGatewayId = None
        self.VpcId = None
        self.OriginalIp = None
        self.TranslationIp = None
        self.LocalIpTranslationAclRuleSet = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.VpcId = params.get("VpcId")
        self.OriginalIp = params.get("OriginalIp")
        self.TranslationIp = params.get("TranslationIp")
        if params.get("LocalIpTranslationAclRuleSet") is not None:
            self.LocalIpTranslationAclRuleSet = []
            for item in params.get("LocalIpTranslationAclRuleSet"):
                obj = AclRuleId()
                obj._deserialize(item)
                self.LocalIpTranslationAclRuleSet.append(obj)


class DeleteLocalIpTranslationAclRuleResponse(AbstractModel):
    """DeleteLocalIpTranslationAclRule返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteLocalIpTranslationNatRuleRequest(AbstractModel):
    """DeleteLocalIpTranslationNatRule请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID
        :type DirectConnectGatewayId: str
        :param VpcId: 字符型VPCID
        :type VpcId: str
        :param LocalIpTranslationNatRuleSet: 本端IP转换列表
        :type LocalIpTranslationNatRuleSet: list of LocalIpTranslationNatRule
        """
        self.DirectConnectGatewayId = None
        self.VpcId = None
        self.LocalIpTranslationNatRuleSet = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.VpcId = params.get("VpcId")
        if params.get("LocalIpTranslationNatRuleSet") is not None:
            self.LocalIpTranslationNatRuleSet = []
            for item in params.get("LocalIpTranslationNatRuleSet"):
                obj = LocalIpTranslationNatRule()
                obj._deserialize(item)
                self.LocalIpTranslationNatRuleSet.append(obj)


class DeleteLocalIpTranslationNatRuleResponse(AbstractModel):
    """DeleteLocalIpTranslationNatRule返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteLocalSourceIpPortTranslationAclRuleRequest(AbstractModel):
    """DeleteLocalSourceIpPortTranslationAclRule请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID
        :type DirectConnectGatewayId: str
        :param VpcId: 字符型VPCID
        :type VpcId: str
        :param TranslationIpPool: IP池
        :type TranslationIpPool: str
        :param LocalSourceIpPortTranslationAclRuleSet: 本端源IP端口转换ACL列表
        :type LocalSourceIpPortTranslationAclRuleSet: list of AclRuleIdType
        """
        self.DirectConnectGatewayId = None
        self.VpcId = None
        self.TranslationIpPool = None
        self.LocalSourceIpPortTranslationAclRuleSet = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.VpcId = params.get("VpcId")
        self.TranslationIpPool = params.get("TranslationIpPool")
        if params.get("LocalSourceIpPortTranslationAclRuleSet") is not None:
            self.LocalSourceIpPortTranslationAclRuleSet = []
            for item in params.get("LocalSourceIpPortTranslationAclRuleSet"):
                obj = AclRuleIdType()
                obj._deserialize(item)
                self.LocalSourceIpPortTranslationAclRuleSet.append(obj)


class DeleteLocalSourceIpPortTranslationAclRuleResponse(AbstractModel):
    """DeleteLocalSourceIpPortTranslationAclRule返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteLocalSourceIpPortTranslationNatRuleRequest(AbstractModel):
    """DeleteLocalSourceIpPortTranslationNatRule请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID
        :type DirectConnectGatewayId: str
        :param VpcId: 字符型VPCID
        :type VpcId: str
        :param LocalSourceIpPortTranslationNatRuleSet: 本端源IP端口转换列表
        :type LocalSourceIpPortTranslationNatRuleSet: list of LocalSourceIpPortTranslationNatRule
        """
        self.DirectConnectGatewayId = None
        self.VpcId = None
        self.LocalSourceIpPortTranslationNatRuleSet = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.VpcId = params.get("VpcId")
        if params.get("LocalSourceIpPortTranslationNatRuleSet") is not None:
            self.LocalSourceIpPortTranslationNatRuleSet = []
            for item in params.get("LocalSourceIpPortTranslationNatRuleSet"):
                obj = LocalSourceIpPortTranslationNatRule()
                obj._deserialize(item)
                self.LocalSourceIpPortTranslationNatRuleSet.append(obj)


class DeleteLocalSourceIpPortTranslationNatRuleResponse(AbstractModel):
    """DeleteLocalSourceIpPortTranslationNatRule返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteNatGatewayDestinationIpPortTranslationNatRuleRequest(AbstractModel):
    """DeleteNatGatewayDestinationIpPortTranslationNatRule请求参数结构体"""

    def __init__(self):
        """
        :param NatGatewayId: NAT网关的ID，形如：`nat-df45454`。
        :type NatGatewayId: str
        :param DestinationIpPortTranslationNatRules: NAT网关的端口转换规则。
        :type DestinationIpPortTranslationNatRules: list of DestinationIpPortTranslationNatRule
        """
        self.NatGatewayId = None
        self.DestinationIpPortTranslationNatRules = None

    def _deserialize(self, params):
        self.NatGatewayId = params.get("NatGatewayId")
        if params.get("DestinationIpPortTranslationNatRules") is not None:
            self.DestinationIpPortTranslationNatRules = []
            for item in params.get("DestinationIpPortTranslationNatRules"):
                obj = DestinationIpPortTranslationNatRule()
                obj._deserialize(item)
                self.DestinationIpPortTranslationNatRules.append(obj)


class DeleteNatGatewayDestinationIpPortTranslationNatRuleResponse(AbstractModel):
    """DeleteNatGatewayDestinationIpPortTranslationNatRule返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteNatGatewayRequest(AbstractModel):
    """DeleteNatGateway请求参数结构体"""

    def __init__(self):
        """
        :param NatGatewayId: NAT网关的ID，形如：`nat-df45454`。
        :type NatGatewayId: str
        """
        self.NatGatewayId = None

    def _deserialize(self, params):
        self.NatGatewayId = params.get("NatGatewayId")


class DeleteNatGatewayResponse(AbstractModel):
    """DeleteNatGateway返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteNetDetectRequest(AbstractModel):
    """DeleteNetDetect请求参数结构体"""

    def __init__(self):
        """
        :param NetDetectId: 网络探测实例`ID`。形如：`netd-12345678`
        :type NetDetectId: str
        """
        self.NetDetectId = None

    def _deserialize(self, params):
        self.NetDetectId = params.get("NetDetectId")


class DeleteNetDetectResponse(AbstractModel):
    """DeleteNetDetect返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteNetworkAclRequest(AbstractModel):
    """DeleteNetworkAcl请求参数结构体"""

    def __init__(self):
        """
        :param NetworkAclId: 网络ACL实例ID。例如：acl-12345678。
        :type NetworkAclId: str
        """
        self.NetworkAclId = None

    def _deserialize(self, params):
        self.NetworkAclId = params.get("NetworkAclId")


class DeleteNetworkAclResponse(AbstractModel):
    """DeleteNetworkAcl返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteNetworkInterfaceExRequest(AbstractModel):
    """DeleteNetworkInterfaceEx请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: VPC实例ID。可通过DescribeVpcs接口返回值中的VpcId获取。
        :type VpcId: str
        :param NetworkInterfaceId: 弹性网卡实例ID，例如：eni-m6dyj72l。
        :type NetworkInterfaceId: str
        :param IsCrossTenant: 是否跨租户创建网卡。默认为true。
        :type IsCrossTenant: bool
        """
        self.VpcId = None
        self.NetworkInterfaceId = None
        self.IsCrossTenant = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.NetworkInterfaceId = params.get("NetworkInterfaceId")
        self.IsCrossTenant = params.get("IsCrossTenant")


class DeleteNetworkInterfaceExResponse(AbstractModel):
    """DeleteNetworkInterfaceEx返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteNetworkInterfaceRequest(AbstractModel):
    """DeleteNetworkInterface请求参数结构体"""

    def __init__(self):
        """
        :param NetworkInterfaceId: 弹性网卡实例ID，例如：eni-m6dyj72l。
        :type NetworkInterfaceId: str
        """
        self.NetworkInterfaceId = None

    def _deserialize(self, params):
        self.NetworkInterfaceId = params.get("NetworkInterfaceId")


class DeleteNetworkInterfaceResponse(AbstractModel):
    """DeleteNetworkInterface返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeletePeerIpTranslationNatRuleRequest(AbstractModel):
    """DeletePeerIpTranslationNatRule请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID
        :type DirectConnectGatewayId: str
        :param VpcId: 字符型VPCID
        :type VpcId: str
        :param PeerIpTranslationNatRuleSet: 对端IP转换列表
        :type PeerIpTranslationNatRuleSet: list of LocalIpTranslationNatRule
        """
        self.DirectConnectGatewayId = None
        self.VpcId = None
        self.PeerIpTranslationNatRuleSet = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.VpcId = params.get("VpcId")
        if params.get("PeerIpTranslationNatRuleSet") is not None:
            self.PeerIpTranslationNatRuleSet = []
            for item in params.get("PeerIpTranslationNatRuleSet"):
                obj = LocalIpTranslationNatRule()
                obj._deserialize(item)
                self.PeerIpTranslationNatRuleSet.append(obj)


class DeletePeerIpTranslationNatRuleResponse(AbstractModel):
    """DeletePeerIpTranslationNatRule返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteRouteTableRequest(AbstractModel):
    """DeleteRouteTable请求参数结构体"""

    def __init__(self):
        """
        :param RouteTableId: 路由表实例ID，例如：rtb-azd4dt1c。
        :type RouteTableId: str
        """
        self.RouteTableId = None

    def _deserialize(self, params):
        self.RouteTableId = params.get("RouteTableId")


class DeleteRouteTableResponse(AbstractModel):
    """DeleteRouteTable返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteRoutesRequest(AbstractModel):
    """DeleteRoutes请求参数结构体"""

    def __init__(self):
        """
        :param RouteTableId: 路由表实例ID。
        :type RouteTableId: str
        :param Routes: 路由策略对象。
        :type Routes: list of Route
        """
        self.RouteTableId = None
        self.Routes = None

    def _deserialize(self, params):
        self.RouteTableId = params.get("RouteTableId")
        if params.get("Routes") is not None:
            self.Routes = []
            for item in params.get("Routes"):
                obj = Route()
                obj._deserialize(item)
                self.Routes.append(obj)


class DeleteRoutesResponse(AbstractModel):
    """DeleteRoutes返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteSecurityGroupPoliciesRequest(AbstractModel):
    """DeleteSecurityGroupPolicies请求参数结构体"""

    def __init__(self):
        """
        :param SecurityGroupId: 安全组实例ID，例如sg-33ocnj9n，可通过DescribeSecurityGroups获取。
        :type SecurityGroupId: str
        :param SecurityGroupPolicySet: 安全组规则集合。一个请求中只能删除单个方向的一条或多条规则。支持指定索引（PolicyIndex） 匹配删除和安全组规则匹配删除两种方式，一个请求中只能使用一种匹配方式。
        :type SecurityGroupPolicySet: :class:`tcecloud.vpc.v20170312.models.SecurityGroupPolicySet`
        """
        self.SecurityGroupId = None
        self.SecurityGroupPolicySet = None

    def _deserialize(self, params):
        self.SecurityGroupId = params.get("SecurityGroupId")
        if params.get("SecurityGroupPolicySet") is not None:
            self.SecurityGroupPolicySet = SecurityGroupPolicySet()
            self.SecurityGroupPolicySet._deserialize(params.get("SecurityGroupPolicySet"))


class DeleteSecurityGroupPoliciesResponse(AbstractModel):
    """DeleteSecurityGroupPolicies返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteSecurityGroupRequest(AbstractModel):
    """DeleteSecurityGroup请求参数结构体"""

    def __init__(self):
        """
        :param SecurityGroupId: 安全组实例ID，例如sg-33ocnj9n，可通过DescribeSecurityGroups获取。
        :type SecurityGroupId: str
        """
        self.SecurityGroupId = None

    def _deserialize(self, params):
        self.SecurityGroupId = params.get("SecurityGroupId")


class DeleteSecurityGroupResponse(AbstractModel):
    """DeleteSecurityGroup返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteServiceTemplateGroupRequest(AbstractModel):
    """DeleteServiceTemplateGroup请求参数结构体"""

    def __init__(self):
        """
        :param ServiceTemplateGroupId: 协议端口模板集合实例ID，例如：ppmg-n17uxvve。
        :type ServiceTemplateGroupId: str
        """
        self.ServiceTemplateGroupId = None

    def _deserialize(self, params):
        self.ServiceTemplateGroupId = params.get("ServiceTemplateGroupId")


class DeleteServiceTemplateGroupResponse(AbstractModel):
    """DeleteServiceTemplateGroup返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteServiceTemplateRequest(AbstractModel):
    """DeleteServiceTemplate请求参数结构体"""

    def __init__(self):
        """
        :param ServiceTemplateId: 协议端口模板实例ID，例如：ppm-e6dy460g。
        :type ServiceTemplateId: str
        """
        self.ServiceTemplateId = None

    def _deserialize(self, params):
        self.ServiceTemplateId = params.get("ServiceTemplateId")


class DeleteServiceTemplateResponse(AbstractModel):
    """DeleteServiceTemplate返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteSubnetRequest(AbstractModel):
    """DeleteSubnet请求参数结构体"""

    def __init__(self):
        """
        :param SubnetId: 子网实例ID。可通过DescribeSubnets接口返回值中的SubnetId获取。
        :type SubnetId: str
        """
        self.SubnetId = None

    def _deserialize(self, params):
        self.SubnetId = params.get("SubnetId")


class DeleteSubnetResponse(AbstractModel):
    """DeleteSubnet返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteTrafficMirrorRequest(AbstractModel):
    """DeleteTrafficMirror请求参数结构体"""

    def __init__(self):
        """
        :param TrafficMirrorId: 流量镜像实例ID
        :type TrafficMirrorId: str
        """
        self.TrafficMirrorId = None

    def _deserialize(self, params):
        self.TrafficMirrorId = params.get("TrafficMirrorId")


class DeleteTrafficMirrorResponse(AbstractModel):
    """DeleteTrafficMirror返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteTrafficPackagesRequest(AbstractModel):
    """DeleteTrafficPackages请求参数结构体"""

    def __init__(self):
        """
        :param TrafficPackageIds: 待删除的流量包唯一ID数组
        :type TrafficPackageIds: list of str
        """
        self.TrafficPackageIds = None

    def _deserialize(self, params):
        self.TrafficPackageIds = params.get("TrafficPackageIds")


class DeleteTrafficPackagesResponse(AbstractModel):
    """DeleteTrafficPackages返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteVpcRequest(AbstractModel):
    """DeleteVpc请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: VPC实例ID。可通过DescribeVpcs接口返回值中的VpcId获取。
        :type VpcId: str
        """
        self.VpcId = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")


class DeleteVpcResponse(AbstractModel):
    """DeleteVpc返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteVpnConnectionRequest(AbstractModel):
    """DeleteVpnConnection请求参数结构体"""

    def __init__(self):
        """
        :param VpnGatewayId: VPN网关实例ID。
        :type VpnGatewayId: str
        :param VpnConnectionId: VPN通道实例ID。形如：vpnx-f49l6u0z。
        :type VpnConnectionId: str
        """
        self.VpnGatewayId = None
        self.VpnConnectionId = None

    def _deserialize(self, params):
        self.VpnGatewayId = params.get("VpnGatewayId")
        self.VpnConnectionId = params.get("VpnConnectionId")


class DeleteVpnConnectionResponse(AbstractModel):
    """DeleteVpnConnection返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteVpnGatewayRequest(AbstractModel):
    """DeleteVpnGateway请求参数结构体"""

    def __init__(self):
        """
        :param VpnGatewayId: VPN网关实例ID。
        :type VpnGatewayId: str
        """
        self.VpnGatewayId = None

    def _deserialize(self, params):
        self.VpnGatewayId = params.get("VpnGatewayId")


class DeleteVpnGatewayResponse(AbstractModel):
    """DeleteVpnGateway返回参数结构体"""

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


class DescribeAccountAttributesResponse(AbstractModel):
    """DescribeAccountAttributes返回参数结构体"""

    def __init__(self):
        """
        :param AccountAttributeSet: 用户账号属性对象
        :type AccountAttributeSet: list of AccountAttribute
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AccountAttributeSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("AccountAttributeSet") is not None:
            self.AccountAttributeSet = []
            for item in params.get("AccountAttributeSet"):
                obj = AccountAttribute()
                obj._deserialize(item)
                self.AccountAttributeSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeAddressActionQuotaRequest(AbstractModel):
    """DescribeAddressActionQuota请求参数结构体"""

    def __init__(self):
        """
        :param AddressIds: 弹性公网EIP的唯一ID
        :type AddressIds: list of str
        :param ActionType: 弹性公网IP的操作类型，包括"ModifyAddressInternetChargeType"
        :type ActionType: str
        :param ActionTypeList: 弹性公网IP的操作类型列表，包括"ModifyAddressInternetChargeType"
        :type ActionTypeList: list of str
        """
        self.AddressIds = None
        self.ActionType = None
        self.ActionTypeList = None

    def _deserialize(self, params):
        self.AddressIds = params.get("AddressIds")
        self.ActionType = params.get("ActionType")
        self.ActionTypeList = params.get("ActionTypeList")


class DescribeAddressActionQuotaResponse(AbstractModel):
    """DescribeAddressActionQuota返回参数结构体"""

    def __init__(self):
        """
        :param QuotaSet: 弹性公网EIP的操作配额详细信息
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


class DescribeAddressAssociationQuotaRequest(AbstractModel):
    """DescribeAddressAssociationQuota请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: [已废弃]待绑定的云主机实例ID
        :type InstanceId: str
        :param InstanceIds: 需要查询的云主机实例ID列表
        :type InstanceIds: list of str
        :param NetworkInterfaceId: [已废弃]待绑定的弹性网卡ID
        :type NetworkInterfaceId: str
        :param NetworkInterfaceIds: 需要查询的弹性网卡ID列表
        :type NetworkInterfaceIds: list of str
        :param TargetInstanceId: 待绑定的云主机实例ID
        :type TargetInstanceId: str
        :param TargetNetworkInterfaceId: 待绑定的弹性网卡ID
        :type TargetNetworkInterfaceId: str
        :param CPU: 指定CPU核数查询云主机绑定配额
        :type CPU: int
        :param Memory: 指定内存大小查询云主机绑定配额
        :type Memory: int
        """
        self.InstanceId = None
        self.InstanceIds = None
        self.NetworkInterfaceId = None
        self.NetworkInterfaceIds = None
        self.TargetInstanceId = None
        self.TargetNetworkInterfaceId = None
        self.CPU = None
        self.Memory = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.InstanceIds = params.get("InstanceIds")
        self.NetworkInterfaceId = params.get("NetworkInterfaceId")
        self.NetworkInterfaceIds = params.get("NetworkInterfaceIds")
        self.TargetInstanceId = params.get("TargetInstanceId")
        self.TargetNetworkInterfaceId = params.get("TargetNetworkInterfaceId")
        self.CPU = params.get("CPU")
        self.Memory = params.get("Memory")


class DescribeAddressAssociationQuotaResponse(AbstractModel):
    """DescribeAddressAssociationQuota返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeAddressAvailabilityRequest(AbstractModel):
    """DescribeAddressAvailability请求参数结构体"""

    def __init__(self):
        """
        :param AddressCount: 申请 EIP 数量，默认值为1。
        :type AddressCount: int
        :param AddressType: EIP类型，EIP|AnycastEIP，默认EIP。
        :type AddressType: str
        :param ApplicableForCLB: 申请适用于CLB的EIP，默认值为false。
        :type ApplicableForCLB: bool
        :param InternetServiceProvider: 运营商名称，可选值[BGP|CTCC|CMCC]，默认BGP。
        :type InternetServiceProvider: str
        :param Zone: EIP可用区，用于指定可用区申请EIP。
        :type Zone: str
        :param LaunchSource: 购买渠道。
        :type LaunchSource: bool
        :param AllPossibleCombinations: 全部可选参数组合。
        :type AllPossibleCombinations: str
        """
        self.AddressCount = None
        self.AddressType = None
        self.ApplicableForCLB = None
        self.InternetServiceProvider = None
        self.Zone = None
        self.LaunchSource = None
        self.AllPossibleCombinations = None

    def _deserialize(self, params):
        self.AddressCount = params.get("AddressCount")
        self.AddressType = params.get("AddressType")
        self.ApplicableForCLB = params.get("ApplicableForCLB")
        self.InternetServiceProvider = params.get("InternetServiceProvider")
        self.Zone = params.get("Zone")
        self.LaunchSource = params.get("LaunchSource")
        self.AllPossibleCombinations = params.get("AllPossibleCombinations")


class DescribeAddressAvailabilityResponse(AbstractModel):
    """DescribeAddressAvailability返回参数结构体"""

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


class DescribeAddressChangeQuotaRequest(AbstractModel):
    """DescribeAddressChangeQuota请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 实例ID列表
        :type InstanceIds: list of str
        """
        self.InstanceIds = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")


class DescribeAddressChangeQuotaResponse(AbstractModel):
    """DescribeAddressChangeQuota返回参数结构体"""

    def __init__(self):
        """
        :param QuotaSet: 实例公网IP配额对象
        :type QuotaSet: list of AddressChangeQuota
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.QuotaSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("QuotaSet") is not None:
            self.QuotaSet = []
            for item in params.get("QuotaSet"):
                obj = AddressChangeQuota()
                obj._deserialize(item)
                self.QuotaSet.append(obj)
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


class DescribeAddressSetRequest(AbstractModel):
    """DescribeAddressSet请求参数结构体"""

    def __init__(self):
        """
        :param TgwGroup: 弹性公网IP集群的标签
        :type TgwGroup: str
        :param SetId: 弹性公网IP集群的唯一ID
        :type SetId: int
        :param AddressIps: 弹性公网IP地址列表
        :type AddressIps: list of str
        """
        self.TgwGroup = None
        self.SetId = None
        self.AddressIps = None

    def _deserialize(self, params):
        self.TgwGroup = params.get("TgwGroup")
        self.SetId = params.get("SetId")
        self.AddressIps = params.get("AddressIps")


class DescribeAddressSetResponse(AbstractModel):
    """DescribeAddressSet返回参数结构体"""

    def __init__(self):
        """
        :param TotalNum: 弹性公网IP总数量
        :type TotalNum: int
        :param UsedNum: 弹性公网IP使用数量
        :type UsedNum: int
        :param AvailableNum: 弹性公网IP可用数量
        :type AvailableNum: int
        :param AddressList: 弹性公网IP详细信息
        :type AddressList: list of AddressBase
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalNum = None
        self.UsedNum = None
        self.AvailableNum = None
        self.AddressList = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalNum = params.get("TotalNum")
        self.UsedNum = params.get("UsedNum")
        self.AvailableNum = params.get("AvailableNum")
        if params.get("AddressList") is not None:
            self.AddressList = []
            for item in params.get("AddressList"):
                obj = AddressBase()
                obj._deserialize(item)
                self.AddressList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeAddressTemplateGroupInstancesRequest(AbstractModel):
    """DescribeAddressTemplateGroupInstances请求参数结构体"""

    def __init__(self):
        """
        :param AddressTemplateGroupId: IP地址组实例ID。例如：ipmg-12345678。
        :type AddressTemplateGroupId: str
        :param Offset: 偏移量，默认为0。
        :type Offset: int
        :param Limit: 返回数量，默认为20，最大值为100。
        :type Limit: int
        """
        self.AddressTemplateGroupId = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.AddressTemplateGroupId = params.get("AddressTemplateGroupId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeAddressTemplateGroupInstancesResponse(AbstractModel):
    """DescribeAddressTemplateGroupInstances返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeAddressTemplateGroupsRequest(AbstractModel):
    """DescribeAddressTemplateGroups请求参数结构体"""

    def __init__(self):
        """
                :param Filters: 过滤条件。
        <li>address-template-group-name - String - （过滤条件）IP地址模板集合名称。</li>
        <li>address-template-group-id - String - （过滤条件）IP地址模板实集合例ID，例如：ipmg-mdunqeb6。</li>
                :type Filters: list of Filter
                :param Offset: 偏移量，默认为0。
                :type Offset: str
                :param Limit: 返回数量，默认为20，最大值为100。
                :type Limit: str
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


class DescribeAddressTemplateGroupsResponse(AbstractModel):
    """DescribeAddressTemplateGroups返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param AddressTemplateGroupSet: IP地址模板。
        :type AddressTemplateGroupSet: list of AddressTemplateGroup
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.AddressTemplateGroupSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("AddressTemplateGroupSet") is not None:
            self.AddressTemplateGroupSet = []
            for item in params.get("AddressTemplateGroupSet"):
                obj = AddressTemplateGroup()
                obj._deserialize(item)
                self.AddressTemplateGroupSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeAddressTemplateInstancesRequest(AbstractModel):
    """DescribeAddressTemplateInstances请求参数结构体"""

    def __init__(self):
        """
        :param AddressTemplateId: IP地址实例ID。例如：ipm-12345678。
        :type AddressTemplateId: str
        :param Offset: 偏移量，默认为0。
        :type Offset: int
        :param Limit: 返回数量，默认为20，最大值为100。
        :type Limit: int
        """
        self.AddressTemplateId = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.AddressTemplateId = params.get("AddressTemplateId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeAddressTemplateInstancesResponse(AbstractModel):
    """DescribeAddressTemplateInstances返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeAddressTemplatesRequest(AbstractModel):
    """DescribeAddressTemplates请求参数结构体"""

    def __init__(self):
        """
                :param Filters: 过滤条件。
        <li>address-template-name - String - （过滤条件）IP地址模板名称。</li>
        <li>address-template-id - String - （过滤条件）IP地址模板实例ID，例如：ipm-mdunqeb6。</li>
                :type Filters: list of Filter
                :param Offset: 偏移量，默认为0。
                :type Offset: str
                :param Limit: 返回数量，默认为20，最大值为100。
                :type Limit: str
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


class DescribeAddressTemplatesResponse(AbstractModel):
    """DescribeAddressTemplates返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param AddressTemplateSet: IP地址模版。
        :type AddressTemplateSet: list of AddressTemplate
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.AddressTemplateSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("AddressTemplateSet") is not None:
            self.AddressTemplateSet = []
            for item in params.get("AddressTemplateSet"):
                obj = AddressTemplate()
                obj._deserialize(item)
                self.AddressTemplateSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeAddressesHistoryRequest(AbstractModel):
    """DescribeAddressesHistory请求参数结构体"""

    def __init__(self):
        """
        :param AddressIds: 待查询EIP的唯一ID数组，形如eip-xxxxxxx
        :type AddressIds: list of str
        :param AddressIps: 待查询IP地址列表数组
        :type AddressIps: list of str
        :param AddressType: EIP类型过滤，包括"WanIP","EIP","AnycastEIP"三种类型。不填该参数默认查询所有EIP类型
        :type AddressType: list of str
        :param InternetServiceProvider: EIP运营商过滤，包括"CMCC","CUCC","CTCC","BGP"四种运营商。不填该参数默认查询所有运营商类型
        :type InternetServiceProvider: list of str
        """
        self.AddressIds = None
        self.AddressIps = None
        self.AddressType = None
        self.InternetServiceProvider = None

    def _deserialize(self, params):
        self.AddressIds = params.get("AddressIds")
        self.AddressIps = params.get("AddressIps")
        self.AddressType = params.get("AddressType")
        self.InternetServiceProvider = params.get("InternetServiceProvider")


class DescribeAddressesHistoryResponse(AbstractModel):
    """DescribeAddressesHistory返回参数结构体"""

    def __init__(self):
        """
        :param RecoverLimit: 该账户在当前地域指定eip找回的配额限制
        :type RecoverLimit: int
        :param Recovered: 该账户在当前地域当月使用指定eip找回的次数
        :type Recovered: int
        :param AddressSet: 查询EIP的基本信息
        :type AddressSet: :class:`tcecloud.vpc.v20170312.models.AddressBasic`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RecoverLimit = None
        self.Recovered = None
        self.AddressSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.RecoverLimit = params.get("RecoverLimit")
        self.Recovered = params.get("Recovered")
        if params.get("AddressSet") is not None:
            self.AddressSet = AddressBasic()
            self.AddressSet._deserialize(params.get("AddressSet"))
        self.RequestId = params.get("RequestId")


class DescribeAddressesRequest(AbstractModel):
    """DescribeAddresses请求参数结构体"""

    def __init__(self):
        """
                :param AddressIds: 标识 EIP 的唯一 ID 列表。EIP 唯一 ID 形如：`eip-11112222`。参数不支持同时指定`AddressIds`和`Filters`。
                :type AddressIds: list of str
                :param Filters: 每次请求的`Filters`的上限为10，`Filter.Values`的上限为5。参数不支持同时指定`AddressIds`和`Filters`。详细的过滤条件如下：
        <li> address-id - String - 是否必填：否 - （过滤条件）按照 EIP 的唯一 ID 过滤。EIP 唯一 ID 形如：eip-11112222。</li>
        <li> address-name - String - 是否必填：否 - （过滤条件）按照 EIP 名称过滤。不支持模糊过滤。</li>
        <li> address-ip - String - 是否必填：否 - （过滤条件）按照 EIP 的 IP 地址过滤。</li>
        <li> address-status - String - 是否必填：否 - （过滤条件）按照 EIP 的状态过滤。状态包含：'CREATING'，'BINDING'，'BIND'，'UNBINDING'，'UNBIND'，'OFFLINING'，'BIND_ENI'。</li>
        <li> instance-id - String - 是否必填：否 - （过滤条件）按照 EIP 绑定的实例 ID 过滤。实例 ID 形如：ins-11112222。</li>
        <li> private-ip-address - String - 是否必填：否 - （过滤条件）按照 EIP 绑定的内网 IP 过滤。</li>
        <li> network-interface-id - String - 是否必填：否 - （过滤条件）按照 EIP 绑定的弹性网卡 ID 过滤。弹性网卡 ID 形如：eni-11112222。</li>
        <li> is-arrears - String - 是否必填：否 - （过滤条件）按照 EIP 是否欠费进行过滤。（TRUE：EIP 处于欠费状态|FALSE：EIP 费用状态正常）</li>
                :type Filters: list of Filter
                :param Offset: 偏移量，默认为0。关于`Offset`的更进一步介绍请参考 API 简介中的相关小节。
                :type Offset: int
                :param Limit: 返回数量，默认为20，最大值为100。关于`Limit`的更进一步介绍请参考 API 简介中的相关小节。
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


class DescribeAnycastRegionRequest(AbstractModel):
    """DescribeAnycastRegion请求参数结构体"""

    def __init__(self):
        """
        :param AnycastZone: AnycastEIP的发布域，当前可选项为: ANYCAST_ZONE_A, ANYCAST_ZONE_B, ANYCAST_ZONE_OVERSEAS, ANYCAST_ZONE_GLOBAL. 其中 ANYCAST_ZONE_A 和 ANYCAST_ZONE_B 为存量废弃字段.
        :type AnycastZone: str
        """
        self.AnycastZone = None

    def _deserialize(self, params):
        self.AnycastZone = params.get("AnycastZone")


class DescribeAnycastRegionResponse(AbstractModel):
    """DescribeAnycastRegion返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 查询到的记录总数
        :type TotalCount: int
        :param RegionSet: 地域信息
        :type RegionSet: :class:`tcecloud.vpc.v20170312.models.AnycastRegionInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.RegionSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("RegionSet") is not None:
            self.RegionSet = AnycastRegionInfo()
            self.RegionSet._deserialize(params.get("RegionSet"))
        self.RequestId = params.get("RequestId")


class DescribeAssistantCidrRequest(AbstractModel):
    """DescribeAssistantCidr请求参数结构体"""

    def __init__(self):
        """
                :param VpcIds: `VPC`实例`ID`数组。形如：[`vpc-6v2ht8q5`]
                :type VpcIds: list of str
                :param Filters: 过滤条件，参数不支持同时指定NetworkInterfaceIds和Filters。
        <li>vpc-id - String - （过滤条件）VPC实例ID，形如：vpc-f49l6u0z。</li>
                :type Filters: list of Filter
                :param Offset: 偏移量，默认为0。
                :type Offset: int
                :param Limit: 返回数量，默认为20，最大值为100。
                :type Limit: int
        """
        self.VpcIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.VpcIds = params.get("VpcIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeAssistantCidrResponse(AbstractModel):
    """DescribeAssistantCidr返回参数结构体"""

    def __init__(self):
        """
        :param AssistantCidrSet: 符合条件的辅助CIDR数组。
        :type AssistantCidrSet: list of AssistantCidr
        :param TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AssistantCidrSet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("AssistantCidrSet") is not None:
            self.AssistantCidrSet = []
            for item in params.get("AssistantCidrSet"):
                obj = AssistantCidr()
                obj._deserialize(item)
                self.AssistantCidrSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeAvailableZoneRequest(AbstractModel):
    """DescribeAvailableZone请求参数结构体"""

    def __init__(self):
        """
        :param InternetServiceProvider: EIP运营商信息，比如"BGP","CMCC","CUCC","CTCC"
        :type InternetServiceProvider: str
        :param Zone: EIP可用区，比如"ap-guangzhou-1"
        :type Zone: str
        """
        self.InternetServiceProvider = None
        self.Zone = None

    def _deserialize(self, params):
        self.InternetServiceProvider = params.get("InternetServiceProvider")
        self.Zone = params.get("Zone")


class DescribeAvailableZoneResponse(AbstractModel):
    """DescribeAvailableZone返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 返回可用区信息数量
        :type TotalCount: int
        :param ZoneSet: 可用区详细信息
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


class DescribeBandwidthAttributeRequest(AbstractModel):
    """DescribeBandwidthAttribute请求参数结构体"""

    def __init__(self):
        """
                :param ZoneId: 当前地域的可用区ID
                :type ZoneId: int
                :param NetworkPayMode: 网络计费模式列表。可取
        'BANDWIDTH_POSTPAID_BY_MONTH',
        'BANDWIDTH_PREPAID_BY_MONTH',
        'TRAFFIC_POSTPAID_BY_HOUR',
        'BANDWIDTH_POSTPAID_BY_HOUR',
        'BANDWIDTH_PACKAGE'
                :type NetworkPayMode: list of int
                :param InstanceIds: 云服务器InstanceId，形如ins-xxx, 批量最大限制100个
                :type InstanceIds: list of str
                :param AddressIds: 弹性公网IP唯一ID，形如eip-xxx,批量最大限制100个
                :type AddressIds: list of str
        """
        self.ZoneId = None
        self.NetworkPayMode = None
        self.InstanceIds = None
        self.AddressIds = None

    def _deserialize(self, params):
        self.ZoneId = params.get("ZoneId")
        self.NetworkPayMode = params.get("NetworkPayMode")
        self.InstanceIds = params.get("InstanceIds")
        self.AddressIds = params.get("AddressIds")


class DescribeBandwidthAttributeResponse(AbstractModel):
    """DescribeBandwidthAttribute返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 带宽属性数量
        :type TotalCount: int
        :param BandwidthAttribute: 带宽属性详细信息
        :type BandwidthAttribute: list of BandwidthAttribute
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.BandwidthAttribute = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("BandwidthAttribute") is not None:
            self.BandwidthAttribute = []
            for item in params.get("BandwidthAttribute"):
                obj = BandwidthAttribute()
                obj._deserialize(item)
                self.BandwidthAttribute.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeBandwidthPackageQuotaRequest(AbstractModel):
    """DescribeBandwidthPackageQuota请求参数结构体"""


class DescribeBandwidthPackageQuotaResponse(AbstractModel):
    """DescribeBandwidthPackageQuota返回参数结构体"""

    def __init__(self):
        """
        :param QuotaSet: 带宽包配额详细信息
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


class DescribeBandwidthPackageResourcesRequest(AbstractModel):
    """DescribeBandwidthPackageResources请求参数结构体"""

    def __init__(self):
        """
                :param BandwidthPackageId: 标识 共享带宽包 的唯一 ID 列表。共享带宽包 唯一 ID 形如：`bwp-11112222`。
                :type BandwidthPackageId: str
                :param Filters: 每次请求的`Filters`的上限为10，`Filter.Values`的上限为5。参数不支持同时指定`AddressIds`和`Filters`。详细的过滤条件如下：
        <li> resource-id - String - 是否必填：否 - （过滤条件）按照 共享带宽包内资源 的唯一 ID 过滤。共享带宽包内资源 唯一 ID 形如：eip-11112222。</li>
        <li> resource-type - String - 是否必填：否 - （过滤条件）按照 共享带宽包内资源 类型过滤，目前仅支持 弹性IP 和 负载均衡 两种类型，可选值为 Address 和 LoadBalance。</li>
                :type Filters: list of Filter
                :param Offset: 偏移量，默认为0。关于`Offset`的更进一步介绍请参考 API 简介中的相关小节。
                :type Offset: int
                :param Limit: 返回数量，默认为20，最大值为100。关于`Limit`的更进一步介绍请参考 API 简介中的相关小节。
                :type Limit: int
        """
        self.BandwidthPackageId = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.BandwidthPackageId = params.get("BandwidthPackageId")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeBandwidthPackageResourcesResponse(AbstractModel):
    """DescribeBandwidthPackageResources返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的 共享带宽包内资源 数量。
        :type TotalCount: int
        :param ResourceSet: 共享带宽包内资源 详细信息列表。
        :type ResourceSet: list of Resource
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.ResourceSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("ResourceSet") is not None:
            self.ResourceSet = []
            for item in params.get("ResourceSet"):
                obj = Resource()
                obj._deserialize(item)
                self.ResourceSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeBandwidthPackagesRequest(AbstractModel):
    """DescribeBandwidthPackages请求参数结构体"""

    def __init__(self):
        """
                :param BandwidthPackageIds: 带宽包唯一ID列表
                :type BandwidthPackageIds: list of str
                :param Filters: 每次请求的`Filters`的上限为10。参数不支持同时指定`BandwidthPackageIds`和`Filters`。详细的过滤条件如下：
        <li> bandwidth-package_id - String - 是否必填：否 - （过滤条件）按照带宽包的唯一标识ID过滤。</li>
        <li> bandwidth-package-name - String - 是否必填：否 - （过滤条件）按照 带宽包名称过滤。不支持模糊过滤。</li>
        <li> network-type - String - 是否必填：否 - （过滤条件）按照带宽包的类型过滤。类型包括'BGP','SINGLEISP'和'ANYCAST'。</li>
        <li> charge-type - String - 是否必填：否 - （过滤条件）按照带宽包的计费类型过滤。计费类型包括'TOP5_POSTPAID_BY_MONTH'和'PERCENT95_POSTPAID_BY_MONTH'</li>
        <li> resource.resource-type - String - 是否必填：否 - （过滤条件）按照带宽包资源类型过滤。资源类型包括'Address'和'LoadBalance'</li>
        <li> resource.resource-id - String - 是否必填：否 - （过滤条件）按照带宽包资源Id过滤。资源Id形如'eip-xxxx','lb-xxxx'</li>
        <li> resource.address-ip - String - 是否必填：否 - （过滤条件）按照带宽包资源Ip过滤。</li>
                :type Filters: list of Filter
                :param Offset: 查询带宽包偏移量
                :type Offset: int
                :param Limit: 查询带宽包数量限制
                :type Limit: int
                :param QueryResources: 是否展示带宽包内部资源，默认展示。True表示展示带宽包内详细资源，False表示只展示带宽包而不展示内部详细资源。
                :type QueryResources: bool
        """
        self.BandwidthPackageIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None
        self.QueryResources = None

    def _deserialize(self, params):
        self.BandwidthPackageIds = params.get("BandwidthPackageIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.QueryResources = params.get("QueryResources")


class DescribeBandwidthPackagesResponse(AbstractModel):
    """DescribeBandwidthPackages返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的带宽包数量
        :type TotalCount: int
        :param BandwidthPackageSet: 描述带宽包详细信息
        :type BandwidthPackageSet: list of BandwidthPackage
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.BandwidthPackageSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("BandwidthPackageSet") is not None:
            self.BandwidthPackageSet = []
            for item in params.get("BandwidthPackageSet"):
                obj = BandwidthPackage()
                obj._deserialize(item)
                self.BandwidthPackageSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeCcnAttachedInstancesRequest(AbstractModel):
    """DescribeCcnAttachedInstances请求参数结构体"""

    def __init__(self):
        """
                :param Offset: 偏移量
                :type Offset: int
                :param Limit: 返回数量
                :type Limit: int
                :param Filters: 过滤条件：
        <li>ccn-id - String -（过滤条件）CCN实例ID。</li>
        <li>instance-type - String -（过滤条件）关联实例类型。</li>
        <li>instance-region - String -（过滤条件）关联实例所属地域。</li>
        <li>instance-id - String -（过滤条件）关联实例实例ID。</li>
                :type Filters: list of Filter
                :param CcnId: 云联网实例ID
                :type CcnId: str
                :param OrderField: 排序字段。支持：`CcnId` `InstanceType` `InstanceId` `InstanceName` `InstanceRegion` `AttachedTime` `State`。
                :type OrderField: str
                :param OrderDirection: 排序方法。顺序：`ASC`，倒序：`DESC`。
                :type OrderDirection: str
        """
        self.Offset = None
        self.Limit = None
        self.Filters = None
        self.CcnId = None
        self.OrderField = None
        self.OrderDirection = None

    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.CcnId = params.get("CcnId")
        self.OrderField = params.get("OrderField")
        self.OrderDirection = params.get("OrderDirection")


class DescribeCcnAttachedInstancesResponse(AbstractModel):
    """DescribeCcnAttachedInstances返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的对象数。
        :type TotalCount: int
        :param InstanceSet: 关联实例列表。
        :type InstanceSet: list of CcnAttachedInstance
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
                obj = CcnAttachedInstance()
                obj._deserialize(item)
                self.InstanceSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeCcnLimitsRequest(AbstractModel):
    """DescribeCcnLimits请求参数结构体"""

    def __init__(self):
        """
                :param Filters: 过滤条件：
        type- Int -（过滤条件）云联网配额类型。
        1：每个开发商可创建的云联网数，2：每个云联网绑定的实例个数，3：单个云联网支持的路由条目。
                :type Filters: list of Filter
                :param Limit: 返回数量
                :type Limit: int
                :param Offset: 偏移量
                :type Offset: int
        """
        self.Filters = None
        self.Limit = None
        self.Offset = None

    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")


class DescribeCcnLimitsResponse(AbstractModel):
    """DescribeCcnLimits返回参数结构体"""

    def __init__(self):
        """
        :param CcnLimitSet: 云联网配额列表
        :type CcnLimitSet: list of CcnLimit
        :param TotalCount: 符合条件的对象数。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.CcnLimitSet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("CcnLimitSet") is not None:
            self.CcnLimitSet = []
            for item in params.get("CcnLimitSet"):
                obj = CcnLimit()
                obj._deserialize(item)
                self.CcnLimitSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeCcnRegionBandwidthLimitsRequest(AbstractModel):
    """DescribeCcnRegionBandwidthLimits请求参数结构体"""

    def __init__(self):
        """
        :param CcnId: CCN实例ID。形如：ccn-f49l6u0z。
        :type CcnId: str
        """
        self.CcnId = None

    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")


class DescribeCcnRegionBandwidthLimitsResponse(AbstractModel):
    """DescribeCcnRegionBandwidthLimits返回参数结构体"""

    def __init__(self):
        """
        :param CcnRegionBandwidthLimitSet: 云联网（CCN）各地域出带宽上限
        :type CcnRegionBandwidthLimitSet: list of CcnRegionBandwidthLimit
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.CcnRegionBandwidthLimitSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("CcnRegionBandwidthLimitSet") is not None:
            self.CcnRegionBandwidthLimitSet = []
            for item in params.get("CcnRegionBandwidthLimitSet"):
                obj = CcnRegionBandwidthLimit()
                obj._deserialize(item)
                self.CcnRegionBandwidthLimitSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeCcnRoutesRequest(AbstractModel):
    """DescribeCcnRoutes请求参数结构体"""

    def __init__(self):
        """
                :param CcnId: CCN实例ID，形如：ccn-gree226l。
                :type CcnId: str
                :param RouteIds: CCN路由策略唯一ID。形如：ccnr-f49l6u0z。
                :type RouteIds: list of str
                :param Filters: 过滤条件，参数不支持同时指定RouteIds和Filters。
        <li>route-id - String -（过滤条件）路由策略ID。</li>
        <li>cidr-block - String -（过滤条件）目的端。</li>
        <li>instance-type - String -（过滤条件）下一跳类型。</li>
        <li>instance-region - String -（过滤条件）下一跳所属地域。</li>
        <li>instance-id - String -（过滤条件）下一跳实例ID。</li>
                :type Filters: list of Filter
                :param Offset: 偏移量
                :type Offset: int
                :param Limit: 返回数量
                :type Limit: int
        """
        self.CcnId = None
        self.RouteIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")
        self.RouteIds = params.get("RouteIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeCcnRoutesResponse(AbstractModel):
    """DescribeCcnRoutes返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的对象数。
        :type TotalCount: int
        :param RouteSet: CCN路由策略对象。
        :type RouteSet: list of CcnRoute
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.RouteSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("RouteSet") is not None:
            self.RouteSet = []
            for item in params.get("RouteSet"):
                obj = CcnRoute()
                obj._deserialize(item)
                self.RouteSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeCcnsRequest(AbstractModel):
    """DescribeCcns请求参数结构体"""

    def __init__(self):
        """
                :param CcnIds: CCN实例ID。形如：ccn-f49l6u0z。每次请求的实例的上限为100。参数不支持同时指定CcnIds和Filters。
                :type CcnIds: list of str
                :param Filters: 过滤条件，参数不支持同时指定CcnIds和Filters。
        <li>ccn-id - String - （过滤条件）CCN唯一ID，形如：vpc-f49l6u0z。</li>
        <li>ccn-name - String - （过滤条件）CCN名称。</li>
        <li>ccn-description - String - （过滤条件）CCN描述。</li>
        <li>state - String - （过滤条件）实例状态， 'ISOLATED': 隔离中（欠费停服），'AVAILABLE'：运行中。</li>
        <li>tag-key - String -是否必填：否- （过滤条件）按照标签键进行过滤。</li>
        <li>tag:tag-key - String - 是否必填：否 - （过滤条件）按照标签键值对进行过滤。 tag-key使用具体的标签键进行替换。使用请参考示例：查询绑定了标签的CCN列表。</li>
                :type Filters: list of Filter
                :param Offset: 偏移量
                :type Offset: int
                :param Limit: 返回数量
                :type Limit: int
                :param OrderField: 排序字段。支持：`CcnId` `CcnName` `CreateTime` `State` `QosLevel`
                :type OrderField: str
                :param OrderDirection: 排序方法。顺序：`ASC`，倒序：`DESC`。
                :type OrderDirection: str
        """
        self.CcnIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None
        self.OrderField = None
        self.OrderDirection = None

    def _deserialize(self, params):
        self.CcnIds = params.get("CcnIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.OrderField = params.get("OrderField")
        self.OrderDirection = params.get("OrderDirection")


class DescribeCcnsResponse(AbstractModel):
    """DescribeCcns返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的对象数。
        :type TotalCount: int
        :param CcnSet: CCN对象。
        :type CcnSet: list of CCN
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.CcnSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("CcnSet") is not None:
            self.CcnSet = []
            for item in params.get("CcnSet"):
                obj = CCN()
                obj._deserialize(item)
                self.CcnSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeClassicLinkInstancesRequest(AbstractModel):
    """DescribeClassicLinkInstances请求参数结构体"""

    def __init__(self):
        """
                :param Filters: 过滤条件。
        <li>vpc-id - String - （过滤条件）VPC实例ID。</li>
        <li>vm-ip - String - （过滤条件）基础网络云服务器IP。</li>
                :type Filters: list of FilterObject
                :param Offset: 偏移量
                :type Offset: str
                :param Limit: 返回数量
                :type Limit: str
        """
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = FilterObject()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeClassicLinkInstancesResponse(AbstractModel):
    """DescribeClassicLinkInstances返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param ClassicLinkInstanceSet: 私有网络和基础网络互通设备。
        :type ClassicLinkInstanceSet: list of ClassicLinkInstance
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.ClassicLinkInstanceSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("ClassicLinkInstanceSet") is not None:
            self.ClassicLinkInstanceSet = []
            for item in params.get("ClassicLinkInstanceSet"):
                obj = ClassicLinkInstance()
                obj._deserialize(item)
                self.ClassicLinkInstanceSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeCustomerGatewayVendorsRequest(AbstractModel):
    """DescribeCustomerGatewayVendors请求参数结构体"""


class DescribeCustomerGatewayVendorsResponse(AbstractModel):
    """DescribeCustomerGatewayVendors返回参数结构体"""

    def __init__(self):
        """
        :param CustomerGatewayVendorSet: 对端网关厂商信息对象。
        :type CustomerGatewayVendorSet: list of CustomerGatewayVendor
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.CustomerGatewayVendorSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("CustomerGatewayVendorSet") is not None:
            self.CustomerGatewayVendorSet = []
            for item in params.get("CustomerGatewayVendorSet"):
                obj = CustomerGatewayVendor()
                obj._deserialize(item)
                self.CustomerGatewayVendorSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeCustomerGatewaysRequest(AbstractModel):
    """DescribeCustomerGateways请求参数结构体"""

    def __init__(self):
        """
                :param CustomerGatewayIds: 对端网关ID，例如：cgw-2wqq41m9。每次请求的实例的上限为100。参数不支持同时指定CustomerGatewayIds和Filters。
                :type CustomerGatewayIds: list of str
                :param Filters: 过滤条件，详见下表：实例过滤条件表。每次请求的Filters的上限为10，Filter.Values的上限为5。参数不支持同时指定CustomerGatewayIds和Filters。
        <li>customer-gateway-id - String - （过滤条件）用户网关唯一ID形如：`cgw-mgp33pll`。</li>
        <li>customer-gateway-name - String - （过滤条件）用户网关名称形如：`test-cgw`。</li>
        <li>ip-address - String - （过滤条件）公网地址形如：`58.211.1.12`。</li>
                :type Filters: list of Filter
                :param Offset: 偏移量，默认为0。关于Offset的更进一步介绍请参考 API 简介中的相关小节。
                :type Offset: int
                :param Limit: 返回数量，默认为20，最大值为100。
                :type Limit: int
        """
        self.CustomerGatewayIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.CustomerGatewayIds = params.get("CustomerGatewayIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeCustomerGatewaysResponse(AbstractModel):
    """DescribeCustomerGateways返回参数结构体"""

    def __init__(self):
        """
        :param CustomerGatewaySet: 对端网关对象列表
        :type CustomerGatewaySet: list of CustomerGateway
        :param TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.CustomerGatewaySet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("CustomerGatewaySet") is not None:
            self.CustomerGatewaySet = []
            for item in params.get("CustomerGatewaySet"):
                obj = CustomerGateway()
                obj._deserialize(item)
                self.CustomerGatewaySet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeDirectConnectGatewayCcnRoutesRequest(AbstractModel):
    """DescribeDirectConnectGatewayCcnRoutes请求参数结构体"""

    def __init__(self):
        """
                :param DirectConnectGatewayId: 专线网关ID，形如：`dcg-prpqlmg1`。
                :type DirectConnectGatewayId: str
                :param CcnRouteType: 云联网路由学习类型，可选值：
        <li>`BGP` - 自动学习。</li>
        <li>`STATIC` - 静态，即用户配置，默认值。</li>
                :type CcnRouteType: str
                :param Offset: 偏移量。
                :type Offset: int
                :param Limit: 返回数量。
                :type Limit: int
        """
        self.DirectConnectGatewayId = None
        self.CcnRouteType = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.CcnRouteType = params.get("CcnRouteType")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeDirectConnectGatewayCcnRoutesResponse(AbstractModel):
    """DescribeDirectConnectGatewayCcnRoutes返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的对象数。
        :type TotalCount: int
        :param RouteSet: 云联网路由（IDC网段）列表。
        :type RouteSet: list of DirectConnectGatewayCcnRoute
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.RouteSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("RouteSet") is not None:
            self.RouteSet = []
            for item in params.get("RouteSet"):
                obj = DirectConnectGatewayCcnRoute()
                obj._deserialize(item)
                self.RouteSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDirectConnectGatewaysRequest(AbstractModel):
    """DescribeDirectConnectGateways请求参数结构体"""

    def __init__(self):
        """
                :param DirectConnectGatewayIds: 专线网关唯一`ID`，形如：`dcg-9o233uri`。
                :type DirectConnectGatewayIds: list of str
                :param Filters: 过滤条件，参数不支持同时指定`DirectConnectGatewayIds`和`Filters`。
        <li>direct-connect-gateway-id - String - 专线网关唯一`ID`，形如：`dcg-9o233uri`。</li>
        <li>direct-connect-gateway-name - String - 专线网关名称，默认模糊查询。</li>
        <li>direct-connect-gateway-ip - String - 专线网关`IP`。</li>
        <li>gateway-type - String - 网关类型，可选值：`NORMAL`（普通型）、`NAT`（NAT型）。</li>
        <li>network-type- String - 网络类型，可选值：`VPC`（私有网络类型）、`CCN`（云联网类型）。</li>
        <li>ccn-id - String - 专线网关所在云联网`ID`。</li>
        <li>vpc-id - String - 专线网关所在私有网络`ID`。</li>
                :type Filters: list of Filter
                :param Offset: 偏移量。
                :type Offset: int
                :param Limit: 返回数量。
                :type Limit: int
        """
        self.DirectConnectGatewayIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.DirectConnectGatewayIds = params.get("DirectConnectGatewayIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeDirectConnectGatewaysResponse(AbstractModel):
    """DescribeDirectConnectGateways返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的对象数。
        :type TotalCount: int
        :param DirectConnectGatewaySet: 专线网关对象数组。
        :type DirectConnectGatewaySet: list of DirectConnectGateway
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.DirectConnectGatewaySet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("DirectConnectGatewaySet") is not None:
            self.DirectConnectGatewaySet = []
            for item in params.get("DirectConnectGatewaySet"):
                obj = DirectConnectGateway()
                obj._deserialize(item)
                self.DirectConnectGatewaySet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDownloadSpecificTrafficPackageUsedDetailsQuotaRequest(AbstractModel):
    """DescribeDownloadSpecificTrafficPackageUsedDetailsQuota请求参数结构体"""

    def __init__(self):
        """
        :param TrafficPackageId: 共享流量包唯一ID
        :type TrafficPackageId: str
        """
        self.TrafficPackageId = None

    def _deserialize(self, params):
        self.TrafficPackageId = params.get("TrafficPackageId")


class DescribeDownloadSpecificTrafficPackageUsedDetailsQuotaResponse(AbstractModel):
    """DescribeDownloadSpecificTrafficPackageUsedDetailsQuota返回参数结构体"""

    def __init__(self):
        """
        :param LimitPerHour: 该流量包每小时可以生成的文件数的配额
        :type LimitPerHour: int
        :param LimitLeft: 该流量包在当前时间区间剩余的可以生成文件的次数
        :type LimitLeft: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.LimitPerHour = None
        self.LimitLeft = None
        self.RequestId = None

    def _deserialize(self, params):
        self.LimitPerHour = params.get("LimitPerHour")
        self.LimitLeft = params.get("LimitLeft")
        self.RequestId = params.get("RequestId")


class DescribeDownloadSpecificTrafficPackageUsedDetailsRequest(AbstractModel):
    """DescribeDownloadSpecificTrafficPackageUsedDetails请求参数结构体"""

    def __init__(self):
        """
        :param TrafficPackageId: 共享流量包唯一ID
        :type TrafficPackageId: str
        :param EndTime: 截止时间,默认为当前时间往前24小时
        :type EndTime: str
        :param Offset: 分页参数，默认为0
        :type Offset: int
        :param Limit: 分页参数，默认为20
        :type Limit: int
        """
        self.TrafficPackageId = None
        self.EndTime = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.TrafficPackageId = params.get("TrafficPackageId")
        self.EndTime = params.get("EndTime")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeDownloadSpecificTrafficPackageUsedDetailsResponse(AbstractModel):
    """DescribeDownloadSpecificTrafficPackageUsedDetails返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合查询条件的记录总数.
        :type TotalCount: int
        :param UsedDetailDownloadSet: 共享流量包用量明细文件生成历史
        :type UsedDetailDownloadSet: list of UsedDetailDownload
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.UsedDetailDownloadSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("UsedDetailDownloadSet") is not None:
            self.UsedDetailDownloadSet = []
            for item in params.get("UsedDetailDownloadSet"):
                obj = UsedDetailDownload()
                obj._deserialize(item)
                self.UsedDetailDownloadSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeEIPIspInfoRequest(AbstractModel):
    """DescribeEIPIspInfo请求参数结构体"""


class DescribeEIPIspInfoResponse(AbstractModel):
    """DescribeEIPIspInfo返回参数结构体"""

    def __init__(self):
        """
        :param IspInfoSet: 运营商信息
        :type IspInfoSet: :class:`tcecloud.vpc.v20170312.models.EIPIspInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.IspInfoSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("IspInfoSet") is not None:
            self.IspInfoSet = EIPIspInfo()
            self.IspInfoSet._deserialize(params.get("IspInfoSet"))
        self.RequestId = params.get("RequestId")


class DescribeEipStatisticsRequest(AbstractModel):
    """DescribeEipStatistics请求参数结构体"""

    def __init__(self):
        """
                :param Filters: 每次请求的`Filters`的上限为10，`Filter.Values`的上限为5。参数不支持同时指定`AddressIds`和`Filters`。详细的过滤条件如下：
        <li> is-ddos - String - 是否必填：否 - （过滤条件）按照EIP是否发生ddos封堵过滤。</li>
        <li> address-type - String - 是否必填：否 - （过滤条件）按照 EIP类型（包括"WanIP","EIP","AnycastEIP","EIP6","Internet"） 过滤，其中"Internet"表示所有可访问internet的IP地址，即"WanIP","EIP","AnycastEIP","EIP6"的组合。</li>
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


class DescribeEipStatisticsResponse(AbstractModel):
    """DescribeEipStatistics返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 全地域EIP总数
        :type TotalCount: int
        :param EipStatisticsSet: 各地域EIP详细统计
        :type EipStatisticsSet: list of EipStatistics
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.EipStatisticsSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("EipStatisticsSet") is not None:
            self.EipStatisticsSet = []
            for item in params.get("EipStatisticsSet"):
                obj = EipStatistics()
                obj._deserialize(item)
                self.EipStatisticsSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeFlowLogRequest(AbstractModel):
    """DescribeFlowLog请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: 私用网络ID或者统一ID，建议使用统一ID
        :type VpcId: str
        :param FlowLogId: 流日志唯一ID
        :type FlowLogId: str
        """
        self.VpcId = None
        self.FlowLogId = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.FlowLogId = params.get("FlowLogId")


class DescribeFlowLogResponse(AbstractModel):
    """DescribeFlowLog返回参数结构体"""

    def __init__(self):
        """
        :param FlowLog: 流日志信息
        :type FlowLog: list of FlowLog
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FlowLog = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("FlowLog") is not None:
            self.FlowLog = []
            for item in params.get("FlowLog"):
                obj = FlowLog()
                obj._deserialize(item)
                self.FlowLog.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeFlowLogsRequest(AbstractModel):
    """DescribeFlowLogs请求参数结构体"""

    def __init__(self):
        """
                :param VpcId: 私用网络ID或者统一ID，建议使用统一ID
                :type VpcId: str
                :param FlowLogId: 流日志唯一ID
                :type FlowLogId: str
                :param FlowLogName: 流日志实例名字
                :type FlowLogName: str
                :param ResourceType: 流日志所属资源类型，VPC|SUBNET|NETWORKINTERFACE
                :type ResourceType: str
                :param ResourceId: 资源唯一ID
                :type ResourceId: str
                :param TrafficType: 流日志采集类型，ACCEPT|REJECT|ALL
                :type TrafficType: str
                :param CloudLogId: 流日志存储ID
                :type CloudLogId: str
                :param CloudLogState: 流日志存储ID状态
                :type CloudLogState: str
                :param OrderField: 按某个字段排序,支持字段：flowLogName,createTime，默认按createTime
                :type OrderField: str
                :param OrderDirection: 升序（asc）还是降序（desc）,默认：desc
                :type OrderDirection: str
                :param Offset: 偏移量，默认为0。
                :type Offset: int
                :param Limit: 每页行数，默认为10
                :type Limit: int
                :param Filters: 过滤条件，参数不支持同时指定FlowLogIds和Filters。
        <li>tag-key - String -是否必填：否- （过滤条件）按照标签键进行过滤。</li>
        <li>tag:tag-key - String - 是否必填：否 - （过滤条件）按照标签键值对进行过滤。 tag-key使用具体的标签键进行替换。</li>
                :type Filters: :class:`tcecloud.vpc.v20170312.models.Filter`
        """
        self.VpcId = None
        self.FlowLogId = None
        self.FlowLogName = None
        self.ResourceType = None
        self.ResourceId = None
        self.TrafficType = None
        self.CloudLogId = None
        self.CloudLogState = None
        self.OrderField = None
        self.OrderDirection = None
        self.Offset = None
        self.Limit = None
        self.Filters = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.FlowLogId = params.get("FlowLogId")
        self.FlowLogName = params.get("FlowLogName")
        self.ResourceType = params.get("ResourceType")
        self.ResourceId = params.get("ResourceId")
        self.TrafficType = params.get("TrafficType")
        self.CloudLogId = params.get("CloudLogId")
        self.CloudLogState = params.get("CloudLogState")
        self.OrderField = params.get("OrderField")
        self.OrderDirection = params.get("OrderDirection")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self.Filters = Filter()
            self.Filters._deserialize(params.get("Filters"))


class DescribeFlowLogsResponse(AbstractModel):
    """DescribeFlowLogs返回参数结构体"""

    def __init__(self):
        """
        :param FlowLog: 流日志实例集合
        :type FlowLog: list of FlowLog
        :param TotalNum: 流日志总数目
        :type TotalNum: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FlowLog = None
        self.TotalNum = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("FlowLog") is not None:
            self.FlowLog = []
            for item in params.get("FlowLog"):
                obj = FlowLog()
                obj._deserialize(item)
                self.FlowLog.append(obj)
        self.TotalNum = params.get("TotalNum")
        self.RequestId = params.get("RequestId")


class DescribeGatewayFlowMonitorDetailRequest(AbstractModel):
    """DescribeGatewayFlowMonitorDetail请求参数结构体"""

    def __init__(self):
        """
        :param TimePoint: 时间点。表示要查询这分钟内的明细。如：`2019-02-28 18:15:20`，将查询 `18:15` 这一分钟内的明细。
        :type TimePoint: str
        :param VpnId: VPN网关实例ID，形如：`vpn-ltjahce6`。
        :type VpnId: str
        :param DirectConnectGatewayId: 专线网关实例ID，形如：`dcg-ltjahce6`。
        :type DirectConnectGatewayId: str
        :param PeeringConnectionId: 对等连接实例ID，形如：`pcx-ltjahce6`。
        :type PeeringConnectionId: str
        :param NatId: NAT网关实例ID，形如：`nat-ltjahce6`。
        :type NatId: str
        :param Offset: 偏移量。
        :type Offset: int
        :param Limit: 返回数量。
        :type Limit: int
        :param OrderField: 排序字段。支持 `InPkg` `OutPkg` `InTraffic` `OutTraffic`。
        :type OrderField: str
        :param OrderDirection: 排序方法。顺序：`ASC`，倒序：`DESC`。
        :type OrderDirection: str
        """
        self.TimePoint = None
        self.VpnId = None
        self.DirectConnectGatewayId = None
        self.PeeringConnectionId = None
        self.NatId = None
        self.Offset = None
        self.Limit = None
        self.OrderField = None
        self.OrderDirection = None

    def _deserialize(self, params):
        self.TimePoint = params.get("TimePoint")
        self.VpnId = params.get("VpnId")
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.PeeringConnectionId = params.get("PeeringConnectionId")
        self.NatId = params.get("NatId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.OrderField = params.get("OrderField")
        self.OrderDirection = params.get("OrderDirection")


class DescribeGatewayFlowMonitorDetailResponse(AbstractModel):
    """DescribeGatewayFlowMonitorDetail返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的对象数。
        :type TotalCount: int
        :param GatewayFlowMonitorDetailSet: 网关流量监控明细。
        :type GatewayFlowMonitorDetailSet: list of GatewayFlowMonitorDetail
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.GatewayFlowMonitorDetailSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("GatewayFlowMonitorDetailSet") is not None:
            self.GatewayFlowMonitorDetailSet = []
            for item in params.get("GatewayFlowMonitorDetailSet"):
                obj = GatewayFlowMonitorDetail()
                obj._deserialize(item)
                self.GatewayFlowMonitorDetailSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeGatewayFlowQosRequest(AbstractModel):
    """DescribeGatewayFlowQos请求参数结构体"""

    def __init__(self):
        """
                :param GatewayId: 网关实例ID，目前我们支持的网关实例类型有，
        专线网关实例ID，形如，`dcg-ltjahce6`；
        Nat网关实例ID，形如，`nat-ltjahce6`；
        VPN网关实例ID，形如，`vpn-ltjahce6`。
                :type GatewayId: str
                :param IpAddresses: 限流的云服务器内网IP。
                :type IpAddresses: list of str
                :param Offset: 偏移量，默认为0。
                :type Offset: int
                :param Limit: 返回数量，默认为20，最大值为100。
                :type Limit: int
        """
        self.GatewayId = None
        self.IpAddresses = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.GatewayId = params.get("GatewayId")
        self.IpAddresses = params.get("IpAddresses")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeGatewayFlowQosResponse(AbstractModel):
    """DescribeGatewayFlowQos返回参数结构体"""

    def __init__(self):
        """
        :param GatewayQosSet: 实例详细信息列表。
        :type GatewayQosSet: list of GatewayQos
        :param TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.GatewayQosSet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("GatewayQosSet") is not None:
            self.GatewayQosSet = []
            for item in params.get("GatewayQosSet"):
                obj = GatewayQos()
                obj._deserialize(item)
                self.GatewayQosSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeHaVipsRequest(AbstractModel):
    """DescribeHaVips请求参数结构体"""

    def __init__(self):
        """
                :param HaVipIds: `HAVIP`唯一`ID`，形如：`havip-9o233uri`。
                :type HaVipIds: list of str
                :param Filters: 过滤条件，参数不支持同时指定`HaVipIds`和`Filters`。
        <li>havip-id - String - `HAVIP`唯一`ID`，形如：`havip-9o233uri`。</li>
        <li>havip-name - String - `HAVIP`名称。</li>
        <li>vpc-id - String - `HAVIP`所在私有网络`ID`。</li>
        <li>subnet-id - String - `HAVIP`所在子网`ID`。</li>
        <li>address-ip - String - `HAVIP`绑定的弹性公网`IP`。</li>
                :type Filters: list of Filter
                :param Offset: 偏移量
                :type Offset: int
                :param Limit: 返回数量
                :type Limit: int
        """
        self.HaVipIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.HaVipIds = params.get("HaVipIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeHaVipsResponse(AbstractModel):
    """DescribeHaVips返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的对象数。
        :type TotalCount: int
        :param HaVipSet: `HAVIP`对象数组。
        :type HaVipSet: list of HaVip
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.HaVipSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("HaVipSet") is not None:
            self.HaVipSet = []
            for item in params.get("HaVipSet"):
                obj = HaVip()
                obj._deserialize(item)
                self.HaVipSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeIp6AddressesRequest(AbstractModel):
    """DescribeIp6Addresses请求参数结构体"""

    def __init__(self):
        """
                :param Ip6AddressIds: 标识 IPV6 的唯一 ID 列表。IPV6 唯一 ID 形如：`eip-11112222`。参数不支持同时指定`Ip6AddressIds`和`Filters`。
                :type Ip6AddressIds: list of str
                :param Filters: 每次请求的`Filters`的上限为10，`Filter.Values`的上限为5。参数不支持同时指定`AddressIds`和`Filters`。详细的过滤条件如下：
        <li> address-ip - String - 是否必填：否 - （过滤条件）按照 EIP 的 IP 地址过滤。</li>
        <li> network-interface-id - String - 是否必填：否 - （过滤条件）按照弹性网卡的唯一ID过滤。</li>
                :type Filters: list of Filter
                :param Offset: 偏移量，默认为0。关于`Offset`的更进一步介绍请参考 API 简介中的相关小节。
                :type Offset: int
                :param Limit: 返回数量，默认为20，最大值为100。关于`Limit`的更进一步介绍请参考 API 简介中的相关小节。
                :type Limit: int
        """
        self.Ip6AddressIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.Ip6AddressIds = params.get("Ip6AddressIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeIp6AddressesResponse(AbstractModel):
    """DescribeIp6Addresses返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的 IPV6 数量。
        :type TotalCount: int
        :param AddressSet: IPV6 详细信息列表。
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


class DescribeIp6IdcInfoRequest(AbstractModel):
    """DescribeIp6IdcInfo请求参数结构体"""


class DescribeIp6IdcInfoResponse(AbstractModel):
    """DescribeIp6IdcInfo返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeIp6TranslatorQuotaRequest(AbstractModel):
    """DescribeIp6TranslatorQuota请求参数结构体"""

    def __init__(self):
        """
        :param Ip6TranslatorIds: 待查询IPV6转换实例的唯一ID列表，形如ip6-xxxxxxxx
        :type Ip6TranslatorIds: list of str
        """
        self.Ip6TranslatorIds = None

    def _deserialize(self, params):
        self.Ip6TranslatorIds = params.get("Ip6TranslatorIds")


class DescribeIp6TranslatorQuotaResponse(AbstractModel):
    """DescribeIp6TranslatorQuota返回参数结构体"""

    def __init__(self):
        """
                :param QuotaSet: 账户在指定地域的IPV6转换实例及规则配额信息
        QUOTAID属性是TOTAL_TRANSLATOR_QUOTA，表示账户在指定地域的IPV6转换实例配额信息；QUOTAID属性是IPV6转换实例唯一ID（形如ip6-xxxxxxxx），表示账户在该转换实例允许创建的转换规则配额
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


class DescribeIp6TranslatorsRequest(AbstractModel):
    """DescribeIp6Translators请求参数结构体"""

    def __init__(self):
        """
                :param Ip6TranslatorIds: IPV6转换实例唯一ID数组，形如ip6-xxxxxxxx
                :type Ip6TranslatorIds: list of str
                :param Filters: 每次请求的`Filters`的上限为10，`Filter.Values`的上限为5。参数不支持同时指定`Ip6TranslatorIds`和`Filters`。详细的过滤条件如下：
        <li> ip6-translator-id - String - 是否必填：否 - （过滤条件）按照IPV6转换实例的唯一ID过滤,形如ip6-xxxxxxx。</li>
        <li> ip6-translator-vip6 - String - 是否必填：否 - （过滤条件）按照IPV6地址过滤。不支持模糊过滤。</li>
        <li> ip6-translator-name - String - 是否必填：否 - （过滤条件）按照IPV6转换实例名称过滤。不支持模糊过滤。</li>
        <li> ip6-translator-status - String - 是否必填：否 - （过滤条件）按照IPV6转换实例的状态过滤。状态取值范围为"CREATING","RUNNING","DELETING","MODIFYING"
                :type Filters: list of Filter
                :param Offset: 偏移量，默认为0。关于`Offset`的更进一步介绍请参考 API 简介中的相关小节。
                :type Offset: int
                :param Limit: 返回数量，默认为20，最大值为100。关于`Limit`的更进一步介绍请参考 API 简介中的相关小节。
                :type Limit: int
        """
        self.Ip6TranslatorIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.Ip6TranslatorIds = params.get("Ip6TranslatorIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeIp6TranslatorsResponse(AbstractModel):
    """DescribeIp6Translators返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合过滤条件的IPV6转换实例数量。
        :type TotalCount: int
        :param Ip6TranslatorSet: 符合过滤条件的IPV6转换实例详细信息
        :type Ip6TranslatorSet: list of Ip6Translator
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.Ip6TranslatorSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Ip6TranslatorSet") is not None:
            self.Ip6TranslatorSet = []
            for item in params.get("Ip6TranslatorSet"):
                obj = Ip6Translator()
                obj._deserialize(item)
                self.Ip6TranslatorSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeIpLocationDownloadLinkRequest(AbstractModel):
    """DescribeIpLocationDownloadLink请求参数结构体"""

    def __init__(self):
        """
        :param Type: ip地址库类型，目前仅支持"ipv4"和"ipv6"。
        :type Type: str
        """
        self.Type = None

    def _deserialize(self, params):
        self.Type = params.get("Type")


class DescribeIpLocationDownloadLinkResponse(AbstractModel):
    """DescribeIpLocationDownloadLink返回参数结构体"""

    def __init__(self):
        """
        :param DownLoadUrl: 下载链接地址
        :type DownLoadUrl: str
        :param ExpiredAt: 链接到期时间。按照`ISO8601`标准表示，并且使用`UTC`时间。格式为：`YYYY-MM-DDThh:mm:ssZ`。
        :type ExpiredAt: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DownLoadUrl = None
        self.ExpiredAt = None
        self.RequestId = None

    def _deserialize(self, params):
        self.DownLoadUrl = params.get("DownLoadUrl")
        self.ExpiredAt = params.get("ExpiredAt")
        self.RequestId = params.get("RequestId")


class DescribeIpLocationRequest(AbstractModel):
    """DescribeIpLocation请求参数结构体"""

    def __init__(self):
        """
        :param AddressIps: IP地址列表，支持IPv4和IPv6。
        :type AddressIps: list of str
        :param Fields: IP地址的字段信息
        :type Fields: :class:`tcecloud.vpc.v20170312.models.IpField`
        """
        self.AddressIps = None
        self.Fields = None

    def _deserialize(self, params):
        self.AddressIps = params.get("AddressIps")
        if params.get("Fields") is not None:
            self.Fields = IpField()
            self.Fields._deserialize(params.get("Fields"))


class DescribeIpLocationResponse(AbstractModel):
    """DescribeIpLocation返回参数结构体"""

    def __init__(self):
        """
        :param AddressInfo: IP地址信息列表
        :type AddressInfo: :class:`tcecloud.vpc.v20170312.models.AddressLibInfo`
        :param Total: IP地址信息个数
        :type Total: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AddressInfo = None
        self.Total = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("AddressInfo") is not None:
            self.AddressInfo = AddressLibInfo()
            self.AddressInfo._deserialize(params.get("AddressInfo"))
        self.Total = params.get("Total")
        self.RequestId = params.get("RequestId")


class DescribeIpOnlineRequest(AbstractModel):
    """DescribeIpOnline请求参数结构体"""

    def __init__(self):
        """
        :param AddressIps: IP地址列表，支持IPv4和IPv6
        :type AddressIps: list of str
        :param Fields: 需要获取的字段信息
        :type Fields: :class:`tcecloud.vpc.v20170312.models.IpField`
        """
        self.AddressIps = None
        self.Fields = None

    def _deserialize(self, params):
        self.AddressIps = params.get("AddressIps")
        if params.get("Fields") is not None:
            self.Fields = IpField()
            self.Fields._deserialize(params.get("Fields"))


class DescribeIpOnlineResponse(AbstractModel):
    """DescribeIpOnline返回参数结构体"""

    def __init__(self):
        """
        :param AddressInfo: IP地址库信息列表
        :type AddressInfo: :class:`tcecloud.vpc.v20170312.models.AddressLibInfo`
        :param Total: IP地址库信息个数
        :type Total: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AddressInfo = None
        self.Total = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("AddressInfo") is not None:
            self.AddressInfo = AddressLibInfo()
            self.AddressInfo._deserialize(params.get("AddressInfo"))
        self.Total = params.get("Total")
        self.RequestId = params.get("RequestId")


class DescribeLocalDestinationIpPortTranslationNatRulesRequest(AbstractModel):
    """DescribeLocalDestinationIpPortTranslationNatRules请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID
        :type DirectConnectGatewayId: str
        :param VpcId: 字符型VPCID
        :type VpcId: str
        :param Offset: 偏移量
        :type Offset: int
        :param Limit: 请求对象个数
        :type Limit: int
        :param Filters: 过滤条件
        :type Filters: list of Filter
        """
        self.DirectConnectGatewayId = None
        self.VpcId = None
        self.Offset = None
        self.Limit = None
        self.Filters = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.VpcId = params.get("VpcId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)


class DescribeLocalDestinationIpPortTranslationNatRulesResponse(AbstractModel):
    """DescribeLocalDestinationIpPortTranslationNatRules返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeLocalIpTranslationAclRulesRequest(AbstractModel):
    """DescribeLocalIpTranslationAclRules请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID
        :type DirectConnectGatewayId: str
        :param VpcId: 字符型VPCID
        :type VpcId: str
        :param Offset: 偏移量
        :type Offset: int
        :param Limit: 请求对象个数
        :type Limit: int
        :param Filters: 过滤条件
        :type Filters: list of Filter
        """
        self.DirectConnectGatewayId = None
        self.VpcId = None
        self.Offset = None
        self.Limit = None
        self.Filters = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.VpcId = params.get("VpcId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)


class DescribeLocalIpTranslationAclRulesResponse(AbstractModel):
    """DescribeLocalIpTranslationAclRules返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeLocalIpTranslationNatRulesRequest(AbstractModel):
    """DescribeLocalIpTranslationNatRules请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID
        :type DirectConnectGatewayId: str
        :param VpcId: 字符型VPCID
        :type VpcId: str
        :param Offset: 偏移量
        :type Offset: int
        :param Limit: 请求对象个数
        :type Limit: int
        :param Filters: 过滤条件
        :type Filters: list of Filter
        """
        self.DirectConnectGatewayId = None
        self.VpcId = None
        self.Offset = None
        self.Limit = None
        self.Filters = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.VpcId = params.get("VpcId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)


class DescribeLocalIpTranslationNatRulesResponse(AbstractModel):
    """DescribeLocalIpTranslationNatRules返回参数结构体"""

    def __init__(self):
        """
        :param LocalIpTranslationNatRuleSet: 本端IP转换列表
        :type LocalIpTranslationNatRuleSet: list of LocalIpTranslationNatRule
        :param TotalCount: 满足条件的本端IP转换列表数目
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.LocalIpTranslationNatRuleSet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("LocalIpTranslationNatRuleSet") is not None:
            self.LocalIpTranslationNatRuleSet = []
            for item in params.get("LocalIpTranslationNatRuleSet"):
                obj = LocalIpTranslationNatRule()
                obj._deserialize(item)
                self.LocalIpTranslationNatRuleSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeLocalSourceIpPortTranslationAclRulesRequest(AbstractModel):
    """DescribeLocalSourceIpPortTranslationAclRules请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID
        :type DirectConnectGatewayId: str
        :param VpcId: 字符型VPCID
        :type VpcId: str
        :param Offset: 偏移量
        :type Offset: int
        :param Limit: 请求对象个数
        :type Limit: int
        :param Filters: 过滤条件
        :type Filters: list of Filter
        """
        self.DirectConnectGatewayId = None
        self.VpcId = None
        self.Offset = None
        self.Limit = None
        self.Filters = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.VpcId = params.get("VpcId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)


class DescribeLocalSourceIpPortTranslationAclRulesResponse(AbstractModel):
    """DescribeLocalSourceIpPortTranslationAclRules返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeLocalSourceIpPortTranslationNatRulesRequest(AbstractModel):
    """DescribeLocalSourceIpPortTranslationNatRules请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID
        :type DirectConnectGatewayId: str
        :param VpcId: 字符型VPCID
        :type VpcId: str
        :param Offset: 偏移量
        :type Offset: int
        :param Limit: 请求对象个数
        :type Limit: int
        :param Filters: 过滤条件
        :type Filters: list of Filter
        """
        self.DirectConnectGatewayId = None
        self.VpcId = None
        self.Offset = None
        self.Limit = None
        self.Filters = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.VpcId = params.get("VpcId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)


class DescribeLocalSourceIpPortTranslationNatRulesResponse(AbstractModel):
    """DescribeLocalSourceIpPortTranslationNatRules返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeNatGatewayDestinationIpPortTranslationNatRulesRequest(AbstractModel):
    """DescribeNatGatewayDestinationIpPortTranslationNatRules请求参数结构体"""

    def __init__(self):
        """
                :param NatGatewayIds: NAT网关ID。
                :type NatGatewayIds: list of str
                :param Filters: 过滤条件:
        参数不支持同时指定NatGatewayIds和Filters。
        <li> nat-gateway-id，NAT网关的ID，如`nat-0yi4hekt`</li>
        <li> vpc-id，私有网络VPC的ID，如`vpc-0yi4hekt`</li>
        <li> public-ip-address， 弹性IP，如`139.199.232.238`。</li>
        <li>public-port， 公网端口。</li>
        <li>private-ip-address， 内网IP，如`10.0.0.1`。</li>
        <li>private-port， 内网端口。</li>
        <li>description，规则描述。</li>
                :type Filters: list of Filter
                :param Offset: 偏移量，默认为0。
                :type Offset: int
                :param Limit: 返回数量，默认为20，最大值为100。
                :type Limit: int
        """
        self.NatGatewayIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.NatGatewayIds = params.get("NatGatewayIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeNatGatewayDestinationIpPortTranslationNatRulesResponse(AbstractModel):
    """DescribeNatGatewayDestinationIpPortTranslationNatRules返回参数结构体"""

    def __init__(self):
        """
        :param NatGatewayDestinationIpPortTranslationNatRuleSet: NAT网关端口转发规则对象数组。
        :type NatGatewayDestinationIpPortTranslationNatRuleSet: list of NatGatewayDestinationIpPortTranslationNatRule
        :param TotalCount: 符合条件的NAT网关端口转发规则对象数目。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.NatGatewayDestinationIpPortTranslationNatRuleSet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("NatGatewayDestinationIpPortTranslationNatRuleSet") is not None:
            self.NatGatewayDestinationIpPortTranslationNatRuleSet = []
            for item in params.get("NatGatewayDestinationIpPortTranslationNatRuleSet"):
                obj = NatGatewayDestinationIpPortTranslationNatRule()
                obj._deserialize(item)
                self.NatGatewayDestinationIpPortTranslationNatRuleSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeNatGatewayQuotaRequest(AbstractModel):
    """DescribeNatGatewayQuota请求参数结构体"""

    def __init__(self):
        """
        :param Zone: 可用区信息
        :type Zone: str
        :param NatGatewayId: NAT网关统一 ID，形如：“nat-abceef"
        :type NatGatewayId: str
        """
        self.Zone = None
        self.NatGatewayId = None

    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.NatGatewayId = params.get("NatGatewayId")


class DescribeNatGatewayQuotaResponse(AbstractModel):
    """DescribeNatGatewayQuota返回参数结构体"""

    def __init__(self):
        """
        :param NatGatewayQuota: NAT网关配额对象。
        :type NatGatewayQuota: :class:`tcecloud.vpc.v20170312.models.NatGatewayQuota`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.NatGatewayQuota = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("NatGatewayQuota") is not None:
            self.NatGatewayQuota = NatGatewayQuota()
            self.NatGatewayQuota._deserialize(params.get("NatGatewayQuota"))
        self.RequestId = params.get("RequestId")


class DescribeNatGatewaysRequest(AbstractModel):
    """DescribeNatGateways请求参数结构体"""

    def __init__(self):
        """
                :param NatGatewayIds: NAT网关统一 ID，形如：`nat-123xx454`。
                :type NatGatewayIds: list of str
                :param Filters: 过滤条件，参数不支持同时指定NatGatewayIds和Filters。
        <li>nat-gateway-id - String - （过滤条件）协议端口模板实例ID，形如：`nat-123xx454`。</li>
        <li>vpc-id - String - （过滤条件）私有网络 唯一ID，形如：`vpc-123xx454`。</li>
        <li>nat-gateway-name - String - （过滤条件）协议端口模板实例ID，形如：`test_nat`。</li>
                :type Filters: list of Filter
                :param Offset: 偏移量，默认为0。
                :type Offset: int
                :param Limit: 返回数量，默认为20，最大值为100。
                :type Limit: int
        """
        self.NatGatewayIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.NatGatewayIds = params.get("NatGatewayIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeNatGatewaysResponse(AbstractModel):
    """DescribeNatGateways返回参数结构体"""

    def __init__(self):
        """
        :param NatGatewaySet: NAT网关对象数组。
        :type NatGatewaySet: list of NatGateway
        :param TotalCount: 符合条件的NAT网关对象个数。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.NatGatewaySet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("NatGatewaySet") is not None:
            self.NatGatewaySet = []
            for item in params.get("NatGatewaySet"):
                obj = NatGateway()
                obj._deserialize(item)
                self.NatGatewaySet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeNetDetectStatesRequest(AbstractModel):
    """DescribeNetDetectStates请求参数结构体"""

    def __init__(self):
        """
                :param NetDetectIds: 网络探测实例`ID`数组。形如：[`netd-12345678`]
                :type NetDetectIds: list of str
                :param Filters: 过滤条件，参数不支持同时指定NetDetectIds和Filters。
        <li>net-detect-id - String - （过滤条件）网络探测实例ID，形如：netd-12345678</li>
                :type Filters: list of Filter
                :param Offset: 偏移量，默认为0。
                :type Offset: int
                :param Limit: 返回数量，默认为20，最大值为100。
                :type Limit: int
        """
        self.NetDetectIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.NetDetectIds = params.get("NetDetectIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeNetDetectStatesResponse(AbstractModel):
    """DescribeNetDetectStates返回参数结构体"""

    def __init__(self):
        """
        :param NetDetectStateSet: 符合条件的网络探测验证结果对象数组。
        :type NetDetectStateSet: list of NetDetectState
        :param TotalCount: 符合条件的网络探测验证结果对象数量。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.NetDetectStateSet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("NetDetectStateSet") is not None:
            self.NetDetectStateSet = []
            for item in params.get("NetDetectStateSet"):
                obj = NetDetectState()
                obj._deserialize(item)
                self.NetDetectStateSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeNetDetectsRequest(AbstractModel):
    """DescribeNetDetects请求参数结构体"""

    def __init__(self):
        """
                :param NetDetectIds: 网络探测实例`ID`数组。形如：[`netd-12345678`]
                :type NetDetectIds: list of str
                :param Filters: 过滤条件，参数不支持同时指定NetDetectIds和Filters。
        <li>vpc-id - String - （过滤条件）VPC实例ID，形如：vpc-12345678</li>
        <li>net-detect-id - String - （过滤条件）网络探测实例ID，形如：netd-12345678</li>
        <li>subnet-id - String - （过滤条件）子网实例ID，形如：subnet-12345678</li>
        <li>net-detect-name - String - （过滤条件）网络探测名称</li>
                :type Filters: list of Filter
                :param Offset: 偏移量，默认为0。
                :type Offset: int
                :param Limit: 返回数量，默认为20，最大值为100。
                :type Limit: int
        """
        self.NetDetectIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.NetDetectIds = params.get("NetDetectIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeNetDetectsResponse(AbstractModel):
    """DescribeNetDetects返回参数结构体"""

    def __init__(self):
        """
        :param NetDetectSet: 符合条件的网络探测对象数组。
        :type NetDetectSet: list of NetDetect
        :param TotalCount: 符合条件的网络探测对象数量。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.NetDetectSet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("NetDetectSet") is not None:
            self.NetDetectSet = []
            for item in params.get("NetDetectSet"):
                obj = NetDetect()
                obj._deserialize(item)
                self.NetDetectSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeNetworkAclsRequest(AbstractModel):
    """DescribeNetworkAcls请求参数结构体"""

    def __init__(self):
        """
                :param NetworkAclIds: 网络ACL实例ID数组。形如：[acl-12345678]。每次请求的实例的上限为100。参数不支持同时指定NetworkAclIds和Filters。
                :type NetworkAclIds: list of str
                :param Filters: 过滤条件，参数不支持同时指定NetworkAclIds和Filters。
        <li>vpc-id - String - （过滤条件）VPC实例ID，形如：vpc-12345678。</li>
        <li>network-acl-id - String - （过滤条件）网络ACL实例ID，形如：acl-12345678。</li>
        <li>network-acl-name - String - （过滤条件）网络ACL实例名称。</li>
                :type Filters: list of Filter
                :param Offset: 偏移量，默认为0。
                :type Offset: int
                :param Limit: 返回数量，默认为20，最小值为1，最大值为100。
                :type Limit: int
        """
        self.NetworkAclIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.NetworkAclIds = params.get("NetworkAclIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeNetworkAclsResponse(AbstractModel):
    """DescribeNetworkAcls返回参数结构体"""

    def __init__(self):
        """
        :param NetworkAclSet: 实例详细信息列表。
        :type NetworkAclSet: list of NetworkAcl
        :param TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.NetworkAclSet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("NetworkAclSet") is not None:
            self.NetworkAclSet = []
            for item in params.get("NetworkAclSet"):
                obj = NetworkAcl()
                obj._deserialize(item)
                self.NetworkAclSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeNetworkInterfaceExtendIpsRequest(AbstractModel):
    """DescribeNetworkInterfaceExtendIps请求参数结构体"""

    def __init__(self):
        """
        :param NetworkInterfaceIds: 弹性网卡的唯一id列表
        :type NetworkInterfaceIds: list of str
        :param Offset: 偏移量，默认为0。
        :type Offset: int
        :param Limit: 每页行数，默认为100
        :type Limit: int
        """
        self.NetworkInterfaceIds = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.NetworkInterfaceIds = params.get("NetworkInterfaceIds")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeNetworkInterfaceExtendIpsResponse(AbstractModel):
    """DescribeNetworkInterfaceExtendIps返回参数结构体"""

    def __init__(self):
        """
        :param NetworkInterfaceExtendIpSet: 返回扩展ip段
        :type NetworkInterfaceExtendIpSet: list of NetworkInterfaceExtendIp
        :param TotalCount: 返回总条目数
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.NetworkInterfaceExtendIpSet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("NetworkInterfaceExtendIpSet") is not None:
            self.NetworkInterfaceExtendIpSet = []
            for item in params.get("NetworkInterfaceExtendIpSet"):
                obj = NetworkInterfaceExtendIp()
                obj._deserialize(item)
                self.NetworkInterfaceExtendIpSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeNetworkInterfaceLimitRequest(AbstractModel):
    """DescribeNetworkInterfaceLimit请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 要查询的CVM实例ID或弹性网卡ID
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class DescribeNetworkInterfaceLimitResponse(AbstractModel):
    """DescribeNetworkInterfaceLimit返回参数结构体"""

    def __init__(self):
        """
        :param EniQuantity: 弹性网卡配额
        :type EniQuantity: int
        :param EniPrivateIpAddressQuantity: 每个弹性网卡可以分配的IP配额
        :type EniPrivateIpAddressQuantity: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.EniQuantity = None
        self.EniPrivateIpAddressQuantity = None
        self.RequestId = None

    def _deserialize(self, params):
        self.EniQuantity = params.get("EniQuantity")
        self.EniPrivateIpAddressQuantity = params.get("EniPrivateIpAddressQuantity")
        self.RequestId = params.get("RequestId")


class DescribeNetworkInterfacesExtraRequest(AbstractModel):
    """DescribeNetworkInterfacesExtra请求参数结构体"""

    def __init__(self):
        """
                :param NetworkInterfaceIds: 弹性网卡实例ID查询。形如：eni-pxir56ns。每次请求的实例的上限为100。参数不支持同时指定NetworkInterfaceIds和Filters。
                :type NetworkInterfaceIds: list of str
                :param Filters: 过滤条件，参数不支持同时指定NetworkInterfaceIds和Filters。
        <li>vpc-id - String - （过滤条件）VPC实例ID，形如：vpc-f49l6u0z。</li>
        <li>network-interface-id - String - （过滤条件）弹性网卡实例ID，形如：eni-5k56k7k7。</li>
        <li>address-ip - String - （过滤条件）弹性网卡内网IP。单IP模糊查询，多IP精确查询。</li>
        <li>wan-ip - String - （过滤条件）弹性网卡公网IP。单IP模糊查询，多IP精确查询。</li>
        <li>instance-id - String - （过滤条件）子机实例ID。</li>
        <li>instance-name - String - （过滤条件）子机实例的名称。</li>
        <li>subnet-id - String - （过滤条件）子网ID。</li>
        <li>is-primary-eni - Boolean - 是否必填：否 - （过滤条件）按照是否主网卡进行过滤。值为true时，仅过滤主网卡；值为false时，仅过滤辅助网卡；次过滤参数为提供时，同时过滤主网卡和辅助网卡。</li>
        <li>is-primary-ip - Boolean - 是否必填：否 - （过滤条件）按照是否主IP进行过滤。值为true时，仅过滤主IP；值为false时，仅过滤辅助IP；无过滤参数为提供时，同时过滤主网卡和辅助网卡。</li>
        <li>is-ipv6 - Boolean - 是否必填：否 - （过滤条件）按照是否ipv6地址进行过滤。值为false或者不传递时，仅过滤ipv4地址；值为true时，仅过滤ipv6地址。</li>
        <li>skip-main-eni-main-pip - Boolean - 是否必填：否 - （过滤条件）过滤掉主网卡的主ip。值为true时，仅过滤掉主网卡的主IP地址。</li>
                :type Filters: list of Filter
                :param Offset: 偏移量，默认为0。
                :type Offset: int
                :param Limit: 返回数量，默认为20，最大值为100。
                :type Limit: int
        """
        self.NetworkInterfaceIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.NetworkInterfaceIds = params.get("NetworkInterfaceIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeNetworkInterfacesExtraResponse(AbstractModel):
    """DescribeNetworkInterfacesExtra返回参数结构体"""

    def __init__(self):
        """
        :param NetworkInterfaceSet: 实例详细信息列表。
        :type NetworkInterfaceSet: list of NetworkInterface
        :param TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.NetworkInterfaceSet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("NetworkInterfaceSet") is not None:
            self.NetworkInterfaceSet = []
            for item in params.get("NetworkInterfaceSet"):
                obj = NetworkInterface()
                obj._deserialize(item)
                self.NetworkInterfaceSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeNetworkInterfacesRequest(AbstractModel):
    """DescribeNetworkInterfaces请求参数结构体"""

    def __init__(self):
        """
                :param NetworkInterfaceIds: 弹性网卡实例ID查询。形如：eni-pxir56ns。每次请求的实例的上限为100。参数不支持同时指定NetworkInterfaceIds和Filters。
                :type NetworkInterfaceIds: list of str
                :param Filters: 过滤条件，参数不支持同时指定NetworkInterfaceIds和Filters。
        <li>vpc-id - String - （过滤条件）VPC实例ID，形如：vpc-f49l6u0z。</li>
        <li>subnet-id - String - （过滤条件）所属子网实例ID，形如：subnet-f49l6u0z。</li>
        <li>network-interface-id - String - （过滤条件）弹性网卡实例ID，形如：eni-5k56k7k7。</li>
        <li>attachment.instance-id - String - （过滤条件）绑定的云服务器实例ID，形如：ins-3nqpdn3i。</li>
        <li>groups.security-group-id - String - （过滤条件）绑定的安全组实例ID，例如：sg-f9ekbxeq。</li>
        <li>network-interface-name - String - （过滤条件）网卡实例名称。</li>
        <li>network-interface-description - String - （过滤条件）网卡实例描述。</li>
        <li>address-ip - String - （过滤条件）内网IPv4地址。</li>
        <li>tag-key - String -是否必填：否- （过滤条件）按照标签键进行过滤。使用请参考示例2</li>
        <li>tag:tag-key - String - 是否必填：否 - （过滤条件）按照标签键值对进行过滤。 tag-key使用具体的标签键进行替换。使用请参考示例3。</li>
        <li>is-primary - Boolean - 是否必填：否 - （过滤条件）按照是否主网卡进行过滤。值为true时，仅过滤主网卡；值为false时，仅过滤辅助网卡；次过滤参数为提供时，同时过滤主网卡和辅助网卡。</li>
                :type Filters: list of Filter
                :param Offset: 偏移量，默认为0。
                :type Offset: int
                :param Limit: 返回数量，默认为20，最大值为100。
                :type Limit: int
        """
        self.NetworkInterfaceIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.NetworkInterfaceIds = params.get("NetworkInterfaceIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeNetworkInterfacesResponse(AbstractModel):
    """DescribeNetworkInterfaces返回参数结构体"""

    def __init__(self):
        """
        :param NetworkInterfaceSet: 实例详细信息列表。
        :type NetworkInterfaceSet: list of NetworkInterface
        :param TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.NetworkInterfaceSet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("NetworkInterfaceSet") is not None:
            self.NetworkInterfaceSet = []
            for item in params.get("NetworkInterfaceSet"):
                obj = NetworkInterface()
                obj._deserialize(item)
                self.NetworkInterfaceSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeNmsCidrsRequest(AbstractModel):
    """DescribeNmsCidrs请求参数结构体"""


class DescribeNmsCidrsResponse(AbstractModel):
    """DescribeNmsCidrs返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribePeerIpTranslationNatRulesRequest(AbstractModel):
    """DescribePeerIpTranslationNatRules请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID
        :type DirectConnectGatewayId: str
        :param VpcId: 字符型VPCID
        :type VpcId: str
        :param Offset: 偏移量
        :type Offset: int
        :param Limit: 请求对象个数
        :type Limit: int
        :param Filters: 过滤条件
        :type Filters: list of Filter
        """
        self.DirectConnectGatewayId = None
        self.VpcId = None
        self.Offset = None
        self.Limit = None
        self.Filters = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.VpcId = params.get("VpcId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)


class DescribePeerIpTranslationNatRulesResponse(AbstractModel):
    """DescribePeerIpTranslationNatRules返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeRegionsRequest(AbstractModel):
    """DescribeRegions请求参数结构体"""


class DescribeRegionsResponse(AbstractModel):
    """DescribeRegions返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 已开服的所有大区列表。
        :type TotalCount: int
        :param RegionSet: 地域信息列表。
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


class DescribeRouteConflictsRequest(AbstractModel):
    """DescribeRouteConflicts请求参数结构体"""

    def __init__(self):
        """
        :param RouteTableId: 路由表实例ID，例如：rtb-azd4dt1c。
        :type RouteTableId: str
        :param DestinationCidrBlocks: 要检查的与之冲突的目的端列表
        :type DestinationCidrBlocks: list of str
        """
        self.RouteTableId = None
        self.DestinationCidrBlocks = None

    def _deserialize(self, params):
        self.RouteTableId = params.get("RouteTableId")
        self.DestinationCidrBlocks = params.get("DestinationCidrBlocks")


class DescribeRouteConflictsResponse(AbstractModel):
    """DescribeRouteConflicts返回参数结构体"""

    def __init__(self):
        """
        :param RouteConflictSet: 路由策略冲突列表
        :type RouteConflictSet: list of RouteConflict
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RouteConflictSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("RouteConflictSet") is not None:
            self.RouteConflictSet = []
            for item in params.get("RouteConflictSet"):
                obj = RouteConflict()
                obj._deserialize(item)
                self.RouteConflictSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeRouteTablesRequest(AbstractModel):
    """DescribeRouteTables请求参数结构体"""

    def __init__(self):
        """
                :param RouteTableIds: 路由表实例ID，例如：rtb-azd4dt1c。
                :type RouteTableIds: list of str
                :param Filters: 过滤条件，参数不支持同时指定RouteTableIds和Filters。
        <li>route-table-id - String - （过滤条件）路由表实例ID。</li>
        <li>route-table-name - String - （过滤条件）路由表名称。</li>
        <li>vpc-id - String - （过滤条件）VPC实例ID，形如：vpc-f49l6u0z。</li>
        <li>association.main - String - （过滤条件）是否主路由表。</li>
        <li>tag-key - String -是否必填：否- （过滤条件）按照标签键进行过滤。</li>
        <li>tag:tag-key - String - 是否必填：否 - （过滤条件）按照标签键值对进行过滤。 tag-key使用具体的标签键进行替换。使用请参考示例2。</li>
                :type Filters: list of Filter
                :param Offset: 偏移量。
                :type Offset: str
                :param Limit: 请求对象个数。
                :type Limit: str
        """
        self.RouteTableIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.RouteTableIds = params.get("RouteTableIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeRouteTablesResponse(AbstractModel):
    """DescribeRouteTables返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param RouteTableSet: 路由表对象。
        :type RouteTableSet: list of RouteTable
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.RouteTableSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("RouteTableSet") is not None:
            self.RouteTableSet = []
            for item in params.get("RouteTableSet"):
                obj = RouteTable()
                obj._deserialize(item)
                self.RouteTableSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeRoutesRequest(AbstractModel):
    """DescribeRoutes请求参数结构体"""

    def __init__(self):
        """
                :param Filters: 过滤条件，参数不支持同时指定RouteTableIds和Filters。
        <li>vpc-id - String - （过滤条件）VPC实例ID，形如：vpc-f49l6u0z。</li>
        <li>gateway-id - String - （过滤条件）网关ID。</li>
        <li>description - String - （过滤条件）路由描述。</li>
                :type Filters: list of Filter
                :param Offset: 偏移量。
                :type Offset: int
                :param Limit: 请求对象个数。
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


class DescribeRoutesResponse(AbstractModel):
    """DescribeRoutes返回参数结构体"""

    def __init__(self):
        """
        :param RouteSet: 路由对象。
        :type RouteSet: list of Route
        :param TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RouteSet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("RouteSet") is not None:
            self.RouteSet = []
            for item in params.get("RouteSet"):
                obj = Route()
                obj._deserialize(item)
                self.RouteSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeSecurityGroupAssociationStatisticsRequest(AbstractModel):
    """DescribeSecurityGroupAssociationStatistics请求参数结构体"""

    def __init__(self):
        """
        :param SecurityGroupIds: 安全实例ID，例如sg-33ocnj9n，可通过DescribeSecurityGroups获取。
        :type SecurityGroupIds: list of str
        """
        self.SecurityGroupIds = None

    def _deserialize(self, params):
        self.SecurityGroupIds = params.get("SecurityGroupIds")


class DescribeSecurityGroupAssociationStatisticsResponse(AbstractModel):
    """DescribeSecurityGroupAssociationStatistics返回参数结构体"""

    def __init__(self):
        """
        :param SecurityGroupAssociationStatisticsSet: 安全组关联实例统计。
        :type SecurityGroupAssociationStatisticsSet: list of SecurityGroupAssociationStatistics
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SecurityGroupAssociationStatisticsSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("SecurityGroupAssociationStatisticsSet") is not None:
            self.SecurityGroupAssociationStatisticsSet = []
            for item in params.get("SecurityGroupAssociationStatisticsSet"):
                obj = SecurityGroupAssociationStatistics()
                obj._deserialize(item)
                self.SecurityGroupAssociationStatisticsSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeSecurityGroupLimitsRequest(AbstractModel):
    """DescribeSecurityGroupLimits请求参数结构体"""


class DescribeSecurityGroupLimitsResponse(AbstractModel):
    """DescribeSecurityGroupLimits返回参数结构体"""

    def __init__(self):
        """
        :param SecurityGroupLimitSet: 用户安全组配额限制。
        :type SecurityGroupLimitSet: :class:`tcecloud.vpc.v20170312.models.SecurityGroupLimitSet`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SecurityGroupLimitSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("SecurityGroupLimitSet") is not None:
            self.SecurityGroupLimitSet = SecurityGroupLimitSet()
            self.SecurityGroupLimitSet._deserialize(params.get("SecurityGroupLimitSet"))
        self.RequestId = params.get("RequestId")


class DescribeSecurityGroupPoliciesRequest(AbstractModel):
    """DescribeSecurityGroupPolicies请求参数结构体"""

    def __init__(self):
        """
        :param SecurityGroupId: 安全组实例ID，例如：sg-33ocnj9n，可通过DescribeSecurityGroups获取。
        :type SecurityGroupId: str
        """
        self.SecurityGroupId = None

    def _deserialize(self, params):
        self.SecurityGroupId = params.get("SecurityGroupId")


class DescribeSecurityGroupPoliciesResponse(AbstractModel):
    """DescribeSecurityGroupPolicies返回参数结构体"""

    def __init__(self):
        """
        :param SecurityGroupPolicySet: 安全组规则集合。
        :type SecurityGroupPolicySet: :class:`tcecloud.vpc.v20170312.models.SecurityGroupPolicySet`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SecurityGroupPolicySet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("SecurityGroupPolicySet") is not None:
            self.SecurityGroupPolicySet = SecurityGroupPolicySet()
            self.SecurityGroupPolicySet._deserialize(params.get("SecurityGroupPolicySet"))
        self.RequestId = params.get("RequestId")


class DescribeSecurityGroupPolicyTemplatesRequest(AbstractModel):
    """DescribeSecurityGroupPolicyTemplates请求参数结构体"""

    def __init__(self):
        """
        :param SceneTag: 场景tag。
        :type SceneTag: str
        """
        self.SceneTag = None

    def _deserialize(self, params):
        self.SceneTag = params.get("SceneTag")


class DescribeSecurityGroupPolicyTemplatesResponse(AbstractModel):
    """DescribeSecurityGroupPolicyTemplates返回参数结构体"""

    def __init__(self):
        """
        :param SecurityGroupPolicyTemplateSet: 安全组规则模板列表。
        :type SecurityGroupPolicyTemplateSet: list of SecurityGroupPolicyTemplate
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SecurityGroupPolicyTemplateSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("SecurityGroupPolicyTemplateSet") is not None:
            self.SecurityGroupPolicyTemplateSet = []
            for item in params.get("SecurityGroupPolicyTemplateSet"):
                obj = SecurityGroupPolicyTemplate()
                obj._deserialize(item)
                self.SecurityGroupPolicyTemplateSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeSecurityGroupReferencesRequest(AbstractModel):
    """DescribeSecurityGroupReferences请求参数结构体"""

    def __init__(self):
        """
        :param SecurityGroupIds: 安全组实例ID数组。格式如：['sg-12345678']
        :type SecurityGroupIds: list of str
        """
        self.SecurityGroupIds = None

    def _deserialize(self, params):
        self.SecurityGroupIds = params.get("SecurityGroupIds")


class DescribeSecurityGroupReferencesResponse(AbstractModel):
    """DescribeSecurityGroupReferences返回参数结构体"""

    def __init__(self):
        """
        :param ReferredSecurityGroupSet: 安全组被引用信息。
        :type ReferredSecurityGroupSet: list of ReferredSecurityGroup
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ReferredSecurityGroupSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("ReferredSecurityGroupSet") is not None:
            self.ReferredSecurityGroupSet = []
            for item in params.get("ReferredSecurityGroupSet"):
                obj = ReferredSecurityGroup()
                obj._deserialize(item)
                self.ReferredSecurityGroupSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeSecurityGroupsRequest(AbstractModel):
    """DescribeSecurityGroups请求参数结构体"""

    def __init__(self):
        """
                :param SecurityGroupIds: 安全组实例ID，例如：sg-33ocnj9n，可通过DescribeSecurityGroups获取。每次请求的实例的上限为100。参数不支持同时指定SecurityGroupIds和Filters。
                :type SecurityGroupIds: list of str
                :param Filters: 过滤条件，参数不支持同时指定SecurityGroupIds和Filters。
        <li>security-group-id - String - （过滤条件）安全组ID。</li>
        <li>project-id - Integer - （过滤条件）项目ID。</li>
        <li>security-group-name - String - （过滤条件）安全组名称。</li>
        <li>tag-key - String -是否必填：否- （过滤条件）按照标签键进行过滤。使用请参考示例2。</li>
        <li>tag:tag-key - String - 是否必填：否 - （过滤条件）按照标签键值对进行过滤。 tag-key使用具体的标签键进行替换。使用请参考示例3。</li>
                :type Filters: list of Filter
                :param Offset: 偏移量，默认为0。
                :type Offset: str
                :param Limit: 返回数量，默认为20，最大值为100。
                :type Limit: str
        """
        self.SecurityGroupIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.SecurityGroupIds = params.get("SecurityGroupIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeSecurityGroupsResponse(AbstractModel):
    """DescribeSecurityGroups返回参数结构体"""

    def __init__(self):
        """
        :param SecurityGroupSet: 安全组对象。
        :type SecurityGroupSet: list of SecurityGroup
        :param TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SecurityGroupSet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("SecurityGroupSet") is not None:
            self.SecurityGroupSet = []
            for item in params.get("SecurityGroupSet"):
                obj = SecurityGroup()
                obj._deserialize(item)
                self.SecurityGroupSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeServiceTemplateGroupInstancesRequest(AbstractModel):
    """DescribeServiceTemplateGroupInstances请求参数结构体"""

    def __init__(self):
        """
        :param ServiceTemplateGroupId: 协议端口实例ID。例如：ppmg-12345678。
        :type ServiceTemplateGroupId: str
        :param Offset: 偏移量，默认为0。
        :type Offset: int
        :param Limit: 返回数量，默认为20，最大值为100。
        :type Limit: int
        """
        self.ServiceTemplateGroupId = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.ServiceTemplateGroupId = params.get("ServiceTemplateGroupId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeServiceTemplateGroupInstancesResponse(AbstractModel):
    """DescribeServiceTemplateGroupInstances返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeServiceTemplateGroupsRequest(AbstractModel):
    """DescribeServiceTemplateGroups请求参数结构体"""

    def __init__(self):
        """
                :param Filters: 过滤条件。
        <li>service-template-group-name - String - （过滤条件）协议端口模板集合名称。</li>
        <li>service-template-group-id - String - （过滤条件）协议端口模板集合实例ID，例如：ppmg-e6dy460g。</li>
                :type Filters: list of Filter
                :param Offset: 偏移量，默认为0。
                :type Offset: str
                :param Limit: 返回数量，默认为20，最大值为100。
                :type Limit: str
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


class DescribeServiceTemplateGroupsResponse(AbstractModel):
    """DescribeServiceTemplateGroups返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param ServiceTemplateGroupSet: 协议端口模板集合。
        :type ServiceTemplateGroupSet: list of ServiceTemplateGroup
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.ServiceTemplateGroupSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("ServiceTemplateGroupSet") is not None:
            self.ServiceTemplateGroupSet = []
            for item in params.get("ServiceTemplateGroupSet"):
                obj = ServiceTemplateGroup()
                obj._deserialize(item)
                self.ServiceTemplateGroupSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeServiceTemplateInstancesRequest(AbstractModel):
    """DescribeServiceTemplateInstances请求参数结构体"""

    def __init__(self):
        """
        :param ServiceTemplateId: 协议端口实例ID。例如：ppm-12345678。
        :type ServiceTemplateId: str
        :param Offset: 偏移量，默认为0。
        :type Offset: int
        :param Limit: 返回数量，默认为20，最大值为100。
        :type Limit: int
        """
        self.ServiceTemplateId = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.ServiceTemplateId = params.get("ServiceTemplateId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeServiceTemplateInstancesResponse(AbstractModel):
    """DescribeServiceTemplateInstances返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeServiceTemplatesRequest(AbstractModel):
    """DescribeServiceTemplates请求参数结构体"""

    def __init__(self):
        """
                :param Filters: 过滤条件。
        <li>service-template-name - String - （过滤条件）协议端口模板名称。</li>
        <li>service-template-id - String - （过滤条件）协议端口模板实例ID，例如：ppm-e6dy460g。</li>
                :type Filters: list of Filter
                :param Offset: 偏移量，默认为0。
                :type Offset: str
                :param Limit: 返回数量，默认为20，最大值为100。
                :type Limit: str
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


class DescribeServiceTemplatesResponse(AbstractModel):
    """DescribeServiceTemplates返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param ServiceTemplateSet: 协议端口模板对象。
        :type ServiceTemplateSet: list of ServiceTemplate
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.ServiceTemplateSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("ServiceTemplateSet") is not None:
            self.ServiceTemplateSet = []
            for item in params.get("ServiceTemplateSet"):
                obj = ServiceTemplate()
                obj._deserialize(item)
                self.ServiceTemplateSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeSingleIspRegionRequest(AbstractModel):
    """DescribeSingleIspRegion请求参数结构体"""


class DescribeSingleIspRegionResponse(AbstractModel):
    """DescribeSingleIspRegion返回参数结构体"""

    def __init__(self):
        """
        :param SingleIspZone: 三网运营商和可用区的映射关系
        :type SingleIspZone: list of SingleIspZone
        :param TotalCount: 支持三网运营商的可用区数量
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SingleIspZone = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("SingleIspZone") is not None:
            self.SingleIspZone = []
            for item in params.get("SingleIspZone"):
                obj = SingleIspZone()
                obj._deserialize(item)
                self.SingleIspZone.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeSpecificTrafficPackageResourcesUsedStatisticsRequest(AbstractModel):
    """DescribeSpecificTrafficPackageResourcesUsedStatistics请求参数结构体"""

    def __init__(self):
        """
        :param TrafficPackageId: 共享流量包唯一ID
        :type TrafficPackageId: str
        :param StartTime: 开始时间，默认为当前时间往前推24小时
        :type StartTime: str
        :param EndTime: 截止时间，默认为当前时间
        :type EndTime: str
        :param Offset: 分页参数，默认为0
        :type Offset: int
        :param Limit: 分页参数，默认为20
        :type Limit: int
        """
        self.TrafficPackageId = None
        self.StartTime = None
        self.EndTime = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.TrafficPackageId = params.get("TrafficPackageId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeSpecificTrafficPackageResourcesUsedStatisticsResponse(AbstractModel):
    """DescribeSpecificTrafficPackageResourcesUsedStatistics返回参数结构体"""

    def __init__(self):
        """
        :param TotalAmount: 符合查询条件的资源记录总数
        :type TotalAmount: int
        :param ResourcesSet: 资源抵扣信息
        :type ResourcesSet: list of TrafficPackageResourceDeduction
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalAmount = None
        self.ResourcesSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalAmount = params.get("TotalAmount")
        if params.get("ResourcesSet") is not None:
            self.ResourcesSet = []
            for item in params.get("ResourcesSet"):
                obj = TrafficPackageResourceDeduction()
                obj._deserialize(item)
                self.ResourcesSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeSpecificTrafficPackageUsedDetailsRequest(AbstractModel):
    """DescribeSpecificTrafficPackageUsedDetails请求参数结构体"""

    def __init__(self):
        """
        :param TrafficPackageId: 共享流量包唯一ID
        :type TrafficPackageId: str
        :param Filters: 每次请求的`Filters`的上限为10，`Filter.Values`的上限为5。详细的过滤条件如下：<li> resource-id - String - 是否必填：否 - （过滤条件）按照抵扣流量资源的唯一 ID 过滤。</li><li> resource-type - String - 是否必填：否 - （过滤条件）按照资源类型过滤，资源类型包括 CVM 和 EIP </li>
        :type Filters: list of Filter
        :param OrderField: 排序条件。该参数仅支持根据抵扣量排序，传值为 deduction
        :type OrderField: str
        :param OrderType: 排序类型，仅支持0和1，0-降序，1-升序。不传默认为0
        :type OrderType: int
        :param StartTime: 开始时间。不传默认为当前时间往前推30天
        :type StartTime: str
        :param EndTime: 结束时间。不传默认为当前时间
        :type EndTime: str
        :param Offset: 分页参数
        :type Offset: int
        :param Limit: 分页参数
        :type Limit: int
        """
        self.TrafficPackageId = None
        self.Filters = None
        self.OrderField = None
        self.OrderType = None
        self.StartTime = None
        self.EndTime = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.TrafficPackageId = params.get("TrafficPackageId")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.OrderField = params.get("OrderField")
        self.OrderType = params.get("OrderType")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeSpecificTrafficPackageUsedDetailsResponse(AbstractModel):
    """DescribeSpecificTrafficPackageUsedDetails返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合查询条件的共享流量包用量明细的总数
        :type TotalCount: int
        :param UsedDetailSet: 共享流量包用量明细列表
        :type UsedDetailSet: list of UsedDetail
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.UsedDetailSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("UsedDetailSet") is not None:
            self.UsedDetailSet = []
            for item in params.get("UsedDetailSet"):
                obj = UsedDetail()
                obj._deserialize(item)
                self.UsedDetailSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeSubnetIdsRequest(AbstractModel):
    """DescribeSubnetIds请求参数结构体"""

    def __init__(self):
        """
        :param SubnetIds: 子网实例ID查询。形如：subnet-pxir56ns。每次请求的实例的上限为100。
        :type SubnetIds: list of str
        :param Offset: 偏移量
        :type Offset: int
        :param Limit: 返回数量
        :type Limit: int
        """
        self.SubnetIds = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.SubnetIds = params.get("SubnetIds")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeSubnetIdsResponse(AbstractModel):
    """DescribeSubnetIds返回参数结构体"""

    def __init__(self):
        """
        :param SubnetSet: 子网对象。
        :type SubnetSet: list of SubnetNum
        :param TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SubnetSet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("SubnetSet") is not None:
            self.SubnetSet = []
            for item in params.get("SubnetSet"):
                obj = SubnetNum()
                obj._deserialize(item)
                self.SubnetSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeSubnetsRequest(AbstractModel):
    """DescribeSubnets请求参数结构体"""

    def __init__(self):
        """
                :param SubnetIds: 子网实例ID查询。形如：subnet-pxir56ns。每次请求的实例的上限为100。参数不支持同时指定SubnetIds和Filters。
                :type SubnetIds: list of str
                :param Filters: 过滤条件，参数不支持同时指定SubnetIds和Filters。
        <li>subnet-id - String - （过滤条件）Subnet实例名称。</li>
        <li>type - Int - （过滤条件）Subnet类型，默认普通子网。</li>
        <li>vpc-id - String - （过滤条件）VPC实例ID，形如：vpc-f49l6u0z。</li>
        <li>cidr-block - String - （过滤条件）子网网段，形如: 192.168.1.0 。</li>
        <li>is-default - Boolean - （过滤条件）是否是默认子网。</li>
        <li>is-remote-vpc-snat - Boolean - （过滤条件）是否为VPC SNAT地址池子网。</li>
        <li>subnet-name - String - （过滤条件）子网名称。</li>
        <li>zone - String - （过滤条件）可用区。</li>
        <li>tag-key - String -是否必填：否- （过滤条件）按照标签键进行过滤。</li>
        <li>tag:tag-key - String - 是否必填：否 - （过滤条件）按照标签键值对进行过滤。 tag-key使用具体的标签键进行替换。使用请参考示例2。</li>
                :type Filters: list of Filter
                :param Offset: 偏移量，默认为0。
                :type Offset: str
                :param Limit: 返回数量，默认为20，最大值为100。
                :type Limit: str
        """
        self.SubnetIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.SubnetIds = params.get("SubnetIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeSubnetsResponse(AbstractModel):
    """DescribeSubnets返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param SubnetSet: 子网对象。
        :type SubnetSet: list of Subnet
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.SubnetSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("SubnetSet") is not None:
            self.SubnetSet = []
            for item in params.get("SubnetSet"):
                obj = Subnet()
                obj._deserialize(item)
                self.SubnetSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeTaskResultRequest(AbstractModel):
    """DescribeTaskResult请求参数结构体"""

    def __init__(self):
        """
        :param TaskId: 异步任务ID。TaskId和DealName必填一个参数
        :type TaskId: int
        :param DealName: 计费订单号。TaskId和DealName必填一个参数
        :type DealName: str
        """
        self.TaskId = None
        self.DealName = None

    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.DealName = params.get("DealName")


class DescribeTaskResultResponse(AbstractModel):
    """DescribeTaskResult返回参数结构体"""

    def __init__(self):
        """
        :param TaskId: 任务ID
        :type TaskId: int
        :param Result: 执行结果，包括"SUCCESS", "FAILED", "RUNNING"
        :type Result: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.Result = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.Result = params.get("Result")
        self.RequestId = params.get("RequestId")


class DescribeTemplateLimitsRequest(AbstractModel):
    """DescribeTemplateLimits请求参数结构体"""


class DescribeTemplateLimitsResponse(AbstractModel):
    """DescribeTemplateLimits返回参数结构体"""

    def __init__(self):
        """
        :param TemplateLimit: 参数模板配额对象。
        :type TemplateLimit: :class:`tcecloud.vpc.v20170312.models.TemplateLimit`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TemplateLimit = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("TemplateLimit") is not None:
            self.TemplateLimit = TemplateLimit()
            self.TemplateLimit._deserialize(params.get("TemplateLimit"))
        self.RequestId = params.get("RequestId")


class DescribeTrafficMirrorsRequest(AbstractModel):
    """DescribeTrafficMirrors请求参数结构体"""

    def __init__(self):
        """
        :param TrafficMirrorIds: 流量镜像实例ID集合
        :type TrafficMirrorIds: list of str
        :param Filters: 流量镜像查询过滤调节
        :type Filters: :class:`tcecloud.vpc.v20170312.models.Filter`
        :param Offset: 偏移量，默认为0。
        :type Offset: int
        :param Limit: 返回数量，默认为20，最大值为100。
        :type Limit: int
        """
        self.TrafficMirrorIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.TrafficMirrorIds = params.get("TrafficMirrorIds")
        if params.get("Filters") is not None:
            self.Filters = Filter()
            self.Filters._deserialize(params.get("Filters"))
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeTrafficMirrorsResponse(AbstractModel):
    """DescribeTrafficMirrors返回参数结构体"""

    def __init__(self):
        """
        :param TrafficMirrorSet: 流量镜像实例信息
        :type TrafficMirrorSet: list of TrafficMirror
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TrafficMirrorSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("TrafficMirrorSet") is not None:
            self.TrafficMirrorSet = []
            for item in params.get("TrafficMirrorSet"):
                obj = TrafficMirror()
                obj._deserialize(item)
                self.TrafficMirrorSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeTrafficPackageQuotaRequest(AbstractModel):
    """DescribeTrafficPackageQuota请求参数结构体"""


class DescribeTrafficPackageQuotaResponse(AbstractModel):
    """DescribeTrafficPackageQuota返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeTrafficPackageStatisticsRequest(AbstractModel):
    """DescribeTrafficPackageStatistics请求参数结构体"""


class DescribeTrafficPackageStatisticsResponse(AbstractModel):
    """DescribeTrafficPackageStatistics返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeTrafficPackagesRequest(AbstractModel):
    """DescribeTrafficPackages请求参数结构体"""

    def __init__(self):
        """
                :param TrafficPackageIds: 共享流量包ID，支持批量
                :type TrafficPackageIds: list of str
                :param Filters: 每次请求的`Filters`的上限为10。参数不支持同时指定`TrafficPackageIds`和`Filters`。详细的过滤条件如下：
        <li> traffic-package_id - String - 是否必填：否 - （过滤条件）按照共享流量包的唯一标识ID过滤。</li>
        <li> traffic-package-name - String - 是否必填：否 - （过滤条件）按照共享流量包名称过滤。不支持模糊过滤。</li>
        <li> status - String - 是否必填：否 - （过滤条件）按照共享流量包状态过滤。可选状态：[AVAILABLE|EXPIRED|EXHAUSTED]</li>
                :type Filters: list of Filter
                :param Offset: 查询共享流量包偏移量
                :type Offset: int
                :param Limit: 查询共享流量包数量限制
                :type Limit: int
        """
        self.TrafficPackageIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.TrafficPackageIds = params.get("TrafficPackageIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeTrafficPackagesResponse(AbstractModel):
    """DescribeTrafficPackages返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeVpcExtendCidrsRequest(AbstractModel):
    """DescribeVpcExtendCidrs请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: VpcId
        :type VpcId: str
        :param Offset: 偏移量，默认为0。
        :type Offset: int
        :param Limit: 每页行数，默认为10
        :type Limit: int
        """
        self.VpcId = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeVpcExtendCidrsResponse(AbstractModel):
    """DescribeVpcExtendCidrs返回参数结构体"""

    def __init__(self):
        """
        :param VpcExtendCidrs: VPC扩展CIDR段
        :type VpcExtendCidrs: list of VpcExtendCidr
        :param TotalCount: 总数目
        :type TotalCount: int
        :param ModifyState: 修改VPC扩展CIDR的状态值；0已完成，1修改中
        :type ModifyState: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.VpcExtendCidrs = None
        self.TotalCount = None
        self.ModifyState = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("VpcExtendCidrs") is not None:
            self.VpcExtendCidrs = []
            for item in params.get("VpcExtendCidrs"):
                obj = VpcExtendCidr()
                obj._deserialize(item)
                self.VpcExtendCidrs.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.ModifyState = params.get("ModifyState")
        self.RequestId = params.get("RequestId")


class DescribeVpcGatewaysRequest(AbstractModel):
    """DescribeVpcGateways请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: VPC实例ID。
        :type VpcId: str
        :param GatewayType: 网关类型。默认取值CVM。目前仅支持查询CVM网关。
        :type GatewayType: str
        """
        self.VpcId = None
        self.GatewayType = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.GatewayType = params.get("GatewayType")


class DescribeVpcGatewaysResponse(AbstractModel):
    """DescribeVpcGateways返回参数结构体"""

    def __init__(self):
        """
        :param GatewaySet: 实例详细信息列表。
        :type GatewaySet: list of VpcGateway
        :param TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.GatewaySet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("GatewaySet") is not None:
            self.GatewaySet = []
            for item in params.get("GatewaySet"):
                obj = VpcGateway()
                obj._deserialize(item)
                self.GatewaySet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeVpcGlobalExtendCidrsRequest(AbstractModel):
    """DescribeVpcGlobalExtendCidrs请求参数结构体"""

    def __init__(self):
        """
        :param Offset: 偏移量，默认为0。
        :type Offset: int
        :param Limit: 返回数量，默认为20，最大值为100。
        :type Limit: int
        """
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeVpcGlobalExtendCidrsResponse(AbstractModel):
    """DescribeVpcGlobalExtendCidrs返回参数结构体"""

    def __init__(self):
        """
        :param VpcGlobalExtendCidrs: 返回全局公共的CIDR段
        :type VpcGlobalExtendCidrs: list of VpcGlobalExtendCidr
        :param TotalCount: 总条目数
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.VpcGlobalExtendCidrs = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("VpcGlobalExtendCidrs") is not None:
            self.VpcGlobalExtendCidrs = []
            for item in params.get("VpcGlobalExtendCidrs"):
                obj = VpcGlobalExtendCidr()
                obj._deserialize(item)
                self.VpcGlobalExtendCidrs.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeVpcIdsRequest(AbstractModel):
    """DescribeVpcIds请求参数结构体"""

    def __init__(self):
        """
        :param VpcIds: VPC实例ID。形如：vpc-f49l6u0z。每次请求的实例的上限为100。
        :type VpcIds: list of str
        :param Offset: 偏移量
        :type Offset: int
        :param Limit: 返回数量
        :type Limit: int
        """
        self.VpcIds = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.VpcIds = params.get("VpcIds")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeVpcIdsResponse(AbstractModel):
    """DescribeVpcIds返回参数结构体"""

    def __init__(self):
        """
        :param VpcSet: VPC对象。
        :type VpcSet: list of VpcNum
        :param TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.VpcSet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("VpcSet") is not None:
            self.VpcSet = []
            for item in params.get("VpcSet"):
                obj = VpcNum()
                obj._deserialize(item)
                self.VpcSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeVpcInstancesRequest(AbstractModel):
    """DescribeVpcInstances请求参数结构体"""

    def __init__(self):
        """
                :param Filters: 过滤条件，参数不支持同时指定RouteTableIds和Filters。
        <li>vpc-id - String - （过滤条件）VPC实例ID，形如：vpc-f49l6u0z。</li>
        <li>instance-id - String - （过滤条件）云主机实例ID。</li>
        <li>instance-name - String - （过滤条件）云主机名称。</li>
                :type Filters: list of Filter
                :param Offset: 偏移量。
                :type Offset: int
                :param Limit: 请求对象个数。
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


class DescribeVpcInstancesResponse(AbstractModel):
    """DescribeVpcInstances返回参数结构体"""

    def __init__(self):
        """
        :param InstanceSet: 云主机实例列表。
        :type InstanceSet: list of CvmInstance
        :param TotalCount: 满足条件的云主机实例个数。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceSet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("InstanceSet") is not None:
            self.InstanceSet = []
            for item in params.get("InstanceSet"):
                obj = CvmInstance()
                obj._deserialize(item)
                self.InstanceSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeVpcIpv6AddressesRequest(AbstractModel):
    """DescribeVpcIpv6Addresses请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: `VPC`实例`ID`，形如：`vpc-f49l6u0z`。
        :type VpcId: str
        :param Ipv6Addresses: `IP`地址列表，批量查询单次请求最多支持`10`个。
        :type Ipv6Addresses: list of str
        :param Offset: 偏移量。
        :type Offset: int
        :param Limit: 返回数量。
        :type Limit: int
        """
        self.VpcId = None
        self.Ipv6Addresses = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.Ipv6Addresses = params.get("Ipv6Addresses")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeVpcIpv6AddressesResponse(AbstractModel):
    """DescribeVpcIpv6Addresses返回参数结构体"""

    def __init__(self):
        """
        :param Ipv6AddressSet: `IPv6`地址列表。
        :type Ipv6AddressSet: list of VpcIpv6Address
        :param TotalCount: `IPv6`地址总数。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Ipv6AddressSet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Ipv6AddressSet") is not None:
            self.Ipv6AddressSet = []
            for item in params.get("Ipv6AddressSet"):
                obj = VpcIpv6Address()
                obj._deserialize(item)
                self.Ipv6AddressSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeVpcLimitsRequest(AbstractModel):
    """DescribeVpcLimits请求参数结构体"""

    def __init__(self):
        """
        :param LimitTypes: 配额名称。每次最大查询100个配额类型。
        :type LimitTypes: list of str
        """
        self.LimitTypes = None

    def _deserialize(self, params):
        self.LimitTypes = params.get("LimitTypes")


class DescribeVpcLimitsResponse(AbstractModel):
    """DescribeVpcLimits返回参数结构体"""

    def __init__(self):
        """
        :param VpcLimitSet: 私有网络配额
        :type VpcLimitSet: list of VpcLimit
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.VpcLimitSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("VpcLimitSet") is not None:
            self.VpcLimitSet = []
            for item in params.get("VpcLimitSet"):
                obj = VpcLimit()
                obj._deserialize(item)
                self.VpcLimitSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeVpcPrivateIpAddressesRequest(AbstractModel):
    """DescribeVpcPrivateIpAddresses请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: `VPC`实例`ID`，形如：`vpc-f49l6u0z`。
        :type VpcId: str
        :param PrivateIpAddresses: 内网`IP`地址列表，批量查询单次请求最多支持`10`个。
        :type PrivateIpAddresses: list of str
        """
        self.VpcId = None
        self.PrivateIpAddresses = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.PrivateIpAddresses = params.get("PrivateIpAddresses")


class DescribeVpcPrivateIpAddressesResponse(AbstractModel):
    """DescribeVpcPrivateIpAddresses返回参数结构体"""

    def __init__(self):
        """
        :param VpcPrivateIpAddressSet: 内网`IP`地址信息列表。
        :type VpcPrivateIpAddressSet: list of VpcPrivateIpAddress
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.VpcPrivateIpAddressSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("VpcPrivateIpAddressSet") is not None:
            self.VpcPrivateIpAddressSet = []
            for item in params.get("VpcPrivateIpAddressSet"):
                obj = VpcPrivateIpAddress()
                obj._deserialize(item)
                self.VpcPrivateIpAddressSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeVpcResourceDashboardRequest(AbstractModel):
    """DescribeVpcResourceDashboard请求参数结构体"""

    def __init__(self):
        """
        :param VpcIds: Vpc实例ID，例如：vpc-f1xjkw1b。
        :type VpcIds: list of str
        """
        self.VpcIds = None

    def _deserialize(self, params):
        self.VpcIds = params.get("VpcIds")


class DescribeVpcResourceDashboardResponse(AbstractModel):
    """DescribeVpcResourceDashboard返回参数结构体"""

    def __init__(self):
        """
        :param ResourceDashboardSet: 资源对象列表。
        :type ResourceDashboardSet: list of ResourceDashboard
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ResourceDashboardSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("ResourceDashboardSet") is not None:
            self.ResourceDashboardSet = []
            for item in params.get("ResourceDashboardSet"):
                obj = ResourceDashboard()
                obj._deserialize(item)
                self.ResourceDashboardSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeVpcTaskResultRequest(AbstractModel):
    """DescribeVpcTaskResult请求参数结构体"""

    def __init__(self):
        """
        :param TaskId: 异步任务请求返回的RequestId。
        :type TaskId: str
        """
        self.TaskId = None

    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")


class DescribeVpcTaskResultResponse(AbstractModel):
    """DescribeVpcTaskResult返回参数结构体"""

    def __init__(self):
        """
        :param Status: 异步任务执行结果。结果：SUCCESS,FAILED,RUNNING。3者其中之一。其中SUCCESS表示任务执行成功，FAILED表示任务执行失败，RUNNING表示任务执行中。
        :type Status: str
        :param Output: 异步任务执行输出。
        :type Output: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Status = None
        self.Output = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.Output = params.get("Output")
        self.RequestId = params.get("RequestId")


class DescribeVpcsRequest(AbstractModel):
    """DescribeVpcs请求参数结构体"""

    def __init__(self):
        """
                :param VpcIds: VPC实例ID。形如：vpc-f49l6u0z。每次请求的实例的上限为100。参数不支持同时指定VpcIds和Filters。
                :type VpcIds: list of str
                :param Filters: 过滤条件，参数不支持同时指定VpcIds和Filters。
        <li>vpc-name - String - （过滤条件）VPC实例名称。</li>
        <li>is-default - String - （过滤条件）是否默认VPC。</li>
        <li>vpc-id - String - （过滤条件）VPC实例ID形如：vpc-f49l6u0z。</li>
        <li>cidr-block - String - （过滤条件）vpc的cidr。</li>
        <li>tag-key - String -是否必填：否- （过滤条件）按照标签键进行过滤。</li>
        <li>tag:tag-key - String - 是否必填：否 - （过滤条件）按照标签键值对进行过滤。 tag-key使用具体的标签键进行替换。使用请参考示例2。</li>
                :type Filters: list of Filter
                :param Offset: 偏移量，默认为0。
                :type Offset: str
                :param Limit: 返回数量，默认为20，最大值为100。
                :type Limit: str
        """
        self.VpcIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.VpcIds = params.get("VpcIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeVpcsResponse(AbstractModel):
    """DescribeVpcs返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的对象数。
        :type TotalCount: int
        :param VpcSet: VPC对象。
        :type VpcSet: list of Vpc
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.VpcSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("VpcSet") is not None:
            self.VpcSet = []
            for item in params.get("VpcSet"):
                obj = Vpc()
                obj._deserialize(item)
                self.VpcSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeVpnConnectionsRequest(AbstractModel):
    """DescribeVpnConnections请求参数结构体"""

    def __init__(self):
        """
                :param VpnConnectionIds: VPN通道实例ID。形如：vpnx-f49l6u0z。每次请求的实例的上限为100。参数不支持同时指定VpnConnectionIds和Filters。
                :type VpnConnectionIds: list of str
                :param Filters: 过滤条件。每次请求的Filters的上限为10，Filter.Values的上限为5。参数不支持同时指定VpnConnectionIds和Filters。
        <li>vpc-id - String - VPC实例ID，形如：`vpc-0a36uwkr`。</li>
        <li>vpn-gateway-id - String - VPN网关实例ID，形如：`vpngw-p4lmqawn`。</li>
        <li>customer-gateway-id - String - 对端网关实例ID，形如：`cgw-l4rblw63`。</li>
        <li>vpn-connection-name - String - 通道名称，形如：`test-vpn`。</li>
        <li>vpn-connection-id - String - 通道实例ID，形如：`vpnx-5p7vkch8"`。</li>
                :type Filters: list of Filter
                :param Offset: 偏移量，默认为0。关于Offset的更进一步介绍请参考 API 简介中的相关小节。
                :type Offset: int
                :param Limit: 返回数量，默认为20，最大值为100。
                :type Limit: int
        """
        self.VpnConnectionIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.VpnConnectionIds = params.get("VpnConnectionIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeVpnConnectionsResponse(AbstractModel):
    """DescribeVpnConnections返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param VpnConnectionSet: VPN通道实例。
        :type VpnConnectionSet: list of VpnConnection
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.VpnConnectionSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("VpnConnectionSet") is not None:
            self.VpnConnectionSet = []
            for item in params.get("VpnConnectionSet"):
                obj = VpnConnection()
                obj._deserialize(item)
                self.VpnConnectionSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeVpnGatewayCcnRoutesRequest(AbstractModel):
    """DescribeVpnGatewayCcnRoutes请求参数结构体"""

    def __init__(self):
        """
        :param VpnGatewayId: VPN网关实例ID
        :type VpnGatewayId: str
        :param Offset: 偏移量
        :type Offset: int
        :param Limit: 返回数量
        :type Limit: int
        """
        self.VpnGatewayId = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.VpnGatewayId = params.get("VpnGatewayId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeVpnGatewayCcnRoutesResponse(AbstractModel):
    """DescribeVpnGatewayCcnRoutes返回参数结构体"""

    def __init__(self):
        """
        :param RouteSet: 云联网路由（IDC网段）列表。
        :type RouteSet: list of VpngwCcnRoutes
        :param TotalCount: 符合条件的对象数。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RouteSet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("RouteSet") is not None:
            self.RouteSet = []
            for item in params.get("RouteSet"):
                obj = VpngwCcnRoutes()
                obj._deserialize(item)
                self.RouteSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeVpnGatewayQuotaRequest(AbstractModel):
    """DescribeVpnGatewayQuota请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: VPC实例ID。形如：vpc-f49l6u0z。
        :type VpcId: str
        :param VpnGatewayId: VPN网关实例ID。形如：vpngw-f49l6u0z。
        :type VpnGatewayId: str
        """
        self.VpcId = None
        self.VpnGatewayId = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.VpnGatewayId = params.get("VpnGatewayId")


class DescribeVpnGatewayQuotaResponse(AbstractModel):
    """DescribeVpnGatewayQuota返回参数结构体"""

    def __init__(self):
        """
        :param VpnGatewayQuotaSet: VPN网关配额对象。
        :type VpnGatewayQuotaSet: list of VpnGatewayQuota
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.VpnGatewayQuotaSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("VpnGatewayQuotaSet") is not None:
            self.VpnGatewayQuotaSet = []
            for item in params.get("VpnGatewayQuotaSet"):
                obj = VpnGatewayQuota()
                obj._deserialize(item)
                self.VpnGatewayQuotaSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeVpnGatewaysRequest(AbstractModel):
    """DescribeVpnGateways请求参数结构体"""

    def __init__(self):
        """
                :param VpnGatewayIds: VPN网关实例ID。形如：vpngw-f49l6u0z。每次请求的实例的上限为100。参数不支持同时指定VpnGatewayIds和Filters。
                :type VpnGatewayIds: list of str
                :param Filters: 过滤条件，参数不支持同时指定VpnGatewayIds和Filters。
        <li>vpc-id - String - （过滤条件）VPC实例ID形如：vpc-f49l6u0z。</li>
        <li>vpn-gateway-id - String - （过滤条件）VPN实例ID形如：vpngw-5aluhh9t。</li>
        <li>vpn-gateway-name - String - （过滤条件）VPN实例名称。</li>
        <li>type - String - （过滤条件）VPN网关类型：'IPSEC', 'SSL'。</li>
        <li>public-ip-address- String - （过滤条件）公网IP。</li>
        <li>renew-flag - String - （过滤条件）网关续费类型，手动续费：'NOTIFY_AND_MANUAL_RENEW'、自动续费：'NOTIFY_AND_AUTO_RENEW'。</li>
        <li>zone - String - （过滤条件）VPN所在可用区，形如：ap-guangzhou-2。</li>
                :type Filters: list of FilterObject
                :param Offset: 偏移量
                :type Offset: int
                :param Limit: 请求对象个数
                :type Limit: int
        """
        self.VpnGatewayIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.VpnGatewayIds = params.get("VpnGatewayIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = FilterObject()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeVpnGatewaysResponse(AbstractModel):
    """DescribeVpnGateways返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param VpnGatewaySet: VPN网关实例详细信息列表。
        :type VpnGatewaySet: list of VpnGateway
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.VpnGatewaySet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("VpnGatewaySet") is not None:
            self.VpnGatewaySet = []
            for item in params.get("VpnGatewaySet"):
                obj = VpnGateway()
                obj._deserialize(item)
                self.VpnGatewaySet.append(obj)
        self.RequestId = params.get("RequestId")


class DestinationIpPortTranslationNatRule(AbstractModel):
    """NAT网关的端口转发规则"""

    def __init__(self):
        """
        :param IpProtocol: 网络协议，可选值：`TCP`、`UDP`。
        :type IpProtocol: str
        :param PublicIpAddress: 弹性IP。
        :type PublicIpAddress: str
        :param PublicPort: 公网端口。
        :type PublicPort: int
        :param PrivateIpAddress: 内网地址。
        :type PrivateIpAddress: str
        :param PrivatePort: 内网端口。
        :type PrivatePort: int
        :param Description: NAT网关转发规则描述。
        :type Description: str
        """
        self.IpProtocol = None
        self.PublicIpAddress = None
        self.PublicPort = None
        self.PrivateIpAddress = None
        self.PrivatePort = None
        self.Description = None

    def _deserialize(self, params):
        self.IpProtocol = params.get("IpProtocol")
        self.PublicIpAddress = params.get("PublicIpAddress")
        self.PublicPort = params.get("PublicPort")
        self.PrivateIpAddress = params.get("PrivateIpAddress")
        self.PrivatePort = params.get("PrivatePort")
        self.Description = params.get("Description")


class DetachCcnInstancesRequest(AbstractModel):
    """DetachCcnInstances请求参数结构体"""

    def __init__(self):
        """
        :param CcnId: CCN实例ID。形如：ccn-f49l6u0z。
        :type CcnId: str
        :param Instances: 要解关联网络实例列表
        :type Instances: list of CcnInstance
        """
        self.CcnId = None
        self.Instances = None

    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")
        if params.get("Instances") is not None:
            self.Instances = []
            for item in params.get("Instances"):
                obj = CcnInstance()
                obj._deserialize(item)
                self.Instances.append(obj)


class DetachCcnInstancesResponse(AbstractModel):
    """DetachCcnInstances返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DetachClassicLinkVpcRequest(AbstractModel):
    """DetachClassicLinkVpc请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: VPC实例ID。可通过DescribeVpcs接口返回值中的VpcId获取。
        :type VpcId: str
        :param InstanceIds: CVM实例ID查询。形如：ins-r8hr2upy。
        :type InstanceIds: list of str
        """
        self.VpcId = None
        self.InstanceIds = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.InstanceIds = params.get("InstanceIds")


class DetachClassicLinkVpcResponse(AbstractModel):
    """DetachClassicLinkVpc返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DetachNetworkInterfaceRequest(AbstractModel):
    """DetachNetworkInterface请求参数结构体"""

    def __init__(self):
        """
        :param NetworkInterfaceId: 弹性网卡实例ID，例如：eni-m6dyj72l。
        :type NetworkInterfaceId: str
        :param InstanceId: CVM实例ID。形如：ins-r8hr2upy。
        :type InstanceId: str
        """
        self.NetworkInterfaceId = None
        self.InstanceId = None

    def _deserialize(self, params):
        self.NetworkInterfaceId = params.get("NetworkInterfaceId")
        self.InstanceId = params.get("InstanceId")


class DetachNetworkInterfaceResponse(AbstractModel):
    """DetachNetworkInterface返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DirectConnectGateway(AbstractModel):
    """专线网关对象。"""

    def __init__(self):
        """
                :param DirectConnectGatewayId: 专线网关`ID`。
                :type DirectConnectGatewayId: str
                :param DirectConnectGatewayName: 专线网关名称。
                :type DirectConnectGatewayName: str
                :param VpcId: 专线网关关联`VPC`实例`ID`。
                :type VpcId: str
                :param NetworkType: 关联网络类型：
        <li>`VPC` - 私有网络</li>
        <li>`CCN` - 云联网</li>
                :type NetworkType: str
                :param NetworkInstanceId: 关联网络实例`ID`：
        <li>`NetworkType`为`VPC`时，这里为私有网络实例`ID`</li>
        <li>`NetworkType`为`CCN`时，这里为云联网实例`ID`</li>
                :type NetworkInstanceId: str
                :param GatewayType: 网关类型：
        <li>NORMAL - 标准型，注：云联网只支持标准型</li>
        <li>NAT - NAT型</li>
        NAT类型支持网络地址转换配置，类型确定后不能修改；一个私有网络可以创建一个NAT类型的专线网关和一个非NAT类型的专线网关
                :type GatewayType: str
                :param CreateTime: 创建时间。
                :type CreateTime: str
                :param DirectConnectGatewayIp: 专线网关IP。
                :type DirectConnectGatewayIp: str
                :param CcnId: 专线网关关联`CCN`实例`ID`。
                :type CcnId: str
                :param CcnRouteType: 云联网路由学习类型：
        <li>`BGP` - 自动学习。</li>
        <li>`STATIC` - 静态，即用户配置。</li>
                :type CcnRouteType: str
                :param EnableBGP: 是否启用BGP。
                :type EnableBGP: bool
                :param EnableBGPCommunity: 开启和关闭BGP的community属性。
                :type EnableBGPCommunity: bool
        """
        self.DirectConnectGatewayId = None
        self.DirectConnectGatewayName = None
        self.VpcId = None
        self.NetworkType = None
        self.NetworkInstanceId = None
        self.GatewayType = None
        self.CreateTime = None
        self.DirectConnectGatewayIp = None
        self.CcnId = None
        self.CcnRouteType = None
        self.EnableBGP = None
        self.EnableBGPCommunity = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.DirectConnectGatewayName = params.get("DirectConnectGatewayName")
        self.VpcId = params.get("VpcId")
        self.NetworkType = params.get("NetworkType")
        self.NetworkInstanceId = params.get("NetworkInstanceId")
        self.GatewayType = params.get("GatewayType")
        self.CreateTime = params.get("CreateTime")
        self.DirectConnectGatewayIp = params.get("DirectConnectGatewayIp")
        self.CcnId = params.get("CcnId")
        self.CcnRouteType = params.get("CcnRouteType")
        self.EnableBGP = params.get("EnableBGP")
        self.EnableBGPCommunity = params.get("EnableBGPCommunity")


class DirectConnectGatewayCcnRoute(AbstractModel):
    """专线网关云联网路由（IDC网段）对象"""

    def __init__(self):
        """
        :param RouteId: 路由ID。
        :type RouteId: str
        :param DestinationCidrBlock: IDC网段。
        :type DestinationCidrBlock: str
        :param ASPath: `BGP`的`AS-Path`属性。
        :type ASPath: list of str
        """
        self.RouteId = None
        self.DestinationCidrBlock = None
        self.ASPath = None

    def _deserialize(self, params):
        self.RouteId = params.get("RouteId")
        self.DestinationCidrBlock = params.get("DestinationCidrBlock")
        self.ASPath = params.get("ASPath")


class DisableCcnRoutesRequest(AbstractModel):
    """DisableCcnRoutes请求参数结构体"""

    def __init__(self):
        """
        :param CcnId: CCN实例ID。形如：ccn-f49l6u0z。
        :type CcnId: str
        :param RouteIds: CCN路由策略唯一ID。形如：ccnr-f49l6u0z。
        :type RouteIds: list of str
        """
        self.CcnId = None
        self.RouteIds = None

    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")
        self.RouteIds = params.get("RouteIds")


class DisableCcnRoutesResponse(AbstractModel):
    """DisableCcnRoutes返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DisableGatewayFlowMonitorRequest(AbstractModel):
    """DisableGatewayFlowMonitor请求参数结构体"""

    def __init__(self):
        """
                :param GatewayId: 网关实例ID，目前我们支持的网关实例类型有，
        专线网关实例ID，形如，`dcg-ltjahce6`；
        Nat网关实例ID，形如，`nat-ltjahce6`；
        VPN网关实例ID，形如，`vpn-ltjahce6`。
                :type GatewayId: str
        """
        self.GatewayId = None

    def _deserialize(self, params):
        self.GatewayId = params.get("GatewayId")


class DisableGatewayFlowMonitorResponse(AbstractModel):
    """DisableGatewayFlowMonitor返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DisableRoutesRequest(AbstractModel):
    """DisableRoutes请求参数结构体"""

    def __init__(self):
        """
        :param RouteTableId: 路由表唯一ID。
        :type RouteTableId: str
        :param RouteIds: 路由策略唯一ID。
        :type RouteIds: list of int non-negative
        """
        self.RouteTableId = None
        self.RouteIds = None

    def _deserialize(self, params):
        self.RouteTableId = params.get("RouteTableId")
        self.RouteIds = params.get("RouteIds")


class DisableRoutesResponse(AbstractModel):
    """DisableRoutes返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DisassociateAddressRequest(AbstractModel):
    """DisassociateAddress请求参数结构体"""

    def __init__(self):
        """
        :param AddressId: 标识 EIP 的唯一 ID。EIP 唯一 ID 形如：`eip-11112222`。
        :type AddressId: str
        :param KeepAddressIdBindWithEniPip: 表示解绑时是EIP从ENI上解绑，还是ENI+EIP从实例上解绑
        :type KeepAddressIdBindWithEniPip: bool
        :param ReallocateNormalPublicIp: 表示解绑 EIP 之后是否分配普通公网 IP。取值范围：<br><li>TRUE：表示解绑 EIP 之后分配普通公网 IP。<br><li>FALSE：表示解绑 EIP 之后不分配普通公网 IP。<br>默认取值：FALSE。<br><br>只有满足以下条件时才能指定该参数：<br><li> 只有在解绑主网卡的主内网 IP 上的 EIP 时才能指定该参数。<br><li>解绑 EIP 后重新分配普通公网 IP 操作一个账号每天最多操作 10 次；详情可通过 DescribeAddressQuota 接口获取。
        :type ReallocateNormalPublicIp: bool
        :param CascadeRelease: [Deprecated] 表示解绑后是否自动释放EIP
        :type CascadeRelease: bool
        """
        self.AddressId = None
        self.KeepAddressIdBindWithEniPip = None
        self.ReallocateNormalPublicIp = None
        self.CascadeRelease = None

    def _deserialize(self, params):
        self.AddressId = params.get("AddressId")
        self.KeepAddressIdBindWithEniPip = params.get("KeepAddressIdBindWithEniPip")
        self.ReallocateNormalPublicIp = params.get("ReallocateNormalPublicIp")
        self.CascadeRelease = params.get("CascadeRelease")


class DisassociateAddressResponse(AbstractModel):
    """DisassociateAddress返回参数结构体"""

    def __init__(self):
        """
        :param TaskId: 异步任务TaskId。可以使用DescribeTaskResult接口查询任务状态。
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class DisassociateNatGatewayAddressRequest(AbstractModel):
    """DisassociateNatGatewayAddress请求参数结构体"""

    def __init__(self):
        """
        :param NatGatewayId: NAT网关的ID，形如：`nat-df45454`。
        :type NatGatewayId: str
        :param PublicIpAddresses: 绑定NAT网关的弹性IP数组。
        :type PublicIpAddresses: list of str
        """
        self.NatGatewayId = None
        self.PublicIpAddresses = None

    def _deserialize(self, params):
        self.NatGatewayId = params.get("NatGatewayId")
        self.PublicIpAddresses = params.get("PublicIpAddresses")


class DisassociateNatGatewayAddressResponse(AbstractModel):
    """DisassociateNatGatewayAddress返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DisassociateNetworkAclSubnetsRequest(AbstractModel):
    """DisassociateNetworkAclSubnets请求参数结构体"""

    def __init__(self):
        """
        :param NetworkAclId: 网络ACL实例ID。例如：acl-12345678。
        :type NetworkAclId: str
        :param SubnetIds: 子网实例ID数组。例如：[subnet-12345678]
        :type SubnetIds: list of str
        """
        self.NetworkAclId = None
        self.SubnetIds = None

    def _deserialize(self, params):
        self.NetworkAclId = params.get("NetworkAclId")
        self.SubnetIds = params.get("SubnetIds")


class DisassociateNetworkAclSubnetsResponse(AbstractModel):
    """DisassociateNetworkAclSubnets返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DisassociateNetworkInterfaceSecurityGroupsRequest(AbstractModel):
    """DisassociateNetworkInterfaceSecurityGroups请求参数结构体"""

    def __init__(self):
        """
        :param NetworkInterfaceIds: 弹性网卡实例ID。形如：eni-pxir56ns。每次请求的实例的上限为100。
        :type NetworkInterfaceIds: list of str
        :param SecurityGroupIds: 安全组实例ID，例如：sg-33ocnj9n，可通过DescribeSecurityGroups获取。每次请求的实例的上限为100。
        :type SecurityGroupIds: list of str
        """
        self.NetworkInterfaceIds = None
        self.SecurityGroupIds = None

    def _deserialize(self, params):
        self.NetworkInterfaceIds = params.get("NetworkInterfaceIds")
        self.SecurityGroupIds = params.get("SecurityGroupIds")


class DisassociateNetworkInterfaceSecurityGroupsResponse(AbstractModel):
    """DisassociateNetworkInterfaceSecurityGroups返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DownloadCustomerGatewayConfigurationRequest(AbstractModel):
    """DownloadCustomerGatewayConfiguration请求参数结构体"""

    def __init__(self):
        """
        :param VpnGatewayId: VPN网关实例ID。
        :type VpnGatewayId: str
        :param VpnConnectionId: VPN通道实例ID。形如：vpnx-f49l6u0z。
        :type VpnConnectionId: str
        :param CustomerGatewayVendor: 对端网关厂商信息对象，可通过DescribeCustomerGatewayVendors获取。
        :type CustomerGatewayVendor: :class:`tcecloud.vpc.v20170312.models.CustomerGatewayVendor`
        :param InterfaceName: 通道接入设备物理接口名称。
        :type InterfaceName: str
        """
        self.VpnGatewayId = None
        self.VpnConnectionId = None
        self.CustomerGatewayVendor = None
        self.InterfaceName = None

    def _deserialize(self, params):
        self.VpnGatewayId = params.get("VpnGatewayId")
        self.VpnConnectionId = params.get("VpnConnectionId")
        if params.get("CustomerGatewayVendor") is not None:
            self.CustomerGatewayVendor = CustomerGatewayVendor()
            self.CustomerGatewayVendor._deserialize(params.get("CustomerGatewayVendor"))
        self.InterfaceName = params.get("InterfaceName")


class DownloadCustomerGatewayConfigurationResponse(AbstractModel):
    """DownloadCustomerGatewayConfiguration返回参数结构体"""

    def __init__(self):
        """
        :param CustomerGatewayConfiguration: XML格式配置信息。
        :type CustomerGatewayConfiguration: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.CustomerGatewayConfiguration = None
        self.RequestId = None

    def _deserialize(self, params):
        self.CustomerGatewayConfiguration = params.get("CustomerGatewayConfiguration")
        self.RequestId = params.get("RequestId")


class DownloadSpecificTrafficPackageUsedDetailsRequest(AbstractModel):
    """DownloadSpecificTrafficPackageUsedDetails请求参数结构体"""

    def __init__(self):
        """
        :param TrafficPackageId: 共享流量包唯一ID
        :type TrafficPackageId: str
        :param Filters: 每次请求的`Filters`的上限为10，`Filter.Values`的上限为5。详细的过滤条件如下：<li> resource-id - String - 是否必填：否 - （过滤条件）按照抵扣流量资源的唯一 ID 过滤。</li><li> resource-type - String - 是否必填：否 - （过滤条件）按照资源类型过滤，资源类型包括 CVM 和 EIP </li>
        :type Filters: list of Filter
        :param StartTime: 开始时间,默认为当前时间往前推30天
        :type StartTime: str
        :param EndTime: 结束时间，默认为当前时间
        :type EndTime: str
        :param HistoryId: 生成历史ID.该参数用于某次生成重新生生成使用
        :type HistoryId: int
        """
        self.TrafficPackageId = None
        self.Filters = None
        self.StartTime = None
        self.EndTime = None
        self.HistoryId = None

    def _deserialize(self, params):
        self.TrafficPackageId = params.get("TrafficPackageId")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.HistoryId = params.get("HistoryId")


class DownloadSpecificTrafficPackageUsedDetailsResponse(AbstractModel):
    """DownloadSpecificTrafficPackageUsedDetails返回参数结构体"""

    def __init__(self):
        """
        :param TaskId: 任务ID
        :type TaskId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class EIPIspInfo(AbstractModel):
    """EIP运营商信息"""

    def __init__(self):
        """
                :param Type: 运营商类型
        CTCC
        CUCC
        CMCC
        BGP
                :type Type: str
                :param Name: 运营商名称
                :type Name: str
        """
        self.Type = None
        self.Name = None

    def _deserialize(self, params):
        self.Type = params.get("Type")
        self.Name = params.get("Name")


class EipStatistics(AbstractModel):
    """描述EIP统计信息的结构"""

    def __init__(self):
        """
        :param Region: 地域英文标识
        :type Region: str
        :param RegionName: 地域中文名称
        :type RegionName: str
        :param TotalCount: 地域EIP总数
        :type TotalCount: int
        """
        self.Region = None
        self.RegionName = None
        self.TotalCount = None

    def _deserialize(self, params):
        self.Region = params.get("Region")
        self.RegionName = params.get("RegionName")
        self.TotalCount = params.get("TotalCount")


class EnableCcnRoutesRequest(AbstractModel):
    """EnableCcnRoutes请求参数结构体"""

    def __init__(self):
        """
        :param CcnId: CCN实例ID。形如：ccn-f49l6u0z。
        :type CcnId: str
        :param RouteIds: CCN路由策略唯一ID。形如：ccnr-f49l6u0z。
        :type RouteIds: list of str
        """
        self.CcnId = None
        self.RouteIds = None

    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")
        self.RouteIds = params.get("RouteIds")


class EnableCcnRoutesResponse(AbstractModel):
    """EnableCcnRoutes返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class EnableGatewayFlowMonitorRequest(AbstractModel):
    """EnableGatewayFlowMonitor请求参数结构体"""

    def __init__(self):
        """
                :param GatewayId: 网关实例ID，目前我们支持的网关实例有，
        专线网关实例ID，形如，`dcg-ltjahce6`；
        Nat网关实例ID，形如，`nat-ltjahce6`；
        VPN网关实例ID，形如，`vpn-ltjahce6`。
                :type GatewayId: str
        """
        self.GatewayId = None

    def _deserialize(self, params):
        self.GatewayId = params.get("GatewayId")


class EnableGatewayFlowMonitorResponse(AbstractModel):
    """EnableGatewayFlowMonitor返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class EnableRoutesRequest(AbstractModel):
    """EnableRoutes请求参数结构体"""

    def __init__(self):
        """
        :param RouteTableId: 路由表唯一ID。
        :type RouteTableId: str
        :param RouteIds: 路由策略唯一ID。
        :type RouteIds: list of int non-negative
        """
        self.RouteTableId = None
        self.RouteIds = None

    def _deserialize(self, params):
        self.RouteTableId = params.get("RouteTableId")
        self.RouteIds = params.get("RouteIds")


class EnableRoutesResponse(AbstractModel):
    """EnableRoutes返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class Filter(AbstractModel):
    """过滤器"""

    def __init__(self):
        """
        :param Name: 属性名称, 若存在多个Filter时，Filter间的关系为逻辑与（AND）关系。
        :type Name: str
        :param Values: 属性值, 若同一个Filter存在多个Values，同一Filter下Values间的关系为逻辑或（OR）关系。
        :type Values: list of str
        """
        self.Name = None
        self.Values = None

    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Values = params.get("Values")


class FilterObject(AbstractModel):
    """过滤器键值对"""

    def __init__(self):
        """
        :param Name: 属性名称, 若存在多个Filter时，Filter间的关系为逻辑与（AND）关系。
        :type Name: str
        :param Values: 属性值, 若同一个Filter存在多个Values，同一Filter下Values间的关系为逻辑或（OR）关系。
        :type Values: list of str
        """
        self.Name = None
        self.Values = None

    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Values = params.get("Values")


class FlowLog(AbstractModel):
    """流日志"""

    def __init__(self):
        """
        :param VpcId: 私用网络ID或者统一ID，建议使用统一ID
        :type VpcId: str
        :param FlowLogId: 流日志唯一ID
        :type FlowLogId: str
        :param FlowLogName: 流日志实例名字
        :type FlowLogName: str
        :param ResourceType: 流日志所属资源类型，VPC|SUBNET|NETWORKINTERFACE
        :type ResourceType: str
        :param ResourceId: 资源唯一ID
        :type ResourceId: str
        :param TrafficType: 流日志采集类型，ACCEPT|REJECT|ALL
        :type TrafficType: str
        :param CloudLogId: 流日志存储ID
        :type CloudLogId: str
        :param CloudLogState: 流日志存储ID状态
        :type CloudLogState: str
        :param FlowLogDescription: 流日志描述信息
        :type FlowLogDescription: str
        :param CreatedTime: 流日志创建时间
        :type CreatedTime: str
        """
        self.VpcId = None
        self.FlowLogId = None
        self.FlowLogName = None
        self.ResourceType = None
        self.ResourceId = None
        self.TrafficType = None
        self.CloudLogId = None
        self.CloudLogState = None
        self.FlowLogDescription = None
        self.CreatedTime = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.FlowLogId = params.get("FlowLogId")
        self.FlowLogName = params.get("FlowLogName")
        self.ResourceType = params.get("ResourceType")
        self.ResourceId = params.get("ResourceId")
        self.TrafficType = params.get("TrafficType")
        self.CloudLogId = params.get("CloudLogId")
        self.CloudLogState = params.get("CloudLogState")
        self.FlowLogDescription = params.get("FlowLogDescription")
        self.CreatedTime = params.get("CreatedTime")


class FlushHaVipRequest(AbstractModel):
    """FlushHaVip请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: VPC实例ID。
        :type VpcId: str
        :param Vip: HAVIP的Vip地址。
        :type Vip: str
        :param MacAddress: HAVIP关联网卡的MAC地址。
        :type MacAddress: str
        :param IfnName: HAVIP关联网卡的网卡接口名称。
        :type IfnName: str
        """
        self.VpcId = None
        self.Vip = None
        self.MacAddress = None
        self.IfnName = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.Vip = params.get("Vip")
        self.MacAddress = params.get("MacAddress")
        self.IfnName = params.get("IfnName")


class FlushHaVipResponse(AbstractModel):
    """FlushHaVip返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class GatewayFlowMonitorDetail(AbstractModel):
    """网关流量监控明细"""

    def __init__(self):
        """
        :param PrivateIpAddress: 来源`IP`。
        :type PrivateIpAddress: str
        :param InPkg: 入包量。
        :type InPkg: int
        :param OutPkg: 出包量。
        :type OutPkg: int
        :param InTraffic: 入带宽，单位：`Byte`。
        :type InTraffic: int
        :param OutTraffic: 出带宽，单位：`Byte`。
        :type OutTraffic: int
        """
        self.PrivateIpAddress = None
        self.InPkg = None
        self.OutPkg = None
        self.InTraffic = None
        self.OutTraffic = None

    def _deserialize(self, params):
        self.PrivateIpAddress = params.get("PrivateIpAddress")
        self.InPkg = params.get("InPkg")
        self.OutPkg = params.get("OutPkg")
        self.InTraffic = params.get("InTraffic")
        self.OutTraffic = params.get("OutTraffic")


class GatewayQos(AbstractModel):
    """网关流控带宽信息"""

    def __init__(self):
        """
        :param VpcId: VPC实例ID。
        :type VpcId: str
        :param IpAddress: 云服务器内网IP。
        :type IpAddress: str
        :param Bandwidth: 流控带宽值。
        :type Bandwidth: int
        :param CreateTime: 创建时间。
        :type CreateTime: str
        """
        self.VpcId = None
        self.IpAddress = None
        self.Bandwidth = None
        self.CreateTime = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.IpAddress = params.get("IpAddress")
        self.Bandwidth = params.get("Bandwidth")
        self.CreateTime = params.get("CreateTime")


class GetCcnRegionBandwidthLimitsRequest(AbstractModel):
    """GetCcnRegionBandwidthLimits请求参数结构体"""

    def __init__(self):
        """
                :param CcnId: CCN实例ID。形如：ccn-f49l6u0z。
                :type CcnId: str
                :param Filters: 过滤条件。
        <li>sregion - String - （过滤条件）源地域，形如：ap-guangzhou。</li>
        <li>dregion - String - （过滤条件）目的地域，形如：ap-shanghai-bm</li>
                :type Filters: list of Filter
                :param SortedBy: 排序条件，目前支持带宽（BandwidthLimit）和过期时间（ExpireTime）
                :type SortedBy: str
                :param Offset: 偏移量
                :type Offset: int
                :param Limit: 返回数量
                :type Limit: int
                :param OrderBy: 排序方式，'ASC':升序,'DESC':降序。
                :type OrderBy: str
        """
        self.CcnId = None
        self.Filters = None
        self.SortedBy = None
        self.Offset = None
        self.Limit = None
        self.OrderBy = None

    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.SortedBy = params.get("SortedBy")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.OrderBy = params.get("OrderBy")


class GetCcnRegionBandwidthLimitsResponse(AbstractModel):
    """GetCcnRegionBandwidthLimits返回参数结构体"""

    def __init__(self):
        """
        :param CcnBandwidthSet: 云联网（CCN）各地域出带宽带宽详情。
        :type CcnBandwidthSet: list of CcnBandwidthInfo
        :param TotalCount: 符合条件的对象数。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.CcnBandwidthSet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("CcnBandwidthSet") is not None:
            self.CcnBandwidthSet = []
            for item in params.get("CcnBandwidthSet"):
                obj = CcnBandwidthInfo()
                obj._deserialize(item)
                self.CcnBandwidthSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class GetCreateCcnBandwidthDealRequest(AbstractModel):
    """GetCreateCcnBandwidthDeal请求参数结构体"""

    def __init__(self):
        """
        :param CcnId: CCN实例ID。
        :type CcnId: str
        :param InstanceChargePrepaid: 预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月实例的购买时长、是否设置自动续费等属性。若指定实例的付费模式为预付费则该参数必传。
        :type InstanceChargePrepaid: :class:`tcecloud.vpc.v20170312.models.InstanceChargePrepaid`
        :param CcnRegionBandwidthLimits: 云联网（CCN）各地域带宽上限。
        :type CcnRegionBandwidthLimits: list of CcnRegionBandwidthLimit
        """
        self.CcnId = None
        self.InstanceChargePrepaid = None
        self.CcnRegionBandwidthLimits = None

    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")
        if params.get("InstanceChargePrepaid") is not None:
            self.InstanceChargePrepaid = InstanceChargePrepaid()
            self.InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))
        if params.get("CcnRegionBandwidthLimits") is not None:
            self.CcnRegionBandwidthLimits = []
            for item in params.get("CcnRegionBandwidthLimits"):
                obj = CcnRegionBandwidthLimit()
                obj._deserialize(item)
                self.CcnRegionBandwidthLimits.append(obj)


class GetCreateCcnBandwidthDealResponse(AbstractModel):
    """GetCreateCcnBandwidthDeal返回参数结构体"""

    def __init__(self):
        """
        :param Deal: 订单详情。
        :type Deal: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Deal = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Deal = params.get("Deal")
        self.RequestId = params.get("RequestId")


class GetDealStatusByNameRequest(AbstractModel):
    """GetDealStatusByName请求参数结构体"""

    def __init__(self):
        """
        :param DealName: 订单号
        :type DealName: str
        """
        self.DealName = None

    def _deserialize(self, params):
        self.DealName = params.get("DealName")


class GetDealStatusByNameResponse(AbstractModel):
    """GetDealStatusByName返回参数结构体"""

    def __init__(self):
        """
        :param DealStatus: 订单号对应的订单状态，UNPAID(未支付)，PAID(已支付)，DELIVERING(发货中)，DELIVER_SUCC(发货成功)，DELIVER_FAIL(发货失败)，REFUNDED(已退款)，CANCELED(已取消)，DENY_PAIDBYOTHERS(代付拒绝)，UNKOWN(未知状态)
        :type DealStatus: str
        :param DealName: 订单号
        :type DealName: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DealStatus = None
        self.DealName = None
        self.RequestId = None

    def _deserialize(self, params):
        self.DealStatus = params.get("DealStatus")
        self.DealName = params.get("DealName")
        self.RequestId = params.get("RequestId")


class GetRenewCcnBandwidthDealRequest(AbstractModel):
    """GetRenewCcnBandwidthDeal请求参数结构体"""

    def __init__(self):
        """
        :param InstanceChargePrepaid: 是否自动续费标识；NOTIFY_AND_AUTO_RENEW：自动续费，NOTIFY_AND_MANUAL_RENEW：手动续费。
        :type InstanceChargePrepaid: :class:`tcecloud.vpc.v20170312.models.InstanceChargePrepaid`
        :param RegionFlowControlId: 流量配置ID。
        :type RegionFlowControlId: str
        """
        self.InstanceChargePrepaid = None
        self.RegionFlowControlId = None

    def _deserialize(self, params):
        if params.get("InstanceChargePrepaid") is not None:
            self.InstanceChargePrepaid = InstanceChargePrepaid()
            self.InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))
        self.RegionFlowControlId = params.get("RegionFlowControlId")


class GetRenewCcnBandwidthDealResponse(AbstractModel):
    """GetRenewCcnBandwidthDeal返回参数结构体"""

    def __init__(self):
        """
        :param Deal: 订单详情。
        :type Deal: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Deal = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Deal = params.get("Deal")
        self.RequestId = params.get("RequestId")


class GetUpdateCcnBandwidthDealRequest(AbstractModel):
    """GetUpdateCcnBandwidthDeal请求参数结构体"""

    def __init__(self):
        """
        :param RenewFlag: 是否自动续费标识；NOTIFY_AND_AUTO_RENEW：自动续费，NOTIFY_AND_MANUAL_RENEW：手动续费。
        :type RenewFlag: str
        :param RegionFlowControlId: 流量配置ID。
        :type RegionFlowControlId: str
        :param MaxBandwidthLimit: 地域间设置带宽，单位：Mbps。
        :type MaxBandwidthLimit: int
        """
        self.RenewFlag = None
        self.RegionFlowControlId = None
        self.MaxBandwidthLimit = None

    def _deserialize(self, params):
        self.RenewFlag = params.get("RenewFlag")
        self.RegionFlowControlId = params.get("RegionFlowControlId")
        self.MaxBandwidthLimit = params.get("MaxBandwidthLimit")


class GetUpdateCcnBandwidthDealResponse(AbstractModel):
    """GetUpdateCcnBandwidthDeal返回参数结构体"""

    def __init__(self):
        """
        :param Deal: 订单详情。
        :type Deal: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Deal = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Deal = params.get("Deal")
        self.RequestId = params.get("RequestId")


class HaVip(AbstractModel):
    """描述 HAVIP 信息"""

    def __init__(self):
        """
                :param HaVipId: `HAVIP`的`ID`，是`HAVIP`的唯一标识。
                :type HaVipId: str
                :param HaVipName: `HAVIP`名称。
                :type HaVipName: str
                :param Vip: 虚拟IP地址。
                :type Vip: str
                :param VpcId: `HAVIP`所在私有网络`ID`。
                :type VpcId: str
                :param SubnetId: `HAVIP`所在子网`ID`。
                :type SubnetId: str
                :param NetworkInterfaceId: `HAVIP`关联弹性网卡`ID`。
                :type NetworkInterfaceId: str
                :param InstanceId: 被绑定的实例`ID`。
                :type InstanceId: str
                :param AddressIp: 绑定`EIP`。
                :type AddressIp: str
                :param State: 状态：
        <li>`AVAILABLE`：运行中</li>
        <li>`UNBIND`：未绑定</li>
                :type State: str
                :param CreatedTime: 创建时间。
                :type CreatedTime: str
                :param Business: 使用havip的业务标识。
                :type Business: str
        """
        self.HaVipId = None
        self.HaVipName = None
        self.Vip = None
        self.VpcId = None
        self.SubnetId = None
        self.NetworkInterfaceId = None
        self.InstanceId = None
        self.AddressIp = None
        self.State = None
        self.CreatedTime = None
        self.Business = None

    def _deserialize(self, params):
        self.HaVipId = params.get("HaVipId")
        self.HaVipName = params.get("HaVipName")
        self.Vip = params.get("Vip")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.NetworkInterfaceId = params.get("NetworkInterfaceId")
        self.InstanceId = params.get("InstanceId")
        self.AddressIp = params.get("AddressIp")
        self.State = params.get("State")
        self.CreatedTime = params.get("CreatedTime")
        self.Business = params.get("Business")


class HaVipAssociateAddressIpRequest(AbstractModel):
    """HaVipAssociateAddressIp请求参数结构体"""

    def __init__(self):
        """
        :param HaVipId: `HAVIP`唯一`ID`，形如：`havip-9o233uri`。必须是没有绑定`EIP`的`HAVIP`
        :type HaVipId: str
        :param AddressIp: 弹性公网`IP`。必须是没有绑定`HAVIP`的`EIP`
        :type AddressIp: str
        """
        self.HaVipId = None
        self.AddressIp = None

    def _deserialize(self, params):
        self.HaVipId = params.get("HaVipId")
        self.AddressIp = params.get("AddressIp")


class HaVipAssociateAddressIpResponse(AbstractModel):
    """HaVipAssociateAddressIp返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class HaVipDisassociateAddressIpRequest(AbstractModel):
    """HaVipDisassociateAddressIp请求参数结构体"""

    def __init__(self):
        """
        :param HaVipId: `HAVIP`唯一`ID`，形如：`havip-9o233uri`。必须是已绑定`EIP`的`HAVIP`。
        :type HaVipId: str
        """
        self.HaVipId = None

    def _deserialize(self, params):
        self.HaVipId = params.get("HaVipId")


class HaVipDisassociateAddressIpResponse(AbstractModel):
    """HaVipDisassociateAddressIp返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class IKEOptionsSpecification(AbstractModel):
    """IKE配置（Internet Key Exchange，因特网密钥交换），IKE具有一套自我保护机制，用户配置网络安全协议"""

    def __init__(self):
        """
        :param PropoEncryAlgorithm: 加密算法，可选值：'3DES-CBC', 'AES-CBC-128', 'AES-CBS-192', 'AES-CBC-256', 'DES-CBC'，默认为3DES-CBC
        :type PropoEncryAlgorithm: str
        :param PropoAuthenAlgorithm: 认证算法：可选值：'MD5', 'SHA1'，默认为MD5
        :type PropoAuthenAlgorithm: str
        :param ExchangeMode: 协商模式：可选值：'AGGRESSIVE', 'MAIN'，默认为MAIN
        :type ExchangeMode: str
        :param LocalIdentity: 本端标识类型：可选值：'ADDRESS', 'FQDN'，默认为ADDRESS
        :type LocalIdentity: str
        :param RemoteIdentity: 对端标识类型：可选值：'ADDRESS', 'FQDN'，默认为ADDRESS
        :type RemoteIdentity: str
        :param LocalAddress: 本端标识，当LocalIdentity选为ADDRESS时，LocalAddress必填。localAddress默认为vpn网关公网IP
        :type LocalAddress: str
        :param RemoteAddress: 对端标识，当RemoteIdentity选为ADDRESS时，RemoteAddress必填
        :type RemoteAddress: str
        :param LocalFqdnName: 本端标识，当LocalIdentity选为FQDN时，LocalFqdnName必填
        :type LocalFqdnName: str
        :param RemoteFqdnName: 对端标识，当remoteIdentity选为FQDN时，RemoteFqdnName必填
        :type RemoteFqdnName: str
        :param DhGroupName: DH group，指定IKE交换密钥时使用的DH组，可选值：'GROUP1', 'GROUP2', 'GROUP5', 'GROUP14', 'GROUP24'，
        :type DhGroupName: str
        :param IKESaLifetimeSeconds: IKE SA Lifetime，单位：秒，设置IKE SA的生存周期，取值范围：60-604800
        :type IKESaLifetimeSeconds: int
        :param IKEVersion: IKE版本
        :type IKEVersion: str
        """
        self.PropoEncryAlgorithm = None
        self.PropoAuthenAlgorithm = None
        self.ExchangeMode = None
        self.LocalIdentity = None
        self.RemoteIdentity = None
        self.LocalAddress = None
        self.RemoteAddress = None
        self.LocalFqdnName = None
        self.RemoteFqdnName = None
        self.DhGroupName = None
        self.IKESaLifetimeSeconds = None
        self.IKEVersion = None

    def _deserialize(self, params):
        self.PropoEncryAlgorithm = params.get("PropoEncryAlgorithm")
        self.PropoAuthenAlgorithm = params.get("PropoAuthenAlgorithm")
        self.ExchangeMode = params.get("ExchangeMode")
        self.LocalIdentity = params.get("LocalIdentity")
        self.RemoteIdentity = params.get("RemoteIdentity")
        self.LocalAddress = params.get("LocalAddress")
        self.RemoteAddress = params.get("RemoteAddress")
        self.LocalFqdnName = params.get("LocalFqdnName")
        self.RemoteFqdnName = params.get("RemoteFqdnName")
        self.DhGroupName = params.get("DhGroupName")
        self.IKESaLifetimeSeconds = params.get("IKESaLifetimeSeconds")
        self.IKEVersion = params.get("IKEVersion")


class IPSECOptionsSpecification(AbstractModel):
    """IPSec配置，Tce提供IPSec安全会话设置"""

    def __init__(self):
        """
        :param EncryptAlgorithm: 加密算法，可选值：'3DES-CBC', 'AES-CBC-128', 'AES-CBC-192', 'AES-CBC-256', 'DES-CBC', 'NULL'， 默认为AES-CBC-128
        :type EncryptAlgorithm: str
        :param IntegrityAlgorith: 认证算法：可选值：'MD5', 'SHA1'，默认为
        :type IntegrityAlgorith: str
        :param IPSECSaLifetimeSeconds: IPsec SA lifetime(s)：单位秒，取值范围：180-604800
        :type IPSECSaLifetimeSeconds: int
        :param PfsDhGroup: PFS：可选值：'NULL', 'DH-GROUP1', 'DH-GROUP2', 'DH-GROUP5', 'DH-GROUP14', 'DH-GROUP24'，默认为NULL
        :type PfsDhGroup: str
        :param IPSECSaLifetimeTraffic: IPsec SA lifetime(KB)：单位KB，取值范围：2560-604800
        :type IPSECSaLifetimeTraffic: int
        """
        self.EncryptAlgorithm = None
        self.IntegrityAlgorith = None
        self.IPSECSaLifetimeSeconds = None
        self.PfsDhGroup = None
        self.IPSECSaLifetimeTraffic = None

    def _deserialize(self, params):
        self.EncryptAlgorithm = params.get("EncryptAlgorithm")
        self.IntegrityAlgorith = params.get("IntegrityAlgorith")
        self.IPSECSaLifetimeSeconds = params.get("IPSECSaLifetimeSeconds")
        self.PfsDhGroup = params.get("PfsDhGroup")
        self.IPSECSaLifetimeTraffic = params.get("IPSECSaLifetimeTraffic")


class InquiryPriceAllocateAddressesRequest(AbstractModel):
    """InquiryPriceAllocateAddresses请求参数结构体"""

    def __init__(self):
        """
        :param AddressCount: 1
        :type AddressCount: int
        :param InternetServiceProvider: 1
        :type InternetServiceProvider: str
        :param VipSet: 1
        :type VipSet: str
        :param TgwGroup: 1
        :type TgwGroup: str
        :param ApplySilence: 1
        :type ApplySilence: int
        :param InternetChargeType: 1
        :type InternetChargeType: str
        :param InternetMaxBandwidthOut: 1
        :type InternetMaxBandwidthOut: int
        :param AddressChargePrepaid: 1
        :type AddressChargePrepaid: :class:`tcecloud.vpc.v20170312.models.AddressChargePrepaid`
        :param DealId: 1
        :type DealId: str
        :param AddressType: 1
        :type AddressType: str
        :param AnycastZone: Anycast发布域，ANYCAST_ZONE_A|ANYCAST_ZONE_B，默认为当前地域可选的任一发布域。
        :type AnycastZone: str
        :param Zone: EIP可用区，用于指定可用区申请EIP。
        :type Zone: str
        :param ApplicableForCLB: 申请可绑定CLB的EIP，默认值为否。仅适用于AnycastEIP。
        :type ApplicableForCLB: bool
        :param Restrictive: 1
        :type Restrictive: bool
        :param BandwidthPackageId: BGP带宽包唯一ID参数。设定该参数且InternetChargeType为BANDWIDTH_PACKAGE，则表示创建的EIP加入该BGP带宽包并采用带宽包计费
        :type BandwidthPackageId: str
        """
        self.AddressCount = None
        self.InternetServiceProvider = None
        self.VipSet = None
        self.TgwGroup = None
        self.ApplySilence = None
        self.InternetChargeType = None
        self.InternetMaxBandwidthOut = None
        self.AddressChargePrepaid = None
        self.DealId = None
        self.AddressType = None
        self.AnycastZone = None
        self.Zone = None
        self.ApplicableForCLB = None
        self.Restrictive = None
        self.BandwidthPackageId = None

    def _deserialize(self, params):
        self.AddressCount = params.get("AddressCount")
        self.InternetServiceProvider = params.get("InternetServiceProvider")
        self.VipSet = params.get("VipSet")
        self.TgwGroup = params.get("TgwGroup")
        self.ApplySilence = params.get("ApplySilence")
        self.InternetChargeType = params.get("InternetChargeType")
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        if params.get("AddressChargePrepaid") is not None:
            self.AddressChargePrepaid = AddressChargePrepaid()
            self.AddressChargePrepaid._deserialize(params.get("AddressChargePrepaid"))
        self.DealId = params.get("DealId")
        self.AddressType = params.get("AddressType")
        self.AnycastZone = params.get("AnycastZone")
        self.Zone = params.get("Zone")
        self.ApplicableForCLB = params.get("ApplicableForCLB")
        self.Restrictive = params.get("Restrictive")
        self.BandwidthPackageId = params.get("BandwidthPackageId")


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


class InquiryPriceAllocateIp6AddressesBandwidthRequest(AbstractModel):
    """InquiryPriceAllocateIp6AddressesBandwidth请求参数结构体"""

    def __init__(self):
        """
        :param Ip6Addresses: 需要开通internet访问能力的IPV6地址
        :type Ip6Addresses: list of str
        :param InternetMaxBandwidthOut: 带宽，单位Mbps。默认是1Mbps
        :type InternetMaxBandwidthOut: int
        :param InternetChargeType: 网络计费模式。IPV6当前支持"TRAFFIC_POSTPAID_BY_HOUR"，默认是TRAFFIC_POSTPAID_BY_HOUR"。
        :type InternetChargeType: str
        """
        self.Ip6Addresses = None
        self.InternetMaxBandwidthOut = None
        self.InternetChargeType = None

    def _deserialize(self, params):
        self.Ip6Addresses = params.get("Ip6Addresses")
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        self.InternetChargeType = params.get("InternetChargeType")


class InquiryPriceAllocateIp6AddressesBandwidthResponse(AbstractModel):
    """InquiryPriceAllocateIp6AddressesBandwidth返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class InquiryPriceCreateBandwidthPackageRequest(AbstractModel):
    """InquiryPriceCreateBandwidthPackage请求参数结构体"""

    def __init__(self):
        """
        :param BandwidthPackageName: 无
        :type BandwidthPackageName: str
        :param NetworkType: 无
        :type NetworkType: str
        :param ChargeType: 无
        :type ChargeType: str
        :param BandwidthPackageCount: 无
        :type BandwidthPackageCount: int
        :param InternetMaxBandwidth: 无
        :type InternetMaxBandwidth: int
        :param TimeSpan: 无
        :type TimeSpan: int
        """
        self.BandwidthPackageName = None
        self.NetworkType = None
        self.ChargeType = None
        self.BandwidthPackageCount = None
        self.InternetMaxBandwidth = None
        self.TimeSpan = None

    def _deserialize(self, params):
        self.BandwidthPackageName = params.get("BandwidthPackageName")
        self.NetworkType = params.get("NetworkType")
        self.ChargeType = params.get("ChargeType")
        self.BandwidthPackageCount = params.get("BandwidthPackageCount")
        self.InternetMaxBandwidth = params.get("InternetMaxBandwidth")
        self.TimeSpan = params.get("TimeSpan")


class InquiryPriceCreateBandwidthPackageResponse(AbstractModel):
    """InquiryPriceCreateBandwidthPackage返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class InquiryPriceCreateCcnBandwidthRequest(AbstractModel):
    """InquiryPriceCreateCcnBandwidth请求参数结构体"""

    def __init__(self):
        """
        :param CcnId: CCN实例ID。
        :type CcnId: str
        :param InstanceChargePrepaid: 预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月实例的购买时长、是否设置自动续费等属性。若指定实例的付费模式为预付费则该参数必传。
        :type InstanceChargePrepaid: :class:`tcecloud.vpc.v20170312.models.InstanceChargePrepaid`
        :param CcnRegionBandwidthLimits: 云联网（CCN）地域带宽详情。
        :type CcnRegionBandwidthLimits: list of CcnRegionBandwidthLimit
        """
        self.CcnId = None
        self.InstanceChargePrepaid = None
        self.CcnRegionBandwidthLimits = None

    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")
        if params.get("InstanceChargePrepaid") is not None:
            self.InstanceChargePrepaid = InstanceChargePrepaid()
            self.InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))
        if params.get("CcnRegionBandwidthLimits") is not None:
            self.CcnRegionBandwidthLimits = []
            for item in params.get("CcnRegionBandwidthLimits"):
                obj = CcnRegionBandwidthLimit()
                obj._deserialize(item)
                self.CcnRegionBandwidthLimits.append(obj)


class InquiryPriceCreateCcnBandwidthResponse(AbstractModel):
    """InquiryPriceCreateCcnBandwidth返回参数结构体"""

    def __init__(self):
        """
        :param Price: 商品价格。
        :type Price: :class:`tcecloud.vpc.v20170312.models.ItemPrice`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Price = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Price") is not None:
            self.Price = ItemPrice()
            self.Price._deserialize(params.get("Price"))
        self.RequestId = params.get("RequestId")


class InquiryPriceCreateTrafficPackagesRequest(AbstractModel):
    """InquiryPriceCreateTrafficPackages请求参数结构体"""

    def __init__(self):
        """
        :param TrafficAmount: 无
        :type TrafficAmount: int
        :param TrafficPackageCount: 无
        :type TrafficPackageCount: int
        """
        self.TrafficAmount = None
        self.TrafficPackageCount = None

    def _deserialize(self, params):
        self.TrafficAmount = params.get("TrafficAmount")
        self.TrafficPackageCount = params.get("TrafficPackageCount")


class InquiryPriceCreateTrafficPackagesResponse(AbstractModel):
    """InquiryPriceCreateTrafficPackages返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class InquiryPriceCreateVpnGatewayRequest(AbstractModel):
    """InquiryPriceCreateVpnGateway请求参数结构体"""

    def __init__(self):
        """
        :param InternetMaxBandwidthOut: 公网带宽设置。可选带宽规格：5, 10, 20, 50, 100；单位：Mbps。
        :type InternetMaxBandwidthOut: int
        :param InstanceChargeType: VPN网关计费模式，PREPAID：表示预付费，即包年包月，POSTPAID_BY_HOUR：表示后付费，即按量计费。默认：POSTPAID_BY_HOUR，如果指定预付费模式，参数InstanceChargePrepaid必填。
        :type InstanceChargeType: str
        :param InstanceChargePrepaid: 预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月实例的购买时长、是否设置自动续费等属性。若指定实例的付费模式为预付费则该参数必传。
        :type InstanceChargePrepaid: :class:`tcecloud.vpc.v20170312.models.InstanceChargePrepaid`
        """
        self.InternetMaxBandwidthOut = None
        self.InstanceChargeType = None
        self.InstanceChargePrepaid = None

    def _deserialize(self, params):
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        self.InstanceChargeType = params.get("InstanceChargeType")
        if params.get("InstanceChargePrepaid") is not None:
            self.InstanceChargePrepaid = InstanceChargePrepaid()
            self.InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))


class InquiryPriceCreateVpnGatewayResponse(AbstractModel):
    """InquiryPriceCreateVpnGateway返回参数结构体"""

    def __init__(self):
        """
        :param Price: 商品价格。
        :type Price: :class:`tcecloud.vpc.v20170312.models.Price`
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


class InquiryPriceModifyAddressInternetChargeTypeRequest(AbstractModel):
    """InquiryPriceModifyAddressInternetChargeType请求参数结构体"""

    def __init__(self):
        """
        :param InternetMaxBandwidthOut: 弹性公网IP调整目标带宽值
        :type InternetMaxBandwidthOut: int
        :param AddressId: 弹性公网IP的唯一ID，形如eip-xxx
        :type AddressId: str
        :param InternetChargeType: 弹性公网IP调整目标计费模式，只支持"BANDWIDTH_PREPAID_BY_MONTH"和"TRAFFIC_POSTPAID_BY_HOUR"
        :type InternetChargeType: str
        :param AddressChargePrepaid: 弹性公网IP的调整目标计费模式是"BANDWIDTH_PREPAID_BY_MONTH"时，必传该参数。
        :type AddressChargePrepaid: :class:`tcecloud.vpc.v20170312.models.AddressChargePrepaid`
        """
        self.InternetMaxBandwidthOut = None
        self.AddressId = None
        self.InternetChargeType = None
        self.AddressChargePrepaid = None

    def _deserialize(self, params):
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        self.AddressId = params.get("AddressId")
        self.InternetChargeType = params.get("InternetChargeType")
        if params.get("AddressChargePrepaid") is not None:
            self.AddressChargePrepaid = AddressChargePrepaid()
            self.AddressChargePrepaid._deserialize(params.get("AddressChargePrepaid"))


class InquiryPriceModifyAddressInternetChargeTypeResponse(AbstractModel):
    """InquiryPriceModifyAddressInternetChargeType返回参数结构体"""

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
        :param AddressIds: EIP唯一ID
        :type AddressIds: list of str
        :param InternetMaxBandwidthOut: 新带宽值
        :type InternetMaxBandwidthOut: int
        :param StartTime: 起始时间
        :type StartTime: str
        :param EndTime: 结束时间
        :type EndTime: str
        :param DealId: 订单ID
        :type DealId: str
        :param BandwidthId: 预约贷款表记录ID
        :type BandwidthId: int
        """
        self.AddressIds = None
        self.InternetMaxBandwidthOut = None
        self.StartTime = None
        self.EndTime = None
        self.DealId = None
        self.BandwidthId = None

    def _deserialize(self, params):
        self.AddressIds = params.get("AddressIds")
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.DealId = params.get("DealId")
        self.BandwidthId = params.get("BandwidthId")


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


class InquiryPriceModifyBandwidthPackageBandwidthRequest(AbstractModel):
    """InquiryPriceModifyBandwidthPackageBandwidth请求参数结构体"""

    def __init__(self):
        """
        :param BandwidthPackageId: 带宽包ID
        :type BandwidthPackageId: str
        :param InternetMaxBandwidth: 修改后的带宽
        :type InternetMaxBandwidth: int
        """
        self.BandwidthPackageId = None
        self.InternetMaxBandwidth = None

    def _deserialize(self, params):
        self.BandwidthPackageId = params.get("BandwidthPackageId")
        self.InternetMaxBandwidth = params.get("InternetMaxBandwidth")


class InquiryPriceModifyBandwidthPackageBandwidthResponse(AbstractModel):
    """InquiryPriceModifyBandwidthPackageBandwidth返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class InquiryPriceModifyIp6AddressesBandwidthRequest(AbstractModel):
    """InquiryPriceModifyIp6AddressesBandwidth请求参数结构体"""

    def __init__(self):
        """
        :param InternetMaxBandwidthOut: 修改的目标带宽，单位Mbps
        :type InternetMaxBandwidthOut: int
        :param Ip6Addresses: IPV6地址。Ip6Addresses和Ip6AddressId必须且只能传一个
        :type Ip6Addresses: list of str
        :param Ip6AddressIds: IPV6地址对应的唯一ID，形如eip-xxxxxxxx。Ip6Addresses和Ip6AddressId必须且只能传一个
        :type Ip6AddressIds: list of str
        """
        self.InternetMaxBandwidthOut = None
        self.Ip6Addresses = None
        self.Ip6AddressIds = None

    def _deserialize(self, params):
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        self.Ip6Addresses = params.get("Ip6Addresses")
        self.Ip6AddressIds = params.get("Ip6AddressIds")


class InquiryPriceModifyIp6AddressesBandwidthResponse(AbstractModel):
    """InquiryPriceModifyIp6AddressesBandwidth返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class InquiryPriceNatGatewayRequest(AbstractModel):
    """InquiryPriceNatGateway请求参数结构体"""

    def __init__(self):
        """
        :param MaxConcurrentConnection: NAT网关并发连接上限，默认值`1000000`
        :type MaxConcurrentConnection: int
        """
        self.MaxConcurrentConnection = None

    def _deserialize(self, params):
        self.MaxConcurrentConnection = params.get("MaxConcurrentConnection")


class InquiryPriceNatGatewayResponse(AbstractModel):
    """InquiryPriceNatGateway返回参数结构体"""

    def __init__(self):
        """
        :param Price: 商品价格。
        :type Price: :class:`tcecloud.vpc.v20170312.models.Price`
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


class InquiryPricePublicIp6AddressesRequest(AbstractModel):
    """InquiryPricePublicIp6Addresses请求参数结构体"""

    def __init__(self):
        """
        :param Ip6Addresses: 需要开通internet访问能力的IPV6地址
        :type Ip6Addresses: list of str
        :param InternetMaxBandwidthOut: 带宽，单位Mbps。默认是1Mbps
        :type InternetMaxBandwidthOut: int
        :param InternetChargeType: 网络计费模式。IPV6当前支持"TRAFFIC_POSTPAID_BY_HOUR"，默认是TRAFFIC_POSTPAID_BY_HOUR"。
        :type InternetChargeType: str
        """
        self.Ip6Addresses = None
        self.InternetMaxBandwidthOut = None
        self.InternetChargeType = None

    def _deserialize(self, params):
        self.Ip6Addresses = params.get("Ip6Addresses")
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        self.InternetChargeType = params.get("InternetChargeType")


class InquiryPricePublicIp6AddressesResponse(AbstractModel):
    """InquiryPricePublicIp6Addresses返回参数结构体"""

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
        :type AddressIds: list of str
        :param AddressChargePrepaid: 1
        :type AddressChargePrepaid: :class:`tcecloud.vpc.v20170312.models.AddressChargePrepaid`
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


class InquiryPriceRenewBandwidthPackageRequest(AbstractModel):
    """InquiryPriceRenewBandwidthPackage请求参数结构体"""

    def __init__(self):
        """
        :param BandwidthPackageId: 带宽包ID
        :type BandwidthPackageId: str
        :param TimeSpan: 续费时长(月)
        :type TimeSpan: int
        """
        self.BandwidthPackageId = None
        self.TimeSpan = None

    def _deserialize(self, params):
        self.BandwidthPackageId = params.get("BandwidthPackageId")
        self.TimeSpan = params.get("TimeSpan")


class InquiryPriceRenewBandwidthPackageResponse(AbstractModel):
    """InquiryPriceRenewBandwidthPackage返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class InquiryPriceRenewCcnBandwidthRequest(AbstractModel):
    """InquiryPriceRenewCcnBandwidth请求参数结构体"""

    def __init__(self):
        """
        :param InstanceChargePrepaid: 预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月实例的购买时长、是否设置自动续费等属性。若指定实例的付费模式为预付费则该参数必传。
        :type InstanceChargePrepaid: :class:`tcecloud.vpc.v20170312.models.InstanceChargePrepaid`
        :param RegionFlowControlId: 流量配置ID。
        :type RegionFlowControlId: str
        """
        self.InstanceChargePrepaid = None
        self.RegionFlowControlId = None

    def _deserialize(self, params):
        if params.get("InstanceChargePrepaid") is not None:
            self.InstanceChargePrepaid = InstanceChargePrepaid()
            self.InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))
        self.RegionFlowControlId = params.get("RegionFlowControlId")


class InquiryPriceRenewCcnBandwidthResponse(AbstractModel):
    """InquiryPriceRenewCcnBandwidth返回参数结构体"""

    def __init__(self):
        """
        :param Price: 商品价格。
        :type Price: :class:`tcecloud.vpc.v20170312.models.ItemPrice`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Price = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Price") is not None:
            self.Price = ItemPrice()
            self.Price._deserialize(params.get("Price"))
        self.RequestId = params.get("RequestId")


class InquiryPriceRenewVpnGatewayRequest(AbstractModel):
    """InquiryPriceRenewVpnGateway请求参数结构体"""

    def __init__(self):
        """
        :param VpnGatewayId: VPN网关实例ID。
        :type VpnGatewayId: str
        :param InstanceChargePrepaid: 预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月实例的购买时长、是否设置自动续费等属性。若指定实例的付费模式为预付费则该参数必传。
        :type InstanceChargePrepaid: :class:`tcecloud.vpc.v20170312.models.InstanceChargePrepaid`
        """
        self.VpnGatewayId = None
        self.InstanceChargePrepaid = None

    def _deserialize(self, params):
        self.VpnGatewayId = params.get("VpnGatewayId")
        if params.get("InstanceChargePrepaid") is not None:
            self.InstanceChargePrepaid = InstanceChargePrepaid()
            self.InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))


class InquiryPriceRenewVpnGatewayResponse(AbstractModel):
    """InquiryPriceRenewVpnGateway返回参数结构体"""

    def __init__(self):
        """
        :param Price: 商品价格。
        :type Price: :class:`tcecloud.vpc.v20170312.models.Price`
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


class InquiryPriceResetVpnGatewayInternetMaxBandwidthRequest(AbstractModel):
    """InquiryPriceResetVpnGatewayInternetMaxBandwidth请求参数结构体"""

    def __init__(self):
        """
        :param VpnGatewayId: VPN网关实例ID。
        :type VpnGatewayId: str
        :param InternetMaxBandwidthOut: 公网带宽设置。可选带宽规格：5, 10, 20, 50, 100；单位：Mbps。
        :type InternetMaxBandwidthOut: int
        """
        self.VpnGatewayId = None
        self.InternetMaxBandwidthOut = None

    def _deserialize(self, params):
        self.VpnGatewayId = params.get("VpnGatewayId")
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")


class InquiryPriceResetVpnGatewayInternetMaxBandwidthResponse(AbstractModel):
    """InquiryPriceResetVpnGatewayInternetMaxBandwidth返回参数结构体"""

    def __init__(self):
        """
        :param Price: 商品价格。
        :type Price: :class:`tcecloud.vpc.v20170312.models.Price`
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


class InquiryPriceUpdateCcnBandwidthRequest(AbstractModel):
    """InquiryPriceUpdateCcnBandwidth请求参数结构体"""

    def __init__(self):
        """
        :param RegionFlowControlId: 流量配置ID。
        :type RegionFlowControlId: str
        :param MaxBandwidthLimit: 云联网（CCN）地域带宽上限。
        :type MaxBandwidthLimit: int
        """
        self.RegionFlowControlId = None
        self.MaxBandwidthLimit = None

    def _deserialize(self, params):
        self.RegionFlowControlId = params.get("RegionFlowControlId")
        self.MaxBandwidthLimit = params.get("MaxBandwidthLimit")


class InquiryPriceUpdateCcnBandwidthResponse(AbstractModel):
    """InquiryPriceUpdateCcnBandwidth返回参数结构体"""

    def __init__(self):
        """
        :param Price: 商品价格。
        :type Price: :class:`tcecloud.vpc.v20170312.models.ItemPrice`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Price = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Price") is not None:
            self.Price = ItemPrice()
            self.Price._deserialize(params.get("Price"))
        self.RequestId = params.get("RequestId")


class InquiryPriceVacancyAddressesRequest(AbstractModel):
    """InquiryPriceVacancyAddresses请求参数结构体"""


class InquiryPriceVacancyAddressesResponse(AbstractModel):
    """InquiryPriceVacancyAddresses返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class InstanceChargePrepaid(AbstractModel):
    """预付费（包年包月）计费对象。"""

    def __init__(self):
        """
        :param Period: 购买实例的时长，单位：月。取值范围：1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 24, 36。
        :type Period: int
        :param RenewFlag: 自动续费标识。取值范围： NOTIFY_AND_AUTO_RENEW：通知过期且自动续费， NOTIFY_AND_MANUAL_RENEW：通知过期不自动续费。默认：NOTIFY_AND_MANUAL_RENEW
        :type RenewFlag: str
        """
        self.Period = None
        self.RenewFlag = None

    def _deserialize(self, params):
        self.Period = params.get("Period")
        self.RenewFlag = params.get("RenewFlag")


class InstanceStatistic(AbstractModel):
    """用于描述实例的统计信息"""

    def __init__(self):
        """
        :param InstanceType: 实例的类型
        :type InstanceType: str
        :param InstanceCount: 实例的个数
        :type InstanceCount: int
        """
        self.InstanceType = None
        self.InstanceCount = None

    def _deserialize(self, params):
        self.InstanceType = params.get("InstanceType")
        self.InstanceCount = params.get("InstanceCount")


class Ip6Rule(AbstractModel):
    """IPV6转换规则"""

    def __init__(self):
        """
        :param Ip6RuleId: IPV6转换规则唯一ID，形如rule6-xxxxxxxx
        :type Ip6RuleId: str
        :param Ip6RuleName: IPV6转换规则名称
        :type Ip6RuleName: str
        :param Vip6: IPV6地址
        :type Vip6: str
        :param Vport6: IPV6端口号
        :type Vport6: int
        :param Protocol: 协议类型，支持TCP/UDP
        :type Protocol: str
        :param Vip: IPV4地址
        :type Vip: str
        :param Vport: IPV4端口号
        :type Vport: int
        :param RuleStatus: 转换规则状态，限于CREATING,RUNNING,DELETING,MODIFYING
        :type RuleStatus: str
        :param CreatedTime: 转换规则创建时间
        :type CreatedTime: str
        """
        self.Ip6RuleId = None
        self.Ip6RuleName = None
        self.Vip6 = None
        self.Vport6 = None
        self.Protocol = None
        self.Vip = None
        self.Vport = None
        self.RuleStatus = None
        self.CreatedTime = None

    def _deserialize(self, params):
        self.Ip6RuleId = params.get("Ip6RuleId")
        self.Ip6RuleName = params.get("Ip6RuleName")
        self.Vip6 = params.get("Vip6")
        self.Vport6 = params.get("Vport6")
        self.Protocol = params.get("Protocol")
        self.Vip = params.get("Vip")
        self.Vport = params.get("Vport")
        self.RuleStatus = params.get("RuleStatus")
        self.CreatedTime = params.get("CreatedTime")


class Ip6RuleInfo(AbstractModel):
    """IPV6转换规则"""

    def __init__(self):
        """
        :param Vport6: IPV6端口号，可在0~65535范围取值
        :type Vport6: int
        :param Protocol: 协议类型，支持TCP/UDP
        :type Protocol: str
        :param Vip: IPV4地址
        :type Vip: str
        :param Vport: IPV4端口号，可在0~65535范围取值
        :type Vport: int
        """
        self.Vport6 = None
        self.Protocol = None
        self.Vip = None
        self.Vport = None

    def _deserialize(self, params):
        self.Vport6 = params.get("Vport6")
        self.Protocol = params.get("Protocol")
        self.Vip = params.get("Vip")
        self.Vport = params.get("Vport")


class Ip6Translator(AbstractModel):
    """IPV6转换实例信息"""

    def __init__(self):
        """
        :param Ip6TranslatorId: IPV6转换实例唯一ID，形如ip6-xxxxxxxx
        :type Ip6TranslatorId: str
        :param Ip6TranslatorName: IPV6转换实例名称
        :type Ip6TranslatorName: str
        :param Vip6: IPV6地址
        :type Vip6: str
        :param IspName: IPV6转换地址所属运营商
        :type IspName: str
        :param TranslatorStatus: 转换实例状态，限于CREATING,RUNNING,DELETING,MODIFYING
        :type TranslatorStatus: str
        :param CreatedTime: IPV6转换实例创建时间
        :type CreatedTime: str
        :param Ip6RuleCount: 绑定的IPV6转换规则数量
        :type Ip6RuleCount: int
        :param IP6RuleSet: IPV6转换规则信息
        :type IP6RuleSet: list of Ip6Rule
        """
        self.Ip6TranslatorId = None
        self.Ip6TranslatorName = None
        self.Vip6 = None
        self.IspName = None
        self.TranslatorStatus = None
        self.CreatedTime = None
        self.Ip6RuleCount = None
        self.IP6RuleSet = None

    def _deserialize(self, params):
        self.Ip6TranslatorId = params.get("Ip6TranslatorId")
        self.Ip6TranslatorName = params.get("Ip6TranslatorName")
        self.Vip6 = params.get("Vip6")
        self.IspName = params.get("IspName")
        self.TranslatorStatus = params.get("TranslatorStatus")
        self.CreatedTime = params.get("CreatedTime")
        self.Ip6RuleCount = params.get("Ip6RuleCount")
        if params.get("IP6RuleSet") is not None:
            self.IP6RuleSet = []
            for item in params.get("IP6RuleSet"):
                obj = Ip6Rule()
                obj._deserialize(item)
                self.IP6RuleSet.append(obj)


class IpField(AbstractModel):
    """IP在线查询的字段信息"""

    def __init__(self):
        """
        :param Comment: 注释字段
        :type Comment: bool
        :param Country: 国家字段信息
        :type Country: bool
        :param Province: 省、州、郡一级行政区域字段信息
        :type Province: bool
        :param City: 市一级行政区域字段信息
        :type City: bool
        :param Region: 市内区域字段信息
        :type Region: bool
        :param Isp: 接入运营商字段信息
        :type Isp: bool
        :param AsName: 骨干运营商字段信息
        :type AsName: bool
        :param AsId: 骨干As号
        :type AsId: bool
        """
        self.Comment = None
        self.Country = None
        self.Province = None
        self.City = None
        self.Region = None
        self.Isp = None
        self.AsName = None
        self.AsId = None

    def _deserialize(self, params):
        self.Comment = params.get("Comment")
        self.Country = params.get("Country")
        self.Province = params.get("Province")
        self.City = params.get("City")
        self.Region = params.get("Region")
        self.Isp = params.get("Isp")
        self.AsName = params.get("AsName")
        self.AsId = params.get("AsId")


class Ipv6Address(AbstractModel):
    """`IPv6`地址信息。"""

    def __init__(self):
        """
                :param Address: `IPv6`地址，形如：`3402:4e00:20:100:0:8cd9:2a67:71f3`
                :type Address: str
                :param Primary: 是否是主`IP`。
                :type Primary: bool
                :param AddressId: `EIP`实例`ID`，形如：`eip-hxlqja90`。
                :type AddressId: str
                :param Description: 描述信息。
                :type Description: str
                :param IsWanIpBlocked: 公网IP是否被封堵。
                :type IsWanIpBlocked: bool
                :param State: `IPv6`地址状态：
        <li>`PENDING`：生产中</li>
        <li>`MIGRATING`：迁移中</li>
        <li>`DELETING`：删除中</li>
        <li>`AVAILABLE`：可用的</li>
                :type State: str
        """
        self.Address = None
        self.Primary = None
        self.AddressId = None
        self.Description = None
        self.IsWanIpBlocked = None
        self.State = None

    def _deserialize(self, params):
        self.Address = params.get("Address")
        self.Primary = params.get("Primary")
        self.AddressId = params.get("AddressId")
        self.Description = params.get("Description")
        self.IsWanIpBlocked = params.get("IsWanIpBlocked")
        self.State = params.get("State")


class Ipv6SubnetCidrBlock(AbstractModel):
    """IPv6子网段对象。"""

    def __init__(self):
        """
        :param SubnetId: 子网实例`ID`。形如：`subnet-pxir56ns`。
        :type SubnetId: str
        :param Ipv6CidrBlock: `IPv6`子网段。形如：`3402:4e00:20:1001::/64`
        :type Ipv6CidrBlock: str
        """
        self.SubnetId = None
        self.Ipv6CidrBlock = None

    def _deserialize(self, params):
        self.SubnetId = params.get("SubnetId")
        self.Ipv6CidrBlock = params.get("Ipv6CidrBlock")


class ItemPrice(AbstractModel):
    """单项计费价格信息"""

    def __init__(self):
        """
        :param UnitPrice: 按量计费后付费单价，单位：元。
        :type UnitPrice: float
        :param ChargeUnit: 按量计费后付费计价单元，可取值范围： HOUR：表示计价单元是按每小时来计算。当前涉及该计价单元的场景有：实例按小时后付费（POSTPAID_BY_HOUR）、带宽按小时后付费（BANDWIDTH_POSTPAID_BY_HOUR）： GB：表示计价单元是按每GB来计算。当前涉及该计价单元的场景有：流量按小时后付费（TRAFFIC_POSTPAID_BY_HOUR）。
        :type ChargeUnit: str
        :param OriginalPrice: 预付费商品的原价，单位：元。
        :type OriginalPrice: float
        :param DiscountPrice: 预付费商品的折扣价，单位：元。
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


class LocalDestinationIpPortTranslationNatRule(AbstractModel):
    """本端目的IP端口转换复杂结构"""

    def __init__(self):
        """
        :param Protocol: 协议
        :type Protocol: str
        :param OriginalPort: 源端口
        :type OriginalPort: int
        :param OriginalIp: 源IP
        :type OriginalIp: str
        :param TranslationPort: 目的端口
        :type TranslationPort: int
        :param TranslationIp: 目的IP
        :type TranslationIp: str
        :param Description: 描述
        :type Description: str
        """
        self.Protocol = None
        self.OriginalPort = None
        self.OriginalIp = None
        self.TranslationPort = None
        self.TranslationIp = None
        self.Description = None

    def _deserialize(self, params):
        self.Protocol = params.get("Protocol")
        self.OriginalPort = params.get("OriginalPort")
        self.OriginalIp = params.get("OriginalIp")
        self.TranslationPort = params.get("TranslationPort")
        self.TranslationIp = params.get("TranslationIp")
        self.Description = params.get("Description")


class LocalIpTranslationAclRule(AbstractModel):
    """本端IP转换ACL规则复杂类型"""

    def __init__(self):
        """
        :param Protocol: 协议
        :type Protocol: str
        :param SourcePort: 源端口
        :type SourcePort: str
        :param DestinationCidr: 目的IP
        :type DestinationCidr: str
        :param DestinationPort: 目的端口
        :type DestinationPort: str
        :param Action: 0 或 1
        :type Action: int
        """
        self.Protocol = None
        self.SourcePort = None
        self.DestinationCidr = None
        self.DestinationPort = None
        self.Action = None

    def _deserialize(self, params):
        self.Protocol = params.get("Protocol")
        self.SourcePort = params.get("SourcePort")
        self.DestinationCidr = params.get("DestinationCidr")
        self.DestinationPort = params.get("DestinationPort")
        self.Action = params.get("Action")


class LocalIpTranslationAclRuleNeedId(AbstractModel):
    """本端IP转换ACL规则复杂类型"""

    def __init__(self):
        """
        :param Protocol: 协议
        :type Protocol: str
        :param SourcePort: 源端口
        :type SourcePort: str
        :param DestinationCidr: 目的IP
        :type DestinationCidr: str
        :param DestinationPort: 目的端口
        :type DestinationPort: str
        :param AclRuleId: 规则ID
        :type AclRuleId: int
        :param Action: 0 或 1
        :type Action: int
        """
        self.Protocol = None
        self.SourcePort = None
        self.DestinationCidr = None
        self.DestinationPort = None
        self.AclRuleId = None
        self.Action = None

    def _deserialize(self, params):
        self.Protocol = params.get("Protocol")
        self.SourcePort = params.get("SourcePort")
        self.DestinationCidr = params.get("DestinationCidr")
        self.DestinationPort = params.get("DestinationPort")
        self.AclRuleId = params.get("AclRuleId")
        self.Action = params.get("Action")


class LocalIpTranslationNatRule(AbstractModel):
    """本端IP转换复杂类型"""

    def __init__(self):
        """
                :param OriginalIp: 原始IP
                :type OriginalIp: str
                :param TranslationIp: 映射IP
                :type TranslationIp: str
                :param Description: 描述
        注意：此字段可能返回 null，表示取不到有效值。
                :type Description: str
        """
        self.OriginalIp = None
        self.TranslationIp = None
        self.Description = None

    def _deserialize(self, params):
        self.OriginalIp = params.get("OriginalIp")
        self.TranslationIp = params.get("TranslationIp")
        self.Description = params.get("Description")


class LocalSourceIpPortTranslationAclRule(AbstractModel):
    """本端源IP端口转换ACL映射规则"""

    def __init__(self):
        """
        :param Protocol: 协议
        :type Protocol: str
        :param SourceCidr: 源地址
        :type SourceCidr: str
        :param SourcePort: 源端口
        :type SourcePort: str
        :param DestinationCidr: 目的地址
        :type DestinationCidr: str
        :param DestinationPort: 目的端口
        :type DestinationPort: str
        :param Action: 动作
        :type Action: int
        """
        self.Protocol = None
        self.SourceCidr = None
        self.SourcePort = None
        self.DestinationCidr = None
        self.DestinationPort = None
        self.Action = None

    def _deserialize(self, params):
        self.Protocol = params.get("Protocol")
        self.SourceCidr = params.get("SourceCidr")
        self.SourcePort = params.get("SourcePort")
        self.DestinationCidr = params.get("DestinationCidr")
        self.DestinationPort = params.get("DestinationPort")
        self.Action = params.get("Action")


class LocalSourceIpPortTranslationAclRuleNeedId(AbstractModel):
    """本端源IP端口转换ACL映射规则"""

    def __init__(self):
        """
        :param Protocol: 协议
        :type Protocol: str
        :param SourceCidr: 源地址
        :type SourceCidr: str
        :param SourcePort: 源端口
        :type SourcePort: str
        :param DestinationCidr: 目的地址
        :type DestinationCidr: str
        :param DestinationPort: 目的端口
        :type DestinationPort: str
        :param AclRuleId: ACL规则ID
        :type AclRuleId: int
        :param Action: 动作
        :type Action: int
        """
        self.Protocol = None
        self.SourceCidr = None
        self.SourcePort = None
        self.DestinationCidr = None
        self.DestinationPort = None
        self.AclRuleId = None
        self.Action = None

    def _deserialize(self, params):
        self.Protocol = params.get("Protocol")
        self.SourceCidr = params.get("SourceCidr")
        self.SourcePort = params.get("SourcePort")
        self.DestinationCidr = params.get("DestinationCidr")
        self.DestinationPort = params.get("DestinationPort")
        self.AclRuleId = params.get("AclRuleId")
        self.Action = params.get("Action")


class LocalSourceIpPortTranslationNatRule(AbstractModel):
    """专线网关本端源IP端口NAT映射地址池"""

    def __init__(self):
        """
        :param IpPool: IP地址池
        :type IpPool: str
        :param Description: 描述
        :type Description: str
        """
        self.IpPool = None
        self.Description = None

    def _deserialize(self, params):
        self.IpPool = params.get("IpPool")
        self.Description = params.get("Description")


class MigrateAddressesRequest(AbstractModel):
    """MigrateAddresses请求参数结构体"""

    def __init__(self):
        """
        :param OldAppId: 弹性公网IP当前所属的账号AppId。公共请求参数中的AppId是迁移目标账号AppId。
        :type OldAppId: int
        :param OldUin: 弹性公网IP当前所属的账号Uin。公共请求参数中的Uin是迁移目标账号Uin
        :type OldUin: str
        :param AddressIds: 待迁移的弹性公网IP唯一ID列表
        :type AddressIds: list of str
        :param DryRun: 用于检测弹性公网IP是否满足迁移条件，不会执行实际迁移。
        :type DryRun: bool
        """
        self.OldAppId = None
        self.OldUin = None
        self.AddressIds = None
        self.DryRun = None

    def _deserialize(self, params):
        self.OldAppId = params.get("OldAppId")
        self.OldUin = params.get("OldUin")
        self.AddressIds = params.get("AddressIds")
        self.DryRun = params.get("DryRun")


class MigrateAddressesResponse(AbstractModel):
    """MigrateAddresses返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class MigrateNetworkInterfaceRequest(AbstractModel):
    """MigrateNetworkInterface请求参数结构体"""

    def __init__(self):
        """
        :param NetworkInterfaceId: 弹性网卡实例ID，例如：eni-m6dyj72l。
        :type NetworkInterfaceId: str
        :param SourceInstanceId: 弹性网卡当前绑定的CVM实例ID。形如：ins-r8hr2upy。
        :type SourceInstanceId: str
        :param DestinationInstanceId: 待迁移的目的CVM实例ID。
        :type DestinationInstanceId: str
        """
        self.NetworkInterfaceId = None
        self.SourceInstanceId = None
        self.DestinationInstanceId = None

    def _deserialize(self, params):
        self.NetworkInterfaceId = params.get("NetworkInterfaceId")
        self.SourceInstanceId = params.get("SourceInstanceId")
        self.DestinationInstanceId = params.get("DestinationInstanceId")


class MigrateNetworkInterfaceResponse(AbstractModel):
    """MigrateNetworkInterface返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class MigratePrivateIpAddressRequest(AbstractModel):
    """MigratePrivateIpAddress请求参数结构体"""

    def __init__(self):
        """
        :param SourceNetworkInterfaceId: 当内网IP绑定的弹性网卡实例ID，例如：eni-m6dyj72l。
        :type SourceNetworkInterfaceId: str
        :param DestinationNetworkInterfaceId: 待迁移的目的弹性网卡实例ID。
        :type DestinationNetworkInterfaceId: str
        :param PrivateIpAddress: 迁移的内网IP地址，例如：10.0.0.6。
        :type PrivateIpAddress: str
        """
        self.SourceNetworkInterfaceId = None
        self.DestinationNetworkInterfaceId = None
        self.PrivateIpAddress = None

    def _deserialize(self, params):
        self.SourceNetworkInterfaceId = params.get("SourceNetworkInterfaceId")
        self.DestinationNetworkInterfaceId = params.get("DestinationNetworkInterfaceId")
        self.PrivateIpAddress = params.get("PrivateIpAddress")


class MigratePrivateIpAddressResponse(AbstractModel):
    """MigratePrivateIpAddress返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyAddressAttributeRequest(AbstractModel):
    """ModifyAddressAttribute请求参数结构体"""

    def __init__(self):
        """
        :param AddressId: 标识 EIP 的唯一 ID。EIP 唯一 ID 形如：`eip-11112222`。
        :type AddressId: str
        :param AddressName: 修改后的 EIP 名称。长度上限为20个字符。
        :type AddressName: str
        :param EipDirectConnection: 设定EIP是否直通，"TRUE"表示直通，"FALSE"表示非直通。注意该参数仅对EIP直通功能可见的用户可以设定。
        :type EipDirectConnection: str
        :param CascadeRelease: 1
        :type CascadeRelease: bool
        """
        self.AddressId = None
        self.AddressName = None
        self.EipDirectConnection = None
        self.CascadeRelease = None

    def _deserialize(self, params):
        self.AddressId = params.get("AddressId")
        self.AddressName = params.get("AddressName")
        self.EipDirectConnection = params.get("EipDirectConnection")
        self.CascadeRelease = params.get("CascadeRelease")


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


class ModifyAddressInternetChargeTypeRequest(AbstractModel):
    """ModifyAddressInternetChargeType请求参数结构体"""

    def __init__(self):
        """
        :param AddressId: 弹性公网IP的唯一ID，形如eip-xxx
        :type AddressId: str
        :param InternetChargeType: 弹性公网IP调整目标计费模式，只支持"BANDWIDTH_PREPAID_BY_MONTH"和"TRAFFIC_POSTPAID_BY_HOUR"
        :type InternetChargeType: str
        :param InternetMaxBandwidthOut: 弹性公网IP调整目标带宽值
        :type InternetMaxBandwidthOut: int
        :param StartTime: 无
        :type StartTime: str
        :param EndTime: 无
        :type EndTime: str
        :param DealId: 无
        :type DealId: str
        :param AddressChargePrepaid: 包月带宽网络计费模式参数。弹性公网IP的调整目标计费模式是"BANDWIDTH_PREPAID_BY_MONTH"时，必传该参数。
        :type AddressChargePrepaid: :class:`tcecloud.vpc.v20170312.models.AddressChargePrepaid`
        """
        self.AddressId = None
        self.InternetChargeType = None
        self.InternetMaxBandwidthOut = None
        self.StartTime = None
        self.EndTime = None
        self.DealId = None
        self.AddressChargePrepaid = None

    def _deserialize(self, params):
        self.AddressId = params.get("AddressId")
        self.InternetChargeType = params.get("InternetChargeType")
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.DealId = params.get("DealId")
        if params.get("AddressChargePrepaid") is not None:
            self.AddressChargePrepaid = AddressChargePrepaid()
            self.AddressChargePrepaid._deserialize(params.get("AddressChargePrepaid"))


class ModifyAddressInternetChargeTypeResponse(AbstractModel):
    """ModifyAddressInternetChargeType返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyAddressTemplateAttributeRequest(AbstractModel):
    """ModifyAddressTemplateAttribute请求参数结构体"""

    def __init__(self):
        """
        :param AddressTemplateId: IP地址模板实例ID，例如：ipm-mdunqeb6。
        :type AddressTemplateId: str
        :param AddressTemplateName: IP地址模板名称。
        :type AddressTemplateName: str
        :param Addresses: 地址信息，支持 IP、CIDR、IP 范围。
        :type Addresses: list of str
        """
        self.AddressTemplateId = None
        self.AddressTemplateName = None
        self.Addresses = None

    def _deserialize(self, params):
        self.AddressTemplateId = params.get("AddressTemplateId")
        self.AddressTemplateName = params.get("AddressTemplateName")
        self.Addresses = params.get("Addresses")


class ModifyAddressTemplateAttributeResponse(AbstractModel):
    """ModifyAddressTemplateAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyAddressTemplateGroupAttributeRequest(AbstractModel):
    """ModifyAddressTemplateGroupAttribute请求参数结构体"""

    def __init__(self):
        """
        :param AddressTemplateGroupId: IP地址模板集合实例ID，例如：ipmg-2uw6ujo6。
        :type AddressTemplateGroupId: str
        :param AddressTemplateGroupName: IP地址模板集合名称。
        :type AddressTemplateGroupName: str
        :param AddressTemplateIds: IP地址模板实例ID， 例如：ipm-mdunqeb6。
        :type AddressTemplateIds: list of str
        """
        self.AddressTemplateGroupId = None
        self.AddressTemplateGroupName = None
        self.AddressTemplateIds = None

    def _deserialize(self, params):
        self.AddressTemplateGroupId = params.get("AddressTemplateGroupId")
        self.AddressTemplateGroupName = params.get("AddressTemplateGroupName")
        self.AddressTemplateIds = params.get("AddressTemplateIds")


class ModifyAddressTemplateGroupAttributeResponse(AbstractModel):
    """ModifyAddressTemplateGroupAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyAddressesAttributeRequest(AbstractModel):
    """ModifyAddressesAttribute请求参数结构体"""

    def __init__(self):
        """
        :param AddressIds: 标识 EIP 的唯一 ID 列表。EIP 唯一 ID 形如：`eip-11112222`。
        :type AddressIds: list of str
        :param CascadeRelease: 1
        :type CascadeRelease: bool
        :param EipDirectConnection: EIP直通属性
        :type EipDirectConnection: bool
        :param FtpAlg: EIP FTP ALG属性
        :type FtpAlg: bool
        :param SipAlg: EIP SIP ALG属性
        :type SipAlg: bool
        :param InstanceIds: 云主机CVM的唯一ID列表，形如`ins-111122222`。该参数用于给云主机的主网卡主外网IP设定属性，且不可和AddressIds同时传入。
        :type InstanceIds: list of str
        """
        self.AddressIds = None
        self.CascadeRelease = None
        self.EipDirectConnection = None
        self.FtpAlg = None
        self.SipAlg = None
        self.InstanceIds = None

    def _deserialize(self, params):
        self.AddressIds = params.get("AddressIds")
        self.CascadeRelease = params.get("CascadeRelease")
        self.EipDirectConnection = params.get("EipDirectConnection")
        self.FtpAlg = params.get("FtpAlg")
        self.SipAlg = params.get("SipAlg")
        self.InstanceIds = params.get("InstanceIds")


class ModifyAddressesAttributeResponse(AbstractModel):
    """ModifyAddressesAttribute返回参数结构体"""

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
        :param AddressIds: EIP唯一标识ID，形如'eip-xxxx'
        :type AddressIds: list of str
        :param InternetMaxBandwidthOut: 调整带宽目标值
        :type InternetMaxBandwidthOut: int
        :param StartTime: 包月带宽起始时间
        :type StartTime: str
        :param EndTime: 包月带宽结束时间
        :type EndTime: str
        """
        self.AddressIds = None
        self.InternetMaxBandwidthOut = None
        self.StartTime = None
        self.EndTime = None

    def _deserialize(self, params):
        self.AddressIds = params.get("AddressIds")
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")


class ModifyAddressesBandwidthResponse(AbstractModel):
    """ModifyAddressesBandwidth返回参数结构体"""

    def __init__(self):
        """
        :param TaskId: 异步任务TaskId。可以使用DescribeTaskResult接口查询任务状态。
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class ModifyAssistantCidrRequest(AbstractModel):
    """ModifyAssistantCidr请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: `VPC`实例`ID`。形如：`vpc-6v2ht8q5`
        :type VpcId: str
        :param NewCidrBlocks: 待添加的负载CIDR。CIDR数组，格式如["10.0.0.0/16", "172.16.0.0/16"]
        :type NewCidrBlocks: list of str
        :param OldCidrBlocks: 待删除的负载CIDR。CIDR数组，格式如["10.0.0.0/16", "172.16.0.0/16"]
        :type OldCidrBlocks: list of str
        """
        self.VpcId = None
        self.NewCidrBlocks = None
        self.OldCidrBlocks = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.NewCidrBlocks = params.get("NewCidrBlocks")
        self.OldCidrBlocks = params.get("OldCidrBlocks")


class ModifyAssistantCidrResponse(AbstractModel):
    """ModifyAssistantCidr返回参数结构体"""

    def __init__(self):
        """
        :param AssistantCidrSet: 辅助CIDR数组。
        :type AssistantCidrSet: list of AssistantCidr
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AssistantCidrSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("AssistantCidrSet") is not None:
            self.AssistantCidrSet = []
            for item in params.get("AssistantCidrSet"):
                obj = AssistantCidr()
                obj._deserialize(item)
                self.AssistantCidrSet.append(obj)
        self.RequestId = params.get("RequestId")


class ModifyBandwidthPackageAttributeRequest(AbstractModel):
    """ModifyBandwidthPackageAttribute请求参数结构体"""

    def __init__(self):
        """
        :param BandwidthPackageId: 带宽包唯一标识ID
        :type BandwidthPackageId: str
        :param BandwidthPackageName: 带宽包名称
        :type BandwidthPackageName: str
        :param ChargeType: 带宽包计费模式
        :type ChargeType: str
        """
        self.BandwidthPackageId = None
        self.BandwidthPackageName = None
        self.ChargeType = None

    def _deserialize(self, params):
        self.BandwidthPackageId = params.get("BandwidthPackageId")
        self.BandwidthPackageName = params.get("BandwidthPackageName")
        self.ChargeType = params.get("ChargeType")


class ModifyBandwidthPackageAttributeResponse(AbstractModel):
    """ModifyBandwidthPackageAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyBandwidthPackageBandwidthRequest(AbstractModel):
    """ModifyBandwidthPackageBandwidth请求参数结构体"""

    def __init__(self):
        """
        :param InternetMaxBandwidth: 带宽包限速大小。单位：Mbps，-1表示不限速。
        :type InternetMaxBandwidth: int
        :param BandwidthPackageId: 共享带宽包ID
        :type BandwidthPackageId: str
        :param BandwidthPackageIds: [已废弃]共享带宽包ID列表
        :type BandwidthPackageIds: list of str
        """
        self.InternetMaxBandwidth = None
        self.BandwidthPackageId = None
        self.BandwidthPackageIds = None

    def _deserialize(self, params):
        self.InternetMaxBandwidth = params.get("InternetMaxBandwidth")
        self.BandwidthPackageId = params.get("BandwidthPackageId")
        self.BandwidthPackageIds = params.get("BandwidthPackageIds")


class ModifyBandwidthPackageBandwidthResponse(AbstractModel):
    """ModifyBandwidthPackageBandwidth返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyCcnAttributeRequest(AbstractModel):
    """ModifyCcnAttribute请求参数结构体"""

    def __init__(self):
        """
        :param CcnId: CCN实例ID。形如：ccn-f49l6u0z。
        :type CcnId: str
        :param CcnName: CCN名称，最大长度不能超过60个字节。
        :type CcnName: str
        :param CcnDescription: CCN描述信息，最大长度不能超过100个字节。
        :type CcnDescription: str
        """
        self.CcnId = None
        self.CcnName = None
        self.CcnDescription = None

    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")
        self.CcnName = params.get("CcnName")
        self.CcnDescription = params.get("CcnDescription")


class ModifyCcnAttributeResponse(AbstractModel):
    """ModifyCcnAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyCcnRegionBandwidthLimitsTypeRequest(AbstractModel):
    """ModifyCcnRegionBandwidthLimitsType请求参数结构体"""

    def __init__(self):
        """
        :param CcnId: 云联网实例ID。
        :type CcnId: str
        :param BandwidthLimitType: 云联网限速类型，INTER_REGION_LIMIT：地域间限速，OUTER_REGION_LIMIT：地域出口限速。
        :type BandwidthLimitType: str
        """
        self.CcnId = None
        self.BandwidthLimitType = None

    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")
        self.BandwidthLimitType = params.get("BandwidthLimitType")


class ModifyCcnRegionBandwidthLimitsTypeResponse(AbstractModel):
    """ModifyCcnRegionBandwidthLimitsType返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyCustomerGatewayAttributeRequest(AbstractModel):
    """ModifyCustomerGatewayAttribute请求参数结构体"""

    def __init__(self):
        """
        :param CustomerGatewayId: 对端网关ID，例如：cgw-2wqq41m9，可通过DescribeCustomerGateways接口查询对端网关。
        :type CustomerGatewayId: str
        :param CustomerGatewayName: 对端网关名称，可任意命名，但不得超过60个字符。
        :type CustomerGatewayName: str
        """
        self.CustomerGatewayId = None
        self.CustomerGatewayName = None

    def _deserialize(self, params):
        self.CustomerGatewayId = params.get("CustomerGatewayId")
        self.CustomerGatewayName = params.get("CustomerGatewayName")


class ModifyCustomerGatewayAttributeResponse(AbstractModel):
    """ModifyCustomerGatewayAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDirectConnectGatewayAttributeRequest(AbstractModel):
    """ModifyDirectConnectGatewayAttribute请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关唯一`ID`，形如：`dcg-9o233uri`。
        :type DirectConnectGatewayId: str
        :param DirectConnectGatewayName: 专线网关名称，可任意命名，但不得超过60个字符。
        :type DirectConnectGatewayName: str
        :param CcnRouteType: 云联网路由学习类型，可选值：`BGP`（自动学习）、`STATIC`（静态，即用户配置）。只有云联网类型专线网关且开启了BGP功能才支持修改`CcnRouteType`。
        :type CcnRouteType: str
        :param EnableBGPCommunity: 专线网关开启BGP community属性。
        :type EnableBGPCommunity: bool
        """
        self.DirectConnectGatewayId = None
        self.DirectConnectGatewayName = None
        self.CcnRouteType = None
        self.EnableBGPCommunity = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.DirectConnectGatewayName = params.get("DirectConnectGatewayName")
        self.CcnRouteType = params.get("CcnRouteType")
        self.EnableBGPCommunity = params.get("EnableBGPCommunity")


class ModifyDirectConnectGatewayAttributeResponse(AbstractModel):
    """ModifyDirectConnectGatewayAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyFlowLogAttributeRequest(AbstractModel):
    """ModifyFlowLogAttribute请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: 私用网络ID或者统一ID，建议使用统一ID
        :type VpcId: str
        :param FlowLogId: 流日志唯一ID
        :type FlowLogId: str
        :param FlowLogName: 流日志实例名字
        :type FlowLogName: str
        :param FlowLogDescription: 流日志实例描述
        :type FlowLogDescription: str
        """
        self.VpcId = None
        self.FlowLogId = None
        self.FlowLogName = None
        self.FlowLogDescription = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.FlowLogId = params.get("FlowLogId")
        self.FlowLogName = params.get("FlowLogName")
        self.FlowLogDescription = params.get("FlowLogDescription")


class ModifyFlowLogAttributeResponse(AbstractModel):
    """ModifyFlowLogAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyGatewayFlowQosRequest(AbstractModel):
    """ModifyGatewayFlowQos请求参数结构体"""

    def __init__(self):
        """
                :param GatewayId: 网关实例ID，目前我们支持的网关实例类型有，
        专线网关实例ID，形如，`dcg-ltjahce6`；
        Nat网关实例ID，形如，`nat-ltjahce6`；
        VPN网关实例ID，形如，`vpn-ltjahce6`。
                :type GatewayId: str
                :param Bandwidth: 流控带宽值。
                :type Bandwidth: int
                :param IpAddresses: 限流的云服务器内网IP。
                :type IpAddresses: list of str
        """
        self.GatewayId = None
        self.Bandwidth = None
        self.IpAddresses = None

    def _deserialize(self, params):
        self.GatewayId = params.get("GatewayId")
        self.Bandwidth = params.get("Bandwidth")
        self.IpAddresses = params.get("IpAddresses")


class ModifyGatewayFlowQosResponse(AbstractModel):
    """ModifyGatewayFlowQos返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyHaVipAttributeRequest(AbstractModel):
    """ModifyHaVipAttribute请求参数结构体"""

    def __init__(self):
        """
        :param HaVipId: `HAVIP`唯一`ID`，形如：`havip-9o233uri`。
        :type HaVipId: str
        :param HaVipName: `HAVIP`名称，可任意命名，但不得超过60个字符。
        :type HaVipName: str
        """
        self.HaVipId = None
        self.HaVipName = None

    def _deserialize(self, params):
        self.HaVipId = params.get("HaVipId")
        self.HaVipName = params.get("HaVipName")


class ModifyHaVipAttributeResponse(AbstractModel):
    """ModifyHaVipAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyIp6AddressesBandwidthRequest(AbstractModel):
    """ModifyIp6AddressesBandwidth请求参数结构体"""

    def __init__(self):
        """
        :param InternetMaxBandwidthOut: 修改的目标带宽，单位Mbps
        :type InternetMaxBandwidthOut: int
        :param Ip6Addresses: IPV6地址。Ip6Addresses和Ip6AddressId必须且只能传一个
        :type Ip6Addresses: list of str
        :param Ip6AddressIds: IPV6地址对应的唯一ID，形如eip-xxxxxxxx。Ip6Addresses和Ip6AddressId必须且只能传一个
        :type Ip6AddressIds: list of str
        """
        self.InternetMaxBandwidthOut = None
        self.Ip6Addresses = None
        self.Ip6AddressIds = None

    def _deserialize(self, params):
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        self.Ip6Addresses = params.get("Ip6Addresses")
        self.Ip6AddressIds = params.get("Ip6AddressIds")


class ModifyIp6AddressesBandwidthResponse(AbstractModel):
    """ModifyIp6AddressesBandwidth返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyIp6RuleRequest(AbstractModel):
    """ModifyIp6Rule请求参数结构体"""

    def __init__(self):
        """
        :param Ip6TranslatorId: IPV6转换实例唯一ID，形如ip6-xxxxxxxx
        :type Ip6TranslatorId: str
        :param Ip6RuleId: IPV6转换规则唯一ID，形如rule6-xxxxxxxx
        :type Ip6RuleId: str
        :param Ip6RuleName: IPV6转换规则修改后的名称
        :type Ip6RuleName: str
        :param Vip: IPV6转换规则修改后的IPV4地址
        :type Vip: str
        :param Vport: IPV6转换规则修改后的IPV4端口号
        :type Vport: int
        """
        self.Ip6TranslatorId = None
        self.Ip6RuleId = None
        self.Ip6RuleName = None
        self.Vip = None
        self.Vport = None

    def _deserialize(self, params):
        self.Ip6TranslatorId = params.get("Ip6TranslatorId")
        self.Ip6RuleId = params.get("Ip6RuleId")
        self.Ip6RuleName = params.get("Ip6RuleName")
        self.Vip = params.get("Vip")
        self.Vport = params.get("Vport")


class ModifyIp6RuleResponse(AbstractModel):
    """ModifyIp6Rule返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyIp6TranslatorRequest(AbstractModel):
    """ModifyIp6Translator请求参数结构体"""

    def __init__(self):
        """
        :param Ip6TranslatorId: IPV6转换实例唯一ID，形如ip6-xxxxxxxxx
        :type Ip6TranslatorId: str
        :param Ip6TranslatorName: IPV6转换实例修改名称
        :type Ip6TranslatorName: str
        """
        self.Ip6TranslatorId = None
        self.Ip6TranslatorName = None

    def _deserialize(self, params):
        self.Ip6TranslatorId = params.get("Ip6TranslatorId")
        self.Ip6TranslatorName = params.get("Ip6TranslatorName")


class ModifyIp6TranslatorResponse(AbstractModel):
    """ModifyIp6Translator返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyIpv6AddressesAttributeRequest(AbstractModel):
    """ModifyIpv6AddressesAttribute请求参数结构体"""

    def __init__(self):
        """
        :param NetworkInterfaceId: 弹性网卡实例`ID`，形如：`eni-m6dyj72l`。
        :type NetworkInterfaceId: str
        :param Ipv6Addresses: 指定的内网IPv6`地址信息。
        :type Ipv6Addresses: list of Ipv6Address
        """
        self.NetworkInterfaceId = None
        self.Ipv6Addresses = None

    def _deserialize(self, params):
        self.NetworkInterfaceId = params.get("NetworkInterfaceId")
        if params.get("Ipv6Addresses") is not None:
            self.Ipv6Addresses = []
            for item in params.get("Ipv6Addresses"):
                obj = Ipv6Address()
                obj._deserialize(item)
                self.Ipv6Addresses.append(obj)


class ModifyIpv6AddressesAttributeResponse(AbstractModel):
    """ModifyIpv6AddressesAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyLocalDestinationIpPortTranslationNatRuleRequest(AbstractModel):
    """ModifyLocalDestinationIpPortTranslationNatRule请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID
        :type DirectConnectGatewayId: str
        :param VpcId: 字符型VPCID
        :type VpcId: str
        :param OldProtocol: 旧的协议
        :type OldProtocol: str
        :param OldOriginalPort: 旧的源端口
        :type OldOriginalPort: int
        :param OldOriginalIp: 旧的源IP
        :type OldOriginalIp: str
        :param OldTranslationPort: 旧的目的端口
        :type OldTranslationPort: int
        :param OldTranslationIp: 旧的目的IP
        :type OldTranslationIp: str
        :param Protocol: 修改后的协议
        :type Protocol: str
        :param OriginalPort: 修改后的源端口
        :type OriginalPort: int
        :param OriginalIp: 修改后的源IP
        :type OriginalIp: str
        :param TranslationPort: 修改后的目的端口
        :type TranslationPort: int
        :param TranslationIp: 修改后的目的IP
        :type TranslationIp: str
        :param Description: 修改后的描述
        :type Description: str
        """
        self.DirectConnectGatewayId = None
        self.VpcId = None
        self.OldProtocol = None
        self.OldOriginalPort = None
        self.OldOriginalIp = None
        self.OldTranslationPort = None
        self.OldTranslationIp = None
        self.Protocol = None
        self.OriginalPort = None
        self.OriginalIp = None
        self.TranslationPort = None
        self.TranslationIp = None
        self.Description = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.VpcId = params.get("VpcId")
        self.OldProtocol = params.get("OldProtocol")
        self.OldOriginalPort = params.get("OldOriginalPort")
        self.OldOriginalIp = params.get("OldOriginalIp")
        self.OldTranslationPort = params.get("OldTranslationPort")
        self.OldTranslationIp = params.get("OldTranslationIp")
        self.Protocol = params.get("Protocol")
        self.OriginalPort = params.get("OriginalPort")
        self.OriginalIp = params.get("OriginalIp")
        self.TranslationPort = params.get("TranslationPort")
        self.TranslationIp = params.get("TranslationIp")
        self.Description = params.get("Description")


class ModifyLocalDestinationIpPortTranslationNatRuleResponse(AbstractModel):
    """ModifyLocalDestinationIpPortTranslationNatRule返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyLocalIpTranslationAclRuleRequest(AbstractModel):
    """ModifyLocalIpTranslationAclRule请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID
        :type DirectConnectGatewayId: str
        :param VpcId: 字符型VPCID
        :type VpcId: str
        :param OriginalIp: 原始IP
        :type OriginalIp: str
        :param TranslationIp: 映射IP
        :type TranslationIp: str
        :param LocalIpTranslationAclRuleSet: 本端IP转换列表ACL列表
        :type LocalIpTranslationAclRuleSet: list of LocalIpTranslationAclRuleNeedId
        """
        self.DirectConnectGatewayId = None
        self.VpcId = None
        self.OriginalIp = None
        self.TranslationIp = None
        self.LocalIpTranslationAclRuleSet = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.VpcId = params.get("VpcId")
        self.OriginalIp = params.get("OriginalIp")
        self.TranslationIp = params.get("TranslationIp")
        if params.get("LocalIpTranslationAclRuleSet") is not None:
            self.LocalIpTranslationAclRuleSet = []
            for item in params.get("LocalIpTranslationAclRuleSet"):
                obj = LocalIpTranslationAclRuleNeedId()
                obj._deserialize(item)
                self.LocalIpTranslationAclRuleSet.append(obj)


class ModifyLocalIpTranslationAclRuleResponse(AbstractModel):
    """ModifyLocalIpTranslationAclRule返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyLocalIpTranslationNatRuleRequest(AbstractModel):
    """ModifyLocalIpTranslationNatRule请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID
        :type DirectConnectGatewayId: str
        :param VpcId: 字符型VPCID
        :type VpcId: str
        :param OldOriginalIp: 旧的原始IP
        :type OldOriginalIp: str
        :param OldTranslationIp: 旧的映射IP
        :type OldTranslationIp: str
        :param OriginalIp: 修改后的原始IP
        :type OriginalIp: str
        :param TranslationIp: 修改后的映射IP
        :type TranslationIp: str
        :param Description: 修改后的描述
        :type Description: str
        """
        self.DirectConnectGatewayId = None
        self.VpcId = None
        self.OldOriginalIp = None
        self.OldTranslationIp = None
        self.OriginalIp = None
        self.TranslationIp = None
        self.Description = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.VpcId = params.get("VpcId")
        self.OldOriginalIp = params.get("OldOriginalIp")
        self.OldTranslationIp = params.get("OldTranslationIp")
        self.OriginalIp = params.get("OriginalIp")
        self.TranslationIp = params.get("TranslationIp")
        self.Description = params.get("Description")


class ModifyLocalIpTranslationNatRuleResponse(AbstractModel):
    """ModifyLocalIpTranslationNatRule返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyLocalSourceIpPortTranslationAclRuleRequest(AbstractModel):
    """ModifyLocalSourceIpPortTranslationAclRule请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID
        :type DirectConnectGatewayId: str
        :param VpcId: 字符型VPCID
        :type VpcId: str
        :param TranslationIpPool: IP池
        :type TranslationIpPool: str
        :param LocalSourceIpPortTranslationAclRuleSet: 本端源IP端口转换ACL列表
        :type LocalSourceIpPortTranslationAclRuleSet: list of LocalSourceIpPortTranslationAclRuleNeedId
        """
        self.DirectConnectGatewayId = None
        self.VpcId = None
        self.TranslationIpPool = None
        self.LocalSourceIpPortTranslationAclRuleSet = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.VpcId = params.get("VpcId")
        self.TranslationIpPool = params.get("TranslationIpPool")
        if params.get("LocalSourceIpPortTranslationAclRuleSet") is not None:
            self.LocalSourceIpPortTranslationAclRuleSet = []
            for item in params.get("LocalSourceIpPortTranslationAclRuleSet"):
                obj = LocalSourceIpPortTranslationAclRuleNeedId()
                obj._deserialize(item)
                self.LocalSourceIpPortTranslationAclRuleSet.append(obj)


class ModifyLocalSourceIpPortTranslationAclRuleResponse(AbstractModel):
    """ModifyLocalSourceIpPortTranslationAclRule返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyLocalSourceIpPortTranslationNatRuleRequest(AbstractModel):
    """ModifyLocalSourceIpPortTranslationNatRule请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID
        :type DirectConnectGatewayId: str
        :param VpcId: 字符型VPCID
        :type VpcId: str
        :param OldLocalSourceIpPortTranslationNatRule: 原本端源IP端口转换
        :type OldLocalSourceIpPortTranslationNatRule: list of LocalSourceIpPortTranslationNatRule
        :param NewLocalSourceIpPortTranslationNatRule: 新本端源IP端口转换
        :type NewLocalSourceIpPortTranslationNatRule: list of LocalSourceIpPortTranslationNatRule
        """
        self.DirectConnectGatewayId = None
        self.VpcId = None
        self.OldLocalSourceIpPortTranslationNatRule = None
        self.NewLocalSourceIpPortTranslationNatRule = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.VpcId = params.get("VpcId")
        if params.get("OldLocalSourceIpPortTranslationNatRule") is not None:
            self.OldLocalSourceIpPortTranslationNatRule = []
            for item in params.get("OldLocalSourceIpPortTranslationNatRule"):
                obj = LocalSourceIpPortTranslationNatRule()
                obj._deserialize(item)
                self.OldLocalSourceIpPortTranslationNatRule.append(obj)
        if params.get("NewLocalSourceIpPortTranslationNatRule") is not None:
            self.NewLocalSourceIpPortTranslationNatRule = []
            for item in params.get("NewLocalSourceIpPortTranslationNatRule"):
                obj = LocalSourceIpPortTranslationNatRule()
                obj._deserialize(item)
                self.NewLocalSourceIpPortTranslationNatRule.append(obj)


class ModifyLocalSourceIpPortTranslationNatRuleResponse(AbstractModel):
    """ModifyLocalSourceIpPortTranslationNatRule返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyNatGatewayAttributeRequest(AbstractModel):
    """ModifyNatGatewayAttribute请求参数结构体"""

    def __init__(self):
        """
        :param NatGatewayId: NAT网关的ID，形如：`nat-df45454`。
        :type NatGatewayId: str
        :param NatGatewayName: NAT网关的名称，形如：`test_nat`。
        :type NatGatewayName: str
        :param InternetMaxBandwidthOut: NAT网关最大外网出带宽(单位:Mbps)。
        :type InternetMaxBandwidthOut: int
        """
        self.NatGatewayId = None
        self.NatGatewayName = None
        self.InternetMaxBandwidthOut = None

    def _deserialize(self, params):
        self.NatGatewayId = params.get("NatGatewayId")
        self.NatGatewayName = params.get("NatGatewayName")
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")


class ModifyNatGatewayAttributeResponse(AbstractModel):
    """ModifyNatGatewayAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyNatGatewayDestinationIpPortTranslationNatRuleRequest(AbstractModel):
    """ModifyNatGatewayDestinationIpPortTranslationNatRule请求参数结构体"""

    def __init__(self):
        """
        :param NatGatewayId: NAT网关的ID，形如：`nat-df45454`。
        :type NatGatewayId: str
        :param SourceNatRule: 源NAT网关的端口转换规则。
        :type SourceNatRule: :class:`tcecloud.vpc.v20170312.models.DestinationIpPortTranslationNatRule`
        :param DestinationNatRule: 目的NAT网关的端口转换规则。
        :type DestinationNatRule: :class:`tcecloud.vpc.v20170312.models.DestinationIpPortTranslationNatRule`
        """
        self.NatGatewayId = None
        self.SourceNatRule = None
        self.DestinationNatRule = None

    def _deserialize(self, params):
        self.NatGatewayId = params.get("NatGatewayId")
        if params.get("SourceNatRule") is not None:
            self.SourceNatRule = DestinationIpPortTranslationNatRule()
            self.SourceNatRule._deserialize(params.get("SourceNatRule"))
        if params.get("DestinationNatRule") is not None:
            self.DestinationNatRule = DestinationIpPortTranslationNatRule()
            self.DestinationNatRule._deserialize(params.get("DestinationNatRule"))


class ModifyNatGatewayDestinationIpPortTranslationNatRuleResponse(AbstractModel):
    """ModifyNatGatewayDestinationIpPortTranslationNatRule返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyNetDetectRequest(AbstractModel):
    """ModifyNetDetect请求参数结构体"""

    def __init__(self):
        """
                :param NetDetectId: 网络探测实例`ID`。形如：`netd-12345678`
                :type NetDetectId: str
                :param NetDetectName: 网络探测名称，最大长度不能超过60个字节。
                :type NetDetectName: str
                :param DetectDestinationIp: 探测目的IPv4地址数组，最多两个。
                :type DetectDestinationIp: list of str
                :param NextHopType: 下一跳类型，目前我们支持的类型有：
        VPN：VPN网关；
        DIRECTCONNECT：专线网关；
        PEERCONNECTION：对等连接；
        NAT：NAT网关；
        NORMAL_CVM：普通云服务器；
                :type NextHopType: str
                :param NextHopDestination: 下一跳目的网关，取值与“下一跳类型”相关：
        下一跳类型为VPN，取值VPN网关ID，形如：vpngw-12345678；
        下一跳类型为DIRECTCONNECT，取值专线网关ID，形如：dcg-12345678；
        下一跳类型为PEERCONNECTION，取值对等连接ID，形如：pcx-12345678；
        下一跳类型为NAT，取值Nat网关，形如：nat-12345678；
        下一跳类型为NORMAL_CVM，取值云服务器IPv4地址，形如：10.0.0.12；
                :type NextHopDestination: str
                :param NetDetectDescription: 网络探测描述。
                :type NetDetectDescription: str
        """
        self.NetDetectId = None
        self.NetDetectName = None
        self.DetectDestinationIp = None
        self.NextHopType = None
        self.NextHopDestination = None
        self.NetDetectDescription = None

    def _deserialize(self, params):
        self.NetDetectId = params.get("NetDetectId")
        self.NetDetectName = params.get("NetDetectName")
        self.DetectDestinationIp = params.get("DetectDestinationIp")
        self.NextHopType = params.get("NextHopType")
        self.NextHopDestination = params.get("NextHopDestination")
        self.NetDetectDescription = params.get("NetDetectDescription")


class ModifyNetDetectResponse(AbstractModel):
    """ModifyNetDetect返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyNetworkAclAttributeRequest(AbstractModel):
    """ModifyNetworkAclAttribute请求参数结构体"""

    def __init__(self):
        """
        :param NetworkAclId: 网络ACL实例ID。例如：acl-12345678。
        :type NetworkAclId: str
        :param NetworkAclName: 网络ACL名称，最大长度不能超过60个字节。
        :type NetworkAclName: str
        """
        self.NetworkAclId = None
        self.NetworkAclName = None

    def _deserialize(self, params):
        self.NetworkAclId = params.get("NetworkAclId")
        self.NetworkAclName = params.get("NetworkAclName")


class ModifyNetworkAclAttributeResponse(AbstractModel):
    """ModifyNetworkAclAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyNetworkAclEntriesRequest(AbstractModel):
    """ModifyNetworkAclEntries请求参数结构体"""

    def __init__(self):
        """
        :param NetworkAclId: 网络ACL实例ID。例如：acl-12345678。
        :type NetworkAclId: str
        :param NetworkAclEntrySet: 网络ACL规则集。
        :type NetworkAclEntrySet: :class:`tcecloud.vpc.v20170312.models.NetworkAclEntrySet`
        """
        self.NetworkAclId = None
        self.NetworkAclEntrySet = None

    def _deserialize(self, params):
        self.NetworkAclId = params.get("NetworkAclId")
        if params.get("NetworkAclEntrySet") is not None:
            self.NetworkAclEntrySet = NetworkAclEntrySet()
            self.NetworkAclEntrySet._deserialize(params.get("NetworkAclEntrySet"))


class ModifyNetworkAclEntriesResponse(AbstractModel):
    """ModifyNetworkAclEntries返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyNetworkInterfaceAttributeRequest(AbstractModel):
    """ModifyNetworkInterfaceAttribute请求参数结构体"""

    def __init__(self):
        """
        :param NetworkInterfaceId: 弹性网卡实例ID，例如：eni-pxir56ns。
        :type NetworkInterfaceId: str
        :param NetworkInterfaceName: 弹性网卡名称，最大长度不能超过60个字节。
        :type NetworkInterfaceName: str
        :param NetworkInterfaceDescription: 弹性网卡描述，可任意命名，但不得超过60个字符。
        :type NetworkInterfaceDescription: str
        :param SecurityGroupIds: 指定绑定的安全组，例如:['sg-1dd51d']。
        :type SecurityGroupIds: list of str
        """
        self.NetworkInterfaceId = None
        self.NetworkInterfaceName = None
        self.NetworkInterfaceDescription = None
        self.SecurityGroupIds = None

    def _deserialize(self, params):
        self.NetworkInterfaceId = params.get("NetworkInterfaceId")
        self.NetworkInterfaceName = params.get("NetworkInterfaceName")
        self.NetworkInterfaceDescription = params.get("NetworkInterfaceDescription")
        self.SecurityGroupIds = params.get("SecurityGroupIds")


class ModifyNetworkInterfaceAttributeResponse(AbstractModel):
    """ModifyNetworkInterfaceAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyNetworkInterfaceExtendIpRequest(AbstractModel):
    """ModifyNetworkInterfaceExtendIp请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: vpc唯一id
        :type VpcId: str
        :param NetworkInterfaceId: 弹性网卡唯一id
        :type NetworkInterfaceId: str
        :param Ips: 扩展ip列表
        :type Ips: list of str
        """
        self.VpcId = None
        self.NetworkInterfaceId = None
        self.Ips = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.NetworkInterfaceId = params.get("NetworkInterfaceId")
        self.Ips = params.get("Ips")


class ModifyNetworkInterfaceExtendIpResponse(AbstractModel):
    """ModifyNetworkInterfaceExtendIp返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyPeerIpTranslationNatRuleRequest(AbstractModel):
    """ModifyPeerIpTranslationNatRule请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID
        :type DirectConnectGatewayId: str
        :param VpcId: 字符型VPCID
        :type VpcId: str
        :param OldOriginalIp: 旧的原始IP
        :type OldOriginalIp: str
        :param OldTranslationIp: 旧的映射IP
        :type OldTranslationIp: str
        :param OriginalIp: 修改后的原始IP
        :type OriginalIp: str
        :param TranslationIp: 修改后的映射IP
        :type TranslationIp: str
        :param Description: 修改后的描述
        :type Description: str
        """
        self.DirectConnectGatewayId = None
        self.VpcId = None
        self.OldOriginalIp = None
        self.OldTranslationIp = None
        self.OriginalIp = None
        self.TranslationIp = None
        self.Description = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        self.VpcId = params.get("VpcId")
        self.OldOriginalIp = params.get("OldOriginalIp")
        self.OldTranslationIp = params.get("OldTranslationIp")
        self.OriginalIp = params.get("OriginalIp")
        self.TranslationIp = params.get("TranslationIp")
        self.Description = params.get("Description")


class ModifyPeerIpTranslationNatRuleResponse(AbstractModel):
    """ModifyPeerIpTranslationNatRule返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyPrivateIpAddressesAttributeRequest(AbstractModel):
    """ModifyPrivateIpAddressesAttribute请求参数结构体"""

    def __init__(self):
        """
        :param NetworkInterfaceId: 弹性网卡实例ID，例如：eni-m6dyj72l。
        :type NetworkInterfaceId: str
        :param PrivateIpAddresses: 指定的内网IP信息。
        :type PrivateIpAddresses: list of PrivateIpAddressSpecification
        """
        self.NetworkInterfaceId = None
        self.PrivateIpAddresses = None

    def _deserialize(self, params):
        self.NetworkInterfaceId = params.get("NetworkInterfaceId")
        if params.get("PrivateIpAddresses") is not None:
            self.PrivateIpAddresses = []
            for item in params.get("PrivateIpAddresses"):
                obj = PrivateIpAddressSpecification()
                obj._deserialize(item)
                self.PrivateIpAddresses.append(obj)


class ModifyPrivateIpAddressesAttributeResponse(AbstractModel):
    """ModifyPrivateIpAddressesAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyRouteTableAttributeRequest(AbstractModel):
    """ModifyRouteTableAttribute请求参数结构体"""

    def __init__(self):
        """
        :param RouteTableId: 路由表实例ID，例如：rtb-azd4dt1c。
        :type RouteTableId: str
        :param RouteTableName: 路由表名称。
        :type RouteTableName: str
        """
        self.RouteTableId = None
        self.RouteTableName = None

    def _deserialize(self, params):
        self.RouteTableId = params.get("RouteTableId")
        self.RouteTableName = params.get("RouteTableName")


class ModifyRouteTableAttributeResponse(AbstractModel):
    """ModifyRouteTableAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifySecurityGroupAttributeRequest(AbstractModel):
    """ModifySecurityGroupAttribute请求参数结构体"""

    def __init__(self):
        """
        :param SecurityGroupId: 安全组实例ID，例如sg-33ocnj9n，可通过DescribeSecurityGroups获取。
        :type SecurityGroupId: str
        :param GroupName: 安全组名称，可任意命名，但不得超过60个字符。
        :type GroupName: str
        :param GroupDescription: 安全组备注，最多100个字符。
        :type GroupDescription: str
        """
        self.SecurityGroupId = None
        self.GroupName = None
        self.GroupDescription = None

    def _deserialize(self, params):
        self.SecurityGroupId = params.get("SecurityGroupId")
        self.GroupName = params.get("GroupName")
        self.GroupDescription = params.get("GroupDescription")


class ModifySecurityGroupAttributeResponse(AbstractModel):
    """ModifySecurityGroupAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifySecurityGroupPoliciesRequest(AbstractModel):
    """ModifySecurityGroupPolicies请求参数结构体"""

    def __init__(self):
        """
        :param SecurityGroupId: 安全组实例ID，例如sg-33ocnj9n，可通过DescribeSecurityGroups获取。
        :type SecurityGroupId: str
        :param SecurityGroupPolicySet: 安全组规则集合。 SecurityGroupPolicySet对象必须同时指定新的出（Egress）入（Ingress）站规则。 SecurityGroupPolicy对象不支持自定义索引（PolicyIndex）。
        :type SecurityGroupPolicySet: :class:`tcecloud.vpc.v20170312.models.SecurityGroupPolicySet`
        :param SortPolicys: 排序安全组标识。值为True时，支持安全组排序；SortPolicys不存在或SortPolicys为False时，为修改安全组规则。
        :type SortPolicys: bool
        """
        self.SecurityGroupId = None
        self.SecurityGroupPolicySet = None
        self.SortPolicys = None

    def _deserialize(self, params):
        self.SecurityGroupId = params.get("SecurityGroupId")
        if params.get("SecurityGroupPolicySet") is not None:
            self.SecurityGroupPolicySet = SecurityGroupPolicySet()
            self.SecurityGroupPolicySet._deserialize(params.get("SecurityGroupPolicySet"))
        self.SortPolicys = params.get("SortPolicys")


class ModifySecurityGroupPoliciesResponse(AbstractModel):
    """ModifySecurityGroupPolicies返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyServiceTemplateAttributeRequest(AbstractModel):
    """ModifyServiceTemplateAttribute请求参数结构体"""

    def __init__(self):
        """
        :param ServiceTemplateId: 协议端口模板实例ID，例如：ppm-529nwwj8。
        :type ServiceTemplateId: str
        :param ServiceTemplateName: 协议端口模板名称。
        :type ServiceTemplateName: str
        :param Services: 支持单个端口、多个端口、连续端口及所有端口，协议支持：TCP、UDP、ICMP、GRE 协议。
        :type Services: list of str
        """
        self.ServiceTemplateId = None
        self.ServiceTemplateName = None
        self.Services = None

    def _deserialize(self, params):
        self.ServiceTemplateId = params.get("ServiceTemplateId")
        self.ServiceTemplateName = params.get("ServiceTemplateName")
        self.Services = params.get("Services")


class ModifyServiceTemplateAttributeResponse(AbstractModel):
    """ModifyServiceTemplateAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyServiceTemplateGroupAttributeRequest(AbstractModel):
    """ModifyServiceTemplateGroupAttribute请求参数结构体"""

    def __init__(self):
        """
        :param ServiceTemplateGroupId: 协议端口模板集合实例ID，例如：ppmg-ei8hfd9a。
        :type ServiceTemplateGroupId: str
        :param ServiceTemplateGroupName: 协议端口模板集合名称。
        :type ServiceTemplateGroupName: str
        :param ServiceTemplateIds: 协议端口模板实例ID，例如：ppm-4dw6agho。
        :type ServiceTemplateIds: list of str
        """
        self.ServiceTemplateGroupId = None
        self.ServiceTemplateGroupName = None
        self.ServiceTemplateIds = None

    def _deserialize(self, params):
        self.ServiceTemplateGroupId = params.get("ServiceTemplateGroupId")
        self.ServiceTemplateGroupName = params.get("ServiceTemplateGroupName")
        self.ServiceTemplateIds = params.get("ServiceTemplateIds")


class ModifyServiceTemplateGroupAttributeResponse(AbstractModel):
    """ModifyServiceTemplateGroupAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifySubnetAttributeRequest(AbstractModel):
    """ModifySubnetAttribute请求参数结构体"""

    def __init__(self):
        """
        :param SubnetId: 子网实例ID。形如：subnet-pxir56ns。
        :type SubnetId: str
        :param SubnetName: 子网名称，最大长度不能超过60个字节。
        :type SubnetName: str
        :param EnableBroadcast: 子网是否开启广播。
        :type EnableBroadcast: str
        """
        self.SubnetId = None
        self.SubnetName = None
        self.EnableBroadcast = None

    def _deserialize(self, params):
        self.SubnetId = params.get("SubnetId")
        self.SubnetName = params.get("SubnetName")
        self.EnableBroadcast = params.get("EnableBroadcast")


class ModifySubnetAttributeResponse(AbstractModel):
    """ModifySubnetAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyTrafficMirrorAttributeRequest(AbstractModel):
    """ModifyTrafficMirrorAttribute请求参数结构体"""

    def __init__(self):
        """
        :param TrafficMirrorId: 流量镜像实例ID
        :type TrafficMirrorId: str
        :param TrafficMirrorName: 流量镜像实例名称
        :type TrafficMirrorName: str
        :param TrafficMirrorDescription: 流量镜像实例描述信息
        :type TrafficMirrorDescription: str
        """
        self.TrafficMirrorId = None
        self.TrafficMirrorName = None
        self.TrafficMirrorDescription = None

    def _deserialize(self, params):
        self.TrafficMirrorId = params.get("TrafficMirrorId")
        self.TrafficMirrorName = params.get("TrafficMirrorName")
        self.TrafficMirrorDescription = params.get("TrafficMirrorDescription")


class ModifyTrafficMirrorAttributeResponse(AbstractModel):
    """ModifyTrafficMirrorAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyTrafficPackageAttributeRequest(AbstractModel):
    """ModifyTrafficPackageAttribute请求参数结构体"""

    def __init__(self):
        """
        :param TrafficPackageId: 共享流量包唯一标识ID
        :type TrafficPackageId: str
        :param TrafficPackageName: 共享流量包名称
        :type TrafficPackageName: str
        """
        self.TrafficPackageId = None
        self.TrafficPackageName = None

    def _deserialize(self, params):
        self.TrafficPackageId = params.get("TrafficPackageId")
        self.TrafficPackageName = params.get("TrafficPackageName")


class ModifyTrafficPackageAttributeResponse(AbstractModel):
    """ModifyTrafficPackageAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyVpcAttributeRequest(AbstractModel):
    """ModifyVpcAttribute请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: VPC实例ID。形如：vpc-f49l6u0z。每次请求的实例的上限为100。参数不支持同时指定VpcIds和Filters。
        :type VpcId: str
        :param VpcName: 私有网络名称，可任意命名，但不得超过60个字符。
        :type VpcName: str
        :param EnableMulticast: 是否开启组播。true: 开启, false: 关闭。
        :type EnableMulticast: str
        :param DnsServers: DNS地址，最多支持4个，第1个默认为主，其余为备
        :type DnsServers: list of str
        :param DomainName: 域名
        :type DomainName: str
        """
        self.VpcId = None
        self.VpcName = None
        self.EnableMulticast = None
        self.DnsServers = None
        self.DomainName = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.VpcName = params.get("VpcName")
        self.EnableMulticast = params.get("EnableMulticast")
        self.DnsServers = params.get("DnsServers")
        self.DomainName = params.get("DomainName")


class ModifyVpcAttributeResponse(AbstractModel):
    """ModifyVpcAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyVpcExtendCidrRequest(AbstractModel):
    """ModifyVpcExtendCidr请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: vpc唯一id
        :type VpcId: str
        :param CidrBlock: 扩展CIDR的cidr
        :type CidrBlock: list of str
        """
        self.VpcId = None
        self.CidrBlock = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.CidrBlock = params.get("CidrBlock")


class ModifyVpcExtendCidrResponse(AbstractModel):
    """ModifyVpcExtendCidr返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyVpnConnectionAttributeRequest(AbstractModel):
    """ModifyVpnConnectionAttribute请求参数结构体"""

    def __init__(self):
        """
        :param VpnConnectionId: VPN通道实例ID。形如：vpnx-f49l6u0z。
        :type VpnConnectionId: str
        :param VpnConnectionName: VPN通道名称，可任意命名，但不得超过60个字符。
        :type VpnConnectionName: str
        :param PreShareKey: 预共享密钥。
        :type PreShareKey: str
        :param SecurityPolicyDatabases: SPD策略组，例如：{"10.0.0.5/24":["172.123.10.5/16"]}，10.0.0.5/24是vpc内网段172.123.10.5/16是IDC网段。用户指定VPC内哪些网段可以和您IDC中哪些网段通信。
        :type SecurityPolicyDatabases: list of SecurityPolicyDatabase
        :param IKEOptionsSpecification: IKE配置（Internet Key Exchange，因特网密钥交换），IKE具有一套自我保护机制，用户配置网络安全协议。
        :type IKEOptionsSpecification: :class:`tcecloud.vpc.v20170312.models.IKEOptionsSpecification`
        :param IPSECOptionsSpecification: IPSec配置，Tce提供IPSec安全会话设置。
        :type IPSECOptionsSpecification: :class:`tcecloud.vpc.v20170312.models.IPSECOptionsSpecification`
        """
        self.VpnConnectionId = None
        self.VpnConnectionName = None
        self.PreShareKey = None
        self.SecurityPolicyDatabases = None
        self.IKEOptionsSpecification = None
        self.IPSECOptionsSpecification = None

    def _deserialize(self, params):
        self.VpnConnectionId = params.get("VpnConnectionId")
        self.VpnConnectionName = params.get("VpnConnectionName")
        self.PreShareKey = params.get("PreShareKey")
        if params.get("SecurityPolicyDatabases") is not None:
            self.SecurityPolicyDatabases = []
            for item in params.get("SecurityPolicyDatabases"):
                obj = SecurityPolicyDatabase()
                obj._deserialize(item)
                self.SecurityPolicyDatabases.append(obj)
        if params.get("IKEOptionsSpecification") is not None:
            self.IKEOptionsSpecification = IKEOptionsSpecification()
            self.IKEOptionsSpecification._deserialize(params.get("IKEOptionsSpecification"))
        if params.get("IPSECOptionsSpecification") is not None:
            self.IPSECOptionsSpecification = IPSECOptionsSpecification()
            self.IPSECOptionsSpecification._deserialize(params.get("IPSECOptionsSpecification"))


class ModifyVpnConnectionAttributeResponse(AbstractModel):
    """ModifyVpnConnectionAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyVpnGatewayAttributeRequest(AbstractModel):
    """ModifyVpnGatewayAttribute请求参数结构体"""

    def __init__(self):
        """
        :param VpnGatewayId: VPN网关实例ID。
        :type VpnGatewayId: str
        :param VpnGatewayName: VPN网关名称，最大长度不能超过60个字节。
        :type VpnGatewayName: str
        :param InstanceChargeType: VPN网关计费模式，目前只支持预付费（即包年包月）到后付费（即按量计费）的转换。即参数只支持：POSTPAID_BY_HOUR。
        :type InstanceChargeType: str
        """
        self.VpnGatewayId = None
        self.VpnGatewayName = None
        self.InstanceChargeType = None

    def _deserialize(self, params):
        self.VpnGatewayId = params.get("VpnGatewayId")
        self.VpnGatewayName = params.get("VpnGatewayName")
        self.InstanceChargeType = params.get("InstanceChargeType")


class ModifyVpnGatewayAttributeResponse(AbstractModel):
    """ModifyVpnGatewayAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyVpnGatewayCcnRoutesRequest(AbstractModel):
    """ModifyVpnGatewayCcnRoutes请求参数结构体"""

    def __init__(self):
        """
        :param VpnGatewayId: VPN网关实例ID
        :type VpnGatewayId: str
        :param Routes: 云联网路由（IDC网段）列表
        :type Routes: list of VpngwCcnRoutes
        """
        self.VpnGatewayId = None
        self.Routes = None

    def _deserialize(self, params):
        self.VpnGatewayId = params.get("VpnGatewayId")
        if params.get("Routes") is not None:
            self.Routes = []
            for item in params.get("Routes"):
                obj = VpngwCcnRoutes()
                obj._deserialize(item)
                self.Routes.append(obj)


class ModifyVpnGatewayCcnRoutesResponse(AbstractModel):
    """ModifyVpnGatewayCcnRoutes返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class NatGateway(AbstractModel):
    """NAT网关对象。"""

    def __init__(self):
        """
                :param NatGatewayId: NAT网关的ID。
                :type NatGatewayId: str
                :param NatGatewayName: NAT网关的名称。
                :type NatGatewayName: str
                :param CreatedTime: NAT网关创建的时间。
                :type CreatedTime: str
                :param State: NAT网关的状态。
         'PENDING'：生产中，'DELETING'：删除中，'AVAILABLE'：运行中，'UPDATING'：升级中，
        ‘FAILED’：失败。
                :type State: str
                :param InternetMaxBandwidthOut: 网关最大外网出带宽(单位:Mbps)。
                :type InternetMaxBandwidthOut: int
                :param MaxConcurrentConnection: 网关并发连接上限。
                :type MaxConcurrentConnection: int
                :param PublicIpAddressSet: 绑定NAT网关的公网IP对象数组。
                :type PublicIpAddressSet: list of NatGatewayAddress
                :param NetworkState: NAT网关网络状态。“AVAILABLE”:运行中, “UNAVAILABLE”:不可用, “INSUFFICIENT”:欠费停服。
                :type NetworkState: str
                :param DestinationIpPortTranslationNatRuleSet: NAT网关的端口转发规则。
                :type DestinationIpPortTranslationNatRuleSet: list of DestinationIpPortTranslationNatRule
                :param VpcId: VPC实例ID。
                :type VpcId: str
                :param Zone: NAT网关所在的可用区。
                :type Zone: str
        """
        self.NatGatewayId = None
        self.NatGatewayName = None
        self.CreatedTime = None
        self.State = None
        self.InternetMaxBandwidthOut = None
        self.MaxConcurrentConnection = None
        self.PublicIpAddressSet = None
        self.NetworkState = None
        self.DestinationIpPortTranslationNatRuleSet = None
        self.VpcId = None
        self.Zone = None

    def _deserialize(self, params):
        self.NatGatewayId = params.get("NatGatewayId")
        self.NatGatewayName = params.get("NatGatewayName")
        self.CreatedTime = params.get("CreatedTime")
        self.State = params.get("State")
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        self.MaxConcurrentConnection = params.get("MaxConcurrentConnection")
        if params.get("PublicIpAddressSet") is not None:
            self.PublicIpAddressSet = []
            for item in params.get("PublicIpAddressSet"):
                obj = NatGatewayAddress()
                obj._deserialize(item)
                self.PublicIpAddressSet.append(obj)
        self.NetworkState = params.get("NetworkState")
        if params.get("DestinationIpPortTranslationNatRuleSet") is not None:
            self.DestinationIpPortTranslationNatRuleSet = []
            for item in params.get("DestinationIpPortTranslationNatRuleSet"):
                obj = DestinationIpPortTranslationNatRule()
                obj._deserialize(item)
                self.DestinationIpPortTranslationNatRuleSet.append(obj)
        self.VpcId = params.get("VpcId")
        self.Zone = params.get("Zone")


class NatGatewayAddress(AbstractModel):
    """NAT网关绑定的弹性IP"""

    def __init__(self):
        """
        :param AddressId: 弹性公网IP（EIP）的唯一 ID，形如：`eip-11112222`。
        :type AddressId: str
        :param PublicIpAddress: 外网IP地址，形如：`123.121.34.33`。
        :type PublicIpAddress: str
        :param IsBlocked: 资源封堵状态。true表示弹性ip处于封堵状态，false表示弹性ip处于未封堵状态。
        :type IsBlocked: bool
        """
        self.AddressId = None
        self.PublicIpAddress = None
        self.IsBlocked = None

    def _deserialize(self, params):
        self.AddressId = params.get("AddressId")
        self.PublicIpAddress = params.get("PublicIpAddress")
        self.IsBlocked = params.get("IsBlocked")


class NatGatewayDestinationIpPortTranslationNatRule(AbstractModel):
    """NAT网关的端口转发规则"""

    def __init__(self):
        """
                :param IpProtocol: 网络协议，可选值：`TCP`、`UDP`。
                :type IpProtocol: str
                :param PublicIpAddress: 弹性IP。
                :type PublicIpAddress: str
                :param PublicPort: 公网端口。
                :type PublicPort: int
                :param PrivateIpAddress: 内网地址。
                :type PrivateIpAddress: str
                :param PrivatePort: 内网端口。
                :type PrivatePort: int
                :param Description: NAT网关转发规则描述。
                :type Description: str
                :param NatGatewayId: NAT网关的ID。
        注意：此字段可能返回 null，表示取不到有效值。
                :type NatGatewayId: str
                :param VpcId: 私有网络VPC的ID。
        注意：此字段可能返回 null，表示取不到有效值。
                :type VpcId: str
                :param CreatedTime: NAT网关转发规则创建时间。
        注意：此字段可能返回 null，表示取不到有效值。
                :type CreatedTime: str
        """
        self.IpProtocol = None
        self.PublicIpAddress = None
        self.PublicPort = None
        self.PrivateIpAddress = None
        self.PrivatePort = None
        self.Description = None
        self.NatGatewayId = None
        self.VpcId = None
        self.CreatedTime = None

    def _deserialize(self, params):
        self.IpProtocol = params.get("IpProtocol")
        self.PublicIpAddress = params.get("PublicIpAddress")
        self.PublicPort = params.get("PublicPort")
        self.PrivateIpAddress = params.get("PrivateIpAddress")
        self.PrivatePort = params.get("PrivatePort")
        self.Description = params.get("Description")
        self.NatGatewayId = params.get("NatGatewayId")
        self.VpcId = params.get("VpcId")
        self.CreatedTime = params.get("CreatedTime")


class NatGatewayQuota(AbstractModel):
    """NAT网关配额"""

    def __init__(self):
        """
        :param BandwidthQuota: NAT网关带宽配额
        :type BandwidthQuota: int
        """
        self.BandwidthQuota = None

    def _deserialize(self, params):
        self.BandwidthQuota = params.get("BandwidthQuota")


class NetDetect(AbstractModel):
    """网络探测对象。"""

    def __init__(self):
        """
                :param VpcId: `VPC`实例`ID`。形如：`vpc-12345678`
                :type VpcId: str
                :param VpcName: `VPC`实例名称。
                :type VpcName: str
                :param SubnetId: 子网实例ID。形如：subnet-12345678。
                :type SubnetId: str
                :param SubnetName: 子网实例名称。
                :type SubnetName: str
                :param NetDetectId: 网络探测实例ID。形如：netd-12345678。
                :type NetDetectId: str
                :param NetDetectName: 网络探测名称，最大长度不能超过60个字节。
                :type NetDetectName: str
                :param DetectDestinationIp: 探测目的IPv4地址数组，最多两个。
                :type DetectDestinationIp: list of str
                :param DetectSourceIp: 系统自动分配的探测源IPv4数组。长度为2。
                :type DetectSourceIp: list of str
                :param NextHopType: 下一跳类型，目前我们支持的类型有：
        VPN：VPN网关；
        DIRECTCONNECT：专线网关；
        PEERCONNECTION：对等连接；
        NAT：NAT网关；
        NORMAL_CVM：普通云服务器；
                :type NextHopType: str
                :param NextHopDestination: 下一跳目的网关，取值与“下一跳类型”相关：
        下一跳类型为VPN，取值VPN网关ID，形如：vpngw-12345678；
        下一跳类型为DIRECTCONNECT，取值专线网关ID，形如：dcg-12345678；
        下一跳类型为PEERCONNECTION，取值对等连接ID，形如：pcx-12345678；
        下一跳类型为NAT，取值Nat网关，形如：nat-12345678；
        下一跳类型为NORMAL_CVM，取值云服务器IPv4地址，形如：10.0.0.12；
                :type NextHopDestination: str
                :param NextHopName: 下一跳网关名称。
        注意：此字段可能返回 null，表示取不到有效值。
                :type NextHopName: str
                :param NetDetectDescription: 网络探测描述。
        注意：此字段可能返回 null，表示取不到有效值。
                :type NetDetectDescription: str
                :param CreateTime: 创建时间。
        注意：此字段可能返回 null，表示取不到有效值。
                :type CreateTime: str
        """
        self.VpcId = None
        self.VpcName = None
        self.SubnetId = None
        self.SubnetName = None
        self.NetDetectId = None
        self.NetDetectName = None
        self.DetectDestinationIp = None
        self.DetectSourceIp = None
        self.NextHopType = None
        self.NextHopDestination = None
        self.NextHopName = None
        self.NetDetectDescription = None
        self.CreateTime = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.VpcName = params.get("VpcName")
        self.SubnetId = params.get("SubnetId")
        self.SubnetName = params.get("SubnetName")
        self.NetDetectId = params.get("NetDetectId")
        self.NetDetectName = params.get("NetDetectName")
        self.DetectDestinationIp = params.get("DetectDestinationIp")
        self.DetectSourceIp = params.get("DetectSourceIp")
        self.NextHopType = params.get("NextHopType")
        self.NextHopDestination = params.get("NextHopDestination")
        self.NextHopName = params.get("NextHopName")
        self.NetDetectDescription = params.get("NetDetectDescription")
        self.CreateTime = params.get("CreateTime")


class NetDetectIpState(AbstractModel):
    """网络探测目的IP的验证结果。"""

    def __init__(self):
        """
                :param DetectDestinationIp: 探测目的IPv4地址。
                :type DetectDestinationIp: str
                :param State: 探测结果。
        0：成功；
        -1：查询不到路由丢包；
        -2：外出ACL丢包；
        -3：IN ACL丢包；
        -4：其他错误；
                :type State: int
                :param Delay: 时延，单位毫秒
                :type Delay: int
                :param PacketLossRate: 丢包率
                :type PacketLossRate: int
        """
        self.DetectDestinationIp = None
        self.State = None
        self.Delay = None
        self.PacketLossRate = None

    def _deserialize(self, params):
        self.DetectDestinationIp = params.get("DetectDestinationIp")
        self.State = params.get("State")
        self.Delay = params.get("Delay")
        self.PacketLossRate = params.get("PacketLossRate")


class NetDetectState(AbstractModel):
    """网络探测验证结果。"""

    def __init__(self):
        """
        :param NetDetectId: 网络探测实例ID。形如：netd-12345678。
        :type NetDetectId: str
        :param NetDetectIpStateSet: 网络探测目的IP验证结果对象数组。
        :type NetDetectIpStateSet: list of NetDetectIpState
        """
        self.NetDetectId = None
        self.NetDetectIpStateSet = None

    def _deserialize(self, params):
        self.NetDetectId = params.get("NetDetectId")
        if params.get("NetDetectIpStateSet") is not None:
            self.NetDetectIpStateSet = []
            for item in params.get("NetDetectIpStateSet"):
                obj = NetDetectIpState()
                obj._deserialize(item)
                self.NetDetectIpStateSet.append(obj)


class NetworkAcl(AbstractModel):
    """网络ACL"""

    def __init__(self):
        """
        :param VpcId: `VPC`实例`ID`。
        :type VpcId: str
        :param NetworkAclId: 网络ACL实例`ID`。
        :type NetworkAclId: str
        :param NetworkAclName: 网络ACL名称，最大长度为60。
        :type NetworkAclName: str
        :param CreatedTime: 创建时间。
        :type CreatedTime: str
        :param SubnetSet: 网络ACL关联的子网数组。
        :type SubnetSet: list of Subnet
        :param IngressEntries: 网络ACl入站规则。
        :type IngressEntries: list of NetworkAclEntry
        :param EgressEntries: 网络ACL出站规则。
        :type EgressEntries: list of NetworkAclEntry
        """
        self.VpcId = None
        self.NetworkAclId = None
        self.NetworkAclName = None
        self.CreatedTime = None
        self.SubnetSet = None
        self.IngressEntries = None
        self.EgressEntries = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.NetworkAclId = params.get("NetworkAclId")
        self.NetworkAclName = params.get("NetworkAclName")
        self.CreatedTime = params.get("CreatedTime")
        if params.get("SubnetSet") is not None:
            self.SubnetSet = []
            for item in params.get("SubnetSet"):
                obj = Subnet()
                obj._deserialize(item)
                self.SubnetSet.append(obj)
        if params.get("IngressEntries") is not None:
            self.IngressEntries = []
            for item in params.get("IngressEntries"):
                obj = NetworkAclEntry()
                obj._deserialize(item)
                self.IngressEntries.append(obj)
        if params.get("EgressEntries") is not None:
            self.EgressEntries = []
            for item in params.get("EgressEntries"):
                obj = NetworkAclEntry()
                obj._deserialize(item)
                self.EgressEntries.append(obj)


class NetworkAclEntry(AbstractModel):
    """网络ACL规则。"""

    def __init__(self):
        """
        :param ModifyTime: 修改时间。
        :type ModifyTime: str
        :param Protocol: 协议, 取值: TCP,UDP, ICMP, ALL。
        :type Protocol: str
        :param Port: 端口(all, 单个port,  range)。当Protocol为ALL或ICMP时，不能指定Port。
        :type Port: str
        :param CidrBlock: 网段或IP(互斥)。
        :type CidrBlock: str
        :param Ipv6CidrBlock: 网段或IPv6(互斥)。
        :type Ipv6CidrBlock: str
        :param Action: ACCEPT 或 DROP。
        :type Action: str
        :param Description: 规则描述，最大长度100。
        :type Description: str
        """
        self.ModifyTime = None
        self.Protocol = None
        self.Port = None
        self.CidrBlock = None
        self.Ipv6CidrBlock = None
        self.Action = None
        self.Description = None

    def _deserialize(self, params):
        self.ModifyTime = params.get("ModifyTime")
        self.Protocol = params.get("Protocol")
        self.Port = params.get("Port")
        self.CidrBlock = params.get("CidrBlock")
        self.Ipv6CidrBlock = params.get("Ipv6CidrBlock")
        self.Action = params.get("Action")
        self.Description = params.get("Description")


class NetworkAclEntrySet(AbstractModel):
    """网络ACL规则集合"""

    def __init__(self):
        """
        :param Ingress: 入站规则。
        :type Ingress: list of NetworkAclEntry
        :param Egress: 出站规则。
        :type Egress: list of NetworkAclEntry
        """
        self.Ingress = None
        self.Egress = None

    def _deserialize(self, params):
        if params.get("Ingress") is not None:
            self.Ingress = []
            for item in params.get("Ingress"):
                obj = NetworkAclEntry()
                obj._deserialize(item)
                self.Ingress.append(obj)
        if params.get("Egress") is not None:
            self.Egress = []
            for item in params.get("Egress"):
                obj = NetworkAclEntry()
                obj._deserialize(item)
                self.Egress.append(obj)


class NetworkInterface(AbstractModel):
    """弹性网卡"""

    def __init__(self):
        """
                :param NetworkInterfaceId: 弹性网卡实例ID，例如：eni-f1xjkw1b。
                :type NetworkInterfaceId: str
                :param NetworkInterfaceName: 弹性网卡名称。
                :type NetworkInterfaceName: str
                :param NetworkInterfaceDescription: 弹性网卡描述。
                :type NetworkInterfaceDescription: str
                :param SubnetId: 子网实例ID。
                :type SubnetId: str
                :param VpcId: VPC实例ID。
                :type VpcId: str
                :param GroupSet: 绑定的安全组。
                :type GroupSet: list of str
                :param Primary: 是否是主网卡。
                :type Primary: bool
                :param MacAddress: MAC地址。
                :type MacAddress: str
                :param State: 弹性网卡状态：
        <li>`PENDING`：创建中</li>
        <li>`AVAILABLE`：可用的</li>
        <li>`ATTACHING`：绑定中</li>
        <li>`DETACHING`：解绑中</li>
        <li>`DELETING`：删除中</li>
                :type State: str
                :param PrivateIpAddressSet: 内网IP信息。
                :type PrivateIpAddressSet: list of PrivateIpAddressSpecification
                :param Attachment: 绑定的云服务器对象。
        注意：此字段可能返回 null，表示取不到有效值。
                :type Attachment: :class:`tcecloud.vpc.v20170312.models.NetworkInterfaceAttachment`
                :param Zone: 可用区。
                :type Zone: str
                :param CreatedTime: 创建时间。
                :type CreatedTime: str
                :param Ipv6AddressSet: `IPv6`地址列表。
                :type Ipv6AddressSet: list of Ipv6Address
                :param TagSet: 标签键值对。
                :type TagSet: list of Tag
                :param EniType: 网卡类型。0 - 弹性网卡；1 - evm弹性网卡。
                :type EniType: int
        """
        self.NetworkInterfaceId = None
        self.NetworkInterfaceName = None
        self.NetworkInterfaceDescription = None
        self.SubnetId = None
        self.VpcId = None
        self.GroupSet = None
        self.Primary = None
        self.MacAddress = None
        self.State = None
        self.PrivateIpAddressSet = None
        self.Attachment = None
        self.Zone = None
        self.CreatedTime = None
        self.Ipv6AddressSet = None
        self.TagSet = None
        self.EniType = None

    def _deserialize(self, params):
        self.NetworkInterfaceId = params.get("NetworkInterfaceId")
        self.NetworkInterfaceName = params.get("NetworkInterfaceName")
        self.NetworkInterfaceDescription = params.get("NetworkInterfaceDescription")
        self.SubnetId = params.get("SubnetId")
        self.VpcId = params.get("VpcId")
        self.GroupSet = params.get("GroupSet")
        self.Primary = params.get("Primary")
        self.MacAddress = params.get("MacAddress")
        self.State = params.get("State")
        if params.get("PrivateIpAddressSet") is not None:
            self.PrivateIpAddressSet = []
            for item in params.get("PrivateIpAddressSet"):
                obj = PrivateIpAddressSpecification()
                obj._deserialize(item)
                self.PrivateIpAddressSet.append(obj)
        if params.get("Attachment") is not None:
            self.Attachment = NetworkInterfaceAttachment()
            self.Attachment._deserialize(params.get("Attachment"))
        self.Zone = params.get("Zone")
        self.CreatedTime = params.get("CreatedTime")
        if params.get("Ipv6AddressSet") is not None:
            self.Ipv6AddressSet = []
            for item in params.get("Ipv6AddressSet"):
                obj = Ipv6Address()
                obj._deserialize(item)
                self.Ipv6AddressSet.append(obj)
        if params.get("TagSet") is not None:
            self.TagSet = []
            for item in params.get("TagSet"):
                obj = Tag()
                obj._deserialize(item)
                self.TagSet.append(obj)
        self.EniType = params.get("EniType")


class NetworkInterfaceAttachment(AbstractModel):
    """弹性网卡绑定关系"""

    def __init__(self):
        """
        :param InstanceId: 云主机实例ID。
        :type InstanceId: str
        :param DeviceIndex: 网卡在云主机实例内的序号。
        :type DeviceIndex: int
        :param InstanceAccountId: 云主机所有者账户信息。
        :type InstanceAccountId: str
        :param AttachTime: 绑定时间。
        :type AttachTime: str
        """
        self.InstanceId = None
        self.DeviceIndex = None
        self.InstanceAccountId = None
        self.AttachTime = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.DeviceIndex = params.get("DeviceIndex")
        self.InstanceAccountId = params.get("InstanceAccountId")
        self.AttachTime = params.get("AttachTime")


class NetworkInterfaceExtendIp(AbstractModel):
    """弹性网卡扩展ip段"""

    def __init__(self):
        """
        :param VpcId: Vpc整型id
        :type VpcId: int
        :param UniqVpcId: Vpc唯一id
        :type UniqVpcId: str
        :param EniId: 弹性网卡整型id
        :type EniId: int
        :param UniqEniId: 弹性网卡唯一id
        :type UniqEniId: str
        :param Ip: 扩展ip
        :type Ip: str
        """
        self.VpcId = None
        self.UniqVpcId = None
        self.EniId = None
        self.UniqEniId = None
        self.Ip = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.UniqVpcId = params.get("UniqVpcId")
        self.EniId = params.get("EniId")
        self.UniqEniId = params.get("UniqEniId")
        self.Ip = params.get("Ip")


class Price(AbstractModel):
    """价格"""

    def __init__(self):
        """
        :param InstancePrice: 实例价格。
        :type InstancePrice: :class:`tcecloud.vpc.v20170312.models.ItemPrice`
        :param BandwidthPrice: 网络价格。
        :type BandwidthPrice: :class:`tcecloud.vpc.v20170312.models.ItemPrice`
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


class PrivateIp6AddressesRequest(AbstractModel):
    """PrivateIp6Addresses请求参数结构体"""

    def __init__(self):
        """
        :param Ip6Addresses: IPV6地址。Ip6Addresses和Ip6AddressIds必须且只能传一个
        :type Ip6Addresses: list of str
        :param Ip6AddressIds: IPV6地址对应的唯一ID，形如eip-xxxxxxxx。Ip6Addresses和Ip6AddressIds必须且只能传一个。
        :type Ip6AddressIds: list of str
        """
        self.Ip6Addresses = None
        self.Ip6AddressIds = None

    def _deserialize(self, params):
        self.Ip6Addresses = params.get("Ip6Addresses")
        self.Ip6AddressIds = params.get("Ip6AddressIds")


class PrivateIp6AddressesResponse(AbstractModel):
    """PrivateIp6Addresses返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class PrivateIpAddressSpecification(AbstractModel):
    """内网IP信息"""

    def __init__(self):
        """
                :param PrivateIpAddress: 内网IP地址。
                :type PrivateIpAddress: str
                :param Primary: 是否是主IP。
                :type Primary: bool
                :param PublicIpAddress: 公网IP地址。
                :type PublicIpAddress: str
                :param AddressId: EIP实例ID，例如：eip-11112222。
                :type AddressId: str
                :param Description: 内网IP描述信息。
                :type Description: str
                :param IsWanIpBlocked: 公网IP是否被封堵。
                :type IsWanIpBlocked: bool
                :param State: IP状态：
        PENDING：生产中
        MIGRATING：迁移中
        DELETING：删除中
        AVAILABLE：可用的
                :type State: str
        """
        self.PrivateIpAddress = None
        self.Primary = None
        self.PublicIpAddress = None
        self.AddressId = None
        self.Description = None
        self.IsWanIpBlocked = None
        self.State = None

    def _deserialize(self, params):
        self.PrivateIpAddress = params.get("PrivateIpAddress")
        self.Primary = params.get("Primary")
        self.PublicIpAddress = params.get("PublicIpAddress")
        self.AddressId = params.get("AddressId")
        self.Description = params.get("Description")
        self.IsWanIpBlocked = params.get("IsWanIpBlocked")
        self.State = params.get("State")


class PublicIp6AddressesRequest(AbstractModel):
    """PublicIp6Addresses请求参数结构体"""

    def __init__(self):
        """
        :param Ip6Addresses: 需要开通internet访问能力的IPV6地址
        :type Ip6Addresses: list of str
        :param InternetMaxBandwidthOut: 带宽，单位Mbps。默认是1Mbps
        :type InternetMaxBandwidthOut: int
        :param InternetChargeType: 网络计费模式。IPV6当前支持"TRAFFIC_POSTPAID_BY_HOUR"，默认是"TRAFFIC_POSTPAID_BY_HOUR"。
        :type InternetChargeType: str
        """
        self.Ip6Addresses = None
        self.InternetMaxBandwidthOut = None
        self.InternetChargeType = None

    def _deserialize(self, params):
        self.Ip6Addresses = params.get("Ip6Addresses")
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        self.InternetChargeType = params.get("InternetChargeType")


class PublicIp6AddressesResponse(AbstractModel):
    """PublicIp6Addresses返回参数结构体"""

    def __init__(self):
        """
        :param AddressSet: 申请到的 IPV6 的唯一 ID 列表。
        :type AddressSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AddressSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.AddressSet = params.get("AddressSet")
        self.RequestId = params.get("RequestId")


class QueryTaskRequest(AbstractModel):
    """QueryTask请求参数结构体"""

    def __init__(self):
        """
        :param TaskId: 异步任务请求返回的RequestId。
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
        :param Output: 异步任务执行输出
        :type Output: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Status = None
        self.Output = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.Output = params.get("Output")
        self.RequestId = params.get("RequestId")


class Quota(AbstractModel):
    """描述配额信息"""

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


class ReferredSecurityGroup(AbstractModel):
    """安全组被引用信息"""

    def __init__(self):
        """
        :param SecurityGroupId: 安全组实例ID。
        :type SecurityGroupId: str
        :param ReferredSecurityGroupIds: 引用安全组实例ID（SecurityGroupId）的所有安全组实例ID。
        :type ReferredSecurityGroupIds: list of str
        """
        self.SecurityGroupId = None
        self.ReferredSecurityGroupIds = None

    def _deserialize(self, params):
        self.SecurityGroupId = params.get("SecurityGroupId")
        self.ReferredSecurityGroupIds = params.get("ReferredSecurityGroupIds")


class RegionInfo(AbstractModel):
    """地域对象"""

    def __init__(self):
        """
        :param Region: 地域ID，如：ap-guangzhou。
        :type Region: str
        :param RegionId: 地域数字ID。
        :type RegionId: int
        :param ShortName: 地域简称，如：gz。
        :type ShortName: str
        :param Name: 地域名称，如：广州。
        :type Name: str
        :param IsChinaMainland: 是否中国大陆地域。
        :type IsChinaMainland: bool
        :param IsFinance: 是否金融地域。
        :type IsFinance: bool
        :param AvailableZoneSet: 可用区列表。
        :type AvailableZoneSet: list of AvailableZone
        :param WhiteListKey: 白名单`key`列表。
        :type WhiteListKey: list of str
        """
        self.Region = None
        self.RegionId = None
        self.ShortName = None
        self.Name = None
        self.IsChinaMainland = None
        self.IsFinance = None
        self.AvailableZoneSet = None
        self.WhiteListKey = None

    def _deserialize(self, params):
        self.Region = params.get("Region")
        self.RegionId = params.get("RegionId")
        self.ShortName = params.get("ShortName")
        self.Name = params.get("Name")
        self.IsChinaMainland = params.get("IsChinaMainland")
        self.IsFinance = params.get("IsFinance")
        if params.get("AvailableZoneSet") is not None:
            self.AvailableZoneSet = []
            for item in params.get("AvailableZoneSet"):
                obj = AvailableZone()
                obj._deserialize(item)
                self.AvailableZoneSet.append(obj)
        self.WhiteListKey = params.get("WhiteListKey")


class RejectAttachCcnInstancesRequest(AbstractModel):
    """RejectAttachCcnInstances请求参数结构体"""

    def __init__(self):
        """
        :param CcnId: CCN实例ID。形如：ccn-f49l6u0z。
        :type CcnId: str
        :param Instances: 拒绝关联实例列表。
        :type Instances: list of CcnInstance
        """
        self.CcnId = None
        self.Instances = None

    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")
        if params.get("Instances") is not None:
            self.Instances = []
            for item in params.get("Instances"):
                obj = CcnInstance()
                obj._deserialize(item)
                self.Instances.append(obj)


class RejectAttachCcnInstancesResponse(AbstractModel):
    """RejectAttachCcnInstances返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ReleaseAddressesRequest(AbstractModel):
    """ReleaseAddresses请求参数结构体"""

    def __init__(self):
        """
        :param AddressIds: 标识 EIP 的唯一 ID 列表。EIP 唯一 ID 形如：`eip-11112222`。
        :type AddressIds: list of str
        """
        self.AddressIds = None

    def _deserialize(self, params):
        self.AddressIds = params.get("AddressIds")


class ReleaseAddressesResponse(AbstractModel):
    """ReleaseAddresses返回参数结构体"""

    def __init__(self):
        """
        :param TaskId: 异步任务TaskId。可以使用DescribeTaskResult接口查询任务状态。
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class ReleaseIp6AddressesBandwidthRequest(AbstractModel):
    """ReleaseIp6AddressesBandwidth请求参数结构体"""

    def __init__(self):
        """
        :param Ip6Addresses: IPV6地址。Ip6Addresses和Ip6AddressIds必须且只能传一个
        :type Ip6Addresses: list of str
        :param Ip6AddressIds: IPV6地址对应的唯一ID，形如eip-xxxxxxxx。Ip6Addresses和Ip6AddressIds必须且只能传一个。
        :type Ip6AddressIds: list of str
        """
        self.Ip6Addresses = None
        self.Ip6AddressIds = None

    def _deserialize(self, params):
        self.Ip6Addresses = params.get("Ip6Addresses")
        self.Ip6AddressIds = params.get("Ip6AddressIds")


class ReleaseIp6AddressesBandwidthResponse(AbstractModel):
    """ReleaseIp6AddressesBandwidth返回参数结构体"""

    def __init__(self):
        """
        :param TaskId: 异步任务TaskId。可以使用DescribeTaskResult接口查询任务状态。
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class RemoveBandwidthPackageResourcesRequest(AbstractModel):
    """RemoveBandwidthPackageResources请求参数结构体"""

    def __init__(self):
        """
        :param BandwidthPackageId: 带宽包唯一标识ID，形如'bwp-xxxx'
        :type BandwidthPackageId: str
        :param ResourceType: 资源类型，包括‘Address’, ‘LoadBalance’
        :type ResourceType: str
        :param ResourceIds: 资源ID，可支持资源形如'eip-xxxx', 'lb-xxxx'
        :type ResourceIds: list of str
        """
        self.BandwidthPackageId = None
        self.ResourceType = None
        self.ResourceIds = None

    def _deserialize(self, params):
        self.BandwidthPackageId = params.get("BandwidthPackageId")
        self.ResourceType = params.get("ResourceType")
        self.ResourceIds = params.get("ResourceIds")


class RemoveBandwidthPackageResourcesResponse(AbstractModel):
    """RemoveBandwidthPackageResources返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class RemoveIp6RulesRequest(AbstractModel):
    """RemoveIp6Rules请求参数结构体"""

    def __init__(self):
        """
        :param Ip6TranslatorId: IPV6转换规则所属的转换实例唯一ID，形如ip6-xxxxxxxx
        :type Ip6TranslatorId: str
        :param Ip6RuleIds: 待删除IPV6转换规则，形如rule6-xxxxxxxx
        :type Ip6RuleIds: list of str
        """
        self.Ip6TranslatorId = None
        self.Ip6RuleIds = None

    def _deserialize(self, params):
        self.Ip6TranslatorId = params.get("Ip6TranslatorId")
        self.Ip6RuleIds = params.get("Ip6RuleIds")


class RemoveIp6RulesResponse(AbstractModel):
    """RemoveIp6Rules返回参数结构体"""

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
        :type AddressChargePrepaid: :class:`tcecloud.vpc.v20170312.models.AddressChargePrepaid`
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


class RenewCcnBandwidthRequest(AbstractModel):
    """RenewCcnBandwidth请求参数结构体"""

    def __init__(self):
        """
        :param InstanceChargePrepaid: 预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月实例的购买时长、是否设置自动续费等属性。若指定实例的付费模式为预付费则该参数必传。
        :type InstanceChargePrepaid: :class:`tcecloud.vpc.v20170312.models.InstanceChargePrepaid`
        :param RegionFlowControlId: 流量配置ID。
        :type RegionFlowControlId: str
        """
        self.InstanceChargePrepaid = None
        self.RegionFlowControlId = None

    def _deserialize(self, params):
        if params.get("InstanceChargePrepaid") is not None:
            self.InstanceChargePrepaid = InstanceChargePrepaid()
            self.InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))
        self.RegionFlowControlId = params.get("RegionFlowControlId")


class RenewCcnBandwidthResponse(AbstractModel):
    """RenewCcnBandwidth返回参数结构体"""

    def __init__(self):
        """
        :param DealName: 订单号。
        :type DealName: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DealName = None
        self.RequestId = None

    def _deserialize(self, params):
        self.DealName = params.get("DealName")
        self.RequestId = params.get("RequestId")


class RenewVpnGatewayRequest(AbstractModel):
    """RenewVpnGateway请求参数结构体"""

    def __init__(self):
        """
        :param VpnGatewayId: VPN网关实例ID。
        :type VpnGatewayId: str
        :param InstanceChargePrepaid: 预付费计费模式。
        :type InstanceChargePrepaid: :class:`tcecloud.vpc.v20170312.models.InstanceChargePrepaid`
        """
        self.VpnGatewayId = None
        self.InstanceChargePrepaid = None

    def _deserialize(self, params):
        self.VpnGatewayId = params.get("VpnGatewayId")
        if params.get("InstanceChargePrepaid") is not None:
            self.InstanceChargePrepaid = InstanceChargePrepaid()
            self.InstanceChargePrepaid._deserialize(params.get("InstanceChargePrepaid"))


class RenewVpnGatewayResponse(AbstractModel):
    """RenewVpnGateway返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ReplaceDirectConnectGatewayCcnRoutesRequest(AbstractModel):
    """ReplaceDirectConnectGatewayCcnRoutes请求参数结构体"""

    def __init__(self):
        """
        :param DirectConnectGatewayId: 专线网关ID，形如：dcg-prpqlmg1
        :type DirectConnectGatewayId: str
        :param Routes: 需要连通的IDC网段列表
        :type Routes: list of DirectConnectGatewayCcnRoute
        """
        self.DirectConnectGatewayId = None
        self.Routes = None

    def _deserialize(self, params):
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")
        if params.get("Routes") is not None:
            self.Routes = []
            for item in params.get("Routes"):
                obj = DirectConnectGatewayCcnRoute()
                obj._deserialize(item)
                self.Routes.append(obj)


class ReplaceDirectConnectGatewayCcnRoutesResponse(AbstractModel):
    """ReplaceDirectConnectGatewayCcnRoutes返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ReplaceRouteTableAssociationRequest(AbstractModel):
    """ReplaceRouteTableAssociation请求参数结构体"""

    def __init__(self):
        """
        :param SubnetId: 子网实例ID，例如：subnet-3x5lf5q0。可通过DescribeSubnets接口查询。
        :type SubnetId: str
        :param RouteTableId: 路由表实例ID，例如：rtb-azd4dt1c。
        :type RouteTableId: str
        """
        self.SubnetId = None
        self.RouteTableId = None

    def _deserialize(self, params):
        self.SubnetId = params.get("SubnetId")
        self.RouteTableId = params.get("RouteTableId")


class ReplaceRouteTableAssociationResponse(AbstractModel):
    """ReplaceRouteTableAssociation返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ReplaceRoutesRequest(AbstractModel):
    """ReplaceRoutes请求参数结构体"""

    def __init__(self):
        """
        :param RouteTableId: 路由表实例ID，例如：rtb-azd4dt1c。
        :type RouteTableId: str
        :param Routes: 路由策略对象。需要指定路由策略ID（RouteId）。
        :type Routes: list of Route
        """
        self.RouteTableId = None
        self.Routes = None

    def _deserialize(self, params):
        self.RouteTableId = params.get("RouteTableId")
        if params.get("Routes") is not None:
            self.Routes = []
            for item in params.get("Routes"):
                obj = Route()
                obj._deserialize(item)
                self.Routes.append(obj)


class ReplaceRoutesResponse(AbstractModel):
    """ReplaceRoutes返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ReplaceSecurityGroupPolicyRequest(AbstractModel):
    """ReplaceSecurityGroupPolicy请求参数结构体"""

    def __init__(self):
        """
        :param SecurityGroupId: 安全组实例ID，例如sg-33ocnj9n，可通过DescribeSecurityGroups获取。
        :type SecurityGroupId: str
        :param SecurityGroupPolicySet: 安全组规则集合对象。
        :type SecurityGroupPolicySet: :class:`tcecloud.vpc.v20170312.models.SecurityGroupPolicySet`
        """
        self.SecurityGroupId = None
        self.SecurityGroupPolicySet = None

    def _deserialize(self, params):
        self.SecurityGroupId = params.get("SecurityGroupId")
        if params.get("SecurityGroupPolicySet") is not None:
            self.SecurityGroupPolicySet = SecurityGroupPolicySet()
            self.SecurityGroupPolicySet._deserialize(params.get("SecurityGroupPolicySet"))


class ReplaceSecurityGroupPolicyResponse(AbstractModel):
    """ReplaceSecurityGroupPolicy返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ResetAttachCcnInstancesRequest(AbstractModel):
    """ResetAttachCcnInstances请求参数结构体"""

    def __init__(self):
        """
        :param CcnId: CCN实例ID。形如：ccn-f49l6u0z。
        :type CcnId: str
        :param CcnUin: CCN所属UIN（根账号）。
        :type CcnUin: str
        :param Instances: 重新申请关联网络实例列表。
        :type Instances: list of CcnInstance
        """
        self.CcnId = None
        self.CcnUin = None
        self.Instances = None

    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")
        self.CcnUin = params.get("CcnUin")
        if params.get("Instances") is not None:
            self.Instances = []
            for item in params.get("Instances"):
                obj = CcnInstance()
                obj._deserialize(item)
                self.Instances.append(obj)


class ResetAttachCcnInstancesResponse(AbstractModel):
    """ResetAttachCcnInstances返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ResetNatGatewayConnectionRequest(AbstractModel):
    """ResetNatGatewayConnection请求参数结构体"""

    def __init__(self):
        """
        :param NatGatewayId: NAT网关ID。
        :type NatGatewayId: str
        :param MaxConcurrentConnection: NAT网关并发连接上限，形如：1000000、3000000、10000000。
        :type MaxConcurrentConnection: int
        """
        self.NatGatewayId = None
        self.MaxConcurrentConnection = None

    def _deserialize(self, params):
        self.NatGatewayId = params.get("NatGatewayId")
        self.MaxConcurrentConnection = params.get("MaxConcurrentConnection")


class ResetNatGatewayConnectionResponse(AbstractModel):
    """ResetNatGatewayConnection返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ResetRoutesRequest(AbstractModel):
    """ResetRoutes请求参数结构体"""

    def __init__(self):
        """
        :param RouteTableId: 路由表实例ID，例如：rtb-azd4dt1c。
        :type RouteTableId: str
        :param RouteTableName: 路由表名称，最大长度不能超过60个字节。
        :type RouteTableName: str
        :param Routes: 路由策略。
        :type Routes: list of Route
        """
        self.RouteTableId = None
        self.RouteTableName = None
        self.Routes = None

    def _deserialize(self, params):
        self.RouteTableId = params.get("RouteTableId")
        self.RouteTableName = params.get("RouteTableName")
        if params.get("Routes") is not None:
            self.Routes = []
            for item in params.get("Routes"):
                obj = Route()
                obj._deserialize(item)
                self.Routes.append(obj)


class ResetRoutesResponse(AbstractModel):
    """ResetRoutes返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ResetTrafficMirrorFilterRequest(AbstractModel):
    """ResetTrafficMirrorFilter请求参数结构体"""

    def __init__(self):
        """
        :param TrafficMirrorId: 流量镜像实例ID
        :type TrafficMirrorId: str
        :param NatId: 流量镜像需要过滤的natgw实例ID
        :type NatId: str
        :param CollectorNormalFilters: 流量镜像需要过滤的五元组规则
        :type CollectorNormalFilters: list of TrafficMirrorFilter
        """
        self.TrafficMirrorId = None
        self.NatId = None
        self.CollectorNormalFilters = None

    def _deserialize(self, params):
        self.TrafficMirrorId = params.get("TrafficMirrorId")
        self.NatId = params.get("NatId")
        if params.get("CollectorNormalFilters") is not None:
            self.CollectorNormalFilters = []
            for item in params.get("CollectorNormalFilters"):
                obj = TrafficMirrorFilter()
                obj._deserialize(item)
                self.CollectorNormalFilters.append(obj)


class ResetTrafficMirrorFilterResponse(AbstractModel):
    """ResetTrafficMirrorFilter返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ResetTrafficMirrorSrcsRequest(AbstractModel):
    """ResetTrafficMirrorSrcs请求参数结构体"""

    def __init__(self):
        """
        :param TrafficMirrorId: 流量镜像实例ID
        :type TrafficMirrorId: str
        :param CollectorSrcs: 流量镜像采集对象
        :type CollectorSrcs: list of str
        """
        self.TrafficMirrorId = None
        self.CollectorSrcs = None

    def _deserialize(self, params):
        self.TrafficMirrorId = params.get("TrafficMirrorId")
        self.CollectorSrcs = params.get("CollectorSrcs")


class ResetTrafficMirrorSrcsResponse(AbstractModel):
    """ResetTrafficMirrorSrcs返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ResetTrafficMirrorTargetRequest(AbstractModel):
    """ResetTrafficMirrorTarget请求参数结构体"""

    def __init__(self):
        """
        :param TrafficMirrorId: 流量镜像实例ID
        :type TrafficMirrorId: str
        :param CollectorTarget: 流量镜像的接收目的信息
        :type CollectorTarget: :class:`tcecloud.vpc.v20170312.models.TrafficMirrorTarget`
        """
        self.TrafficMirrorId = None
        self.CollectorTarget = None

    def _deserialize(self, params):
        self.TrafficMirrorId = params.get("TrafficMirrorId")
        if params.get("CollectorTarget") is not None:
            self.CollectorTarget = TrafficMirrorTarget()
            self.CollectorTarget._deserialize(params.get("CollectorTarget"))


class ResetTrafficMirrorTargetResponse(AbstractModel):
    """ResetTrafficMirrorTarget返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ResetVpnConnectionRequest(AbstractModel):
    """ResetVpnConnection请求参数结构体"""

    def __init__(self):
        """
        :param VpnGatewayId: VPN网关实例ID。
        :type VpnGatewayId: str
        :param VpnConnectionId: VPN通道实例ID。形如：vpnx-f49l6u0z。
        :type VpnConnectionId: str
        """
        self.VpnGatewayId = None
        self.VpnConnectionId = None

    def _deserialize(self, params):
        self.VpnGatewayId = params.get("VpnGatewayId")
        self.VpnConnectionId = params.get("VpnConnectionId")


class ResetVpnConnectionResponse(AbstractModel):
    """ResetVpnConnection返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ResetVpnGatewayInternetMaxBandwidthRequest(AbstractModel):
    """ResetVpnGatewayInternetMaxBandwidth请求参数结构体"""

    def __init__(self):
        """
        :param VpnGatewayId: VPN网关实例ID。
        :type VpnGatewayId: str
        :param InternetMaxBandwidthOut: 公网带宽设置。可选带宽规格：5, 10, 20, 50, 100；单位：Mbps。
        :type InternetMaxBandwidthOut: int
        """
        self.VpnGatewayId = None
        self.InternetMaxBandwidthOut = None

    def _deserialize(self, params):
        self.VpnGatewayId = params.get("VpnGatewayId")
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")


class ResetVpnGatewayInternetMaxBandwidthResponse(AbstractModel):
    """ResetVpnGatewayInternetMaxBandwidth返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class Resource(AbstractModel):
    """描述带宽包资源信息的结构"""

    def __init__(self):
        """
        :param ResourceType: 带宽包资源类型，包括'Address'和'LoadBalance'
        :type ResourceType: str
        :param ResourceId: 带宽包资源Id，形如'eip-xxxx', 'lb-xxxx'
        :type ResourceId: str
        :param AddressIp: 带宽包资源Ip
        :type AddressIp: str
        """
        self.ResourceType = None
        self.ResourceId = None
        self.AddressIp = None

    def _deserialize(self, params):
        self.ResourceType = params.get("ResourceType")
        self.ResourceId = params.get("ResourceId")
        self.AddressIp = params.get("AddressIp")


class ResourceDashboard(AbstractModel):
    """VPC资源看板（各资源个数）"""

    def __init__(self):
        """
        :param VpcId: Vpc实例ID，例如：vpc-f1xjkw1b。
        :type VpcId: str
        :param SubnetId: 子网实例ID，例如：subnet-bthucmmy。
        :type SubnetId: str
        :param Classiclink: 基础网络互通。
        :type Classiclink: int
        :param Dcg: 专线网关。
        :type Dcg: int
        :param Pcx: 对等连接。
        :type Pcx: int
        :param Ip: 当前已使用的IP总数。
        :type Ip: int
        :param Nat: NAT网关。
        :type Nat: int
        :param Vpngw: VPN网关。
        :type Vpngw: int
        :param FlowLog: 流日志。
        :type FlowLog: int
        :param NetworkDetect: 网络探测。
        :type NetworkDetect: int
        :param NetworkACL: 网络ACL。
        :type NetworkACL: int
        :param CVM: 云主机。
        :type CVM: int
        :param LB: 负载均衡。
        :type LB: int
        :param CDB: 关系型数据库。
        :type CDB: int
        :param Cmem: 云数据库 TencentDB for Memcached。
        :type Cmem: int
        :param CTSDB: 时序数据库。
        :type CTSDB: int
        :param MariaDB: 数据库 TencentDB for MariaDB（TDSQL）。
        :type MariaDB: int
        :param SQLServer: 数据库 TencentDB for SQL Server。
        :type SQLServer: int
        :param Postgres: 云数据库 TencentDB for PostgreSQL。
        :type Postgres: int
        :param NAS: 网络附加存储。
        :type NAS: int
        :param Greenplumn: Snova云数据仓库。
        :type Greenplumn: int
        :param Ckafka: 消息队列 CKAFKA。
        :type Ckafka: int
        :param Grocery: Grocery。
        :type Grocery: int
        :param HSM: 数据加密服务。
        :type HSM: int
        :param Tcaplus: 游戏存储 Tcaplus。
        :type Tcaplus: int
        :param Cnas: Cnas。
        :type Cnas: int
        :param TiDB: HTAP 数据库 TiDB。
        :type TiDB: int
        :param Emr: EMR 集群。
        :type Emr: int
        :param SEAL: SEAL。
        :type SEAL: int
        :param CFS: 文件存储 CFS。
        :type CFS: int
        :param Oracle: Oracle。
        :type Oracle: int
        :param ElasticSearch: ElasticSearch服务。
        :type ElasticSearch: int
        :param TBaaS: 区块链服务。
        :type TBaaS: int
        :param Itop: Itop。
        :type Itop: int
        :param DBAudit: 云数据库审计。
        :type DBAudit: int
        :param CynosDBPostgres: 企业级云数据库 CynosDB for Postgres。
        :type CynosDBPostgres: int
        :param Redis: 数据库 TencentDB for Redis。
        :type Redis: int
        :param MongoDB: 数据库 TencentDB for MongoDB。
        :type MongoDB: int
        :param DCDB: 分布式数据库 TencentDB for TDSQL。
        :type DCDB: int
        :param CynosDBMySQL: 企业级云数据库 CynosDB for MySQL。
        :type CynosDBMySQL: int
        :param Subnet: 子网。
        :type Subnet: int
        :param RouteTable: 路由表。
        :type RouteTable: int
        """
        self.VpcId = None
        self.SubnetId = None
        self.Classiclink = None
        self.Dcg = None
        self.Pcx = None
        self.Ip = None
        self.Nat = None
        self.Vpngw = None
        self.FlowLog = None
        self.NetworkDetect = None
        self.NetworkACL = None
        self.CVM = None
        self.LB = None
        self.CDB = None
        self.Cmem = None
        self.CTSDB = None
        self.MariaDB = None
        self.SQLServer = None
        self.Postgres = None
        self.NAS = None
        self.Greenplumn = None
        self.Ckafka = None
        self.Grocery = None
        self.HSM = None
        self.Tcaplus = None
        self.Cnas = None
        self.TiDB = None
        self.Emr = None
        self.SEAL = None
        self.CFS = None
        self.Oracle = None
        self.ElasticSearch = None
        self.TBaaS = None
        self.Itop = None
        self.DBAudit = None
        self.CynosDBPostgres = None
        self.Redis = None
        self.MongoDB = None
        self.DCDB = None
        self.CynosDBMySQL = None
        self.Subnet = None
        self.RouteTable = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.Classiclink = params.get("Classiclink")
        self.Dcg = params.get("Dcg")
        self.Pcx = params.get("Pcx")
        self.Ip = params.get("Ip")
        self.Nat = params.get("Nat")
        self.Vpngw = params.get("Vpngw")
        self.FlowLog = params.get("FlowLog")
        self.NetworkDetect = params.get("NetworkDetect")
        self.NetworkACL = params.get("NetworkACL")
        self.CVM = params.get("CVM")
        self.LB = params.get("LB")
        self.CDB = params.get("CDB")
        self.Cmem = params.get("Cmem")
        self.CTSDB = params.get("CTSDB")
        self.MariaDB = params.get("MariaDB")
        self.SQLServer = params.get("SQLServer")
        self.Postgres = params.get("Postgres")
        self.NAS = params.get("NAS")
        self.Greenplumn = params.get("Greenplumn")
        self.Ckafka = params.get("Ckafka")
        self.Grocery = params.get("Grocery")
        self.HSM = params.get("HSM")
        self.Tcaplus = params.get("Tcaplus")
        self.Cnas = params.get("Cnas")
        self.TiDB = params.get("TiDB")
        self.Emr = params.get("Emr")
        self.SEAL = params.get("SEAL")
        self.CFS = params.get("CFS")
        self.Oracle = params.get("Oracle")
        self.ElasticSearch = params.get("ElasticSearch")
        self.TBaaS = params.get("TBaaS")
        self.Itop = params.get("Itop")
        self.DBAudit = params.get("DBAudit")
        self.CynosDBPostgres = params.get("CynosDBPostgres")
        self.Redis = params.get("Redis")
        self.MongoDB = params.get("MongoDB")
        self.DCDB = params.get("DCDB")
        self.CynosDBMySQL = params.get("CynosDBMySQL")
        self.Subnet = params.get("Subnet")
        self.RouteTable = params.get("RouteTable")


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


class Route(AbstractModel):
    """路由策略对象"""

    def __init__(self):
        """
                :param DestinationCidrBlock: 目的网段，取值不能在私有网络网段内，例如：112.20.51.0/24。
                :type DestinationCidrBlock: str
                :param GatewayType: 下一跳类型，目前我们支持的类型有：
        CVM：公网网关类型的云服务器；
        VPN：VPN网关；
        DIRECTCONNECT：专线网关；
        PEERCONNECTION：对等连接；
        SSLVPN：sslvpn网关；
        NAT：NAT网关;
        NORMAL_CVM：普通云服务器；
        EIP：云服务器的公网IP；
        CCN：云联网。
                :type GatewayType: str
                :param GatewayId: 下一跳地址，这里只需要指定不同下一跳类型的网关ID，系统会自动匹配到下一跳地址。
        特别注意：当 GatewayType 为 EIP 时，GatewayId 固定值 '0'
                :type GatewayId: str
                :param RouteId: 路由策略ID。
                :type RouteId: int
                :param RouteDescription: 路由策略描述。
                :type RouteDescription: str
                :param Enabled: 是否启用
                :type Enabled: bool
                :param RouteType: 路由类型，目前我们支持的类型有：
        USER：用户路由；
        NETD：网络探测路由，创建网络探测实例时，系统默认下发，不可编辑与删除；
        CCN：云联网路由，系统默认下发，不可编辑与删除。
        用户只能添加和操作 USER 类型的路由。
                :type RouteType: str
                :param RouteTableId: 路由表实例ID，例如：rtb-azd4dt1c。
                :type RouteTableId: str
        """
        self.DestinationCidrBlock = None
        self.GatewayType = None
        self.GatewayId = None
        self.RouteId = None
        self.RouteDescription = None
        self.Enabled = None
        self.RouteType = None
        self.RouteTableId = None

    def _deserialize(self, params):
        self.DestinationCidrBlock = params.get("DestinationCidrBlock")
        self.GatewayType = params.get("GatewayType")
        self.GatewayId = params.get("GatewayId")
        self.RouteId = params.get("RouteId")
        self.RouteDescription = params.get("RouteDescription")
        self.Enabled = params.get("Enabled")
        self.RouteType = params.get("RouteType")
        self.RouteTableId = params.get("RouteTableId")


class RouteConflict(AbstractModel):
    """路由冲突对象"""

    def __init__(self):
        """
        :param RouteTableId: 路由表实例ID，例如：rtb-azd4dt1c。
        :type RouteTableId: str
        :param DestinationCidrBlock: 要检查的与之冲突的目的端
        :type DestinationCidrBlock: str
        :param ConflictSet: 冲突的路由策略列表
        :type ConflictSet: list of Route
        """
        self.RouteTableId = None
        self.DestinationCidrBlock = None
        self.ConflictSet = None

    def _deserialize(self, params):
        self.RouteTableId = params.get("RouteTableId")
        self.DestinationCidrBlock = params.get("DestinationCidrBlock")
        if params.get("ConflictSet") is not None:
            self.ConflictSet = []
            for item in params.get("ConflictSet"):
                obj = Route()
                obj._deserialize(item)
                self.ConflictSet.append(obj)


class RouteTable(AbstractModel):
    """路由表对象"""

    def __init__(self):
        """
                :param VpcId: VPC实例ID。
                :type VpcId: str
                :param RouteTableId: 路由表实例ID，例如：rtb-azd4dt1c。
                :type RouteTableId: str
                :param RouteTableName: 路由表名称。
                :type RouteTableName: str
                :param AssociationSet: 路由表关联关系。
                :type AssociationSet: list of RouteTableAssociation
                :param RouteSet: 路由表策略集合。
                :type RouteSet: list of Route
                :param Main: 是否默认路由表。
                :type Main: bool
                :param CreatedTime: 创建时间。
                :type CreatedTime: str
                :param TagSet: 标签键值对。
                :type TagSet: list of Tag
                :param SubnetNum: 子网数
        注意：此字段可能返回 null，表示取不到有效值。
                :type SubnetNum: int
        """
        self.VpcId = None
        self.RouteTableId = None
        self.RouteTableName = None
        self.AssociationSet = None
        self.RouteSet = None
        self.Main = None
        self.CreatedTime = None
        self.TagSet = None
        self.SubnetNum = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.RouteTableId = params.get("RouteTableId")
        self.RouteTableName = params.get("RouteTableName")
        if params.get("AssociationSet") is not None:
            self.AssociationSet = []
            for item in params.get("AssociationSet"):
                obj = RouteTableAssociation()
                obj._deserialize(item)
                self.AssociationSet.append(obj)
        if params.get("RouteSet") is not None:
            self.RouteSet = []
            for item in params.get("RouteSet"):
                obj = Route()
                obj._deserialize(item)
                self.RouteSet.append(obj)
        self.Main = params.get("Main")
        self.CreatedTime = params.get("CreatedTime")
        if params.get("TagSet") is not None:
            self.TagSet = []
            for item in params.get("TagSet"):
                obj = Tag()
                obj._deserialize(item)
                self.TagSet.append(obj)
        self.SubnetNum = params.get("SubnetNum")


class RouteTableAssociation(AbstractModel):
    """路由表关联关系"""

    def __init__(self):
        """
        :param SubnetId: 子网实例ID。
        :type SubnetId: str
        :param RouteTableId: 路由表实例ID。
        :type RouteTableId: str
        """
        self.SubnetId = None
        self.RouteTableId = None

    def _deserialize(self, params):
        self.SubnetId = params.get("SubnetId")
        self.RouteTableId = params.get("RouteTableId")


class SecurityGroup(AbstractModel):
    """安全组对象"""

    def __init__(self):
        """
        :param SecurityGroupId: 安全组实例ID，例如：sg-ohuuioma。
        :type SecurityGroupId: str
        :param SecurityGroupName: 安全组名称，可任意命名，但不得超过60个字符。
        :type SecurityGroupName: str
        :param SecurityGroupDesc: 安全组备注，最多100个字符。
        :type SecurityGroupDesc: str
        :param ProjectId: 项目id，默认0。可在qcloud控制台项目管理页面查询到。
        :type ProjectId: str
        :param IsDefault: 是否是默认安全组，默认安全组不支持删除。
        :type IsDefault: bool
        :param CreatedTime: 安全组创建时间。
        :type CreatedTime: str
        :param TagSet: 标签键值对。
        :type TagSet: list of Tag
        """
        self.SecurityGroupId = None
        self.SecurityGroupName = None
        self.SecurityGroupDesc = None
        self.ProjectId = None
        self.IsDefault = None
        self.CreatedTime = None
        self.TagSet = None

    def _deserialize(self, params):
        self.SecurityGroupId = params.get("SecurityGroupId")
        self.SecurityGroupName = params.get("SecurityGroupName")
        self.SecurityGroupDesc = params.get("SecurityGroupDesc")
        self.ProjectId = params.get("ProjectId")
        self.IsDefault = params.get("IsDefault")
        self.CreatedTime = params.get("CreatedTime")
        if params.get("TagSet") is not None:
            self.TagSet = []
            for item in params.get("TagSet"):
                obj = Tag()
                obj._deserialize(item)
                self.TagSet.append(obj)


class SecurityGroupAssociationStatistics(AbstractModel):
    """安全组关联的实例统计"""

    def __init__(self):
        """
        :param SecurityGroupId: 安全组实例ID。
        :type SecurityGroupId: str
        :param CVM: 云服务器实例数。
        :type CVM: int
        :param CDB: 数据库实例数。
        :type CDB: int
        :param ENI: 弹性网卡实例数。
        :type ENI: int
        :param SG: 被安全组引用数。
        :type SG: int
        :param CLB: 负载均衡实例数。
        :type CLB: int
        :param InstanceStatistics: 全量实例的绑定统计。
        :type InstanceStatistics: list of InstanceStatistic
        :param TotalCount: 所有资源的总计数（不包含被安全组引用数）。
        :type TotalCount: int
        """
        self.SecurityGroupId = None
        self.CVM = None
        self.CDB = None
        self.ENI = None
        self.SG = None
        self.CLB = None
        self.InstanceStatistics = None
        self.TotalCount = None

    def _deserialize(self, params):
        self.SecurityGroupId = params.get("SecurityGroupId")
        self.CVM = params.get("CVM")
        self.CDB = params.get("CDB")
        self.ENI = params.get("ENI")
        self.SG = params.get("SG")
        self.CLB = params.get("CLB")
        if params.get("InstanceStatistics") is not None:
            self.InstanceStatistics = []
            for item in params.get("InstanceStatistics"):
                obj = InstanceStatistic()
                obj._deserialize(item)
                self.InstanceStatistics.append(obj)
        self.TotalCount = params.get("TotalCount")


class SecurityGroupLimitSet(AbstractModel):
    """用户安全组配额限制。"""

    def __init__(self):
        """
        :param SecurityGroupLimit: 每个项目每个地域可创建安全组数
        :type SecurityGroupLimit: int
        :param SecurityGroupPolicyLimit: 安全组下的最大规则数
        :type SecurityGroupPolicyLimit: int
        :param ReferedSecurityGroupLimit: 安全组下嵌套安全组规则数
        :type ReferedSecurityGroupLimit: int
        :param SecurityGroupInstanceLimit: 单安全组关联实例数
        :type SecurityGroupInstanceLimit: int
        :param InstanceSecurityGroupLimit: 实例关联安全组数
        :type InstanceSecurityGroupLimit: int
        """
        self.SecurityGroupLimit = None
        self.SecurityGroupPolicyLimit = None
        self.ReferedSecurityGroupLimit = None
        self.SecurityGroupInstanceLimit = None
        self.InstanceSecurityGroupLimit = None

    def _deserialize(self, params):
        self.SecurityGroupLimit = params.get("SecurityGroupLimit")
        self.SecurityGroupPolicyLimit = params.get("SecurityGroupPolicyLimit")
        self.ReferedSecurityGroupLimit = params.get("ReferedSecurityGroupLimit")
        self.SecurityGroupInstanceLimit = params.get("SecurityGroupInstanceLimit")
        self.InstanceSecurityGroupLimit = params.get("InstanceSecurityGroupLimit")


class SecurityGroupPolicy(AbstractModel):
    """安全组规则对象"""

    def __init__(self):
        """
        :param PolicyIndex: 安全组规则索引号。
        :type PolicyIndex: int
        :param Protocol: 协议, 取值: TCP,UDP, ICMP。
        :type Protocol: str
        :param Port: 端口(all, 离散port,  range)。
        :type Port: str
        :param ServiceTemplate: 协议端口ID或者协议端口组ID。ServiceTemplate和Protocol+Port互斥。
        :type ServiceTemplate: :class:`tcecloud.vpc.v20170312.models.ServiceTemplateSpecification`
        :param CidrBlock: 网段或IP(互斥)。
        :type CidrBlock: str
        :param Ipv6CidrBlock: 网段或IPv6(互斥)。
        :type Ipv6CidrBlock: str
        :param SecurityGroupId: 安全组实例ID，例如：sg-ohuuioma。
        :type SecurityGroupId: str
        :param AddressTemplate: IP地址ID或者ID地址组ID。
        :type AddressTemplate: :class:`tcecloud.vpc.v20170312.models.AddressTemplateSpecification`
        :param Action: ACCEPT 或 DROP。
        :type Action: str
        :param PolicyDescription: 安全组规则描述。
        :type PolicyDescription: str
        :param ModifyTime: 安全组最近修改时间。
        :type ModifyTime: str
        """
        self.PolicyIndex = None
        self.Protocol = None
        self.Port = None
        self.ServiceTemplate = None
        self.CidrBlock = None
        self.Ipv6CidrBlock = None
        self.SecurityGroupId = None
        self.AddressTemplate = None
        self.Action = None
        self.PolicyDescription = None
        self.ModifyTime = None

    def _deserialize(self, params):
        self.PolicyIndex = params.get("PolicyIndex")
        self.Protocol = params.get("Protocol")
        self.Port = params.get("Port")
        if params.get("ServiceTemplate") is not None:
            self.ServiceTemplate = ServiceTemplateSpecification()
            self.ServiceTemplate._deserialize(params.get("ServiceTemplate"))
        self.CidrBlock = params.get("CidrBlock")
        self.Ipv6CidrBlock = params.get("Ipv6CidrBlock")
        self.SecurityGroupId = params.get("SecurityGroupId")
        if params.get("AddressTemplate") is not None:
            self.AddressTemplate = AddressTemplateSpecification()
            self.AddressTemplate._deserialize(params.get("AddressTemplate"))
        self.Action = params.get("Action")
        self.PolicyDescription = params.get("PolicyDescription")
        self.ModifyTime = params.get("ModifyTime")


class SecurityGroupPolicyCheckInfo(AbstractModel):
    """安全组策略检测结果对象"""

    def __init__(self):
        """
        :param Direction: 数据流方向，取值：inbound(入站)，outbound(出站)。
        :type Direction: str
        :param Protocol: 协议, 取值: TCP,UDP, ICMP。
        :type Protocol: str
        :param Port: 端口号，对于入站为目标端口，对于出站为源端口。
        :type Port: str
        :param Action: 数据流是否方通，取值：ACCEPT(方通)，DROP(未方通)。
        :type Action: str
        """
        self.Direction = None
        self.Protocol = None
        self.Port = None
        self.Action = None

    def _deserialize(self, params):
        self.Direction = params.get("Direction")
        self.Protocol = params.get("Protocol")
        self.Port = params.get("Port")
        self.Action = params.get("Action")


class SecurityGroupPolicySet(AbstractModel):
    """安全组规则集合"""

    def __init__(self):
        """
        :param Version: 安全组规则当前版本。用户每次更新安全规则版本会自动加1，防止更新的路由规则已过期，不填不考虑冲突。
        :type Version: str
        :param Egress: 出站规则。
        :type Egress: list of SecurityGroupPolicy
        :param Ingress: 入站规则。
        :type Ingress: list of SecurityGroupPolicy
        """
        self.Version = None
        self.Egress = None
        self.Ingress = None

    def _deserialize(self, params):
        self.Version = params.get("Version")
        if params.get("Egress") is not None:
            self.Egress = []
            for item in params.get("Egress"):
                obj = SecurityGroupPolicy()
                obj._deserialize(item)
                self.Egress.append(obj)
        if params.get("Ingress") is not None:
            self.Ingress = []
            for item in params.get("Ingress"):
                obj = SecurityGroupPolicy()
                obj._deserialize(item)
                self.Ingress.append(obj)


class SecurityGroupPolicyTemplate(AbstractModel):
    """安全组规则模板"""

    def __init__(self):
        """
        :param TemplateName: 模板名称。
        :type TemplateName: str
        :param TemplateRemark: 模板描述。
        :type TemplateRemark: str
        :param Ingress: 入站规则。
        :type Ingress: list of SecurityGroupPolicy
        :param Egress: 出站规则。
        :type Egress: list of SecurityGroupPolicy
        """
        self.TemplateName = None
        self.TemplateRemark = None
        self.Ingress = None
        self.Egress = None

    def _deserialize(self, params):
        self.TemplateName = params.get("TemplateName")
        self.TemplateRemark = params.get("TemplateRemark")
        if params.get("Ingress") is not None:
            self.Ingress = []
            for item in params.get("Ingress"):
                obj = SecurityGroupPolicy()
                obj._deserialize(item)
                self.Ingress.append(obj)
        if params.get("Egress") is not None:
            self.Egress = []
            for item in params.get("Egress"):
                obj = SecurityGroupPolicy()
                obj._deserialize(item)
                self.Egress.append(obj)


class SecurityPolicyDatabase(AbstractModel):
    """SecurityPolicyDatabase策略"""

    def __init__(self):
        """
        :param LocalCidrBlock: 本端网段
        :type LocalCidrBlock: str
        :param RemoteCidrBlock: 对端网段
        :type RemoteCidrBlock: list of str
        """
        self.LocalCidrBlock = None
        self.RemoteCidrBlock = None

    def _deserialize(self, params):
        self.LocalCidrBlock = params.get("LocalCidrBlock")
        self.RemoteCidrBlock = params.get("RemoteCidrBlock")


class ServiceTemplate(AbstractModel):
    """协议端口模板"""

    def __init__(self):
        """
        :param ServiceTemplateId: 协议端口实例ID，例如：ppm-f5n1f8da。
        :type ServiceTemplateId: str
        :param ServiceTemplateName: 模板名称。
        :type ServiceTemplateName: str
        :param ServiceSet: 协议端口信息。
        :type ServiceSet: list of str
        :param CreatedTime: 创建时间。
        :type CreatedTime: str
        """
        self.ServiceTemplateId = None
        self.ServiceTemplateName = None
        self.ServiceSet = None
        self.CreatedTime = None

    def _deserialize(self, params):
        self.ServiceTemplateId = params.get("ServiceTemplateId")
        self.ServiceTemplateName = params.get("ServiceTemplateName")
        self.ServiceSet = params.get("ServiceSet")
        self.CreatedTime = params.get("CreatedTime")


class ServiceTemplateGroup(AbstractModel):
    """协议端口模板集合"""

    def __init__(self):
        """
        :param ServiceTemplateGroupId: 协议端口模板集合实例ID，例如：ppmg-2klmrefu。
        :type ServiceTemplateGroupId: str
        :param ServiceTemplateGroupName: 协议端口模板集合名称。
        :type ServiceTemplateGroupName: str
        :param ServiceTemplateIdSet: 协议端口模板实例ID。
        :type ServiceTemplateIdSet: list of str
        :param CreatedTime: 创建时间。
        :type CreatedTime: str
        :param ServiceTemplateSet: 协议端口模板实例信息。
        :type ServiceTemplateSet: list of ServiceTemplate
        """
        self.ServiceTemplateGroupId = None
        self.ServiceTemplateGroupName = None
        self.ServiceTemplateIdSet = None
        self.CreatedTime = None
        self.ServiceTemplateSet = None

    def _deserialize(self, params):
        self.ServiceTemplateGroupId = params.get("ServiceTemplateGroupId")
        self.ServiceTemplateGroupName = params.get("ServiceTemplateGroupName")
        self.ServiceTemplateIdSet = params.get("ServiceTemplateIdSet")
        self.CreatedTime = params.get("CreatedTime")
        if params.get("ServiceTemplateSet") is not None:
            self.ServiceTemplateSet = []
            for item in params.get("ServiceTemplateSet"):
                obj = ServiceTemplate()
                obj._deserialize(item)
                self.ServiceTemplateSet.append(obj)


class ServiceTemplateSpecification(AbstractModel):
    """协议端口模版"""

    def __init__(self):
        """
        :param ServiceId: 协议端口ID，例如：ppm-f5n1f8da。
        :type ServiceId: str
        :param ServiceGroupId: 协议端口组ID，例如：ppmg-f5n1f8da。
        :type ServiceGroupId: str
        """
        self.ServiceId = None
        self.ServiceGroupId = None

    def _deserialize(self, params):
        self.ServiceId = params.get("ServiceId")
        self.ServiceGroupId = params.get("ServiceGroupId")


class SetCcnBandwidthRenewFlagRequest(AbstractModel):
    """SetCcnBandwidthRenewFlag请求参数结构体"""

    def __init__(self):
        """
        :param RegionFlowControlIds: 流量配置ID。
        :type RegionFlowControlIds: list of str
        :param AutoRenewFlag: 是否自动续费标识，1：自动续费；2：不自动续费
        :type AutoRenewFlag: int
        :param RenewFlag: 是否自动续费标识，NOTIFY_AND_AUTO_RENEW：自动续费；NOTIFY_AND_MANUAL_RENEW： 不自动续费
        :type RenewFlag: str
        """
        self.RegionFlowControlIds = None
        self.AutoRenewFlag = None
        self.RenewFlag = None

    def _deserialize(self, params):
        self.RegionFlowControlIds = params.get("RegionFlowControlIds")
        self.AutoRenewFlag = params.get("AutoRenewFlag")
        self.RenewFlag = params.get("RenewFlag")


class SetCcnBandwidthRenewFlagResponse(AbstractModel):
    """SetCcnBandwidthRenewFlag返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class SetCcnRegionBandwidthLimitsRequest(AbstractModel):
    """SetCcnRegionBandwidthLimits请求参数结构体"""

    def __init__(self):
        """
        :param CcnId: CCN实例ID。形如：ccn-f49l6u0z。
        :type CcnId: str
        :param CcnRegionBandwidthLimits: 云联网（CCN）各地域出带宽上限。
        :type CcnRegionBandwidthLimits: list of CcnRegionBandwidthLimit
        """
        self.CcnId = None
        self.CcnRegionBandwidthLimits = None

    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")
        if params.get("CcnRegionBandwidthLimits") is not None:
            self.CcnRegionBandwidthLimits = []
            for item in params.get("CcnRegionBandwidthLimits"):
                obj = CcnRegionBandwidthLimit()
                obj._deserialize(item)
                self.CcnRegionBandwidthLimits.append(obj)


class SetCcnRegionBandwidthLimitsResponse(AbstractModel):
    """SetCcnRegionBandwidthLimits返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class SetVpnGatewaysRenewFlagRequest(AbstractModel):
    """SetVpnGatewaysRenewFlag请求参数结构体"""

    def __init__(self):
        """
                :param VpnGatewayIds: VPNGW字符型ID列表
                :type VpnGatewayIds: list of str
                :param AutoRenewFlag: 自动续费标记[0, 1, 2]
        0表示默认状态(初始状态)， 1表示自动续费，2表示明确不自动续费
                :type AutoRenewFlag: int
                :param Type: VPNGW类型['IPSEC', 'SSL']
                :type Type: str
        """
        self.VpnGatewayIds = None
        self.AutoRenewFlag = None
        self.Type = None

    def _deserialize(self, params):
        self.VpnGatewayIds = params.get("VpnGatewayIds")
        self.AutoRenewFlag = params.get("AutoRenewFlag")
        self.Type = params.get("Type")


class SetVpnGatewaysRenewFlagResponse(AbstractModel):
    """SetVpnGatewaysRenewFlag返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class SingleIspZone(AbstractModel):
    """可用区与三网运营商的映射关系"""

    def __init__(self):
        """
        :param Zone: 可用区
        :type Zone: str
        :param ZoneId: 可用区ID
        :type ZoneId: int
        :param Singleisp: 三网运营商，包括"CMCC", "CTCC", "CUCC"
        :type Singleisp: list of str
        """
        self.Zone = None
        self.ZoneId = None
        self.Singleisp = None

    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.ZoneId = params.get("ZoneId")
        self.Singleisp = params.get("Singleisp")


class StartTrafficMirrorRequest(AbstractModel):
    """StartTrafficMirror请求参数结构体"""

    def __init__(self):
        """
        :param TrafficMirrorId: 流量镜像实例ID
        :type TrafficMirrorId: str
        """
        self.TrafficMirrorId = None

    def _deserialize(self, params):
        self.TrafficMirrorId = params.get("TrafficMirrorId")


class StartTrafficMirrorResponse(AbstractModel):
    """StartTrafficMirror返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class StopTrafficMirrorRequest(AbstractModel):
    """StopTrafficMirror请求参数结构体"""

    def __init__(self):
        """
        :param TrafficMirrorId: 流量镜像实例ID
        :type TrafficMirrorId: str
        """
        self.TrafficMirrorId = None

    def _deserialize(self, params):
        self.TrafficMirrorId = params.get("TrafficMirrorId")


class StopTrafficMirrorResponse(AbstractModel):
    """StopTrafficMirror返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class Subnet(AbstractModel):
    """子网对象"""

    def __init__(self):
        """
                :param VpcId: `VPC`实例`ID`。
                :type VpcId: str
                :param SubnetId: 子网实例`ID`，例如：subnet-bthucmmy。
                :type SubnetId: str
                :param SubnetName: 子网名称。
                :type SubnetName: str
                :param CidrBlock: 子网的 `IPv4` `CIDR`。
                :type CidrBlock: str
                :param IsDefault: 是否默认子网。
                :type IsDefault: bool
                :param EnableBroadcast: 是否开启广播。
                :type EnableBroadcast: bool
                :param Zone: 可用区。
                :type Zone: str
                :param RouteTableId: 路由表实例ID，例如：rtb-l2h8d7c2。
                :type RouteTableId: str
                :param CreatedTime: 创建时间。
                :type CreatedTime: str
                :param AvailableIpAddressCount: 可用`IP`数。
                :type AvailableIpAddressCount: int
                :param Ipv6CidrBlock: 子网的 `IPv6` `CIDR`。
                :type Ipv6CidrBlock: str
                :param NetworkAclId: 关联`ACL`ID
                :type NetworkAclId: str
                :param IsRemoteVpcSnat: 是否为 `SNAT` 地址池子网。
                :type IsRemoteVpcSnat: bool
                :param TotalIpAddressCount: 子网`IP`总数。
                :type TotalIpAddressCount: int
                :param TagSet: 标签键值对。
                :type TagSet: list of Tag
                :param Type: 子网类型
                :type Type: int
                :param VmNum: vm数量
        注意：此字段可能返回 null，表示取不到有效值。
                :type VmNum: int
        """
        self.VpcId = None
        self.SubnetId = None
        self.SubnetName = None
        self.CidrBlock = None
        self.IsDefault = None
        self.EnableBroadcast = None
        self.Zone = None
        self.RouteTableId = None
        self.CreatedTime = None
        self.AvailableIpAddressCount = None
        self.Ipv6CidrBlock = None
        self.NetworkAclId = None
        self.IsRemoteVpcSnat = None
        self.TotalIpAddressCount = None
        self.TagSet = None
        self.Type = None
        self.VmNum = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.SubnetName = params.get("SubnetName")
        self.CidrBlock = params.get("CidrBlock")
        self.IsDefault = params.get("IsDefault")
        self.EnableBroadcast = params.get("EnableBroadcast")
        self.Zone = params.get("Zone")
        self.RouteTableId = params.get("RouteTableId")
        self.CreatedTime = params.get("CreatedTime")
        self.AvailableIpAddressCount = params.get("AvailableIpAddressCount")
        self.Ipv6CidrBlock = params.get("Ipv6CidrBlock")
        self.NetworkAclId = params.get("NetworkAclId")
        self.IsRemoteVpcSnat = params.get("IsRemoteVpcSnat")
        self.TotalIpAddressCount = params.get("TotalIpAddressCount")
        if params.get("TagSet") is not None:
            self.TagSet = []
            for item in params.get("TagSet"):
                obj = Tag()
                obj._deserialize(item)
                self.TagSet.append(obj)
        self.Type = params.get("Type")
        self.VmNum = params.get("VmNum")


class SubnetInput(AbstractModel):
    """子网对象"""

    def __init__(self):
        """
        :param CidrBlock: 子网的`CIDR`。
        :type CidrBlock: str
        :param SubnetName: 子网名称。
        :type SubnetName: str
        :param Zone: 可用区。形如：`ap-guangzhou-2`。
        :type Zone: str
        :param RouteTableId: 指定关联路由表，形如：`rtb-3ryrwzuu`。
        :type RouteTableId: str
        """
        self.CidrBlock = None
        self.SubnetName = None
        self.Zone = None
        self.RouteTableId = None

    def _deserialize(self, params):
        self.CidrBlock = params.get("CidrBlock")
        self.SubnetName = params.get("SubnetName")
        self.Zone = params.get("Zone")
        self.RouteTableId = params.get("RouteTableId")


class SubnetNum(AbstractModel):
    """子网数字ID"""

    def __init__(self):
        """
        :param VpcId: VPC实例ID。
        :type VpcId: str
        :param VpcNumId: VPC实例数字ID。
        :type VpcNumId: int
        :param SubnetId: 子网实例ID。
        :type SubnetId: str
        :param SubnetNumId: 子网实例数字ID。
        :type SubnetNumId: int
        """
        self.VpcId = None
        self.VpcNumId = None
        self.SubnetId = None
        self.SubnetNumId = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.VpcNumId = params.get("VpcNumId")
        self.SubnetId = params.get("SubnetId")
        self.SubnetNumId = params.get("SubnetNumId")


class Tag(AbstractModel):
    """标签键值对"""

    def __init__(self):
        """
                :param Key: 标签键
        注意：此字段可能返回 null，表示取不到有效值。
                :type Key: str
                :param Value: 标签值
        注意：此字段可能返回 null，表示取不到有效值。
                :type Value: str
        """
        self.Key = None
        self.Value = None

    def _deserialize(self, params):
        self.Key = params.get("Key")
        self.Value = params.get("Value")


class TemplateLimit(AbstractModel):
    """参数模板配额"""

    def __init__(self):
        """
        :param AddressTemplateMemberLimit: 参数模板IP地址成员配额。
        :type AddressTemplateMemberLimit: int
        :param AddressTemplateGroupMemberLimit: 参数模板IP地址组成员配额。
        :type AddressTemplateGroupMemberLimit: int
        :param ServiceTemplateMemberLimit: 参数模板I协议端口成员配额。
        :type ServiceTemplateMemberLimit: int
        :param ServiceTemplateGroupMemberLimit: 参数模板协议端口组成员配额。
        :type ServiceTemplateGroupMemberLimit: int
        """
        self.AddressTemplateMemberLimit = None
        self.AddressTemplateGroupMemberLimit = None
        self.ServiceTemplateMemberLimit = None
        self.ServiceTemplateGroupMemberLimit = None

    def _deserialize(self, params):
        self.AddressTemplateMemberLimit = params.get("AddressTemplateMemberLimit")
        self.AddressTemplateGroupMemberLimit = params.get("AddressTemplateGroupMemberLimit")
        self.ServiceTemplateMemberLimit = params.get("ServiceTemplateMemberLimit")
        self.ServiceTemplateGroupMemberLimit = params.get("ServiceTemplateGroupMemberLimit")


class TrafficFlow(AbstractModel):
    """流量描述。"""

    def __init__(self):
        """
                :param Value: 实际流量，单位为 字节
                :type Value: int
                :param FormatValue: 格式化后的流量，单位见参数 FormatUnit
        注意：此字段可能返回 null，表示取不到有效值。
                :type FormatValue: float
                :param FormatUnit: 格式化后流量的单位
        注意：此字段可能返回 null，表示取不到有效值。
                :type FormatUnit: str
        """
        self.Value = None
        self.FormatValue = None
        self.FormatUnit = None

    def _deserialize(self, params):
        self.Value = params.get("Value")
        self.FormatValue = params.get("FormatValue")
        self.FormatUnit = params.get("FormatUnit")


class TrafficMirror(AbstractModel):
    """流量镜像实例"""

    def __init__(self):
        """
        :param VpcId: VPC实例ID
        :type VpcId: str
        :param TrafficMirrorId: 流量镜像实例
        :type TrafficMirrorId: str
        :param TrafficMirrorName: TrafficMirrorName
        :type TrafficMirrorName: str
        :param TrafficMirrorDescribe: 流量镜像描述
        :type TrafficMirrorDescribe: str
        :param State: 流量镜像状态
        :type State: str
        :param Direction: 流量镜像采集方向
        :type Direction: str
        :param CollectorSrcs: 流量镜像采集对象
        :type CollectorSrcs: list of str
        :param NatId: 流量镜像过滤的nat网关实例ID
        :type NatId: str
        :param CollectorNormalFilters: 流量镜像过滤的五元组规则
        :type CollectorNormalFilters: list of TrafficMirrorFilter
        :param CollectorTarget: 流量镜接收目标
        :type CollectorTarget: :class:`tcecloud.vpc.v20170312.models.TrafficMirrorTarget`
        :param CreateTime: 流量镜像创建时间
        :type CreateTime: str
        """
        self.VpcId = None
        self.TrafficMirrorId = None
        self.TrafficMirrorName = None
        self.TrafficMirrorDescribe = None
        self.State = None
        self.Direction = None
        self.CollectorSrcs = None
        self.NatId = None
        self.CollectorNormalFilters = None
        self.CollectorTarget = None
        self.CreateTime = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.TrafficMirrorId = params.get("TrafficMirrorId")
        self.TrafficMirrorName = params.get("TrafficMirrorName")
        self.TrafficMirrorDescribe = params.get("TrafficMirrorDescribe")
        self.State = params.get("State")
        self.Direction = params.get("Direction")
        self.CollectorSrcs = params.get("CollectorSrcs")
        self.NatId = params.get("NatId")
        if params.get("CollectorNormalFilters") is not None:
            self.CollectorNormalFilters = []
            for item in params.get("CollectorNormalFilters"):
                obj = TrafficMirrorFilter()
                obj._deserialize(item)
                self.CollectorNormalFilters.append(obj)
        if params.get("CollectorTarget") is not None:
            self.CollectorTarget = TrafficMirrorTarget()
            self.CollectorTarget._deserialize(params.get("CollectorTarget"))
        self.CreateTime = params.get("CreateTime")


class TrafficMirrorFilter(AbstractModel):
    """流量镜像五元组过滤规则对象"""

    def __init__(self):
        """
        :param SrcNet: 过滤规则的源网段
        :type SrcNet: str
        :param DstNet: 过滤规则的目的网段
        :type DstNet: str
        :param Protocol: 过滤规则的协议
        :type Protocol: str
        :param SrcPort: 过滤规则的源端口，默认值1-65535
        :type SrcPort: str
        :param DstPort: 过滤规则的目的端口，默认值1-65535
        :type DstPort: str
        """
        self.SrcNet = None
        self.DstNet = None
        self.Protocol = None
        self.SrcPort = None
        self.DstPort = None

    def _deserialize(self, params):
        self.SrcNet = params.get("SrcNet")
        self.DstNet = params.get("DstNet")
        self.Protocol = params.get("Protocol")
        self.SrcPort = params.get("SrcPort")
        self.DstPort = params.get("DstPort")


class TrafficMirrorTarget(AbstractModel):
    """流量镜像采集目标类型"""

    def __init__(self):
        """
        :param TargetIps: 流量镜像的接收IP
        :type TargetIps: list of str
        :param AlgHash: 流量镜像接收IP组，均衡规则，支持ENI/FIVE_TUPLE_FLOW
        :type AlgHash: str
        """
        self.TargetIps = None
        self.AlgHash = None

    def _deserialize(self, params):
        self.TargetIps = params.get("TargetIps")
        self.AlgHash = params.get("AlgHash")


class TrafficPackageResourceDeduction(AbstractModel):
    """共享流量包资源抵扣量"""

    def __init__(self):
        """
        :param ResourceId: 抵扣资源唯一ID
        :type ResourceId: str
        :param Deduction: 抵扣量
        :type Deduction: :class:`tcecloud.vpc.v20170312.models.TrafficFlow`
        """
        self.ResourceId = None
        self.Deduction = None

    def _deserialize(self, params):
        self.ResourceId = params.get("ResourceId")
        if params.get("Deduction") is not None:
            self.Deduction = TrafficFlow()
            self.Deduction._deserialize(params.get("Deduction"))


class TransformAddressRequest(AbstractModel):
    """TransformAddress请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 待操作有普通公网 IP 的实例 ID。实例 ID 形如：`ins-11112222`。可通过登录控制台查询，也可通过 DescribeInstances 接口返回值中的`InstanceId`获取。
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


class UnassignIpv6AddressesRequest(AbstractModel):
    """UnassignIpv6Addresses请求参数结构体"""

    def __init__(self):
        """
        :param NetworkInterfaceId: 弹性网卡实例`ID`，形如：`eni-m6dyj72l`。
        :type NetworkInterfaceId: str
        :param Ipv6Addresses: 指定的`IPv6`地址列表，单次最多指定10个。
        :type Ipv6Addresses: list of Ipv6Address
        """
        self.NetworkInterfaceId = None
        self.Ipv6Addresses = None

    def _deserialize(self, params):
        self.NetworkInterfaceId = params.get("NetworkInterfaceId")
        if params.get("Ipv6Addresses") is not None:
            self.Ipv6Addresses = []
            for item in params.get("Ipv6Addresses"):
                obj = Ipv6Address()
                obj._deserialize(item)
                self.Ipv6Addresses.append(obj)


class UnassignIpv6AddressesResponse(AbstractModel):
    """UnassignIpv6Addresses返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UnassignIpv6CidrBlockRequest(AbstractModel):
    """UnassignIpv6CidrBlock请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: `VPC`实例`ID`，形如：`vpc-f49l6u0z`。
        :type VpcId: str
        :param Ipv6CidrBlock: `IPv6`网段。形如：`3402:4e00:20:1000::/56`
        :type Ipv6CidrBlock: str
        """
        self.VpcId = None
        self.Ipv6CidrBlock = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.Ipv6CidrBlock = params.get("Ipv6CidrBlock")


class UnassignIpv6CidrBlockResponse(AbstractModel):
    """UnassignIpv6CidrBlock返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UnassignIpv6SubnetCidrBlockRequest(AbstractModel):
    """UnassignIpv6SubnetCidrBlock请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: 子网所在私有网络`ID`。形如：`vpc-f49l6u0z`。
        :type VpcId: str
        :param Ipv6SubnetCidrBlocks: `IPv6` 子网段列表。
        :type Ipv6SubnetCidrBlocks: list of Ipv6SubnetCidrBlock
        """
        self.VpcId = None
        self.Ipv6SubnetCidrBlocks = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        if params.get("Ipv6SubnetCidrBlocks") is not None:
            self.Ipv6SubnetCidrBlocks = []
            for item in params.get("Ipv6SubnetCidrBlocks"):
                obj = Ipv6SubnetCidrBlock()
                obj._deserialize(item)
                self.Ipv6SubnetCidrBlocks.append(obj)


class UnassignIpv6SubnetCidrBlockResponse(AbstractModel):
    """UnassignIpv6SubnetCidrBlock返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UnassignPrivateIpAddressesRequest(AbstractModel):
    """UnassignPrivateIpAddresses请求参数结构体"""

    def __init__(self):
        """
        :param NetworkInterfaceId: 弹性网卡实例ID，例如：eni-m6dyj72l。
        :type NetworkInterfaceId: str
        :param PrivateIpAddresses: 指定的内网IP信息，单次最多指定10个。
        :type PrivateIpAddresses: list of PrivateIpAddressSpecification
        """
        self.NetworkInterfaceId = None
        self.PrivateIpAddresses = None

    def _deserialize(self, params):
        self.NetworkInterfaceId = params.get("NetworkInterfaceId")
        if params.get("PrivateIpAddresses") is not None:
            self.PrivateIpAddresses = []
            for item in params.get("PrivateIpAddresses"):
                obj = PrivateIpAddressSpecification()
                obj._deserialize(item)
                self.PrivateIpAddresses.append(obj)


class UnassignPrivateIpAddressesResponse(AbstractModel):
    """UnassignPrivateIpAddresses返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpdateCcnBandwidthRequest(AbstractModel):
    """UpdateCcnBandwidth请求参数结构体"""

    def __init__(self):
        """
        :param RenewFlag: 是否自动续费标识；NOTIFY_AND_AUTO_RENEW：自动续费，NOTIFY_AND_MANUAL_RENEW：手动续费。
        :type RenewFlag: str
        :param RegionFlowControlId: 流量配置ID。
        :type RegionFlowControlId: str
        :param MaxBandwidthLimit: 地域间设置带宽，单位：Mbps。
        :type MaxBandwidthLimit: int
        """
        self.RenewFlag = None
        self.RegionFlowControlId = None
        self.MaxBandwidthLimit = None

    def _deserialize(self, params):
        self.RenewFlag = params.get("RenewFlag")
        self.RegionFlowControlId = params.get("RegionFlowControlId")
        self.MaxBandwidthLimit = params.get("MaxBandwidthLimit")


class UpdateCcnBandwidthResponse(AbstractModel):
    """UpdateCcnBandwidth返回参数结构体"""

    def __init__(self):
        """
        :param DealName: 订单号。
        :type DealName: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DealName = None
        self.RequestId = None

    def _deserialize(self, params):
        self.DealName = params.get("DealName")
        self.RequestId = params.get("RequestId")


class UpdateTrafficMirrorAllFilterRequest(AbstractModel):
    """UpdateTrafficMirrorAllFilter请求参数结构体"""

    def __init__(self):
        """
        :param TrafficMirrorId: 流量镜像实例ID
        :type TrafficMirrorId: str
        :param Direction: 流量镜像采集方向
        :type Direction: str
        :param CollectorSrcs: 流量镜像采集对象
        :type CollectorSrcs: list of str
        :param NatId: 流量镜像需要过滤的natgw实例
        :type NatId: str
        :param CollectorNormalFilters: 流量镜像需要过滤的五元组规则
        :type CollectorNormalFilters: list of TrafficMirrorFilter
        """
        self.TrafficMirrorId = None
        self.Direction = None
        self.CollectorSrcs = None
        self.NatId = None
        self.CollectorNormalFilters = None

    def _deserialize(self, params):
        self.TrafficMirrorId = params.get("TrafficMirrorId")
        self.Direction = params.get("Direction")
        self.CollectorSrcs = params.get("CollectorSrcs")
        self.NatId = params.get("NatId")
        if params.get("CollectorNormalFilters") is not None:
            self.CollectorNormalFilters = []
            for item in params.get("CollectorNormalFilters"):
                obj = TrafficMirrorFilter()
                obj._deserialize(item)
                self.CollectorNormalFilters.append(obj)


class UpdateTrafficMirrorAllFilterResponse(AbstractModel):
    """UpdateTrafficMirrorAllFilter返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpdateTrafficMirrorDirectionRequest(AbstractModel):
    """UpdateTrafficMirrorDirection请求参数结构体"""

    def __init__(self):
        """
        :param TrafficMirrorId: 流量镜像实例ID
        :type TrafficMirrorId: str
        :param Direction: 流量镜像采集方向
        :type Direction: str
        """
        self.TrafficMirrorId = None
        self.Direction = None

    def _deserialize(self, params):
        self.TrafficMirrorId = params.get("TrafficMirrorId")
        self.Direction = params.get("Direction")


class UpdateTrafficMirrorDirectionResponse(AbstractModel):
    """UpdateTrafficMirrorDirection返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UsedDetail(AbstractModel):
    """共享流量包用量明细"""

    def __init__(self):
        """
                :param TrafficPackageId: 流量包唯一ID
                :type TrafficPackageId: str
                :param TrafficPackageName: 流量包名称
        注意：此字段可能返回 null，表示取不到有效值。
                :type TrafficPackageName: str
                :param TotalAmount: 流量包总量
                :type TotalAmount: :class:`tcecloud.vpc.v20170312.models.TrafficFlow`
                :param Deduction: 本次抵扣
                :type Deduction: :class:`tcecloud.vpc.v20170312.models.TrafficFlow`
                :param RemainingAmount: 本次抵扣后剩余量
                :type RemainingAmount: :class:`tcecloud.vpc.v20170312.models.TrafficFlow`
                :param Time: 抵扣时间
                :type Time: str
                :param ResourceType: 资源类型
                :type ResourceType: str
                :param ResourceId: 资源ID
                :type ResourceId: str
                :param ResourceName: 资源名称
                :type ResourceName: str
                :param Deadline: 流量包到期时间
                :type Deadline: str
        """
        self.TrafficPackageId = None
        self.TrafficPackageName = None
        self.TotalAmount = None
        self.Deduction = None
        self.RemainingAmount = None
        self.Time = None
        self.ResourceType = None
        self.ResourceId = None
        self.ResourceName = None
        self.Deadline = None

    def _deserialize(self, params):
        self.TrafficPackageId = params.get("TrafficPackageId")
        self.TrafficPackageName = params.get("TrafficPackageName")
        if params.get("TotalAmount") is not None:
            self.TotalAmount = TrafficFlow()
            self.TotalAmount._deserialize(params.get("TotalAmount"))
        if params.get("Deduction") is not None:
            self.Deduction = TrafficFlow()
            self.Deduction._deserialize(params.get("Deduction"))
        if params.get("RemainingAmount") is not None:
            self.RemainingAmount = TrafficFlow()
            self.RemainingAmount._deserialize(params.get("RemainingAmount"))
        self.Time = params.get("Time")
        self.ResourceType = params.get("ResourceType")
        self.ResourceId = params.get("ResourceId")
        self.ResourceName = params.get("ResourceName")
        self.Deadline = params.get("Deadline")


class UsedDetailDownload(AbstractModel):
    """共享流量包的用量明细文件生成历史"""

    def __init__(self):
        """
                :param Id: 生成历史唯一ID
                :type Id: int
                :param TrafficPackageId: 共享流量包唯一ID
                :type TrafficPackageId: str
                :param StartTime: 开始时间
                :type StartTime: str
                :param EndTime: 结束时间
                :type EndTime: str
                :param DownloadUrl: 下载链接
        注意：此字段可能返回 null，表示取不到有效值。
                :type DownloadUrl: str
                :param Filename: 文件名称
                :type Filename: str
                :param Status: 任务状态. RUNNING-正在生成， SUCCESS-成功， FAIL-失败
                :type Status: str
                :param ErrorMsg: 错误信息
        注意：此字段可能返回 null，表示取不到有效值。
                :type ErrorMsg: str
                :param ExpiredAt: 下载链接过期时间
        注意：此字段可能返回 null，表示取不到有效值。
                :type ExpiredAt: str
                :param CreatedAt: 文件生成时间
                :type CreatedAt: str
                :param IsExpired: 下载链接是否已经过期
        注意：此字段可能返回 null，表示取不到有效值。
                :type IsExpired: bool
        """
        self.Id = None
        self.TrafficPackageId = None
        self.StartTime = None
        self.EndTime = None
        self.DownloadUrl = None
        self.Filename = None
        self.Status = None
        self.ErrorMsg = None
        self.ExpiredAt = None
        self.CreatedAt = None
        self.IsExpired = None

    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.TrafficPackageId = params.get("TrafficPackageId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.DownloadUrl = params.get("DownloadUrl")
        self.Filename = params.get("Filename")
        self.Status = params.get("Status")
        self.ErrorMsg = params.get("ErrorMsg")
        self.ExpiredAt = params.get("ExpiredAt")
        self.CreatedAt = params.get("CreatedAt")
        self.IsExpired = params.get("IsExpired")


class Vpc(AbstractModel):
    """私有网络(VPC)对象。"""

    def __init__(self):
        """
                :param VpcName: `VPC`名称。
                :type VpcName: str
                :param VpcId: `VPC`实例`ID`，例如：vpc-azd4dt1c。
                :type VpcId: str
                :param CidrBlock: `VPC`的`IPv4` `CIDR`。
                :type CidrBlock: str
                :param IsDefault: 是否默认`VPC`。
                :type IsDefault: bool
                :param EnableMulticast: 是否开启组播。
                :type EnableMulticast: bool
                :param CreatedTime: 创建时间。
                :type CreatedTime: str
                :param DnsServerSet: `DNS`列表。
                :type DnsServerSet: list of str
                :param DomainName: `DHCP`域名选项值。
                :type DomainName: str
                :param DhcpOptionsId: `DHCP`选项集`ID`。
                :type DhcpOptionsId: str
                :param EnableDhcp: 是否开启`DHCP`。
                :type EnableDhcp: bool
                :param Ipv6CidrBlock: `VPC`的`IPv6` `CIDR`。
                :type Ipv6CidrBlock: str
                :param TagSet: 标签键值对
                :type TagSet: list of Tag
                :param AssistantCidrSet: 辅助CIDR
        注意：此字段可能返回 null，表示取不到有效值。
                :type AssistantCidrSet: list of AssistantCidr
        """
        self.VpcName = None
        self.VpcId = None
        self.CidrBlock = None
        self.IsDefault = None
        self.EnableMulticast = None
        self.CreatedTime = None
        self.DnsServerSet = None
        self.DomainName = None
        self.DhcpOptionsId = None
        self.EnableDhcp = None
        self.Ipv6CidrBlock = None
        self.TagSet = None
        self.AssistantCidrSet = None

    def _deserialize(self, params):
        self.VpcName = params.get("VpcName")
        self.VpcId = params.get("VpcId")
        self.CidrBlock = params.get("CidrBlock")
        self.IsDefault = params.get("IsDefault")
        self.EnableMulticast = params.get("EnableMulticast")
        self.CreatedTime = params.get("CreatedTime")
        self.DnsServerSet = params.get("DnsServerSet")
        self.DomainName = params.get("DomainName")
        self.DhcpOptionsId = params.get("DhcpOptionsId")
        self.EnableDhcp = params.get("EnableDhcp")
        self.Ipv6CidrBlock = params.get("Ipv6CidrBlock")
        if params.get("TagSet") is not None:
            self.TagSet = []
            for item in params.get("TagSet"):
                obj = Tag()
                obj._deserialize(item)
                self.TagSet.append(obj)
        if params.get("AssistantCidrSet") is not None:
            self.AssistantCidrSet = []
            for item in params.get("AssistantCidrSet"):
                obj = AssistantCidr()
                obj._deserialize(item)
                self.AssistantCidrSet.append(obj)


class VpcExtendCidr(AbstractModel):
    """vpc扩展的CIDR"""

    def __init__(self):
        """
        :param VpcId: vpcId
        :type VpcId: str
        :param CidrBlock: CIDR
        :type CidrBlock: str
        :param CreateTime: 创建时间
        :type CreateTime: str
        """
        self.VpcId = None
        self.CidrBlock = None
        self.CreateTime = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.CidrBlock = params.get("CidrBlock")
        self.CreateTime = params.get("CreateTime")


class VpcGateway(AbstractModel):
    """VPC下的网关信息"""

    def __init__(self):
        """
        :param SubnetId: 子网实例ID。
        :type SubnetId: str
        :param Pip: 内网IP地址。
        :type Pip: str
        :param WanIp: 公网IP地址。
        :type WanIp: str
        """
        self.SubnetId = None
        self.Pip = None
        self.WanIp = None

    def _deserialize(self, params):
        self.SubnetId = params.get("SubnetId")
        self.Pip = params.get("Pip")
        self.WanIp = params.get("WanIp")


class VpcGlobalExtendCidr(AbstractModel):
    """查询VPC全局扩展cidr段"""

    def __init__(self):
        """
        :param Subnet: subnet值
        :type Subnet: str
        :param Mask: 子网掩码
        :type Mask: str
        :param IntMask: 整型子网掩码
        :type IntMask: int
        :param CreateTime: 创建时间
        :type CreateTime: str
        """
        self.Subnet = None
        self.Mask = None
        self.IntMask = None
        self.CreateTime = None

    def _deserialize(self, params):
        self.Subnet = params.get("Subnet")
        self.Mask = params.get("Mask")
        self.IntMask = params.get("IntMask")
        self.CreateTime = params.get("CreateTime")


class VpcIpv6Address(AbstractModel):
    """VPC内网IPv6对象。"""

    def __init__(self):
        """
        :param Ipv6Address: `VPC`内`IPv6`地址。
        :type Ipv6Address: str
        :param CidrBlock: 所属子网 `IPv6` `CIDR`。
        :type CidrBlock: str
        :param Ipv6AddressType: `IPv6`类型。
        :type Ipv6AddressType: str
        :param CreatedTime: `IPv6`申请时间。
        :type CreatedTime: str
        """
        self.Ipv6Address = None
        self.CidrBlock = None
        self.Ipv6AddressType = None
        self.CreatedTime = None

    def _deserialize(self, params):
        self.Ipv6Address = params.get("Ipv6Address")
        self.CidrBlock = params.get("CidrBlock")
        self.Ipv6AddressType = params.get("Ipv6AddressType")
        self.CreatedTime = params.get("CreatedTime")


class VpcLimit(AbstractModel):
    """私有网络配额"""

    def __init__(self):
        """
        :param LimitType: 私有网络配额描述
        :type LimitType: str
        :param LimitValue: 私有网络配额值
        :type LimitValue: int
        """
        self.LimitType = None
        self.LimitValue = None

    def _deserialize(self, params):
        self.LimitType = params.get("LimitType")
        self.LimitValue = params.get("LimitValue")


class VpcNum(AbstractModel):
    """vpc数字ID"""

    def __init__(self):
        """
        :param VpcId: VPC实例ID。
        :type VpcId: str
        :param VpcNumId: VPC实例数字ID。
        :type VpcNumId: int
        """
        self.VpcId = None
        self.VpcNumId = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.VpcNumId = params.get("VpcNumId")


class VpcPrivateIpAddress(AbstractModel):
    """VPC内网IP对象。"""

    def __init__(self):
        """
        :param PrivateIpAddress: `VPC`内网`IP`。
        :type PrivateIpAddress: str
        :param CidrBlock: 所属子网`CIDR`。
        :type CidrBlock: str
        :param PrivateIpAddressType: 内网`IP`类型。
        :type PrivateIpAddressType: str
        :param CreatedTime: `IP`申请时间。
        :type CreatedTime: str
        """
        self.PrivateIpAddress = None
        self.CidrBlock = None
        self.PrivateIpAddressType = None
        self.CreatedTime = None

    def _deserialize(self, params):
        self.PrivateIpAddress = params.get("PrivateIpAddress")
        self.CidrBlock = params.get("CidrBlock")
        self.PrivateIpAddressType = params.get("PrivateIpAddressType")
        self.CreatedTime = params.get("CreatedTime")


class VpnConnection(AbstractModel):
    """VPN通道对象。"""

    def __init__(self):
        """
        :param VpnConnectionId: 通道实例ID。
        :type VpnConnectionId: str
        :param VpnConnectionName: 通道名称。
        :type VpnConnectionName: str
        :param VpcId: VPC实例ID。
        :type VpcId: str
        :param VpnGatewayId: VPN网关实例ID。
        :type VpnGatewayId: str
        :param CustomerGatewayId: 对端网关实例ID。
        :type CustomerGatewayId: str
        :param PreShareKey: 预共享密钥。
        :type PreShareKey: str
        :param VpnProto: 通道传输协议。
        :type VpnProto: str
        :param EncryptProto: 通道加密协议。
        :type EncryptProto: str
        :param RouteType: 路由类型。
        :type RouteType: str
        :param CreatedTime: 创建时间。
        :type CreatedTime: str
        :param State: 通道的生产状态，PENDING：生产中，AVAILABLE：运行中，DELETING：删除中。
        :type State: str
        :param NetStatus: 通道连接状态，AVAILABLE：已连接。
        :type NetStatus: str
        :param SecurityPolicyDatabaseSet: SPD。
        :type SecurityPolicyDatabaseSet: list of SecurityPolicyDatabase
        :param IKEOptionsSpecification: IKE选项。
        :type IKEOptionsSpecification: :class:`tcecloud.vpc.v20170312.models.IKEOptionsSpecification`
        :param IPSECOptionsSpecification: IPSEC选择。
        :type IPSECOptionsSpecification: :class:`tcecloud.vpc.v20170312.models.IPSECOptionsSpecification`
        """
        self.VpnConnectionId = None
        self.VpnConnectionName = None
        self.VpcId = None
        self.VpnGatewayId = None
        self.CustomerGatewayId = None
        self.PreShareKey = None
        self.VpnProto = None
        self.EncryptProto = None
        self.RouteType = None
        self.CreatedTime = None
        self.State = None
        self.NetStatus = None
        self.SecurityPolicyDatabaseSet = None
        self.IKEOptionsSpecification = None
        self.IPSECOptionsSpecification = None

    def _deserialize(self, params):
        self.VpnConnectionId = params.get("VpnConnectionId")
        self.VpnConnectionName = params.get("VpnConnectionName")
        self.VpcId = params.get("VpcId")
        self.VpnGatewayId = params.get("VpnGatewayId")
        self.CustomerGatewayId = params.get("CustomerGatewayId")
        self.PreShareKey = params.get("PreShareKey")
        self.VpnProto = params.get("VpnProto")
        self.EncryptProto = params.get("EncryptProto")
        self.RouteType = params.get("RouteType")
        self.CreatedTime = params.get("CreatedTime")
        self.State = params.get("State")
        self.NetStatus = params.get("NetStatus")
        if params.get("SecurityPolicyDatabaseSet") is not None:
            self.SecurityPolicyDatabaseSet = []
            for item in params.get("SecurityPolicyDatabaseSet"):
                obj = SecurityPolicyDatabase()
                obj._deserialize(item)
                self.SecurityPolicyDatabaseSet.append(obj)
        if params.get("IKEOptionsSpecification") is not None:
            self.IKEOptionsSpecification = IKEOptionsSpecification()
            self.IKEOptionsSpecification._deserialize(params.get("IKEOptionsSpecification"))
        if params.get("IPSECOptionsSpecification") is not None:
            self.IPSECOptionsSpecification = IPSECOptionsSpecification()
            self.IPSECOptionsSpecification._deserialize(params.get("IPSECOptionsSpecification"))


class VpnGateway(AbstractModel):
    """VPN网关对象。"""

    def __init__(self):
        """
        :param VpnGatewayId: 网关实例ID。
        :type VpnGatewayId: str
        :param VpcId: VPC实例ID。
        :type VpcId: str
        :param VpnGatewayName: 网关实例名称。
        :type VpnGatewayName: str
        :param Type: 网关实例类型：'IPSEC', 'SSL','CCN'。
        :type Type: str
        :param State: 网关实例状态， 'PENDING'：生产中，'DELETING'：删除中，'AVAILABLE'：运行中。
        :type State: str
        :param PublicIpAddress: 网关公网IP。
        :type PublicIpAddress: str
        :param RenewFlag: 网关续费类型：'NOTIFY_AND_MANUAL_RENEW'：手动续费，'NOTIFY_AND_AUTO_RENEW'：自动续费，'NOT_NOTIFY_AND_NOT_RENEW'：到期不续费。
        :type RenewFlag: str
        :param InstanceChargeType: 网关付费类型：POSTPAID_BY_HOUR：按小时后付费，PREPAID：包年包月预付费，
        :type InstanceChargeType: str
        :param InternetMaxBandwidthOut: 网关出带宽。
        :type InternetMaxBandwidthOut: int
        :param CreatedTime: 创建时间。
        :type CreatedTime: str
        :param ExpiredTime: 预付费网关过期时间。
        :type ExpiredTime: str
        :param IsAddressBlocked: 公网IP是否被封堵。
        :type IsAddressBlocked: bool
        :param NewPurchasePlan: 计费模式变更，PREPAID_TO_POSTPAID：包年包月预付费到期转按小时后付费。
        :type NewPurchasePlan: str
        :param RestrictState: 网关计费装，PROTECTIVELY_ISOLATED：被安全隔离的实例，NORMAL：正常。
        :type RestrictState: str
        :param Zone: 可用区，如：ap-guangzhou-2
        :type Zone: str
        :param VpnGatewayQuotaSet: 网关带宽配额信息
        :type VpnGatewayQuotaSet: list of VpnGatewayQuota
        :param Version: 网关实例版本信息
        :type Version: str
        :param NetworkInstanceId: Type值为CCN时，该值表示云联网实例ID
        :type NetworkInstanceId: str
        """
        self.VpnGatewayId = None
        self.VpcId = None
        self.VpnGatewayName = None
        self.Type = None
        self.State = None
        self.PublicIpAddress = None
        self.RenewFlag = None
        self.InstanceChargeType = None
        self.InternetMaxBandwidthOut = None
        self.CreatedTime = None
        self.ExpiredTime = None
        self.IsAddressBlocked = None
        self.NewPurchasePlan = None
        self.RestrictState = None
        self.Zone = None
        self.VpnGatewayQuotaSet = None
        self.Version = None
        self.NetworkInstanceId = None

    def _deserialize(self, params):
        self.VpnGatewayId = params.get("VpnGatewayId")
        self.VpcId = params.get("VpcId")
        self.VpnGatewayName = params.get("VpnGatewayName")
        self.Type = params.get("Type")
        self.State = params.get("State")
        self.PublicIpAddress = params.get("PublicIpAddress")
        self.RenewFlag = params.get("RenewFlag")
        self.InstanceChargeType = params.get("InstanceChargeType")
        self.InternetMaxBandwidthOut = params.get("InternetMaxBandwidthOut")
        self.CreatedTime = params.get("CreatedTime")
        self.ExpiredTime = params.get("ExpiredTime")
        self.IsAddressBlocked = params.get("IsAddressBlocked")
        self.NewPurchasePlan = params.get("NewPurchasePlan")
        self.RestrictState = params.get("RestrictState")
        self.Zone = params.get("Zone")
        if params.get("VpnGatewayQuotaSet") is not None:
            self.VpnGatewayQuotaSet = []
            for item in params.get("VpnGatewayQuotaSet"):
                obj = VpnGatewayQuota()
                obj._deserialize(item)
                self.VpnGatewayQuotaSet.append(obj)
        self.Version = params.get("Version")
        self.NetworkInstanceId = params.get("NetworkInstanceId")


class VpnGatewayQuota(AbstractModel):
    """VPN网关配额对象"""

    def __init__(self):
        """
        :param Bandwidth: 带宽配额
        :type Bandwidth: int
        :param Cname: 配额中文名称
        :type Cname: str
        :param Name: 配额英文名称
        :type Name: str
        """
        self.Bandwidth = None
        self.Cname = None
        self.Name = None

    def _deserialize(self, params):
        self.Bandwidth = params.get("Bandwidth")
        self.Cname = params.get("Cname")
        self.Name = params.get("Name")


class VpngwCcnRoutes(AbstractModel):
    """VPN网关云联网路由信息"""

    def __init__(self):
        """
                :param RouteId: 路由信息ID
                :type RouteId: str
                :param Status: 路由信息是否启用
        ENABLE：启用该路由
        DISABLE：不启用该路由
                :type Status: str
        """
        self.RouteId = None
        self.Status = None

    def _deserialize(self, params):
        self.RouteId = params.get("RouteId")
        self.Status = params.get("Status")


class ZoneInfo(AbstractModel):
    """EIP可用区列表信息"""

    def __init__(self):
        """
        :param Zone: 可用区名称，例如，ap-guangzhou-1
        :type Zone: str
        :param ZoneName: 可用区描述，例如，广州一区
        :type ZoneName: str
        :param ZoneId: 可用区ID
        :type ZoneId: int
        :param ZoneState: 可用区状态，目前只有两种状态，分别是UNAVAILABLE和AVAILABLE
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

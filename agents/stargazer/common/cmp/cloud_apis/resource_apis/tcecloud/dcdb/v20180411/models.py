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


class ActiveDedicatedDBInstanceRequest(AbstractModel):
    """ActiveDedicatedDBInstance请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID列表，形如：dcdbt-ow728lmc。
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class ActiveDedicatedDBInstanceResponse(AbstractModel):
    """ActiveDedicatedDBInstance返回参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例Id，透传入参
        :type InstanceId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.RequestId = params.get("RequestId")


class ActiveHourDCDBInstanceRequest(AbstractModel):
    """ActiveHourDCDBInstance请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID，形如dcdbt-87zif6ha
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class ActiveHourDCDBInstanceResponse(AbstractModel):
    """ActiveHourDCDBInstance返回参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID，形如dcdbt-87zif6ha
        :type InstanceId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.RequestId = params.get("RequestId")


class AddShardConfig(AbstractModel):
    """升级实例 -- 新增分片类型"""

    def __init__(self):
        """
        :param ShardCount: 新增分片的数量
        :type ShardCount: int
        :param ShardMemory: 分片内存大小，单位 GB
        :type ShardMemory: int
        :param ShardStorage: 分片存储大小，单位 GB
        :type ShardStorage: int
        """
        self.ShardCount = None
        self.ShardMemory = None
        self.ShardStorage = None

    def _deserialize(self, params):
        self.ShardCount = params.get("ShardCount")
        self.ShardMemory = params.get("ShardMemory")
        self.ShardStorage = params.get("ShardStorage")


class AuditLog(AbstractModel):
    """审计日志"""

    def __init__(self):
        """
        :param InstanceType: 实例类型
        :type InstanceType: int
        :param AppId: 应用id
        :type AppId: int
        :param DbName: 操作的数据库
        :type DbName: str
        :param User: 操作用户
        :type User: str
        :param Sql: sql语句
        :type Sql: str
        :param MatchRule: 匹配规则
        :type MatchRule: str
        :param ClientIpPort: 客户端ip 端口
        :type ClientIpPort: str
        :param ReceiveTime: sql接收时间
        :type ReceiveTime: int
        :param ReceiveTimeStr: sql接收时间字符串
        :type ReceiveTimeStr: str
        :param CostTime: 花费时间
        :type CostTime: int
        :param RowsEffected: 影响行数
        :type RowsEffected: int
        :param ResultCode: 执行结果
        :type ResultCode: int
        :param SqlType: sql类型
        :type SqlType: str
        :param TableName: 操作表名
        :type TableName: str
        :param StrategyName: 策略名称
        :type StrategyName: str
        :param InstanceName: 实例名称
        :type InstanceName: str
        :param InstanceId: 实例Id
        :type InstanceId: str
        """
        self.InstanceType = None
        self.AppId = None
        self.DbName = None
        self.User = None
        self.Sql = None
        self.MatchRule = None
        self.ClientIpPort = None
        self.ReceiveTime = None
        self.ReceiveTimeStr = None
        self.CostTime = None
        self.RowsEffected = None
        self.ResultCode = None
        self.SqlType = None
        self.TableName = None
        self.StrategyName = None
        self.InstanceName = None
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceType = params.get("InstanceType")
        self.AppId = params.get("AppId")
        self.DbName = params.get("DbName")
        self.User = params.get("User")
        self.Sql = params.get("Sql")
        self.MatchRule = params.get("MatchRule")
        self.ClientIpPort = params.get("ClientIpPort")
        self.ReceiveTime = params.get("ReceiveTime")
        self.ReceiveTimeStr = params.get("ReceiveTimeStr")
        self.CostTime = params.get("CostTime")
        self.RowsEffected = params.get("RowsEffected")
        self.ResultCode = params.get("ResultCode")
        self.SqlType = params.get("SqlType")
        self.TableName = params.get("TableName")
        self.StrategyName = params.get("StrategyName")
        self.InstanceName = params.get("InstanceName")
        self.InstanceId = params.get("InstanceId")


class AuditRule(AbstractModel):
    """审计规则"""

    def __init__(self):
        """
        :param Id: 规则Id
        :type Id: int
        :param Name: 规则名称
        :type Name: str
        :param CreateTime: 规则创建时间
        :type CreateTime: str
        :param UpdateTime: 规则更新时间
        :type UpdateTime: str
        :param Description: 规则描述
        :type Description: str
        :param AppId: 应用Id
        :type AppId: int
        :param DbType: db类型
        :type DbType: int
        :param Filters: 审计规则
        :type Filters: str
        :param Status: 规则状态
        :type Status: int
        """
        self.Id = None
        self.Name = None
        self.CreateTime = None
        self.UpdateTime = None
        self.Description = None
        self.AppId = None
        self.DbType = None
        self.Filters = None
        self.Status = None

    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Name = params.get("Name")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.Description = params.get("Description")
        self.AppId = params.get("AppId")
        self.DbType = params.get("DbType")
        self.Filters = params.get("Filters")
        self.Status = params.get("Status")


class AuditRuleDetail(AbstractModel):
    """审计规则详情"""

    def __init__(self):
        """
        :param Id: 规则Id
        :type Id: int
        :param Name: 规则名称
        :type Name: str
        :param CreateTime: 创建时间
        :type CreateTime: str
        :param UpdateTime: 更新时间
        :type UpdateTime: str
        :param Description: 规则描述
        :type Description: str
        :param AppId: 应用Id
        :type AppId: int
        :param DbType: db类型
        :type DbType: int
        :param Filters: 规则
        :type Filters: str
        :param Status: 规则状态
        :type Status: int
        :param Rules: 规则列表
        :type Rules: list of RuleItem
        """
        self.Id = None
        self.Name = None
        self.CreateTime = None
        self.UpdateTime = None
        self.Description = None
        self.AppId = None
        self.DbType = None
        self.Filters = None
        self.Status = None
        self.Rules = None

    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Name = params.get("Name")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.Description = params.get("Description")
        self.AppId = params.get("AppId")
        self.DbType = params.get("DbType")
        self.Filters = params.get("Filters")
        self.Status = params.get("Status")
        if params.get("Rules") is not None:
            self.Rules = []
            for item in params.get("Rules"):
                obj = RuleItem()
                obj._deserialize(item)
                self.Rules.append(obj)


class AuditStrategy(AbstractModel):
    """审计策略"""

    def __init__(self):
        """
        :param Id: 策略Id
        :type Id: int
        :param Name: 策略名称
        :type Name: str
        :param Description: 策略描述
        :type Description: str
        :param AppId: 应用Id
        :type AppId: int
        :param InstanceId: 实例Id
        :type InstanceId: str
        :param RuleName: 规则名称
        :type RuleName: str
        :param AlterType: 响应策略，0放行，1不放行
        :type AlterType: int
        :param ActionType: 脱敏记录，0不脱敏，1脱敏
        :type ActionType: int
        :param Status: 策略状态，0不启用，1启用
        :type Status: int
        :param Priority: 优先顺序
        :type Priority: int
        :param CreateTime: 创建时间
        :type CreateTime: str
        :param UpdateTime: 更新时间
        :type UpdateTime: str
        """
        self.Id = None
        self.Name = None
        self.Description = None
        self.AppId = None
        self.InstanceId = None
        self.RuleName = None
        self.AlterType = None
        self.ActionType = None
        self.Status = None
        self.Priority = None
        self.CreateTime = None
        self.UpdateTime = None

    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Name = params.get("Name")
        self.Description = params.get("Description")
        self.AppId = params.get("AppId")
        self.InstanceId = params.get("InstanceId")
        self.RuleName = params.get("RuleName")
        self.AlterType = params.get("AlterType")
        self.ActionType = params.get("ActionType")
        self.Status = params.get("Status")
        self.Priority = params.get("Priority")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")


class AuthenticateCAMRequest(AbstractModel):
    """AuthenticateCAM请求参数结构体"""

    def __init__(self):
        """
        :param ApiName: 待鉴权的接口名，如 CreateDCDBInstance
        :type ApiName: str
        :param Resources: 待鉴权资源信息，cam 六段式资源格式或 *
        :type Resources: list of str
        """
        self.ApiName = None
        self.Resources = None

    def _deserialize(self, params):
        self.ApiName = params.get("ApiName")
        self.Resources = params.get("Resources")


class AuthenticateCAMResponse(AbstractModel):
    """AuthenticateCAM返回参数结构体"""

    def __init__(self):
        """
        :param IsRoot: 当前请求账号是否为根账号
        :type IsRoot: int
        :param IsAllPass: 当前请求账号是否有全部权限
        :type IsAllPass: int
        :param OwnerAppId: 主账号的appId
        :type OwnerAppId: int
        :param Permissions: 权限详情
        :type Permissions: list of Permission
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.IsRoot = None
        self.IsAllPass = None
        self.OwnerAppId = None
        self.Permissions = None
        self.RequestId = None

    def _deserialize(self, params):
        self.IsRoot = params.get("IsRoot")
        self.IsAllPass = params.get("IsAllPass")
        self.OwnerAppId = params.get("OwnerAppId")
        if params.get("Permissions") is not None:
            self.Permissions = []
            for item in params.get("Permissions"):
                obj = Permission()
                obj._deserialize(item)
                self.Permissions.append(obj)
        self.RequestId = params.get("RequestId")


class CheckIpStatusRequest(AbstractModel):
    """CheckIpStatus请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例Id，形如：dcdbt-ow728lmc
        :type InstanceId: str
        :param VpcId: 目标私有网络ID
        :type VpcId: str
        :param SubnetId: 目标子网ID
        :type SubnetId: str
        :param Vip: 目标虚拟IP
        :type Vip: str
        """
        self.InstanceId = None
        self.VpcId = None
        self.SubnetId = None
        self.Vip = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.Vip = params.get("Vip")


class CheckIpStatusResponse(AbstractModel):
    """CheckIpStatus返回参数结构体"""

    def __init__(self):
        """
        :param Vip: 透传入参
        :type Vip: str
        :param Status: Vip可用状态：0 - 可用，300 - 此ip已被子网内其他用户占用， 301 - 此ip不在子网内， 302 - ip格式错误， 303 - 该IP为实例当前IP。
        :type Status: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Vip = None
        self.Status = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Vip = params.get("Vip")
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class CloneAccountRequest(AbstractModel):
    """CloneAccount请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID
        :type InstanceId: str
        :param SrcUser: 源用户账户名
        :type SrcUser: str
        :param SrcHost: 源用户HOST
        :type SrcHost: str
        :param DstUser: 目的用户账户名
        :type DstUser: str
        :param DstHost: 目的用户HOST
        :type DstHost: str
        :param DstDesc: 目的用户账户描述
        :type DstDesc: str
        """
        self.InstanceId = None
        self.SrcUser = None
        self.SrcHost = None
        self.DstUser = None
        self.DstHost = None
        self.DstDesc = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.SrcUser = params.get("SrcUser")
        self.SrcHost = params.get("SrcHost")
        self.DstUser = params.get("DstUser")
        self.DstHost = params.get("DstHost")
        self.DstDesc = params.get("DstDesc")


class CloneAccountResponse(AbstractModel):
    """CloneAccount返回参数结构体"""

    def __init__(self):
        """
        :param FlowId: 异步任务流程ID
        :type FlowId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class CloseDBExtranetAccessRequest(AbstractModel):
    """CloseDBExtranetAccess请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 待关闭外网访问的实例ID。形如：dcdbt-ow728lmc，可以通过 DescribeDCDBInstances 查询实例详情获得。
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class CloseDBExtranetAccessResponse(AbstractModel):
    """CloseDBExtranetAccess返回参数结构体"""

    def __init__(self):
        """
        :param FlowId: 异步任务Id，可通过 DescribeFlow 查询任务状态。
        :type FlowId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class ConstraintRange(AbstractModel):
    """约束类型值的范围"""

    def __init__(self):
        """
        :param Min: 约束类型为section时的最小值
        :type Min: str
        :param Max: 约束类型为section时的最大值
        :type Max: str
        """
        self.Min = None
        self.Max = None

    def _deserialize(self, params):
        self.Min = params.get("Min")
        self.Max = params.get("Max")


class CopyAccountPrivilegesRequest(AbstractModel):
    """CopyAccountPrivileges请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：dcdbt-ow728lmc。
        :type InstanceId: str
        :param SrcUserName: 源用户名
        :type SrcUserName: str
        :param SrcHost: 源用户允许的访问 host
        :type SrcHost: str
        :param DstUserName: 目的用户名
        :type DstUserName: str
        :param DstHost: 目的用户允许的访问 host
        :type DstHost: str
        :param SrcReadOnly: 源账号的 ReadOnly 属性
        :type SrcReadOnly: str
        :param DstReadOnly: 目的账号的 ReadOnly 属性
        :type DstReadOnly: str
        """
        self.InstanceId = None
        self.SrcUserName = None
        self.SrcHost = None
        self.DstUserName = None
        self.DstHost = None
        self.SrcReadOnly = None
        self.DstReadOnly = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.SrcUserName = params.get("SrcUserName")
        self.SrcHost = params.get("SrcHost")
        self.DstUserName = params.get("DstUserName")
        self.DstHost = params.get("DstHost")
        self.SrcReadOnly = params.get("SrcReadOnly")
        self.DstReadOnly = params.get("DstReadOnly")


class CopyAccountPrivilegesResponse(AbstractModel):
    """CopyAccountPrivileges返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateAccountRequest(AbstractModel):
    """CreateAccount请求参数结构体"""

    def __init__(self):
        """
                :param InstanceId: 实例 ID，形如：dcdbt-ow728lmc，可以通过 DescribeDCDBInstances 查询实例详情获得。
                :type InstanceId: str
                :param UserName: AccountName
                :type UserName: str
                :param Host: 可以登录的主机，与mysql 账号的 host 格式一致，可以支持通配符，例如 %，10.%，10.20.%。
                :type Host: str
                :param Password: 账号密码，由字母、数字或常见符号组成，不能包含分号、单引号和双引号，长度为6~32位。
                :type Password: str
                :param ReadOnly: 是否创建为只读账号，0：否， 1：该账号的sql请求优先选择备机执行，备机不可用时选择主机执行，2：优先选择备机执行，备机不可用时操作失败，3：只从备机读取。
                :type ReadOnly: int
                :param Description: 账号备注，可以包含中文、英文字符、常见符号和数字，长度为0~256字符
                :type Description: str
                :param DelayThresh: 如果备机延迟超过本参数设置值，系统将认为备机发生故障
        建议该参数值大于10。当ReadOnly选择1、2时该参数生效。
                :type DelayThresh: int
        """
        self.InstanceId = None
        self.UserName = None
        self.Host = None
        self.Password = None
        self.ReadOnly = None
        self.Description = None
        self.DelayThresh = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.UserName = params.get("UserName")
        self.Host = params.get("Host")
        self.Password = params.get("Password")
        self.ReadOnly = params.get("ReadOnly")
        self.Description = params.get("Description")
        self.DelayThresh = params.get("DelayThresh")


class CreateAccountResponse(AbstractModel):
    """CreateAccount返回参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例Id，透传入参。
        :type InstanceId: str
        :param UserName: 用户名，透传入参。
        :type UserName: str
        :param Host: 允许访问的 host，透传入参。
        :type Host: str
        :param ReadOnly: 透传入参。
        :type ReadOnly: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceId = None
        self.UserName = None
        self.Host = None
        self.ReadOnly = None
        self.RequestId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.UserName = params.get("UserName")
        self.Host = params.get("Host")
        self.ReadOnly = params.get("ReadOnly")
        self.RequestId = params.get("RequestId")


class CreateDCDBInstanceRequest(AbstractModel):
    """CreateDCDBInstance请求参数结构体"""

    def __init__(self):
        """
                :param Zones: 分片节点可用区分布，最多可填两个可用区。当分片规格为一主两从时，其中两个节点在第一个可用区。
                :type Zones: list of str
                :param Period: 欲购买的时长，单位：月。
                :type Period: int
                :param ShardMemory: 分片内存大小，单位：GB，可以通过 DescribeShardSpec
         查询实例规格获得。
                :type ShardMemory: int
                :param ShardStorage: 分片存储空间大小，单位：GB，可以通过 DescribeShardSpec
         查询实例规格获得。
                :type ShardStorage: int
                :param ShardNodeCount: 单个分片节点个数，可以通过 DescribeShardSpec
         查询实例规格获得。
                :type ShardNodeCount: int
                :param ShardCount: 实例分片个数，可选范围2-8，可以通过升级实例进行新增分片到最多64个分片。
                :type ShardCount: int
                :param Count: 欲购买实例的数量，目前只支持购买1个实例
                :type Count: int
                :param ProjectId: 项目 ID，可以通过查看项目列表获取，不传则关联到默认项目
                :type ProjectId: int
                :param VpcId: 虚拟私有网络 ID，不传或传空表示创建为基础网络
                :type VpcId: str
                :param SubnetId: 虚拟私有网络子网 ID，VpcId不为空时必填
                :type SubnetId: str
                :param DbVersionId: 数据库引擎版本，当前可选：10.0.10，10.1.9，5.7.17。
        10.0.10 - Mariadb 10.0.10；
        10.1.9 - Mariadb 10.1.9；
        5.7.17 - Percona 5.7.17。
        如果不填的话，默认为10.1.9，表示Mariadb 10.1.9。
                :type DbVersionId: str
                :param AutoVoucher: 是否自动使用代金券进行支付，默认不使用。
                :type AutoVoucher: bool
                :param VoucherIds: 代金券ID列表，目前仅支持指定一张代金券。
                :type VoucherIds: list of str
        """
        self.Zones = None
        self.Period = None
        self.ShardMemory = None
        self.ShardStorage = None
        self.ShardNodeCount = None
        self.ShardCount = None
        self.Count = None
        self.ProjectId = None
        self.VpcId = None
        self.SubnetId = None
        self.DbVersionId = None
        self.AutoVoucher = None
        self.VoucherIds = None

    def _deserialize(self, params):
        self.Zones = params.get("Zones")
        self.Period = params.get("Period")
        self.ShardMemory = params.get("ShardMemory")
        self.ShardStorage = params.get("ShardStorage")
        self.ShardNodeCount = params.get("ShardNodeCount")
        self.ShardCount = params.get("ShardCount")
        self.Count = params.get("Count")
        self.ProjectId = params.get("ProjectId")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.DbVersionId = params.get("DbVersionId")
        self.AutoVoucher = params.get("AutoVoucher")
        self.VoucherIds = params.get("VoucherIds")


class CreateDCDBInstanceResponse(AbstractModel):
    """CreateDCDBInstance返回参数结构体"""

    def __init__(self):
        """
               :param DealName: 长订单号。可以据此调用 DescribeOrders
        查询订单详细信息，或在支付失败时调用用户账号相关接口进行支付。
               :type DealName: str
               :param InstanceIds: 订单对应的实例 ID 列表，如果此处没有返回实例 ID，可以通过订单查询接口获取。还可通过实例查询接口查询实例是否创建完成。
               :type InstanceIds: list of str
               :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
               :type RequestId: str
        """
        self.DealName = None
        self.InstanceIds = None
        self.RequestId = None

    def _deserialize(self, params):
        self.DealName = params.get("DealName")
        self.InstanceIds = params.get("InstanceIds")
        self.RequestId = params.get("RequestId")


class CreateHourDCDBInstanceRequest(AbstractModel):
    """CreateHourDCDBInstance请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: VPC网络ID，形如vpc-qquscup9。
        :type VpcId: str
        :param SubnetId: VPC网络子网ID，形如subnet-mfhkoln6。
        :type SubnetId: str
        :param ShardMemory: 分片内存大小，单位为GB。
        :type ShardMemory: int
        :param ShardStorage: 分片磁盘大小，单位为GB。
        :type ShardStorage: int
        :param ShardNodeCount: 每个分片的节点个数，值为2或者3。2-一主一从；3-一主两从
        :type ShardNodeCount: int
        :param ShardCount: 分片的个数。取值范围为[2, 64]，即最小分片个数为2，最大分片个数为64。
        :type ShardCount: int
        :param Zones: 实例可用区信息，只能填一个可用区或者两个可用区。如果只填一个，那么主库和从库可用区一致；如果填两个，那么前一个表示主库可用区，后一个表示从库可用区。
        :type Zones: list of str
        :param ProjectId: 项目ID。
        :type ProjectId: int
        :param DbVersionId: 数据库版本。取值为10.0.10，10.1.9，5.7.17或者5.6.39。不填默认为5.7.17。
        :type DbVersionId: str
        :param Count: 购买数量
        :type Count: int
        :param ShardCpu: 分片 Cpu，单位： 核
        :type ShardCpu: int
        :param SecurityGroupId: 安全组ID
        :type SecurityGroupId: str
        :param InstanceName: 实例名称
        :type InstanceName: str
        :param ExclusterId: 资源池 Id，TCE 专用
        :type ExclusterId: str
        """
        self.VpcId = None
        self.SubnetId = None
        self.ShardMemory = None
        self.ShardStorage = None
        self.ShardNodeCount = None
        self.ShardCount = None
        self.Zones = None
        self.ProjectId = None
        self.DbVersionId = None
        self.Count = None
        self.ShardCpu = None
        self.SecurityGroupId = None
        self.InstanceName = None
        self.ExclusterId = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.ShardMemory = params.get("ShardMemory")
        self.ShardStorage = params.get("ShardStorage")
        self.ShardNodeCount = params.get("ShardNodeCount")
        self.ShardCount = params.get("ShardCount")
        self.Zones = params.get("Zones")
        self.ProjectId = params.get("ProjectId")
        self.DbVersionId = params.get("DbVersionId")
        self.Count = params.get("Count")
        self.ShardCpu = params.get("ShardCpu")
        self.SecurityGroupId = params.get("SecurityGroupId")
        self.InstanceName = params.get("InstanceName")
        self.ExclusterId = params.get("ExclusterId")


class CreateHourDCDBInstanceResponse(AbstractModel):
    """CreateHourDCDBInstance返回参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 创建的DCDB实例ID列表，形如dcdbt-87zif6ha
        :type InstanceIds: list of str
        :param FlowId: 创建实例异步任务ID，以FlowId作为参数调用DescribeFlow API接口查询创建实例任务执行状态。
        :type FlowId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceIds = None
        self.FlowId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class CreateTmpDCDBInstanceRequest(AbstractModel):
    """CreateTmpDCDBInstance请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 回档实例的ID，如:dcdbt-fp0n6tul
        :type InstanceId: str
        :param RollbackTime: 回档时间点
        :type RollbackTime: str
        :param UserType: 用户类型
        :type UserType: int
        """
        self.InstanceId = None
        self.RollbackTime = None
        self.UserType = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.RollbackTime = params.get("RollbackTime")
        self.UserType = params.get("UserType")


class CreateTmpDCDBInstanceResponse(AbstractModel):
    """CreateTmpDCDBInstance返回参数结构体"""

    def __init__(self):
        """
        :param FlowId: 异步任务流程ID。
        :type FlowId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class DBAccount(AbstractModel):
    """云数据库账号信息"""

    def __init__(self):
        """
                :param UserName: 用户名
                :type UserName: str
                :param Host: 用户可以从哪台主机登录（对应 MySQL 用户的 host 字段，UserName + Host 唯一标识一个用户，IP形式，IP段以%结尾；支持填入%；为空默认等于%）
                :type Host: str
                :param Description: 用户备注信息
                :type Description: str
                :param CreateTime: 创建时间
                :type CreateTime: str
                :param UpdateTime: 最后更新时间
                :type UpdateTime: str
                :param ReadOnly: 只读标记，0：否， 1：该账号的sql请求优先选择备机执行，备机不可用时选择主机执行，2：优先选择备机执行，备机不可用时操作失败。
                :type ReadOnly: int
                :param DelayThresh: 如果备机延迟超过本参数设置值，系统将认为备机发生故障
        建议该参数值大于10。当ReadOnly选择1、2时该参数生效。
                :type DelayThresh: int
        """
        self.UserName = None
        self.Host = None
        self.Description = None
        self.CreateTime = None
        self.UpdateTime = None
        self.ReadOnly = None
        self.DelayThresh = None

    def _deserialize(self, params):
        self.UserName = params.get("UserName")
        self.Host = params.get("Host")
        self.Description = params.get("Description")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.ReadOnly = params.get("ReadOnly")
        self.DelayThresh = params.get("DelayThresh")


class DBEngine(AbstractModel):
    """描述可选的 DB 引擎"""

    def __init__(self):
        """
        :param Type: 引擎类型，MariaDB 或 Percona
        :type Type: str
        :param Version: 引擎版本号，创建实例时传递该值
        :type Version: str
        :param Name: 名称，用于展示
        :type Name: str
        :param Description: 引擎版本描述信息
        :type Description: str
        """
        self.Type = None
        self.Version = None
        self.Name = None
        self.Description = None

    def _deserialize(self, params):
        self.Type = params.get("Type")
        self.Version = params.get("Version")
        self.Name = params.get("Name")
        self.Description = params.get("Description")


class DBParamValue(AbstractModel):
    """云数据库参数信息。"""

    def __init__(self):
        """
        :param Param: 参数名称
        :type Param: str
        :param Value: 参数值
        :type Value: str
        """
        self.Param = None
        self.Value = None

    def _deserialize(self, params):
        self.Param = params.get("Param")
        self.Value = params.get("Value")


class DCDBInstanceInfo(AbstractModel):
    """分布式数据库实例信息"""

    def __init__(self):
        """
                :param InstanceId: 实例ID
                :type InstanceId: str
                :param InstanceName: 实例名称
                :type InstanceName: str
                :param AppId: APPID
                :type AppId: int
                :param ProjectId: 项目ID
                :type ProjectId: int
                :param Region: 地域
                :type Region: str
                :param Zone: 可用区
                :type Zone: str
                :param VpcId: VPC数字ID
                :type VpcId: int
                :param SubnetId: Subnet数字ID
                :type SubnetId: int
                :param StatusDesc: 状态中文描述
                :type StatusDesc: str
                :param Status: 状态
                :type Status: int
                :param Vip: 内网IP
                :type Vip: str
                :param Vport: 内网端口
                :type Vport: int
                :param CreateTime: 创建时间
                :type CreateTime: str
                :param AutoRenewFlag: 自动续费标志
                :type AutoRenewFlag: int
                :param Memory: 内存大小，单位 GB
                :type Memory: int
                :param Storage: 存储大小，单位 GB
                :type Storage: int
                :param ShardCount: 分片个数
                :type ShardCount: int
                :param PeriodEndTime: 到期时间
                :type PeriodEndTime: str
                :param IsolatedTimestamp: 隔离时间
                :type IsolatedTimestamp: str
                :param Uin: UIN
                :type Uin: str
                :param ShardDetail: 分片详情
                :type ShardDetail: list of ShardInfo
                :param NodeCount: 节点数，2 为一主一从， 3 为一主二从
                :type NodeCount: int
                :param IsTmp: 临时实例标记，0 为非临时实例
                :type IsTmp: int
                :param ExclusterId: 独享集群Id，为空表示非独享集群实例
                :type ExclusterId: str
                :param UniqueVpcId: 字符串型的私有网络Id
                :type UniqueVpcId: str
                :param UniqueSubnetId: 字符串型的私有网络子网Id
                :type UniqueSubnetId: str
                :param Id: 数字实例Id（过时字段，请勿依赖该值）
                :type Id: int
                :param WanDomain: 外网访问的域名，公网可解析
                :type WanDomain: str
                :param WanVip: 外网 IP 地址，公网可访问
                :type WanVip: str
                :param WanPort: 外网端口
                :type WanPort: int
                :param Pid: 产品类型 Id（过时字段，请勿依赖该值）
                :type Pid: int
                :param UpdateTime: 实例最后更新时间，格式为 2006-01-02 15:04:05
                :type UpdateTime: str
                :param DbEngine: 数据库引擎
                :type DbEngine: str
                :param DbVersion: 数据库引擎版本
                :type DbVersion: str
                :param Paymode: 付费模式
                :type Paymode: str
                :param Locker: 实例处于异步任务状态时，表示异步任务流程ID
        注意：此字段可能返回 null，表示取不到有效值。
                :type Locker: int
                :param WanStatus: 外网状态，0-未开通；1-已开通；2-关闭；3-开通中
                :type WanStatus: int
                :param IsAuditSupported: 该实例是否支持审计。1-支持；0-不支持
                :type IsAuditSupported: int
        """
        self.InstanceId = None
        self.InstanceName = None
        self.AppId = None
        self.ProjectId = None
        self.Region = None
        self.Zone = None
        self.VpcId = None
        self.SubnetId = None
        self.StatusDesc = None
        self.Status = None
        self.Vip = None
        self.Vport = None
        self.CreateTime = None
        self.AutoRenewFlag = None
        self.Memory = None
        self.Storage = None
        self.ShardCount = None
        self.PeriodEndTime = None
        self.IsolatedTimestamp = None
        self.Uin = None
        self.ShardDetail = None
        self.NodeCount = None
        self.IsTmp = None
        self.ExclusterId = None
        self.UniqueVpcId = None
        self.UniqueSubnetId = None
        self.Id = None
        self.WanDomain = None
        self.WanVip = None
        self.WanPort = None
        self.Pid = None
        self.UpdateTime = None
        self.DbEngine = None
        self.DbVersion = None
        self.Paymode = None
        self.Locker = None
        self.WanStatus = None
        self.IsAuditSupported = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.AppId = params.get("AppId")
        self.ProjectId = params.get("ProjectId")
        self.Region = params.get("Region")
        self.Zone = params.get("Zone")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.StatusDesc = params.get("StatusDesc")
        self.Status = params.get("Status")
        self.Vip = params.get("Vip")
        self.Vport = params.get("Vport")
        self.CreateTime = params.get("CreateTime")
        self.AutoRenewFlag = params.get("AutoRenewFlag")
        self.Memory = params.get("Memory")
        self.Storage = params.get("Storage")
        self.ShardCount = params.get("ShardCount")
        self.PeriodEndTime = params.get("PeriodEndTime")
        self.IsolatedTimestamp = params.get("IsolatedTimestamp")
        self.Uin = params.get("Uin")
        if params.get("ShardDetail") is not None:
            self.ShardDetail = []
            for item in params.get("ShardDetail"):
                obj = ShardInfo()
                obj._deserialize(item)
                self.ShardDetail.append(obj)
        self.NodeCount = params.get("NodeCount")
        self.IsTmp = params.get("IsTmp")
        self.ExclusterId = params.get("ExclusterId")
        self.UniqueVpcId = params.get("UniqueVpcId")
        self.UniqueSubnetId = params.get("UniqueSubnetId")
        self.Id = params.get("Id")
        self.WanDomain = params.get("WanDomain")
        self.WanVip = params.get("WanVip")
        self.WanPort = params.get("WanPort")
        self.Pid = params.get("Pid")
        self.UpdateTime = params.get("UpdateTime")
        self.DbEngine = params.get("DbEngine")
        self.DbVersion = params.get("DbVersion")
        self.Paymode = params.get("Paymode")
        self.Locker = params.get("Locker")
        self.WanStatus = params.get("WanStatus")
        self.IsAuditSupported = params.get("IsAuditSupported")


class DCDBShardInfo(AbstractModel):
    """描述分布式数据库分片信息。"""

    def __init__(self):
        """
        :param InstanceId: 所属实例Id
        :type InstanceId: str
        :param ShardSerialId: 分片SQL透传Id，用于将sql透传到指定分片执行
        :type ShardSerialId: str
        :param ShardInstanceId: 全局唯一的分片Id
        :type ShardInstanceId: str
        :param Status: 状态：0 创建中，1 流程处理中， 2 运行中，3 分片未初始化
        :type Status: int
        :param StatusDesc: 状态中文描述
        :type StatusDesc: str
        :param CreateTime: 创建时间
        :type CreateTime: str
        :param VpcId: 字符串格式的私有网络Id
        :type VpcId: str
        :param SubnetId: 字符串格式的私有网络子网Id
        :type SubnetId: str
        :param ProjectId: 项目ID
        :type ProjectId: int
        :param Region: 地域
        :type Region: str
        :param Zone: 可用区
        :type Zone: str
        :param Memory: 内存大小，单位 GB
        :type Memory: int
        :param Storage: 存储大小，单位 GB
        :type Storage: int
        :param PeriodEndTime: 到期时间
        :type PeriodEndTime: str
        :param NodeCount: 节点数，2 为一主一从， 3 为一主二从
        :type NodeCount: int
        :param StorageUsage: 存储使用率，单位为 %
        :type StorageUsage: float
        :param MemoryUsage: 内存使用率，单位为 %
        :type MemoryUsage: float
        :param ShardId: 数字分片Id（过时字段，请勿依赖该值）
        :type ShardId: int
        :param Pid: 产品ProductID
        :type Pid: int
        :param ProxyVersion: Proxy版本
        :type ProxyVersion: str
        """
        self.InstanceId = None
        self.ShardSerialId = None
        self.ShardInstanceId = None
        self.Status = None
        self.StatusDesc = None
        self.CreateTime = None
        self.VpcId = None
        self.SubnetId = None
        self.ProjectId = None
        self.Region = None
        self.Zone = None
        self.Memory = None
        self.Storage = None
        self.PeriodEndTime = None
        self.NodeCount = None
        self.StorageUsage = None
        self.MemoryUsage = None
        self.ShardId = None
        self.Pid = None
        self.ProxyVersion = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.ShardSerialId = params.get("ShardSerialId")
        self.ShardInstanceId = params.get("ShardInstanceId")
        self.Status = params.get("Status")
        self.StatusDesc = params.get("StatusDesc")
        self.CreateTime = params.get("CreateTime")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.ProjectId = params.get("ProjectId")
        self.Region = params.get("Region")
        self.Zone = params.get("Zone")
        self.Memory = params.get("Memory")
        self.Storage = params.get("Storage")
        self.PeriodEndTime = params.get("PeriodEndTime")
        self.NodeCount = params.get("NodeCount")
        self.StorageUsage = params.get("StorageUsage")
        self.MemoryUsage = params.get("MemoryUsage")
        self.ShardId = params.get("ShardId")
        self.Pid = params.get("Pid")
        self.ProxyVersion = params.get("ProxyVersion")


class Database(AbstractModel):
    """数据库信息"""

    def __init__(self):
        """
        :param DbName: 数据库名称
        :type DbName: str
        """
        self.DbName = None

    def _deserialize(self, params):
        self.DbName = params.get("DbName")


class DatabaseFunction(AbstractModel):
    """数据库函数信息"""

    def __init__(self):
        """
        :param Func: 函数名称
        :type Func: str
        """
        self.Func = None

    def _deserialize(self, params):
        self.Func = params.get("Func")


class DatabaseProcedure(AbstractModel):
    """数据库存储过程信息"""

    def __init__(self):
        """
        :param Proc: 存储过程名称
        :type Proc: str
        """
        self.Proc = None

    def _deserialize(self, params):
        self.Proc = params.get("Proc")


class DatabaseTable(AbstractModel):
    """数据库表信息"""

    def __init__(self):
        """
        :param Table: 表名
        :type Table: str
        """
        self.Table = None

    def _deserialize(self, params):
        self.Table = params.get("Table")


class DatabaseView(AbstractModel):
    """数据库视图信息"""

    def __init__(self):
        """
        :param View: 视图名称
        :type View: str
        """
        self.View = None

    def _deserialize(self, params):
        self.View = params.get("View")


class Deal(AbstractModel):
    """订单信息"""

    def __init__(self):
        """
                :param DealName: 订单号
                :type DealName: str
                :param OwnerUin: 所属账号
                :type OwnerUin: str
                :param Count: 商品数量
                :type Count: int
                :param FlowId: 关联的流程 Id，可用于查询流程执行状态
                :type FlowId: int
                :param InstanceIds: 只有创建实例的订单会填充该字段，表示该订单创建的实例的 ID。
        注意：此字段可能返回 null，表示取不到有效值。
                :type InstanceIds: list of str
                :param PayMode: 付费模式，0后付费/1预付费
                :type PayMode: int
        """
        self.DealName = None
        self.OwnerUin = None
        self.Count = None
        self.FlowId = None
        self.InstanceIds = None
        self.PayMode = None

    def _deserialize(self, params):
        self.DealName = params.get("DealName")
        self.OwnerUin = params.get("OwnerUin")
        self.Count = params.get("Count")
        self.FlowId = params.get("FlowId")
        self.InstanceIds = params.get("InstanceIds")
        self.PayMode = params.get("PayMode")


class DeleteAccountRequest(AbstractModel):
    """DeleteAccount请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID，形如：dcdbt-ow728lmc，可以通过 DescribeDCDBInstances 查询实例详情获得。
        :type InstanceId: str
        :param UserName: 用户名
        :type UserName: str
        :param Host: 用户允许的访问 host
        :type Host: str
        """
        self.InstanceId = None
        self.UserName = None
        self.Host = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.UserName = params.get("UserName")
        self.Host = params.get("Host")


class DeleteAccountResponse(AbstractModel):
    """DeleteAccount返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteTmpInstanceRequest(AbstractModel):
    """DeleteTmpInstance请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class DeleteTmpInstanceResponse(AbstractModel):
    """DeleteTmpInstance返回参数结构体"""

    def __init__(self):
        """
        :param FlowId: 异步任务流程ID。
        :type FlowId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class DescribeAccountPrivilegesRequest(AbstractModel):
    """DescribeAccountPrivileges请求参数结构体"""

    def __init__(self):
        r"""
        :param InstanceId: 实例 ID，形如：dcdbt-ow7t8lmc。
        :type InstanceId: str
        :param UserName: 登录用户名。
        :type UserName: str
        :param Host: 用户允许的访问 host，用户名+host唯一确定一个账号。
        :type Host: str
        :param DbName: 数据库名。如果为 \*，表示查询全局权限（即 \*.\*），此时忽略 Type 和 Object 参数
        :type DbName: str
        :param Type: 类型,可以填入 table 、 view 、 proc 、 func 和 \*。
        当 DbName 为具体数据库名，Type为 \* 时，表示查询该数据库权限（即db.\*），此时忽略 Object 参数
        :type Type: str
        :param Object: 具体的 Type 的名称，比如 Type 为 table 时就是具体的表名。
        DbName 和 Type 都为具体名称，则 Object 表示具体对象名，不能为 \* 或者为空
        :type Object: str
        :param ColName: 当 Type=table 时，ColName 为 \* 表示查询表的权限，如果为具体字段名，表示查询对应字段的权限
        :type ColName: str
        """
        self.InstanceId = None
        self.UserName = None
        self.Host = None
        self.DbName = None
        self.Type = None
        self.Object = None
        self.ColName = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.UserName = params.get("UserName")
        self.Host = params.get("Host")
        self.DbName = params.get("DbName")
        self.Type = params.get("Type")
        self.Object = params.get("Object")
        self.ColName = params.get("ColName")


class DescribeAccountPrivilegesResponse(AbstractModel):
    """DescribeAccountPrivileges返回参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例Id
        :type InstanceId: str
        :param Privileges: 权限列表。
        :type Privileges: list of str
        :param UserName: 数据库账号用户名
        :type UserName: str
        :param Host: 数据库账号Host
        :type Host: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceId = None
        self.Privileges = None
        self.UserName = None
        self.Host = None
        self.RequestId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Privileges = params.get("Privileges")
        self.UserName = params.get("UserName")
        self.Host = params.get("Host")
        self.RequestId = params.get("RequestId")


class DescribeAccountsRequest(AbstractModel):
    """DescribeAccounts请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID，形如：dcdbt-ow728lmc。
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class DescribeAccountsResponse(AbstractModel):
    """DescribeAccounts返回参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID，透传入参。
        :type InstanceId: str
        :param Users: 实例用户列表。
        :type Users: list of DBAccount
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceId = None
        self.Users = None
        self.RequestId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("Users") is not None:
            self.Users = []
            for item in params.get("Users"):
                obj = DBAccount()
                obj._deserialize(item)
                self.Users.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeAuditLogsRequest(AbstractModel):
    """DescribeAuditLogs请求参数结构体"""

    def __init__(self):
        """
        :param StartTime: 开始时间
        :type StartTime: str
        :param EndTime: 结束时间
        :type EndTime: str
        :param ClientIpPorts: 客户端IP和端口列表
        :type ClientIpPorts: list of str
        :param SqlUsers: sql操作者列表
        :type SqlUsers: list of str
        :param SqlTypes: sql类型列表
        :type SqlTypes: list of str
        :param StrategyNames: 审计策略名称列表
        :type StrategyNames: list of str
        :param InstanceIds: 实例ID列表
        :type InstanceIds: list of str
        :param DbNames: 数据库名称列表
        :type DbNames: list of str
        :param SearchKey: 搜索关键字，sql可选
        :type SearchKey: str
        :param KeyWords: 搜索关键字的条件值
        :type KeyWords: list of str
        :param Limit: 分页，页大小，默认150
        :type Limit: int
        :param Offset: 分页，页偏移量，默认0
        :type Offset: int
        :param OrderBy: 排序字段，costtime,rowseffected,name,receivetime可选，默认receivetime
        :type OrderBy: str
        :param OrderByType: 排序方式，desc，asc可选
        :type OrderByType: str
        """
        self.StartTime = None
        self.EndTime = None
        self.ClientIpPorts = None
        self.SqlUsers = None
        self.SqlTypes = None
        self.StrategyNames = None
        self.InstanceIds = None
        self.DbNames = None
        self.SearchKey = None
        self.KeyWords = None
        self.Limit = None
        self.Offset = None
        self.OrderBy = None
        self.OrderByType = None

    def _deserialize(self, params):
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.ClientIpPorts = params.get("ClientIpPorts")
        self.SqlUsers = params.get("SqlUsers")
        self.SqlTypes = params.get("SqlTypes")
        self.StrategyNames = params.get("StrategyNames")
        self.InstanceIds = params.get("InstanceIds")
        self.DbNames = params.get("DbNames")
        self.SearchKey = params.get("SearchKey")
        self.KeyWords = params.get("KeyWords")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.OrderBy = params.get("OrderBy")
        self.OrderByType = params.get("OrderByType")


class DescribeAuditLogsResponse(AbstractModel):
    """DescribeAuditLogs返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 总记录数
        :type TotalCount: int
        :param AuditLogSet: 审计日志列表
        :type AuditLogSet: list of AuditLog
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.AuditLogSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("AuditLogSet") is not None:
            self.AuditLogSet = []
            for item in params.get("AuditLogSet"):
                obj = AuditLog()
                obj._deserialize(item)
                self.AuditLogSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeAuditRuleDetailRequest(AbstractModel):
    """DescribeAuditRuleDetail请求参数结构体"""

    def __init__(self):
        """
        :param RuleId: 规则Id
        :type RuleId: int
        """
        self.RuleId = None

    def _deserialize(self, params):
        self.RuleId = params.get("RuleId")


class DescribeAuditRuleDetailResponse(AbstractModel):
    """DescribeAuditRuleDetail返回参数结构体"""

    def __init__(self):
        """
        :param AuditRuleDetail: 审计规则
        :type AuditRuleDetail: :class:`tcecloud.dcdb.v20180411.models.AuditRuleDetail`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AuditRuleDetail = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("AuditRuleDetail") is not None:
            self.AuditRuleDetail = AuditRuleDetail()
            self.AuditRuleDetail._deserialize(params.get("AuditRuleDetail"))
        self.RequestId = params.get("RequestId")


class DescribeAuditRulesRequest(AbstractModel):
    """DescribeAuditRules请求参数结构体"""

    def __init__(self):
        """
        :param RuleNames: 规则名称列表
        :type RuleNames: list of str
        :param Limit: 分页，页大小，默认150
        :type Limit: int
        :param Offset: 分页，页偏移量，默认0
        :type Offset: int
        :param OrderBy: 排序字段，createTime,updateTime,name可选，默认createTime
        :type OrderBy: str
        :param OrderByType: 排序方式，desc，asc可选
        :type OrderByType: str
        """
        self.RuleNames = None
        self.Limit = None
        self.Offset = None
        self.OrderBy = None
        self.OrderByType = None

    def _deserialize(self, params):
        self.RuleNames = params.get("RuleNames")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.OrderBy = params.get("OrderBy")
        self.OrderByType = params.get("OrderByType")


class DescribeAuditRulesResponse(AbstractModel):
    """DescribeAuditRules返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 总记录数
        :type TotalCount: int
        :param RuleSet: 审计规则列表
        :type RuleSet: list of AuditRule
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.RuleSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("RuleSet") is not None:
            self.RuleSet = []
            for item in params.get("RuleSet"):
                obj = AuditRule()
                obj._deserialize(item)
                self.RuleSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeAuditStrategiesRequest(AbstractModel):
    """DescribeAuditStrategies请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例Id，可以通过 DescribeDBInstances 查询实例详情获得。
        :type InstanceId: str
        :param StrategyNames: 策略名称列表
        :type StrategyNames: list of str
        :param RuleNames: 规则名称列表
        :type RuleNames: list of str
        :param AlterTypes: 响应策略，0放行，1不放行
        :type AlterTypes: list of int
        :param ActionTypes: 脱敏记录，0不脱敏，1脱敏
        :type ActionTypes: list of int
        :param Status: 策略状态，0不启用，1启用
        :type Status: list of int
        :param Priorities: 优先顺序
        :type Priorities: list of int
        """
        self.InstanceId = None
        self.StrategyNames = None
        self.RuleNames = None
        self.AlterTypes = None
        self.ActionTypes = None
        self.Status = None
        self.Priorities = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StrategyNames = params.get("StrategyNames")
        self.RuleNames = params.get("RuleNames")
        self.AlterTypes = params.get("AlterTypes")
        self.ActionTypes = params.get("ActionTypes")
        self.Status = params.get("Status")
        self.Priorities = params.get("Priorities")


class DescribeAuditStrategiesResponse(AbstractModel):
    """DescribeAuditStrategies返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 总记录数
        :type TotalCount: int
        :param SessionId: 会话Id
        :type SessionId: int
        :param StrategySet: 审计策略列表
        :type StrategySet: list of AuditStrategy
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.SessionId = None
        self.StrategySet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        self.SessionId = params.get("SessionId")
        if params.get("StrategySet") is not None:
            self.StrategySet = []
            for item in params.get("StrategySet"):
                obj = AuditStrategy()
                obj._deserialize(item)
                self.StrategySet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeAvailableExclusiveGroupsRequest(AbstractModel):
    """DescribeAvailableExclusiveGroups请求参数结构体"""


class DescribeAvailableExclusiveGroupsResponse(AbstractModel):
    """DescribeAvailableExclusiveGroups返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 独享资源池数目
        :type TotalCount: int
        :param Items: 独享资源池信息
        :type Items: list of FenceInfoItem
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.Items = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Items") is not None:
            self.Items = []
            for item in params.get("Items"):
                obj = FenceInfoItem()
                obj._deserialize(item)
                self.Items.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeBatchDCDBRenewalPriceRequest(AbstractModel):
    """DescribeBatchDCDBRenewalPrice请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 待续费的实例ID数组。形如：["dcdbt-ow728lmc"]，可以通过 DescribeDCDBInstances 查询实例详情获得。
        :type InstanceIds: list of str
        :param Period: 续费时长，单位：月。
        :type Period: int
        """
        self.InstanceIds = None
        self.Period = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.Period = params.get("Period")


class DescribeBatchDCDBRenewalPriceResponse(AbstractModel):
    """DescribeBatchDCDBRenewalPrice返回参数结构体"""

    def __init__(self):
        """
        :param OriginalPrice: 原价，单位：分
        :type OriginalPrice: int
        :param Price: 实际价格，单位：分。受折扣等影响，可能和原价不同。
        :type Price: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.OriginalPrice = None
        self.Price = None
        self.RequestId = None

    def _deserialize(self, params):
        self.OriginalPrice = params.get("OriginalPrice")
        self.Price = params.get("Price")
        self.RequestId = params.get("RequestId")


class DescribeDBDetailMetricsRequest(AbstractModel):
    """DescribeDBDetailMetrics请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例Id，形如：tdsql-ow728lmc
        :type InstanceId: str
        :param StartTime: 起始日期，格式yyyy-mm-dd
        :type StartTime: str
        :param EndTime: 结束日期，格式yyyy-mm-dd
        :type EndTime: str
        :param MetricNames: 需要请求的指标名，当前支持的指标有：
        :type MetricNames: list of str
        :param Period: 监控统计周期。默认为取值为300，单位为s，当前可选：60，300
        :type Period: int
        :param ShardId: 实例分片ID
        :type ShardId: str
        """
        self.InstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.MetricNames = None
        self.Period = None
        self.ShardId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.MetricNames = params.get("MetricNames")
        self.Period = params.get("Period")
        self.ShardId = params.get("ShardId")


class DescribeDBDetailMetricsResponse(AbstractModel):
    """DescribeDBDetailMetrics返回参数结构体"""

    def __init__(self):
        """
        :param StartTime: 开始时间
        :type StartTime: str
        :param EndTime: 结束时间
        :type EndTime: str
        :param Period: 统计周期
        :type Period: int
        :param MasterDataPoints: 主节点数据点数组
        :type MasterDataPoints: list of MetricDataPoint
        :param Slave1DataPoints: 备机1数据点数组
        :type Slave1DataPoints: list of MetricDataPoint
        :param Slave2DataPoints: 备机2数据点数组
        :type Slave2DataPoints: list of MetricDataPoint
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.StartTime = None
        self.EndTime = None
        self.Period = None
        self.MasterDataPoints = None
        self.Slave1DataPoints = None
        self.Slave2DataPoints = None
        self.RequestId = None

    def _deserialize(self, params):
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Period = params.get("Period")
        if params.get("MasterDataPoints") is not None:
            self.MasterDataPoints = []
            for item in params.get("MasterDataPoints"):
                obj = MetricDataPoint()
                obj._deserialize(item)
                self.MasterDataPoints.append(obj)
        if params.get("Slave1DataPoints") is not None:
            self.Slave1DataPoints = []
            for item in params.get("Slave1DataPoints"):
                obj = MetricDataPoint()
                obj._deserialize(item)
                self.Slave1DataPoints.append(obj)
        if params.get("Slave2DataPoints") is not None:
            self.Slave2DataPoints = []
            for item in params.get("Slave2DataPoints"):
                obj = MetricDataPoint()
                obj._deserialize(item)
                self.Slave2DataPoints.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDBEnginesRequest(AbstractModel):
    """DescribeDBEngines请求参数结构体"""


class DescribeDBEnginesResponse(AbstractModel):
    """DescribeDBEngines返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 返回的引擎总数
        :type TotalCount: int
        :param Items: 支持的引擎列表
        :type Items: list of DBEngine
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.Items = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Items") is not None:
            self.Items = []
            for item in params.get("Items"):
                obj = DBEngine()
                obj._deserialize(item)
                self.Items.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDBInstanceRsipRequest(AbstractModel):
    """DescribeDBInstanceRsip请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class DescribeDBInstanceRsipResponse(AbstractModel):
    """DescribeDBInstanceRsip返回参数结构体"""

    def __init__(self):
        """
        :param Rsips: 后端RS信息
        :type Rsips: list of Rsip
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Rsips = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Rsips") is not None:
            self.Rsips = []
            for item in params.get("Rsips"):
                obj = Rsip()
                obj._deserialize(item)
                self.Rsips.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDBLogFilesRequest(AbstractModel):
    """DescribeDBLogFiles请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：dcdbt-ow7t8lmc。
        :type InstanceId: str
        :param ShardId: 分片 ID，形如：shard-7noic7tv
        :type ShardId: str
        :param Type: 请求日志类型，取值只能为1、2、3或者4。1-binlog，2-冷备，3-errlog，4-slowlog。
        :type Type: int
        """
        self.InstanceId = None
        self.ShardId = None
        self.Type = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.ShardId = params.get("ShardId")
        self.Type = params.get("Type")


class DescribeDBLogFilesResponse(AbstractModel):
    """DescribeDBLogFiles返回参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：dcdbt-ow728lmc。
        :type InstanceId: str
        :param Type: 请求日志类型。1-binlog，2-冷备，3-errlog，4-slowlog。
        :type Type: int
        :param Total: 请求日志总数
        :type Total: int
        :param Files: 日志文件列表
        :type Files: list of LogFileInfo
        :param VpcPrefix: 如果是VPC网络的实例，做用本前缀加上URI为下载地址
        :type VpcPrefix: str
        :param NormalPrefix: 如果是普通网络的实例，做用本前缀加上URI为下载地址
        :type NormalPrefix: str
        :param ShardId: 分片 ID，形如：shard-7noic7tv
        :type ShardId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceId = None
        self.Type = None
        self.Total = None
        self.Files = None
        self.VpcPrefix = None
        self.NormalPrefix = None
        self.ShardId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Type = params.get("Type")
        self.Total = params.get("Total")
        if params.get("Files") is not None:
            self.Files = []
            for item in params.get("Files"):
                obj = LogFileInfo()
                obj._deserialize(item)
                self.Files.append(obj)
        self.VpcPrefix = params.get("VpcPrefix")
        self.NormalPrefix = params.get("NormalPrefix")
        self.ShardId = params.get("ShardId")
        self.RequestId = params.get("RequestId")


class DescribeDBMetricsRequest(AbstractModel):
    """DescribeDBMetrics请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例Id，形如：dcdbt-ow728lmc
        :type InstanceId: str
        :param StartTime: 起始日期，格式yyyy-mm-dd
        :type StartTime: str
        :param EndTime: 结束日期，格式yyyy-mm-dd
        :type EndTime: str
        :param MetricNames: 需要请求的指标名，当前支持的指标有：
        :type MetricNames: list of str
        :param Period: 监控统计周期。默认为取值为300，单位为s，当前可选：60，300
        :type Period: int
        :param ShardId: DCDB分片ID，形如shard-15xl67ih。如果填充该字段，表示拉取的是该分片的监控信息
        :type ShardId: str
        """
        self.InstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.MetricNames = None
        self.Period = None
        self.ShardId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.MetricNames = params.get("MetricNames")
        self.Period = params.get("Period")
        self.ShardId = params.get("ShardId")


class DescribeDBMetricsResponse(AbstractModel):
    """DescribeDBMetrics返回参数结构体"""

    def __init__(self):
        """
        :param Period: 监控统计周期
        :type Period: int
        :param DataPoints: 监控指标数据点数组
        :type DataPoints: list of MetricDataPoint
        :param StartTime: 开始时间
        :type StartTime: str
        :param EndTime: 结束时间
        :type EndTime: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Period = None
        self.DataPoints = None
        self.StartTime = None
        self.EndTime = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Period = params.get("Period")
        if params.get("DataPoints") is not None:
            self.DataPoints = []
            for item in params.get("DataPoints"):
                obj = MetricDataPoint()
                obj._deserialize(item)
                self.DataPoints.append(obj)
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.RequestId = params.get("RequestId")


class DescribeDBParametersRequest(AbstractModel):
    """DescribeDBParameters请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：dcdbt-ow7t8lmc。
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class DescribeDBParametersResponse(AbstractModel):
    """DescribeDBParameters返回参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：dcdbt-ow7t8lmc。
        :type InstanceId: str
        :param Params: 请求DB的当前参数值
        :type Params: list of ParamDesc
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceId = None
        self.Params = None
        self.RequestId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("Params") is not None:
            self.Params = []
            for item in params.get("Params"):
                obj = ParamDesc()
                obj._deserialize(item)
                self.Params.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDBSecurityGroupsRequest(AbstractModel):
    """DescribeDBSecurityGroups请求参数结构体"""

    def __init__(self):
        """
        :param Product: 数据库引擎名称：mariadb,cdb,cynosdb,dcdb,redis,mongodb 等。
        :type Product: str
        :param InstanceId: 实例ID，格式如：cdb-c1nl9rpv或者cdbro-c1nl9rpv，与云数据库控制台页面中显示的实例ID相同。
        :type InstanceId: str
        """
        self.Product = None
        self.InstanceId = None

    def _deserialize(self, params):
        self.Product = params.get("Product")
        self.InstanceId = params.get("InstanceId")


class DescribeDBSecurityGroupsResponse(AbstractModel):
    """DescribeDBSecurityGroups返回参数结构体"""

    def __init__(self):
        """
        :param Groups: 安全组规则
        :type Groups: list of SecurityGroup
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Groups = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Groups") is not None:
            self.Groups = []
            for item in params.get("Groups"):
                obj = SecurityGroup()
                obj._deserialize(item)
                self.Groups.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDBSlowLogAnalysisRequest(AbstractModel):
    """DescribeDBSlowLogAnalysis请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如 dcdbt-hw0qj6m1
        :type InstanceId: str
        :param StartTime: 开始时间，形如 2006-01-02 15:04:05
        :type StartTime: str
        :param Db: 要查询的慢查询语句对应的数据库名称
        :type Db: str
        :param User: 要查询的慢查询语句对应的用户名称
        :type User: str
        :param CheckSum: 要查询的慢查询语句的校验和，可以通过查询慢查询日志列表获得
        :type CheckSum: str
        :param ShardId: 实例分片ID，形如 shard-nbchf68b
        :type ShardId: str
        :param EndTime: 结束时间，形如 2006-01-02 15:04:05，不填的话默认是当前时间
        :type EndTime: str
        :param Slave: 是否查询从机的慢查询。0-主机；1-从机，默认查询主机慢查询
        :type Slave: int
        """
        self.InstanceId = None
        self.StartTime = None
        self.Db = None
        self.User = None
        self.CheckSum = None
        self.ShardId = None
        self.EndTime = None
        self.Slave = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.Db = params.get("Db")
        self.User = params.get("User")
        self.CheckSum = params.get("CheckSum")
        self.ShardId = params.get("ShardId")
        self.EndTime = params.get("EndTime")
        self.Slave = params.get("Slave")


class DescribeDBSlowLogAnalysisResponse(AbstractModel):
    """DescribeDBSlowLogAnalysis返回参数结构体"""

    def __init__(self):
        """
        :param StartTime: 慢查询SQL出现的开始时间
        :type StartTime: str
        :param EndTime: 慢查询SQL出现的结束时间
        :type EndTime: str
        :param Data: 返回的慢查询详情数据。每个点代表一个时间段内慢查询SQL出现的记录次数，
        一个时间段的长度由请求的开始时间和结束时间的差值决定，小于1天是5分钟一段，大于1天小于7天是30分钟一段，大于7天是2个小时一段。
        :type Data: list of int
        :param Period: Data 数组中的数据点间隔，单位为秒
        :type Period: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.StartTime = None
        self.EndTime = None
        self.Data = None
        self.Period = None
        self.RequestId = None

    def _deserialize(self, params):
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Data = params.get("Data")
        self.Period = params.get("Period")
        self.RequestId = params.get("RequestId")


class DescribeDBSlowLogsRequest(AbstractModel):
    """DescribeDBSlowLogs请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：dcdbt-hw0qj6m1
        :type InstanceId: str
        :param Offset: 从结果的第几条数据开始返回
        :type Offset: int
        :param Limit: 返回的结果条数
        :type Limit: int
        :param StartTime: 查询的起始时间，形如2016-07-23 14:55:20
        :type StartTime: str
        :param ShardId: 实例的分片ID，形如shard-53ima8ln
        :type ShardId: str
        :param EndTime: 查询的结束时间，形如2016-08-22 14:55:20。如果不填，那么查询结束时间就是当前时间
        :type EndTime: str
        :param Db: 要查询的具体数据库名称
        :type Db: str
        :param OrderBy: 排序指标，取值为query_time_sum或者query_count。不填默认按照query_time_sum排序
        :type OrderBy: str
        :param OrderByType: 排序类型，desc（降序）或者asc（升序）。不填默认desc排序
        :type OrderByType: str
        :param Slave: 是否查询从机的慢查询，0-主机; 1-从机。不填默认查询主机慢查询
        :type Slave: int
        """
        self.InstanceId = None
        self.Offset = None
        self.Limit = None
        self.StartTime = None
        self.ShardId = None
        self.EndTime = None
        self.Db = None
        self.OrderBy = None
        self.OrderByType = None
        self.Slave = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.StartTime = params.get("StartTime")
        self.ShardId = params.get("ShardId")
        self.EndTime = params.get("EndTime")
        self.Db = params.get("Db")
        self.OrderBy = params.get("OrderBy")
        self.OrderByType = params.get("OrderByType")
        self.Slave = params.get("Slave")


class DescribeDBSlowLogsResponse(AbstractModel):
    """DescribeDBSlowLogs返回参数结构体"""

    def __init__(self):
        """
        :param LockTimeSum: 所有语句锁时间总和
        :type LockTimeSum: float
        :param QueryCount: 所有语句查询总次数
        :type QueryCount: int
        :param Total: 总记录数
        :type Total: int
        :param QueryTimeSum: 所有语句查询时间总和
        :type QueryTimeSum: float
        :param Data: 慢查询日志数据
        :type Data: list of SlowLogData
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.LockTimeSum = None
        self.QueryCount = None
        self.Total = None
        self.QueryTimeSum = None
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        self.LockTimeSum = params.get("LockTimeSum")
        self.QueryCount = params.get("QueryCount")
        self.Total = params.get("Total")
        self.QueryTimeSum = params.get("QueryTimeSum")
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = SlowLogData()
                obj._deserialize(item)
                self.Data.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDBSyncModeRequest(AbstractModel):
    """DescribeDBSyncMode请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 待修改同步模式的实例ID。形如：dcdbt-ow728lmc。
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class DescribeDBSyncModeResponse(AbstractModel):
    """DescribeDBSyncMode返回参数结构体"""

    def __init__(self):
        """
        :param SyncMode: 同步模式：0 异步，1 强同步， 2 强同步可退化
        :type SyncMode: int
        :param IsModifying: 是否有修改流程在执行中：1 是， 0 否。
        :type IsModifying: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SyncMode = None
        self.IsModifying = None
        self.RequestId = None

    def _deserialize(self, params):
        self.SyncMode = params.get("SyncMode")
        self.IsModifying = params.get("IsModifying")
        self.RequestId = params.get("RequestId")


class DescribeDBTmpInstancesRequest(AbstractModel):
    """DescribeDBTmpInstances请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class DescribeDBTmpInstancesResponse(AbstractModel):
    """DescribeDBTmpInstances返回参数结构体"""

    def __init__(self):
        """
        :param TmpInstances: 临时实例
        :type TmpInstances: list of TmpInstance
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TmpInstances = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("TmpInstances") is not None:
            self.TmpInstances = []
            for item in params.get("TmpInstances"):
                obj = TmpInstance()
                obj._deserialize(item)
                self.TmpInstances.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDCDBBinlogTimeRequest(AbstractModel):
    """DescribeDCDBBinlogTime请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID
        :type InstanceId: str
        :param UserType: 用户类型
        :type UserType: int
        """
        self.InstanceId = None
        self.UserType = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.UserType = params.get("UserType")


class DescribeDCDBBinlogTimeResponse(AbstractModel):
    """DescribeDCDBBinlogTime返回参数结构体"""

    def __init__(self):
        """
        :param StartTime: 开始时间
        :type StartTime: str
        :param EndTime: 结束时间
        :type EndTime: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.StartTime = None
        self.EndTime = None
        self.RequestId = None

    def _deserialize(self, params):
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.RequestId = params.get("RequestId")


class DescribeDCDBInstanceDetailRequest(AbstractModel):
    """DescribeDCDBInstanceDetail请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID，形如dcdbt-7oaxtcb7
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class DescribeDCDBInstanceDetailResponse(AbstractModel):
    """DescribeDCDBInstanceDetail返回参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID，形如dcdbt-7oaxtcb7
        :type InstanceId: str
        :param InstanceName: 实例名称
        :type InstanceName: str
        :param Status: 实例状态。0-实例创建中；1-异步任务处理中；2-运行中；3-实例未初始化；-1-实例已隔离
        :type Status: int
        :param StatusDesc: 实例目前运行状态描述
        :type StatusDesc: str
        :param Vip: 实例内网IP地址
        :type Vip: str
        :param Vport: 实例内网端口
        :type Vport: int
        :param NodeCount: 实例节点数。值为2时表示一主一从，值为3时表示一主二从
        :type NodeCount: int
        :param Region: 实例所在地域名称，形如ap-guangzhou
        :type Region: str
        :param VpcId: 实例私有网络ID，形如vpc-r9jr0de3
        :type VpcId: str
        :param SubnetId: 实例私有网络子网ID，形如subnet-6rqs61o2
        :type SubnetId: str
        :param WanStatus: 外网状态，0-未开通；1-已开通；2-关闭；3-开通中
        :type WanStatus: int
        :param WanDomain: 外网访问的域名，公网可解析
        :type WanDomain: str
        :param WanVip: 外网IP地址，公网可访问
        :type WanVip: str
        :param WanPort: 外网访问端口
        :type WanPort: int
        :param ProjectId: 实例所属项目ID
        :type ProjectId: int
        :param AutoRenewFlag: 实例自动续费标志。0-正常续费；1-自动续费；2-到期不续费
        :type AutoRenewFlag: int
        :param ExclusterId: 独享集群ID
        :type ExclusterId: str
        :param PayMode: 付费模式。prepaid-预付费；postpaid-按量计费
        :type PayMode: str
        :param CreateTime: 实例创建时间，格式为 2006-01-02 15:04:05
        :type CreateTime: str
        :param PeriodEndTime: 实例到期时间，格式为 2006-01-02 15:04:05
        :type PeriodEndTime: str
        :param DbVersion: 数据库版本信息
        :type DbVersion: str
        :param IsAuditSupported: 实例是否支持审计。0-不支持；1-支持
        :type IsAuditSupported: int
        :param IsEncryptSupported: 实例是否支持数据加密。0-不支持；1-支持
        :type IsEncryptSupported: int
        :param Machine: 实例母机机器型号
        :type Machine: str
        :param Memory: 实例内存大小，单位 GB，各个分片的内存大小的和
        :type Memory: int
        :param Storage: 实例磁盘存储大小，单位 GB，各个分片的磁盘大小的和
        :type Storage: int
        :param StorageUsage: 实例存储空间使用率，计算方式为：各个分片已经使用的磁盘大小的和/各个分片的磁盘大小的和。
        :type StorageUsage: float
        :param LogStorage: 日志存储空间大小，单位GB
        :type LogStorage: int
        :param Pid: 产品类型ID
        :type Pid: int
        :param MasterZone: 主DB可用区
        :type MasterZone: str
        :param SlaveZones: 从DB可用区
        :type SlaveZones: list of str
        :param Shards: 分片信息
        :type Shards: list of ShardBriefInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceId = None
        self.InstanceName = None
        self.Status = None
        self.StatusDesc = None
        self.Vip = None
        self.Vport = None
        self.NodeCount = None
        self.Region = None
        self.VpcId = None
        self.SubnetId = None
        self.WanStatus = None
        self.WanDomain = None
        self.WanVip = None
        self.WanPort = None
        self.ProjectId = None
        self.AutoRenewFlag = None
        self.ExclusterId = None
        self.PayMode = None
        self.CreateTime = None
        self.PeriodEndTime = None
        self.DbVersion = None
        self.IsAuditSupported = None
        self.IsEncryptSupported = None
        self.Machine = None
        self.Memory = None
        self.Storage = None
        self.StorageUsage = None
        self.LogStorage = None
        self.Pid = None
        self.MasterZone = None
        self.SlaveZones = None
        self.Shards = None
        self.RequestId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.Status = params.get("Status")
        self.StatusDesc = params.get("StatusDesc")
        self.Vip = params.get("Vip")
        self.Vport = params.get("Vport")
        self.NodeCount = params.get("NodeCount")
        self.Region = params.get("Region")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.WanStatus = params.get("WanStatus")
        self.WanDomain = params.get("WanDomain")
        self.WanVip = params.get("WanVip")
        self.WanPort = params.get("WanPort")
        self.ProjectId = params.get("ProjectId")
        self.AutoRenewFlag = params.get("AutoRenewFlag")
        self.ExclusterId = params.get("ExclusterId")
        self.PayMode = params.get("PayMode")
        self.CreateTime = params.get("CreateTime")
        self.PeriodEndTime = params.get("PeriodEndTime")
        self.DbVersion = params.get("DbVersion")
        self.IsAuditSupported = params.get("IsAuditSupported")
        self.IsEncryptSupported = params.get("IsEncryptSupported")
        self.Machine = params.get("Machine")
        self.Memory = params.get("Memory")
        self.Storage = params.get("Storage")
        self.StorageUsage = params.get("StorageUsage")
        self.LogStorage = params.get("LogStorage")
        self.Pid = params.get("Pid")
        self.MasterZone = params.get("MasterZone")
        self.SlaveZones = params.get("SlaveZones")
        if params.get("Shards") is not None:
            self.Shards = []
            for item in params.get("Shards"):
                obj = ShardBriefInfo()
                obj._deserialize(item)
                self.Shards.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDCDBInstancesRequest(AbstractModel):
    """DescribeDCDBInstances请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 按照一个或者多个实例 ID 查询。实例 ID 形如：dcdbt-2t4cf98d
        :type InstanceIds: list of str
        :param SearchName: 搜索的字段名，当前支持的值有：instancename、vip、all。
        传 instancename 表示按实例名进行搜索；传 vip 表示按内网IP进行搜索；传 all 将会按实例ID、实例名和内网IP进行搜索。
        :type SearchName: str
        :param SearchKey: 搜索的关键字，支持模糊搜索。多个关键字使用换行符（'\n'）分割。
        :type SearchKey: str
        :param ProjectIds: 按项目 ID 查询
        :type ProjectIds: list of int
        :param IsFilterVpc: 是否根据 VPC 网络来搜索
        :type IsFilterVpc: bool
        :param VpcId: 私有网络 ID， IsFilterVpc 为 1 时有效
        :type VpcId: str
        :param SubnetId: 私有网络的子网 ID， IsFilterVpc 为 1 时有效
        :type SubnetId: str
        :param OrderBy: 排序字段， projectId， createtime， instancename 三者之一
        :type OrderBy: str
        :param OrderByType: 排序类型， desc 或者 asc
        :type OrderByType: str
        :param Offset: 偏移量，默认为 0
        :type Offset: int
        :param Limit: 返回数量，默认为 10，最大值为 100。
        :type Limit: int
        :param ExclusterType: 1非独享集群，2独享集群， 0全部
        :type ExclusterType: int
        :param IsFilterExcluster: 标识是否使用ExclusterType字段, false不使用，true使用
        :type IsFilterExcluster: bool
        :param ExclusterIds: 独享集群ID
        :type ExclusterIds: list of str
        """
        self.InstanceIds = None
        self.SearchName = None
        self.SearchKey = None
        self.ProjectIds = None
        self.IsFilterVpc = None
        self.VpcId = None
        self.SubnetId = None
        self.OrderBy = None
        self.OrderByType = None
        self.Offset = None
        self.Limit = None
        self.ExclusterType = None
        self.IsFilterExcluster = None
        self.ExclusterIds = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.SearchName = params.get("SearchName")
        self.SearchKey = params.get("SearchKey")
        self.ProjectIds = params.get("ProjectIds")
        self.IsFilterVpc = params.get("IsFilterVpc")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.OrderBy = params.get("OrderBy")
        self.OrderByType = params.get("OrderByType")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.ExclusterType = params.get("ExclusterType")
        self.IsFilterExcluster = params.get("IsFilterExcluster")
        self.ExclusterIds = params.get("ExclusterIds")


class DescribeDCDBInstancesResponse(AbstractModel):
    """DescribeDCDBInstances返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的实例数量
        :type TotalCount: int
        :param Instances: 实例详细信息列表
        :type Instances: list of DCDBInstanceInfo
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
                obj = DCDBInstanceInfo()
                obj._deserialize(item)
                self.Instances.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDCDBPriceRequest(AbstractModel):
    """DescribeDCDBPrice请求参数结构体"""

    def __init__(self):
        """
               :param Zone: 欲新购实例的可用区ID。
               :type Zone: str
               :param Count: 欲购买实例的数量，目前只支持购买1个实例
               :type Count: int
               :param Period: 欲购买的时长，单位：月。
               :type Period: int
               :param ShardNodeCount: 单个分片节点个数大小，可以通过 DescribeShardSpec
        查询实例规格获得。
               :type ShardNodeCount: int
               :param ShardMemory: 分片内存大小，单位：GB，可以通过 DescribeShardSpec
        查询实例规格获得。
               :type ShardMemory: int
               :param ShardStorage: 分片存储空间大小，单位：GB，可以通过 DescribeShardSpec
        查询实例规格获得。
               :type ShardStorage: int
               :param ShardCount: 实例分片个数，可选范围2-8，可以通过升级实例进行新增分片到最多64个分片。
               :type ShardCount: int
               :param Paymode: 付费类型。postpaid：按量付费   prepaid：预付费
               :type Paymode: str
        """
        self.Zone = None
        self.Count = None
        self.Period = None
        self.ShardNodeCount = None
        self.ShardMemory = None
        self.ShardStorage = None
        self.ShardCount = None
        self.Paymode = None

    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.Count = params.get("Count")
        self.Period = params.get("Period")
        self.ShardNodeCount = params.get("ShardNodeCount")
        self.ShardMemory = params.get("ShardMemory")
        self.ShardStorage = params.get("ShardStorage")
        self.ShardCount = params.get("ShardCount")
        self.Paymode = params.get("Paymode")


class DescribeDCDBPriceResponse(AbstractModel):
    """DescribeDCDBPrice返回参数结构体"""

    def __init__(self):
        """
        :param OriginalPrice: 原价，单位：分
        :type OriginalPrice: int
        :param Price: 实际价格，单位：分。受折扣等影响，可能和原价不同。
        :type Price: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.OriginalPrice = None
        self.Price = None
        self.RequestId = None

    def _deserialize(self, params):
        self.OriginalPrice = params.get("OriginalPrice")
        self.Price = params.get("Price")
        self.RequestId = params.get("RequestId")


class DescribeDCDBRenewalPriceRequest(AbstractModel):
    """DescribeDCDBRenewalPrice请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 待续费的实例ID。形如：dcdbt-ow728lmc，可以通过 DescribeDCDBInstances 查询实例详情获得。
        :type InstanceId: str
        :param Period: 续费时长，单位：月。不传则默认为1个月。
        :type Period: int
        """
        self.InstanceId = None
        self.Period = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Period = params.get("Period")


class DescribeDCDBRenewalPriceResponse(AbstractModel):
    """DescribeDCDBRenewalPrice返回参数结构体"""

    def __init__(self):
        """
        :param OriginalPrice: 原价，单位：分
        :type OriginalPrice: int
        :param Price: 实际价格，单位：分。受折扣等影响，可能和原价不同。
        :type Price: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.OriginalPrice = None
        self.Price = None
        self.RequestId = None

    def _deserialize(self, params):
        self.OriginalPrice = params.get("OriginalPrice")
        self.Price = params.get("Price")
        self.RequestId = params.get("RequestId")


class DescribeDCDBSaleInfoRequest(AbstractModel):
    """DescribeDCDBSaleInfo请求参数结构体"""


class DescribeDCDBSaleInfoResponse(AbstractModel):
    """DescribeDCDBSaleInfo返回参数结构体"""

    def __init__(self):
        """
        :param RegionList: 可售卖地域信息列表
        :type RegionList: list of RegionInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RegionList = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("RegionList") is not None:
            self.RegionList = []
            for item in params.get("RegionList"):
                obj = RegionInfo()
                obj._deserialize(item)
                self.RegionList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDCDBShardsRequest(AbstractModel):
    """DescribeDCDBShards请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID，形如：dcdbt-ow728lmc。
        :type InstanceId: str
        :param ShardInstanceIds: 分片Id列表。
        :type ShardInstanceIds: list of str
        :param Offset: 偏移量，默认为 0
        :type Offset: int
        :param Limit: 返回数量，默认为 20，最大值为 100。
        :type Limit: int
        :param OrderBy: 排序字段， 目前仅支持 createtime
        :type OrderBy: str
        :param OrderByType: 排序类型， desc 或者 asc
        :type OrderByType: str
        """
        self.InstanceId = None
        self.ShardInstanceIds = None
        self.Offset = None
        self.Limit = None
        self.OrderBy = None
        self.OrderByType = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.ShardInstanceIds = params.get("ShardInstanceIds")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.OrderBy = params.get("OrderBy")
        self.OrderByType = params.get("OrderByType")


class DescribeDCDBShardsResponse(AbstractModel):
    """DescribeDCDBShards返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的分片数量
        :type TotalCount: int
        :param Shards: 分片信息列表
        :type Shards: list of DCDBShardInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.Shards = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Shards") is not None:
            self.Shards = []
            for item in params.get("Shards"):
                obj = DCDBShardInfo()
                obj._deserialize(item)
                self.Shards.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDCDBUpgradePriceRequest(AbstractModel):
    """DescribeDCDBUpgradePrice请求参数结构体"""

    def __init__(self):
        """
                :param InstanceId: 待升级的实例ID。形如：dcdbt-ow728lmc，可以通过 DescribeDCDBInstances 查询实例详情获得。
                :type InstanceId: str
                :param UpgradeType: 升级类型，取值范围:
        <li> EXPAND: 升级实例中的已有分片 </li>
         <li> SPLIT: 将已有分片中的数据切分到新增分片上</li>
                :type UpgradeType: str
                :param AddShardConfig: 新增分片配置，当UpgradeType为ADD时生效。
                :type AddShardConfig: :class:`tcecloud.dcdb.v20180411.models.AddShardConfig`
                :param ExpandShardConfig: 扩容分片配置，当UpgradeType为EXPAND时生效。
                :type ExpandShardConfig: :class:`tcecloud.dcdb.v20180411.models.ExpandShardConfig`
                :param SplitShardConfig: 切分分片配置，当UpgradeType为SPLIT时生效。
                :type SplitShardConfig: :class:`tcecloud.dcdb.v20180411.models.SplitShardConfig`
        """
        self.InstanceId = None
        self.UpgradeType = None
        self.AddShardConfig = None
        self.ExpandShardConfig = None
        self.SplitShardConfig = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.UpgradeType = params.get("UpgradeType")
        if params.get("AddShardConfig") is not None:
            self.AddShardConfig = AddShardConfig()
            self.AddShardConfig._deserialize(params.get("AddShardConfig"))
        if params.get("ExpandShardConfig") is not None:
            self.ExpandShardConfig = ExpandShardConfig()
            self.ExpandShardConfig._deserialize(params.get("ExpandShardConfig"))
        if params.get("SplitShardConfig") is not None:
            self.SplitShardConfig = SplitShardConfig()
            self.SplitShardConfig._deserialize(params.get("SplitShardConfig"))


class DescribeDCDBUpgradePriceResponse(AbstractModel):
    """DescribeDCDBUpgradePrice返回参数结构体"""

    def __init__(self):
        """
        :param OriginalPrice: 原价，单位：分
        :type OriginalPrice: int
        :param Price: 实际价格，单位：分。受折扣等影响，可能和原价不同。
        :type Price: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.OriginalPrice = None
        self.Price = None
        self.RequestId = None

    def _deserialize(self, params):
        self.OriginalPrice = params.get("OriginalPrice")
        self.Price = params.get("Price")
        self.RequestId = params.get("RequestId")


class DescribeDatabaseObjectsRequest(AbstractModel):
    """DescribeDatabaseObjects请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：dcdbt-ow7t8lmc。
        :type InstanceId: str
        :param DbName: 数据库名称，通过 DescribeDatabases 接口获取。
        :type DbName: str
        """
        self.InstanceId = None
        self.DbName = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.DbName = params.get("DbName")


class DescribeDatabaseObjectsResponse(AbstractModel):
    """DescribeDatabaseObjects返回参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 透传入参。
        :type InstanceId: str
        :param DbName: 数据库名称。
        :type DbName: str
        :param Tables: 表列表。
        :type Tables: list of DatabaseTable
        :param Views: 视图列表。
        :type Views: list of DatabaseView
        :param Procs: 存储过程列表。
        :type Procs: list of DatabaseProcedure
        :param Funcs: 函数列表。
        :type Funcs: list of DatabaseFunction
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceId = None
        self.DbName = None
        self.Tables = None
        self.Views = None
        self.Procs = None
        self.Funcs = None
        self.RequestId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.DbName = params.get("DbName")
        if params.get("Tables") is not None:
            self.Tables = []
            for item in params.get("Tables"):
                obj = DatabaseTable()
                obj._deserialize(item)
                self.Tables.append(obj)
        if params.get("Views") is not None:
            self.Views = []
            for item in params.get("Views"):
                obj = DatabaseView()
                obj._deserialize(item)
                self.Views.append(obj)
        if params.get("Procs") is not None:
            self.Procs = []
            for item in params.get("Procs"):
                obj = DatabaseProcedure()
                obj._deserialize(item)
                self.Procs.append(obj)
        if params.get("Funcs") is not None:
            self.Funcs = []
            for item in params.get("Funcs"):
                obj = DatabaseFunction()
                obj._deserialize(item)
                self.Funcs.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDatabaseTableRequest(AbstractModel):
    """DescribeDatabaseTable请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：dcdbt-ow7t8lmc。
        :type InstanceId: str
        :param DbName: 数据库名称，通过 DescribeDatabases 接口获取。
        :type DbName: str
        :param Table: 表名称，通过 DescribeDatabaseObjects 接口获取。
        :type Table: str
        """
        self.InstanceId = None
        self.DbName = None
        self.Table = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.DbName = params.get("DbName")
        self.Table = params.get("Table")


class DescribeDatabaseTableResponse(AbstractModel):
    """DescribeDatabaseTable返回参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例名称。
        :type InstanceId: str
        :param DbName: 数据库名称。
        :type DbName: str
        :param Table: 表名称。
        :type Table: str
        :param Cols: 列信息。
        :type Cols: list of TableColumn
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceId = None
        self.DbName = None
        self.Table = None
        self.Cols = None
        self.RequestId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.DbName = params.get("DbName")
        self.Table = params.get("Table")
        if params.get("Cols") is not None:
            self.Cols = []
            for item in params.get("Cols"):
                obj = TableColumn()
                obj._deserialize(item)
                self.Cols.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDatabasesRequest(AbstractModel):
    """DescribeDatabases请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：dcdbt-ow7t8lmc。
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class DescribeDatabasesResponse(AbstractModel):
    """DescribeDatabases返回参数结构体"""

    def __init__(self):
        """
        :param Databases: 该实例上的数据库列表。
        :type Databases: list of Database
        :param InstanceId: 透传入参。
        :type InstanceId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Databases = None
        self.InstanceId = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Databases") is not None:
            self.Databases = []
            for item in params.get("Databases"):
                obj = Database()
                obj._deserialize(item)
                self.Databases.append(obj)
        self.InstanceId = params.get("InstanceId")
        self.RequestId = params.get("RequestId")


class DescribeFenceShardSpecRequest(AbstractModel):
    """DescribeFenceShardSpec请求参数结构体"""


class DescribeFenceShardSpecResponse(AbstractModel):
    """DescribeFenceShardSpec返回参数结构体"""

    def __init__(self):
        """
        :param SpecConfig: 按机型分类的可售卖规格列表
        :type SpecConfig: list of SpecConfig
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SpecConfig = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("SpecConfig") is not None:
            self.SpecConfig = []
            for item in params.get("SpecConfig"):
                obj = SpecConfig()
                obj._deserialize(item)
                self.SpecConfig.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeFlowRequest(AbstractModel):
    """DescribeFlow请求参数结构体"""

    def __init__(self):
        """
        :param FlowId: 异步请求接口返回的任务流程号。
        :type FlowId: int
        """
        self.FlowId = None

    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")


class DescribeFlowResponse(AbstractModel):
    """DescribeFlow返回参数结构体"""

    def __init__(self):
        """
        :param Status: 流程状态，0：成功，1：失败，2：运行中
        :type Status: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Status = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class DescribeInstancesRequest(AbstractModel):
    """DescribeInstances请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 实例ID的数组
        :type InstanceIds: list of str
        :param Limit: 每次最多拉取多少个实例
        :type Limit: int
        :param Offset: 拉取实例列表时候的偏移量
        :type Offset: int
        :param ProjectId: 按照项目ID进行过滤
        :type ProjectId: int
        :param UniqueVpcId: 私有网络ID，形如 vpc-nobbvxkf
        :type UniqueVpcId: str
        :param UniqueSubnetId: 子网ID，形如 subnet-dnn20os8
        :type UniqueSubnetId: str
        """
        self.InstanceIds = None
        self.Limit = None
        self.Offset = None
        self.ProjectId = None
        self.UniqueVpcId = None
        self.UniqueSubnetId = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.ProjectId = params.get("ProjectId")
        self.UniqueVpcId = params.get("UniqueVpcId")
        self.UniqueSubnetId = params.get("UniqueSubnetId")


class DescribeInstancesResponse(AbstractModel):
    """DescribeInstances返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的实例总的个数
        :type TotalCount: int
        :param Instances: 实例列表
        :type Instances: list of InstanceResource
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
                obj = InstanceResource()
                obj._deserialize(item)
                self.Instances.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeLatestCloudDBAReportRequest(AbstractModel):
    """DescribeLatestCloudDBAReport请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID
        :type InstanceId: str
        :param ShardId: DCDB实例分片ID
        :type ShardId: str
        """
        self.InstanceId = None
        self.ShardId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.ShardId = params.get("ShardId")


class DescribeLatestCloudDBAReportResponse(AbstractModel):
    """DescribeLatestCloudDBAReport返回参数结构体"""

    def __init__(self):
        """
        :param Score: 本次检测的有效分数
        :type Score: int
        :param ReportName: 本次检测报告的名称
        :type ReportName: str
        :param ReportDetail: 本次检测报告的详情
        :type ReportDetail: str
        :param FinishTime: 本次检测报告的完成时间
        :type FinishTime: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Score = None
        self.ReportName = None
        self.ReportDetail = None
        self.FinishTime = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Score = params.get("Score")
        self.ReportName = params.get("ReportName")
        self.ReportDetail = params.get("ReportDetail")
        self.FinishTime = params.get("FinishTime")
        self.RequestId = params.get("RequestId")


class DescribeLogFileRetentionPeriodRequest(AbstractModel):
    """DescribeLogFileRetentionPeriod请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc。
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class DescribeLogFileRetentionPeriodResponse(AbstractModel):
    """DescribeLogFileRetentionPeriod返回参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc。
        :type InstanceId: str
        :param Days: 日志备份天数
        :type Days: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceId = None
        self.Days = None
        self.RequestId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Days = params.get("Days")
        self.RequestId = params.get("RequestId")


class DescribeOrdersRequest(AbstractModel):
    """DescribeOrders请求参数结构体"""

    def __init__(self):
        """
        :param DealNames: 待查询的长订单号列表，创建实例、续费实例、扩容实例接口返回。
        :type DealNames: list of str
        """
        self.DealNames = None

    def _deserialize(self, params):
        self.DealNames = params.get("DealNames")


class DescribeOrdersResponse(AbstractModel):
    """DescribeOrders返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 返回的订单数量。
        :type TotalCount: list of int
        :param Deals: 订单信息列表。
        :type Deals: list of Deal
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.Deals = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Deals") is not None:
            self.Deals = []
            for item in params.get("Deals"):
                obj = Deal()
                obj._deserialize(item)
                self.Deals.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeProjectSecurityGroupsRequest(AbstractModel):
    """DescribeProjectSecurityGroups请求参数结构体"""

    def __init__(self):
        """
        :param Product: 数据库引擎名称：mariadb,cdb,cynosdb,dcdb,redis,mongodb
        :type Product: str
        :param ProjectId: 项目Id
        :type ProjectId: int
        """
        self.Product = None
        self.ProjectId = None

    def _deserialize(self, params):
        self.Product = params.get("Product")
        self.ProjectId = params.get("ProjectId")


class DescribeProjectSecurityGroupsResponse(AbstractModel):
    """DescribeProjectSecurityGroups返回参数结构体"""

    def __init__(self):
        """
        :param Groups: 安全组规则。
        :type Groups: list of SecurityGroup
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Groups = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Groups") is not None:
            self.Groups = []
            for item in params.get("Groups"):
                obj = SecurityGroup()
                obj._deserialize(item)
                self.Groups.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeProjectsRequest(AbstractModel):
    """DescribeProjects请求参数结构体"""


class DescribeProjectsResponse(AbstractModel):
    """DescribeProjects返回参数结构体"""

    def __init__(self):
        """
        :param Projects: 项目列表
        :type Projects: list of Project
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Projects = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Projects") is not None:
            self.Projects = []
            for item in params.get("Projects"):
                obj = Project()
                obj._deserialize(item)
                self.Projects.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeShardSpecRequest(AbstractModel):
    """DescribeShardSpec请求参数结构体"""


class DescribeShardSpecResponse(AbstractModel):
    """DescribeShardSpec返回参数结构体"""

    def __init__(self):
        """
        :param SpecConfig: 按机型分类的可售卖规格列表
        :type SpecConfig: list of SpecConfig
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SpecConfig = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("SpecConfig") is not None:
            self.SpecConfig = []
            for item in params.get("SpecConfig"):
                obj = SpecConfig()
                obj._deserialize(item)
                self.SpecConfig.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeSqlLogsRequest(AbstractModel):
    """DescribeSqlLogs请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：dcdbt-ow728lmc，可以通过 DescribeDCDBInstances 查询实例详情获得。
        :type InstanceId: str
        :param Offset: SQL日志偏移。
        :type Offset: int
        :param Limit: 拉取数量（0-10000，为0时拉取总数信息）。
        :type Limit: int
        """
        self.InstanceId = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeSqlLogsResponse(AbstractModel):
    """DescribeSqlLogs返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 当前消息队列中的sql日志条目数。
        :type TotalCount: int
        :param StartOffset: 消息队列中的sql日志起始偏移。
        :type StartOffset: int
        :param EndOffset: 消息队列中的sql日志结束偏移。
        :type EndOffset: int
        :param Offset: 返回的第一条sql日志的偏移。
        :type Offset: int
        :param Count: 返回的sql日志数量。
        :type Count: int
        :param SqlItems: Sql日志列表。
        :type SqlItems: list of SqlLogItem
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.StartOffset = None
        self.EndOffset = None
        self.Offset = None
        self.Count = None
        self.SqlItems = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        self.StartOffset = params.get("StartOffset")
        self.EndOffset = params.get("EndOffset")
        self.Offset = params.get("Offset")
        self.Count = params.get("Count")
        if params.get("SqlItems") is not None:
            self.SqlItems = []
            for item in params.get("SqlItems"):
                obj = SqlLogItem()
                obj._deserialize(item)
                self.SqlItems.append(obj)
        self.RequestId = params.get("RequestId")


class DestroyHourDCDBInstanceRequest(AbstractModel):
    """DestroyHourDCDBInstance请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID，形如dcdbt-87zif6ha
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class DestroyHourDCDBInstanceResponse(AbstractModel):
    """DestroyHourDCDBInstance返回参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID，形如dcdbt-87zif6ha
        :type InstanceId: str
        :param FlowId: 删除DCDB任务异步流程ID，以FlowId作为参数调用API 接口DescribeFlow 查询删除任务执行状态。
        :type FlowId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceId = None
        self.FlowId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class ExpandShardConfig(AbstractModel):
    """升级实例 -- 扩容分片类型"""

    def __init__(self):
        """
        :param ShardInstanceIds: 分片ID数组
        :type ShardInstanceIds: list of str
        :param ShardMemory: 分片内存大小，单位 GB
        :type ShardMemory: int
        :param ShardStorage: 分片存储大小，单位 GB
        :type ShardStorage: int
        """
        self.ShardInstanceIds = None
        self.ShardMemory = None
        self.ShardStorage = None

    def _deserialize(self, params):
        self.ShardInstanceIds = params.get("ShardInstanceIds")
        self.ShardMemory = params.get("ShardMemory")
        self.ShardStorage = params.get("ShardStorage")


class FenceInfoItem(AbstractModel):
    """独享资源池信息"""

    def __init__(self):
        """
        :param FenceId: 独享资源池ID
        :type FenceId: str
        """
        self.FenceId = None

    def _deserialize(self, params):
        self.FenceId = params.get("FenceId")


class GrantAccountPrivilegesRequest(AbstractModel):
    """GrantAccountPrivileges请求参数结构体"""

    def __init__(self):
        r"""
                :param InstanceId: 实例 ID，形如：dcdbt-ow728lmc。
                :type InstanceId: str
                :param UserName: 登录用户名。
                :type UserName: str
                :param Host: 用户允许的访问 host，用户名+host唯一确定一个账号。
                :type Host: str
                :param DbName: 数据库名。如果为 \*，表示查询全局权限（即 \*.\*），此时忽略 Type 和 Object 参数
                :type DbName: str
                :param Privileges: 全局权限： SELECT，INSERT，UPDATE，DELETE，CREATE，DROP，REFERENCES，
                INDEX，ALTER，CREATE TEMPORARY TABLES，LOCK TABLES，EXECUTE，CREATE VIEW，SHOW VIEW，
                CREATE ROUTINE，ALTER ROUTINE，EVENT，TRIGGER，SHOW DATABASES
        库权限： SELECT，INSERT，UPDATE，DELETE，CREATE，DROP，REFERENCES，INDEX，ALTER，CREATE TEMPORARY TABLES，
        LOCK TABLES，EXECUTE，CREATE VIEW，SHOW VIEW，CREATE ROUTINE，ALTER ROUTINE，EVENT，TRIGGER
        表/视图权限： SELECT，INSERT，UPDATE，DELETE，CREATE，DROP，REFERENCES，INDEX，ALTER，CREATE VIEW，
        SHOW VIEW，TRIGGER
        存储过程/函数权限： ALTER ROUTINE，EXECUTE
        字段权限： INSERT，REFERENCES，SELECT，UPDATE
                :type Privileges: list of str
                :param Type: 类型,可以填入 table 、 view 、 proc 、 func 和 \*。当 DbName 为具体数据库名，
                Type为 \* 时，表示设置该数据库权限（即db.\*），此时忽略 Object 参数
                :type Type: str
                :param Object: 具体的 Type 的名称，比如 Type 为 table 时就是具体的表名。DbName 和 Type 都为具体名称，
                则 Object 表示具体对象名，不能为 \* 或者为空
                :type Object: str
                :param ColName: 当 Type=table 时，ColName 为 \* 表示对表授权，如果为具体字段名，表示对字段授权
                :type ColName: str
        """
        self.InstanceId = None
        self.UserName = None
        self.Host = None
        self.DbName = None
        self.Privileges = None
        self.Type = None
        self.Object = None
        self.ColName = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.UserName = params.get("UserName")
        self.Host = params.get("Host")
        self.DbName = params.get("DbName")
        self.Privileges = params.get("Privileges")
        self.Type = params.get("Type")
        self.Object = params.get("Object")
        self.ColName = params.get("ColName")


class GrantAccountPrivilegesResponse(AbstractModel):
    """GrantAccountPrivileges返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class Inbound(AbstractModel):
    """安全组入站规则"""

    def __init__(self):
        """
        :param Action: 策略，ACCEPT或者DROP。
        :type Action: str
        :param AddressModule: 地址组id代表的地址集合。
        :type AddressModule: str
        :param CidrIp: 来源Ip或Ip段，例如192.168.0.0/16。
        :type CidrIp: str
        :param Desc: 描述。
        :type Desc: str
        :param IpProtocol: 网络协议，支持udp、tcp等。
        :type IpProtocol: str
        :param PortRange: 端口。
        :type PortRange: str
        :param ServiceModule: 服务组id代表的协议和端口集合。
        :type ServiceModule: str
        :param Id: 安全组id代表的地址集合。
        :type Id: str
        """
        self.Action = None
        self.AddressModule = None
        self.CidrIp = None
        self.Desc = None
        self.IpProtocol = None
        self.PortRange = None
        self.ServiceModule = None
        self.Id = None

    def _deserialize(self, params):
        self.Action = params.get("Action")
        self.AddressModule = params.get("AddressModule")
        self.CidrIp = params.get("CidrIp")
        self.Desc = params.get("Desc")
        self.IpProtocol = params.get("IpProtocol")
        self.PortRange = params.get("PortRange")
        self.ServiceModule = params.get("ServiceModule")
        self.Id = params.get("Id")


class InitDCDBInstancesRequest(AbstractModel):
    """InitDCDBInstances请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 待初始化的实例Id列表，形如：dcdbt-ow728lmc，可以通过 DescribeDCDBInstances 查询实例详情获得。
        :type InstanceIds: list of str
        :param Params: 参数列表。本接口的可选值为：character_set_server（字符集，必传），
        lower_case_table_names（表名大小写敏感，必传，0 - 敏感；1-不敏感），
        innodb_page_size（innodb数据页，默认16K），sync_mode（同步模式：0 - 异步； 1 - 强同步；2 - 强同步可退化。默认为强同步）。
        :type Params: list of DBParamValue
        """
        self.InstanceIds = None
        self.Params = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        if params.get("Params") is not None:
            self.Params = []
            for item in params.get("Params"):
                obj = DBParamValue()
                obj._deserialize(item)
                self.Params.append(obj)


class InitDCDBInstancesResponse(AbstractModel):
    """InitDCDBInstances返回参数结构体"""

    def __init__(self):
        """
        :param FlowIds: 异步任务Id，可通过 DescribeFlow 查询任务状态。
        :type FlowIds: list of int non-negative
        :param InstanceIds: 透传入参。
        :type InstanceIds: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FlowIds = None
        self.InstanceIds = None
        self.RequestId = None

    def _deserialize(self, params):
        self.FlowIds = params.get("FlowIds")
        self.InstanceIds = params.get("InstanceIds")
        self.RequestId = params.get("RequestId")


class InstanceResource(AbstractModel):
    """数据库实例信息"""

    def __init__(self):
        """
        :param Id: 数据库实例的数字ID
        :type Id: int
        :param InstanceId: 实例ID，形如 dcdbt-ifzc58fh或者tdsqlshard-ifzc58fh
        :type InstanceId: str
        :param InstanceName: 实例名称
        :type InstanceName: str
        :param AppId: 账户的应用ID
        :type AppId: int
        :param OriginSerialId: 实例的原始SerialId
        :type OriginSerialId: str
        :param SerialId: 实例的当前SerialId
        :type SerialId: str
        :param Region: 实例所在地域
        :type Region: str
        :param Zone: 实例所在可用区
        :type Zone: str
        :param VpcId: 实例所属VPC的数字ID
        :type VpcId: int
        :param SubnetId: 实例所属子网的数字ID
        :type SubnetId: int
        :param UniqueVpcId: 实例所属VPC的字符串唯一ID
        :type UniqueVpcId: str
        :param UniqueSubnetId: 实例所属子网的字符串唯一ID
        :type UniqueSubnetId: str
        :param Status: 实例运行状态
        :type Status: int
        :param Vip: 实例Vip
        :type Vip: str
        :param Vport: 实例Vport
        :type Vport: int
        :param ZkName: 实例所属Zk的名字
        :type ZkName: str
        :param ClusterName: 实例所属集群的名字
        :type ClusterName: str
        :param NodeCount: 实例的节点个数
        :type NodeCount: int
        :param DbVersion: 实例的数据库版本
        :type DbVersion: str
        :param ShardDetail: 分片信息
        :type ShardDetail: list of InstanceShardInfo
        """
        self.Id = None
        self.InstanceId = None
        self.InstanceName = None
        self.AppId = None
        self.OriginSerialId = None
        self.SerialId = None
        self.Region = None
        self.Zone = None
        self.VpcId = None
        self.SubnetId = None
        self.UniqueVpcId = None
        self.UniqueSubnetId = None
        self.Status = None
        self.Vip = None
        self.Vport = None
        self.ZkName = None
        self.ClusterName = None
        self.NodeCount = None
        self.DbVersion = None
        self.ShardDetail = None

    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.AppId = params.get("AppId")
        self.OriginSerialId = params.get("OriginSerialId")
        self.SerialId = params.get("SerialId")
        self.Region = params.get("Region")
        self.Zone = params.get("Zone")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.UniqueVpcId = params.get("UniqueVpcId")
        self.UniqueSubnetId = params.get("UniqueSubnetId")
        self.Status = params.get("Status")
        self.Vip = params.get("Vip")
        self.Vport = params.get("Vport")
        self.ZkName = params.get("ZkName")
        self.ClusterName = params.get("ClusterName")
        self.NodeCount = params.get("NodeCount")
        self.DbVersion = params.get("DbVersion")
        if params.get("ShardDetail") is not None:
            self.ShardDetail = []
            for item in params.get("ShardDetail"):
                obj = InstanceShardInfo()
                obj._deserialize(item)
                self.ShardDetail.append(obj)


class InstanceShardInfo(AbstractModel):
    """TDSQL实例的分片信息"""

    def __init__(self):
        """
        :param ShardInstanceId: 分片ID
        :type ShardInstanceId: str
        :param ShardSerialId: 分片的SerialId
        :type ShardSerialId: str
        :param Status: 分片的运行状态
        :type Status: int
        """
        self.ShardInstanceId = None
        self.ShardSerialId = None
        self.Status = None

    def _deserialize(self, params):
        self.ShardInstanceId = params.get("ShardInstanceId")
        self.ShardSerialId = params.get("ShardSerialId")
        self.Status = params.get("Status")


class IsolateDedicatedDBInstanceRequest(AbstractModel):
    """IsolateDedicatedDBInstance请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 Id，形如：dcdbt-ow728lmc。
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class IsolateDedicatedDBInstanceResponse(AbstractModel):
    """IsolateDedicatedDBInstance返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class IsolateHourDCDBInstanceRequest(AbstractModel):
    """IsolateHourDCDBInstance请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID，形如dcdbt-87zif6ha。
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class IsolateHourDCDBInstanceResponse(AbstractModel):
    """IsolateHourDCDBInstance返回参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID，形如dcdbt-87zif6ha。
        :type InstanceId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.RequestId = params.get("RequestId")


class LogFileInfo(AbstractModel):
    """拉取的日志信息"""

    def __init__(self):
        """
        :param Mtime: Log最后修改时间
        :type Mtime: int
        :param Length: 文件长度
        :type Length: int
        :param Uri: 下载Log时用到的统一资源标识符
        :type Uri: str
        :param FileName: 文件名
        :type FileName: str
        """
        self.Mtime = None
        self.Length = None
        self.Uri = None
        self.FileName = None

    def _deserialize(self, params):
        self.Mtime = params.get("Mtime")
        self.Length = params.get("Length")
        self.Uri = params.get("Uri")
        self.FileName = params.get("FileName")


class MetricDataPoint(AbstractModel):
    """监控指标数据点"""

    def __init__(self):
        """
        :param MetricName: 指标名称
        :type MetricName: str
        :param Values: 监控值数组，该数组和Timestamps一一对应
        :type Values: list of float
        :param Timestamps: 时间戳数组，表示那些时间点有数据，缺失的时间戳，没有数据点，可以理解为掉点了
        :type Timestamps: list of float
        """
        self.MetricName = None
        self.Values = None
        self.Timestamps = None

    def _deserialize(self, params):
        self.MetricName = params.get("MetricName")
        self.Values = params.get("Values")
        self.Timestamps = params.get("Timestamps")


class ModifyAccountDescriptionRequest(AbstractModel):
    """ModifyAccountDescription请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：dcdbt-ow728lmc。
        :type InstanceId: str
        :param UserName: 登录用户名。
        :type UserName: str
        :param Host: 用户允许的访问 host，用户名+host唯一确定一个账号。
        :type Host: str
        :param Description: 新的账号备注，长度 0~256。
        :type Description: str
        """
        self.InstanceId = None
        self.UserName = None
        self.Host = None
        self.Description = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.UserName = params.get("UserName")
        self.Host = params.get("Host")
        self.Description = params.get("Description")


class ModifyAccountDescriptionResponse(AbstractModel):
    """ModifyAccountDescription返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyAutoRenewFlagRequest(AbstractModel):
    """ModifyAutoRenewFlag请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 实例 ID列表，形如：dcdbt-ow728lmc。
        :type InstanceIds: list of str
        :param AutoRenewFlag: 自动续费标记。
        :type AutoRenewFlag: int
        """
        self.InstanceIds = None
        self.AutoRenewFlag = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.AutoRenewFlag = params.get("AutoRenewFlag")


class ModifyAutoRenewFlagResponse(AbstractModel):
    """ModifyAutoRenewFlag返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDBInstanceNameRequest(AbstractModel):
    """ModifyDBInstanceName请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID，形如tdsql-hdaprz0v
        :type InstanceId: str
        :param InstanceName: 实例名称
        :type InstanceName: str
        """
        self.InstanceId = None
        self.InstanceName = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")


class ModifyDBInstanceNameResponse(AbstractModel):
    """ModifyDBInstanceName返回参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID
        :type InstanceId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.RequestId = params.get("RequestId")


class ModifyDBInstanceSecurityGroupsRequest(AbstractModel):
    """ModifyDBInstanceSecurityGroups请求参数结构体"""

    def __init__(self):
        """
        :param Product: 数据库引擎名称：mariadb,cdb,cynosdb,dcdb,redis,mongodb 等。
        :type Product: str
        :param SecurityGroupIds: 要修改的安全组ID列表，一个或者多个安全组Id组成的数组。
        :type SecurityGroupIds: list of str
        :param InstanceId: 实例ID，格式如：cdb-c1nl9rpv或者cdbro-c1nl9rpv，与云数据库控制台页面中显示的实例ID相同
        :type InstanceId: str
        """
        self.Product = None
        self.SecurityGroupIds = None
        self.InstanceId = None

    def _deserialize(self, params):
        self.Product = params.get("Product")
        self.SecurityGroupIds = params.get("SecurityGroupIds")
        self.InstanceId = params.get("InstanceId")


class ModifyDBInstanceSecurityGroupsResponse(AbstractModel):
    """ModifyDBInstanceSecurityGroups返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDBInstancesProjectRequest(AbstractModel):
    """ModifyDBInstancesProject请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 待修改的实例ID列表。实例 ID 形如：dcdbt-ow728lmc。
        :type InstanceIds: list of str
        :param ProjectId: 要分配的项目 ID，可以通过 DescribeProjects 查询项目列表接口获取。
        :type ProjectId: int
        """
        self.InstanceIds = None
        self.ProjectId = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.ProjectId = params.get("ProjectId")


class ModifyDBInstancesProjectResponse(AbstractModel):
    """ModifyDBInstancesProject返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDBParametersRequest(AbstractModel):
    """ModifyDBParameters请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：dcdbt-ow728lmc。
        :type InstanceId: str
        :param Params: 参数列表，每一个元素是Param和Value的组合
        :type Params: list of DBParamValue
        """
        self.InstanceId = None
        self.Params = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("Params") is not None:
            self.Params = []
            for item in params.get("Params"):
                obj = DBParamValue()
                obj._deserialize(item)
                self.Params.append(obj)


class ModifyDBParametersResponse(AbstractModel):
    """ModifyDBParameters返回参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：dcdbt-ow728lmc。
        :type InstanceId: str
        :param Result: 各参数修改结果
        :type Result: list of ParamModifyResult
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceId = None
        self.Result = None
        self.RequestId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("Result") is not None:
            self.Result = []
            for item in params.get("Result"):
                obj = ParamModifyResult()
                obj._deserialize(item)
                self.Result.append(obj)
        self.RequestId = params.get("RequestId")


class ModifyDBSyncModeRequest(AbstractModel):
    """ModifyDBSyncMode请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 待修改同步模式的实例ID。形如：dcdbt-ow728lmc。
        :type InstanceId: str
        :param SyncMode: 同步模式：0 异步，1 强同步， 2 强同步可退化
        :type SyncMode: int
        """
        self.InstanceId = None
        self.SyncMode = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.SyncMode = params.get("SyncMode")


class ModifyDBSyncModeResponse(AbstractModel):
    """ModifyDBSyncMode返回参数结构体"""

    def __init__(self):
        """
        :param FlowId: 异步任务Id，可通过 DescribeFlow 查询任务状态。
        :type FlowId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class ModifyInstanceNetworkRequest(AbstractModel):
    """ModifyInstanceNetwork请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID
        :type InstanceId: str
        :param VpcId: 希望转到的VPC网络的VpcId
        :type VpcId: str
        :param SubnetId: 希望转到的VPC网络的子网ID
        :type SubnetId: str
        :param Vip: 如果需要指定VIP，填上该字段
        :type Vip: str
        """
        self.InstanceId = None
        self.VpcId = None
        self.SubnetId = None
        self.Vip = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.Vip = params.get("Vip")


class ModifyInstanceNetworkResponse(AbstractModel):
    """ModifyInstanceNetwork返回参数结构体"""

    def __init__(self):
        """
        :param FlowId: 异步任务ID，根据此FlowId通过DescribeFlow接口查询任务进行状态
        :type FlowId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class ModifyInstanceRemarkRequest(AbstractModel):
    """ModifyInstanceRemark请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID
        :type InstanceId: str
        :param Remark: 备注
        :type Remark: str
        """
        self.InstanceId = None
        self.Remark = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Remark = params.get("Remark")


class ModifyInstanceRemarkResponse(AbstractModel):
    """ModifyInstanceRemark返回参数结构体"""

    def __init__(self):
        """
        :param Remark: 备注
        :type Remark: str
        :param IsModify: 是否修改
        :type IsModify: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Remark = None
        self.IsModify = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Remark = params.get("Remark")
        self.IsModify = params.get("IsModify")
        self.RequestId = params.get("RequestId")


class ModifyInstanceVipRequest(AbstractModel):
    """ModifyInstanceVip请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID
        :type InstanceId: str
        :param Vip: 实例Vip
        :type Vip: str
        """
        self.InstanceId = None
        self.Vip = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Vip = params.get("Vip")


class ModifyInstanceVipResponse(AbstractModel):
    """ModifyInstanceVip返回参数结构体"""

    def __init__(self):
        """
        :param FlowId: 异步任务流程ID
        :type FlowId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class ModifyInstanceVportRequest(AbstractModel):
    """ModifyInstanceVport请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID
        :type InstanceId: str
        :param Vport: 目标 vport
        :type Vport: int
        """
        self.InstanceId = None
        self.Vport = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Vport = params.get("Vport")


class ModifyInstanceVportResponse(AbstractModel):
    """ModifyInstanceVport返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyLogFileRetentionPeriodRequest(AbstractModel):
    """ModifyLogFileRetentionPeriod请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc。
        :type InstanceId: str
        :param Days: 保存的天数,不能超过30
        :type Days: int
        """
        self.InstanceId = None
        self.Days = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Days = params.get("Days")


class ModifyLogFileRetentionPeriodResponse(AbstractModel):
    """ModifyLogFileRetentionPeriod返回参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc。
        :type InstanceId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.RequestId = params.get("RequestId")


class OpenDBExtranetAccessRequest(AbstractModel):
    """OpenDBExtranetAccess请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 待开放外网访问的实例ID。形如：dcdbt-ow728lmc。
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class OpenDBExtranetAccessResponse(AbstractModel):
    """OpenDBExtranetAccess返回参数结构体"""

    def __init__(self):
        """
        :param FlowId: 异步任务Id，可通过 DescribeFlow 查询任务状态。
        :type FlowId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class Outbound(AbstractModel):
    """安全组出站规则"""

    def __init__(self):
        """
        :param Action: 策略，ACCEPT或者DROP。
        :type Action: str
        :param AddressModule: 地址组id代表的地址集合。
        :type AddressModule: str
        :param CidrIp: 来源Ip或Ip段，例如192.168.0.0/16。
        :type CidrIp: str
        :param Desc: 描述。
        :type Desc: str
        :param IpProtocol: 网络协议，支持udp、tcp等。
        :type IpProtocol: str
        :param PortRange: 端口。
        :type PortRange: str
        :param ServiceModule: 服务组id代表的协议和端口集合。
        :type ServiceModule: str
        :param Id: 安全组id代表的地址集合。
        :type Id: str
        """
        self.Action = None
        self.AddressModule = None
        self.CidrIp = None
        self.Desc = None
        self.IpProtocol = None
        self.PortRange = None
        self.ServiceModule = None
        self.Id = None

    def _deserialize(self, params):
        self.Action = params.get("Action")
        self.AddressModule = params.get("AddressModule")
        self.CidrIp = params.get("CidrIp")
        self.Desc = params.get("Desc")
        self.IpProtocol = params.get("IpProtocol")
        self.PortRange = params.get("PortRange")
        self.ServiceModule = params.get("ServiceModule")
        self.Id = params.get("Id")


class ParamConstraint(AbstractModel):
    """参数约束"""

    def __init__(self):
        """
                :param Type: 约束类型,如枚举enum，区间section
                :type Type: str
                :param Enum: 约束类型为enum时的可选值列表
                :type Enum: str
                :param Range: 约束类型为section时的范围
        注意：此字段可能返回 null，表示取不到有效值。
                :type Range: :class:`tcecloud.dcdb.v20180411.models.ConstraintRange`
                :param String: 约束类型为string时的可选值列表
                :type String: str
        """
        self.Type = None
        self.Enum = None
        self.Range = None
        self.String = None

    def _deserialize(self, params):
        self.Type = params.get("Type")
        self.Enum = params.get("Enum")
        if params.get("Range") is not None:
            self.Range = ConstraintRange()
            self.Range._deserialize(params.get("Range"))
        self.String = params.get("String")


class ParamDesc(AbstractModel):
    """DB参数描述"""

    def __init__(self):
        """
                :param Param: 参数名字
                :type Param: str
                :param Value: 当前参数值
                :type Value: str
                :param SetValue: 设置过的值，参数生效后，该值和value一样。未设置过就不返回该字段。
        注意：此字段可能返回 null，表示取不到有效值。
                :type SetValue: str
                :param Default: 系统默认值
                :type Default: str
                :param Constraint: 参数限制
                :type Constraint: :class:`tcecloud.dcdb.v20180411.models.ParamConstraint`
        """
        self.Param = None
        self.Value = None
        self.SetValue = None
        self.Default = None
        self.Constraint = None

    def _deserialize(self, params):
        self.Param = params.get("Param")
        self.Value = params.get("Value")
        self.SetValue = params.get("SetValue")
        self.Default = params.get("Default")
        if params.get("Constraint") is not None:
            self.Constraint = ParamConstraint()
            self.Constraint._deserialize(params.get("Constraint"))


class ParamModifyResult(AbstractModel):
    """修改参数结果"""

    def __init__(self):
        """
        :param Param: 修改参数名字
        :type Param: str
        :param Code: 参数修改结果。0表示修改成功；-1表示修改失败；-2表示该参数值非法
        :type Code: int
        """
        self.Param = None
        self.Code = None

    def _deserialize(self, params):
        self.Param = params.get("Param")
        self.Code = params.get("Code")


class Permission(AbstractModel):
    """描述对资源权限，仅内部使用。"""

    def __init__(self):
        """
        :param Resource: 资源对象
        :type Resource: str
        :param IsPermitted: 是否有权限，1 - 有权限， 0 - 无权限
        :type IsPermitted: int
        """
        self.Resource = None
        self.IsPermitted = None

    def _deserialize(self, params):
        self.Resource = params.get("Resource")
        self.IsPermitted = params.get("IsPermitted")


class Project(AbstractModel):
    """项目信息描述"""

    def __init__(self):
        """
        :param ProjectId: 项目ID
        :type ProjectId: int
        :param OwnerUin: 资源拥有者（主账号）uin
        :type OwnerUin: int
        :param AppId: 应用Id
        :type AppId: int
        :param Name: 项目名称
        :type Name: str
        :param CreatorUin: 创建者uin
        :type CreatorUin: int
        :param SrcPlat: 来源平台
        :type SrcPlat: str
        :param SrcAppId: 来源AppId
        :type SrcAppId: int
        :param Status: 项目状态,0正常，-1关闭。默认项目为3
        :type Status: int
        :param CreateTime: 创建时间
        :type CreateTime: str
        :param IsDefault: 是否默认项目，1 是，0 不是
        :type IsDefault: int
        :param Info: 描述信息
        :type Info: str
        """
        self.ProjectId = None
        self.OwnerUin = None
        self.AppId = None
        self.Name = None
        self.CreatorUin = None
        self.SrcPlat = None
        self.SrcAppId = None
        self.Status = None
        self.CreateTime = None
        self.IsDefault = None
        self.Info = None

    def _deserialize(self, params):
        self.ProjectId = params.get("ProjectId")
        self.OwnerUin = params.get("OwnerUin")
        self.AppId = params.get("AppId")
        self.Name = params.get("Name")
        self.CreatorUin = params.get("CreatorUin")
        self.SrcPlat = params.get("SrcPlat")
        self.SrcAppId = params.get("SrcAppId")
        self.Status = params.get("Status")
        self.CreateTime = params.get("CreateTime")
        self.IsDefault = params.get("IsDefault")
        self.Info = params.get("Info")


class RegionInfo(AbstractModel):
    """售卖可用区信息"""

    def __init__(self):
        """
        :param Region: 地域英文ID
        :type Region: str
        :param RegionId: 地域数字ID
        :type RegionId: int
        :param RegionName: 地域中文名
        :type RegionName: str
        :param ZoneList: 可用区列表
        :type ZoneList: list of ZonesInfo
        :param AvailableChoice: 可选择的主可用区和从可用区
        :type AvailableChoice: list of ShardZoneChooseInfo
        """
        self.Region = None
        self.RegionId = None
        self.RegionName = None
        self.ZoneList = None
        self.AvailableChoice = None

    def _deserialize(self, params):
        self.Region = params.get("Region")
        self.RegionId = params.get("RegionId")
        self.RegionName = params.get("RegionName")
        if params.get("ZoneList") is not None:
            self.ZoneList = []
            for item in params.get("ZoneList"):
                obj = ZonesInfo()
                obj._deserialize(item)
                self.ZoneList.append(obj)
        if params.get("AvailableChoice") is not None:
            self.AvailableChoice = []
            for item in params.get("AvailableChoice"):
                obj = ShardZoneChooseInfo()
                obj._deserialize(item)
                self.AvailableChoice.append(obj)


class RenewDCDBInstanceRequest(AbstractModel):
    """RenewDCDBInstance请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 待续费的实例ID。形如：dcdbt-ow728lmc，可以通过 DescribeDCDBInstances 查询实例详情获得。
        :type InstanceId: str
        :param Period: 续费时长，单位：月。
        :type Period: int
        :param AutoVoucher: 是否自动使用代金券进行支付，默认不使用。
        :type AutoVoucher: bool
        :param VoucherIds: 代金券ID列表，目前仅支持指定一张代金券。
        :type VoucherIds: list of str
        """
        self.InstanceId = None
        self.Period = None
        self.AutoVoucher = None
        self.VoucherIds = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Period = params.get("Period")
        self.AutoVoucher = params.get("AutoVoucher")
        self.VoucherIds = params.get("VoucherIds")


class RenewDCDBInstanceResponse(AbstractModel):
    """RenewDCDBInstance返回参数结构体"""

    def __init__(self):
        """
               :param DealName: 长订单号。可以据此调用 DescribeOrders
        查询订单详细信息，或在支付失败时调用用户账号相关接口进行支付。
               :type DealName: str
               :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
               :type RequestId: str
        """
        self.DealName = None
        self.RequestId = None

    def _deserialize(self, params):
        self.DealName = params.get("DealName")
        self.RequestId = params.get("RequestId")


class ResetAccountPasswordRequest(AbstractModel):
    """ResetAccountPassword请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：dcdbt-ow728lmc。
        :type InstanceId: str
        :param UserName: 登录用户名。
        :type UserName: str
        :param Host: 用户允许的访问 host，用户名+host唯一确定一个账号。
        :type Host: str
        :param Password: 新密码，由字母、数字或常见符号组成，不能包含分号、单引号和双引号，长度为6~32位。
        :type Password: str
        """
        self.InstanceId = None
        self.UserName = None
        self.Host = None
        self.Password = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.UserName = params.get("UserName")
        self.Host = params.get("Host")
        self.Password = params.get("Password")


class ResetAccountPasswordResponse(AbstractModel):
    """ResetAccountPassword返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class Rsip(AbstractModel):
    """拉取实例后端RS信息，返回IP和PORT结构体数组"""

    def __init__(self):
        """
        :param Ip: Ip地址
        :type Ip: str
        :param Port: 端口
        :type Port: int
        """
        self.Ip = None
        self.Port = None

    def _deserialize(self, params):
        self.Ip = params.get("Ip")
        self.Port = params.get("Port")


class RuleItem(AbstractModel):
    """审计规则条目"""

    def __init__(self):
        """
        :param RuleType: 规格类型
        :type RuleType: int
        :param OperationType: 操作类型
        :type OperationType: int
        :param OperationValue: 操作值
        :type OperationValue: str
        """
        self.RuleType = None
        self.OperationType = None
        self.OperationValue = None

    def _deserialize(self, params):
        self.RuleType = params.get("RuleType")
        self.OperationType = params.get("OperationType")
        self.OperationValue = params.get("OperationValue")


class SecurityGroup(AbstractModel):
    """安全组规则"""

    def __init__(self):
        """
        :param CreateTime: 创建时间，时间格式：yyyy-mm-dd hh:mm:ss。
        :type CreateTime: str
        :param ProjectId: 项目ID。
        :type ProjectId: int
        :param SecurityGroupId: 安全组ID。
        :type SecurityGroupId: str
        :param SecurityGroupName: 安全组名称。
        :type SecurityGroupName: str
        :param SecurityGroupRemark: 安全组备注。
        :type SecurityGroupRemark: str
        :param Outbound: 出站规则。
        :type Outbound: list of Outbound
        :param Inbound: 入站规则。
        :type Inbound: list of Inbound
        """
        self.CreateTime = None
        self.ProjectId = None
        self.SecurityGroupId = None
        self.SecurityGroupName = None
        self.SecurityGroupRemark = None
        self.Outbound = None
        self.Inbound = None

    def _deserialize(self, params):
        self.CreateTime = params.get("CreateTime")
        self.ProjectId = params.get("ProjectId")
        self.SecurityGroupId = params.get("SecurityGroupId")
        self.SecurityGroupName = params.get("SecurityGroupName")
        self.SecurityGroupRemark = params.get("SecurityGroupRemark")
        if params.get("Outbound") is not None:
            self.Outbound = []
            for item in params.get("Outbound"):
                obj = Outbound()
                obj._deserialize(item)
                self.Outbound.append(obj)
        if params.get("Inbound") is not None:
            self.Inbound = []
            for item in params.get("Inbound"):
                obj = Inbound()
                obj._deserialize(item)
                self.Inbound.append(obj)


class ShardBriefInfo(AbstractModel):
    """DCDB分片信息"""

    def __init__(self):
        """
        :param ShardSerialId: 分片SerialId
        :type ShardSerialId: str
        :param ShardInstanceId: 分片ID，形如shard-7vg1o339
        :type ShardInstanceId: str
        :param Status: 分片运行状态
        :type Status: int
        :param StatusDesc: 分片运行状态描述
        :type StatusDesc: str
        :param CreateTime: 分片创建时间
        :type CreateTime: str
        :param Memory: 分片内存大小，单位GB
        :type Memory: int
        :param Storage: 分片磁盘大小，单位GB
        :type Storage: int
        :param LogDisk: 分片日志磁盘空间大小，单位GB
        :type LogDisk: int
        :param NodeCount: 分片节点个数
        :type NodeCount: int
        :param StorageUsage: 分片磁盘空间使用率
        :type StorageUsage: float
        :param ProxyVersion: 分片Proxy版本信息
        :type ProxyVersion: str
        :param ShardMasterZone: 分片主DB可用区
        :type ShardMasterZone: str
        :param ShardSlaveZones: 分片从DB可用区
        :type ShardSlaveZones: list of str
        """
        self.ShardSerialId = None
        self.ShardInstanceId = None
        self.Status = None
        self.StatusDesc = None
        self.CreateTime = None
        self.Memory = None
        self.Storage = None
        self.LogDisk = None
        self.NodeCount = None
        self.StorageUsage = None
        self.ProxyVersion = None
        self.ShardMasterZone = None
        self.ShardSlaveZones = None

    def _deserialize(self, params):
        self.ShardSerialId = params.get("ShardSerialId")
        self.ShardInstanceId = params.get("ShardInstanceId")
        self.Status = params.get("Status")
        self.StatusDesc = params.get("StatusDesc")
        self.CreateTime = params.get("CreateTime")
        self.Memory = params.get("Memory")
        self.Storage = params.get("Storage")
        self.LogDisk = params.get("LogDisk")
        self.NodeCount = params.get("NodeCount")
        self.StorageUsage = params.get("StorageUsage")
        self.ProxyVersion = params.get("ProxyVersion")
        self.ShardMasterZone = params.get("ShardMasterZone")
        self.ShardSlaveZones = params.get("ShardSlaveZones")


class ShardInfo(AbstractModel):
    """分片信息"""

    def __init__(self):
        """
        :param ShardInstanceId: 分片ID
        :type ShardInstanceId: str
        :param ShardSerialId: 分片Set ID
        :type ShardSerialId: str
        :param Status: 状态：0 创建中，1 流程处理中， 2 运行中，3 分片未初始化，-2 分片已删除
        :type Status: int
        :param Createtime: 创建时间
        :type Createtime: str
        :param Memory: 内存大小，单位 GB
        :type Memory: int
        :param Storage: 存储大小，单位 GB
        :type Storage: int
        :param ShardId: 分片数字ID
        :type ShardId: int
        :param NodeCount: 节点数，2 为一主一从， 3 为一主二从
        :type NodeCount: int
        :param Pid: 产品类型 Id（过时字段，请勿依赖该值）
        :type Pid: int
        """
        self.ShardInstanceId = None
        self.ShardSerialId = None
        self.Status = None
        self.Createtime = None
        self.Memory = None
        self.Storage = None
        self.ShardId = None
        self.NodeCount = None
        self.Pid = None

    def _deserialize(self, params):
        self.ShardInstanceId = params.get("ShardInstanceId")
        self.ShardSerialId = params.get("ShardSerialId")
        self.Status = params.get("Status")
        self.Createtime = params.get("Createtime")
        self.Memory = params.get("Memory")
        self.Storage = params.get("Storage")
        self.ShardId = params.get("ShardId")
        self.NodeCount = params.get("NodeCount")
        self.Pid = params.get("Pid")


class ShardZoneChooseInfo(AbstractModel):
    """分片节点可用区选择"""

    def __init__(self):
        """
        :param MasterZone: 主可用区
        :type MasterZone: :class:`tcecloud.dcdb.v20180411.models.ZonesInfo`
        :param SlaveZones: 可选的从可用区
        :type SlaveZones: list of ZonesInfo
        """
        self.MasterZone = None
        self.SlaveZones = None

    def _deserialize(self, params):
        if params.get("MasterZone") is not None:
            self.MasterZone = ZonesInfo()
            self.MasterZone._deserialize(params.get("MasterZone"))
        if params.get("SlaveZones") is not None:
            self.SlaveZones = []
            for item in params.get("SlaveZones"):
                obj = ZonesInfo()
                obj._deserialize(item)
                self.SlaveZones.append(obj)


class SlowLogData(AbstractModel):
    """慢查询条目信息"""

    def __init__(self):
        """
        :param CheckSum: 语句校验和，用于查询详情
        :type CheckSum: str
        :param Db: 数据库名称
        :type Db: str
        :param FingerPrint: 抽象的SQL语句
        :type FingerPrint: str
        :param LockTimeAvg: 平均的锁时间
        :type LockTimeAvg: str
        :param LockTimeMax: 最大锁时间
        :type LockTimeMax: str
        :param LockTimeMin: 最小锁时间
        :type LockTimeMin: str
        :param LockTimeSum: 锁时间总和
        :type LockTimeSum: str
        :param QueryCount: 查询次数
        :type QueryCount: str
        :param QueryTimeAvg: 平均查询时间
        :type QueryTimeAvg: str
        :param QueryTimeMax: 最大查询时间
        :type QueryTimeMax: str
        :param QueryTimeMin: 最小查询时间
        :type QueryTimeMin: str
        :param QueryTimeSum: 查询时间总和
        :type QueryTimeSum: str
        :param RowsExaminedSum: 扫描行数
        :type RowsExaminedSum: str
        :param RowsSentSum: 发送行数
        :type RowsSentSum: str
        :param TsMax: 最后执行时间
        :type TsMax: str
        :param TsMin: 首次执行时间
        :type TsMin: str
        :param User: 帐号
        :type User: str
        """
        self.CheckSum = None
        self.Db = None
        self.FingerPrint = None
        self.LockTimeAvg = None
        self.LockTimeMax = None
        self.LockTimeMin = None
        self.LockTimeSum = None
        self.QueryCount = None
        self.QueryTimeAvg = None
        self.QueryTimeMax = None
        self.QueryTimeMin = None
        self.QueryTimeSum = None
        self.RowsExaminedSum = None
        self.RowsSentSum = None
        self.TsMax = None
        self.TsMin = None
        self.User = None

    def _deserialize(self, params):
        self.CheckSum = params.get("CheckSum")
        self.Db = params.get("Db")
        self.FingerPrint = params.get("FingerPrint")
        self.LockTimeAvg = params.get("LockTimeAvg")
        self.LockTimeMax = params.get("LockTimeMax")
        self.LockTimeMin = params.get("LockTimeMin")
        self.LockTimeSum = params.get("LockTimeSum")
        self.QueryCount = params.get("QueryCount")
        self.QueryTimeAvg = params.get("QueryTimeAvg")
        self.QueryTimeMax = params.get("QueryTimeMax")
        self.QueryTimeMin = params.get("QueryTimeMin")
        self.QueryTimeSum = params.get("QueryTimeSum")
        self.RowsExaminedSum = params.get("RowsExaminedSum")
        self.RowsSentSum = params.get("RowsSentSum")
        self.TsMax = params.get("TsMax")
        self.TsMin = params.get("TsMin")
        self.User = params.get("User")


class SpecConfig(AbstractModel):
    """按机型分类的规格配置"""

    def __init__(self):
        """
        :param Machine: 规格机型
        :type Machine: str
        :param SpecConfigInfos: 规格列表
        :type SpecConfigInfos: list of SpecConfigInfo
        """
        self.Machine = None
        self.SpecConfigInfos = None

    def _deserialize(self, params):
        self.Machine = params.get("Machine")
        if params.get("SpecConfigInfos") is not None:
            self.SpecConfigInfos = []
            for item in params.get("SpecConfigInfos"):
                obj = SpecConfigInfo()
                obj._deserialize(item)
                self.SpecConfigInfos.append(obj)


class SpecConfigInfo(AbstractModel):
    """实例可售卖规格详细信息，创建实例和扩容实例时 NodeCount、Memory 确定售卖规格，硬盘大小可用区间为[MinStorage,MaxStorage]"""

    def __init__(self):
        """
        :param NodeCount: 节点个数，2 表示一主一从，3 表示一主二从
        :type NodeCount: int
        :param Memory: 内存大小，单位 GB
        :type Memory: int
        :param MinStorage: 数据盘规格最小值，单位 GB
        :type MinStorage: int
        :param MaxStorage: 数据盘规格最大值，单位 GB
        :type MaxStorage: int
        :param SuitInfo: 推荐的使用场景
        :type SuitInfo: str
        :param Pid: 产品类型 Id
        :type Pid: int
        :param Qps: 最大 Qps 值
        :type Qps: int
        """
        self.NodeCount = None
        self.Memory = None
        self.MinStorage = None
        self.MaxStorage = None
        self.SuitInfo = None
        self.Pid = None
        self.Qps = None
        self.Cpu = None

    def _deserialize(self, params):
        self.NodeCount = params.get("NodeCount")
        self.Memory = params.get("Memory")
        self.MinStorage = params.get("MinStorage")
        self.MaxStorage = params.get("MaxStorage")
        self.SuitInfo = params.get("SuitInfo")
        self.Pid = params.get("Pid")
        self.Qps = params.get("Qps")
        self.Cpu = params.get("Cpu")


class SplitShardConfig(AbstractModel):
    """升级实例 -- 切分分片类型"""

    def __init__(self):
        """
        :param ShardInstanceIds: 分片ID数组
        :type ShardInstanceIds: list of str
        :param SplitRate: 数据切分比例
        :type SplitRate: int
        :param ShardMemory: 分片内存大小，单位 GB
        :type ShardMemory: int
        :param ShardStorage: 分片存储大小，单位 GB
        :type ShardStorage: int
        """
        self.ShardInstanceIds = None
        self.SplitRate = None
        self.ShardMemory = None
        self.ShardStorage = None

    def _deserialize(self, params):
        self.ShardInstanceIds = params.get("ShardInstanceIds")
        self.SplitRate = params.get("SplitRate")
        self.ShardMemory = params.get("ShardMemory")
        self.ShardStorage = params.get("ShardStorage")


class SqlLogItem(AbstractModel):
    """描述一条sql日志的详细信息。"""

    def __init__(self):
        """
        :param Offset: 本条日志在消息队列中的偏移量。
        :type Offset: int
        :param User: 执行本条sql的用户。
        :type User: str
        :param Client: 执行本条sql的客户端IP+端口。
        :type Client: str
        :param DbName: 数据库名称。
        :type DbName: str
        :param Sql: 执行的sql语句。
        :type Sql: str
        :param SelectRowNum: 返回的数据行数。
        :type SelectRowNum: int
        :param AffectRowNum: 影响行数。
        :type AffectRowNum: int
        :param Timestamp: Sql执行时间戳。
        :type Timestamp: int
        :param TimeCostMs: Sql耗时，单位为毫秒。
        :type TimeCostMs: int
        :param ResultCode: Sql返回码，0为成功。
        :type ResultCode: int
        """
        self.Offset = None
        self.User = None
        self.Client = None
        self.DbName = None
        self.Sql = None
        self.SelectRowNum = None
        self.AffectRowNum = None
        self.Timestamp = None
        self.TimeCostMs = None
        self.ResultCode = None

    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.User = params.get("User")
        self.Client = params.get("Client")
        self.DbName = params.get("DbName")
        self.Sql = params.get("Sql")
        self.SelectRowNum = params.get("SelectRowNum")
        self.AffectRowNum = params.get("AffectRowNum")
        self.Timestamp = params.get("Timestamp")
        self.TimeCostMs = params.get("TimeCostMs")
        self.ResultCode = params.get("ResultCode")


class StartSmartDBARequest(AbstractModel):
    """StartSmartDBA请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID
        :type InstanceId: str
        :param ShardId: DCDB实例的分片ID
        :type ShardId: str
        """
        self.InstanceId = None
        self.ShardId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.ShardId = params.get("ShardId")


class StartSmartDBAResponse(AbstractModel):
    """StartSmartDBA返回参数结构体"""

    def __init__(self):
        """
        :param FlowId: 异步任务流程ID
        :type FlowId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class SwitchRollbackInstanceRequest(AbstractModel):
    """SwitchRollbackInstance请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 源/旧实例ID
        :type InstanceId: str
        :param DstInstanceId: 目标实例ID
        :type DstInstanceId: str
        """
        self.InstanceId = None
        self.DstInstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.DstInstanceId = params.get("DstInstanceId")


class SwitchRollbackInstanceResponse(AbstractModel):
    """SwitchRollbackInstance返回参数结构体"""

    def __init__(self):
        """
        :param FlowId: 异步任务流程ID。
        :type FlowId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class TableColumn(AbstractModel):
    """数据库列信息"""

    def __init__(self):
        """
        :param Col: 列名称
        :type Col: str
        :param Type: 列类型
        :type Type: str
        """
        self.Col = None
        self.Type = None

    def _deserialize(self, params):
        self.Col = params.get("Col")
        self.Type = params.get("Type")


class TerminateDedicatedDBInstanceRequest(AbstractModel):
    """TerminateDedicatedDBInstance请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 Id，形如：dcdbt-ow728lmc。
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class TerminateDedicatedDBInstanceResponse(AbstractModel):
    """TerminateDedicatedDBInstance返回参数结构体"""

    def __init__(self):
        """
        :param FlowId: 异步流程Id
        :type FlowId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class TmpInstance(AbstractModel):
    """临时实例"""

    def __init__(self):
        """
        :param AppId: 应用ID
        :type AppId: int
        :param CreateTime: 创建时间
        :type CreateTime: str
        :param InstanceRemark: 实例备注
        :type InstanceRemark: str
        :param TempType: 0:非临时实例 ,1:无效临时实例, 2:回档成功的有效临时实例
        :type TempType: int
        :param Status: 实例状态,0:待初始化,1:流程处理中,2:有效状态,-1:已隔离，-2：已下线
        :type Status: int
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc。
        :type InstanceId: str
        :param Vip: 实例虚IP
        :type Vip: str
        :param Vport: 实例虚端口
        :type Vport: int
        :param PeriodEndTime: 有效期结束时间
        :type PeriodEndTime: str
        :param SrcInstanceId: 源实例 ID，形如：tdsql-ow728lmc。
        :type SrcInstanceId: str
        :param StatusDesc: 实例状态描述
        :type StatusDesc: str
        :param Region: 实例所在地域
        :type Region: str
        :param Zone: 实例所在可用区
        :type Zone: str
        """
        self.AppId = None
        self.CreateTime = None
        self.InstanceRemark = None
        self.TempType = None
        self.Status = None
        self.InstanceId = None
        self.Vip = None
        self.Vport = None
        self.PeriodEndTime = None
        self.SrcInstanceId = None
        self.StatusDesc = None
        self.Region = None
        self.Zone = None

    def _deserialize(self, params):
        self.AppId = params.get("AppId")
        self.CreateTime = params.get("CreateTime")
        self.InstanceRemark = params.get("InstanceRemark")
        self.TempType = params.get("TempType")
        self.Status = params.get("Status")
        self.InstanceId = params.get("InstanceId")
        self.Vip = params.get("Vip")
        self.Vport = params.get("Vport")
        self.PeriodEndTime = params.get("PeriodEndTime")
        self.SrcInstanceId = params.get("SrcInstanceId")
        self.StatusDesc = params.get("StatusDesc")
        self.Region = params.get("Region")
        self.Zone = params.get("Zone")


class UpgradeDCDBInstanceRequest(AbstractModel):
    """UpgradeDCDBInstance请求参数结构体"""

    def __init__(self):
        """
                :param InstanceId: 待升级的实例ID。形如：dcdbt-ow728lmc，可以通过 DescribeDCDBInstances 查询实例详情获得。
                :type InstanceId: str
                :param UpgradeType: 升级类型，取值范围:
        <li> ADD: 新增分片 </li>
         <li> EXPAND: 升级实例中的已有分片 </li>
         <li> SPLIT: 将已有分片中的数据切分到新增分片上</li>
                :type UpgradeType: str
                :param AddShardConfig: 新增分片配置，当UpgradeType为ADD时生效。
                :type AddShardConfig: :class:`tcecloud.dcdb.v20180411.models.AddShardConfig`
                :param ExpandShardConfig: 扩容分片配置，当UpgradeType为EXPAND时生效。
                :type ExpandShardConfig: :class:`tcecloud.dcdb.v20180411.models.ExpandShardConfig`
                :param SplitShardConfig: 切分分片配置，当UpgradeType为SPLIT时生效。
                :type SplitShardConfig: :class:`tcecloud.dcdb.v20180411.models.SplitShardConfig`
                :param AutoVoucher: 是否自动使用代金券进行支付，默认不使用。
                :type AutoVoucher: bool
                :param VoucherIds: 代金券ID列表，目前仅支持指定一张代金券。
                :type VoucherIds: list of str
        """
        self.InstanceId = None
        self.UpgradeType = None
        self.AddShardConfig = None
        self.ExpandShardConfig = None
        self.SplitShardConfig = None
        self.AutoVoucher = None
        self.VoucherIds = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.UpgradeType = params.get("UpgradeType")
        if params.get("AddShardConfig") is not None:
            self.AddShardConfig = AddShardConfig()
            self.AddShardConfig._deserialize(params.get("AddShardConfig"))
        if params.get("ExpandShardConfig") is not None:
            self.ExpandShardConfig = ExpandShardConfig()
            self.ExpandShardConfig._deserialize(params.get("ExpandShardConfig"))
        if params.get("SplitShardConfig") is not None:
            self.SplitShardConfig = SplitShardConfig()
            self.SplitShardConfig._deserialize(params.get("SplitShardConfig"))
        self.AutoVoucher = params.get("AutoVoucher")
        self.VoucherIds = params.get("VoucherIds")


class UpgradeDCDBInstanceResponse(AbstractModel):
    """UpgradeDCDBInstance返回参数结构体"""

    def __init__(self):
        """
               :param DealName: 长订单号。可以据此调用 DescribeOrders
        查询订单详细信息，或在支付失败时调用用户账号相关接口进行支付。
               :type DealName: str
               :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
               :type RequestId: str
        """
        self.DealName = None
        self.RequestId = None

    def _deserialize(self, params):
        self.DealName = params.get("DealName")
        self.RequestId = params.get("RequestId")


class UpgradeDedicatedDCDBInstanceRequest(AbstractModel):
    """UpgradeDedicatedDCDBInstance请求参数结构体"""

    def __init__(self):
        """
        :param UpgradeType: 升级类型，取值为ADD，SPLIT和EXPAND。ADD-添加分片；SPLIT-切分某个分片；EXPAND-垂直扩容某个分片
        :type UpgradeType: str
        :param InstanceId: 实例ID，形如 dcdbt-mlfjm74h
        :type InstanceId: str
        :param AddShardConfig: 当UpgradeType取值为ADD时，添加分片的配置参数
        :type AddShardConfig: :class:`tcecloud.dcdb.v20180411.models.AddShardConfig`
        :param ExpandShardConfig: 当UpgradeType取值为EXPAND时，垂直扩容分片的配置参数
        :type ExpandShardConfig: :class:`tcecloud.dcdb.v20180411.models.ExpandShardConfig`
        :param SplitShardConfig: 当UpgradeType取值为SPLIT时，切分分片的配置参数
        :type SplitShardConfig: :class:`tcecloud.dcdb.v20180411.models.SplitShardConfig`
        """
        self.UpgradeType = None
        self.InstanceId = None
        self.AddShardConfig = None
        self.ExpandShardConfig = None
        self.SplitShardConfig = None

    def _deserialize(self, params):
        self.UpgradeType = params.get("UpgradeType")
        self.InstanceId = params.get("InstanceId")
        if params.get("AddShardConfig") is not None:
            self.AddShardConfig = AddShardConfig()
            self.AddShardConfig._deserialize(params.get("AddShardConfig"))
        if params.get("ExpandShardConfig") is not None:
            self.ExpandShardConfig = ExpandShardConfig()
            self.ExpandShardConfig._deserialize(params.get("ExpandShardConfig"))
        if params.get("SplitShardConfig") is not None:
            self.SplitShardConfig = SplitShardConfig()
            self.SplitShardConfig._deserialize(params.get("SplitShardConfig"))


class UpgradeDedicatedDCDBInstanceResponse(AbstractModel):
    """UpgradeDedicatedDCDBInstance返回参数结构体"""

    def __init__(self):
        """
        :param FlowId: 异步任务流程ID
        :type FlowId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class UpgradeHourDCDBInstanceRequest(AbstractModel):
    """UpgradeHourDCDBInstance请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID，形如dcdbt-87zif6ha
        :type InstanceId: str
        :param UpgradeType: 升级类型，取值为ADD，SPLIT或者EXPAND
        :type UpgradeType: str
        :param AddShardConfig: UpgradeType为ADD类型时，需要填写该参数
        :type AddShardConfig: :class:`tcecloud.dcdb.v20180411.models.AddShardConfig`
        :param ExpandShardConfig: UpgradeType为EXPAND类型时，需要填写该参数
        :type ExpandShardConfig: list of ExpandShardConfig
        :param SplitShardConfig: UpgradeType为SPLIT类型时，需要填写该参数
        :type SplitShardConfig: :class:`tcecloud.dcdb.v20180411.models.SplitShardConfig`
        :param SwitchStartTime: 切换开始时间，格式如: "2019-12-12 07:00:00"。开始时间必须在当前时间一个小时以后，3天以内。
        :type SwitchStartTime: str
        :param SwitchEndTime: 切换结束时间,  格式如: "2019-12-12 07:15:00"，结束时间必须大于开始时间。
        :type SwitchEndTime: str
        :param SwitchAutoRetry: 是否自动重试。 0：不自动重试  1：自动重试
        :type SwitchAutoRetry: int
        """
        self.InstanceId = None
        self.UpgradeType = None
        self.AddShardConfig = None
        self.ExpandShardConfig = None
        self.SplitShardConfig = None
        self.SwitchStartTime = None
        self.SwitchEndTime = None
        self.SwitchAutoRetry = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.UpgradeType = params.get("UpgradeType")
        if params.get("AddShardConfig") is not None:
            self.AddShardConfig = AddShardConfig()
            self.AddShardConfig._deserialize(params.get("AddShardConfig"))
        if params.get("ExpandShardConfig") is not None:
            self.ExpandShardConfig = []
            for item in params.get("ExpandShardConfig"):
                obj = ExpandShardConfig()
                obj._deserialize(item)
                self.ExpandShardConfig.append(obj)
        if params.get("SplitShardConfig") is not None:
            self.SplitShardConfig = SplitShardConfig()
            self.SplitShardConfig._deserialize(params.get("SplitShardConfig"))
        self.SwitchStartTime = params.get("SwitchStartTime")
        self.SwitchEndTime = params.get("SwitchEndTime")
        self.SwitchAutoRetry = params.get("SwitchAutoRetry")


class UpgradeHourDCDBInstanceResponse(AbstractModel):
    """UpgradeHourDCDBInstance返回参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID，形如dcdbt-87zif6ha
        :type InstanceId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.RequestId = params.get("RequestId")


class ZonesInfo(AbstractModel):
    """可用区信息"""

    def __init__(self):
        """
        :param Zone: 可用区英文ID
        :type Zone: str
        :param ZoneId: 可用区数字ID
        :type ZoneId: int
        :param ZoneName: 可用区中文名
        :type ZoneName: str
        """
        self.Zone = None
        self.ZoneId = None
        self.ZoneName = None

    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.ZoneId = params.get("ZoneId")
        self.ZoneName = params.get("ZoneName")

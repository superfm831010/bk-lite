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
        :param InstanceId: 实例 Id，形如：tdsql-ow728lmc。
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


class ActiveHourDBInstanceRequest(AbstractModel):
    """ActiveHourDBInstance请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID，形如tdsql-o0q206pq
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class ActiveHourDBInstanceResponse(AbstractModel):
    """ActiveHourDBInstance返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


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
        :param ApiName: 待鉴权的接口名，如 CreateDBInstance
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
        :param InstanceId: 实例Id，形如：tdsql-ow728lmc。
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


class CloseDBExtranetAccessRequest(AbstractModel):
    """CloseDBExtranetAccess请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 待关闭外网访问的实例ID。形如：tdsql-ow728lmc，可以通过 DescribeDBInstances 查询实例详情获得。
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


class ConfTemplate(AbstractModel):
    """参数模板"""

    def __init__(self):
        """
        :param ConfigTemplateId: 参数模板Id
        :type ConfigTemplateId: int
        :param AppId: 应用id
        :type AppId: int
        :param TemplateName: 参数模板名称
        :type TemplateName: str
        :param TemplateDesc: 参数模板描述
        :type TemplateDesc: str
        :param TemplateDefault: 默认模板
        :type TemplateDefault: str
        """
        self.ConfigTemplateId = None
        self.AppId = None
        self.TemplateName = None
        self.TemplateDesc = None
        self.TemplateDefault = None

    def _deserialize(self, params):
        self.ConfigTemplateId = params.get("ConfigTemplateId")
        self.AppId = params.get("AppId")
        self.TemplateName = params.get("TemplateName")
        self.TemplateDesc = params.get("TemplateDesc")
        self.TemplateDefault = params.get("TemplateDefault")


class ConfigParam(AbstractModel):
    """配置模板参数"""

    def __init__(self):
        """
        :param Param: 参数名
        :type Param: str
        :param Value: 参数值
        :type Value: str
        """
        self.Param = None
        self.Value = None

    def _deserialize(self, params):
        self.Param = params.get("Param")
        self.Value = params.get("Value")


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
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc，可以通过 DescribeDBInstances 查询实例详情获得。
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
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc，可以通过 DescribeDBInstances 查询实例详情获得。
        :type InstanceId: str
        :param UserName: 登录用户名，由字幕、数字、下划线和连字符组成，长度为1~32位。
        :type UserName: str
        :param Host: 可以登录的主机，与mysql 账号的 host 格式一致，可以支持通配符，例如 %，10.%，10.20.%。
        :type Host: str
        :param Password: 账号密码，由字母、数字或常见符号组成，不能包含分号、单引号和双引号，长度为6~32位。
        :type Password: str
        :param ReadOnly: 是否创建为只读账号，0：否， 1：该账号的sql请求优先选择备机执行，备机不可用时选择主机执行，2：优先选择备机执行，备机不可用时操作失败。
        :type ReadOnly: int
        :param Description: 账号备注，可以包含中文、英文字符、常见符号和数字，长度为0~256字符
        :type Description: str
        :param DelayThresh: 根据传入时间判断备机不可用
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


class CreateConfigTemplateRequest(AbstractModel):
    """CreateConfigTemplate请求参数结构体"""

    def __init__(self):
        """
        :param Name: 参数模板名称
        :type Name: str
        :param Description: 参数模板描述
        :type Description: str
        :param TemplateDefault: 默认模板，默认值default
        :type TemplateDefault: str
        :param ConfigParams: 配置模板参数
        :type ConfigParams: list of ConfigParam
        """
        self.Name = None
        self.Description = None
        self.TemplateDefault = None
        self.ConfigParams = None

    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Description = params.get("Description")
        self.TemplateDefault = params.get("TemplateDefault")
        if params.get("ConfigParams") is not None:
            self.ConfigParams = []
            for item in params.get("ConfigParams"):
                obj = ConfigParam()
                obj._deserialize(item)
                self.ConfigParams.append(obj)


class CreateConfigTemplateResponse(AbstractModel):
    """CreateConfigTemplate返回参数结构体"""

    def __init__(self):
        """
        :param ConfigTemplateId: 参数模板Id
        :type ConfigTemplateId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ConfigTemplateId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.ConfigTemplateId = params.get("ConfigTemplateId")
        self.RequestId = params.get("RequestId")


class CreateDBInstanceRequest(AbstractModel):
    """CreateDBInstance请求参数结构体"""

    def __init__(self):
        """
               :param Zones: 实例节点可用区分布，最多可填两个可用区。当分片规格为一主两从时，其中两个节点在第一个可用区。
               :type Zones: list of str
               :param NodeCount: 节点个数大小，可以通过 DescribeDBInstanceSpecs
        查询实例规格获得。
               :type NodeCount: int
               :param Memory: 内存大小，单位：GB，可以通过 DescribeDBInstanceSpecs
        查询实例规格获得。
               :type Memory: int
               :param Storage: 存储空间大小，单位：GB，可以通过 DescribeDBInstanceSpecs
        查询实例规格获得不同内存大小对应的磁盘规格下限和上限。
               :type Storage: int
               :param Period: 欲购买的时长，单位：月。
               :type Period: int
               :param Count: 欲购买的数量，默认查询购买1个实例的价格。
               :type Count: int
               :param AutoVoucher: 是否自动使用代金券进行支付，默认不使用。
               :type AutoVoucher: bool
               :param VoucherIds: 代金券ID列表，目前仅支持指定一张代金券。
               :type VoucherIds: list of str
               :param VpcId: 虚拟私有网络 ID，不传表示创建为基础网络
               :type VpcId: str
               :param SubnetId: 虚拟私有网络子网 ID，VpcId 不为空时必填
               :type SubnetId: str
               :param ProjectId: 项目 ID，可以通过查看项目列表获取，不传则关联到默认项目
               :type ProjectId: int
               :param DbVersionId: 数据库引擎版本，当前可选：10.0.10，10.1.9，5.7.17。如果不传的话，默认为 Mariadb 10.1.9。
               :type DbVersionId: str
        """
        self.Zones = None
        self.NodeCount = None
        self.Memory = None
        self.Storage = None
        self.Period = None
        self.Count = None
        self.AutoVoucher = None
        self.VoucherIds = None
        self.VpcId = None
        self.SubnetId = None
        self.ProjectId = None
        self.DbVersionId = None

    def _deserialize(self, params):
        self.Zones = params.get("Zones")
        self.NodeCount = params.get("NodeCount")
        self.Memory = params.get("Memory")
        self.Storage = params.get("Storage")
        self.Period = params.get("Period")
        self.Count = params.get("Count")
        self.AutoVoucher = params.get("AutoVoucher")
        self.VoucherIds = params.get("VoucherIds")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.ProjectId = params.get("ProjectId")
        self.DbVersionId = params.get("DbVersionId")


class CreateDBInstanceResponse(AbstractModel):
    """CreateDBInstance返回参数结构体"""

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


class CreateHourDBInstanceRequest(AbstractModel):
    """CreateHourDBInstance请求参数结构体"""

    def __init__(self):
        """
        :param Zones: 实例可用区信息。只可填一个或者两个可用区。如果只填一个，则主库和从库都在该可用区；如果填两个，则主库在第一个可用区，从库在第二个可用区。
        :type Zones: list of str
        :param NodeCount: 实例节点个数，为2或者3。2表示一主一从；3表示一主两从。
        :type NodeCount: int
        :param VpcId: VPC网络ID，形如vpc-qquscup9。
        :type VpcId: str
        :param SubnetId: VPC子网ID，形如subnet-mfhkoln6。
        :type SubnetId: str
        :param Memory: 购买实例内存大小，单位为GB。
        :type Memory: int
        :param Storage: 购买实例磁盘大小，单位为GB。
        :type Storage: int
        :param Count: 购买实例个数。如果不填，则默认购买一个实例。取值范围为1到10。
        :type Count: int
        :param ProjectId: 项目ID。
        :type ProjectId: int
        :param DbVersionId: 数据库版本，所填值为10.0.10，10.1.9，5.7.17或者5.6.39。不填的话，默认购买5.7.17版本实例。
        :type DbVersionId: str
        :param Cpu: 购买的CPU大小，单位为核
        :type Cpu: int
        :param ExclusterId: 独享集群id
        :type ExclusterId: str
        :param InstanceName: 实例名称
        :type InstanceName: str
        :param SecurityGroupId: 安全组id
        :type SecurityGroupId: str
        """
        self.Zones = None
        self.NodeCount = None
        self.VpcId = None
        self.SubnetId = None
        self.Memory = None
        self.Storage = None
        self.Count = None
        self.ProjectId = None
        self.DbVersionId = None
        self.Cpu = None
        self.ExclusterId = None
        self.InstanceName = None
        self.SecurityGroupId = None

    def _deserialize(self, params):
        self.Zones = params.get("Zones")
        self.NodeCount = params.get("NodeCount")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.Memory = params.get("Memory")
        self.Storage = params.get("Storage")
        self.Count = params.get("Count")
        self.ProjectId = params.get("ProjectId")
        self.DbVersionId = params.get("DbVersionId")
        self.Cpu = params.get("Cpu")
        self.ExclusterId = params.get("ExclusterId")
        self.InstanceName = params.get("InstanceName")
        self.SecurityGroupId = params.get("SecurityGroupId")


class CreateHourDBInstanceResponse(AbstractModel):
    """CreateHourDBInstance返回参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 购买实例的ID。
        :type InstanceIds: list of str
        :param FlowId: 购买实例异步任务流程ID，以FlowId作为参数调用DescribeFlow API接口，查询创建实例任务执行状态。
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


class CreateTmpInstancesRequest(AbstractModel):
    """CreateTmpInstances请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 回档实例的ID列表，形如：tdsql-ow728lmc。
        :type InstanceIds: list of str
        :param RollbackTime: 回档时间点
        :type RollbackTime: str
        """
        self.InstanceIds = None
        self.RollbackTime = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.RollbackTime = params.get("RollbackTime")


class CreateTmpInstancesResponse(AbstractModel):
    """CreateTmpInstances返回参数结构体"""

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
                :param DelayThresh: 该字段对只读帐号有意义，表示选择主备延迟小于该值的备机
        注意：此字段可能返回 null，表示取不到有效值。
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


class DBBackupTimeConfig(AbstractModel):
    """云数据库实例备份时间配置信息"""

    def __init__(self):
        """
        :param InstanceId: 实例 Id
        :type InstanceId: str
        :param StartBackupTime: 每天备份执行的区间的开始时间，格式 mm:ss，形如 22:00
        :type StartBackupTime: str
        :param EndBackupTime: 每天备份执行的区间的结束时间，格式 mm:ss，形如 23:00
        :type EndBackupTime: str
        """
        self.InstanceId = None
        self.StartBackupTime = None
        self.EndBackupTime = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartBackupTime = params.get("StartBackupTime")
        self.EndBackupTime = params.get("EndBackupTime")


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


class DBInstance(AbstractModel):
    """描述云数据库实例的详细信息。"""

    def __init__(self):
        """
                :param InstanceId: 实例 Id，唯一标识一个 TDSQL 实例
                :type InstanceId: str
                :param InstanceName: 实例名称，用户可修改
                :type InstanceName: str
                :param AppId: 实例所属应用 Id
                :type AppId: int
                :param ProjectId: 实例所属项目 Id
                :type ProjectId: int
                :param Region: 实例所在地域名称，如 ap-shanghai
                :type Region: str
                :param Zone: 实例所在可用区名称，如 ap-shanghai-1
                :type Zone: str
                :param VpcId: 私有网络 Id，基础网络时为 0
                :type VpcId: int
                :param SubnetId: 子网 Id，基础网络时为 0
                :type SubnetId: int
                :param Status: 实例状态：0 创建中，1 流程处理中， 2 运行中，3 实例未初始化，-1 实例已隔离，-2 实例已删除
                :type Status: int
                :param Vip: 内网 IP 地址
                :type Vip: str
                :param Vport: 内网端口
                :type Vport: int
                :param WanDomain: 外网访问的域名，公网可解析
                :type WanDomain: str
                :param WanVip: 外网 IP 地址，公网可访问
                :type WanVip: str
                :param WanPort: 外网端口
                :type WanPort: int
                :param CreateTime: 实例创建时间，格式为 2006-01-02 15:04:05
                :type CreateTime: str
                :param UpdateTime: 实例最后更新时间，格式为 2006-01-02 15:04:05
                :type UpdateTime: str
                :param AutoRenewFlag: 自动续费标志：0 否，1 是
                :type AutoRenewFlag: int
                :param PeriodEndTime: 实例到期时间，格式为 2006-01-02 15:04:05
                :type PeriodEndTime: str
                :param Uin: 实例所属账号
                :type Uin: str
                :param TdsqlVersion: TDSQL 版本信息
                :type TdsqlVersion: str
                :param Memory: 实例内存大小，单位 GB
                :type Memory: int
                :param Storage: 实例存储大小，单位 GB
                :type Storage: int
                :param UniqueVpcId: 字符串型的私有网络Id
                :type UniqueVpcId: str
                :param UniqueSubnetId: 字符串型的私有网络子网Id
                :type UniqueSubnetId: str
                :param OriginSerialId: 原始实例ID（过时字段，请勿依赖该值）
                :type OriginSerialId: str
                :param NodeCount: 节点数，2为一主一从，3为一主二从
                :type NodeCount: int
                :param IsTmp: 是否临时实例，0为否，非0为是
                :type IsTmp: int
                :param ExclusterId: 独享集群Id，为空表示为普通实例
                :type ExclusterId: str
                :param Id: 数字实例Id（过时字段，请勿依赖该值）
                :type Id: int
                :param Pid: 产品类型 Id
                :type Pid: int
                :param Qps: 最大 Qps 值
                :type Qps: int
                :param Paymode: 付费模式
        注意：此字段可能返回 null，表示取不到有效值。
                :type Paymode: str
                :param Locker: 实例处于异步任务时的异步任务流程ID
        注意：此字段可能返回 null，表示取不到有效值。
                :type Locker: int
                :param StatusDesc: 实例目前运行状态描述
        注意：此字段可能返回 null，表示取不到有效值。
                :type StatusDesc: str
                :param WanStatus: 外网状态，0-未开通；1-已开通；2-关闭；3-开通中
                :type WanStatus: int
                :param IsAuditSupported: 该实例是否支持审计。1-支持；0-不支持
                :type IsAuditSupported: int
                :param Machine: 机器型号
                :type Machine: str
                :param IsEncryptSupported: 是否支持数据加密。1-支持；0-不支持
                :type IsEncryptSupported: int
        """
        self.InstanceId = None
        self.InstanceName = None
        self.AppId = None
        self.ProjectId = None
        self.Region = None
        self.Zone = None
        self.VpcId = None
        self.SubnetId = None
        self.Status = None
        self.Vip = None
        self.Vport = None
        self.WanDomain = None
        self.WanVip = None
        self.WanPort = None
        self.CreateTime = None
        self.UpdateTime = None
        self.AutoRenewFlag = None
        self.PeriodEndTime = None
        self.Uin = None
        self.TdsqlVersion = None
        self.Memory = None
        self.Storage = None
        self.UniqueVpcId = None
        self.UniqueSubnetId = None
        self.OriginSerialId = None
        self.NodeCount = None
        self.IsTmp = None
        self.ExclusterId = None
        self.Id = None
        self.Pid = None
        self.Qps = None
        self.Paymode = None
        self.Locker = None
        self.StatusDesc = None
        self.WanStatus = None
        self.IsAuditSupported = None
        self.Machine = None
        self.IsEncryptSupported = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.AppId = params.get("AppId")
        self.ProjectId = params.get("ProjectId")
        self.Region = params.get("Region")
        self.Zone = params.get("Zone")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.Status = params.get("Status")
        self.Vip = params.get("Vip")
        self.Vport = params.get("Vport")
        self.WanDomain = params.get("WanDomain")
        self.WanVip = params.get("WanVip")
        self.WanPort = params.get("WanPort")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.AutoRenewFlag = params.get("AutoRenewFlag")
        self.PeriodEndTime = params.get("PeriodEndTime")
        self.Uin = params.get("Uin")
        self.TdsqlVersion = params.get("TdsqlVersion")
        self.Memory = params.get("Memory")
        self.Storage = params.get("Storage")
        self.UniqueVpcId = params.get("UniqueVpcId")
        self.UniqueSubnetId = params.get("UniqueSubnetId")
        self.OriginSerialId = params.get("OriginSerialId")
        self.NodeCount = params.get("NodeCount")
        self.IsTmp = params.get("IsTmp")
        self.ExclusterId = params.get("ExclusterId")
        self.Id = params.get("Id")
        self.Pid = params.get("Pid")
        self.Qps = params.get("Qps")
        self.Paymode = params.get("Paymode")
        self.Locker = params.get("Locker")
        self.StatusDesc = params.get("StatusDesc")
        self.WanStatus = params.get("WanStatus")
        self.IsAuditSupported = params.get("IsAuditSupported")
        self.Machine = params.get("Machine")
        self.IsEncryptSupported = params.get("IsEncryptSupported")


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
        :param InstanceId: 实例ID，形如：tdsql-ow728lmc，可以通过 DescribeDBInstances 查询实例详情获得。
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


class DeleteConfigTemplateRequest(AbstractModel):
    """DeleteConfigTemplate请求参数结构体"""

    def __init__(self):
        """
        :param ConfigTemplateId: 参数模板Id，可以通过 DescribeConfigTemplates 查询参数模板列表获得。
        :type ConfigTemplateId: int
        """
        self.ConfigTemplateId = None

    def _deserialize(self, params):
        self.ConfigTemplateId = params.get("ConfigTemplateId")


class DeleteConfigTemplateResponse(AbstractModel):
    """DeleteConfigTemplate返回参数结构体"""

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
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc。
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
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc，可以通过 DescribeDBInstances 查询实例详情获得。
        :type InstanceId: str
        :param UserName: 登录用户名。
        :type UserName: str
        :param Host: 用户允许的访问 host，用户名+host唯一确定一个账号。
        :type Host: str
        :param DbName: 数据库名。如果为 \*，表示查询全局权限（即 \*.\*），此时忽略 Type 和 Object 参数
        :type DbName: str
        :param Type: 类型,可以填入 table 、 view 、 proc 、 func 和 \*。当 DbName 为具体数据库名，Type为 \* 时，表示查询该数据库权限（即db.\*），此时忽略 Object 参数
        :type Type: str
        :param Object: 具体的 Type 的名称，比如 Type 为 table 时就是具体的表名。DbName 和 Type 都为具体名称，则 Object 表示具体对象名，不能为 \* 或者为空
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
        :param InstanceId: 实例ID，形如：tdsql-ow728lmc，可以通过 DescribeDBInstances 查询实例详情获得。
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
        :param InstanceIds: 实例uuid列表
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
        :type AuditRuleDetail: :class:`tcecloud.mariadb.v20170312.models.AuditRuleDetail`
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
        :param StrategySet: 审计策略列表
        :type StrategySet: list of AuditStrategy
        :param SessionId: 会话Id
        :type SessionId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.StrategySet = None
        self.SessionId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("StrategySet") is not None:
            self.StrategySet = []
            for item in params.get("StrategySet"):
                obj = AuditStrategy()
                obj._deserialize(item)
                self.StrategySet.append(obj)
        self.SessionId = params.get("SessionId")
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


class DescribeBackupTimeRequest(AbstractModel):
    """DescribeBackupTime请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 实例ID，形如：tdsql-ow728lmc，可以通过 DescribeDBInstances 查询实例详情获得。
        :type InstanceIds: list of str
        """
        self.InstanceIds = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")


class DescribeBackupTimeResponse(AbstractModel):
    """DescribeBackupTime返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 返回的配置数量
        :type TotalCount: int
        :param Items: 实例备份时间配置信息
        :type Items: list of DBBackupTimeConfig
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
                obj = DBBackupTimeConfig()
                obj._deserialize(item)
                self.Items.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeBatchRenewalPriceRequest(AbstractModel):
    """DescribeBatchRenewalPrice请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 待续费的实例ID数组。形如：["tdsql-ow728lmc"]，可以通过 DescribeDBInstances 查询实例详情获得。
        :type InstanceIds: list of str
        :param Period: 续费时长，单位：月。
        :type Period: int
        """
        self.InstanceIds = None
        self.Period = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.Period = params.get("Period")


class DescribeBatchRenewalPriceResponse(AbstractModel):
    """DescribeBatchRenewalPrice返回参数结构体"""

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


class DescribeBinlogTimeRequest(AbstractModel):
    """DescribeBinlogTime请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc。
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class DescribeBinlogTimeResponse(AbstractModel):
    """DescribeBinlogTime返回参数结构体"""

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


class DescribeConfigHistoriesRequest(AbstractModel):
    """DescribeConfigHistories请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc。
        :type InstanceId: str
        :param Limit: 限制数目
        :type Limit: int
        :param Offset: 偏移量
        :type Offset: int
        """
        self.InstanceId = None
        self.Limit = None
        self.Offset = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")


class DescribeConfigHistoriesResponse(AbstractModel):
    """DescribeConfigHistories返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 总数目
        :type TotalCount: int
        :param InstanceConfigSet: 实例配置列表
        :type InstanceConfigSet: list of InstanceConfig
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.InstanceConfigSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("InstanceConfigSet") is not None:
            self.InstanceConfigSet = []
            for item in params.get("InstanceConfigSet"):
                obj = InstanceConfig()
                obj._deserialize(item)
                self.InstanceConfigSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeConfigTemplateRequest(AbstractModel):
    """DescribeConfigTemplate请求参数结构体"""

    def __init__(self):
        """
        :param ConfigTemplateId: 参数模板Id，可以通过 DescribeConfigTemplates 查询参数模板列表获得。
        :type ConfigTemplateId: int
        """
        self.ConfigTemplateId = None

    def _deserialize(self, params):
        self.ConfigTemplateId = params.get("ConfigTemplateId")


class DescribeConfigTemplateResponse(AbstractModel):
    """DescribeConfigTemplate返回参数结构体"""

    def __init__(self):
        """
        :param ConfigTemplateId: 参数模板Id
        :type ConfigTemplateId: int
        :param AppId: 应用Id
        :type AppId: int
        :param TemplateName: 参数模板名称
        :type TemplateName: str
        :param TemplateDesc: 参数模板描述
        :type TemplateDesc: str
        :param TemplateDefault: 默认模板
        :type TemplateDefault: str
        :param TemplateParamSet: 模板参数列表
        :type TemplateParamSet: list of TemplateParam
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ConfigTemplateId = None
        self.AppId = None
        self.TemplateName = None
        self.TemplateDesc = None
        self.TemplateDefault = None
        self.TemplateParamSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.ConfigTemplateId = params.get("ConfigTemplateId")
        self.AppId = params.get("AppId")
        self.TemplateName = params.get("TemplateName")
        self.TemplateDesc = params.get("TemplateDesc")
        self.TemplateDefault = params.get("TemplateDefault")
        if params.get("TemplateParamSet") is not None:
            self.TemplateParamSet = []
            for item in params.get("TemplateParamSet"):
                obj = TemplateParam()
                obj._deserialize(item)
                self.TemplateParamSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeConfigTemplatesRequest(AbstractModel):
    """DescribeConfigTemplates请求参数结构体"""

    def __init__(self):
        """
        :param SearchKey: 模板名称模糊搜索
        :type SearchKey: str
        :param WithDefaultTemplate: 是否返回默认模板，1:返回,0:不返回
        :type WithDefaultTemplate: int
        :param Limit: 分页，页大小，默认150
        :type Limit: int
        :param Offset: 分页，页偏移量，默认0
        :type Offset: int
        """
        self.SearchKey = None
        self.WithDefaultTemplate = None
        self.Limit = None
        self.Offset = None

    def _deserialize(self, params):
        self.SearchKey = params.get("SearchKey")
        self.WithDefaultTemplate = params.get("WithDefaultTemplate")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")


class DescribeConfigTemplatesResponse(AbstractModel):
    """DescribeConfigTemplates返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 总记录数
        :type TotalCount: int
        :param TemplateSet: 参数模板列表
        :type TemplateSet: list of ConfTemplate
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.TemplateSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("TemplateSet") is not None:
            self.TemplateSet = []
            for item in params.get("TemplateSet"):
                obj = ConfTemplate()
                obj._deserialize(item)
                self.TemplateSet.append(obj)
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
        """
        self.InstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.MetricNames = None
        self.Period = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.MetricNames = params.get("MetricNames")
        self.Period = params.get("Period")


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


class DescribeDBEncryptAttributesRequest(AbstractModel):
    """DescribeDBEncryptAttributes请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例Id，形如：tdsql-ow728lmc。
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class DescribeDBEncryptAttributesResponse(AbstractModel):
    """DescribeDBEncryptAttributes返回参数结构体"""

    def __init__(self):
        """
        :param EncryptStatus: 是否启用加密，1-已开启；0-未开启。
        :type EncryptStatus: int
        :param CipherText: DEK密钥
        :type CipherText: str
        :param ExpireDate: DEK密钥过期日期。
        :type ExpireDate: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.EncryptStatus = None
        self.CipherText = None
        self.ExpireDate = None
        self.RequestId = None

    def _deserialize(self, params):
        self.EncryptStatus = params.get("EncryptStatus")
        self.CipherText = params.get("CipherText")
        self.ExpireDate = params.get("ExpireDate")
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


class DescribeDBInstanceDetailRequest(AbstractModel):
    """DescribeDBInstanceDetail请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例Id形如：tdsql-ow728lmc。
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class DescribeDBInstanceDetailResponse(AbstractModel):
    """DescribeDBInstanceDetail返回参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例Id
        :type InstanceId: str
        :param InstanceName: 实例名称
        :type InstanceName: str
        :param Status: 实例状态
        :type Status: int
        :param StatusDesc: 实例目前运行状态描述
        :type StatusDesc: str
        :param Vip: 内网 IP 地址
        :type Vip: str
        :param Vport: 内网端口
        :type Vport: int
        :param IsTmp: 是否临时实例，0为否，非0为是
        :type IsTmp: int
        :param NodeCount: 节点数，2为一主一从，3为一主二从
        :type NodeCount: int
        :param Region: 实例所在地域名称，如 ap-shanghai
        :type Region: str
        :param Zone: 实例所在可用区名称，如 ap-shanghai-1
        :type Zone: str
        :param VpcId: 字符串型的私有网络Id
        :type VpcId: str
        :param SubnetId: 字符串型的私有网络子网Id
        :type SubnetId: str
        :param WanStatus: 外网状态，0-未开通；1-已开通；2-关闭；3-开通中
        :type WanStatus: int
        :param WanDomain: 外网访问的域名，公网可解析
        :type WanDomain: str
        :param WanVip: 外网 IP 地址，公网可访问
        :type WanVip: str
        :param WanPort: 外网端口
        :type WanPort: int
        :param ProjectId: 实例所属项目 Id
        :type ProjectId: int
        :param TdsqlVersion: TDSQL 版本信息
        :type TdsqlVersion: str
        :param Memory: 实例内存大小，单位 GB
        :type Memory: int
        :param Storage: 实例存储大小，单位 GB
        :type Storage: int
        :param MasterZone: 主可用区，如 ap-shanghai-1
        :type MasterZone: str
        :param SlaveZones: 从可用区列表，如 [ap-shanghai-2]
        :type SlaveZones: list of str
        :param AutoRenewFlag: 自动续费标志：0 否，1 是
        :type AutoRenewFlag: int
        :param ExclusterId: 独享集群Id，普通实例为空
        :type ExclusterId: str
        :param PayMode: 付费模式：prepaid 表示预付费
        :type PayMode: str
        :param CreateTime: 实例创建时间，格式为 2006-01-02 15:04:05
        :type CreateTime: str
        :param IsAuditSupported: 实例是否支持审计
        :type IsAuditSupported: bool
        :param PeriodEndTime: 实例到期时间，格式为 2006-01-02 15:04:05
        :type PeriodEndTime: str
        :param Machine: 机型信息
        :type Machine: str
        :param StorageUsage: 存储空间使用率
        :type StorageUsage: str
        :param LogStorage: 日志存储空间大小，单位 GB
        :type LogStorage: int
        :param IsEncryptSupported: 是否支持数据加密。1-支持；0-不支持
        :type IsEncryptSupported: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceId = None
        self.InstanceName = None
        self.Status = None
        self.StatusDesc = None
        self.Vip = None
        self.Vport = None
        self.IsTmp = None
        self.NodeCount = None
        self.Region = None
        self.Zone = None
        self.VpcId = None
        self.SubnetId = None
        self.WanStatus = None
        self.WanDomain = None
        self.WanVip = None
        self.WanPort = None
        self.ProjectId = None
        self.TdsqlVersion = None
        self.Memory = None
        self.Storage = None
        self.MasterZone = None
        self.SlaveZones = None
        self.AutoRenewFlag = None
        self.ExclusterId = None
        self.PayMode = None
        self.CreateTime = None
        self.IsAuditSupported = None
        self.PeriodEndTime = None
        self.Machine = None
        self.StorageUsage = None
        self.LogStorage = None
        self.IsEncryptSupported = None
        self.RequestId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.Status = params.get("Status")
        self.StatusDesc = params.get("StatusDesc")
        self.Vip = params.get("Vip")
        self.Vport = params.get("Vport")
        self.IsTmp = params.get("IsTmp")
        self.NodeCount = params.get("NodeCount")
        self.Region = params.get("Region")
        self.Zone = params.get("Zone")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.WanStatus = params.get("WanStatus")
        self.WanDomain = params.get("WanDomain")
        self.WanVip = params.get("WanVip")
        self.WanPort = params.get("WanPort")
        self.ProjectId = params.get("ProjectId")
        self.TdsqlVersion = params.get("TdsqlVersion")
        self.Memory = params.get("Memory")
        self.Storage = params.get("Storage")
        self.MasterZone = params.get("MasterZone")
        self.SlaveZones = params.get("SlaveZones")
        self.AutoRenewFlag = params.get("AutoRenewFlag")
        self.ExclusterId = params.get("ExclusterId")
        self.PayMode = params.get("PayMode")
        self.CreateTime = params.get("CreateTime")
        self.IsAuditSupported = params.get("IsAuditSupported")
        self.PeriodEndTime = params.get("PeriodEndTime")
        self.Machine = params.get("Machine")
        self.StorageUsage = params.get("StorageUsage")
        self.LogStorage = params.get("LogStorage")
        self.IsEncryptSupported = params.get("IsEncryptSupported")
        self.RequestId = params.get("RequestId")


class DescribeDBInstanceHAInfoRequest(AbstractModel):
    """DescribeDBInstanceHAInfo请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例Id，形如：tdsql-ow728lmc
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class DescribeDBInstanceHAInfoResponse(AbstractModel):
    """DescribeDBInstanceHAInfo返回参数结构体"""

    def __init__(self):
        """
        :param MasterZone: 当前主所在可用区
        :type MasterZone: str
        :param SwitchStatus: 当前切换状态，0-未切换，1-切换中
        :type SwitchStatus: int
        :param SwitchAllowed: 当前是否允许切换
        :type SwitchAllowed: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.MasterZone = None
        self.SwitchStatus = None
        self.SwitchAllowed = None
        self.RequestId = None

    def _deserialize(self, params):
        self.MasterZone = params.get("MasterZone")
        self.SwitchStatus = params.get("SwitchStatus")
        self.SwitchAllowed = params.get("SwitchAllowed")
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


class DescribeDBInstanceSpecsRequest(AbstractModel):
    """DescribeDBInstanceSpecs请求参数结构体"""


class DescribeDBInstanceSpecsResponse(AbstractModel):
    """DescribeDBInstanceSpecs返回参数结构体"""

    def __init__(self):
        """
        :param Specs: 按机型分类的可售卖规格列表
        :type Specs: list of InstanceSpec
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Specs = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Specs") is not None:
            self.Specs = []
            for item in params.get("Specs"):
                obj = InstanceSpec()
                obj._deserialize(item)
                self.Specs.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDBInstancesRequest(AbstractModel):
    """DescribeDBInstances请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 按照一个或者多个实例 ID 查询。实例 ID 形如：tdsql-ow728lmc。每次请求的实例的上限为100。
        :type InstanceIds: list of str
        :param SearchName: 搜索的字段名，当前支持的值有：instancename、vip、all。传 instancename 表示按实例名进行搜索；传 vip 表示按内网IP进行搜索；传 all 将会按实例ID、实例名和内网IP进行搜索。
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
        :param Limit: 返回数量，默认为 20，最大值为 100。
        :type Limit: int
        :param OriginSerialIds: 按 OriginSerialId 查询
        :type OriginSerialIds: list of str
        :param IsFilterExcluster: 标识是否使用ExclusterType字段, false不使用，true使用
        :type IsFilterExcluster: bool
        :param ExclusterType: 实例所属独享集群类型。取值范围：1-非独享集群，2-独享集群， 0-全部
        :type ExclusterType: int
        :param ExclusterIds: 按独享集群Id过滤实例，独享集群Id形如dbdc-4ih6uct9
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
        self.OriginSerialIds = None
        self.IsFilterExcluster = None
        self.ExclusterType = None
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
        self.OriginSerialIds = params.get("OriginSerialIds")
        self.IsFilterExcluster = params.get("IsFilterExcluster")
        self.ExclusterType = params.get("ExclusterType")
        self.ExclusterIds = params.get("ExclusterIds")


class DescribeDBInstancesResponse(AbstractModel):
    """DescribeDBInstances返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的实例数量
        :type TotalCount: int
        :param Instances: 实例详细信息列表
        :type Instances: list of DBInstance
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
                obj = DBInstance()
                obj._deserialize(item)
                self.Instances.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDBLogFilesRequest(AbstractModel):
    """DescribeDBLogFiles请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc。
        :type InstanceId: str
        :param Type: 请求日志类型，取值只能为1、2、3或者4。1-binlog，2-冷备，3-errlog，4-slowlog。
        :type Type: int
        """
        self.InstanceId = None
        self.Type = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Type = params.get("Type")


class DescribeDBLogFilesResponse(AbstractModel):
    """DescribeDBLogFiles返回参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc。
        :type InstanceId: str
        :param Type: 请求日志类型，取值只能为1、2、3或者4。1-binlog，2-冷备，3-errlog，4-slowlog。
        :type Type: int
        :param Total: 请求日志总数
        :type Total: int
        :param Files: 包含uri、length、mtime（修改时间）等信息
        :type Files: list of LogFileInfo
        :param VpcPrefix: 如果是VPC网络的实例，做用本前缀加上URI为下载地址
        :type VpcPrefix: str
        :param NormalPrefix: 如果是普通网络的实例，做用本前缀加上URI为下载地址
        :type NormalPrefix: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceId = None
        self.Type = None
        self.Total = None
        self.Files = None
        self.VpcPrefix = None
        self.NormalPrefix = None
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
        self.RequestId = params.get("RequestId")


class DescribeDBMetricsRequest(AbstractModel):
    """DescribeDBMetrics请求参数结构体"""

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
        """
        self.InstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.MetricNames = None
        self.Period = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.MetricNames = params.get("MetricNames")
        self.Period = params.get("Period")


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
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc。
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class DescribeDBParametersResponse(AbstractModel):
    """DescribeDBParameters返回参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc。
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


class DescribeDBPerformanceDetailsRequest(AbstractModel):
    """DescribeDBPerformanceDetails请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc。
        :type InstanceId: str
        :param StartTime: 开始日期，格式yyyy-mm-dd
        :type StartTime: str
        :param EndTime: 结束日期，格式yyyy-mm-dd
        :type EndTime: str
        :param MetricName: 拉取的指标名，支持的值为：long_query,select_total,update_total,insert_total,delete_total,mem_hit_rate,disk_iops,conn_active,is_master_switched,slave_delay
        :type MetricName: str
        """
        self.InstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.MetricName = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.MetricName = params.get("MetricName")


class DescribeDBPerformanceDetailsResponse(AbstractModel):
    """DescribeDBPerformanceDetails返回参数结构体"""

    def __init__(self):
        """
        :param Master: 主节点性能监控数据
        :type Master: :class:`tcecloud.mariadb.v20170312.models.PerformanceMonitorSet`
        :param Slave1: 备机1性能监控数据
        :type Slave1: :class:`tcecloud.mariadb.v20170312.models.PerformanceMonitorSet`
        :param Slave2: 备机2性能监控数据，如果实例是一主一从，则没有该字段
        :type Slave2: :class:`tcecloud.mariadb.v20170312.models.PerformanceMonitorSet`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Master = None
        self.Slave1 = None
        self.Slave2 = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Master") is not None:
            self.Master = PerformanceMonitorSet()
            self.Master._deserialize(params.get("Master"))
        if params.get("Slave1") is not None:
            self.Slave1 = PerformanceMonitorSet()
            self.Slave1._deserialize(params.get("Slave1"))
        if params.get("Slave2") is not None:
            self.Slave2 = PerformanceMonitorSet()
            self.Slave2._deserialize(params.get("Slave2"))
        self.RequestId = params.get("RequestId")


class DescribeDBPerformanceRequest(AbstractModel):
    """DescribeDBPerformance请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc。
        :type InstanceId: str
        :param StartTime: 开始日期，格式yyyy-mm-dd
        :type StartTime: str
        :param EndTime: 结束日期，格式yyyy-mm-dd
        :type EndTime: str
        :param MetricName: 拉取的指标名，支持的值为：long_query,select_total,update_total,insert_total,delete_total,mem_hit_rate,disk_iops,conn_active,is_master_switched,slave_delay
        :type MetricName: str
        """
        self.InstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.MetricName = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.MetricName = params.get("MetricName")


class DescribeDBPerformanceResponse(AbstractModel):
    """DescribeDBPerformance返回参数结构体"""

    def __init__(self):
        """
        :param LongQuery: 慢查询数
        :type LongQuery: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param SelectTotal: 查询操作数SELECT
        :type SelectTotal: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param UpdateTotal: 更新操作数UPDATE
        :type UpdateTotal: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param InsertTotal: 插入操作数INSERT
        :type InsertTotal: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param DeleteTotal: 删除操作数DELETE
        :type DeleteTotal: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param MemHitRate: 缓存命中率
        :type MemHitRate: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param DiskIops: 磁盘每秒IO次数
        :type DiskIops: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param ConnActive: 活跃连接数
        :type ConnActive: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param IsMasterSwitched: 是否发生主备切换，1为发生，0否
        :type IsMasterSwitched: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param SlaveDelay: 主备延迟
        :type SlaveDelay: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.LongQuery = None
        self.SelectTotal = None
        self.UpdateTotal = None
        self.InsertTotal = None
        self.DeleteTotal = None
        self.MemHitRate = None
        self.DiskIops = None
        self.ConnActive = None
        self.IsMasterSwitched = None
        self.SlaveDelay = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("LongQuery") is not None:
            self.LongQuery = MonitorData()
            self.LongQuery._deserialize(params.get("LongQuery"))
        if params.get("SelectTotal") is not None:
            self.SelectTotal = MonitorData()
            self.SelectTotal._deserialize(params.get("SelectTotal"))
        if params.get("UpdateTotal") is not None:
            self.UpdateTotal = MonitorData()
            self.UpdateTotal._deserialize(params.get("UpdateTotal"))
        if params.get("InsertTotal") is not None:
            self.InsertTotal = MonitorData()
            self.InsertTotal._deserialize(params.get("InsertTotal"))
        if params.get("DeleteTotal") is not None:
            self.DeleteTotal = MonitorData()
            self.DeleteTotal._deserialize(params.get("DeleteTotal"))
        if params.get("MemHitRate") is not None:
            self.MemHitRate = MonitorData()
            self.MemHitRate._deserialize(params.get("MemHitRate"))
        if params.get("DiskIops") is not None:
            self.DiskIops = MonitorData()
            self.DiskIops._deserialize(params.get("DiskIops"))
        if params.get("ConnActive") is not None:
            self.ConnActive = MonitorData()
            self.ConnActive._deserialize(params.get("ConnActive"))
        if params.get("IsMasterSwitched") is not None:
            self.IsMasterSwitched = MonitorData()
            self.IsMasterSwitched._deserialize(params.get("IsMasterSwitched"))
        if params.get("SlaveDelay") is not None:
            self.SlaveDelay = MonitorData()
            self.SlaveDelay._deserialize(params.get("SlaveDelay"))
        self.RequestId = params.get("RequestId")


class DescribeDBResourceUsageDetailsRequest(AbstractModel):
    """DescribeDBResourceUsageDetails请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc。
        :type InstanceId: str
        :param StartTime: 开始日期，格式yyyy-mm-dd
        :type StartTime: str
        :param EndTime: 结束日期，格式yyyy-mm-dd
        :type EndTime: str
        :param MetricName: 拉取的指标名称，支持的值为：data_disk_available,binlog_disk_available,mem_available,cpu_usage_rate
        :type MetricName: str
        """
        self.InstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.MetricName = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.MetricName = params.get("MetricName")


class DescribeDBResourceUsageDetailsResponse(AbstractModel):
    """DescribeDBResourceUsageDetails返回参数结构体"""

    def __init__(self):
        """
        :param Master: 主节点资源使用情况监控数据
        :type Master: :class:`tcecloud.mariadb.v20170312.models.ResourceUsageMonitorSet`
        :param Slave1: 备机1资源使用情况监控数据
        :type Slave1: :class:`tcecloud.mariadb.v20170312.models.ResourceUsageMonitorSet`
        :param Slave2: 备机2资源使用情况监控数据
        :type Slave2: :class:`tcecloud.mariadb.v20170312.models.ResourceUsageMonitorSet`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Master = None
        self.Slave1 = None
        self.Slave2 = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Master") is not None:
            self.Master = ResourceUsageMonitorSet()
            self.Master._deserialize(params.get("Master"))
        if params.get("Slave1") is not None:
            self.Slave1 = ResourceUsageMonitorSet()
            self.Slave1._deserialize(params.get("Slave1"))
        if params.get("Slave2") is not None:
            self.Slave2 = ResourceUsageMonitorSet()
            self.Slave2._deserialize(params.get("Slave2"))
        self.RequestId = params.get("RequestId")


class DescribeDBResourceUsageRequest(AbstractModel):
    """DescribeDBResourceUsage请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc。
        :type InstanceId: str
        :param StartTime: 开始日期，格式yyyy-mm-dd
        :type StartTime: str
        :param EndTime: 结束日期，格式yyyy-mm-dd
        :type EndTime: str
        :param MetricName: 拉取的指标名称，支持的值为：data_disk_available,binlog_disk_available,mem_available,cpu_usage_rate
        :type MetricName: str
        """
        self.InstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.MetricName = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.MetricName = params.get("MetricName")


class DescribeDBResourceUsageResponse(AbstractModel):
    """DescribeDBResourceUsage返回参数结构体"""

    def __init__(self):
        """
        :param BinlogDiskAvailable: binlog日志磁盘可用空间,单位GB
        :type BinlogDiskAvailable: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param DataDiskAvailable: 磁盘可用空间,单位GB
        :type DataDiskAvailable: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param CpuUsageRate: CPU利用率
        :type CpuUsageRate: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param MemAvailable: 内存可用空间,单位GB
        :type MemAvailable: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.BinlogDiskAvailable = None
        self.DataDiskAvailable = None
        self.CpuUsageRate = None
        self.MemAvailable = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("BinlogDiskAvailable") is not None:
            self.BinlogDiskAvailable = MonitorData()
            self.BinlogDiskAvailable._deserialize(params.get("BinlogDiskAvailable"))
        if params.get("DataDiskAvailable") is not None:
            self.DataDiskAvailable = MonitorData()
            self.DataDiskAvailable._deserialize(params.get("DataDiskAvailable"))
        if params.get("CpuUsageRate") is not None:
            self.CpuUsageRate = MonitorData()
            self.CpuUsageRate._deserialize(params.get("CpuUsageRate"))
        if params.get("MemAvailable") is not None:
            self.MemAvailable = MonitorData()
            self.MemAvailable._deserialize(params.get("MemAvailable"))
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
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc，可以通过 DescribeDBInstances 查询实例详情获得。
        :type InstanceId: str
        :param StartTime: 开始时间
        :type StartTime: str
        :param Db: 要查询的慢查询语句对应的数据库名称
        :type Db: str
        :param User: 要查询的慢查询语句对应的用户名称
        :type User: str
        :param CheckSum: 要查询的慢查询语句的校验和，可以通过查询慢查询日志列表获得
        :type CheckSum: str
        :param EndTime: 结束时间
        :type EndTime: str
        :param Slave: 是否查询从机的慢查询。0-主机；1-从机
        :type Slave: int
        """
        self.InstanceId = None
        self.StartTime = None
        self.Db = None
        self.User = None
        self.CheckSum = None
        self.EndTime = None
        self.Slave = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.Db = params.get("Db")
        self.User = params.get("User")
        self.CheckSum = params.get("CheckSum")
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
        :param Data: 返回的慢查询详情数据。每个点代表一个时间段内慢查询SQL出现的记录次数，一个时间段的长度由请求的开始时间和结束时间的差值决定，小于1天是5分钟一段，大于1天小于7天是30分钟一段，大于7天是2个小时一段。
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
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc。
        :type InstanceId: str
        :param Offset: 从结果的第几条数据开始返回
        :type Offset: int
        :param Limit: 返回的结果条数
        :type Limit: int
        :param StartTime: 查询的起始时间，形如2016-07-23 14:55:20
        :type StartTime: str
        :param EndTime: 查询的结束时间，形如2016-08-22 14:55:20
        :type EndTime: str
        :param Db: 要查询的具体数据库名称
        :type Db: str
        :param OrderBy: 排序指标，取值为query_time_sum或者query_count
        :type OrderBy: str
        :param OrderByType: 排序类型，desc或者asc
        :type OrderByType: str
        :param Slave: 是否查询从机的慢查询，0-主机; 1-从机
        :type Slave: int
        """
        self.InstanceId = None
        self.Offset = None
        self.Limit = None
        self.StartTime = None
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
        self.EndTime = params.get("EndTime")
        self.Db = params.get("Db")
        self.OrderBy = params.get("OrderBy")
        self.OrderByType = params.get("OrderByType")
        self.Slave = params.get("Slave")


class DescribeDBSlowLogsResponse(AbstractModel):
    """DescribeDBSlowLogs返回参数结构体"""

    def __init__(self):
        """
        :param Data: 慢查询日志数据
        :type Data: list of SlowLogData
        :param LockTimeSum: 所有语句锁时间总和
        :type LockTimeSum: float
        :param QueryCount: 所有语句查询总次数
        :type QueryCount: int
        :param Total: 总记录数
        :type Total: int
        :param QueryTimeSum: 所有语句查询时间总和
        :type QueryTimeSum: float
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.LockTimeSum = None
        self.QueryCount = None
        self.Total = None
        self.QueryTimeSum = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = SlowLogData()
                obj._deserialize(item)
                self.Data.append(obj)
        self.LockTimeSum = params.get("LockTimeSum")
        self.QueryCount = params.get("QueryCount")
        self.Total = params.get("Total")
        self.QueryTimeSum = params.get("QueryTimeSum")
        self.RequestId = params.get("RequestId")


class DescribeDBSyncModeRequest(AbstractModel):
    """DescribeDBSyncMode请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID，形如：tdsql-ow728lmc
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


class DescribeDefaultConfigTemplateRequest(AbstractModel):
    """DescribeDefaultConfigTemplate请求参数结构体"""

    def __init__(self):
        """
        :param DefaultTemplateName: 默认模板名称
        :type DefaultTemplateName: str
        """
        self.DefaultTemplateName = None

    def _deserialize(self, params):
        self.DefaultTemplateName = params.get("DefaultTemplateName")


class DescribeDefaultConfigTemplateResponse(AbstractModel):
    """DescribeDefaultConfigTemplate返回参数结构体"""

    def __init__(self):
        """
        :param TemplateParamSet: 参数列表
        :type TemplateParamSet: list of TemplateParam
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TemplateParamSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("TemplateParamSet") is not None:
            self.TemplateParamSet = []
            for item in params.get("TemplateParamSet"):
                obj = TemplateParam()
                obj._deserialize(item)
                self.TemplateParamSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeFenceDBInstanceSpecsRequest(AbstractModel):
    """DescribeFenceDBInstanceSpecs请求参数结构体"""


class DescribeFenceDBInstanceSpecsResponse(AbstractModel):
    """DescribeFenceDBInstanceSpecs返回参数结构体"""

    def __init__(self):
        """
        :param Specs: 按机型分类的可售卖规格列表
        :type Specs: list of InstanceSpec
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Specs = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Specs") is not None:
            self.Specs = []
            for item in params.get("Specs"):
                obj = InstanceSpec()
                obj._deserialize(item)
                self.Specs.append(obj)
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


class DescribeInstanceProxyConfigRequest(AbstractModel):
    """DescribeInstanceProxyConfig请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class DescribeInstanceProxyConfigResponse(AbstractModel):
    """DescribeInstanceProxyConfig返回参数结构体"""

    def __init__(self):
        """
        :param ProxyConfigParamSet: 网关配置参数
        :type ProxyConfigParamSet: list of ProxyConfigParam
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ProxyConfigParamSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("ProxyConfigParamSet") is not None:
            self.ProxyConfigParamSet = []
            for item in params.get("ProxyConfigParamSet"):
                obj = ProxyConfigParam()
                obj._deserialize(item)
                self.ProxyConfigParamSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInstanceSSLAttributesRequest(AbstractModel):
    """DescribeInstanceSSLAttributes请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class DescribeInstanceSSLAttributesResponse(AbstractModel):
    """DescribeInstanceSSLAttributes返回参数结构体"""

    def __init__(self):
        """
        :param Status: 实例SSL认证功能当前状态。1-开启中；2-已开启；3-已关闭；4-关闭中
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
        :param SerialIds: 实例的SerialId
        :type SerialIds: list of str
        :param Limit: 分页返回，每页返回的数目，默认为20。取值范围为1到100
        :type Limit: int
        :param Offset: 从偏移量Offset开始返回，默认取值为0
        :type Offset: int
        :param OrderBy: 取值为createtime或者instancename，表示按照创建时间或者实例名进行排序
        :type OrderBy: str
        :param OrderByType: 取值为desc或者asc。desc-表示降序；asc-表示升序
        :type OrderByType: str
        :param ClusterNames: 集群名称数组
        :type ClusterNames: list of str
        :param ZkNames: Zk名称数组
        :type ZkNames: list of str
        :param Vips: Vip数组
        :type Vips: list of str
        :param InstanceNames: 实例名称数组
        :type InstanceNames: list of str
        :param InstanceIds: 实例ID的数组
        :type InstanceIds: list of str
        :param ProjectId: 按照项目ID进行过滤
        :type ProjectId: int
        :param UniqueVpcId: 私有网络ID，形如 vpc-nobbvxkf
        :type UniqueVpcId: str
        :param UniqueSubnetId: 子网ID，形如 subnet-dnn20os8
        :type UniqueSubnetId: str
        """
        self.SerialIds = None
        self.Limit = None
        self.Offset = None
        self.OrderBy = None
        self.OrderByType = None
        self.ClusterNames = None
        self.ZkNames = None
        self.Vips = None
        self.InstanceNames = None
        self.InstanceIds = None
        self.ProjectId = None
        self.UniqueVpcId = None
        self.UniqueSubnetId = None

    def _deserialize(self, params):
        self.SerialIds = params.get("SerialIds")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.OrderBy = params.get("OrderBy")
        self.OrderByType = params.get("OrderByType")
        self.ClusterNames = params.get("ClusterNames")
        self.ZkNames = params.get("ZkNames")
        self.Vips = params.get("Vips")
        self.InstanceNames = params.get("InstanceNames")
        self.InstanceIds = params.get("InstanceIds")
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
        :type Instances: list of InstanceInfo
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
                obj = InstanceInfo()
                obj._deserialize(item)
                self.Instances.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeLatestCloudDBAReportRequest(AbstractModel):
    """DescribeLatestCloudDBAReport请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


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


class DescribePriceRequest(AbstractModel):
    """DescribePrice请求参数结构体"""

    def __init__(self):
        """
               :param Zone: 欲新购实例的可用区ID。
               :type Zone: str
               :param NodeCount: 实例节点个数，可以通过 DescribeDBInstanceSpecs
        查询实例规格获得。
               :type NodeCount: int
               :param Memory: 内存大小，单位：GB，可以通过 DescribeDBInstanceSpecs
        查询实例规格获得。
               :type Memory: int
               :param Storage: 存储空间大小，单位：GB，可以通过 DescribeDBInstanceSpecs
        查询实例规格获得不同内存大小对应的磁盘规格下限和上限。
               :type Storage: int
               :param Period: 欲购买的时长，单位：月。
               :type Period: int
               :param Count: 欲购买的数量，默认查询购买1个实例的价格。
               :type Count: int
               :param Paymode: 付费类型。postpaid：按量付费   prepaid：预付费
               :type Paymode: str
        """
        self.Zone = None
        self.NodeCount = None
        self.Memory = None
        self.Storage = None
        self.Period = None
        self.Count = None
        self.Paymode = None

    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.NodeCount = params.get("NodeCount")
        self.Memory = params.get("Memory")
        self.Storage = params.get("Storage")
        self.Period = params.get("Period")
        self.Count = params.get("Count")
        self.Paymode = params.get("Paymode")


class DescribePriceResponse(AbstractModel):
    """DescribePrice返回参数结构体"""

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


class DescribeRenewalPriceRequest(AbstractModel):
    """DescribeRenewalPrice请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 待续费的实例ID。形如：tdsql-ow728lmc，可以通过 DescribeDBInstances 查询实例详情获得。
        :type InstanceId: str
        :param Period: 续费时长，单位：月。不传则默认为1个月。
        :type Period: int
        """
        self.InstanceId = None
        self.Period = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Period = params.get("Period")


class DescribeRenewalPriceResponse(AbstractModel):
    """DescribeRenewalPrice返回参数结构体"""

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


class DescribeSaleInfoRequest(AbstractModel):
    """DescribeSaleInfo请求参数结构体"""


class DescribeSaleInfoResponse(AbstractModel):
    """DescribeSaleInfo返回参数结构体"""

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


class DescribeSqlLogsRequest(AbstractModel):
    """DescribeSqlLogs请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc，可以通过 DescribeDBInstances 查询实例详情获得。
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


class DescribeSyncTasksRequest(AbstractModel):
    """DescribeSyncTasks请求参数结构体"""

    def __init__(self):
        """
        :param TaskNames: 任务名称列表，用于根据任务名称筛选。
        :type TaskNames: list of str
        :param TaskIds: 任务Id列表，用于根据任务Id筛选。
        :type TaskIds: list of int
        :param SrcInstanceIds: 同步源实例Id列表，实例Id形如：tdsql-ow728lmc，用于源实例Id筛选。
        :type SrcInstanceIds: list of str
        :param DstInstanceIds: 同步目标实例Id列表，实例Id形如：tdsql-ow728lmc，用于目标实例Id筛选。
        :type DstInstanceIds: list of str
        :param Status: 任务状态，0：初始化任务，1：参数不对，2：执行过程中，3：执行成功， 4：任务被停止，5：执行失败，用于任务状态筛选。
        :type Status: list of int
        :param Limit: 分页，页大小，默认20。
        :type Limit: int
        :param Offset: 分页，页偏移量，默认0。
        :type Offset: int
        :param OrderBy: 排序字段，默认createtime
        :type OrderBy: str
        :param OrderByType: 排序方式，desc，asc可选，默认desc
        :type OrderByType: str
        """
        self.TaskNames = None
        self.TaskIds = None
        self.SrcInstanceIds = None
        self.DstInstanceIds = None
        self.Status = None
        self.Limit = None
        self.Offset = None
        self.OrderBy = None
        self.OrderByType = None

    def _deserialize(self, params):
        self.TaskNames = params.get("TaskNames")
        self.TaskIds = params.get("TaskIds")
        self.SrcInstanceIds = params.get("SrcInstanceIds")
        self.DstInstanceIds = params.get("DstInstanceIds")
        self.Status = params.get("Status")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.OrderBy = params.get("OrderBy")
        self.OrderByType = params.get("OrderByType")


class DescribeSyncTasksResponse(AbstractModel):
    """DescribeSyncTasks返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 总记录数
        :type TotalCount: int
        :param SyncTaskSet: 同步任务列表
        :type SyncTaskSet: list of SyncTaskInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.SyncTaskSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("SyncTaskSet") is not None:
            self.SyncTaskSet = []
            for item in params.get("SyncTaskSet"):
                obj = SyncTaskInfo()
                obj._deserialize(item)
                self.SyncTaskSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeUpgradePriceRequest(AbstractModel):
    """DescribeUpgradePrice请求参数结构体"""

    def __init__(self):
        """
               :param InstanceId: 待升级的实例ID。形如：tdsql-ow728lmc，可以通过 DescribeDBInstances 查询实例详情获得。
               :type InstanceId: str
               :param Memory: 内存大小，单位：GB，可以通过 DescribeDBInstanceSpecs
        查询实例规格获得。
               :type Memory: int
               :param Storage: 存储空间大小，单位：GB，可以通过 DescribeDBInstanceSpecs
        查询实例规格获得不同内存大小对应的磁盘规格下限和上限。
               :type Storage: int
        """
        self.InstanceId = None
        self.Memory = None
        self.Storage = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Memory = params.get("Memory")
        self.Storage = params.get("Storage")


class DescribeUpgradePriceResponse(AbstractModel):
    """DescribeUpgradePrice返回参数结构体"""

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


class DescribeUserTasksRequest(AbstractModel):
    """DescribeUserTasks请求参数结构体"""

    def __init__(self):
        """
        :param RegionIds: 地域ID列表
        :type RegionIds: list of int
        :param Statuses: 状态列表
        :type Statuses: list of int
        :param InstanceIds: 实例ID列表，形如：tdsql-ow728lmc。
        :type InstanceIds: list of str
        :param FlowTypes: 任务类型列表
        :type FlowTypes: list of int
        :param StartTime: 开始时间
        :type StartTime: str
        :param EndTime: 结束时间
        :type EndTime: str
        :param UTaskIds: 用户任务ID列表
        :type UTaskIds: list of int
        :param Limit: 限制数目
        :type Limit: int
        :param Offset: 偏移量
        :type Offset: int
        """
        self.RegionIds = None
        self.Statuses = None
        self.InstanceIds = None
        self.FlowTypes = None
        self.StartTime = None
        self.EndTime = None
        self.UTaskIds = None
        self.Limit = None
        self.Offset = None

    def _deserialize(self, params):
        self.RegionIds = params.get("RegionIds")
        self.Statuses = params.get("Statuses")
        self.InstanceIds = params.get("InstanceIds")
        self.FlowTypes = params.get("FlowTypes")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.UTaskIds = params.get("UTaskIds")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")


class DescribeUserTasksResponse(AbstractModel):
    """DescribeUserTasks返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 总数目
        :type TotalCount: int
        :param FlowSet: 任务列表
        :type FlowSet: list of Flow
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.FlowSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("FlowSet") is not None:
            self.FlowSet = []
            for item in params.get("FlowSet"):
                obj = Flow()
                obj._deserialize(item)
                self.FlowSet.append(obj)
        self.RequestId = params.get("RequestId")


class DestroyHourDBInstanceRequest(AbstractModel):
    """DestroyHourDBInstance请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID，形如tdsql-o0q206pq
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class DestroyHourDBInstanceResponse(AbstractModel):
    """DestroyHourDBInstance返回参数结构体"""

    def __init__(self):
        """
        :param FlowId: 删除任务ID。删除任务是异步任务，用FlowId做为参数，调用DescribeFlow接口，查询任务执行状态。
        :type FlowId: int
        :param InstanceId: 实例Id，形如tdsql-o0q206pq
        :type InstanceId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FlowId = None
        self.InstanceId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.InstanceId = params.get("InstanceId")
        self.RequestId = params.get("RequestId")


class DstExtraInfo(AbstractModel):
    """展示同步任务详情时，表示目标实例的一些额外信息。"""

    def __init__(self):
        """
                :param SubnetId: 私用网络ID
        注意：此字段可能返回 null，表示取不到有效值。
                :type SubnetId: str
                :param VpcId: 子网ID
        注意：此字段可能返回 null，表示取不到有效值。
                :type VpcId: str
                :param User: 目标实例登录用户名
        注意：此字段可能返回 null，表示取不到有效值。
                :type User: str
                :param Ip: 目标实例的IP地址
        注意：此字段可能返回 null，表示取不到有效值。
                :type Ip: str
                :param Port: 目标实例的端口地址
        注意：此字段可能返回 null，表示取不到有效值。
                :type Port: int
                :param DirectConnectGatewayId: 如果目标实例通过专线接入的话，表示接入的专线ID
        注意：此字段可能返回 null，表示取不到有效值。
                :type DirectConnectGatewayId: str
        """
        self.SubnetId = None
        self.VpcId = None
        self.User = None
        self.Ip = None
        self.Port = None
        self.DirectConnectGatewayId = None

    def _deserialize(self, params):
        self.SubnetId = params.get("SubnetId")
        self.VpcId = params.get("VpcId")
        self.User = params.get("User")
        self.Ip = params.get("Ip")
        self.Port = params.get("Port")
        self.DirectConnectGatewayId = params.get("DirectConnectGatewayId")


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


class Flow(AbstractModel):
    """任务"""

    def __init__(self):
        """
        :param Id: 任务ID
        :type Id: int
        :param AppId: 应用ID
        :type AppId: int
        :param Status: 状态
        :type Status: int
        :param UserTaskType: 用户任务类型
        :type UserTaskType: int
        :param CreateTime: 创建时间
        :type CreateTime: str
        :param EndTime: 结束时间
        :type EndTime: str
        :param ErrMsg: 错误信息
        :type ErrMsg: str
        :param InputData: 输入数据
        :type InputData: str
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc
        :type InstanceId: str
        :param InstanceName: 实例名称
        :type InstanceName: str
        :param RegionId: 地域ID
        :type RegionId: int
        """
        self.Id = None
        self.AppId = None
        self.Status = None
        self.UserTaskType = None
        self.CreateTime = None
        self.EndTime = None
        self.ErrMsg = None
        self.InputData = None
        self.InstanceId = None
        self.InstanceName = None
        self.RegionId = None

    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.AppId = params.get("AppId")
        self.Status = params.get("Status")
        self.UserTaskType = params.get("UserTaskType")
        self.CreateTime = params.get("CreateTime")
        self.EndTime = params.get("EndTime")
        self.ErrMsg = params.get("ErrMsg")
        self.InputData = params.get("InputData")
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.RegionId = params.get("RegionId")


class GrantAccountPrivilegesRequest(AbstractModel):
    """GrantAccountPrivileges请求参数结构体"""

    def __init__(self):
        r"""
                :param InstanceId: 实例 ID，形如：tdsql-ow728lmc，可以通过 DescribeDBInstances 查询实例详情获得。
                :type InstanceId: str
                :param UserName: 登录用户名。
                :type UserName: str
                :param Host: 用户允许的访问 host，用户名+host唯一确定一个账号。
                :type Host: str
                :param DbName: 数据库名。如果为 \*，表示设置全局权限（即 \*.\*），此时忽略 Type 和 Object 参数。当DbName不为\*时，需要传入参 Type。
                :type DbName: str
                :param Privileges: 全局权限： SELECT，INSERT，UPDATE，DELETE，CREATE，DROP，REFERENCES，INDEX，ALTER，CREATE TEMPORARY TABLES，LOCK TABLES，EXECUTE，CREATE VIEW，SHOW VIEW，CREATE ROUTINE，ALTER ROUTINE，EVENT，TRIGGER，SHOW DATABASES
        库权限： SELECT，INSERT，UPDATE，DELETE，CREATE，DROP，REFERENCES，INDEX，ALTER，CREATE TEMPORARY TABLES，LOCK TABLES，EXECUTE，CREATE VIEW，SHOW VIEW，CREATE ROUTINE，ALTER ROUTINE，EVENT，TRIGGER
        表/视图权限： SELECT，INSERT，UPDATE，DELETE，CREATE，DROP，REFERENCES，INDEX，ALTER，CREATE VIEW，SHOW VIEW，TRIGGER
        存储过程/函数权限： ALTER ROUTINE，EXECUTE
        字段权限： INSERT，REFERENCES，SELECT，UPDATE
                :type Privileges: list of str
                :param Type: 类型,可以填入 table 、 view 、 proc 、 func 和 \*。当 DbName 为具体数据库名，Type为 \* 时，表示设置该数据库权限（即db.\*），此时忽略 Object 参数
                :type Type: str
                :param Object: 具体的 Type 的名称，比如 Type 为 table 时就是具体的表名。DbName 和 Type 都为具体名称，则 Object 表示具体对象名，不能为 \* 或者为空
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


class InitDBInstancesRequest(AbstractModel):
    """InitDBInstances请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 待初始化的实例Id列表，形如：tdsql-ow728lmc，可以通过 DescribeDBInstances 查询实例详情获得。
        :type InstanceIds: list of str
        :param Params: 参数列表。本接口的可选值为：character_set_server（字符集，必传），lower_case_table_names（表名大小写敏感，必传，0 - 敏感；1-不敏感），innodb_page_size（innodb数据页，默认16K），sync_mode（同步模式：0 - 异步； 1 - 强同步；2 - 强同步可退化。默认为强同步）。
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


class InitDBInstancesResponse(AbstractModel):
    """InitDBInstances返回参数结构体"""

    def __init__(self):
        """
        :param FlowId: 异步任务Id，可通过 DescribeFlow 查询任务状态。
        :type FlowId: int
        :param InstanceIds: 透传入参。
        :type InstanceIds: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FlowId = None
        self.InstanceIds = None
        self.RequestId = None

    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.InstanceIds = params.get("InstanceIds")
        self.RequestId = params.get("RequestId")


class InstanceConfig(AbstractModel):
    """实例配置"""

    def __init__(self):
        """
        :param Id: 实例配置ID，形如：1
        :type Id: int
        :param ModTime: 修改时间
        :type ModTime: str
        :param ParamName: 参数名称
        :type ParamName: str
        :param ParamNewValue: 修改后参数值
        :type ParamNewValue: str
        :param ParamOldValue: 修改前参数值
        :type ParamOldValue: str
        :param Status: 修改状态, 0:成功, -1:失败, -2:值非法
        :type Status: int
        """
        self.Id = None
        self.ModTime = None
        self.ParamName = None
        self.ParamNewValue = None
        self.ParamOldValue = None
        self.Status = None

    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.ModTime = params.get("ModTime")
        self.ParamName = params.get("ParamName")
        self.ParamNewValue = params.get("ParamNewValue")
        self.ParamOldValue = params.get("ParamOldValue")
        self.Status = params.get("Status")


class InstanceInfo(AbstractModel):
    """实例信息"""

    def __init__(self):
        """
        :param InstanceId: 实例短ID，形如tdsql-hdbirf67
        :type InstanceId: str
        :param InstanceName: 实例名称
        :type InstanceName: str
        :param AppId: 实例对应的AppId
        :type AppId: int
        :param OriginSerialId: 实例最初的SerialId，实例扩容后SerialId会变，OriginSerialId表示实例最初的SerialId，不会改变
        :type OriginSerialId: str
        :param SerialId: 实例SerialId
        :type SerialId: str
        :param Region: 实例地域
        :type Region: str
        :param Zone: 实例可用区
        :type Zone: str
        :param VpcId: 实例是VPC网络的话，表示实例VPC网络ID，数字ID
        :type VpcId: int
        :param SubnetId: 实例是VPC网络的话，表示实例所属子网ID，数字ID
        :type SubnetId: int
        :param UniqueVpcId: 实例是VPC网络的话，表示实例VPC网络ID，英文短ID
        :type UniqueVpcId: str
        :param UniqueSubnetId: 实例是VPC网络的话，表示实例子网ID，英文短ID
        :type UniqueSubnetId: str
        :param Status: 实例状态信息
        :type Status: int
        :param Vip: 实例Vip
        :type Vip: str
        :param Vport: 实例端口
        :type Vport: int
        :param ZkName: 实例对应的ZK名称
        :type ZkName: str
        :param ClusterName: 实例集群名称
        :type ClusterName: str
        :param NodeCount: 实例是一主一从还是一主两从。2-一主一从；3-一主两从
        :type NodeCount: int
        :param Id: 实例数字ID
        :type Id: int
        :param DbVersion: 数据库版本
        :type DbVersion: str
        """
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
        self.Id = None
        self.DbVersion = None

    def _deserialize(self, params):
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
        self.Id = params.get("Id")
        self.DbVersion = params.get("DbVersion")


class InstanceSpec(AbstractModel):
    """按机型归类的实例可售卖规格信息"""

    def __init__(self):
        """
        :param Machine: 设备型号
        :type Machine: str
        :param SpecInfos: 该机型对应的可售卖规格列表
        :type SpecInfos: list of SpecConfigInfo
        """
        self.Machine = None
        self.SpecInfos = None

    def _deserialize(self, params):
        self.Machine = params.get("Machine")
        if params.get("SpecInfos") is not None:
            self.SpecInfos = []
            for item in params.get("SpecInfos"):
                obj = SpecConfigInfo()
                obj._deserialize(item)
                self.SpecInfos.append(obj)


class IsolateDedicatedDBInstanceRequest(AbstractModel):
    """IsolateDedicatedDBInstance请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 Id，形如：tdsql-ow728lmc。
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


class IsolateHourDBInstanceRequest(AbstractModel):
    """IsolateHourDBInstance请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID，形如tdsql-o0q206pq
        :type InstanceId: str
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class IsolateHourDBInstanceResponse(AbstractModel):
    """IsolateHourDBInstance返回参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID，形如tdsql-o0q206pq
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
        注意：此字段可能返回 null，表示取不到有效值。
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
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc，可以通过 DescribeDBInstances 查询实例详情获得。
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
        :param InstanceIds: 实例 ID列表，形如：tdsql-ow728lmc。
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


class ModifyBackupTimeRequest(AbstractModel):
    """ModifyBackupTime请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID，形如：tdsql-ow728lmc，可以通过 DescribeDBInstances 查询实例详情获得。
        :type InstanceId: str
        :param StartBackupTime: 每天备份执行的区间的开始时间，格式 mm:ss，形如 22:00
        :type StartBackupTime: str
        :param EndBackupTime: 每天备份执行的区间的结束时间，格式 mm:ss，形如 23:59
        :type EndBackupTime: str
        """
        self.InstanceId = None
        self.StartBackupTime = None
        self.EndBackupTime = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartBackupTime = params.get("StartBackupTime")
        self.EndBackupTime = params.get("EndBackupTime")


class ModifyBackupTimeResponse(AbstractModel):
    """ModifyBackupTime返回参数结构体"""

    def __init__(self):
        """
        :param Status: 设置的状态，0 表示成功
        :type Status: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Status = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class ModifyConfigTemplateRequest(AbstractModel):
    """ModifyConfigTemplate请求参数结构体"""

    def __init__(self):
        """
        :param ConfigTemplateId: 参数模板Id，可以通过 DescribeConfigTemplates 查询参数模板列表获得。
        :type ConfigTemplateId: int
        :param ConfigParams: 配置模板参数列表
        :type ConfigParams: list of ConfigParam
        """
        self.ConfigTemplateId = None
        self.ConfigParams = None

    def _deserialize(self, params):
        self.ConfigTemplateId = params.get("ConfigTemplateId")
        if params.get("ConfigParams") is not None:
            self.ConfigParams = []
            for item in params.get("ConfigParams"):
                obj = ConfigParam()
                obj._deserialize(item)
                self.ConfigParams.append(obj)


class ModifyConfigTemplateResponse(AbstractModel):
    """ModifyConfigTemplate返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDBEncryptAttributesRequest(AbstractModel):
    """ModifyDBEncryptAttributes请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例Id，形如：tdsql-ow728lmc。
        :type InstanceId: str
        :param EncryptEnabled: 是否启用数据加密，开启后暂不支持关闭。本接口的可选值为：1-开启数据加密。
        :type EncryptEnabled: int
        """
        self.InstanceId = None
        self.EncryptEnabled = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.EncryptEnabled = params.get("EncryptEnabled")


class ModifyDBEncryptAttributesResponse(AbstractModel):
    """ModifyDBEncryptAttributes返回参数结构体"""

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
        :param InstanceId: 待修改的实例 ID。形如：tdsql-ow728lmc，可以通过 DescribeDBInstances 查询实例详情获得。
        :type InstanceId: str
        :param InstanceName: 新的实例名称。允许的字符为字母、数字、下划线、连字符和中文。
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
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
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
        :param InstanceIds: 待修改的实例ID列表。实例 ID 形如：tdsql-ow728lmc，可以通过 DescribeDBInstances 查询实例详情获得。
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
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc。
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
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc。
        :type InstanceId: str
        :param Result: 参数修改结果
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
        :param InstanceId: 待修改同步模式的实例ID。形如：tdsql-ow728lmc。
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
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc。
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


class ModifyInstanceSSLAttributesRequest(AbstractModel):
    """ModifyInstanceSSLAttributes请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID
        :type InstanceId: str
        :param SSLEnabled: 是否开启实例的SSL认证。0-关闭；1-开启
        :type SSLEnabled: int
        """
        self.InstanceId = None
        self.SSLEnabled = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.SSLEnabled = params.get("SSLEnabled")


class ModifyInstanceSSLAttributesResponse(AbstractModel):
    """ModifyInstanceSSLAttributes返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyInstanceVipRequest(AbstractModel):
    """ModifyInstanceVip请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例ID
        :type InstanceId: str
        :param Vip: 实例VIP
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


class MonitorData(AbstractModel):
    """监控数据"""

    def __init__(self):
        """
        :param StartTime: 起始时间，形如 2018-03-24 23:59:59
        :type StartTime: str
        :param EndTime: 结束时间，形如 2018-03-24 23:59:59
        :type EndTime: str
        :param Data: 监控数据
        :type Data: list of float
        """
        self.StartTime = None
        self.EndTime = None
        self.Data = None

    def _deserialize(self, params):
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Data = params.get("Data")


class OpenDBExtranetAccessRequest(AbstractModel):
    """OpenDBExtranetAccess请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 待开放外网访问的实例ID。形如：tdsql-ow728lmc，可以通过 DescribeDBInstances 查询实例详情获得。
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
                :type Range: :class:`tcecloud.mariadb.v20170312.models.ConstraintRange`
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
                :param SetValue: 设置过的值，参数生效后，该值和value一样。
        注意：此字段可能返回 null，表示取不到有效值。
                :type SetValue: str
                :param Default: 系统默认值
                :type Default: str
                :param Constraint: 参数限制
                :type Constraint: :class:`tcecloud.mariadb.v20170312.models.ParamConstraint`
                :param HaveSetValue: 是否有设置过值，false:没有设置过值，true:有设置过值。
                :type HaveSetValue: bool
        """
        self.Param = None
        self.Value = None
        self.SetValue = None
        self.Default = None
        self.Constraint = None
        self.HaveSetValue = None

    def _deserialize(self, params):
        self.Param = params.get("Param")
        self.Value = params.get("Value")
        self.SetValue = params.get("SetValue")
        self.Default = params.get("Default")
        if params.get("Constraint") is not None:
            self.Constraint = ParamConstraint()
            self.Constraint._deserialize(params.get("Constraint"))
        self.HaveSetValue = params.get("HaveSetValue")


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


class PerformanceMonitorSet(AbstractModel):
    """DB性能监控指标集合"""

    def __init__(self):
        """
        :param UpdateTotal: 更新操作数UPDATE
        :type UpdateTotal: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param DiskIops: 磁盘每秒IO次数
        :type DiskIops: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param ConnActive: 活跃连接数
        :type ConnActive: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param MemHitRate: 缓存命中率
        :type MemHitRate: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param SlaveDelay: 主备延迟
        :type SlaveDelay: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param SelectTotal: 查询操作数SELECT
        :type SelectTotal: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param LongQuery: 慢查询数
        :type LongQuery: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param DeleteTotal: 删除操作数DELETE
        :type DeleteTotal: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param InsertTotal: 插入操作数INSERT
        :type InsertTotal: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param IsMasterSwitched: 是否发生主备切换，1为发生，0否
        :type IsMasterSwitched: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        """
        self.UpdateTotal = None
        self.DiskIops = None
        self.ConnActive = None
        self.MemHitRate = None
        self.SlaveDelay = None
        self.SelectTotal = None
        self.LongQuery = None
        self.DeleteTotal = None
        self.InsertTotal = None
        self.IsMasterSwitched = None

    def _deserialize(self, params):
        if params.get("UpdateTotal") is not None:
            self.UpdateTotal = MonitorData()
            self.UpdateTotal._deserialize(params.get("UpdateTotal"))
        if params.get("DiskIops") is not None:
            self.DiskIops = MonitorData()
            self.DiskIops._deserialize(params.get("DiskIops"))
        if params.get("ConnActive") is not None:
            self.ConnActive = MonitorData()
            self.ConnActive._deserialize(params.get("ConnActive"))
        if params.get("MemHitRate") is not None:
            self.MemHitRate = MonitorData()
            self.MemHitRate._deserialize(params.get("MemHitRate"))
        if params.get("SlaveDelay") is not None:
            self.SlaveDelay = MonitorData()
            self.SlaveDelay._deserialize(params.get("SlaveDelay"))
        if params.get("SelectTotal") is not None:
            self.SelectTotal = MonitorData()
            self.SelectTotal._deserialize(params.get("SelectTotal"))
        if params.get("LongQuery") is not None:
            self.LongQuery = MonitorData()
            self.LongQuery._deserialize(params.get("LongQuery"))
        if params.get("DeleteTotal") is not None:
            self.DeleteTotal = MonitorData()
            self.DeleteTotal._deserialize(params.get("DeleteTotal"))
        if params.get("InsertTotal") is not None:
            self.InsertTotal = MonitorData()
            self.InsertTotal._deserialize(params.get("InsertTotal"))
        if params.get("IsMasterSwitched") is not None:
            self.IsMasterSwitched = MonitorData()
            self.IsMasterSwitched._deserialize(params.get("IsMasterSwitched"))


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
    """描述一个项目的基本信息。"""

    def __init__(self):
        """
        :param IsDefault: 是否默认项目，1 是，0 不是
        :type IsDefault: int
        :param Status: 项目状态,0正常，-1关闭。默认项目为3
        :type Status: int
        :param Name: 项目名称
        :type Name: str
        :param ProjectId: 项目ID
        :type ProjectId: int
        :param AppId: 应用ID
        :type AppId: int
        :param OwnerUin: 主账号Id
        :type OwnerUin: int
        :param CreatorUin: 创建者Id
        :type CreatorUin: int
        :param SrcPlat: 来源平台
        :type SrcPlat: str
        :param SrcAppId: 来源AppId
        :type SrcAppId: int
        :param CreateTime: 创建时间
        :type CreateTime: str
        :param Info: 描述信息
        :type Info: str
        """
        self.IsDefault = None
        self.Status = None
        self.Name = None
        self.ProjectId = None
        self.AppId = None
        self.OwnerUin = None
        self.CreatorUin = None
        self.SrcPlat = None
        self.SrcAppId = None
        self.CreateTime = None
        self.Info = None

    def _deserialize(self, params):
        self.IsDefault = params.get("IsDefault")
        self.Status = params.get("Status")
        self.Name = params.get("Name")
        self.ProjectId = params.get("ProjectId")
        self.AppId = params.get("AppId")
        self.OwnerUin = params.get("OwnerUin")
        self.CreatorUin = params.get("CreatorUin")
        self.SrcPlat = params.get("SrcPlat")
        self.SrcAppId = params.get("SrcAppId")
        self.CreateTime = params.get("CreateTime")
        self.Info = params.get("Info")


class ProxyConfigParam(AbstractModel):
    """网关配置参数"""

    def __init__(self):
        """
        :param Param: 配置参数名称
        :type Param: str
        :param Value: 配置参数值
        :type Value: str
        """
        self.Param = None
        self.Value = None

    def _deserialize(self, params):
        self.Param = params.get("Param")
        self.Value = params.get("Value")


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
        :type AvailableChoice: list of ZoneChooseInfo
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
                obj = ZoneChooseInfo()
                obj._deserialize(item)
                self.AvailableChoice.append(obj)


class RenewDBInstanceRequest(AbstractModel):
    """RenewDBInstance请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 待续费的实例ID。形如：tdsql-ow728lmc，可以通过 DescribeDBInstances 查询实例详情获得。
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


class RenewDBInstanceResponse(AbstractModel):
    """RenewDBInstance返回参数结构体"""

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
        :param InstanceId: 实例 ID，形如：tdsql-ow728lmc，可以通过 DescribeDBInstances 查询实例详情获得。
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


class ResourceUsageMonitorSet(AbstractModel):
    """DB资源使用情况监控指标集合"""

    def __init__(self):
        """
        :param BinlogDiskAvailable: binlog日志磁盘可用空间,单位GB
        :type BinlogDiskAvailable: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param CpuUsageRate: CPU利用率
        :type CpuUsageRate: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param MemAvailable: 内存可用空间,单位GB
        :type MemAvailable: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        :param DataDiskAvailable: 磁盘可用空间,单位GB
        :type DataDiskAvailable: :class:`tcecloud.mariadb.v20170312.models.MonitorData`
        """
        self.BinlogDiskAvailable = None
        self.CpuUsageRate = None
        self.MemAvailable = None
        self.DataDiskAvailable = None

    def _deserialize(self, params):
        if params.get("BinlogDiskAvailable") is not None:
            self.BinlogDiskAvailable = MonitorData()
            self.BinlogDiskAvailable._deserialize(params.get("BinlogDiskAvailable"))
        if params.get("CpuUsageRate") is not None:
            self.CpuUsageRate = MonitorData()
            self.CpuUsageRate._deserialize(params.get("CpuUsageRate"))
        if params.get("MemAvailable") is not None:
            self.MemAvailable = MonitorData()
            self.MemAvailable._deserialize(params.get("MemAvailable"))
        if params.get("DataDiskAvailable") is not None:
            self.DataDiskAvailable = MonitorData()
            self.DataDiskAvailable._deserialize(params.get("DataDiskAvailable"))


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


class SpecConfigInfo(AbstractModel):
    """实例可售卖规格详细信息，创建实例和扩容实例时 Pid+MemSize 唯一确定一种售卖规格，磁盘大小可用区间为[MinDataDisk,MaxDataDisk]"""

    def __init__(self):
        """
        :param Machine: 设备型号
        :type Machine: str
        :param Memory: 内存大小，单位 GB
        :type Memory: int
        :param MinStorage: 数据盘规格最小值，单位 GB
        :type MinStorage: int
        :param MaxStorage: 数据盘规格最大值，单位 GB
        :type MaxStorage: int
        :param SuitInfo: 推荐的使用场景
        :type SuitInfo: str
        :param Qps: 最大 Qps 值
        :type Qps: int
        :param Pid: 产品类型 Id
        :type Pid: int
        :param NodeCount: 节点个数，2 表示一主一从，3 表示一主二从
        :type NodeCount: int
        """
        self.Machine = None
        self.Memory = None
        self.MinStorage = None
        self.MaxStorage = None
        self.SuitInfo = None
        self.Qps = None
        self.Pid = None
        self.Cpu = None
        self.NodeCount = None

    def _deserialize(self, params):
        self.Machine = params.get("Machine")
        self.Memory = params.get("Memory")
        self.MinStorage = params.get("MinStorage")
        self.MaxStorage = params.get("MaxStorage")
        self.SuitInfo = params.get("SuitInfo")
        self.Qps = params.get("Qps")
        self.Pid = params.get("Pid")
        self.Cpu = params.get("Cpu")
        self.NodeCount = params.get("NodeCount")


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
        """
        self.InstanceId = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")


class StartSmartDBAResponse(AbstractModel):
    """StartSmartDBA返回参数结构体"""

    def __init__(self):
        """
        :param FlowId: 异步任务ID，调用DescribeFlow查询任务状态
        :type FlowId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class SwitchDBInstanceHARequest(AbstractModel):
    """SwitchDBInstanceHA请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例Id，形如 tdsql-ow728lmc
        :type InstanceId: str
        :param Zone: 切换的目标区域，会自动选择该可用区中延迟最低的节点
        :type Zone: str
        """
        self.InstanceId = None
        self.Zone = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Zone = params.get("Zone")


class SwitchDBInstanceHAResponse(AbstractModel):
    """SwitchDBInstanceHA返回参数结构体"""

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


class SwitchRollbackInstanceRequest(AbstractModel):
    """SwitchRollbackInstance请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 源/旧实例ID，形如：tdsql-ow728lmc。
        :type InstanceId: str
        :param DstInstanceId: 目标实例ID，形如：tdsql-ow728lmc。
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


class SyncDbInfo(AbstractModel):
    """多源同步详情"""

    def __init__(self):
        """
        :param OrgInfo: 同步源信息
        :type OrgInfo: str
        :param DstInfo: 同步目标信息
        :type DstInfo: str
        """
        self.OrgInfo = None
        self.DstInfo = None

    def _deserialize(self, params):
        self.OrgInfo = params.get("OrgInfo")
        self.DstInfo = params.get("DstInfo")


class SyncTaskInfo(AbstractModel):
    """多源同步任务"""

    def __init__(self):
        """
                :param Id: Id
                :type Id: int
                :param TaskId: 任务Id
                :type TaskId: int
                :param Status: 任务状态，0：初始化中，1：启动中，2：执行过程中，3：错误，重试中， 4：任务被停止，5：执行失败
                :type Status: int
                :param TaskName: 任务名称
                :type TaskName: str
                :param SyncTime: 同步时间
                :type SyncTime: str
                :param CreateTime: 任务创建时间
                :type CreateTime: str
                :param Delay: 同步延时
                :type Delay: int
                :param SrcInstanceId: 源实例id，形如：tdsql-ow728lmc
                :type SrcInstanceId: str
                :param DstInstanceId: 目标实例id，形如：tdsql-ow728lmc
                :type DstInstanceId: str
                :param IsPaused: 是否被终止，0：没有，1：终止
                :type IsPaused: str
                :param Pause: 终止描述
                :type Pause: str
                :param Description: 任务描述
                :type Description: str
                :param MsgCount: 信息次数
                :type MsgCount: str
                :param UpdateCount: 更新次数
                :type UpdateCount: str
                :param Db: 库名称
                :type Db: str
                :param Table: 表名称
                :type Table: str
                :param SyncInfo: 同步信息
                :type SyncInfo: str
                :param SyncDbInfoSet: 同步规则列表
                :type SyncDbInfoSet: list of SyncDbInfo
                :param DstInstanceType: 目标实例类型
                :type DstInstanceType: str
                :param RegexAble: 匹配模式
                :type RegexAble: str
                :param SrcInstanceType: 源实例类型，取值为mariadb或者dcdb
                :type SrcInstanceType: str
                :param TopicName: 当同步类型为ckafka时，表示目标ckafka的topic名称
                :type TopicName: str
                :param DstAccessType: 同步任务的目标实例的接入类型。目前可选值有cdb和dcg。cdb-表示云上的实例；dcg-表示目标实例通过专线接入
                :type DstAccessType: str
                :param DstExtraInfo: 表示目标实例的一些额外信息。比如如果目标实例是通过专线接入的话，关于专线的一些信息就放在DstExtraInfo中。
        注意：此字段可能返回 null，表示取不到有效值。
                :type DstExtraInfo: :class:`tcecloud.mariadb.v20170312.models.DstExtraInfo`
        """
        self.Id = None
        self.TaskId = None
        self.Status = None
        self.TaskName = None
        self.SyncTime = None
        self.CreateTime = None
        self.Delay = None
        self.SrcInstanceId = None
        self.DstInstanceId = None
        self.IsPaused = None
        self.Pause = None
        self.Description = None
        self.MsgCount = None
        self.UpdateCount = None
        self.Db = None
        self.Table = None
        self.SyncInfo = None
        self.SyncDbInfoSet = None
        self.DstInstanceType = None
        self.RegexAble = None
        self.SrcInstanceType = None
        self.TopicName = None
        self.DstAccessType = None
        self.DstExtraInfo = None

    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.TaskId = params.get("TaskId")
        self.Status = params.get("Status")
        self.TaskName = params.get("TaskName")
        self.SyncTime = params.get("SyncTime")
        self.CreateTime = params.get("CreateTime")
        self.Delay = params.get("Delay")
        self.SrcInstanceId = params.get("SrcInstanceId")
        self.DstInstanceId = params.get("DstInstanceId")
        self.IsPaused = params.get("IsPaused")
        self.Pause = params.get("Pause")
        self.Description = params.get("Description")
        self.MsgCount = params.get("MsgCount")
        self.UpdateCount = params.get("UpdateCount")
        self.Db = params.get("Db")
        self.Table = params.get("Table")
        self.SyncInfo = params.get("SyncInfo")
        if params.get("SyncDbInfoSet") is not None:
            self.SyncDbInfoSet = []
            for item in params.get("SyncDbInfoSet"):
                obj = SyncDbInfo()
                obj._deserialize(item)
                self.SyncDbInfoSet.append(obj)
        self.DstInstanceType = params.get("DstInstanceType")
        self.RegexAble = params.get("RegexAble")
        self.SrcInstanceType = params.get("SrcInstanceType")
        self.TopicName = params.get("TopicName")
        self.DstAccessType = params.get("DstAccessType")
        if params.get("DstExtraInfo") is not None:
            self.DstExtraInfo = DstExtraInfo()
            self.DstExtraInfo._deserialize(params.get("DstExtraInfo"))


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


class TemplateConstraintRange(AbstractModel):
    """参数模板中数值型参数的范围约束"""

    def __init__(self):
        """
        :param Min: 约束范围最小值
        :type Min: str
        :param Max: 约束范围最大值
        :type Max: str
        """
        self.Min = None
        self.Max = None

    def _deserialize(self, params):
        self.Min = params.get("Min")
        self.Max = params.get("Max")


class TemplateParam(AbstractModel):
    """参数模板参数"""

    def __init__(self):
        """
        :param Param: 参数名
        :type Param: str
        :param Value: 参数值
        :type Value: str
        :param Default: 参数默认值
        :type Default: str
        :param Constraint: 参数约束条件
        :type Constraint: :class:`tcecloud.mariadb.v20170312.models.TemplateParamConstraint`
        """
        self.Param = None
        self.Value = None
        self.Default = None
        self.Constraint = None

    def _deserialize(self, params):
        self.Param = params.get("Param")
        self.Value = params.get("Value")
        self.Default = params.get("Default")
        if params.get("Constraint") is not None:
            self.Constraint = TemplateParamConstraint()
            self.Constraint._deserialize(params.get("Constraint"))


class TemplateParamConstraint(AbstractModel):
    """参数模板参数约束条件"""

    def __init__(self):
        """
                :param Type: 约束类型
                :type Type: str
                :param Range: 约束范围
        注意：此字段可能返回 null，表示取不到有效值。
                :type Range: :class:`tcecloud.mariadb.v20170312.models.TemplateConstraintRange`
                :param Enum: 约束枚举
                :type Enum: str
                :param Str: 约束字符串
                :type Str: str
        """
        self.Type = None
        self.Range = None
        self.Enum = None
        self.Str = None

    def _deserialize(self, params):
        self.Type = params.get("Type")
        if params.get("Range") is not None:
            self.Range = TemplateConstraintRange()
            self.Range._deserialize(params.get("Range"))
        self.Enum = params.get("Enum")
        self.Str = params.get("Str")


class TerminateDedicatedDBInstanceRequest(AbstractModel):
    """TerminateDedicatedDBInstance请求参数结构体"""

    def __init__(self):
        """
        :param InstanceId: 实例 Id，形如：tdsql-ow728lmc。
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
        注意：此字段可能返回 null，表示取不到有效值。
                :type AppId: int
                :param CreateTime: 创建时间
        注意：此字段可能返回 null，表示取不到有效值。
                :type CreateTime: str
                :param InstanceRemark: 实例备注
        注意：此字段可能返回 null，表示取不到有效值。
                :type InstanceRemark: str
                :param TempType: 0:非临时实例 ,1:无效临时实例, 2:回档成功的有效临时实例
        注意：此字段可能返回 null，表示取不到有效值。
                :type TempType: int
                :param Status: 实例状态,0:待初始化,1:流程处理中,2:有效状态,-1:已隔离，-2：已下线
        注意：此字段可能返回 null，表示取不到有效值。
                :type Status: int
                :param InstanceId: 实例 ID，形如：tdsql-ow728lmc。
        注意：此字段可能返回 null，表示取不到有效值。
                :type InstanceId: str
                :param Vip: 实例虚IP
        注意：此字段可能返回 null，表示取不到有效值。
                :type Vip: str
                :param Vport: 实例虚端口
        注意：此字段可能返回 null，表示取不到有效值。
                :type Vport: int
                :param PeriodEndTime: 有效期结束时间
        注意：此字段可能返回 null，表示取不到有效值。
                :type PeriodEndTime: str
                :param SrcInstanceId: 源实例 ID，形如：tdsql-ow728lmc。
        注意：此字段可能返回 null，表示取不到有效值。
                :type SrcInstanceId: str
                :param StatusDesc: 实例状态描述
        注意：此字段可能返回 null，表示取不到有效值。
                :type StatusDesc: str
                :param Region: 实例所在地域
        注意：此字段可能返回 null，表示取不到有效值。
                :type Region: str
                :param Zone: 实例所在可用区
        注意：此字段可能返回 null，表示取不到有效值。
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


class UpgradeDBInstanceRequest(AbstractModel):
    """UpgradeDBInstance请求参数结构体"""

    def __init__(self):
        """
               :param InstanceId: 待升级的实例ID。形如：tdsql-ow728lmc，可以通过 DescribeDBInstances 查询实例详情获得。
               :type InstanceId: str
               :param Memory: 内存大小，单位：GB，可以通过 DescribeDBInstanceSpecs
        查询实例规格获得。
               :type Memory: int
               :param Storage: 存储空间大小，单位：GB，可以通过 DescribeDBInstanceSpecs
        查询实例规格获得不同内存大小对应的磁盘规格下限和上限。
               :type Storage: int
               :param AutoVoucher: 是否自动使用代金券进行支付，默认不使用。
               :type AutoVoucher: bool
               :param VoucherIds: 代金券ID列表，目前仅支持指定一张代金券。
               :type VoucherIds: list of str
        """
        self.InstanceId = None
        self.Memory = None
        self.Storage = None
        self.AutoVoucher = None
        self.VoucherIds = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Memory = params.get("Memory")
        self.Storage = params.get("Storage")
        self.AutoVoucher = params.get("AutoVoucher")
        self.VoucherIds = params.get("VoucherIds")


class UpgradeDBInstanceResponse(AbstractModel):
    """UpgradeDBInstance返回参数结构体"""

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


class UpgradeDedicatedDBInstanceRequest(AbstractModel):
    """UpgradeDedicatedDBInstance请求参数结构体"""

    def __init__(self):
        """
               :param InstanceId: 待升级的实例ID。形如：tdsql-ow728lmc，可以通过 DescribeDBInstances 查询实例获得。
               :type InstanceId: str
               :param Memory: 内存大小，单位：GB，可以通过 DescribeFenceDBInstanceSpecs
        查询实例规格获得。
               :type Memory: int
               :param Storage: 存储空间大小，单位：GB，可以通过 DescribeFenceDBInstanceSpecs
        查询实例规格获得不同内存大小对应的磁盘规格下限和上限。
               :type Storage: int
        """
        self.InstanceId = None
        self.Memory = None
        self.Storage = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Memory = params.get("Memory")
        self.Storage = params.get("Storage")


class UpgradeDedicatedDBInstanceResponse(AbstractModel):
    """UpgradeDedicatedDBInstance返回参数结构体"""

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


class UpgradeHourDBInstanceRequest(AbstractModel):
    """UpgradeHourDBInstance请求参数结构体"""

    def __init__(self):
        """
        :param Memory: 升级后实例的内存，单位GB，其值不能小于当前实例的内存大小。
        :type Memory: int
        :param Storage: 升级后实例的磁盘大小，单位GB，其值不能小于当前实例的磁盘大小。
        :type Storage: int
        :param InstanceId: 实例ID，形如tdsql-o0q206pq。
        :type InstanceId: str
        :param NodeCount: 当前实例节点个数。NodeCount为2表示一主一从，为3表示一主两从。
        :type NodeCount: int
        :param Cpu: 升级后实例的cpu大小， 单位核，其值不能小于当前实例的cpu
        :type Cpu: int
        :param SwitchStartTime: 切换开始时间，格式如: "2019-12-12 07:00:00"。开始时间必须在当前时间一个小时以后，3天以内。
        :type SwitchStartTime: str
        :param SwitchEndTime: 切换结束时间,  格式如: "2019-12-12 07:15:00"，结束时间必须大于开始时间。
        :type SwitchEndTime: str
        :param SwitchAutoRetry: 是否自动重试。 0：不自动重试  1：自动重试
        :type SwitchAutoRetry: int
        """
        self.Memory = None
        self.Storage = None
        self.InstanceId = None
        self.NodeCount = None
        self.Cpu = None
        self.SwitchStartTime = None
        self.SwitchEndTime = None
        self.SwitchAutoRetry = None

    def _deserialize(self, params):
        self.Memory = params.get("Memory")
        self.Storage = params.get("Storage")
        self.InstanceId = params.get("InstanceId")
        self.NodeCount = params.get("NodeCount")
        self.Cpu = params.get("Cpu")
        self.SwitchStartTime = params.get("SwitchStartTime")
        self.SwitchEndTime = params.get("SwitchEndTime")
        self.SwitchAutoRetry = params.get("SwitchAutoRetry")


class UpgradeHourDBInstanceResponse(AbstractModel):
    """UpgradeHourDBInstance返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ZoneChooseInfo(AbstractModel):
    """分片节点可用区选择"""

    def __init__(self):
        """
        :param MasterZone: 主可用区
        :type MasterZone: :class:`tcecloud.mariadb.v20170312.models.ZonesInfo`
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

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


class AddConvergence(AbstractModel):
    """告警收敛添加"""

    def __init__(self):
        """
        :param Status: 状态
        :type Status: str
        :param Message: 返回信息
        :type Message: str
        :param ConvId: 告警收敛id
        :type ConvId: str
        """
        self.Status = None
        self.Message = None
        self.ConvId = None

    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.Message = params.get("Message")
        self.ConvId = params.get("ConvId")


class AddConvergenceRequest(AbstractModel):
    """AddConvergence请求参数结构体"""

    def __init__(self):
        """
        :param TopicId: 无
        :type TopicId: str
        :param Data: 无
        :type Data: :class:`tcecloud.amp.v20190911.models.Conv`
        """
        self.TopicId = None
        self.Data = None

    def _deserialize(self, params):
        self.TopicId = params.get("TopicId")
        if params.get("Data") is not None:
            self.Data = Conv()
            self.Data._deserialize(params.get("Data"))


class AddConvergenceResponse(AbstractModel):
    """AddConvergence返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.AddConvergence`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = AddConvergence()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class AddHandle(AbstractModel):
    """告警处理添加"""

    def __init__(self):
        """
        :param HandleId: 告警处理id
        :type HandleId: str
        :param Status: 状态
        :type Status: str
        :param Message: 返回信息
        :type Message: str
        """
        self.HandleId = None
        self.Status = None
        self.Message = None

    def _deserialize(self, params):
        self.HandleId = params.get("HandleId")
        self.Status = params.get("Status")
        self.Message = params.get("Message")


class AddHandleRequest(AbstractModel):
    """AddHandle请求参数结构体"""

    def __init__(self):
        """
        :param TopicId: 无
        :type TopicId: str
        :param Data: 无
        :type Data: :class:`tcecloud.amp.v20190911.models.Handle`
        """
        self.TopicId = None
        self.Data = None

    def _deserialize(self, params):
        self.TopicId = params.get("TopicId")
        if params.get("Data") is not None:
            self.Data = Handle()
            self.Data._deserialize(params.get("Data"))


class AddHandleResponse(AbstractModel):
    """AddHandle返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.AddHandle`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = AddHandle()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class AddShield(AbstractModel):
    """增加屏蔽"""

    def __init__(self):
        """
        :param Status: 状态
        :type Status: str
        :param Message: 返回信息
        :type Message: str
        :param ShieldId: 屏蔽id
        :type ShieldId: str
        """
        self.Status = None
        self.Message = None
        self.ShieldId = None

    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.Message = params.get("Message")
        self.ShieldId = params.get("ShieldId")


class AddShieldRequest(AbstractModel):
    """AddShield请求参数结构体"""

    def __init__(self):
        """
        :param TopicId: 无
        :type TopicId: str
        :param Data: 无
        :type Data: :class:`tcecloud.amp.v20190911.models.Shield`
        """
        self.TopicId = None
        self.Data = None

    def _deserialize(self, params):
        self.TopicId = params.get("TopicId")
        if params.get("Data") is not None:
            self.Data = Shield()
            self.Data._deserialize(params.get("Data"))


class AddShieldResponse(AbstractModel):
    """AddShield返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.AddShield`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = AddShield()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class AddSub(AbstractModel):
    """增加订阅"""

    def __init__(self):
        """
        :param Status: 状态
        :type Status: str
        :param Message: 信息
        :type Message: str
        :param SubsId: 告警订阅id
        :type SubsId: str
        """
        self.Status = None
        self.Message = None
        self.SubsId = None

    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.Message = params.get("Message")
        self.SubsId = params.get("SubsId")


class AddSubRequest(AbstractModel):
    """AddSub请求参数结构体"""

    def __init__(self):
        """
        :param TopicId: 告警源id
        :type TopicId: str
        :param Data: 订阅信息
        :type Data: :class:`tcecloud.amp.v20190911.models.Subs`
        """
        self.TopicId = None
        self.Data = None

    def _deserialize(self, params):
        self.TopicId = params.get("TopicId")
        if params.get("Data") is not None:
            self.Data = Subs()
            self.Data._deserialize(params.get("Data"))


class AddSubResponse(AbstractModel):
    """AddSub返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.AddSub`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = AddSub()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class AddTopic(AbstractModel):
    """创建告警源"""

    def __init__(self):
        """
        :param Status: 状态
        :type Status: str
        :param Message: 返回信息
        :type Message: str
        :param TopicId: 告警源id
        :type TopicId: str
        """
        self.Status = None
        self.Message = None
        self.TopicId = None

    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.Message = params.get("Message")
        self.TopicId = params.get("TopicId")


class AddTopicRequest(AbstractModel):
    """AddTopic请求参数结构体"""

    def __init__(self):
        """
        :param Data: 告警源信息
        :type Data: :class:`tcecloud.amp.v20190911.models.Topic`
        """
        self.Data = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = Topic()
            self.Data._deserialize(params.get("Data"))


class AddTopicResponse(AbstractModel):
    """AddTopic返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.AddTopic`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = AddTopic()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class AlertField(AbstractModel):
    """自定义告警内容"""

    def __init__(self):
        """
        :param Key: 自定义告警字段
        :type Key: str
        :param Value: 自定义告警值
        :type Value: str
        """
        self.Key = None
        self.Value = None

    def _deserialize(self, params):
        self.Key = params.get("Key")
        self.Value = params.get("Value")


class ConfigHistory(AbstractModel):
    """日志"""

    def __init__(self):
        """
        :param Id: id
        :type Id: str
        :param AppId: 开发者账号
        :type AppId: int
        :param TopicId: 告警源id
        :type TopicId: str
        :param OwnerUin: 主账号uin
        :type OwnerUin: int
        :param SubUin: 子账户uin
        :type SubUin: int
        :param RequestId: 请求id
        :type RequestId: str
        :param EditTime: 编辑时间戳
        :type EditTime: int
        :param EditType: 编辑类型
        :type EditType: str
        :param EditItem: 编辑内容
        :type EditItem: str
        :param BeforeEdit: 编辑开始前
        :type BeforeEdit: str
        :param AfterEdit: 编辑开始后
        :type AfterEdit: str
        """
        self.Id = None
        self.AppId = None
        self.TopicId = None
        self.OwnerUin = None
        self.SubUin = None
        self.RequestId = None
        self.EditTime = None
        self.EditType = None
        self.EditItem = None
        self.BeforeEdit = None
        self.AfterEdit = None

    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.AppId = params.get("AppId")
        self.TopicId = params.get("TopicId")
        self.OwnerUin = params.get("OwnerUin")
        self.SubUin = params.get("SubUin")
        self.RequestId = params.get("RequestId")
        self.EditTime = params.get("EditTime")
        self.EditType = params.get("EditType")
        self.EditItem = params.get("EditItem")
        self.BeforeEdit = params.get("BeforeEdit")
        self.AfterEdit = params.get("AfterEdit")


class Conv(AbstractModel):
    """告警收敛规则"""

    def __init__(self):
        """
        :param TopicId: 告警源ID
        :type TopicId: str
        :param ConvName: 收敛规则名
        :type ConvName: str
        :param ConvId: 收敛规则ID 更新必填
        :type ConvId: str
        :param ConvRules: 屏蔽条件
        :type ConvRules: list of JudgeRules
        :param ConvPeriod: 收敛时长
        :type ConvPeriod: int
        :param ConvCounts: 最大收敛数
        :type ConvCounts: int
        :param AppId: 开发者帐号
        :type AppId: int
        :param OwnerUin: 告警订阅创建者uin
        :type OwnerUin: int
        :param LastEditUin: 最后更新订阅的uin
        :type LastEditUin: int
        :param UpdateTime: 最后更新时间戳
        :type UpdateTime: int
        :param InsertTime: 插入时间戳
        :type InsertTime: int
        :param ConvRulesDimension: 收敛维度
        :type ConvRulesDimension: str
        """
        self.TopicId = None
        self.ConvName = None
        self.ConvId = None
        self.ConvRules = None
        self.ConvPeriod = None
        self.ConvCounts = None
        self.AppId = None
        self.OwnerUin = None
        self.LastEditUin = None
        self.UpdateTime = None
        self.InsertTime = None
        self.ConvRulesDimension = None

    def _deserialize(self, params):
        self.TopicId = params.get("TopicId")
        self.ConvName = params.get("ConvName")
        self.ConvId = params.get("ConvId")
        if params.get("ConvRules") is not None:
            self.ConvRules = []
            for item in params.get("ConvRules"):
                obj = JudgeRules()
                obj._deserialize(item)
                self.ConvRules.append(obj)
        self.ConvPeriod = params.get("ConvPeriod")
        self.ConvCounts = params.get("ConvCounts")
        self.AppId = params.get("AppId")
        self.OwnerUin = params.get("OwnerUin")
        self.LastEditUin = params.get("LastEditUin")
        self.UpdateTime = params.get("UpdateTime")
        self.InsertTime = params.get("InsertTime")
        self.ConvRulesDimension = params.get("ConvRulesDimension")


class DeleteConvergencesRequest(AbstractModel):
    """DeleteConvergences请求参数结构体"""

    def __init__(self):
        """
        :param TopicId: 告警源id
        :type TopicId: str
        :param ConvIds: 收敛规则id
        :type ConvIds: list of str
        """
        self.TopicId = None
        self.ConvIds = None

    def _deserialize(self, params):
        self.TopicId = params.get("TopicId")
        self.ConvIds = params.get("ConvIds")


class DeleteConvergencesResponse(AbstractModel):
    """DeleteConvergences返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.UpdateOrDelReturn`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = UpdateOrDelReturn()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DeleteHandlesRequest(AbstractModel):
    """DeleteHandles请求参数结构体"""

    def __init__(self):
        """
        :param TopicId: 无
        :type TopicId: str
        :param HandleIds: 无
        :type HandleIds: list of str
        """
        self.TopicId = None
        self.HandleIds = None

    def _deserialize(self, params):
        self.TopicId = params.get("TopicId")
        self.HandleIds = params.get("HandleIds")


class DeleteHandlesResponse(AbstractModel):
    """DeleteHandles返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.UpdateOrDelReturn`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = UpdateOrDelReturn()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DeleteShieldsRequest(AbstractModel):
    """DeleteShields请求参数结构体"""

    def __init__(self):
        """
        :param TopicId: 告警源id
        :type TopicId: str
        :param ShieldIds: 屏蔽规则id
        :type ShieldIds: list of str
        """
        self.TopicId = None
        self.ShieldIds = None

    def _deserialize(self, params):
        self.TopicId = params.get("TopicId")
        self.ShieldIds = params.get("ShieldIds")


class DeleteShieldsResponse(AbstractModel):
    """DeleteShields返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.UpdateOrDelReturn`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = UpdateOrDelReturn()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DeleteSubsRequest(AbstractModel):
    """DeleteSubs请求参数结构体"""

    def __init__(self):
        """
        :param SubsIds: 订阅规则id
        :type SubsIds: list of str
        """
        self.SubsIds = None

    def _deserialize(self, params):
        self.SubsIds = params.get("SubsIds")


class DeleteSubsResponse(AbstractModel):
    """DeleteSubs返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.UpdateOrDelReturn`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = UpdateOrDelReturn()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DeleteTopicsRequest(AbstractModel):
    """DeleteTopics请求参数结构体"""

    def __init__(self):
        """
        :param TopicIds: 告警源id数组
        :type TopicIds: list of str
        """
        self.TopicIds = None

    def _deserialize(self, params):
        self.TopicIds = params.get("TopicIds")


class DeleteTopicsResponse(AbstractModel):
    """DeleteTopics返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.UpdateOrDelReturn`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = UpdateOrDelReturn()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class Field(AbstractModel):
    """自定义参数信息"""

    def __init__(self):
        """
        :param Key: 参数字段
        :type Key: str
        :param Type: 字段类型:string字符型  number数字型
        :type Type: str
        :param Name: 参数字段名
        :type Name: str
        :param Default: 默认值
        :type Default: str
        """
        self.Key = None
        self.Type = None
        self.Name = None
        self.Default = None

    def _deserialize(self, params):
        self.Key = params.get("Key")
        self.Type = params.get("Type")
        self.Name = params.get("Name")
        self.Default = params.get("Default")


class FieldNew(AbstractModel):
    """自定义参数信息"""

    def __init__(self):
        """
        :param Key: 参数字段
        :type Key: str
        :param Type: 字段类型:string字符型  number数字型
        :type Type: str
        :param Name: 参数字段名
        :type Name: str
        :param Default: 默认值
        :type Default: str
        :param IsDefault: 是否为默认
        :type IsDefault: bool
        """
        self.Key = None
        self.Type = None
        self.Name = None
        self.Default = None
        self.IsDefault = None

    def _deserialize(self, params):
        self.Key = params.get("Key")
        self.Type = params.get("Type")
        self.Name = params.get("Name")
        self.Default = params.get("Default")
        self.IsDefault = params.get("IsDefault")


class GetAlertHistory(AbstractModel):
    """获取告警历史"""

    def __init__(self):
        """
        :param Histories: 告警历史
        :type Histories: list of History
        :param Columns: 自定义字段
        :type Columns: list of FieldNew
        :param Total: 总数
        :type Total: int
        """
        self.Histories = None
        self.Columns = None
        self.Total = None

    def _deserialize(self, params):
        if params.get("Histories") is not None:
            self.Histories = []
            for item in params.get("Histories"):
                obj = History()
                obj._deserialize(item)
                self.Histories.append(obj)
        if params.get("Columns") is not None:
            self.Columns = []
            for item in params.get("Columns"):
                obj = FieldNew()
                obj._deserialize(item)
                self.Columns.append(obj)
        self.Total = params.get("Total")


class GetAlertHistoryById(AbstractModel):
    """获取单条告警历史"""

    def __init__(self):
        """
        :param History: 告警历史
        :type History: :class:`tcecloud.amp.v20190911.models.History`
        :param Columns: 自定义告警字段
        :type Columns: list of FieldNew
        """
        self.History = None
        self.Columns = None

    def _deserialize(self, params):
        if params.get("History") is not None:
            self.History = History()
            self.History._deserialize(params.get("History"))
        if params.get("Columns") is not None:
            self.Columns = []
            for item in params.get("Columns"):
                obj = FieldNew()
                obj._deserialize(item)
                self.Columns.append(obj)


class GetAlertHistoryByIdRequest(AbstractModel):
    """GetAlertHistoryById请求参数结构体"""

    def __init__(self):
        """
        :param AlertId: 告警id
        :type AlertId: str
        """
        self.AlertId = None

    def _deserialize(self, params):
        self.AlertId = params.get("AlertId")


class GetAlertHistoryByIdResponse(AbstractModel):
    """GetAlertHistoryById返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.GetAlertHistoryById`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = GetAlertHistoryById()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class GetAlertHistoryRequest(AbstractModel):
    """GetAlertHistory请求参数结构体"""

    def __init__(self):
        """
        :param Offset: 分页需要的偏移量
        :type Offset: int
        :param Limit: 分页中每页的大小
        :type Limit: int
        :param OccurStartTimestamp: 搜索告警发生时间的开始时间戳
        :type OccurStartTimestamp: int
        :param OccurEndTimestamp: 搜索告警发生时间的结束时间戳
        :type OccurEndTimestamp: int
        :param ReceiveStartTimestamp: 搜索告警接收时间的开始时间戳
        :type ReceiveStartTimestamp: int
        :param ReceiveEndTimestamp: 搜索告警接收时间的结束时间戳
        :type ReceiveEndTimestamp: int
        :param Status: 搜索告警的状态限制 all 全部  continue 非连续点 convergence 已收敛 shield 已屏蔽 send 已发送 reserve 无订阅
        :type Status: str
        :param TopicId: 要搜索告警的主题Id
        :type TopicId: str
        :param SearchContent: 全局搜索内容
        :type SearchContent: str
        :param SortKey: 排序字段
        :type SortKey: str
        :param SortOrder: 排序字段顺序
        :type SortOrder: str
        :param SearchKeyValuePairs: 分字段进行告警搜索KV对 例如 [{\"key\":\"alarmStatus\",\"value\":\"告警中\"}]
        :type SearchKeyValuePairs: str
        :param SubId: 告警订阅Id
        :type SubId: str
        """
        self.Offset = None
        self.Limit = None
        self.OccurStartTimestamp = None
        self.OccurEndTimestamp = None
        self.ReceiveStartTimestamp = None
        self.ReceiveEndTimestamp = None
        self.Status = None
        self.TopicId = None
        self.SearchContent = None
        self.SortKey = None
        self.SortOrder = None
        self.SearchKeyValuePairs = None
        self.SubId = None

    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.OccurStartTimestamp = params.get("OccurStartTimestamp")
        self.OccurEndTimestamp = params.get("OccurEndTimestamp")
        self.ReceiveStartTimestamp = params.get("ReceiveStartTimestamp")
        self.ReceiveEndTimestamp = params.get("ReceiveEndTimestamp")
        self.Status = params.get("Status")
        self.TopicId = params.get("TopicId")
        self.SearchContent = params.get("SearchContent")
        self.SortKey = params.get("SortKey")
        self.SortOrder = params.get("SortOrder")
        self.SearchKeyValuePairs = params.get("SearchKeyValuePairs")
        self.SubId = params.get("SubId")


class GetAlertHistoryResponse(AbstractModel):
    """GetAlertHistory返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.GetAlertHistory`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = GetAlertHistory()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class GetConfigHistory(AbstractModel):
    """获取日志历史"""

    def __init__(self):
        """
        :param Histories: 日志历史
        :type Histories: list of ConfigHistory
        :param Total: 总数
        :type Total: int
        """
        self.Histories = None
        self.Total = None

    def _deserialize(self, params):
        if params.get("Histories") is not None:
            self.Histories = []
            for item in params.get("Histories"):
                obj = ConfigHistory()
                obj._deserialize(item)
                self.Histories.append(obj)
        self.Total = params.get("Total")


class GetConfigHistoryRequest(AbstractModel):
    """GetConfigHistory请求参数结构体"""

    def __init__(self):
        """
        :param Offset: 分页需要的偏移量
        :type Offset: int
        :param Limit: 分页中每页的大小
        :type Limit: int
        :param StartTimestamp: 开始时间戳
        :type StartTimestamp: int
        :param EndTimestamp: 结束时间戳
        :type EndTimestamp: int
        :param TopicId: 要搜索告警源Id
        :type TopicId: str
        :param ModifyType: 搜索类型 all create  update delete
        :type ModifyType: str
        :param SortKey: 排序字段
        :type SortKey: str
        :param SortOrder: 排序字段顺序
        :type SortOrder: str
        """
        self.Offset = None
        self.Limit = None
        self.StartTimestamp = None
        self.EndTimestamp = None
        self.TopicId = None
        self.ModifyType = None
        self.SortKey = None
        self.SortOrder = None

    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.StartTimestamp = params.get("StartTimestamp")
        self.EndTimestamp = params.get("EndTimestamp")
        self.TopicId = params.get("TopicId")
        self.ModifyType = params.get("ModifyType")
        self.SortKey = params.get("SortKey")
        self.SortOrder = params.get("SortOrder")


class GetConfigHistoryResponse(AbstractModel):
    """GetConfigHistory返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.GetConfigHistory`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = GetConfigHistory()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class GetConvergence(AbstractModel):
    """收敛规则"""

    def __init__(self):
        """
        :param Convs: 收敛规则信息
        :type Convs: :class:`tcecloud.amp.v20190911.models.Conv`
        """
        self.Convs = None

    def _deserialize(self, params):
        if params.get("Convs") is not None:
            self.Convs = Conv()
            self.Convs._deserialize(params.get("Convs"))


class GetConvergenceRequest(AbstractModel):
    """GetConvergence请求参数结构体"""

    def __init__(self):
        """
        :param ConvId: 无
        :type ConvId: str
        """
        self.ConvId = None

    def _deserialize(self, params):
        self.ConvId = params.get("ConvId")


class GetConvergenceResponse(AbstractModel):
    """GetConvergence返回参数结构体"""

    def __init__(self):
        """
        :param Data: 无
        :type Data: :class:`tcecloud.amp.v20190911.models.GetConvergence`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = GetConvergence()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class GetConvergences(AbstractModel):
    """告警收敛信息"""

    def __init__(self):
        """
        :param Convs: 告警收敛规则
        :type Convs: list of Conv
        :param Total: 总数
        :type Total: int
        """
        self.Convs = None
        self.Total = None

    def _deserialize(self, params):
        if params.get("Convs") is not None:
            self.Convs = []
            for item in params.get("Convs"):
                obj = Conv()
                obj._deserialize(item)
                self.Convs.append(obj)
        self.Total = params.get("Total")


class GetConvergencesRequest(AbstractModel):
    """GetConvergences请求参数结构体"""

    def __init__(self):
        """
        :param TopicId: 无
        :type TopicId: str
        :param Offset: 无
        :type Offset: int
        :param Limit: 无
        :type Limit: int
        """
        self.TopicId = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.TopicId = params.get("TopicId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class GetConvergencesResponse(AbstractModel):
    """GetConvergences返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.GetConvergences`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = GetConvergences()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class GetHandle(AbstractModel):
    """获取处理规则信息"""

    def __init__(self):
        """
        :param Handle: 处理规则
        :type Handle: :class:`tcecloud.amp.v20190911.models.Handle`
        """
        self.Handle = None

    def _deserialize(self, params):
        if params.get("Handle") is not None:
            self.Handle = Handle()
            self.Handle._deserialize(params.get("Handle"))


class GetHandleRequest(AbstractModel):
    """GetHandle请求参数结构体"""

    def __init__(self):
        """
        :param HandleId: 无
        :type HandleId: str
        """
        self.HandleId = None

    def _deserialize(self, params):
        self.HandleId = params.get("HandleId")


class GetHandleResponse(AbstractModel):
    """GetHandle返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.GetHandle`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = GetHandle()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class GetHandles(AbstractModel):
    """获取处理规则信息"""

    def __init__(self):
        """
        :param Handles: 处理规则信息
        :type Handles: list of Handle
        :param Total: 总数
        :type Total: int
        """
        self.Handles = None
        self.Total = None

    def _deserialize(self, params):
        if params.get("Handles") is not None:
            self.Handles = []
            for item in params.get("Handles"):
                obj = Handle()
                obj._deserialize(item)
                self.Handles.append(obj)
        self.Total = params.get("Total")


class GetHandlesRequest(AbstractModel):
    """GetHandles请求参数结构体"""

    def __init__(self):
        """
        :param Offset: 无
        :type Offset: int
        :param Limit: 无
        :type Limit: int
        :param TopicId: 无
        :type TopicId: str
        """
        self.Offset = None
        self.Limit = None
        self.TopicId = None

    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.TopicId = params.get("TopicId")


class GetHandlesResponse(AbstractModel):
    """GetHandles返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.GetHandles`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = GetHandles()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class GetShield(AbstractModel):
    """屏蔽规则信息"""

    def __init__(self):
        """
        :param Shield: 屏蔽规则信息
        :type Shield: :class:`tcecloud.amp.v20190911.models.Shield`
        """
        self.Shield = None

    def _deserialize(self, params):
        if params.get("Shield") is not None:
            self.Shield = Shield()
            self.Shield._deserialize(params.get("Shield"))


class GetShieldRequest(AbstractModel):
    """GetShield请求参数结构体"""

    def __init__(self):
        """
        :param ShieldId: 无
        :type ShieldId: str
        """
        self.ShieldId = None

    def _deserialize(self, params):
        self.ShieldId = params.get("ShieldId")


class GetShieldResponse(AbstractModel):
    """GetShield返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.GetShield`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = GetShield()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class GetShields(AbstractModel):
    """屏蔽规则信息"""

    def __init__(self):
        """
        :param Shields: 屏蔽规则信息
        :type Shields: list of Shield
        :param Total: 总数
        :type Total: int
        """
        self.Shields = None
        self.Total = None

    def _deserialize(self, params):
        if params.get("Shields") is not None:
            self.Shields = []
            for item in params.get("Shields"):
                obj = Shield()
                obj._deserialize(item)
                self.Shields.append(obj)
        self.Total = params.get("Total")


class GetShieldsRequest(AbstractModel):
    """GetShields请求参数结构体"""

    def __init__(self):
        """
        :param Offset: 无
        :type Offset: int
        :param Limit: 无
        :type Limit: int
        :param TopicId: 无
        :type TopicId: str
        """
        self.Offset = None
        self.Limit = None
        self.TopicId = None

    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.TopicId = params.get("TopicId")


class GetShieldsResponse(AbstractModel):
    """GetShields返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.GetShields`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = GetShields()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class GetSub(AbstractModel):
    """获取订阅"""

    def __init__(self):
        """
        :param Subs: 告警订阅信息
        :type Subs: :class:`tcecloud.amp.v20190911.models.Subs`
        """
        self.Subs = None

    def _deserialize(self, params):
        if params.get("Subs") is not None:
            self.Subs = Subs()
            self.Subs._deserialize(params.get("Subs"))


class GetSubRequest(AbstractModel):
    """GetSub请求参数结构体"""

    def __init__(self):
        """
        :param SubsId: 订阅规则id
        :type SubsId: str
        """
        self.SubsId = None

    def _deserialize(self, params):
        self.SubsId = params.get("SubsId")


class GetSubResponse(AbstractModel):
    """GetSub返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.GetSub`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = GetSub()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class GetSubs(AbstractModel):
    """获取告警订阅信息"""

    def __init__(self):
        """
        :param Subs: 告警订阅信息
        :type Subs: list of Subs
        :param Total: 总数
        :type Total: int
        """
        self.Subs = None
        self.Total = None

    def _deserialize(self, params):
        if params.get("Subs") is not None:
            self.Subs = []
            for item in params.get("Subs"):
                obj = Subs()
                obj._deserialize(item)
                self.Subs.append(obj)
        self.Total = params.get("Total")


class GetSubsRequest(AbstractModel):
    """GetSubs请求参数结构体"""

    def __init__(self):
        """
        :param TopicId: 告警源id
        :type TopicId: str
        :param Offset: 无
        :type Offset: int
        :param Limit: 无
        :type Limit: int
        :param SearchSubsName: 搜索信息
        :type SearchSubsName: str
        """
        self.TopicId = None
        self.Offset = None
        self.Limit = None
        self.SearchSubsName = None

    def _deserialize(self, params):
        self.TopicId = params.get("TopicId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.SearchSubsName = params.get("SearchSubsName")


class GetSubsResponse(AbstractModel):
    """GetSubs返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.GetSubs`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = GetSubs()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class GetTopic(AbstractModel):
    """告警源信息"""

    def __init__(self):
        """
        :param Topic: 告警源信息
        :type Topic: :class:`tcecloud.amp.v20190911.models.Topic`
        """
        self.Topic = None

    def _deserialize(self, params):
        if params.get("Topic") is not None:
            self.Topic = Topic()
            self.Topic._deserialize(params.get("Topic"))


class GetTopicFieldTemplate(AbstractModel):
    """返回信息"""

    def __init__(self):
        """
        :param Columns: 返回信息
        :type Columns: list of FieldNew
        """
        self.Columns = None

    def _deserialize(self, params):
        if params.get("Columns") is not None:
            self.Columns = []
            for item in params.get("Columns"):
                obj = FieldNew()
                obj._deserialize(item)
                self.Columns.append(obj)


class GetTopicFieldTemplateRequest(AbstractModel):
    """GetTopicFieldTemplate请求参数结构体"""

    def __init__(self):
        """
        :param TopicId: 告警源id
        :type TopicId: str
        """
        self.TopicId = None

    def _deserialize(self, params):
        self.TopicId = params.get("TopicId")


class GetTopicFieldTemplateResponse(AbstractModel):
    """GetTopicFieldTemplate返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.GetTopicFieldTemplate`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = GetTopicFieldTemplate()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class GetTopicRequest(AbstractModel):
    """GetTopic请求参数结构体"""

    def __init__(self):
        """
        :param TopicId: 告警源id
        :type TopicId: str
        """
        self.TopicId = None

    def _deserialize(self, params):
        self.TopicId = params.get("TopicId")


class GetTopicResponse(AbstractModel):
    """GetTopic返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.GetTopic`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = GetTopic()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class GetTopics(AbstractModel):
    """获取告警源列表"""

    def __init__(self):
        """
        :param Topics: 告警源数据
        :type Topics: list of Topic
        :param Total: 总数
        :type Total: int
        """
        self.Topics = None
        self.Total = None

    def _deserialize(self, params):
        if params.get("Topics") is not None:
            self.Topics = []
            for item in params.get("Topics"):
                obj = Topic()
                obj._deserialize(item)
                self.Topics.append(obj)
        self.Total = params.get("Total")


class GetTopicsRequest(AbstractModel):
    """GetTopics请求参数结构体"""

    def __init__(self):
        """
        :param Offset: 起始位置0
        :type Offset: int
        :param Limit: 每页限制长度
        :type Limit: int
        :param SearchTopicName: 模糊搜索告警源名称
        :type SearchTopicName: str
        """
        self.Offset = None
        self.Limit = None
        self.SearchTopicName = None

    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.SearchTopicName = params.get("SearchTopicName")


class GetTopicsResponse(AbstractModel):
    """GetTopics返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.GetTopics`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = GetTopics()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class Handle(AbstractModel):
    """处理规则"""

    def __init__(self):
        """
        :param TopicId: 告警源ID
        :type TopicId: str
        :param HandleName: 告警处理名
        :type HandleName: str
        :param HandleJudgeType: 判断条件类型 all / custom
        :type HandleJudgeType: str
        :param HandleActionType: 处理方式 pre / parallel
        :type HandleActionType: str
        :param HandleActionURL: 回调url
        :type HandleActionURL: str
        :param HandleActionPriority: 告警优先级
        :type HandleActionPriority: int
        :param HandleActionCode: 验证码
        :type HandleActionCode: str
        :param HandleId: 告警处理ID 更新必填
        :type HandleId: str
        :param HandleJudgeRules: 告警处理条件
        :type HandleJudgeRules: list of JudgeRules
        :param AppId: 开发者帐号
        :type AppId: int
        :param OwnerUin: 屏蔽规则创建者uin
        :type OwnerUin: int
        :param LastEditUin: 最后更新屏蔽规则的uin
        :type LastEditUin: int
        :param UpdateTime: 最后更新时间戳
        :type UpdateTime: int
        :param InsertTime: 插入时间戳
        :type InsertTime: int
        :param HandleActionVerification: 是否验证
        :type HandleActionVerification: int
        """
        self.TopicId = None
        self.HandleName = None
        self.HandleJudgeType = None
        self.HandleActionType = None
        self.HandleActionURL = None
        self.HandleActionPriority = None
        self.HandleActionCode = None
        self.HandleId = None
        self.HandleJudgeRules = None
        self.AppId = None
        self.OwnerUin = None
        self.LastEditUin = None
        self.UpdateTime = None
        self.InsertTime = None
        self.HandleActionVerification = None

    def _deserialize(self, params):
        self.TopicId = params.get("TopicId")
        self.HandleName = params.get("HandleName")
        self.HandleJudgeType = params.get("HandleJudgeType")
        self.HandleActionType = params.get("HandleActionType")
        self.HandleActionURL = params.get("HandleActionURL")
        self.HandleActionPriority = params.get("HandleActionPriority")
        self.HandleActionCode = params.get("HandleActionCode")
        self.HandleId = params.get("HandleId")
        if params.get("HandleJudgeRules") is not None:
            self.HandleJudgeRules = []
            for item in params.get("HandleJudgeRules"):
                obj = JudgeRules()
                obj._deserialize(item)
                self.HandleJudgeRules.append(obj)
        self.AppId = params.get("AppId")
        self.OwnerUin = params.get("OwnerUin")
        self.LastEditUin = params.get("LastEditUin")
        self.UpdateTime = params.get("UpdateTime")
        self.InsertTime = params.get("InsertTime")
        self.HandleActionVerification = params.get("HandleActionVerification")


class History(AbstractModel):
    """告警内容"""

    def __init__(self):
        """
        :param TopicId: 告警源id
        :type TopicId: str
        :param TopicName: 告警源名称
        :type TopicName: str
        :param OwnerUin: 主账号uin
        :type OwnerUin: int
        :param SubUin: 子账号uin
        :type SubUin: int
        :param RequestId: 告警id
        :type RequestId: str
        :param OccurTime: 发生时间
        :type OccurTime: int
        :param ReceiveTime: 接收时间
        :type ReceiveTime: int
        :param Status: 告警状态
        :type Status: str
        :param ReceiverGroups: 接收组
        :type ReceiverGroups: list of int
        :param NotifyWays: 发送方式
        :type NotifyWays: list of str
        :param AlertField: 自定义字段
        :type AlertField: list of AlertField
        :param PolicyName: 策略名称
        :type PolicyName: str
        """
        self.TopicId = None
        self.TopicName = None
        self.OwnerUin = None
        self.SubUin = None
        self.RequestId = None
        self.OccurTime = None
        self.ReceiveTime = None
        self.Status = None
        self.ReceiverGroups = None
        self.NotifyWays = None
        self.AlertField = None
        self.PolicyName = None

    def _deserialize(self, params):
        self.TopicId = params.get("TopicId")
        self.TopicName = params.get("TopicName")
        self.OwnerUin = params.get("OwnerUin")
        self.SubUin = params.get("SubUin")
        self.RequestId = params.get("RequestId")
        self.OccurTime = params.get("OccurTime")
        self.ReceiveTime = params.get("ReceiveTime")
        self.Status = params.get("Status")
        self.ReceiverGroups = params.get("ReceiverGroups")
        self.NotifyWays = params.get("NotifyWays")
        if params.get("AlertField") is not None:
            self.AlertField = []
            for item in params.get("AlertField"):
                obj = AlertField()
                obj._deserialize(item)
                self.AlertField.append(obj)
        self.PolicyName = params.get("PolicyName")


class Inform(AbstractModel):
    """告警通道模板"""

    def __init__(self):
        """
        :param SMS: 短信通道告警模板
        :type SMS: :class:`tcecloud.amp.v20190911.models.InformTmp`
        :param CALL: 语音通知通道告警模板
        :type CALL: :class:`tcecloud.amp.v20190911.models.InformTmp`
        :param EMAIL: 电子邮件通道告警模板
        :type EMAIL: :class:`tcecloud.amp.v20190911.models.InformTmp`
        :param WECHAT: 微信通道告警模板
        :type WECHAT: :class:`tcecloud.amp.v20190911.models.InformTmp`
        """
        self.SMS = None
        self.CALL = None
        self.EMAIL = None
        self.WECHAT = None

    def _deserialize(self, params):
        if params.get("SMS") is not None:
            self.SMS = InformTmp()
            self.SMS._deserialize(params.get("SMS"))
        if params.get("CALL") is not None:
            self.CALL = InformTmp()
            self.CALL._deserialize(params.get("CALL"))
        if params.get("EMAIL") is not None:
            self.EMAIL = InformTmp()
            self.EMAIL._deserialize(params.get("EMAIL"))
        if params.get("WECHAT") is not None:
            self.WECHAT = InformTmp()
            self.WECHAT._deserialize(params.get("WECHAT"))


class InformTmp(AbstractModel):
    """告警模板"""

    def __init__(self):
        """
        :param Enable: 是否启用该模板
        :type Enable: bool
        :param Title: 告警模板标题
        :type Title: str
        :param Template: 告警模板
        :type Template: str
        :param Rules: 告警模板匹配规则
        :type Rules: list of JudgeRules
        """
        self.Enable = None
        self.Title = None
        self.Template = None
        self.Rules = None

    def _deserialize(self, params):
        self.Enable = params.get("Enable")
        self.Title = params.get("Title")
        self.Template = params.get("Template")
        if params.get("Rules") is not None:
            self.Rules = []
            for item in params.get("Rules"):
                obj = JudgeRules()
                obj._deserialize(item)
                self.Rules.append(obj)


class JudgeRules(AbstractModel):
    """规则信息"""

    def __init__(self):
        """
        :param Key: 自定义参数
        :type Key: str
        :param Type: 字段类型:string字符型  number数字型
        :type Type: str
        :param Calc: 规则符  ==,!=,<=,>=
        :type Calc: str
        :param Value: 规则值
        :type Value: str
        """
        self.Key = None
        self.Type = None
        self.Calc = None
        self.Value = None

    def _deserialize(self, params):
        self.Key = params.get("Key")
        self.Type = params.get("Type")
        self.Calc = params.get("Calc")
        self.Value = params.get("Value")


class SendAlarmRequest(AbstractModel):
    """SendAlarm请求参数结构体"""

    def __init__(self):
        """
        :param TopicId: 告警源id
        :type TopicId: str
        :param Params: 自定义参数
        :type Params: str
        """
        self.TopicId = None
        self.Params = None

    def _deserialize(self, params):
        self.TopicId = params.get("TopicId")
        self.Params = params.get("Params")


class SendAlarmResponse(AbstractModel):
    """SendAlarm返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.UpdateOrDelReturn`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = UpdateOrDelReturn()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class Shield(AbstractModel):
    """告警屏蔽"""

    def __init__(self):
        """
        :param TopicId: 告警源id
        :type TopicId: str
        :param ShieldName: 屏蔽规则名
        :type ShieldName: str
        :param ShieldType: 屏蔽条件 all / custom
        :type ShieldType: str
        :param ShieldTimeType: 屏蔽条件 period / absolute
        :type ShieldTimeType: str
        :param ShieldTimeStart: 开始屏蔽时间戳
        :type ShieldTimeStart: int
        :param ShieldTimeEnd: 结束屏蔽时间戳
        :type ShieldTimeEnd: int
        :param ShieldId: 屏蔽规则ID 更新必填
        :type ShieldId: str
        :param ShieldRules: 自定义屏蔽条件
        :type ShieldRules: list of JudgeRules
        :param ShieldDayOfWeek: 周期屏蔽时的屏蔽设置星期几
        :type ShieldDayOfWeek: list of int
        :param AppId: 开发者帐号
        :type AppId: int
        :param OwnerUin: 屏蔽规则创建者uin
        :type OwnerUin: int
        :param LastEditUin: 最后更新屏蔽规则的uin
        :type LastEditUin: int
        :param UpdateTime: 最后更新时间戳
        :type UpdateTime: int
        :param InsertTime: 插入时间戳
        :type InsertTime: int
        """
        self.TopicId = None
        self.ShieldName = None
        self.ShieldType = None
        self.ShieldTimeType = None
        self.ShieldTimeStart = None
        self.ShieldTimeEnd = None
        self.ShieldId = None
        self.ShieldRules = None
        self.ShieldDayOfWeek = None
        self.AppId = None
        self.OwnerUin = None
        self.LastEditUin = None
        self.UpdateTime = None
        self.InsertTime = None

    def _deserialize(self, params):
        self.TopicId = params.get("TopicId")
        self.ShieldName = params.get("ShieldName")
        self.ShieldType = params.get("ShieldType")
        self.ShieldTimeType = params.get("ShieldTimeType")
        self.ShieldTimeStart = params.get("ShieldTimeStart")
        self.ShieldTimeEnd = params.get("ShieldTimeEnd")
        self.ShieldId = params.get("ShieldId")
        if params.get("ShieldRules") is not None:
            self.ShieldRules = []
            for item in params.get("ShieldRules"):
                obj = JudgeRules()
                obj._deserialize(item)
                self.ShieldRules.append(obj)
        self.ShieldDayOfWeek = params.get("ShieldDayOfWeek")
        self.AppId = params.get("AppId")
        self.OwnerUin = params.get("OwnerUin")
        self.LastEditUin = params.get("LastEditUin")
        self.UpdateTime = params.get("UpdateTime")
        self.InsertTime = params.get("InsertTime")


class Subs(AbstractModel):
    """订阅信息"""

    def __init__(self):
        """
        :param TopicId: 告警源id
        :type TopicId: str
        :param SubsName: 订阅名称
        :type SubsName: str
        :param SubsType: 订阅类型 all / custom
        :type SubsType: str
        :param NotifyWay: 通知方式 SMS,EMAIL,WECHAT,CALL
        :type NotifyWay: list of str
        :param SubsId: 订阅id 更新必填
        :type SubsId: str
        :param TopicName: 告警源名称
        :type TopicName: str
        :param SubsRules: 订阅规则
        :type SubsRules: list of JudgeRules
        :param ReceiverGroups: 接收用户组
        :type ReceiverGroups: list of int
        :param PhoneNotifyOrder: 语音告警接收人顺序
        :type PhoneNotifyOrder: list of int
        :param PhoneCircleTimes: 语音告警轮询次数
        :type PhoneCircleTimes: int
        :param PhoneInnerInterval: 语音告警轮内间隔
        :type PhoneInnerInterval: int
        :param PhoneCircleInterval: 语音告警次间间隔
        :type PhoneCircleInterval: int
        :param PhoneArriveNotice: 语音告警触达通知
        :type PhoneArriveNotice: int
        :param AppId: 开发者帐号
        :type AppId: int
        :param OwnerUin: 告警订阅创建者uin
        :type OwnerUin: int
        :param LastEditUin: 最后更新订阅的uin
        :type LastEditUin: int
        :param UpdateTime: 最后更新时间戳
        :type UpdateTime: int
        :param InsertTime: 插入时间戳
        :type InsertTime: int
        :param ValidStartTime: 订阅有效开始时间
        :type ValidStartTime: int
        :param ValidEndTime: 订阅有效结束时间
        :type ValidEndTime: int
        :param ReceiverUins: 接收人
        :type ReceiverUins: list of int
        """
        self.TopicId = None
        self.SubsName = None
        self.SubsType = None
        self.NotifyWay = None
        self.SubsId = None
        self.TopicName = None
        self.SubsRules = None
        self.ReceiverGroups = None
        self.PhoneNotifyOrder = None
        self.PhoneCircleTimes = None
        self.PhoneInnerInterval = None
        self.PhoneCircleInterval = None
        self.PhoneArriveNotice = None
        self.AppId = None
        self.OwnerUin = None
        self.LastEditUin = None
        self.UpdateTime = None
        self.InsertTime = None
        self.ValidStartTime = None
        self.ValidEndTime = None
        self.ReceiverUins = None

    def _deserialize(self, params):
        self.TopicId = params.get("TopicId")
        self.SubsName = params.get("SubsName")
        self.SubsType = params.get("SubsType")
        self.NotifyWay = params.get("NotifyWay")
        self.SubsId = params.get("SubsId")
        self.TopicName = params.get("TopicName")
        if params.get("SubsRules") is not None:
            self.SubsRules = []
            for item in params.get("SubsRules"):
                obj = JudgeRules()
                obj._deserialize(item)
                self.SubsRules.append(obj)
        self.ReceiverGroups = params.get("ReceiverGroups")
        self.PhoneNotifyOrder = params.get("PhoneNotifyOrder")
        self.PhoneCircleTimes = params.get("PhoneCircleTimes")
        self.PhoneInnerInterval = params.get("PhoneInnerInterval")
        self.PhoneCircleInterval = params.get("PhoneCircleInterval")
        self.PhoneArriveNotice = params.get("PhoneArriveNotice")
        self.AppId = params.get("AppId")
        self.OwnerUin = params.get("OwnerUin")
        self.LastEditUin = params.get("LastEditUin")
        self.UpdateTime = params.get("UpdateTime")
        self.InsertTime = params.get("InsertTime")
        self.ValidStartTime = params.get("ValidStartTime")
        self.ValidEndTime = params.get("ValidEndTime")
        self.ReceiverUins = params.get("ReceiverUins")


class Topic(AbstractModel):
    """告警源参数"""

    def __init__(self):
        """
        :param TopicName: 告警源名称
        :type TopicName: str
        :param FieldType: 告警源类型(默认参数为manual)
        :type FieldType: str
        :param Fields: 自定义字段信息
        :type Fields: list of Field
        :param TopicId: 告警源id 更新必填
        :type TopicId: str
        :param AppId: Appid
        :type AppId: int
        :param OwnerUin: 创建人uin
        :type OwnerUin: int
        :param LastEditUin: 最后编辑人uin
        :type LastEditUin: int
        :param UpdateTime: 更新时间（时间戳）
        :type UpdateTime: int
        :param InsertTime: 创建时间（时间戳）
        :type InsertTime: int
        :param InformTemplate: 告警模板
        :type InformTemplate: :class:`tcecloud.amp.v20190911.models.Inform`
        """
        self.TopicName = None
        self.FieldType = None
        self.Fields = None
        self.TopicId = None
        self.AppId = None
        self.OwnerUin = None
        self.LastEditUin = None
        self.UpdateTime = None
        self.InsertTime = None
        self.InformTemplate = None

    def _deserialize(self, params):
        self.TopicName = params.get("TopicName")
        self.FieldType = params.get("FieldType")
        if params.get("Fields") is not None:
            self.Fields = []
            for item in params.get("Fields"):
                obj = Field()
                obj._deserialize(item)
                self.Fields.append(obj)
        self.TopicId = params.get("TopicId")
        self.AppId = params.get("AppId")
        self.OwnerUin = params.get("OwnerUin")
        self.LastEditUin = params.get("LastEditUin")
        self.UpdateTime = params.get("UpdateTime")
        self.InsertTime = params.get("InsertTime")
        if params.get("InformTemplate") is not None:
            self.InformTemplate = Inform()
            self.InformTemplate._deserialize(params.get("InformTemplate"))


class UpdateConvergenceRequest(AbstractModel):
    """UpdateConvergence请求参数结构体"""

    def __init__(self):
        """
        :param TopicId: 无
        :type TopicId: str
        :param Data: 无
        :type Data: :class:`tcecloud.amp.v20190911.models.Conv`
        """
        self.TopicId = None
        self.Data = None

    def _deserialize(self, params):
        self.TopicId = params.get("TopicId")
        if params.get("Data") is not None:
            self.Data = Conv()
            self.Data._deserialize(params.get("Data"))


class UpdateConvergenceResponse(AbstractModel):
    """UpdateConvergence返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.UpdateOrDelReturn`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = UpdateOrDelReturn()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class UpdateHandleRequest(AbstractModel):
    """UpdateHandle请求参数结构体"""

    def __init__(self):
        """
        :param TopicId: 无
        :type TopicId: str
        :param Data: 无
        :type Data: :class:`tcecloud.amp.v20190911.models.Handle`
        """
        self.TopicId = None
        self.Data = None

    def _deserialize(self, params):
        self.TopicId = params.get("TopicId")
        if params.get("Data") is not None:
            self.Data = Handle()
            self.Data._deserialize(params.get("Data"))


class UpdateHandleResponse(AbstractModel):
    """UpdateHandle返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.UpdateOrDelReturn`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = UpdateOrDelReturn()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class UpdateOrDelReturn(AbstractModel):
    """返回信息"""

    def __init__(self):
        """
        :param Status: 状态
        :type Status: str
        :param Message: 信息
        :type Message: str
        """
        self.Status = None
        self.Message = None

    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.Message = params.get("Message")


class UpdateSubRequest(AbstractModel):
    """UpdateSub请求参数结构体"""

    def __init__(self):
        """
        :param SubsId: 无
        :type SubsId: str
        :param Data: 无
        :type Data: :class:`tcecloud.amp.v20190911.models.Subs`
        :param TopicId: 无
        :type TopicId: str
        """
        self.SubsId = None
        self.Data = None
        self.TopicId = None

    def _deserialize(self, params):
        self.SubsId = params.get("SubsId")
        if params.get("Data") is not None:
            self.Data = Subs()
            self.Data._deserialize(params.get("Data"))
        self.TopicId = params.get("TopicId")


class UpdateSubResponse(AbstractModel):
    """UpdateSub返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.UpdateOrDelReturn`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = UpdateOrDelReturn()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class UpdateTopicRequest(AbstractModel):
    """UpdateTopic请求参数结构体"""

    def __init__(self):
        """
        :param TopicId: 修改告警主题Id
        :type TopicId: str
        :param Data: 修改告警内容
        :type Data: :class:`tcecloud.amp.v20190911.models.Topic`
        """
        self.TopicId = None
        self.Data = None

    def _deserialize(self, params):
        self.TopicId = params.get("TopicId")
        if params.get("Data") is not None:
            self.Data = Topic()
            self.Data._deserialize(params.get("Data"))


class UpdateTopicResponse(AbstractModel):
    """UpdateTopic返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回信息
        :type Data: :class:`tcecloud.amp.v20190911.models.UpdateOrDelReturn`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = UpdateOrDelReturn()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")

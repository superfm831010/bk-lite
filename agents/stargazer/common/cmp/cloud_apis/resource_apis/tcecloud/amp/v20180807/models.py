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
        :param Status: 搜索告警的状态限制
        :type Status: str
        :param TopicId: 要搜索告警的主题Id
        :type TopicId: str
        :param SearchContent: 全局搜索内容
        :type SearchContent: str
        :param SortKey: 排序字段
        :type SortKey: str
        :param SortOrder: 排序字段顺序
        :type SortOrder: str
        :param SearchKeyValuePairs: 分字段进行告警搜索KV对
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
        :param Data: 无
        :type Data: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Data = params.get("Data")
        self.RequestId = params.get("RequestId")


class SendMessageRequest(AbstractModel):
    """SendMessage请求参数结构体"""

    def __init__(self):
        """
        :param TopicId: 发布告警的主题Id
        :type TopicId: str
        :param Params: 发布告警的内容
        :type Params: str
        """
        self.TopicId = None
        self.Params = None

    def _deserialize(self, params):
        self.TopicId = params.get("TopicId")
        self.Params = params.get("Params")


class SendMessageResponse(AbstractModel):
    """SendMessage返回参数结构体"""

    def __init__(self):
        """
        :param Data: 无
        :type Data: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Data = params.get("Data")
        self.RequestId = params.get("RequestId")


class UpdateHandleRequest(AbstractModel):
    """UpdateHandle请求参数结构体"""

    def __init__(self):
        """
        :param TopicId: 无
        :type TopicId: str
        :param Data: 无
        :type Data: str
        """
        self.TopicId = None
        self.Data = None

    def _deserialize(self, params):
        self.TopicId = params.get("TopicId")
        self.Data = params.get("Data")


class UpdateHandleResponse(AbstractModel):
    """UpdateHandle返回参数结构体"""

    def __init__(self):
        """
        :param Data: 无
        :type Data: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Data = params.get("Data")
        self.RequestId = params.get("RequestId")

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

import json

from common.cmp.cloud_apis.resource_apis.tcecloud.amp.v20190911 import models
from common.cmp.cloud_apis.resource_apis.tcecloud.common.abstract_client import AbstractClient
from common.cmp.cloud_apis.resource_apis.tcecloud.common.exception.tce_cloud_sdk_exception import TceCloudSDKException


class AmpClient(AbstractClient):
    _apiVersion = "2019-09-11"
    _endpoint = "amp.api3.{{conf.main_domain}}"

    def AddConvergence(self, request):
        """添加收敛规则

        :param request: 调用AddConvergence所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.AddConvergenceRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.AddConvergenceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AddConvergence", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AddConvergenceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def AddHandle(self, request):
        """增加处理规则

        :param request: 调用AddHandle所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.AddHandleRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.AddHandleResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AddHandle", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AddHandleResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def AddShield(self, request):
        """添加屏蔽规则

        :param request: 调用AddShield所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.AddShieldRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.AddShieldResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AddShield", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AddShieldResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def AddSub(self, request):
        """增加订阅

        :param request: 调用AddSub所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.AddSubRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.AddSubResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AddSub", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AddSubResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def AddTopic(self, request):
        """添加告警源

        :param request: 调用AddTopic所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.AddTopicRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.AddTopicResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AddTopic", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AddTopicResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteConvergences(self, request):
        """删除多个收敛规则

        :param request: 调用DeleteConvergences所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.DeleteConvergencesRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.DeleteConvergencesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteConvergences", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteConvergencesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteHandles(self, request):
        """删除多个处理规则

        :param request: 调用DeleteHandles所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.DeleteHandlesRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.DeleteHandlesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteHandles", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteHandlesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteShields(self, request):
        """删除多个屏蔽规则

        :param request: 调用DeleteShields所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.DeleteShieldsRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.DeleteShieldsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteShields", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteShieldsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteSubs(self, request):
        """删除多个订阅

        :param request: 调用DeleteSubs所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.DeleteSubsRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.DeleteSubsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteSubs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteSubsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteTopics(self, request):
        """删除多个告警主题

        :param request: 调用DeleteTopics所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.DeleteTopicsRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.DeleteTopicsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteTopics", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteTopicsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def GetAlertHistory(self, request):
        """获取告警历史

        :param request: 调用GetAlertHistory所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.GetAlertHistoryRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.GetAlertHistoryResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetAlertHistory", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetAlertHistoryResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def GetAlertHistoryById(self, request):
        """获取告警历史详情

        :param request: 调用GetAlertHistoryById所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.GetAlertHistoryByIdRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.GetAlertHistoryByIdResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetAlertHistoryById", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetAlertHistoryByIdResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def GetConfigHistory(self, request):
        """获取修改历史

        :param request: 调用GetConfigHistory所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.GetConfigHistoryRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.GetConfigHistoryResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetConfigHistory", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetConfigHistoryResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def GetConvergence(self, request):
        """获取单个收敛规则

        :param request: 调用GetConvergence所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.GetConvergenceRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.GetConvergenceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetConvergence", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetConvergenceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def GetConvergences(self, request):
        """获取收敛规则

        :param request: 调用GetConvergences所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.GetConvergencesRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.GetConvergencesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetConvergences", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetConvergencesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def GetHandle(self, request):
        """获取单个告警处理

        :param request: 调用GetHandle所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.GetHandleRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.GetHandleResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetHandle", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetHandleResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def GetHandles(self, request):
        """获取处理动作

        :param request: 调用GetHandles所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.GetHandlesRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.GetHandlesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetHandles", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetHandlesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def GetShield(self, request):
        """获取单个屏蔽

        :param request: 调用GetShield所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.GetShieldRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.GetShieldResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetShield", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetShieldResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def GetShields(self, request):
        """获取屏蔽规则

        :param request: 调用GetShields所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.GetShieldsRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.GetShieldsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetShields", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetShieldsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def GetSub(self, request):
        """获取单个订阅规则

        :param request: 调用GetSub所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.GetSubRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.GetSubResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetSub", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetSubResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def GetSubs(self, request):
        """获取订阅

        :param request: 调用GetSubs所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.GetSubsRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.GetSubsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetSubs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetSubsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def GetTopic(self, request):
        """获取单个告警主题

        :param request: 调用GetTopic所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.GetTopicRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.GetTopicResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetTopic", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetTopicResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def GetTopicFieldTemplate(self, request):
        """获取告警参数信息

        :param request: 调用GetTopicFieldTemplate所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.GetTopicFieldTemplateRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.GetTopicFieldTemplateResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetTopicFieldTemplate", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetTopicFieldTemplateResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def GetTopics(self, request):
        """获取所有告警主题

        :param request: 调用GetTopics所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.GetTopicsRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.GetTopicsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetTopics", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetTopicsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def SendAlarm(self, request):
        """发送告警接口

        :param request: 调用SendAlarm所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.SendAlarmRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.SendAlarmResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SendAlarm", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SendAlarmResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def UpdateConvergence(self, request):
        """修改收敛规则

        :param request: 调用UpdateConvergence所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.UpdateConvergenceRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.UpdateConvergenceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("UpdateConvergence", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UpdateConvergenceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def UpdateHandle(self, request):
        """修改处理规则

        :param request: 调用UpdateHandle所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.UpdateHandleRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.UpdateHandleResponse`

        """
        try:
            params = request._serialize()
            body = self.call("UpdateHandle", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UpdateHandleResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def UpdateSub(self, request):
        """修改订阅

        :param request: 调用UpdateSub所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.UpdateSubRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.UpdateSubResponse`

        """
        try:
            params = request._serialize()
            body = self.call("UpdateSub", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UpdateSubResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def UpdateTopic(self, request):
        """修改告警主题

        :param request: 调用UpdateTopic所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20190911.models.UpdateTopicRequest`
        :rtype: :class:`tcecloud.amp.v20190911.models.UpdateTopicResponse`

        """
        try:
            params = request._serialize()
            body = self.call("UpdateTopic", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UpdateTopicResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

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

from common.cmp.cloud_apis.resource_apis.tcecloud.amp.v20180807 import models
from common.cmp.cloud_apis.resource_apis.tcecloud.common.abstract_client import AbstractClient
from common.cmp.cloud_apis.resource_apis.tcecloud.common.exception.tce_cloud_sdk_exception import TceCloudSDKException


class AmpClient(AbstractClient):
    _apiVersion = "2018-08-07"
    _endpoint = "amp.api3.{{conf.main_domain}}"

    def GetAlertHistory(self, request):
        """
        获取告警历史
        :param request: 调用GetAlertHistory所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20180807.models.GetAlertHistoryRequest`
        :rtype: :class:`tcecloud.amp.v20180807.models.GetAlertHistoryResponse`

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

    def SendMessage(self, request):
        """发布消息

        :param request: 调用SendMessage所需参数的结构体。
        :type request: :class:`tcecloud.amp.v20180807.models.SendMessageRequest`
        :rtype: :class:`tcecloud.amp.v20180807.models.SendMessageResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SendMessage", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SendMessageResponse()
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
        :type request: :class:`tcecloud.amp.v20180807.models.UpdateHandleRequest`
        :rtype: :class:`tcecloud.amp.v20180807.models.UpdateHandleResponse`

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

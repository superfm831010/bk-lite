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

from common.cmp.cloud_apis.resource_apis.tcecloud.common.abstract_client import AbstractClient
from common.cmp.cloud_apis.resource_apis.tcecloud.common.exception.tce_cloud_sdk_exception import TceCloudSDKException
from common.cmp.cloud_apis.resource_apis.tcecloud.csp.v20200107 import models


class CspClient(AbstractClient):
    _apiVersion = "2020-01-07"
    _endpoint = "csp.api3.{{conf.main_domain}}"

    def DeleteMultipleObject(self, request):
        """删除多个对象

        :param request: 调用DeleteMultipleObject所需参数的结构体。
        :type request: :class:`tcecloud.csp.v20200107.models.DeleteMultipleObjectRequest`
        :rtype: :class:`tcecloud.csp.v20200107.models.DeleteMultipleObjectResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteMultipleObject", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteMultipleObjectResponse()
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

    def DeleteObject(self, request):
        """DELETE Object 接口请求可以在 COS 的存储桶中将一个对象（Object）删除。该操作需要请求者对存储桶有 WRITE 权限。

        :param request: 调用DeleteObject所需参数的结构体。
        :type request: :class:`tcecloud.csp.v20200107.models.DeleteObjectRequest`
        :rtype: :class:`tcecloud.csp.v20200107.models.DeleteObjectResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteObject", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteObjectResponse()
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

    def GetBucketReferer(self, request):
        """获取存储桶 Referer 白名单或者黑名单

        :param request: 调用GetBucketReferer所需参数的结构体。
        :type request: :class:`tcecloud.csp.v20200107.models.GetBucketRefererRequest`
        :rtype: :class:`tcecloud.csp.v20200107.models.GetBucketRefererResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetBucketReferer", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetBucketRefererResponse()
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

    def GetOverview(self, request):
        """获取用户的概览信息

        :param request: 调用GetOverview所需参数的结构体。
        :type request: :class:`tcecloud.csp.v20200107.models.GetOverviewRequest`
        :rtype: :class:`tcecloud.csp.v20200107.models.GetOverviewResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetOverview", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetOverviewResponse()
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

    def GetRegionList(self, request):
        """获取用户地域列表

        :param request: 调用GetRegionList所需参数的结构体。
        :type request: :class:`tcecloud.csp.v20200107.models.GetRegionListRequest`
        :rtype: :class:`tcecloud.csp.v20200107.models.GetRegionListResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetRegionList", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetRegionListResponse()
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

    def GetService(self, request):
        """获取存储桶列表

        :param request: 调用GetService所需参数的结构体。
        :type request: :class:`tcecloud.csp.v20200107.models.GetServiceRequest`
        :rtype: :class:`tcecloud.csp.v20200107.models.GetServiceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetService", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetServiceResponse()
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

    def GetStatDay(self, request):
        """获取单日单存储桶统计信息

        :param request: 调用GetStatDay所需参数的结构体。
        :type request: :class:`tcecloud.csp.v20200107.models.GetStatDayRequest`
        :rtype: :class:`tcecloud.csp.v20200107.models.GetStatDayResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetStatDay", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetStatDayResponse()
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

    def GetStatDays(self, request):
        """获取多日单存储桶的统计信息

        :param request: 调用GetStatDays所需参数的结构体。
        :type request: :class:`tcecloud.csp.v20200107.models.GetStatDaysRequest`
        :rtype: :class:`tcecloud.csp.v20200107.models.GetStatDaysResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetStatDays", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetStatDaysResponse()
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

    def GetStatHttpDay(self, request):
        """获取单日单存储桶的http请求统计信息

        :param request: 调用GetStatHttpDay所需参数的结构体。
        :type request: :class:`tcecloud.csp.v20200107.models.GetStatHttpDayRequest`
        :rtype: :class:`tcecloud.csp.v20200107.models.GetStatHttpDayResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetStatHttpDay", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetStatHttpDayResponse()
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

    def GetStatHttpDays(self, request):
        """获取多日单存储桶的http请求统计信息

        :param request: 调用GetStatHttpDays所需参数的结构体。
        :type request: :class:`tcecloud.csp.v20200107.models.GetStatHttpDaysRequest`
        :rtype: :class:`tcecloud.csp.v20200107.models.GetStatHttpDaysResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetStatHttpDays", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetStatHttpDaysResponse()
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

    def GetUserStat(self, request):
        """获取用户状态

        :param request: 调用GetUserStat所需参数的结构体。
        :type request: :class:`tcecloud.csp.v20200107.models.GetUserStatRequest`
        :rtype: :class:`tcecloud.csp.v20200107.models.GetUserStatResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetUserStat", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetUserStatResponse()
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

    def HeadObject(self, request):
        """获取对象属性

        :param request: 调用HeadObject所需参数的结构体。
        :type request: :class:`tcecloud.csp.v20200107.models.HeadObjectRequest`
        :rtype: :class:`tcecloud.csp.v20200107.models.HeadObjectResponse`

        """
        try:
            params = request._serialize()
            body = self.call("HeadObject", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.HeadObjectResponse()
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

    def OpenCosBilling(self, request):
        """开通COS计费

        :param request: 调用OpenCosBilling所需参数的结构体。
        :type request: :class:`tcecloud.csp.v20200107.models.OpenCosBillingRequest`
        :rtype: :class:`tcecloud.csp.v20200107.models.OpenCosBillingResponse`

        """
        try:
            params = request._serialize()
            body = self.call("OpenCosBilling", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.OpenCosBillingResponse()
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

    def PutBucket(self, request):
        """创建存储桶

        :param request: 调用PutBucket所需参数的结构体。
        :type request: :class:`tcecloud.csp.v20200107.models.PutBucketRequest`
        :rtype: :class:`tcecloud.csp.v20200107.models.PutBucketResponse`

        """
        try:
            params = request._serialize()
            body = self.call("PutBucket", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.PutBucketResponse()
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

    def PutBucketReferer(self, request):
        """为存储桶设置 Referer 白名单或者黑名单

        :param request: 调用PutBucketReferer所需参数的结构体。
        :type request: :class:`tcecloud.csp.v20200107.models.PutBucketRefererRequest`
        :rtype: :class:`tcecloud.csp.v20200107.models.PutBucketRefererResponse`

        """
        try:
            params = request._serialize()
            body = self.call("PutBucketReferer", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.PutBucketRefererResponse()
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

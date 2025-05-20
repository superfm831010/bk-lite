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

from common.cmp.cloud_apis.resource_apis.tcecloud.cfs.v20180416 import models
from common.cmp.cloud_apis.resource_apis.tcecloud.common.abstract_client import AbstractClient
from common.cmp.cloud_apis.resource_apis.tcecloud.common.exception.tce_cloud_sdk_exception import TceCloudSDKException


class CfsClient(AbstractClient):
    _apiVersion = "2018-04-16"
    _endpoint = "cfs.api3.{{conf.main_domain}}"

    def CreateCfsFileSystem(self, request):
        """用于添加新文件系统

        :param request: 调用CreateCfsFileSystem所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20180416.models.CreateCfsFileSystemRequest`
        :rtype: :class:`tcecloud.cfs.v20180416.models.CreateCfsFileSystemResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateCfsFileSystem", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateCfsFileSystemResponse()
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

    def CreateCfsPGroup(self, request):
        """本接口（CreateCfsPGroup）用于创建权限组

        :param request: 调用CreateCfsPGroup所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20180416.models.CreateCfsPGroupRequest`
        :rtype: :class:`tcecloud.cfs.v20180416.models.CreateCfsPGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateCfsPGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateCfsPGroupResponse()
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

    def CreateCfsRule(self, request):
        """本接口（CreateCfsRule）用于创建权限组规则。

        :param request: 调用CreateCfsRule所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20180416.models.CreateCfsRuleRequest`
        :rtype: :class:`tcecloud.cfs.v20180416.models.CreateCfsRuleResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateCfsRule", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateCfsRuleResponse()
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

    def DeleteCfsFileSystem(self, request):
        """用于删除文件系统

        :param request: 调用DeleteCfsFileSystem所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20180416.models.DeleteCfsFileSystemRequest`
        :rtype: :class:`tcecloud.cfs.v20180416.models.DeleteCfsFileSystemResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteCfsFileSystem", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteCfsFileSystemResponse()
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

    def DeleteCfsPGroup(self, request):
        """本接口（DeleteCfsPGroup）用于删除权限组。

        :param request: 调用DeleteCfsPGroup所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20180416.models.DeleteCfsPGroupRequest`
        :rtype: :class:`tcecloud.cfs.v20180416.models.DeleteCfsPGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteCfsPGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteCfsPGroupResponse()
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

    def DeleteCfsRule(self, request):
        """本接口（DeleteCfsRule）用于删除权限组规则。

        :param request: 调用DeleteCfsRule所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20180416.models.DeleteCfsRuleRequest`
        :rtype: :class:`tcecloud.cfs.v20180416.models.DeleteCfsRuleResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteCfsRule", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteCfsRuleResponse()
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

    def QueryAvailableZoneInfo(self, request):
        """本接口（QueryAvailableZoneInfo）用于查询区域的可用情况。

        :param request: 调用QueryAvailableZoneInfo所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20180416.models.QueryAvailableZoneInfoRequest`
        :rtype: :class:`tcecloud.cfs.v20180416.models.QueryAvailableZoneInfoResponse`

        """
        try:
            params = request._serialize()
            body = self.call("QueryAvailableZoneInfo", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.QueryAvailableZoneInfoResponse()
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

    def QueryCfsFileSystem(self, request):
        """用于查询文件系统

        :param request: 调用QueryCfsFileSystem所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20180416.models.QueryCfsFileSystemRequest`
        :rtype: :class:`tcecloud.cfs.v20180416.models.QueryCfsFileSystemResponse`

        """
        try:
            params = request._serialize()
            body = self.call("QueryCfsFileSystem", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.QueryCfsFileSystemResponse()
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

    def QueryCfsKmsKeys(self, request):
        """本接口（QueryCfsKmsKeys）用于查询KMS服务的密钥。

        :param request: 调用QueryCfsKmsKeys所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20180416.models.QueryCfsKmsKeysRequest`
        :rtype: :class:`tcecloud.cfs.v20180416.models.QueryCfsKmsKeysResponse`

        """
        try:
            params = request._serialize()
            body = self.call("QueryCfsKmsKeys", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.QueryCfsKmsKeysResponse()
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

    def QueryCfsPGroup(self, request):
        """本接口（QueryCfsPGroup）用于查询权限组列表。

        :param request: 调用QueryCfsPGroup所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20180416.models.QueryCfsPGroupRequest`
        :rtype: :class:`tcecloud.cfs.v20180416.models.QueryCfsPGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("QueryCfsPGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.QueryCfsPGroupResponse()
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

    def QueryCfsRule(self, request):
        """本接口（QueryCfsRule）用于查询权限组规则列表。

        :param request: 调用QueryCfsRule所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20180416.models.QueryCfsRuleRequest`
        :rtype: :class:`tcecloud.cfs.v20180416.models.QueryCfsRuleResponse`

        """
        try:
            params = request._serialize()
            body = self.call("QueryCfsRule", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.QueryCfsRuleResponse()
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

    def QueryCfsServiceStatus(self, request):
        """本接口（QueryCfsServiceStatus）用于查询用户使用CFS的服务状态。

        :param request: 调用QueryCfsServiceStatus所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20180416.models.QueryCfsServiceStatusRequest`
        :rtype: :class:`tcecloud.cfs.v20180416.models.QueryCfsServiceStatusResponse`

        """
        try:
            params = request._serialize()
            body = self.call("QueryCfsServiceStatus", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.QueryCfsServiceStatusResponse()
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

    def QueryMountTarget(self, request):
        """本接口（QueryMountTarget）用于查询文件系统挂载点信息

        :param request: 调用QueryMountTarget所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20180416.models.QueryMountTargetRequest`
        :rtype: :class:`tcecloud.cfs.v20180416.models.QueryMountTargetResponse`

        """
        try:
            params = request._serialize()
            body = self.call("QueryMountTarget", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.QueryMountTargetResponse()
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

    def QueryMountTargetsWithRegion(self, request):
        """查询区域挂载点情况，只用于控制台

        :param request: 调用QueryMountTargetsWithRegion所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20180416.models.QueryMountTargetsWithRegionRequest`
        :rtype: :class:`tcecloud.cfs.v20180416.models.QueryMountTargetsWithRegionResponse`

        """
        try:
            params = request._serialize()
            body = self.call("QueryMountTargetsWithRegion", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.QueryMountTargetsWithRegionResponse()
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

    def SignUpCfsService(self, request):
        """本接口（SignUpCfsService）用于开通CFS服务。

        :param request: 调用SignUpCfsService所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20180416.models.SignUpCfsServiceRequest`
        :rtype: :class:`tcecloud.cfs.v20180416.models.SignUpCfsServiceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SignUpCfsService", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SignUpCfsServiceResponse()
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

    def UpdateCfsFileSystemName(self, request):
        """本接口（UpdateCfsFileSystemName）用于更新文件系统名

        :param request: 调用UpdateCfsFileSystemName所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20180416.models.UpdateCfsFileSystemNameRequest`
        :rtype: :class:`tcecloud.cfs.v20180416.models.UpdateCfsFileSystemNameResponse`

        """
        try:
            params = request._serialize()
            body = self.call("UpdateCfsFileSystemName", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UpdateCfsFileSystemNameResponse()
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

    def UpdateCfsFileSystemPGroup(self, request):
        """本接口（UpdateCfsFileSystemPGroup）用于更新文件系统所使用的权限组

        :param request: 调用UpdateCfsFileSystemPGroup所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20180416.models.UpdateCfsFileSystemPGroupRequest`
        :rtype: :class:`tcecloud.cfs.v20180416.models.UpdateCfsFileSystemPGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("UpdateCfsFileSystemPGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UpdateCfsFileSystemPGroupResponse()
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

    def UpdateCfsFileSystemSizeLimit(self, request):
        """本接口（UpdateCfsFileSystemSizeLimit）用于更新文件系统存储容量限制。

        :param request: 调用UpdateCfsFileSystemSizeLimit所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20180416.models.UpdateCfsFileSystemSizeLimitRequest`
        :rtype: :class:`tcecloud.cfs.v20180416.models.UpdateCfsFileSystemSizeLimitResponse`

        """
        try:
            params = request._serialize()
            body = self.call("UpdateCfsFileSystemSizeLimit", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UpdateCfsFileSystemSizeLimitResponse()
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

    def UpdateCfsPGroup(self, request):
        """本接口（UpdateCfsPGroup）更新权限组信息。

        :param request: 调用UpdateCfsPGroup所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20180416.models.UpdateCfsPGroupRequest`
        :rtype: :class:`tcecloud.cfs.v20180416.models.UpdateCfsPGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("UpdateCfsPGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UpdateCfsPGroupResponse()
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

    def UpdateCfsRule(self, request):
        """本接口（UpdateCfsRule）用于更新权限规则。

        :param request: 调用UpdateCfsRule所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20180416.models.UpdateCfsRuleRequest`
        :rtype: :class:`tcecloud.cfs.v20180416.models.UpdateCfsRuleResponse`

        """
        try:
            params = request._serialize()
            body = self.call("UpdateCfsRule", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UpdateCfsRuleResponse()
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

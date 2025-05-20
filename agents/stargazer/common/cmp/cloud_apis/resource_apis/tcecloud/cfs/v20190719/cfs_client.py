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

from common.cmp.cloud_apis.resource_apis.tcecloud.cfs.v20190719 import models
from common.cmp.cloud_apis.resource_apis.tcecloud.common.abstract_client import AbstractClient
from common.cmp.cloud_apis.resource_apis.tcecloud.common.exception.tce_cloud_sdk_exception import TceCloudSDKException


class CfsClient(AbstractClient):
    _apiVersion = "2019-07-19"
    _endpoint = "cfs.api3.{{conf.main_domain}}"

    def AddMountTarget(self, request):
        """用于创建挂载点

        :param request: 调用AddMountTarget所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20190719.models.AddMountTargetRequest`
        :rtype: :class:`tcecloud.cfs.v20190719.models.AddMountTargetResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AddMountTarget", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AddMountTargetResponse()
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

    def CreateCfsFileSystem(self, request):
        """用于添加新文件系统

        :param request: 调用CreateCfsFileSystem所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20190719.models.CreateCfsFileSystemRequest`
        :rtype: :class:`tcecloud.cfs.v20190719.models.CreateCfsFileSystemResponse`

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
        :type request: :class:`tcecloud.cfs.v20190719.models.CreateCfsPGroupRequest`
        :rtype: :class:`tcecloud.cfs.v20190719.models.CreateCfsPGroupResponse`

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
        :type request: :class:`tcecloud.cfs.v20190719.models.CreateCfsRuleRequest`
        :rtype: :class:`tcecloud.cfs.v20190719.models.CreateCfsRuleResponse`

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
        :type request: :class:`tcecloud.cfs.v20190719.models.DeleteCfsFileSystemRequest`
        :rtype: :class:`tcecloud.cfs.v20190719.models.DeleteCfsFileSystemResponse`

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
        :type request: :class:`tcecloud.cfs.v20190719.models.DeleteCfsPGroupRequest`
        :rtype: :class:`tcecloud.cfs.v20190719.models.DeleteCfsPGroupResponse`

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
        :type request: :class:`tcecloud.cfs.v20190719.models.DeleteCfsRuleRequest`
        :rtype: :class:`tcecloud.cfs.v20190719.models.DeleteCfsRuleResponse`

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

    def DeleteMountTarget(self, request):
        """本接口（DeleteMountTarget）用于删除挂载点

        :param request: 调用DeleteMountTarget所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20190719.models.DeleteMountTargetRequest`
        :rtype: :class:`tcecloud.cfs.v20190719.models.DeleteMountTargetResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteMountTarget", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteMountTargetResponse()
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

    def DescribeAvailableZoneInfo(self, request):
        """本接口（DescribeAvailableZoneInfo）用于查询区域的可用情况。

        :param request: 调用DescribeAvailableZoneInfo所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20190719.models.DescribeAvailableZoneInfoRequest`
        :rtype: :class:`tcecloud.cfs.v20190719.models.DescribeAvailableZoneInfoResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeAvailableZoneInfo", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAvailableZoneInfoResponse()
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

    def DescribeCfsFileSystemClients(self, request):
        """查询挂载该文件系统的客户端。此功能需要客户端安装CFS监控插件。

        :param request: 调用DescribeCfsFileSystemClients所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20190719.models.DescribeCfsFileSystemClientsRequest`
        :rtype: :class:`tcecloud.cfs.v20190719.models.DescribeCfsFileSystemClientsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeCfsFileSystemClients", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCfsFileSystemClientsResponse()
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

    def DescribeCfsFileSystems(self, request):
        """本接口（DescribeCfsFileSystems）用于查询文件系统

        :param request: 调用DescribeCfsFileSystems所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20190719.models.DescribeCfsFileSystemsRequest`
        :rtype: :class:`tcecloud.cfs.v20190719.models.DescribeCfsFileSystemsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeCfsFileSystems", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCfsFileSystemsResponse()
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

    def DescribeCfsPGroups(self, request):
        """本接口（DescribeCfsPGroups）用于查询权限组列表。

        :param request: 调用DescribeCfsPGroups所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20190719.models.DescribeCfsPGroupsRequest`
        :rtype: :class:`tcecloud.cfs.v20190719.models.DescribeCfsPGroupsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeCfsPGroups", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCfsPGroupsResponse()
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

    def DescribeCfsRules(self, request):
        """本接口（DescribeCfsRules）用于查询权限组规则列表。

        :param request: 调用DescribeCfsRules所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20190719.models.DescribeCfsRulesRequest`
        :rtype: :class:`tcecloud.cfs.v20190719.models.DescribeCfsRulesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeCfsRules", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCfsRulesResponse()
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

    def DescribeCfsServiceStatus(self, request):
        """本接口（DescribeCfsServiceStatus）用于查询用户使用CFS的服务状态。

        :param request: 调用DescribeCfsServiceStatus所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20190719.models.DescribeCfsServiceStatusRequest`
        :rtype: :class:`tcecloud.cfs.v20190719.models.DescribeCfsServiceStatusResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeCfsServiceStatus", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCfsServiceStatusResponse()
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

    def DescribeCfsTags(self, request):
        """查询cfs资源池列表

        :param request: 调用DescribeCfsTags所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20190719.models.DescribeCfsTagsRequest`
        :rtype: :class:`tcecloud.cfs.v20190719.models.DescribeCfsTagsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeCfsTags", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCfsTagsResponse()
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

    def DescribeMountTargets(self, request):
        """本接口（DescribeMountTargets）用于查询文件系统挂载点信息

        :param request: 调用DescribeMountTargets所需参数的结构体。
        :type request: :class:`tcecloud.cfs.v20190719.models.DescribeMountTargetsRequest`
        :rtype: :class:`tcecloud.cfs.v20190719.models.DescribeMountTargetsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeMountTargets", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeMountTargetsResponse()
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
        :type request: :class:`tcecloud.cfs.v20190719.models.SignUpCfsServiceRequest`
        :rtype: :class:`tcecloud.cfs.v20190719.models.SignUpCfsServiceResponse`

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
        :type request: :class:`tcecloud.cfs.v20190719.models.UpdateCfsFileSystemNameRequest`
        :rtype: :class:`tcecloud.cfs.v20190719.models.UpdateCfsFileSystemNameResponse`

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
        :type request: :class:`tcecloud.cfs.v20190719.models.UpdateCfsFileSystemPGroupRequest`
        :rtype: :class:`tcecloud.cfs.v20190719.models.UpdateCfsFileSystemPGroupResponse`

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
        :type request: :class:`tcecloud.cfs.v20190719.models.UpdateCfsFileSystemSizeLimitRequest`
        :rtype: :class:`tcecloud.cfs.v20190719.models.UpdateCfsFileSystemSizeLimitResponse`

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
        :type request: :class:`tcecloud.cfs.v20190719.models.UpdateCfsPGroupRequest`
        :rtype: :class:`tcecloud.cfs.v20190719.models.UpdateCfsPGroupResponse`

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
        :type request: :class:`tcecloud.cfs.v20190719.models.UpdateCfsRuleRequest`
        :rtype: :class:`tcecloud.cfs.v20190719.models.UpdateCfsRuleResponse`

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

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
from common.cmp.cloud_apis.resource_apis.tcecloud.tcr.v20190924 import models


class TcrClient(AbstractClient):
    _apiVersion = "2019-09-24"
    _endpoint = "tcr.api3.{{conf.main_domain}}"

    def BatchDeleteFavorRepositoryPersonal(self, request):
        """批量删除个人收藏仓库

        :param request: 调用BatchDeleteFavorRepositoryPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.BatchDeleteFavorRepositoryPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.BatchDeleteFavorRepositoryPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("BatchDeleteFavorRepositoryPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.BatchDeleteFavorRepositoryPersonalResponse()
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

    def BatchDeleteImagePersonal(self, request):
        """用于在个人版镜像仓库中批量删除Tag

        :param request: 调用BatchDeleteImagePersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.BatchDeleteImagePersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.BatchDeleteImagePersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("BatchDeleteImagePersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.BatchDeleteImagePersonalResponse()
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

    def BatchDeleteRepositoryPersonal(self, request):
        """用于个人版镜像仓库中批量删除镜像仓库

        :param request: 调用BatchDeleteRepositoryPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.BatchDeleteRepositoryPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.BatchDeleteRepositoryPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("BatchDeleteRepositoryPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.BatchDeleteRepositoryPersonalResponse()
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

    def CreateApplicationTokenPersonal(self, request):
        """用于创建第三方应用访问凭证

        :param request: 调用CreateApplicationTokenPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.CreateApplicationTokenPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.CreateApplicationTokenPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateApplicationTokenPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateApplicationTokenPersonalResponse()
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

    def CreateApplicationTriggerPersonal(self, request):
        """用于创建应用更新触发器

        :param request: 调用CreateApplicationTriggerPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.CreateApplicationTriggerPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.CreateApplicationTriggerPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateApplicationTriggerPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateApplicationTriggerPersonalResponse()
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

    def CreateFavorRepositoryPersonal(self, request):
        """创建个人收藏仓库

        :param request: 调用CreateFavorRepositoryPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.CreateFavorRepositoryPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.CreateFavorRepositoryPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateFavorRepositoryPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateFavorRepositoryPersonalResponse()
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

    def CreateImageBuildPersonal(self, request):
        """创建镜像构建规则

        :param request: 调用CreateImageBuildPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.CreateImageBuildPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.CreateImageBuildPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateImageBuildPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateImageBuildPersonalResponse()
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

    def CreateImageBuildTaskDockerPersonal(self, request):
        """创建基于Dockerfile的镜像构建任务

        :param request: 调用CreateImageBuildTaskDockerPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.CreateImageBuildTaskDockerPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.CreateImageBuildTaskDockerPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateImageBuildTaskDockerPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateImageBuildTaskDockerPersonalResponse()
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

    def CreateImageBuildTaskManuallyPersonal(self, request):
        """创建手动执行的镜像构建任务

        :param request: 调用CreateImageBuildTaskManuallyPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.CreateImageBuildTaskManuallyPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.CreateImageBuildTaskManuallyPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateImageBuildTaskManuallyPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateImageBuildTaskManuallyPersonalResponse()
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

    def CreateImageLifecyclePersonal(self, request):
        """用于在个人版中创建清理策略

        :param request: 调用CreateImageLifecyclePersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.CreateImageLifecyclePersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.CreateImageLifecyclePersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateImageLifecyclePersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateImageLifecyclePersonalResponse()
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

    def CreateInstance(self, request):
        """创建实例

        :param request: 调用CreateInstance所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.CreateInstanceRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.CreateInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateInstanceResponse()
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

    def CreateInstanceToken(self, request):
        """获取临时登录密码

        :param request: 调用CreateInstanceToken所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.CreateInstanceTokenRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.CreateInstanceTokenResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateInstanceToken", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateInstanceTokenResponse()
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

    def CreateNamespacePersonal(self, request):
        """创建个人版镜像仓库命名空间，此命名空间全局唯一

        :param request: 调用CreateNamespacePersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.CreateNamespacePersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.CreateNamespacePersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateNamespacePersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateNamespacePersonalResponse()
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

    def CreateRepo(self, request):
        """用于在共享版仓库中创建镜像仓库

        :param request: 调用CreateRepo所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.CreateRepoRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.CreateRepoResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateRepo", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateRepoResponse()
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

    def CreateRepositoryPersonal(self, request):
        """用于在个人版仓库中创建镜像仓库

        :param request: 调用CreateRepositoryPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.CreateRepositoryPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.CreateRepositoryPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateRepositoryPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateRepositoryPersonalResponse()
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

    def CreateSecurityPolicies(self, request):
        """创建实例公网访问白名单策略

        :param request: 调用CreateSecurityPolicies所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.CreateSecurityPoliciesRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.CreateSecurityPoliciesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateSecurityPolicies", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateSecurityPoliciesResponse()
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

    def CreateSecurityPolicy(self, request):
        """创建实例公网访问白名单策略

        :param request: 调用CreateSecurityPolicy所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.CreateSecurityPolicyRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.CreateSecurityPolicyResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateSecurityPolicy", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateSecurityPolicyResponse()
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

    def CreateSourceCodeAuthPersonal(self, request):
        """创建源代码授权

        :param request: 调用CreateSourceCodeAuthPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.CreateSourceCodeAuthPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.CreateSourceCodeAuthPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateSourceCodeAuthPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateSourceCodeAuthPersonalResponse()
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

    def CreateUserPersonal(self, request):
        """创建个人用户

        :param request: 调用CreateUserPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.CreateUserPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.CreateUserPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateUserPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateUserPersonalResponse()
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

    def DeleteApplicationTriggerPersonal(self, request):
        """用于删除应用更新触发器

        :param request: 调用DeleteApplicationTriggerPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DeleteApplicationTriggerPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DeleteApplicationTriggerPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteApplicationTriggerPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteApplicationTriggerPersonalResponse()
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

    def DeleteFavorRepositoryPersonal(self, request):
        """删除个人收藏仓库

        :param request: 调用DeleteFavorRepositoryPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DeleteFavorRepositoryPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DeleteFavorRepositoryPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteFavorRepositoryPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteFavorRepositoryPersonalResponse()
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

    def DeleteFavorRepositoryRegionPersonal(self, request):
        """删除指定地域所有个人收藏仓库

        :param request: 调用DeleteFavorRepositoryRegionPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DeleteFavorRepositoryRegionPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DeleteFavorRepositoryRegionPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteFavorRepositoryRegionPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteFavorRepositoryRegionPersonalResponse()
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

    def DeleteImageBuildPersonal(self, request):
        """删除镜像构建规则

        :param request: 调用DeleteImageBuildPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DeleteImageBuildPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DeleteImageBuildPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteImageBuildPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteImageBuildPersonalResponse()
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

    def DeleteImageBuildTaskPersonal(self, request):
        """删除镜像构建任务

        :param request: 调用DeleteImageBuildTaskPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DeleteImageBuildTaskPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DeleteImageBuildTaskPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteImageBuildTaskPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteImageBuildTaskPersonalResponse()
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

    def DeleteImageLifecycleGlobalPersonal(self, request):
        """用于删除个人版全局镜像版本自动清理策略

        :param request: 调用DeleteImageLifecycleGlobalPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DeleteImageLifecycleGlobalPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DeleteImageLifecycleGlobalPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteImageLifecycleGlobalPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteImageLifecycleGlobalPersonalResponse()
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

    def DeleteImageLifecyclePersonal(self, request):
        """用于在个人版镜像仓库中删除仓库Tag自动清理策略

        :param request: 调用DeleteImageLifecyclePersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DeleteImageLifecyclePersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DeleteImageLifecyclePersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteImageLifecyclePersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteImageLifecyclePersonalResponse()
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

    def DeleteImagePersonal(self, request):
        """用于在个人版中删除tag

        :param request: 调用DeleteImagePersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DeleteImagePersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DeleteImagePersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteImagePersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteImagePersonalResponse()
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

    def DeleteInstance(self, request):
        """删除镜像仓库企业版实例

        :param request: 调用DeleteInstance所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DeleteInstanceRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DeleteInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteInstanceResponse()
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

    def DeleteNamespacePersonal(self, request):
        """删除共享版命名空间

        :param request: 调用DeleteNamespacePersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DeleteNamespacePersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DeleteNamespacePersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteNamespacePersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteNamespacePersonalResponse()
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

    def DeleteRepositoryPersonal(self, request):
        """用于个人版镜像仓库中删除

        :param request: 调用DeleteRepositoryPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DeleteRepositoryPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DeleteRepositoryPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteRepositoryPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteRepositoryPersonalResponse()
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

    def DeleteSecurityPolicy(self, request):
        """删除实例公网访问白名单策略

        :param request: 调用DeleteSecurityPolicy所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DeleteSecurityPolicyRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DeleteSecurityPolicyResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteSecurityPolicy", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteSecurityPolicyResponse()
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

    def DeleteSourceCodeAuthPersonal(self, request):
        """删除源代码授权

        :param request: 调用DeleteSourceCodeAuthPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DeleteSourceCodeAuthPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DeleteSourceCodeAuthPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteSourceCodeAuthPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteSourceCodeAuthPersonalResponse()
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

    def DescribeApplicationTokenPersonal(self, request):
        """用于获取第三方应用访问凭证

        :param request: 调用DescribeApplicationTokenPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeApplicationTokenPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeApplicationTokenPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeApplicationTokenPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeApplicationTokenPersonalResponse()
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

    def DescribeApplicationTriggerLogPersonal(self, request):
        """用于查询应用更新触发器触发日志

        :param request: 调用DescribeApplicationTriggerLogPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeApplicationTriggerLogPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeApplicationTriggerLogPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeApplicationTriggerLogPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeApplicationTriggerLogPersonalResponse()
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

    def DescribeApplicationTriggerPersonal(self, request):
        """用于查询应用更新触发器

        :param request: 调用DescribeApplicationTriggerPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeApplicationTriggerPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeApplicationTriggerPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeApplicationTriggerPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeApplicationTriggerPersonalResponse()
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

    def DescribeDockerHubImagePersonal(self, request):
        """查询DockerHub镜像列表

        :param request: 调用DescribeDockerHubImagePersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeDockerHubImagePersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeDockerHubImagePersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDockerHubImagePersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDockerHubImagePersonalResponse()
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

    def DescribeDockerHubRepositoryInfoPersonal(self, request):
        """查询DockerHub仓库信息

        :param request: 调用DescribeDockerHubRepositoryInfoPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeDockerHubRepositoryInfoPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeDockerHubRepositoryInfoPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDockerHubRepositoryInfoPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDockerHubRepositoryInfoPersonalResponse()
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

    def DescribeDockerHubRepositoryPersonal(self, request):
        """查询DockerHub仓库列表

        :param request: 调用DescribeDockerHubRepositoryPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeDockerHubRepositoryPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeDockerHubRepositoryPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDockerHubRepositoryPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDockerHubRepositoryPersonalResponse()
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

    def DescribeExternalEndpointStatus(self, request):
        """查询实例公网访问入口状态

        :param request: 调用DescribeExternalEndpointStatus所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeExternalEndpointStatusRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeExternalEndpointStatusResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeExternalEndpointStatus", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeExternalEndpointStatusResponse()
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

    def DescribeFavorRepositoryPersonal(self, request):
        """查询个人收藏仓库

        :param request: 调用DescribeFavorRepositoryPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeFavorRepositoryPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeFavorRepositoryPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeFavorRepositoryPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeFavorRepositoryPersonalResponse()
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

    def DescribeImageBuildPersonal(self, request):
        """查询镜像构建规则

        :param request: 调用DescribeImageBuildPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeImageBuildPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeImageBuildPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeImageBuildPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeImageBuildPersonalResponse()
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

    def DescribeImageBuildTaskLogInfoPersonal(self, request):
        """查询镜像构建任务日志信息

        :param request: 调用DescribeImageBuildTaskLogInfoPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeImageBuildTaskLogInfoPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeImageBuildTaskLogInfoPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeImageBuildTaskLogInfoPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeImageBuildTaskLogInfoPersonalResponse()
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

    def DescribeImageBuildTaskLogPersonal(self, request):
        """查询镜像构建任务日志

        :param request: 调用DescribeImageBuildTaskLogPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeImageBuildTaskLogPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeImageBuildTaskLogPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeImageBuildTaskLogPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeImageBuildTaskLogPersonalResponse()
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

    def DescribeImageConfigPersonal(self, request):
        """用于查询镜像版本配置信息

        :param request: 调用DescribeImageConfigPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeImageConfigPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeImageConfigPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeImageConfigPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeImageConfigPersonalResponse()
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

    def DescribeImageFilterPersonal(self, request):
        """用于在个人版中查询与指定tag镜像内容相同的tag列表

        :param request: 调用DescribeImageFilterPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeImageFilterPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeImageFilterPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeImageFilterPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeImageFilterPersonalResponse()
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

    def DescribeImageLifecycleGlobalPersonal(self, request):
        """用于获取个人版全局镜像版本自动清理策略

        :param request: 调用DescribeImageLifecycleGlobalPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeImageLifecycleGlobalPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeImageLifecycleGlobalPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeImageLifecycleGlobalPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeImageLifecycleGlobalPersonalResponse()
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

    def DescribeImageLifecyclePersonal(self, request):
        """用于获取个人版仓库中自动清理策略

        :param request: 调用DescribeImageLifecyclePersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeImageLifecyclePersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeImageLifecyclePersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeImageLifecyclePersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeImageLifecyclePersonalResponse()
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

    def DescribeImagePersonal(self, request):
        """用于获取个人版镜像仓库tag列表

        :param request: 调用DescribeImagePersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeImagePersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeImagePersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeImagePersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeImagePersonalResponse()
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

    def DescribeInstanceStatus(self, request):
        """查询实例当前状态以及过程信息

        :param request: 调用DescribeInstanceStatus所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeInstanceStatusRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeInstanceStatusResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstanceStatus", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstanceStatusResponse()
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

    def DescribeInstances(self, request):
        """查询实例信息

        :param request: 调用DescribeInstances所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeInstancesRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstancesResponse()
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

    def DescribeInternalEndpoints(self, request):
        """查询实例内网访问VPC链接

        :param request: 调用DescribeInternalEndpoints所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeInternalEndpointsRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeInternalEndpointsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInternalEndpoints", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInternalEndpointsResponse()
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

    def DescribeNamespacePersonal(self, request):
        """查询个人版命名空间信息

        :param request: 调用DescribeNamespacePersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeNamespacePersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeNamespacePersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeNamespacePersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeNamespacePersonalResponse()
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

    def DescribeRegions(self, request):
        """用于在TCR中获取可用区域

        :param request: 调用DescribeRegions所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeRegionsRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeRegionsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRegions", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRegionsResponse()
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

    def DescribeRepositoryAllPersonal(self, request):
        """用于查询所有可访问的镜像仓库

        :param request: 调用DescribeRepositoryAllPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeRepositoryAllPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeRepositoryAllPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRepositoryAllPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRepositoryAllPersonalResponse()
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

    def DescribeRepositoryFilterPersonal(self, request):
        """用于在个人版镜像仓库中，获取满足输入搜索条件的用户镜像仓库

        :param request: 调用DescribeRepositoryFilterPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeRepositoryFilterPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeRepositoryFilterPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRepositoryFilterPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRepositoryFilterPersonalResponse()
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

    def DescribeRepositoryOwnerPersonal(self, request):
        """用于在个人版中获取用户全部的镜像仓库列表

        :param request: 调用DescribeRepositoryOwnerPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeRepositoryOwnerPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeRepositoryOwnerPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRepositoryOwnerPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRepositoryOwnerPersonalResponse()
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

    def DescribeRepositoryPersonal(self, request):
        """查询个人版仓库信息

        :param request: 调用DescribeRepositoryPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeRepositoryPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeRepositoryPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRepositoryPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRepositoryPersonalResponse()
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

    def DescribeSecurityPolicies(self, request):
        """查询实例公网访问白名单策略

        :param request: 调用DescribeSecurityPolicies所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeSecurityPoliciesRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeSecurityPoliciesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeSecurityPolicies", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeSecurityPoliciesResponse()
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

    def DescribeSourceCodeAuthPersonal(self, request):
        """查询源代码授权

        :param request: 调用DescribeSourceCodeAuthPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeSourceCodeAuthPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeSourceCodeAuthPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeSourceCodeAuthPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeSourceCodeAuthPersonalResponse()
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

    def DescribeSourceCodeAuthUserInfoPersonal(self, request):
        """查询源代码授权用户信息

        :param request: 调用DescribeSourceCodeAuthUserInfoPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeSourceCodeAuthUserInfoPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeSourceCodeAuthUserInfoPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeSourceCodeAuthUserInfoPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeSourceCodeAuthUserInfoPersonalResponse()
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

    def DescribeSourceCodeRepositoryBranchPersonal(self, request):
        """查询源代码仓库分支列表

        :param request: 调用DescribeSourceCodeRepositoryBranchPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeSourceCodeRepositoryBranchPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeSourceCodeRepositoryBranchPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeSourceCodeRepositoryBranchPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeSourceCodeRepositoryBranchPersonalResponse()
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

    def DescribeSourceCodeRepositoryPersonal(self, request):
        """查询源代码仓库列表

        :param request: 调用DescribeSourceCodeRepositoryPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeSourceCodeRepositoryPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeSourceCodeRepositoryPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeSourceCodeRepositoryPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeSourceCodeRepositoryPersonalResponse()
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

    def DescribeUserPersonal(self, request):
        """查询个人用户信息

        :param request: 调用DescribeUserPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeUserPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeUserPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeUserPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeUserPersonalResponse()
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

    def DescribeUserQuotaPersonal(self, request):
        """查询个人用户配额

        :param request: 调用DescribeUserQuotaPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DescribeUserQuotaPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DescribeUserQuotaPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeUserQuotaPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeUserQuotaPersonalResponse()
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

    def DuplicateImagePersonal(self, request):
        """用于在个人版镜像仓库中复制镜像版本

        :param request: 调用DuplicateImagePersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.DuplicateImagePersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.DuplicateImagePersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DuplicateImagePersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DuplicateImagePersonalResponse()
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

    def ForwardRequest(self, request):
        """TCR 代理转发接口

        :param request: 调用ForwardRequest所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.ForwardRequestRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.ForwardRequestResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ForwardRequest", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ForwardRequestResponse()
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

    def ManageExternalEndpoint(self, request):
        """管理实例公网访问

        :param request: 调用ManageExternalEndpoint所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.ManageExternalEndpointRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.ManageExternalEndpointResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ManageExternalEndpoint", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ManageExternalEndpointResponse()
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

    def ManageImageLifecycleGlobalPersonal(self, request):
        """用于设置个人版全局镜像版本自动清理策略

        :param request: 调用ManageImageLifecycleGlobalPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.ManageImageLifecycleGlobalPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.ManageImageLifecycleGlobalPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ManageImageLifecycleGlobalPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ManageImageLifecycleGlobalPersonalResponse()
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

    def ManageInternalEndpoint(self, request):
        """管理实例内网访问VPC链接

        :param request: 调用ManageInternalEndpoint所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.ManageInternalEndpointRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.ManageInternalEndpointResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ManageInternalEndpoint", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ManageInternalEndpointResponse()
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

    def ManageReplication(self, request):
        """管理实例同步

        :param request: 调用ManageReplication所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.ManageReplicationRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.ManageReplicationResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ManageReplication", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ManageReplicationResponse()
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

    def ModifyApplicationTriggerPersonal(self, request):
        """用于修改应用更新触发器

        :param request: 调用ModifyApplicationTriggerPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.ModifyApplicationTriggerPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.ModifyApplicationTriggerPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyApplicationTriggerPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyApplicationTriggerPersonalResponse()
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

    def ModifyImageBuildPersonal(self, request):
        """修改镜像构建规则

        :param request: 调用ModifyImageBuildPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.ModifyImageBuildPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.ModifyImageBuildPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyImageBuildPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyImageBuildPersonalResponse()
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

    def ModifyInstance(self, request):
        """更新实例信息

        :param request: 调用ModifyInstance所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.ModifyInstanceRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.ModifyInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyInstanceResponse()
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

    def ModifyRepositoryAccessPersonal(self, request):
        """用于更新个人版镜像仓库的访问属性

        :param request: 调用ModifyRepositoryAccessPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.ModifyRepositoryAccessPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.ModifyRepositoryAccessPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyRepositoryAccessPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyRepositoryAccessPersonalResponse()
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

    def ModifyRepositoryInfoPersonal(self, request):
        """用于在个人版镜像仓库中更新容器镜像描述

        :param request: 调用ModifyRepositoryInfoPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.ModifyRepositoryInfoPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.ModifyRepositoryInfoPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyRepositoryInfoPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyRepositoryInfoPersonalResponse()
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

    def ModifySecurityPolicy(self, request):
        """更新实例公网访问白名单

        :param request: 调用ModifySecurityPolicy所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.ModifySecurityPolicyRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.ModifySecurityPolicyResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifySecurityPolicy", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifySecurityPolicyResponse()
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

    def ModifyUserPasswordPersonal(self, request):
        """修改个人用户登录密码

        :param request: 调用ModifyUserPasswordPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.ModifyUserPasswordPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.ModifyUserPasswordPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyUserPasswordPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyUserPasswordPersonalResponse()
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

    def ValidateApplicationTokenPersonal(self, request):
        """用于验证第三方应用访问凭证

        :param request: 调用ValidateApplicationTokenPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.ValidateApplicationTokenPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.ValidateApplicationTokenPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ValidateApplicationTokenPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ValidateApplicationTokenPersonalResponse()
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

    def ValidateGitHubAuthPersonal(self, request):
        """验证GitHub授权

        :param request: 调用ValidateGitHubAuthPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.ValidateGitHubAuthPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.ValidateGitHubAuthPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ValidateGitHubAuthPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ValidateGitHubAuthPersonalResponse()
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

    def ValidateNamespaceExistPersonal(self, request):
        """查询个人版用户命名空间是否存在

        :param request: 调用ValidateNamespaceExistPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.ValidateNamespaceExistPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.ValidateNamespaceExistPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ValidateNamespaceExistPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ValidateNamespaceExistPersonalResponse()
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

    def ValidateRepositoryExistPersonal(self, request):
        """用于判断个人版仓库是否存在

        :param request: 调用ValidateRepositoryExistPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.ValidateRepositoryExistPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.ValidateRepositoryExistPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ValidateRepositoryExistPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ValidateRepositoryExistPersonalResponse()
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

    def ValidateUserPersonal(self, request):
        """验证个人用户

        :param request: 调用ValidateUserPersonal所需参数的结构体。
        :type request: :class:`tcecloud.tcr.v20190924.models.ValidateUserPersonalRequest`
        :rtype: :class:`tcecloud.tcr.v20190924.models.ValidateUserPersonalResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ValidateUserPersonal", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ValidateUserPersonalResponse()
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

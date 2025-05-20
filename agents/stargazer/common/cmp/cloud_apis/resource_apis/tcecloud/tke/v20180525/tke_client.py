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
from common.cmp.cloud_apis.resource_apis.tcecloud.tke.v20180525 import models


class TkeClient(AbstractClient):
    _apiVersion = "2018-05-25"
    _endpoint = "tke.api3.{{conf.main_domain}}"

    def AddAlarmPolicy(self, request):
        """添加告警策略

        :param request: 调用AddAlarmPolicy所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.AddAlarmPolicyRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.AddAlarmPolicyResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AddAlarmPolicy", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AddAlarmPolicyResponse()
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

    def AddClusterCIDRToCcn(self, request):
        """添加TKE集群CIDR到云联网

        :param request: 调用AddClusterCIDRToCcn所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.AddClusterCIDRToCcnRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.AddClusterCIDRToCcnResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AddClusterCIDRToCcn", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AddClusterCIDRToCcnResponse()
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

    def AddClusterCIDRToVbc(self, request):
        """发布tke集群cidr到云联网

        :param request: 调用AddClusterCIDRToVbc所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.AddClusterCIDRToVbcRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.AddClusterCIDRToVbcResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AddClusterCIDRToVbc", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AddClusterCIDRToVbcResponse()
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

    def AddClusterInstances(self, request):
        """扩展集群节点，API 3.0

        :param request: 调用AddClusterInstances所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.AddClusterInstancesRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.AddClusterInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AddClusterInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AddClusterInstancesResponse()
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

    def AddExistedInstances(self, request):
        """添加已经存在的实例到集群

        :param request: 调用AddExistedInstances所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.AddExistedInstancesRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.AddExistedInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AddExistedInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AddExistedInstancesResponse()
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

    def CheckClusterCIDR(self, request):
        """检查集群的CIDR是否冲突

        :param request: 调用CheckClusterCIDR所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.CheckClusterCIDRRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.CheckClusterCIDRResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CheckClusterCIDR", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CheckClusterCIDRResponse()
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

    def CheckClusterHostName(self, request):
        """检查集群节点主机名称，判断节点主机名称是否符合规则，是否可以加入集群。

        :param request: 调用CheckClusterHostName所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.CheckClusterHostNameRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.CheckClusterHostNameResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CheckClusterHostName", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CheckClusterHostNameResponse()
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

    def CheckClusterImage(self, request):
        """检查镜像是否支持设置为集群镜像

        :param request: 调用CheckClusterImage所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.CheckClusterImageRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.CheckClusterImageResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CheckClusterImage", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CheckClusterImageResponse()
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

    def CheckInstancesUpgradeAble(self, request):
        """检查给定节点列表中哪些是可升级的

        :param request: 调用CheckInstancesUpgradeAble所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.CheckInstancesUpgradeAbleRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.CheckInstancesUpgradeAbleResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CheckInstancesUpgradeAble", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CheckInstancesUpgradeAbleResponse()
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

    def CheckLogCollectorHostPath(self, request):
        """检查主机路径

        :param request: 调用CheckLogCollectorHostPath所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.CheckLogCollectorHostPathRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.CheckLogCollectorHostPathResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CheckLogCollectorHostPath", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CheckLogCollectorHostPathResponse()
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

    def CheckLogCollectorName(self, request):
        """通过名称检查日志采集规则是否存在

        :param request: 调用CheckLogCollectorName所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.CheckLogCollectorNameRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.CheckLogCollectorNameResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CheckLogCollectorName", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CheckLogCollectorNameResponse()
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

    def CreateCluster(self, request):
        """创建集群

        :param request: 调用CreateCluster所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.CreateClusterRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.CreateClusterResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateCluster", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateClusterResponse()
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

    def CreateClusterAsGroup(self, request):
        """为已经存在的集群创建伸缩组

        :param request: 调用CreateClusterAsGroup所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.CreateClusterAsGroupRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.CreateClusterAsGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateClusterAsGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateClusterAsGroupResponse()
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

    def CreateClusterEndpoint(self, request):
        """创建集群访问端口(独立集群开启内网/外网访问，托管集群支持开启内网访问)

        :param request: 调用CreateClusterEndpoint所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.CreateClusterEndpointRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.CreateClusterEndpointResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateClusterEndpoint", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateClusterEndpointResponse()
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

    def CreateClusterEndpointVip(self, request):
        """创建托管集群外网访问端口（老的方式，仅支持托管集群外网端口）

        :param request: 调用CreateClusterEndpointVip所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.CreateClusterEndpointVipRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.CreateClusterEndpointVipResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateClusterEndpointVip", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateClusterEndpointVipResponse()
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

    def CreateClusterInstances(self, request):
        """扩展(新建)集群节点

        :param request: 调用CreateClusterInstances所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.CreateClusterInstancesRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.CreateClusterInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateClusterInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateClusterInstancesResponse()
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

    def CreateClusterRoute(self, request):
        """创建集群路由

        :param request: 调用CreateClusterRoute所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.CreateClusterRouteRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.CreateClusterRouteResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateClusterRoute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateClusterRouteResponse()
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

    def CreateClusterRouteTable(self, request):
        """创建集群路由表

        :param request: 调用CreateClusterRouteTable所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.CreateClusterRouteTableRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.CreateClusterRouteTableResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateClusterRouteTable", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateClusterRouteTableResponse()
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

    def CreateIndependentCluster(self, request):
        """创建独立集群

        :param request: 调用CreateIndependentCluster所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.CreateIndependentClusterRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.CreateIndependentClusterResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateIndependentCluster", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateIndependentClusterResponse()
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

    def CreateTKECluster(self, request):
        """创建TKE集群

        :param request: 调用CreateTKECluster所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.CreateTKEClusterRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.CreateTKEClusterResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateTKECluster", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateTKEClusterResponse()
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

    def DeleteAlarmPolicies(self, request):
        """删除告警策略，支持批量删除

        :param request: 调用DeleteAlarmPolicies所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DeleteAlarmPoliciesRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DeleteAlarmPoliciesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteAlarmPolicies", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteAlarmPoliciesResponse()
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

    def DeleteCluster(self, request):
        """删除集群(YUNAPI V3版本)

        :param request: 调用DeleteCluster所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DeleteClusterRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DeleteClusterResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteCluster", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteClusterResponse()
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

    def DeleteClusterAsGroups(self, request):
        """删除集群伸缩组

        :param request: 调用DeleteClusterAsGroups所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DeleteClusterAsGroupsRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DeleteClusterAsGroupsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteClusterAsGroups", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteClusterAsGroupsResponse()
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

    def DeleteClusterCIDRFromCcn(self, request):
        """从云联网删除集群CIDR的路由

        :param request: 调用DeleteClusterCIDRFromCcn所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DeleteClusterCIDRFromCcnRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DeleteClusterCIDRFromCcnResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteClusterCIDRFromCcn", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteClusterCIDRFromCcnResponse()
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

    def DeleteClusterCIDRFromVbc(self, request):
        """从云联网删除集群CIDR

        :param request: 调用DeleteClusterCIDRFromVbc所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DeleteClusterCIDRFromVbcRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DeleteClusterCIDRFromVbcResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteClusterCIDRFromVbc", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteClusterCIDRFromVbcResponse()
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

    def DeleteClusterEndpoint(self, request):
        """删除集群访问端口(独立集群开启内网/外网访问，托管集群支持开启内网访问)

        :param request: 调用DeleteClusterEndpoint所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DeleteClusterEndpointRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DeleteClusterEndpointResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteClusterEndpoint", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteClusterEndpointResponse()
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

    def DeleteClusterEndpointVip(self, request):
        """删除托管集群外网访问端口（老的方式，仅支持托管集群外网端口）

        :param request: 调用DeleteClusterEndpointVip所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DeleteClusterEndpointVipRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DeleteClusterEndpointVipResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteClusterEndpointVip", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteClusterEndpointVipResponse()
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

    def DeleteClusterInstances(self, request):
        """删除集群中的实例

        :param request: 调用DeleteClusterInstances所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DeleteClusterInstancesRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DeleteClusterInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteClusterInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteClusterInstancesResponse()
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

    def DeleteClusterRoute(self, request):
        """删除集群路由

        :param request: 调用DeleteClusterRoute所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DeleteClusterRouteRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DeleteClusterRouteResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteClusterRoute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteClusterRouteResponse()
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

    def DeleteClusterRouteTable(self, request):
        """删除集群路由表

        :param request: 调用DeleteClusterRouteTable所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DeleteClusterRouteTableRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DeleteClusterRouteTableResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteClusterRouteTable", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteClusterRouteTableResponse()
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

    def DescribeAlarmPolicies(self, request):
        """获取告警策略列表

        :param request: 调用DescribeAlarmPolicies所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeAlarmPoliciesRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeAlarmPoliciesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeAlarmPolicies", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAlarmPoliciesResponse()
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

    def DescribeAvailableClusterVersion(self, request):
        """获取集群可以升级的所有版本

        :param request: 调用DescribeAvailableClusterVersion所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeAvailableClusterVersionRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeAvailableClusterVersionResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeAvailableClusterVersion", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAvailableClusterVersionResponse()
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

    def DescribeCcnInstances(self, request):
        """用于查询vpc是否加入云联网

        :param request: 调用DescribeCcnInstances所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeCcnInstancesRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeCcnInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeCcnInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCcnInstancesResponse()
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

    def DescribeCcnRoutes(self, request):
        """用于查询tke集群CIDR是否加入云联网

        :param request: 调用DescribeCcnRoutes所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeCcnRoutesRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeCcnRoutesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeCcnRoutes", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCcnRoutesResponse()
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

    def DescribeClsLogSets(self, request):
        """列出CLS日志集

        :param request: 调用DescribeClsLogSets所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeClsLogSetsRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeClsLogSetsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClsLogSets", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClsLogSetsResponse()
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

    def DescribeClsLogTopics(self, request):
        """列出CLS日志主题

        :param request: 调用DescribeClsLogTopics所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeClsLogTopicsRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeClsLogTopicsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClsLogTopics", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClsLogTopicsResponse()
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

    def DescribeClusterAsGroupOption(self, request):
        """集群弹性伸缩配置

        :param request: 调用DescribeClusterAsGroupOption所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeClusterAsGroupOptionRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeClusterAsGroupOptionResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClusterAsGroupOption", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClusterAsGroupOptionResponse()
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

    def DescribeClusterAsGroups(self, request):
        """集群关联的伸缩组列表

        :param request: 调用DescribeClusterAsGroups所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeClusterAsGroupsRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeClusterAsGroupsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClusterAsGroups", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClusterAsGroupsResponse()
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

    def DescribeClusterAvailableExtraArgs(self, request):
        """查询集群可用的自定义参数

        :param request: 调用DescribeClusterAvailableExtraArgs所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeClusterAvailableExtraArgsRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeClusterAvailableExtraArgsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClusterAvailableExtraArgs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClusterAvailableExtraArgsResponse()
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

    def DescribeClusterCreateProgress(self, request):
        """获取集群创建进度

        :param request: 调用DescribeClusterCreateProgress所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeClusterCreateProgressRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeClusterCreateProgressResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClusterCreateProgress", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClusterCreateProgressResponse()
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

    def DescribeClusterEndpointStatus(self, request):
        """查询集群访问端口状态(独立集群开启内网/外网访问，托管集群支持开启内网访问)

        :param request: 调用DescribeClusterEndpointStatus所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeClusterEndpointStatusRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeClusterEndpointStatusResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClusterEndpointStatus", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClusterEndpointStatusResponse()
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

    def DescribeClusterEndpointVipStatus(self, request):
        """查询集群开启端口流程状态(仅支持托管集群外网端口)

        :param request: 调用DescribeClusterEndpointVipStatus所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeClusterEndpointVipStatusRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeClusterEndpointVipStatusResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClusterEndpointVipStatus", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClusterEndpointVipStatusResponse()
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

    def DescribeClusterExtraArgs(self, request):
        """查询集群自定义参数

        :param request: 调用DescribeClusterExtraArgs所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeClusterExtraArgsRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeClusterExtraArgsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClusterExtraArgs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClusterExtraArgsResponse()
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

    def DescribeClusterHealthyStatus(self, request):
        """描述集群目前的健康状态

        :param request: 调用DescribeClusterHealthyStatus所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeClusterHealthyStatusRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeClusterHealthyStatusResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClusterHealthyStatus", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClusterHealthyStatusResponse()
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

    def DescribeClusterInspectionOverviews(self, request):
        """获得集群巡检报告列表

        :param request: 调用DescribeClusterInspectionOverviews所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeClusterInspectionOverviewsRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeClusterInspectionOverviewsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClusterInspectionOverviews", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClusterInspectionOverviewsResponse()
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

    def DescribeClusterInspectionReport(self, request):
        """获得集群巡检报告页详情

        :param request: 调用DescribeClusterInspectionReport所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeClusterInspectionReportRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeClusterInspectionReportResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClusterInspectionReport", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClusterInspectionReportResponse()
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

    def DescribeClusterInspections(self, request):
        """集群巡检概览

        :param request: 调用DescribeClusterInspections所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeClusterInspectionsRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeClusterInspectionsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClusterInspections", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClusterInspectionsResponse()
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

    def DescribeClusterInstanceIds(self, request):
        """获取集群节点ID列表【仅内部使用】

        :param request: 调用DescribeClusterInstanceIds所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeClusterInstanceIdsRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeClusterInstanceIdsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClusterInstanceIds", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClusterInstanceIdsResponse()
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

    def DescribeClusterInstances(self, request):
        """查询集群下节点实例信息

        :param request: 调用DescribeClusterInstances所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeClusterInstancesRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeClusterInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClusterInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClusterInstancesResponse()
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

    def DescribeClusterPods(self, request):
        """该接口获取集群内Pod相关的详细描述信息，参考kubernetes API获取pod，只对内部短期使用

        :param request: 调用DescribeClusterPods所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeClusterPodsRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeClusterPodsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClusterPods", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClusterPodsResponse()
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

    def DescribeClusterRouteTables(self, request):
        """查询集群路由表

        :param request: 调用DescribeClusterRouteTables所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeClusterRouteTablesRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeClusterRouteTablesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClusterRouteTables", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClusterRouteTablesResponse()
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

    def DescribeClusterRoutes(self, request):
        """查询集群路由

        :param request: 调用DescribeClusterRoutes所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeClusterRoutesRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeClusterRoutesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClusterRoutes", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClusterRoutesResponse()
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

    def DescribeClusterSecurity(self, request):
        """集群的密钥信息

        :param request: 调用DescribeClusterSecurity所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeClusterSecurityRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeClusterSecurityResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClusterSecurity", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClusterSecurityResponse()
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

    def DescribeClusterServices(self, request):
        """该接口获取集群内Service相关的详细描述信息，参考kubernetes API获取Service，只对内部短期使用

        :param request: 调用DescribeClusterServices所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeClusterServicesRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeClusterServicesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClusterServices", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClusterServicesResponse()
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

    def DescribeClusterStatus(self, request):
        """查看集群状态列表【非对外接口】

        :param request: 调用DescribeClusterStatus所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeClusterStatusRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeClusterStatusResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClusterStatus", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClusterStatusResponse()
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

    def DescribeClusters(self, request):
        """查询集群列表

        :param request: 调用DescribeClusters所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeClustersRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeClustersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClusters", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClustersResponse()
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

    def DescribeClustersResourceStatus(self, request):
        """获取集群资源状态

        :param request: 调用DescribeClustersResourceStatus所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeClustersResourceStatusRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeClustersResourceStatusResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClustersResourceStatus", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClustersResourceStatusResponse()
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

    def DescribeExistedInstances(self, request):
        """查询已经存在的节点，判断是否可以加入集群

        :param request: 调用DescribeExistedInstances所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeExistedInstancesRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeExistedInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeExistedInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeExistedInstancesResponse()
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

    def DescribeFlowIdStatus(self, request):
        """查询集群开启端口流程状态(仅支持托管集群外网端口)

        :param request: 调用DescribeFlowIdStatus所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeFlowIdStatusRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeFlowIdStatusResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeFlowIdStatus", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeFlowIdStatusResponse()
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

    def DescribeImages(self, request):
        """获取镜像信息

        :param request: 调用DescribeImages所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeImagesRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeImagesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeImages", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeImagesResponse()
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

    def DescribeInstanceCreateProgress(self, request):
        """获取节点创建进度

        :param request: 调用DescribeInstanceCreateProgress所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeInstanceCreateProgressRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeInstanceCreateProgressResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstanceCreateProgress", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstanceCreateProgressResponse()
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

    def DescribeInstancesVersion(self, request):
        """worker节点的版本统计

        :param request: 调用DescribeInstancesVersion所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeInstancesVersionRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeInstancesVersionResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstancesVersion", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstancesVersionResponse()
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

    def DescribeQuota(self, request):
        """获取集群配额

        :param request: 调用DescribeQuota所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeQuotaRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeQuotaResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeQuota", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeQuotaResponse()
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
        """获取容器服务支持的所有地域

        :param request: 调用DescribeRegions所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeRegionsRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeRegionsResponse`

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

    def DescribeRouteTableConflicts(self, request):
        """查询路由表冲突列表

        :param request: 调用DescribeRouteTableConflicts所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeRouteTableConflictsRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeRouteTableConflictsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRouteTableConflicts", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRouteTableConflictsResponse()
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

    def DescribeUpgradeClusterProgress(self, request):
        """获取集群升级进度

        :param request: 调用DescribeUpgradeClusterProgress所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeUpgradeClusterProgressRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeUpgradeClusterProgressResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeUpgradeClusterProgress", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeUpgradeClusterProgressResponse()
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

    def DescribeVersions(self, request):
        """获取集群版本信息

        :param request: 调用DescribeVersions所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DescribeVersionsRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DescribeVersionsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeVersions", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeVersionsResponse()
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

    def DrainClusterNode(self, request):
        """驱逐集群中的节点

        :param request: 调用DrainClusterNode所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.DrainClusterNodeRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.DrainClusterNodeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DrainClusterNode", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DrainClusterNodeResponse()
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

    def EnableVpcPeerClusterRoutes(self, request):
        """启动对等连接容器路由

        :param request: 调用EnableVpcPeerClusterRoutes所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.EnableVpcPeerClusterRoutesRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.EnableVpcPeerClusterRoutesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("EnableVpcPeerClusterRoutes", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.EnableVpcPeerClusterRoutesResponse()
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
        """YUNAPI 转发请求给TKE APIServer接口

        :param request: 调用ForwardRequest所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.ForwardRequestRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.ForwardRequestResponse`

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

    def GetUpgradeClusterProgress(self, request):
        """返回当前集群升级进度

        :param request: 调用GetUpgradeClusterProgress所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.GetUpgradeClusterProgressRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.GetUpgradeClusterProgressResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetUpgradeClusterProgress", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetUpgradeClusterProgressResponse()
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

    def GetUpgradeInstanceProgress(self, request):
        """获得节点升级当前的进度

        :param request: 调用GetUpgradeInstanceProgress所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.GetUpgradeInstanceProgressRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.GetUpgradeInstanceProgressResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetUpgradeInstanceProgress", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetUpgradeInstanceProgressResponse()
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

    def GetVbcInstance(self, request):
        """查询vpc是否加入云联网

        :param request: 调用GetVbcInstance所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.GetVbcInstanceRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.GetVbcInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetVbcInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetVbcInstanceResponse()
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

    def GetVbcRoute(self, request):
        """查询tke集群cidr是否加入云联网

        :param request: 调用GetVbcRoute所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.GetVbcRouteRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.GetVbcRouteResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetVbcRoute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetVbcRouteResponse()
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

    def ModifyAlarmPolicy(self, request):
        """修改告警策略

        :param request: 调用ModifyAlarmPolicy所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.ModifyAlarmPolicyRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.ModifyAlarmPolicyResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyAlarmPolicy", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyAlarmPolicyResponse()
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

    def ModifyClusterAsGroupAttribute(self, request):
        """修改集群伸缩组属性

        :param request: 调用ModifyClusterAsGroupAttribute所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.ModifyClusterAsGroupAttributeRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.ModifyClusterAsGroupAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyClusterAsGroupAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyClusterAsGroupAttributeResponse()
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

    def ModifyClusterAsGroupOptionAttribute(self, request):
        """修改集群弹性伸缩属性

        :param request: 调用ModifyClusterAsGroupOptionAttribute所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.ModifyClusterAsGroupOptionAttributeRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.ModifyClusterAsGroupOptionAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyClusterAsGroupOptionAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyClusterAsGroupOptionAttributeResponse()
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

    def ModifyClusterAttribute(self, request):
        """修改集群属性

        :param request: 调用ModifyClusterAttribute所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.ModifyClusterAttributeRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.ModifyClusterAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyClusterAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyClusterAttributeResponse()
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

    def ModifyClusterEndpointSP(self, request):
        """修改托管集群外网端口的安全策略（老的方式，仅支持托管集群外网端口）

        :param request: 调用ModifyClusterEndpointSP所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.ModifyClusterEndpointSPRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.ModifyClusterEndpointSPResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyClusterEndpointSP", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyClusterEndpointSPResponse()
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

    def ModifyClusterImage(self, request):
        """修改集群镜像

        :param request: 调用ModifyClusterImage所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.ModifyClusterImageRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.ModifyClusterImageResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyClusterImage", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyClusterImageResponse()
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

    def ModifyClusterInspection(self, request):
        """更新集群巡检配置

        :param request: 调用ModifyClusterInspection所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.ModifyClusterInspectionRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.ModifyClusterInspectionResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyClusterInspection", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyClusterInspectionResponse()
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

    def ModifyClusterUpgradingState(self, request):
        """暂停或者取消集群升级

        :param request: 调用ModifyClusterUpgradingState所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.ModifyClusterUpgradingStateRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.ModifyClusterUpgradingStateResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyClusterUpgradingState", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyClusterUpgradingStateResponse()
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

    def OpUpgradeClusterInstances(self, request):
        """用于控制节点升级任务

        :param request: 调用OpUpgradeClusterInstances所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.OpUpgradeClusterInstancesRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.OpUpgradeClusterInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("OpUpgradeClusterInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.OpUpgradeClusterInstancesResponse()
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

    def PauseClusterInstances(self, request):
        """暂停集群节点升级, API 3.0

        :param request: 调用PauseClusterInstances所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.PauseClusterInstancesRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.PauseClusterInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("PauseClusterInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.PauseClusterInstancesResponse()
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

    def ResumeClusterInstances(self, request):
        """恢复集群节点升级，API 3.0

        :param request: 调用ResumeClusterInstances所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.ResumeClusterInstancesRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.ResumeClusterInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ResumeClusterInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ResumeClusterInstancesResponse()
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

    def RunClusterInspections(self, request):
        """触发一次集群巡检。

        :param request: 调用RunClusterInspections所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.RunClusterInspectionsRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.RunClusterInspectionsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("RunClusterInspections", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.RunClusterInspectionsResponse()
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

    def ServiceMeshForwardRequest(self, request):
        """服务网格代理转发

        :param request: 调用ServiceMeshForwardRequest所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.ServiceMeshForwardRequestRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.ServiceMeshForwardRequestResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ServiceMeshForwardRequest", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ServiceMeshForwardRequestResponse()
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

    def UpdateClusterInstances(self, request):
        """集群节点k8s版本升级，API 3.0

        :param request: 调用UpdateClusterInstances所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.UpdateClusterInstancesRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.UpdateClusterInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("UpdateClusterInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UpdateClusterInstancesResponse()
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

    def UpdateClusterVersion(self, request):
        """升级集群 Master 组件到指定版本

        :param request: 调用UpdateClusterVersion所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.UpdateClusterVersionRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.UpdateClusterVersionResponse`

        """
        try:
            params = request._serialize()
            body = self.call("UpdateClusterVersion", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UpdateClusterVersionResponse()
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

    def UpgradeClusterInstances(self, request):
        """给集群的一批work节点进行升级

        :param request: 调用UpgradeClusterInstances所需参数的结构体。
        :type request: :class:`tcecloud.tke.v20180525.models.UpgradeClusterInstancesRequest`
        :rtype: :class:`tcecloud.tke.v20180525.models.UpgradeClusterInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("UpgradeClusterInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UpgradeClusterInstancesResponse()
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

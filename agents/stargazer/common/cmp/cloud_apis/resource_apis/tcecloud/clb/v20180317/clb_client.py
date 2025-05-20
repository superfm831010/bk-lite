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

from common.cmp.cloud_apis.resource_apis.tcecloud.clb.v20180317 import models
from common.cmp.cloud_apis.resource_apis.tcecloud.common.abstract_client import AbstractClient
from common.cmp.cloud_apis.resource_apis.tcecloud.common.exception.tce_cloud_sdk_exception import TceCloudSDKException


class ClbClient(AbstractClient):
    _apiVersion = "2018-03-17"
    _endpoint = "clb.api3.{{conf.main_domain}}"

    def AddCustomizedConfig(self, request):
        """新增个性化配置

        :param request: 调用AddCustomizedConfig所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.AddCustomizedConfigRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.AddCustomizedConfigResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AddCustomizedConfig", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AddCustomizedConfigResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def AssociateCustomizedConfig(self, request):
        """关联配置到server或location，根据配置类型关联到server或location。

        :param request: 调用AssociateCustomizedConfig所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.AssociateCustomizedConfigRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.AssociateCustomizedConfigResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AssociateCustomizedConfig", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AssociateCustomizedConfigResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def AssociateTargetGroups(self, request):
        """本接口(AssociateTargetGroups)用来将目标组绑定到负载均衡的监听器（四层协议）或转发规则（七层协议）上。
        本接口为异步接口，本接口返回成功后需以返回的 RequestID 为入参，调用 DescribeTaskStatus 接口查询本次任务是否成功。

        :param request: 调用AssociateTargetGroups所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.AssociateTargetGroupsRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.AssociateTargetGroupsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AssociateTargetGroups", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AssociateTargetGroupsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def AutoRewrite(self, request):
        """用户需要先创建出一个HTTPS:443监听器，并在其下创建转发规则。通过调用本接口，系统会自动创建出一个HTTP:80监听器（如果之前不存在），并在其下创建转发规则，与HTTPS:443监听器下的Domains（在入参中指定）对应。创建成功后可以通过HTTP:80地址自动跳转为HTTPS:443地址进行访问。
        本接口为异步接口，本接口返回成功后需以返回的RequestID为入参，调用DescribeTaskStatus接口查询本次任务是否成功。

        :param request: 调用AutoRewrite所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.AutoRewriteRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.AutoRewriteResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AutoRewrite", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AutoRewriteResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def BatchDeregisterTargets(self, request):
        """批量解绑四七层后端服务。

        :param request: 调用BatchDeregisterTargets所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.BatchDeregisterTargetsRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.BatchDeregisterTargetsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("BatchDeregisterTargets", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.BatchDeregisterTargetsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def BatchModifyTargetWeight(self, request):
        """本接口(BatchModifyTargetWeight)用于批量修改负载均衡监听器绑定的后端机器的转发权重，支持负载均衡的4层和7层监听器；不支持传统型负载均衡。
        本接口为异步接口，本接口返回成功后需以返回的 RequestID 为入参，调用 DescribeTaskStatus 接口查询本次任务是否成功。

        :param request: 调用BatchModifyTargetWeight所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.BatchModifyTargetWeightRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.BatchModifyTargetWeightResponse`

        """
        try:
            params = request._serialize()
            body = self.call("BatchModifyTargetWeight", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.BatchModifyTargetWeightResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def BatchRegisterTargets(self, request):
        """批量绑定虚拟主机或弹性网卡，支持跨域绑定，支持四层、七层（TCP、UDP、HTTP、HTTPS）协议绑定。

        :param request: 调用BatchRegisterTargets所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.BatchRegisterTargetsRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.BatchRegisterTargetsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("BatchRegisterTargets", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.BatchRegisterTargetsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreateListener(self, request):
        """在一个负载均衡实例下创建监听器。
        本接口为异步接口，接口返回成功后，需以返回的 RequestId 为入参，调用 DescribeTaskStatus 接口查询本次任务是否成功。

        :param request: 调用CreateListener所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.CreateListenerRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.CreateListenerResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateListener", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateListenerResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreateLoadBalancer(self, request):
        """本接口(CreateLoadBalancer)用来创建负载均衡实例（本接口只支持购买按量计费的负载均衡，包年包月的负载均衡请通过控制台购买）。为了使用负载均衡服务，您必须购买一个或多个负载均衡实例。成功调用该接口后，会返回负载均衡实例的唯一 ID。负载均衡实例的类型分为：公网、内网。详情可参考产品说明中的产品类型。
        注意：(1)指定可用区申请负载均衡、跨zone容灾(仅香港支持)【如果您需要体验该功能，请通过 工单申请】；(2)目前只有北京、上海、广州支持IPv6；(3)一个账号在每个地域的默认购买配额为：公网100个，内网100个。
        本接口为异步接口，接口成功返回后，可使用 DescribeLoadBalancers 接口查询负载均衡实例的状态（如创建中、正常），以确定是否创建成功。

        :param request: 调用CreateLoadBalancer所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.CreateLoadBalancerRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.CreateLoadBalancerResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateLoadBalancer", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateLoadBalancerResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreateLoadBalancerSnatIps(self, request):
        """针对SnatPro负载均衡，这个接口用于添加SnatIp，如果负载均衡没有开启SnatPro，添加SnatIp后会自动开启

        :param request: 调用CreateLoadBalancerSnatIps所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.CreateLoadBalancerSnatIpsRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.CreateLoadBalancerSnatIpsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateLoadBalancerSnatIps", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateLoadBalancerSnatIpsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreateRule(self, request):
        """CreateRule 接口用于在一个已存在的负载均衡七层监听器下创建转发规则，七层监听器中，后端服务必须绑定到规则上而非监听器上。
        本接口为异步接口，本接口返回成功后需以返回的RequestID为入参，调用DescribeTaskStatus接口查询本次任务是否成功。

        :param request: 调用CreateRule所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.CreateRuleRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.CreateRuleResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateRule", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateRuleResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreateTargetGroup(self, request):
        """创建目标组。（目标组功能正在灰度中，需要开通白名单支持）

        :param request: 调用CreateTargetGroup所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.CreateTargetGroupRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.CreateTargetGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateTargetGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateTargetGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteCustomizedConfig(self, request):
        """删除配置

        :param request: 调用DeleteCustomizedConfig所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DeleteCustomizedConfigRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DeleteCustomizedConfigResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteCustomizedConfig", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteCustomizedConfigResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteListener(self, request):
        """本接口用来删除负载均衡实例下的监听器（四层和七层）。
        本接口为异步接口，接口返回成功后，需以得到的 RequestID 为入参，调用 DescribeTaskStatus 接口查询本次任务是否成功。

        :param request: 调用DeleteListener所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DeleteListenerRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DeleteListenerResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteListener", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteListenerResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteLoadBalancer(self, request):
        """DeleteLoadBalancer 接口用以删除指定的一个或多个负载均衡实例。
        本接口为异步接口，接口返回成功后，需以返回的 RequestId 为入参，调用 DescribeTaskStatus 接口查询本次任务是否成功。

        :param request: 调用DeleteLoadBalancer所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DeleteLoadBalancerRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DeleteLoadBalancerResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteLoadBalancer", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteLoadBalancerResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteLoadBalancerListeners(self, request):
        """该接口支持删除负载均衡的多个监听器。
        本接口为异步接口，本接口返回成功后需以返回的 RequestID 为入参，调用 DescribeTaskStatus 接口查询本次任务是否成功。

        :param request: 调用DeleteLoadBalancerListeners所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DeleteLoadBalancerListenersRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DeleteLoadBalancerListenersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteLoadBalancerListeners", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteLoadBalancerListenersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteLoadBalancerSnatIps(self, request):
        """对于SnatPro的负载均衡，这个接口用于删除SnatIp

        :param request: 调用DeleteLoadBalancerSnatIps所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DeleteLoadBalancerSnatIpsRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DeleteLoadBalancerSnatIpsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteLoadBalancerSnatIps", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteLoadBalancerSnatIpsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteRewrite(self, request):
        """DeleteRewrite 接口支持删除指定转发规则之间的重定向关系。
        本接口为异步接口，本接口返回成功后需以返回的RequestID为入参，调用DescribeTaskStatus接口查询本次任务是否成功。

        :param request: 调用DeleteRewrite所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DeleteRewriteRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DeleteRewriteResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteRewrite", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteRewriteResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteRule(self, request):
        """DeleteRule 接口用来删除负载均衡实例七层监听器下的转发规则。
        本接口为异步接口，本接口返回成功后需以返回的RequestID为入参，调用DescribeTaskStatus接口查询本次任务是否成功。

        :param request: 调用DeleteRule所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DeleteRuleRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DeleteRuleResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteRule", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteRuleResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteTargetGroups(self, request):
        """删除目标组

        :param request: 调用DeleteTargetGroups所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DeleteTargetGroupsRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DeleteTargetGroupsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteTargetGroups", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteTargetGroupsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeregisterTargetGroupInstances(self, request):
        """将服务器从目标组中解绑。
        本接口为异步接口，本接口返回成功后需以返回的 RequestID 为入参，调用 DescribeTaskStatus 接口查询本次任务是否成功。

        :param request: 调用DeregisterTargetGroupInstances所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DeregisterTargetGroupInstancesRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DeregisterTargetGroupInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeregisterTargetGroupInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeregisterTargetGroupInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeregisterTargets(self, request):
        """DeregisterTargets 接口用来将一台或多台后端服务从负载均衡的监听器或转发规则上解绑，对于四层监听器，只需指定监听器ID即可，对于七层监听器，还需通过LocationId或Domain+Url指定转发规则。
        本接口为异步接口，本接口返回成功后需以返回的RequestID为入参，调用DescribeTaskStatus接口查询本次任务是否成功。

        :param request: 调用DeregisterTargets所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DeregisterTargetsRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DeregisterTargetsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeregisterTargets", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeregisterTargetsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeregisterTargetsFromClassicalLB(self, request):
        """DeregisterTargetsFromClassicalLB 接口用于解绑负载均衡后端服务。
        本接口为异步接口，接口返回成功后，需以返回的 RequestId 为入参，调用 DescribeTaskStatus 接口查询本次任务是否成功。

        :param request: 调用DeregisterTargetsFromClassicalLB所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DeregisterTargetsFromClassicalLBRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DeregisterTargetsFromClassicalLBResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeregisterTargetsFromClassicalLB", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeregisterTargetsFromClassicalLBResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeBlockIPList(self, request):
        """查询一个负载均衡所封禁的IP列表（黑名单）。（接口灰度中，如需使用请提工单）

        :param request: 调用DescribeBlockIPList所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeBlockIPListRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeBlockIPListResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeBlockIPList", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBlockIPListResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeBlockIPTask(self, request):
        """根据 ModifyBlockIPList 接口返回的异步任务的ID，查询封禁IP（黑名单）异步任务的执行状态。（接口灰度中，如需使用请提工单）

        :param request: 调用DescribeBlockIPTask所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeBlockIPTaskRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeBlockIPTaskResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeBlockIPTask", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBlockIPTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeClassicalLBByInstanceId(self, request):
        """DescribeClassicalLBByInstanceId用于通过后端实例ID获取传统型负载均衡ID列表

        :param request: 调用DescribeClassicalLBByInstanceId所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeClassicalLBByInstanceIdRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeClassicalLBByInstanceIdResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClassicalLBByInstanceId", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClassicalLBByInstanceIdResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeClassicalLBHealthStatus(self, request):
        """DescribeClassicalLBHealthStatus用于获取传统型负载均衡后端的健康状态

        :param request: 调用DescribeClassicalLBHealthStatus所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeClassicalLBHealthStatusRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeClassicalLBHealthStatusResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClassicalLBHealthStatus", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClassicalLBHealthStatusResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeClassicalLBListeners(self, request):
        """DescribeClassicalLBListeners 接口用于获取传统型负载均衡的监听器信息。

        :param request: 调用DescribeClassicalLBListeners所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeClassicalLBListenersRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeClassicalLBListenersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClassicalLBListeners", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClassicalLBListenersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeClassicalLBTargets(self, request):
        """DescribeClassicalLBTargets用于获取传统型负载均衡绑定的后端服务

        :param request: 调用DescribeClassicalLBTargets所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeClassicalLBTargetsRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeClassicalLBTargetsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClassicalLBTargets", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClassicalLBTargetsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeClusterResources(self, request):
        """查询独占集群中资源列表，支持按集群ID、vip、负载均衡ID、是否闲置为过滤条件检索

        :param request: 调用DescribeClusterResources所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeClusterResourcesRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeClusterResourcesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClusterResources", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClusterResourcesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeCustomizedConfigAssociateList(self, request):
        """拉取配置绑定的 server 或 location，如果 domain 存在，结果将根据 domain 过滤。或拉取配置绑定的 loadbalancer。

        :param request: 调用DescribeCustomizedConfigAssociateList所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeCustomizedConfigAssociateListRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeCustomizedConfigAssociateListResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeCustomizedConfigAssociateList", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCustomizedConfigAssociateListResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeCustomizedConfigContent(self, request):
        """拉取配置内容。

        :param request: 调用DescribeCustomizedConfigContent所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeCustomizedConfigContentRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeCustomizedConfigContentResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeCustomizedConfigContent", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCustomizedConfigContentResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeCustomizedConfigLBAssociateList(self, request):
        """拉取LB下绑定的列表

        :param request: 调用DescribeCustomizedConfigLBAssociateList所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeCustomizedConfigLBAssociateListRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeCustomizedConfigLBAssociateListResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeCustomizedConfigLBAssociateList", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCustomizedConfigLBAssociateListResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeCustomizedConfigList(self, request):
        """拉取个性化配置列表，返回用户 AppId 下指定类型的配置。

        :param request: 调用DescribeCustomizedConfigList所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeCustomizedConfigListRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeCustomizedConfigListResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeCustomizedConfigList", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCustomizedConfigListResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeExclusiveClusters(self, request):
        """查询集群信息列表，支持以集群类型、集群唯一ID、集群名字、集群标签、集群内vip、集群内负载均衡唯一id、集群网络类型、可用区等条件进行检索

        :param request: 调用DescribeExclusiveClusters所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeExclusiveClustersRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeExclusiveClustersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeExclusiveClusters", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeExclusiveClustersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeLBActionLimit(self, request):
        """该接口用于查询LB相关操作配额

        :param request: 调用DescribeLBActionLimit所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeLBActionLimitRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeLBActionLimitResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeLBActionLimit", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeLBActionLimitResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeLBListeners(self, request):
        """查询后端云主机或弹性网卡绑定的负载均衡，支持弹性网卡和cvm查询。

        :param request: 调用DescribeLBListeners所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeLBListenersRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeLBListenersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeLBListeners", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeLBListenersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeListeners(self, request):
        """DescribeListeners 接口可根据负载均衡器 ID，监听器的协议或端口作为过滤条件获取监听器列表。如果不指定任何过滤条件，则返回该负载均衡实例下的所有监听器。

        :param request: 调用DescribeListeners所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeListenersRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeListenersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeListeners", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeListenersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeLoadBalancerCount(self, request):
        """查询一个账户在一个地域的负载均衡实例总数

        :param request: 调用DescribeLoadBalancerCount所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeLoadBalancerCountRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeLoadBalancerCountResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeLoadBalancerCount", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeLoadBalancerCountResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeLoadBalancerListByCertId(self, request):
        """根据证书ID查询其在一个地域中所关联到负载均衡实例列表

        :param request: 调用DescribeLoadBalancerListByCertId所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeLoadBalancerListByCertIdRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeLoadBalancerListByCertIdResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeLoadBalancerListByCertId", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeLoadBalancerListByCertIdResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeLoadBalancers(self, request):
        """查询一个地域的负载均衡实例列表

        :param request: 调用DescribeLoadBalancers所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeLoadBalancersRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeLoadBalancersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeLoadBalancers", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeLoadBalancersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeLoadBalancersFeature(self, request):
        """获取负载均衡实例支持的功能

        :param request: 调用DescribeLoadBalancersFeature所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeLoadBalancersFeatureRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeLoadBalancersFeatureResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeLoadBalancersFeature", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeLoadBalancersFeatureResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeLoadBalancersForVpc(self, request):
        """提供为VPC控制台用，查询负载均衡实例（部分信息没有查）。

        :param request: 调用DescribeLoadBalancersForVpc所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeLoadBalancersForVpcRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeLoadBalancersForVpcResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeLoadBalancersForVpc", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeLoadBalancersForVpcResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeMasterZones(self, request):
        """查询一个地域的可用区列表

        :param request: 调用DescribeMasterZones所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeMasterZonesRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeMasterZonesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeMasterZones", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeMasterZonesResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        """查询配额

        :param request: 调用DescribeQuota所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeQuotaRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeQuotaResponse`

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

    def DescribeRewrite(self, request):
        """DescribeRewrite 接口可根据负载均衡实例ID，查询一个负载均衡实例下转发规则的重定向关系。如果不指定监听器ID或转发规则ID，则返回该负载均衡实例下的所有重定向关系。

        :param request: 调用DescribeRewrite所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeRewriteRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeRewriteResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRewrite", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRewriteResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeSetByVip(self, request):
        """通过VIP查找该VIP落在哪个独占集群（四层 + 七层）

        一个vip的七层规则可能落在不同集群，根据vip+协议+vport来区分


        :param request: 调用DescribeSetByVip所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeSetByVipRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeSetByVipResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeSetByVip", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeSetByVipResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeSetCapacity(self, request):
        """提供云API，用户可以通过API获取独占集群的总容量

        四层独占集群：出带宽、入带宽、出流量、入流量、连接数

        七层独占集群：QPS、连接数

        :param request: 调用DescribeSetCapacity所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeSetCapacityRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeSetCapacityResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeSetCapacity", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeSetCapacityResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeSetInnerName(self, request):
        """根据集群对外英文名、appid查询中文名

        :param request: 调用DescribeSetInnerName所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeSetInnerNameRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeSetInnerNameResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeSetInnerName", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeSetInnerNameResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeSetVip(self, request):
        """通过集群名字查询vip

        :param request: 调用DescribeSetVip所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeSetVipRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeSetVipResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeSetVip", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeSetVipResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeSets(self, request):
        """查询独占集群列表，入参为搜索字段名，默认返回列表

        :param request: 调用DescribeSets所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeSetsRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeSetsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeSets", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeSetsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeSingleIsp(self, request):
        """返回某个地域所支持的运营商列表。

        :param request: 调用DescribeSingleIsp所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeSingleIspRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeSingleIspResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeSingleIsp", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeSingleIspResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeTargetCountForLoadBalancers(self, request):
        """查询负载均衡实例绑定的后端服务总数

        :param request: 调用DescribeTargetCountForLoadBalancers所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeTargetCountForLoadBalancersRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeTargetCountForLoadBalancersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeTargetCountForLoadBalancers", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTargetCountForLoadBalancersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeTargetGroupInstances(self, request):
        """获取目标组绑定的服务器信息

        :param request: 调用DescribeTargetGroupInstances所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeTargetGroupInstancesRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeTargetGroupInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeTargetGroupInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTargetGroupInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeTargetGroupList(self, request):
        """获取目标组列表

        :param request: 调用DescribeTargetGroupList所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeTargetGroupListRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeTargetGroupListResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeTargetGroupList", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTargetGroupListResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeTargetGroups(self, request):
        """查询目标组信息

        :param request: 调用DescribeTargetGroups所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeTargetGroupsRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeTargetGroupsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeTargetGroups", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTargetGroupsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeTargetHealth(self, request):
        """DescribeTargetHealth 接口用来获取负载均衡后端服务的健康检查结果，不支持传统型负载均衡。

        :param request: 调用DescribeTargetHealth所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeTargetHealthRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeTargetHealthResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeTargetHealth", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTargetHealthResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeTargets(self, request):
        """DescribeTargets 接口用来查询负载均衡实例的某些监听器绑定的后端服务列表。

        :param request: 调用DescribeTargets所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeTargetsRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeTargetsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeTargets", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTargetsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeTaskStatus(self, request):
        """本接口用于查询异步任务的执行状态，对于非查询类的接口（创建/删除负载均衡实例、监听器、规则以及绑定或解绑后端服务等），在接口调用成功后，都需要使用本接口查询任务最终是否执行成功。

        :param request: 调用DescribeTaskStatus所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DescribeTaskStatusRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DescribeTaskStatusResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeTaskStatus", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTaskStatusResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DisassociateCustomizedConfig(self, request):
        """解绑配置。

        :param request: 调用DisassociateCustomizedConfig所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DisassociateCustomizedConfigRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DisassociateCustomizedConfigResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DisassociateCustomizedConfig", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DisassociateCustomizedConfigResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DisassociateTargetGroups(self, request):
        """解除规则的目标组关联关系。
        本接口为异步接口，本接口返回成功后需以返回的 RequestID 为入参，调用 DescribeTaskStatus 接口查询本次任务是否成功。

        :param request: 调用DisassociateTargetGroups所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.DisassociateTargetGroupsRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.DisassociateTargetGroupsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DisassociateTargetGroups", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DisassociateTargetGroupsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceCreateLoadBalancer(self, request):
        """查询创建负载均衡的价格

        :param request: 调用InquiryPriceCreateLoadBalancer所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.InquiryPriceCreateLoadBalancerRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.InquiryPriceCreateLoadBalancerResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceCreateLoadBalancer", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceCreateLoadBalancerResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceModifyLoadBalancer(self, request):
        """预付费负载均衡修改配置询价

        :param request: 调用InquiryPriceModifyLoadBalancer所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.InquiryPriceModifyLoadBalancerRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.InquiryPriceModifyLoadBalancerResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceModifyLoadBalancer", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceModifyLoadBalancerResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceRefundLoadBalancer(self, request):
        """查询负载均衡退费价格

        :param request: 调用InquiryPriceRefundLoadBalancer所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.InquiryPriceRefundLoadBalancerRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.InquiryPriceRefundLoadBalancerResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceRefundLoadBalancer", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceRefundLoadBalancerResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceRenewLoadBalancer(self, request):
        """查询对负载均衡续费的价格，只支持预付费负载均衡续费

        :param request: 调用InquiryPriceRenewLoadBalancer所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.InquiryPriceRenewLoadBalancerRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.InquiryPriceRenewLoadBalancerResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceRenewLoadBalancer", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceRenewLoadBalancerResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ManualRewrite(self, request):
        """用户手动配置原访问地址和重定向地址，系统自动将原访问地址的请求重定向至对应路径的目的地址。同一域名下可以配置多条路径作为重定向策略，实现http/https之间请求的自动跳转。设置重定向时，需满足如下约束条件：若A已经重定向至B，则A不能再重定向至C（除非先删除老的重定向关系，再建立新的重定向关系），B不能重定向至任何其它地址。
        本接口为异步接口，本接口返回成功后需以返回的RequestID为入参，调用DescribeTaskStatus接口查询本次任务是否成功。

        :param request: 调用ManualRewrite所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.ManualRewriteRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.ManualRewriteResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ManualRewrite", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ManualRewriteResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def MigrateAppIdVIP(self, request):
        """跨开发商迁移负载均衡的VIP。
        本接口为异步接口，本接口返回成功后需以返回的RequestID为入参，调用DescribeTaskStatus接口查询本次任务是否成功。

        :param request: 调用MigrateAppIdVIP所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.MigrateAppIdVIPRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.MigrateAppIdVIPResponse`

        """
        try:
            params = request._serialize()
            body = self.call("MigrateAppIdVIP", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.MigrateAppIdVIPResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyBlockIPList(self, request):
        """修改负载均衡的IP（client IP）封禁黑名单列表，一个转发规则最多支持封禁 2000000 个IP，及黑名单容量为 2000000。
        （接口灰度中，如需使用请提工单）

        :param request: 调用ModifyBlockIPList所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.ModifyBlockIPListRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.ModifyBlockIPListResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyBlockIPList", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyBlockIPListResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyCustomizedConfig(self, request):
        """修改个性化配置。如果配置已经绑定clb、server或location，同时更新。

        :param request: 调用ModifyCustomizedConfig所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.ModifyCustomizedConfigRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.ModifyCustomizedConfigResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyCustomizedConfig", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyCustomizedConfigResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyDnat(self, request):
        """打开或关闭clb直通功能

        :param request: 调用ModifyDnat所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.ModifyDnatRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.ModifyDnatResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyDnat", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyDnatResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyDomain(self, request):
        """ModifyDomain接口用来修改负载均衡七层监听器下的域名。
        本接口为异步接口，本接口返回成功后需以返回的RequestID为入参，调用DescribeTaskStatus接口查询本次任务是否成功。

        :param request: 调用ModifyDomain所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.ModifyDomainRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.ModifyDomainResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyDomain", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyDomainResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyDomainAttributes(self, request):
        """ModifyDomainAttributes接口用于修改负载均衡7层监听器转发规则的域名级别属性，如修改域名、修改DefaultServer、开启/关闭Http2、修改证书。
        本接口为异步接口，本接口返回成功后，需以返回的RequestId为入参，调用DescribeTaskStatus接口查询本次任务是否成功。

        :param request: 调用ModifyDomainAttributes所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.ModifyDomainAttributesRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.ModifyDomainAttributesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyDomainAttributes", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyDomainAttributesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyListener(self, request):
        """ModifyListener接口用来修改负载均衡监听器的属性，包括监听器名称、健康检查参数、证书信息、转发策略等。本接口不支持传统型负载均衡。
        本接口为异步接口，本接口返回成功后需以返回的RequestID为入参，调用DescribeTaskStatus接口查询本次任务是否成功。

        :param request: 调用ModifyListener所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.ModifyListenerRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.ModifyListenerResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyListener", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyListenerResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyLoadBalancerAttributes(self, request):
        """修改负载均衡实例的属性。支持修改负载均衡实例的名称、设置负载均衡的跨域属性。

        :param request: 调用ModifyLoadBalancerAttributes所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.ModifyLoadBalancerAttributesRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.ModifyLoadBalancerAttributesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyLoadBalancerAttributes", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyLoadBalancerAttributesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyLoadBalancersProject(self, request):
        """修改一个或多个负载均衡实例所属项目。

        :param request: 调用ModifyLoadBalancersProject所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.ModifyLoadBalancersProjectRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.ModifyLoadBalancersProjectResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyLoadBalancersProject", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyLoadBalancersProjectResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyRule(self, request):
        """ModifyRule 接口用来修改负载均衡七层监听器下的转发规则的各项属性，包括转发路径、健康检查属性、转发策略等。
        本接口为异步接口，本接口返回成功后需以返回的RequestID为入参，调用DescribeTaskStatus接口查询本次任务是否成功。

        :param request: 调用ModifyRule所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.ModifyRuleRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.ModifyRuleResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyRule", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyRuleResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyTargetGroupAttribute(self, request):
        """修改目标组的名称或者默认端口属性

        :param request: 调用ModifyTargetGroupAttribute所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.ModifyTargetGroupAttributeRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.ModifyTargetGroupAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyTargetGroupAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyTargetGroupAttributeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyTargetGroupInstancesPort(self, request):
        """批量修改目标组服务器端口。
        本接口为异步接口，本接口返回成功后需以返回的 RequestID 为入参，调用 DescribeTaskStatus 接口查询本次任务是否成功。

        :param request: 调用ModifyTargetGroupInstancesPort所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.ModifyTargetGroupInstancesPortRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.ModifyTargetGroupInstancesPortResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyTargetGroupInstancesPort", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyTargetGroupInstancesPortResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyTargetGroupInstancesWeight(self, request):
        """批量修改目标组的服务器权重。
        本接口为异步接口，本接口返回成功后需以返回的 RequestID 为入参，调用 DescribeTaskStatus 接口查询本次任务是否成功。

        :param request: 调用ModifyTargetGroupInstancesWeight所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.ModifyTargetGroupInstancesWeightRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.ModifyTargetGroupInstancesWeightResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyTargetGroupInstancesWeight", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyTargetGroupInstancesWeightResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyTargetPort(self, request):
        """ModifyTargetPort接口用于修改监听器绑定的后端服务的端口。
        本接口为异步接口，本接口返回成功后需以返回的RequestID为入参，调用DescribeTaskStatus接口查询本次任务是否成功。

        :param request: 调用ModifyTargetPort所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.ModifyTargetPortRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.ModifyTargetPortResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyTargetPort", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyTargetPortResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyTargetWeight(self, request):
        """ModifyTargetWeight 接口用于修改负载均衡绑定的后端服务的转发权重。
        本接口为异步接口，本接口返回成功后需以返回的RequestID为入参，调用DescribeTaskStatus接口查询本次任务是否成功。

        :param request: 调用ModifyTargetWeight所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.ModifyTargetWeightRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.ModifyTargetWeightResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyTargetWeight", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyTargetWeightResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def QueryBlockIPTask(self, request):
        """查询封禁IP（黑名单）异步任务的执行状态。（接口灰度中，如需使用请提工单）

        :param request: 调用QueryBlockIPTask所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.QueryBlockIPTaskRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.QueryBlockIPTaskResponse`

        """
        try:
            params = request._serialize()
            body = self.call("QueryBlockIPTask", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.QueryBlockIPTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def QuerySetByVip(self, request):
        """通过VIP查找该VIP落在哪个独占集群（四层 + 七层）

        一个vip的七层规则可能落在不同集群，根据vip+协议+vport来区分


        :param request: 调用QuerySetByVip所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.QuerySetByVipRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.QuerySetByVipResponse`

        """
        try:
            params = request._serialize()
            body = self.call("QuerySetByVip", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.QuerySetByVipResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def QuerySetCapacity(self, request):
        """提供云API，用户可以通过API获取独占集群的总容量

        四层独占集群：出带宽、入带宽、出流量、入流量、连接数

        七层独占集群：QPS、连接数

        :param request: 调用QuerySetCapacity所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.QuerySetCapacityRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.QuerySetCapacityResponse`

        """
        try:
            params = request._serialize()
            body = self.call("QuerySetCapacity", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.QuerySetCapacityResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def QuerySetVip(self, request):
        """通过集群名字查询vip

        :param request: 调用QuerySetVip所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.QuerySetVipRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.QuerySetVipResponse`

        """
        try:
            params = request._serialize()
            body = self.call("QuerySetVip", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.QuerySetVipResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def RegisterTargetGroupInstances(self, request):
        """注册服务器到目标组。
        本接口为异步接口，本接口返回成功后需以返回的 RequestID 为入参，调用 DescribeTaskStatus 接口查询本次任务是否成功。

        :param request: 调用RegisterTargetGroupInstances所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.RegisterTargetGroupInstancesRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.RegisterTargetGroupInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("RegisterTargetGroupInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.RegisterTargetGroupInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def RegisterTargets(self, request):
        """RegisterTargets 接口用来将一台或多台后端服务绑定到负载均衡的监听器（或7层转发规则），在此之前您需要先行创建相关的4层监听器或7层转发规则。对于四层监听器（TCP、UDP），只需指定监听器ID即可，对于七层监听器（HTTP、HTTPS），还需通过LocationId或者Domain+Url指定转发规则。
        本接口为异步接口，本接口返回成功后需以返回的RequestID为入参，调用DescribeTaskStatus接口查询本次任务是否成功。

        :param request: 调用RegisterTargets所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.RegisterTargetsRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.RegisterTargetsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("RegisterTargets", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.RegisterTargetsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def RegisterTargetsWithClassicalLB(self, request):
        """RegisterTargetsWithClassicalLB 接口用于绑定后端服务到传统型负载均衡。
        本接口为异步接口，接口返回成功后，需以返回的 RequestId 为入参，调用 DescribeTaskStatus 接口查询本次任务是否成功。

        :param request: 调用RegisterTargetsWithClassicalLB所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.RegisterTargetsWithClassicalLBRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.RegisterTargetsWithClassicalLBResponse`

        """
        try:
            params = request._serialize()
            body = self.call("RegisterTargetsWithClassicalLB", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.RegisterTargetsWithClassicalLBResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ReplaceCertForLoadBalancers(self, request):
        """ReplaceCertForLoadBalancers 接口用以替换负载均衡实例所关联的证书，对于各个地域的负载均衡，如果指定的老的证书ID与其有关联关系，则会先解除关联，再建立新证书与该负载均衡的关联关系。
        此接口支持替换服务端证书或客户端证书。
        需要使用的新证书，可以通过传入证书ID来指定，如果不指定证书ID，则必须传入证书内容等相关信息，用以新建证书并绑定至负载均衡。
        注：本接口仅可从广州地域调用。

        :param request: 调用ReplaceCertForLoadBalancers所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.ReplaceCertForLoadBalancersRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.ReplaceCertForLoadBalancersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ReplaceCertForLoadBalancers", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ReplaceCertForLoadBalancersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def SetCustomizedConfigForLoadBalancer(self, request):
        """负载均衡维度的个性化配置相关操作：创建、删除、修改、绑定、解绑

        :param request: 调用SetCustomizedConfigForLoadBalancer所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.SetCustomizedConfigForLoadBalancerRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.SetCustomizedConfigForLoadBalancerResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SetCustomizedConfigForLoadBalancer", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SetCustomizedConfigForLoadBalancerResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def SetLoadBalancerClsLog(self, request):
        """增加、删除、更新负载均衡的日志服务(CLS)主题

        :param request: 调用SetLoadBalancerClsLog所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.SetLoadBalancerClsLogRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.SetLoadBalancerClsLogResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SetLoadBalancerClsLog", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SetLoadBalancerClsLogResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def SetLoadBalancerExclusiveTag(self, request):
        """设置负载均衡七层集群的独占标签。

        :param request: 调用SetLoadBalancerExclusiveTag所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.SetLoadBalancerExclusiveTagRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.SetLoadBalancerExclusiveTagResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SetLoadBalancerExclusiveTag", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SetLoadBalancerExclusiveTagResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def SetLoadBalancerLog(self, request):
        """增加、删除、更新负载均衡日志访问，该功能目前仅支持以下地域：北京、上海、广州、香港、上海金融、深圳金融。

        :param request: 调用SetLoadBalancerLog所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.SetLoadBalancerLogRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.SetLoadBalancerLogResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SetLoadBalancerLog", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SetLoadBalancerLogResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def SetLoadBalancerSecurityGroups(self, request):
        """SetLoadBalancerSecurityGroups 接口支持对一个公网负载均衡实例执行设置（绑定、解绑）安全组操作。查询一个负载均衡实例目前已绑定的安全组，可使用 DescribeLoadBalancers 接口。本接口是set语义，
        绑定操作时，入参需要传入负载均衡实例要绑定的所有安全组（已绑定的+新增绑定的）。
        解绑操作时，入参需要传入负载均衡实例执行解绑后所绑定的所有安全组；如果要解绑所有安全组，可不传此参数，或传入空数组。注意：内网负载均衡不支持绑定安全组。

        :param request: 调用SetLoadBalancerSecurityGroups所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.SetLoadBalancerSecurityGroupsRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.SetLoadBalancerSecurityGroupsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SetLoadBalancerSecurityGroups", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SetLoadBalancerSecurityGroupsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def SetSecurityGroupForLoadbalancers(self, request):
        """绑定或解绑一个安全组到多个公网负载均衡实例。注意：内网负载均衡不支持绑定安全组。

        :param request: 调用SetSecurityGroupForLoadbalancers所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.SetSecurityGroupForLoadbalancersRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.SetSecurityGroupForLoadbalancersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SetSecurityGroupForLoadbalancers", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SetSecurityGroupForLoadbalancersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def TestEzio(self, request):
        """测试

        :param request: 调用TestEzio所需参数的结构体。
        :type request: :class:`tcecloud.clb.v20180317.models.TestEzioRequest`
        :rtype: :class:`tcecloud.clb.v20180317.models.TestEzioResponse`

        """
        try:
            params = request._serialize()
            body = self.call("TestEzio", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.TestEzioResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

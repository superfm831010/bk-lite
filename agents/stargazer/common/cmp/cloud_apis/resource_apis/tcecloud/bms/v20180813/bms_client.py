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

from common.cmp.cloud_apis.resource_apis.tcecloud.bms.v20180813 import models
from common.cmp.cloud_apis.resource_apis.tcecloud.common.abstract_client import AbstractClient
from common.cmp.cloud_apis.resource_apis.tcecloud.common.exception.tce_cloud_sdk_exception import TceCloudSDKException


class BmsClient(AbstractClient):
    _apiVersion = "2018-08-13"
    _endpoint = "bms.api3.{{conf.main_domain}}"

    def DescribeDisks(self, request):
        """本接口（DescribeDisks）用于查询BMS硬盘列表。

        * 可以根据BMS硬盘ID等信息来查询BMS硬盘的详细信息，不同条件之间为与(AND)的关系，过滤信息详细请见过滤器`Filter`。
        * 如果参数为空，返回当前用户一定数量（`Limit`所指定的数量，默认为20）的BMS硬盘列表。

        :param request: 调用DescribeDisks所需参数的结构体。
        :type request: :class:`tcecloud.bms.v20180813.models.DescribeDisksRequest`
        :rtype: :class:`tcecloud.bms.v20180813.models.DescribeDisksResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDisks", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDisksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeFlavors(self, request):
        """显示套餐列表详情。

        :param request: 调用DescribeFlavors所需参数的结构体。
        :type request: :class:`tcecloud.bms.v20180813.models.DescribeFlavorsRequest`
        :rtype: :class:`tcecloud.bms.v20180813.models.DescribeFlavorsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeFlavors", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeFlavorsResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        """本接口 (DescribeInstances) 用于查询一个或多个实例的详细信息。

        * 可以根据实例`ID`、实例名称或者实例计费模式等信息来查询实例的详细信息。过滤信息详细请见过滤器`Filter`。
        * 如果参数为空，返回当前用户一定数量（`Limit`所指定的数量，默认为20）的实例。

        :param request: 调用DescribeInstances所需参数的结构体。
        :type request: :class:`tcecloud.bms.v20180813.models.DescribeInstancesRequest`
        :rtype: :class:`tcecloud.bms.v20180813.models.DescribeInstancesResponse`

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

    def GetInstancesByTaskId(self, request):
        """根据部署任务的ID查询对应的实例ID信息

        :param request: 调用GetInstancesByTaskId所需参数的结构体。
        :type request: :class:`tcecloud.bms.v20180813.models.GetInstancesByTaskIdRequest`
        :rtype: :class:`tcecloud.bms.v20180813.models.GetInstancesByTaskIdResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetInstancesByTaskId", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetInstancesByTaskIdResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceBmsInstanceForTrade(self, request):
        """bms询价

        :param request: 调用InquiryPriceBmsInstanceForTrade所需参数的结构体。
        :type request: :class:`tcecloud.bms.v20180813.models.InquiryPriceBmsInstanceForTradeRequest`
        :rtype: :class:`tcecloud.bms.v20180813.models.InquiryPriceBmsInstanceForTradeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceBmsInstanceForTrade", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceBmsInstanceForTradeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyInstancesAttribute(self, request):
        """本接口 (ModifyInstancesAttribute) 用于修改实例的属性（目前只支持修改实例的名称）。

        * “实例名称”仅为方便用户自己管理之用，Tce并不以此名称作为提交工单或是进行实例管理操作的依据。
        * 支持批量操作。每次请求批量实例的上限为100。

        :param request: 调用ModifyInstancesAttribute所需参数的结构体。
        :type request: :class:`tcecloud.bms.v20180813.models.ModifyInstancesAttributeRequest`
        :rtype: :class:`tcecloud.bms.v20180813.models.ModifyInstancesAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyInstancesAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyInstancesAttributeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def QueryTask(self, request):
        """查询异步任务执行结果

        :param request: 调用QueryTask所需参数的结构体。
        :type request: :class:`tcecloud.bms.v20180813.models.QueryTaskRequest`
        :rtype: :class:`tcecloud.bms.v20180813.models.QueryTaskResponse`

        """
        try:
            params = request._serialize()
            body = self.call("QueryTask", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.QueryTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def RebootInstances(self, request):
        """本接口 (RebootInstances) 用于重启实例。

        * 只有状态为`RUNNING`的实例才可以进行此操作。
        * 接口调用成功时，实例会进入`REBOOTING`状态；重启实例成功时，实例会进入`RUNNING`状态。

        :param request: 调用RebootInstances所需参数的结构体。
        :type request: :class:`tcecloud.bms.v20180813.models.RebootInstancesRequest`
        :rtype: :class:`tcecloud.bms.v20180813.models.RebootInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("RebootInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.RebootInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ResetInstance(self, request):
        """本接口 (ResetInstance) 用于重装指定实例上的操作系统。

        * 如果指定了`OperatingSystem`参数，则使用指定的系统重装；否则按照当前实例使用的系统进行重装。
        * 系统盘将会被格式化，并重置；请确保系统盘中无重要文件。

        :param request: 调用ResetInstance所需参数的结构体。
        :type request: :class:`tcecloud.bms.v20180813.models.ResetInstanceRequest`
        :rtype: :class:`tcecloud.bms.v20180813.models.ResetInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ResetInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ResetInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def RunInstances(self, request):
        """本接口 (RunInstances) 用于创建一个或多个指定配置的实例。

        :param request: 调用RunInstances所需参数的结构体。
        :type request: :class:`tcecloud.bms.v20180813.models.RunInstancesRequest`
        :rtype: :class:`tcecloud.bms.v20180813.models.RunInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("RunInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.RunInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def StartInstances(self, request):
        """本接口 (StartInstances) 用于启动一个或多个实例。

        * 只有状态为`STOPPED`的实例才可以进行此操作。
        * 接口调用成功时，实例会进入`STARTING`状态；启动实例成功时，实例会进入`RUNNING`状态。

        :param request: 调用StartInstances所需参数的结构体。
        :type request: :class:`tcecloud.bms.v20180813.models.StartInstancesRequest`
        :rtype: :class:`tcecloud.bms.v20180813.models.StartInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("StartInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.StartInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def StopInstances(self, request):
        """本接口 (StopInstances) 用于关闭一个或多个实例。

        * 只有状态为`RUNNING`的实例才可以进行此操作。
        * 接口调用成功时，实例会进入`STOPPING`状态；关闭实例成功时，实例会进入`STOPPED`状态。

        :param request: 调用StopInstances所需参数的结构体。
        :type request: :class:`tcecloud.bms.v20180813.models.StopInstancesRequest`
        :rtype: :class:`tcecloud.bms.v20180813.models.StopInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("StopInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.StopInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def TerminateInstances(self, request):
        """本接口 (TerminateInstances) 用于主动退还实例。

        * 不再使用的实例，可通过本接口主动退还。

        :param request: 调用TerminateInstances所需参数的结构体。
        :type request: :class:`tcecloud.bms.v20180813.models.TerminateInstancesRequest`
        :rtype: :class:`tcecloud.bms.v20180813.models.TerminateInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("TerminateInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.TerminateInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

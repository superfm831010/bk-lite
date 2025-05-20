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
from common.cmp.cloud_apis.resource_apis.tcecloud.monitor.v20170312 import models


class MonitorClient(AbstractClient):
    _apiVersion = "2017-03-12"
    _endpoint = "monitor.api3.{{conf.main_domain}}"

    def DescribeAlarmMetrics(self, request):
        """查询可用于配置告警的指标列表

        :param request: 调用DescribeAlarmMetrics所需参数的结构体。
        :type request: :class:`tcecloud.monitor.v20170312.models.DescribeAlarmMetricsRequest`
        :rtype: :class:`tcecloud.monitor.v20170312.models.DescribeAlarmMetricsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeAlarmMetrics", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAlarmMetricsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeBaseMetrics(self, request):
        """获取基础指标详情

        :param request: 调用DescribeBaseMetrics所需参数的结构体。
        :type request: :class:`tcecloud.monitor.v20170312.models.DescribeBaseMetricsRequest`
        :rtype: :class:`tcecloud.monitor.v20170312.models.DescribeBaseMetricsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeBaseMetrics", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBaseMetricsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def GetMonitorData(self, request):
        """获取云产品的监控数据。传入产品的命名空间、对象维度描述和监控指标即可获得相应的监控数据。
        接口调用频率限制为：50次/秒，500次/分钟。
        若您需要调用的指标、对象较多，可能存在因限频出现拉取失败的情况，建议尽量将请求按时间维度均摊。

        :param request: 调用GetMonitorData所需参数的结构体。
        :type request: :class:`tcecloud.monitor.v20170312.models.GetMonitorDataRequest`
        :rtype: :class:`tcecloud.monitor.v20170312.models.GetMonitorDataResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetMonitorData", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetMonitorDataResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

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

from common.cmp.cloud_apis.resource_apis.tcecloud.common.abstract_model import AbstractModel


class DescribeAlarmMetricsRequest(AbstractModel):
    """DescribeAlarmMetrics请求参数结构体"""


class DescribeAlarmMetricsResponse(AbstractModel):
    """DescribeAlarmMetrics返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeBaseMetricsRequest(AbstractModel):
    """DescribeBaseMetrics请求参数结构体"""

    def __init__(self):
        """
        :param Namespace: 业务命名空间
        :type Namespace: str
        :param MetricName: 指标名
        :type MetricName: str
        """
        self.Namespace = None
        self.MetricName = None

    def _deserialize(self, params):
        self.Namespace = params.get("Namespace")
        self.MetricName = params.get("MetricName")


class DescribeBaseMetricsResponse(AbstractModel):
    """DescribeBaseMetrics返回参数结构体"""

    def __init__(self):
        """
        :param MetricSet: 查询得到的指标描述列表
        :type MetricSet: list of MetricObject
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.MetricSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("MetricSet") is not None:
            self.MetricSet = []
            for item in params.get("MetricSet"):
                obj = MetricObject()
                obj._deserialize(item)
                self.MetricSet.append(obj)
        self.RequestId = params.get("RequestId")


class GetMonitorDataRequest(AbstractModel):
    """GetMonitorData请求参数结构体"""

    def __init__(self):
        """
        :param Namespace: 命名空间，每个云产品会有一个命名空间
        :type Namespace: str
        :param MetricName: 指标名称
        :type MetricName: str
        :param Dimensions: 实例对象的维度组合
        :type Dimensions: list of str
        :param Period: 监控统计周期。默认为取值为300，单位为s
        :type Period: int
        :param StartTime: 起始时间，如 2018-01-01 00:00:00
        :type StartTime: str
        :param EndTime: 结束时间，默认为当前时间。 endTime不能小于startTime
        :type EndTime: str
        :param Statistics: 统计类型
        :type Statistics: str
        """
        self.Namespace = None
        self.MetricName = None
        self.Dimensions = None
        self.Period = None
        self.StartTime = None
        self.EndTime = None
        self.Statistics = None

    def _deserialize(self, params):
        self.Namespace = params.get("Namespace")
        self.MetricName = params.get("MetricName")
        self.Dimensions = params.get("Dimensions")
        self.Period = params.get("Period")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Statistics = params.get("Statistics")


class GetMonitorDataResponse(AbstractModel):
    """GetMonitorData返回参数结构体"""

    def __init__(self):
        """
        :param MetricName: 监控指标
        :type MetricName: str
        :param StartTime: 数据点起始时间
        :type StartTime: str
        :param EndTime: 数据点结束时间
        :type EndTime: str
        :param Period: 数据统计周期
        :type Period: int
        :param DataPoints: 监控数据列表
        :type DataPoints: list of PointsObject
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.MetricName = None
        self.StartTime = None
        self.EndTime = None
        self.Period = None
        self.DataPoints = None
        self.RequestId = None

    def _deserialize(self, params):
        self.MetricName = params.get("MetricName")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Period = params.get("Period")
        if params.get("DataPoints") is not None:
            self.DataPoints = []
            for item in params.get("DataPoints"):
                obj = PointsObject()
                obj._deserialize(item)
                self.DataPoints.append(obj)
        self.RequestId = params.get("RequestId")


class MetricObject(AbstractModel):
    """对业务指标的单位及支持统计周期的描述"""

    def __init__(self):
        """
        :param Namespace: 命名空间，每个云产品会有一个命名空间
        :type Namespace: str
        :param MetricName: 指标名称
        :type MetricName: str
        :param Unit: 指标使用的单位
        :type Unit: str
        :param Period: 指标支持的统计周期，单位是秒，如60、300
        :type Period: list of int
        """
        self.Namespace = None
        self.MetricName = None
        self.Unit = None
        self.Period = None

    def _deserialize(self, params):
        self.Namespace = params.get("Namespace")
        self.MetricName = params.get("MetricName")
        self.Unit = params.get("Unit")
        self.Period = params.get("Period")


class PointsObject(AbstractModel):
    """实例对应的监控数据列表"""

    def __init__(self):
        """
        :param Dimensions: 监控实例的维度组合
        :type Dimensions: list of str
        :param Points: 监控数据点数组，每个点的时间跨度为一个Period值
        :type Points: list of float
        """
        self.Dimensions = None
        self.Points = None

    def _deserialize(self, params):
        self.Dimensions = params.get("Dimensions")
        self.Points = params.get("Points")

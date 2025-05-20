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

from common.cmp.cloud_apis.resource_apis.tcecloud.ckafka.v20190819 import models
from common.cmp.cloud_apis.resource_apis.tcecloud.common.abstract_client import AbstractClient
from common.cmp.cloud_apis.resource_apis.tcecloud.common.exception.tce_cloud_sdk_exception import TceCloudSDKException


class CkafkaClient(AbstractClient):
    _apiVersion = "2019-08-19"
    _endpoint = "ckafka.api3.{{conf.main_domain}}"

    def CreateAcl(self, request):
        """添加 ACL 策略

        :param request: 调用CreateAcl所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.CreateAclRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.CreateAclResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateAcl", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateAclResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreateConnector(self, request):
        """创建数据同步任务

        :param request: 调用CreateConnector所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.CreateConnectorRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.CreateConnectorResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateConnector", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateConnectorResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        :type request: :class:`tcecloud.ckafka.v20190819.models.CreateInstanceRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.CreateInstanceResponse`

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

    def CreateInstancePost(self, request):
        """创建按量计费实例

        :param request: 调用CreateInstancePost所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.CreateInstancePostRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.CreateInstancePostResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateInstancePost", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateInstancePostResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreateInstancePre(self, request):
        """创建实例(预付费包年包月)

        :param request: 调用CreateInstancePre所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.CreateInstancePreRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.CreateInstancePreResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateInstancePre", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateInstancePreResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreateInstanceTce(self, request):
        """创建tce实例

        :param request: 调用CreateInstanceTce所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.CreateInstanceTceRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.CreateInstanceTceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateInstanceTce", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateInstanceTceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreatePartition(self, request):
        """本接口用于增加主题中的分区

        :param request: 调用CreatePartition所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.CreatePartitionRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.CreatePartitionResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreatePartition", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreatePartitionResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreateRoute(self, request):
        """添加实例路由

        :param request: 调用CreateRoute所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.CreateRouteRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.CreateRouteResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateRoute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateRouteResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreateTopic(self, request):
        """创建ckafka主题

        :param request: 调用CreateTopic所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.CreateTopicRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.CreateTopicResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateTopic", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateTopicResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreateTopicIpWhiteList(self, request):
        """创建主题ip白名单

        :param request: 调用CreateTopicIpWhiteList所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.CreateTopicIpWhiteListRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.CreateTopicIpWhiteListResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateTopicIpWhiteList", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateTopicIpWhiteListResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreateUser(self, request):
        """添加用户

        :param request: 调用CreateUser所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.CreateUserRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.CreateUserResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateUser", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateUserResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteAcl(self, request):
        """删除ACL

        :param request: 调用DeleteAcl所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DeleteAclRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DeleteAclResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteAcl", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteAclResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteConnector(self, request):
        """删除Connector

        :param request: 调用DeleteConnector所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DeleteConnectorRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DeleteConnectorResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteConnector", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteConnectorResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        """删除实例

        :param request: 调用DeleteInstance所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DeleteInstanceRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DeleteInstanceResponse`

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

    def DeleteRoute(self, request):
        """删除路由

        :param request: 调用DeleteRoute所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DeleteRouteRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DeleteRouteResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteRoute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteRouteResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteTopic(self, request):
        """删除ckafka主题

        :param request: 调用DeleteTopic所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DeleteTopicRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DeleteTopicResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteTopic", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteTopicResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteTopicIpWhiteList(self, request):
        """删除主题IP白名单

        :param request: 调用DeleteTopicIpWhiteList所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DeleteTopicIpWhiteListRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DeleteTopicIpWhiteListResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteTopicIpWhiteList", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteTopicIpWhiteListResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteUser(self, request):
        """删除用户

        :param request: 调用DeleteUser所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DeleteUserRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DeleteUserResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteUser", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteUserResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeACL(self, request):
        """枚举ACL

        :param request: 调用DescribeACL所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeACLRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeACLResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeACL", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeACLResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeAppIdIsVip(self, request):
        """查询客户是否为大客户

        :param request: 调用DescribeAppIdIsVip所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeAppIdIsVipRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeAppIdIsVipResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeAppIdIsVip", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAppIdIsVipResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeAppInfo(self, request):
        """查询用户列表

        :param request: 调用DescribeAppInfo所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeAppInfoRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeAppInfoResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeAppInfo", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAppInfoResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeBrokers(self, request):
        """用于给运维提供枚举broker信息的接口

        :param request: 调用DescribeBrokers所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeBrokersRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeBrokersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeBrokers", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBrokersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeCkafkaPrice(self, request):
        """询价

        :param request: 调用DescribeCkafkaPrice所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeCkafkaPriceRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeCkafkaPriceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeCkafkaPrice", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCkafkaPriceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeCkafkaTypeConfigs(self, request):
        """获取实例规格配置

        :param request: 调用DescribeCkafkaTypeConfigs所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeCkafkaTypeConfigsRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeCkafkaTypeConfigsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeCkafkaTypeConfigs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCkafkaTypeConfigsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeCkafkaZone(self, request):
        """用于查看ckafka的可用区列表

        :param request: 调用DescribeCkafkaZone所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeCkafkaZoneRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeCkafkaZoneResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeCkafkaZone", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCkafkaZoneResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeConnector(self, request):
        """获取数据同步任务列表

        :param request: 调用DescribeConnector所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeConnectorRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeConnectorResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeConnector", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeConnectorResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeConnectorConfigs(self, request):
        """查询connector配置

        :param request: 调用DescribeConnectorConfigs所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeConnectorConfigsRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeConnectorConfigsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeConnectorConfigs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeConnectorConfigsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeConnectorStatus(self, request):
        """查询Connector状态

        :param request: 调用DescribeConnectorStatus所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeConnectorStatusRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeConnectorStatusResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeConnectorStatus", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeConnectorStatusResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeConsumerGroup(self, request):
        """查询消费分组信息

        :param request: 调用DescribeConsumerGroup所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeConsumerGroupRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeConsumerGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeConsumerGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeConsumerGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeGroup(self, request):
        """枚举消费分组(精简版)

        :param request: 调用DescribeGroup所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeGroupRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeGroupInfo(self, request):
        """获取消费分组信息

        :param request: 调用DescribeGroupInfo所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeGroupInfoRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeGroupInfoResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeGroupInfo", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeGroupInfoResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeGroupOffsets(self, request):
        """获取消费分组offset

        :param request: 调用DescribeGroupOffsets所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeGroupOffsetsRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeGroupOffsetsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeGroupOffsets", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeGroupOffsetsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeIfCommunity(self, request):
        """查询实例是否为社区版

        :param request: 调用DescribeIfCommunity所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeIfCommunityRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeIfCommunityResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeIfCommunity", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeIfCommunityResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeInstance(self, request):
        """本接口（DescribeInstance）用于在用户账户下获取消息队列 CKafka 实例列表

        :param request: 调用DescribeInstance所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeInstanceRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeInstanceAttributes(self, request):
        """获取实例属性

        :param request: 调用DescribeInstanceAttributes所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeInstanceAttributesRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeInstanceAttributesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstanceAttributes", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstanceAttributesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeInstanceDetail(self, request):
        """用户账户下获取实例列表详情

        :param request: 调用DescribeInstanceDetail所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeInstanceDetailRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeInstanceDetailResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstanceDetail", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstanceDetailResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        """本接口（DescribeInstance）用于在用户账户下获取消息队列 CKafka 实例列表

        :param request: 调用DescribeInstances所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeInstancesRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeInstancesResponse`

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

    def DescribeInstancesDetail(self, request):
        """用户账户下获取实例列表详情

        :param request: 调用DescribeInstancesDetail所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeInstancesDetailRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeInstancesDetailResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstancesDetail", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstancesDetailResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeRegion(self, request):
        """枚举地域

        :param request: 调用DescribeRegion所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeRegionRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeRegionResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRegion", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRegionResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeRoute(self, request):
        """查看路由信息

        :param request: 调用DescribeRoute所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeRouteRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeRouteResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRoute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRouteResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        """查询任务状态

        :param request: 调用DescribeTaskStatus所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeTaskStatusRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeTaskStatusResponse`

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

    def DescribeTopic(self, request):
        """接口请求域名：https://ckafka.tencentcloudapi.com
        本接口（DescribeTopic）用于在用户获取消息队列 CKafka 实例的主题列表

        :param request: 调用DescribeTopic所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeTopicRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeTopicResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeTopic", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTopicResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeTopicAttributes(self, request):
        """获取主题属性

        :param request: 调用DescribeTopicAttributes所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeTopicAttributesRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeTopicAttributesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeTopicAttributes", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTopicAttributesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeTopicDetail(self, request):
        """获取主题列表详情（仅控制台调用）

        :param request: 调用DescribeTopicDetail所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeTopicDetailRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeTopicDetailResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeTopicDetail", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTopicDetailResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeUser(self, request):
        """查询用户信息

        :param request: 调用DescribeUser所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.DescribeUserRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.DescribeUserResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeUser", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeUserResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyForward(self, request):
        """本接口  用于给消息队列 主题配置转发规则。

        :param request: 调用ModifyForward所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.ModifyForwardRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.ModifyForwardResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyForward", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyForwardResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyGroupOffsets(self, request):
        """设置Groups 消费分组offset

        :param request: 调用ModifyGroupOffsets所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.ModifyGroupOffsetsRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.ModifyGroupOffsetsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyGroupOffsets", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyGroupOffsetsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyInstanceAttributes(self, request):
        """设置实例属性

        :param request: 调用ModifyInstanceAttributes所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.ModifyInstanceAttributesRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.ModifyInstanceAttributesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyInstanceAttributes", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyInstanceAttributesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyPassword(self, request):
        """修改密码

        :param request: 调用ModifyPassword所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.ModifyPasswordRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.ModifyPasswordResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyPassword", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyPasswordResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyResourceTce(self, request):
        """修改实例

        :param request: 调用ModifyResourceTce所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.ModifyResourceTceRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.ModifyResourceTceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyResourceTce", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyResourceTceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyTopicAttributes(self, request):
        """本接口用于修改主题属性。

        :param request: 调用ModifyTopicAttributes所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.ModifyTopicAttributesRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.ModifyTopicAttributesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyTopicAttributes", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyTopicAttributesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def PauseConnector(self, request):
        """暂停数据同步任务

        :param request: 调用PauseConnector所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.PauseConnectorRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.PauseConnectorResponse`

        """
        try:
            params = request._serialize()
            body = self.call("PauseConnector", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.PauseConnectorResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def RenewInstance(self, request):
        """续费实例

        :param request: 调用RenewInstance所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.RenewInstanceRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.RenewInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("RenewInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.RenewInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ResumeConnector(self, request):
        """启动Connector任务

        :param request: 调用ResumeConnector所需参数的结构体。
        :type request: :class:`tcecloud.ckafka.v20190819.models.ResumeConnectorRequest`
        :rtype: :class:`tcecloud.ckafka.v20190819.models.ResumeConnectorResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ResumeConnector", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ResumeConnectorResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

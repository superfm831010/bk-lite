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
from common.cmp.cloud_apis.resource_apis.tcecloud.dcdb.v20180411 import models


class DcdbClient(AbstractClient):
    _apiVersion = "2018-04-11"
    _endpoint = "dcdb.api3.{{conf.main_domain}}"

    def ActiveDedicatedDBInstance(self, request):
        """本接口（ActiveDedicatedDBInstance）用于恢复已隔离的独享分布式数据库实例。

        :param request: 调用ActiveDedicatedDBInstance所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.ActiveDedicatedDBInstanceRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.ActiveDedicatedDBInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ActiveDedicatedDBInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ActiveDedicatedDBInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ActiveHourDCDBInstance(self, request):
        """本接口（ActiveHourDCDBInstance）用于恢复按量计费DCDB实例。

        :param request: 调用ActiveHourDCDBInstance所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.ActiveHourDCDBInstanceRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.ActiveHourDCDBInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ActiveHourDCDBInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ActiveHourDCDBInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def AuthenticateCAM(self, request):
        """本接口（AuthenticateCAM）为控制台提供预鉴权

        :param request: 调用AuthenticateCAM所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.AuthenticateCAMRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.AuthenticateCAMResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AuthenticateCAM", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AuthenticateCAMResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CheckIpStatus(self, request):
        """本接口(CheckIpStatus)用于查询指定的私有网络中的虚拟IP是否可用。

        :param request: 调用CheckIpStatus所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.CheckIpStatusRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.CheckIpStatusResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CheckIpStatus", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CheckIpStatusResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CloneAccount(self, request):
        """本接口（CloneAccount）用于克隆实例账户。

        :param request: 调用CloneAccount所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.CloneAccountRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.CloneAccountResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CloneAccount", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CloneAccountResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CloseDBExtranetAccess(self, request):
        """本接口(CloseDBExtranetAccess)用于关闭云数据库实例的外网访问。关闭外网访问后，外网地址将不可访问，查询实例列表接口将不返回对应实例的外网域名和端口信息。

        :param request: 调用CloseDBExtranetAccess所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.CloseDBExtranetAccessRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.CloseDBExtranetAccessResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CloseDBExtranetAccess", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CloseDBExtranetAccessResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CopyAccountPrivileges(self, request):
        """本接口（CopyAccountPrivileges）用于复制云数据库账号的权限。
        注意：相同用户名，不同Host是不同的账号，Readonly属性相同的账号之间才能复制权限。

        :param request: 调用CopyAccountPrivileges所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.CopyAccountPrivilegesRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.CopyAccountPrivilegesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CopyAccountPrivileges", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CopyAccountPrivilegesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreateAccount(self, request):
        """本接口（CreateAccount）用于创建云数据库账号。一个实例可以创建多个不同的账号，相同的用户名+不同的host是不同的账号。

        :param request: 调用CreateAccount所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.CreateAccountRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.CreateAccountResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateAccount", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateAccountResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreateDCDBInstance(self, request):
        """本接口（CreateDCDBInstance）用于创建包年包月的云数据库实例，可通过传入实例规格、数据库版本号、购买时长等信息创建云数据库实例。

        :param request: 调用CreateDCDBInstance所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.CreateDCDBInstanceRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.CreateDCDBInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateDCDBInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateDCDBInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreateHourDCDBInstance(self, request):
        """本接口（CreateHourDCDBInstance）用于创建按量计费的DCDB实例。

        :param request: 调用CreateHourDCDBInstance所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.CreateHourDCDBInstanceRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.CreateHourDCDBInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateHourDCDBInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateHourDCDBInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreateTmpDCDBInstance(self, request):
        """本接口（CreateTmpDCDBInstance）用于创建临时实例。

        :param request: 调用CreateTmpDCDBInstance所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.CreateTmpDCDBInstanceRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.CreateTmpDCDBInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateTmpDCDBInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateTmpDCDBInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteAccount(self, request):
        """本接口（DeleteAccount）用于删除云数据库账号。用户名+host唯一确定一个账号。

        :param request: 调用DeleteAccount所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DeleteAccountRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DeleteAccountResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteAccount", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteAccountResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteTmpInstance(self, request):
        """本接口（DeleteTmpInstance）用于删除临时实例。

        :param request: 调用DeleteTmpInstance所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DeleteTmpInstanceRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DeleteTmpInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteTmpInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteTmpInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeAccountPrivileges(self, request):
        """本接口（DescribeAccountPrivileges）用于查询云数据库账号权限。
        注意：注意：相同用户名，不同Host是不同的账号。

        :param request: 调用DescribeAccountPrivileges所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeAccountPrivilegesRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeAccountPrivilegesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeAccountPrivileges", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAccountPrivilegesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeAccounts(self, request):
        """本接口（DescribeAccounts）用于查询指定云数据库实例的账号列表。

        :param request: 调用DescribeAccounts所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeAccountsRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeAccountsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeAccounts", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAccountsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeAuditLogs(self, request):
        """本接口（DescribeAuditLogs）用于查询审计日志列表。

        :param request: 调用DescribeAuditLogs所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeAuditLogsRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeAuditLogsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeAuditLogs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAuditLogsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeAuditRuleDetail(self, request):
        """本接口（DescribeAuditRuleDetail）用于查询审计规则详情。

        :param request: 调用DescribeAuditRuleDetail所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeAuditRuleDetailRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeAuditRuleDetailResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeAuditRuleDetail", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAuditRuleDetailResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeAuditRules(self, request):
        """本接口（DescribeAuditRules）用于查询审计规则列表。

        :param request: 调用DescribeAuditRules所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeAuditRulesRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeAuditRulesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeAuditRules", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAuditRulesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeAuditStrategies(self, request):
        """本接口（DescribeAuditStrategies）用于查询某一个实例的审计策略列表。

        :param request: 调用DescribeAuditStrategies所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeAuditStrategiesRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeAuditStrategiesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeAuditStrategies", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAuditStrategiesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeAvailableExclusiveGroups(self, request):
        """本接口(DescribeAvailableExclusiveGroups)用于拉取独享资源池信息

        :param request: 调用DescribeAvailableExclusiveGroups所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeAvailableExclusiveGroupsRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeAvailableExclusiveGroupsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeAvailableExclusiveGroups", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAvailableExclusiveGroupsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeBatchDCDBRenewalPrice(self, request):
        """本接口（DescribeBatchDCDBRenewalPrice）用于在续费分布式数据库实例时，批量查询续费的价格。

        :param request: 调用DescribeBatchDCDBRenewalPrice所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeBatchDCDBRenewalPriceRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeBatchDCDBRenewalPriceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeBatchDCDBRenewalPrice", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBatchDCDBRenewalPriceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDBDetailMetrics(self, request):
        """本接口(DescribeDBDetailMetrics)用于查询云数据库主备详细监控指标。

        :param request: 调用DescribeDBDetailMetrics所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeDBDetailMetricsRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeDBDetailMetricsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDBDetailMetrics", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDBDetailMetricsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDBEngines(self, request):
        """本接口用于在调用创建接口前查询当前支持的数据库引擎列表

        :param request: 调用DescribeDBEngines所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeDBEnginesRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeDBEnginesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDBEngines", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDBEnginesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDBInstanceRsip(self, request):
        """本接口（DescribeDBInstanceRsip）用于获取实例Rsip

        :param request: 调用DescribeDBInstanceRsip所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeDBInstanceRsipRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeDBInstanceRsipResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDBInstanceRsip", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDBInstanceRsipResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDBLogFiles(self, request):
        """本接口(DescribeDBLogFiles)用于获取数据库的各种日志列表，包括冷备、binlog、errlog和slowlog。

        :param request: 调用DescribeDBLogFiles所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeDBLogFilesRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeDBLogFilesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDBLogFiles", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDBLogFilesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDBMetrics(self, request):
        """本接口(DescribeDBMetrics)用于查询云数据库监控指标。

        :param request: 调用DescribeDBMetrics所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeDBMetricsRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeDBMetricsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDBMetrics", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDBMetricsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDBParameters(self, request):
        """本接口(DescribeDBParameters)用于获取数据库的当前参数设置。

        :param request: 调用DescribeDBParameters所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeDBParametersRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeDBParametersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDBParameters", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDBParametersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDBSecurityGroups(self, request):
        """本接口(DescribeDBSecurityGroups)用于查询实例的安全组详情。

        :param request: 调用DescribeDBSecurityGroups所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeDBSecurityGroupsRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeDBSecurityGroupsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDBSecurityGroups", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDBSecurityGroupsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDBSlowLogAnalysis(self, request):
        """本接口(DescribeDBSlowLogAnalysis)用于获取慢查询记录详情。

        :param request: 调用DescribeDBSlowLogAnalysis所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeDBSlowLogAnalysisRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeDBSlowLogAnalysisResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDBSlowLogAnalysis", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDBSlowLogAnalysisResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDBSlowLogs(self, request):
        """本接口(DescribeDBSlowLogs)用于查询慢查询日志列表。

        :param request: 调用DescribeDBSlowLogs所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeDBSlowLogsRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeDBSlowLogsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDBSlowLogs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDBSlowLogsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDBSyncMode(self, request):
        """本接口（DescribeDBSyncMode）用于查询云数据库实例的同步模式。

        :param request: 调用DescribeDBSyncMode所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeDBSyncModeRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeDBSyncModeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDBSyncMode", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDBSyncModeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDBTmpInstances(self, request):
        """本接口（DescribeDBTmpInstances）用于获取实例回档生成的临时实例

        :param request: 调用DescribeDBTmpInstances所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeDBTmpInstancesRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeDBTmpInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDBTmpInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDBTmpInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDCDBBinlogTime(self, request):
        """本接口（DescribeDCDBBinlogTime）用于查询可回档时间范围。

        :param request: 调用DescribeDCDBBinlogTime所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeDCDBBinlogTimeRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeDCDBBinlogTimeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDCDBBinlogTime", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDCDBBinlogTimeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDCDBInstanceDetail(self, request):
        """本接口（DescribeDCDBInstanceDetail）用于获取DCDB实例详情

        :param request: 调用DescribeDCDBInstanceDetail所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeDCDBInstanceDetailRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeDCDBInstanceDetailResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDCDBInstanceDetail", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDCDBInstanceDetailResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDCDBInstances(self, request):
        """查询云数据库实例列表，支持通过项目ID、实例ID、内网地址、实例名称等来筛选实例。
        如果不指定任何筛选条件，则默认返回10条实例记录，单次请求最多支持返回100条实例记录。

        :param request: 调用DescribeDCDBInstances所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeDCDBInstancesRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeDCDBInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDCDBInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDCDBInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDCDBPrice(self, request):
        """本接口（DescribeDCDBPrice）用于在购买实例前，查询实例的价格。

        :param request: 调用DescribeDCDBPrice所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeDCDBPriceRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeDCDBPriceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDCDBPrice", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDCDBPriceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDCDBRenewalPrice(self, request):
        """本接口（DescribeDCDBRenewalPrice）用于在续费分布式数据库实例时，查询续费的价格。

        :param request: 调用DescribeDCDBRenewalPrice所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeDCDBRenewalPriceRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeDCDBRenewalPriceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDCDBRenewalPrice", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDCDBRenewalPriceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDCDBSaleInfo(self, request):
        """本接口(DescribeDCDBSaleInfo)用于查询分布式数据库可售卖的地域和可用区信息。

        :param request: 调用DescribeDCDBSaleInfo所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeDCDBSaleInfoRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeDCDBSaleInfoResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDCDBSaleInfo", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDCDBSaleInfoResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDCDBShards(self, request):
        """本接口（DescribeDCDBShards）用于查询云数据库实例的分片信息。

        :param request: 调用DescribeDCDBShards所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeDCDBShardsRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeDCDBShardsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDCDBShards", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDCDBShardsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDCDBUpgradePrice(self, request):
        """本接口（DescribeDCDBUpgradePrice）用于查询升级分布式数据库实例价格。

        :param request: 调用DescribeDCDBUpgradePrice所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeDCDBUpgradePriceRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeDCDBUpgradePriceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDCDBUpgradePrice", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDCDBUpgradePriceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDatabaseObjects(self, request):
        """本接口（DescribeDatabaseObjects）用于查询云数据库实例的数据库中的对象列表，包含表、存储过程、视图和函数。

        :param request: 调用DescribeDatabaseObjects所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeDatabaseObjectsRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeDatabaseObjectsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDatabaseObjects", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDatabaseObjectsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDatabaseTable(self, request):
        """本接口（DescribeDatabaseTable）用于查询云数据库实例的表信息。

        :param request: 调用DescribeDatabaseTable所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeDatabaseTableRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeDatabaseTableResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDatabaseTable", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDatabaseTableResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDatabases(self, request):
        """本接口（DescribeDatabases）用于查询云数据库实例的数据库列表。

        :param request: 调用DescribeDatabases所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeDatabasesRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeDatabasesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDatabases", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDatabasesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeFenceShardSpec(self, request):
        """本接口(DescribeFenceShardSpec)用于查询可创建的独享分布式数据库实例的规格配置。

        :param request: 调用DescribeFenceShardSpec所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeFenceShardSpecRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeFenceShardSpecResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeFenceShardSpec", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeFenceShardSpecResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeFlow(self, request):
        """本接口（DescribeFlow）用于查询流程状态

        :param request: 调用DescribeFlow所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeFlowRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeFlowResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeFlow", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeFlowResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        """本接口（DescribeInstances）用于云监控拉取实例列表

        :param request: 调用DescribeInstances所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeInstancesRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeInstancesResponse`

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

    def DescribeLatestCloudDBAReport(self, request):
        """本接口（DescribeLatestCloudDBAReport）用于获取最新的性能检测报告

        :param request: 调用DescribeLatestCloudDBAReport所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeLatestCloudDBAReportRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeLatestCloudDBAReportResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeLatestCloudDBAReport", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeLatestCloudDBAReportResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeLogFileRetentionPeriod(self, request):
        """本接口(DescribeLogFileRetentionPeriod)用于查看数据库备份日志的备份天数的设置情况。

        :param request: 调用DescribeLogFileRetentionPeriod所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeLogFileRetentionPeriodRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeLogFileRetentionPeriodResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeLogFileRetentionPeriod", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeLogFileRetentionPeriodResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeOrders(self, request):
        """本接口（DescribeOrders）用于查询分布式数据库订单信息。传入订单Id来查询订单关联的分布式数据库实例，和对应的任务流程ID。

        :param request: 调用DescribeOrders所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeOrdersRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeOrdersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeOrders", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeOrdersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeProjectSecurityGroups(self, request):
        """本接口(DescribeProjectSecurityGroups)用于查询项目的安全组详情。

        :param request: 调用DescribeProjectSecurityGroups所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeProjectSecurityGroupsRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeProjectSecurityGroupsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeProjectSecurityGroups", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeProjectSecurityGroupsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeProjects(self, request):
        """本接口（DescribeProjects）用于查询项目列表

        :param request: 调用DescribeProjects所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeProjectsRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeProjectsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeProjects", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeProjectsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeShardSpec(self, request):
        """查询可创建的分布式数据库可售卖的分片规格配置。

        :param request: 调用DescribeShardSpec所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeShardSpecRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeShardSpecResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeShardSpec", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeShardSpecResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeSqlLogs(self, request):
        """本接口（DescribeSqlLogs）用于获取实例SQL日志。

        :param request: 调用DescribeSqlLogs所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DescribeSqlLogsRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DescribeSqlLogsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeSqlLogs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeSqlLogsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DestroyHourDCDBInstance(self, request):
        """本接口（DestroyHourDCDBInstance）用于销毁按量计费实例。

        :param request: 调用DestroyHourDCDBInstance所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.DestroyHourDCDBInstanceRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.DestroyHourDCDBInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DestroyHourDCDBInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DestroyHourDCDBInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def GrantAccountPrivileges(self, request):
        """本接口（GrantAccountPrivileges）用于给云数据库账号赋权。
        注意：相同用户名，不同Host是不同的账号。

        :param request: 调用GrantAccountPrivileges所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.GrantAccountPrivilegesRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.GrantAccountPrivilegesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GrantAccountPrivileges", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GrantAccountPrivilegesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InitDCDBInstances(self, request):
        """本接口(InitDCDBInstances)用于初始化云数据库实例，包括设置默认字符集、表名大小写敏感等。

        :param request: 调用InitDCDBInstances所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.InitDCDBInstancesRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.InitDCDBInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InitDCDBInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InitDCDBInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def IsolateDedicatedDBInstance(self, request):
        """本接口（IsolateDedicatedDBInstance）用于隔离独享云数据库实例。

        :param request: 调用IsolateDedicatedDBInstance所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.IsolateDedicatedDBInstanceRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.IsolateDedicatedDBInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("IsolateDedicatedDBInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.IsolateDedicatedDBInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def IsolateHourDCDBInstance(self, request):
        """本接口（IsolateHourDCDBInstance）用于隔离按量计费DCDB实例。

        :param request: 调用IsolateHourDCDBInstance所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.IsolateHourDCDBInstanceRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.IsolateHourDCDBInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("IsolateHourDCDBInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.IsolateHourDCDBInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyAccountDescription(self, request):
        """本接口（ModifyAccountDescription）用于修改云数据库账号备注。
        注意：相同用户名，不同Host是不同的账号。

        :param request: 调用ModifyAccountDescription所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.ModifyAccountDescriptionRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.ModifyAccountDescriptionResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyAccountDescription", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyAccountDescriptionResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyAutoRenewFlag(self, request):
        """本接口（ModifyAutoRenewFlag）用于修改自动续费标记。

        :param request: 调用ModifyAutoRenewFlag所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.ModifyAutoRenewFlagRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.ModifyAutoRenewFlagResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyAutoRenewFlag", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyAutoRenewFlagResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyDBInstanceName(self, request):
        """本接口（ModifyDBInstanceName）用于修改实例名字

        :param request: 调用ModifyDBInstanceName所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.ModifyDBInstanceNameRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.ModifyDBInstanceNameResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyDBInstanceName", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyDBInstanceNameResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyDBInstanceSecurityGroups(self, request):
        """本接口(ModifyDBInstanceSecurityGroups)用于修改实例绑定的安全组

        :param request: 调用ModifyDBInstanceSecurityGroups所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.ModifyDBInstanceSecurityGroupsRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.ModifyDBInstanceSecurityGroupsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyDBInstanceSecurityGroups", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyDBInstanceSecurityGroupsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyDBInstancesProject(self, request):
        """本接口（ModifyDBInstancesProject）用于修改云数据库实例所属项目。

        :param request: 调用ModifyDBInstancesProject所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.ModifyDBInstancesProjectRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.ModifyDBInstancesProjectResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyDBInstancesProject", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyDBInstancesProjectResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyDBParameters(self, request):
        """本接口(ModifyDBParameters)用于修改数据库参数。

        :param request: 调用ModifyDBParameters所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.ModifyDBParametersRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.ModifyDBParametersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyDBParameters", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyDBParametersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyDBSyncMode(self, request):
        """本接口（ModifyDBSyncMode）用于修改云数据库实例的同步模式。

        :param request: 调用ModifyDBSyncMode所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.ModifyDBSyncModeRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.ModifyDBSyncModeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyDBSyncMode", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyDBSyncModeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyInstanceNetwork(self, request):
        """本接口（ModifyInstanceNetwork）用于修改实例所属网络。

        :param request: 调用ModifyInstanceNetwork所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.ModifyInstanceNetworkRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.ModifyInstanceNetworkResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyInstanceNetwork", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyInstanceNetworkResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyInstanceRemark(self, request):
        """本接口（ModifyInstanceRemark）用于修改实例备注。

        :param request: 调用ModifyInstanceRemark所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.ModifyInstanceRemarkRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.ModifyInstanceRemarkResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyInstanceRemark", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyInstanceRemarkResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyInstanceVip(self, request):
        """本接口（ModifyInstanceVip）用于修改实例Vip

        :param request: 调用ModifyInstanceVip所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.ModifyInstanceVipRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.ModifyInstanceVipResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyInstanceVip", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyInstanceVipResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyInstanceVport(self, request):
        """本接口（ModifyInstanceVport）用于修改实例Vport

        :param request: 调用ModifyInstanceVport所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.ModifyInstanceVportRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.ModifyInstanceVportResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyInstanceVport", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyInstanceVportResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyLogFileRetentionPeriod(self, request):
        """本接口(ModifyLogFileRetentionPeriod)用于修改数据库备份日志保存天数。

        :param request: 调用ModifyLogFileRetentionPeriod所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.ModifyLogFileRetentionPeriodRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.ModifyLogFileRetentionPeriodResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyLogFileRetentionPeriod", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyLogFileRetentionPeriodResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def OpenDBExtranetAccess(self, request):
        """本接口（OpenDBExtranetAccess）用于开通云数据库实例的外网访问。开通外网访问后，您可通过外网域名和端口访问实例，可使用查询实例列表接口获取外网域名和端口信息。

        :param request: 调用OpenDBExtranetAccess所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.OpenDBExtranetAccessRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.OpenDBExtranetAccessResponse`

        """
        try:
            params = request._serialize()
            body = self.call("OpenDBExtranetAccess", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.OpenDBExtranetAccessResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def RenewDCDBInstance(self, request):
        """本接口（RenewDCDBInstance）用于续费分布式数据库实例。

        :param request: 调用RenewDCDBInstance所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.RenewDCDBInstanceRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.RenewDCDBInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("RenewDCDBInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.RenewDCDBInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ResetAccountPassword(self, request):
        """本接口（ResetAccountPassword）用于重置云数据库账号的密码。
        注意：相同用户名，不同Host是不同的账号。

        :param request: 调用ResetAccountPassword所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.ResetAccountPasswordRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.ResetAccountPasswordResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ResetAccountPassword", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ResetAccountPasswordResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def StartSmartDBA(self, request):
        """本接口（StartSmartDBA）用于启动性能检测任务。

        :param request: 调用StartSmartDBA所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.StartSmartDBARequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.StartSmartDBAResponse`

        """
        try:
            params = request._serialize()
            body = self.call("StartSmartDBA", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.StartSmartDBAResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def SwitchRollbackInstance(self, request):
        """本接口（SwitchRollbackInstance）用于切换回档实例。

        :param request: 调用SwitchRollbackInstance所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.SwitchRollbackInstanceRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.SwitchRollbackInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SwitchRollbackInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SwitchRollbackInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def TerminateDedicatedDBInstance(self, request):
        """本接口（IsolateDedicatedDBInstance）用于销毁已隔离的独享分布式数据库实例。

        :param request: 调用TerminateDedicatedDBInstance所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.TerminateDedicatedDBInstanceRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.TerminateDedicatedDBInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("TerminateDedicatedDBInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.TerminateDedicatedDBInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def UpgradeDCDBInstance(self, request):
        """本接口（UpgradeDCDBInstance）用于升级分布式数据库实例。本接口完成下单和支付两个动作，如果发生支付失败的错误，调用用户账户相关接口中的支付订单接口（PayDeals）重新支付即可。

        :param request: 调用UpgradeDCDBInstance所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.UpgradeDCDBInstanceRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.UpgradeDCDBInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("UpgradeDCDBInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UpgradeDCDBInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def UpgradeDedicatedDCDBInstance(self, request):
        """本接口（UpgradeDedicatedDCDBInstance）用于升级独享DCDB实例

        :param request: 调用UpgradeDedicatedDCDBInstance所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.UpgradeDedicatedDCDBInstanceRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.UpgradeDedicatedDCDBInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("UpgradeDedicatedDCDBInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UpgradeDedicatedDCDBInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def UpgradeHourDCDBInstance(self, request):
        """本接口（UpgradeHourDCDBInstance）用于升级升级按量计费DCDB实例

        :param request: 调用UpgradeHourDCDBInstance所需参数的结构体。
        :type request: :class:`tcecloud.dcdb.v20180411.models.UpgradeHourDCDBInstanceRequest`
        :rtype: :class:`tcecloud.dcdb.v20180411.models.UpgradeHourDCDBInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("UpgradeHourDCDBInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UpgradeHourDCDBInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

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
from common.cmp.cloud_apis.resource_apis.tcecloud.mariadb.v20170312 import models


class MariadbClient(AbstractClient):
    _apiVersion = "2017-03-12"
    _endpoint = "mariadb.api3.{{conf.main_domain}}"

    def ActiveDedicatedDBInstance(self, request):
        """本接口（ActiveDedicatedDBInstance）用于恢复已隔离的独享云数据库实例。

        :param request: 调用ActiveDedicatedDBInstance所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.ActiveDedicatedDBInstanceRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.ActiveDedicatedDBInstanceResponse`

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

    def ActiveHourDBInstance(self, request):
        """本接口（ActiveHourDBInstance）用于恢复隔离的按量计费实例。

        :param request: 调用ActiveHourDBInstance所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.ActiveHourDBInstanceRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.ActiveHourDBInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ActiveHourDBInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ActiveHourDBInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        """本接口为控制台提供预鉴权

        :param request: 调用AuthenticateCAM所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.AuthenticateCAMRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.AuthenticateCAMResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.CheckIpStatusRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.CheckIpStatusResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.CloneAccountRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.CloneAccountResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.CloseDBExtranetAccessRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.CloseDBExtranetAccessResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.CopyAccountPrivilegesRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.CopyAccountPrivilegesResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.CreateAccountRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.CreateAccountResponse`

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

    def CreateConfigTemplate(self, request):
        """本接口（CreateConfigTemplate）用于创建参数模板。

        :param request: 调用CreateConfigTemplate所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.CreateConfigTemplateRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.CreateConfigTemplateResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateConfigTemplate", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateConfigTemplateResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreateDBInstance(self, request):
        """本接口（CreateDBInstance）用于创建包年包月的云数据库实例，可通过传入实例规格、数据库版本号、购买时长和数量等信息创建云数据库实例。

        :param request: 调用CreateDBInstance所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.CreateDBInstanceRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.CreateDBInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateDBInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateDBInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreateHourDBInstance(self, request):
        """本接口（CreateHourDBInstance）用于创建按量计费实例。

        :param request: 调用CreateHourDBInstance所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.CreateHourDBInstanceRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.CreateHourDBInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateHourDBInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateHourDBInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreateTmpInstances(self, request):
        """本接口（CreateTmpInstances）用于创建临时实例。

        :param request: 调用CreateTmpInstances所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.CreateTmpInstancesRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.CreateTmpInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateTmpInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateTmpInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DeleteAccountRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DeleteAccountResponse`

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

    def DeleteConfigTemplate(self, request):
        """本接口（DeleteConfigTemplate）用于删除参数模板。

        :param request: 调用DeleteConfigTemplate所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DeleteConfigTemplateRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DeleteConfigTemplateResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteConfigTemplate", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteConfigTemplateResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DeleteTmpInstanceRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DeleteTmpInstanceResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeAccountPrivilegesRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeAccountPrivilegesResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeAccountsRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeAccountsResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeAuditLogsRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeAuditLogsResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeAuditRuleDetailRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeAuditRuleDetailResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeAuditRulesRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeAuditRulesResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeAuditStrategiesRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeAuditStrategiesResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeAvailableExclusiveGroupsRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeAvailableExclusiveGroupsResponse`

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

    def DescribeBackupTime(self, request):
        """本接口（DescribeBackupTime）用于获取云数据库的备份时间。后台系统将根据此配置定期进行实例备份。

        :param request: 调用DescribeBackupTime所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeBackupTimeRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeBackupTimeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeBackupTime", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBackupTimeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeBatchRenewalPrice(self, request):
        """本接口（DescribeBatchRenewalPrice）用于批量实例续费询价

        :param request: 调用DescribeBatchRenewalPrice所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeBatchRenewalPriceRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeBatchRenewalPriceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeBatchRenewalPrice", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBatchRenewalPriceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeBinlogTime(self, request):
        """本接口（DescribeBinlogTime）用于查询可回档时间范围。

        :param request: 调用DescribeBinlogTime所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeBinlogTimeRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeBinlogTimeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeBinlogTime", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBinlogTimeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeConfigHistories(self, request):
        """本接口（DescribeConfigHistories）用于查询配置历史列表。

        :param request: 调用DescribeConfigHistories所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeConfigHistoriesRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeConfigHistoriesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeConfigHistories", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeConfigHistoriesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeConfigTemplate(self, request):
        """本接口（DescribeConfigTemplate）用于查询参数模板详情。

        :param request: 调用DescribeConfigTemplate所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeConfigTemplateRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeConfigTemplateResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeConfigTemplate", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeConfigTemplateResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeConfigTemplates(self, request):
        """本接口（DescribeConfigTemplates）用于查询参数模板列表。

        :param request: 调用DescribeConfigTemplates所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeConfigTemplatesRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeConfigTemplatesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeConfigTemplates", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeConfigTemplatesResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeDBDetailMetricsRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeDBDetailMetricsResponse`

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

    def DescribeDBEncryptAttributes(self, request):
        """本接口(DescribeDBEncryptAttributes)用于查询实例数据加密状态。

        :param request: 调用DescribeDBEncryptAttributes所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeDBEncryptAttributesRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeDBEncryptAttributesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDBEncryptAttributes", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDBEncryptAttributesResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeDBEnginesRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeDBEnginesResponse`

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

    def DescribeDBInstanceDetail(self, request):
        """本接口(DescribeDBInstanceDetail)用于查询指定实例的详细信息。

        :param request: 调用DescribeDBInstanceDetail所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeDBInstanceDetailRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeDBInstanceDetailResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDBInstanceDetail", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDBInstanceDetailResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDBInstanceHAInfo(self, request):
        """本接口（DescribeDBInstanceHAInfo）用于查询数据库实例的当前主可用区及主备切换状态。

        :param request: 调用DescribeDBInstanceHAInfo所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeDBInstanceHAInfoRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeDBInstanceHAInfoResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDBInstanceHAInfo", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDBInstanceHAInfoResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeDBInstanceRsipRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeDBInstanceRsipResponse`

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

    def DescribeDBInstanceSpecs(self, request):
        """本接口(DescribeDBInstanceSpecs)用于查询可创建的云数据库可售卖的规格配置。

        :param request: 调用DescribeDBInstanceSpecs所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeDBInstanceSpecsRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeDBInstanceSpecsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDBInstanceSpecs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDBInstanceSpecsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDBInstances(self, request):
        """本接口（DescribeDBInstances）用于查询云数据库实例列表，支持通过项目ID、实例ID、内网地址、实例名称等来筛选实例。
        如果不指定任何筛选条件，则默认返回20条实例记录，单次请求最多支持返回100条实例记录。

        :param request: 调用DescribeDBInstances所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeDBInstancesRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeDBInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDBInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDBInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeDBLogFilesRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeDBLogFilesResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeDBMetricsRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeDBMetricsResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeDBParametersRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeDBParametersResponse`

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

    def DescribeDBPerformance(self, request):
        """本接口(DescribeDBPerformance)用于查看数据库实例当前性能数据。

        :param request: 调用DescribeDBPerformance所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeDBPerformanceRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeDBPerformanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDBPerformance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDBPerformanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDBPerformanceDetails(self, request):
        """本接口(DescribeDBPerformanceDetails)用于查看实例性能数据详情。

        :param request: 调用DescribeDBPerformanceDetails所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeDBPerformanceDetailsRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeDBPerformanceDetailsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDBPerformanceDetails", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDBPerformanceDetailsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDBResourceUsage(self, request):
        """本接口(DescribeDBResourceUsage)用于查看数据库实例资源的使用情况。

        :param request: 调用DescribeDBResourceUsage所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeDBResourceUsageRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeDBResourceUsageResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDBResourceUsage", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDBResourceUsageResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDBResourceUsageDetails(self, request):
        """本接口(DescribeDBResourceUsageDetails)用于查看数据库实例当前性能数据。

        :param request: 调用DescribeDBResourceUsageDetails所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeDBResourceUsageDetailsRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeDBResourceUsageDetailsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDBResourceUsageDetails", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDBResourceUsageDetailsResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeDBSecurityGroupsRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeDBSecurityGroupsResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeDBSlowLogAnalysisRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeDBSlowLogAnalysisResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeDBSlowLogsRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeDBSlowLogsResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeDBSyncModeRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeDBSyncModeResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeDBTmpInstancesRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeDBTmpInstancesResponse`

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

    def DescribeDatabaseObjects(self, request):
        """本接口（DescribeDatabaseObjects）用于查询云数据库实例的数据库中的对象列表，包含表、存储过程、视图和函数。

        :param request: 调用DescribeDatabaseObjects所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeDatabaseObjectsRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeDatabaseObjectsResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeDatabaseTableRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeDatabaseTableResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeDatabasesRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeDatabasesResponse`

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

    def DescribeDefaultConfigTemplate(self, request):
        """本接口（DescribeDefaultConfigTemplate）用于查询默认参数模板信息。

        :param request: 调用DescribeDefaultConfigTemplate所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeDefaultConfigTemplateRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeDefaultConfigTemplateResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDefaultConfigTemplate", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDefaultConfigTemplateResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeFenceDBInstanceSpecs(self, request):
        """本接口(DescribeFenceShardSpec)用于查询可创建的独享云数据库实例的规格配置。

        :param request: 调用DescribeFenceDBInstanceSpecs所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeFenceDBInstanceSpecsRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeFenceDBInstanceSpecsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeFenceDBInstanceSpecs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeFenceDBInstanceSpecsResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        """本接口（DescribeFlow）用于查询流程状态。

        :param request: 调用DescribeFlow所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeFlowRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeFlowResponse`

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

    def DescribeInstanceProxyConfig(self, request):
        """本接口（DescribeInstanceProxyConfig）用于拉取实例网关配置

        :param request: 调用DescribeInstanceProxyConfig所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeInstanceProxyConfigRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeInstanceProxyConfigResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstanceProxyConfig", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstanceProxyConfigResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeInstanceSSLAttributes(self, request):
        """本接口（DescribeInstanceSSLAttributes）用于拉取实例SSL认证属性

        :param request: 调用DescribeInstanceSSLAttributes所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeInstanceSSLAttributesRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeInstanceSSLAttributesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstanceSSLAttributes", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstanceSSLAttributesResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        """本接口（DescribeInstances）用于拉取实例信息，Barad使用。

        :param request: 调用DescribeInstances所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeInstancesRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeInstancesResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeLatestCloudDBAReportRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeLatestCloudDBAReportResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeLogFileRetentionPeriodRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeLogFileRetentionPeriodResponse`

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
        """本接口（DescribeOrders）用于查询云数据库订单信息。传入订单Id来查询订单关联的云数据库实例，和对应的任务流程ID。

        :param request: 调用DescribeOrders所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeOrdersRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeOrdersResponse`

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

    def DescribePrice(self, request):
        """本接口（DescribePrice）用于在购买实例前，查询实例的价格。

        :param request: 调用DescribePrice所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribePriceRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribePriceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribePrice", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribePriceResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeProjectSecurityGroupsRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeProjectSecurityGroupsResponse`

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
        """本接口（DescribeProjects）用于查询项目列表。

        :param request: 调用DescribeProjects所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeProjectsRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeProjectsResponse`

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

    def DescribeRenewalPrice(self, request):
        """本接口（DescribeRenewalPrice）用于在续费云数据库实例时，查询续费的价格。

        :param request: 调用DescribeRenewalPrice所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeRenewalPriceRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeRenewalPriceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRenewalPrice", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRenewalPriceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeSaleInfo(self, request):
        """本接口(DescribeSaleInfo)用于查询云数据库可售卖的地域和可用区信息。

        :param request: 调用DescribeSaleInfo所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeSaleInfoRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeSaleInfoResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeSaleInfo", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeSaleInfoResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeSqlLogsRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeSqlLogsResponse`

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

    def DescribeSyncTasks(self, request):
        """本接口（DescribeSyncTasks）用于拉取多源同步任务列表

        :param request: 调用DescribeSyncTasks所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeSyncTasksRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeSyncTasksResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeSyncTasks", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeSyncTasksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeUpgradePrice(self, request):
        """本接口（DescribeUpgradePrice）用于在扩容云数据库实例时，查询扩容的价格。

        :param request: 调用DescribeUpgradePrice所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeUpgradePriceRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeUpgradePriceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeUpgradePrice", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeUpgradePriceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeUserTasks(self, request):
        """本接口（DescribeUserTasks）用于查询用户任务列表。

        :param request: 调用DescribeUserTasks所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DescribeUserTasksRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DescribeUserTasksResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeUserTasks", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeUserTasksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DestroyHourDBInstance(self, request):
        """本接口（DestroyHourDBInstance）用于销毁按量计费实例。

        :param request: 调用DestroyHourDBInstance所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.DestroyHourDBInstanceRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.DestroyHourDBInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DestroyHourDBInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DestroyHourDBInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        :type request: :class:`tcecloud.mariadb.v20170312.models.GrantAccountPrivilegesRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.GrantAccountPrivilegesResponse`

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

    def InitDBInstances(self, request):
        """本接口(InitDBInstances)用于初始化云数据库实例，包括设置默认字符集、表名大小写敏感等。

        :param request: 调用InitDBInstances所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.InitDBInstancesRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.InitDBInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InitDBInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InitDBInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        :type request: :class:`tcecloud.mariadb.v20170312.models.IsolateDedicatedDBInstanceRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.IsolateDedicatedDBInstanceResponse`

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

    def IsolateHourDBInstance(self, request):
        """本接口（IsolateHourDBInstance）用于隔离按量计费实例。

        :param request: 调用IsolateHourDBInstance所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.IsolateHourDBInstanceRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.IsolateHourDBInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("IsolateHourDBInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.IsolateHourDBInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        :type request: :class:`tcecloud.mariadb.v20170312.models.ModifyAccountDescriptionRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.ModifyAccountDescriptionResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.ModifyAutoRenewFlagRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.ModifyAutoRenewFlagResponse`

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

    def ModifyBackupTime(self, request):
        """本接口（ModifyBackupTime）用于设置云数据库实例的备份时间。后台系统将根据此配置定期进行实例备份。

        :param request: 调用ModifyBackupTime所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.ModifyBackupTimeRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.ModifyBackupTimeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyBackupTime", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyBackupTimeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyConfigTemplate(self, request):
        """本接口（ModifyConfigTemplate）用于修改参数模板。

        :param request: 调用ModifyConfigTemplate所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.ModifyConfigTemplateRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.ModifyConfigTemplateResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyConfigTemplate", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyConfigTemplateResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyDBEncryptAttributes(self, request):
        """本接口(ModifyDBEncryptAttributes)用于修改实例数据加密。

        :param request: 调用ModifyDBEncryptAttributes所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.ModifyDBEncryptAttributesRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.ModifyDBEncryptAttributesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyDBEncryptAttributes", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyDBEncryptAttributesResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        """本接口（ModifyDBInstanceName）用于修改云数据库实例的名称。

        :param request: 调用ModifyDBInstanceName所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.ModifyDBInstanceNameRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.ModifyDBInstanceNameResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.ModifyDBInstanceSecurityGroupsRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.ModifyDBInstanceSecurityGroupsResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.ModifyDBInstancesProjectRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.ModifyDBInstancesProjectResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.ModifyDBParametersRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.ModifyDBParametersResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.ModifyDBSyncModeRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.ModifyDBSyncModeResponse`

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
        """本接口（ModifyInstanceNetwork）用于修改实例所属网络

        :param request: 调用ModifyInstanceNetwork所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.ModifyInstanceNetworkRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.ModifyInstanceNetworkResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.ModifyInstanceRemarkRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.ModifyInstanceRemarkResponse`

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

    def ModifyInstanceSSLAttributes(self, request):
        """本接口  （ModifyInstanceSSLAttributes）用于修改实例SSL认证功能属性

        :param request: 调用ModifyInstanceSSLAttributes所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.ModifyInstanceSSLAttributesRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.ModifyInstanceSSLAttributesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyInstanceSSLAttributes", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyInstanceSSLAttributesResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        """本接口（ModifyInstanceVip）用于修改实例VIP

        :param request: 调用ModifyInstanceVip所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.ModifyInstanceVipRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.ModifyInstanceVipResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.ModifyInstanceVportRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.ModifyInstanceVportResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.ModifyLogFileRetentionPeriodRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.ModifyLogFileRetentionPeriodResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.OpenDBExtranetAccessRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.OpenDBExtranetAccessResponse`

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

    def RenewDBInstance(self, request):
        """本接口（RenewDBInstance）用于续费云数据库实例。

        :param request: 调用RenewDBInstance所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.RenewDBInstanceRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.RenewDBInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("RenewDBInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.RenewDBInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        :type request: :class:`tcecloud.mariadb.v20170312.models.ResetAccountPasswordRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.ResetAccountPasswordResponse`

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
        :type request: :class:`tcecloud.mariadb.v20170312.models.StartSmartDBARequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.StartSmartDBAResponse`

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

    def SwitchDBInstanceHA(self, request):
        """本接口（SwitchDBInstanceHA）用于发起实例主备切换。

        :param request: 调用SwitchDBInstanceHA所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.SwitchDBInstanceHARequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.SwitchDBInstanceHAResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SwitchDBInstanceHA", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SwitchDBInstanceHAResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        :type request: :class:`tcecloud.mariadb.v20170312.models.SwitchRollbackInstanceRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.SwitchRollbackInstanceResponse`

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
        """本接口（IsolateDedicatedDBInstance）用于销毁已隔离的独享云数据库实例。

        :param request: 调用TerminateDedicatedDBInstance所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.TerminateDedicatedDBInstanceRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.TerminateDedicatedDBInstanceResponse`

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

    def UpgradeDBInstance(self, request):
        """本接口(UpgradeDBInstance)用于扩容云数据库实例。本接口完成下单和支付两个动作，如果发生支付失败的错误，调用用户账户相关接口中的支付订单接口（PayDeals）重新支付即可。

        :param request: 调用UpgradeDBInstance所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.UpgradeDBInstanceRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.UpgradeDBInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("UpgradeDBInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UpgradeDBInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def UpgradeDedicatedDBInstance(self, request):
        """本接口(UpgradeDedicatedDBInstance)用于扩容独享云数据库实例。

        :param request: 调用UpgradeDedicatedDBInstance所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.UpgradeDedicatedDBInstanceRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.UpgradeDedicatedDBInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("UpgradeDedicatedDBInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UpgradeDedicatedDBInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def UpgradeHourDBInstance(self, request):
        """本接口（UpgradeHourDBInstance）用于升级按量计费的规格。

        :param request: 调用UpgradeHourDBInstance所需参数的结构体。
        :type request: :class:`tcecloud.mariadb.v20170312.models.UpgradeHourDBInstanceRequest`
        :rtype: :class:`tcecloud.mariadb.v20170312.models.UpgradeHourDBInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("UpgradeHourDBInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UpgradeHourDBInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

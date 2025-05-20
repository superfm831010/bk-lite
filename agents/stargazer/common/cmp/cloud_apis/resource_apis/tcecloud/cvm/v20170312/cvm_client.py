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
from common.cmp.cloud_apis.resource_apis.tcecloud.cvm.v20170312 import models


class CvmClient(AbstractClient):
    _apiVersion = "2017-03-12"
    _endpoint = "cvm.api3.{{conf.main_domain}}"

    def AllocateAddresses(self, request):
        """本接口 (AllocateAddresses) 用于申请一个或多个弹性公网IP（简称 EIP）。
        * EIP 是专为动态云计算设计的静态 IP 地址。借助 EIP，您可以快速将 EIP 重新映射到您的另一个实例上，从而屏蔽实例故障。
        * 您的 EIP 与Tce账户相关联，而不是与某个实例相关联。在您选择显式释放该地址，或欠费超过七天之前，它会一直与您的Tce账户保持关联。
        * 平台对用户每地域能申请的 EIP 最大配额有所限制，可参见 EIP 产品简介，上述配额可通过 DescribeAddressQuota 接口获取。

        :param request: 调用AllocateAddresses所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.AllocateAddressesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.AllocateAddressesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AllocateAddresses", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AllocateAddressesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def AllocateHosts(self, request):
        """本接口 (AllocateHosts) 用于创建一个或多个指定配置的CDH实例。
        * 当HostChargeType为PREPAID时，必须指定HostChargePrepaid参数。

        :param request: 调用AllocateHosts所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.AllocateHostsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.AllocateHostsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AllocateHosts", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AllocateHostsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def AssociateAddress(self, request):
        """本接口 (AssociateAddress) 用于将弹性公网IP（简称 EIP）绑定到实例或弹性网卡的指定内网 IP 上。
        * 将 EIP 绑定到实例上，其本质是将 EIP 绑定到实例上主网卡的主内网 IP 上。
        * 将 EIP 绑定到主网卡的主内网IP上，绑定过程会把其上绑定的普通公网 IP 自动解绑并释放。
        * 如果指定网卡的内网 IP 已经绑定了 EIP，则必须先解绑该 EIP，才能再绑定新的。
        * EIP 如果欠费或被封堵，则不能被绑定。
        * 只有状态为 UNBIND 的 EIP 才能够被绑定。

        :param request: 调用AssociateAddress所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.AssociateAddressRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.AssociateAddressResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AssociateAddress", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AssociateAddressResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def AssociateInstancesKeyPairs(self, request):
        """本接口 (AssociateInstancesKeyPairs) 用于将密钥绑定到实例上。

        * 将密钥的公钥写入到实例的`SSH`配置当中，用户就可以通过该密钥的私钥来登录实例。
        * 如果实例原来绑定过密钥，那么原来的密钥将失效。
        * 如果实例原来是通过密码登录，绑定密钥后无法使用密码登录。
        * 支持批量操作。每次请求批量实例的上限为100。如果批量实例存在不允许操作的实例，操作会以特定错误码返回。

        :param request: 调用AssociateInstancesKeyPairs所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.AssociateInstancesKeyPairsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.AssociateInstancesKeyPairsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AssociateInstancesKeyPairs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AssociateInstancesKeyPairsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def AssociateSecurityGroups(self, request):
        """本接口 (AssociateSecurityGroups) 用于绑定安全组到指定实例。

        :param request: 调用AssociateSecurityGroups所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.AssociateSecurityGroupsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.AssociateSecurityGroupsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AssociateSecurityGroups", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AssociateSecurityGroupsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def AuditMarketImage(self, request):
        """None

        :param request: 调用AuditMarketImage所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.AuditMarketImageRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.AuditMarketImageResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AuditMarketImage", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AuditMarketImageResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CancelAuditMarketImage(self, request):
        """None

        :param request: 调用CancelAuditMarketImage所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.CancelAuditMarketImageRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.CancelAuditMarketImageResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CancelAuditMarketImage", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CancelAuditMarketImageResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CheckInstancesConnectivity(self, request):
        """本接口 (DescribeInstancesConnectivity) 用于查询一个或多个实例的网络连通性，包括操作系统默认的远程登录服务端口和ICMP。
        - 如果是Linux操作系统，会检查默认远程登录端口号 22
        - 如果是Windows操作系统，会检查默认远程登录端口号3389

        :param request: 调用CheckInstancesConnectivity所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.CheckInstancesConnectivityRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.CheckInstancesConnectivityResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CheckInstancesConnectivity", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CheckInstancesConnectivityResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ColdMigrate(self, request):
        """冷迁移实例

        :param request: 调用ColdMigrate所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ColdMigrateRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ColdMigrateResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ColdMigrate", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ColdMigrateResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ColdMigrateInstance(self, request):
        """离线实例迁移。用于将一个系统盘镜像迁移到一个实例中。用户需要首先在Tce创建一个实例，然后通过本接口将需要运行的操作系统系统盘镜像迁移到该实例，实例的配置信息保持不变。
        注意：为了防止兼容性错误，建议用户在创建实例的时候尽量选取与需要迁移的系统盘相似的操作系统。

        :param request: 调用ColdMigrateInstance所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ColdMigrateInstanceRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ColdMigrateInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ColdMigrateInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ColdMigrateInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CopyInstanceDisk(self, request):
        """本接口 (CopyInstanceDisk) 用于拷贝实例的系统盘到弹性云硬盘。

        * 实例需要处于`关机`状态。
        * 需要指定未挂载、非加密弹性云硬盘，并且容量大于等于系统盘容量。
        * 实例与待挂载的磁盘需要在同一个可用区。

        :param request: 调用CopyInstanceDisk所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.CopyInstanceDiskRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.CopyInstanceDiskResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CopyInstanceDisk", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CopyInstanceDiskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreateDisasterRecoverGroup(self, request):
        """创建容灾组，该功能对资源挑战较大，请谨慎使用。创建好的容灾组，可在创建实例的时指定。

        :param request: 调用CreateDisasterRecoverGroup所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.CreateDisasterRecoverGroupRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.CreateDisasterRecoverGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateDisasterRecoverGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateDisasterRecoverGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreateImage(self, request):
        """本接口(CreateImage)用于将实例的系统盘制作为新镜像，创建后的镜像可以用于创建实例。

        :param request: 调用CreateImage所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.CreateImageRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.CreateImageResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateImage", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateImageResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreateKeyPair(self, request):
        """本接口 (CreateKeyPair) 用于创建一个 `OpenSSH RSA` 密钥对，可以用于登录 `Linux` 实例。

        * 开发者只需指定密钥对名称，即可由系统自动创建密钥对，并返回所生成的密钥对的 `ID` 及其公钥、私钥的内容。
        * 密钥对名称不能和已经存在的密钥对的名称重复。
        * 私钥的内容可以保存到文件中作为 `SSH` 的一种认证方式。
        * Tce不会保存用户的私钥，请妥善保管。

        :param request: 调用CreateKeyPair所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.CreateKeyPairRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.CreateKeyPairResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateKeyPair", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateKeyPairResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteDisasterRecoverGroup(self, request):
        """删除容灾组,仅空容灾组才能被删除。

        :param request: 调用DeleteDisasterRecoverGroup所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DeleteDisasterRecoverGroupRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DeleteDisasterRecoverGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteDisasterRecoverGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteDisasterRecoverGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteDisasterRecoverGroups(self, request):
        """本接口 (DeleteDisasterRecoverGroups)用于删除分散置放群组。只有空的置放群组才能被删除，非空的群组需要先销毁组内所有云服务器，才能执行删除操作，不然会产生删除置放群组失败的错误。

        :param request: 调用DeleteDisasterRecoverGroups所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DeleteDisasterRecoverGroupsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DeleteDisasterRecoverGroupsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteDisasterRecoverGroups", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteDisasterRecoverGroupsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteImages(self, request):
        """本接口（DeleteImages）用于删除一个或多个镜像。

        * 当镜像状态为`创建中`和`使用中`时, 不允许删除。镜像状态可以通过DescribeImages获取。
        * 每个地域最多只支持创建10个自定义镜像，删除镜像可以释放账户的配额。
        * 当镜像正在被其它账户分享时，不允许删除。

        :param request: 调用DeleteImages所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DeleteImagesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DeleteImagesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteImages", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteImagesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteInstancesActionTimer(self, request):
        """删除定时任务

        :param request: 调用DeleteInstancesActionTimer所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DeleteInstancesActionTimerRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DeleteInstancesActionTimerResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteInstancesActionTimer", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteInstancesActionTimerResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteKeyPairs(self, request):
        """本接口 (DeleteKeyPairs) 用于删除已在Tce托管的密钥对。

        * 可以同时删除多个密钥对。
        * 不能删除已被实例或镜像引用的密钥对，所以需要独立判断是否所有密钥对都被成功删除。

        :param request: 调用DeleteKeyPairs所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DeleteKeyPairsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DeleteKeyPairsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteKeyPairs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteKeyPairsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeAccountAttributes(self, request):
        """无

        :param request: 调用DescribeAccountAttributes所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeAccountAttributesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeAccountAttributesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeAccountAttributes", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAccountAttributesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeAddressBandwidthConfigs(self, request):
        """无

        :param request: 调用DescribeAddressBandwidthConfigs所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeAddressBandwidthConfigsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeAddressBandwidthConfigsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeAddressBandwidthConfigs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAddressBandwidthConfigsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeAddressQuota(self, request):
        """本接口 (DescribeAddressQuota) 用于查询您账户的弹性公网IP（简称 EIP）在当前地域的配额信息。配额详情可参见 EIP 产品简介。

        :param request: 调用DescribeAddressQuota所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeAddressQuotaRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeAddressQuotaResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeAddressQuota", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAddressQuotaResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeAddresses(self, request):
        """本接口 (DescribeAddresses) 用于查询一个或多个弹性公网IP（简称 EIP）的详细信息。
        * 如果参数为空，返回当前用户一定数量（Limit所指定的数量，默认为20）的 EIP。

        :param request: 调用DescribeAddresses所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeAddressesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeAddressesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeAddresses", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAddressesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDisasterRecoverGroupQuota(self, request):
        """查询置放群组配额

        :param request: 调用DescribeDisasterRecoverGroupQuota所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeDisasterRecoverGroupQuotaRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeDisasterRecoverGroupQuotaResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDisasterRecoverGroupQuota", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDisasterRecoverGroupQuotaResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDisasterRecoverGroups(self, request):
        """查询容灾组信息

        :param request: 调用DescribeDisasterRecoverGroups所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeDisasterRecoverGroupsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeDisasterRecoverGroupsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDisasterRecoverGroups", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDisasterRecoverGroupsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeHosts(self, request):
        """本接口 (DescribeHosts) 用于获取一个或多个CDH实例的详细信息。

        :param request: 调用DescribeHosts所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeHostsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeHostsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeHosts", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeHostsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeImageQuota(self, request):
        """本接口(DescribeImageQuota)用于查询用户帐号的镜像配额。

        :param request: 调用DescribeImageQuota所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeImageQuotaRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeImageQuotaResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeImageQuota", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeImageQuotaResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeImageSharePermission(self, request):
        """本接口（ModifyImageSharePermission）用于修改镜像分享信息。

        :param request: 调用DescribeImageSharePermission所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeImageSharePermissionRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeImageSharePermissionResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeImageSharePermission", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeImageSharePermissionResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeImageSnapshotStatus(self, request):
        """本接口(DescribeImageSnapShotStatus)用于查询镜像是否存在快照

        :param request: 调用DescribeImageSnapshotStatus所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeImageSnapshotStatusRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeImageSnapshotStatusResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeImageSnapshotStatus", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeImageSnapshotStatusResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        """本接口(DescribeImages) 用于查看镜像列表。

        * 可以通过指定镜像ID来查询指定镜像的详细信息，或通过设定过滤器来查询满足过滤条件的镜像的详细信息。
        * 指定偏移(Offset)和限制(Limit)来选择结果中的一部分，默认返回满足条件的前20个镜像信息。

        :param request: 调用DescribeImages所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeImagesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeImagesResponse`

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

    def DescribeImagesAttribute(self, request):
        """根据unImgId查询DeviceImageId

        :param request: 调用DescribeImagesAttribute所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeImagesAttributeRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeImagesAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeImagesAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeImagesAttributeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeImportImageOs(self, request):
        """查看可以导入的镜像操作系统信息。

        :param request: 调用DescribeImportImageOs所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeImportImageOsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeImportImageOsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeImportImageOs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeImportImageOsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeImportSnapshotTask(self, request):
        """无

        :param request: 调用DescribeImportSnapshotTask所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeImportSnapshotTaskRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeImportSnapshotTaskResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeImportSnapshotTask", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeImportSnapshotTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeInstanceAttachedDevices(self, request):
        """None

        :param request: 调用DescribeInstanceAttachedDevices所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeInstanceAttachedDevicesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeInstanceAttachedDevicesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstanceAttachedDevices", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstanceAttachedDevicesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeInstanceChargeTypeConfigs(self, request):
        """本接口(DescribeInstanceChargeTypeConfigs) 查询 CVM 实例可支持的各种计费模式。

        :param request: 调用DescribeInstanceChargeTypeConfigs所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeInstanceChargeTypeConfigsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeInstanceChargeTypeConfigsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstanceChargeTypeConfigs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstanceChargeTypeConfigsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeInstanceConfigInfos(self, request):
        """本接口(DescribeInstanceConfigInfos) 获取实例静态配置信息，包含CPU核数、CPU型号、内存大小和带宽信息等。

        :param request: 调用DescribeInstanceConfigInfos所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeInstanceConfigInfosRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeInstanceConfigInfosResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstanceConfigInfos", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstanceConfigInfosResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeInstanceFamilyConfigs(self, request):
        """本接口（DescribeInstanceFamilyConfigs）查询当前用户和地域所支持的机型族列表信息。

        :param request: 调用DescribeInstanceFamilyConfigs所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeInstanceFamilyConfigsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeInstanceFamilyConfigsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstanceFamilyConfigs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstanceFamilyConfigsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeInstanceInternetBandwidthConfigs(self, request):
        """本接口 (DescribeInstanceInternetBandwidthConfigs) 用于查询实例带宽配置。

        * 只支持查询`BANDWIDTH_PREPAID`计费模式的带宽配置。
        * 接口返回实例的所有带宽配置信息（包含历史的带宽配置信息）。

        :param request: 调用DescribeInstanceInternetBandwidthConfigs所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeInstanceInternetBandwidthConfigsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeInstanceInternetBandwidthConfigsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstanceInternetBandwidthConfigs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstanceInternetBandwidthConfigsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeInstanceOperationLogs(self, request):
        """本接口（DescribeInstanceOperationLogs）查询指定实例操作记录。

        :param request: 调用DescribeInstanceOperationLogs所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeInstanceOperationLogsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeInstanceOperationLogsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstanceOperationLogs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstanceOperationLogsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeInstanceStatistics(self, request):
        """本接口 (DescribeInstanceStatistics) 用于查询各个地域资源概览。

        :param request: 调用DescribeInstanceStatistics所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeInstanceStatisticsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeInstanceStatisticsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstanceStatistics", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstanceStatisticsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeInstanceTypeConfigs(self, request):
        """本接口 (DescribeInstanceTypeConfigs) 用于查询实例机型配置。

        * 可以根据`zone`、`instance-family`来查询实例机型配置。过滤条件详见过滤器`Filter`。
        * 如果参数为空，返回指定地域的所有实例机型配置。

        :param request: 调用DescribeInstanceTypeConfigs所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeInstanceTypeConfigsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeInstanceTypeConfigsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstanceTypeConfigs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstanceTypeConfigsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeInstanceTypeNameConfigs(self, request):
        """本接口 (DescribeInstanceTypeNameConfigs) 用于查询实例类型的名称。

        :param request: 调用DescribeInstanceTypeNameConfigs所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeInstanceTypeNameConfigsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeInstanceTypeNameConfigsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstanceTypeNameConfigs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstanceTypeNameConfigsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeInstanceTypeQuota(self, request):
        """本接口 (DescribeInstanceTypeQuota) 用于查询实例的机型配额。

        :param request: 调用DescribeInstanceTypeQuota所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeInstanceTypeQuotaRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeInstanceTypeQuotaResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstanceTypeQuota", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstanceTypeQuotaResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeInstanceVncUrl(self, request):
        """用于查询实例 VNC 地址

        :param request: 调用DescribeInstanceVncUrl所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeInstanceVncUrlRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeInstanceVncUrlResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstanceVncUrl", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstanceVncUrlResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeInstancesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeInstancesResponse`

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

    def DescribeInstancesActionTimer(self, request):
        """查询定时任务信息

        :param request: 调用DescribeInstancesActionTimer所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeInstancesActionTimerRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeInstancesActionTimerResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstancesActionTimer", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstancesActionTimerResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeInstancesAttribute(self, request):
        """用于获取实例订单Id。

        :param request: 调用DescribeInstancesAttribute所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeInstancesAttributeRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeInstancesAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstancesAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstancesAttributeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeInstancesCreateImageAttributes(self, request):
        """查询是否支持在线制作整机镜像的属性接口

        :param request: 调用DescribeInstancesCreateImageAttributes所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeInstancesCreateImageAttributesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeInstancesCreateImageAttributesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstancesCreateImageAttributes", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstancesCreateImageAttributesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeInstancesOperationLimit(self, request):
        """无

        :param request: 调用DescribeInstancesOperationLimit所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeInstancesOperationLimitRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeInstancesOperationLimitResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstancesOperationLimit", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstancesOperationLimitResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeInstancesRecentFailedOperation(self, request):
        """本接口(DescribeInstancesRecentFailedOperation) 获取实例最近失败操作记录。

        :param request: 调用DescribeInstancesRecentFailedOperation所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeInstancesRecentFailedOperationRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeInstancesRecentFailedOperationResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstancesRecentFailedOperation", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstancesRecentFailedOperationResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeInstancesReturnable(self, request):
        """本接口 (DescribeInstancesReturnable) 用于检查子机是否可退还。

        :param request: 调用DescribeInstancesReturnable所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeInstancesReturnableRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeInstancesReturnableResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstancesReturnable", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstancesReturnableResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeInstancesStatus(self, request):
        """本接口 (DescribeInstancesStatus) 用于查询一个或多个实例的状态。

        * 可以根据实例`ID`来查询实例的状态。
        * 如果参数为空，返回当前用户一定数量（Limit所指定的数量，默认为20）的实例状态。

        :param request: 调用DescribeInstancesStatus所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeInstancesStatusRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeInstancesStatusResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstancesStatus", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstancesStatusResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeInternetChargeTypeConfigs(self, request):
        """查询网络计费的类型

        :param request: 调用DescribeInternetChargeTypeConfigs所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeInternetChargeTypeConfigsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeInternetChargeTypeConfigsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInternetChargeTypeConfigs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInternetChargeTypeConfigsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeKeyPairs(self, request):
        """本接口 (DescribeKeyPairs) 用于查询密钥对信息。

        * 密钥对是通过一种算法生成的一对密钥，在生成的密钥对中，一个向外界公开，称为公钥；另一个用户自己保留，称为私钥。密钥对的公钥内容可以通过这个接口查询，但私钥内容系统不保留。

        :param request: 调用DescribeKeyPairs所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeKeyPairsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeKeyPairsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeKeyPairs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeKeyPairsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeKeyPairsAttribute(self, request):
        """内部接口，查询密钥ID对应的内部密钥ID。

        :param request: 调用DescribeKeyPairsAttribute所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeKeyPairsAttributeRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeKeyPairsAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeKeyPairsAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeKeyPairsAttributeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeMarketImages(self, request):
        """用于查询市场镜像。暂不暴露给用户

        :param request: 调用DescribeMarketImages所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeMarketImagesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeMarketImagesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeMarketImages", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeMarketImagesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeMigrateTaskStatus(self, request):
        """根据服务迁移(离线实例迁移，离线数据迁移)接口返回的JobId查询任务状态及进度。

        :param request: 调用DescribeMigrateTaskStatus所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeMigrateTaskStatusRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeMigrateTaskStatusResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeMigrateTaskStatus", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeMigrateTaskStatusResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeNetworkSharingGroups(self, request):
        """None

        :param request: 调用DescribeNetworkSharingGroups所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeNetworkSharingGroupsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeNetworkSharingGroupsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeNetworkSharingGroups", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeNetworkSharingGroupsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeRecomendedZones(self, request):
        """查询可用区规格配额排序列表

        :param request: 调用DescribeRecomendedZones所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeRecomendedZonesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeRecomendedZonesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRecomendedZones", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRecomendedZonesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeRecommendedZones(self, request):
        """查询可用区规格配额排序列表

        :param request: 调用DescribeRecommendedZones所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeRecommendedZonesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeRecommendedZonesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRecommendedZones", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRecommendedZonesResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        """本接口(DescribeRegions)用于查询地域信息。

        :param request: 调用DescribeRegions所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeRegionsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeRegionsResponse`

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

    def DescribeResourcesOverview(self, request):
        """查询概览页详情

        :param request: 调用DescribeResourcesOverview所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeResourcesOverviewRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeResourcesOverviewResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeResourcesOverview", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeResourcesOverviewResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeTask(self, request):
        """获取任务信息, des或者allinone的taskid的信息

        :param request: 调用DescribeTask所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeTaskRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeTaskResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeTask", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeUserAvailableZones(self, request):
        """无

        :param request: 调用DescribeUserAvailableZones所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeUserAvailableZonesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeUserAvailableZonesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeUserAvailableZones", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeUserAvailableZonesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeUserGlobalConfigs(self, request):
        """查询用户全局配置

        :param request: 调用DescribeUserGlobalConfigs所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeUserGlobalConfigsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeUserGlobalConfigsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeUserGlobalConfigs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeUserGlobalConfigsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeUserInstanceQuota(self, request):
        """用于查询用户可用区下配额。

        :param request: 调用DescribeUserInstanceQuota所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeUserInstanceQuotaRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeUserInstanceQuotaResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeUserInstanceQuota", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeUserInstanceQuotaResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeUserMigrateTasks(self, request):
        """本接口（DescribeUserMigrateTasks）用于查询用户的服务迁移任务记录。

        :param request: 调用DescribeUserMigrateTasks所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeUserMigrateTasksRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeUserMigrateTasksResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeUserMigrateTasks", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeUserMigrateTasksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeUserZoneStatus(self, request):
        """本接口(DescribeUserZoneStatus) 查询可用区实例计费类型状态。

        :param request: 调用DescribeUserZoneStatus所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeUserZoneStatusRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeUserZoneStatusResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeUserZoneStatus", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeUserZoneStatusResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeZoneCdhInstanceConfigInfos(self, request):
        """获取专用宿主机的机型配置信息,以及售罄状态信息列表。

        :param request: 调用DescribeZoneCdhInstanceConfigInfos所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeZoneCdhInstanceConfigInfosRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeZoneCdhInstanceConfigInfosResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeZoneCdhInstanceConfigInfos", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeZoneCdhInstanceConfigInfosResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeZoneCpuQuota(self, request):
        """本接口(DescribeZoneCpuQuota）用于查询可用区的CPU配额信息。

        :param request: 调用DescribeZoneCpuQuota所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeZoneCpuQuotaRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeZoneCpuQuotaResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeZoneCpuQuota", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeZoneCpuQuotaResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeZoneHostConfigInfos(self, request):
        """获取专用宿主机的机型配置信息,以及售罄状态信息列表。

        :param request: 调用DescribeZoneHostConfigInfos所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeZoneHostConfigInfosRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeZoneHostConfigInfosResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeZoneHostConfigInfos", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeZoneHostConfigInfosResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeZoneHostForSellStatus(self, request):
        """获取专用宿主机的大区售罄情况

        :param request: 调用DescribeZoneHostForSellStatus所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeZoneHostForSellStatusRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeZoneHostForSellStatusResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeZoneHostForSellStatus", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeZoneHostForSellStatusResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeZoneInstanceConfigInfos(self, request):
        """本接口(DescribeZoneInstanceConfigInfos) 获取可用区的机型信息。

        :param request: 调用DescribeZoneInstanceConfigInfos所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeZoneInstanceConfigInfosRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeZoneInstanceConfigInfosResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeZoneInstanceConfigInfos", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeZoneInstanceConfigInfosResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeZones(self, request):
        """本接口(DescribeZones)用于查询可用区信息。

        :param request: 调用DescribeZones所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DescribeZonesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DescribeZonesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeZones", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeZonesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DisassociateAddress(self, request):
        """本接口 (DisassociateAddress) 用于解绑弹性公网IP（简称 EIP）。
        * 只有状态为 BIND 和 BIND_ENI 的 EIP 才能进行解绑定操作。
        * EIP 如果被封堵，则不能进行解绑定操作。

        :param request: 调用DisassociateAddress所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DisassociateAddressRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DisassociateAddressResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DisassociateAddress", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DisassociateAddressResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DisassociateInstancesKeyPairs(self, request):
        """本接口 (DisassociateInstancesKeyPairs) 用于解除实例的密钥绑定关系。

        * 只支持`STOPPED`状态的`Linux`操作系统的实例。
        * 解绑密钥后，实例可以通过原来设置的密码登录。
        * 如果原来没有设置密码，解绑后将无法使用 `SSH` 登录。可以调用 ResetInstancesPassword 接口来设置登陆密码。
        * 支持批量操作。每次请求批量实例的上限为100。如果批量实例存在不允许操作的实例，操作会以特定错误码返回。

        :param request: 调用DisassociateInstancesKeyPairs所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DisassociateInstancesKeyPairsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DisassociateInstancesKeyPairsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DisassociateInstancesKeyPairs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DisassociateInstancesKeyPairsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DisassociateSecurityGroups(self, request):
        """本接口 (DisassociateSecurityGroups) 用于解绑实例的指定安全组。

        :param request: 调用DisassociateSecurityGroups所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.DisassociateSecurityGroupsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.DisassociateSecurityGroupsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DisassociateSecurityGroups", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DisassociateSecurityGroupsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ExitLiveMigrateInstance(self, request):
        """退出在线服务迁移。用于使实例退出在线服务迁移模式，一般使用在在线服务迁移成功或者失败后。该接口不可直接被用户调用。

        :param request: 调用ExitLiveMigrateInstance所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ExitLiveMigrateInstanceRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ExitLiveMigrateInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ExitLiveMigrateInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ExitLiveMigrateInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ExportImage(self, request):
        """提供一个COS Bucket，并授权，我们将会导出这个镜像到指定的 Bucket 中。

        :param request: 调用ExportImage所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ExportImageRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ExportImageResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ExportImage", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ExportImageResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def FailoverMigrate(self, request):
        """故障迁移

        :param request: 调用FailoverMigrate所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.FailoverMigrateRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.FailoverMigrateResponse`

        """
        try:
            params = request._serialize()
            body = self.call("FailoverMigrate", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.FailoverMigrateResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ImportCbs(self, request):
        """本接口(ImportCbs)用于导入数据盘至一块云盘(CBS)中。

        * 用户需要确认需要导入的数据盘大小小于云盘的容量。
        * 用户需要传入未挂载的云盘作为参数以进行导入。
        * 导入过程中请不要操作云盘。

        :param request: 调用ImportCbs所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ImportCbsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ImportCbsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ImportCbs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ImportCbsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ImportFullCvmImage(self, request):
        """可以同时导入系统盘镜像和数据盘，并制作整机镜像。

        :param request: 调用ImportFullCvmImage所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ImportFullCvmImageRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ImportFullCvmImageResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ImportFullCvmImage", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ImportFullCvmImageResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ImportImage(self, request):
        """本接口(ImportImage)用于导入镜像，导入后的镜像可用于创建实例。

        :param request: 调用ImportImage所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ImportImageRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ImportImageResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ImportImage", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ImportImageResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ImportInstancesActionTimer(self, request):
        """导入定时任务

        :param request: 调用ImportInstancesActionTimer所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ImportInstancesActionTimerRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ImportInstancesActionTimerResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ImportInstancesActionTimer", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ImportInstancesActionTimerResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ImportKeyPair(self, request):
        """本接口 (ImportKeyPair) 用于导入密钥对。

        * 本接口的功能是将密钥对导入到用户账户，并不会自动绑定到实例。如需绑定可以使用AssociasteInstancesKeyPair接口。
        * 需指定密钥对名称以及该密钥对的公钥文本。
        * 如果用户只有私钥，可以通过 `SSL` 工具将私钥转换成公钥后再导入。

        :param request: 调用ImportKeyPair所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ImportKeyPairRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ImportKeyPairResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ImportKeyPair", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ImportKeyPairResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ImportSnapshot(self, request):
        """导入数据盘镜像，并制作为CBS快照。制作的快照可用于创建CBS数据盘。

        :param request: 调用ImportSnapshot所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ImportSnapshotRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ImportSnapshotResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ImportSnapshot", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ImportSnapshotResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceAllocateAddresses(self, request):
        """无

        :param request: 调用InquiryPriceAllocateAddresses所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.InquiryPriceAllocateAddressesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.InquiryPriceAllocateAddressesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceAllocateAddresses", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceAllocateAddressesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceAllocateHosts(self, request):
        """创建CDH实例询价（当HostChargeType为PREPAID时，必须指定HostChargePrepaid参数）

        :param request: 调用InquiryPriceAllocateHosts所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.InquiryPriceAllocateHostsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.InquiryPriceAllocateHostsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceAllocateHosts", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceAllocateHostsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceCreateDisasterRecoverGroup(self, request):
        """无

        :param request: 调用InquiryPriceCreateDisasterRecoverGroup所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.InquiryPriceCreateDisasterRecoverGroupRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.InquiryPriceCreateDisasterRecoverGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceCreateDisasterRecoverGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceCreateDisasterRecoverGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceDeleteDisasterRecoverGroup(self, request):
        """无

        :param request: 调用InquiryPriceDeleteDisasterRecoverGroup所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.InquiryPriceDeleteDisasterRecoverGroupRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.InquiryPriceDeleteDisasterRecoverGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceDeleteDisasterRecoverGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceDeleteDisasterRecoverGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceModifyAddressesBandwidth(self, request):
        """无

        :param request: 调用InquiryPriceModifyAddressesBandwidth所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.InquiryPriceModifyAddressesBandwidthRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.InquiryPriceModifyAddressesBandwidthResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceModifyAddressesBandwidth", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceModifyAddressesBandwidthResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceModifyInstanceInternetChargeType(self, request):
        """本接口 (InquiryPriceModifyInstanceInternetChargeType) 用于切换实例公网网络的计费模式询价。

        * 只支持从 `BANDWIDTH_PREPAID` 计费模式切换为`TRAFFIC_POSTPAID_BY_HOUR`计费模式，或者从 `TRAFFIC_POSTPAID_BY_HOUR` 计费模式切换为`BANDWIDTH_PREPAID`计费模式。

        :param request: 调用InquiryPriceModifyInstanceInternetChargeType所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.InquiryPriceModifyInstanceInternetChargeTypeRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.InquiryPriceModifyInstanceInternetChargeTypeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceModifyInstanceInternetChargeType", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceModifyInstanceInternetChargeTypeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceModifyInstancesChargeType(self, request):
        """本接口 (InquiryPriceModifyInstancesChargeType) 用于切换实例的计费模式询价。

        * 只支持从 `POSTPAID_BY_HOUR` 计费模式切换为`PREPAID`计费模式。
        * 关机不收费的实例、`BC1`和`BS1`机型族的实例、设置定时销毁的实例不支持该操作。

        :param request: 调用InquiryPriceModifyInstancesChargeType所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.InquiryPriceModifyInstancesChargeTypeRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.InquiryPriceModifyInstancesChargeTypeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceModifyInstancesChargeType", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceModifyInstancesChargeTypeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceQueryDisasterRecoverGroup(self, request):
        """无

        :param request: 调用InquiryPriceQueryDisasterRecoverGroup所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.InquiryPriceQueryDisasterRecoverGroupRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.InquiryPriceQueryDisasterRecoverGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceQueryDisasterRecoverGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceQueryDisasterRecoverGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceRenewAddresses(self, request):
        """无

        :param request: 调用InquiryPriceRenewAddresses所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.InquiryPriceRenewAddressesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.InquiryPriceRenewAddressesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceRenewAddresses", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceRenewAddressesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceRenewHosts(self, request):
        """续费CDH实例询价

        :param request: 调用InquiryPriceRenewHosts所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.InquiryPriceRenewHostsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.InquiryPriceRenewHostsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceRenewHosts", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceRenewHostsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceRenewInstances(self, request):
        """本接口 (InquiryPriceRenewInstances) 用于续费包年包月实例询价。

        * 只支持查询包年包月实例的续费价格。

        :param request: 调用InquiryPriceRenewInstances所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.InquiryPriceRenewInstancesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.InquiryPriceRenewInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceRenewInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceRenewInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceResetInstance(self, request):
        """本接口 (InquiryPriceResetInstance) 用于重装实例询价。* 如果指定了`ImageId`参数，则使用指定的镜像进行重装询价；否则按照当前实例使用的镜像进行重装询价。* 目前只支持系统盘类型是`CLOUD_BASIC`、`CLOUD_PREMIUM`、`CLOUD_SSD`类型的实例使用该接口实现`Linux`和`Windows`操作系统切换的重装询价。* 目前不支持海外地域的实例使用该接口实现`Linux`和`Windows`操作系统切换的重装询价。

        :param request: 调用InquiryPriceResetInstance所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.InquiryPriceResetInstanceRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.InquiryPriceResetInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceResetInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceResetInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceResetInstancesInternetMaxBandwidth(self, request):
        """本接口 (InquiryPriceResetInstancesInternetMaxBandwidth) 用于调整实例公网带宽上限询价。

        * 不同机型带宽上限范围不一致，具体限制详见购买网络带宽。
        * 对于`BANDWIDTH_PREPAID`计费方式的带宽，需要输入参数`StartTime`和`EndTime`，指定调整后的带宽的生效时间段。在这种场景下目前不支持调小带宽，会涉及扣费，请确保账户余额充足。可通过`DescribeAccountBalance`接口查询账户余额。
        * 对于 `TRAFFIC_POSTPAID_BY_HOUR`、 `BANDWIDTH_POSTPAID_BY_HOUR` 和 `BANDWIDTH_PACKAGE` 计费方式的带宽，使用该接口调整带宽上限是实时生效的，可以在带宽允许的范围内调大或者调小带宽，不支持输入参数 `StartTime` 和 `EndTime` 。
        * 接口不支持调整`BANDWIDTH_POSTPAID_BY_MONTH`计费方式的带宽。
        * 接口不支持批量调整 `BANDWIDTH_PREPAID` 和 `BANDWIDTH_POSTPAID_BY_HOUR` 计费方式的带宽。
        * 接口不支持批量调整混合计费方式的带宽。例如不支持同时调整`TRAFFIC_POSTPAID_BY_HOUR`和`BANDWIDTH_PACKAGE`计费方式的带宽。

        :param request: 调用InquiryPriceResetInstancesInternetMaxBandwidth所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.InquiryPriceResetInstancesInternetMaxBandwidthRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.InquiryPriceResetInstancesInternetMaxBandwidthResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceResetInstancesInternetMaxBandwidth", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceResetInstancesInternetMaxBandwidthResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceResetInstancesType(self, request):
        """本接口 (InquiryPriceResetInstancesType) 用于调整实例的机型询价。

        * 目前只支持系统盘类型是`CLOUD_BASIC`、`CLOUD_PREMIUM`、`CLOUD_SSD`类型的实例使用该接口进行调整机型询价。
        * 目前不支持CDH实例使用该接口调整机型询价。
        * 目前不支持跨机型系统来调整机型，即使用该接口时指定的`InstanceType`和实例原来的机型需要属于同一系列。
        * 对于包年包月实例，使用该接口会涉及扣费，请确保账户余额充足。可通过`DescribeAccountBalance`接口查询账户余额。

        :param request: 调用InquiryPriceResetInstancesType所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.InquiryPriceResetInstancesTypeRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.InquiryPriceResetInstancesTypeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceResetInstancesType", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceResetInstancesTypeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceResizeInstanceDisks(self, request):
        """本接口 (InquiryPriceResizeInstanceDisks) 用于扩容实例的数据盘询价。

        * 目前只支持扩容随实例购买的数据盘询价，且数据盘类型为：`CLOUD_BASIC`、`CLOUD_PREMIUM`、`CLOUD_SSD`。
        * 目前不支持CDH实例使用该接口扩容数据盘询价。* 仅支持包年包月实例随机器购买的数据盘。* 目前只支持扩容一块数据盘询价。

        :param request: 调用InquiryPriceResizeInstanceDisks所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.InquiryPriceResizeInstanceDisksRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.InquiryPriceResizeInstanceDisksResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceResizeInstanceDisks", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceResizeInstanceDisksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceRunInstances(self, request):
        """本接口(InquiryPriceRunInstances)用于创建实例询价。本接口仅允许针对购买限制范围内的实例配置进行询价, 详见：创建实例。

        :param request: 调用InquiryPriceRunInstances所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.InquiryPriceRunInstancesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.InquiryPriceRunInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceRunInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceRunInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceTerminateInstances(self, request):
        """本接口 (InquiryPriceTerminateInstances) 用于退还实例询价。

        * 查询退还实例可以返还的费用。
        * 支持批量操作，每次请求批量实例的上限为100。如果批量实例存在不允许操作的实例，操作会以特定错误码返回。

        :param request: 调用InquiryPriceTerminateInstances所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.InquiryPriceTerminateInstancesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.InquiryPriceTerminateInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceTerminateInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceTerminateInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceUpdateDisasterRecoverGroup(self, request):
        """无

        :param request: 调用InquiryPriceUpdateDisasterRecoverGroup所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.InquiryPriceUpdateDisasterRecoverGroupRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.InquiryPriceUpdateDisasterRecoverGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceUpdateDisasterRecoverGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceUpdateDisasterRecoverGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def LiveMigrate(self, request):
        """热迁移实例

        :param request: 调用LiveMigrate所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.LiveMigrateRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.LiveMigrateResponse`

        """
        try:
            params = request._serialize()
            body = self.call("LiveMigrate", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.LiveMigrateResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def LiveMigrateInstance(self, request):
        """在线迁移实例。用于将一台运行中的实例导入到Tce。该接口不可由用户直接调用

        :param request: 调用LiveMigrateInstance所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.LiveMigrateInstanceRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.LiveMigrateInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("LiveMigrateInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.LiveMigrateInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyAddressAttribute(self, request):
        """本接口 (ModifyAddressAttribute) 用于修改弹性公网IP（简称 EIP）的名称。

        :param request: 调用ModifyAddressAttribute所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ModifyAddressAttributeRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ModifyAddressAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyAddressAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyAddressAttributeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyAddressesBandwidth(self, request):
        """无

        :param request: 调用ModifyAddressesBandwidth所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ModifyAddressesBandwidthRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ModifyAddressesBandwidthResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyAddressesBandwidth", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyAddressesBandwidthResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyDisasterRecoverGroup(self, request):
        """修改容灾组信息

        :param request: 调用ModifyDisasterRecoverGroup所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ModifyDisasterRecoverGroupRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ModifyDisasterRecoverGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyDisasterRecoverGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyDisasterRecoverGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyDisasterRecoverGroupAttribute(self, request):
        """本接口 (ModifyDisasterRecoverGroupAttribute)用于修改分散置放群组属性。

        :param request: 调用ModifyDisasterRecoverGroupAttribute所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ModifyDisasterRecoverGroupAttributeRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ModifyDisasterRecoverGroupAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyDisasterRecoverGroupAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyDisasterRecoverGroupAttributeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyHostsAttribute(self, request):
        """本接口（ModifyHostsAttribute）用于修改CDH实例的属性，如实例名称和续费标记等。参数HostName和RenewFlag必须设置其中一个，但不能同时设置。

        :param request: 调用ModifyHostsAttribute所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ModifyHostsAttributeRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ModifyHostsAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyHostsAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyHostsAttributeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyImageAttribute(self, request):
        """本接口（ModifyImageAttribute）用于修改镜像属性。

        * 已分享的镜像无法修改属性。

        :param request: 调用ModifyImageAttribute所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ModifyImageAttributeRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ModifyImageAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyImageAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyImageAttributeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyImageSharePermission(self, request):
        """本接口（ModifyImageSharePermission）用于修改镜像分享信息。

        * 分享镜像后，被分享账户可以通过该镜像创建实例。
        * 每个自定义镜像最多可共享给50个账户。
        * 分享镜像无法更改名称，描述，仅可用于创建实例。
        * 只支持分享到对方账户相同地域。

        :param request: 调用ModifyImageSharePermission所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ModifyImageSharePermissionRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ModifyImageSharePermissionResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyImageSharePermission", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyImageSharePermissionResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyInstanceInternetChargeType(self, request):
        """本接口 (ModifyInstanceInternetChargeType) 用于切换实例公网网络的计费模式。

        * 只支持从 `BANDWIDTH_PREPAID` 计费模式切换为`TRAFFIC_POSTPAID_BY_HOUR`计费模式，或者从 `TRAFFIC_POSTPAID_BY_HOUR` 计费模式切换为`BANDWIDTH_PREPAID`计费模式。
        * 切换实例公网网络的计费模式有操作次数限制，可通过 `DescribeInstancesOperationLimit` 接口查询剩余操作次数。

        :param request: 调用ModifyInstanceInternetChargeType所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ModifyInstanceInternetChargeTypeRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ModifyInstanceInternetChargeTypeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyInstanceInternetChargeType", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyInstanceInternetChargeTypeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyInstancesActionTimer(self, request):
        """修改定时任务信息

        :param request: 调用ModifyInstancesActionTimer所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ModifyInstancesActionTimerRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ModifyInstancesActionTimerResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyInstancesActionTimer", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyInstancesActionTimerResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        :type request: :class:`tcecloud.cvm.v20170312.models.ModifyInstancesAttributeRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ModifyInstancesAttributeResponse`

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

    def ModifyInstancesChargeType(self, request):
        """本接口 (ModifyInstancesChargeType) 用于切换实例的计费模式。

        * 只支持从 `POSTPAID_BY_HOUR` 计费模式切换为`PREPAID`计费模式。
        * 关机不收费的实例、`BC1`和`BS1`机型族的实例、设置定时销毁的实例不支持该操作。

        :param request: 调用ModifyInstancesChargeType所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ModifyInstancesChargeTypeRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ModifyInstancesChargeTypeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyInstancesChargeType", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyInstancesChargeTypeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyInstancesProject(self, request):
        """本接口 (ModifyInstancesProject) 用于修改实例所属项目。

        * 项目为一个虚拟概念，用户可以在一个账户下面建立多个项目，每个项目中管理不同的资源；将多个不同实例分属到不同项目中，后续使用 `DescribeInstances`接口查询实例，项目ID可用于过滤结果。
        * 绑定负载均衡的实例不支持修改实例所属项目，请先使用`DeregisterInstancesFromLoadBalancer`接口解绑负载均衡。
        * 修改实例所属项目会自动解关联实例原来关联的安全组，修改完成后可能使用`ModifySecurityGroupsOfInstance`接口关联安全组。
        * 支持批量操作。每次请求批量实例的上限为100。

        :param request: 调用ModifyInstancesProject所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ModifyInstancesProjectRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ModifyInstancesProjectResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyInstancesProject", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyInstancesProjectResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyInstancesRenewFlag(self, request):
        """本接口 (ModifyInstancesRenewFlag) 用于修改包年包月实例续费标识。

        * 实例被标识为自动续费后，每次在实例到期时，会自动续费一个月。
        * 支持批量操作。每次请求批量实例的上限为100。

        :param request: 调用ModifyInstancesRenewFlag所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ModifyInstancesRenewFlagRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ModifyInstancesRenewFlagResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyInstancesRenewFlag", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyInstancesRenewFlagResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyInstancesVpcAttribute(self, request):
        """本接口(ModifyInstancesVpcAttribute)用于修改实例vpc属性，如私有网络ip。
        * 此操作默认会关闭实例，完成后再启动。
        * 当指定私有网络ID和子网ID（子网必须在实例所在的可用区）与指定实例所在私有网络不一致时，会将实例迁移至指定的私有网络的子网下。执行此操作前请确保指定的实例上没有绑定弹性网卡和负载均衡。
        * 实例操作结果可以通过调用 DescribeInstances 接口查询，如果实例的最新操作状态(LatestOperationState)为“SUCCESS”，则代表操作成功。

        :param request: 调用ModifyInstancesVpcAttribute所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ModifyInstancesVpcAttributeRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ModifyInstancesVpcAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyInstancesVpcAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyInstancesVpcAttributeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyKeyPairAttribute(self, request):
        """本接口 (ModifyKeyPairAttribute) 用于修改密钥对属性。

        * 修改密钥对ID所指定的密钥对的名称和描述信息。
        * 密钥对名称不能和已经存在的密钥对的名称重复。
        * 密钥对ID是密钥对的唯一标识，不可修改。

        :param request: 调用ModifyKeyPairAttribute所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ModifyKeyPairAttributeRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ModifyKeyPairAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyKeyPairAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyKeyPairAttributeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyUserGlobalConfigs(self, request):
        """修改用户全局配置

        :param request: 调用ModifyUserGlobalConfigs所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ModifyUserGlobalConfigsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ModifyUserGlobalConfigsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyUserGlobalConfigs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyUserGlobalConfigsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def QueryDisasterRecoverGroup(self, request):
        """无

        :param request: 调用QueryDisasterRecoverGroup所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.QueryDisasterRecoverGroupRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.QueryDisasterRecoverGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("QueryDisasterRecoverGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.QueryDisasterRecoverGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def QueryFlowLogs(self, request):
        """本接口 (QueryFlowLogs) 用于查询 CVM 后端业务模块的日志流水。

        * 支持根据 AppId、Uin、SubAccountUin 查询该用户在指定业务模块下操作记录。
        * 支持根据 RequestId 查询该请求在 CVM_API 这个模块下的操作日志信息。
        * 支持根据 RequestId 查询该请求调用 CVM_DES 这个模块返回的的任务 ID。
        * 如果参数为空，返回当前用户一定数量（Limit所指定的数量，默认为20）的日志信息。

        :param request: 调用QueryFlowLogs所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.QueryFlowLogsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.QueryFlowLogsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("QueryFlowLogs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.QueryFlowLogsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def QueryHosts(self, request):
        """QueryHosts

        :param request: 调用QueryHosts所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.QueryHostsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.QueryHostsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("QueryHosts", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.QueryHostsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def QueryInstances(self, request):
        """QueryInstances

        :param request: 调用QueryInstances所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.QueryInstancesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.QueryInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("QueryInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.QueryInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def QueryInstancesActionTimer(self, request):
        """无

        :param request: 调用QueryInstancesActionTimer所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.QueryInstancesActionTimerRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.QueryInstancesActionTimerResponse`

        """
        try:
            params = request._serialize()
            body = self.call("QueryInstancesActionTimer", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.QueryInstancesActionTimerResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def QueryMigrateTask(self, request):
        """查询迁移任务进度。

        :param request: 调用QueryMigrateTask所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.QueryMigrateTaskRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.QueryMigrateTaskResponse`

        """
        try:
            params = request._serialize()
            body = self.call("QueryMigrateTask", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.QueryMigrateTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        * 支持强制重启。强制重启的效果等同于关闭物理计算机的电源开关再重新启动。强制重启可能会导致数据丢失或文件系统损坏，请仅在服务器不能正常重启时使用。
        * 支持批量操作，每次请求批量实例的上限为100。

        :param request: 调用RebootInstances所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.RebootInstancesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.RebootInstancesResponse`

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

    def RefreshInternalUserEnvironment(self, request):
        """None

        :param request: 调用RefreshInternalUserEnvironment所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.RefreshInternalUserEnvironmentRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.RefreshInternalUserEnvironmentResponse`

        """
        try:
            params = request._serialize()
            body = self.call("RefreshInternalUserEnvironment", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.RefreshInternalUserEnvironmentResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ReleaseAddresses(self, request):
        """本接口 (ReleaseAddresses) 用于释放一个或多个弹性公网IP（简称 EIP）。
        * 该操作不可逆，释放后 EIP 关联的 IP 地址将不再属于您的名下。
        * 只有状态为 UNBIND 的 EIP 才能进行释放操作。

        :param request: 调用ReleaseAddresses所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ReleaseAddressesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ReleaseAddressesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ReleaseAddresses", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ReleaseAddressesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def RenewAddresses(self, request):
        """无

        :param request: 调用RenewAddresses所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.RenewAddressesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.RenewAddressesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("RenewAddresses", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.RenewAddressesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def RenewHosts(self, request):
        """本接口 (RenewHosts) 用于续费包年包月CDH实例。

        * 只支持操作包年包月实例，否则操作会以特定错误码返回。
        * 续费时请确保账户余额充足。可通过`DescribeAccountBalance`接口查询账户余额。

        :param request: 调用RenewHosts所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.RenewHostsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.RenewHostsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("RenewHosts", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.RenewHostsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def RenewInstances(self, request):
        """本接口 (RenewInstances) 用于续费包年包月实例。

        * 只支持操作包年包月实例。
        * 续费时请确保账户余额充足。可通过`DescribeAccountBalance`接口查询账户余额。

        :param request: 调用RenewInstances所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.RenewInstancesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.RenewInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("RenewInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.RenewInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
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

        * 如果指定了`ImageId`参数，则使用指定的镜像重装；否则按照当前实例使用的镜像进行重装。
        * 系统盘将会被格式化，并重置；请确保系统盘中无重要文件。
        * `Linux`和`Windows`系统互相切换时，该实例系统盘`ID`将发生变化，系统盘关联快照将无法回滚、恢复数据。
        * 密码不指定将会通过站内信下发随机密码。
        * 目前只支持系统盘类型是`CLOUD_BASIC`、`CLOUD_PREMIUM`、`CLOUD_SSD`类型的实例使用该接口实现`Linux`和`Windows`操作系统切换。
        * 目前不支持海外地域的实例使用该接口实现`Linux`和`Windows`操作系统切换。

        :param request: 调用ResetInstance所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ResetInstanceRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ResetInstanceResponse`

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

    def ResetInstancesInternetMaxBandwidth(self, request):
        """本接口 (ResetInstancesInternetMaxBandwidth) 用于调整实例公网带宽上限。

        * 不同机型带宽上限范围不一致，具体限制详见购买网络带宽。
        * 对于 `BANDWIDTH_PREPAID` 计费方式的带宽，需要输入参数 `StartTime` 和 `EndTime` ，指定调整后的带宽的生效时间段。在这种场景下目前不支持调小带宽，会涉及扣费，请确保账户余额充足。可通过 `DescribeAccountBalance` 接口查询账户余额。
        * 对于 `TRAFFIC_POSTPAID_BY_HOUR` 、 `BANDWIDTH_POSTPAID_BY_HOUR` 和 `BANDWIDTH_PACKAGE` 计费方式的带宽，使用该接口调整带宽上限是实时生效的，可以在带宽允许的范围内调大或者调小带宽，不支持输入参数 `StartTime` 和 `EndTime` 。
        * 接口不支持调整 `BANDWIDTH_POSTPAID_BY_MONTH` 计费方式的带宽。
        * 接口不支持批量调整 `BANDWIDTH_PREPAID` 和 `BANDWIDTH_POSTPAID_BY_HOUR` 计费方式的带宽。
        * 接口不支持批量调整混合计费方式的带宽。例如不支持同时调整 `TRAFFIC_POSTPAID_BY_HOUR` 和 `BANDWIDTH_PACKAGE` 计费方式的带宽。

        :param request: 调用ResetInstancesInternetMaxBandwidth所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ResetInstancesInternetMaxBandwidthRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ResetInstancesInternetMaxBandwidthResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ResetInstancesInternetMaxBandwidth", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ResetInstancesInternetMaxBandwidthResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ResetInstancesPassword(self, request):
        """本接口 (ResetInstancesPassword) 用于将实例操作系统的密码重置为用户指定的密码。

        * 只修改管理员帐号的密码。实例的操作系统不同，管理员帐号也会不一样(`Windows`为`Administrator`，`Ubuntu`为`ubuntu`，其它系统为`root`)。
        * 重置处于运行中状态的实例，需要显式指定强制关机参数`ForceStop`。如果没有显式指定强制关机参数，则只有处于关机状态的实例才允许执行重置密码操作。
        * 支持批量操作。将多个实例操作系统的密码重置为相同的密码。每次请求批量实例的上限为100。

        :param request: 调用ResetInstancesPassword所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ResetInstancesPasswordRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ResetInstancesPasswordResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ResetInstancesPassword", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ResetInstancesPasswordResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ResetInstancesType(self, request):
        """本接口 (ResetInstancesType) 用于调整实例的机型。
        * 目前只支持系统盘类型是`CLOUD_BASIC`、`CLOUD_PREMIUM`、`CLOUD_SSD`类型的实例使用该接口进行机型调整。
        * 目前不支持CDH实例使用该接口调整机型。* 目前不支持跨机型系统来调整机型，即使用该接口时指定的`InstanceType`和实例原来的机型需要属于同一系列。* 对于包年包月实例，使用该接口会涉及扣费，请确保账户余额充足。可通过`DescribeAccountBalance`接口查询账户余额。

        :param request: 调用ResetInstancesType所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ResetInstancesTypeRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ResetInstancesTypeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ResetInstancesType", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ResetInstancesTypeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ResizeInstanceDisks(self, request):
        """本接口 (ResizeInstanceDisks) 用于扩容实例的数据盘。

        * 目前只支持扩容随实例购买的数据盘，且数据盘类型为：`CLOUD_BASIC`、`CLOUD_PREMIUM`、`CLOUD_SSD`。* 目前不支持CDH实例使用该接口扩容数据盘。
        * 对于包年包月实例，使用该接口会涉及扣费，请确保账户余额充足。可通过`DescribeAccountBalance`接口查询账户余额。
        * 目前只支持扩容一块数据盘。

        :param request: 调用ResizeInstanceDisks所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ResizeInstanceDisksRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ResizeInstanceDisksResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ResizeInstanceDisks", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ResizeInstanceDisksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ResumeInstances(self, request):
        """本接口 (ResumeInstances) 用于恢复一个或多个实例。

        :param request: 调用ResumeInstances所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ResumeInstancesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ResumeInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ResumeInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ResumeInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ReturnAddresses(self, request):
        """无

        :param request: 调用ReturnAddresses所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ReturnAddressesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ReturnAddressesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ReturnAddresses", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ReturnAddressesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ReturnNormalAddresses(self, request):
        """无

        :param request: 调用ReturnNormalAddresses所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.ReturnNormalAddressesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.ReturnNormalAddressesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ReturnNormalAddresses", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ReturnNormalAddressesResponse()
                model._deserialize(response["Response"])
                return model
            else:
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

        * 实例创建成功后将自动开机启动，实例状态变为“运行中”。
        * 预付费实例的购买会预先扣除本次实例购买所需金额，按小时后付费实例购买会预先冻结本次实例购买一小时内所需金额，在调用本接口前请确保账户余额充足。
        * 本接口允许购买的实例数量遵循CVM实例购买限制，所创建的实例和官网入口创建的实例共用配额。
        * 本接口为异步接口，当创建请求下发成功后会返回一个实例`ID`列表，此时实例的创建并立即未完成。在此期间实例的状态将会处于“准备中”，可以通过调用 DescribeInstancesStatus 接口查询对应实例的状态，来判断生产有没有最终成功。如果实例的状态由“准备中”变为“运行中”，则为创建成功。

        :param request: 调用RunInstances所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.RunInstancesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.RunInstancesResponse`

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

    def SearchUserInstance(self, request):
        """无

        :param request: 调用SearchUserInstance所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.SearchUserInstanceRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.SearchUserInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SearchUserInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SearchUserInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        * 支持批量操作。每次请求批量实例的上限为100。

        :param request: 调用StartInstances所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.StartInstancesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.StartInstancesResponse`

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
        * 支持强制关闭。强制关机的效果等同于关闭物理计算机的电源开关。强制关机可能会导致数据丢失或文件系统损坏，请仅在服务器不能正常关机时使用。
        * 支持批量操作。每次请求批量实例的上限为100。

        :param request: 调用StopInstances所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.StopInstancesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.StopInstancesResponse`

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

    def SuspendInstances(self, request):
        """本接口 (SuspendInstances) 用于启动一个或多个实例。

        :param request: 调用SuspendInstances所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.SuspendInstancesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.SuspendInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SuspendInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SuspendInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def SwitchParameterAllocateHosts(self, request):
        """创建CDH实例参数转换（当HostChargeType为PREPAID时，必须指定HostChargePrepaid参数）

        :param request: 调用SwitchParameterAllocateHosts所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.SwitchParameterAllocateHostsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.SwitchParameterAllocateHostsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SwitchParameterAllocateHosts", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SwitchParameterAllocateHostsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def SwitchParameterModifyInstanceInternetChargeType(self, request):
        """本接口 (SwitchParameterModifyInstanceInternetChargeType) 用于切换实例公网网络的计费模式参数转换。

        * 只支持从 `BANDWIDTH_PREPAID` 计费模式切换为`TRAFFIC_POSTPAID_BY_HOUR`计费模式，或者从 `TRAFFIC_POSTPAID_BY_HOUR` 计费模式切换为`BANDWIDTH_PREPAID`计费模式。
        * 切换实例公网网络的计费模式有操作次数限制，可通过 `DescribeInstancesOperationLimit` 接口查询剩余操作次数。

        :param request: 调用SwitchParameterModifyInstanceInternetChargeType所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.SwitchParameterModifyInstanceInternetChargeTypeRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.SwitchParameterModifyInstanceInternetChargeTypeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SwitchParameterModifyInstanceInternetChargeType", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SwitchParameterModifyInstanceInternetChargeTypeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def SwitchParameterModifyInstancesChargeType(self, request):
        """本接口 (SwitchParameterModifyInstancesChargeType) 用于切换实例的计费模式参数转换。

        * 只支持从 `POSTPAID_BY_HOUR` 计费模式切换为`PREPAID`计费模式。
        * 关机不收费的实例、`BC1`和`BS1`机型的实例、设置定时销毁的实例不支持该操作。

        :param request: 调用SwitchParameterModifyInstancesChargeType所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.SwitchParameterModifyInstancesChargeTypeRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.SwitchParameterModifyInstancesChargeTypeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SwitchParameterModifyInstancesChargeType", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SwitchParameterModifyInstancesChargeTypeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def SwitchParameterRenewHosts(self, request):
        """续费CDH实例参数转换

        :param request: 调用SwitchParameterRenewHosts所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.SwitchParameterRenewHostsRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.SwitchParameterRenewHostsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SwitchParameterRenewHosts", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SwitchParameterRenewHostsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def SwitchParameterRenewInstances(self, request):
        """本接口 (SwitchParameterRenewInstances) 用于续费包年包月实例参数转换。

        * 只支持操作包年包月实例。

        :param request: 调用SwitchParameterRenewInstances所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.SwitchParameterRenewInstancesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.SwitchParameterRenewInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SwitchParameterRenewInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SwitchParameterRenewInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def SwitchParameterResetInstance(self, request):
        """本接口 (SwitchParameterResetInstance) 用于重装指定实例上的操作系统参数转换。

        * 如果指定了`ImageId`参数，则使用指定的镜像重装；否则按照当前实例使用的镜像进行重装。
        * 系统盘将会被格式化，并重置；请确保系统盘中无重要文件。
        * `Linux`和`Windows`系统互相切换时，该实例系统盘`ID`将发生变化，系统盘关联快照将无法回滚、恢复数据。
        * 密码不指定将会通过站内信下发随机密码。
        * 目前只支持系统盘类型是`CLOUD_BASIC`、`CLOUD_PREMIUM`、`CLOUD_SSD`类型的实例使用该接口实现`Linux`和`Windows`操作系统切换。
        * 目前不支持海外地域的实例使用该接口实现`Linux`和`Windows`操作系统切换。

        :param request: 调用SwitchParameterResetInstance所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.SwitchParameterResetInstanceRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.SwitchParameterResetInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SwitchParameterResetInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SwitchParameterResetInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def SwitchParameterResetInstancesInternetMaxBandwidth(self, request):
        """本接口 (SwitchParameterResetInstancesInternetMaxBandwidth) 用于调整实例公网带宽上限参数转换。

        * 不同机型带宽上限范围不一致，具体限制详见购买网络带宽。
        * 对于 `BANDWIDTH_PREPAID` 计费方式的带宽，需要输入参数 `StartTime` 和 `EndTime` ，指定调整后的带宽的生效时间段。在这种场景下目前不支持调小带宽，会涉及扣费，请确保账户余额充足。可通过 `DescribeAccountBalance` 接口查询账户余额。
        * 对于 `TRAFFIC_POSTPAID_BY_HOUR` 、 `BANDWIDTH_POSTPAID_BY_HOUR` 和 `BANDWIDTH_PACKAGE` 计费方式的带宽，使用该接口调整带宽上限是实时生效的，可以在带宽允许的范围内调大或者调小带宽，不支持输入参数 `StartTime` 和 `EndTime` 。
        * 接口不支持调整 `BANDWIDTH_POSTPAID_BY_MONTH` 计费方式的带宽。
        * 接口不支持批量调整 `BANDWIDTH_PREPAID` 和 `BANDWIDTH_POSTPAID_BY_HOUR` 计费方式的带宽。
        * 接口不支持批量调整混合计费方式的带宽。例如不支持同时调整 `TRAFFIC_POSTPAID_BY_HOUR` 和 `BANDWIDTH_PACKAGE` 计费方式的带宽。

        :param request: 调用SwitchParameterResetInstancesInternetMaxBandwidth所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.SwitchParameterResetInstancesInternetMaxBandwidthRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.SwitchParameterResetInstancesInternetMaxBandwidthResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SwitchParameterResetInstancesInternetMaxBandwidth", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SwitchParameterResetInstancesInternetMaxBandwidthResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def SwitchParameterResetInstancesType(self, request):
        """本接口 (SwitchParameterResetInstancesType) 用于调整实例的机型参数转换。
        * 目前只支持系统盘类型是`CLOUD_BASIC`、`CLOUD_PREMIUM`、`CLOUD_SSD`类型的实例使用该接口进行机型调整。
        * 目前不支持CDH实例使用该接口调整机型。* 目前不支持跨机型系统来调整机型，即使用该接口时指定的`InstanceType`和实例原来的机型需要属于同一系列。* 对于包年包月实例，使用该接口会涉及扣费，请确保账户余额充足。可通过`DescribeAccountBalance`接口查询账户余额。

        :param request: 调用SwitchParameterResetInstancesType所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.SwitchParameterResetInstancesTypeRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.SwitchParameterResetInstancesTypeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SwitchParameterResetInstancesType", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SwitchParameterResetInstancesTypeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def SwitchParameterResizeInstanceDisks(self, request):
        """本接口 (SwitchParameterResizeInstanceDisks) 用于扩容实例的数据盘参数转换。

        * 目前只支持扩容随实例购买的数据盘，且数据盘类型为：`CLOUD_BASIC`、`CLOUD_PREMIUM`、`CLOUD_SSD`。
        * 目前不支持CDH实例使用该接口扩容数据盘。
        * 对于包年包月实例，使用该接口会涉及扣费，请确保账户余额充足。可通过`DescribeAccountBalance`接口查询账户余额。
        * 目前只支持扩容一块数据盘。

        :param request: 调用SwitchParameterResizeInstanceDisks所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.SwitchParameterResizeInstanceDisksRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.SwitchParameterResizeInstanceDisksResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SwitchParameterResizeInstanceDisks", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SwitchParameterResizeInstanceDisksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def SwitchParameterRunInstances(self, request):
        """本接口 (SwitchParameterRunInstances) 用于创建一个或多个指定配置的实例参数转换。

        * 实例创建成功后将自动开机启动，实例状态变为“运行中”。
        * 预付费实例的购买会预先扣除本次实例购买所需金额，按小时后付费实例购买会预先冻结本次实例购买一小时内所需金额，在调用本接口前请确保账户余额充足。
        * 本接口允许购买的实例数量遵循CVM实例购买限制，所创建的实例和官网入口创建的实例共用配额。
        * 本接口为异步接口，当创建请求下发成功后会返回一个实例`ID`列表，此时实例的创建并立即未完成。在此期间实例的状态将会处于“准备中”，可以通过调用 DescribeInstancesStatus 接口查询对应实例的状态，来判断生产有没有最终成功。如果实例的状态由“准备中”变为“运行中”，则为创建成功。

        :param request: 调用SwitchParameterRunInstances所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.SwitchParameterRunInstancesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.SwitchParameterRunInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SwitchParameterRunInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SwitchParameterRunInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def SyncImages(self, request):
        """本接口（SyncImages）用于将自定义镜像同步到其它地区。

        * 该接口每次调用只支持同步一个镜像。
        * 该接口支持多个同步地域。
        * 单个帐号在每个地域最多支持存在10个自定义镜像。

        :param request: 调用SyncImages所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.SyncImagesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.SyncImagesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SyncImages", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SyncImagesResponse()
                model._deserialize(response["Response"])
                return model
            else:
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
        * 按量计费的实例通过本接口可直接退还；包年包月实例如符合退还规则，也可通过本接口主动退还。
        * 支持批量操作，每次请求批量实例的上限为100。

        :param request: 调用TerminateInstances所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.TerminateInstancesRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.TerminateInstancesResponse`

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

    def TransformAddress(self, request):
        """本接口 (TransformAddress) 用于将实例的普通公网 IP 转换为弹性公网IP（简称 EIP）。
        * 平台对用户每地域每日解绑 EIP 重新分配普通公网 IP 次数有所限制（可参见 EIP 产品简介）。上述配额可通过 DescribeAddressQuota 接口获取。

        :param request: 调用TransformAddress所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.TransformAddressRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.TransformAddressResponse`

        """
        try:
            params = request._serialize()
            body = self.call("TransformAddress", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.TransformAddressResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def UpdateDisasterRecoverGroup(self, request):
        """无

        :param request: 调用UpdateDisasterRecoverGroup所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.UpdateDisasterRecoverGroupRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.UpdateDisasterRecoverGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("UpdateDisasterRecoverGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UpdateDisasterRecoverGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def UpdateInstanceVpcConfig(self, request):
        """本接口(UpdateInstanceVpcConfig)用于修改实例vpc属性，如私有网络ip。
        * 此操作默认会关闭实例，完成后再启动。
        * 不支持跨VpcId操作。

        :param request: 调用UpdateInstanceVpcConfig所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.UpdateInstanceVpcConfigRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.UpdateInstanceVpcConfigResponse`

        """
        try:
            params = request._serialize()
            body = self.call("UpdateInstanceVpcConfig", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UpdateInstanceVpcConfigResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def UpdateInstancesActionTimer(self, request):
        """无

        :param request: 调用UpdateInstancesActionTimer所需参数的结构体。
        :type request: :class:`tcecloud.cvm.v20170312.models.UpdateInstancesActionTimerRequest`
        :rtype: :class:`tcecloud.cvm.v20170312.models.UpdateInstancesActionTimerResponse`

        """
        try:
            params = request._serialize()
            body = self.call("UpdateInstancesActionTimer", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UpdateInstancesActionTimerResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

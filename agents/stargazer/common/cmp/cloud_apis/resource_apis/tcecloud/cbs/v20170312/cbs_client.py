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

from common.cmp.cloud_apis.resource_apis.tcecloud.cbs.v20170312 import models
from common.cmp.cloud_apis.resource_apis.tcecloud.common.abstract_client import AbstractClient
from common.cmp.cloud_apis.resource_apis.tcecloud.common.exception.tce_cloud_sdk_exception import TceCloudSDKException


class CbsClient(AbstractClient):
    _apiVersion = "2017-03-12"
    _endpoint = "cbs.api3.{{conf.main_domain}}"

    def ApplySnapshot(self, request):
        """本接口（ApplySnapshot）用于回滚快照到原云硬盘。

        * 仅支持回滚到原云硬盘上。对于数据盘快照，如果您需要复制快照数据到其它云硬盘上，请使用CreateDisks接口创建新的弹性云盘，将快照数据复制到新购云盘上。
        * 用于回滚的快照必须处于NORMAL状态。快照状态可以通过DescribeSnapshots接口查询，见输出参数中SnapshotState字段解释。
        * 如果是弹性云盘，则云盘必须处于未挂载状态，云硬盘挂载状态可以通过DescribeDisks接口查询，见Attached字段解释；如果是随云主机一起购买的非弹性云盘，则云主机必须处于关机状态，云主机状态可以通过DescribeInstancesStatus接口查询。

        :param request: 调用ApplySnapshot所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.ApplySnapshotRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.ApplySnapshotResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ApplySnapshot", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ApplySnapshotResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def AttachDisks(self, request):
        """本接口（AttachDisks）用于挂载云硬盘。

        * 支持批量操作，将多块云盘挂载到同一云主机。如果多个云盘存在不允许挂载的云盘，则操作不执行，以返回特定的错误码返回。
        * 本接口为异步接口，当挂载云盘的请求成功返回时，表示后台已发起挂载云盘的操作，可通过接口DescribeDisks来查询对应云盘的状态，如果云盘的状态由“ATTACHING”变为“ATTACHED”，则为挂载成功。

        :param request: 调用AttachDisks所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.AttachDisksRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.AttachDisksResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AttachDisks", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AttachDisksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def BindAutoSnapshotPolicy(self, request):
        """本接口（BindAutoSnapshotPolicy）用于绑定云硬盘到指定的定期快照策略。

        * 每个地域最多可创建10个定期快照策略, 每个定期快照策略最多能绑定80个云硬盘。
        * 当已绑定定期快照策略的云硬盘处于未使用状态（即弹性云盘未挂载或非弹性云盘的主机处于关机状态）将不会创建定期快照。

        :param request: 调用BindAutoSnapshotPolicy所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.BindAutoSnapshotPolicyRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.BindAutoSnapshotPolicyResponse`

        """
        try:
            params = request._serialize()
            body = self.call("BindAutoSnapshotPolicy", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.BindAutoSnapshotPolicyResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CopySnapshotCrossRegions(self, request):
        """本接口（CopySnapshotCrossRegion）用于快照跨地域复制。

        * 本接口为异步接口，当跨地域复制的请求下发成功后会返回一个新的快照ID，此时快照未立即复制到目标地域，可请求目标地域的DescribeSnapshots接口新快照的状态，判断是否复制完成。如果快照的状态为“NORMAL”，表示快照复制完成。

        :param request: 调用CopySnapshotCrossRegions所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.CopySnapshotCrossRegionsRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.CopySnapshotCrossRegionsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CopySnapshotCrossRegions", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CopySnapshotCrossRegionsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreateAutoSnapshotPolicy(self, request):
        """本接口（CreateAutoSnapshotPolicy）用于创建定期快照策略。

        * 每个地域最多创建10个定期快照策略。
        * 每个地域可创建的快照有数量和容量的限制，具体请见Tce控制台快照页面提示。

        :param request: 调用CreateAutoSnapshotPolicy所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.CreateAutoSnapshotPolicyRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.CreateAutoSnapshotPolicyResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateAutoSnapshotPolicy", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateAutoSnapshotPolicyResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreateDisks(self, request):
        """本接口（CreateDisks）用于创建云硬盘。

        * 预付费云盘的购买会预先扣除本次云盘购买所需金额，在调用本接口前请确保账户余额充足。
        * 本接口支持传入数据盘快照来创建云盘，实现将快照数据复制到新购云盘上。
        * 本接口为异步接口，当创建请求下发成功后会返回一个新建的云盘ID列表，此时云盘的创建并未立即完成。可以通过调用DescribeDisks接口根据DiskId查询对应云盘，如果能查到云盘，且状态为'UNATTACHED'或'ATTACHED'，则表示创建成功。

        :param request: 调用CreateDisks所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.CreateDisksRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.CreateDisksResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateDisks", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateDisksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def CreateSnapshot(self, request):
        """本接口（CreateSnapshot）用于对指定云盘创建快照。

        * 只有具有快照能力的云硬盘才能创建快照。云硬盘是否具有快照能力可由DescribeDisks接口查询，见SnapshotAbility字段。
        * 可创建快照数量限制见产品使用限制。

        :param request: 调用CreateSnapshot所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.CreateSnapshotRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.CreateSnapshotResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateSnapshot", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateSnapshotResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteAutoSnapshotPolicies(self, request):
        """本接口（DeleteAutoSnapshotPolicies）用于删除定期快照策略。

        *  支持批量操作。如果多个定期快照策略存在无法删除的，则操作不执行，以特定错误码返回。

        :param request: 调用DeleteAutoSnapshotPolicies所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.DeleteAutoSnapshotPoliciesRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.DeleteAutoSnapshotPoliciesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteAutoSnapshotPolicies", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteAutoSnapshotPoliciesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DeleteSnapshots(self, request):
        """本接口（DeleteSnapshots）用于删除快照。

        * 快照必须处于NORMAL状态，快照状态可以通过DescribeSnapshots接口查询，见输出参数中SnapshotState字段解释。
        * 支持批量操作。如果多个快照存在无法删除的快照，则操作不执行，以返回特定的错误码返回。

        :param request: 调用DeleteSnapshots所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.DeleteSnapshotsRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.DeleteSnapshotsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteSnapshots", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteSnapshotsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeAutoSnapshotPolicies(self, request):
        """本接口（DescribeAutoSnapshotPolicies）用于查询定期快照策略。

        * 可以根据定期快照策略ID、名称或者状态等信息来查询定期快照策略的详细信息，不同条件之间为与(AND)的关系，过滤信息详细请见过滤器`Filter`。
        * 如果参数为空，返回当前用户一定数量（`Limit`所指定的数量，默认为20）的定期快照策略表。

        :param request: 调用DescribeAutoSnapshotPolicies所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.DescribeAutoSnapshotPoliciesRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.DescribeAutoSnapshotPoliciesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeAutoSnapshotPolicies", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAutoSnapshotPoliciesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeBlockStorages(self, request):
        """本接口（DescribeBlockStorages）用于查询块存储列表。可以同时查询本地盘和云盘。

        :param request: 调用DescribeBlockStorages所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.DescribeBlockStoragesRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.DescribeBlockStoragesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeBlockStorages", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBlockStoragesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDiskAssociatedAutoSnapshotPolicy(self, request):
        """本接口（DescribeDiskAssociatedAutoSnapshotPolicy）用于查询云盘绑定的定期快照策略。

        :param request: 调用DescribeDiskAssociatedAutoSnapshotPolicy所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.DescribeDiskAssociatedAutoSnapshotPolicyRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.DescribeDiskAssociatedAutoSnapshotPolicyResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDiskAssociatedAutoSnapshotPolicy", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDiskAssociatedAutoSnapshotPolicyResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDiskAssociatedSnapshots(self, request):
        """本接口（DescribeDiskAssociatedSnapshots）用于查询云盘关联的快照。

        :param request: 调用DescribeDiskAssociatedSnapshots所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.DescribeDiskAssociatedSnapshotsRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.DescribeDiskAssociatedSnapshotsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDiskAssociatedSnapshots", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDiskAssociatedSnapshotsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDiskConfigQuota(self, request):
        """本接口（DescribeDiskConfigQuota）用于查询云硬盘配额。

        :param request: 调用DescribeDiskConfigQuota所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.DescribeDiskConfigQuotaRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.DescribeDiskConfigQuotaResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDiskConfigQuota", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDiskConfigQuotaResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDiskStoragePoolGroups(self, request):
        """查询云硬盘存储资源池组信息

        :param request: 调用DescribeDiskStoragePoolGroups所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.DescribeDiskStoragePoolGroupsRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.DescribeDiskStoragePoolGroupsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDiskStoragePoolGroups", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDiskStoragePoolGroupsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDiskSupportFeatures(self, request):
        """查询云硬盘产品支持的特性。

        :param request: 调用DescribeDiskSupportFeatures所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.DescribeDiskSupportFeaturesRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.DescribeDiskSupportFeaturesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeDiskSupportFeatures", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDiskSupportFeaturesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeDisks(self, request):
        """本接口（DescribeDisks）用于查询云硬盘列表。

        * 可以根据云硬盘ID、云硬盘类型或者云硬盘状态等信息来查询云硬盘的详细信息，不同条件之间为与(AND)的关系，过滤信息详细请见过滤器`Filter`。
        * 如果参数为空，返回当前用户一定数量（`Limit`所指定的数量，默认为20）的云硬盘列表。

        :param request: 调用DescribeDisks所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.DescribeDisksRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.DescribeDisksResponse`

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

    def DescribeInstancesDiskNum(self, request):
        """本接口（DescribeInstancesDiskNum）用于查询实例已挂载云硬盘数量。

        * 支持批量操作，当传入多个云服务器实例ID，返回结果会分别列出每个云服务器挂载的云硬盘数量。

        :param request: 调用DescribeInstancesDiskNum所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.DescribeInstancesDiskNumRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.DescribeInstancesDiskNumResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeInstancesDiskNum", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstancesDiskNumResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeSnapshotSharePermission(self, request):
        """本接口（DescribeSnapshotSharePermission）用于查询快照的分享信息。

        :param request: 调用DescribeSnapshotSharePermission所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.DescribeSnapshotSharePermissionRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.DescribeSnapshotSharePermissionResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeSnapshotSharePermission", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeSnapshotSharePermissionResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeSnapshots(self, request):
        """本接口（DescribeSnapshots）用于查询快照的详细信息。

        * 根据快照ID、创建快照的云硬盘ID、创建快照的云硬盘类型等对结果进行过滤，不同条件之间为与(AND)的关系，过滤信息详细请见过滤器`Filter`。
        *  如果参数为空，返回当前用户一定数量（`Limit`所指定的数量，默认为20）的快照列表。

        :param request: 调用DescribeSnapshots所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.DescribeSnapshotsRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.DescribeSnapshotsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeSnapshots", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeSnapshotsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeUserDiskResources(self, request):
        """本接口（DescribeUserTotalResources）用于查询用户在所有地域的云盘数量、快照数量及配额。

        :param request: 调用DescribeUserDiskResources所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.DescribeUserDiskResourcesRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.DescribeUserDiskResourcesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeUserDiskResources", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeUserDiskResourcesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeUserTotalResources(self, request):
        """本接口（DescribeUserTotalResources）用于查询用户在所有地域的云盘数量、快照数量及配额。

        :param request: 调用DescribeUserTotalResources所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.DescribeUserTotalResourcesRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.DescribeUserTotalResourcesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeUserTotalResources", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeUserTotalResourcesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeZoneDiskConfigInfos(self, request):
        """查询对应的云盘资源是否可以创建

        :param request: 调用DescribeZoneDiskConfigInfos所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.DescribeZoneDiskConfigInfosRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.DescribeZoneDiskConfigInfosResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeZoneDiskConfigInfos", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeZoneDiskConfigInfosResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeZoneDiskConfigInfos2(self, request):
        """查询对应的云盘资源是否可以创建

        :param request: 调用DescribeZoneDiskConfigInfos2所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.DescribeZoneDiskConfigInfos2Request`
        :rtype: :class:`tcecloud.cbs.v20170312.models.DescribeZoneDiskConfigInfos2Response`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeZoneDiskConfigInfos2", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeZoneDiskConfigInfos2Response()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DetachDisks(self, request):
        """本接口（DetachDisks）用于解挂云硬盘。

        * 支持批量操作，解挂挂载在同一主机上的多块云盘。如果多块云盘存在不允许解挂载的云盘，则操作不执行，以返回特定的错误码返回。
        * 本接口为异步接口，当请求成功返回时，云盘并未立即从主机解挂载，可通过接口DescribeDisks来查询对应云盘的状态，如果云盘的状态由“ATTACHED”变为“UNATTACHED”，则为解挂载成功。

        :param request: 调用DetachDisks所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.DetachDisksRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.DetachDisksResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DetachDisks", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DetachDisksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def GetSnapOverview(self, request):
        """获取快照概览信息

        :param request: 调用GetSnapOverview所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.GetSnapOverviewRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.GetSnapOverviewResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetSnapOverview", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetSnapOverviewResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceCreateDisks(self, request):
        """本接口（InquiryPriceCreateDisks）用于创建云硬盘询价。

        * 支持查询创建多块云硬盘的价格，此时返回结果为总价格。

        :param request: 调用InquiryPriceCreateDisks所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.InquiryPriceCreateDisksRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.InquiryPriceCreateDisksResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceCreateDisks", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceCreateDisksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceCreateSnapshots(self, request):
        """本接口（InquiryPriceCreateSnapshots）用于创建快照询价。
        * 当前快照不计费，询价价格均为0。

        :param request: 调用InquiryPriceCreateSnapshots所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.InquiryPriceCreateSnapshotsRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.InquiryPriceCreateSnapshotsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceCreateSnapshots", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceCreateSnapshotsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceModifyDiskAttributes(self, request):
        """本接口（InquiryPriceModifyDiskAttributes）用于修改云盘类型询价。

        * 当前仅支持弹性云盘修改类型（DescribeDisks接口的返回字段Portable为true表示弹性云盘）。
        * 当前仅支持云盘类型升级，不支持降级，具体如下:
            * CLOUD_BASIC变更为CLOUD_PREMIUM；
            * CLOUD_BASIC变更为CLOUD_SSD；
            * CLOUD_PREMIUM变更为CLOUD_SSD。

        :param request: 调用InquiryPriceModifyDiskAttributes所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.InquiryPriceModifyDiskAttributesRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.InquiryPriceModifyDiskAttributesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceModifyDiskAttributes", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceModifyDiskAttributesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceRenewDisks(self, request):
        """本接口（InquiryPriceRenewDisks）用于续费云硬盘询价。

        * 只支持查询预付费模式的弹性云盘续费价格。
        * 支持与挂载实例一起续费的场景，需要在DiskChargePrepaid参数中指定CurInstanceDeadline，此时会按对齐到实例续费后的到期时间来续费询价。
        * 支持为多块云盘指定不同的续费时长，此时返回的价格为多块云盘续费的总价格。

        :param request: 调用InquiryPriceRenewDisks所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.InquiryPriceRenewDisksRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.InquiryPriceRenewDisksResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceRenewDisks", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceRenewDisksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def InquiryPriceResizeDisk(self, request):
        """本接口（InquiryPriceResizeDisk）用于扩容云硬盘询价。

        * 只支持预付费模式的云硬盘扩容询价。

        :param request: 调用InquiryPriceResizeDisk所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.InquiryPriceResizeDiskRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.InquiryPriceResizeDiskResponse`

        """
        try:
            params = request._serialize()
            body = self.call("InquiryPriceResizeDisk", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InquiryPriceResizeDiskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyAutoSnapshotPolicyAttribute(self, request):
        """本接口（ModifyAutoSnapshotPolicyAttribute）用于修改定期快照策略属性。

        * 可通过该接口修改定期快照策略的执行策略、名称、是否激活等属性。
        * 修改保留天数时必须保证不与是否永久保留属性冲突，否则整个操作失败，以特定的错误码返回。

        :param request: 调用ModifyAutoSnapshotPolicyAttribute所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.ModifyAutoSnapshotPolicyAttributeRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.ModifyAutoSnapshotPolicyAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyAutoSnapshotPolicyAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyAutoSnapshotPolicyAttributeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyDiskAttributes(self, request):
        """本接口（ModifyDiskAttributes）用于修改云硬盘属性。

        * 只支持修改弹性云盘的项目ID。随云主机创建的云硬盘项目ID与云主机联动。可以通过DescribeDisks接口查询，见输出参数中Portable字段解释。
        * “云硬盘名称”仅为方便用户自己管理之用，Tce并不以此名称作为提交工单或是进行云盘管理操作的依据。
        * 支持批量操作，如果传入多个云盘ID，则所有云盘修改为同一属性。如果存在不允许操作的云盘，则操作不执行，以特定错误码返回。

        :param request: 调用ModifyDiskAttributes所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.ModifyDiskAttributesRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.ModifyDiskAttributesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyDiskAttributes", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyDiskAttributesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifyDisksRenewFlag(self, request):
        """本接口（ModifyDisksRenewFlag）用于修改云硬盘续费标识，支持批量修改。

        :param request: 调用ModifyDisksRenewFlag所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.ModifyDisksRenewFlagRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.ModifyDisksRenewFlagResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyDisksRenewFlag", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyDisksRenewFlagResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifySnapshotAttribute(self, request):
        """本接口（ModifySnapshotAttribute）用于修改指定快照的属性。

        * 当前仅支持修改快照名称及将非永久快照修改为永久快照。
        * “快照名称”仅为方便用户自己管理之用，Tce并不以此名称作为提交工单或是进行快照管理操作的依据。

        :param request: 调用ModifySnapshotAttribute所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.ModifySnapshotAttributeRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.ModifySnapshotAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifySnapshotAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifySnapshotAttributeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ModifySnapshotsSharePermission(self, request):
        """本接口（ModifySnapshotsSharePermission）用于修改快照分享信息。

        分享快照后，被分享账户可以通过该快照创建云硬盘。
        * 每个快照最多可分享给50个账户。
        * 分享快照无法更改名称，描述，仅可用于创建云硬盘。
        * 只支持分享到对方账户相同地域。
        * 仅支持分享数据盘快照。

        :param request: 调用ModifySnapshotsSharePermission所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.ModifySnapshotsSharePermissionRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.ModifySnapshotsSharePermissionResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifySnapshotsSharePermission", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifySnapshotsSharePermissionResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def RenewDisk(self, request):
        """本接口（RenewDisk）用于续费云硬盘。

        * 只支持预付费的云硬盘。云硬盘类型可以通过DescribeDisks接口查询，见输出参数中DiskChargeType字段解释。
        * 支持与挂载实例一起续费的场景，需要在DiskChargePrepaid参数中指定CurInstanceDeadline，此时会按对齐到子机续费后的到期时间来续费。
        * 续费时请确保账户余额充足。可通过DescribeAccountBalance接口查询账户余额。

        :param request: 调用RenewDisk所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.RenewDiskRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.RenewDiskResponse`

        """
        try:
            params = request._serialize()
            body = self.call("RenewDisk", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.RenewDiskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def ResizeDisk(self, request):
        """本接口（ResizeDisk）用于扩容云硬盘。

        * 只支持扩容弹性云盘。云硬盘类型可以通过DescribeDisks接口查询，见输出参数中Portable字段解释。随云主机创建的云硬盘需通过ResizeInstanceDisks接口扩容。
        * 本接口为异步接口，接口成功返回时，云盘并未立即扩容到指定大小，可通过接口DescribeDisks来查询对应云盘的状态，如果云盘的状态为“EXPANDING”，表示正在扩容中，当状态变为“UNATTACHED”，表示扩容完成。

        :param request: 调用ResizeDisk所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.ResizeDiskRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.ResizeDiskResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ResizeDisk", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ResizeDiskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def SwitchParameterCreateDisks(self, request):
        """本接口（SwitchParameterCreateDisks）用于得到创建云硬盘的订单参数。

        :param request: 调用SwitchParameterCreateDisks所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.SwitchParameterCreateDisksRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.SwitchParameterCreateDisksResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SwitchParameterCreateDisks", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SwitchParameterCreateDisksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def SwitchParameterModifyDiskAttributes(self, request):
        """本接口（SwitchParameterModifyDiskAttributes）用于获取修改云盘类型的订单参数。
        * 仅支持预付费弹性云盘；
        * 当前仅支持一次传入一块云盘。

        :param request: 调用SwitchParameterModifyDiskAttributes所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.SwitchParameterModifyDiskAttributesRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.SwitchParameterModifyDiskAttributesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SwitchParameterModifyDiskAttributes", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SwitchParameterModifyDiskAttributesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def SwitchParameterRenewDisks(self, request):
        """本接口（SwitchParameterRenewDisks）用于得到续费云硬盘的订单参数。
        * 支持与挂载云主机一起续费的场景，需要在DiskChargePrepaid参数中指定CurInstanceDeadline，此时会按对齐到子机到期时间来续费。

        :param request: 调用SwitchParameterRenewDisks所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.SwitchParameterRenewDisksRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.SwitchParameterRenewDisksResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SwitchParameterRenewDisks", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SwitchParameterRenewDisksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def SwitchParameterResizeDisk(self, request):
        """本接口（SwitchParameterResizeDisk）用于得到扩容云硬盘的订单参数。

        :param request: 调用SwitchParameterResizeDisk所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.SwitchParameterResizeDiskRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.SwitchParameterResizeDiskResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SwitchParameterResizeDisk", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SwitchParameterResizeDiskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def TerminateDisks(self, request):
        """本接口（TerminateDisks）用于退还云硬盘。

        * 当前仅支持退还包年包月云盘。
        * 支持批量操作，每次请求批量云硬盘的上限为50。如果批量云盘存在不允许操作的，请求会以特定错误码返回。

        :param request: 调用TerminateDisks所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.TerminateDisksRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.TerminateDisksResponse`

        """
        try:
            params = request._serialize()
            body = self.call("TerminateDisks", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.TerminateDisksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def UnbindAutoSnapshotPolicy(self, request):
        """本接口（UnbindAutoSnapshotPolicy）用于解除云硬盘绑定的定期快照策略。

        * 支持批量操作，可一次解除多个云盘与同一定期快照策略的绑定。
        * 如果传入的云盘未绑定到当前定期快照策略，接口将自动跳过，仅解绑与当前定期快照策略绑定的云盘。

        :param request: 调用UnbindAutoSnapshotPolicy所需参数的结构体。
        :type request: :class:`tcecloud.cbs.v20170312.models.UnbindAutoSnapshotPolicyRequest`
        :rtype: :class:`tcecloud.cbs.v20170312.models.UnbindAutoSnapshotPolicyResponse`

        """
        try:
            params = request._serialize()
            body = self.call("UnbindAutoSnapshotPolicy", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UnbindAutoSnapshotPolicyResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

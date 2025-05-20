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


class ApplySnapshotRequest(AbstractModel):
    """ApplySnapshot请求参数结构体"""

    def __init__(self):
        """
        :param SnapshotId: 快照ID, 可通过DescribeSnapshots查询。
        :type SnapshotId: str
        :param DiskId: 快照原云硬盘ID，可通过DescribeDisks接口查询。
        :type DiskId: str
        """
        self.SnapshotId = None
        self.DiskId = None

    def _deserialize(self, params):
        self.SnapshotId = params.get("SnapshotId")
        self.DiskId = params.get("DiskId")


class ApplySnapshotResponse(AbstractModel):
    """ApplySnapshot返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AttachDisksRequest(AbstractModel):
    """AttachDisks请求参数结构体"""

    def __init__(self):
        """
        :param DiskIds: 将要被挂载的弹性云盘ID。通过DescribeDisks接口查询。单次最多可挂载10块弹性云盘。
        :type DiskIds: list of str
        :param InstanceId: 云服务器实例ID。云盘将被挂载到此云服务器上，通过DescribeInstances接口查询。
        :type InstanceId: str
        :param AlignType: 可选参数，不传该参数则仅执行挂载操作。<br>传入该参数，
        会在挂载时将云盘的生命周期与待挂载主机对齐。取值范围：<br><li>AUTO_RENEW：云盘未设置自动续费时，可传该值，
        将云盘设置为自动续费。<br><li> DEADLINE_ALIGN：当云盘的到期时间早于待挂载主机，可传该值，将云盘的到期时间与主机对齐。
        :type AlignType: str
        :param DeleteWithInstance: 可选参数，不传该参数则仅执行挂载操作。传入`True`时，
        会在挂载成功后将云硬盘设置为随云主机销毁模式，仅对按量计费云硬盘有效。
        :type DeleteWithInstance: bool
        :param InstanceIds: 可选参数，用于控制台批量挂载共享盘到多个CVM时指定实例ID。
        如果传入多个InstanceId，那么DisksId中指定的云盘必须全部为共享云盘，否则返回错误。
        :type InstanceIds: list of str
        """
        self.DiskIds = None
        self.InstanceId = None
        self.AlignType = None
        self.DeleteWithInstance = None
        self.InstanceIds = None

    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")
        self.InstanceId = params.get("InstanceId")
        self.AlignType = params.get("AlignType")
        self.DeleteWithInstance = params.get("DeleteWithInstance")
        self.InstanceIds = params.get("InstanceIds")


class AttachDisksResponse(AbstractModel):
    """AttachDisks返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AutoSnapshotPolicy(AbstractModel):
    """描述了定期快照策略的详细信息"""

    def __init__(self):
        """
        :param AutoSnapshotPolicyId: 定期快照策略ID。
        :type AutoSnapshotPolicyId: str
        :param AutoSnapshotPolicyName: 定期快照策略名称。
        :type AutoSnapshotPolicyName: str
        :param AutoSnapshotPolicyState: 定期快照策略的状态。取值范围：<br><li>NORMAL：正常<br><li>ISOLATED：已隔离。
        :type AutoSnapshotPolicyState: str
        :param IsActivated: 定期快照策略是否激活。
        :type IsActivated: bool
        :param IsPermanent: 使用该定期快照策略创建出来的快照是否永久保留。
        :type IsPermanent: bool
        :param RetentionDays: 使用该定期快照策略创建出来的快照保留天数。
        :type RetentionDays: int
        :param CreateTime: 定期快照策略的创建时间。
        :type CreateTime: str
        :param NextTriggerTime: 定期快照下次触发的时间。
        :type NextTriggerTime: str
        :param Policy: 定期快照的执行策略。
        :type Policy: list of Policy
        :param DiskIdSet: 已绑定当前定期快照策略的云盘ID列表。
        :type DiskIdSet: list of str
        """
        self.AutoSnapshotPolicyId = None
        self.AutoSnapshotPolicyName = None
        self.AutoSnapshotPolicyState = None
        self.IsActivated = None
        self.IsPermanent = None
        self.RetentionDays = None
        self.CreateTime = None
        self.NextTriggerTime = None
        self.Policy = None
        self.DiskIdSet = None

    def _deserialize(self, params):
        self.AutoSnapshotPolicyId = params.get("AutoSnapshotPolicyId")
        self.AutoSnapshotPolicyName = params.get("AutoSnapshotPolicyName")
        self.AutoSnapshotPolicyState = params.get("AutoSnapshotPolicyState")
        self.IsActivated = params.get("IsActivated")
        self.IsPermanent = params.get("IsPermanent")
        self.RetentionDays = params.get("RetentionDays")
        self.CreateTime = params.get("CreateTime")
        self.NextTriggerTime = params.get("NextTriggerTime")
        if params.get("Policy") is not None:
            self.Policy = []
            for item in params.get("Policy"):
                obj = Policy()
                obj._deserialize(item)
                self.Policy.append(obj)
        self.DiskIdSet = params.get("DiskIdSet")


class BindAutoSnapshotPolicyRequest(AbstractModel):
    """BindAutoSnapshotPolicy请求参数结构体"""

    def __init__(self):
        """
        :param AutoSnapshotPolicyId: 要绑定的定期快照策略ID。
        :type AutoSnapshotPolicyId: str
        :param DiskIds: 要绑定的云硬盘ID列表，一次请求最多绑定80块云盘。
        :type DiskIds: list of str
        """
        self.AutoSnapshotPolicyId = None
        self.DiskIds = None

    def _deserialize(self, params):
        self.AutoSnapshotPolicyId = params.get("AutoSnapshotPolicyId")
        self.DiskIds = params.get("DiskIds")


class BindAutoSnapshotPolicyResponse(AbstractModel):
    """BindAutoSnapshotPolicy返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class BlockStorage(AbstractModel):
    """描述块存储的详细信息。"""

    def __init__(self):
        """
                :param DiskId: 块存储ID。
                :type DiskId: str
                :param DiskName: 块存储名称。
                :type DiskName: str
                :param DiskSize: 块存储大小，单位GB。
                :type DiskSize: int
                :param DiskType: 块存储介质类型。取值范围：
                <br><li>CLOUD_BASIC<br><li>CLOUD_PREMIUM<br><li>CLOUD_SSD<br><li>
                CLOUD_ENHANCEDSSD<br><li>LOCAL_BASIC<br><li>LOCAL_SSD
                :type DiskType: str
                :param DiskUsage: 块存储类型。取值范围：<br><li>SYSTEM_DISK：系统盘<br><li>DATA_DISK：数据盘。
                :type DiskUsage: str
                :param InstanceId: 块存储挂载的实例ID。
        注意：此字段可能返回 null，表示取不到有效值。
                :type InstanceId: str
                :param InstanceName: 块存储挂载的实例名称。
                :type InstanceName: str
        """
        self.DiskId = None
        self.DiskName = None
        self.DiskSize = None
        self.DiskType = None
        self.DiskUsage = None
        self.InstanceId = None
        self.InstanceName = None

    def _deserialize(self, params):
        self.DiskId = params.get("DiskId")
        self.DiskName = params.get("DiskName")
        self.DiskSize = params.get("DiskSize")
        self.DiskType = params.get("DiskType")
        self.DiskUsage = params.get("DiskUsage")
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")


class CopySnapshotCrossRegionsRequest(AbstractModel):
    """CopySnapshotCrossRegions请求参数结构体"""

    def __init__(self):
        """
        :param DestinationRegions: 快照需要复制到的目标地域，各地域的标准取值可通过接口DescribeRegions查询，且只能传入支持快照的地域。
        :type DestinationRegions: list of str
        :param SnapshotId: 需要跨地域复制的源快照ID，可通过DescribeSnapshots查询。
        :type SnapshotId: str
        :param SnapshotName: 新复制快照的名称，如果不传，则默认取值为“Copied snap-11112222 from 地域名”。
        :type SnapshotName: str
        """
        self.DestinationRegions = None
        self.SnapshotId = None
        self.SnapshotName = None

    def _deserialize(self, params):
        self.DestinationRegions = params.get("DestinationRegions")
        self.SnapshotId = params.get("SnapshotId")
        self.SnapshotName = params.get("SnapshotName")


class CopySnapshotCrossRegionsResponse(AbstractModel):
    """CopySnapshotCrossRegions返回参数结构体"""

    def __init__(self):
        """
        :param SnapshotCopyResultSet: 快照跨地域复制的结果，如果请求下发成功，则返回相应地地域的新快照ID，否则返回Error。
        :type SnapshotCopyResultSet: list of SnapshotCopyResult
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SnapshotCopyResultSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("SnapshotCopyResultSet") is not None:
            self.SnapshotCopyResultSet = []
            for item in params.get("SnapshotCopyResultSet"):
                obj = SnapshotCopyResult()
                obj._deserialize(item)
                self.SnapshotCopyResultSet.append(obj)
        self.RequestId = params.get("RequestId")


class CreateAutoSnapshotPolicyRequest(AbstractModel):
    """CreateAutoSnapshotPolicy请求参数结构体"""

    def __init__(self):
        """
        :param Policy: 定期快照的执行策略。
        :type Policy: list of Policy
        :param AutoSnapshotPolicyName: 要创建的定期快照策略名。不传则默认为“未命名”。最大长度不能超60个字节。
        :type AutoSnapshotPolicyName: str
        :param IsActivated: 是否激活定期快照策略，FALSE表示未激活，TRUE表示激活，默认为TRUE。
        :type IsActivated: bool
        :param IsPermanent: 通过该定期快照策略创建的快照是否永久保留。FALSE表示非永久保留，TRUE表示永久保留，默认为FALSE。
        :type IsPermanent: bool
        :param RetentionDays: 通过该定期快照策略创建的快照保留天数，默认保留7天，该参数不可与`IsPermanent`参数冲突，即若定期快照策略设置为永久保留，本参数应置0。
        :type RetentionDays: int
        :param DryRun: 是否创建定期快照的执行策略。TRUE表示只需获取首次开始备份的时间，不实际创建定期快照策略，FALSE表示创建，默认为FALSE。
        :type DryRun: bool
        """
        self.Policy = None
        self.AutoSnapshotPolicyName = None
        self.IsActivated = None
        self.IsPermanent = None
        self.RetentionDays = None
        self.DryRun = None

    def _deserialize(self, params):
        if params.get("Policy") is not None:
            self.Policy = []
            for item in params.get("Policy"):
                obj = Policy()
                obj._deserialize(item)
                self.Policy.append(obj)
        self.AutoSnapshotPolicyName = params.get("AutoSnapshotPolicyName")
        self.IsActivated = params.get("IsActivated")
        self.IsPermanent = params.get("IsPermanent")
        self.RetentionDays = params.get("RetentionDays")
        self.DryRun = params.get("DryRun")


class CreateAutoSnapshotPolicyResponse(AbstractModel):
    """CreateAutoSnapshotPolicy返回参数结构体"""

    def __init__(self):
        """
        :param AutoSnapshotPolicyId: 新创建的定期快照策略ID。
        :type AutoSnapshotPolicyId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoSnapshotPolicyId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.AutoSnapshotPolicyId = params.get("AutoSnapshotPolicyId")
        self.RequestId = params.get("RequestId")


class CreateDisksRequest(AbstractModel):
    """CreateDisks请求参数结构体"""

    def __init__(self):
        """
        :param DiskType: 硬盘介质类型。取值范围：<br><li>CLOUD_BASIC：表示普通云硬盘<br><li>CLOUD_PREMIUM：表示高性能云硬盘<br><li>CLOUD_SSD：表示SSD云硬盘。
        :type DiskType: str
        :param DiskChargeType: 云硬盘计费类型。<br><li>PREPAID：预付费，即包年包月<br><li>POSTPAID_BY_HOUR：按小时后付费<br>目前只支持后付费模式。
        :type DiskChargeType: str
        :param Placement: 实例所在的位置。通过该参数可以指定实例所属可用区，所属项目。若不指定项目，将在默认项目下进行创建。
        :type Placement: :class:`tcecloud.cbs.v20170312.models.Placement`
        :param DiskName: 云盘显示名称。不传则默认为“未命名”。最大长度不能超60个字节。
        :type DiskName: str
        :param DiskCount: 创建云硬盘数量，不传则默认为1。单次请求最多可创建的云盘数有限制，具体参见云硬盘使用限制。
        :type DiskCount: int
        :param DiskChargePrepaid: 预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月云盘的购买时长、是否设置自动续费等属性，创建预付费云盘该参数必传。
        :type DiskChargePrepaid: :class:`tcecloud.cbs.v20170312.models.DiskChargePrepaid`
        :param DiskSize: 云硬盘大小，单位为GB。<br><li>如果传入`SnapshotId`则可不传`DiskSize`，此时新建云盘的大小为快照大小<br><li>如果传入`SnapshotId`同时传入`DiskSize`，则云盘大小必须大于或等于快照大小<br><li>云盘大小取值范围： 普通云硬盘:10GB ~ 4000G；高性能云硬盘:50GB ~ 4000GB；SSD云硬盘:100GB ~ 4000GB。步长均为10GB
        :type DiskSize: int
        :param SnapshotId: 快照ID，如果传入则根据此快照创建云硬盘，快照类型必须为数据盘快照，可通过DescribeSnapshots接口查询快照，见输出参数DiskUsage解释。
        :type SnapshotId: str
        :param ClientToken: 用于保证请求幂等性的字符串。该字符串由客户生成，需保证不同请求之间唯一，最大值不超过64个ASCII字符。若不指定该参数，则无法保证请求的幂等性。
        :type ClientToken: str
        :param Encrypt: 传入该参数用于创建加密云盘，取值固定为ENCRYPT。
        :type Encrypt: str
        :param Tags: 云盘绑定的标签。
        :type Tags: list of Tag
        :param Shareable: 可选参数，默认为False。传入True时，云盘将创建为共享型云盘。
        :type Shareable: bool
        :param AutoSnapshotPolicyId: 定期快照策略ID。传入该参数时，云硬盘创建成功后将会自动绑定该定期快照策略
        :type AutoSnapshotPolicyId: str
        :param DiskStoragePoolGroup: 存储资源池组
        :type DiskStoragePoolGroup: str
        """
        self.DiskType = None
        self.DiskChargeType = None
        self.Placement = None
        self.DiskName = None
        self.DiskCount = None
        self.DiskChargePrepaid = None
        self.DiskSize = None
        self.SnapshotId = None
        self.ClientToken = None
        self.Encrypt = None
        self.Tags = None
        self.Shareable = None
        self.AutoSnapshotPolicyId = None
        self.DiskStoragePoolGroup = None

    def _deserialize(self, params):
        self.DiskType = params.get("DiskType")
        self.DiskChargeType = params.get("DiskChargeType")
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        self.DiskName = params.get("DiskName")
        self.DiskCount = params.get("DiskCount")
        if params.get("DiskChargePrepaid") is not None:
            self.DiskChargePrepaid = DiskChargePrepaid()
            self.DiskChargePrepaid._deserialize(params.get("DiskChargePrepaid"))
        self.DiskSize = params.get("DiskSize")
        self.SnapshotId = params.get("SnapshotId")
        self.ClientToken = params.get("ClientToken")
        self.Encrypt = params.get("Encrypt")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.Shareable = params.get("Shareable")
        self.AutoSnapshotPolicyId = params.get("AutoSnapshotPolicyId")
        self.DiskStoragePoolGroup = params.get("DiskStoragePoolGroup")


class CreateDisksResponse(AbstractModel):
    """CreateDisks返回参数结构体"""

    def __init__(self):
        """
        :param DiskIdSet: 创建的云硬盘ID列表。
        :type DiskIdSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DiskIdSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.DiskIdSet = params.get("DiskIdSet")
        self.RequestId = params.get("RequestId")


class CreateSnapshotRequest(AbstractModel):
    """CreateSnapshot请求参数结构体"""

    def __init__(self):
        """
        :param DiskId: 需要创建快照的云硬盘ID，可通过DescribeDisks接口查询。
        :type DiskId: str
        :param SnapshotName: 快照名称，不传则新快照名称默认为“未命名”。
        :type SnapshotName: str
        """
        self.DiskId = None
        self.SnapshotName = None

    def _deserialize(self, params):
        self.DiskId = params.get("DiskId")
        self.SnapshotName = params.get("SnapshotName")


class CreateSnapshotResponse(AbstractModel):
    """CreateSnapshot返回参数结构体"""

    def __init__(self):
        """
        :param SnapshotId: 新创建的快照ID。
        :type SnapshotId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SnapshotId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.SnapshotId = params.get("SnapshotId")
        self.RequestId = params.get("RequestId")


class DeleteAutoSnapshotPoliciesRequest(AbstractModel):
    """DeleteAutoSnapshotPolicies请求参数结构体"""

    def __init__(self):
        """
        :param AutoSnapshotPolicyIds: 要删除的定期快照策略ID列表。
        :type AutoSnapshotPolicyIds: list of str
        """
        self.AutoSnapshotPolicyIds = None

    def _deserialize(self, params):
        self.AutoSnapshotPolicyIds = params.get("AutoSnapshotPolicyIds")


class DeleteAutoSnapshotPoliciesResponse(AbstractModel):
    """DeleteAutoSnapshotPolicies返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteSnapshotsRequest(AbstractModel):
    """DeleteSnapshots请求参数结构体"""

    def __init__(self):
        """
        :param SnapshotIds: 要删除的快照ID列表，可通过DescribeSnapshots查询。
        :type SnapshotIds: list of str
        """
        self.SnapshotIds = None

    def _deserialize(self, params):
        self.SnapshotIds = params.get("SnapshotIds")


class DeleteSnapshotsResponse(AbstractModel):
    """DeleteSnapshots返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeAutoSnapshotPoliciesRequest(AbstractModel):
    """DescribeAutoSnapshotPolicies请求参数结构体"""

    def __init__(self):
        """
        :param AutoSnapshotPolicyIds: 要查询的定期快照策略ID列表。参数不支持同时指定`AutoSnapshotPolicyIds`和`Filters`。
        :type AutoSnapshotPolicyIds: list of str
        :param Filters: 过滤条件。参数不支持同时指定`AutoSnapshotPolicyIds`和`Filters`。<br><li>auto-snapshot-policy-id - Array of String - 是否必填：否 -（过滤条件）按定期快照策略ID进行过滤。定期快照策略ID形如：`asp-11112222`。<br><li>auto-snapshot-policy-state - Array of String - 是否必填：否 -（过滤条件）按定期快照策略的状态进行过滤。定期快照策略ID形如：`asp-11112222`。(NORMAL：正常 | ISOLATED：已隔离。)<br><li>auto-snapshot-policy-name - Array of String - 是否必填：否 -（过滤条件）按定期快照策略名称进行过滤。
        :type Filters: list of Filter
        :param Limit: 返回数量，默认为20，最大值为100。关于`Limit`的更进一步介绍请参考 API [简介]中的相关小节。
        :type Limit: int
        :param Offset: 偏移量，默认为0。关于`Offset`的更进一步介绍请参考API[简介]中的相关小节。
        :type Offset: int
        :param Order: 输出定期快照列表的排列顺序。取值范围：<br><li>ASC：升序排列<br><li>DESC：降序排列。
        :type Order: str
        :param OrderField: 定期快照列表排序的依据字段。取值范围：<br><li>CREATETIME：依据定期快照的创建时间排序<br>默认按创建时间排序。
        :type OrderField: str
        """
        self.AutoSnapshotPolicyIds = None
        self.Filters = None
        self.Limit = None
        self.Offset = None
        self.Order = None
        self.OrderField = None

    def _deserialize(self, params):
        self.AutoSnapshotPolicyIds = params.get("AutoSnapshotPolicyIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.Order = params.get("Order")
        self.OrderField = params.get("OrderField")


class DescribeAutoSnapshotPoliciesResponse(AbstractModel):
    """DescribeAutoSnapshotPolicies返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 有效的定期快照策略数量。
        :type TotalCount: int
        :param AutoSnapshotPolicySet: 定期快照策略列表。
        :type AutoSnapshotPolicySet: list of AutoSnapshotPolicy
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.AutoSnapshotPolicySet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("AutoSnapshotPolicySet") is not None:
            self.AutoSnapshotPolicySet = []
            for item in params.get("AutoSnapshotPolicySet"):
                obj = AutoSnapshotPolicy()
                obj._deserialize(item)
                self.AutoSnapshotPolicySet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeBlockStoragesRequest(AbstractModel):
    """DescribeBlockStorages请求参数结构体"""

    def __init__(self):
        """
        :param Limit: 返回数量，默认为100，最大值为1000。关于Limit的更进一步介绍请参考 API 简介中的相关小节。
        :type Limit: int
        :param Offset: 偏移量，默认为0。关于Offset的更进一步介绍请参考 API 简介中的相关小节。
        :type Offset: int
        :param DiskIds: 按照一个或者多个云硬盘ID查询。
        :type DiskIds: list of str
        :param InnerSearch: 内部参数，用于支持搜索框搜索。
        :type InnerSearch: str
        """
        self.Limit = None
        self.Offset = None
        self.DiskIds = None
        self.InnerSearch = None

    def _deserialize(self, params):
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.DiskIds = params.get("DiskIds")
        self.InnerSearch = params.get("InnerSearch")


class DescribeBlockStoragesResponse(AbstractModel):
    """DescribeBlockStorages返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的块存储数量。
        :type TotalCount: int
        :param DiskSet: 块存储详细信息列表。
        :type DiskSet: list of BlockStorage
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.DiskSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("DiskSet") is not None:
            self.DiskSet = []
            for item in params.get("DiskSet"):
                obj = BlockStorage()
                obj._deserialize(item)
                self.DiskSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDiskAssociatedAutoSnapshotPolicyRequest(AbstractModel):
    """DescribeDiskAssociatedAutoSnapshotPolicy请求参数结构体"""

    def __init__(self):
        """
        :param DiskId: 要查询的云硬盘ID。
        :type DiskId: str
        """
        self.DiskId = None

    def _deserialize(self, params):
        self.DiskId = params.get("DiskId")


class DescribeDiskAssociatedAutoSnapshotPolicyResponse(AbstractModel):
    """DescribeDiskAssociatedAutoSnapshotPolicy返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 云盘绑定的定期快照数量。
        :type TotalCount: int
        :param AutoSnapshotPolicySet: 云盘绑定的定期快照列表。
        :type AutoSnapshotPolicySet: list of AutoSnapshotPolicy
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.AutoSnapshotPolicySet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("AutoSnapshotPolicySet") is not None:
            self.AutoSnapshotPolicySet = []
            for item in params.get("AutoSnapshotPolicySet"):
                obj = AutoSnapshotPolicy()
                obj._deserialize(item)
                self.AutoSnapshotPolicySet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDiskAssociatedSnapshotsRequest(AbstractModel):
    """DescribeDiskAssociatedSnapshots请求参数结构体"""

    def __init__(self):
        """
        :param DiskId: 要查询的云硬盘ID。
        :type DiskId: str
        :param Offset: 偏移量，默认为0。关于`Offset`的更进一步介绍请参考API简介中的相关小节。
        :type Offset: int
        :param Limit: 返回数量，默认为20，最大值为100。关于`Limit`的更进一步介绍请参考 API 简介中的相关小节。
        :type Limit: int
        """
        self.DiskId = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.DiskId = params.get("DiskId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeDiskAssociatedSnapshotsResponse(AbstractModel):
    """DescribeDiskAssociatedSnapshots返回参数结构体"""

    def __init__(self):
        """
        :param SnapshotSet: 云盘关联的快照列表
        :type SnapshotSet: list of Snapshot
        :param TotalSnapSize: 云盘关联的快照总大小
        :type TotalSnapSize: int
        :param TotalCount: 云盘关联的快照总数量
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SnapshotSet = None
        self.TotalSnapSize = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("SnapshotSet") is not None:
            self.SnapshotSet = []
            for item in params.get("SnapshotSet"):
                obj = Snapshot()
                obj._deserialize(item)
                self.SnapshotSet.append(obj)
        self.TotalSnapSize = params.get("TotalSnapSize")
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeDiskConfigQuotaRequest(AbstractModel):
    """DescribeDiskConfigQuota请求参数结构体"""

    def __init__(self):
        """
        :param InquiryType: 查询类别，取值范围。<br><li>INQUIRY_CBS_CONFIG：查询云盘配置列表<br><li>INQUIRY_CVM_CONFIG：查询云盘与实例搭配的配置列表。
        :type InquiryType: str
        :param Zones: 查询一个或多个可用区下的配置。
        :type Zones: list of str
        :param DiskChargeType: 付费模式。取值范围：<br><li>PREPAID：预付费<br><li>POSTPAID_BY_HOUR：后付费。
        :type DiskChargeType: str
        :param DiskTypes: 硬盘介质类型。取值范围：<br><li>CLOUD_BASIC：表示普通云硬盘<br><li>CLOUD_PREMIUM：表示高性能云硬盘<br><li>CLOUD_SSD：表示SSD云硬盘。
        :type DiskTypes: list of str
        :param DiskUsage: 系统盘或数据盘。取值范围：<br><li>SYSTEM_DISK：表示系统盘<br><li>DATA_DISK：表示数据盘。
        :type DiskUsage: str
        :param DeviceClasses: 实例机型。
        :type DeviceClasses: list of str
        :param InstanceFamilies: 按照实例机型系列过滤。实例机型系列形如：S1、I1、M1等。详见实例类型
        :type InstanceFamilies: list of str
        :param CPU: 实例CPU核数。
        :type CPU: int
        :param Memory: 实例内存大小。
        :type Memory: int
        :param InnerInquiryType: INQUIRY_RESIZE、INQUIRY_CREATE
        :type InnerInquiryType: str
        """
        self.InquiryType = None
        self.Zones = None
        self.DiskChargeType = None
        self.DiskTypes = None
        self.DiskUsage = None
        self.DeviceClasses = None
        self.InstanceFamilies = None
        self.CPU = None
        self.Memory = None
        self.InnerInquiryType = None

    def _deserialize(self, params):
        self.InquiryType = params.get("InquiryType")
        self.Zones = params.get("Zones")
        self.DiskChargeType = params.get("DiskChargeType")
        self.DiskTypes = params.get("DiskTypes")
        self.DiskUsage = params.get("DiskUsage")
        self.DeviceClasses = params.get("DeviceClasses")
        self.InstanceFamilies = params.get("InstanceFamilies")
        self.CPU = params.get("CPU")
        self.Memory = params.get("Memory")
        self.InnerInquiryType = params.get("InnerInquiryType")


class DescribeDiskConfigQuotaResponse(AbstractModel):
    """DescribeDiskConfigQuota返回参数结构体"""

    def __init__(self):
        """
        :param DiskConfigSet: 云盘配置列表。
        :type DiskConfigSet: list of DiskConfig
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DiskConfigSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("DiskConfigSet") is not None:
            self.DiskConfigSet = []
            for item in params.get("DiskConfigSet"):
                obj = DiskConfig()
                obj._deserialize(item)
                self.DiskConfigSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDiskStoragePoolGroupsRequest(AbstractModel):
    """DescribeDiskStoragePoolGroups请求参数结构体"""

    def __init__(self):
        """
        :param Filters: 过滤
        :type Filters: list of Filters
        :param Limit: 限制单次查询的最大数量
        :type Limit: int
        """
        self.Filters = None
        self.Limit = None

    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filters()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Limit = params.get("Limit")


class DescribeDiskStoragePoolGroupsResponse(AbstractModel):
    """DescribeDiskStoragePoolGroups返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeDiskSupportFeaturesRequest(AbstractModel):
    """DescribeDiskSupportFeatures请求参数结构体"""


class DescribeDiskSupportFeaturesResponse(AbstractModel):
    """DescribeDiskSupportFeatures返回参数结构体"""

    def __init__(self):
        """
        :param DiskFeature: 云硬盘产品特性详情。
        :type DiskFeature: :class:`tcecloud.cbs.v20170312.models.DiskFeature`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DiskFeature = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("DiskFeature") is not None:
            self.DiskFeature = DiskFeature()
            self.DiskFeature._deserialize(params.get("DiskFeature"))
        self.RequestId = params.get("RequestId")


class DescribeDisksRequest(AbstractModel):
    """DescribeDisks请求参数结构体"""

    def __init__(self):
        """
        :param DiskIds: 按照一个或者多个云硬盘ID查询。云硬盘ID形如：`disk-11112222`，此参数的具体格式可参考API简介的ids.N一节）。参数不支持同时指定`DiskIds`和`Filters`。
        :type DiskIds: list of str
        :param Filters: 过滤条件。参数不支持同时指定`DiskIds`和`Filters`。<br><li>disk-usage - Array of String - 是否必填：否 -（过滤条件）按云盘类型过滤。 (SYSTEM_DISK：表示系统盘 | DATA_DISK：表示数据盘)<br><li>disk-charge-type - Array of String - 是否必填：否 -（过滤条件）按照云硬盘计费模式过滤。 (PREPAID：表示预付费，即包年包月 | POSTPAID_BY_HOUR：表示后付费，即按量计费。)<br><li>portable - Array of Bool - 是否必填：否 -（过滤条件）按是否为弹性云盘过滤。 (TRUE：表示弹性云盘 | FALSE：表示非弹性云盘。)<br><li>project-id - Array of Integer - 是否必填：否 -（过滤条件）按云硬盘所属项目ID过滤。<br><li>disk-id - Array of String - 是否必填：否 -（过滤条件）按照云硬盘ID过滤。云盘ID形如：`disk-11112222`。<br><li>disk-name - Array of String - 是否必填：否 -（过滤条件）按照云盘名称过滤。<br><li>disk-type - Array of String - 是否必填：否 -（过滤条件）按照云盘介质类型过滤。(CLOUD_BASIC：表示普通云硬盘 | CLOUD_PREMIUM：表示高性能云硬盘。| CLOUD_SSD：SSD表示SSD云硬盘。)<br><li>disk-state - Array of String - 是否必填：否 -（过滤条件）按照云盘状态过滤。(UNATTACHED：未挂载 | ATTACHING：挂载中 | ATTACHED：已挂载 | DETACHING：解挂中 | EXPANDING：扩容中 | ROLLBACKING：回滚中 | TORECYCLE：待回收。)<br><li>instance-id - Array of String - 是否必填：否 -（过滤条件）按照云盘挂载的云主机实例ID过滤。可根据此参数查询挂载在指定云主机下的云硬盘。<br><li>zone - Array of String - 是否必填：否 -（过滤条件）按照可用区过滤。<br><li>instance-ip-address - Array of String - 是否必填：否 -（过滤条件）按云盘所挂载云主机的内网或外网IP过滤。<br><li>instance-name - Array of String - 是否必填：否 -（过滤条件）按云盘所挂载的实例名称过滤。
        :type Filters: list of Filter
        :param Offset: 偏移量，默认为0。关于`Offset`的更进一步介绍请参考API简介中的相关小节。
        :type Offset: int
        :param Limit: 返回数量，默认为20，最大值为100。关于`Limit`的更进一步介绍请参考 API 简介中的相关小节。
        :type Limit: int
        :param Order: 输出云盘列表的排列顺序。取值范围：<br><li>ASC：升序排列<br><li>DESC：降序排列。
        :type Order: str
        :param OrderField: 云盘列表排序的依据字段。取值范围：<br><li>CREATE_TIME：依据云盘的创建时间排序<br><li>DEADLINE：依据云盘的到期时间排序<br>默认按云盘创建时间排序。
        :type OrderField: str
        :param ReturnBindAutoSnapshotPolicy: 云盘详情中是否需要返回云盘绑定的定期快照策略ID，TRUE表示需要返回，FALSE表示不返回。
        :type ReturnBindAutoSnapshotPolicy: bool
        :param InnerSearch: 内部参数，用于支持搜索框搜索。
        :type InnerSearch: str
        """
        self.DiskIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None
        self.Order = None
        self.OrderField = None
        self.ReturnBindAutoSnapshotPolicy = None
        self.InnerSearch = None

    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.Order = params.get("Order")
        self.OrderField = params.get("OrderField")
        self.ReturnBindAutoSnapshotPolicy = params.get("ReturnBindAutoSnapshotPolicy")
        self.InnerSearch = params.get("InnerSearch")


class DescribeDisksResponse(AbstractModel):
    """DescribeDisks返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的云硬盘数量。
        :type TotalCount: int
        :param DiskSet: 云硬盘的详细信息列表。
        :type DiskSet: list of Disk
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.DiskSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("DiskSet") is not None:
            self.DiskSet = []
            for item in params.get("DiskSet"):
                obj = Disk()
                obj._deserialize(item)
                self.DiskSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInstancesDiskNumRequest(AbstractModel):
    """DescribeInstancesDiskNum请求参数结构体"""

    def __init__(self):
        """
        :param InstanceIds: 云服务器实例ID，通过DescribeInstances接口查询。
        :type InstanceIds: list of str
        """
        self.InstanceIds = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")


class DescribeInstancesDiskNumResponse(AbstractModel):
    """DescribeInstancesDiskNum返回参数结构体"""

    def __init__(self):
        """
        :param AttachedDiskCount: 当前云服务器已挂载弹性云盘数量。
        :type AttachedDiskCount: int
        :param MaxAttachCount: 当前云服务器最大可挂载弹性云盘数量。
        :type MaxAttachCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AttachedDiskCount = None
        self.MaxAttachCount = None
        self.RequestId = None

    def _deserialize(self, params):
        self.AttachedDiskCount = params.get("AttachedDiskCount")
        self.MaxAttachCount = params.get("MaxAttachCount")
        self.RequestId = params.get("RequestId")


class DescribeSnapshotSharePermissionRequest(AbstractModel):
    """DescribeSnapshotSharePermission请求参数结构体"""

    def __init__(self):
        """
        :param SnapshotId: 要查询快照的ID。可通过DescribeSnapshots查询获取。
        :type SnapshotId: str
        """
        self.SnapshotId = None

    def _deserialize(self, params):
        self.SnapshotId = params.get("SnapshotId")


class DescribeSnapshotSharePermissionResponse(AbstractModel):
    """DescribeSnapshotSharePermission返回参数结构体"""

    def __init__(self):
        """
        :param SharePermissionSet: 快照的分享信息的集合
        :type SharePermissionSet: list of SharePermission
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SharePermissionSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("SharePermissionSet") is not None:
            self.SharePermissionSet = []
            for item in params.get("SharePermissionSet"):
                obj = SharePermission()
                obj._deserialize(item)
                self.SharePermissionSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeSnapshotsRequest(AbstractModel):
    """DescribeSnapshots请求参数结构体"""

    def __init__(self):
        """
        :param SnapshotIds: 要查询快照的ID列表。参数不支持同时指定`SnapshotIds`和`Filters`。
        :type SnapshotIds: list of str
        :param Filters: 过滤条件。参数不支持同时指定`SnapshotIds`和`Filters`。<br><li>snapshot-id - Array of String - 是否必填：否 -（过滤条件）按照快照的ID过滤。快照ID形如：`snap-11112222`。<br><li>snapshot-name - Array of String - 是否必填：否 -（过滤条件）按照快照名称过滤。<br><li>snapshot-state - Array of String - 是否必填：否 -（过滤条件）按照快照状态过滤。 (NORMAL：正常 | CREATING：创建中 | ROLLBACKING：回滚中。)<br><li>disk-usage - Array of String - 是否必填：否 -（过滤条件）按创建快照的云盘类型过滤。 (SYSTEM_DISK：代表系统盘 | DATA_DISK：代表数据盘。)<br><li>project-id  - Array of String - 是否必填：否 -（过滤条件）按云硬盘所属项目ID过滤。<br><li>disk-id  - Array of String - 是否必填：否 -（过滤条件）按照创建快照的云硬盘ID过滤。<br><li>zone - Array of String - 是否必填：否 -（过滤条件）按照可用区过滤。
        :type Filters: list of Filter
        :param Offset: 偏移量，默认为0。关于`Offset`的更进一步介绍请参考API简介中的相关小节。
        :type Offset: int
        :param Limit: 返回数量，默认为20，最大值为100。关于`Limit`的更进一步介绍请参考 API 简介中的相关小节。
        :type Limit: int
        :param Order: 输出云盘列表的排列顺序。取值范围：<br><li>ASC：升序排列<br><li>DESC：降序排列。
        :type Order: str
        :param OrderField: 快照列表排序的依据字段。取值范围：<br><li>CREATE_TIME：依据快照的创建时间排序<br>默认按创建时间排序。
        :type OrderField: str
        """
        self.SnapshotIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None
        self.Order = None
        self.OrderField = None

    def _deserialize(self, params):
        self.SnapshotIds = params.get("SnapshotIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.Order = params.get("Order")
        self.OrderField = params.get("OrderField")


class DescribeSnapshotsResponse(AbstractModel):
    """DescribeSnapshots返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 快照的数量。
        :type TotalCount: int
        :param SnapshotSet: 快照的详情列表。
        :type SnapshotSet: list of Snapshot
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.SnapshotSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("SnapshotSet") is not None:
            self.SnapshotSet = []
            for item in params.get("SnapshotSet"):
                obj = Snapshot()
                obj._deserialize(item)
                self.SnapshotSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeUserDiskResourcesRequest(AbstractModel):
    """DescribeUserDiskResources请求参数结构体"""

    def __init__(self):
        """
        :param Regions: 指定要查询的地域，支持同时传入多个地域。不传该参数，则默认查询所有地域。
        :type Regions: list of str
        """
        self.Regions = None

    def _deserialize(self, params):
        self.Regions = params.get("Regions")


class DescribeUserDiskResourcesResponse(AbstractModel):
    """DescribeUserDiskResources返回参数结构体"""

    def __init__(self):
        """
        :param ResourcesDetailSet: 描述第个地域的资源详情。
        :type ResourcesDetailSet: list of ResourcesDetail
        :param DiskOverview: 描述指定地域云硬盘总体使用情况。
        :type DiskOverview: list of DiskOverview
        :param SnapOverview: 描述指定地域快照总体使用情况。
        :type SnapOverview: :class:`tcecloud.cbs.v20170312.models.SnapOverview`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ResourcesDetailSet = None
        self.DiskOverview = None
        self.SnapOverview = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("ResourcesDetailSet") is not None:
            self.ResourcesDetailSet = []
            for item in params.get("ResourcesDetailSet"):
                obj = ResourcesDetail()
                obj._deserialize(item)
                self.ResourcesDetailSet.append(obj)
        if params.get("DiskOverview") is not None:
            self.DiskOverview = []
            for item in params.get("DiskOverview"):
                obj = DiskOverview()
                obj._deserialize(item)
                self.DiskOverview.append(obj)
        if params.get("SnapOverview") is not None:
            self.SnapOverview = SnapOverview()
            self.SnapOverview._deserialize(params.get("SnapOverview"))
        self.RequestId = params.get("RequestId")


class DescribeUserTotalResourcesRequest(AbstractModel):
    """DescribeUserTotalResources请求参数结构体"""

    def __init__(self):
        """
        :param ResourceType: 查询资源的类别。取值范围：<br><li>DISK：查询各地域下的云盘数量<br><li>SNAPSHOT：查询各地域下的快照数量及配额。
        :type ResourceType: str
        :param Regions: 指定要查询的地域，支持同时传入多个地域。不传该参数，则默认查询所有地域。
        :type Regions: list of str
        """
        self.ResourceType = None
        self.Regions = None

    def _deserialize(self, params):
        self.ResourceType = params.get("ResourceType")
        self.Regions = params.get("Regions")


class DescribeUserTotalResourcesResponse(AbstractModel):
    """DescribeUserTotalResources返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeZoneDiskConfigInfos2Request(AbstractModel):
    """DescribeZoneDiskConfigInfos2请求参数结构体"""

    def __init__(self):
        """
        :param DiskChargeType: 付费模式
        :type DiskChargeType: str
        :param Zone: zone
        :type Zone: str
        :param DiskConfigSet: 磁盘配置
        :type DiskConfigSet: list of DiskConfigSet
        """
        self.DiskChargeType = None
        self.Zone = None
        self.DiskConfigSet = None

    def _deserialize(self, params):
        self.DiskChargeType = params.get("DiskChargeType")
        self.Zone = params.get("Zone")
        if params.get("DiskConfigSet") is not None:
            self.DiskConfigSet = []
            for item in params.get("DiskConfigSet"):
                obj = DiskConfigSet()
                obj._deserialize(item)
                self.DiskConfigSet.append(obj)


class DescribeZoneDiskConfigInfos2Response(AbstractModel):
    """DescribeZoneDiskConfigInfos2返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeZoneDiskConfigInfosRequest(AbstractModel):
    """DescribeZoneDiskConfigInfos请求参数结构体"""

    def __init__(self):
        """
        :param DiskChargeType: 付费类型。
        :type DiskChargeType: str
        :param DiskConfigs: 云盘配置列表。
        :type DiskConfigs: list of DiskConfigSet
        :param Zone: 可用区。
        :type Zone: str
        """
        self.DiskChargeType = None
        self.DiskConfigs = None
        self.Zone = None

    def _deserialize(self, params):
        self.DiskChargeType = params.get("DiskChargeType")
        if params.get("DiskConfigs") is not None:
            self.DiskConfigs = []
            for item in params.get("DiskConfigs"):
                obj = DiskConfigSet()
                obj._deserialize(item)
                self.DiskConfigs.append(obj)
        self.Zone = params.get("Zone")


class DescribeZoneDiskConfigInfosResponse(AbstractModel):
    """DescribeZoneDiskConfigInfos返回参数结构体"""

    def __init__(self):
        """
        :param DiskConfigSetQuota: 可创建云盘数量
        :type DiskConfigSetQuota: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DiskConfigSetQuota = None
        self.RequestId = None

    def _deserialize(self, params):
        self.DiskConfigSetQuota = params.get("DiskConfigSetQuota")
        self.RequestId = params.get("RequestId")


class DetachDisksRequest(AbstractModel):
    """DetachDisks请求参数结构体"""

    def __init__(self):
        """
        :param DiskIds: 将要解挂的云硬盘ID， 通过DescribeDisks接口查询，单次请求最多可解挂10块弹性云盘。
        :type DiskIds: list of str
        :param InstanceId: 对于非共享型云盘，会忽略该参数；对于共享型云盘，该参数表示要从哪个CVM实例上解挂云盘。
        :type InstanceId: str
        """
        self.DiskIds = None
        self.InstanceId = None

    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")
        self.InstanceId = params.get("InstanceId")


class DetachDisksResponse(AbstractModel):
    """DetachDisks返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class Disk(AbstractModel):
    """描述了云硬盘的详细信息"""

    def __init__(self):
        """
                :param DiskId: 云硬盘ID。
                :type DiskId: str
                :param DiskUsage: 云硬盘类型。取值范围：<br><li>SYSTEM_DISK：系统盘<br><li>DATA_DISK：数据盘。
                :type DiskUsage: str
                :param DiskChargeType: 付费模式。取值范围：<br><li>PREPAID：预付费，即包年包月<br><li>POSTPAID_BY_HOUR：后付费，即按量计费。
                :type DiskChargeType: str
                :param Portable: 是否为弹性云盘，false表示非弹性云盘，true表示弹性云盘。
                :type Portable: bool
                :param Placement: 云硬盘所在的位置。
                :type Placement: :class:`tcecloud.cbs.v20170312.models.Placement`
                :param SnapshotAbility: 云盘是否具备创建快照的能力。取值范围：<br><li>false表示不具备<br><li>true表示具备。
                :type SnapshotAbility: bool
                :param DiskName: 云硬盘名称。
                :type DiskName: str
                :param DiskSize: 云硬盘大小。
                :type DiskSize: int
                :param DiskState: 云盘状态。取值范围：<br><li>UNATTACHED：未挂载<br><li>ATTACHING：挂载中<br><li>ATTACHED：已挂载<br><li>DETACHING：解挂中<br><li>EXPANDING：扩容中<br><li>ROLLBACKING：回滚中。
                :type DiskState: str
                :param DiskType: 云盘介质类型。取值范围：<br><li>CLOUD_BASIC：表示普通云硬<br><li>CLOUD_PREMIUM：表示高性能云硬盘<br><li>CLOUD_SSD：SSD表示SSD云硬盘。
                :type DiskType: str
                :param Attached: 云盘是否挂载到云主机上。取值范围：<br><li>false:表示未挂载<br><li>true:表示已挂载。
                :type Attached: bool
                :param InstanceId: 云硬盘挂载的云主机ID。
                :type InstanceId: str
                :param CreateTime: 云硬盘的创建时间。
                :type CreateTime: str
                :param DeadlineTime: 云硬盘的到期时间。
                :type DeadlineTime: str
                :param Rollbacking: 云盘是否处于快照回滚状态。取值范围：<br><li>false:表示不处于快照回滚状态<br><li>true:表示处于快照回滚状态。
                :type Rollbacking: bool
                :param RollbackPercent: 云盘快照回滚的进度。
                :type RollbackPercent: int
                :param Encrypt: 云盘是否为加密盘。取值范围：<br><li>false:表示非加密盘<br><li>true:表示加密盘。
                :type Encrypt: bool
                :param AutoRenewFlagError: 云盘已挂载到子机，且子机与云盘都是包年包月。<br><li>true：子机设置了自动续费标识，但云盘未设置<br><li>false：云盘自动续费标识正常。
                :type AutoRenewFlagError: bool
                :param RenewFlag: 自动续费标识。取值范围：<br><li>NOTIFY_AND_AUTO_RENEW：通知过期且自动续费<br><li>NOTIFY_AND_MANUAL_RENEW：通知过期不自动续费<br><li>DISABLE_NOTIFY_AND_MANUAL_RENEW：不通知过期不自动续费。
                :type RenewFlag: str
                :param DeadlineError: 在云盘已挂载到实例，且实例与云盘都是包年包月的条件下，此字段才有意义。<br><li>true:云盘到期时间早于实例。<br><li>false：云盘到期时间晚于实例。
                :type DeadlineError: bool
                :param IsReturnable: 判断预付费的云盘是否支持主动退还。<br><li>true:支持主动退还<br><li>false:不支持主动退还。
                :type IsReturnable: bool
                :param ReturnFailCode: 预付费云盘在不支持主动退还的情况下，该参数表明不支持主动退还的具体原因。取值范围：<br><li>1：云硬盘已经退还<br><li>2：云硬盘已过期<br><li>3：云盘不支持退还<br><li>8：超过可退还数量的限制。
                :type ReturnFailCode: int
                :param AutoSnapshotPolicyIds: 云盘关联的定期快照ID。只有在调用DescribeDisks接口时，入参ReturnBindAutoSnapshotPolicy取值为TRUE才会返回该参数。
                :type AutoSnapshotPolicyIds: list of str
                :param Tags: 与云盘绑定的标签，云盘未绑定标签则取值为空。
        注意：此字段可能返回 null，表示取不到有效值。
                :type Tags: list of Tag
                :param DeleteWithInstance: 云盘是否与挂载的实例一起销毁。<br><li>true:销毁实例时会同时销毁云盘，只支持按小时后付费云盘。<br><li>false：销毁实例时不销毁云盘。
        注意：此字段可能返回 null，表示取不到有效值。
                :type DeleteWithInstance: bool
                :param DifferDaysOfDeadline: 当前时间距离盘到期的天数（仅对预付费盘有意义）。
        注意：此字段可能返回 null，表示取不到有效值。
                :type DifferDaysOfDeadline: int
                :param Migrating: 云盘是否处于类型变更中。取值范围：<br><li>false:表示云盘不处于类型变更中<br><li>true:表示云盘已发起类型变更，正处于迁移中。
        注意：此字段可能返回 null，表示取不到有效值。
                :type Migrating: bool
                :param MigratePercent: 云盘类型变更的迁移进度，取值0到100。
        注意：此字段可能返回 null，表示取不到有效值。
                :type MigratePercent: int
                :param Shareable: 云盘是否为共享型云盘。
        注意：此字段可能返回 null，表示取不到有效值。
                :type Shareable: bool
                :param InstanceIdList: 对于非共享型云盘，该参数为空数组。对于共享型云盘，则表示该云盘当前被挂载到的CVM实例InstanceId
        注意：此字段可能返回 null，表示取不到有效值。
                :type InstanceIdList: list of str
                :param SnapshotCount: 云盘拥有的快照总数。
        注意：此字段可能返回 null，表示取不到有效值。
                :type SnapshotCount: int
                :param SnapshotSize: 云盘拥有的快照总容量，单位为MB。
        注意：此字段可能返回 null，表示取不到有效值。
                :type SnapshotSize: int
        """
        self.DiskId = None
        self.DiskUsage = None
        self.DiskChargeType = None
        self.Portable = None
        self.Placement = None
        self.SnapshotAbility = None
        self.DiskName = None
        self.DiskSize = None
        self.DiskState = None
        self.DiskType = None
        self.Attached = None
        self.InstanceId = None
        self.CreateTime = None
        self.DeadlineTime = None
        self.Rollbacking = None
        self.RollbackPercent = None
        self.Encrypt = None
        self.AutoRenewFlagError = None
        self.RenewFlag = None
        self.DeadlineError = None
        self.IsReturnable = None
        self.ReturnFailCode = None
        self.AutoSnapshotPolicyIds = None
        self.Tags = None
        self.DeleteWithInstance = None
        self.DifferDaysOfDeadline = None
        self.Migrating = None
        self.MigratePercent = None
        self.Shareable = None
        self.InstanceIdList = None
        self.SnapshotCount = None
        self.SnapshotSize = None

    def _deserialize(self, params):
        self.DiskId = params.get("DiskId")
        self.DiskUsage = params.get("DiskUsage")
        self.DiskChargeType = params.get("DiskChargeType")
        self.Portable = params.get("Portable")
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        self.SnapshotAbility = params.get("SnapshotAbility")
        self.DiskName = params.get("DiskName")
        self.DiskSize = params.get("DiskSize")
        self.DiskState = params.get("DiskState")
        self.DiskType = params.get("DiskType")
        self.Attached = params.get("Attached")
        self.InstanceId = params.get("InstanceId")
        self.CreateTime = params.get("CreateTime")
        self.DeadlineTime = params.get("DeadlineTime")
        self.Rollbacking = params.get("Rollbacking")
        self.RollbackPercent = params.get("RollbackPercent")
        self.Encrypt = params.get("Encrypt")
        self.AutoRenewFlagError = params.get("AutoRenewFlagError")
        self.RenewFlag = params.get("RenewFlag")
        self.DeadlineError = params.get("DeadlineError")
        self.IsReturnable = params.get("IsReturnable")
        self.ReturnFailCode = params.get("ReturnFailCode")
        self.AutoSnapshotPolicyIds = params.get("AutoSnapshotPolicyIds")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.DeleteWithInstance = params.get("DeleteWithInstance")
        self.DifferDaysOfDeadline = params.get("DifferDaysOfDeadline")
        self.Migrating = params.get("Migrating")
        self.MigratePercent = params.get("MigratePercent")
        self.Shareable = params.get("Shareable")
        self.InstanceIdList = params.get("InstanceIdList")
        self.SnapshotCount = params.get("SnapshotCount")
        self.SnapshotSize = params.get("SnapshotSize")


class DiskChargePrepaid(AbstractModel):
    """描述了实例的计费模式"""

    def __init__(self):
        """
        :param Period: 购买云盘的时长，默认单位为月，此时，取值范围：1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 24, 36。
        :type Period: int
        :param RenewFlag: 自动续费标识。取值范围：<br><li>NOTIFY_AND_AUTO_RENEW：通知过期且自动续费<br><li>NOTIFY_AND_MANUAL_RENEW：通知过期不自动续费<br><li>DISABLE_NOTIFY_AND_MANUAL_RENEW：不通知过期不自动续费<br><br>默认取值：NOTIFY_AND_MANUAL_RENEW：通知过期不自动续费。
        :type RenewFlag: str
        :param CurInstanceDeadline: 需要将云盘的到期时间与挂载的子机对齐时，可传入该参数。该参数表示子机当前的到期时间，此时Period如果传入，则表示子机需要续费的时长，云盘会自动按对齐到子机续费后的到期时间续费。
        :type CurInstanceDeadline: str
        """
        self.Period = None
        self.RenewFlag = None
        self.CurInstanceDeadline = None

    def _deserialize(self, params):
        self.Period = params.get("Period")
        self.RenewFlag = params.get("RenewFlag")
        self.CurInstanceDeadline = params.get("CurInstanceDeadline")


class DiskConfig(AbstractModel):
    """云盘配置。"""

    def __init__(self):
        """
        :param Available: 配置是否可用。
        :type Available: bool
        :param DiskType: 云盘介质类型。取值范围：<br><li>CLOUD_BASIC：表示普通云硬盘<br><li>CLOUD_PREMIUM：表示高性能云硬盘<br><li>CLOUD_SSD：SSD表示SSD云硬盘。
        :type DiskType: str
        :param DiskUsage: 云盘类型。取值范围：<br><li>SYSTEM_DISK：表示系统盘<br><li>DATA_DISK：表示数据盘。
        :type DiskUsage: str
        :param DiskChargeType: 付费模式。取值范围：<br><li>PREPAID：表示预付费，即包年包月<br><li>POSTPAID_BY_HOUR：表示后付费，即按量计费。
        :type DiskChargeType: str
        :param MaxDiskSize: 最大可配置云盘大小。
        :type MaxDiskSize: int
        :param MinDiskSize: 最小可配置云盘大小。
        :type MinDiskSize: int
        :param Zone: 所在可用区。
        :type Zone: str
        :param DeviceClass: 实例机型。
        :type DeviceClass: str
        :param InstanceFamily: 实例机型系列。详见实例类型
        :type InstanceFamily: str
        """
        self.Available = None
        self.DiskType = None
        self.DiskUsage = None
        self.DiskChargeType = None
        self.MaxDiskSize = None
        self.MinDiskSize = None
        self.Zone = None
        self.DeviceClass = None
        self.InstanceFamily = None

    def _deserialize(self, params):
        self.Available = params.get("Available")
        self.DiskType = params.get("DiskType")
        self.DiskUsage = params.get("DiskUsage")
        self.DiskChargeType = params.get("DiskChargeType")
        self.MaxDiskSize = params.get("MaxDiskSize")
        self.MinDiskSize = params.get("MinDiskSize")
        self.Zone = params.get("Zone")
        self.DeviceClass = params.get("DeviceClass")
        self.InstanceFamily = params.get("InstanceFamily")


class DiskConfigSet(AbstractModel):
    """云盘配置"""

    def __init__(self):
        """
        :param DiskUsage: 系统盘或数据盘
        :type DiskUsage: str
        :param DiskType: CLOUD_BASIC、CLOUD_PREMIUM、CLOUD_SSD
        :type DiskType: str
        :param DiskSize: 云盘大小
        :type DiskSize: int
        :param SnapshotId: 快照ID
        :type SnapshotId: str
        """
        self.DiskUsage = None
        self.DiskType = None
        self.DiskSize = None
        self.SnapshotId = None

    def _deserialize(self, params):
        self.DiskUsage = params.get("DiskUsage")
        self.DiskType = params.get("DiskType")
        self.DiskSize = params.get("DiskSize")
        self.SnapshotId = params.get("SnapshotId")


class DiskFeature(AbstractModel):
    """云硬盘产品支持的特性。"""

    def __init__(self):
        """
                :param TradeType: 云硬盘使用的计费系统。取值范围：<br><li>bmppro：计费系统<br><li>bsp：计量系统
        注意：此字段可能返回 null，表示取不到有效值。
                :type TradeType: str
        """
        self.TradeType = None

    def _deserialize(self, params):
        self.TradeType = params.get("TradeType")


class DiskOrder(AbstractModel):
    """请求计费的订单参数。"""

    def __init__(self):
        """
        :param GoodsCategoryId: 产品类别。
        :type GoodsCategoryId: int
        :param GoodsNum: 产品数量。
        :type GoodsNum: int
        :param ProjectId: 项目ID。
        :type ProjectId: int
        :param GoodsDetail: 产品详情。
        :type GoodsDetail: :class:`tcecloud.cbs.v20170312.models.GoodsDetail`
        :param RegionId: 地域ID。
        :type RegionId: int
        :param ZoneId: 可用区ID。
        :type ZoneId: int
        :param PayMode: 付费模式。
        :type PayMode: int
        :param Type: 云盘类别。
        :type Type: str
        """
        self.GoodsCategoryId = None
        self.GoodsNum = None
        self.ProjectId = None
        self.GoodsDetail = None
        self.RegionId = None
        self.ZoneId = None
        self.PayMode = None
        self.Type = None

    def _deserialize(self, params):
        self.GoodsCategoryId = params.get("GoodsCategoryId")
        self.GoodsNum = params.get("GoodsNum")
        self.ProjectId = params.get("ProjectId")
        if params.get("GoodsDetail") is not None:
            self.GoodsDetail = GoodsDetail()
            self.GoodsDetail._deserialize(params.get("GoodsDetail"))
        self.RegionId = params.get("RegionId")
        self.ZoneId = params.get("ZoneId")
        self.PayMode = params.get("PayMode")
        self.Type = params.get("Type")


class DiskOverview(AbstractModel):
    """用户云硬盘信息概览，包括云硬盘总数，已过期云硬盘数，7天内将到期云硬盘数。"""

    def __init__(self):
        """
        :param DiskNumberTotal: 用户云硬盘总数。
        :type DiskNumberTotal: int
        :param ExpiredNumberTotal: 用户已过期云硬盘总数。
        :type ExpiredNumberTotal: int
        :param DiskNumberExpireIn7days: 用户7天内将到期云硬盘总数
        :type DiskNumberExpireIn7days: int
        """
        self.DiskNumberTotal = None
        self.ExpiredNumberTotal = None
        self.DiskNumberExpireIn7days = None

    def _deserialize(self, params):
        self.DiskNumberTotal = params.get("DiskNumberTotal")
        self.ExpiredNumberTotal = params.get("ExpiredNumberTotal")
        self.DiskNumberExpireIn7days = params.get("DiskNumberExpireIn7days")


class DiskResizeConfig(AbstractModel):
    """云盘扩容配置，用于SwitchParameterResizeDisk接口出参。"""

    def __init__(self):
        """
        :param Pid: 产品ID。
        :type Pid: int
        :param CbsSize: 云盘大小。
        :type CbsSize: int
        :param MediumType: 云盘介质类型。
        :type MediumType: str
        """
        self.Pid = None
        self.CbsSize = None
        self.MediumType = None

    def _deserialize(self, params):
        self.Pid = params.get("Pid")
        self.CbsSize = params.get("CbsSize")
        self.MediumType = params.get("MediumType")


class Filter(AbstractModel):
    """描述键值对过滤器，用于条件过滤查询。"""

    def __init__(self):
        """
        :param Name: 过滤键的名称。
        :type Name: str
        :param Values: 一个或者多个过滤值。
        :type Values: list of str
        """
        self.Name = None
        self.Values = None

    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Values = params.get("Values")


class Filters(AbstractModel):
    """描述键值对过滤器，用于条件过滤查询。"""

    def __init__(self):
        """
        :param Name: 过滤键的名称。
        :type Name: str
        :param Values: 一个或者多个过滤值。
        :type Values: list of str
        """
        self.Name = None
        self.Values = None

    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Values = params.get("Values")


class GetSnapOverviewRequest(AbstractModel):
    """GetSnapOverview请求参数结构体"""


class GetSnapOverviewResponse(AbstractModel):
    """GetSnapOverview返回参数结构体"""

    def __init__(self):
        """
        :param TotalSize: 用户快照总大小
        :type TotalSize: float
        :param RealTradeSize: 用户快照总大小（用于计费）
        :type RealTradeSize: float
        :param FreeQuota: 快照免费额度
        :type FreeQuota: float
        :param TotalNums: 快照总个数
        :type TotalNums: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalSize = None
        self.RealTradeSize = None
        self.FreeQuota = None
        self.TotalNums = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalSize = params.get("TotalSize")
        self.RealTradeSize = params.get("RealTradeSize")
        self.FreeQuota = params.get("FreeQuota")
        self.TotalNums = params.get("TotalNums")
        self.RequestId = params.get("RequestId")


class GoodsDetail(AbstractModel):
    """产品详情。"""

    def __init__(self):
        """
        :param TimeSpan: 购买或续费云盘的时长。
        :type TimeSpan: int
        :param Pid: 产品ID。
        :type Pid: int
        :param DiskType: 云盘类型，系统盘或数据盘。
        :type DiskType: str
        :param ProductInfo: 产品信息描述。
        :type ProductInfo: list of ProductInfo
        :param MediumType: 云盘介质类型。
        :type MediumType: str
        :param TimeUnit: 时长“TimeSpan”的单位。
        :type TimeUnit: str
        :param CbsSize: 云盘大小。
        :type CbsSize: int
        """
        self.TimeSpan = None
        self.Pid = None
        self.DiskType = None
        self.ProductInfo = None
        self.MediumType = None
        self.TimeUnit = None
        self.CbsSize = None

    def _deserialize(self, params):
        self.TimeSpan = params.get("TimeSpan")
        self.Pid = params.get("Pid")
        self.DiskType = params.get("DiskType")
        if params.get("ProductInfo") is not None:
            self.ProductInfo = []
            for item in params.get("ProductInfo"):
                obj = ProductInfo()
                obj._deserialize(item)
                self.ProductInfo.append(obj)
        self.MediumType = params.get("MediumType")
        self.TimeUnit = params.get("TimeUnit")
        self.CbsSize = params.get("CbsSize")


class InquiryPriceCreateDisksRequest(AbstractModel):
    """InquiryPriceCreateDisks请求参数结构体"""

    def __init__(self):
        """
        :param DiskType: 云硬盘类型。取值范围：<br><li>普通云硬盘：CLOUD_BASIC<br><li>高性能云硬盘：CLOUD_PREMIUM<br><li>SSD云硬盘：CLOUD_SSD。
        :type DiskType: str
        :param DiskSize: 云盘大小，取值范围： 普通云硬盘:10GB ~ 4000G；高性能云硬盘:50GB ~ 4000GB；SSD云硬盘:100GB ~ 4000GB，步长均为10GB。
        :type DiskSize: int
        :param DiskChargeType: 付费模式，目前只有预付费，即只能取值为PREPAID。
        :type DiskChargeType: str
        :param DiskChargePrepaid: 预付费相关参数设置，通过该参数可以指定包年包月云盘的购买时长，预付费云盘该参数必传。
        :type DiskChargePrepaid: :class:`tcecloud.cbs.v20170312.models.DiskChargePrepaid`
        :param DiskCount: 购买云盘的数量。不填则默认为1。
        :type DiskCount: int
        :param ProjectId: 云盘所属项目ID。
        :type ProjectId: int
        """
        self.DiskType = None
        self.DiskSize = None
        self.DiskChargeType = None
        self.DiskChargePrepaid = None
        self.DiskCount = None
        self.ProjectId = None

    def _deserialize(self, params):
        self.DiskType = params.get("DiskType")
        self.DiskSize = params.get("DiskSize")
        self.DiskChargeType = params.get("DiskChargeType")
        if params.get("DiskChargePrepaid") is not None:
            self.DiskChargePrepaid = DiskChargePrepaid()
            self.DiskChargePrepaid._deserialize(params.get("DiskChargePrepaid"))
        self.DiskCount = params.get("DiskCount")
        self.ProjectId = params.get("ProjectId")


class InquiryPriceCreateDisksResponse(AbstractModel):
    """InquiryPriceCreateDisks返回参数结构体"""

    def __init__(self):
        """
        :param DiskPrice: 描述了新购云盘的价格。
        :type DiskPrice: :class:`tcecloud.cbs.v20170312.models.Price`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DiskPrice = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("DiskPrice") is not None:
            self.DiskPrice = Price()
            self.DiskPrice._deserialize(params.get("DiskPrice"))
        self.RequestId = params.get("RequestId")


class InquiryPriceCreateSnapshotsRequest(AbstractModel):
    """InquiryPriceCreateSnapshots请求参数结构体"""

    def __init__(self):
        """
        :param Placement: 实例所在的位置。通过该参数可以指定实例所属可用区，所属项目。若不指定项目，将在默认项目下进行创建。
        :type Placement: :class:`tcecloud.cbs.v20170312.models.Placement`
        :param DiskSize: 创建快照的云硬盘大小，单位为GB。
        :type DiskSize: int
        :param DiskChargePrepaid: 指定快照创建的时长。
        :type DiskChargePrepaid: :class:`tcecloud.cbs.v20170312.models.DiskChargePrepaid`
        :param SnapshotCount: 创建快照的数量。默认取值为1。
        :type SnapshotCount: int
        """
        self.Placement = None
        self.DiskSize = None
        self.DiskChargePrepaid = None
        self.SnapshotCount = None

    def _deserialize(self, params):
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        self.DiskSize = params.get("DiskSize")
        if params.get("DiskChargePrepaid") is not None:
            self.DiskChargePrepaid = DiskChargePrepaid()
            self.DiskChargePrepaid._deserialize(params.get("DiskChargePrepaid"))
        self.SnapshotCount = params.get("SnapshotCount")


class InquiryPriceCreateSnapshotsResponse(AbstractModel):
    """InquiryPriceCreateSnapshots返回参数结构体"""

    def __init__(self):
        """
        :param SnapshotPrice: 创建快照的价格。
        :type SnapshotPrice: :class:`tcecloud.cbs.v20170312.models.Price`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SnapshotPrice = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("SnapshotPrice") is not None:
            self.SnapshotPrice = Price()
            self.SnapshotPrice._deserialize(params.get("SnapshotPrice"))
        self.RequestId = params.get("RequestId")


class InquiryPriceModifyDiskAttributesRequest(AbstractModel):
    """InquiryPriceModifyDiskAttributes请求参数结构体"""

    def __init__(self):
        """
        :param DiskIds: 需迁移的云盘实例ID列表，**当前仅支持一次传入一块云盘**。
        :type DiskIds: list of str
        :param DiskType: 云盘变更的目标类型，取值范围：<br><li>CLOUD_PREMIUM：表示高性能云硬盘<br><li>CLOUD_SSD：表示SSD云硬盘。<br>**当前不支持类型降级**
        :type DiskType: str
        :param ProjectId: 云盘所属项目ID。 如传入则仅用于鉴权。
        :type ProjectId: int
        """
        self.DiskIds = None
        self.DiskType = None
        self.ProjectId = None

    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")
        self.DiskType = params.get("DiskType")
        self.ProjectId = params.get("ProjectId")


class InquiryPriceModifyDiskAttributesResponse(AbstractModel):
    """InquiryPriceModifyDiskAttributes返回参数结构体"""

    def __init__(self):
        """
        :param DiskPrice: 描述了变更云盘类型的价格。
        :type DiskPrice: :class:`tcecloud.cbs.v20170312.models.Price`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DiskPrice = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("DiskPrice") is not None:
            self.DiskPrice = Price()
            self.DiskPrice._deserialize(params.get("DiskPrice"))
        self.RequestId = params.get("RequestId")


class InquiryPriceRenewDisksRequest(AbstractModel):
    """InquiryPriceRenewDisks请求参数结构体"""

    def __init__(self):
        """
        :param DiskIds: 云硬盘ID， 通过DescribeDisks接口查询。
        :type DiskIds: list of str
        :param DiskChargePrepaids: 预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月云盘的购买时长。如果在该参数中指定CurInstanceDeadline，则会按对齐到子机到期时间来续费。如果是批量续费询价，该参数与Disks参数一一对应，元素数量需保持一致。
        :type DiskChargePrepaids: list of DiskChargePrepaid
        :param NewDeadline: 指定云盘新的到期时间，形式如：2017-12-17 00:00:00。参数`NewDeadline`和`DiskChargePrepaids`是两种指定询价时长的方式，两者必传一个。
        :type NewDeadline: str
        :param ProjectId: 云盘所属项目ID。 如传入则仅用于鉴权。
        :type ProjectId: int
        """
        self.DiskIds = None
        self.DiskChargePrepaids = None
        self.NewDeadline = None
        self.ProjectId = None

    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")
        if params.get("DiskChargePrepaids") is not None:
            self.DiskChargePrepaids = []
            for item in params.get("DiskChargePrepaids"):
                obj = DiskChargePrepaid()
                obj._deserialize(item)
                self.DiskChargePrepaids.append(obj)
        self.NewDeadline = params.get("NewDeadline")
        self.ProjectId = params.get("ProjectId")


class InquiryPriceRenewDisksResponse(AbstractModel):
    """InquiryPriceRenewDisks返回参数结构体"""

    def __init__(self):
        """
        :param DiskPrice: 描述了续费云盘的价格。
        :type DiskPrice: :class:`tcecloud.cbs.v20170312.models.Price`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DiskPrice = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("DiskPrice") is not None:
            self.DiskPrice = Price()
            self.DiskPrice._deserialize(params.get("DiskPrice"))
        self.RequestId = params.get("RequestId")


class InquiryPriceResizeDiskRequest(AbstractModel):
    """InquiryPriceResizeDisk请求参数结构体"""

    def __init__(self):
        """
        :param DiskId: 云硬盘ID， 通过DescribeDisks接口查询。
        :type DiskId: str
        :param DiskSize: 云硬盘扩容后的大小，单位为GB，不得小于当前云硬盘大小。取值范围： 普通云硬盘:10GB ~ 4000G；高性能云硬盘:50GB ~ 4000GB；SSD云硬盘:100GB ~ 4000GB，步长均为10GB。
        :type DiskSize: int
        :param ProjectId: 云盘所属项目ID。 如传入则仅用于鉴权。
        :type ProjectId: int
        """
        self.DiskId = None
        self.DiskSize = None
        self.ProjectId = None

    def _deserialize(self, params):
        self.DiskId = params.get("DiskId")
        self.DiskSize = params.get("DiskSize")
        self.ProjectId = params.get("ProjectId")


class InquiryPriceResizeDiskResponse(AbstractModel):
    """InquiryPriceResizeDisk返回参数结构体"""

    def __init__(self):
        """
        :param DiskPrice: 描述了扩容云盘的价格。
        :type DiskPrice: :class:`tcecloud.cbs.v20170312.models.Price`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DiskPrice = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("DiskPrice") is not None:
            self.DiskPrice = Price()
            self.DiskPrice._deserialize(params.get("DiskPrice"))
        self.RequestId = params.get("RequestId")


class ModifyAutoSnapshotPolicyAttributeRequest(AbstractModel):
    """ModifyAutoSnapshotPolicyAttribute请求参数结构体"""

    def __init__(self):
        """
        :param AutoSnapshotPolicyId: 定期快照策略ID。
        :type AutoSnapshotPolicyId: str
        :param Policy: 定期快照的执行策略。
        :type Policy: list of Policy
        :param AutoSnapshotPolicyName: 要创建的定期快照策略名。不传则默认为“未命名”。最大长度不能超60个字节。
        :type AutoSnapshotPolicyName: str
        :param IsActivated: 是否激活定期快照策略，FALSE表示未激活，TRUE表示激活，默认为TRUE。
        :type IsActivated: bool
        :param IsPermanent: 通过该定期快照策略创建的快照是否永久保留。FALSE表示非永久保留，TRUE表示永久保留，默认为FALSE。
        :type IsPermanent: bool
        :param RetentionDays: 通过该定期快照策略创建的快照保留天数，该参数不可与`IsPermanent`参数冲突，即若定期快照策略设置为永久保留，`RetentionDays`应置0。
        :type RetentionDays: int
        """
        self.AutoSnapshotPolicyId = None
        self.Policy = None
        self.AutoSnapshotPolicyName = None
        self.IsActivated = None
        self.IsPermanent = None
        self.RetentionDays = None

    def _deserialize(self, params):
        self.AutoSnapshotPolicyId = params.get("AutoSnapshotPolicyId")
        if params.get("Policy") is not None:
            self.Policy = []
            for item in params.get("Policy"):
                obj = Policy()
                obj._deserialize(item)
                self.Policy.append(obj)
        self.AutoSnapshotPolicyName = params.get("AutoSnapshotPolicyName")
        self.IsActivated = params.get("IsActivated")
        self.IsPermanent = params.get("IsPermanent")
        self.RetentionDays = params.get("RetentionDays")


class ModifyAutoSnapshotPolicyAttributeResponse(AbstractModel):
    """ModifyAutoSnapshotPolicyAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDiskAttributesRequest(AbstractModel):
    """ModifyDiskAttributes请求参数结构体"""

    def __init__(self):
        """
        :param DiskIds: 一个或多个待操作的云硬盘ID。如果传入多个云盘ID，仅支持所有云盘修改为同一属性。
        :type DiskIds: list of str
        :param ProjectId: 新的云硬盘项目ID，只支持修改弹性云盘的项目ID。通过DescribeProject接口查询可用项目及其ID。
        :type ProjectId: int
        :param DiskName: 新的云硬盘名称。
        :type DiskName: str
        :param Portable: 是否为弹性云盘，FALSE表示非弹性云盘，TRUE表示弹性云盘。仅支持非弹性云盘修改为弹性云盘。
        :type Portable: bool
        :param DeleteWithInstance: 成功挂载到云主机后该云硬盘是否随云主机销毁，TRUE表示随云主机销毁，FALSE表示不随云主机销毁。仅支持按量计费云硬盘数据盘。
        :type DeleteWithInstance: bool
        :param DiskType: 变更云盘类型时，可传入该参数，表示变更的目标类型，取值范围：<br><li>CLOUD_PREMIUM：表示高性能云硬盘<br><li>CLOUD_SSD：表示SSD云硬盘。<br>当前不支持批量变更类型，即传入DiskType时，DiskIds仅支持传入一块云盘；<br>变更云盘类型时不支持同时变更其他属性。
        :type DiskType: str
        """
        self.DiskIds = None
        self.ProjectId = None
        self.DiskName = None
        self.Portable = None
        self.DeleteWithInstance = None
        self.DiskType = None

    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")
        self.ProjectId = params.get("ProjectId")
        self.DiskName = params.get("DiskName")
        self.Portable = params.get("Portable")
        self.DeleteWithInstance = params.get("DeleteWithInstance")
        self.DiskType = params.get("DiskType")


class ModifyDiskAttributesResponse(AbstractModel):
    """ModifyDiskAttributes返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDisksRenewFlagRequest(AbstractModel):
    """ModifyDisksRenewFlag请求参数结构体"""

    def __init__(self):
        """
        :param DiskIds: 一个或多个待操作的云硬盘ID。
        :type DiskIds: list of str
        :param RenewFlag: 云盘的续费标识。取值范围：<br><li>NOTIFY_AND_AUTO_RENEW：通知过期且自动续费<br><li>NOTIFY_AND_MANUAL_RENEW：通知过期不自动续费<br><li>DISABLE_NOTIFY_AND_MANUAL_RENEW：不通知过期不自动续费。
        :type RenewFlag: str
        """
        self.DiskIds = None
        self.RenewFlag = None

    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")
        self.RenewFlag = params.get("RenewFlag")


class ModifyDisksRenewFlagResponse(AbstractModel):
    """ModifyDisksRenewFlag返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifySnapshotAttributeRequest(AbstractModel):
    """ModifySnapshotAttribute请求参数结构体"""

    def __init__(self):
        """
        :param SnapshotId: 快照ID, 可通过DescribeSnapshots查询。
        :type SnapshotId: str
        :param SnapshotName: 新的快照名称。最长为60个字符。
        :type SnapshotName: str
        :param IsPermanent: 快照的保留时间，FALSE表示非永久保留，TRUE表示永久保留。仅支持将非永久快照修改为永久快照。
        :type IsPermanent: bool
        """
        self.SnapshotId = None
        self.SnapshotName = None
        self.IsPermanent = None

    def _deserialize(self, params):
        self.SnapshotId = params.get("SnapshotId")
        self.SnapshotName = params.get("SnapshotName")
        self.IsPermanent = params.get("IsPermanent")


class ModifySnapshotAttributeResponse(AbstractModel):
    """ModifySnapshotAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifySnapshotsSharePermissionRequest(AbstractModel):
    """ModifySnapshotsSharePermission请求参数结构体"""

    def __init__(self):
        """
        :param AccountIds: 接收分享快照的账号Id列表，array型参数的格式可以参考API简介。帐号ID不同于QQ号，查询用户帐号ID请查看帐号信息中的帐号ID栏。
        :type AccountIds: list of str
        :param Permission: 操作，包括 SHARE，CANCEL。其中SHARE代表分享操作，CANCEL代表取消分享操作。
        :type Permission: str
        :param SnapshotIds: 快照ID, 可通过DescribeSnapshots查询获取。
        :type SnapshotIds: list of str
        """
        self.AccountIds = None
        self.Permission = None
        self.SnapshotIds = None

    def _deserialize(self, params):
        self.AccountIds = params.get("AccountIds")
        self.Permission = params.get("Permission")
        self.SnapshotIds = params.get("SnapshotIds")


class ModifySnapshotsSharePermissionResponse(AbstractModel):
    """ModifySnapshotsSharePermission返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class Placement(AbstractModel):
    """描述了实例的抽象位置，包括其所在的可用区，所属的项目"""

    def __init__(self):
        """
        :param Zone: 实例所属的可用区ID。该参数也可以通过调用  DescribeZones 的返回值中的Zone字段来获取。
        :type Zone: str
        :param ProjectId: 实例所属项目ID。该参数可以通过调用 DescribeProject 的返回值中的 projectId 字段来获取。不填为默认项目。
        :type ProjectId: int
        """
        self.Zone = None
        self.ProjectId = None

    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.ProjectId = params.get("ProjectId")


class Policy(AbstractModel):
    """描述了定期快照的执行策略"""

    def __init__(self):
        """
        :param DayOfWeek: 选定周一到周日中需要创建快照的日期，取值范围：[0, 6]。0表示周一触发，依此类推。
        :type DayOfWeek: list of int non-negative
        :param Hour: 指定定期快照策略的触发时间。单位为小时，取值范围：[0, 23]。00:00 ~ 23:00 共 24 个时间点可选，1表示 01:00，依此类推。
        :type Hour: list of int non-negative
        """
        self.DayOfWeek = None
        self.Hour = None

    def _deserialize(self, params):
        self.DayOfWeek = params.get("DayOfWeek")
        self.Hour = params.get("Hour")


class Price(AbstractModel):
    """描述了云盘的价格"""

    def __init__(self):
        """
        :param OriginalPrice: 预支费用的原价，单位：元。
        :type OriginalPrice: float
        :param DiscountPrice: 预支费用的折扣价，单位：元。
        :type DiscountPrice: float
        """
        self.OriginalPrice = None
        self.DiscountPrice = None

    def _deserialize(self, params):
        self.OriginalPrice = params.get("OriginalPrice")
        self.DiscountPrice = params.get("DiscountPrice")


class ProductInfo(AbstractModel):
    """描述订单参数转换接口输出的产品信息。"""

    def __init__(self):
        """
        :param Name: 属性名称。
        :type Name: str
        :param Value: 属性值。
        :type Value: str
        """
        self.Name = None
        self.Value = None

    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Value = params.get("Value")


class RenewDiskRequest(AbstractModel):
    """RenewDisk请求参数结构体"""

    def __init__(self):
        """
        :param DiskChargePrepaid: 预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月云盘的续费时长。在云盘与挂载的实例一起续费的场景下，可以指定参数CurInstanceDeadline，此时云盘会按对齐到实例续费后的到期时间来续费。
        :type DiskChargePrepaid: :class:`tcecloud.cbs.v20170312.models.DiskChargePrepaid`
        :param DiskId: 云硬盘ID， 通过DescribeDisks接口查询。
        :type DiskId: str
        """
        self.DiskChargePrepaid = None
        self.DiskId = None

    def _deserialize(self, params):
        if params.get("DiskChargePrepaid") is not None:
            self.DiskChargePrepaid = DiskChargePrepaid()
            self.DiskChargePrepaid._deserialize(params.get("DiskChargePrepaid"))
        self.DiskId = params.get("DiskId")


class RenewDiskResponse(AbstractModel):
    """RenewDisk返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ResizeDiskOrder(AbstractModel):
    """请求计费的订单参数（扩容）。"""

    def __init__(self):
        """
                :param GoodsCategoryId: 产品类别。
                :type GoodsCategoryId: int
                :param GoodsNum: 产品数量。
                :type GoodsNum: int
                :param ProjectId: 项目ID。
                :type ProjectId: int
                :param GoodsDetail: 产品详情。
                :type GoodsDetail: :class:`tcecloud.cbs.v20170312.models.ResizeGoodsDetail`
                :param RegionId: 地域ID。
                :type RegionId: int
                :param ZoneId: 可用区ID。
                :type ZoneId: int
                :param PayMode: 付费模式。
                :type PayMode: int
                :param Type: 云盘类别。
        注意：此字段可能返回 null，表示取不到有效值。
                :type Type: str
                :param SubProductCode: 子产品ID。
        注意：此字段可能返回 null，表示取不到有效值。
                :type SubProductCode: str
        """
        self.GoodsCategoryId = None
        self.GoodsNum = None
        self.ProjectId = None
        self.GoodsDetail = None
        self.RegionId = None
        self.ZoneId = None
        self.PayMode = None
        self.Type = None
        self.SubProductCode = None

    def _deserialize(self, params):
        self.GoodsCategoryId = params.get("GoodsCategoryId")
        self.GoodsNum = params.get("GoodsNum")
        self.ProjectId = params.get("ProjectId")
        if params.get("GoodsDetail") is not None:
            self.GoodsDetail = ResizeGoodsDetail()
            self.GoodsDetail._deserialize(params.get("GoodsDetail"))
        self.RegionId = params.get("RegionId")
        self.ZoneId = params.get("ZoneId")
        self.PayMode = params.get("PayMode")
        self.Type = params.get("Type")
        self.SubProductCode = params.get("SubProductCode")


class ResizeDiskRequest(AbstractModel):
    """ResizeDisk请求参数结构体"""

    def __init__(self):
        """
        :param DiskId: 云硬盘ID， 通过DescribeDisks接口查询。
        :type DiskId: str
        :param DiskSize: 云硬盘扩容后的大小，单位为GB，必须大于当前云硬盘大小。取值范围： 普通云硬盘:10GB ~ 4000G；高性能云硬盘:50GB ~ 4000GB；SSD云硬盘:100GB ~ 4000GB，步长均为10GB。
        :type DiskSize: int
        """
        self.DiskId = None
        self.DiskSize = None

    def _deserialize(self, params):
        self.DiskId = params.get("DiskId")
        self.DiskSize = params.get("DiskSize")


class ResizeDiskResponse(AbstractModel):
    """ResizeDisk返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ResizeGoodsDetail(AbstractModel):
    """产品续费详情，只用于SwitchParameterResizeDisks接口。"""

    def __init__(self):
        """
        :param Pid: 产品ID。
        :type Pid: int
        :param ResourceId: 云盘ID。
        :type ResourceId: str
        :param CurDeadline: 云盘当前到期时间。
        :type CurDeadline: str
        :param ProductInfo: 产品信息描述。
        :type ProductInfo: list of ProductInfo
        :param NewConfig: 云盘扩容后的配置。
        :type NewConfig: :class:`tcecloud.cbs.v20170312.models.DiskResizeConfig`
        :param OldConfig: 云盘扩容前的配置。
        :type OldConfig: :class:`tcecloud.cbs.v20170312.models.DiskResizeConfig`
        """
        self.Pid = None
        self.ResourceId = None
        self.CurDeadline = None
        self.ProductInfo = None
        self.NewConfig = None
        self.OldConfig = None

    def _deserialize(self, params):
        self.Pid = params.get("Pid")
        self.ResourceId = params.get("ResourceId")
        self.CurDeadline = params.get("CurDeadline")
        if params.get("ProductInfo") is not None:
            self.ProductInfo = []
            for item in params.get("ProductInfo"):
                obj = ProductInfo()
                obj._deserialize(item)
                self.ProductInfo.append(obj)
        if params.get("NewConfig") is not None:
            self.NewConfig = DiskResizeConfig()
            self.NewConfig._deserialize(params.get("NewConfig"))
        if params.get("OldConfig") is not None:
            self.OldConfig = DiskResizeConfig()
            self.OldConfig._deserialize(params.get("OldConfig"))


class ResourcesDetail(AbstractModel):
    """描述用户的资源详情。"""

    def __init__(self):
        """
        :param Region: 资源所在地域。
        :type Region: str
        :param SnapshotNumberTotal: 快照用户数量配额。
        :type SnapshotNumberTotal: int
        :param SnapshotNumberUsed: 已使用的快照数量。
        :type SnapshotNumberUsed: int
        :param SnapshotCapacityTotal: 快照容量配额。
        :type SnapshotCapacityTotal: int
        :param SnapshotCapacityUsed: 已使用的快照容量，单位GB。
        :type SnapshotCapacityUsed: int
        :param DiskNumber: 云盘数量。
        :type DiskNumber: int
        :param NewDiskFlag: 当前地域是否包含新购买的云盘。
        :type NewDiskFlag: bool
        :param SnapshotSupportCrossCopy: 当前地域是否支持跨地域复制
        :type SnapshotSupportCrossCopy: bool
        :param DiskNumberIsolated: 回收站内的云盘数量。
        :type DiskNumberIsolated: int
        """
        self.Region = None
        self.SnapshotNumberTotal = None
        self.SnapshotNumberUsed = None
        self.SnapshotCapacityTotal = None
        self.SnapshotCapacityUsed = None
        self.DiskNumber = None
        self.NewDiskFlag = None
        self.SnapshotSupportCrossCopy = None
        self.DiskNumberIsolated = None

    def _deserialize(self, params):
        self.Region = params.get("Region")
        self.SnapshotNumberTotal = params.get("SnapshotNumberTotal")
        self.SnapshotNumberUsed = params.get("SnapshotNumberUsed")
        self.SnapshotCapacityTotal = params.get("SnapshotCapacityTotal")
        self.SnapshotCapacityUsed = params.get("SnapshotCapacityUsed")
        self.DiskNumber = params.get("DiskNumber")
        self.NewDiskFlag = params.get("NewDiskFlag")
        self.SnapshotSupportCrossCopy = params.get("SnapshotSupportCrossCopy")
        self.DiskNumberIsolated = params.get("DiskNumberIsolated")


class SharePermission(AbstractModel):
    """快照分享信息集合"""

    def __init__(self):
        """
        :param CreatedTime: 快照分享的时间
        :type CreatedTime: str
        :param AccountId: 分享的账号Id
        :type AccountId: str
        """
        self.CreatedTime = None
        self.AccountId = None

    def _deserialize(self, params):
        self.CreatedTime = params.get("CreatedTime")
        self.AccountId = params.get("AccountId")


class SnapOverview(AbstractModel):
    """用户快照信息概览，包括已创建的快照的总数和总容量。"""

    def __init__(self):
        """
        :param SnapshotCapacityUsedTotal: 用户已创建快照总容量。
        :type SnapshotCapacityUsedTotal: float
        :param SnapshotNumberUsedTotal: 用户已创建快照总个数。
        :type SnapshotNumberUsedTotal: int
        """
        self.SnapshotCapacityUsedTotal = None
        self.SnapshotNumberUsedTotal = None

    def _deserialize(self, params):
        self.SnapshotCapacityUsedTotal = params.get("SnapshotCapacityUsedTotal")
        self.SnapshotNumberUsedTotal = params.get("SnapshotNumberUsedTotal")


class Snapshot(AbstractModel):
    """描述了快照的详细信息"""

    def __init__(self):
        """
        :param SnapshotId: 快照ID。
        :type SnapshotId: str
        :param Placement: 快照所在的位置。
        :type Placement: :class:`tcecloud.cbs.v20170312.models.Placement`
        :param DiskUsage: 创建此快照的云硬盘类型。取值范围：<br><li>SYSTEM_DISK：系统盘<br><li>DATA_DISK：数据盘。
        :type DiskUsage: str
        :param DiskId: 创建此快照的云硬盘ID。
        :type DiskId: str
        :param DiskSize: 创建此快照的云硬盘大小。
        :type DiskSize: int
        :param SnapshotState: 快照的状态。取值范围：<br><li>NORMAL：正常<br><li>CREATING：创建中<br><li>ROLLBACKING：回滚中<br><li>COPYING_FROM_REMOTE：跨地域复制快照拷贝中。
        :type SnapshotState: str
        :param SnapshotName: 快照名称，用户自定义的快照别名。调用ModifySnapshotAttribute可修改此字段。
        :type SnapshotName: str
        :param Percent: 快照创建进度百分比，快照创建成功后此字段恒为100。
        :type Percent: int
        :param CreateTime: 快照的创建时间。
        :type CreateTime: str
        :param DeadlineTime: 快照到期时间。如果快照为永久保留，此字段为空。
        :type DeadlineTime: str
        :param Encrypt: 是否为加密盘创建的快照。取值范围：<br><li>true：该快照为加密盘创建的<br><li>false:非加密盘创建的快照。
        :type Encrypt: bool
        :param IsPermanent: 是否为永久快照。取值范围：<br><li>true：永久快照<br><li>false：非永久快照。
        :type IsPermanent: bool
        """
        self.SnapshotId = None
        self.Placement = None
        self.DiskUsage = None
        self.DiskId = None
        self.DiskSize = None
        self.SnapshotState = None
        self.SnapshotName = None
        self.Percent = None
        self.CreateTime = None
        self.DeadlineTime = None
        self.Encrypt = None
        self.IsPermanent = None

    def _deserialize(self, params):
        self.SnapshotId = params.get("SnapshotId")
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        self.DiskUsage = params.get("DiskUsage")
        self.DiskId = params.get("DiskId")
        self.DiskSize = params.get("DiskSize")
        self.SnapshotState = params.get("SnapshotState")
        self.SnapshotName = params.get("SnapshotName")
        self.Percent = params.get("Percent")
        self.CreateTime = params.get("CreateTime")
        self.DeadlineTime = params.get("DeadlineTime")
        self.Encrypt = params.get("Encrypt")
        self.IsPermanent = params.get("IsPermanent")


class SnapshotCopyResult(AbstractModel):
    """描述快照跨地域复制的结果。"""

    def __init__(self):
        """
        :param DestinationRegion: 跨地复制的目标地域。
        :type DestinationRegion: str
        :param SnapshotId: 复制到目标地域的新快照ID。
        :type SnapshotId: str
        """
        self.DestinationRegion = None
        self.SnapshotId = None

    def _deserialize(self, params):
        self.DestinationRegion = params.get("DestinationRegion")
        self.SnapshotId = params.get("SnapshotId")


class SwitchParameterCreateDisksRequest(AbstractModel):
    """SwitchParameterCreateDisks请求参数结构体"""

    def __init__(self):
        """
        :param DiskType: 硬盘介质类型。取值范围：<br><li>CLOUD_BASIC：表示普通云硬盘<br><li>CLOUD_PREMIUM：表示高性能云硬盘<br><li>CLOUD_SSD：表示SSD云硬盘。
        :type DiskType: str
        :param DiskChargeType: 付费模式，目前只有预付费，即只能取值为PREPAID。
        :type DiskChargeType: str
        :param DiskChargePrepaid: 预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月云盘的购买时长、是否设置自动续费等属性。
        :type DiskChargePrepaid: :class:`tcecloud.cbs.v20170312.models.DiskChargePrepaid`
        :param Placement: 云硬盘所在的位置。通过该参数可以指定云硬盘所属可用区，所属项目。若不指定项目，将在默认项目下进行创建。
        :type Placement: :class:`tcecloud.cbs.v20170312.models.Placement`
        :param DiskSize: 云硬盘大小，单位为GB。<br><li>如果传入`SnapshotId`则可不传`DiskSize`，此时新建云盘的大小为快照大小<br><li>如果传入`SnapshotId`同时传入`DiskSize`，则云盘大小必须大于或等于快照大小<br><li>云盘大小取值范围： 普通云硬盘:10GB ~ 4000G；高性能云硬盘:50GB ~ 4000GB；SSD云硬盘:100GB ~ 4000GB。步长均为10GB
        :type DiskSize: int
        :param DiskCount: 购买数量。单次请求最多可创建的云盘数有限制，具体参见云硬盘使用限制。默认取值为1。
        :type DiskCount: int
        :param DiskUsage: 指定创建系统盘或数据盘。取值范围：<br><li>SYSTEM_DISK：表示系统盘<br><li>DATA_DISK：表示数据盘。
        :type DiskUsage: str
        :param SnapshotId: 快照ID，如果传入则根据此快照创建云硬盘，快照类型必须为数据盘快照，可通过DescribeSnapshots接口查询快照，见输出参数DiskUsage解释。
        :type SnapshotId: str
        :param DiskName: 云盘显示名称。不传则默认为“未命名”。最大长度不能超60个字节。
        :type DiskName: str
        :param Encrypt: 传入该参数用于创建加密云盘，取值固定为ENCRYPT。
        :type Encrypt: str
        :param Tags: 云盘绑定的标签。
        :type Tags: list of Tag
        :param AutoSnapshotPolicyId: 定期快照策略ID。传入此参数时，当云硬盘创建成功后将会自动绑定该定期快照策略
        :type AutoSnapshotPolicyId: str
        :param Shareable: 可选参数，默认为False。传入True时，云盘将创建为共享型云盘。
        :type Shareable: bool
        :param DiskStoragePoolGroup: 资源池组
        :type DiskStoragePoolGroup: str
        """
        self.DiskType = None
        self.DiskChargeType = None
        self.DiskChargePrepaid = None
        self.Placement = None
        self.DiskSize = None
        self.DiskCount = None
        self.DiskUsage = None
        self.SnapshotId = None
        self.DiskName = None
        self.Encrypt = None
        self.Tags = None
        self.AutoSnapshotPolicyId = None
        self.Shareable = None
        self.DiskStoragePoolGroup = None

    def _deserialize(self, params):
        self.DiskType = params.get("DiskType")
        self.DiskChargeType = params.get("DiskChargeType")
        if params.get("DiskChargePrepaid") is not None:
            self.DiskChargePrepaid = DiskChargePrepaid()
            self.DiskChargePrepaid._deserialize(params.get("DiskChargePrepaid"))
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        self.DiskSize = params.get("DiskSize")
        self.DiskCount = params.get("DiskCount")
        self.DiskUsage = params.get("DiskUsage")
        self.SnapshotId = params.get("SnapshotId")
        self.DiskName = params.get("DiskName")
        self.Encrypt = params.get("Encrypt")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.AutoSnapshotPolicyId = params.get("AutoSnapshotPolicyId")
        self.Shareable = params.get("Shareable")
        self.DiskStoragePoolGroup = params.get("DiskStoragePoolGroup")


class SwitchParameterCreateDisksResponse(AbstractModel):
    """SwitchParameterCreateDisks返回参数结构体"""

    def __init__(self):
        """
        :param DiskOrder: 计费订单参数。
        :type DiskOrder: list of DiskOrder
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DiskOrder = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("DiskOrder") is not None:
            self.DiskOrder = []
            for item in params.get("DiskOrder"):
                obj = DiskOrder()
                obj._deserialize(item)
                self.DiskOrder.append(obj)
        self.RequestId = params.get("RequestId")


class SwitchParameterModifyDiskAttributesRequest(AbstractModel):
    """SwitchParameterModifyDiskAttributes请求参数结构体"""

    def __init__(self):
        """
        :param DiskIds: 需迁移的云盘实例ID列表，**当前仅支持一次传入一块云盘**。
        :type DiskIds: list of str
        :param DiskType: 云盘变更的目标类型，取值范围：<br><li>CLOUD_PREMIUM：表示高性能云硬盘<br><li>CLOUD_SSD：表示SSD云硬盘。<br>**当前不支持类型降级**
        :type DiskType: str
        """
        self.DiskIds = None
        self.DiskType = None

    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")
        self.DiskType = params.get("DiskType")


class SwitchParameterModifyDiskAttributesResponse(AbstractModel):
    """SwitchParameterModifyDiskAttributes返回参数结构体"""

    def __init__(self):
        """
        :param DiskOrder: 变更云盘类型计费订单参数。
        :type DiskOrder: :class:`tcecloud.cbs.v20170312.models.ResizeDiskOrder`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DiskOrder = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("DiskOrder") is not None:
            self.DiskOrder = ResizeDiskOrder()
            self.DiskOrder._deserialize(params.get("DiskOrder"))
        self.RequestId = params.get("RequestId")


class SwitchParameterRenewDisksRequest(AbstractModel):
    """SwitchParameterRenewDisks请求参数结构体"""

    def __init__(self):
        """
        :param DiskIds: 一个或多个待操作的云硬盘ID。
        :type DiskIds: list of str
        :param DiskChargePrepaids: 预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月云盘的续费时长。在云盘与挂载的实例一起续费的场景下，可以指定参数CurInstanceDeadline，此时云盘会按对齐到实例续费后的到期时间来续费。
        :type DiskChargePrepaids: list of DiskChargePrepaid
        """
        self.DiskIds = None
        self.DiskChargePrepaids = None

    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")
        if params.get("DiskChargePrepaids") is not None:
            self.DiskChargePrepaids = []
            for item in params.get("DiskChargePrepaids"):
                obj = DiskChargePrepaid()
                obj._deserialize(item)
                self.DiskChargePrepaids.append(obj)


class SwitchParameterRenewDisksResponse(AbstractModel):
    """SwitchParameterRenewDisks返回参数结构体"""

    def __init__(self):
        """
        :param DiskOrder: 计费订单参数。
        :type DiskOrder: list of DiskOrder
        :param NeedAlignWithInstance: 到期时间对齐到实例时，是否有云盘需要续费。该参数只有在对齐实例到期时间时才返回。
        :type NeedAlignWithInstance: bool
        :param NewDeadlineSet: 云盘续费后的到期时间。
        :type NewDeadlineSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DiskOrder = None
        self.NeedAlignWithInstance = None
        self.NewDeadlineSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("DiskOrder") is not None:
            self.DiskOrder = []
            for item in params.get("DiskOrder"):
                obj = DiskOrder()
                obj._deserialize(item)
                self.DiskOrder.append(obj)
        self.NeedAlignWithInstance = params.get("NeedAlignWithInstance")
        self.NewDeadlineSet = params.get("NewDeadlineSet")
        self.RequestId = params.get("RequestId")


class SwitchParameterResizeDiskRequest(AbstractModel):
    """SwitchParameterResizeDisk请求参数结构体"""

    def __init__(self):
        """
        :param DiskId: 云硬盘ID， 通过DescribeDisks接口查询。
        :type DiskId: str
        :param DiskSize: 扩容后的磁盘大小。必须大于当前值，最大值为4000G，步长为10G。
        :type DiskSize: int
        """
        self.DiskId = None
        self.DiskSize = None

    def _deserialize(self, params):
        self.DiskId = params.get("DiskId")
        self.DiskSize = params.get("DiskSize")


class SwitchParameterResizeDiskResponse(AbstractModel):
    """SwitchParameterResizeDisk返回参数结构体"""

    def __init__(self):
        """
        :param DiskOrder: 计费订单参数。
        :type DiskOrder: list of DiskOrder
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DiskOrder = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("DiskOrder") is not None:
            self.DiskOrder = []
            for item in params.get("DiskOrder"):
                obj = DiskOrder()
                obj._deserialize(item)
                self.DiskOrder.append(obj)
        self.RequestId = params.get("RequestId")


class Tag(AbstractModel):
    """标签。"""

    def __init__(self):
        """
        :param Key: 标签健。
        :type Key: str
        :param Value: 标签值。
        :type Value: str
        """
        self.Key = None
        self.Value = None

    def _deserialize(self, params):
        self.Key = params.get("Key")
        self.Value = params.get("Value")


class TerminateDisksRequest(AbstractModel):
    """TerminateDisks请求参数结构体"""

    def __init__(self):
        """
        :param DiskIds: 需退还的云盘ID列表。
        :type DiskIds: list of str
        """
        self.DiskIds = None

    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")


class TerminateDisksResponse(AbstractModel):
    """TerminateDisks返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UnbindAutoSnapshotPolicyRequest(AbstractModel):
    """UnbindAutoSnapshotPolicy请求参数结构体"""

    def __init__(self):
        """
        :param DiskIds: 要解绑定期快照策略的云盘ID列表。
        :type DiskIds: list of str
        :param AutoSnapshotPolicyId: 要解绑的定期快照策略ID。
        :type AutoSnapshotPolicyId: str
        """
        self.DiskIds = None
        self.AutoSnapshotPolicyId = None

    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")
        self.AutoSnapshotPolicyId = params.get("AutoSnapshotPolicyId")


class UnbindAutoSnapshotPolicyResponse(AbstractModel):
    """UnbindAutoSnapshotPolicy返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")

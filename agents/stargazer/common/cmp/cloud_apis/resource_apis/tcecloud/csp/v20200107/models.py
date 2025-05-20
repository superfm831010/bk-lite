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


class DeleteMultipleObjectRequest(AbstractModel):
    """DeleteMultipleObject请求参数结构体"""

    def __init__(self):
        """
        :param TmpSecretId: 临时密钥的 tmpSecretId
        :type TmpSecretId: str
        :param TmpSecretKey: 临时密钥的 tmpSecretKey
        :type TmpSecretKey: str
        :param SessionToken: 临时密钥的 sessionToken
        :type SessionToken: str
        :param CosRegion: 存储桶所在的 COS 地域
        :type CosRegion: str
        :param Bucket: 存储桶的名称，命名格式为 BucketName-APPID
        :type Bucket: str
        :param Objects: 要删除的对象列表
        :type Objects: list of DeleteObjectObjects
        """
        self.TmpSecretId = None
        self.TmpSecretKey = None
        self.SessionToken = None
        self.CosRegion = None
        self.Bucket = None
        self.Objects = None

    def _deserialize(self, params):
        self.TmpSecretId = params.get("TmpSecretId")
        self.TmpSecretKey = params.get("TmpSecretKey")
        self.SessionToken = params.get("SessionToken")
        self.CosRegion = params.get("CosRegion")
        self.Bucket = params.get("Bucket")
        if params.get("Objects") is not None:
            self.Objects = []
            for item in params.get("Objects"):
                obj = DeleteObjectObjects()
                obj._deserialize(item)
                self.Objects.append(obj)


class DeleteMultipleObjectResponse(AbstractModel):
    """DeleteMultipleObject返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteObjectObjects(AbstractModel):
    """对象列表"""

    def __init__(self):
        """
        :param Key: 对象键（Object 的名称），对象在存储桶中的唯一标识
        :type Key: str
        :param VersionId: 要删除的对象版本 ID 或 DeleteMarker 版本 ID
        :type VersionId: str
        """
        self.Key = None
        self.VersionId = None

    def _deserialize(self, params):
        self.Key = params.get("Key")
        self.VersionId = params.get("VersionId")


class DeleteObjectRequest(AbstractModel):
    """DeleteObject请求参数结构体"""

    def __init__(self):
        """
        :param TmpSecretId: 临时密钥的 tmpSecretId
        :type TmpSecretId: str
        :param TmpSecretKey: 临时密钥的 tmpSecretKey
        :type TmpSecretKey: str
        :param SessionToken: 临时密钥的 sessionToken
        :type SessionToken: str
        :param CosRegion: 存储桶所在的 COS 地域
        :type CosRegion: str
        :param Bucket: 存储桶的名称，命名格式为 BucketName-APPID
        :type Bucket: str
        :param ObjectKey: 对象键（Object 的名称），对象在存储桶中的唯一标识
        :type ObjectKey: str
        :param VersionId: 要删除的对象版本 ID 或 DeleteMarker 版本 ID
        :type VersionId: str
        """
        self.TmpSecretId = None
        self.TmpSecretKey = None
        self.SessionToken = None
        self.CosRegion = None
        self.Bucket = None
        self.ObjectKey = None
        self.VersionId = None

    def _deserialize(self, params):
        self.TmpSecretId = params.get("TmpSecretId")
        self.TmpSecretKey = params.get("TmpSecretKey")
        self.SessionToken = params.get("SessionToken")
        self.CosRegion = params.get("CosRegion")
        self.Bucket = params.get("Bucket")
        self.ObjectKey = params.get("ObjectKey")
        self.VersionId = params.get("VersionId")


class DeleteObjectResponse(AbstractModel):
    """DeleteObject返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class GetBucketRefererRequest(AbstractModel):
    """GetBucketReferer请求参数结构体"""

    def __init__(self):
        """
        :param TmpSecretId: 临时密钥的 tmpSecretId
        :type TmpSecretId: str
        :param TmpSecretKey: 临时密钥的 tmpSecretKey
        :type TmpSecretKey: str
        :param SessionToken: 临时密钥的 sessionToken
        :type SessionToken: str
        :param CosRegion: 存储桶所在的 COS 地域
        :type CosRegion: str
        :param Bucket: 存储桶的名称，命名格式为 BucketName-APPID
        :type Bucket: str
        """
        self.TmpSecretId = None
        self.TmpSecretKey = None
        self.SessionToken = None
        self.CosRegion = None
        self.Bucket = None

    def _deserialize(self, params):
        self.TmpSecretId = params.get("TmpSecretId")
        self.TmpSecretKey = params.get("TmpSecretKey")
        self.SessionToken = params.get("SessionToken")
        self.CosRegion = params.get("CosRegion")
        self.Bucket = params.get("Bucket")


class GetBucketRefererResponse(AbstractModel):
    """GetBucketReferer返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class GetOverviewRequest(AbstractModel):
    """GetOverview请求参数结构体"""

    def __init__(self):
        """
        :param CosRegion: COS 地域
        :type CosRegion: str
        """
        self.CosRegion = None

    def _deserialize(self, params):
        self.CosRegion = params.get("CosRegion")


class GetOverviewResponse(AbstractModel):
    """GetOverview返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class GetRegionListRequest(AbstractModel):
    """GetRegionList请求参数结构体"""


class GetRegionListResponse(AbstractModel):
    """GetRegionList返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class GetServiceRequest(AbstractModel):
    """GetService请求参数结构体"""

    def __init__(self):
        """
        :param TmpSecretId: 临时密钥的 tmpSecretId
        :type TmpSecretId: str
        :param TmpSecretKey: 临时密钥的 tmpSecretKey
        :type TmpSecretKey: str
        :param CosRegion: 存储桶所在的 COS 地域
        :type CosRegion: str
        :param SessionToken: 临时密钥的 sessionToken
        :type SessionToken: str
        """
        self.TmpSecretId = None
        self.TmpSecretKey = None
        self.CosRegion = None
        self.SessionToken = None

    def _deserialize(self, params):
        self.TmpSecretId = params.get("TmpSecretId")
        self.TmpSecretKey = params.get("TmpSecretKey")
        self.CosRegion = params.get("CosRegion")
        self.SessionToken = params.get("SessionToken")


class GetServiceResponse(AbstractModel):
    """GetService返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        :param Buckets: 存储桶列表。
        :type Buckets: list
        """
        self.RequestId = None
        self.Buckets = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")
        self.Buckets = params.get("Buckets")


class GetStatDayRequest(AbstractModel):
    """GetStatDay请求参数结构体"""

    def __init__(self):
        """
        :param CosRegion: 存储桶所在 COS 地域
        :type CosRegion: str
        :param Bucket: 存储桶名称
        :type Bucket: str
        :param Date: 统计信息日期
        :type Date: str
        :param StorageType: 存储类型 1:标准存储 2:低频存储
        :type StorageType: int
        """
        self.CosRegion = None
        self.Bucket = None
        self.Date = None
        self.StorageType = None

    def _deserialize(self, params):
        self.CosRegion = params.get("CosRegion")
        self.Bucket = params.get("Bucket")
        self.Date = params.get("Date")
        self.StorageType = params.get("StorageType")


class GetStatDayResponse(AbstractModel):
    """GetStatDay返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class GetStatDaysRequest(AbstractModel):
    """GetStatDays请求参数结构体"""

    def __init__(self):
        """
        :param CosRegion: 存储桶所在 COS 地域
        :type CosRegion: str
        :param Bucket: 存储桶名称
        :type Bucket: str
        :param StartDate: 统计信息开始日期
        :type StartDate: str
        :param EndDate: 统计信息结束日期
        :type EndDate: str
        :param StorageType: 存储类型 1: 标准存储 2: 低频存储
        :type StorageType: int
        """
        self.CosRegion = None
        self.Bucket = None
        self.StartDate = None
        self.EndDate = None
        self.StorageType = None

    def _deserialize(self, params):
        self.CosRegion = params.get("CosRegion")
        self.Bucket = params.get("Bucket")
        self.StartDate = params.get("StartDate")
        self.EndDate = params.get("EndDate")
        self.StorageType = params.get("StorageType")


class GetStatDaysResponse(AbstractModel):
    """GetStatDays返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class GetStatHttpDayRequest(AbstractModel):
    """GetStatHttpDay请求参数结构体"""

    def __init__(self):
        """
        :param CosRegion: 存储桶所在 COS 地域
        :type CosRegion: str
        :param Bucket: 存储桶名称
        :type Bucket: str
        :param Date: 统计信息日期
        :type Date: str
        :param StorageType: 存储类型，1: 标准存储; 2: 低频存储
        :type StorageType: int
        """
        self.CosRegion = None
        self.Bucket = None
        self.Date = None
        self.StorageType = None

    def _deserialize(self, params):
        self.CosRegion = params.get("CosRegion")
        self.Bucket = params.get("Bucket")
        self.Date = params.get("Date")
        self.StorageType = params.get("StorageType")


class GetStatHttpDayResponse(AbstractModel):
    """GetStatHttpDay返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class GetStatHttpDaysRequest(AbstractModel):
    """GetStatHttpDays请求参数结构体"""

    def __init__(self):
        """
        :param CosRegion: 存储桶所在 COS 地域
        :type CosRegion: str
        :param Bucket: 存储桶名称
        :type Bucket: str
        :param StartDate: 统计信息开始日期
        :type StartDate: str
        :param EndDate: 统计信息结束日期
        :type EndDate: str
        :param StorageType: 存储类型，1: 标准存储; 2: 低频存储
        :type StorageType: int
        """
        self.CosRegion = None
        self.Bucket = None
        self.StartDate = None
        self.EndDate = None
        self.StorageType = None

    def _deserialize(self, params):
        self.CosRegion = params.get("CosRegion")
        self.Bucket = params.get("Bucket")
        self.StartDate = params.get("StartDate")
        self.EndDate = params.get("EndDate")
        self.StorageType = params.get("StorageType")


class GetStatHttpDaysResponse(AbstractModel):
    """GetStatHttpDays返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class GetUserStatRequest(AbstractModel):
    """GetUserStat请求参数结构体"""

    def __init__(self):
        """
        :param CosRegion: 存储桶所在的 COS 地域
        :type CosRegion: str
        """
        self.CosRegion = None

    def _deserialize(self, params):
        self.CosRegion = params.get("CosRegion")


class GetUserStatResponse(AbstractModel):
    """GetUserStat返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class HeadObjectRequest(AbstractModel):
    """HeadObject请求参数结构体"""

    def __init__(self):
        """
        :param TmpSecretId: 临时密钥的 tmpSecretId
        :type TmpSecretId: str
        :param TmpSecretKey: 临时密钥的 tmpSecretKey
        :type TmpSecretKey: str
        :param CosRegion: 存储桶所在的 COS 地域
        :type CosRegion: str
        :param Bucket: 存储桶的名称，命名格式为 BucketName-APPID
        :type Bucket: str
        :param Key: 对象键（Object 的名称），对象在存储桶中的唯一标识
        :type Key: str
        :param SessionToken: 临时密钥的 sessionToken
        :type SessionToken: str
        """
        self.TmpSecretId = None
        self.TmpSecretKey = None
        self.CosRegion = None
        self.Bucket = None
        self.Key = None
        self.SessionToken = None

    def _deserialize(self, params):
        self.TmpSecretId = params.get("TmpSecretId")
        self.TmpSecretKey = params.get("TmpSecretKey")
        self.CosRegion = params.get("CosRegion")
        self.Bucket = params.get("Bucket")
        self.Key = params.get("Key")
        self.SessionToken = params.get("SessionToken")


class HeadObjectResponse(AbstractModel):
    """HeadObject返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class OpenCosBillingRequest(AbstractModel):
    """OpenCosBilling请求参数结构体"""

    def __init__(self):
        """
        :param CosRegion: 存储桶所在的 COS 地域
        :type CosRegion: str
        """
        self.CosRegion = None

    def _deserialize(self, params):
        self.CosRegion = params.get("CosRegion")


class OpenCosBillingResponse(AbstractModel):
    """OpenCosBilling返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class PutBucketRefererRequest(AbstractModel):
    """PutBucketReferer请求参数结构体"""

    def __init__(self):
        """
        :param TmpSecretId: 临时密钥的 tmpSecretId
        :type TmpSecretId: str
        :param TmpSecretKey: 临时密钥的 tmpSecretKey
        :type TmpSecretKey: str
        :param SessionToken: 临时密钥的 sessionToken
        :type SessionToken: str
        :param CosRegion: 存储桶所在的 COS 地域
        :type CosRegion: str
        :param Bucket: 存储桶的名称，命名格式为 BucketName-APPID
        :type Bucket: str
        :param RefererConfiguration: 防盗链配置信息
        :type RefererConfiguration: :class:`tcecloud.csp.v20200107.models.RefererConfiguration`
        """
        self.TmpSecretId = None
        self.TmpSecretKey = None
        self.SessionToken = None
        self.CosRegion = None
        self.Bucket = None
        self.RefererConfiguration = None

    def _deserialize(self, params):
        self.TmpSecretId = params.get("TmpSecretId")
        self.TmpSecretKey = params.get("TmpSecretKey")
        self.SessionToken = params.get("SessionToken")
        self.CosRegion = params.get("CosRegion")
        self.Bucket = params.get("Bucket")
        if params.get("RefererConfiguration") is not None:
            self.RefererConfiguration = RefererConfiguration()
            self.RefererConfiguration._deserialize(params.get("RefererConfiguration"))


class PutBucketRefererResponse(AbstractModel):
    """PutBucketReferer返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class PutBucketRequest(AbstractModel):
    """PutBucket请求参数结构体"""

    def __init__(self):
        """
        :param TmpSecretId: 临时密钥的 tmpSecretId
        :type TmpSecretId: str
        :param TmpSecretKey: 临时密钥的 tmpSecretKey
        :type TmpSecretKey: str
        :param CosRegion: 存储桶所在的 COS 地域
        :type CosRegion: str
        :param Bucket: 存储桶的名称，命名格式为 BucketName-APPID
        :type Bucket: str
        :param SessionToken: 临时密钥的 sessionToken
        :type SessionToken: str
        :param ACL: 定义存储桶的访问控制列表（ACL）属性。枚举值请参见 ACL 概述 文档中存储桶的预设 ACL 部分，例如 private，public-read 等，默认为 private
        :type ACL: str
        :param GrantRead: 赋予被授权者读取存储桶的权限，格式：id="[OwnerUin]"，可使用半角逗号（,）分隔多组被授权者： 当需要给子账号授权时，id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>" 当需要给主账号授权时，id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>" 例如'id="qcs::cam::uin/100000000001:uin/100000000001", id="qcs::cam::uin/100000000001:uin/100000000011"'
        :type GrantRead: str
        :param GrantWrite: 赋予被授权者写入存储桶的权限，格式：id="[OwnerUin]"，可使用半角逗号（,）分隔多组被授权者： 当需要给子账号授权时，id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>" 当需要给主账号授权时，id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>" 例如'id="qcs::cam::uin/100000000001:uin/100000000001", id="qcs::cam::uin/100000000001:uin/100000000011"'
        :type GrantWrite: str
        :param GrantReadAcp: 赋予被授权者读取存储桶的访问控制列表（ACL）和存储桶策略（Policy）的权限。可使用半角逗号（,）分隔多组被授权者： 当需要给子账号授权时，id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>" 当需要给主账号授权时，id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>" 例如'id="qcs::cam::uin/100000000001:uin/100000000001", id="qcs::cam::uin/100000000001:uin/100000000011"'
        :type GrantReadAcp: str
        :param GrantWriteAcp: 赋予被授权者写入存储桶的访问控制列表（ACL）和存储桶策略（Policy）的权限，可使用半角逗号（,）分隔多组被授权者： 当需要给子账号授权时，id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>" 当需要给主账号授权时，id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>" 例如'id="qcs::cam::uin/100000000001:uin/100000000001",id="qcs::cam::uin/100000000001:uin/100000000011"'
        :type GrantWriteAcp: str
        :param GrantFullControl: 赋予被授权者操作存储桶的所有权限，格式：id="[OwnerUin]"，可使用半角逗号（,）分隔多组被授权者： 当需要给子账号授权时，id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>" 当需要给主账号授权时，id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>" 例如'id="qcs::cam::uin/100000000001:uin/100000000001", id="qcs::cam::uin/100000000001:uin/100000000011"'
        :type GrantFullControl: str
        """
        self.TmpSecretId = None
        self.TmpSecretKey = None
        self.CosRegion = None
        self.Bucket = None
        self.SessionToken = None
        self.ACL = None
        self.GrantRead = None
        self.GrantWrite = None
        self.GrantReadAcp = None
        self.GrantWriteAcp = None
        self.GrantFullControl = None

    def _deserialize(self, params):
        self.TmpSecretId = params.get("TmpSecretId")
        self.TmpSecretKey = params.get("TmpSecretKey")
        self.CosRegion = params.get("CosRegion")
        self.Bucket = params.get("Bucket")
        self.SessionToken = params.get("SessionToken")
        self.ACL = params.get("ACL")
        self.GrantRead = params.get("GrantRead")
        self.GrantWrite = params.get("GrantWrite")
        self.GrantReadAcp = params.get("GrantReadAcp")
        self.GrantWriteAcp = params.get("GrantWriteAcp")
        self.GrantFullControl = params.get("GrantFullControl")


class PutBucketResponse(AbstractModel):
    """PutBucket返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class RefererConfiguration(AbstractModel):
    """防盗链配置信息"""

    def __init__(self):
        """
        :param Status: 是否开启防盗链，枚举值：Enabled、Disabled
        :type Status: str
        :param RefererType: 防盗链类型，枚举值：Black-List、White-List
        :type RefererType: str
        :param DomainList: 生效域名列表， 支持多个域名且为前缀匹配， 支持带端口的域名和 IP， 支持通配符*，做二级域名或多级域名的通配
        :type DomainList: :class:`tcecloud.csp.v20200107.models.RefererConfigurationDomainList`
        :param EmptyReferConfiguration: 是否允许空 Referer 访问，枚举值：Allow、Deny，默认值为 Deny
        :type EmptyReferConfiguration: str
        """
        self.Status = None
        self.RefererType = None
        self.DomainList = None
        self.EmptyReferConfiguration = None

    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RefererType = params.get("RefererType")
        if params.get("DomainList") is not None:
            self.DomainList = RefererConfigurationDomainList()
            self.DomainList._deserialize(params.get("DomainList"))
        self.EmptyReferConfiguration = params.get("EmptyReferConfiguration")


class RefererConfigurationDomainList(AbstractModel):
    """防盗链配置信息的域名列表"""

    def __init__(self):
        """
        :param Domains: 生效域名列表， 支持多个域名且为前缀匹配， 支持带端口的域名和 IP， 支持通配符*，做二级域名或多级域名的通配
        :type Domains: list of str
        """
        self.Domains = None

    def _deserialize(self, params):
        self.Domains = params.get("Domains")

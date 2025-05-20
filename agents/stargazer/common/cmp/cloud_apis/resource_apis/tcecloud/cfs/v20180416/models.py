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


class CfsKmsKeys(AbstractModel):
    """CfsKmsKeys"""

    def __init__(self):
        """
        :param NextRotateTime: 下次轮转时间戳
        :type NextRotateTime: int
        :param Owner: 密钥属主
        :type Owner: str
        :param KeyRotationEnabled: 密钥轮转是否开启
        :type KeyRotationEnabled: bool
        :param KeyId: Key的ID
        :type KeyId: str
        :param Alias: 密钥别名
        :type Alias: str
        :param CreateTime: 创建时间戳
        :type CreateTime: int
        :param Description: 密钥描述
        :type Description: str
        :param KeyState: Key状态，可选值为“Enabled“，”Disabled“
        :type KeyState: str
        :param KeyUsage: 密钥使用方
        :type KeyUsage: str
        :param Type: Key类型
        :type Type: int
        :param CreatorUin: 创建者UIN
        :type CreatorUin: int
        """
        self.NextRotateTime = None
        self.Owner = None
        self.KeyRotationEnabled = None
        self.KeyId = None
        self.Alias = None
        self.CreateTime = None
        self.Description = None
        self.KeyState = None
        self.KeyUsage = None
        self.Type = None
        self.CreatorUin = None

    def _deserialize(self, params):
        self.NextRotateTime = params.get("NextRotateTime")
        self.Owner = params.get("Owner")
        self.KeyRotationEnabled = params.get("KeyRotationEnabled")
        self.KeyId = params.get("KeyId")
        self.Alias = params.get("Alias")
        self.CreateTime = params.get("CreateTime")
        self.Description = params.get("Description")
        self.KeyState = params.get("KeyState")
        self.KeyUsage = params.get("KeyUsage")
        self.Type = params.get("Type")
        self.CreatorUin = params.get("CreatorUin")


class CreateCfsFileSystemRequest(AbstractModel):
    """CreateCfsFileSystem请求参数结构体"""

    def __init__(self):
        """
        :param NetInterface: 网络类型
        :type NetInterface: str
        :param PGroupId: 权限组 ID
        :type PGroupId: str
        :param ZoneId: 可用区 ID
        :type ZoneId: int
        :param Zone: 可用区缩写
        :type Zone: str
        :param CreationToken: 用户自定义文件系统名称
        :type CreationToken: str
        :param Protocol: 文件系统协议类型
        :type Protocol: str
        :param StorageType: 文件系统存储类型
        :type StorageType: str
        :param VpcId: VPC ID
        :type VpcId: int
        :param UnVpcId: 系统分配的VPC统一ID
        :type UnVpcId: str
        :param SubnetId: 子网 ID
        :type SubnetId: int
        :param UnSubnetId: 系统分配的子网统一 ID
        :type UnSubnetId: str
        :param MountIP: 指定IP地址，仅VPC网络支持
        :type MountIP: str
        :param StorageResourcePkgId: 文件系统绑定的存储包，每个文件系统只能绑定一个。低频文件系统该字段为必填
        :type StorageResourcePkgId: str
        :param BandwidthResourcePkgId: 文件系统绑定的带宽包，每个文件系统只能绑定一个
        :type BandwidthResourcePkgId: str
        :param FsName: 用户自定义文件系统名称，优先级优于CreationToken
        :type FsName: str
        :param Encrypted: 文件系统协议类型，输入值 NFS，CIFS；不填默认为 NFS
        :type Encrypted: bool
        :param KmsKeyId: 文件系统是否加密
        :type KmsKeyId: str
        """
        self.NetInterface = None
        self.PGroupId = None
        self.ZoneId = None
        self.Zone = None
        self.CreationToken = None
        self.Protocol = None
        self.StorageType = None
        self.VpcId = None
        self.UnVpcId = None
        self.SubnetId = None
        self.UnSubnetId = None
        self.MountIP = None
        self.StorageResourcePkgId = None
        self.BandwidthResourcePkgId = None
        self.FsName = None
        self.Encrypted = None
        self.KmsKeyId = None

    def _deserialize(self, params):
        self.NetInterface = params.get("NetInterface")
        self.PGroupId = params.get("PGroupId")
        self.ZoneId = params.get("ZoneId")
        self.Zone = params.get("Zone")
        self.CreationToken = params.get("CreationToken")
        self.Protocol = params.get("Protocol")
        self.StorageType = params.get("StorageType")
        self.VpcId = params.get("VpcId")
        self.UnVpcId = params.get("UnVpcId")
        self.SubnetId = params.get("SubnetId")
        self.UnSubnetId = params.get("UnSubnetId")
        self.MountIP = params.get("MountIP")
        self.StorageResourcePkgId = params.get("StorageResourcePkgId")
        self.BandwidthResourcePkgId = params.get("BandwidthResourcePkgId")
        self.FsName = params.get("FsName")
        self.Encrypted = params.get("Encrypted")
        self.KmsKeyId = params.get("KmsKeyId")


class CreateCfsFileSystemResponse(AbstractModel):
    """CreateCfsFileSystem返回参数结构体"""

    def __init__(self):
        """
        :param CreationTime: 创建时间
        :type CreationTime: str
        :param CreationToken: 用户自定义文件系统名称
        :type CreationToken: str
        :param FileSystemId: 文件系统 ID
        :type FileSystemId: str
        :param LifeCycleState: 文件系统状态
        :type LifeCycleState: str
        :param SizeByte: 文件系统已使用容量大小
        :type SizeByte: int
        :param ZoneId: 可用区 ID
        :type ZoneId: int
        :param FsName: 用户自定义文件系统名称
        :type FsName: str
        :param Encrypted: 文件系统是否加密
        :type Encrypted: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.CreationTime = None
        self.CreationToken = None
        self.FileSystemId = None
        self.LifeCycleState = None
        self.SizeByte = None
        self.ZoneId = None
        self.FsName = None
        self.Encrypted = None
        self.RequestId = None

    def _deserialize(self, params):
        self.CreationTime = params.get("CreationTime")
        self.CreationToken = params.get("CreationToken")
        self.FileSystemId = params.get("FileSystemId")
        self.LifeCycleState = params.get("LifeCycleState")
        self.SizeByte = params.get("SizeByte")
        self.ZoneId = params.get("ZoneId")
        self.FsName = params.get("FsName")
        self.Encrypted = params.get("Encrypted")
        self.RequestId = params.get("RequestId")


class CreateCfsPGroupRequest(AbstractModel):
    """CreateCfsPGroup请求参数结构体"""

    def __init__(self):
        """
        :param Name: 权限组名称
        :type Name: str
        :param DescInfo: 权限组描述信息
        :type DescInfo: str
        """
        self.Name = None
        self.DescInfo = None

    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.DescInfo = params.get("DescInfo")


class CreateCfsPGroupResponse(AbstractModel):
    """CreateCfsPGroup返回参数结构体"""

    def __init__(self):
        """
        :param PGroupId: 权限组ID
        :type PGroupId: str
        :param Name: 权限组名字
        :type Name: str
        :param DescInfo: 权限组描述信息
        :type DescInfo: str
        :param BindCfsNum: 权限组关联文件系统个数
        :type BindCfsNum: int
        :param CDate: 权限组创建时间
        :type CDate: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.PGroupId = None
        self.Name = None
        self.DescInfo = None
        self.BindCfsNum = None
        self.CDate = None
        self.RequestId = None

    def _deserialize(self, params):
        self.PGroupId = params.get("PGroupId")
        self.Name = params.get("Name")
        self.DescInfo = params.get("DescInfo")
        self.BindCfsNum = params.get("BindCfsNum")
        self.CDate = params.get("CDate")
        self.RequestId = params.get("RequestId")


class CreateCfsRuleRequest(AbstractModel):
    """CreateCfsRule请求参数结构体"""

    def __init__(self):
        """
        :param PGroupId: 权限组ID
        :type PGroupId: str
        :param AuthClientIp: 允许访问的客户端IP地址或地址段
        :type AuthClientIp: str
        :param Priority: 规则优先级，参数范围1-100。 其中 1 为最高，100为最低
        :type Priority: int
        :param RWPermission: 读写权限, 可选参数：ro, rw。ro为只读，rw为读写，不填默认为读写
        :type RWPermission: str
        :param UserPermission: 用户权限，可选参数：all_squash，no_all_squash，root_squash，no_root_squash。
        其中all_squash为所有访问用户都会被映射为匿名用户或用户组；no_all_squash为访问用户会先与本机用户匹配，
        匹配失败后再映射为匿名用户或用户组；root_squash为将来访的root用户映射为匿名用户或用户组；
        no_root_squash为来访的root用户保持root帐号权限。不填默认为no_root_squash。
        :type UserPermission: str
        """
        self.PGroupId = None
        self.AuthClientIp = None
        self.Priority = None
        self.RWPermission = None
        self.UserPermission = None

    def _deserialize(self, params):
        self.PGroupId = params.get("PGroupId")
        self.AuthClientIp = params.get("AuthClientIp")
        self.Priority = params.get("Priority")
        self.RWPermission = params.get("RWPermission")
        self.UserPermission = params.get("UserPermission")


class CreateCfsRuleResponse(AbstractModel):
    """CreateCfsRule返回参数结构体"""

    def __init__(self):
        """
        :param RuleId: 规则ID
        :type RuleId: str
        :param PGroupId: 权限组ID
        :type PGroupId: str
        :param AuthClientIp: 客户端IP
        :type AuthClientIp: str
        :param RWPermission: 读写权限
        :type RWPermission: str
        :param UserPermission: 用户权限
        :type UserPermission: str
        :param Priority: 优先级
        :type Priority: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RuleId = None
        self.PGroupId = None
        self.AuthClientIp = None
        self.RWPermission = None
        self.UserPermission = None
        self.Priority = None
        self.RequestId = None

    def _deserialize(self, params):
        self.RuleId = params.get("RuleId")
        self.PGroupId = params.get("PGroupId")
        self.AuthClientIp = params.get("AuthClientIp")
        self.RWPermission = params.get("RWPermission")
        self.UserPermission = params.get("UserPermission")
        self.Priority = params.get("Priority")
        self.RequestId = params.get("RequestId")


class DeleteCfsFileSystemRequest(AbstractModel):
    """DeleteCfsFileSystem请求参数结构体"""

    def __init__(self):
        """
        :param FileSystemId: 文件系统 ID
        :type FileSystemId: str
        """
        self.FileSystemId = None

    def _deserialize(self, params):
        self.FileSystemId = params.get("FileSystemId")


class DeleteCfsFileSystemResponse(AbstractModel):
    """DeleteCfsFileSystem返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteCfsPGroupRequest(AbstractModel):
    """DeleteCfsPGroup请求参数结构体"""

    def __init__(self):
        """
        :param PGroupId: 权限组ID
        :type PGroupId: str
        """
        self.PGroupId = None

    def _deserialize(self, params):
        self.PGroupId = params.get("PGroupId")


class DeleteCfsPGroupResponse(AbstractModel):
    """DeleteCfsPGroup返回参数结构体"""

    def __init__(self):
        """
        :param PGroupId: 权限组ID
        :type PGroupId: str
        :param AppId: 用户ID
        :type AppId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.PGroupId = None
        self.AppId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.PGroupId = params.get("PGroupId")
        self.AppId = params.get("AppId")
        self.RequestId = params.get("RequestId")


class DeleteCfsRuleRequest(AbstractModel):
    """DeleteCfsRule请求参数结构体"""

    def __init__(self):
        """
        :param PGroupId: 权限组ID
        :type PGroupId: str
        :param RuleId: 规则ID
        :type RuleId: str
        """
        self.PGroupId = None
        self.RuleId = None

    def _deserialize(self, params):
        self.PGroupId = params.get("PGroupId")
        self.RuleId = params.get("RuleId")


class DeleteCfsRuleResponse(AbstractModel):
    """DeleteCfsRule返回参数结构体"""

    def __init__(self):
        """
        :param RuleId: 规则ID
        :type RuleId: str
        :param PGroupId: 权限组ID
        :type PGroupId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RuleId = None
        self.PGroupId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.RuleId = params.get("RuleId")
        self.PGroupId = params.get("PGroupId")
        self.RequestId = params.get("RequestId")


class FileSystemInfo(AbstractModel):
    """文件系统基本信息"""

    def __init__(self):
        """
        :param CreationTime: 创建时间
        :type CreationTime: str
        :param CreationToken: 用户自定义名称
        :type CreationToken: str
        :param FileSystemId: 文件系统ID
        :type FileSystemId: str
        :param LifeCycleState: 文件系统状态
        :type LifeCycleState: str
        :param SizeByte: 文件系统已使用容量
        :type SizeByte: int
        :param SizeLimit: 文件系统最大空间限制
        :type SizeLimit: int
        :param ZoneId: 区域ID
        :type ZoneId: int
        :param Zone: 区域名称
        :type Zone: str
        :param Protocol: 文件系统协议类型
        :type Protocol: str
        :param StorageType: 文件系统存储类型
        :type StorageType: str
        :param StorageResourcePkg: 文件系统绑定的存储包
        :type StorageResourcePkg: str
        :param BandwidthResourcePkg: 文件系统绑定的带宽包
        :type BandwidthResourcePkg: str
        :param PGroup: 文件系统绑定权限组信息
        :type PGroup: :class:`tcecloud.cfs.v20180416.models.PGroup`
        :param FsName: 用户自定义名称
        :type FsName: str
        :param Encrypted: 文件系统是否加密
        :type Encrypted: bool
        :param KmsKeyId: 加密所使用的密钥，可以为密钥的ID或者ARN
        :type KmsKeyId: str
        """
        self.CreationTime = None
        self.CreationToken = None
        self.FileSystemId = None
        self.LifeCycleState = None
        self.SizeByte = None
        self.SizeLimit = None
        self.ZoneId = None
        self.Zone = None
        self.Protocol = None
        self.StorageType = None
        self.StorageResourcePkg = None
        self.BandwidthResourcePkg = None
        self.PGroup = None
        self.FsName = None
        self.Encrypted = None
        self.KmsKeyId = None

    def _deserialize(self, params):
        self.CreationTime = params.get("CreationTime")
        self.CreationToken = params.get("CreationToken")
        self.FileSystemId = params.get("FileSystemId")
        self.LifeCycleState = params.get("LifeCycleState")
        self.SizeByte = params.get("SizeByte")
        self.SizeLimit = params.get("SizeLimit")
        self.ZoneId = params.get("ZoneId")
        self.Zone = params.get("Zone")
        self.Protocol = params.get("Protocol")
        self.StorageType = params.get("StorageType")
        self.StorageResourcePkg = params.get("StorageResourcePkg")
        self.BandwidthResourcePkg = params.get("BandwidthResourcePkg")
        if params.get("PGroup") is not None:
            self.PGroup = PGroup()
            self.PGroup._deserialize(params.get("PGroup"))
        self.FsName = params.get("FsName")
        self.Encrypted = params.get("Encrypted")
        self.KmsKeyId = params.get("KmsKeyId")


class MountInfo(AbstractModel):
    """挂载点信息"""

    def __init__(self):
        """
        :param FileSystemId: 文件系统 ID
        :type FileSystemId: str
        :param MountTargetId: 挂载点 ID
        :type MountTargetId: str
        :param IpAddress: 挂载点 IP
        :type IpAddress: str
        :param FSID: 挂载根目录
        :type FSID: str
        :param LifeCycleState: 挂载点状态
        :type LifeCycleState: str
        :param NetworkInterface: 网络类型
        :type NetworkInterface: str
        :param VpcId: 私有网络 ID
        :type VpcId: str
        :param VpcName: 私有网络名称
        :type VpcName: str
        :param SubnetId: 子网 Id
        :type SubnetId: str
        :param SubnetName: 子网名称
        :type SubnetName: str
        """
        self.FileSystemId = None
        self.MountTargetId = None
        self.IpAddress = None
        self.FSID = None
        self.LifeCycleState = None
        self.NetworkInterface = None
        self.VpcId = None
        self.VpcName = None
        self.SubnetId = None
        self.SubnetName = None

    def _deserialize(self, params):
        self.FileSystemId = params.get("FileSystemId")
        self.MountTargetId = params.get("MountTargetId")
        self.IpAddress = params.get("IpAddress")
        self.FSID = params.get("FSID")
        self.LifeCycleState = params.get("LifeCycleState")
        self.NetworkInterface = params.get("NetworkInterface")
        self.VpcId = params.get("VpcId")
        self.VpcName = params.get("VpcName")
        self.SubnetId = params.get("SubnetId")
        self.SubnetName = params.get("SubnetName")


class MountTargetCollectionWithRegion(AbstractModel):
    """用于QueryMountTargetsWithRegion接口"""

    def __init__(self):
        """
        :param NumberOfMountTargets: 挂载点数量
        :type NumberOfMountTargets: int
        :param FileSystemId: 文件系统 ID
        :type FileSystemId: str
        :param MountTargets: 挂载点详情
        :type MountTargets: list of MountTargetsWithRegion
        """
        self.NumberOfMountTargets = None
        self.FileSystemId = None
        self.MountTargets = None

    def _deserialize(self, params):
        self.NumberOfMountTargets = params.get("NumberOfMountTargets")
        self.FileSystemId = params.get("FileSystemId")
        if params.get("MountTargets") is not None:
            self.MountTargets = []
            for item in params.get("MountTargets"):
                obj = MountTargetsWithRegion()
                obj._deserialize(item)
                self.MountTargets.append(obj)


class MountTargetsWithRegion(AbstractModel):
    """用于QueryMountTargetsWithRegion接口"""

    def __init__(self):
        """
        :param VpcId: 私有网络 ID
        :type VpcId: str
        :param IpAddress: 挂载点 IP
        :type IpAddress: str
        """
        self.VpcId = None
        self.IpAddress = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.IpAddress = params.get("IpAddress")


class PGroup(AbstractModel):
    """文件系统绑定权限组信息"""

    def __init__(self):
        """
        :param PGroupId: 权限组ID
        :type PGroupId: str
        :param Name: 权限组名称
        :type Name: str
        """
        self.PGroupId = None
        self.Name = None

    def _deserialize(self, params):
        self.PGroupId = params.get("PGroupId")
        self.Name = params.get("Name")


class PGroupRules(AbstractModel):
    """权限组规则列表"""

    def __init__(self):
        """
        :param RuleId: 规则ID
        :type RuleId: str
        :param AuthClientIp: 允许访问的客户端IP
        :type AuthClientIp: str
        :param RWPermission: 读写权限, ro为只读，rw为读写
        :type RWPermission: str
        :param UserPermission: 用户权限。其中all_squash为所有访问用户都会被映射为匿名用户或用户组；
        no_all_squash为访问用户会先与本机用户匹配，匹配失败后再映射为匿名用户或用户组；
        root_squash为将来访的root用户映射为匿名用户或用户组；
        no_root_squash为来访的root用户保持root帐号权限。
        :type UserPermission: str
        :param Priority: 规则优先级，1-100。 其中 1 为最高，100为最低
        :type Priority: int
        """
        self.RuleId = None
        self.AuthClientIp = None
        self.RWPermission = None
        self.UserPermission = None
        self.Priority = None

    def _deserialize(self, params):
        self.RuleId = params.get("RuleId")
        self.AuthClientIp = params.get("AuthClientIp")
        self.RWPermission = params.get("RWPermission")
        self.UserPermission = params.get("UserPermission")
        self.Priority = params.get("Priority")


class PGroups(AbstractModel):
    """权限组数组"""

    def __init__(self):
        """
        :param PGroupId: 权限组ID
        :type PGroupId: str
        :param Name: 权限组名称
        :type Name: str
        :param DescInfo: 描述信息
        :type DescInfo: str
        :param CDate: 创建时间
        :type CDate: str
        :param BindCfsNum: 关联文件系统个数
        :type BindCfsNum: int
        """
        self.PGroupId = None
        self.Name = None
        self.DescInfo = None
        self.CDate = None
        self.BindCfsNum = None

    def _deserialize(self, params):
        self.PGroupId = params.get("PGroupId")
        self.Name = params.get("Name")
        self.DescInfo = params.get("DescInfo")
        self.CDate = params.get("CDate")
        self.BindCfsNum = params.get("BindCfsNum")


class QueryAvailableZoneInfoRequest(AbstractModel):
    """QueryAvailableZoneInfo请求参数结构体"""


class QueryAvailableZoneInfoResponse(AbstractModel):
    """QueryAvailableZoneInfo返回参数结构体"""

    def __init__(self):
        """
        :param RegionZones: 可用区列表
        :type RegionZones: list of VersionCtrlRegion
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RegionZones = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("RegionZones") is not None:
            self.RegionZones = []
            for item in params.get("RegionZones"):
                obj = VersionCtrlRegion()
                obj._deserialize(item)
                self.RegionZones.append(obj)
        self.RequestId = params.get("RequestId")


class QueryCfsFileSystemRequest(AbstractModel):
    """QueryCfsFileSystem请求参数结构体"""

    def __init__(self):
        """
        :param FileSystemId: 文件系统 ID
        :type FileSystemId: str
        :param InternationalFlag: 此选项值为1时，未命名文件系统名使用英文
        :type InternationalFlag: int
        """
        self.FileSystemId = None
        self.InternationalFlag = None

    def _deserialize(self, params):
        self.FileSystemId = params.get("FileSystemId")
        self.InternationalFlag = params.get("InternationalFlag")


class QueryCfsFileSystemResponse(AbstractModel):
    """QueryCfsFileSystem返回参数结构体"""

    def __init__(self):
        """
        :param FileSystems: 文件系统信息
        :type FileSystems: list of FileSystemInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FileSystems = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("FileSystems") is not None:
            self.FileSystems = []
            for item in params.get("FileSystems"):
                obj = FileSystemInfo()
                obj._deserialize(item)
                self.FileSystems.append(obj)
        self.RequestId = params.get("RequestId")


class QueryCfsKmsKeysRequest(AbstractModel):
    """QueryCfsKmsKeys请求参数结构体"""


class QueryCfsKmsKeysResponse(AbstractModel):
    """QueryCfsKmsKeys返回参数结构体"""

    def __init__(self):
        """
        :param CfsKmsKeys: KmsKey列表
        :type CfsKmsKeys: list of CfsKmsKeys
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.CfsKmsKeys = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("CfsKmsKeys") is not None:
            self.CfsKmsKeys = []
            for item in params.get("CfsKmsKeys"):
                obj = CfsKmsKeys()
                obj._deserialize(item)
                self.CfsKmsKeys.append(obj)
        self.RequestId = params.get("RequestId")


class QueryCfsPGroupRequest(AbstractModel):
    """QueryCfsPGroup请求参数结构体"""

    def __init__(self):
        """
        :param InternationalFlag: 此选项值为1时，默认权限组使用英文
        :type InternationalFlag: int
        """
        self.InternationalFlag = None

    def _deserialize(self, params):
        self.InternationalFlag = params.get("InternationalFlag")


class QueryCfsPGroupResponse(AbstractModel):
    """QueryCfsPGroup返回参数结构体"""

    def __init__(self):
        """
        :param PGrouplist: 权限组信息列表
        :type PGrouplist: list of PGroups
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.PGrouplist = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("PGrouplist") is not None:
            self.PGrouplist = []
            for item in params.get("PGrouplist"):
                obj = PGroups()
                obj._deserialize(item)
                self.PGrouplist.append(obj)
        self.RequestId = params.get("RequestId")


class QueryCfsRuleRequest(AbstractModel):
    """QueryCfsRule请求参数结构体"""

    def __init__(self):
        """
        :param PGroupId: 权限组ID
        :type PGroupId: str
        """
        self.PGroupId = None

    def _deserialize(self, params):
        self.PGroupId = params.get("PGroupId")


class QueryCfsRuleResponse(AbstractModel):
    """QueryCfsRule返回参数结构体"""

    def __init__(self):
        """
        :param RuleList: 权限组规则列表
        :type RuleList: list of PGroupRules
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RuleList = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("RuleList") is not None:
            self.RuleList = []
            for item in params.get("RuleList"):
                obj = PGroupRules()
                obj._deserialize(item)
                self.RuleList.append(obj)
        self.RequestId = params.get("RequestId")


class QueryCfsServiceStatusRequest(AbstractModel):
    """QueryCfsServiceStatus请求参数结构体"""


class QueryCfsServiceStatusResponse(AbstractModel):
    """QueryCfsServiceStatus返回参数结构体"""

    def __init__(self):
        """
        :param CfsServiceStatus: 该用户当前CFS服务的状态，none为未开通，creating为开通中，created为已开通
        :type CfsServiceStatus: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.CfsServiceStatus = None
        self.RequestId = None

    def _deserialize(self, params):
        self.CfsServiceStatus = params.get("CfsServiceStatus")
        self.RequestId = params.get("RequestId")


class QueryMountTargetRequest(AbstractModel):
    """QueryMountTarget请求参数结构体"""

    def __init__(self):
        """
        :param FileSystemId: 文件系统 ID
        :type FileSystemId: str
        """
        self.FileSystemId = None

    def _deserialize(self, params):
        self.FileSystemId = params.get("FileSystemId")


class QueryMountTargetResponse(AbstractModel):
    """QueryMountTarget返回参数结构体"""

    def __init__(self):
        """
        :param MountTargets: 挂载点详情
        :type MountTargets: list of MountInfo
        :param NumberOfMountTargets: 挂载点数量
        :type NumberOfMountTargets: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.MountTargets = None
        self.NumberOfMountTargets = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("MountTargets") is not None:
            self.MountTargets = []
            for item in params.get("MountTargets"):
                obj = MountInfo()
                obj._deserialize(item)
                self.MountTargets.append(obj)
        self.NumberOfMountTargets = params.get("NumberOfMountTargets")
        self.RequestId = params.get("RequestId")


class QueryMountTargetsWithRegionRequest(AbstractModel):
    """QueryMountTargetsWithRegion请求参数结构体"""


class QueryMountTargetsWithRegionResponse(AbstractModel):
    """QueryMountTargetsWithRegion返回参数结构体"""

    def __init__(self):
        """
        :param MountTargetCollection: 挂载点列表
        :type MountTargetCollection: list of MountTargetCollectionWithRegion
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.MountTargetCollection = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("MountTargetCollection") is not None:
            self.MountTargetCollection = []
            for item in params.get("MountTargetCollection"):
                obj = MountTargetCollectionWithRegion()
                obj._deserialize(item)
                self.MountTargetCollection.append(obj)
        self.RequestId = params.get("RequestId")


class SignUpCfsServiceRequest(AbstractModel):
    """SignUpCfsService请求参数结构体"""


class SignUpCfsServiceResponse(AbstractModel):
    """SignUpCfsService返回参数结构体"""

    def __init__(self):
        """
        :param CfsServiceStatus: 该用户当前CFS服务的状态，none是未开通，creating是开通中，created是已开通
        :type CfsServiceStatus: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.CfsServiceStatus = None
        self.RequestId = None

    def _deserialize(self, params):
        self.CfsServiceStatus = params.get("CfsServiceStatus")
        self.RequestId = params.get("RequestId")


class UpdateCfsFileSystemNameRequest(AbstractModel):
    """UpdateCfsFileSystemName请求参数结构体"""

    def __init__(self):
        """
        :param FileSystemId: 文件系统ID
        :type FileSystemId: str
        :param CreationToken: 用户自定义文件系统名称
        :type CreationToken: str
        :param FsName: 用户自定义文件系统名称，优先级优于CreationToken
        :type FsName: str
        """
        self.FileSystemId = None
        self.CreationToken = None
        self.FsName = None

    def _deserialize(self, params):
        self.FileSystemId = params.get("FileSystemId")
        self.CreationToken = params.get("CreationToken")
        self.FsName = params.get("FsName")


class UpdateCfsFileSystemNameResponse(AbstractModel):
    """UpdateCfsFileSystemName返回参数结构体"""

    def __init__(self):
        """
        :param CreationToken: 用户自定义文件系统名称
        :type CreationToken: str
        :param FileSystemId: 文件系统ID
        :type FileSystemId: str
        :param FsName: 用户自定义文件系统名称
        :type FsName: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.CreationToken = None
        self.FileSystemId = None
        self.FsName = None
        self.RequestId = None

    def _deserialize(self, params):
        self.CreationToken = params.get("CreationToken")
        self.FileSystemId = params.get("FileSystemId")
        self.FsName = params.get("FsName")
        self.RequestId = params.get("RequestId")


class UpdateCfsFileSystemPGroupRequest(AbstractModel):
    """UpdateCfsFileSystemPGroup请求参数结构体"""

    def __init__(self):
        """
        :param PGroupId: 权限组ID
        :type PGroupId: str
        :param FileSystemId: 文件系统ID
        :type FileSystemId: str
        """
        self.PGroupId = None
        self.FileSystemId = None

    def _deserialize(self, params):
        self.PGroupId = params.get("PGroupId")
        self.FileSystemId = params.get("FileSystemId")


class UpdateCfsFileSystemPGroupResponse(AbstractModel):
    """UpdateCfsFileSystemPGroup返回参数结构体"""

    def __init__(self):
        """
        :param PGroupId: 权限组ID
        :type PGroupId: str
        :param FileSystemId: 文件系统ID
        :type FileSystemId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.PGroupId = None
        self.FileSystemId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.PGroupId = params.get("PGroupId")
        self.FileSystemId = params.get("FileSystemId")
        self.RequestId = params.get("RequestId")


class UpdateCfsFileSystemSizeLimitRequest(AbstractModel):
    """UpdateCfsFileSystemSizeLimit请求参数结构体"""

    def __init__(self):
        """
        :param FsLimit: 文件系统容量限制大小，输入范围1-1073741824, 单位为GB
        :type FsLimit: int
        :param FileSystemId: 文件系统ID
        :type FileSystemId: str
        """
        self.FsLimit = None
        self.FileSystemId = None

    def _deserialize(self, params):
        self.FsLimit = params.get("FsLimit")
        self.FileSystemId = params.get("FileSystemId")


class UpdateCfsFileSystemSizeLimitResponse(AbstractModel):
    """UpdateCfsFileSystemSizeLimit返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpdateCfsPGroupRequest(AbstractModel):
    """UpdateCfsPGroup请求参数结构体"""

    def __init__(self):
        """
        :param PGroupId: 权限组ID
        :type PGroupId: str
        :param Name: 权限组名称
        :type Name: str
        :param DescInfo: 描述信息
        :type DescInfo: str
        """
        self.PGroupId = None
        self.Name = None
        self.DescInfo = None

    def _deserialize(self, params):
        self.PGroupId = params.get("PGroupId")
        self.Name = params.get("Name")
        self.DescInfo = params.get("DescInfo")


class UpdateCfsPGroupResponse(AbstractModel):
    """UpdateCfsPGroup返回参数结构体"""

    def __init__(self):
        """
        :param PGroupId: 权限组ID
        :type PGroupId: str
        :param Name: 权限组名称
        :type Name: str
        :param DescInfo: 描述信息
        :type DescInfo: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.PGroupId = None
        self.Name = None
        self.DescInfo = None
        self.RequestId = None

    def _deserialize(self, params):
        self.PGroupId = params.get("PGroupId")
        self.Name = params.get("Name")
        self.DescInfo = params.get("DescInfo")
        self.RequestId = params.get("RequestId")


class UpdateCfsRuleRequest(AbstractModel):
    """UpdateCfsRule请求参数结构体"""

    def __init__(self):
        """
        :param PGroupId: 权限组ID
        :type PGroupId: str
        :param RuleId: 规则ID
        :type RuleId: str
        :param AuthClientIp: 允许访问的客户端IP地址或地址段
        :type AuthClientIp: str
        :param RWPermission: 读写权限, 可选参数：ro, rw。ro为只读，rw为读写
        :type RWPermission: str
        :param UserPermission: 用户权限，可选参数：all_squash，no_all_squash，root_squash，no_root_squash。
        其中all_squash为所有访问用户都会被映射为匿名用户或用户组；
        no_all_squash为访问用户会先与本机用户匹配，匹配失败后再映射为匿名用户或用户组；
        root_squash为将来访的root用户映射为匿名用户或用户组；no_root_squash为来访的root用户保持root帐号权限。
        :type UserPermission: str
        :param Priority: 规则优先级，参数范围1-100。 其中 1 为最高，100为最低
        :type Priority: int
        """
        self.PGroupId = None
        self.RuleId = None
        self.AuthClientIp = None
        self.RWPermission = None
        self.UserPermission = None
        self.Priority = None

    def _deserialize(self, params):
        self.PGroupId = params.get("PGroupId")
        self.RuleId = params.get("RuleId")
        self.AuthClientIp = params.get("AuthClientIp")
        self.RWPermission = params.get("RWPermission")
        self.UserPermission = params.get("UserPermission")
        self.Priority = params.get("Priority")


class UpdateCfsRuleResponse(AbstractModel):
    """UpdateCfsRule返回参数结构体"""

    def __init__(self):
        """
        :param PGroupId: 权限组ID
        :type PGroupId: str
        :param RuleId: 规则ID
        :type RuleId: str
        :param AuthClientIp: 允许访问的客户端IP
        :type AuthClientIp: str
        :param RWPermission: 读写权限
        :type RWPermission: str
        :param UserPermission: 用户权限
        :type UserPermission: str
        :param Priority: 优先级
        :type Priority: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.PGroupId = None
        self.RuleId = None
        self.AuthClientIp = None
        self.RWPermission = None
        self.UserPermission = None
        self.Priority = None
        self.RequestId = None

    def _deserialize(self, params):
        self.PGroupId = params.get("PGroupId")
        self.RuleId = params.get("RuleId")
        self.AuthClientIp = params.get("AuthClientIp")
        self.RWPermission = params.get("RWPermission")
        self.UserPermission = params.get("UserPermission")
        self.Priority = params.get("Priority")
        self.RequestId = params.get("RequestId")


class VersionCtrlProtoStatus(AbstractModel):
    """版本控制-协议详情"""

    def __init__(self):
        """
        :param SaleStatus: 售卖状态。可选值有“sale_out”：售罄、“saling”：可售、“no_saling”：不可销售
        :type SaleStatus: str
        :param Protocol: 协议类型。可选值有“NFS”、“CIFS”
        :type Protocol: str
        """
        self.SaleStatus = None
        self.Protocol = None

    def _deserialize(self, params):
        self.SaleStatus = params.get("SaleStatus")
        self.Protocol = params.get("Protocol")


class VersionCtrlRegion(AbstractModel):
    """版本控制-区域数组"""

    def __init__(self):
        """
        :param Region: 区域名称，如“ap-beijing”
        :type Region: str
        :param RegionName: 区域名称，如“bj”
        :type RegionName: str
        :param RegionStatus: 区域可用情况，当区域内至少有一个可用区处于可售状态时，取值为AVAILABLE，否则为UNAVAILABLE
        :type RegionStatus: str
        :param Zones: 可用区数组
        :type Zones: list of VersionCtrlZone
        """
        self.Region = None
        self.RegionName = None
        self.RegionStatus = None
        self.Zones = None

    def _deserialize(self, params):
        self.Region = params.get("Region")
        self.RegionName = params.get("RegionName")
        self.RegionStatus = params.get("RegionStatus")
        if params.get("Zones") is not None:
            self.Zones = []
            for item in params.get("Zones"):
                obj = VersionCtrlZone()
                obj._deserialize(item)
                self.Zones.append(obj)


class VersionCtrlType(AbstractModel):
    """版本控制-类型数组"""

    def __init__(self):
        """
        :param Protocols: 协议与售卖详情
        :type Protocols: list of VersionCtrlProtoStatus
        :param Type: 存储类型。可选值有”SD“：标准、“HP”：高性能、“IA”：低频
        :type Type: str
        """
        self.Protocols = None
        self.Type = None

    def _deserialize(self, params):
        if params.get("Protocols") is not None:
            self.Protocols = []
            for item in params.get("Protocols"):
                obj = VersionCtrlProtoStatus()
                obj._deserialize(item)
                self.Protocols.append(obj)
        self.Type = params.get("Type")


class VersionCtrlZone(AbstractModel):
    """版本控制-可用区数组"""

    def __init__(self):
        """
        :param Zone: 可用区名称
        :type Zone: str
        :param ZoneId: 可用区ID
        :type ZoneId: int
        :param ZoneCnName: 可用区中文名称
        :type ZoneCnName: str
        :param Types: Type数组
        :type Types: list of VersionCtrlType
        """
        self.Zone = None
        self.ZoneId = None
        self.ZoneCnName = None
        self.Types = None

    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.ZoneId = params.get("ZoneId")
        self.ZoneCnName = params.get("ZoneCnName")
        if params.get("Types") is not None:
            self.Types = []
            for item in params.get("Types"):
                obj = VersionCtrlType()
                obj._deserialize(item)
                self.Types.append(obj)

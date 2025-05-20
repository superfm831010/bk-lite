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


class AccessVpc(AbstractModel):
    """内网接入信息"""

    def __init__(self):
        """
        :param VpcId: Vpc的Id
        :type VpcId: str
        :param SubnetId: 子网Id
        :type SubnetId: str
        :param Status: 内网接入状态
        :type Status: str
        :param AccessIp: 内网接入Ip
        :type AccessIp: str
        """
        self.VpcId = None
        self.SubnetId = None
        self.Status = None
        self.AccessIp = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.Status = params.get("Status")
        self.AccessIp = params.get("AccessIp")


class AuthUser(AbstractModel):
    """构建用户信息"""

    def __init__(self):
        """
        :param Name: 用户名
        :type Name: str
        :param Email: 用户邮箱
        :type Email: str
        """
        self.Name = None
        self.Email = None

    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Email = params.get("Email")


class AuthUserInfoResp(AbstractModel):
    """构建用户的信息返回值"""

    def __init__(self):
        """
        :param User: 构建用户信息
        :type User: :class:`tcecloud.tcr.v20190924.models.AuthUser`
        """
        self.User = None

    def _deserialize(self, params):
        if params.get("User") is not None:
            self.User = AuthUser()
            self.User._deserialize(params.get("User"))


class AutoDelStrategyInfo(AbstractModel):
    """自动删除策略信息"""

    def __init__(self):
        """
        :param Username: 用户名
        :type Username: str
        :param RepoName: 仓库名
        :type RepoName: str
        :param Type: 类型
        :type Type: str
        :param Value: 策略值
        :type Value: int
        :param Valid: Valid
        :type Valid: int
        :param CreationTime: 创建时间
        :type CreationTime: str
        """
        self.Username = None
        self.RepoName = None
        self.Type = None
        self.Value = None
        self.Valid = None
        self.CreationTime = None

    def _deserialize(self, params):
        self.Username = params.get("Username")
        self.RepoName = params.get("RepoName")
        self.Type = params.get("Type")
        self.Value = params.get("Value")
        self.Valid = params.get("Valid")
        self.CreationTime = params.get("CreationTime")


class AutoDelStrategyInfoResp(AbstractModel):
    """获取自动删除策略"""

    def __init__(self):
        """
                :param TotalCount: 总数目
                :type TotalCount: int
                :param StrategyInfo: 自动删除策略列表
        注意：此字段可能返回 null，表示取不到有效值。
                :type StrategyInfo: list of AutoDelStrategyInfo
        """
        self.TotalCount = None
        self.StrategyInfo = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("StrategyInfo") is not None:
            self.StrategyInfo = []
            for item in params.get("StrategyInfo"):
                obj = AutoDelStrategyInfo()
                obj._deserialize(item)
                self.StrategyInfo.append(obj)


class BatchDeleteFavorRepositoryPersonalRequest(AbstractModel):
    """BatchDeleteFavorRepositoryPersonal请求参数结构体"""

    def __init__(self):
        """
        :param Favors: 收藏仓库的列表
        :type Favors: list of RequestFavor
        """
        self.Favors = None

    def _deserialize(self, params):
        if params.get("Favors") is not None:
            self.Favors = []
            for item in params.get("Favors"):
                obj = RequestFavor()
                obj._deserialize(item)
                self.Favors.append(obj)


class BatchDeleteFavorRepositoryPersonalResponse(AbstractModel):
    """BatchDeleteFavorRepositoryPersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class BatchDeleteImagePersonalRequest(AbstractModel):
    """BatchDeleteImagePersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 仓库名称
        :type RepoName: str
        :param Tags: Tag列表
        :type Tags: list of str
        """
        self.RepoName = None
        self.Tags = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")
        self.Tags = params.get("Tags")


class BatchDeleteImagePersonalResponse(AbstractModel):
    """BatchDeleteImagePersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class BatchDeleteRepositoryPersonalRequest(AbstractModel):
    """BatchDeleteRepositoryPersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoNames: 仓库名称数组
        :type RepoNames: list of str
        """
        self.RepoNames = None

    def _deserialize(self, params):
        self.RepoNames = params.get("RepoNames")


class BatchDeleteRepositoryPersonalResponse(AbstractModel):
    """BatchDeleteRepositoryPersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class BuildBranchResp(AbstractModel):
    """构建分支返回信息"""

    def __init__(self):
        """
        :param Branches: 构建的分支信息
        :type Branches: list of str
        """
        self.Branches = None

    def _deserialize(self, params):
        self.Branches = params.get("Branches")


class BuildHistoryResp(AbstractModel):
    """构建历史信息"""

    def __init__(self):
        """
        :param BuildHistory: 构建信息
        :type BuildHistory: :class:`tcecloud.tcr.v20190924.models.BuildInfo`
        """
        self.BuildHistory = None

    def _deserialize(self, params):
        if params.get("BuildHistory") is not None:
            self.BuildHistory = BuildInfo()
            self.BuildHistory._deserialize(params.get("BuildHistory"))


class BuildInfo(AbstractModel):
    """构建信息"""

    def __init__(self):
        """
                :param Id: Id
                :type Id: int
                :param AppId: AppId
                :type AppId: int
                :param BuildType: 构建类型
                :type BuildType: str
                :param BuildManually: 是否手动构建
                :type BuildManually: int
                :param BuildWorkDir: 构建工作目录
                :type BuildWorkDir: str
                :param Args: 构建参数
        注意：此字段可能返回 null，表示取不到有效值。
                :type Args: str
                :param Status: 构建状态
                :type Status: str
                :param StartTime: 构建开始时间
                :type StartTime: str
                :param EndTime: 构建结束时间
                :type EndTime: str
                :param GitServer: 构建仓库地址
                :type GitServer: str
                :param Group: repo所在的group
                :type Group: str
                :param Repo: 构建所在的repo
                :type Repo: str
                :param RepoUrl: Repo url地址
        注意：此字段可能返回 null，表示取不到有效值。
                :type RepoUrl: str
                :param Owner: 用户在git服务器上的用户名
                :type Owner: str
                :param Branch: 构建的分支
                :type Branch: str
                :param DockerfilePath: dockerfile在仓库中的路径
                :type DockerfilePath: str
                :param RegistryNamespace: registry中的namespace
                :type RegistryNamespace: str
                :param RegistryUsername: 用户在registry中的用户名
                :type RegistryUsername: str
                :param Image: 镜像名称，不包含tag
                :type Image: str
                :param ForceImage: 镜像名
                :type ForceImage: str
                :param CommitSHA: 提交的SHA
                :type CommitSHA: str
                :param CommitAuthor: 提交的作者
                :type CommitAuthor: str
                :param CommitMessage: 提交的信息
                :type CommitMessage: str
                :param CommitTime: 提交的时间
                :type CommitTime: str
                :param BuildLog: 构建日志
                :type BuildLog: str
        """
        self.Id = None
        self.AppId = None
        self.BuildType = None
        self.BuildManually = None
        self.BuildWorkDir = None
        self.Args = None
        self.Status = None
        self.StartTime = None
        self.EndTime = None
        self.GitServer = None
        self.Group = None
        self.Repo = None
        self.RepoUrl = None
        self.Owner = None
        self.Branch = None
        self.DockerfilePath = None
        self.RegistryNamespace = None
        self.RegistryUsername = None
        self.Image = None
        self.ForceImage = None
        self.CommitSHA = None
        self.CommitAuthor = None
        self.CommitMessage = None
        self.CommitTime = None
        self.BuildLog = None

    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.AppId = params.get("AppId")
        self.BuildType = params.get("BuildType")
        self.BuildManually = params.get("BuildManually")
        self.BuildWorkDir = params.get("BuildWorkDir")
        self.Args = params.get("Args")
        self.Status = params.get("Status")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.GitServer = params.get("GitServer")
        self.Group = params.get("Group")
        self.Repo = params.get("Repo")
        self.RepoUrl = params.get("RepoUrl")
        self.Owner = params.get("Owner")
        self.Branch = params.get("Branch")
        self.DockerfilePath = params.get("DockerfilePath")
        self.RegistryNamespace = params.get("RegistryNamespace")
        self.RegistryUsername = params.get("RegistryUsername")
        self.Image = params.get("Image")
        self.ForceImage = params.get("ForceImage")
        self.CommitSHA = params.get("CommitSHA")
        self.CommitAuthor = params.get("CommitAuthor")
        self.CommitMessage = params.get("CommitMessage")
        self.CommitTime = params.get("CommitTime")
        self.BuildLog = params.get("BuildLog")


class BuildInfoResp(AbstractModel):
    """构建信息的返回信息"""

    def __init__(self):
        """
        :param TotalCount: 总数
        :type TotalCount: int
        :param BuildList: 构建信息列表
        :type BuildList: list of BuildInfo
        """
        self.TotalCount = None
        self.BuildList = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("BuildList") is not None:
            self.BuildList = []
            for item in params.get("BuildList"):
                obj = BuildInfo()
                obj._deserialize(item)
                self.BuildList.append(obj)


class BuildRepo(AbstractModel):
    """源代码仓库信息"""

    def __init__(self):
        """
                :param GitServer: 源码所在的git服务
                :type GitServer: str
                :param Group: repo所在的group
                :type Group: str
                :param RepoName: 源码在git服务器上的仓库名
                :type RepoName: str
                :param RepoId: 仓库Id
                :type RepoId: int
                :param Desc: 仓库描述
        注意：此字段可能返回 null，表示取不到有效值。
                :type Desc: str
                :param Private: 是否为私有
        注意：此字段可能返回 null，表示取不到有效值。
                :type Private: bool
                :param WebUrl: WebUrl
        注意：此字段可能返回 null，表示取不到有效值。
                :type WebUrl: str
        """
        self.GitServer = None
        self.Group = None
        self.RepoName = None
        self.RepoId = None
        self.Desc = None
        self.Private = None
        self.WebUrl = None

    def _deserialize(self, params):
        self.GitServer = params.get("GitServer")
        self.Group = params.get("Group")
        self.RepoName = params.get("RepoName")
        self.RepoId = params.get("RepoId")
        self.Desc = params.get("Desc")
        self.Private = params.get("Private")
        self.WebUrl = params.get("WebUrl")


class BuildReposList(AbstractModel):
    """构建仓库列表信息"""

    def __init__(self):
        """
        :param Repos: 仓库信息列表
        :type Repos: list of BuildRepo
        """
        self.Repos = None

    def _deserialize(self, params):
        if params.get("Repos") is not None:
            self.Repos = []
            for item in params.get("Repos"):
                obj = BuildRepo()
                obj._deserialize(item)
                self.Repos.append(obj)


class BuildRule(AbstractModel):
    """构建规则"""

    def __init__(self):
        """
                :param RegistryNamespace: registry中的namespace
                :type RegistryNamespace: str
                :param RegistryUsername: 用户在registry中的用户名
                :type RegistryUsername: str
                :param ImageName: 镜像名称，不包含tag
                :type ImageName: str
                :param ImageTagFormat: 镜像tag的格式
                :type ImageTagFormat: str
                :param GitServer: 源码所在的git服务
                :type GitServer: str
                :param Group: repo所在的group
                :type Group: str
                :param Repo: 源码在git服务器上的仓库名
                :type Repo: str
                :param Owner: 用户在git服务器上的用户名
                :type Owner: str
                :param Branches: 分支
        注意：此字段可能返回 null，表示取不到有效值。
                :type Branches: list of str
                :param Tag: Tag
        注意：此字段可能返回 null，表示取不到有效值。
                :type Tag: int
                :param DockerfilePath: dockerfile在仓库中的路径
        注意：此字段可能返回 null，表示取不到有效值。
                :type DockerfilePath: str
                :param BuildWorkDir: 工作目录
        注意：此字段可能返回 null，表示取不到有效值。
                :type BuildWorkDir: str
                :param ForceTag: 构建出的镜像覆盖该Tag
        注意：此字段可能返回 null，表示取不到有效值。
                :type ForceTag: str
                :param BuildArgs: Args
        注意：此字段可能返回 null，表示取不到有效值。
                :type BuildArgs: str
        """
        self.RegistryNamespace = None
        self.RegistryUsername = None
        self.ImageName = None
        self.ImageTagFormat = None
        self.GitServer = None
        self.Group = None
        self.Repo = None
        self.Owner = None
        self.Branches = None
        self.Tag = None
        self.DockerfilePath = None
        self.BuildWorkDir = None
        self.ForceTag = None
        self.BuildArgs = None

    def _deserialize(self, params):
        self.RegistryNamespace = params.get("RegistryNamespace")
        self.RegistryUsername = params.get("RegistryUsername")
        self.ImageName = params.get("ImageName")
        self.ImageTagFormat = params.get("ImageTagFormat")
        self.GitServer = params.get("GitServer")
        self.Group = params.get("Group")
        self.Repo = params.get("Repo")
        self.Owner = params.get("Owner")
        self.Branches = params.get("Branches")
        self.Tag = params.get("Tag")
        self.DockerfilePath = params.get("DockerfilePath")
        self.BuildWorkDir = params.get("BuildWorkDir")
        self.ForceTag = params.get("ForceTag")
        self.BuildArgs = params.get("BuildArgs")


class BuildRuleResp(AbstractModel):
    """Build的信息返回值"""

    def __init__(self):
        """
        :param BuildRule: BuildRule信息
        :type BuildRule: :class:`tcecloud.tcr.v20190924.models.BuildRule`
        """
        self.BuildRule = None

    def _deserialize(self, params):
        if params.get("BuildRule") is not None:
            self.BuildRule = BuildRule()
            self.BuildRule._deserialize(params.get("BuildRule"))


class CreateApplicationTokenPersonalRequest(AbstractModel):
    """CreateApplicationTokenPersonal请求参数结构体"""


class CreateApplicationTokenPersonalResponse(AbstractModel):
    """CreateApplicationTokenPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 创建第三方应用访问凭证执行结果
        :type Data: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Data = params.get("Data")
        self.RequestId = params.get("RequestId")


class CreateApplicationTriggerPersonalRequest(AbstractModel):
    """CreateApplicationTriggerPersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 触发器关联的镜像仓库，library/test格式
        :type RepoName: str
        :param TriggerName: 触发器名称
        :type TriggerName: str
        :param InvokeMethod: 触发方式，"all"全部触发，"taglist"指定tag触发，"regex"正则触发
        :type InvokeMethod: str
        :param ClusterId: 应用所在TKE集群ID
        :type ClusterId: str
        :param Namespace: 应用所在TKE集群命名空间
        :type Namespace: str
        :param WorkloadType: 应用所在TKE集群工作负载类型,支持Deployment、StatefulSet、DaemonSet、CronJob、Job。
        :type WorkloadType: str
        :param WorkloadName: 应用所在TKE集群工作负载名称
        :type WorkloadName: str
        :param ContainerName: 应用所在TKE集群工作负载下容器名称
        :type ContainerName: str
        :param ClusterRegion: 应用所在TKE集群地域
        :type ClusterRegion: int
        :param InvokeExpr: 触发方式对应的表达式
        :type InvokeExpr: str
        """
        self.RepoName = None
        self.TriggerName = None
        self.InvokeMethod = None
        self.ClusterId = None
        self.Namespace = None
        self.WorkloadType = None
        self.WorkloadName = None
        self.ContainerName = None
        self.ClusterRegion = None
        self.InvokeExpr = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")
        self.TriggerName = params.get("TriggerName")
        self.InvokeMethod = params.get("InvokeMethod")
        self.ClusterId = params.get("ClusterId")
        self.Namespace = params.get("Namespace")
        self.WorkloadType = params.get("WorkloadType")
        self.WorkloadName = params.get("WorkloadName")
        self.ContainerName = params.get("ContainerName")
        self.ClusterRegion = params.get("ClusterRegion")
        self.InvokeExpr = params.get("InvokeExpr")


class CreateApplicationTriggerPersonalResponse(AbstractModel):
    """CreateApplicationTriggerPersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateFavorRepositoryPersonalRequest(AbstractModel):
    """CreateFavorRepositoryPersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 仓库的名称
        :type RepoName: str
        :param RepoType: 仓库的类型
        :type RepoType: str
        """
        self.RepoName = None
        self.RepoType = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")
        self.RepoType = params.get("RepoType")


class CreateFavorRepositoryPersonalResponse(AbstractModel):
    """CreateFavorRepositoryPersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateImageBuildPersonalRequest(AbstractModel):
    """CreateImageBuildPersonal请求参数结构体"""

    def __init__(self):
        """
        :param RegistryNamespace: registry中的namespace
        :type RegistryNamespace: str
        :param RegistryUsername: 用户在registry中的用户名
        :type RegistryUsername: str
        :param ImageName: 镜像名称，不包含tag
        :type ImageName: str
        :param ImageTagFormat: 镜像tag的格式
        :type ImageTagFormat: str
        :param GitServer: 源码所在的git服务
        :type GitServer: str
        :param Group: repo所在的group
        :type Group: str
        :param Repo: 源码在git服务器上的仓库名
        :type Repo: str
        :param Owner: 用户在git服务器上的用户名
        :type Owner: str
        :param Trigger: Trigger信息
        :type Trigger: :class:`tcecloud.tcr.v20190924.models.Trigger`
        :param DockerfilePath: dockerfile在仓库中的路径
        :type DockerfilePath: str
        :param WorkDir: 工作目录
        :type WorkDir: str
        :param ForceTag: 构建出的镜像覆盖该Tag
        :type ForceTag: str
        :param Args: Args
        :type Args: list of str
        """
        self.RegistryNamespace = None
        self.RegistryUsername = None
        self.ImageName = None
        self.ImageTagFormat = None
        self.GitServer = None
        self.Group = None
        self.Repo = None
        self.Owner = None
        self.Trigger = None
        self.DockerfilePath = None
        self.WorkDir = None
        self.ForceTag = None
        self.Args = None

    def _deserialize(self, params):
        self.RegistryNamespace = params.get("RegistryNamespace")
        self.RegistryUsername = params.get("RegistryUsername")
        self.ImageName = params.get("ImageName")
        self.ImageTagFormat = params.get("ImageTagFormat")
        self.GitServer = params.get("GitServer")
        self.Group = params.get("Group")
        self.Repo = params.get("Repo")
        self.Owner = params.get("Owner")
        if params.get("Trigger") is not None:
            self.Trigger = Trigger()
            self.Trigger._deserialize(params.get("Trigger"))
        self.DockerfilePath = params.get("DockerfilePath")
        self.WorkDir = params.get("WorkDir")
        self.ForceTag = params.get("ForceTag")
        self.Args = params.get("Args")


class CreateImageBuildPersonalResponse(AbstractModel):
    """CreateImageBuildPersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateImageBuildTaskDockerPersonalRequest(AbstractModel):
    """CreateImageBuildTaskDockerPersonal请求参数结构体"""

    def __init__(self):
        """
        :param Dockerfile: dockerfile在仓库中的路径
        :type Dockerfile: str
        :param RegistryUserName: 用户在registry中的用户名
        :type RegistryUserName: str
        :param RegistryNamespace: registry中的namespace
        :type RegistryNamespace: str
        :param Image: 镜像名称
        :type Image: str
        """
        self.Dockerfile = None
        self.RegistryUserName = None
        self.RegistryNamespace = None
        self.Image = None

    def _deserialize(self, params):
        self.Dockerfile = params.get("Dockerfile")
        self.RegistryUserName = params.get("RegistryUserName")
        self.RegistryNamespace = params.get("RegistryNamespace")
        self.Image = params.get("Image")


class CreateImageBuildTaskDockerPersonalResponse(AbstractModel):
    """CreateImageBuildTaskDockerPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 构建Id
        :type Data: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Data = params.get("Data")
        self.RequestId = params.get("RequestId")


class CreateImageBuildTaskManuallyPersonalRequest(AbstractModel):
    """CreateImageBuildTaskManuallyPersonal请求参数结构体"""

    def __init__(self):
        """
        :param RegistryNamespace: registry所在的namespace
        :type RegistryNamespace: str
        :param ImageName: 镜像名称
        :type ImageName: str
        :param TagFormat: Tag的格式
        :type TagFormat: str
        :param Type: 仓库类型
        :type Type: str
        :param BranchOrCommit: 仓库分支或者是commit
        :type BranchOrCommit: str
        """
        self.RegistryNamespace = None
        self.ImageName = None
        self.TagFormat = None
        self.Type = None
        self.BranchOrCommit = None

    def _deserialize(self, params):
        self.RegistryNamespace = params.get("RegistryNamespace")
        self.ImageName = params.get("ImageName")
        self.TagFormat = params.get("TagFormat")
        self.Type = params.get("Type")
        self.BranchOrCommit = params.get("BranchOrCommit")


class CreateImageBuildTaskManuallyPersonalResponse(AbstractModel):
    """CreateImageBuildTaskManuallyPersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateImageLifecyclePersonalRequest(AbstractModel):
    """CreateImageLifecyclePersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 仓库名称
        :type RepoName: str
        :param Type: keep_last_days:保留最近几天的数据;keep_last_nums:保留最近多少个
        :type Type: str
        :param Val: 策略值
        :type Val: int
        """
        self.RepoName = None
        self.Type = None
        self.Val = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")
        self.Type = params.get("Type")
        self.Val = params.get("Val")


class CreateImageLifecyclePersonalResponse(AbstractModel):
    """CreateImageLifecyclePersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateInstanceRequest(AbstractModel):
    """CreateInstance请求参数结构体"""

    def __init__(self):
        """
        :param RegistryName: 企业版实例名称
        :type RegistryName: str
        :param RegistryType: 企业版实例类型
        :type RegistryType: str
        """
        self.RegistryName = None
        self.RegistryType = None

    def _deserialize(self, params):
        self.RegistryName = params.get("RegistryName")
        self.RegistryType = params.get("RegistryType")


class CreateInstanceResponse(AbstractModel):
    """CreateInstance返回参数结构体"""

    def __init__(self):
        """
        :param RegistryId: 企业版实例Id
        :type RegistryId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RegistryId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.RegistryId = params.get("RegistryId")
        self.RequestId = params.get("RequestId")


class CreateInstanceTokenRequest(AbstractModel):
    """CreateInstanceToken请求参数结构体"""

    def __init__(self):
        """
        :param RegistryId: 实例Id
        :type RegistryId: str
        """
        self.RegistryId = None

    def _deserialize(self, params):
        self.RegistryId = params.get("RegistryId")


class CreateInstanceTokenResponse(AbstractModel):
    """CreateInstanceToken返回参数结构体"""

    def __init__(self):
        """
        :param Token: 临时密码
        :type Token: str
        :param ExpTime: 临时密码有效期时间戳
        :type ExpTime: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Token = None
        self.ExpTime = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Token = params.get("Token")
        self.ExpTime = params.get("ExpTime")
        self.RequestId = params.get("RequestId")


class CreateNamespacePersonalRequest(AbstractModel):
    """CreateNamespacePersonal请求参数结构体"""

    def __init__(self):
        """
        :param Namespace: 命名空间名称
        :type Namespace: str
        """
        self.Namespace = None

    def _deserialize(self, params):
        self.Namespace = params.get("Namespace")


class CreateNamespacePersonalResponse(AbstractModel):
    """CreateNamespacePersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateRepoRequest(AbstractModel):
    """CreateRepo请求参数结构体"""

    def __init__(self):
        """
        :param Reponame: 仓库名称
        :type Reponame: str
        :param Public: 是否公共,1:公共,0:私有
        :type Public: int
        :param Description: 仓库描述
        :type Description: str
        """
        self.Reponame = None
        self.Public = None
        self.Description = None

    def _deserialize(self, params):
        self.Reponame = params.get("Reponame")
        self.Public = params.get("Public")
        self.Description = params.get("Description")


class CreateRepoResponse(AbstractModel):
    """CreateRepo返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateRepositoryPersonalRequest(AbstractModel):
    """CreateRepositoryPersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 仓库名称
        :type RepoName: str
        :param Public: 是否公共,1:公共,0:私有
        :type Public: int
        :param Description: 仓库描述
        :type Description: str
        """
        self.RepoName = None
        self.Public = None
        self.Description = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")
        self.Public = params.get("Public")
        self.Description = params.get("Description")


class CreateRepositoryPersonalResponse(AbstractModel):
    """CreateRepositoryPersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateSecurityPoliciesRequest(AbstractModel):
    """CreateSecurityPolicies请求参数结构体"""

    def __init__(self):
        """
        :param RegistryId: 实例Id
        :type RegistryId: str
        :param CidrBlock: 192.168.0.0/24
        :type CidrBlock: str
        :param Description: 描述
        :type Description: str
        """
        self.RegistryId = None
        self.CidrBlock = None
        self.Description = None

    def _deserialize(self, params):
        self.RegistryId = params.get("RegistryId")
        self.CidrBlock = params.get("CidrBlock")
        self.Description = params.get("Description")


class CreateSecurityPoliciesResponse(AbstractModel):
    """CreateSecurityPolicies返回参数结构体"""

    def __init__(self):
        """
        :param RegistryId: 实例Id
        :type RegistryId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RegistryId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.RegistryId = params.get("RegistryId")
        self.RequestId = params.get("RequestId")


class CreateSecurityPolicyRequest(AbstractModel):
    """CreateSecurityPolicy请求参数结构体"""

    def __init__(self):
        """
        :param RegistryId: 实例Id
        :type RegistryId: str
        :param CidrBlock: 192.168.0.0/24
        :type CidrBlock: str
        :param Description: 备注
        :type Description: str
        """
        self.RegistryId = None
        self.CidrBlock = None
        self.Description = None

    def _deserialize(self, params):
        self.RegistryId = params.get("RegistryId")
        self.CidrBlock = params.get("CidrBlock")
        self.Description = params.get("Description")


class CreateSecurityPolicyResponse(AbstractModel):
    """CreateSecurityPolicy返回参数结构体"""

    def __init__(self):
        """
        :param RegistryId: 实例Id
        :type RegistryId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RegistryId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.RegistryId = params.get("RegistryId")
        self.RequestId = params.get("RequestId")


class CreateSourceCodeAuthPersonalRequest(AbstractModel):
    """CreateSourceCodeAuthPersonal请求参数结构体"""

    def __init__(self):
        """
        :param GitServer: GitServer地址
        :type GitServer: str
        :param Owner: 用户信息
        :type Owner: str
        :param GitToken: git 秘钥
        :type GitToken: str
        """
        self.GitServer = None
        self.Owner = None
        self.GitToken = None

    def _deserialize(self, params):
        self.GitServer = params.get("GitServer")
        self.Owner = params.get("Owner")
        self.GitToken = params.get("GitToken")


class CreateSourceCodeAuthPersonalResponse(AbstractModel):
    """CreateSourceCodeAuthPersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateUserPersonalRequest(AbstractModel):
    """CreateUserPersonal请求参数结构体"""

    def __init__(self):
        """
        :param Password: 用户密码
        :type Password: str
        """
        self.Password = None

    def _deserialize(self, params):
        self.Password = params.get("Password")


class CreateUserPersonalResponse(AbstractModel):
    """CreateUserPersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteApplicationTriggerPersonalRequest(AbstractModel):
    """DeleteApplicationTriggerPersonal请求参数结构体"""

    def __init__(self):
        """
        :param TriggerName: 触发器名称
        :type TriggerName: str
        """
        self.TriggerName = None

    def _deserialize(self, params):
        self.TriggerName = params.get("TriggerName")


class DeleteApplicationTriggerPersonalResponse(AbstractModel):
    """DeleteApplicationTriggerPersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteFavorRepositoryPersonalRequest(AbstractModel):
    """DeleteFavorRepositoryPersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 仓库名称
        :type RepoName: str
        :param RepoType: 仓库类型
        :type RepoType: str
        """
        self.RepoName = None
        self.RepoType = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")
        self.RepoType = params.get("RepoType")


class DeleteFavorRepositoryPersonalResponse(AbstractModel):
    """DeleteFavorRepositoryPersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteFavorRepositoryRegionPersonalRequest(AbstractModel):
    """DeleteFavorRepositoryRegionPersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 被收藏的仓库名称
        :type RepoName: str
        """
        self.RepoName = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")


class DeleteFavorRepositoryRegionPersonalResponse(AbstractModel):
    """DeleteFavorRepositoryRegionPersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteImageBuildPersonalRequest(AbstractModel):
    """DeleteImageBuildPersonal请求参数结构体"""

    def __init__(self):
        """
        :param Images: 镜像列表
        :type Images: list of str
        """
        self.Images = None

    def _deserialize(self, params):
        self.Images = params.get("Images")


class DeleteImageBuildPersonalResponse(AbstractModel):
    """DeleteImageBuildPersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteImageBuildTaskPersonalRequest(AbstractModel):
    """DeleteImageBuildTaskPersonal请求参数结构体"""

    def __init__(self):
        """
        :param BuildId: 构建任务ID
        :type BuildId: int
        """
        self.BuildId = None

    def _deserialize(self, params):
        self.BuildId = params.get("BuildId")


class DeleteImageBuildTaskPersonalResponse(AbstractModel):
    """DeleteImageBuildTaskPersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteImageLifecycleGlobalPersonalRequest(AbstractModel):
    """DeleteImageLifecycleGlobalPersonal请求参数结构体"""


class DeleteImageLifecycleGlobalPersonalResponse(AbstractModel):
    """DeleteImageLifecycleGlobalPersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteImageLifecyclePersonalRequest(AbstractModel):
    """DeleteImageLifecyclePersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 仓库名称
        :type RepoName: str
        """
        self.RepoName = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")


class DeleteImageLifecyclePersonalResponse(AbstractModel):
    """DeleteImageLifecyclePersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteImagePersonalRequest(AbstractModel):
    """DeleteImagePersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 仓库名称
        :type RepoName: str
        :param Tag: Tag名
        :type Tag: str
        """
        self.RepoName = None
        self.Tag = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")
        self.Tag = params.get("Tag")


class DeleteImagePersonalResponse(AbstractModel):
    """DeleteImagePersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteInstanceRequest(AbstractModel):
    """DeleteInstance请求参数结构体"""

    def __init__(self):
        """
        :param RegistryId: 实例id
        :type RegistryId: str
        """
        self.RegistryId = None

    def _deserialize(self, params):
        self.RegistryId = params.get("RegistryId")


class DeleteInstanceResponse(AbstractModel):
    """DeleteInstance返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteNamespacePersonalRequest(AbstractModel):
    """DeleteNamespacePersonal请求参数结构体"""

    def __init__(self):
        """
        :param Namespace: 命名空间名称
        :type Namespace: str
        """
        self.Namespace = None

    def _deserialize(self, params):
        self.Namespace = params.get("Namespace")


class DeleteNamespacePersonalResponse(AbstractModel):
    """DeleteNamespacePersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteRepositoryPersonalRequest(AbstractModel):
    """DeleteRepositoryPersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 仓库名称
        :type RepoName: str
        """
        self.RepoName = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")


class DeleteRepositoryPersonalResponse(AbstractModel):
    """DeleteRepositoryPersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteSecurityPolicyRequest(AbstractModel):
    """DeleteSecurityPolicy请求参数结构体"""

    def __init__(self):
        """
        :param RegistryId: 实例Id
        :type RegistryId: str
        :param PolicyIndex: 白名单Id
        :type PolicyIndex: int
        :param PolicyVersion: 白名单版本
        :type PolicyVersion: str
        """
        self.RegistryId = None
        self.PolicyIndex = None
        self.PolicyVersion = None

    def _deserialize(self, params):
        self.RegistryId = params.get("RegistryId")
        self.PolicyIndex = params.get("PolicyIndex")
        self.PolicyVersion = params.get("PolicyVersion")


class DeleteSecurityPolicyResponse(AbstractModel):
    """DeleteSecurityPolicy返回参数结构体"""

    def __init__(self):
        """
        :param RegistryId: 实例Id
        :type RegistryId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RegistryId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.RegistryId = params.get("RegistryId")
        self.RequestId = params.get("RequestId")


class DeleteSourceCodeAuthPersonalRequest(AbstractModel):
    """DeleteSourceCodeAuthPersonal请求参数结构体"""

    def __init__(self):
        """
        :param GitServer: Server 地址（GitHub或者GitLab）
        :type GitServer: str
        """
        self.GitServer = None

    def _deserialize(self, params):
        self.GitServer = params.get("GitServer")


class DeleteSourceCodeAuthPersonalResponse(AbstractModel):
    """DeleteSourceCodeAuthPersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DesGitAuthRsp(AbstractModel):
    """查询GitAuth返回值"""

    def __init__(self):
        """
        :param AuthMap: 用户GitAuth信息
        :type AuthMap: str
        """
        self.AuthMap = None

    def _deserialize(self, params):
        self.AuthMap = params.get("AuthMap")


class DescribeApplicationTokenPersonalRequest(AbstractModel):
    """DescribeApplicationTokenPersonal请求参数结构体"""


class DescribeApplicationTokenPersonalResp(AbstractModel):
    """镜像仓库凭证"""

    def __init__(self):
        """
        :param ApplicationToken: 镜像仓库凭证
        :type ApplicationToken: str
        """
        self.ApplicationToken = None

    def _deserialize(self, params):
        self.ApplicationToken = params.get("ApplicationToken")


class DescribeApplicationTokenPersonalResponse(AbstractModel):
    """DescribeApplicationTokenPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 获取镜像仓库个人版凭证
        :type Data: :class:`tcecloud.tcr.v20190924.models.DescribeApplicationTokenPersonalResp`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = DescribeApplicationTokenPersonalResp()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeApplicationTriggerLogPersonalRequest(AbstractModel):
    """DescribeApplicationTriggerLogPersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 仓库名称
        :type RepoName: str
        :param Offset: 偏移量，默认为0
        :type Offset: int
        :param Limit: 返回最大数量，默认 20, 最大值 100
        :type Limit: int
        :param Order: 升序或降序
        :type Order: str
        :param OrderBy: 按某列排序
        :type OrderBy: str
        """
        self.RepoName = None
        self.Offset = None
        self.Limit = None
        self.Order = None
        self.OrderBy = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.Order = params.get("Order")
        self.OrderBy = params.get("OrderBy")


class DescribeApplicationTriggerLogPersonalResp(AbstractModel):
    """查询应用更新触发器触发日志返回值"""

    def __init__(self):
        """
                :param TotalCount: 返回总数
                :type TotalCount: int
                :param LogInfo: 触发日志列表
        注意：此字段可能返回 null，表示取不到有效值。
                :type LogInfo: list of TriggerLogResp
        """
        self.TotalCount = None
        self.LogInfo = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("LogInfo") is not None:
            self.LogInfo = []
            for item in params.get("LogInfo"):
                obj = TriggerLogResp()
                obj._deserialize(item)
                self.LogInfo.append(obj)


class DescribeApplicationTriggerLogPersonalResponse(AbstractModel):
    """DescribeApplicationTriggerLogPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 触发日志返回值
        :type Data: :class:`tcecloud.tcr.v20190924.models.DescribeApplicationTriggerLogPersonalResp`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = DescribeApplicationTriggerLogPersonalResp()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeApplicationTriggerPersonalRequest(AbstractModel):
    """DescribeApplicationTriggerPersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 仓库名称
        :type RepoName: str
        :param TriggerName: 触发器名称
        :type TriggerName: str
        :param Offset: 偏移量，默认为0
        :type Offset: int
        :param Limit: 返回最大数量，默认 20, 最大值 100
        :type Limit: int
        """
        self.RepoName = None
        self.TriggerName = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")
        self.TriggerName = params.get("TriggerName")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeApplicationTriggerPersonalResp(AbstractModel):
    """拉取触发器列表返回值"""

    def __init__(self):
        """
        :param TotalCount: 返回条目总数
        :type TotalCount: int
        :param TriggerInfo: 触发器列表
        :type TriggerInfo: list of TriggerResp
        """
        self.TotalCount = None
        self.TriggerInfo = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("TriggerInfo") is not None:
            self.TriggerInfo = []
            for item in params.get("TriggerInfo"):
                obj = TriggerResp()
                obj._deserialize(item)
                self.TriggerInfo.append(obj)


class DescribeApplicationTriggerPersonalResponse(AbstractModel):
    """DescribeApplicationTriggerPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 触发器列表返回值
        :type Data: :class:`tcecloud.tcr.v20190924.models.DescribeApplicationTriggerPersonalResp`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = DescribeApplicationTriggerPersonalResp()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeDockerHubImagePersonalRequest(AbstractModel):
    """DescribeDockerHubImagePersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 仓库名称
        :type RepoName: str
        """
        self.RepoName = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")


class DescribeDockerHubImagePersonalResponse(AbstractModel):
    """DescribeDockerHubImagePersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 查询dockerhub仓库镜像列表的返回值
        :type Data: :class:`tcecloud.tcr.v20190924.models.DockerHubTagList`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = DockerHubTagList()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeDockerHubRepositoryInfoPersonalRequest(AbstractModel):
    """DescribeDockerHubRepositoryInfoPersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 仓库名称
        :type RepoName: str
        """
        self.RepoName = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")


class DescribeDockerHubRepositoryInfoPersonalResponse(AbstractModel):
    """DescribeDockerHubRepositoryInfoPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: DockerHub仓库信息
        :type Data: :class:`tcecloud.tcr.v20190924.models.DockerHubRepoinfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = DockerHubRepoinfo()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeDockerHubRepositoryPersonalRequest(AbstractModel):
    """DescribeDockerHubRepositoryPersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 仓库名称
        :type RepoName: str
        :param Limit: Limit用于分页
        :type Limit: int
        :param Offset: 偏移量用于分页
        :type Offset: int
        """
        self.RepoName = None
        self.Limit = None
        self.Offset = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")


class DescribeDockerHubRepositoryPersonalResponse(AbstractModel):
    """DescribeDockerHubRepositoryPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: dockerhub仓库列表
        :type Data: :class:`tcecloud.tcr.v20190924.models.RespDockerHubRepoList`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = RespDockerHubRepoList()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeExternalEndpointStatusRequest(AbstractModel):
    """DescribeExternalEndpointStatus请求参数结构体"""

    def __init__(self):
        """
        :param RegistryId: 实例Id
        :type RegistryId: str
        """
        self.RegistryId = None

    def _deserialize(self, params):
        self.RegistryId = params.get("RegistryId")


class DescribeExternalEndpointStatusResponse(AbstractModel):
    """DescribeExternalEndpointStatus返回参数结构体"""

    def __init__(self):
        """
        :param Status: 开启公网访问状态，包括开启中，开启成功以及关闭和更新失败等
        :type Status: str
        :param Reason: 原因
        :type Reason: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Status = None
        self.Reason = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.Reason = params.get("Reason")
        self.RequestId = params.get("RequestId")


class DescribeFavorRepositoryPersonalRequest(AbstractModel):
    """DescribeFavorRepositoryPersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 仓库名称
        :type RepoName: str
        :param Limit: 分页Limit
        :type Limit: int
        :param Offset: Offset用于分页
        :type Offset: int
        """
        self.RepoName = None
        self.Limit = None
        self.Offset = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")


class DescribeFavorRepositoryPersonalResponse(AbstractModel):
    """DescribeFavorRepositoryPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 个人收藏仓库列表返回信息
        :type Data: :class:`tcecloud.tcr.v20190924.models.FavorResp`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = FavorResp()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeImageBuildPersonalRequest(AbstractModel):
    """DescribeImageBuildPersonal请求参数结构体"""

    def __init__(self):
        """
        :param RegistryNamespace: registry中的namespace
        :type RegistryNamespace: str
        :param Image: Image名称
        :type Image: str
        """
        self.RegistryNamespace = None
        self.Image = None

    def _deserialize(self, params):
        self.RegistryNamespace = params.get("RegistryNamespace")
        self.Image = params.get("Image")


class DescribeImageBuildPersonalResponse(AbstractModel):
    """DescribeImageBuildPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: BuildRule信息返回值
        :type Data: :class:`tcecloud.tcr.v20190924.models.BuildRuleResp`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = BuildRuleResp()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeImageBuildTaskLogInfoPersonalRequest(AbstractModel):
    """DescribeImageBuildTaskLogInfoPersonal请求参数结构体"""

    def __init__(self):
        """
        :param BuildId: 构建日志ID
        :type BuildId: int
        """
        self.BuildId = None

    def _deserialize(self, params):
        self.BuildId = params.get("BuildId")


class DescribeImageBuildTaskLogInfoPersonalResponse(AbstractModel):
    """DescribeImageBuildTaskLogInfoPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 构建历史信息
        :type Data: :class:`tcecloud.tcr.v20190924.models.BuildHistoryResp`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = BuildHistoryResp()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeImageBuildTaskLogPersonalRequest(AbstractModel):
    """DescribeImageBuildTaskLogPersonal请求参数结构体"""

    def __init__(self):
        """
        :param ImageName: 镜像名称
        :type ImageName: str
        :param RegistryNamespace: registry在仓库中的namespace
        :type RegistryNamespace: str
        :param Offset: Offset用于分页
        :type Offset: int
        :param Limit: Limit用于分页
        :type Limit: int
        """
        self.ImageName = None
        self.RegistryNamespace = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.ImageName = params.get("ImageName")
        self.RegistryNamespace = params.get("RegistryNamespace")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeImageBuildTaskLogPersonalResponse(AbstractModel):
    """DescribeImageBuildTaskLogPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 构建日志
        :type Data: :class:`tcecloud.tcr.v20190924.models.BuildInfoResp`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = BuildInfoResp()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeImageConfigPersonalRequest(AbstractModel):
    """DescribeImageConfigPersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 仓库名称
        :type RepoName: str
        :param Tag: Tag名称
        :type Tag: str
        """
        self.RepoName = None
        self.Tag = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")
        self.Tag = params.get("Tag")


class DescribeImageConfigPersonalResponse(AbstractModel):
    """DescribeImageConfigPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: payload
        :type Data: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Data = params.get("Data")
        self.RequestId = params.get("RequestId")


class DescribeImageFilterPersonalRequest(AbstractModel):
    """DescribeImageFilterPersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 仓库名称
        :type RepoName: str
        :param Tag: Tag名
        :type Tag: str
        """
        self.RepoName = None
        self.Tag = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")
        self.Tag = params.get("Tag")


class DescribeImageFilterPersonalResponse(AbstractModel):
    """DescribeImageFilterPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: payload
        :type Data: :class:`tcecloud.tcr.v20190924.models.SameImagesResp`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = SameImagesResp()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeImageLifecycleGlobalPersonalRequest(AbstractModel):
    """DescribeImageLifecycleGlobalPersonal请求参数结构体"""


class DescribeImageLifecycleGlobalPersonalResponse(AbstractModel):
    """DescribeImageLifecycleGlobalPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 全局自动删除策略信息
        :type Data: :class:`tcecloud.tcr.v20190924.models.AutoDelStrategyInfoResp`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = AutoDelStrategyInfoResp()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeImageLifecyclePersonalRequest(AbstractModel):
    """DescribeImageLifecyclePersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 仓库名称
        :type RepoName: str
        """
        self.RepoName = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")


class DescribeImageLifecyclePersonalResponse(AbstractModel):
    """DescribeImageLifecyclePersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 自动删除策略信息
        :type Data: :class:`tcecloud.tcr.v20190924.models.AutoDelStrategyInfoResp`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = AutoDelStrategyInfoResp()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeImagePersonalRequest(AbstractModel):
    """DescribeImagePersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 仓库名称
        :type RepoName: str
        :param Offset: 偏移量，默认为0
        :type Offset: int
        :param Limit: 返回最大数量，默认 20, 最大值 100
        :type Limit: int
        :param Tag: tag名称，可根据输入搜索
        :type Tag: str
        """
        self.RepoName = None
        self.Offset = None
        self.Limit = None
        self.Tag = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.Tag = params.get("Tag")


class DescribeImagePersonalResponse(AbstractModel):
    """DescribeImagePersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 镜像tag信息
        :type Data: :class:`tcecloud.tcr.v20190924.models.TagInfoResp`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = TagInfoResp()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeInstanceStatusRequest(AbstractModel):
    """DescribeInstanceStatus请求参数结构体"""

    def __init__(self):
        """
        :param RegistryIds: 实例ID的数组
        :type RegistryIds: list of str
        """
        self.RegistryIds = None

    def _deserialize(self, params):
        self.RegistryIds = params.get("RegistryIds")


class DescribeInstanceStatusResponse(AbstractModel):
    """DescribeInstanceStatus返回参数结构体"""

    def __init__(self):
        """
        :param RegistryStatusSet: 实例的状态列表
        :type RegistryStatusSet: list of RegistryStatus
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RegistryStatusSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("RegistryStatusSet") is not None:
            self.RegistryStatusSet = []
            for item in params.get("RegistryStatusSet"):
                obj = RegistryStatus()
                obj._deserialize(item)
                self.RegistryStatusSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInstancesRequest(AbstractModel):
    """DescribeInstances请求参数结构体"""

    def __init__(self):
        """
                :param Registryids: 实例ID列表(为空时，
        表示获取账号下所有实例)
                :type Registryids: list of str
                :param Offset: 偏移量,默认0
                :type Offset: int
                :param Limit: 最大输出条数，默认20，最大为100
                :type Limit: int
                :param Filters: 过滤条件
                :type Filters: list of Filter
                :param AllRegion: 获取所有地域的实例，默认为False
                :type AllRegion: bool
        """
        self.Registryids = None
        self.Offset = None
        self.Limit = None
        self.Filters = None
        self.AllRegion = None

    def _deserialize(self, params):
        self.Registryids = params.get("Registryids")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.AllRegion = params.get("AllRegion")


class DescribeInstancesResponse(AbstractModel):
    """DescribeInstances返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 总实例个数
        :type TotalCount: int
        :param Registries: 实例信息列表
        :type Registries: list of Registry
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.Registries = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Registries") is not None:
            self.Registries = []
            for item in params.get("Registries"):
                obj = Registry()
                obj._deserialize(item)
                self.Registries.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInternalEndpointsRequest(AbstractModel):
    """DescribeInternalEndpoints请求参数结构体"""

    def __init__(self):
        """
        :param RegistryId: 实例Id
        :type RegistryId: str
        """
        self.RegistryId = None

    def _deserialize(self, params):
        self.RegistryId = params.get("RegistryId")


class DescribeInternalEndpointsResponse(AbstractModel):
    """DescribeInternalEndpoints返回参数结构体"""

    def __init__(self):
        """
        :param AccessVpcSet: 内网接入信息的列表
        :type AccessVpcSet: list of AccessVpc
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AccessVpcSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("AccessVpcSet") is not None:
            self.AccessVpcSet = []
            for item in params.get("AccessVpcSet"):
                obj = AccessVpc()
                obj._deserialize(item)
                self.AccessVpcSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeNamespacePersonalRequest(AbstractModel):
    """DescribeNamespacePersonal请求参数结构体"""

    def __init__(self):
        """
        :param Namespace: 命名空间，支持模糊查询
        :type Namespace: str
        :param Limit: 单页数量
        :type Limit: int
        :param Offset: 偏移量
        :type Offset: int
        """
        self.Namespace = None
        self.Limit = None
        self.Offset = None

    def _deserialize(self, params):
        self.Namespace = params.get("Namespace")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")


class DescribeNamespacePersonalResponse(AbstractModel):
    """DescribeNamespacePersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 用户命名空间返回信息
        :type Data: :class:`tcecloud.tcr.v20190924.models.NamespaceInfoResp`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = NamespaceInfoResp()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeRegionsRequest(AbstractModel):
    """DescribeRegions请求参数结构体"""


class DescribeRegionsResponse(AbstractModel):
    """DescribeRegions返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 返回的总数
        :type TotalCount: int
        :param Regions: 地域信息列表
        :type Regions: list of Region
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.Regions = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Regions") is not None:
            self.Regions = []
            for item in params.get("Regions"):
                obj = Region()
                obj._deserialize(item)
                self.Regions.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeRepositoryAllPersonalRequest(AbstractModel):
    """DescribeRepositoryAllPersonal请求参数结构体"""

    def __init__(self):
        """
        :param Offset: 偏移量，默认为0
        :type Offset: int
        :param Limit: 返回最大数量，默认 20, 最大值 100
        :type Limit: int
        :param RepoName: 仓库名称
        :type RepoName: str
        :param OrderBy: 筛选条件，支持pullCount和official两个值
        :type OrderBy: str
        :param Order: 升序还是降序，默认是desc，还可以选择asc
        :type Order: str
        """
        self.Offset = None
        self.Limit = None
        self.RepoName = None
        self.OrderBy = None
        self.Order = None

    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.RepoName = params.get("RepoName")
        self.OrderBy = params.get("OrderBy")
        self.Order = params.get("Order")


class DescribeRepositoryAllPersonalResponse(AbstractModel):
    """DescribeRepositoryAllPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 镜像仓库列表
        :type Data: :class:`tcecloud.tcr.v20190924.models.RepoInfoResp`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = RepoInfoResp()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeRepositoryFilterPersonalRequest(AbstractModel):
    """DescribeRepositoryFilterPersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 搜索镜像名
        :type RepoName: str
        :param Offset: 偏移量，默认为0
        :type Offset: int
        :param Limit: 返回最大数量，默认 20，最大100
        :type Limit: int
        :param Public: 筛选条件：1表示public，0表示private
        :type Public: int
        :param Namespace: 命名空间
        :type Namespace: str
        """
        self.RepoName = None
        self.Offset = None
        self.Limit = None
        self.Public = None
        self.Namespace = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.Public = params.get("Public")
        self.Namespace = params.get("Namespace")


class DescribeRepositoryFilterPersonalResponse(AbstractModel):
    """DescribeRepositoryFilterPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 仓库信息
        :type Data: :class:`tcecloud.tcr.v20190924.models.SearchUserRepositoryResp`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = SearchUserRepositoryResp()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeRepositoryOwnerPersonalRequest(AbstractModel):
    """DescribeRepositoryOwnerPersonal请求参数结构体"""

    def __init__(self):
        """
        :param Offset: 偏移量，默认为0
        :type Offset: int
        :param Limit: 返回最大数量，默认 20, 最大值 100
        :type Limit: int
        :param RepoName: 仓库名称
        :type RepoName: str
        """
        self.Offset = None
        self.Limit = None
        self.RepoName = None

    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.RepoName = params.get("RepoName")


class DescribeRepositoryOwnerPersonalResponse(AbstractModel):
    """DescribeRepositoryOwnerPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 仓库信息
        :type Data: :class:`tcecloud.tcr.v20190924.models.RepoInfoResp`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = RepoInfoResp()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeRepositoryPersonalRequest(AbstractModel):
    """DescribeRepositoryPersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 仓库名字
        :type RepoName: str
        """
        self.RepoName = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")


class DescribeRepositoryPersonalResponse(AbstractModel):
    """DescribeRepositoryPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 仓库信息
        :type Data: :class:`tcecloud.tcr.v20190924.models.RepositoryInfoResp`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = RepositoryInfoResp()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeSecurityPoliciesRequest(AbstractModel):
    """DescribeSecurityPolicies请求参数结构体"""

    def __init__(self):
        """
        :param RegistryId: 实例的Id
        :type RegistryId: str
        """
        self.RegistryId = None

    def _deserialize(self, params):
        self.RegistryId = params.get("RegistryId")


class DescribeSecurityPoliciesResponse(AbstractModel):
    """DescribeSecurityPolicies返回参数结构体"""

    def __init__(self):
        """
        :param SecurityPolicySet: 实例安全策略组
        :type SecurityPolicySet: list of SecurityPolicy
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SecurityPolicySet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("SecurityPolicySet") is not None:
            self.SecurityPolicySet = []
            for item in params.get("SecurityPolicySet"):
                obj = SecurityPolicy()
                obj._deserialize(item)
                self.SecurityPolicySet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeSourceCodeAuthPersonalRequest(AbstractModel):
    """DescribeSourceCodeAuthPersonal请求参数结构体"""


class DescribeSourceCodeAuthPersonalResponse(AbstractModel):
    """DescribeSourceCodeAuthPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 查询信息
        :type Data: :class:`tcecloud.tcr.v20190924.models.DesGitAuthRsp`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = DesGitAuthRsp()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeSourceCodeAuthUserInfoPersonalRequest(AbstractModel):
    """DescribeSourceCodeAuthUserInfoPersonal请求参数结构体"""

    def __init__(self):
        """
        :param Type: 类型
        :type Type: str
        """
        self.Type = None

    def _deserialize(self, params):
        self.Type = params.get("Type")


class DescribeSourceCodeAuthUserInfoPersonalResponse(AbstractModel):
    """DescribeSourceCodeAuthUserInfoPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 源代码授权用户信息
        :type Data: :class:`tcecloud.tcr.v20190924.models.AuthUserInfoResp`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = AuthUserInfoResp()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeSourceCodeRepositoryBranchPersonalRequest(AbstractModel):
    """DescribeSourceCodeRepositoryBranchPersonal请求参数结构体"""

    def __init__(self):
        """
        :param Type: 代码仓库类型
        :type Type: str
        :param Group: repo所在的group
        :type Group: str
        :param Repo: 源码在git服务器上的仓库名
        :type Repo: str
        :param Page: Page
        :type Page: int
        :param PerPage: PerPage
        :type PerPage: int
        """
        self.Type = None
        self.Group = None
        self.Repo = None
        self.Page = None
        self.PerPage = None

    def _deserialize(self, params):
        self.Type = params.get("Type")
        self.Group = params.get("Group")
        self.Repo = params.get("Repo")
        self.Page = params.get("Page")
        self.PerPage = params.get("PerPage")


class DescribeSourceCodeRepositoryBranchPersonalResponse(AbstractModel):
    """DescribeSourceCodeRepositoryBranchPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 构建仓库分支信息
        :type Data: :class:`tcecloud.tcr.v20190924.models.BuildBranchResp`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = BuildBranchResp()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeSourceCodeRepositoryPersonalRequest(AbstractModel):
    """DescribeSourceCodeRepositoryPersonal请求参数结构体"""

    def __init__(self):
        """
        :param Type: 代码仓库类型
        :type Type: str
        :param Page: Page
        :type Page: int
        :param PerPage: PerPage
        :type PerPage: int
        """
        self.Type = None
        self.Page = None
        self.PerPage = None

    def _deserialize(self, params):
        self.Type = params.get("Type")
        self.Page = params.get("Page")
        self.PerPage = params.get("PerPage")


class DescribeSourceCodeRepositoryPersonalResponse(AbstractModel):
    """DescribeSourceCodeRepositoryPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 构建仓库列表
        :type Data: :class:`tcecloud.tcr.v20190924.models.BuildReposList`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = BuildReposList()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeUserPersonalRequest(AbstractModel):
    """DescribeUserPersonal请求参数结构体"""


class DescribeUserPersonalResponse(AbstractModel):
    """DescribeUserPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 返回的用户信息
        :type Data: :class:`tcecloud.tcr.v20190924.models.UserInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = UserInfo()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeUserQuotaPersonalRequest(AbstractModel):
    """DescribeUserQuotaPersonal请求参数结构体"""


class DescribeUserQuotaPersonalResponse(AbstractModel):
    """DescribeUserQuotaPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 配额返回信息
        :type Data: :class:`tcecloud.tcr.v20190924.models.RespLimit`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = RespLimit()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DockerHubRepoinfo(AbstractModel):
    """DockerHub仓库信息"""

    def __init__(self):
        """
        :param Reponame: 仓库名称
        :type Reponame: str
        :param Repotype: 仓库类型
        :type Repotype: str
        :param Logo: 仓库Logo
        :type Logo: str
        :param SimpleDesc: 简述
        :type SimpleDesc: str
        :param DetailDesc: 详述
        :type DetailDesc: str
        :param FavorCount: 收藏次数
        :type FavorCount: int
        :param IsUserFavor: 是否用户的收藏
        :type IsUserFavor: bool
        """
        self.Reponame = None
        self.Repotype = None
        self.Logo = None
        self.SimpleDesc = None
        self.DetailDesc = None
        self.FavorCount = None
        self.IsUserFavor = None

    def _deserialize(self, params):
        self.Reponame = params.get("Reponame")
        self.Repotype = params.get("Repotype")
        self.Logo = params.get("Logo")
        self.SimpleDesc = params.get("SimpleDesc")
        self.DetailDesc = params.get("DetailDesc")
        self.FavorCount = params.get("FavorCount")
        self.IsUserFavor = params.get("IsUserFavor")


class DockerHubTagList(AbstractModel):
    """用于返回dockerhub的tag列表"""

    def __init__(self):
        """
                :param Reponame: DockerHub的仓库名称
        注意：此字段可能返回 null，表示取不到有效值。
                :type Reponame: str
                :param TagList: Tag的列表
        注意：此字段可能返回 null，表示取不到有效值。
                :type TagList: list of str
        """
        self.Reponame = None
        self.TagList = None

    def _deserialize(self, params):
        self.Reponame = params.get("Reponame")
        self.TagList = params.get("TagList")


class DupImageTagResp(AbstractModel):
    """复制镜像tag返回值"""

    def __init__(self):
        """
        :param Digest: 镜像Digest值
        :type Digest: str
        """
        self.Digest = None

    def _deserialize(self, params):
        self.Digest = params.get("Digest")


class DuplicateImagePersonalRequest(AbstractModel):
    """DuplicateImagePersonal请求参数结构体"""

    def __init__(self):
        """
        :param SrcImage: 源镜像名称，不包含domain。例如： tencentyun/foo:v1
        :type SrcImage: str
        :param DestImage: 目的镜像名称，不包含domain。例如： tencentyun/foo:latest
        :type DestImage: str
        """
        self.SrcImage = None
        self.DestImage = None

    def _deserialize(self, params):
        self.SrcImage = params.get("SrcImage")
        self.DestImage = params.get("DestImage")


class DuplicateImagePersonalResponse(AbstractModel):
    """DuplicateImagePersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 复制镜像返回值
        :type Data: :class:`tcecloud.tcr.v20190924.models.DupImageTagResp`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = DupImageTagResp()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class FavorResp(AbstractModel):
    """用于获取收藏仓库的响应"""

    def __init__(self):
        """
                :param TotalCount: 收藏仓库的总数
                :type TotalCount: int
                :param RepoInfo: 仓库信息数组
        注意：此字段可能返回 null，表示取不到有效值。
                :type RepoInfo: list of Favors
        """
        self.TotalCount = None
        self.RepoInfo = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("RepoInfo") is not None:
            self.RepoInfo = []
            for item in params.get("RepoInfo"):
                obj = Favors()
                obj._deserialize(item)
                self.RepoInfo.append(obj)


class Favors(AbstractModel):
    """仓库收藏"""

    def __init__(self):
        """
                :param RepoName: 仓库名字
                :type RepoName: str
                :param RepoType: 仓库类型
                :type RepoType: str
                :param PullCount: Pull总共的次数
        注意：此字段可能返回 null，表示取不到有效值。
                :type PullCount: int
                :param FavorCount: 仓库收藏次数
        注意：此字段可能返回 null，表示取不到有效值。
                :type FavorCount: int
                :param Public: 仓库是否公开
        注意：此字段可能返回 null，表示取不到有效值。
                :type Public: int
                :param IsQcloudOfficial: 是否为官方所有
        注意：此字段可能返回 null，表示取不到有效值。
                :type IsQcloudOfficial: bool
                :param TagCount: 仓库Tag的数量
        注意：此字段可能返回 null，表示取不到有效值。
                :type TagCount: int
                :param Logo: Logo
        注意：此字段可能返回 null，表示取不到有效值。
                :type Logo: str
                :param Region: 地域
                :type Region: str
                :param RegionId: 地域的Id
                :type RegionId: int
        """
        self.RepoName = None
        self.RepoType = None
        self.PullCount = None
        self.FavorCount = None
        self.Public = None
        self.IsQcloudOfficial = None
        self.TagCount = None
        self.Logo = None
        self.Region = None
        self.RegionId = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")
        self.RepoType = params.get("RepoType")
        self.PullCount = params.get("PullCount")
        self.FavorCount = params.get("FavorCount")
        self.Public = params.get("Public")
        self.IsQcloudOfficial = params.get("IsQcloudOfficial")
        self.TagCount = params.get("TagCount")
        self.Logo = params.get("Logo")
        self.Region = params.get("Region")
        self.RegionId = params.get("RegionId")


class Filter(AbstractModel):
    """过滤器"""

    def __init__(self):
        """
        :param Name: 属性名称, 若存在多个Filter时，Filter间的关系为逻辑与（AND）关系。
        :type Name: str
        :param Values: 属性值, 若同一个Filter存在多个Values，同一Filter下Values间的关系为逻辑或（OR）关系。
        :type Values: list of str
        """
        self.Name = None
        self.Values = None

    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Values = params.get("Values")


class ForwardRequestRequest(AbstractModel):
    """ForwardRequest请求参数结构体"""

    def __init__(self):
        """
        :param Method: 请求tcr对应的方法
        :type Method: str
        :param Path: 请求tcr对应的路径
        :type Path: str
        :param RegistryId: 请求的实例ID
        :type RegistryId: str
        :param Accept: 请求tcr中的HTTP头中Accept参数
        :type Accept: str
        :param ContentType: 请求tcr http头中ContentType参数
        :type ContentType: str
        :param RequestBody: 请求tcr中的body信息
        :type RequestBody: str
        """
        self.Method = None
        self.Path = None
        self.RegistryId = None
        self.Accept = None
        self.ContentType = None
        self.RequestBody = None

    def _deserialize(self, params):
        self.Method = params.get("Method")
        self.Path = params.get("Path")
        self.RegistryId = params.get("RegistryId")
        self.Accept = params.get("Accept")
        self.ContentType = params.get("ContentType")
        self.RequestBody = params.get("RequestBody")


class ForwardRequestResponse(AbstractModel):
    """ForwardRequest返回参数结构体"""

    def __init__(self):
        """
        :param ResponseBody: 代理请求响应body
        :type ResponseBody: str
        :param ResponseHeaders: 代理请求响应的header
        :type ResponseHeaders: list of ResponseHeader
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ResponseBody = None
        self.ResponseHeaders = None
        self.RequestId = None

    def _deserialize(self, params):
        self.ResponseBody = params.get("ResponseBody")
        if params.get("ResponseHeaders") is not None:
            self.ResponseHeaders = []
            for item in params.get("ResponseHeaders"):
                obj = ResponseHeader()
                obj._deserialize(item)
                self.ResponseHeaders.append(obj)
        self.RequestId = params.get("RequestId")


class HubSimpleInfo(AbstractModel):
    """Hub的信息描述"""

    def __init__(self):
        """
        :param Reponame: 仓库名称
        :type Reponame: str
        :param Repotype: 仓库类型
        :type Repotype: str
        :param Logo: 仓库Logo
        :type Logo: str
        :param SimpleDesc: 仓库简述
        :type SimpleDesc: str
        :param IsUserFavor: 是否为收藏
        :type IsUserFavor: bool
        :param FavorCount: 收藏数量
        :type FavorCount: int
        """
        self.Reponame = None
        self.Repotype = None
        self.Logo = None
        self.SimpleDesc = None
        self.IsUserFavor = None
        self.FavorCount = None

    def _deserialize(self, params):
        self.Reponame = params.get("Reponame")
        self.Repotype = params.get("Repotype")
        self.Logo = params.get("Logo")
        self.SimpleDesc = params.get("SimpleDesc")
        self.IsUserFavor = params.get("IsUserFavor")
        self.FavorCount = params.get("FavorCount")


class Limit(AbstractModel):
    """共享镜像仓库用户配额"""

    def __init__(self):
        """
        :param Username: 用户名
        :type Username: str
        :param Type: 配额的类型
        :type Type: str
        :param Value: 配置的值
        :type Value: int
        """
        self.Username = None
        self.Type = None
        self.Value = None

    def _deserialize(self, params):
        self.Username = params.get("Username")
        self.Type = params.get("Type")
        self.Value = params.get("Value")


class ManageExternalEndpointRequest(AbstractModel):
    """ManageExternalEndpoint请求参数结构体"""

    def __init__(self):
        """
        :param RegistryId: 实例Id
        :type RegistryId: str
        :param Operation: 操作（Create/Delete）
        :type Operation: str
        """
        self.RegistryId = None
        self.Operation = None

    def _deserialize(self, params):
        self.RegistryId = params.get("RegistryId")
        self.Operation = params.get("Operation")


class ManageExternalEndpointResponse(AbstractModel):
    """ManageExternalEndpoint返回参数结构体"""

    def __init__(self):
        """
        :param RegistryId: 实例Id
        :type RegistryId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RegistryId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.RegistryId = params.get("RegistryId")
        self.RequestId = params.get("RequestId")


class ManageImageLifecycleGlobalPersonalRequest(AbstractModel):
    """ManageImageLifecycleGlobalPersonal请求参数结构体"""

    def __init__(self):
        """
        :param Type: global_keep_last_days:全局保留最近几天的数据;global_keep_last_nums:全局保留最近多少个
        :type Type: str
        :param Val: 策略值
        :type Val: int
        """
        self.Type = None
        self.Val = None

    def _deserialize(self, params):
        self.Type = params.get("Type")
        self.Val = params.get("Val")


class ManageImageLifecycleGlobalPersonalResponse(AbstractModel):
    """ManageImageLifecycleGlobalPersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ManageInternalEndpointRequest(AbstractModel):
    """ManageInternalEndpoint请求参数结构体"""

    def __init__(self):
        """
        :param RegistryId: 实例Id
        :type RegistryId: str
        :param Operation: Create/Delete
        :type Operation: str
        :param VpcId: 需要接入的用户vpcid
        :type VpcId: str
        :param SubnetId: 需要接入的用户子网id
        :type SubnetId: str
        """
        self.RegistryId = None
        self.Operation = None
        self.VpcId = None
        self.SubnetId = None

    def _deserialize(self, params):
        self.RegistryId = params.get("RegistryId")
        self.Operation = params.get("Operation")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")


class ManageInternalEndpointResponse(AbstractModel):
    """ManageInternalEndpoint返回参数结构体"""

    def __init__(self):
        """
        :param RegistryId: 实例Id
        :type RegistryId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RegistryId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.RegistryId = params.get("RegistryId")
        self.RequestId = params.get("RequestId")


class ManageReplicationRequest(AbstractModel):
    """ManageReplication请求参数结构体"""

    def __init__(self):
        """
        :param SourceRegistryId: 复制源实例ID
        :type SourceRegistryId: str
        :param DestinationRegistryId: 复制目标实例ID
        :type DestinationRegistryId: str
        :param Rule: 同步规则
        :type Rule: :class:`tcecloud.tcr.v20190924.models.ReplicationRule`
        :param Description: 规则描述
        :type Description: str
        """
        self.SourceRegistryId = None
        self.DestinationRegistryId = None
        self.Rule = None
        self.Description = None

    def _deserialize(self, params):
        self.SourceRegistryId = params.get("SourceRegistryId")
        self.DestinationRegistryId = params.get("DestinationRegistryId")
        if params.get("Rule") is not None:
            self.Rule = ReplicationRule()
            self.Rule._deserialize(params.get("Rule"))
        self.Description = params.get("Description")


class ManageReplicationResponse(AbstractModel):
    """ManageReplication返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyApplicationTriggerPersonalRequest(AbstractModel):
    """ModifyApplicationTriggerPersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 触发器关联的镜像仓库，library/test格式
        :type RepoName: str
        :param TriggerName: 触发器名称
        :type TriggerName: str
        :param InvokeMethod: 触发方式，"all"全部触发，"taglist"指定tag触发，"regex"正则触发
        :type InvokeMethod: str
        :param InvokeExpr: 触发方式对应的表达式
        :type InvokeExpr: str
        :param ClusterId: 应用所在TKE集群ID
        :type ClusterId: str
        :param Namespace: 应用所在TKE集群命名空间
        :type Namespace: str
        :param WorkloadType: 应用所在TKE集群工作负载类型,支持Deployment、StatefulSet、DaemonSet、CronJob、Job。
        :type WorkloadType: str
        :param WorkloadName: 应用所在TKE集群工作负载名称
        :type WorkloadName: str
        :param ContainerName: 应用所在TKE集群工作负载下容器名称
        :type ContainerName: str
        :param ClusterRegion: 应用所在TKE集群地域数字ID，如1（广州）、16（成都）
        :type ClusterRegion: int
        :param NewTriggerName: 新触发器名称
        :type NewTriggerName: str
        """
        self.RepoName = None
        self.TriggerName = None
        self.InvokeMethod = None
        self.InvokeExpr = None
        self.ClusterId = None
        self.Namespace = None
        self.WorkloadType = None
        self.WorkloadName = None
        self.ContainerName = None
        self.ClusterRegion = None
        self.NewTriggerName = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")
        self.TriggerName = params.get("TriggerName")
        self.InvokeMethod = params.get("InvokeMethod")
        self.InvokeExpr = params.get("InvokeExpr")
        self.ClusterId = params.get("ClusterId")
        self.Namespace = params.get("Namespace")
        self.WorkloadType = params.get("WorkloadType")
        self.WorkloadName = params.get("WorkloadName")
        self.ContainerName = params.get("ContainerName")
        self.ClusterRegion = params.get("ClusterRegion")
        self.NewTriggerName = params.get("NewTriggerName")


class ModifyApplicationTriggerPersonalResponse(AbstractModel):
    """ModifyApplicationTriggerPersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyImageBuildPersonalRequest(AbstractModel):
    """ModifyImageBuildPersonal请求参数结构体"""

    def __init__(self):
        """
        :param RegistryNamespace: registry中的namespace
        :type RegistryNamespace: str
        :param RegistryUsername: 用户在registry中的用户名
        :type RegistryUsername: str
        :param ImageName: 镜像名称，不包含tag
        :type ImageName: str
        :param ImageTagFormat: 镜像tag的格式
        :type ImageTagFormat: str
        :param GitServer: 源码所在的git服务
        :type GitServer: str
        :param Group: repo所在的group
        :type Group: str
        :param Repo: 源码在git服务器上的仓库名
        :type Repo: str
        :param Owner: 用户在git服务器上的用户名
        :type Owner: str
        :param Trigger: Trigger
        :type Trigger: :class:`tcecloud.tcr.v20190924.models.Trigger`
        :param DockerfilePath: dockerfile在仓库中的路径
        :type DockerfilePath: str
        :param WorkDir: 工作目录
        :type WorkDir: str
        :param ForceTag: 构建出的镜像覆盖该Tag
        :type ForceTag: str
        :param Args: Args
        :type Args: list of str
        """
        self.RegistryNamespace = None
        self.RegistryUsername = None
        self.ImageName = None
        self.ImageTagFormat = None
        self.GitServer = None
        self.Group = None
        self.Repo = None
        self.Owner = None
        self.Trigger = None
        self.DockerfilePath = None
        self.WorkDir = None
        self.ForceTag = None
        self.Args = None

    def _deserialize(self, params):
        self.RegistryNamespace = params.get("RegistryNamespace")
        self.RegistryUsername = params.get("RegistryUsername")
        self.ImageName = params.get("ImageName")
        self.ImageTagFormat = params.get("ImageTagFormat")
        self.GitServer = params.get("GitServer")
        self.Group = params.get("Group")
        self.Repo = params.get("Repo")
        self.Owner = params.get("Owner")
        if params.get("Trigger") is not None:
            self.Trigger = Trigger()
            self.Trigger._deserialize(params.get("Trigger"))
        self.DockerfilePath = params.get("DockerfilePath")
        self.WorkDir = params.get("WorkDir")
        self.ForceTag = params.get("ForceTag")
        self.Args = params.get("Args")


class ModifyImageBuildPersonalResponse(AbstractModel):
    """ModifyImageBuildPersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyInstanceRequest(AbstractModel):
    """ModifyInstance请求参数结构体"""

    def __init__(self):
        """
        :param RegistryId: 实例ID
        :type RegistryId: str
        :param RegistryType: 实例的规格
        :type RegistryType: str
        """
        self.RegistryId = None
        self.RegistryType = None

    def _deserialize(self, params):
        self.RegistryId = params.get("RegistryId")
        self.RegistryType = params.get("RegistryType")


class ModifyInstanceResponse(AbstractModel):
    """ModifyInstance返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyRepositoryAccessPersonalRequest(AbstractModel):
    """ModifyRepositoryAccessPersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 仓库名称
        :type RepoName: str
        :param Public: 默认值为0
        :type Public: int
        """
        self.RepoName = None
        self.Public = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")
        self.Public = params.get("Public")


class ModifyRepositoryAccessPersonalResponse(AbstractModel):
    """ModifyRepositoryAccessPersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyRepositoryInfoPersonalRequest(AbstractModel):
    """ModifyRepositoryInfoPersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 仓库名称
        :type RepoName: str
        :param Description: 仓库描述
        :type Description: str
        """
        self.RepoName = None
        self.Description = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")
        self.Description = params.get("Description")


class ModifyRepositoryInfoPersonalResponse(AbstractModel):
    """ModifyRepositoryInfoPersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifySecurityPolicyRequest(AbstractModel):
    """ModifySecurityPolicy请求参数结构体"""

    def __init__(self):
        """
        :param RegistryId: 实例的Id
        :type RegistryId: str
        :param PolicyIndex: PolicyId
        :type PolicyIndex: int
        :param CidrBlock: 192.168.0.0/24 白名单Ip
        :type CidrBlock: str
        :param Description: 备注
        :type Description: str
        """
        self.RegistryId = None
        self.PolicyIndex = None
        self.CidrBlock = None
        self.Description = None

    def _deserialize(self, params):
        self.RegistryId = params.get("RegistryId")
        self.PolicyIndex = params.get("PolicyIndex")
        self.CidrBlock = params.get("CidrBlock")
        self.Description = params.get("Description")


class ModifySecurityPolicyResponse(AbstractModel):
    """ModifySecurityPolicy返回参数结构体"""

    def __init__(self):
        """
        :param RegistryId: 实例Id
        :type RegistryId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RegistryId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.RegistryId = params.get("RegistryId")
        self.RequestId = params.get("RequestId")


class ModifyUserPasswordPersonalRequest(AbstractModel):
    """ModifyUserPasswordPersonal请求参数结构体"""

    def __init__(self):
        """
        :param Password: 更新后的密码
        :type Password: str
        """
        self.Password = None

    def _deserialize(self, params):
        self.Password = params.get("Password")


class ModifyUserPasswordPersonalResponse(AbstractModel):
    """ModifyUserPasswordPersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class NamespaceInfo(AbstractModel):
    """命名空间信息"""

    def __init__(self):
        """
        :param Namespace: 命名空间
        :type Namespace: str
        :param CreationTime: 创建时间
        :type CreationTime: str
        :param RepoCount: 命名空间下仓库数量
        :type RepoCount: int
        """
        self.Namespace = None
        self.CreationTime = None
        self.RepoCount = None

    def _deserialize(self, params):
        self.Namespace = params.get("Namespace")
        self.CreationTime = params.get("CreationTime")
        self.RepoCount = params.get("RepoCount")


class NamespaceInfoResp(AbstractModel):
    """获取命名空间信息返回"""

    def __init__(self):
        """
        :param NamespaceCount: 命名空间数量
        :type NamespaceCount: int
        :param NamespaceInfo: 命名空间信息
        :type NamespaceInfo: list of NamespaceInfo
        """
        self.NamespaceCount = None
        self.NamespaceInfo = None

    def _deserialize(self, params):
        self.NamespaceCount = params.get("NamespaceCount")
        if params.get("NamespaceInfo") is not None:
            self.NamespaceInfo = []
            for item in params.get("NamespaceInfo"):
                obj = NamespaceInfo()
                obj._deserialize(item)
                self.NamespaceInfo.append(obj)


class NamespaceIsExistsResp(AbstractModel):
    """NamespaceIsExists返回类型"""

    def __init__(self):
        """
        :param IsExist: 命名空间是否存在
        :type IsExist: bool
        :param IsPreserved: 是否为保留命名空间
        :type IsPreserved: bool
        """
        self.IsExist = None
        self.IsPreserved = None

    def _deserialize(self, params):
        self.IsExist = params.get("IsExist")
        self.IsPreserved = params.get("IsPreserved")


class Region(AbstractModel):
    """地域信息"""

    def __init__(self):
        """
        :param Alias: gz
        :type Alias: str
        :param RegionId: 1
        :type RegionId: int
        :param RegionName: ap-guangzhou
        :type RegionName: str
        :param Status: alluser
        :type Status: str
        :param Remark: remark
        :type Remark: str
        :param CreatedAt: 创建时间
        :type CreatedAt: str
        :param UpdatedAt: 更新时间
        :type UpdatedAt: str
        :param Id: id
        :type Id: int
        """
        self.Alias = None
        self.RegionId = None
        self.RegionName = None
        self.Status = None
        self.Remark = None
        self.CreatedAt = None
        self.UpdatedAt = None
        self.Id = None

    def _deserialize(self, params):
        self.Alias = params.get("Alias")
        self.RegionId = params.get("RegionId")
        self.RegionName = params.get("RegionName")
        self.Status = params.get("Status")
        self.Remark = params.get("Remark")
        self.CreatedAt = params.get("CreatedAt")
        self.UpdatedAt = params.get("UpdatedAt")
        self.Id = params.get("Id")


class Registry(AbstractModel):
    """实例信息结构体"""

    def __init__(self):
        """
        :param RegistryId: 实例ID
        :type RegistryId: str
        :param RegistryName: 实例名称
        :type RegistryName: str
        :param RegistryType: 实例规格
        :type RegistryType: str
        :param Status: 实例状态
        :type Status: str
        :param PublicDomain: 实例的公共访问地址
        :type PublicDomain: str
        :param CreatedAt: 实例创建时间
        :type CreatedAt: str
        :param RegionName: 地域名称
        :type RegionName: str
        :param RegionId: 地域Id
        :type RegionId: int
        :param EnableAnonymous: 是否支持匿名
        :type EnableAnonymous: bool
        :param TokenValidTime: Token有效时间
        :type TokenValidTime: int
        """
        self.RegistryId = None
        self.RegistryName = None
        self.RegistryType = None
        self.Status = None
        self.PublicDomain = None
        self.CreatedAt = None
        self.RegionName = None
        self.RegionId = None
        self.EnableAnonymous = None
        self.TokenValidTime = None

    def _deserialize(self, params):
        self.RegistryId = params.get("RegistryId")
        self.RegistryName = params.get("RegistryName")
        self.RegistryType = params.get("RegistryType")
        self.Status = params.get("Status")
        self.PublicDomain = params.get("PublicDomain")
        self.CreatedAt = params.get("CreatedAt")
        self.RegionName = params.get("RegionName")
        self.RegionId = params.get("RegionId")
        self.EnableAnonymous = params.get("EnableAnonymous")
        self.TokenValidTime = params.get("TokenValidTime")


class RegistryCondition(AbstractModel):
    """实例创建过程"""

    def __init__(self):
        """
                :param Type: 实例创建过程类型
                :type Type: str
                :param Status: 实例创建过程状态
                :type Status: str
                :param Reason: 转换到该过程的简明原因
        注意：此字段可能返回 null，表示取不到有效值。
                :type Reason: str
        """
        self.Type = None
        self.Status = None
        self.Reason = None

    def _deserialize(self, params):
        self.Type = params.get("Type")
        self.Status = params.get("Status")
        self.Reason = params.get("Reason")


class RegistryStatus(AbstractModel):
    """实例状态"""

    def __init__(self):
        """
                :param RegistryId: 实例的Id
                :type RegistryId: str
                :param Status: 实例的状态
                :type Status: str
                :param Conditions: 附加状态
        注意：此字段可能返回 null，表示取不到有效值。
                :type Conditions: list of RegistryCondition
        """
        self.RegistryId = None
        self.Status = None
        self.Conditions = None

    def _deserialize(self, params):
        self.RegistryId = params.get("RegistryId")
        self.Status = params.get("Status")
        if params.get("Conditions") is not None:
            self.Conditions = []
            for item in params.get("Conditions"):
                obj = RegistryCondition()
                obj._deserialize(item)
                self.Conditions.append(obj)


class ReplicationFilter(AbstractModel):
    """同步规则过滤器"""

    def __init__(self):
        """
        :param Type: 类型（name、tag和resource）
        :type Type: str
        :param Value: 默认为空
        :type Value: str
        """
        self.Type = None
        self.Value = None

    def _deserialize(self, params):
        self.Type = params.get("Type")
        self.Value = params.get("Value")


class ReplicationRule(AbstractModel):
    """同步规则"""

    def __init__(self):
        """
        :param Name: 同步规则名称
        :type Name: str
        :param DestNamespace: 目标命名空间
        :type DestNamespace: str
        :param Override: 是否覆盖
        :type Override: bool
        :param Filters: 同步过滤条件
        :type Filters: list of ReplicationFilter
        """
        self.Name = None
        self.DestNamespace = None
        self.Override = None
        self.Filters = None

    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.DestNamespace = params.get("DestNamespace")
        self.Override = params.get("Override")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = ReplicationFilter()
                obj._deserialize(item)
                self.Filters.append(obj)


class RepoInfo(AbstractModel):
    """仓库的信息"""

    def __init__(self):
        """
        :param RepoName: 仓库名称
        :type RepoName: str
        :param RepoType: 仓库类型
        :type RepoType: str
        :param TagCount: Tag数量
        :type TagCount: int
        :param Public: 是否为公开
        :type Public: int
        :param IsUserFavor: 是否为用户收藏
        :type IsUserFavor: bool
        :param IsQcloudOfficial: 是否为Tce官方仓库
        :type IsQcloudOfficial: bool
        :param FavorCount: 被收藏的个数
        :type FavorCount: int
        :param PullCount: 拉取的数量
        :type PullCount: int
        :param Description: 描述
        :type Description: str
        :param CreationTime: 仓库创建时间
        :type CreationTime: str
        :param UpdateTime: 仓库更新时间
        :type UpdateTime: str
        """
        self.RepoName = None
        self.RepoType = None
        self.TagCount = None
        self.Public = None
        self.IsUserFavor = None
        self.IsQcloudOfficial = None
        self.FavorCount = None
        self.PullCount = None
        self.Description = None
        self.CreationTime = None
        self.UpdateTime = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")
        self.RepoType = params.get("RepoType")
        self.TagCount = params.get("TagCount")
        self.Public = params.get("Public")
        self.IsUserFavor = params.get("IsUserFavor")
        self.IsQcloudOfficial = params.get("IsQcloudOfficial")
        self.FavorCount = params.get("FavorCount")
        self.PullCount = params.get("PullCount")
        self.Description = params.get("Description")
        self.CreationTime = params.get("CreationTime")
        self.UpdateTime = params.get("UpdateTime")


class RepoInfoResp(AbstractModel):
    """仓库信息的返回信息"""

    def __init__(self):
        """
        :param TotalCount: 仓库总数
        :type TotalCount: int
        :param RepoInfo: 仓库信息列表
        :type RepoInfo: list of RepoInfo
        :param Server: Server信息
        :type Server: str
        """
        self.TotalCount = None
        self.RepoInfo = None
        self.Server = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("RepoInfo") is not None:
            self.RepoInfo = []
            for item in params.get("RepoInfo"):
                obj = RepoInfo()
                obj._deserialize(item)
                self.RepoInfo.append(obj)
        self.Server = params.get("Server")


class RepoIsExistResp(AbstractModel):
    """仓库是否存在的返回值"""

    def __init__(self):
        """
        :param IsExist: 仓库是否存在
        :type IsExist: bool
        """
        self.IsExist = None

    def _deserialize(self, params):
        self.IsExist = params.get("IsExist")


class RepositoryInfoResp(AbstractModel):
    """查询共享版仓库信息返回"""

    def __init__(self):
        """
                :param RepoName: 镜像仓库名字
                :type RepoName: str
                :param RepoType: 镜像仓库类型
                :type RepoType: str
                :param Server: 镜像仓库服务地址
                :type Server: str
                :param CreationTime: 创建时间
                :type CreationTime: str
                :param Description: 镜像仓库描述
        注意：此字段可能返回 null，表示取不到有效值。
                :type Description: str
                :param Public: 是否为公有镜像
                :type Public: int
                :param PullCount: 下载次数
                :type PullCount: int
                :param FavorCount: 收藏次数
                :type FavorCount: int
                :param IsUserFavor: 是否为用户收藏
                :type IsUserFavor: bool
                :param IsQcloudOfficial: 是否为Tce官方镜像
                :type IsQcloudOfficial: bool
        """
        self.RepoName = None
        self.RepoType = None
        self.Server = None
        self.CreationTime = None
        self.Description = None
        self.Public = None
        self.PullCount = None
        self.FavorCount = None
        self.IsUserFavor = None
        self.IsQcloudOfficial = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")
        self.RepoType = params.get("RepoType")
        self.Server = params.get("Server")
        self.CreationTime = params.get("CreationTime")
        self.Description = params.get("Description")
        self.Public = params.get("Public")
        self.PullCount = params.get("PullCount")
        self.FavorCount = params.get("FavorCount")
        self.IsUserFavor = params.get("IsUserFavor")
        self.IsQcloudOfficial = params.get("IsQcloudOfficial")


class RequestFavor(AbstractModel):
    """请求的入参，用于收藏镜像仓库"""

    def __init__(self):
        """
        :param RepoName: 收藏的镜像仓库名称
        :type RepoName: str
        :param RepoType: 收藏的镜像仓库类型
        :type RepoType: str
        :param RegionId: 地域Id
        :type RegionId: str
        """
        self.RepoName = None
        self.RepoType = None
        self.RegionId = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")
        self.RepoType = params.get("RepoType")
        self.RegionId = params.get("RegionId")


class RespDockerHubRepoList(AbstractModel):
    """用于DokcerHub 仓库列表信息的返回信息"""

    def __init__(self):
        """
        :param TotalCount: 仓库总数
        :type TotalCount: int
        :param RepoInfo: 仓库信息列表
        :type RepoInfo: list of HubSimpleInfo
        """
        self.TotalCount = None
        self.RepoInfo = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("RepoInfo") is not None:
            self.RepoInfo = []
            for item in params.get("RepoInfo"):
                obj = HubSimpleInfo()
                obj._deserialize(item)
                self.RepoInfo.append(obj)


class RespLimit(AbstractModel):
    """用户配额返回值"""

    def __init__(self):
        """
        :param LimitInfo: 配额信息
        :type LimitInfo: list of Limit
        """
        self.LimitInfo = None

    def _deserialize(self, params):
        if params.get("LimitInfo") is not None:
            self.LimitInfo = []
            for item in params.get("LimitInfo"):
                obj = Limit()
                obj._deserialize(item)
                self.LimitInfo.append(obj)


class ResponseHeader(AbstractModel):
    """Tcr转发接口返回的头信息"""

    def __init__(self):
        """
                :param Key: Key
        注意：此字段可能返回 null，表示取不到有效值。
                :type Key: str
                :param Value: Value
        注意：此字段可能返回 null，表示取不到有效值。
                :type Value: str
        """
        self.Key = None
        self.Value = None

    def _deserialize(self, params):
        self.Key = params.get("Key")
        self.Value = params.get("Value")


class SameImagesResp(AbstractModel):
    """指定tag镜像内容相同的tag列表"""

    def __init__(self):
        """
                :param SameImages: tag列表
        注意：此字段可能返回 null，表示取不到有效值。
                :type SameImages: list of str
        """
        self.SameImages = None

    def _deserialize(self, params):
        self.SameImages = params.get("SameImages")


class SearchUserRepositoryResp(AbstractModel):
    """获取满足输入搜索条件的用户镜像仓库"""

    def __init__(self):
        """
        :param TotalCount: 总个数
        :type TotalCount: int
        :param RepoInfo: 仓库列表
        :type RepoInfo: list of RepoInfo
        :param Server: Server
        :type Server: str
        :param PrivilegeFiltered: PrivilegeFiltered
        :type PrivilegeFiltered: bool
        """
        self.TotalCount = None
        self.RepoInfo = None
        self.Server = None
        self.PrivilegeFiltered = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("RepoInfo") is not None:
            self.RepoInfo = []
            for item in params.get("RepoInfo"):
                obj = RepoInfo()
                obj._deserialize(item)
                self.RepoInfo.append(obj)
        self.Server = params.get("Server")
        self.PrivilegeFiltered = params.get("PrivilegeFiltered")


class SecurityPolicy(AbstractModel):
    """安全策略"""

    def __init__(self):
        """
        :param PolicyIndex: 策略索引
        :type PolicyIndex: int
        :param Description: 备注
        :type Description: str
        :param CidrBlock: 192.168.1.0/24
        :type CidrBlock: str
        :param PolicyVersion: 安全策略的版本
        :type PolicyVersion: str
        """
        self.PolicyIndex = None
        self.Description = None
        self.CidrBlock = None
        self.PolicyVersion = None

    def _deserialize(self, params):
        self.PolicyIndex = params.get("PolicyIndex")
        self.Description = params.get("Description")
        self.CidrBlock = params.get("CidrBlock")
        self.PolicyVersion = params.get("PolicyVersion")


class TagInfo(AbstractModel):
    """镜像tag信息"""

    def __init__(self):
        """
                :param TagName: Tag名称
                :type TagName: str
                :param TagId: 镜像Id
                :type TagId: str
                :param ImageId: docker image 可以看到的id
                :type ImageId: str
                :param Size: 大小
                :type Size: str
                :param CreationTime: 镜像的创建时间
                :type CreationTime: str
                :param DurationDays: 镜像创建至今时间长度
        注意：此字段可能返回 null，表示取不到有效值。
                :type DurationDays: str
                :param Author: 镜像的作者
                :type Author: str
                :param Architecture: 次镜像建议运行的系统架构
                :type Architecture: str
                :param DockerVersion: 创建此镜像的docker版本
                :type DockerVersion: str
                :param OS: 此镜像建议运行系统
                :type OS: str
                :param SizeByte: SizeByte
                :type SizeByte: int
                :param Id: Id
                :type Id: int
                :param UpdateTime: 数据更新时间
                :type UpdateTime: str
                :param PushTime: 镜像更新时间
                :type PushTime: str
        """
        self.TagName = None
        self.TagId = None
        self.ImageId = None
        self.Size = None
        self.CreationTime = None
        self.DurationDays = None
        self.Author = None
        self.Architecture = None
        self.DockerVersion = None
        self.OS = None
        self.SizeByte = None
        self.Id = None
        self.UpdateTime = None
        self.PushTime = None

    def _deserialize(self, params):
        self.TagName = params.get("TagName")
        self.TagId = params.get("TagId")
        self.ImageId = params.get("ImageId")
        self.Size = params.get("Size")
        self.CreationTime = params.get("CreationTime")
        self.DurationDays = params.get("DurationDays")
        self.Author = params.get("Author")
        self.Architecture = params.get("Architecture")
        self.DockerVersion = params.get("DockerVersion")
        self.OS = params.get("OS")
        self.SizeByte = params.get("SizeByte")
        self.Id = params.get("Id")
        self.UpdateTime = params.get("UpdateTime")
        self.PushTime = params.get("PushTime")


class TagInfoResp(AbstractModel):
    """Tag列表的返回值"""

    def __init__(self):
        """
        :param TagCount: Tag的总数
        :type TagCount: int
        :param TagInfo: TagInfo列表
        :type TagInfo: list of TagInfo
        :param Server: Server
        :type Server: str
        :param RepoName: 仓库名称
        :type RepoName: str
        """
        self.TagCount = None
        self.TagInfo = None
        self.Server = None
        self.RepoName = None

    def _deserialize(self, params):
        self.TagCount = params.get("TagCount")
        if params.get("TagInfo") is not None:
            self.TagInfo = []
            for item in params.get("TagInfo"):
                obj = TagInfo()
                obj._deserialize(item)
                self.TagInfo.append(obj)
        self.Server = params.get("Server")
        self.RepoName = params.get("RepoName")


class Trigger(AbstractModel):
    """Trigger，用于ccb"""

    def __init__(self):
        """
        :param Branches: 分支
        :type Branches: list of str
        :param Tag: Tag
        :type Tag: int
        """
        self.Branches = None
        self.Tag = None

    def _deserialize(self, params):
        self.Branches = params.get("Branches")
        self.Tag = params.get("Tag")


class TriggerInvokeCondition(AbstractModel):
    """触发器触发条件"""

    def __init__(self):
        """
                :param InvokeMethod: 触发方式
                :type InvokeMethod: str
                :param InvokeExpr: 触发表达式
        注意：此字段可能返回 null，表示取不到有效值。
                :type InvokeExpr: str
        """
        self.InvokeMethod = None
        self.InvokeExpr = None

    def _deserialize(self, params):
        self.InvokeMethod = params.get("InvokeMethod")
        self.InvokeExpr = params.get("InvokeExpr")


class TriggerInvokePara(AbstractModel):
    """触发器触发参数"""

    def __init__(self):
        """
                :param AppId: AppId
        注意：此字段可能返回 null，表示取不到有效值。
                :type AppId: str
                :param ClusterId: TKE集群ID
        注意：此字段可能返回 null，表示取不到有效值。
                :type ClusterId: str
                :param Namespace: TKE集群命名空间
        注意：此字段可能返回 null，表示取不到有效值。
                :type Namespace: str
                :param ServiceName: TKE集群工作负载名称
        注意：此字段可能返回 null，表示取不到有效值。
                :type ServiceName: str
                :param ContainerName: TKE集群工作负载中容器名称
        注意：此字段可能返回 null，表示取不到有效值。
                :type ContainerName: str
                :param ClusterRegion: TKE集群地域数字ID
        注意：此字段可能返回 null，表示取不到有效值。
                :type ClusterRegion: int
        """
        self.AppId = None
        self.ClusterId = None
        self.Namespace = None
        self.ServiceName = None
        self.ContainerName = None
        self.ClusterRegion = None

    def _deserialize(self, params):
        self.AppId = params.get("AppId")
        self.ClusterId = params.get("ClusterId")
        self.Namespace = params.get("Namespace")
        self.ServiceName = params.get("ServiceName")
        self.ContainerName = params.get("ContainerName")
        self.ClusterRegion = params.get("ClusterRegion")


class TriggerInvokeResult(AbstractModel):
    """触发器触发结果"""

    def __init__(self):
        """
                :param ReturnCode: 请求TKE返回值
        注意：此字段可能返回 null，表示取不到有效值。
                :type ReturnCode: int
                :param ReturnMsg: 请求TKE返回信息
        注意：此字段可能返回 null，表示取不到有效值。
                :type ReturnMsg: str
        """
        self.ReturnCode = None
        self.ReturnMsg = None

    def _deserialize(self, params):
        self.ReturnCode = params.get("ReturnCode")
        self.ReturnMsg = params.get("ReturnMsg")


class TriggerLogResp(AbstractModel):
    """触发器日志"""

    def __init__(self):
        """
                :param RepoName: 仓库名称
        注意：此字段可能返回 null，表示取不到有效值。
                :type RepoName: str
                :param TagName: Tag名称
        注意：此字段可能返回 null，表示取不到有效值。
                :type TagName: str
                :param TriggerName: 触发器名称
        注意：此字段可能返回 null，表示取不到有效值。
                :type TriggerName: str
                :param InvokeSource: 触发方式
        注意：此字段可能返回 null，表示取不到有效值。
                :type InvokeSource: str
                :param InvokeAction: 触发动作
        注意：此字段可能返回 null，表示取不到有效值。
                :type InvokeAction: str
                :param InvokeTime: 触发时间
        注意：此字段可能返回 null，表示取不到有效值。
                :type InvokeTime: str
                :param InvokeCondition: 触发条件
        注意：此字段可能返回 null，表示取不到有效值。
                :type InvokeCondition: :class:`tcecloud.tcr.v20190924.models.TriggerInvokeCondition`
                :param InvokePara: 触发参数
        注意：此字段可能返回 null，表示取不到有效值。
                :type InvokePara: :class:`tcecloud.tcr.v20190924.models.TriggerInvokePara`
                :param InvokeResult: 触发结果
        注意：此字段可能返回 null，表示取不到有效值。
                :type InvokeResult: :class:`tcecloud.tcr.v20190924.models.TriggerInvokeResult`
        """
        self.RepoName = None
        self.TagName = None
        self.TriggerName = None
        self.InvokeSource = None
        self.InvokeAction = None
        self.InvokeTime = None
        self.InvokeCondition = None
        self.InvokePara = None
        self.InvokeResult = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")
        self.TagName = params.get("TagName")
        self.TriggerName = params.get("TriggerName")
        self.InvokeSource = params.get("InvokeSource")
        self.InvokeAction = params.get("InvokeAction")
        self.InvokeTime = params.get("InvokeTime")
        if params.get("InvokeCondition") is not None:
            self.InvokeCondition = TriggerInvokeCondition()
            self.InvokeCondition._deserialize(params.get("InvokeCondition"))
        if params.get("InvokePara") is not None:
            self.InvokePara = TriggerInvokePara()
            self.InvokePara._deserialize(params.get("InvokePara"))
        if params.get("InvokeResult") is not None:
            self.InvokeResult = TriggerInvokeResult()
            self.InvokeResult._deserialize(params.get("InvokeResult"))


class TriggerResp(AbstractModel):
    """触发器返回值"""

    def __init__(self):
        """
                :param TriggerName: 触发器名称
        注意：此字段可能返回 null，表示取不到有效值。
                :type TriggerName: str
                :param InvokeSource: 触发来源
        注意：此字段可能返回 null，表示取不到有效值。
                :type InvokeSource: str
                :param InvokeAction: 触发动作
        注意：此字段可能返回 null，表示取不到有效值。
                :type InvokeAction: str
                :param CreateTime: 创建时间
        注意：此字段可能返回 null，表示取不到有效值。
                :type CreateTime: str
                :param UpdateTime: 更新时间
        注意：此字段可能返回 null，表示取不到有效值。
                :type UpdateTime: str
                :param InvokeCondition: 触发条件
        注意：此字段可能返回 null，表示取不到有效值。
                :type InvokeCondition: :class:`tcecloud.tcr.v20190924.models.TriggerInvokeCondition`
                :param InvokePara: 触发器参数
        注意：此字段可能返回 null，表示取不到有效值。
                :type InvokePara: :class:`tcecloud.tcr.v20190924.models.TriggerInvokePara`
        """
        self.TriggerName = None
        self.InvokeSource = None
        self.InvokeAction = None
        self.CreateTime = None
        self.UpdateTime = None
        self.InvokeCondition = None
        self.InvokePara = None

    def _deserialize(self, params):
        self.TriggerName = params.get("TriggerName")
        self.InvokeSource = params.get("InvokeSource")
        self.InvokeAction = params.get("InvokeAction")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        if params.get("InvokeCondition") is not None:
            self.InvokeCondition = TriggerInvokeCondition()
            self.InvokeCondition._deserialize(params.get("InvokeCondition"))
        if params.get("InvokePara") is not None:
            self.InvokePara = TriggerInvokePara()
            self.InvokePara._deserialize(params.get("InvokePara"))


class UserInfo(AbstractModel):
    """共享版用户信息"""

    def __init__(self):
        """
        :param Username: 用户名
        :type Username: str
        :param AppId: AppId
        :type AppId: int
        :param ApplicationToken: 密码
        :type ApplicationToken: str
        :param CreationTime: 创建时间
        :type CreationTime: str
        """
        self.Username = None
        self.AppId = None
        self.ApplicationToken = None
        self.CreationTime = None

    def _deserialize(self, params):
        self.Username = params.get("Username")
        self.AppId = params.get("AppId")
        self.ApplicationToken = params.get("ApplicationToken")
        self.CreationTime = params.get("CreationTime")


class UserIsExistsResp(AbstractModel):
    """用户是否存在"""

    def __init__(self):
        """
        :param IsExist: 用户是否存在
        :type IsExist: bool
        :param MainIsExist: 主账号是否存在
        :type MainIsExist: bool
        """
        self.IsExist = None
        self.MainIsExist = None

    def _deserialize(self, params):
        self.IsExist = params.get("IsExist")
        self.MainIsExist = params.get("MainIsExist")


class ValidateApplicationTokenPersonalRequest(AbstractModel):
    """ValidateApplicationTokenPersonal请求参数结构体"""

    def __init__(self):
        """
        :param ApplicationToken: 用户凭证
        :type ApplicationToken: str
        """
        self.ApplicationToken = None

    def _deserialize(self, params):
        self.ApplicationToken = params.get("ApplicationToken")


class ValidateApplicationTokenPersonalResponse(AbstractModel):
    """ValidateApplicationTokenPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 验证结果
        :type Data: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Data = params.get("Data")
        self.RequestId = params.get("RequestId")


class ValidateGitHubAuthPersonalRequest(AbstractModel):
    """ValidateGitHubAuthPersonal请求参数结构体"""

    def __init__(self):
        """
        :param Code: Code
        :type Code: str
        """
        self.Code = None

    def _deserialize(self, params):
        self.Code = params.get("Code")


class ValidateGitHubAuthPersonalResponse(AbstractModel):
    """ValidateGitHubAuthPersonal返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ValidateNamespaceExistPersonalRequest(AbstractModel):
    """ValidateNamespaceExistPersonal请求参数结构体"""

    def __init__(self):
        """
        :param Namespace: 命名空间名称
        :type Namespace: str
        """
        self.Namespace = None

    def _deserialize(self, params):
        self.Namespace = params.get("Namespace")


class ValidateNamespaceExistPersonalResponse(AbstractModel):
    """ValidateNamespaceExistPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 命名空间是否存在
        :type Data: :class:`tcecloud.tcr.v20190924.models.NamespaceIsExistsResp`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = NamespaceIsExistsResp()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class ValidateRepositoryExistPersonalRequest(AbstractModel):
    """ValidateRepositoryExistPersonal请求参数结构体"""

    def __init__(self):
        """
        :param RepoName: 仓库名称
        :type RepoName: str
        """
        self.RepoName = None

    def _deserialize(self, params):
        self.RepoName = params.get("RepoName")


class ValidateRepositoryExistPersonalResponse(AbstractModel):
    """ValidateRepositoryExistPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 仓库是否存在
        :type Data: :class:`tcecloud.tcr.v20190924.models.RepoIsExistResp`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = RepoIsExistResp()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class ValidateUserPersonalRequest(AbstractModel):
    """ValidateUserPersonal请求参数结构体"""

    def __init__(self):
        """
        :param Username: 自定义用户名
        :type Username: str
        """
        self.Username = None

    def _deserialize(self, params):
        self.Username = params.get("Username")


class ValidateUserPersonalResponse(AbstractModel):
    """ValidateUserPersonal返回参数结构体"""

    def __init__(self):
        """
        :param Data: 判断用户存在的返回值
        :type Data: :class:`tcecloud.tcr.v20190924.models.UserIsExistsResp`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = UserIsExistsResp()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")

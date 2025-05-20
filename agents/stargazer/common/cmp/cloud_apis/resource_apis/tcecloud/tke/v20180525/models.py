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


class AbnormalDetail(AbstractModel):
    """异常的资源详情"""

    def __init__(self):
        """
        :param Namespace: kubernetes namespace
        :type Namespace: str
        :param ResourceName: kubernetes资源名称
        :type ResourceName: str
        """
        self.Namespace = None
        self.ResourceName = None

    def _deserialize(self, params):
        self.Namespace = params.get("Namespace")
        self.ResourceName = params.get("ResourceName")


class AddAlarmPolicyRequest(AbstractModel):
    """AddAlarmPolicy请求参数结构体"""

    def __init__(self):
        """
        :param ClusterInstanceId: 集群ID
        :type ClusterInstanceId: str
        :param Namespace: 命名空间
        :type Namespace: str
        :param WorkloadType: 工作负载类型
        :type WorkloadType: str
        :param AlarmPolicySettings: 告警策略设置
        :type AlarmPolicySettings: :class:`tcecloud.tke.v20180525.models.AlarmPolicySettings`
        :param NotifySettings: 告警通知设置
        :type NotifySettings: :class:`tcecloud.tke.v20180525.models.NotifySettings`
        :param ShieldSettings: 告警屏蔽设置
        :type ShieldSettings: :class:`tcecloud.tke.v20180525.models.ShieldSettings`
        """
        self.ClusterInstanceId = None
        self.Namespace = None
        self.WorkloadType = None
        self.AlarmPolicySettings = None
        self.NotifySettings = None
        self.ShieldSettings = None

    def _deserialize(self, params):
        self.ClusterInstanceId = params.get("ClusterInstanceId")
        self.Namespace = params.get("Namespace")
        self.WorkloadType = params.get("WorkloadType")
        if params.get("AlarmPolicySettings") is not None:
            self.AlarmPolicySettings = AlarmPolicySettings()
            self.AlarmPolicySettings._deserialize(params.get("AlarmPolicySettings"))
        if params.get("NotifySettings") is not None:
            self.NotifySettings = NotifySettings()
            self.NotifySettings._deserialize(params.get("NotifySettings"))
        if params.get("ShieldSettings") is not None:
            self.ShieldSettings = ShieldSettings()
            self.ShieldSettings._deserialize(params.get("ShieldSettings"))


class AddAlarmPolicyResponse(AbstractModel):
    """AddAlarmPolicy返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AddClusterCIDRToCcnRequest(AbstractModel):
    """AddClusterCIDRToCcn请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: 私有网络ID，形如vpc-xxx。创建托管空集群时必传。
        :type VpcId: str
        :param ClusterCIDR: 用于分配集群容器和服务 IP 的 CIDR，不得与 VPC CIDR 冲突，也不得与同 VPC 内其他集群 CIDR 冲突
        :type ClusterCIDR: str
        """
        self.VpcId = None
        self.ClusterCIDR = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.ClusterCIDR = params.get("ClusterCIDR")


class AddClusterCIDRToCcnResponse(AbstractModel):
    """AddClusterCIDRToCcn返回参数结构体"""

    def __init__(self):
        """
        :param RouteSet: 云联网路由数组
        :type RouteSet: list of CcnRoute
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RouteSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("RouteSet") is not None:
            self.RouteSet = []
            for item in params.get("RouteSet"):
                obj = CcnRoute()
                obj._deserialize(item)
                self.RouteSet.append(obj)
        self.RequestId = params.get("RequestId")


class AddClusterCIDRToVbcRequest(AbstractModel):
    """AddClusterCIDRToVbc请求参数结构体"""

    def __init__(self):
        """
        :param UnVpcId: vpc唯一id
        :type UnVpcId: str
        :param ClusterCIDR: 集群cidr
        :type ClusterCIDR: str
        """
        self.UnVpcId = None
        self.ClusterCIDR = None

    def _deserialize(self, params):
        self.UnVpcId = params.get("UnVpcId")
        self.ClusterCIDR = params.get("ClusterCIDR")


class AddClusterCIDRToVbcResponse(AbstractModel):
    """AddClusterCIDRToVbc返回参数结构体"""

    def __init__(self):
        """
        :param Detail: 返回详情
        :type Detail: list of CcnRoute
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Detail = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Detail") is not None:
            self.Detail = []
            for item in params.get("Detail"):
                obj = CcnRoute()
                obj._deserialize(item)
                self.Detail.append(obj)
        self.RequestId = params.get("RequestId")


class AddClusterInstancesRequest(AbstractModel):
    """AddClusterInstances请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群 ID，请填写 查询集群列表 接口中返回的 clusterId 字段
        :type ClusterId: str
        :param CvmRunInstances: cvm创建透传参数，json化字符串格式
        :type CvmRunInstances: str
        :param MountTarget: 数据盘挂载点, 默认不挂载数据盘. 已格式化的 ext3，ext4，xfs 文件系统的数据盘将直接挂载，其他文件系统或未格式化的数据盘将自动格式化为ext4 并挂载，请注意备份数据! 无数据盘或有多块数据盘的云主机此设置不生效。
        :type MountTarget: list of str
        :param DockerGraphPath: dockerd --graph 指定值, 默认为 /var/lib/docker
        :type DockerGraphPath: list of str
        :param UserScript: base64 编码的用户脚本, 此脚本会在 k8s 组件运行后执行, 需要用户保证脚本的可重入及重试逻辑, 脚本及其生成的日志文件可在节点的 /data/ccs_userscript/ 路径查看, 如果要求节点需要在进行初始化完成后才可加入调度, 可配合 unschedulable 参数使用, 在 userScript 最后初始化完成后, 添加 kubectl uncordon nodename --kubeconfig=/root/.kube/config 命令使节点加入调度
        :type UserScript: list of str
        :param OsName: 系统名。centos7.2x86_64 或者 ubuntu16.04.1 LTSx86_64，仅当新建集群为空集群, 第一次向空集群添加节点时需要指定. 当集群系统确定后, 后续添加的节点都是集群系统
        :type OsName: str
        :param Unschedulable: 设置加入的节点是否参与调度，默认值为0，表示参与调度；非0表示不参与调度, 待节点初始化完成之后, 可执行kubectl uncordon nodename使node加入调度.
        :type Unschedulable: int
        """
        self.ClusterId = None
        self.CvmRunInstances = None
        self.MountTarget = None
        self.DockerGraphPath = None
        self.UserScript = None
        self.OsName = None
        self.Unschedulable = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.CvmRunInstances = params.get("CvmRunInstances")
        self.MountTarget = params.get("MountTarget")
        self.DockerGraphPath = params.get("DockerGraphPath")
        self.UserScript = params.get("UserScript")
        self.OsName = params.get("OsName")
        self.Unschedulable = params.get("Unschedulable")


class AddClusterInstancesResponse(AbstractModel):
    """AddClusterInstances返回参数结构体"""

    def __init__(self):
        """
        :param InstanceIdSet: 节点实例id
        :type InstanceIdSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceIdSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.InstanceIdSet = params.get("InstanceIdSet")
        self.RequestId = params.get("RequestId")


class AddExistedInstancesRequest(AbstractModel):
    """AddExistedInstances请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param InstanceIds: 实例列表
        :type InstanceIds: list of str
        :param InstanceAdvancedSettings: 实例额外需要设置参数信息
        :type InstanceAdvancedSettings: :class:`tcecloud.tke.v20180525.models.InstanceAdvancedSettings`
        :param EnhancedService: 增强服务。通过该参数可以指定是否开启云安全、云监控等服务。若不指定该参数，则默认开启云监控、云安全服务。
        :type EnhancedService: :class:`tcecloud.tke.v20180525.models.EnhancedService`
        :param LoginSettings: 节点登录信息（目前仅支持使用Password或者单个KeyIds）
        :type LoginSettings: :class:`tcecloud.tke.v20180525.models.LoginSettings`
        :param SecurityGroupIds: 实例所属安全组。该参数可以通过调用 DescribeSecurityGroups 的返回值中的sgId字段来获取。若不指定该参数，则绑定默认安全组。（目前仅支持设置单个sgId）
        :type SecurityGroupIds: list of str
        :param HostName: 重装系统时，可以指定修改实例的HostName(集群为HostName模式时，此参数必传，规则名称除不支持大写字符外与CVM创建实例接口HostName一致)
        :type HostName: str
        :param NodePool: 节点池选项
        :type NodePool: :class:`tcecloud.tke.v20180525.models.NodePoolOption`
        """
        self.ClusterId = None
        self.InstanceIds = None
        self.InstanceAdvancedSettings = None
        self.EnhancedService = None
        self.LoginSettings = None
        self.SecurityGroupIds = None
        self.HostName = None
        self.NodePool = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.InstanceIds = params.get("InstanceIds")
        if params.get("InstanceAdvancedSettings") is not None:
            self.InstanceAdvancedSettings = InstanceAdvancedSettings()
            self.InstanceAdvancedSettings._deserialize(params.get("InstanceAdvancedSettings"))
        if params.get("EnhancedService") is not None:
            self.EnhancedService = EnhancedService()
            self.EnhancedService._deserialize(params.get("EnhancedService"))
        if params.get("LoginSettings") is not None:
            self.LoginSettings = LoginSettings()
            self.LoginSettings._deserialize(params.get("LoginSettings"))
        self.SecurityGroupIds = params.get("SecurityGroupIds")
        self.HostName = params.get("HostName")
        if params.get("NodePool") is not None:
            self.NodePool = NodePoolOption()
            self.NodePool._deserialize(params.get("NodePool"))


class AddExistedInstancesResponse(AbstractModel):
    """AddExistedInstances返回参数结构体"""

    def __init__(self):
        """
        :param FailedInstanceIds: 失败的节点ID
        :type FailedInstanceIds: list of str
        :param SuccInstanceIds: 成功的节点ID
        :type SuccInstanceIds: list of str
        :param TimeoutInstanceIds: 超时未返回出来节点的ID(可能失败，也可能成功)
        :type TimeoutInstanceIds: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FailedInstanceIds = None
        self.SuccInstanceIds = None
        self.TimeoutInstanceIds = None
        self.RequestId = None

    def _deserialize(self, params):
        self.FailedInstanceIds = params.get("FailedInstanceIds")
        self.SuccInstanceIds = params.get("SuccInstanceIds")
        self.TimeoutInstanceIds = params.get("TimeoutInstanceIds")
        self.RequestId = params.get("RequestId")


class AlarmMetric(AbstractModel):
    """告警指标结构体"""

    def __init__(self):
        """
                :param ArgusPolicyName: 指标描述
                :type ArgusPolicyName: str
                :param Evaluator: 告警判断设置
                :type Evaluator: :class:`tcecloud.tke.v20180525.models.Evaluator`
                :param ContinuePeriod: 持续周期
                :type ContinuePeriod: int
                :param Status: 状态，true表示OK
                :type Status: bool
                :param MetricId: 告警指标ID
                :type MetricId: str
                :param Measurement: ARGUS系统Measurement
                :type Measurement: str
                :param StatisticsPeriod: 统计周期
                :type StatisticsPeriod: int
                :param MetricName: 指标名
                :type MetricName: str
                :param Unit: 指标单位
        注意：此字段可能返回 null，表示取不到有效值。
                :type Unit: str
        """
        self.ArgusPolicyName = None
        self.Evaluator = None
        self.ContinuePeriod = None
        self.Status = None
        self.MetricId = None
        self.Measurement = None
        self.StatisticsPeriod = None
        self.MetricName = None
        self.Unit = None

    def _deserialize(self, params):
        self.ArgusPolicyName = params.get("ArgusPolicyName")
        if params.get("Evaluator") is not None:
            self.Evaluator = Evaluator()
            self.Evaluator._deserialize(params.get("Evaluator"))
        self.ContinuePeriod = params.get("ContinuePeriod")
        self.Status = params.get("Status")
        self.MetricId = params.get("MetricId")
        self.Measurement = params.get("Measurement")
        self.StatisticsPeriod = params.get("StatisticsPeriod")
        self.MetricName = params.get("MetricName")
        self.Unit = params.get("Unit")


class AlarmPolicy(AbstractModel):
    """告警策略结构体"""

    def __init__(self):
        """
                :param AlarmPolicyId: 告警策略ID
                :type AlarmPolicyId: str
                :param ClusterInstanceId: k8s集群ID
                :type ClusterInstanceId: str
                :param Namespace: k8s命名空间
        注意：此字段可能返回 null，表示取不到有效值。
                :type Namespace: str
                :param WorkloadType: k8s工作负载类型
        注意：此字段可能返回 null，表示取不到有效值。
                :type WorkloadType: str
                :param AlarmPolicySettings: 告警策略settings
                :type AlarmPolicySettings: :class:`tcecloud.tke.v20180525.models.AlarmPolicySettings`
                :param NotifySettings: 告警通知settings
                :type NotifySettings: :class:`tcecloud.tke.v20180525.models.NotifySettings`
                :param ShieldSettings: 告警屏蔽settings
                :type ShieldSettings: :class:`tcecloud.tke.v20180525.models.ShieldSettings`
        """
        self.AlarmPolicyId = None
        self.ClusterInstanceId = None
        self.Namespace = None
        self.WorkloadType = None
        self.AlarmPolicySettings = None
        self.NotifySettings = None
        self.ShieldSettings = None

    def _deserialize(self, params):
        self.AlarmPolicyId = params.get("AlarmPolicyId")
        self.ClusterInstanceId = params.get("ClusterInstanceId")
        self.Namespace = params.get("Namespace")
        self.WorkloadType = params.get("WorkloadType")
        if params.get("AlarmPolicySettings") is not None:
            self.AlarmPolicySettings = AlarmPolicySettings()
            self.AlarmPolicySettings._deserialize(params.get("AlarmPolicySettings"))
        if params.get("NotifySettings") is not None:
            self.NotifySettings = NotifySettings()
            self.NotifySettings._deserialize(params.get("NotifySettings"))
        if params.get("ShieldSettings") is not None:
            self.ShieldSettings = ShieldSettings()
            self.ShieldSettings._deserialize(params.get("ShieldSettings"))


class AlarmPolicyFilter(AbstractModel):
    """告警策略过滤"""

    def __init__(self):
        """
        :param AlarmPolicyName: 告警策略名称
        :type AlarmPolicyName: str
        """
        self.AlarmPolicyName = None

    def _deserialize(self, params):
        self.AlarmPolicyName = params.get("AlarmPolicyName")


class AlarmPolicySettings(AbstractModel):
    """告警策略settings"""

    def __init__(self):
        """
                :param AlarmPolicyName: 告警策略名称
                :type AlarmPolicyName: str
                :param AlarmPolicyType: 告警类型，有cluster，node，pod三种类型。
                :type AlarmPolicyType: str
                :param AlarmMetrics: 告警指标列表。
                :type AlarmMetrics: list of AlarmMetric
                :param AlarmObjects: 告警对象，多个用逗号分隔。
        注意：此字段可能返回 null，表示取不到有效值。
                :type AlarmObjects: str
                :param AlarmPolicyDescription: 告警策略描述
        注意：此字段可能返回 null，表示取不到有效值。
                :type AlarmPolicyDescription: str
                :param AlarmObjectsType: 告警对象绑定类型。
        all：全部对象绑定。
        part：只有选择的部分对象绑定。
        注意：此字段可能返回 null，表示取不到有效值。
                :type AlarmObjectsType: str
        """
        self.AlarmPolicyName = None
        self.AlarmPolicyType = None
        self.AlarmMetrics = None
        self.AlarmObjects = None
        self.AlarmPolicyDescription = None
        self.AlarmObjectsType = None

    def _deserialize(self, params):
        self.AlarmPolicyName = params.get("AlarmPolicyName")
        self.AlarmPolicyType = params.get("AlarmPolicyType")
        if params.get("AlarmMetrics") is not None:
            self.AlarmMetrics = []
            for item in params.get("AlarmMetrics"):
                obj = AlarmMetric()
                obj._deserialize(item)
                self.AlarmMetrics.append(obj)
        self.AlarmObjects = params.get("AlarmObjects")
        self.AlarmPolicyDescription = params.get("AlarmPolicyDescription")
        self.AlarmObjectsType = params.get("AlarmObjectsType")


class AutoScalingGroupRange(AbstractModel):
    """集群关联的伸缩组最大实例数最小值实例数"""

    def __init__(self):
        """
        :param MinSize: 伸缩组最小实例数
        :type MinSize: int
        :param MaxSize: 伸缩组最大实例数
        :type MaxSize: int
        """
        self.MinSize = None
        self.MaxSize = None

    def _deserialize(self, params):
        self.MinSize = params.get("MinSize")
        self.MaxSize = params.get("MaxSize")


class AvailableExtraArgs(AbstractModel):
    """集群可用的自定义参数"""

    def __init__(self):
        """
                :param KubeAPIServer: kube-apiserver可用的自定义参数
        注意：此字段可能返回 null，表示取不到有效值。
                :type KubeAPIServer: list of Flag
                :param KubeControllerManager: kube-controller-manager可用的自定义参数
        注意：此字段可能返回 null，表示取不到有效值。
                :type KubeControllerManager: list of Flag
                :param KubeScheduler: kube-scheduler可用的自定义参数
        注意：此字段可能返回 null，表示取不到有效值。
                :type KubeScheduler: list of Flag
                :param Kubelet: kubelet可用的自定义参数
        注意：此字段可能返回 null，表示取不到有效值。
                :type Kubelet: list of Flag
        """
        self.KubeAPIServer = None
        self.KubeControllerManager = None
        self.KubeScheduler = None
        self.Kubelet = None

    def _deserialize(self, params):
        if params.get("KubeAPIServer") is not None:
            self.KubeAPIServer = []
            for item in params.get("KubeAPIServer"):
                obj = Flag()
                obj._deserialize(item)
                self.KubeAPIServer.append(obj)
        if params.get("KubeControllerManager") is not None:
            self.KubeControllerManager = []
            for item in params.get("KubeControllerManager"):
                obj = Flag()
                obj._deserialize(item)
                self.KubeControllerManager.append(obj)
        if params.get("KubeScheduler") is not None:
            self.KubeScheduler = []
            for item in params.get("KubeScheduler"):
                obj = Flag()
                obj._deserialize(item)
                self.KubeScheduler.append(obj)
        if params.get("Kubelet") is not None:
            self.Kubelet = []
            for item in params.get("Kubelet"):
                obj = Flag()
                obj._deserialize(item)
                self.Kubelet.append(obj)


class CcnInstance(AbstractModel):
    """云联网实例"""

    def __init__(self):
        """
                :param CcnId: 云联网实例ID
        注意：此字段可能返回 null，表示取不到有效值。
                :type CcnId: str
                :param InstanceType: 关联实例类型：
        VPC：私有网络
        DIRECTCONNECT：专线网关
        BMVPC：黑石私有网络
        注意：此字段可能返回 null，表示取不到有效值。
                :type InstanceType: str
                :param InstanceId: 关联实例ID
        注意：此字段可能返回 null，表示取不到有效值。
                :type InstanceId: str
                :param InstanceRegion: 关联实例所属大区，例如：ap-guangzhou
        注意：此字段可能返回 null，表示取不到有效值。
                :type InstanceRegion: str
                :param InstanceUin: 关联实例所属UIN（根账号
        注意：此字段可能返回 null，表示取不到有效值。
                :type InstanceUin: str
                :param Cidrs: 关联实例CIDR
        注意：此字段可能返回 null，表示取不到有效值。
                :type Cidrs: list of str
                :param State: 关联实例状态：
        PENDING：申请中
        ACTIVE：已连接
        EXPIRED：已过期
        REJECTED：已拒绝
        DELETED：已删除
        FAILED：失败的（2小时后将异步强制解关联）
        ATTACHING：关联中
        DETACHING：解关联中
        DETACHFAILED：解关联失败（2小时后将异步强制解关联）
        注意：此字段可能返回 null，表示取不到有效值。
                :type State: str
                :param CcnUin: 云联网所属UIN（根账号）
        注意：此字段可能返回 null，表示取不到有效值。
                :type CcnUin: str
        """
        self.CcnId = None
        self.InstanceType = None
        self.InstanceId = None
        self.InstanceRegion = None
        self.InstanceUin = None
        self.Cidrs = None
        self.State = None
        self.CcnUin = None

    def _deserialize(self, params):
        self.CcnId = params.get("CcnId")
        self.InstanceType = params.get("InstanceType")
        self.InstanceId = params.get("InstanceId")
        self.InstanceRegion = params.get("InstanceRegion")
        self.InstanceUin = params.get("InstanceUin")
        self.Cidrs = params.get("Cidrs")
        self.State = params.get("State")
        self.CcnUin = params.get("CcnUin")


class CcnRoute(AbstractModel):
    """用于查询/添加/删除集群cidr到云联网"""

    def __init__(self):
        """
                :param RouteId: 路由策略ID
        注意：此字段可能返回 null，表示取不到有效值。
                :type RouteId: str
                :param DestinationCidrBlock: 目的端
        注意：此字段可能返回 null，表示取不到有效值。
                :type DestinationCidrBlock: str
                :param InstanceType: 下一跳类型（关联实例类型），所有类型：VPC、DIRECTCONNECT
        注意：此字段可能返回 null，表示取不到有效值。
                :type InstanceType: str
                :param InstanceId: 下一跳（关联实例）
        注意：此字段可能返回 null，表示取不到有效值。
                :type InstanceId: str
                :param InstanceRegion: 下一跳所属地域（关联实例所属地域）
        注意：此字段可能返回 null，表示取不到有效值。
                :type InstanceRegion: str
                :param InstanceUin: 关联实例所属UIN（根账号）
        注意：此字段可能返回 null，表示取不到有效值。
                :type InstanceUin: str
        """
        self.RouteId = None
        self.DestinationCidrBlock = None
        self.InstanceType = None
        self.InstanceId = None
        self.InstanceRegion = None
        self.InstanceUin = None

    def _deserialize(self, params):
        self.RouteId = params.get("RouteId")
        self.DestinationCidrBlock = params.get("DestinationCidrBlock")
        self.InstanceType = params.get("InstanceType")
        self.InstanceId = params.get("InstanceId")
        self.InstanceRegion = params.get("InstanceRegion")
        self.InstanceUin = params.get("InstanceUin")


class CheckClusterCIDRRequest(AbstractModel):
    """CheckClusterCIDR请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: 集群的vpc-id
        :type VpcId: str
        :param ClusterCIDR: 集群的CIDR
        :type ClusterCIDR: str
        """
        self.VpcId = None
        self.ClusterCIDR = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.ClusterCIDR = params.get("ClusterCIDR")


class CheckClusterCIDRResponse(AbstractModel):
    """CheckClusterCIDR返回参数结构体"""

    def __init__(self):
        """
                :param IsConflict: 是否存在CIDR冲突。
                :type IsConflict: bool
                :param ConflictType: CIDR冲突的类型("CIDR_CONFLICT_WITH_OTHER_CLUSTER" 同VPC其他集群CIDR存在冲突
        "CIDR_CONFLICT_WITH_VPC_CIDR" 与VPC的CIDR存在冲突
        "CIDR_CONFLICT_WITH_VPC_GLOBAL_ROUTE" 与同VPC的全局路由存在冲突)。
                :type ConflictType: str
                :param ConflictMsg: CIDR冲突描述信息。
                :type ConflictMsg: str
                :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
                :type RequestId: str
        """
        self.IsConflict = None
        self.ConflictType = None
        self.ConflictMsg = None
        self.RequestId = None

    def _deserialize(self, params):
        self.IsConflict = params.get("IsConflict")
        self.ConflictType = params.get("ConflictType")
        self.ConflictMsg = params.get("ConflictMsg")
        self.RequestId = params.get("RequestId")


class CheckClusterHostNameRequest(AbstractModel):
    """CheckClusterHostName请求参数结构体"""

    def __init__(self):
        """
        :param HostNames: 节点主机名称列表
        :type HostNames: list of HostNameValue
        :param ClusterId: 集群ID(如果往已经存在的集群内加节点，则需要传对应的集群ID)
        :type ClusterId: str
        """
        self.HostNames = None
        self.ClusterId = None

    def _deserialize(self, params):
        if params.get("HostNames") is not None:
            self.HostNames = []
            for item in params.get("HostNames"):
                obj = HostNameValue()
                obj._deserialize(item)
                self.HostNames.append(obj)
        self.ClusterId = params.get("ClusterId")


class CheckClusterHostNameResponse(AbstractModel):
    """CheckClusterHostName返回参数结构体"""

    def __init__(self):
        """
        :param BEnable: 节点主机名校验是否通过(true: 通过 false: 不通过 )
        :type BEnable: bool
        :param ErrMsg: 节点主机名校验不通过的原因
        :type ErrMsg: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.BEnable = None
        self.ErrMsg = None
        self.RequestId = None

    def _deserialize(self, params):
        self.BEnable = params.get("BEnable")
        self.ErrMsg = params.get("ErrMsg")
        self.RequestId = params.get("RequestId")


class CheckClusterImageRequest(AbstractModel):
    """CheckClusterImage请求参数结构体"""

    def __init__(self):
        """
        :param ImageId: 指定有效的镜像ID，格式形如img-xxxx。可通过登录控制台查询，也可调用接口 DescribeImages，取返回信息中的ImageId字段。
        :type ImageId: str
        """
        self.ImageId = None

    def _deserialize(self, params):
        self.ImageId = params.get("ImageId")


class CheckClusterImageResponse(AbstractModel):
    """CheckClusterImage返回参数结构体"""

    def __init__(self):
        """
        :param Suitable: 是否支持设置为集群镜像
        :type Suitable: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Suitable = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Suitable = params.get("Suitable")
        self.RequestId = params.get("RequestId")


class CheckInstancesUpgradeAbleRequest(AbstractModel):
    """CheckInstancesUpgradeAble请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param InstanceIds: 节点列表
        :type InstanceIds: list of str
        :param UpgradeType: 升级类型
        :type UpgradeType: str
        """
        self.ClusterId = None
        self.InstanceIds = None
        self.UpgradeType = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.InstanceIds = params.get("InstanceIds")
        self.UpgradeType = params.get("UpgradeType")


class CheckInstancesUpgradeAbleResponse(AbstractModel):
    """CheckInstancesUpgradeAble返回参数结构体"""

    def __init__(self):
        """
        :param ClusterVersion: 集群master当前小版本
        :type ClusterVersion: str
        :param LatestVersion: 集群master对应的大版本目前最新小版本
        :type LatestVersion: str
        :param UpgradeAbleInstances: 可升级节点列表
        :type UpgradeAbleInstances: list of UpgradeAbleInstancesItem
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ClusterVersion = None
        self.LatestVersion = None
        self.UpgradeAbleInstances = None
        self.RequestId = None

    def _deserialize(self, params):
        self.ClusterVersion = params.get("ClusterVersion")
        self.LatestVersion = params.get("LatestVersion")
        if params.get("UpgradeAbleInstances") is not None:
            self.UpgradeAbleInstances = []
            for item in params.get("UpgradeAbleInstances"):
                obj = UpgradeAbleInstancesItem()
                obj._deserialize(item)
                self.UpgradeAbleInstances.append(obj)
        self.RequestId = params.get("RequestId")


class CheckLogCollectorHostPathRequest(AbstractModel):
    """CheckLogCollectorHostPath请求参数结构体"""

    def __init__(self):
        """
        :param Path: 路径名
        :type Path: str
        """
        self.Path = None

    def _deserialize(self, params):
        self.Path = params.get("Path")


class CheckLogCollectorHostPathResponse(AbstractModel):
    """CheckLogCollectorHostPath返回参数结构体"""

    def __init__(self):
        """
        :param Result: 主机路径是否合法
        :type Result: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Result = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Result = params.get("Result")
        self.RequestId = params.get("RequestId")


class CheckLogCollectorNameRequest(AbstractModel):
    """CheckLogCollectorName请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param LogCollectorName: 日志采集规则名称
        :type LogCollectorName: str
        """
        self.ClusterId = None
        self.LogCollectorName = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.LogCollectorName = params.get("LogCollectorName")


class CheckLogCollectorNameResponse(AbstractModel):
    """CheckLogCollectorName返回参数结构体"""

    def __init__(self):
        """
        :param Result: 日志采集规则是否存在（true：存在，false：不存在）
        :type Result: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Result = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Result = params.get("Result")
        self.RequestId = params.get("RequestId")


class Cluster(AbstractModel):
    """集群信息结构体"""

    def __init__(self):
        """
                :param ClusterId: 集群ID
                :type ClusterId: str
                :param ClusterName: 集群名称
                :type ClusterName: str
                :param ClusterDescription: 集群描述
                :type ClusterDescription: str
                :param ClusterVersion: 集群版本（默认值为1.10.5）
                :type ClusterVersion: str
                :param ClusterOs: 集群系统。centos7.2x86_64 或者 ubuntu16.04.1 LTSx86_64，默认取值为ubuntu16.04.1 LTSx86_64
                :type ClusterOs: str
                :param ClusterType: 集群类型，托管集群：MANAGED_CLUSTER，独立集群：INDEPENDENT_CLUSTER。
                :type ClusterType: str
                :param ClusterNetworkSettings: 集群网络相关参数
                :type ClusterNetworkSettings: :class:`tcecloud.tke.v20180525.models.ClusterNetworkSettings`
                :param ClusterNodeNum: 集群当前node数量
                :type ClusterNodeNum: int
                :param ProjectId: 集群所属的项目ID
                :type ProjectId: int
                :param TagSpecification: 标签描述列表。
        注意：此字段可能返回 null，表示取不到有效值。
                :type TagSpecification: list of TagSpecification
                :param ClusterStatus: 集群状态 (Running 运行中  Creating 创建中 Abnormal 异常  )
                :type ClusterStatus: str
                :param Property: 集群属性(包括集群不同属性的MAP，属性字段包括NodeNameType (lan-ip模式和hostname 模式，默认无lan-ip模式))
        注意：此字段可能返回 null，表示取不到有效值。
                :type Property: str
                :param ClusterMaterNodeNum: 集群当前master数量
                :type ClusterMaterNodeNum: int
                :param ImageId: 集群使用镜像id
        注意：此字段可能返回 null，表示取不到有效值。
                :type ImageId: str
                :param OsCustomizeType: OsCustomizeType
        注意：此字段可能返回 null，表示取不到有效值。
                :type OsCustomizeType: str
                :param ContainerRuntime: 集群运行环境docker或container
        注意：此字段可能返回 null，表示取不到有效值。
                :type ContainerRuntime: str
                :param CreatedTime: 创建时间
        注意：此字段可能返回 null，表示取不到有效值。
                :type CreatedTime: str
        """
        self.ClusterId = None
        self.ClusterName = None
        self.ClusterDescription = None
        self.ClusterVersion = None
        self.ClusterOs = None
        self.ClusterType = None
        self.ClusterNetworkSettings = None
        self.ClusterNodeNum = None
        self.ProjectId = None
        self.TagSpecification = None
        self.ClusterStatus = None
        self.Property = None
        self.ClusterMaterNodeNum = None
        self.ImageId = None
        self.OsCustomizeType = None
        self.ContainerRuntime = None
        self.CreatedTime = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.ClusterName = params.get("ClusterName")
        self.ClusterDescription = params.get("ClusterDescription")
        self.ClusterVersion = params.get("ClusterVersion")
        self.ClusterOs = params.get("ClusterOs")
        self.ClusterType = params.get("ClusterType")
        if params.get("ClusterNetworkSettings") is not None:
            self.ClusterNetworkSettings = ClusterNetworkSettings()
            self.ClusterNetworkSettings._deserialize(params.get("ClusterNetworkSettings"))
        self.ClusterNodeNum = params.get("ClusterNodeNum")
        self.ProjectId = params.get("ProjectId")
        if params.get("TagSpecification") is not None:
            self.TagSpecification = []
            for item in params.get("TagSpecification"):
                obj = TagSpecification()
                obj._deserialize(item)
                self.TagSpecification.append(obj)
        self.ClusterStatus = params.get("ClusterStatus")
        self.Property = params.get("Property")
        self.ClusterMaterNodeNum = params.get("ClusterMaterNodeNum")
        self.ImageId = params.get("ImageId")
        self.OsCustomizeType = params.get("OsCustomizeType")
        self.ContainerRuntime = params.get("ContainerRuntime")
        self.CreatedTime = params.get("CreatedTime")


class ClusterAdvancedSettings(AbstractModel):
    """集群高级配置"""

    def __init__(self):
        """
        :param IPVS: 是否启用IPVS
        :type IPVS: bool
        :param AsEnabled: 是否启用集群节点自动扩缩容(创建集群流程不支持开启此功能)
        :type AsEnabled: bool
        :param ContainerRuntime: 集群使用的runtime类型，包括"docker"和"containerd"两种类型，默认为"docker"
        :type ContainerRuntime: str
        :param NodeNameType: 集群中节点NodeName类型（包括 hostname,lan-ip两种形式，默认为lan-ip。如果开启了hostname模式，创建节点时需要设置HostName参数，并且InstanceName需要和HostName一致）
        :type NodeNameType: str
        :param ExtraArgs: 集群自定义参数
        :type ExtraArgs: :class:`tcecloud.tke.v20180525.models.ClusterExtraArgs`
        :param NetworkType: 集群网络类型（包括GR(全局路由)和VPC-CNI两种模式，默认为GR。
        :type NetworkType: str
        :param IsNonStaticIpMode: 集群VPC-CNI模式是否为非固定IP，默认: FALSE 固定IP。
        :type IsNonStaticIpMode: bool
        """
        self.IPVS = None
        self.AsEnabled = None
        self.ContainerRuntime = None
        self.NodeNameType = None
        self.ExtraArgs = None
        self.NetworkType = None
        self.IsNonStaticIpMode = None

    def _deserialize(self, params):
        self.IPVS = params.get("IPVS")
        self.AsEnabled = params.get("AsEnabled")
        self.ContainerRuntime = params.get("ContainerRuntime")
        self.NodeNameType = params.get("NodeNameType")
        if params.get("ExtraArgs") is not None:
            self.ExtraArgs = ClusterExtraArgs()
            self.ExtraArgs._deserialize(params.get("ExtraArgs"))
        self.NetworkType = params.get("NetworkType")
        self.IsNonStaticIpMode = params.get("IsNonStaticIpMode")


class ClusterAsGroup(AbstractModel):
    """集群关联的伸缩组信息"""

    def __init__(self):
        """
                :param AutoScalingGroupId: 伸缩组ID
                :type AutoScalingGroupId: str
                :param Status: 伸缩组状态(开启 enabled 开启中 enabling 关闭 disabled 关闭中 disabling 更新中 updating 删除中 deleting 开启缩容中 scaleDownEnabling 关闭缩容中 scaleDownDisabling)
                :type Status: str
                :param IsUnschedulable: 节点是否设置成不可调度
        注意：此字段可能返回 null，表示取不到有效值。
                :type IsUnschedulable: bool
                :param Labels: 伸缩组的label列表
        注意：此字段可能返回 null，表示取不到有效值。
                :type Labels: list of Label
        """
        self.AutoScalingGroupId = None
        self.Status = None
        self.IsUnschedulable = None
        self.Labels = None

    def _deserialize(self, params):
        self.AutoScalingGroupId = params.get("AutoScalingGroupId")
        self.Status = params.get("Status")
        self.IsUnschedulable = params.get("IsUnschedulable")
        if params.get("Labels") is not None:
            self.Labels = []
            for item in params.get("Labels"):
                obj = Label()
                obj._deserialize(item)
                self.Labels.append(obj)


class ClusterAsGroupAttribute(AbstractModel):
    """集群伸缩组属性"""

    def __init__(self):
        """
        :param AutoScalingGroupId: 伸缩组ID
        :type AutoScalingGroupId: str
        :param AutoScalingGroupEnabled: 是否开启
        :type AutoScalingGroupEnabled: bool
        :param AutoScalingGroupRange: 伸缩组最大最小实例数
        :type AutoScalingGroupRange: :class:`tcecloud.tke.v20180525.models.AutoScalingGroupRange`
        """
        self.AutoScalingGroupId = None
        self.AutoScalingGroupEnabled = None
        self.AutoScalingGroupRange = None

    def _deserialize(self, params):
        self.AutoScalingGroupId = params.get("AutoScalingGroupId")
        self.AutoScalingGroupEnabled = params.get("AutoScalingGroupEnabled")
        if params.get("AutoScalingGroupRange") is not None:
            self.AutoScalingGroupRange = AutoScalingGroupRange()
            self.AutoScalingGroupRange._deserialize(params.get("AutoScalingGroupRange"))


class ClusterAsGroupOption(AbstractModel):
    """集群弹性伸缩配置"""

    def __init__(self):
        """
                :param IsScaleDownEnabled: 是否开启缩容
        注意：此字段可能返回 null，表示取不到有效值。
                :type IsScaleDownEnabled: bool
                :param Expander: 多伸缩组情况下扩容选择算法(random 随机选择，most-pods 最多类型的Pod least-waste 最少的资源浪费，默认为random)
        注意：此字段可能返回 null，表示取不到有效值。
                :type Expander: str
                :param MaxEmptyBulkDelete: 最大并发缩容数
        注意：此字段可能返回 null，表示取不到有效值。
                :type MaxEmptyBulkDelete: int
                :param ScaleDownDelay: 集群扩容后多少分钟开始判断缩容（默认为10分钟）
        注意：此字段可能返回 null，表示取不到有效值。
                :type ScaleDownDelay: int
                :param ScaleDownUnneededTime: 节点连续空闲多少分钟后被缩容（默认为 10分钟）
        注意：此字段可能返回 null，表示取不到有效值。
                :type ScaleDownUnneededTime: int
                :param ScaleDownUtilizationThreshold: 节点资源使用量低于多少(百分比)时认为空闲(默认: 50(百分比))
        注意：此字段可能返回 null，表示取不到有效值。
                :type ScaleDownUtilizationThreshold: int
                :param SkipNodesWithLocalStorage: 含有本地存储Pod的节点是否不缩容(默认： FALSE)
        注意：此字段可能返回 null，表示取不到有效值。
                :type SkipNodesWithLocalStorage: bool
                :param SkipNodesWithSystemPods: 含有kube-system namespace下非DaemonSet管理的Pod的节点是否不缩容 (默认： FALSE)
        注意：此字段可能返回 null，表示取不到有效值。
                :type SkipNodesWithSystemPods: bool
                :param IgnoreDaemonSetsUtilization: 计算资源使用量时是否默认忽略DaemonSet的实例(默认值: False，不忽略)
        注意：此字段可能返回 null，表示取不到有效值。
                :type IgnoreDaemonSetsUtilization: bool
        """
        self.IsScaleDownEnabled = None
        self.Expander = None
        self.MaxEmptyBulkDelete = None
        self.ScaleDownDelay = None
        self.ScaleDownUnneededTime = None
        self.ScaleDownUtilizationThreshold = None
        self.SkipNodesWithLocalStorage = None
        self.SkipNodesWithSystemPods = None
        self.IgnoreDaemonSetsUtilization = None

    def _deserialize(self, params):
        self.IsScaleDownEnabled = params.get("IsScaleDownEnabled")
        self.Expander = params.get("Expander")
        self.MaxEmptyBulkDelete = params.get("MaxEmptyBulkDelete")
        self.ScaleDownDelay = params.get("ScaleDownDelay")
        self.ScaleDownUnneededTime = params.get("ScaleDownUnneededTime")
        self.ScaleDownUtilizationThreshold = params.get("ScaleDownUtilizationThreshold")
        self.SkipNodesWithLocalStorage = params.get("SkipNodesWithLocalStorage")
        self.SkipNodesWithSystemPods = params.get("SkipNodesWithSystemPods")
        self.IgnoreDaemonSetsUtilization = params.get("IgnoreDaemonSetsUtilization")


class ClusterBasicSettings(AbstractModel):
    """描述集群的基本配置信息"""

    def __init__(self):
        """
        :param ClusterOs: 集群系统。centos7.2x86_64 或者 ubuntu16.04.1 LTSx86_64，默认取值为ubuntu16.04.1 LTSx86_64
        :type ClusterOs: str
        :param ClusterVersion: 集群版本,默认值为1.10.5
        :type ClusterVersion: str
        :param ClusterName: 集群名称
        :type ClusterName: str
        :param ClusterDescription: 集群描述
        :type ClusterDescription: str
        :param VpcId: 私有网络ID，形如vpc-xxx。创建托管空集群时必传。
        :type VpcId: str
        :param ProjectId: 集群内新增资源所属项目ID。
        :type ProjectId: int
        :param TagSpecification: 标签描述列表。通过指定该参数可以同时绑定标签到相应的资源实例，当前仅支持绑定标签到集群实例。
        :type TagSpecification: list of TagSpecification
        :param OsCustomizeType: 容器的镜像版本，"DOCKER_CUSTOMIZE"(容器定制版),"GENERAL"(普通版本，默认值)
        :type OsCustomizeType: str
        :param NeedWorkSecurityGroup: 是否开启节点的默认安全组(默认: 否，Aphla特性)
        :type NeedWorkSecurityGroup: bool
        """
        self.ClusterOs = None
        self.ClusterVersion = None
        self.ClusterName = None
        self.ClusterDescription = None
        self.VpcId = None
        self.ProjectId = None
        self.TagSpecification = None
        self.OsCustomizeType = None
        self.NeedWorkSecurityGroup = None

    def _deserialize(self, params):
        self.ClusterOs = params.get("ClusterOs")
        self.ClusterVersion = params.get("ClusterVersion")
        self.ClusterName = params.get("ClusterName")
        self.ClusterDescription = params.get("ClusterDescription")
        self.VpcId = params.get("VpcId")
        self.ProjectId = params.get("ProjectId")
        if params.get("TagSpecification") is not None:
            self.TagSpecification = []
            for item in params.get("TagSpecification"):
                obj = TagSpecification()
                obj._deserialize(item)
                self.TagSpecification.append(obj)
        self.OsCustomizeType = params.get("OsCustomizeType")
        self.NeedWorkSecurityGroup = params.get("NeedWorkSecurityGroup")


class ClusterCIDRSettings(AbstractModel):
    """集群容器网络相关参数"""

    def __init__(self):
        """
        :param ClusterCIDR: 用于分配集群容器和服务 IP 的 CIDR，不得与 VPC CIDR 冲突，也不得与同 VPC 内其他集群 CIDR 冲突。且网段范围必须在内网网段内，例如:10.1.0.0/14, 192.168.0.1/18,172.16.0.0/16。
        :type ClusterCIDR: str
        :param IgnoreClusterCIDRConflict: 是否忽略 ClusterCIDR 冲突错误, 默认不忽略
        :type IgnoreClusterCIDRConflict: bool
        :param MaxNodePodNum: 集群中每个Node上最大的Pod数量。取值范围4～256。不为2的幂值时会向上取最接近的2的幂值。
        :type MaxNodePodNum: int
        :param MaxClusterServiceNum: 集群最大的service数量。取值范围32～32768，不为2的幂值时会向上取最接近的2的幂值。
        :type MaxClusterServiceNum: int
        :param ServiceCIDR: 用于分配集群服务 IP 的 CIDR，不得与 VPC CIDR 冲突，也不得与同 VPC 内其他集群 CIDR 冲突。且网段范围必须在内网网段内，例如:10.1.0.0/14, 192.168.0.1/18,172.16.0.0/16。
        :type ServiceCIDR: str
        :param EniSubnetIds: VPC-CNI网络模式下，弹性网卡的子网Id。
        :type EniSubnetIds: list of str
        :param ClaimExpiredSeconds: VPC-CNI网络模式下，弹性网卡IP的回收时间，取值范围[300,15768000)
        :type ClaimExpiredSeconds: int
        """
        self.ClusterCIDR = None
        self.IgnoreClusterCIDRConflict = None
        self.MaxNodePodNum = None
        self.MaxClusterServiceNum = None
        self.ServiceCIDR = None
        self.EniSubnetIds = None
        self.ClaimExpiredSeconds = None

    def _deserialize(self, params):
        self.ClusterCIDR = params.get("ClusterCIDR")
        self.IgnoreClusterCIDRConflict = params.get("IgnoreClusterCIDRConflict")
        self.MaxNodePodNum = params.get("MaxNodePodNum")
        self.MaxClusterServiceNum = params.get("MaxClusterServiceNum")
        self.ServiceCIDR = params.get("ServiceCIDR")
        self.EniSubnetIds = params.get("EniSubnetIds")
        self.ClaimExpiredSeconds = params.get("ClaimExpiredSeconds")


class ClusterExtraArgs(AbstractModel):
    """集群master自定义参数"""

    def __init__(self):
        """
                :param KubeAPIServer: kube-apiserver自定义参数
        注意：此字段可能返回 null，表示取不到有效值。
                :type KubeAPIServer: list of str
                :param KubeControllerManager: kube-controller-manager自定义参数
        注意：此字段可能返回 null，表示取不到有效值。
                :type KubeControllerManager: list of str
                :param KubeScheduler: kube-scheduler自定义参数
        注意：此字段可能返回 null，表示取不到有效值。
                :type KubeScheduler: list of str
        """
        self.KubeAPIServer = None
        self.KubeControllerManager = None
        self.KubeScheduler = None

    def _deserialize(self, params):
        self.KubeAPIServer = params.get("KubeAPIServer")
        self.KubeControllerManager = params.get("KubeControllerManager")
        self.KubeScheduler = params.get("KubeScheduler")


class ClusterHealthyPodsStatus(AbstractModel):
    """集群健康检查中pod的健康情况"""

    def __init__(self):
        """
                :param Total: pod总数
                :type Total: int
                :param NotReadyTotal: NotReady的pod总数
                :type NotReadyTotal: int
                :param NotReadyPods: NotReady的pod详细信息
        注意：此字段可能返回 null，表示取不到有效值。
                :type NotReadyPods: list of NotReadyPodsItem
        """
        self.Total = None
        self.NotReadyTotal = None
        self.NotReadyPods = None

    def _deserialize(self, params):
        self.Total = params.get("Total")
        self.NotReadyTotal = params.get("NotReadyTotal")
        if params.get("NotReadyPods") is not None:
            self.NotReadyPods = []
            for item in params.get("NotReadyPods"):
                obj = NotReadyPodsItem()
                obj._deserialize(item)
                self.NotReadyPods.append(obj)


class ClusterInspectionOverview(AbstractModel):
    """集群巡检一次检测的概览"""

    def __init__(self):
        """
                :param Id: 本次检查的id，用于与其他检测结果区分
                :type Id: str
                :param StartTime: 检查的时间
                :type StartTime: str
                :param Error: 如果检查异常终止，则该字段包含错误信息
        注意：此字段可能返回 null，表示取不到有效值。
                :type Error: str
                :param GoodItem: 正常项总数
        注意：此字段可能返回 null，表示取不到有效值。
                :type GoodItem: int
                :param WarnItem: 警告项总数
        注意：此字段可能返回 null，表示取不到有效值。
                :type WarnItem: int
                :param RiskItem: 高风险项总数
        注意：此字段可能返回 null，表示取不到有效值。
                :type RiskItem: int
                :param SeriousItem: 严重项总数
        注意：此字段可能返回 null，表示取不到有效值。
                :type SeriousItem: int
                :param FailedItem: 检测失败项总数
        注意：此字段可能返回 null，表示取不到有效值。
                :type FailedItem: int
        """
        self.Id = None
        self.StartTime = None
        self.Error = None
        self.GoodItem = None
        self.WarnItem = None
        self.RiskItem = None
        self.SeriousItem = None
        self.FailedItem = None

    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.StartTime = params.get("StartTime")
        self.Error = params.get("Error")
        self.GoodItem = params.get("GoodItem")
        self.WarnItem = params.get("WarnItem")
        self.RiskItem = params.get("RiskItem")
        self.SeriousItem = params.get("SeriousItem")
        self.FailedItem = params.get("FailedItem")


class ClusterInspectionProgress(AbstractModel):
    """集群巡检当前进度"""

    def __init__(self):
        """
                :param Step: 当前步骤名称：
        init_env: 初始化环境，安装agent。
        init_k8s_resources：获取kubernetes资源
        init_components: 获取核心组件参数
        init_machines：获取节点系统参数
        diagnostic： 正在检查集群
                :type Step: str
                :param Percent: 检查进度百分比
                :type Percent: float
        """
        self.Step = None
        self.Percent = None

    def _deserialize(self, params):
        self.Step = params.get("Step")
        self.Percent = params.get("Percent")


class ClusterInstancesVersion(AbstractModel):
    """集群中worker节点不同版本节点数统计信息"""

    def __init__(self):
        """
                :param ClusterId: 集群ID
                :type ClusterId: str
                :param ClusterVersion: 集群版本
                :type ClusterVersion: str
                :param InstanceVersions: 节点版本统计信息
                :type InstanceVersions: list of ClusterInstancesVersionItem
                :param Error: 出错信息
        注意：此字段可能返回 null，表示取不到有效值。
                :type Error: str
                :param UpgradeAble: 是否存在可升级节点
        注意：此字段可能返回 null，表示取不到有效值。
                :type UpgradeAble: bool
        """
        self.ClusterId = None
        self.ClusterVersion = None
        self.InstanceVersions = None
        self.Error = None
        self.UpgradeAble = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.ClusterVersion = params.get("ClusterVersion")
        if params.get("InstanceVersions") is not None:
            self.InstanceVersions = []
            for item in params.get("InstanceVersions"):
                obj = ClusterInstancesVersionItem()
                obj._deserialize(item)
                self.InstanceVersions.append(obj)
        self.Error = params.get("Error")
        self.UpgradeAble = params.get("UpgradeAble")


class ClusterInstancesVersionItem(AbstractModel):
    """集群中某个版本的worker节点数目"""

    def __init__(self):
        """
                :param InstanceVersion: 版本
                :type InstanceVersion: str
                :param Total: 节点数
                :type Total: int
                :param UpgradeAble: 是否可升级
        注意：此字段可能返回 null，表示取不到有效值。
                :type UpgradeAble: bool
        """
        self.InstanceVersion = None
        self.Total = None
        self.UpgradeAble = None

    def _deserialize(self, params):
        self.InstanceVersion = params.get("InstanceVersion")
        self.Total = params.get("Total")
        self.UpgradeAble = params.get("UpgradeAble")


class ClusterNetworkSettings(AbstractModel):
    """集群网络相关的参数"""

    def __init__(self):
        """
        :param ClusterCIDR: 用于分配集群容器和服务 IP 的 CIDR，不得与 VPC CIDR 冲突，也不得与同 VPC 内其他集群 CIDR 冲突
        :type ClusterCIDR: str
        :param IgnoreClusterCIDRConflict: 是否忽略 ClusterCIDR 冲突错误, 默认不忽略
        :type IgnoreClusterCIDRConflict: bool
        :param MaxNodePodNum: 集群中每个Node上最大的Pod数量(默认为256)
        :type MaxNodePodNum: int
        :param MaxClusterServiceNum: 集群最大的service数量(默认为256)
        :type MaxClusterServiceNum: int
        :param Ipvs: 是否启用IPVS(默认不开启)
        :type Ipvs: bool
        :param VpcId: 集群的VPCID（如果创建空集群，为必传值，否则自动设置为和集群的节点保持一致）
        :type VpcId: str
        :param Cni: 网络插件是否启用CNI(默认开启)
        :type Cni: bool
        """
        self.ClusterCIDR = None
        self.IgnoreClusterCIDRConflict = None
        self.MaxNodePodNum = None
        self.MaxClusterServiceNum = None
        self.Ipvs = None
        self.VpcId = None
        self.Cni = None

    def _deserialize(self, params):
        self.ClusterCIDR = params.get("ClusterCIDR")
        self.IgnoreClusterCIDRConflict = params.get("IgnoreClusterCIDRConflict")
        self.MaxNodePodNum = params.get("MaxNodePodNum")
        self.MaxClusterServiceNum = params.get("MaxClusterServiceNum")
        self.Ipvs = params.get("Ipvs")
        self.VpcId = params.get("VpcId")
        self.Cni = params.get("Cni")


class ClusterStatus(AbstractModel):
    """集群状态信息"""

    def __init__(self):
        """
                :param ClusterId: 集群Id
                :type ClusterId: str
                :param ClusterState: 集群状态
                :type ClusterState: str
                :param ClusterInstanceState: 集群下机器实例的状态
                :type ClusterInstanceState: str
                :param ClusterBMonitor: 集群是否开启监控
                :type ClusterBMonitor: bool
                :param ClusterInitNodeNum: 集群创建中的节点数，-1表示获取节点状态超时，-2表示获取节点状态失败
                :type ClusterInitNodeNum: int
                :param ClusterRunningNodeNum: 集群运行中的节点数，-1表示获取节点状态超时，-2表示获取节点状态失败
                :type ClusterRunningNodeNum: int
                :param ClusterFailedNodeNum: 集群异常的节点数，-1表示获取节点状态超时，-2表示获取节点状态失败
                :type ClusterFailedNodeNum: int
                :param ClusterClosedNodeNum: 集群已关机的节点数，-1表示获取节点状态超时，-2表示获取节点状态失败
        注意：此字段可能返回 null，表示取不到有效值。
                :type ClusterClosedNodeNum: int
                :param ClusterClosingNodeNum: 集群关机中的节点数，-1表示获取节点状态超时，-2表示获取节点状态失败
        注意：此字段可能返回 null，表示取不到有效值。
                :type ClusterClosingNodeNum: int
        """
        self.ClusterId = None
        self.ClusterState = None
        self.ClusterInstanceState = None
        self.ClusterBMonitor = None
        self.ClusterInitNodeNum = None
        self.ClusterRunningNodeNum = None
        self.ClusterFailedNodeNum = None
        self.ClusterClosedNodeNum = None
        self.ClusterClosingNodeNum = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.ClusterState = params.get("ClusterState")
        self.ClusterInstanceState = params.get("ClusterInstanceState")
        self.ClusterBMonitor = params.get("ClusterBMonitor")
        self.ClusterInitNodeNum = params.get("ClusterInitNodeNum")
        self.ClusterRunningNodeNum = params.get("ClusterRunningNodeNum")
        self.ClusterFailedNodeNum = params.get("ClusterFailedNodeNum")
        self.ClusterClosedNodeNum = params.get("ClusterClosedNodeNum")
        self.ClusterClosingNodeNum = params.get("ClusterClosingNodeNum")


class ContainerStatus(AbstractModel):
    """容器状态描述信息"""

    def __init__(self):
        """
        :param Name: 容器名称
        :type Name: str
        :param ContainerId: 容器ID
        :type ContainerId: str
        :param Status: 容器状态
        :type Status: str
        :param Reason: 容器处于该状态的原因
        :type Reason: str
        :param Image: 容器镜像ID
        :type Image: str
        """
        self.Name = None
        self.ContainerId = None
        self.Status = None
        self.Reason = None
        self.Image = None

    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.ContainerId = params.get("ContainerId")
        self.Status = params.get("Status")
        self.Reason = params.get("Reason")
        self.Image = params.get("Image")


class CreateClusterAsGroupRequest(AbstractModel):
    """CreateClusterAsGroup请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param AutoScalingGroupPara: 伸缩组创建透传参数，json化字符串格式，详见伸缩组创建实例接口。LaunchConfigurationId由LaunchConfigurePara参数创建，不支持填写
        :type AutoScalingGroupPara: str
        :param LaunchConfigurePara: 启动配置创建透传参数，json化字符串格式，详见创建启动配置接口。另外ImageId参数由于集群维度已经有的ImageId信息，这个字段不需要填写。UserData字段设置通过UserScript设置，这个字段不需要填写。
        :type LaunchConfigurePara: str
        :param InstanceAdvancedSettings: 节点高级配置信息
        :type InstanceAdvancedSettings: :class:`tcecloud.tke.v20180525.models.InstanceAdvancedSettings`
        :param Labels: 节点Label数组
        :type Labels: list of Label
        """
        self.ClusterId = None
        self.AutoScalingGroupPara = None
        self.LaunchConfigurePara = None
        self.InstanceAdvancedSettings = None
        self.Labels = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.AutoScalingGroupPara = params.get("AutoScalingGroupPara")
        self.LaunchConfigurePara = params.get("LaunchConfigurePara")
        if params.get("InstanceAdvancedSettings") is not None:
            self.InstanceAdvancedSettings = InstanceAdvancedSettings()
            self.InstanceAdvancedSettings._deserialize(params.get("InstanceAdvancedSettings"))
        if params.get("Labels") is not None:
            self.Labels = []
            for item in params.get("Labels"):
                obj = Label()
                obj._deserialize(item)
                self.Labels.append(obj)


class CreateClusterAsGroupResponse(AbstractModel):
    """CreateClusterAsGroup返回参数结构体"""

    def __init__(self):
        """
        :param LaunchConfigurationId: 启动配置ID
        :type LaunchConfigurationId: str
        :param AutoScalingGroupId: 伸缩组ID
        :type AutoScalingGroupId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.LaunchConfigurationId = None
        self.AutoScalingGroupId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.LaunchConfigurationId = params.get("LaunchConfigurationId")
        self.AutoScalingGroupId = params.get("AutoScalingGroupId")
        self.RequestId = params.get("RequestId")


class CreateClusterEndpointRequest(AbstractModel):
    """CreateClusterEndpoint请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param BExtranet: 是否为外网访问（默认值: False 不为外网访问）
        :type BExtranet: bool
        :param SubnetId: 集群端口所在的子网ID  (仅在开启非外网访问时需要填，必须为集群所在VPC内的子网)
        :type SubnetId: str
        :param IsExtranet: 是否为外网访问（TRUE 外网访问 FALSE 内网访问，默认值： FALSE）
        :type IsExtranet: bool
        """
        self.ClusterId = None
        self.BExtranet = None
        self.SubnetId = None
        self.IsExtranet = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.BExtranet = params.get("BExtranet")
        self.SubnetId = params.get("SubnetId")
        self.IsExtranet = params.get("IsExtranet")


class CreateClusterEndpointResponse(AbstractModel):
    """CreateClusterEndpoint返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateClusterEndpointVipRequest(AbstractModel):
    """CreateClusterEndpointVip请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param SecurityPolicies: 安全策略放通单个IP或CIDR(例如: "192.168.1.0/24",默认为拒绝所有)
        :type SecurityPolicies: list of str
        """
        self.ClusterId = None
        self.SecurityPolicies = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.SecurityPolicies = params.get("SecurityPolicies")


class CreateClusterEndpointVipResponse(AbstractModel):
    """CreateClusterEndpointVip返回参数结构体"""

    def __init__(self):
        """
        :param RequestFlowId: 请求任务的FlowId
        :type RequestFlowId: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestFlowId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestFlowId = params.get("RequestFlowId")
        self.RequestId = params.get("RequestId")


class CreateClusterInstancesRequest(AbstractModel):
    """CreateClusterInstances请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群 ID，请填写 查询集群列表 接口中返回的 clusterId 字段
        :type ClusterId: str
        :param RunInstancePara: CVM创建透传参数，json化字符串格式，详见CVM创建实例接口。
        :type RunInstancePara: str
        :param InstanceAdvancedSettings: 实例额外需要设置参数信息
        :type InstanceAdvancedSettings: :class:`tcecloud.tke.v20180525.models.InstanceAdvancedSettings`
        """
        self.ClusterId = None
        self.RunInstancePara = None
        self.InstanceAdvancedSettings = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.RunInstancePara = params.get("RunInstancePara")
        if params.get("InstanceAdvancedSettings") is not None:
            self.InstanceAdvancedSettings = InstanceAdvancedSettings()
            self.InstanceAdvancedSettings._deserialize(params.get("InstanceAdvancedSettings"))


class CreateClusterInstancesResponse(AbstractModel):
    """CreateClusterInstances返回参数结构体"""

    def __init__(self):
        """
        :param InstanceIdSet: 节点实例ID
        :type InstanceIdSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceIdSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.InstanceIdSet = params.get("InstanceIdSet")
        self.RequestId = params.get("RequestId")


class CreateClusterRequest(AbstractModel):
    """CreateCluster请求参数结构体"""

    def __init__(self):
        """
        :param ClusterCIDRSettings: 集群容器网络配置信息
        :type ClusterCIDRSettings: :class:`tcecloud.tke.v20180525.models.ClusterCIDRSettings`
        :param ClusterType: 集群类型，托管集群：MANAGED_CLUSTER，独立集群：INDEPENDENT_CLUSTER。
        :type ClusterType: str
        :param RunInstancesForNode: CVM创建透传参数，json化字符串格式，详见CVM创建实例接口。总机型(包括地域)数量不超过10个，相同机型(地域)购买多台机器可以通过设置参数中RunInstances中InstanceCount来实现。
        :type RunInstancesForNode: list of RunInstancesForNode
        :param ClusterBasicSettings: 集群的基本配置信息
        :type ClusterBasicSettings: :class:`tcecloud.tke.v20180525.models.ClusterBasicSettings`
        :param ClusterAdvancedSettings: 集群高级配置信息
        :type ClusterAdvancedSettings: :class:`tcecloud.tke.v20180525.models.ClusterAdvancedSettings`
        :param InstanceAdvancedSettings: 节点高级配置信息
        :type InstanceAdvancedSettings: :class:`tcecloud.tke.v20180525.models.InstanceAdvancedSettings`
        :param ExistedInstancesForNode: 已存在实例的配置信息。所有实例必须在同一个VPC中，最大数量不超过100。
        :type ExistedInstancesForNode: list of ExistedInstancesForNode
        :param InstanceDataDiskMountSettings: CVM类型和其对应的数据盘挂载配置信息
        :type InstanceDataDiskMountSettings: list of InstanceDataDiskMountSetting
        """
        self.ClusterCIDRSettings = None
        self.ClusterType = None
        self.RunInstancesForNode = None
        self.ClusterBasicSettings = None
        self.ClusterAdvancedSettings = None
        self.InstanceAdvancedSettings = None
        self.ExistedInstancesForNode = None
        self.InstanceDataDiskMountSettings = None

    def _deserialize(self, params):
        if params.get("ClusterCIDRSettings") is not None:
            self.ClusterCIDRSettings = ClusterCIDRSettings()
            self.ClusterCIDRSettings._deserialize(params.get("ClusterCIDRSettings"))
        self.ClusterType = params.get("ClusterType")
        if params.get("RunInstancesForNode") is not None:
            self.RunInstancesForNode = []
            for item in params.get("RunInstancesForNode"):
                obj = RunInstancesForNode()
                obj._deserialize(item)
                self.RunInstancesForNode.append(obj)
        if params.get("ClusterBasicSettings") is not None:
            self.ClusterBasicSettings = ClusterBasicSettings()
            self.ClusterBasicSettings._deserialize(params.get("ClusterBasicSettings"))
        if params.get("ClusterAdvancedSettings") is not None:
            self.ClusterAdvancedSettings = ClusterAdvancedSettings()
            self.ClusterAdvancedSettings._deserialize(params.get("ClusterAdvancedSettings"))
        if params.get("InstanceAdvancedSettings") is not None:
            self.InstanceAdvancedSettings = InstanceAdvancedSettings()
            self.InstanceAdvancedSettings._deserialize(params.get("InstanceAdvancedSettings"))
        if params.get("ExistedInstancesForNode") is not None:
            self.ExistedInstancesForNode = []
            for item in params.get("ExistedInstancesForNode"):
                obj = ExistedInstancesForNode()
                obj._deserialize(item)
                self.ExistedInstancesForNode.append(obj)
        if params.get("InstanceDataDiskMountSettings") is not None:
            self.InstanceDataDiskMountSettings = []
            for item in params.get("InstanceDataDiskMountSettings"):
                obj = InstanceDataDiskMountSetting()
                obj._deserialize(item)
                self.InstanceDataDiskMountSettings.append(obj)


class CreateClusterResponse(AbstractModel):
    """CreateCluster返回参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ClusterId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.RequestId = params.get("RequestId")


class CreateClusterRouteRequest(AbstractModel):
    """CreateClusterRoute请求参数结构体"""

    def __init__(self):
        """
        :param RouteTableName: 路由表名称。
        :type RouteTableName: str
        :param DestinationCidrBlock: 目的端CIDR。
        :type DestinationCidrBlock: str
        :param GatewayIp: 下一跳地址。
        :type GatewayIp: str
        """
        self.RouteTableName = None
        self.DestinationCidrBlock = None
        self.GatewayIp = None

    def _deserialize(self, params):
        self.RouteTableName = params.get("RouteTableName")
        self.DestinationCidrBlock = params.get("DestinationCidrBlock")
        self.GatewayIp = params.get("GatewayIp")


class CreateClusterRouteResponse(AbstractModel):
    """CreateClusterRoute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateClusterRouteTableRequest(AbstractModel):
    """CreateClusterRouteTable请求参数结构体"""

    def __init__(self):
        """
        :param RouteTableName: 路由表名称
        :type RouteTableName: str
        :param RouteTableCidrBlock: 路由表CIDR
        :type RouteTableCidrBlock: str
        :param VpcId: 路由表绑定的VPC
        :type VpcId: str
        :param IgnoreClusterCidrConflict: 是否忽略CIDR冲突
        :type IgnoreClusterCidrConflict: int
        """
        self.RouteTableName = None
        self.RouteTableCidrBlock = None
        self.VpcId = None
        self.IgnoreClusterCidrConflict = None

    def _deserialize(self, params):
        self.RouteTableName = params.get("RouteTableName")
        self.RouteTableCidrBlock = params.get("RouteTableCidrBlock")
        self.VpcId = params.get("VpcId")
        self.IgnoreClusterCidrConflict = params.get("IgnoreClusterCidrConflict")


class CreateClusterRouteTableResponse(AbstractModel):
    """CreateClusterRouteTable返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateIndependentClusterRequest(AbstractModel):
    """CreateIndependentCluster请求参数结构体"""

    def __init__(self):
        """
        :param RunInstancesForNode: CVM创建透传参数，json化字符串格式, 各种角色的节点配置信息
        :type RunInstancesForNode: list of RunInstancesForNode
        :param ClusterCIDRSettings: 集群容器网络配置信息
        :type ClusterCIDRSettings: :class:`tcecloud.tke.v20180525.models.ClusterCIDRSettings`
        :param ClusterBasicSettings: 集群的基本配置信息
        :type ClusterBasicSettings: :class:`tcecloud.tke.v20180525.models.ClusterBasicSettings`
        :param ClusterAdvancedSettings: 集群高级配置信息
        :type ClusterAdvancedSettings: :class:`tcecloud.tke.v20180525.models.ClusterAdvancedSettings`
        :param InstanceAdvancedSettings: 节点高级配置信息
        :type InstanceAdvancedSettings: :class:`tcecloud.tke.v20180525.models.InstanceAdvancedSettings`
        """
        self.RunInstancesForNode = None
        self.ClusterCIDRSettings = None
        self.ClusterBasicSettings = None
        self.ClusterAdvancedSettings = None
        self.InstanceAdvancedSettings = None

    def _deserialize(self, params):
        if params.get("RunInstancesForNode") is not None:
            self.RunInstancesForNode = []
            for item in params.get("RunInstancesForNode"):
                obj = RunInstancesForNode()
                obj._deserialize(item)
                self.RunInstancesForNode.append(obj)
        if params.get("ClusterCIDRSettings") is not None:
            self.ClusterCIDRSettings = ClusterCIDRSettings()
            self.ClusterCIDRSettings._deserialize(params.get("ClusterCIDRSettings"))
        if params.get("ClusterBasicSettings") is not None:
            self.ClusterBasicSettings = ClusterBasicSettings()
            self.ClusterBasicSettings._deserialize(params.get("ClusterBasicSettings"))
        if params.get("ClusterAdvancedSettings") is not None:
            self.ClusterAdvancedSettings = ClusterAdvancedSettings()
            self.ClusterAdvancedSettings._deserialize(params.get("ClusterAdvancedSettings"))
        if params.get("InstanceAdvancedSettings") is not None:
            self.InstanceAdvancedSettings = InstanceAdvancedSettings()
            self.InstanceAdvancedSettings._deserialize(params.get("InstanceAdvancedSettings"))


class CreateIndependentClusterResponse(AbstractModel):
    """CreateIndependentCluster返回参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ClusterId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.RequestId = params.get("RequestId")


class CreateTKEClusterRequest(AbstractModel):
    """CreateTKECluster请求参数结构体"""

    def __init__(self):
        """
        :param ClusterCIDRSettings: 集群容器网络配置信息
        :type ClusterCIDRSettings: :class:`tcecloud.tke.v20180525.models.ClusterCIDRSettings`
        :param IndependentCluster: 是否独立集群
        :type IndependentCluster: bool
        :param RunInstancesForNode: CVM创建透传参数，json化字符串格式, 各种角色的节点配置信息
        :type RunInstancesForNode: list of RunInstancesForNode
        :param ClusterBasicSettings: 集群的基本配置信息
        :type ClusterBasicSettings: :class:`tcecloud.tke.v20180525.models.ClusterBasicSettings`
        :param ClusterAdvancedSettings: 集群高级配置信息
        :type ClusterAdvancedSettings: :class:`tcecloud.tke.v20180525.models.ClusterAdvancedSettings`
        :param InstanceAdvancedSettings: 节点高级配置信息
        :type InstanceAdvancedSettings: :class:`tcecloud.tke.v20180525.models.InstanceAdvancedSettings`
        """
        self.ClusterCIDRSettings = None
        self.IndependentCluster = None
        self.RunInstancesForNode = None
        self.ClusterBasicSettings = None
        self.ClusterAdvancedSettings = None
        self.InstanceAdvancedSettings = None

    def _deserialize(self, params):
        if params.get("ClusterCIDRSettings") is not None:
            self.ClusterCIDRSettings = ClusterCIDRSettings()
            self.ClusterCIDRSettings._deserialize(params.get("ClusterCIDRSettings"))
        self.IndependentCluster = params.get("IndependentCluster")
        if params.get("RunInstancesForNode") is not None:
            self.RunInstancesForNode = []
            for item in params.get("RunInstancesForNode"):
                obj = RunInstancesForNode()
                obj._deserialize(item)
                self.RunInstancesForNode.append(obj)
        if params.get("ClusterBasicSettings") is not None:
            self.ClusterBasicSettings = ClusterBasicSettings()
            self.ClusterBasicSettings._deserialize(params.get("ClusterBasicSettings"))
        if params.get("ClusterAdvancedSettings") is not None:
            self.ClusterAdvancedSettings = ClusterAdvancedSettings()
            self.ClusterAdvancedSettings._deserialize(params.get("ClusterAdvancedSettings"))
        if params.get("InstanceAdvancedSettings") is not None:
            self.InstanceAdvancedSettings = InstanceAdvancedSettings()
            self.InstanceAdvancedSettings._deserialize(params.get("InstanceAdvancedSettings"))


class CreateTKEClusterResponse(AbstractModel):
    """CreateTKECluster返回参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ClusterId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.RequestId = params.get("RequestId")


class DataDisk(AbstractModel):
    """描述了k8s节点数据盘相关配置与信息。"""

    def __init__(self):
        """
        :param DiskType: 云盘类型
        :type DiskType: str
        :param FileSystem: 文件系统(ext3/ext4/xfs)
        :type FileSystem: str
        :param DiskSize: 云盘大小(G）
        :type DiskSize: int
        :param AutoFormatAndMount: 是否自动化格式盘并挂载
        :type AutoFormatAndMount: bool
        :param MountTarget: 挂载目录
        :type MountTarget: str
        """
        self.DiskType = None
        self.FileSystem = None
        self.DiskSize = None
        self.AutoFormatAndMount = None
        self.MountTarget = None

    def _deserialize(self, params):
        self.DiskType = params.get("DiskType")
        self.FileSystem = params.get("FileSystem")
        self.DiskSize = params.get("DiskSize")
        self.AutoFormatAndMount = params.get("AutoFormatAndMount")
        self.MountTarget = params.get("MountTarget")


class DeleteAlarmPoliciesRequest(AbstractModel):
    """DeleteAlarmPolicies请求参数结构体"""

    def __init__(self):
        """
        :param ClusterInstanceId: k8s集群ID
        :type ClusterInstanceId: str
        :param AlarmPolicyIds: 告警策略ID列表
        :type AlarmPolicyIds: list of str
        """
        self.ClusterInstanceId = None
        self.AlarmPolicyIds = None

    def _deserialize(self, params):
        self.ClusterInstanceId = params.get("ClusterInstanceId")
        self.AlarmPolicyIds = params.get("AlarmPolicyIds")


class DeleteAlarmPoliciesResponse(AbstractModel):
    """DeleteAlarmPolicies返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteClusterAsGroupsRequest(AbstractModel):
    """DeleteClusterAsGroups请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID，通过DescribeClusters接口获取。
        :type ClusterId: str
        :param AutoScalingGroupIds: 集群伸缩组ID的列表
        :type AutoScalingGroupIds: list of str
        :param KeepInstance: 是否保留伸缩组中的节点(默认值： false(不保留))
        :type KeepInstance: bool
        """
        self.ClusterId = None
        self.AutoScalingGroupIds = None
        self.KeepInstance = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.AutoScalingGroupIds = params.get("AutoScalingGroupIds")
        self.KeepInstance = params.get("KeepInstance")


class DeleteClusterAsGroupsResponse(AbstractModel):
    """DeleteClusterAsGroups返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteClusterCIDRFromCcnRequest(AbstractModel):
    """DeleteClusterCIDRFromCcn请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: 私有网络ID，形如vpc-xxx。创建托管空集群时必传。
        :type VpcId: str
        :param ClusterCIDR: 私有网络ID，形如vpc-xxx。创建托管空集群时必传。
        :type ClusterCIDR: str
        """
        self.VpcId = None
        self.ClusterCIDR = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.ClusterCIDR = params.get("ClusterCIDR")


class DeleteClusterCIDRFromCcnResponse(AbstractModel):
    """DeleteClusterCIDRFromCcn返回参数结构体"""

    def __init__(self):
        """
        :param RouteSet: 云联网路由数组
        :type RouteSet: list of CcnRoute
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RouteSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("RouteSet") is not None:
            self.RouteSet = []
            for item in params.get("RouteSet"):
                obj = CcnRoute()
                obj._deserialize(item)
                self.RouteSet.append(obj)
        self.RequestId = params.get("RequestId")


class DeleteClusterCIDRFromVbcRequest(AbstractModel):
    """DeleteClusterCIDRFromVbc请求参数结构体"""

    def __init__(self):
        """
        :param UniqVpcId: vpc唯一id
        :type UniqVpcId: str
        :param ClusterCIDR: 集群cidr
        :type ClusterCIDR: str
        """
        self.UniqVpcId = None
        self.ClusterCIDR = None

    def _deserialize(self, params):
        self.UniqVpcId = params.get("UniqVpcId")
        self.ClusterCIDR = params.get("ClusterCIDR")


class DeleteClusterCIDRFromVbcResponse(AbstractModel):
    """DeleteClusterCIDRFromVbc返回参数结构体"""

    def __init__(self):
        """
        :param Detail: 详情
        :type Detail: list of CcnRoute
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Detail = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Detail") is not None:
            self.Detail = []
            for item in params.get("Detail"):
                obj = CcnRoute()
                obj._deserialize(item)
                self.Detail.append(obj)
        self.RequestId = params.get("RequestId")


class DeleteClusterEndpointRequest(AbstractModel):
    """DeleteClusterEndpoint请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param BExtranet: 是否为外网访问（默认值: False 不为外网访问）
        :type BExtranet: bool
        :param IsExtranet: 是否为外网访问（TRUE 外网访问 FALSE 内网访问，默认值： FALSE）
        :type IsExtranet: bool
        """
        self.ClusterId = None
        self.BExtranet = None
        self.IsExtranet = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.BExtranet = params.get("BExtranet")
        self.IsExtranet = params.get("IsExtranet")


class DeleteClusterEndpointResponse(AbstractModel):
    """DeleteClusterEndpoint返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteClusterEndpointVipRequest(AbstractModel):
    """DeleteClusterEndpointVip请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        """
        self.ClusterId = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")


class DeleteClusterEndpointVipResponse(AbstractModel):
    """DeleteClusterEndpointVip返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteClusterInstancesRequest(AbstractModel):
    """DeleteClusterInstances请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param InstanceIds: 主机InstanceId列表
        :type InstanceIds: list of str
        :param InstanceDeleteMode: 集群实例删除时的策略：terminate（销毁实例，仅支持按量计费云主机实例） retain （仅移除，保留实例）
        :type InstanceDeleteMode: str
        :param ForceDelete: 是否强制删除(当节点在初始化时，可以指定参数为TRUE)
        :type ForceDelete: bool
        """
        self.ClusterId = None
        self.InstanceIds = None
        self.InstanceDeleteMode = None
        self.ForceDelete = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.InstanceIds = params.get("InstanceIds")
        self.InstanceDeleteMode = params.get("InstanceDeleteMode")
        self.ForceDelete = params.get("ForceDelete")


class DeleteClusterInstancesResponse(AbstractModel):
    """DeleteClusterInstances返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteClusterRequest(AbstractModel):
    """DeleteCluster请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param InstanceDeleteMode: 集群实例删除时的策略：terminate（销毁实例，仅支持按量计费云主机实例） retain （仅移除，保留实例）
        :type InstanceDeleteMode: str
        """
        self.ClusterId = None
        self.InstanceDeleteMode = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.InstanceDeleteMode = params.get("InstanceDeleteMode")


class DeleteClusterResponse(AbstractModel):
    """DeleteCluster返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteClusterRouteRequest(AbstractModel):
    """DeleteClusterRoute请求参数结构体"""

    def __init__(self):
        """
        :param RouteTableName: 路由表名称。
        :type RouteTableName: str
        :param GatewayIp: 下一跳地址。
        :type GatewayIp: str
        :param DestinationCidrBlock: 目的端CIDR。
        :type DestinationCidrBlock: str
        """
        self.RouteTableName = None
        self.GatewayIp = None
        self.DestinationCidrBlock = None

    def _deserialize(self, params):
        self.RouteTableName = params.get("RouteTableName")
        self.GatewayIp = params.get("GatewayIp")
        self.DestinationCidrBlock = params.get("DestinationCidrBlock")


class DeleteClusterRouteResponse(AbstractModel):
    """DeleteClusterRoute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteClusterRouteTableRequest(AbstractModel):
    """DeleteClusterRouteTable请求参数结构体"""

    def __init__(self):
        """
        :param RouteTableName: 路由表名称
        :type RouteTableName: str
        """
        self.RouteTableName = None

    def _deserialize(self, params):
        self.RouteTableName = params.get("RouteTableName")


class DeleteClusterRouteTableResponse(AbstractModel):
    """DeleteClusterRouteTable返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeAlarmPoliciesRequest(AbstractModel):
    """DescribeAlarmPolicies请求参数结构体"""

    def __init__(self):
        """
        :param ClusterInstanceId: k8s集群ID
        :type ClusterInstanceId: str
        :param Offset: 偏移量,默认0
        :type Offset: int
        :param Limit: 最大输出条数，默认20
        :type Limit: int
        :param Filter: 过滤条件
        :type Filter: :class:`tcecloud.tke.v20180525.models.AlarmPolicyFilter`
        """
        self.ClusterInstanceId = None
        self.Offset = None
        self.Limit = None
        self.Filter = None

    def _deserialize(self, params):
        self.ClusterInstanceId = params.get("ClusterInstanceId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        if params.get("Filter") is not None:
            self.Filter = AlarmPolicyFilter()
            self.Filter._deserialize(params.get("Filter"))


class DescribeAlarmPoliciesResponse(AbstractModel):
    """DescribeAlarmPolicies返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 集群告警策略总个数
        :type TotalCount: int
        :param AlarmPolicySet: 集群告警列表
        :type AlarmPolicySet: list of AlarmPolicy
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.AlarmPolicySet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("AlarmPolicySet") is not None:
            self.AlarmPolicySet = []
            for item in params.get("AlarmPolicySet"):
                obj = AlarmPolicy()
                obj._deserialize(item)
                self.AlarmPolicySet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeAvailableClusterVersionRequest(AbstractModel):
    """DescribeAvailableClusterVersion请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群 Id
        :type ClusterId: str
        :param ClusterIds: 集群 Id 列表
        :type ClusterIds: list of str
        """
        self.ClusterId = None
        self.ClusterIds = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.ClusterIds = params.get("ClusterIds")


class DescribeAvailableClusterVersionResponse(AbstractModel):
    """DescribeAvailableClusterVersion返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeCcnInstancesRequest(AbstractModel):
    """DescribeCcnInstances请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: 私有网络ID，形如vpc-xxx。创建托管空集群时必传。
        :type VpcId: str
        """
        self.VpcId = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")


class DescribeCcnInstancesResponse(AbstractModel):
    """DescribeCcnInstances返回参数结构体"""

    def __init__(self):
        """
        :param InstanceSet: 关联网络实例列表
        :type InstanceSet: list of CcnInstance
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("InstanceSet") is not None:
            self.InstanceSet = []
            for item in params.get("InstanceSet"):
                obj = CcnInstance()
                obj._deserialize(item)
                self.InstanceSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeCcnRoutesRequest(AbstractModel):
    """DescribeCcnRoutes请求参数结构体"""

    def __init__(self):
        """
        :param VpcId: 私有网络ID，形如vpc-xxx。创建托管空集群时必传。
        :type VpcId: str
        :param ClusterCIDR: 用于分配集群容器和服务 IP 的 CIDR，不得与 VPC CIDR 冲突，也不得与同 VPC 内其他集群 CIDR 冲突
        :type ClusterCIDR: str
        """
        self.VpcId = None
        self.ClusterCIDR = None

    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.ClusterCIDR = params.get("ClusterCIDR")


class DescribeCcnRoutesResponse(AbstractModel):
    """DescribeCcnRoutes返回参数结构体"""

    def __init__(self):
        """
        :param RouteSet: 云联网路由数组
        :type RouteSet: list of CcnRoute
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RouteSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("RouteSet") is not None:
            self.RouteSet = []
            for item in params.get("RouteSet"):
                obj = CcnRoute()
                obj._deserialize(item)
                self.RouteSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeClsLogSetsRequest(AbstractModel):
    """DescribeClsLogSets请求参数结构体"""


class DescribeClsLogSetsResponse(AbstractModel):
    """DescribeClsLogSets返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 日志集数量
        :type TotalCount: int
        :param Logsets: 日志集集合
        :type Logsets: list of LogSet
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.Logsets = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Logsets") is not None:
            self.Logsets = []
            for item in params.get("Logsets"):
                obj = LogSet()
                obj._deserialize(item)
                self.Logsets.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeClsLogTopicsRequest(AbstractModel):
    """DescribeClsLogTopics请求参数结构体"""

    def __init__(self):
        """
        :param LogSetId: 日志集ID
        :type LogSetId: str
        """
        self.LogSetId = None

    def _deserialize(self, params):
        self.LogSetId = params.get("LogSetId")


class DescribeClsLogTopicsResponse(AbstractModel):
    """DescribeClsLogTopics返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 日志主题的数量
        :type TotalCount: int
        :param Topics: 日志主题集合
        :type Topics: list of LogTopic
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.Topics = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Topics") is not None:
            self.Topics = []
            for item in params.get("Topics"):
                obj = LogTopic()
                obj._deserialize(item)
                self.Topics.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeClusterAsGroupOptionRequest(AbstractModel):
    """DescribeClusterAsGroupOption请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        """
        self.ClusterId = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")


class DescribeClusterAsGroupOptionResponse(AbstractModel):
    """DescribeClusterAsGroupOption返回参数结构体"""

    def __init__(self):
        """
        :param ClusterAsGroupOption: 集群弹性伸缩属性
        :type ClusterAsGroupOption: :class:`tcecloud.tke.v20180525.models.ClusterAsGroupOption`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ClusterAsGroupOption = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("ClusterAsGroupOption") is not None:
            self.ClusterAsGroupOption = ClusterAsGroupOption()
            self.ClusterAsGroupOption._deserialize(params.get("ClusterAsGroupOption"))
        self.RequestId = params.get("RequestId")


class DescribeClusterAsGroupsRequest(AbstractModel):
    """DescribeClusterAsGroups请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param AutoScalingGroupIds: 伸缩组ID列表，如果为空，表示拉取集群关联的所有伸缩组。
        :type AutoScalingGroupIds: list of str
        :param Offset: 偏移量，默认为0。关于Offset的更进一步介绍请参考 API 简介中的相关小节。
        :type Offset: int
        :param Limit: 返回数量，默认为20，最大值为100。关于Limit的更进一步介绍请参考 API 简介中的相关小节。
        :type Limit: int
        """
        self.ClusterId = None
        self.AutoScalingGroupIds = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.AutoScalingGroupIds = params.get("AutoScalingGroupIds")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeClusterAsGroupsResponse(AbstractModel):
    """DescribeClusterAsGroups返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 集群关联的伸缩组总数
        :type TotalCount: int
        :param ClusterAsGroupSet: 集群关联的伸缩组列表
        :type ClusterAsGroupSet: :class:`tcecloud.tke.v20180525.models.ClusterAsGroup`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.ClusterAsGroupSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("ClusterAsGroupSet") is not None:
            self.ClusterAsGroupSet = ClusterAsGroup()
            self.ClusterAsGroupSet._deserialize(params.get("ClusterAsGroupSet"))
        self.RequestId = params.get("RequestId")


class DescribeClusterAvailableExtraArgsRequest(AbstractModel):
    """DescribeClusterAvailableExtraArgs请求参数结构体"""

    def __init__(self):
        """
        :param ClusterVersion: 集群版本
        :type ClusterVersion: str
        :param ClusterType: 集群类型(MANAGED_CLUSTER或INDEPENDENT_CLUSTER)
        :type ClusterType: str
        """
        self.ClusterVersion = None
        self.ClusterType = None

    def _deserialize(self, params):
        self.ClusterVersion = params.get("ClusterVersion")
        self.ClusterType = params.get("ClusterType")


class DescribeClusterAvailableExtraArgsResponse(AbstractModel):
    """DescribeClusterAvailableExtraArgs返回参数结构体"""

    def __init__(self):
        """
        :param ClusterVersion: 集群版本
        :type ClusterVersion: str
        :param AvailableExtraArgs: 可用的自定义参数
        :type AvailableExtraArgs: :class:`tcecloud.tke.v20180525.models.AvailableExtraArgs`
        :param ClusterType: 集群类型
        :type ClusterType: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ClusterVersion = None
        self.AvailableExtraArgs = None
        self.ClusterType = None
        self.RequestId = None

    def _deserialize(self, params):
        self.ClusterVersion = params.get("ClusterVersion")
        if params.get("AvailableExtraArgs") is not None:
            self.AvailableExtraArgs = AvailableExtraArgs()
            self.AvailableExtraArgs._deserialize(params.get("AvailableExtraArgs"))
        self.ClusterType = params.get("ClusterType")
        self.RequestId = params.get("RequestId")


class DescribeClusterCreateProgressRequest(AbstractModel):
    """DescribeClusterCreateProgress请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群 Id
        :type ClusterId: str
        """
        self.ClusterId = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")


class DescribeClusterCreateProgressResponse(AbstractModel):
    """DescribeClusterCreateProgress返回参数结构体"""

    def __init__(self):
        """
        :param Progress: 创建进度
        :type Progress: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Progress = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Progress = params.get("Progress")
        self.RequestId = params.get("RequestId")


class DescribeClusterEndpointStatusRequest(AbstractModel):
    """DescribeClusterEndpointStatus请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param BExtranet: 是否为外网访问（默认值: False 不为外网访问）
        :type BExtranet: bool
        :param IsExtranet: 是否为外网访问（TRUE 外网访问 FALSE 内网访问，默认值： FALSE）
        :type IsExtranet: bool
        """
        self.ClusterId = None
        self.BExtranet = None
        self.IsExtranet = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.BExtranet = params.get("BExtranet")
        self.IsExtranet = params.get("IsExtranet")


class DescribeClusterEndpointStatusResponse(AbstractModel):
    """DescribeClusterEndpointStatus返回参数结构体"""

    def __init__(self):
        """
        :param Status: 查询集群访问端口状态（Created 开启成功，Creating 开启中中，NotFound 未开启）
        :type Status: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Status = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class DescribeClusterEndpointVipStatusRequest(AbstractModel):
    """DescribeClusterEndpointVipStatus请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        """
        self.ClusterId = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")


class DescribeClusterEndpointVipStatusResponse(AbstractModel):
    """DescribeClusterEndpointVipStatus返回参数结构体"""

    def __init__(self):
        """
        :param Status: 端口操作状态 (Creating 创建中  CreateFailed 创建失败 Created 创建完成 Deleting 删除中 DeletedFailed 删除失败 Deleted 已删除 NotFound 未发现操作 )
        :type Status: str
        :param ErrorMsg: 操作失败的原因
        :type ErrorMsg: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Status = None
        self.ErrorMsg = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.ErrorMsg = params.get("ErrorMsg")
        self.RequestId = params.get("RequestId")


class DescribeClusterExtraArgsRequest(AbstractModel):
    """DescribeClusterExtraArgs请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        """
        self.ClusterId = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")


class DescribeClusterExtraArgsResponse(AbstractModel):
    """DescribeClusterExtraArgs返回参数结构体"""

    def __init__(self):
        """
        :param ClusterExtraArgs: 集群自定义参数
        :type ClusterExtraArgs: :class:`tcecloud.tke.v20180525.models.ClusterExtraArgs`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ClusterExtraArgs = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("ClusterExtraArgs") is not None:
            self.ClusterExtraArgs = ClusterExtraArgs()
            self.ClusterExtraArgs._deserialize(params.get("ClusterExtraArgs"))
        self.RequestId = params.get("RequestId")


class DescribeClusterHealthyStatusRequest(AbstractModel):
    """DescribeClusterHealthyStatus请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群实例ID
        :type ClusterId: str
        """
        self.ClusterId = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")


class DescribeClusterHealthyStatusResponse(AbstractModel):
    """DescribeClusterHealthyStatus返回参数结构体"""

    def __init__(self):
        """
        :param PodsStatus: 集群Pod健康状态
        :type PodsStatus: :class:`tcecloud.tke.v20180525.models.ClusterHealthyPodsStatus`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.PodsStatus = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("PodsStatus") is not None:
            self.PodsStatus = ClusterHealthyPodsStatus()
            self.PodsStatus._deserialize(params.get("PodsStatus"))
        self.RequestId = params.get("RequestId")


class DescribeClusterInspectionItem(AbstractModel):
    """描述集群巡检概览信息"""

    def __init__(self):
        """
                :param ClusterId: 集群实例id
                :type ClusterId: str
                :param Error: 如果发生错误，则该字段包含错误信息
        注意：此字段可能返回 null，表示取不到有效值。
                :type Error: str
                :param Progress: 如果当前正在巡检，则该字段包含检测巡检
        注意：此字段可能返回 null，表示取不到有效值。
                :type Progress: :class:`tcecloud.tke.v20180525.models.ClusterInspectionProgress`
                :param LastResult: 最近一次巡检结果概览
        注意：此字段可能返回 null，表示取不到有效值。
                :type LastResult: :class:`tcecloud.tke.v20180525.models.ClusterInspectionOverview`
                :param Cron: 自动巡检周期，crontab格式
        注意：此字段可能返回 null，表示取不到有效值。
                :type Cron: str
        """
        self.ClusterId = None
        self.Error = None
        self.Progress = None
        self.LastResult = None
        self.Cron = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.Error = params.get("Error")
        if params.get("Progress") is not None:
            self.Progress = ClusterInspectionProgress()
            self.Progress._deserialize(params.get("Progress"))
        if params.get("LastResult") is not None:
            self.LastResult = ClusterInspectionOverview()
            self.LastResult._deserialize(params.get("LastResult"))
        self.Cron = params.get("Cron")


class DescribeClusterInspectionOverviewsRequest(AbstractModel):
    """DescribeClusterInspectionOverviews请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群实例id
        :type ClusterId: str
        :param Limit: 最多返回多少条记录
        :type Limit: int
        :param Offset: 从最近第几条记录开始返回
        :type Offset: int
        """
        self.ClusterId = None
        self.Limit = None
        self.Offset = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")


class DescribeClusterInspectionOverviewsResponse(AbstractModel):
    """DescribeClusterInspectionOverviews返回参数结构体"""

    def __init__(self):
        """
        :param OverviewSet: 集群巡检报告列表
        :type OverviewSet: list of ClusterInspectionOverview
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.OverviewSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("OverviewSet") is not None:
            self.OverviewSet = []
            for item in params.get("OverviewSet"):
                obj = ClusterInspectionOverview()
                obj._deserialize(item)
                self.OverviewSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeClusterInspectionReportRequest(AbstractModel):
    """DescribeClusterInspectionReport请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群实例id
        :type ClusterId: str
        :param ReportId: 报告页id
        :type ReportId: str
        """
        self.ClusterId = None
        self.ReportId = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.ReportId = params.get("ReportId")


class DescribeClusterInspectionReportResponse(AbstractModel):
    """DescribeClusterInspectionReport返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeClusterInspectionsRequest(AbstractModel):
    """DescribeClusterInspections请求参数结构体"""

    def __init__(self):
        """
        :param ClusterIds: 目标集群实例id数组
        :type ClusterIds: list of str
        """
        self.ClusterIds = None

    def _deserialize(self, params):
        self.ClusterIds = params.get("ClusterIds")


class DescribeClusterInspectionsResponse(AbstractModel):
    """DescribeClusterInspections返回参数结构体"""

    def __init__(self):
        """
        :param ResultSet: 各集群巡检概览
        :type ResultSet: list of DescribeClusterInspectionItem
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ResultSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("ResultSet") is not None:
            self.ResultSet = []
            for item in params.get("ResultSet"):
                obj = DescribeClusterInspectionItem()
                obj._deserialize(item)
                self.ResultSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeClusterInstanceIdsRequest(AbstractModel):
    """DescribeClusterInstanceIds请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param InstanceRole: 节点角色, MASTER, WORKER, ETCD, MASTER_ETCD,ALL, 默认为WORKER。默认为WORKER类型。
        :type InstanceRole: str
        :param Offset: 偏移量，默认为0。关于Offset的更进一步介绍请参考 API 简介中的相关小节。
        :type Offset: int
        :param Limit: 返回数量，默认为20，最大值为100。关于Limit的更进一步介绍请参考 API 简介中的相关小节。
        :type Limit: int
        :param VagueIpAddress: 根据节点的IP地址进行搜索，同时搜索内网IP和外网IP
        :type VagueIpAddress: str
        :param VagueInstanceName: 根据节点的名称进行模糊搜索
        :type VagueInstanceName: str
        :param InstanceStates: 根据节点的状态进行筛选
        :type InstanceStates: list of str
        """
        self.ClusterId = None
        self.InstanceRole = None
        self.Offset = None
        self.Limit = None
        self.VagueIpAddress = None
        self.VagueInstanceName = None
        self.InstanceStates = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.InstanceRole = params.get("InstanceRole")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.VagueIpAddress = params.get("VagueIpAddress")
        self.VagueInstanceName = params.get("VagueInstanceName")
        self.InstanceStates = params.get("InstanceStates")


class DescribeClusterInstanceIdsResponse(AbstractModel):
    """DescribeClusterInstanceIds返回参数结构体"""

    def __init__(self):
        """
        :param InstanceIdSet: 节点ID列表
        :type InstanceIdSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceIdSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.InstanceIdSet = params.get("InstanceIdSet")
        self.RequestId = params.get("RequestId")


class DescribeClusterInstancesRequest(AbstractModel):
    """DescribeClusterInstances请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param Offset: 偏移量，默认为0。关于Offset的更进一步介绍请参考 API 简介中的相关小节。
        :type Offset: int
        :param Limit: 返回数量，默认为20，最大值为100。关于Limit的更进一步介绍请参考 API 简介中的相关小节。
        :type Limit: int
        :param InstanceIds: 需要获取的节点实例Id列表。如果为空，表示拉取集群下所有节点实例。
        :type InstanceIds: list of str
        :param InstanceRole: 节点角色, MASTER, WORKER, ETCD, MASTER_ETCD,ALL, 默认为WORKER。默认为WORKER类型。
        :type InstanceRole: str
        :param Filters: 过滤条件列表
        :type Filters: list of Filter
        """
        self.ClusterId = None
        self.Offset = None
        self.Limit = None
        self.InstanceIds = None
        self.InstanceRole = None
        self.Filters = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.InstanceIds = params.get("InstanceIds")
        self.InstanceRole = params.get("InstanceRole")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)


class DescribeClusterInstancesResponse(AbstractModel):
    """DescribeClusterInstances返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 集群中实例总数
        :type TotalCount: int
        :param InstanceSet: 集群中实例列表
        :type InstanceSet: list of Instance
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.InstanceSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("InstanceSet") is not None:
            self.InstanceSet = []
            for item in params.get("InstanceSet"):
                obj = Instance()
                obj._deserialize(item)
                self.InstanceSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeClusterPodsRequest(AbstractModel):
    """DescribeClusterPods请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param ServiceName: Deployment名称
        :type ServiceName: str
        :param Namespace: 命名空间名称，默认为default
        :type Namespace: str
        :param SearchName: 过滤参数，从PodIP、NodeIP、PodName中过滤含有该参数的Pod实例
        :type SearchName: str
        :param Limit: 最大输出条数，默认0
        :type Limit: int
        :param Offset: 偏移量，默认0
        :type Offset: int
        """
        self.ClusterId = None
        self.ServiceName = None
        self.Namespace = None
        self.SearchName = None
        self.Limit = None
        self.Offset = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.ServiceName = params.get("ServiceName")
        self.Namespace = params.get("Namespace")
        self.SearchName = params.get("SearchName")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")


class DescribeClusterPodsResponse(AbstractModel):
    """DescribeClusterPods返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 返回的Pod总数
        :type TotalCount: int
        :param Pods: Pod信息
        :type Pods: list of PodInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.Pods = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Pods") is not None:
            self.Pods = []
            for item in params.get("Pods"):
                obj = PodInfo()
                obj._deserialize(item)
                self.Pods.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeClusterRouteTablesRequest(AbstractModel):
    """DescribeClusterRouteTables请求参数结构体"""


class DescribeClusterRouteTablesResponse(AbstractModel):
    """DescribeClusterRouteTables返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param RouteTableSet: 集群路由表对象。
        :type RouteTableSet: list of RouteTableInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.RouteTableSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("RouteTableSet") is not None:
            self.RouteTableSet = []
            for item in params.get("RouteTableSet"):
                obj = RouteTableInfo()
                obj._deserialize(item)
                self.RouteTableSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeClusterRoutesRequest(AbstractModel):
    """DescribeClusterRoutes请求参数结构体"""

    def __init__(self):
        """
        :param RouteTableName: 路由表名称。
        :type RouteTableName: str
        """
        self.RouteTableName = None

    def _deserialize(self, params):
        self.RouteTableName = params.get("RouteTableName")


class DescribeClusterRoutesResponse(AbstractModel):
    """DescribeClusterRoutes返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param RouteSet: 集群路由对象。
        :type RouteSet: list of RouteInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.RouteSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("RouteSet") is not None:
            self.RouteSet = []
            for item in params.get("RouteSet"):
                obj = RouteInfo()
                obj._deserialize(item)
                self.RouteSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeClusterSecurityRequest(AbstractModel):
    """DescribeClusterSecurity请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群 ID，请填写 查询集群列表 接口中返回的 clusterId 字段
        :type ClusterId: str
        :param JnsGwEndpointEnable: 是否返回内网地址(默认: FALSE)
        :type JnsGwEndpointEnable: bool
        """
        self.ClusterId = None
        self.JnsGwEndpointEnable = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.JnsGwEndpointEnable = params.get("JnsGwEndpointEnable")


class DescribeClusterSecurityResponse(AbstractModel):
    """DescribeClusterSecurity返回参数结构体"""

    def __init__(self):
        """
        :param UserName: 集群的账号名称
        :type UserName: str
        :param Password: 集群的访问密码
        :type Password: str
        :param CertificationAuthority: 集群访问CA证书
        :type CertificationAuthority: str
        :param ClusterExternalEndpoint: 集群访问的地址
        :type ClusterExternalEndpoint: str
        :param Domain: 集群访问的域名
        :type Domain: str
        :param PgwEndpoint: 集群Endpoint地址
        :type PgwEndpoint: str
        :param SecurityPolicy: 集群访问策略组
        :type SecurityPolicy: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.UserName = None
        self.Password = None
        self.CertificationAuthority = None
        self.ClusterExternalEndpoint = None
        self.Domain = None
        self.PgwEndpoint = None
        self.SecurityPolicy = None
        self.RequestId = None

    def _deserialize(self, params):
        self.UserName = params.get("UserName")
        self.Password = params.get("Password")
        self.CertificationAuthority = params.get("CertificationAuthority")
        self.ClusterExternalEndpoint = params.get("ClusterExternalEndpoint")
        self.Domain = params.get("Domain")
        self.PgwEndpoint = params.get("PgwEndpoint")
        self.SecurityPolicy = params.get("SecurityPolicy")
        self.RequestId = params.get("RequestId")


class DescribeClusterServicesRequest(AbstractModel):
    """DescribeClusterServices请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param Namespace: 命名空间
        :type Namespace: str
        :param AllNamespace: 是否使用所有命名空间
        :type AllNamespace: int
        """
        self.ClusterId = None
        self.Namespace = None
        self.AllNamespace = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.Namespace = params.get("Namespace")
        self.AllNamespace = params.get("AllNamespace")


class DescribeClusterServicesResponse(AbstractModel):
    """DescribeClusterServices返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 返回的Service总数
        :type TotalCount: int
        :param Services: Service详细信息
        :type Services: list of SummaryService
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.Services = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Services") is not None:
            self.Services = []
            for item in params.get("Services"):
                obj = SummaryService()
                obj._deserialize(item)
                self.Services.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeClusterStatusRequest(AbstractModel):
    """DescribeClusterStatus请求参数结构体"""

    def __init__(self):
        """
        :param ClusterIds: 集群ID列表，不传默认拉取所有集群
        :type ClusterIds: list of str
        """
        self.ClusterIds = None

    def _deserialize(self, params):
        self.ClusterIds = params.get("ClusterIds")


class DescribeClusterStatusResponse(AbstractModel):
    """DescribeClusterStatus返回参数结构体"""

    def __init__(self):
        """
        :param ClusterStatusSet: 集群状态列表
        :type ClusterStatusSet: list of ClusterStatus
        :param TotalCount: 集群个数
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ClusterStatusSet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("ClusterStatusSet") is not None:
            self.ClusterStatusSet = []
            for item in params.get("ClusterStatusSet"):
                obj = ClusterStatus()
                obj._deserialize(item)
                self.ClusterStatusSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeClustersRequest(AbstractModel):
    """DescribeClusters请求参数结构体"""

    def __init__(self):
        """
                :param ClusterIds: 集群ID列表(为空时，
        表示获取账号下所有集群)
                :type ClusterIds: list of str
                :param Offset: 偏移量,默认0
                :type Offset: int
                :param Limit: 最大输出条数，默认20，最大为100
                :type Limit: int
                :param Filters: 过滤条件,当前只支持按照单个条件ClusterName进行过滤
                :type Filters: list of Filter
        """
        self.ClusterIds = None
        self.Offset = None
        self.Limit = None
        self.Filters = None

    def _deserialize(self, params):
        self.ClusterIds = params.get("ClusterIds")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)


class DescribeClustersResourceStatusRequest(AbstractModel):
    """DescribeClustersResourceStatus请求参数结构体"""

    def __init__(self):
        """
        :param Dimensions: 资源维度，可传列表
        :type Dimensions: list of str
        :param ClusterInstancesIds: 集群id，可传列表
        :type ClusterInstancesIds: list of str
        :param ResourceType: 获取资源类型
        :type ResourceType: str
        """
        self.Dimensions = None
        self.ClusterInstancesIds = None
        self.ResourceType = None

    def _deserialize(self, params):
        self.Dimensions = params.get("Dimensions")
        self.ClusterInstancesIds = params.get("ClusterInstancesIds")
        self.ResourceType = params.get("ResourceType")


class DescribeClustersResourceStatusResponse(AbstractModel):
    """DescribeClustersResourceStatus返回参数结构体"""

    def __init__(self):
        """
        :param ResourceStatusSet: 集群资源状态集合
        :type ResourceStatusSet: list of ResourceStatus
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ResourceStatusSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("ResourceStatusSet") is not None:
            self.ResourceStatusSet = []
            for item in params.get("ResourceStatusSet"):
                obj = ResourceStatus()
                obj._deserialize(item)
                self.ResourceStatusSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeClustersResponse(AbstractModel):
    """DescribeClusters返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 集群总个数
        :type TotalCount: int
        :param Clusters: 集群信息列表
        :type Clusters: list of Cluster
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.Clusters = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Clusters") is not None:
            self.Clusters = []
            for item in params.get("Clusters"):
                obj = Cluster()
                obj._deserialize(item)
                self.Clusters.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeExistedInstancesRequest(AbstractModel):
    """DescribeExistedInstances请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群 ID，请填写查询集群列表 接口中返回的 ClusterId 字段（仅通过ClusterId获取需要过滤条件中的VPCID。节点状态比较时会使用该地域下所有集群中的节点进行比较。参数不支持同时指定InstanceIds和ClusterId。
        :type ClusterId: str
        :param InstanceIds: 按照一个或者多个实例ID查询。实例ID形如：ins-xxxxxxxx。（此参数的具体格式可参考API简介的id.N一节）。每次请求的实例的上限为100。参数不支持同时指定InstanceIds和Filters。
        :type InstanceIds: list of str
        :param Filters: 过滤条件,字段和详见CVM查询实例如果设置了ClusterId，会附加集群的VPCID作为查询字段，在此情况下如果在Filter中指定了"vpc-id"作为过滤字段，指定的VPCID必须与集群的VPCID相同。
        :type Filters: list of Filter
        :param VagueIpAddress: 实例IP进行过滤(同时支持内网IP和外网IP)
        :type VagueIpAddress: str
        :param VagueInstanceName: 实例名称进行过滤
        :type VagueInstanceName: str
        :param Offset: 偏移量，默认为0。关于Offset的更进一步介绍请参考 API 简介中的相关小节。
        :type Offset: int
        :param Limit: 返回数量，默认为20，最大值为100。关于Limit的更进一步介绍请参考 API 简介中的相关小节。
        :type Limit: int
        """
        self.ClusterId = None
        self.InstanceIds = None
        self.Filters = None
        self.VagueIpAddress = None
        self.VagueInstanceName = None
        self.Offset = None
        self.Limit = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.InstanceIds = params.get("InstanceIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.VagueIpAddress = params.get("VagueIpAddress")
        self.VagueInstanceName = params.get("VagueInstanceName")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")


class DescribeExistedInstancesResponse(AbstractModel):
    """DescribeExistedInstances返回参数结构体"""

    def __init__(self):
        """
        :param ExistedInstanceSet: 已经存在的实例信息数组。
        :type ExistedInstanceSet: list of ExistedInstance
        :param TotalCount: 符合条件的实例数量。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ExistedInstanceSet = None
        self.TotalCount = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("ExistedInstanceSet") is not None:
            self.ExistedInstanceSet = []
            for item in params.get("ExistedInstanceSet"):
                obj = ExistedInstance()
                obj._deserialize(item)
                self.ExistedInstanceSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeFlowIdStatusRequest(AbstractModel):
    """DescribeFlowIdStatus请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param RequestFlowId: 开启集群外网访问端口的任务ID
        :type RequestFlowId: int
        """
        self.ClusterId = None
        self.RequestFlowId = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.RequestFlowId = params.get("RequestFlowId")


class DescribeFlowIdStatusResponse(AbstractModel):
    """DescribeFlowIdStatus返回参数结构体"""

    def __init__(self):
        """
        :param Status: 任务状态
        :type Status: str
        :param ErrorMsg: 任务错误信息
        :type ErrorMsg: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Status = None
        self.ErrorMsg = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.ErrorMsg = params.get("ErrorMsg")
        self.RequestId = params.get("RequestId")


class DescribeImagesRequest(AbstractModel):
    """DescribeImages请求参数结构体"""


class DescribeImagesResponse(AbstractModel):
    """DescribeImages返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 镜像数量
        :type TotalCount: int
        :param ImageInstanceSet: 镜像信息列表
        :type ImageInstanceSet: list of ImageInstance
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.ImageInstanceSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("ImageInstanceSet") is not None:
            self.ImageInstanceSet = []
            for item in params.get("ImageInstanceSet"):
                obj = ImageInstance()
                obj._deserialize(item)
                self.ImageInstanceSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInstanceCreateProgressRequest(AbstractModel):
    """DescribeInstanceCreateProgress请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群Id
        :type ClusterId: str
        :param InstanceId: 节点实例Id
        :type InstanceId: str
        """
        self.ClusterId = None
        self.InstanceId = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.InstanceId = params.get("InstanceId")


class DescribeInstanceCreateProgressResponse(AbstractModel):
    """DescribeInstanceCreateProgress返回参数结构体"""

    def __init__(self):
        """
        :param Progress: 创建进度
        :type Progress: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Progress = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Progress = params.get("Progress")
        self.RequestId = params.get("RequestId")


class DescribeInstancesVersionRequest(AbstractModel):
    """DescribeInstancesVersion请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID列表
        :type ClusterId: list of str
        """
        self.ClusterId = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")


class DescribeInstancesVersionResponse(AbstractModel):
    """DescribeInstancesVersion返回参数结构体"""

    def __init__(self):
        """
        :param Clusters: 不同版本节点个数统计结果
        :type Clusters: list of ClusterInstancesVersion
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Clusters = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Clusters") is not None:
            self.Clusters = []
            for item in params.get("Clusters"):
                obj = ClusterInstancesVersion()
                obj._deserialize(item)
                self.Clusters.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeQuotaRequest(AbstractModel):
    """DescribeQuota请求参数结构体"""


class DescribeQuotaResponse(AbstractModel):
    """DescribeQuota返回参数结构体"""

    def __init__(self):
        """
        :param MaxClustersNum: 该账号当前地域支持的最大集群数量
        :type MaxClustersNum: int
        :param MaxNodesNum: 该账号当前地域单集群支持的最大节点数量
        :type MaxNodesNum: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.MaxClustersNum = None
        self.MaxNodesNum = None
        self.RequestId = None

    def _deserialize(self, params):
        self.MaxClustersNum = params.get("MaxClustersNum")
        self.MaxNodesNum = params.get("MaxNodesNum")
        self.RequestId = params.get("RequestId")


class DescribeRegionsRequest(AbstractModel):
    """DescribeRegions请求参数结构体"""


class DescribeRegionsResponse(AbstractModel):
    """DescribeRegions返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 地域的数量
        :type TotalCount: int
        :param RegionInstanceSet: 地域列表
        :type RegionInstanceSet: list of RegionInstance
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.RegionInstanceSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("RegionInstanceSet") is not None:
            self.RegionInstanceSet = []
            for item in params.get("RegionInstanceSet"):
                obj = RegionInstance()
                obj._deserialize(item)
                self.RegionInstanceSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeRouteTableConflictsRequest(AbstractModel):
    """DescribeRouteTableConflicts请求参数结构体"""

    def __init__(self):
        """
        :param RouteTableCidrBlock: 路由表CIDR
        :type RouteTableCidrBlock: str
        :param VpcId: 路由表绑定的VPC
        :type VpcId: str
        """
        self.RouteTableCidrBlock = None
        self.VpcId = None

    def _deserialize(self, params):
        self.RouteTableCidrBlock = params.get("RouteTableCidrBlock")
        self.VpcId = params.get("VpcId")


class DescribeRouteTableConflictsResponse(AbstractModel):
    """DescribeRouteTableConflicts返回参数结构体"""

    def __init__(self):
        """
        :param HasConflict: 路由表是否冲突。
        :type HasConflict: bool
        :param RouteTableConflictSet: 路由表冲突列表。
        :type RouteTableConflictSet: list of RouteTableConflict
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.HasConflict = None
        self.RouteTableConflictSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.HasConflict = params.get("HasConflict")
        if params.get("RouteTableConflictSet") is not None:
            self.RouteTableConflictSet = []
            for item in params.get("RouteTableConflictSet"):
                obj = RouteTableConflict()
                obj._deserialize(item)
                self.RouteTableConflictSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeUpgradeClusterProgressRequest(AbstractModel):
    """DescribeUpgradeClusterProgress请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群实例ID
        :type ClusterId: str
        """
        self.ClusterId = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")


class DescribeUpgradeClusterProgressResponse(AbstractModel):
    """DescribeUpgradeClusterProgress返回参数结构体"""

    def __init__(self):
        """
        :param Steps: 集群升级整体进度
        :type Steps: :class:`tcecloud.tke.v20180525.models.TaskStepInfo`
        :param Instances: 每个节点的进度
        :type Instances: :class:`tcecloud.tke.v20180525.models.TaskStepInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Steps = None
        self.Instances = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Steps") is not None:
            self.Steps = TaskStepInfo()
            self.Steps._deserialize(params.get("Steps"))
        if params.get("Instances") is not None:
            self.Instances = TaskStepInfo()
            self.Instances._deserialize(params.get("Instances"))
        self.RequestId = params.get("RequestId")


class DescribeVersionsRequest(AbstractModel):
    """DescribeVersions请求参数结构体"""


class DescribeVersionsResponse(AbstractModel):
    """DescribeVersions返回参数结构体"""

    def __init__(self):
        """
        :param TotalCount: 版本数量
        :type TotalCount: int
        :param VersionInstanceSet: 版本列表
        :type VersionInstanceSet: list of VersionInstance
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.VersionInstanceSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("VersionInstanceSet") is not None:
            self.VersionInstanceSet = []
            for item in params.get("VersionInstanceSet"):
                obj = VersionInstance()
                obj._deserialize(item)
                self.VersionInstanceSet.append(obj)
        self.RequestId = params.get("RequestId")


class DrainClusterNodeRequest(AbstractModel):
    """DrainClusterNode请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param InstanceId: 实例ID
        :type InstanceId: str
        :param DryRun: 是否只是拉取列表
        :type DryRun: bool
        """
        self.ClusterId = None
        self.InstanceId = None
        self.DryRun = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.InstanceId = params.get("InstanceId")
        self.DryRun = params.get("DryRun")


class DrainClusterNodeResponse(AbstractModel):
    """DrainClusterNode返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class EnableVpcPeerClusterRoutesRequest(AbstractModel):
    """EnableVpcPeerClusterRoutes请求参数结构体"""

    def __init__(self):
        """
        :param RouteTableName: 路由表名称
        :type RouteTableName: str
        :param VpcPeerId: 对等连接实例ID
        :type VpcPeerId: str
        """
        self.RouteTableName = None
        self.VpcPeerId = None

    def _deserialize(self, params):
        self.RouteTableName = params.get("RouteTableName")
        self.VpcPeerId = params.get("VpcPeerId")


class EnableVpcPeerClusterRoutesResponse(AbstractModel):
    """EnableVpcPeerClusterRoutes返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class EnhancedService(AbstractModel):
    """描述了实例的增强服务启用情况与其设置，如云安全，云监控等实例 Agent"""

    def __init__(self):
        """
        :param SecurityService: 开启云安全服务。若不指定该参数，则默认开启云安全服务。
        :type SecurityService: :class:`tcecloud.tke.v20180525.models.RunSecurityServiceEnabled`
        :param MonitorService: 开启云安全服务。若不指定该参数，则默认开启云监控服务。
        :type MonitorService: :class:`tcecloud.tke.v20180525.models.RunMonitorServiceEnabled`
        """
        self.SecurityService = None
        self.MonitorService = None

    def _deserialize(self, params):
        if params.get("SecurityService") is not None:
            self.SecurityService = RunSecurityServiceEnabled()
            self.SecurityService._deserialize(params.get("SecurityService"))
        if params.get("MonitorService") is not None:
            self.MonitorService = RunMonitorServiceEnabled()
            self.MonitorService._deserialize(params.get("MonitorService"))


class Evaluator(AbstractModel):
    """告警指标判断逻辑结构体"""

    def __init__(self):
        """
        :param Type: 告警判断类型，目前支持gt和lt两种
        :type Type: str
        :param Value: 告警设置的阈值
        :type Value: float
        """
        self.Type = None
        self.Value = None

    def _deserialize(self, params):
        self.Type = params.get("Type")
        self.Value = params.get("Value")


class ExistedInstance(AbstractModel):
    """已经存在的实例信息"""

    def __init__(self):
        """
                :param Usable: 实例是否支持加入集群(TRUE 可以加入 FALSE 不能加入)。
        注意：此字段可能返回 null，表示取不到有效值。
                :type Usable: bool
                :param UnusableReason: 实例不支持加入的原因。
        注意：此字段可能返回 null，表示取不到有效值。
                :type UnusableReason: str
                :param AlreadyInCluster: 实例已经所在的集群ID。
        注意：此字段可能返回 null，表示取不到有效值。
                :type AlreadyInCluster: str
                :param InstanceId: 实例ID形如：ins-xxxxxxxx。
                :type InstanceId: str
                :param InstanceName: 实例名称。
        注意：此字段可能返回 null，表示取不到有效值。
                :type InstanceName: str
                :param PrivateIpAddresses: 实例主网卡的内网IP列表。
        注意：此字段可能返回 null，表示取不到有效值。
                :type PrivateIpAddresses: list of str
                :param PublicIpAddresses: 实例主网卡的公网IP列表。
        注意：此字段可能返回 null，表示取不到有效值。
        注意：此字段可能返回 null，表示取不到有效值。
                :type PublicIpAddresses: list of str
                :param CreatedTime: 创建时间。按照ISO8601标准表示，并且使用UTC时间。格式为：YYYY-MM-DDThh:mm:ssZ。
        注意：此字段可能返回 null，表示取不到有效值。
                :type CreatedTime: str
                :param InstanceChargeType: 实例计费模式。取值范围：
        PREPAID：表示预付费，即包年包月
        POSTPAID_BY_HOUR：表示后付费，即按量计费
        CDHPAID：CDH付费，即只对CDH计费，不对CDH上的实例计费。
        注意：此字段可能返回 null，表示取不到有效值。
                :type InstanceChargeType: str
                :param CPU: 实例的CPU核数，单位：核。
        注意：此字段可能返回 null，表示取不到有效值。
                :type CPU: int
                :param Memory: 实例内存容量，单位：GB。
        注意：此字段可能返回 null，表示取不到有效值。
                :type Memory: int
                :param OsName: 操作系统名称。
        注意：此字段可能返回 null，表示取不到有效值。
                :type OsName: str
                :param InstanceType: 实例机型。
        注意：此字段可能返回 null，表示取不到有效值。
                :type InstanceType: str
        """
        self.Usable = None
        self.UnusableReason = None
        self.AlreadyInCluster = None
        self.InstanceId = None
        self.InstanceName = None
        self.PrivateIpAddresses = None
        self.PublicIpAddresses = None
        self.CreatedTime = None
        self.InstanceChargeType = None
        self.CPU = None
        self.Memory = None
        self.OsName = None
        self.InstanceType = None

    def _deserialize(self, params):
        self.Usable = params.get("Usable")
        self.UnusableReason = params.get("UnusableReason")
        self.AlreadyInCluster = params.get("AlreadyInCluster")
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.PrivateIpAddresses = params.get("PrivateIpAddresses")
        self.PublicIpAddresses = params.get("PublicIpAddresses")
        self.CreatedTime = params.get("CreatedTime")
        self.InstanceChargeType = params.get("InstanceChargeType")
        self.CPU = params.get("CPU")
        self.Memory = params.get("Memory")
        self.OsName = params.get("OsName")
        self.InstanceType = params.get("InstanceType")


class ExistedInstancesForNode(AbstractModel):
    """不同角色的已存在节点配置参数"""

    def __init__(self):
        """
        :param NodeRole: 节点角色，取值:MASTER_ETCD, WORKER。MASTER_ETCD只有在创建 INDEPENDENT_CLUSTER 独立集群时需要指定。MASTER_ETCD节点数量为3～7，建议为奇数。MASTER_ETCD最小配置为4C8G。
        :type NodeRole: str
        :param ExistedInstancesPara: 已存在实例的重装参数
        :type ExistedInstancesPara: :class:`tcecloud.tke.v20180525.models.ExistedInstancesPara`
        :param InstanceAdvancedSettingsOverride: 节点高级设置，会覆盖集群级别设置的InstanceAdvancedSettings（当前只对节点自定义参数ExtraArgs生效）
        :type InstanceAdvancedSettingsOverride: :class:`tcecloud.tke.v20180525.models.InstanceAdvancedSettings`
        """
        self.NodeRole = None
        self.ExistedInstancesPara = None
        self.InstanceAdvancedSettingsOverride = None

    def _deserialize(self, params):
        self.NodeRole = params.get("NodeRole")
        if params.get("ExistedInstancesPara") is not None:
            self.ExistedInstancesPara = ExistedInstancesPara()
            self.ExistedInstancesPara._deserialize(params.get("ExistedInstancesPara"))
        if params.get("InstanceAdvancedSettingsOverride") is not None:
            self.InstanceAdvancedSettingsOverride = InstanceAdvancedSettings()
            self.InstanceAdvancedSettingsOverride._deserialize(params.get("InstanceAdvancedSettingsOverride"))


class ExistedInstancesPara(AbstractModel):
    """已存在实例的重装参数"""

    def __init__(self):
        """
        :param InstanceIds: 集群ID
        :type InstanceIds: list of str
        :param InstanceAdvancedSettings: 实例额外需要设置参数信息
        :type InstanceAdvancedSettings: :class:`tcecloud.tke.v20180525.models.InstanceAdvancedSettings`
        :param EnhancedService: 增强服务。通过该参数可以指定是否开启云安全、云监控等服务。若不指定该参数，则默认开启云监控、云安全服务。
        :type EnhancedService: str
        :param LoginSettings: 节点登录信息（目前仅支持使用Password或者单个KeyIds）
        :type LoginSettings: str
        :param SecurityGroupIds: 实例所属安全组。该参数可以通过调用 DescribeSecurityGroups 的返回值中的sgId字段来获取。若不指定该参数，则绑定默认安全组。
        :type SecurityGroupIds: list of str
        :param HostName: 重装系统时，可以指定修改实例的HostName(集群为HostName模式时，此参数必传，规则名称除不支持大写字符外与CVM创建实例接口HostName一致)
        :type HostName: str
        """
        self.InstanceIds = None
        self.InstanceAdvancedSettings = None
        self.EnhancedService = None
        self.LoginSettings = None
        self.SecurityGroupIds = None
        self.HostName = None

    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        if params.get("InstanceAdvancedSettings") is not None:
            self.InstanceAdvancedSettings = InstanceAdvancedSettings()
            self.InstanceAdvancedSettings._deserialize(params.get("InstanceAdvancedSettings"))
        self.EnhancedService = params.get("EnhancedService")
        self.LoginSettings = params.get("LoginSettings")
        self.SecurityGroupIds = params.get("SecurityGroupIds")
        self.HostName = params.get("HostName")


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


class Flag(AbstractModel):
    """参数描述"""

    def __init__(self):
        """
        :param Name: 参数名
        :type Name: str
        :param Type: 参数类型
        :type Type: str
        :param Usage: 参数描述
        :type Usage: str
        :param Default: 参数默认值
        :type Default: str
        :param Constraint: 参数可选范围（目前包含range和in两种，"[]"代表range，如"[1, 5]"表示参数必须>=1且 <=5, "()"代表in， 如"('aa', 'bb')"表示参数只能为字符串'aa'或者'bb'，该参数为空表示不校验）
        :type Constraint: str
        """
        self.Name = None
        self.Type = None
        self.Usage = None
        self.Default = None
        self.Constraint = None

    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Type = params.get("Type")
        self.Usage = params.get("Usage")
        self.Default = params.get("Default")
        self.Constraint = params.get("Constraint")


class ForwardRequestRequest(AbstractModel):
    """ForwardRequest请求参数结构体"""

    def __init__(self):
        """
        :param Method: 请求tke-apiserver http请求对应的方法
        :type Method: str
        :param Path: 请求tke-apiserver  http请求访问路径
        :type Path: str
        :param Accept: 请求tke-apiserver http头中Accept参数
        :type Accept: str
        :param ContentType: 请求tke-apiserver http头中ContentType参数
        :type ContentType: str
        :param RequestBody: 请求tke-apiserver http请求body信息
        :type RequestBody: str
        :param ClusterName: 请求tke-apiserver http头中X-TKE-ClusterName参数
        :type ClusterName: str
        :param EncodedBody: 是否编码请求body信息
        :type EncodedBody: bool
        """
        self.Method = None
        self.Path = None
        self.Accept = None
        self.ContentType = None
        self.RequestBody = None
        self.ClusterName = None
        self.EncodedBody = None

    def _deserialize(self, params):
        self.Method = params.get("Method")
        self.Path = params.get("Path")
        self.Accept = params.get("Accept")
        self.ContentType = params.get("ContentType")
        self.RequestBody = params.get("RequestBody")
        self.ClusterName = params.get("ClusterName")
        self.EncodedBody = params.get("EncodedBody")


class ForwardRequestResponse(AbstractModel):
    """ForwardRequest返回参数结构体"""

    def __init__(self):
        """
        :param ResponseBody: 请求tke-apiserver http请求返回的body信息
        :type ResponseBody: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ResponseBody = None
        self.RequestId = None

    def _deserialize(self, params):
        self.ResponseBody = params.get("ResponseBody")
        self.RequestId = params.get("RequestId")


class GetUpgradeClusterProgressRequest(AbstractModel):
    """GetUpgradeClusterProgress请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群实例ID
        :type ClusterId: str
        """
        self.ClusterId = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")


class GetUpgradeClusterProgressResponse(AbstractModel):
    """GetUpgradeClusterProgress返回参数结构体"""

    def __init__(self):
        """
        :param Steps: 集群升级整体进度
        :type Steps: :class:`tcecloud.tke.v20180525.models.TaskStepInfo`
        :param Instances: 每个节点的进度
        :type Instances: :class:`tcecloud.tke.v20180525.models.TaskStepInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Steps = None
        self.Instances = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Steps") is not None:
            self.Steps = TaskStepInfo()
            self.Steps._deserialize(params.get("Steps"))
        if params.get("Instances") is not None:
            self.Instances = TaskStepInfo()
            self.Instances._deserialize(params.get("Instances"))
        self.RequestId = params.get("RequestId")


class GetUpgradeInstanceProgressRequest(AbstractModel):
    """GetUpgradeInstanceProgress请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param Limit: 最多获取多少个节点的进度
        :type Limit: int
        :param Offset: 从第几个节点开始获取进度
        :type Offset: int
        """
        self.ClusterId = None
        self.Limit = None
        self.Offset = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")


class GetUpgradeInstanceProgressResponse(AbstractModel):
    """GetUpgradeInstanceProgress返回参数结构体"""

    def __init__(self):
        """
                :param Total: 升级节点总数
                :type Total: int
                :param Done: 已升级节点总数
                :type Done: int
                :param LifeState: 升级任务生命周期
        process 运行中
        paused 已停止
        pauing 正在停止
        done  已完成
        timeout 已超时
        aborted 已取消
                :type LifeState: str
                :param Instances: 各节点升级进度详情
                :type Instances: list of InstanceUpgradeProgressItem
                :param ClusterStatus: 集群当前状态
                :type ClusterStatus: :class:`tcecloud.tke.v20180525.models.InstanceUpgradeClusterStatus`
                :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
                :type RequestId: str
        """
        self.Total = None
        self.Done = None
        self.LifeState = None
        self.Instances = None
        self.ClusterStatus = None
        self.RequestId = None

    def _deserialize(self, params):
        self.Total = params.get("Total")
        self.Done = params.get("Done")
        self.LifeState = params.get("LifeState")
        if params.get("Instances") is not None:
            self.Instances = []
            for item in params.get("Instances"):
                obj = InstanceUpgradeProgressItem()
                obj._deserialize(item)
                self.Instances.append(obj)
        if params.get("ClusterStatus") is not None:
            self.ClusterStatus = InstanceUpgradeClusterStatus()
            self.ClusterStatus._deserialize(params.get("ClusterStatus"))
        self.RequestId = params.get("RequestId")


class GetVbcInstanceRequest(AbstractModel):
    """GetVbcInstance请求参数结构体"""

    def __init__(self):
        """
        :param UnVpcId: vpc唯一id
        :type UnVpcId: str
        """
        self.UnVpcId = None

    def _deserialize(self, params):
        self.UnVpcId = params.get("UnVpcId")


class GetVbcInstanceResponse(AbstractModel):
    """GetVbcInstance返回参数结构体"""

    def __init__(self):
        """
        :param Detail: 详情
        :type Detail: list of CcnRoute
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Detail = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Detail") is not None:
            self.Detail = []
            for item in params.get("Detail"):
                obj = CcnRoute()
                obj._deserialize(item)
                self.Detail.append(obj)
        self.RequestId = params.get("RequestId")


class GetVbcRouteRequest(AbstractModel):
    """GetVbcRoute请求参数结构体"""

    def __init__(self):
        """
        :param UnVpcId: vpc唯一id
        :type UnVpcId: str
        :param ClusterCIDR: 集群cidr
        :type ClusterCIDR: str
        """
        self.UnVpcId = None
        self.ClusterCIDR = None

    def _deserialize(self, params):
        self.UnVpcId = params.get("UnVpcId")
        self.ClusterCIDR = params.get("ClusterCIDR")


class GetVbcRouteResponse(AbstractModel):
    """GetVbcRoute返回参数结构体"""

    def __init__(self):
        """
        :param Detail: 详情
        :type Detail: list of CcnRoute
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Detail = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Detail") is not None:
            self.Detail = []
            for item in params.get("Detail"):
                obj = CcnRoute()
                obj._deserialize(item)
                self.Detail.append(obj)
        self.RequestId = params.get("RequestId")


class HostNameValue(AbstractModel):
    """节点主机名称结构"""

    def __init__(self):
        """
        :param Name: 主机名称
        :type Name: str
        :param Value: 主机数量
        :type Value: int
        """
        self.Name = None
        self.Value = None

    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Value = params.get("Value")


class ImageInstance(AbstractModel):
    """镜像信息"""

    def __init__(self):
        """
                :param Alias: 镜像别名
        注意：此字段可能返回 null，表示取不到有效值。
                :type Alias: str
                :param OsName: 操作系统名称
        注意：此字段可能返回 null，表示取不到有效值。
                :type OsName: str
                :param ImageId: 镜像ID
        注意：此字段可能返回 null，表示取不到有效值。
                :type ImageId: str
                :param OsCustomizeType: 容器的镜像版本，"DOCKER_CUSTOMIZE"(容器定制版),"GENERAL"(普通版本，默认值)
        注意：此字段可能返回 null，表示取不到有效值。
                :type OsCustomizeType: str
        """
        self.Alias = None
        self.OsName = None
        self.ImageId = None
        self.OsCustomizeType = None

    def _deserialize(self, params):
        self.Alias = params.get("Alias")
        self.OsName = params.get("OsName")
        self.ImageId = params.get("ImageId")
        self.OsCustomizeType = params.get("OsCustomizeType")


class Instance(AbstractModel):
    """集群的实例信息"""

    def __init__(self):
        """
                :param InstanceId: 实例ID
                :type InstanceId: str
                :param InstanceRole: 节点角色, MASTER, WORKER, ETCD, MASTER_ETCD,ALL, 默认为WORKER
                :type InstanceRole: str
                :param FailedReason: 实例异常(或者处于初始化中)的原因
                :type FailedReason: str
                :param InstanceState: 实例的状态（running 运行中，initializing 初始化中，failed 异常）
                :type InstanceState: str
                :param DrainStatus: 实例是否封锁状态
        注意：此字段可能返回 null，表示取不到有效值。
                :type DrainStatus: str
                :param InstanceAdvancedSettings: 节点配置
        注意：此字段可能返回 null，表示取不到有效值。
                :type InstanceAdvancedSettings: :class:`tcecloud.tke.v20180525.models.InstanceAdvancedSettings`
                :param CreatedTime: 添加时间
                :type CreatedTime: str
        """
        self.InstanceId = None
        self.InstanceRole = None
        self.FailedReason = None
        self.InstanceState = None
        self.DrainStatus = None
        self.InstanceAdvancedSettings = None
        self.CreatedTime = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.InstanceRole = params.get("InstanceRole")
        self.FailedReason = params.get("FailedReason")
        self.InstanceState = params.get("InstanceState")
        self.DrainStatus = params.get("DrainStatus")
        if params.get("InstanceAdvancedSettings") is not None:
            self.InstanceAdvancedSettings = InstanceAdvancedSettings()
            self.InstanceAdvancedSettings._deserialize(params.get("InstanceAdvancedSettings"))
        self.CreatedTime = params.get("CreatedTime")


class InstanceAdvancedSettings(AbstractModel):
    """描述了k8s集群相关配置与信息。"""

    def __init__(self):
        """
        :param MountTarget: 数据盘挂载点, 默认不挂载数据盘. 已格式化的 ext3，ext4，xfs 文件系统的数据盘将直接挂载，其他文件系统或未格式化的数据盘将自动格式化为ext4 并挂载，请注意备份数据! 无数据盘或有多块数据盘的云主机此设置不生效。
        :type MountTarget: str
        :param DockerGraphPath: dockerd --graph 指定值, 默认为 /var/lib/docker
        :type DockerGraphPath: str
        :param UserScript: base64 编码的用户脚本, 此脚本会在 k8s 组件运行后执行, 需要用户保证脚本的可重入及重试逻辑, 脚本及其生成的日志文件可在节点的 /data/ccs_userscript/ 路径查看, 如果要求节点需要在进行初始化完成后才可加入调度, 可配合 unschedulable 参数使用, 在 userScript 最后初始化完成后, 添加 kubectl uncordon nodename --kubeconfig=/root/.kube/config 命令使节点加入调度
        :type UserScript: str
        :param Unschedulable: 设置加入的节点是否参与调度，默认值为0，表示参与调度；非0表示不参与调度, 待节点初始化完成之后, 可执行kubectl uncordon nodename使node加入调度.
        :type Unschedulable: int
        :param Labels: 节点Label数组
        :type Labels: list of Label
        :param DataDisks: 数据盘相关信息
        :type DataDisks: list of DataDisk
        :param ExtraArgs: 节点相关的自定义参数信息
        :type ExtraArgs: :class:`tcecloud.tke.v20180525.models.InstanceExtraArgs`
        """
        self.MountTarget = None
        self.DockerGraphPath = None
        self.UserScript = None
        self.Unschedulable = None
        self.Labels = None
        self.DataDisks = None
        self.ExtraArgs = None

    def _deserialize(self, params):
        self.MountTarget = params.get("MountTarget")
        self.DockerGraphPath = params.get("DockerGraphPath")
        self.UserScript = params.get("UserScript")
        self.Unschedulable = params.get("Unschedulable")
        if params.get("Labels") is not None:
            self.Labels = []
            for item in params.get("Labels"):
                obj = Label()
                obj._deserialize(item)
                self.Labels.append(obj)
        if params.get("DataDisks") is not None:
            self.DataDisks = []
            for item in params.get("DataDisks"):
                obj = DataDisk()
                obj._deserialize(item)
                self.DataDisks.append(obj)
        if params.get("ExtraArgs") is not None:
            self.ExtraArgs = InstanceExtraArgs()
            self.ExtraArgs._deserialize(params.get("ExtraArgs"))


class InstanceDataDiskMountSetting(AbstractModel):
    """CVM实例数据盘挂载配置"""

    def __init__(self):
        """
        :param InstanceType: CVM实例类型
        :type InstanceType: str
        :param DataDisks: 数据盘挂载信息
        :type DataDisks: list of DataDisk
        :param Zone: CVM实例所属可用区
        :type Zone: str
        """
        self.InstanceType = None
        self.DataDisks = None
        self.Zone = None

    def _deserialize(self, params):
        self.InstanceType = params.get("InstanceType")
        if params.get("DataDisks") is not None:
            self.DataDisks = []
            for item in params.get("DataDisks"):
                obj = DataDisk()
                obj._deserialize(item)
                self.DataDisks.append(obj)
        self.Zone = params.get("Zone")


class InstanceExtraArgs(AbstractModel):
    """节点自定义参数"""

    def __init__(self):
        """
                :param Kubelet: kubelet自定义参数
        注意：此字段可能返回 null，表示取不到有效值。
                :type Kubelet: list of str
        """
        self.Kubelet = None

    def _deserialize(self, params):
        self.Kubelet = params.get("Kubelet")


class InstanceUpgradeClusterStatus(AbstractModel):
    """节点升级过程中集群当前状态"""

    def __init__(self):
        """
        :param PodTotal: pod总数
        :type PodTotal: int
        :param NotReadyPod: NotReady pod总数
        :type NotReadyPod: int
        """
        self.PodTotal = None
        self.NotReadyPod = None

    def _deserialize(self, params):
        self.PodTotal = params.get("PodTotal")
        self.NotReadyPod = params.get("NotReadyPod")


class InstanceUpgradePreCheckResult(AbstractModel):
    """某个节点升级前检查结果"""

    def __init__(self):
        """
        :param CheckPass: 检查是否通过
        :type CheckPass: bool
        :param Items: 检查项数组
        :type Items: list of InstanceUpgradePreCheckResultItem
        :param SinglePods: 本节点独立pod列表
        :type SinglePods: list of str
        """
        self.CheckPass = None
        self.Items = None
        self.SinglePods = None

    def _deserialize(self, params):
        self.CheckPass = params.get("CheckPass")
        if params.get("Items") is not None:
            self.Items = []
            for item in params.get("Items"):
                obj = InstanceUpgradePreCheckResultItem()
                obj._deserialize(item)
                self.Items.append(obj)
        self.SinglePods = params.get("SinglePods")


class InstanceUpgradePreCheckResultItem(AbstractModel):
    """节点升级检查项结果"""

    def __init__(self):
        """
        :param Namespace: 工作负载的命名空间
        :type Namespace: str
        :param WorkLoadKind: 工作负载类型
        :type WorkLoadKind: str
        :param WorkLoadName: 工作负载名称
        :type WorkLoadName: str
        :param Before: 驱逐节点前工作负载running的pod数目
        :type Before: int
        :param After: 驱逐节点后工作负载running的pod数目
        :type After: int
        :param Pods: 工作负载在本节点上的pod列表
        :type Pods: list of str
        """
        self.Namespace = None
        self.WorkLoadKind = None
        self.WorkLoadName = None
        self.Before = None
        self.After = None
        self.Pods = None

    def _deserialize(self, params):
        self.Namespace = params.get("Namespace")
        self.WorkLoadKind = params.get("WorkLoadKind")
        self.WorkLoadName = params.get("WorkLoadName")
        self.Before = params.get("Before")
        self.After = params.get("After")
        self.Pods = params.get("Pods")


class InstanceUpgradeProgressItem(AbstractModel):
    """某个节点的升级进度"""

    def __init__(self):
        """
                :param InstanceID: 节点instanceID
                :type InstanceID: str
                :param LifeState: 任务生命周期
        process 运行中
        paused 已停止
        pauing 正在停止
        done  已完成
        timeout 已超时
        aborted 已取消
        pending 还未开始
                :type LifeState: str
                :param StartAt: 升级开始时间
        注意：此字段可能返回 null，表示取不到有效值。
                :type StartAt: str
                :param EndAt: 升级结束时间
        注意：此字段可能返回 null，表示取不到有效值。
                :type EndAt: str
                :param CheckResult: 升级前检查结果
                :type CheckResult: :class:`tcecloud.tke.v20180525.models.InstanceUpgradePreCheckResult`
                :param Detail: 升级步骤详情
                :type Detail: list of TaskStepInfo
        """
        self.InstanceID = None
        self.LifeState = None
        self.StartAt = None
        self.EndAt = None
        self.CheckResult = None
        self.Detail = None

    def _deserialize(self, params):
        self.InstanceID = params.get("InstanceID")
        self.LifeState = params.get("LifeState")
        self.StartAt = params.get("StartAt")
        self.EndAt = params.get("EndAt")
        if params.get("CheckResult") is not None:
            self.CheckResult = InstanceUpgradePreCheckResult()
            self.CheckResult._deserialize(params.get("CheckResult"))
        if params.get("Detail") is not None:
            self.Detail = []
            for item in params.get("Detail"):
                obj = TaskStepInfo()
                obj._deserialize(item)
                self.Detail.append(obj)


class Label(AbstractModel):
    """k8s中标签，一般以数组的方式存在"""

    def __init__(self):
        """
        :param Name: map表中的Name
        :type Name: str
        :param Value: map表中的Value
        :type Value: str
        """
        self.Name = None
        self.Value = None

    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Value = params.get("Value")


class LogSet(AbstractModel):
    """日志集"""

    def __init__(self):
        """
        :param LogSetId: 日志集ID
        :type LogSetId: str
        :param LogSetName: 日志集名称
        :type LogSetName: list of str
        :param Period: 周期
        :type Period: int
        :param CreateTime: 创建时间
        :type CreateTime: str
        """
        self.LogSetId = None
        self.LogSetName = None
        self.Period = None
        self.CreateTime = None

    def _deserialize(self, params):
        self.LogSetId = params.get("LogSetId")
        self.LogSetName = params.get("LogSetName")
        self.Period = params.get("Period")
        self.CreateTime = params.get("CreateTime")


class LogTopic(AbstractModel):
    """日志主题"""

    def __init__(self):
        """
        :param LogSetId: 日志集ID
        :type LogSetId: str
        :param TopicId: 日志主题ID
        :type TopicId: str
        :param TopicName: 日志主题名称
        :type TopicName: str
        :param Path: 路径
        :type Path: str
        :param CreateTime: 创建时间
        :type CreateTime: str
        :param LogType: 日志类型
        :type LogType: str
        :param Collection: 是否采集
        :type Collection: bool
        :param Index: 是否有索引
        :type Index: bool
        """
        self.LogSetId = None
        self.TopicId = None
        self.TopicName = None
        self.Path = None
        self.CreateTime = None
        self.LogType = None
        self.Collection = None
        self.Index = None

    def _deserialize(self, params):
        self.LogSetId = params.get("LogSetId")
        self.TopicId = params.get("TopicId")
        self.TopicName = params.get("TopicName")
        self.Path = params.get("Path")
        self.CreateTime = params.get("CreateTime")
        self.LogType = params.get("LogType")
        self.Collection = params.get("Collection")
        self.Index = params.get("Index")


class LoginSettings(AbstractModel):
    """描述了实例登录相关配置与信息。"""

    def __init__(self):
        """
        :param Password: 实例登录密码。不同操作系统类型密码复杂度限制不一样，具体如下：<br><li>Linux实例密码必须8到16位，至少包括两项[a-z，A-Z]、[0-9] 和 [( ) ` ~ ! @ # $ % ^ & * - + = | { } [ ] : ; ' , . ? / ]中的特殊符号。<br><li>Windows实例密码必须12到16位，至少包括三项[a-z]，[A-Z]，[0-9] 和 [( ) ` ~ ! @ # $ % ^ & * - + = { } [ ] : ; ' , . ? /]中的特殊符号。<br><br>若不指定该参数，则由系统随机生成密码，并通过站内信方式通知到用户。
        :type Password: str
        :param KeyIds: 密钥ID列表。关联密钥后，就可以通过对应的私钥来访问实例；KeyId可通过接口DescribeKeyPairs获取，密钥与密码不能同时指定，同时Windows操作系统不支持指定密钥。当前仅支持购买的时候指定一个密钥。
        :type KeyIds: list of str
        :param KeepImageLogin: 保持镜像的原始设置。该参数与Password或KeyIds.N不能同时指定。只有使用自定义镜像、共享镜像或外部导入镜像创建实例时才能指定该参数为TRUE。取值范围：<br><li>TRUE：表示保持镜像的登录设置<br><li>FALSE：表示不保持镜像的登录设置<br><br>默认取值：FALSE。
        :type KeepImageLogin: str
        """
        self.Password = None
        self.KeyIds = None
        self.KeepImageLogin = None

    def _deserialize(self, params):
        self.Password = params.get("Password")
        self.KeyIds = params.get("KeyIds")
        self.KeepImageLogin = params.get("KeepImageLogin")


class ModifyAlarmPolicyRequest(AbstractModel):
    """ModifyAlarmPolicy请求参数结构体"""

    def __init__(self):
        """
        :param ClusterInstanceId: k8s集群ID
        :type ClusterInstanceId: str
        :param AlarmPolicyId: 告警策略ID
        :type AlarmPolicyId: str
        :param Namespace: k8s命名空间
        :type Namespace: str
        :param WorkloadType: k8s工作负载类型，有deplogyment，job，crontab
        :type WorkloadType: str
        :param AlarmPolicySettings: 告警策略settings
        :type AlarmPolicySettings: :class:`tcecloud.tke.v20180525.models.AlarmPolicySettings`
        :param NotifySettings: 告警通知settings
        :type NotifySettings: :class:`tcecloud.tke.v20180525.models.NotifySettings`
        :param ShieldSettings: 告警屏蔽settings
        :type ShieldSettings: :class:`tcecloud.tke.v20180525.models.ShieldSettings`
        """
        self.ClusterInstanceId = None
        self.AlarmPolicyId = None
        self.Namespace = None
        self.WorkloadType = None
        self.AlarmPolicySettings = None
        self.NotifySettings = None
        self.ShieldSettings = None

    def _deserialize(self, params):
        self.ClusterInstanceId = params.get("ClusterInstanceId")
        self.AlarmPolicyId = params.get("AlarmPolicyId")
        self.Namespace = params.get("Namespace")
        self.WorkloadType = params.get("WorkloadType")
        if params.get("AlarmPolicySettings") is not None:
            self.AlarmPolicySettings = AlarmPolicySettings()
            self.AlarmPolicySettings._deserialize(params.get("AlarmPolicySettings"))
        if params.get("NotifySettings") is not None:
            self.NotifySettings = NotifySettings()
            self.NotifySettings._deserialize(params.get("NotifySettings"))
        if params.get("ShieldSettings") is not None:
            self.ShieldSettings = ShieldSettings()
            self.ShieldSettings._deserialize(params.get("ShieldSettings"))


class ModifyAlarmPolicyResponse(AbstractModel):
    """ModifyAlarmPolicy返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyClusterAsGroupAttributeRequest(AbstractModel):
    """ModifyClusterAsGroupAttribute请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param ClusterAsGroupAttribute: 集群关联的伸缩组属性
        :type ClusterAsGroupAttribute: :class:`tcecloud.tke.v20180525.models.ClusterAsGroupAttribute`
        """
        self.ClusterId = None
        self.ClusterAsGroupAttribute = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        if params.get("ClusterAsGroupAttribute") is not None:
            self.ClusterAsGroupAttribute = ClusterAsGroupAttribute()
            self.ClusterAsGroupAttribute._deserialize(params.get("ClusterAsGroupAttribute"))


class ModifyClusterAsGroupAttributeResponse(AbstractModel):
    """ModifyClusterAsGroupAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyClusterAsGroupOptionAttributeRequest(AbstractModel):
    """ModifyClusterAsGroupOptionAttribute请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param ClusterAsGroupOption: 集群弹性伸缩属性
        :type ClusterAsGroupOption: :class:`tcecloud.tke.v20180525.models.ClusterAsGroupOption`
        """
        self.ClusterId = None
        self.ClusterAsGroupOption = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        if params.get("ClusterAsGroupOption") is not None:
            self.ClusterAsGroupOption = ClusterAsGroupOption()
            self.ClusterAsGroupOption._deserialize(params.get("ClusterAsGroupOption"))


class ModifyClusterAsGroupOptionAttributeResponse(AbstractModel):
    """ModifyClusterAsGroupOptionAttribute返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyClusterAttributeRequest(AbstractModel):
    """ModifyClusterAttribute请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param ProjectId: 集群所属项目
        :type ProjectId: int
        :param ClusterName: 集群名称
        :type ClusterName: str
        :param ClusterDesc: 集群描述
        :type ClusterDesc: str
        """
        self.ClusterId = None
        self.ProjectId = None
        self.ClusterName = None
        self.ClusterDesc = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.ProjectId = params.get("ProjectId")
        self.ClusterName = params.get("ClusterName")
        self.ClusterDesc = params.get("ClusterDesc")


class ModifyClusterAttributeResponse(AbstractModel):
    """ModifyClusterAttribute返回参数结构体"""

    def __init__(self):
        """
        :param ProjectId: 集群所属项目
        :type ProjectId: int
        :param ClusterName: 集群名称
        :type ClusterName: str
        :param ClusterDesc: 集群描述
        :type ClusterDesc: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ProjectId = None
        self.ClusterName = None
        self.ClusterDesc = None
        self.RequestId = None

    def _deserialize(self, params):
        self.ProjectId = params.get("ProjectId")
        self.ClusterName = params.get("ClusterName")
        self.ClusterDesc = params.get("ClusterDesc")
        self.RequestId = params.get("RequestId")


class ModifyClusterEndpointSPRequest(AbstractModel):
    """ModifyClusterEndpointSP请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param SecurityPolicies: 安全策略放通单个IP或CIDR(例如: "192.168.1.0/24",默认为拒绝所有)
        :type SecurityPolicies: list of str
        """
        self.ClusterId = None
        self.SecurityPolicies = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.SecurityPolicies = params.get("SecurityPolicies")


class ModifyClusterEndpointSPResponse(AbstractModel):
    """ModifyClusterEndpointSP返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyClusterImageRequest(AbstractModel):
    """ModifyClusterImage请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param ImageId: 指定有效的镜像ID，格式形如img-xxxx。可通过登录控制台查询，也可调用接口 DescribeImages，取返回信息中的ImageId字段。
        :type ImageId: str
        :param OsCustomizeType: "DOCKER_CUSTOMIZE"(容器定制版),"GENERAL"(普通版本，默认值)
        :type OsCustomizeType: str
        """
        self.ClusterId = None
        self.ImageId = None
        self.OsCustomizeType = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.ImageId = params.get("ImageId")
        self.OsCustomizeType = params.get("OsCustomizeType")


class ModifyClusterImageResponse(AbstractModel):
    """ModifyClusterImage返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyClusterInspectionRequest(AbstractModel):
    """ModifyClusterInspection请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群实例id
        :type ClusterId: str
        :param Cron: 自动巡检周期
        :type Cron: str
        """
        self.ClusterId = None
        self.Cron = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.Cron = params.get("Cron")


class ModifyClusterInspectionResponse(AbstractModel):
    """ModifyClusterInspection返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyClusterUpgradingStateRequest(AbstractModel):
    """ModifyClusterUpgradingState请求参数结构体"""

    def __init__(self):
        """
                :param ClusterId: 集群实例ID
                :type ClusterId: str
                :param Operation: 操作类型：
        pause 暂停集群升级
        resume 继续集群升级
        abort 取消集群升级
                :type Operation: str
                :param ForceAbort: 如果是取消集群升级，该参数设置为true表示强制取消
                :type ForceAbort: bool
        """
        self.ClusterId = None
        self.Operation = None
        self.ForceAbort = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.Operation = params.get("Operation")
        self.ForceAbort = params.get("ForceAbort")


class ModifyClusterUpgradingStateResponse(AbstractModel):
    """ModifyClusterUpgradingState返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class NodePoolOption(AbstractModel):
    """加入存量节点时的节点池选项"""

    def __init__(self):
        """
        :param AddToNodePool: 是否加入节点池
        :type AddToNodePool: bool
        :param NodePoolId: 节点池id
        :type NodePoolId: str
        """
        self.AddToNodePool = None
        self.NodePoolId = None

    def _deserialize(self, params):
        self.AddToNodePool = params.get("AddToNodePool")
        self.NodePoolId = params.get("NodePoolId")


class NotReadyPodsItem(AbstractModel):
    """集群某个命名空间下NotReady的Pod集合"""

    def __init__(self):
        """
                :param Namespace: 命名空间名称
                :type Namespace: str
                :param Pods: pod列表
        注意：此字段可能返回 null，表示取不到有效值。
                :type Pods: list of str
        """
        self.Namespace = None
        self.Pods = None

    def _deserialize(self, params):
        self.Namespace = params.get("Namespace")
        self.Pods = params.get("Pods")


class NotifySettings(AbstractModel):
    """告警通知settings"""

    def __init__(self):
        """
                :param ReceiverGroups: 告警接收组（用户组）
                :type ReceiverGroups: list of int
                :param NotifyWay: 告警通知方式。目前有SMS、EMAIL、CALL、WECHAT方式。
        分别代表：短信、邮件、电话、微信
                :type NotifyWay: list of str
                :param PhoneNotifyOrder: 电话告警顺序。
        注：NotifyWay选择CALL，采用该参数。
        注意：此字段可能返回 null，表示取不到有效值。
                :type PhoneNotifyOrder: list of int
                :param PhoneCircleTimes: 电话告警次数。
        注：NotifyWay选择CALL，采用该参数。
        注意：此字段可能返回 null，表示取不到有效值。
                :type PhoneCircleTimes: int
                :param PhoneInnerInterval: 电话告警轮内间隔。单位：秒
        注：NotifyWay选择CALL，采用该参数。
        注意：此字段可能返回 null，表示取不到有效值。
                :type PhoneInnerInterval: int
                :param PhoneCircleInterval: 电话告警轮外间隔。单位：秒
        注：NotifyWay选择CALL，采用该参数。
        注意：此字段可能返回 null，表示取不到有效值。
                :type PhoneCircleInterval: int
                :param PhoneArriveNotice: 电话告警触达通知
        注：NotifyWay选择CALL，采用该参数。
        注意：此字段可能返回 null，表示取不到有效值。
                :type PhoneArriveNotice: int
        """
        self.ReceiverGroups = None
        self.NotifyWay = None
        self.PhoneNotifyOrder = None
        self.PhoneCircleTimes = None
        self.PhoneInnerInterval = None
        self.PhoneCircleInterval = None
        self.PhoneArriveNotice = None

    def _deserialize(self, params):
        self.ReceiverGroups = params.get("ReceiverGroups")
        self.NotifyWay = params.get("NotifyWay")
        self.PhoneNotifyOrder = params.get("PhoneNotifyOrder")
        self.PhoneCircleTimes = params.get("PhoneCircleTimes")
        self.PhoneInnerInterval = params.get("PhoneInnerInterval")
        self.PhoneCircleInterval = params.get("PhoneCircleInterval")
        self.PhoneArriveNotice = params.get("PhoneArriveNotice")


class OpUpgradeClusterInstancesRequest(AbstractModel):
    """OpUpgradeClusterInstances请求参数结构体"""

    def __init__(self):
        """
                :param ClusterId: 节点实例ID
                :type ClusterId: str
                :param Operation: 操作类型
        pause 暂停任务（任务必须处于运行中）
        resume 恢复任务（任务必须处于已暂停状态）
        abort 停止任务（任务必须处于已暂停状态）
                :type Operation: str
        """
        self.ClusterId = None
        self.Operation = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.Operation = params.get("Operation")


class OpUpgradeClusterInstancesResponse(AbstractModel):
    """OpUpgradeClusterInstances返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class PauseClusterInstancesRequest(AbstractModel):
    """PauseClusterInstances请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        """
        self.ClusterId = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")


class PauseClusterInstancesResponse(AbstractModel):
    """PauseClusterInstances返回参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ClusterId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.RequestId = params.get("RequestId")


class PodInfo(AbstractModel):
    """Pod的详细描述信息"""

    def __init__(self):
        """
                :param Name: Pod名称
        注意：此字段可能返回 null，表示取不到有效值。
                :type Name: str
                :param Status: Pod当前状态
        注意：此字段可能返回 null，表示取不到有效值。
                :type Status: str
                :param Reason: 处于当前状态原因
        注意：此字段可能返回 null，表示取不到有效值。
                :type Reason: str
                :param SourceReason: 在kubernetes中展示的原因
        注意：此字段可能返回 null，表示取不到有效值。
                :type SourceReason: str
                :param Ip: Pod IP
        注意：此字段可能返回 null，表示取不到有效值。
                :type Ip: str
                :param RestartCount: Pod重启次数
        注意：此字段可能返回 null，表示取不到有效值。
                :type RestartCount: int
                :param ReadyCount: Pod就绪容器数量
        注意：此字段可能返回 null，表示取不到有效值。
                :type ReadyCount: int
                :param NodeName: 所在节点名称
        注意：此字段可能返回 null，表示取不到有效值。
                :type NodeName: str
                :param NodeIp: 所在节点IP
        注意：此字段可能返回 null，表示取不到有效值。
                :type NodeIp: str
                :param StartTime: Pod启动时间
        注意：此字段可能返回 null，表示取不到有效值。
                :type StartTime: str
                :param Containers: Pod所含容器信息
        注意：此字段可能返回 null，表示取不到有效值。
                :type Containers: list of ContainerStatus
        """
        self.Name = None
        self.Status = None
        self.Reason = None
        self.SourceReason = None
        self.Ip = None
        self.RestartCount = None
        self.ReadyCount = None
        self.NodeName = None
        self.NodeIp = None
        self.StartTime = None
        self.Containers = None

    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Status = params.get("Status")
        self.Reason = params.get("Reason")
        self.SourceReason = params.get("SourceReason")
        self.Ip = params.get("Ip")
        self.RestartCount = params.get("RestartCount")
        self.ReadyCount = params.get("ReadyCount")
        self.NodeName = params.get("NodeName")
        self.NodeIp = params.get("NodeIp")
        self.StartTime = params.get("StartTime")
        if params.get("Containers") is not None:
            self.Containers = []
            for item in params.get("Containers"):
                obj = ContainerStatus()
                obj._deserialize(item)
                self.Containers.append(obj)


class RegionInstance(AbstractModel):
    """地域属性信息"""

    def __init__(self):
        """
                :param RegionName: 地域名称
        注意：此字段可能返回 null，表示取不到有效值。
                :type RegionName: str
                :param RegionId: 地域ID
        注意：此字段可能返回 null，表示取不到有效值。
                :type RegionId: int
                :param Status: 地域状态
        注意：此字段可能返回 null，表示取不到有效值。
                :type Status: str
                :param FeatureGates: 地域特性开关(按照JSON的形式返回所有属性)
        注意：此字段可能返回 null，表示取不到有效值。
                :type FeatureGates: str
                :param Alias: 地域简称
        注意：此字段可能返回 null，表示取不到有效值。
                :type Alias: str
                :param Remark: 地域白名单
        注意：此字段可能返回 null，表示取不到有效值。
                :type Remark: str
        """
        self.RegionName = None
        self.RegionId = None
        self.Status = None
        self.FeatureGates = None
        self.Alias = None
        self.Remark = None

    def _deserialize(self, params):
        self.RegionName = params.get("RegionName")
        self.RegionId = params.get("RegionId")
        self.Status = params.get("Status")
        self.FeatureGates = params.get("FeatureGates")
        self.Alias = params.get("Alias")
        self.Remark = params.get("Remark")


class ResourceStatus(AbstractModel):
    """资源状态"""

    def __init__(self):
        """
        :param ClusterInstanceId: 集群ID
        :type ClusterInstanceId: str
        :param Status: 各资源状态
        :type Status: list of ResourceStatusItem
        """
        self.ClusterInstanceId = None
        self.Status = None

    def _deserialize(self, params):
        self.ClusterInstanceId = params.get("ClusterInstanceId")
        if params.get("Status") is not None:
            self.Status = []
            for item in params.get("Status"):
                obj = ResourceStatusItem()
                obj._deserialize(item)
                self.Status.append(obj)


class ResourceStatusItem(AbstractModel):
    """资源状态"""

    def __init__(self):
        """
        :param Dimension: 维度
        :type Dimension: str
        :param TotalNum: 总数
        :type TotalNum: int
        :param AbnormalNum: 异常数
        :type AbnormalNum: int
        :param AbnormalDetail: 异常详情
        :type AbnormalDetail: list of AbnormalDetail
        """
        self.Dimension = None
        self.TotalNum = None
        self.AbnormalNum = None
        self.AbnormalDetail = None

    def _deserialize(self, params):
        self.Dimension = params.get("Dimension")
        self.TotalNum = params.get("TotalNum")
        self.AbnormalNum = params.get("AbnormalNum")
        if params.get("AbnormalDetail") is not None:
            self.AbnormalDetail = []
            for item in params.get("AbnormalDetail"):
                obj = AbnormalDetail()
                obj._deserialize(item)
                self.AbnormalDetail.append(obj)


class ResumeClusterInstancesRequest(AbstractModel):
    """ResumeClusterInstances请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        """
        self.ClusterId = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")


class ResumeClusterInstancesResponse(AbstractModel):
    """ResumeClusterInstances返回参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群ID
        :type ClusterId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ClusterId = None
        self.RequestId = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.RequestId = params.get("RequestId")


class RouteInfo(AbstractModel):
    """集群路由对象"""

    def __init__(self):
        """
        :param RouteTableName: 路由表名称。
        :type RouteTableName: str
        :param DestinationCidrBlock: 目的端CIDR。
        :type DestinationCidrBlock: str
        :param GatewayIp: 下一跳地址。
        :type GatewayIp: str
        """
        self.RouteTableName = None
        self.DestinationCidrBlock = None
        self.GatewayIp = None

    def _deserialize(self, params):
        self.RouteTableName = params.get("RouteTableName")
        self.DestinationCidrBlock = params.get("DestinationCidrBlock")
        self.GatewayIp = params.get("GatewayIp")


class RouteTableConflict(AbstractModel):
    """路由表冲突对象"""

    def __init__(self):
        """
                :param RouteTableType: 路由表类型。
                :type RouteTableType: str
                :param RouteTableCidrBlock: 路由表CIDR。
        注意：此字段可能返回 null，表示取不到有效值。
                :type RouteTableCidrBlock: str
                :param RouteTableName: 路由表名称。
        注意：此字段可能返回 null，表示取不到有效值。
                :type RouteTableName: str
                :param RouteTableId: 路由表ID。
        注意：此字段可能返回 null，表示取不到有效值。
                :type RouteTableId: str
        """
        self.RouteTableType = None
        self.RouteTableCidrBlock = None
        self.RouteTableName = None
        self.RouteTableId = None

    def _deserialize(self, params):
        self.RouteTableType = params.get("RouteTableType")
        self.RouteTableCidrBlock = params.get("RouteTableCidrBlock")
        self.RouteTableName = params.get("RouteTableName")
        self.RouteTableId = params.get("RouteTableId")


class RouteTableInfo(AbstractModel):
    """集群路由表对象"""

    def __init__(self):
        """
        :param RouteTableName: 路由表名称。
        :type RouteTableName: str
        :param RouteTableCidrBlock: 路由表CIDR。
        :type RouteTableCidrBlock: str
        :param VpcId: VPC实例ID。
        :type VpcId: str
        """
        self.RouteTableName = None
        self.RouteTableCidrBlock = None
        self.VpcId = None

    def _deserialize(self, params):
        self.RouteTableName = params.get("RouteTableName")
        self.RouteTableCidrBlock = params.get("RouteTableCidrBlock")
        self.VpcId = params.get("VpcId")


class RunClusterInspectionResponseItem(AbstractModel):
    """触发集群巡检请求返回"""

    def __init__(self):
        """
                :param ClusterId: 集群实例id
                :type ClusterId: str
                :param Error: 如果请求未能正常被处理，则Error中将包含错误信息
        注意：此字段可能返回 null，表示取不到有效值。
                :type Error: str
        """
        self.ClusterId = None
        self.Error = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.Error = params.get("Error")


class RunClusterInspectionsRequest(AbstractModel):
    """RunClusterInspections请求参数结构体"""

    def __init__(self):
        """
        :param ClusterIds: 目标集群列表
        :type ClusterIds: list of str
        """
        self.ClusterIds = None

    def _deserialize(self, params):
        self.ClusterIds = params.get("ClusterIds")


class RunClusterInspectionsResponse(AbstractModel):
    """RunClusterInspections返回参数结构体"""

    def __init__(self):
        """
        :param ResultSet: 每个集群的处理结果
        :type ResultSet: list of RunClusterInspectionResponseItem
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ResultSet = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("ResultSet") is not None:
            self.ResultSet = []
            for item in params.get("ResultSet"):
                obj = RunClusterInspectionResponseItem()
                obj._deserialize(item)
                self.ResultSet.append(obj)
        self.RequestId = params.get("RequestId")


class RunInstancesForNode(AbstractModel):
    """不同角色的节点配置参数"""

    def __init__(self):
        """
        :param NodeRole: 节点角色，取值:MASTER_ETCD, WORKER。MASTER_ETCD只有在创建 INDEPENDENT_CLUSTER 独立集群时需要指定。MASTER_ETCD节点数量为3～7，建议为奇数。MASTER_ETCD节点最小配置为4C8G。
        :type NodeRole: str
        :param RunInstancesPara: CVM创建透传参数，json化字符串格式，详见CVM创建实例接口，传入公共参数外的其他参数即可，其中ImageId会替换为TKE集群OS对应的镜像。
        :type RunInstancesPara: list of str
        :param InstanceAdvancedSettingsOverrides: 节点高级设置，该参数会覆盖集群级别设置的InstanceAdvancedSettings，和上边的RunInstancesPara按照顺序一一对应（当前只对节点自定义参数ExtraArgs生效）。
        :type InstanceAdvancedSettingsOverrides: list of InstanceAdvancedSettings
        """
        self.NodeRole = None
        self.RunInstancesPara = None
        self.InstanceAdvancedSettingsOverrides = None

    def _deserialize(self, params):
        self.NodeRole = params.get("NodeRole")
        self.RunInstancesPara = params.get("RunInstancesPara")
        if params.get("InstanceAdvancedSettingsOverrides") is not None:
            self.InstanceAdvancedSettingsOverrides = []
            for item in params.get("InstanceAdvancedSettingsOverrides"):
                obj = InstanceAdvancedSettings()
                obj._deserialize(item)
                self.InstanceAdvancedSettingsOverrides.append(obj)


class RunMonitorServiceEnabled(AbstractModel):
    """描述了 “云监控” 服务相关的信息"""

    def __init__(self):
        """
        :param Enabled: 是否开启云监控服务。取值范围：<br><li>TRUE：表示开启云监控服务<br><li>FALSE：表示不开启云监控服务<br><br>默认取值：TRUE。
        :type Enabled: bool
        """
        self.Enabled = None

    def _deserialize(self, params):
        self.Enabled = params.get("Enabled")


class RunSecurityServiceEnabled(AbstractModel):
    """描述了 “云安全” 服务相关的信息"""

    def __init__(self):
        """
        :param Enabled: 是否开启云安全服务。取值范围：<br><li>TRUE：表示开启云安全服务<br><li>FALSE：表示不开启云安全服务<br><br>默认取值：TRUE。
        :type Enabled: bool
        """
        self.Enabled = None

    def _deserialize(self, params):
        self.Enabled = params.get("Enabled")


class ServiceMeshForwardRequestRequest(AbstractModel):
    """ServiceMeshForwardRequest请求参数结构体"""

    def __init__(self):
        """
        :param Method: method
        :type Method: str
        :param Path: path
        :type Path: str
        :param Accept: accept
        :type Accept: str
        :param ContentType: ContentType
        :type ContentType: str
        :param RequestBody: RequestBody
        :type RequestBody: str
        """
        self.Method = None
        self.Path = None
        self.Accept = None
        self.ContentType = None
        self.RequestBody = None

    def _deserialize(self, params):
        self.Method = params.get("Method")
        self.Path = params.get("Path")
        self.Accept = params.get("Accept")
        self.ContentType = params.get("ContentType")
        self.RequestBody = params.get("RequestBody")


class ServiceMeshForwardRequestResponse(AbstractModel):
    """ServiceMeshForwardRequest返回参数结构体"""

    def __init__(self):
        """
        :param ResponseBody: 返回的内容
        :type ResponseBody: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ResponseBody = None
        self.RequestId = None

    def _deserialize(self, params):
        self.ResponseBody = params.get("ResponseBody")
        self.RequestId = params.get("RequestId")


class ShieldSettings(AbstractModel):
    """告警屏蔽settings，目前仅支持按时间段屏蔽"""

    def __init__(self):
        """
                :param EnableShield: 是否启动告警屏蔽功能
                :type EnableShield: bool
                :param ShieldTimeStart: 告警屏蔽开始时间，单位s，如8:00:00=> 8 * 60 * 60=28800
        注意：此字段可能返回 null，表示取不到有效值。
                :type ShieldTimeStart: int
                :param ShieldTimeEnd: 告警屏蔽结束时间，单位s，如10:00:00=> 10 * 60 * 60=36000
        注意：此字段可能返回 null，表示取不到有效值。
                :type ShieldTimeEnd: int
        """
        self.EnableShield = None
        self.ShieldTimeStart = None
        self.ShieldTimeEnd = None

    def _deserialize(self, params):
        self.EnableShield = params.get("EnableShield")
        self.ShieldTimeStart = params.get("ShieldTimeStart")
        self.ShieldTimeEnd = params.get("ShieldTimeEnd")


class SummaryService(AbstractModel):
    """Service详细信息"""

    def __init__(self):
        """
                :param Name: Service名称
        注意：此字段可能返回 null，表示取不到有效值。
                :type Name: str
                :param Status: Service状态
        注意：此字段可能返回 null，表示取不到有效值。
                :type Status: str
                :param ServiceIp: Service IP
        注意：此字段可能返回 null，表示取不到有效值。
                :type ServiceIp: str
                :param ExternalIp: 外网IP
        注意：此字段可能返回 null，表示取不到有效值。
                :type ExternalIp: str
                :param LbId: 负载均衡ID
        注意：此字段可能返回 null，表示取不到有效值。
                :type LbId: str
                :param LbStatus: 负载均衡状态
        注意：此字段可能返回 null，表示取不到有效值。
                :type LbStatus: str
                :param AccessType: Service访问类型
        注意：此字段可能返回 null，表示取不到有效值。
                :type AccessType: str
                :param DesiredReplicas: 期望副本数
        注意：此字段可能返回 null，表示取不到有效值。
                :type DesiredReplicas: int
                :param CurrentReplicas: 当前副本数
        注意：此字段可能返回 null，表示取不到有效值。
                :type CurrentReplicas: int
                :param CreatedAt: 创建时间
        注意：此字段可能返回 null，表示取不到有效值。
                :type CreatedAt: str
                :param Namespace: 命名空间
        注意：此字段可能返回 null，表示取不到有效值。
                :type Namespace: str
        """
        self.Name = None
        self.Status = None
        self.ServiceIp = None
        self.ExternalIp = None
        self.LbId = None
        self.LbStatus = None
        self.AccessType = None
        self.DesiredReplicas = None
        self.CurrentReplicas = None
        self.CreatedAt = None
        self.Namespace = None

    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Status = params.get("Status")
        self.ServiceIp = params.get("ServiceIp")
        self.ExternalIp = params.get("ExternalIp")
        self.LbId = params.get("LbId")
        self.LbStatus = params.get("LbStatus")
        self.AccessType = params.get("AccessType")
        self.DesiredReplicas = params.get("DesiredReplicas")
        self.CurrentReplicas = params.get("CurrentReplicas")
        self.CreatedAt = params.get("CreatedAt")
        self.Namespace = params.get("Namespace")


class Tag(AbstractModel):
    """标签绑定的资源类型，当前支持类型："cluster" """

    def __init__(self):
        """
        :param Key: 标签键
        :type Key: str
        :param Value: 标签值
        :type Value: str
        """
        self.Key = None
        self.Value = None

    def _deserialize(self, params):
        self.Key = params.get("Key")
        self.Value = params.get("Value")


class TagSpecification(AbstractModel):
    """标签描述列表。通过指定该参数可以同时绑定标签到相应的资源实例，当前仅支持绑定标签到云主机实例。"""

    def __init__(self):
        """
                :param ResourceType: 标签绑定的资源类型，当前支持类型："cluster"
        注意：此字段可能返回 null，表示取不到有效值。
                :type ResourceType: str
                :param Tags: 标签对列表
        注意：此字段可能返回 null，表示取不到有效值。
                :type Tags: list of Tag
        """
        self.ResourceType = None
        self.Tags = None

    def _deserialize(self, params):
        self.ResourceType = params.get("ResourceType")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)


class TaskStepInfo(AbstractModel):
    """任务步骤信息"""

    def __init__(self):
        """
                :param Step: 步骤名称
                :type Step: str
                :param LifeState: 生命周期
        pending : 步骤未开始
        running: 步骤执行中
        success: 步骤成功完成
        failed: 步骤失败
                :type LifeState: str
                :param StartAt: 步骤开始时间
        注意：此字段可能返回 null，表示取不到有效值。
                :type StartAt: str
                :param EndAt: 步骤结束时间
        注意：此字段可能返回 null，表示取不到有效值。
                :type EndAt: str
                :param FailedMsg: 若步骤生命周期为failed,则此字段显示错误信息
        注意：此字段可能返回 null，表示取不到有效值。
                :type FailedMsg: str
        """
        self.Step = None
        self.LifeState = None
        self.StartAt = None
        self.EndAt = None
        self.FailedMsg = None

    def _deserialize(self, params):
        self.Step = params.get("Step")
        self.LifeState = params.get("LifeState")
        self.StartAt = params.get("StartAt")
        self.EndAt = params.get("EndAt")
        self.FailedMsg = params.get("FailedMsg")


class UpdateClusterInstancesRequest(AbstractModel):
    """UpdateClusterInstances请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群 ID，请填写 需要升级的集群的 clusterId 字段
        :type ClusterId: str
        :param InstanceIds: 升级的节点ID列表，请选择集群中需要升级的节点ID列表
        :type InstanceIds: list of str
        :param InstanceAdvancedSettings: 描述了实例创建相关的一些高级设置。
        :type InstanceAdvancedSettings: :class:`tcecloud.tke.v20180525.models.InstanceAdvancedSettings`
        :param LoginSettings: 描述了实例登录相关配置与信息。
        :type LoginSettings: str
        :param EnhancedService: 描述了实例的增强服务启用情况与其设置，如云安全，云监控等实例 Agent。
        :type EnhancedService: str
        """
        self.ClusterId = None
        self.InstanceIds = None
        self.InstanceAdvancedSettings = None
        self.LoginSettings = None
        self.EnhancedService = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.InstanceIds = params.get("InstanceIds")
        if params.get("InstanceAdvancedSettings") is not None:
            self.InstanceAdvancedSettings = InstanceAdvancedSettings()
            self.InstanceAdvancedSettings._deserialize(params.get("InstanceAdvancedSettings"))
        self.LoginSettings = params.get("LoginSettings")
        self.EnhancedService = params.get("EnhancedService")


class UpdateClusterInstancesResponse(AbstractModel):
    """UpdateClusterInstances返回参数结构体"""

    def __init__(self):
        """
        :param InstanceIdSet: 成功启动更新的节点Id列表
        :type InstanceIdSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.InstanceIdSet = None
        self.RequestId = None

    def _deserialize(self, params):
        self.InstanceIdSet = params.get("InstanceIdSet")
        self.RequestId = params.get("RequestId")


class UpdateClusterVersionRequest(AbstractModel):
    """UpdateClusterVersion请求参数结构体"""

    def __init__(self):
        """
        :param ClusterId: 集群 Id
        :type ClusterId: str
        :param DstVersion: 需要升级到的版本
        :type DstVersion: str
        :param ExtraArgs: 集群自定义参数
        :type ExtraArgs: :class:`tcecloud.tke.v20180525.models.ClusterExtraArgs`
        :param MaxNotReadyPercent: 可容忍的最大不可用pod数目
        :type MaxNotReadyPercent: float
        :param SkipPreCheck: 是否跳过预检查阶段
        :type SkipPreCheck: bool
        """
        self.ClusterId = None
        self.DstVersion = None
        self.ExtraArgs = None
        self.MaxNotReadyPercent = None
        self.SkipPreCheck = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.DstVersion = params.get("DstVersion")
        if params.get("ExtraArgs") is not None:
            self.ExtraArgs = ClusterExtraArgs()
            self.ExtraArgs._deserialize(params.get("ExtraArgs"))
        self.MaxNotReadyPercent = params.get("MaxNotReadyPercent")
        self.SkipPreCheck = params.get("SkipPreCheck")


class UpdateClusterVersionResponse(AbstractModel):
    """UpdateClusterVersion返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpgradeAbleInstancesItem(AbstractModel):
    """可升级节点信息"""

    def __init__(self):
        """
        :param InstanceId: 节点Id
        :type InstanceId: str
        :param Version: 节点的当前版本
        :type Version: str
        """
        self.InstanceId = None
        self.Version = None

    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Version = params.get("Version")


class UpgradeClusterInstancesRequest(AbstractModel):
    """UpgradeClusterInstances请求参数结构体"""

    def __init__(self):
        """
                :param ClusterId: 集群ID
                :type ClusterId: str
                :param Operation: create 表示开始一次升级任务
        pause 表示停止任务
        resume表示继续任务
        abort表示终止任务
                :type Operation: str
                :param UpgradeType: 升级类型，目前只支持reset
                :type UpgradeType: str
                :param InstanceIds: 需要升级的节点列表
                :type InstanceIds: list of str
                :param ResetParam: 当节点重新加入集群时候所使用的参数，参考添加已有节点接口
                :type ResetParam: :class:`tcecloud.tke.v20180525.models.UpgradeNodeResetParam`
                :param SkipPreCheck: 是否忽略节点升级前检查
                :type SkipPreCheck: bool
                :param MaxNotReadyPercent: 最大可容忍的不可用Pod比例
                :type MaxNotReadyPercent: float
        """
        self.ClusterId = None
        self.Operation = None
        self.UpgradeType = None
        self.InstanceIds = None
        self.ResetParam = None
        self.SkipPreCheck = None
        self.MaxNotReadyPercent = None

    def _deserialize(self, params):
        self.ClusterId = params.get("ClusterId")
        self.Operation = params.get("Operation")
        self.UpgradeType = params.get("UpgradeType")
        self.InstanceIds = params.get("InstanceIds")
        if params.get("ResetParam") is not None:
            self.ResetParam = UpgradeNodeResetParam()
            self.ResetParam._deserialize(params.get("ResetParam"))
        self.SkipPreCheck = params.get("SkipPreCheck")
        self.MaxNotReadyPercent = params.get("MaxNotReadyPercent")


class UpgradeClusterInstancesResponse(AbstractModel):
    """UpgradeClusterInstances返回参数结构体"""

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None

    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpgradeNodeResetParam(AbstractModel):
    """节点升级重装参数"""

    def __init__(self):
        """
        :param InstanceAdvancedSettings: 实例额外需要设置参数信息
        :type InstanceAdvancedSettings: :class:`tcecloud.tke.v20180525.models.InstanceAdvancedSettings`
        :param EnhancedService: 增强服务。通过该参数可以指定是否开启云安全、云监控等服务。若不指定该参数，则默认开启云监控、云安全服务。
        :type EnhancedService: str
        :param LoginSettings: 节点登录信息（目前仅支持使用Password或者单个KeyIds）
        :type LoginSettings: str
        :param SecurityGroupIds: 实例所属安全组。该参数可以通过调用 DescribeSecurityGroups 的返回值中的sgId字段来获取。若不指定该参数，则绑定默认安全组。（目前仅支持设置单个sgId）
        :type SecurityGroupIds: list of str
        """
        self.InstanceAdvancedSettings = None
        self.EnhancedService = None
        self.LoginSettings = None
        self.SecurityGroupIds = None

    def _deserialize(self, params):
        if params.get("InstanceAdvancedSettings") is not None:
            self.InstanceAdvancedSettings = InstanceAdvancedSettings()
            self.InstanceAdvancedSettings._deserialize(params.get("InstanceAdvancedSettings"))
        self.EnhancedService = params.get("EnhancedService")
        self.LoginSettings = params.get("LoginSettings")
        self.SecurityGroupIds = params.get("SecurityGroupIds")


class VersionInstance(AbstractModel):
    """版本信息"""

    def __init__(self):
        """
                :param Name: 版本名称
        注意：此字段可能返回 null，表示取不到有效值。
                :type Name: str
                :param Version: 版本信息
        注意：此字段可能返回 null，表示取不到有效值。
                :type Version: str
                :param Remark: Remark
        注意：此字段可能返回 null，表示取不到有效值。
                :type Remark: str
        """
        self.Name = None
        self.Version = None
        self.Remark = None

    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Version = params.get("Version")
        self.Remark = params.get("Remark")

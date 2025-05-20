# -*- coding: UTF-8 -*-
import datetime
import logging
import socket
import ssl
import time
from functools import reduce
from ssl import SSLEOFError

from pyVim import connect
from pyVim.connect import SmartConnect
from pyVim.task import WaitForTask
from pyVmomi import vim

from common.cmp.cloud_apis.base import PrivateCloudManage
from common.cmp.cloud_apis.cloud_object.base import VPC, Disk, Image, Region, Subnet, Zone
from common.cmp.cloud_apis.constant import CloudResourceType, CloudType
from common.cmp.cloud_apis.resource_apis.resource_format.common.base_format import get_format_method
from common.cmp.utils import convert_param_to_list, get_compute_price_module, get_storage_pricemodule

# from .constant import VmwareVirtualMachineStatus

logger = logging.getLogger("root")


class CwVmware(object):
    def __init__(self, account, password, region, host="", **kwargs):
        self.account = account
        self.password = password
        self.host = host
        self.region = region
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.si = self._connect_vc()
        self.content = self.si.RetrieveContent()

    def __getattr__(self, item):
        return Vmware(si=self.si, content=self.content, name=item, region=self.region)

    def _connect_vc(self):
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            context.verify_mode = ssl.CERT_NONE
            si = SmartConnect(host=self.host, user=self.account, pwd=self.password, port=443, sslContext=context)
            return si
        except (SSLEOFError, socket.error):
            context = ssl._create_unverified_context()
            context.verify_mode = ssl.CERT_NONE
            si = SmartConnect(host=self.host, user=self.account, pwd=self.password, port=443, sslContext=context)
            return si
        except Exception as e:
            logger.exception("connect_vc error" + str(e))
            return None

    @classmethod
    def deconnect_vc(cls, si):
        connect.Disconnect(si)


class Vmware(PrivateCloudManage):
    """
    This class providing all operations on VMware vSphere platform.
    """

    def __init__(self, si, content, name, region):
        """
        Initialize vmware vSphere object.
        :param si: a service instance object using for connecting to the specified server.
        :param content: retrieve content object
        :param name: calling method name
        """
        self.si = si
        self.content = content
        self.name = name
        self.region = region
        self.cloud_type = CloudType.VMWARE.value

    # find method name and exec it.
    def __call__(self, *args, **kwargs):
        return getattr(self, self.name, self._non_function)(*args, **kwargs)

    # if method name not found, then exec _non_function method.
    @classmethod
    def _non_function(cls, *args, **kwargs):
        return {"result": True, "data": []}

    def get_connection_result(self):
        """
        check if this object works.
        :return: A dict with a “key: value” pair of object. The key name is result, and the value is a boolean type.
        :rtype: dict
        """
        if self.si:
            return {"result": True}

    def __region_format(self, region_obj):
        if region_obj:
            return Region(
                id=region_obj._moId,
                name=region_obj.name,
                text=region_obj.name,
                platform_type=CloudType.VMWARE.value,
                description="",
                created_time="",
                updated_time="",
                extra={},
            ).to_dict()
        else:
            return None

    def list_regions(self):
        """
        get datacenter list
        :rtype: dict
        """
        container = self.content.viewManager.CreateContainerView(self.content.rootFolder, [vim.Datacenter], True)
        datacenter_list = container.view
        return {"result": True, "data": [self._format_resource_result("region", i) for i in datacenter_list if i]}
        # return {"result": True, "data": [self.__region_format(i) for i in datacenter_list if i]}

    def __find_region_by_id(self, dc_id):
        region_obj = None
        region_obj_rs = self.list_regions()
        if region_obj_rs["result"]:
            for cur_region in region_obj_rs["data"]:
                if cur_region.get("id") == dc_id:
                    region_obj = cur_region
                    break
        return region_obj

    def __zone_format(self, zone_obj, **kwargs):
        if zone_obj:
            return Zone(
                id=zone_obj._moId,
                name=zone_obj.name,
                platform_type=CloudType.VMWARE.value,
                description="",
                status="",
                created_time="",
                updated_time="",
                extra={"dc_id": kwargs["region_id"], "dc_name": kwargs["region_name"]},
            ).to_dict()
        else:
            return None

    def list_zones(self, **kwargs):
        """
        get zone list on cloud platforms
        :param kwargs: accept multiple key value pair arguments.
        -----------------
        * region: the Id of a specific datacenter.(required)
        -----------------
        :rtype: dict
        """
        data = []
        if kwargs.get("region"):
            region = kwargs["region"]
            dc_obj = self._get_obj_bymoId(self.content, [vim.Datacenter], region)
            container = self.content.viewManager.CreateContainerView(dc_obj.hostFolder, [vim.ComputeResource], True)
            data = [
                self._format_resource_result("zone", {"obj": i, "region_id": region, "region_name": dc_obj.name})
                for i in container.view
                if i
            ]
        else:
            region_rs = self.list_regions()
            if region_rs["result"]:
                for cur_region in region_rs["data"]:
                    dc_obj = self._get_obj_bymoId(self.content, [vim.Datacenter], cur_region["resource_id"])
                    container = self.content.viewManager.CreateContainerView(
                        dc_obj.hostFolder, [vim.ComputeResource], True
                    )
                    data.extend(
                        [
                            self._format_resource_result(
                                "zone",
                                {
                                    "obj": i,
                                    "region_id": cur_region["resource_id"],
                                    "region_name": cur_region["resource_name"],
                                },
                            )
                            for i in container.view
                            if i
                        ]
                    )
        return {"result": True, "data": data}

    @classmethod
    def _get_obj_bymoId(cls, content, vim_type, mo_id):
        obj = None
        container = content.viewManager.CreateContainerView(content.rootFolder, vim_type, True)
        for c in container.view:
            if mo_id:
                if c._moId == mo_id:
                    obj = c
                    break
            else:
                obj = None
                break
        return obj

    def get_projects(self):
        """
        get project list on cloud platforms
        :rtype: dict
        """
        return {"result": False, "message": "无项目信息！"}

    def get_domains(self):
        """
        get domain list on cloud platforms
        :rtype: dict
        """
        return {"result": False, "message": "无域名信息！"}

    # ------------------***** compute *****-------------------
    def get_flavors(self, **kwargs):
        """
        get flavor list on cloud platforms
        :param kwargs:
        :rtype: dict
        """
        return {"result": False, "message": "无配置列表信息！"}

    def get_available_flavor(self, **kwargs):
        return {"result": True, "data": kwargs["config"]}

    def get_flavor_detail(self, uuid=None, **kwargs):
        """
        Get a specific flavor.
        :param uuid: flavor universally unique identifier(uuid).
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        return {"result": False, "message": "无法查看详细配置信息！"}

    def get_vms(self):
        """
        Get vm list on vmware vsphere platforms
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        try:
            content = self.content
            vm_list = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True).view
            vms_list = []
            for vm in vm_list:
                if not vm.config.template:
                    vm_format_data = self.__vm_format(vm)
                    if vm_format_data:
                        vms_list.append(vm_format_data)
            return {"result": True, "data": vms_list, "total": len(vm_list)}
        except Exception as e:
            logger.exception("get_vm_info")
            return {"result": False, "message": str(e)}

    def list_vms(self, ids=None):
        """
        Get vm list on vmware vsphere platforms
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        try:
            content = self.content
            vms_list = []
            disk_list = []
            snapshot_list = []
            ids = convert_param_to_list(ids)
            if ids:
                vm_obj = self._get_obj_bymoId(content, [vim.VirtualMachine], ids[0])
                vm_instance, vm_disk_data, vm_snap_data = self.__vm_format(vm_obj)
                if vm_instance:
                    vms_list = [vm_instance]
                if vm_disk_data:
                    disk_list.extend(vm_disk_data)
                if vm_snap_data:
                    snapshot_list.extend(vm_snap_data)
            else:
                vm_list = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True).view
                for vm in vm_list:
                    try:
                        if not vm.config.template:
                            vm_format_data, vm_disk_data, vm_snap_data = self.__vm_format(vm)
                            if vm_format_data:
                                vms_list.append(vm_format_data)
                            if vm_disk_data:
                                disk_list.extend(vm_disk_data)
                            if vm_snap_data:
                                snapshot_list.extend(vm_snap_data)
                    except Exception:
                        logger.error("list_vms——not found attribute template: {}".format(vm.name))
            # return {"result": True, "data": vms_list, "total": total}
            return {
                "result": True,
                "data": {"list_vms": vms_list, "list_disks": disk_list, "list_snapshots": snapshot_list},
            }
        except Exception as e:
            logger.exception("get_vm_info" + str(e))
            return {"result": False, "message": str(e)}

    def __nic_format(self, nic_obj):
        if nic_obj:
            pass
        else:
            return None

    def __vm_format(self, vm_obj):
        try:
            if not str(vm_obj.runtime.connectionState) == "disconnected":
                vm_id = vm_obj._moId
                name = vm_obj.name
                vm_instance = self._format_resource_result("vm", vm_obj)
                disk_list = []
                disk_object_rs = self.get_vm_disks(vm_obj._moId)
                if disk_object_rs["result"]:
                    disk_list = disk_object_rs["data"]

                snapshot_list = []
                snapshot_obj_rs = self.get_vm_snapshots({"vm_id": vm_id, "vm_name": name})
                if snapshot_obj_rs["result"]:
                    snapshot_list = snapshot_obj_rs["data"]

                return vm_instance, disk_list, snapshot_list
            else:
                return None, None, None
        except Exception as e:
            logger.exception("get_vm_info:" + str(e))
            return None, None, None

    def _format_resource_result(self, resource_type, obj):
        """
        格式化获取到的资源结果
        Args:
            resource_type (str): 资源类型名 如 region
            data (list or object): 待格式化的数据，

        Returns:

        """
        try:
            # cloud_type 这些哪里来。。。
            format_method = get_format_method(self.cloud_type, resource_type, region_id=self.region)

            return format_method(obj)
        except Exception as e:
            logger.exception("get_vm_info:" + str(e))
            return None

    def get_vm_detail(self, vm_id):
        """
        Get a specific vm.
        :param vm_id: the ID of a specific vm.
        :rtype: dict
        """
        content = self.content
        try:
            vm_obj = self._get_obj_bymoId(content, [vim.VirtualMachine], vm_id)
            return {"result": True, "data": self.__vm_format(vm_obj)}
        except Exception as e:
            logger.exception("get_vm_info")
            return {"result": False, "message": str(e)}

    @classmethod
    def _get_identity_win(cls, computer_name, passwordstr):
        # windows配置
        # 设置Unattend
        gui_unattended = vim.CustomizationGuiUnattended()
        gui_unattended.autoLogon = False
        gui_unattended.autoLogonCount = 0
        gui_unattended.timeZone = 210
        # 设置密码
        if passwordstr:
            password = vim.CustomizationPassword()
            password.plainText = True
            password.value = passwordstr
            gui_unattended.password = password
        # 设置identification
        identification = vim.CustomizationIdentification()
        identification.joinWorkgroup = "WorkGroup"
        # 设置计算机名
        if computer_name:
            computer_name_data = vim.CustomizationFixedName()
            computer_name_data.name = computer_name
        else:
            computer_name_data = vim.CustomizationVirtualMachineName()
        # 设置user_data
        user_data = vim.CustomizationUserData()
        user_data.computerName = computer_name_data
        user_data.fullName = "user"
        user_data.orgName = "org"
        user_data.productId = ""
        # 设置identity
        identity = vim.CustomizationSysprep()
        identity.guiUnattended = gui_unattended
        identity.identification = identification
        identity.userData = user_data
        return identity

    @classmethod
    def _get_identity_linux(cls, computer_name):
        # Linux配置
        # 设置计算机名
        if computer_name:
            host_name = vim.CustomizationFixedName()
            host_name.name = computer_name
        else:
            host_name = vim.CustomizationVirtualMachineName()
        # 设置identity
        identity = vim.CustomizationLinuxPrep()
        identity.hostName = host_name
        identity.domain = ""
        # identity.timeZone = "Asia/Shanghai"
        return identity

    def _get_customizationspec(self, ipaddr, mask, gateway, dns_list, vmtemplate_os, computer_name, passwordstr):
        # 设置IP
        if ipaddr:
            ip = vim.CustomizationFixedIp()
            ip.ipAddress = ipaddr
        else:
            ip = vim.CustomizationDhcpIpGenerator()
        # 设置网卡
        adapter_ipsetting = vim.CustomizationIPSettings()
        adapter_ipsetting.ip = ip
        if mask:
            adapter_ipsetting.subnetMask = mask
        if gateway:
            adapter_ipsetting.gateway = gateway
        # adapter_ipsetting.dnsServerList = dns_list
        # 设置nicMap
        nic_setting_map = vim.CustomizationAdapterMapping()
        nic_setting_map.adapter = adapter_ipsetting
        nic_setting_maps = [nic_setting_map]
        # 设置globalIPSettings
        global_ip_settings = vim.CustomizationGlobalIPSettings()
        global_ip_settings.dnsServerList = dns_list
        if vmtemplate_os.startswith("win"):
            identity = self._get_identity_win(computer_name, passwordstr)
        else:
            identity = self._get_identity_linux(computer_name)
        # 设置customizationspec
        customizationspec = vim.CustomizationSpec()
        customizationspec.nicSettingMap = nic_setting_maps
        customizationspec.globalIPSettings = global_ip_settings
        customizationspec.identity = identity
        return customizationspec

    def _get_vmconfig(
        self, content, cpu_cores, mem, vmtemplate_id, vswitch_id, vswitch_name, data_disk_size, disk_type
    ):
        # 设置网卡和硬盘设备

        vmtemplate = self._get_obj_bymoId(content, [vim.VirtualMachine], vmtemplate_id)
        devices = vmtemplate.config.hardware.device
        device_change = []
        unit_number = 0
        disk_temp = vim.vm.device.VirtualDisk()
        keys = []
        for i in devices:
            keys.append(i.key)
            if isinstance(i, vim.VirtualEthernetCard):
                nic_change0 = vim.VirtualDeviceConfigSpec()
                nic_change0.device = i
                nic_change0.operation = vim.vm.device.VirtualDeviceSpec.Operation.remove
                device_change.append(nic_change0)
            elif isinstance(i, vim.VirtualDisk):
                if unit_number <= int(i.unitNumber):
                    unit_number = int(i.unitNumber)
                    disk_temp = i
        nic_change = vim.VirtualDeviceConfigSpec()
        nic_change.device = vim.vm.device.VirtualVmxnet3()
        # nic_change.device.deviceInfo = vim.Description()
        # nic_change.device.deviceInfo.summary = vswitch_name
        netnic = self._get_obj_bymoId(content, [vim.Network], vswitch_id)
        if isinstance(netnic, vim.dvs.DistributedVirtualPortgroup):
            nic_change.device.backing = vim.vm.device.VirtualEthernetCard.DistributedVirtualPortBackingInfo()
            nic_change.device.backing.port = vim.dvs.PortConnection()
            nic_change.device.backing.port.switchUuid = netnic.config.distributedVirtualSwitch.uuid
            nic_change.device.backing.port.portgroupKey = netnic.key
        else:
            nic_change.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
            nic_change.device.backing.network = netnic
            nic_change.device.backing.deviceName = vswitch_name
            # nic_change.device.backing.deviceName = netnic.name
            nic_change.device.backing.useAutoDetect = False
        nic_change.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
        nic_change.device.connectable.startConnected = True
        nic_change.device.connectable.allowGuestControl = True
        nic_change.device.connectable.connected = False
        # nic_change.device.connectable.status = 'untried'
        nic_change.device.wakeOnLanEnabled = True
        nic_change.device.addressType = "assigned"
        nic_change.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        device_change.append(nic_change)
        if int(data_disk_size) != 0:
            unit_number = unit_number + 1
            disk_add = vim.VirtualDeviceConfigSpec()
            disk_add.device = vim.vm.device.VirtualDisk()
            disk_add.device.capacityInKB = (int(data_disk_size)) * 1024 * 1024
            disk_add.device.controllerKey = disk_temp.controllerKey
            disk_add.device.unitNumber = unit_number
            new_key = int(disk_temp.key) + 1
            while new_key in keys:
                new_key += 1
            disk_add.device.key = new_key
            disk_add.device.backing = vim.vm.device.VirtualDisk.FlatVer2BackingInfo()
            disk_add.device.backing.diskMode = "persistent"
            disk_type = disk_type.lower()
            if disk_type == "thin":
                disk_add.device.backing.thinProvisioned = True
            elif disk_type == "eager":
                disk_add.device.backing.thinProvisioned = False
                disk_add.device.backing.eagerlyScrub = True
            disk_add.fileOperation = "create"
            disk_add.operation = "add"
            device_change.append(disk_add)
        # 设置config（内存、CPU、设备）
        config = vim.VirtualMachineConfigSpec()
        config.memoryMB = (int(mem)) * 1024
        # config.numCoresPerSocket = (int(cpu_cores))/2
        config.numCPUs = int(cpu_cores)
        config.deviceChange = device_change
        return config

    @classmethod
    def _get_datastore_bysp(cls, storage_pod):
        datastores = [i for i in storage_pod.childEntity if i.summary.accessible]
        datastore = datastores[0]
        for i in datastores:
            if i.summary.freeSpace > datastore.summary.freeSpace:
                datastore = i
        return datastore

    # 根据自定义条件创建虚拟机
    def clone_vm_custom(self, content, args):
        try:
            customizationspec = self._get_customizationspec(
                args["ip"],
                args["mask"],
                args["gateway"],
                args["dns"],
                args["vmtemplate_os"],
                args["computer_name"],
                args["vmtemplate_pwd"],
            )
            config = self._get_vmconfig(
                content,
                args["cpu"],
                args["mem"],
                args["vmtemplate_moId"],
                args["vs_moId"],
                args["vs_name"],
                args["disk_size"],
                args["disk_type"],
            )
            # 设置RelocateSpec
            relocate_spec = vim.vm.RelocateSpec()
            datastore = self._get_obj_bymoId(content, [vim.Datastore], args["ds_moId"])
            if not datastore:
                storage_pod = self._get_obj_bymoId(content, [vim.StoragePod], args["ds_moId"])
                datastore = self._get_datastore_bysp(storage_pod)
            relocate_spec.datastore = datastore
            hc = self._get_obj_bymoId(content, [vim.ComputeResource], args["hc_moId"])
            if not hc:
                hc = self._get_obj_bymoId(content, [vim.ClusterComputeResource], args["hc_moId"])
            relocate_spec.pool = hc.resourcePool
            # 设置clonespec
            clonespec = vim.vm.CloneSpec()
            clonespec.customization = customizationspec
            clonespec.location = relocate_spec
            clonespec.config = config
            clonespec.powerOn = True
            # 设置目标文件夹
            dc = self._get_obj_bymoId(content, [vim.Datacenter], args["dc_moId"])
            if args["folder_moId"]:
                folder = self._get_obj_bymoId(content, [vim.Folder], args["folder_moId"])
            else:
                folder = dc.vmFolder
            # 克隆虚拟机
            vmtemplate = self._get_obj_bymoId(content, [vim.VirtualMachine], args["vmtemplate_moId"])
            task = vmtemplate.Clone(folder, args["vm_name"], clonespec)
            return task
        except Exception as e:
            logger.exception("clone_vm_custom")
            return {"result": False, "message": str(e)}

    # 删除创建失败的虚拟机
    def delete_failvm(self, fail_vm):
        try:
            n = 0
            while n < 3:
                if fail_vm.summary.runtime.powerState == "poweredOn":
                    task1 = fail_vm.PowerOff()
                    task_result1 = self._wait_for_task(task1)
                    n += 1
                    if task_result1["result"]:
                        break
                else:
                    break
            time.sleep(3)
            task2 = fail_vm.Destroy()
            task_result = self._wait_for_task(task2)
            return task_result
        except Exception as e:
            error_msg = e.message if e.message else str(e)
            return {"result": False, "message": error_msg}

    def _wait_for_task(self, task):
        """
        wait for a vCenter task to finish
        """
        task_done = False
        while not task_done:
            if task.info.state == "success":
                # task_done = True
                return {"result": True, "data": task.info.result}
            if task.info.state == "error":
                # task_done = True
                return {"result": False, "message": task.info.error.msg}

    # def _wait_for_vm_task(self, task):
    #     """
    #     wait for a vCenter task to finish
    #     """
    #     task_done = False
    #     while not task_done:
    #         if task.get("result"):
    #             # task_done = True
    #             return {"result": True, "data": task.get("data")}
    #         else:
    #             # task_done = True
    #             return {"result": False, "message": task.get("message")}

    def create_vm(self, args):
        """
        Create a vm.
        :param args: type dict.(required)
            dc_moId：数据中心id,类型：string。
            hc_moId：计算资源id，类型：string。
            ds_moId：数据存储id，类型：string。
            vs_moId：端口组Id,类型：string。
            vs_name：端口组名称，类型：string。
            folder_moId：文件夹ID，类型：string。
            vmtemplate_os：模板ID，类型：string。
            computer_name：虚拟机名称，类型：string。
            vmtemplate_pwd：虚拟机密码，类型：string。
            cpu：cpu数量，类型：int。
            mem：内存大小，类型：int。
            disk_size：磁盘大小，类型：int。
            disk_type：磁盘类型，类型：string。
            ip：虚拟机IP地址，类型：string。
            mask：虚拟机子网掩码，类型：string。
            gateway：虚拟机网关，类型：string。
            dns：DNS服务器，类型：string。
        :rtype: dict
        """
        content = self.content
        try:
            logger.info("开始进行配置" + str(args))
            task = self.clone_vm_custom(content, args)
            task_result = self._wait_for_task(task)
            if task_result["result"]:
                newvm = task_result["data"]
                event_filter = vim.event.EventFilterSpec()
                filter_spec_entity = vim.event.EventFilterSpec.ByEntity()
                filter_spec_entity.entity = newvm
                filter_spec_entity.recursion = vim.event.EventFilterSpec.RecursionOption.all
                event_filter.entity = filter_spec_entity
                task_fi = False
                a = datetime.datetime.now()
                logger.info("自定义配置属性设置完成，开始应用")
                while not task_fi:
                    events = content.eventManager.QueryEvents(filter=event_filter)
                    for event in events:
                        if isinstance(event, vim.event.CustomizationSucceeded):
                            return {"result": True, "data": newvm}
                    b = datetime.datetime.now()
                    if (b - a).seconds > 1200:
                        self.delete_failvm(newvm)
                        return {"result": False, "message": "虚拟机创建成功，自定义配置应用超时"}
            else:
                return {"result": False, "message": task.info.error.msg}
        except Exception as e:
            logger.exception("wait_for_vmclone_finish error")
            return {"result": False, "message": str(e)}

    def start_vm(self, vm_id):
        """
        Start a vm.
        :param vm_id: the ID of a specific vm.
        :rtype: dict
        """
        content = self.content
        try:
            vm = self._get_obj_bymoId(content, [vim.VirtualMachine], vm_id)
            power_state = vm.summary.runtime.powerState
            if power_state != "poweredOn":
                task = vm.PowerOn()
                task_result = self._wait_for_task(task)
                return task_result
            else:
                return {"result": False, "message": "已开机状态的虚拟机无法进行开机操作"}
        except Exception as e:
            logger.exception("start_vm(instance_id):" + vm_id)
            error_msg = e.message if e.message else str(e)
            return {"result": False, "message": error_msg}

    def stop_vm(self, vm_id):
        """
        Stop a vm.
        :param vm_id: the ID of a specific vm.
        :rtype: dict
        """
        content = self.content
        try:
            vm = self._get_obj_bymoId(content, [vim.VirtualMachine], vm_id)
            power_state = vm.summary.runtime.powerState
            if power_state == "poweredOn":
                vm.ShutdownGuest()
                return {"result": True}
            else:
                return {"result": False, "message": "已关机状态的虚拟机无法进行关机操作"}
        except Exception as e:
            logger.exception("stop_vm(instance_id):" + vm_id)
            error_msg = e.message if e.message else str(e)
            return {"result": False, "message": error_msg}

    def restart_vm(self, vm_id):
        """
        Restart a vm.
        :param vm_id: the ID of a specific vm.
        :rtype: dict
        """
        content = self.content
        try:
            vm = self._get_obj_bymoId(content, [vim.VirtualMachine], vm_id)
            power_state = vm.summary.runtime.powerState
            if power_state == "poweredOn":
                vm.RebootGuest()
                return {"result": True}
            else:
                return {"result": False, "message": "已关机状态的虚拟机无法进行重启操作"}
        except Exception as e:
            logger.exception("restart_vm(instance_id):" + vm_id)
            error_msg = e.message if e.message else str(e)
            return {"result": False, "message": error_msg}

    def change_vm_cpu(self, new_cpu, vm_id):
        """
        Set the number of Cores in a specific vm.
        :param new_cpu: the number of cores.
        :param vm_id: the ID of the vm.
        :rtype: dict
        """
        content = self.content
        vm_obj = self._get_obj_bymoId(content, [vim.VirtualMachine], vm_id)
        vm_cores_per_socket = int(vm_obj.config.hardware.numCoresPerSocket)
        try:
            if vm_obj.summary.runtime.powerState == "poweredOff":
                spec = vim.vm.ConfigSpec()
                spec.numCPUs = int(new_cpu)
                task = vm_obj.ReconfigVM_Task(spec=spec)
                WaitForTask(task)
                return {"result": True}
            else:
                if vm_obj.config.cpuHotAddEnabled:
                    if not isinstance(int(new_cpu) / vm_cores_per_socket, int):
                        return {"result": False, "message": "每个插槽的内核数为" + str(vm_cores_per_socket) + ",请输入其整数倍数值"}
                    if new_cpu > 24 or new_cpu < 1:
                        return {"result": False, "message": "总CPU内核数必须介于1~24之间"}
                    else:
                        spec = vim.vm.ConfigSpec()
                        spec.numCPUs = new_cpu
                        task = vm_obj.ReconfigVM_Task(spec=spec)
                        WaitForTask(task)
                        return {"result": True}
                else:
                    return {"result": False, "message": "未启用热插拔，无法在线更改CPU！"}
        except Exception as e:
            error_msg = e.message if e.message else str(e)
            return {"result": False, "message": error_msg}

    def change_vm_mem(self, new_memory, vm_id):
        """
        Set the size of memory in a specific vm.
        :param new_memory: the size of memory.
        :param vm_id: the ID of the vm.
        :rtype: dict
        """
        content = self.content
        vm_obj = self._get_obj_bymoId(content, [vim.VirtualMachine], vm_id)
        vm_memory_mb = int(vm_obj.config.hardware.memoryMB)
        new_memory_mb = int(new_memory * 1024)
        try:
            if vm_obj.summary.runtime.powerState == "poweredOff":
                spec = vim.vm.ConfigSpec()
                spec.memoryMB = int(new_memory_mb)
                task = vm_obj.ReconfigVM_Task(spec=spec)
                WaitForTask(task)
                return {"result": True}
            else:
                if vm_obj.config.memoryHotAddEnabled:
                    if not isinstance(int(new_memory_mb) / 4, int):
                        return {"result": False, "message": "内存必须是4M的倍数"}
                    if new_memory_mb < vm_memory_mb:
                        return {"result": False, "message": "内存必须介于" + str(vm_memory_mb / 1024) + "GB和64GB之间"}
                    else:
                        spec = vim.vm.ConfigSpec()
                        spec.memoryMB = int(new_memory_mb)
                        task = vm_obj.ReconfigVM_Task(spec=spec)
                        WaitForTask(task)
                        return {"result": True}
                else:
                    return {"result": False, "message": "未启用热插拔，无法在线更改内存！"}
        except Exception as e:
            logger.exception("change_vm_mem")
            error_msg = e.message if e.message else str(e)
            return {"result": False, "message": error_msg}

    def modify_vm(self, **kwargs):
        """
        Resize a vm(cpu、memory).
        :param kwargs: type dict. Contains two keys. eg. kwargs = {"InstanceId": "vm-98", "InstanceType": [2, 2048]}
        :rtype: dict
        """
        try:
            vm_id = kwargs["InstanceId"]
            new_cpu = kwargs["InstanceType"][0]
            new_memory = kwargs["InstanceType"][1]
            change_cpu = self.change_vm_cpu(new_cpu, vm_id)
            if not change_cpu["result"]:
                return change_cpu
            change_memory = self.change_vm_mem(new_memory, vm_id)
            if not change_memory["result"]:
                return change_memory
            return {"result": True}
        except Exception as e:
            logger.exception("modify_vm")
            return {"result": False, "message": str(e)}

    def destroy_vm(self, vm_id):
        """
        Destroy a vm.
        :param vm_id: the ID of a specific vm.
        :rtype: dict
        """
        content = self.content
        try:
            vm_obj = self._get_obj_bymoId(content, [vim.VirtualMachine], vm_id)
            if vm_obj.runtime.powerState == "poweredOn":
                task = vm_obj.PowerOffVM_Task()
                if self._wait_for_task(task)["result"]:
                    logger.exception("power off vm(instance_id):" + vm_id)
                else:
                    logger.exception("power off vm failed!(instance_id):" + vm_id)
            else:
                logger.info("vm state is power off!")
            destroy_task = vm_obj.Destroy_Task()
            return self._wait_for_task(destroy_task)
        except Exception as e:
            logger.exception("destroy_vm(instance_id):" + vm_id)
            error_msg = e.message if e.message else str(e)
            return {"result": False, "message": error_msg}

    def get_available_specs(self, **kwargs):
        """
        Get available specs.
        :param kwargs: accept multiple key value pair arguments.
        ---------------
        config: available config info.(required)
        ---------------
        :rtype: dict
        """
        try:
            return {"result": True, "data": kwargs["config"]}
        except Exception as e:
            logger.exception("get_Available_vm")
            return {"result": False, "message": str(e)}

    def add_vm_disk(self, **kwargs):
        """
        Create a disk and attach to a specific vm.
        :param kwargs: accept multiple key value pair arguments.
        ----------------
        * vm_id: the ID of a specific vm.(required)
        * disk_size: disk size.(required)
        * disk_type: the type of disk.(optional)
                     type: str
                     value: thin(精简置备） | eager(厚置备快速置零) | lazy(厚置备延迟置零)
                     defualt: thin
        ----------------
        :rtype: dict
        """
        content = self.content
        vm_id = kwargs["vm_id"]
        new_disk_size = int(kwargs["disk_size"])
        new_disk_type = kwargs.get("disk_type", "thin").lower()
        vm_obj = self._get_obj_bymoId(content, [vim.VirtualMachine], vm_id)
        try:
            unit_number = 0
            controller = ""
            for dev in vm_obj.config.hardware.device:
                if hasattr(dev.backing, "fileName"):
                    unit_number = int(dev.unitNumber) + 1
                    if unit_number == 7:
                        unit_number += 1
                    if unit_number >= 16:
                        return {"result": False, "message": "磁盘数据已达到上限"}
                if isinstance(dev, vim.vm.device.VirtualSCSIController):
                    controller = dev
            dev_changes = []
            virtual_disk_spec = vim.vm.device.VirtualDeviceSpec()
            virtual_disk_spec.fileOperation = "create"
            virtual_disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
            virtual_disk_spec.device = vim.vm.device.VirtualDisk()
            virtual_disk_spec.device.backing = vim.vm.device.VirtualDisk.FlatVer2BackingInfo()
            if new_disk_type == "thin":
                virtual_disk_spec.device.backing.thinProvisioned = True
            elif new_disk_type == "eager":
                virtual_disk_spec.device.backing.thinProvisioned = False
                virtual_disk_spec.device.backing.eagerlyScrub = True
            elif new_disk_type == "lazy":
                virtual_disk_spec.device.backing.thinProvisioned = False
                virtual_disk_spec.device.backing.eagerlyScrub = False
            virtual_disk_spec.device.backing.diskMode = "persistent"
            virtual_disk_spec.device.unitNumber = unit_number
            virtual_disk_spec.device.capacityInKB = int(new_disk_size) * 1024 * 1024
            virtual_disk_spec.device.controllerKey = controller.key
            dev_changes.append(virtual_disk_spec)
            spec = vim.vm.ConfigSpec()
            spec.deviceChange = dev_changes
            task = vm_obj.ReconfigVM_Task(spec=spec)
            WaitForTask(task)
            return {"result": True, "data": vm_id}
        except Exception as e:
            error_msg = e.message if e.message else str(e)
            return {"result": False, "message": error_msg}

    def remote_connect_vm(self, vm_id):
        """
        Connect to a remote vm desktop.
        :param vm_id: the ID of a specific.
        :rtype: dict
        """
        try:
            content = self.content
            vm = self._get_obj_bymoId(content, [vim.VirtualMachine], vm_id)
            ticket = vm.AcquireTicket("webmks")
            url = "wss://" + str(ticket.host) + ":" + str(ticket.port) + "/ticket/" + str(ticket.ticket)
            return {"result": True, "data": url}
        except Exception as e:
            logger.exception("remote_vm(instance_id):" + vm_id)
            return {"result": False, "message": str(e)}

    def __disk_format(self, disk_obj, vm_obj):
        if disk_obj:
            data_store = disk_obj.backing.datastore
            region_obj = data_store.parent.parent
            return Disk(
                id=disk_obj.backing.uuid,
                name=disk_obj.deviceInfo.label,
                device_type="",
                status="使用中",
                disk_size=int(disk_obj.capacityInKB / 1024 / 1024),
                platform_type=CloudType.VMWARE.value,
                is_attached=True,
                disk_type="系统盘" if disk_obj.unitNumber == 0 else "数据盘",
                description="",
                encrypted="",
                tags=[],
                disk_format="",
                project_info={},
                region_info={"id": region_obj._moId, "name": region_obj.name},
                zone_id=data_store._moId,
                zone_name=data_store.name,
                server_id=vm_obj._moId,
                server_name=vm_obj.name,
                snapshot_info=[],
                charge_type="",
                end_time="",
                created_time="",
                updated_time="",
                extra={
                    "provisioned": "精简置备" if disk_obj.backing.thinProvisioned else "厚置备",
                    "fileName": disk_obj.backing.fileName,
                    "unitNumber": disk_obj.unitNumber,
                },
            ).to_dict()
        else:
            return None

    def get_vm_disks(self, vm_id):
        """
        Get all disks from a specific VM instance.
        :param vm_id: the ID of a specific vm.
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        content = self.content
        try:
            vm_obj = self._get_obj_bymoId(content, [vim.VirtualMachine], vm_id)
            disk_list = []
            for dev in vm_obj.config.hardware.device:
                if isinstance(dev, vim.vm.device.VirtualDisk):
                    disk_instance = self._format_resource_result("disk", {"dev": dev, "vm_obj": vm_obj})
                    if disk_instance:
                        disk_list.append(disk_instance)
                    # disk_list.append(self.__disk_format(dev,  vm_obj))
            return {"result": True, "data": disk_list}
        except Exception as e:
            logger.exception("get vm disk failed(instance_id):" + vm_id)
            error_msg = e.message if e.message else str(e)
            return {"result": False, "message": error_msg}

    # ------------------***** snapshot *****------------------
    def __find_vm_snapshot(self, snapshot_obj, snapshot_id):
        """
        find a specific snapshot by ID.
        :param snapshot_obj: SnapshotTree List object.
        :param snapshot_id: the ID of a specific snapshot.
        :return: SnapshotTree object.
        """
        correct_snapshot_obj = None
        for cur_obj in snapshot_obj:
            if cur_obj.snapshot._moId == snapshot_id:
                correct_snapshot_obj = cur_obj
                return correct_snapshot_obj
            if len(cur_obj.childSnapshotList) != 0:
                correct_snapshot_obj = self.__find_vm_snapshot(cur_obj.childSnapshotList, snapshot_id)
                if correct_snapshot_obj:
                    return correct_snapshot_obj
        return correct_snapshot_obj

    def get_vm_snapshots(self, vm_param_obj):
        """
        Get all snapshots from a specific vm.
        :param vm_param_obj: the ID of a specific vm.
        :rtype: dict
        """
        content = self.content
        try:
            vm_obj = self._get_obj_bymoId(content, [vim.VirtualMachine], vm_param_obj["vm_id"])
            if not vm_obj.snapshot:
                return {"result": True, "data": []}
            snapshot_obj = vm_obj.snapshot.rootSnapshotList
            return {"result": True, "data": self.__snapshot_format(snapshot_obj, vm_param_obj)}
        except Exception as e:
            logger.exception("get_vm_snapshots")
            return {"result": False, "message": e}

    def __snapshot_format(self, snapshot_obj, vm_param_obj):
        snapshot_list = []
        for cur_obj in snapshot_obj:
            snapshot_list.append(
                self._format_resource_result("snapshot", {"vm_param_obj": vm_param_obj, "cur_obj": cur_obj})
            )
            if cur_obj.childSnapshotList:
                snapshot_rs = self.__snapshot_format(cur_obj.childSnapshotList, vm_param_obj)
                if snapshot_rs:
                    snapshot_list.extend(snapshot_rs)
                else:
                    return None
        return snapshot_list

    def create_snapshot(self, **kwargs):
        """
        Create a snapshot from a specific vm.
        :param vm_id: the ID of a specific vm.
        :param kwargs: accept multiple key value pair arguments.
        ---------------
        * snapshot_name: the name of new snapshot.(required)
        * description: Description of the snapshot.(optional)
        * memory: enable memory snapshot. type boolean. default is true
        * quiesce: type boolean. default is false
        ---------------
        :rtype: dict
        """
        content = self.content
        vm_id = kwargs.get("vm_id")
        if not vm_id:
            return {"result": False, "message": "vm_id为必传参数"}
        try:
            vm_obj = self._get_obj_bymoId(content, [vim.VirtualMachine], vm_id)
            task = vm_obj.CreateSnapshot_Task(
                name=kwargs.get("snapshot_name", ""),
                description=kwargs.get("snapshot_desc", ""),
                memory=kwargs.get("many", True),
                quiesce=kwargs.get("quiesce", False),
            )
            task_result = self._wait_for_task(task)
            return task_result
        except Exception as e:
            error_msg = e.message if e.message else str(e)
            return {"result": False, "message": error_msg}

    def delete_snapshot(self, snapshot_id, vm_id):
        """
        Remove a snapshot from a specific vm
        :param snapshot_id: the ID of a specific vm
        :param vm_id: the ID of a specific vm.
        :rtype: dict
        """
        content = self.content
        try:
            vm_obj = self._get_obj_bymoId(content, [vim.VirtualMachine], vm_id)
            snapshot_obj = vm_obj.snapshot.rootSnapshotList
            correct_snapshot = self.__find_vm_snapshot(snapshot_obj, snapshot_id)
            if correct_snapshot:
                task = correct_snapshot.snapshot.RemoveSnapshot_Task(False)
                return self._wait_for_task(task)
            else:
                return {"result": False, "message": "无法找到该快照！"}
        except Exception as e:
            return {"result": False, "message": e}

    def list_snapshots(self, **kwargs):
        """
        Get all vm snapshots.
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        return {"result": False, "message": "方法不支持！"}

    def restore_snapshot(self, **kwargs):
        """
        recover a specific vm from a specific snapshot.
        :param vm_id: the ID of a specific vm.
        :param snapshot_id: the ID of a specific snapshot.
        :rtype: dict
        """
        vm_id = kwargs["vm_id"]
        snapshot_id = kwargs["snapshot_id"]
        if not (vm_id and snapshot_id):
            return {"result": False, "message": "vm_id/snapshot_id为必传参数"}
        content = self.content
        try:
            vm_obj = self._get_obj_bymoId(content, [vim.VirtualMachine], vm_id)
            snapshot_obj = vm_obj.snapshot.rootSnapshotList
            correct_snapshot = self.__find_vm_snapshot(snapshot_obj, snapshot_id)
            if correct_snapshot:
                task = correct_snapshot.snapshot.RevertToSnapshot_Task()
                return self._wait_for_task(task)
            else:
                return {"result": False, "message": "无法找到该快照！"}
        except Exception as e:
            error_msg = e.message if e.message else str(e)
            return {"result": False, "message": error_msg}

    # ------------------***** tag *****------------------
    def create_tag(self, **kwargs):
        """
        Create a tag.
        :param kwargs: accept multiple key value pair arguments.
        :return:
        """
        return {"result": False, "message": "vmware无标签创建功能！"}

    def delete_tag(self, **kwargs):
        """
        Delete a tag.
        :param kwargs:
        :return: accept multiple key value pair arguments.
        """
        return {"result": False, "message": "vmware无标签删除功能！"}

    def update_tag(self, uuid, **kwargs):
        """
        Update key-value of a tag.
        :param uuid: tag universally unique identifier(uuid).
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        return {"result": False, "message": "vmware无标签更新功能！"}

    def get_tags(self, **kwargs):
        """
        Get tag list on cloud platforms.
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        return {"result": False, "message": "vmware无获取标签列表功能！"}

    def remove_resource_tag(self, uuid, **kwargs):
        """
        Delete a specific tag from a specific resource.
        :param uuid: the ID of resource
        :param kwargs: accept multiple key value pair arguments.
        """
        return {"result": False, "message": "vmware无删除指定资源的标签创建功能！"}

    def get_resource_tags(self, uuid, **kwargs):
        """
        Get all tags from a specific resource.
        :param uuid: the ID of resource
        :param kwargs: accept multiple key value pair arguments.
        """
        return {"result": False, "message": "vmware无获取指定资源的标签功能！"}

    # ------------------***** storage *****-------------------
    def list_disks(self, **kwargs):
        """
        Get disk list on cloud platforms.
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        return {"result": False, "message": "获取失败，方法暂时未实现！"}

    def get_disk_detail(self, disk_number):
        """
        Get a specific disk.
        :param disk_number: the number of disk.
        :rtype: dict
        """
        return {"result": False, "message": "获取失败，方法暂时未实现！"}

    def create_disk(self, **kwargs):
        """
        Create a disk and attach to a specific vm.
        :param kwargs: accept multiple key value pair arguments.
        ----------------
        * vm_id: the ID of a specific vm.(required)
        * disk_size: disk size.(required)
        * disk_type: the type of disk.(optional)
                     type: str
                     value: thin(精简置备） | eager(厚置备快速置零) | lazy(厚置备延迟置零)
                     defualt: thin
        ----------------
        :rtype: dict
        """
        return self.add_vm_disk(**kwargs)

    def attach_disk(self, **kwargs):
        """
        Attach a specific disk to a specific vm.
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        return {"result": False, "message": "vmware不支持挂载磁盘！"}

    def detach_disk(self, **kwargs):
        """
        Detach a specific disk from a specific vm.
        :param kwargs: accept multiple key value pair arguments.
        * vm_id: the id of vm.(required)
                 type: str
        * disk_number: the number of disk.(required)
                       type: int
        :rtype: dict
        """
        vm_id = kwargs.get("vm_id")
        disk_number = int(kwargs.get("disk_number"))
        # res = self.destroy_disk(vm_id, disk_number)
        res = self.delete_disk(disk_number, vm_id)
        if res["result"]:
            return res
        else:
            return {"result": False, "message": res["data"]}

    def delete_disk(self, disk_number, vm_id):
        """
        Delete a specific disk from a specific vm.
        :param vm_id: the ID of a specific vm.
        :param disk_number: the number of a specific disk. type int
        :rtype: dict
        """
        content = self.content
        try:
            vm_obj = self._get_obj_bymoId(content, [vim.VirtualMachine], vm_id)
            virtual_hdd_device = None
            for dev in vm_obj.config.hardware.device:
                if isinstance(dev, vim.vm.device.VirtualDisk) and dev.unitNumber == disk_number:
                    virtual_hdd_device = dev
            if not virtual_hdd_device:
                return {"result": False, "message": "无法找到磁盘！"}
            virtual_hdd_spec = vim.vm.device.VirtualDeviceSpec()
            virtual_hdd_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.remove
            virtual_hdd_spec.device = virtual_hdd_device
            spec = vim.vm.ConfigSpec()
            spec.deviceChange = [virtual_hdd_spec]
            task = vm_obj.ReconfigVM_Task(spec=spec)
            return self._wait_for_task(task)
        except Exception as e:
            logger.exception("delete disk[" + disk_number + "] from a specific vm[" + vm_id + "] failed!")
            error_msg = e.message if e.message else str(e)
            if vm_obj.rootSnapshot:
                return {"result": False, "message": "该磁盘已做快照，不能删除！"}
            return {"result": False, "message": error_msg}

    def extend_disk(self, vm_id, disk_number, disk_size):
        """
        extend a specific disk in a specific vm
        :param vm_id: the ID of a specific vm.
        :param disk_number: the number of a specific disk. type int
        :param disk_size: the size of a specific disk. type int
        :rtype: dict
        """
        content = self.content
        try:
            vm_obj = self._get_obj_bymoId(content, [vim.VirtualMachine], vm_id)
            virtual_disk_device = None
            for dev in vm_obj.config.hardware.device:
                if isinstance(dev, vim.vm.device.VirtualDisk) and dev.unitNumber == disk_number:
                    virtual_disk_device = dev
            if not virtual_disk_device:
                return {"result": False, "message": "无法找到磁盘！"}
            if virtual_disk_device.capacityInKB >= disk_size * 1024 * 1024:
                return {"result": False, "message": "调整磁盘的容量不能小于原容量！"}
            virtual_disk_spec = vim.vm.device.VirtualDeviceSpec()
            virtual_disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
            virtual_disk_spec.device = virtual_disk_device
            virtual_disk_spec.device.capacityInKB = int(disk_size) * 1024 * 1024
            dev_changes = [virtual_disk_spec]
            spec = vim.vm.ConfigSpec()
            spec.deviceChange = dev_changes
            task = vm_obj.ReconfigVM_Task(spec=spec)
            return self._wait_for_task(task)
        except Exception as e:
            error_msg = e.message if e.message else str(e)
            if not vm_obj.rootSnapshot:
                return {"result": False, "message": "该磁盘已做快照，不能扩展！"}
            return {"result": False, "message": error_msg}

    def get_disk_snapshots(self, **kwargs):
        """
        Get disk snapshot list.
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        return {"result": False, "message": "获取所有磁盘的快照失败，方法暂时未实现！"}

    def get_disk_snapshot_detail(self, **kwargs):
        """
        Get a specific disk snapshot detail info.
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        return {"result": False, "message": "获取磁盘快照详细资料失败，方法暂时未实现！"}

    def get_images(self):
        """
        Get template list.
        :rtype: dict
        """
        content = self.content
        try:
            vm_obj = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True).view
            vmtemplate_list = []
            for cur_obj in vm_obj:
                config = cur_obj.summary.config
                if config.template:
                    vmtemplate_list.append(self.__template_format(cur_obj))
            return {"result": True, "data": vmtemplate_list}
        except Exception as e:
            logger.exception("get template list failed!")
            return {"result": False, "message": str(e)}

    def list_images(self, template_id=None):
        """
        Get template list.
        :rtype: dict
        """
        content = self.content

        try:
            vm_obj = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True).view
            vmtemplate_list = []
            if template_id:
                for cur_obj in vm_obj:
                    if cur_obj._moId == template_id:
                        data = self._format_resource_result("image", cur_obj)
                        if data:
                            vmtemplate_list = [data]
                    else:
                        logger.exception("get a specific template[" + template_id + "] failed!")
            else:
                for cur_obj in vm_obj:
                    config = cur_obj.summary.config
                    if config.template:
                        vmtemplate_data = self._format_resource_result("image", cur_obj)
                        if vmtemplate_data:
                            vmtemplate_list.append(vmtemplate_data)
            return {"result": True, "data": vmtemplate_list}
        except Exception as e:
            logger.exception("get template list failed!")
            return {"result": False, "message": str(e)}

    def get_image_detail(self, template_id):
        """
        Get a specific template.
        :param template_id: the ID of a specific template.
        :rtype: dict
        """
        content = self.content
        try:
            vm_obj = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True).view
            for cur_obj in vm_obj:
                if cur_obj._moId == template_id:
                    return {"result": True, "data": self.__template_format(cur_obj)}
            else:
                logger.exception("get a specific template[" + template_id + "] failed!")
                return {"result": False, "message": "找不到指定的镜像！"}
        except Exception as e:
            logger.exception("get a specific template[" + template_id + "] failed!")
            return {"result": False, "message": str(e)}

    @classmethod
    def __template_format(cls, template_obj):
        """
        template obj format
        :param template_obj:
        :rtype: dict
        """
        vm_config = template_obj.config
        region_obj = template_obj.parent.parent
        return Image(
            id=template_obj._moId,
            name=template_obj.name,
            image_size="",
            status="可用",
            platform_type=CloudType.VMWARE.value,
            image_platform=vm_config.guestFullName,
            image_type="私有",
            tags=[],
            description=vm_config.annotation,
            created_time="",
            updated_time="",
            os_arch="",
            os_bit="",
            os_type="",
            image_format="",
            project_info={},
            region_info={"id": region_obj._moId, "name": region_obj.name},
            zone_info={},
            visibility="",
            extra={},
        ).to_dict()

    # 只能删除由关机状态的虚拟机做成的模版
    def destroy_image(self, template_id):
        """
        Delete a specific image.
        :param template_id: the ID of a specific template.
        :rtype: dict
        """
        content = self.content
        try:
            template_obj = self._get_obj_bymoId(content, [vim.VirtualMachine], template_id)
            destroy_task = template_obj.Destroy()
            return self._wait_for_task(destroy_task)
        except Exception as e:
            logger.exception("delete a specific template[" + template_id + "]")
            return {"result": False, "message": str(e)}

    # ------------------***** network *****-------------------
    def list_security_groups(self, **kwargs):
        """
        Get security group list.
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        return {"result": False, "message": "vmware不支持安全组！"}

    def get_security_group_detail(self, uuid, **kwargs):
        """
        Get a specific security group.
        :param uuid: uuid: security group universally unique identifier(uuid).
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        return {"result": False, "message": "vmware不支持安全组！"}

    def destroy_security_group(self, uuid, **kwargs):
        """
        Delete a specific security group.
        :param uuid: uuid: security group universally unique identifier(uuid).
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        return {"result": False, "message": "vmware不支持安全组！"}

    def create_security_group(self, **kwargs):
        """
        Create a specific security group.
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        return {"result": False, "message": "vmware不支持安全组！"}

    def modify_security_group(self, uuid, **kwargs):
        """
        Modify a specific security group.
        :param uuid: uuid: security group universally unique identifier(uuid).
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        return {"result": False, "message": "vmware不支持安全组！"}

    def list_security_group_rule(self, uuid, **kwargs):
        """
        Get a specific rule info from a specific security group.
        :param uuid: uuid: security group rule universally unique identifier(uuid).
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        return {"result": False, "message": "vmware不支持安全组规则！"}

    def create_security_group_rule(self, **kwargs):
        """
        Create a specific rule from a specific security group.
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        return {"result": False, "message": "vmware不支持安全组规则！"}

    def destroy_security_group_rule(self, uuid, **kwargs):
        """
        Delete a specific rule info from a specific security group.
        :param uuid: uuid: security group rule universally unique identifier(uuid).
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        return {"result": False, "message": "vmware不支持安全组规则！"}

    def _vswitch_format(self, vswitch_obj, host_obj):
        if vswitch_obj:
            zone_obj = host_obj.parent
            region_obj = zone_obj.parent.parent
            return VPC(
                id=vswitch_obj.name.replace("/", "").replace(".", ""),
                name=vswitch_obj.name,
                status="可用",
                platform_type=CloudType.VMWARE.value,
                router_info=[],
                network_addr="",
                is_default=None,
                region_info={"id": region_obj._moId, "name": region_obj.name},
                zone_info={"id": zone_obj._moId, "name": zone_obj.name},
                vm_host_id=host_obj._moId,
                project_info={},
                description="",
                tags=[],
                updated_time="",
                created_time="",
                resource_group="",
                extra={"mtu": vswitch_obj.mtu},
            ).to_dict()
        else:
            return None

    def list_vpcs(self, ids=None):
        """
        Get vswitch list from all hosts.
        :rtype: dict
        """
        content = self.content
        try:
            host_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
            vswitch_list = []
            if ids:
                for cur_host in host_view.view:
                    if not cur_host.config:
                        continue
                    if cur_host._moId == ids[0]:
                        vswitch_obj = cur_host.config.network.vswitch
                        for cur_vswitch in vswitch_obj:
                            vswitch_data = self._format_resource_result(
                                "vpc", {"cur_vswitch": cur_vswitch, "cur_host": cur_host}
                            )
                            if vswitch_data:
                                vswitch_list.append(vswitch_data)
                        break
            else:
                for cur_host in host_view.view:
                    if not cur_host.config:
                        continue
                    vswitch_obj = cur_host.config.network.vswitch
                    for cur_vswitch in vswitch_obj:
                        vswitch_data = self._format_resource_result(
                            "vpc", {"cur_vswitch": cur_vswitch, "cur_host": cur_host}
                        )
                        if vswitch_data:
                            vswitch_list.append(vswitch_data)

            return {"result": True, "data": vswitch_list}
        except Exception as e:
            logger.exception("get all vswitch list")
            return {"result": False, "message": str(e)}

    def create_vpc(self, **kwargs):
        """
        Create a vswitch under a specific host.
        :param host_id: the ID of a specific host.
        :param kwargs: accept multiple key value pair arguments.
        ---------------
        * vswitchName: the name of vswitch.(required)
        * numPorts: the number of ports.(optional) default is 1024
        * mtu: mtu.(optional) default is 1500
        ---------------
        :rtype: dict
        """
        host_id = kwargs["host_id"]
        if not host_id:
            return {"result": False, "message": "host_id为必传参数！"}
        content = self.content
        try:
            cluster_list = content.viewManager.CreateContainerView(content.rootFolder, [vim.ComputeResource], True).view
            for c in cluster_list:
                for h in c.host:
                    if h._moId == host_id:
                        vswitch_spec = vim.host.VirtualSwitch.Specification()
                        vswitch_spec.numPorts = kwargs.get("numPorts", 1024)
                        vswitch_spec.mtu = kwargs.get("mtu", 1450)
                        h.configManager.networkSystem.AddVirtualSwitch(kwargs.get("vswitchName", ""), vswitch_spec)
                        return {"result": True, "data": kwargs.get("vswitchName", "")}
                else:
                    return {"result": False, "message": "未匹配到指定的主机！"}
            return {"result": False, "message": "未匹配到该集群！"}
        except Exception as e:
            logger.exception("get_host_info")
            return {"result": False, "message": str(e)}

    def delete_vpc(self, host_id, vswitch_name):
        """
        Delete a specific vswitch from a specific host.
        :param host_id: the ID of a specific host.
        :param vswitch_name: the name of vswitch.
        :rtype: dict
        """
        content = self.content
        try:
            cluster_list = content.viewManager.CreateContainerView(content.rootFolder, [vim.ComputeResource], True).view
            for c in cluster_list:
                for h in c.host:
                    if h._moId == host_id:
                        h.configManager.networkSystem.RemoveVirtualSwitch(vswitch_name)
                        return {"result": True}
                else:
                    return {"result": False, "message": "未匹配到指定的主机！"}
            return {"result": False, "message": "未匹配到该集群！"}
        except Exception as e:
            logger.exception("get_host_info")
            return {"result": False, "message": str(e)}

    def modify_vpc(self, hc_id, **kwargs):
        """
        Modify a specific vswitch.
        :param hc_id: the ID of a specific host.
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        return {"result": "False", "message": "修改vswich参数暂时未实现！"}

    def get_vpc_detail(self, host_id):
        """
        Get vswitch list under a specific hosts.
        :param host_id: the ID of a specific host.
        :rtype: dict
        """
        content = self.content
        try:
            host_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
            vswitch_list = []
            for cur_host in host_view.view:
                if cur_host._moId == host_id:
                    vswitch_obj = cur_host.config.network.vswitch
                    for cur_vswitch in vswitch_obj:
                        vswitch_list.append(self._vswitch_format(cur_vswitch, cur_host))
                    break
            return {"result": True, "data": vswitch_list}
        except Exception as e:
            logger.exception("get switch list under a specific host.")
            return {"result": False, "message": str(e)}

    def get_public_ip(self, **kwargs):
        """
        Get a public ip address from a specific vm.
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        return {"result": False, "message": "vmware不支持查看公网IP！"}

    def __portgroup_format(self, portgroup_obj, host_pg_list, host_obj):
        if portgroup_obj:
            zone_obj = host_obj.parent
            region_obj = zone_obj.parent.parent
            portgroup_name = portgroup_obj.key.split("key-vim.host.PortGroup-")[1]
            portgroup_id = None
            vm_num = 0
            for cur_pg in host_pg_list:
                if cur_pg.get("name") == portgroup_name:
                    portgroup_id = cur_pg.get("id")
                    vm_num = cur_pg.get("vm_num")
                    break
            else:
                return None
            return Subnet(
                id=portgroup_id,
                name=portgroup_name,
                vpc_id=portgroup_obj.vswitch.split("key-vim.host.VirtualSwitch-")[1].replace("/", "").replace(".", ""),
                status="可用",
                platform_type=CloudType.VMWARE.value,
                updated_time="",
                created_time="",
                tags=[],
                description="",
                vm_host_id=host_obj._moId,
                project_info={},
                region_info={"id": region_obj._moId, "name": region_obj.name},
                zone_info={"id": zone_obj._moId, "name": region_obj.name},
                extra={
                    "vm_num": vm_num,
                },
            ).to_dict()
        else:
            return None

    def __get_host_pg_list(self, host_obj):
        host_pg_list = []
        for cur_pg in host_obj.network:
            if cur_pg.name == "Management Network":
                continue
            host_pg_list.append({"id": cur_pg._moId, "name": cur_pg.name, "vm_num": len(cur_pg.vm)})
        return host_pg_list

    def get_subnets(self, **kwargs):
        """
        Get all portgroup list.
        :rtype: dict
        """
        content = self.content
        try:
            if kwargs.get("hc_id", ""):
                hc = self._get_obj_bymoId(content, [vim.ClusterComputeResource], kwargs["hc_id"])
                if not hc:
                    hc = self._get_obj_bymoId(content, [vim.ComputeResource], kwargs["hc_id"])
                vswitch = hc.network
                portgroup_list = []
                for i in vswitch:
                    if i.summary.accessible:
                        vs_id = i._moId
                        if isinstance(i, vim.dvs.DistributedVirtualPortgroup):
                            if hasattr(i.config, "uplink"):
                                if not i.config.uplink:
                                    portgroup_list.append({"vs_moId": vs_id, "vs_name": i.name.encode("utf8")})
                            else:
                                portgroup_list.append({"vs_moId": vs_id, "vs_name": i.name.encode("utf8")})
                        else:
                            portgroup_list.append({"vs_moId": vs_id, "vs_name": i.name.encode("utf8")})
                return {"result": True, "data": portgroup_list}
            host_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
            portgroup_list = []
            for cur_host in host_view.view:
                host_pg_list = self.__get_host_pg_list(cur_host)
                for cur_portgroup in cur_host.config.network.portgroup:
                    if cur_portgroup.key.split("key-vim.host.PortGroup-")[1] != "Management Network":
                        subnet_obj = self.__portgroup_format(cur_portgroup, host_pg_list, cur_host)
                        if not subnet_obj:
                            continue
                        portgroup_list.append(subnet_obj)
            return {"result": True, "data": portgroup_list}
        except Exception as e:
            logger.exception("get portgroup list from all host")
            return {"result": False, "message": str(e)}

    def list_subnets(self, host_id=None, vswitch_name="", **kwargs):
        """
        Get all portgroup list.
        :rtype: dict
        """
        content = self.content
        portgroup_list = []
        try:
            host_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
            if host_id:
                for cur_host in host_view.view:
                    if not cur_host.config:
                        continue
                    if cur_host._moId == host_id:
                        host_pg_list = self.__get_host_pg_list(cur_host)
                        for cur_portgroup in cur_host.config.network.portgroup:
                            subnet_obj = self._format_resource_result(
                                "subnet",
                                {"cur_portgroup": cur_portgroup, "host_pg_list": host_pg_list, "cur_host": cur_host},
                            )
                            if not subnet_obj:
                                continue
                            portgroup_list.append(subnet_obj)
                        break
                portgroup_list = [x for x in portgroup_list if x.get("vpc_id") == vswitch_name]
            else:
                if kwargs.get("hc_id", ""):
                    hc = self._get_obj_bymoId(content, [vim.ClusterComputeResource], kwargs["hc_id"])
                    if not hc:
                        hc = self._get_obj_bymoId(content, [vim.ComputeResource], kwargs["hc_id"])
                    vswitch = hc.network
                    portgroup_list = []
                    for i in vswitch:
                        if i.summary.accessible:
                            vs_id = i._moId
                            if isinstance(i, vim.dvs.DistributedVirtualPortgroup):
                                if hasattr(i.config, "uplink"):
                                    if not i.config.uplink:
                                        portgroup_list.append({"vs_moId": vs_id, "vs_name": i.name.encode("utf8")})
                                else:
                                    portgroup_list.append({"vs_moId": vs_id, "vs_name": i.name.encode("utf8")})
                            else:
                                portgroup_list.append({"vs_moId": vs_id, "vs_name": i.name.encode("utf8")})
                    return {"result": True, "data": portgroup_list}
                host_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
                portgroup_list = []
                for cur_host in host_view.view:
                    if not cur_host.config:
                        continue
                    host_pg_list = self.__get_host_pg_list(cur_host)
                    for cur_portgroup in cur_host.config.network.portgroup:
                        if cur_portgroup.key.split("key-vim.host.PortGroup-")[1] != "Management Network":
                            subnet_obj = self._format_resource_result(
                                "subnet",
                                {"cur_portgroup": cur_portgroup, "host_pg_list": host_pg_list, "cur_host": cur_host},
                            )
                            if not subnet_obj:
                                continue
                            portgroup_list.append(subnet_obj)
            return {"result": True, "data": portgroup_list}
        except Exception as e:
            logger.exception("get portgroup list from all host")
            return {"result": False, "message": str(e)}

    def get_subnet_detail(self, host_id, vswitch_name):
        """
        Get portgroup list from a specific vswitch in a specific host.
        :param host_id: the ID of a specific host.
        :param vswitch_name: the name of vswitch.
        :rtype: dict
        """
        content = self.content
        try:
            host_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
            portgroup_list = []
            for cur_host in host_view.view:
                if cur_host._moId == host_id:
                    host_pg_list = self.__get_host_pg_list(cur_host)
                    for cur_portgroup in cur_host.config.network.portgroup:
                        subnet_obj = self.__portgroup_format(cur_portgroup, host_pg_list, cur_host)
                        if not subnet_obj:
                            continue
                        portgroup_list.append(subnet_obj)
                    break
            return {"result": True, "data": [x for x in portgroup_list if x.get("vpc_id") == vswitch_name]}
        except Exception as e:
            logger.exception("get portgroup list from a specific host")
            return {"result": False, "message": str(e)}

        host_vswitch_rs = self.get_vpc_detail(host_id)
        network_list = []
        if host_vswitch_rs["result"]:
            vswitch_list = host_vswitch_rs["data"]
            for cur_vswitch in vswitch_list:
                if cur_vswitch.get("vs_name") == vswitch_name:
                    for port_group_name in cur_vswitch.get("port_group"):
                        for cur_network in cur_vswitch.get("network_list"):
                            if port_group_name == cur_network.get("name"):
                                network_list.append({"id": cur_network.get("id"), "name": cur_network.get("name")})
            return {"result": True, "data": network_list}
        else:
            return {"result": False, "message": "获取主机下的vswitch失败！"}

    def create_subnet(self, host_id, **kwargs):
        """
        Create a subnet from a specific network.
        :param host_id: the ID of a specific host.
        :param kwargs: accept multiple key value pair arguments.
        ---------------
        * vswitchName: the name of vswitch.(required)
        * portgroupName: the name of portgroup.(required)
        * vlanId: the ID of vlan.(required)
        ---------------
        :rtype: dict
        """
        content = self.content
        try:
            cluster_list = content.viewManager.CreateContainerView(content.rootFolder, [vim.ComputeResource], True).view
            for c in cluster_list:
                for h in c.host:
                    if h._moId == host_id:
                        portgroup_spec = vim.host.PortGroup.Specification()
                        portgroup_spec.vswitchName = kwargs.get("vswitchName", "")
                        portgroup_spec.name = kwargs.get("portgroupName", "")
                        portgroup_spec.vlanId = int(kwargs.get("vlanId", 0))
                        network_policy = vim.host.NetworkPolicy()
                        network_policy.security = vim.host.NetworkPolicy.SecurityPolicy()
                        network_policy.security.allowPromiscuous = True
                        network_policy.security.macChanges = False
                        network_policy.security.forgedTransmits = False
                        portgroup_spec.policy = network_policy
                        h.configManager.networkSystem.AddPortGroup(portgroup_spec)
                        return {"result": True, "data": kwargs.get("portgroupName", "")}
            else:
                return {"result": False, "message": "未匹配到指定的主机！"}
            return {"result": False, "message": "未匹配到该集群！"}
        except Exception as e:
            logger.exception("get_host_info")
            return {"result": False, "message": str(e)}

    def delete_subnet(self, host_id, portgroup_name):
        """
        Delete a specific portgroup from a specific host.
        :param host_id: the ID of a specific host.
        :param portgroupName: the name of portgroup.
        :rtype: dict
        """
        content = self.content
        try:
            cluster_list = content.viewManager.CreateContainerView(content.rootFolder, [vim.ComputeResource], True).view
            for c in cluster_list:
                for h in c.host:
                    if h._moId == host_id:
                        h.configManager.networkSystem.RemovePortGroup(portgroup_name)
                        return {"result": True}
                else:
                    return {"result": False, "message": "未匹配到指定的主机！"}
            return {"result": False, "message": "未匹配到该集群！"}
        except Exception as e:
            logger.exception("get_host_info")
            return {"result": False, "message": str(e)}

    def modify_subnet(self, host_id, **kwargs):
        """
        Modify a specific subnet from a specific network.
        :param host_id: the ID of a specific host.
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        return {"result": "False", "message": "修改portgroup参数暂时未实现！"}

    # ------------------***** charge *****-------------------
    def get_virtual_cost(self, **kwargs):
        """
        Get current cost budget.
        :param kwargs: accept multiple key value pair arguments.
        -----------------
        * account_name: account name.(required)
        -----------------
        :rtype: dict
        """
        content = self.content
        datacenter_list = content.viewManager.CreateContainerView(content.rootFolder, [vim.Datacenter], True).view
        return_data = []
        for i in datacenter_list:
            dc_id = i._moId
            cluster_list = i.hostFolder.childEntity
            for c in cluster_list:
                hc_id = c._moId
                vm_list = reduce(lambda a, b: a + b, [x.vm for x in c.host])
                computer_price_module, spec_list = get_compute_price_module(
                    "VMware", kwargs["account_name"], dc_id, hc_id
                )
                for v in vm_list:
                    price_vm = price_disk = 0
                    summary = v.summary
                    hardware = v.config.hardware
                    try:
                        if summary.config.template is False:
                            cpu = hardware.numCPU
                            mem = hardware.memoryMB / 1024
                            if computer_price_module:
                                for spec in spec_list:
                                    if int(spec[1]) == int(cpu) and int(spec[2]) == int(mem):
                                        price_vm = spec[3]
                            device = hardware.device
                            for d in device:
                                if isinstance(d, vim.vm.device.VirtualDisk):
                                    ds_id = d.backing.datastore._moId
                                    storage_price_module, storage_price = get_storage_pricemodule(
                                        "VMware", kwargs["account_name"], dc_id, ds_id
                                    )
                                    capacity = float(d.capacityInKB) / 1024 / 1024
                                    if storage_price_module:
                                        price_disk += capacity * storage_price[1]
                                    else:
                                        price_disk += 0
                            return_data.append(
                                {
                                    "resourceId": v._moId,
                                    "name": v.name,
                                    "cpu": cpu,
                                    "mem": mem,
                                    "cost_all": round(float(price_vm), 2) + round(float(price_disk), 2),
                                    "cost_vm": round(float(price_vm), 2),
                                    "cost_disk": round(float(price_disk), 2),
                                    "cost_net": 0.0,
                                    "cost_time": datetime.datetime.now().strftime("%Y-%m-%d"),
                                    "source_type": CloudResourceType.VM.value,
                                }
                            )
                    except Exception:
                        continue

        return {"result": True, "data": return_data}

    def get_computer_price(self, cpu, mem, computerpricemodule):
        """
        Get computer price
        :param cpu: the number of cpu.(required)
        :param mem: the size of memory.(required)
        :param computerpricemodule: computer price module.(required)
        :return:
        """
        if computerpricemodule.computerpricemoduledetail_set.filter(cpu=cpu, mem=mem).exists():
            price_vm = computerpricemodule.computerpricemoduledetail_set.filter(cpu=cpu, mem=mem).first().price_perday
        else:
            price_vm = 0
        return price_vm

    # ------------------***** monitor *****-------------------
    def monitor_data(self, counter="cpu.usage.average", interval=20, **kwargs):
        """
        monitor cpu usage or memory usage.
        :param counter: type str.(required) "cpu.usage.average" | "mem.usage.average"
        :param kwargs: accept multiple key value pair arguments.
        --------------
        * obj: vm object.(requried)
        * StartTime: start time.(required)
        * EndTime: end time.(required)
        --------------
        :rtype: dict
        """
        content = self.content
        obj = kwargs["obj"]
        start_time = kwargs["StartTime"]
        end_time = kwargs["EndTime"]
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        try:
            counter_info = self._get_vmware_metrics(content)
            counter_key = counter_info[counter]
            metric_id = vim.PerformanceManager.MetricId(counterId=counter_key, instance="*")

            spec_list = []
            for i in obj:
                spec = vim.PerformanceManager.QuerySpec(
                    startTime=start_time,
                    endTime=end_time,
                    entity=i,
                    metricId=[metric_id],
                    maxSample=1,
                    intervalId=interval,
                )
                spec_list.append(spec)
            result = content.perfManager.QueryPerf(querySpec=spec_list)
            return {"result": True, "res": result}
        except Exception as e:
            logger.exception("monitor_data")
            return {"result": False, "message": str(e)}

    def get_monitor_data(self, **kwargs):
        """
        Get monitor data from a specific vm.
        :param kwargs: accept multiple key value pair arguments.
        ------------------
        * StartTime: start time.(required)
        * EndTime: end time.(required)
        * resourceId: the ID of resource.(required)
        ------------------
        :rtype: dict
        """
        content = self.content
        now_time = datetime.datetime.now() + datetime.timedelta(minutes=-5)
        hour_time = datetime.datetime.now() + datetime.timedelta(hours=-1)
        now_time = datetime.datetime.strftime(now_time, "%Y-%m-%d %H:%M:%S")
        hour_time = datetime.datetime.strftime(hour_time, "%Y-%m-%d %H:%M:%S")
        data = {"StartTime": kwargs.get("StartTime", hour_time), "EndTime": kwargs.get("EndTime", now_time)}
        resource_id = kwargs.get("resourceId", "")
        resource_id_list = resource_id.split(",")
        obj_list = []
        res = {}
        try:
            container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
            for n in container.view:
                for i in resource_id_list:
                    if n._moId == i and n.summary.runtime.powerState == "poweredOn":
                        obj_list.append(n)
                        res[i] = {}
            if obj_list:
                data["obj"] = obj_list
                counter = "cpu.usage.average"
                cpu_result = self.monitor_data(counter, **data)
                counter = "mem.usage.average"
                memory_result = self.monitor_data(counter, **data)
                if cpu_result["result"]:
                    for n in cpu_result["res"]:
                        cpu_data = []
                        vm_name = str(n.entity._moId)
                        if n.value:
                            for k, i in enumerate(n.sampleInfo):
                                time_datetime = i.timestamp
                                time_cn = time_datetime + datetime.timedelta(hours=8)
                                timestamp = time.mktime(time_cn.timetuple())
                                rate = float(n.value[0].value[k])
                                cpu_data.append([timestamp, float("%.2f" % (rate / 100))])
                        res[vm_name]["cpu_data"] = cpu_data
                if memory_result["result"]:
                    for n in memory_result["res"]:
                        memory_data = []
                        vm_name = str(n.entity._moId)
                        if n.value:
                            for k, i in enumerate(n.sampleInfo):
                                time_datetime = i.timestamp
                                time_cn = time_datetime + datetime.timedelta(hours=8)
                                timestamp = time.mktime(time_cn.timetuple())
                                rate = int(n.value[0].value[k])
                                memory_data.append([timestamp, float("%.2f" % (rate / 100))])
                        res[vm_name]["memory_data"] = memory_data
                        res[vm_name]["disk_data"] = []
                res["result"] = True
                return res
            else:
                return {"result": False, "message": "未获取到监控信息"}
        except Exception as e:
            logger.exception("get_monitor_data")
            return {"result": False, "message": str(e)}

    def get_load_monitor_data(self, **kwargs):
        """
        Get monitor data from a specific vm.
        :param kwargs: accept multiple key value pair arguments.
        ------------------
        * StartTime: start time.(required)
        * EndTime: end time.(required)
        * resourceId: the ID of resource.(required)
        ------------------
        :rtype: dict
        """
        content = self.content
        now_time = datetime.datetime.now() + datetime.timedelta(minutes=-5)
        hour_time = datetime.datetime.now() + datetime.timedelta(hours=-1)
        data = {"StartTime": str(kwargs.get("StartTime", hour_time)), "EndTime": str(kwargs.get("EndTime", now_time))}
        resource_id_list = kwargs["resourceId"]
        obj_list = []
        res = {}
        try:
            container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
            for n in container.view:
                for i in resource_id_list:
                    if n._moId == i and n.summary.runtime.powerState == "poweredOn":
                        obj_list.append(n)
                        res[i] = {}
            if obj_list:
                data["obj"] = obj_list
                counter = "cpu.usage.average"
                cpu_result = self.monitor_data(counter, **data)
                counter = "mem.usage.average"
                memory_result = self.monitor_data(counter, **data)
                if cpu_result["result"]:
                    for n in cpu_result["res"]:
                        cpu_data = []
                        vm_name = str(n.entity._moId)
                        if n.value:
                            for k, i in enumerate(n.sampleInfo):
                                # time_datetime = i.timestamp
                                # time_cn = time_datetime + datetime.timedelta(hours=8)
                                # timestamp = time.mktime(time_cn.timetuple())
                                rate = float(n.value[0].value[k])
                                cpu_data.append(round(rate / 100, 3))
                        res[vm_name]["cpu_data"] = cpu_data
                if memory_result["result"]:
                    for n in memory_result["res"]:
                        memory_data = []
                        vm_name = str(n.entity._moId)
                        if n.value:
                            for k, i in enumerate(n.sampleInfo):
                                # time_datetime = i.timestamp
                                # time_cn = time_datetime + datetime.timedelta(hours=8)
                                # timestamp = time.mktime(time_cn.timetuple())
                                rate = float(n.value[0].value[k])
                                memory_data.append(round(rate / 100, 3))
                        res[vm_name]["memory_data"] = memory_data
                        res[vm_name]["load_data"] = []

                return {"result": True, "data": res}
            else:
                return {"result": False, "message": "未获取到监控信息"}
        except Exception as e:
            logger.exception("get_monitor_data")
            return {"result": False, "message": str(e)}

    def get_metric_counter(self, metric):
        metric_mapping = {
            "cpu_usage_average": "cpu.usage.average",
            "cpu_usagemhz_average": "cpu.usagemhz.average",
            "mem_usage_average": "mem.usage.average",
            "mem_consumed_average": "mem.consumed.average",
            # "disk_used_average": "disk.used.average", #磁盘使用率,需要单独计算,暂不支持
            "disk_read_average": "disk.read.average",
            "disk_write_average": "disk.write.average",
            "disk_numberRead_summation": "disk.numberRead.summation",
            "disk_numberWrite_summation": "disk.numberWrite.summation",
            "disk_io_usage": "disk.usage.average",
            "net_bytesRx_average": "net.bytesRx.average",
            "net_bytesTx_average": "net.bytesTx.average",
            "disk_used_latest": "disk.used.latest",
            "disk_capacity_latest": "disk.capacity.latest",
        }
        return metric_mapping.get(metric)

    def _get_vm_disk_used_average(self, obj_list, obj_type="vm"):
        metric_data = {}
        if obj_type == "vm":
            for obj in obj_list:
                disks = obj.guest.disk
                all_disk_capacity = 0
                all_used_space = 0
                # 遍历磁盘信息列表，计算每个磁盘的使用率
                for disk in disks:
                    disk_capacity = disk.capacity / (1024 * 1024)  # 将磁盘容量转换为 MB
                    disk_free_space = disk.freeSpace / (1024 * 1024)  # 将可用磁盘空间转换为 MB
                    disk_used_space = disk_capacity - disk_free_space
                    all_disk_capacity += disk_capacity
                    all_used_space += disk_used_space
                if all_disk_capacity == 0:
                    disk_usage = 0
                else:
                    disk_usage = round((all_used_space / all_disk_capacity) * 100, 3)
                metric_data[obj._moId] = disk_usage
            return metric_data
        else:
            return metric_data

    def _get_vm_datastore_accessible(self, obj_list):
        metric_data = {}
        for obj in obj_list:
            metric_data[obj._moId] = int(obj.summary.accessible)
        return metric_data

    def _get_esxi_cpu_usage(self, data=None):
        metric_data = {}
        data = data or {}
        cpu_usagemhz = self.monitor_data("cpu.usagemhz.average", **data)
        if not cpu_usagemhz["result"]:
            return {}

        for index, host in enumerate(cpu_usagemhz["res"]):
            hardware = host.entity.hardware
            esxi_name = str(host.entity._moId)
            cpu_info = hardware.cpuInfo

            # 总 CPU 核心数和每核心 MHz
            num_cores = cpu_info.numCpuCores  # 总核心数
            cpu_mhz = cpu_info.hz // 10 ** 6

            # 总 CPU 频率（以 MHz 为单位）
            total_cpu_mhz = num_cores * cpu_mhz

            if not host.value:
                return {}
            for k, i in enumerate(host.sampleInfo):
                time_datetime = i.timestamp
                time_cn = time_datetime + datetime.timedelta(hours=8)
                timestamp = int(time.mktime(time_cn.timetuple()))

            if total_cpu_mhz == 0:
                cpu_usage = 0
            else:
                # 计算 CPU 使用率
                cpu_usage = round(host.value[0].value[-1] / total_cpu_mhz * 100, 2)
            metric_data[esxi_name] = (cpu_usage, timestamp)

        return metric_data

    def _get_vm_datastore_disk(self, obj_list, metric, data=None):
        metric_data = {}
        data = data or {}
        used_latest_data = self.monitor_data("disk.used.latest", interval=300, **data)
        capacity_latest_data = self.monitor_data("disk.capacity.latest", interval=300, **data)
        if not all([capacity_latest_data["result"], used_latest_data["result"]]):
            return {}

        for index, used_latest in enumerate(used_latest_data["res"]):
            vm_name = str(used_latest.entity._moId)
            capacity_latest = capacity_latest_data["res"][index]
            if all(
                [
                    capacity_latest.value,
                    capacity_latest.value[0].value,
                    capacity_latest.value,
                    capacity_latest.value[0].value,
                ]
            ):
                lasted_used_value = used_latest.value[0].value[-1]
                lasted_capacity_value = capacity_latest.value[0].value[-1]
                if metric == "disk_used_average":
                    if lasted_used_value == 0:
                        value = 0
                    else:
                        value = float(round(lasted_used_value / lasted_capacity_value * 100, 3))
                elif metric == "disk_free_average":
                    value = float(round((lasted_capacity_value - lasted_used_value) / (1024 * 1024), 3))
                else:
                    continue
                metric_data[vm_name] = value

        return metric_data

    def get_weops_monitor_data(self, **kwargs):  # noqa
        """
        Get monitor data from a specific vm.
        :param kwargs: accept multiple key value pair arguments.
        ------------------
        * StartTime: start time.(required)
        * EndTime: end time.(required)
        * resourceId: the ID of resource.(required)
        ------------------
        :rtype: dict
        """
        content = self.content
        now_time = datetime.datetime.now() + datetime.timedelta(minutes=-5)
        hour_time = datetime.datetime.now() + datetime.timedelta(hours=-1)
        data = {"StartTime": str(kwargs.get("StartTime", hour_time)), "EndTime": str(kwargs.get("EndTime", now_time))}
        # 是否使用 UTC 时间
        utc = kwargs.get("utc", False)
        resource_id_list = kwargs["resourceId"]
        if isinstance(resource_id_list, str):
            resource_id_list = resource_id_list.split(",")

        resources = kwargs.get("context", {}).get("resources", [])
        if not resources:
            return {"result": False, "message": "未获取到实例信息"}
        metrics = kwargs.get("Metrics")
        _obj_type = None
        if resources[0]["bk_obj_id"] == "vmware_esxi":
            _obj_type = "esxi"
            obj_type = [vim.HostSystem]
            metrics = metrics or [
                "cpu_usage_average",
                "cpu_usagemhz_average",
                "mem_usage_average",
                "mem_consumed_average",
                "disk_read_average",
                "disk_write_average",
                "net_bytesRx_average",
                "net_bytesTx_average",
                "disk_numberRead_summation",
                "disk_numberWrite_summation",
            ]
        elif resources[0]["bk_obj_id"] == "vmware_ds":
            _obj_type = "datastore"

            obj_type = [vim.Datastore]
            metrics = metrics or ["disk_used_average", "disk_free_average", "store_accessible"]
        else:
            obj_type = [vim.VirtualMachine]
            _obj_type = "vm"
            metrics = metrics or [
                "cpu_usage_average",
                "cpu_usagemhz_average",
                "mem_usage_average",
                "mem_consumed_average",
                "disk_used_average",
                "disk_read_average",
                "disk_write_average",
                "net_bytesRx_average",
                "net_bytesTx_average",
                "disk_numberRead_summation",
                "disk_numberWrite_summation",
                "disk_io_usage",
                "power_state",
            ]
        obj_list = []
        res = {}
        try:
            container = content.viewManager.CreateContainerView(content.rootFolder, obj_type, True)
            for n in container.view:
                for i in resource_id_list:
                    if n._moId == i:
                        obj_list.append(n)
                        res[i] = {}
            if not obj_list:
                return {"result": False, "message": "未获取到监控信息"}
            filter_obj_list = obj_list
            if _obj_type == "vm":
                filter_obj_list = list(filter(lambda x: x.summary.runtime.powerState == "poweredOn", obj_list))
            for metric in metrics:
                if _obj_type == "vm" and metric == "power_state":
                    for obj in obj_list:
                        res.setdefault(obj._moId, {}).setdefault(metric, []).append(
                            [
                                int(time.mktime(time.strptime(data["EndTime"], "%Y-%m-%d %H:%M:%S"))) * 1000,
                                int(obj.summary.runtime.powerState == "poweredOn"),
                            ]
                        )
                        continue

                data["obj"] = filter_obj_list
                if metric == "disk_used_average" and _obj_type == "vm":
                    metric_data = self._get_vm_disk_used_average(filter_obj_list, obj_type=_obj_type)
                    for _obj, metric_value in metric_data.items():
                        res.setdefault(_obj, {}).setdefault(metric, []).append(
                            [int(time.mktime(time.strptime(data["EndTime"], "%Y-%m-%d %H:%M:%S"))) * 1000, metric_value]
                        )
                    continue
                elif metric == "store_accessible":
                    metric_data = self._get_vm_datastore_accessible(filter_obj_list)
                    for _obj, metric_value in metric_data.items():
                        res.setdefault(_obj, {}).setdefault(metric, []).append(
                            [int(time.mktime(time.strptime(data["EndTime"], "%Y-%m-%d %H:%M:%S"))) * 1000, metric_value]
                        )
                    continue
                elif metric in ["disk_used_average", "disk_free_average"] and _obj_type == "datastore":
                    metric_data = self._get_vm_datastore_disk(filter_obj_list, metric, data=data)
                    for _obj, metric_value in metric_data.items():
                        res.setdefault(_obj, {}).setdefault(metric, []).append(
                            [int(time.mktime(time.strptime(data["EndTime"], "%Y-%m-%d %H:%M:%S"))) * 1000, metric_value]
                        )
                    continue
                if _obj_type == "esxi" and metric in ["cpu_usage_average"]:

                    metric_data = self._get_esxi_cpu_usage(data=data)
                    for _obj, metric_value in metric_data.items():
                        value, timestamp = metric_value
                        res.setdefault(_obj, {}).setdefault(metric, []).append([timestamp * 1000, value])
                    continue

                counter = self.get_metric_counter(metric)
                if not counter:
                    continue
                metric_result = self.monitor_data(counter, **data)
                if metric_result["result"]:
                    for n in metric_result["res"]:
                        vm_name = str(n.entity._moId)
                        if n.value:
                            for k, i in enumerate(n.sampleInfo):
                                time_datetime = i.timestamp
                                if not utc:
                                    time_datetime = time_datetime + datetime.timedelta(hours=8)
                                timestamp = int(time.mktime(time_datetime.timetuple()))
                                # 补充维度能力
                                no_dims = len(n.value) == 1
                                for i in n.value:
                                    dims = None
                                    if not no_dims:
                                        instance = i.id.instance or n.entity.name
                                        dims = (("instance", instance),)
                                    rate = i.value[k]
                                    if metric in ["cpu_usage_average", "mem_usage_average", "disk_io_usage"]:
                                        rate = i.value[k] / 100
                                    if metric in ["mem_consumed_average"]:
                                        rate = i.value[k] / 1024
                                    _value = round(float(rate), 3)
                                    if not dims:
                                        res.setdefault(vm_name, {}).setdefault(metric, []).append(
                                            [timestamp * 1000, _value]
                                        )
                                    else:
                                        res.setdefault(vm_name, {}).setdefault(metric, {}).setdefault(dims, []).append(
                                            [timestamp * 1000, _value]
                                        )

            return {"result": True, "data": res}

        except Exception as e:
            logger.exception("get_weops_monitor_data")
            return {"result": False, "message": str(e)}

    # -----------***** private cloud compute *****-------------
    def get_hosts(self):
        """
        Get all host list.
        :param cluster_id: the ID of a specific cluster
        :rtype: dict
        """
        content = self.content
        try:
            cluster_list = content.viewManager.CreateContainerView(content.rootFolder, [vim.ComputeResource], True).view
            hosts_list = []
            for c in cluster_list:
                for h in c.host:
                    host_id = h._moId
                    vm_num = 0
                    for v in h.vm:
                        if not v.config.template:
                            vm_num += 1
                    hosts_list.append(
                        {
                            "resource_id": host_id,
                            "resource_name": h.name.decode("utf8"),
                            "resource_type": "physicalhost",
                            "moId": host_id,
                            "name": h.name.decode("utf8"),
                            "cluster_id": c._moId,
                            "ds_num": len(c.datastore),
                            "net_num": len(c.network),
                            "vm_num": vm_num,
                        }
                    )
            return {"result": True, "data": hosts_list}
        except Exception as e:
            logger.exception("get_host_info")
            return {"result": False, "message": str(e)}

    def get_hosts_by_cluster(self, cluster_id):
        """
        Get all host list.
        :param cluster_id: the ID of a specific cluster
        :rtype: dict
        """
        content = self.content
        try:
            cluster_list = content.viewManager.CreateContainerView(content.rootFolder, [vim.ComputeResource], True).view
            hosts_list = []
            for c in cluster_list:
                if c._moId == cluster_id:
                    for h in c.host:
                        host_id = h._moId
                        vm_num = 0
                        for v in h.vm:
                            if not v.config.template:
                                vm_num += 1
                        hosts_list.append(
                            {
                                "resource_id": host_id,
                                "resource_name": h.name,
                                "resource_type": "physicalhost",
                                "moId": host_id,
                                "name": h.name,
                                "cluster_id": c._moId,
                                "ds_num": len(c.datastore),
                                "net_num": len(c.network),
                                "vm_num": vm_num,
                            }
                        )
            return {"result": True, "data": hosts_list}
        except Exception as e:
            logger.exception("get_host_info")
            return {"result": False, "message": str(e)}

    def get_host_detail(self, host_id, cluster_id):
        """
        Get a specific host.
        :param host_id: the ID of a specific host.
        :param cluster_id: the ID of a specific cluster
        :rtype: dict
        """
        content = self.content
        try:
            cluster_list = content.viewManager.CreateContainerView(content.rootFolder, [vim.ComputeResource], True).view
            for c in cluster_list:
                c_id = c._moId
                if cluster_id == c_id:
                    for h in c.host:
                        if h._moId == host_id:
                            # 存储情况
                            ds_list = h.datastore
                            ds_sum = 0
                            ds_free = 0
                            for i in ds_list:
                                ds_sum += i.summary.capacity
                                ds_free += i.summary.freeSpace
                            # CPU、内存情况
                            cpu_used = (
                                0 if not h.summary.quickStats.overallCpuUsage else h.summary.quickStats.overallCpuUsage
                            )
                            memory_used = (
                                0
                                if not h.summary.quickStats.overallMemoryUsage
                                else h.summary.quickStats.overallMemoryUsage
                            )
                            ds_used = ds_sum - ds_free
                            cpu_sum = h.summary.hardware.cpuMhz * h.summary.hardware.numCpuCores
                            cpu_free = cpu_sum - cpu_used
                            memory_sum = h.summary.hardware.memorySize / 1024 / 1024
                            memory_free = memory_sum - memory_used
                            data = {
                                "ds_sum": "%.2f" % (float(ds_sum) / 1024 / 1024 / 1024),
                                "ds_used": "%.2f" % (float(ds_used) / 1024 / 1024 / 1024),
                                "ds_free": "%.2f" % (float(ds_free) / 1024 / 1024 / 1024),
                                "ds_per": int(float("%.2f" % (float(ds_used) / ds_sum)) * 100),
                                "CPU_sum": "%.2f" % (float(cpu_sum) / 1000),
                                "CPU_used": "%.2f" % (float(cpu_used) / 1000),
                                "CPU_free": "%.2f" % (float(cpu_free) / 1000),
                                "CPU_per": int(float("%.2f" % (float(cpu_used) / cpu_sum)) * 100),
                                "memory_sum": "%.2f" % (float(memory_sum) / 1024),
                                "memory_used": "%.2f" % (float(memory_used) / 1024),
                                "memory_free": "%.2f" % (float(memory_free) / 1000),
                                "memory_per": int(float("%.2f" % (float(memory_used) / memory_sum)) * 100),
                            }
                            return {"result": True, "data": data}
            return {"result": False, "message": "未匹配到该主机！"}
        except Exception as e:
            logger.exception("get_host_data")
            return {"result": False, "message": str(e)}

    def list_hosts(self, host_id=None, cluster_id=None):
        content = self.content
        try:
            cluster_list = content.viewManager.CreateContainerView(content.rootFolder, [vim.ComputeResource], True).view
            hosts_list = []
            for c in cluster_list:
                c_id = c._moId
                if host_id and cluster_id:
                    if cluster_id == c_id:
                        for h in c.host:
                            if h._moId == host_id:
                                host_instance = self._format_resource_result("host", {"h": h, "c": c})
                                if host_instance:
                                    hosts_list = [host_instance]
                else:
                    for h in c.host:
                        host_instance = self._format_resource_result("host", {"h": h, "c": c})
                        if host_instance:
                            hosts_list.append(host_instance)
            return {"result": True, "data": hosts_list}
        except Exception as e:
            logger.exception("get_host_info")
            return {"result": False, "message": str(e)}

    def get_clusters(self):
        """
        Get cluster list.
        :rtype: dict
        """
        content = self.content
        try:
            cluster_obj = content.viewManager.CreateContainerView(content.rootFolder, [vim.ComputeResource], True).view
            cluster_list = []
            for h in cluster_obj:
                # 虚机数量
                host_list = h.host
                vm_num = 0
                for i in host_list:
                    for k in i.vm:
                        if not k.config.template:
                            vm_num += 1
                cluster_list.append(
                    {
                        "resource_id": h._moId,
                        "resource_name": h.name.decode("utf8"),
                        "resource_type": "cluster",
                        "moId": h._moId,
                        "name": h.name.decode("utf8"),
                        "ds_num": len(h.datastore),
                        "vm_num": vm_num,
                        "net_num": len(h.network),
                    }
                )
            return {"result": True, "data": cluster_list}
        except Exception as e:
            logger.exception("get_cluster_info")
            return {"result": False, "message": str(e)}

    def get_cluster_detail(self, cluster_id):
        """
        Get a specific cluster.
        :param cluster_id: the ID of a specific cluster.
        :rtype: dict
        """
        content = self.content
        try:
            host_list = content.viewManager.CreateContainerView(content.rootFolder, [vim.ComputeResource], True).view
            for h in host_list:
                if h._moId == cluster_id:
                    # 存储情况
                    ds_list = h.datastore
                    ds_sum = 0
                    ds_free = 0
                    for i in ds_list:
                        ds_sum += i.summary.capacity
                        ds_free += i.summary.freeSpace
                    # CPU、内存情况
                    cluster_host_list = h.host
                    cpu_used = 0
                    memory_used = 0
                    for i in cluster_host_list:
                        cpu_used += (
                            0 if not i.summary.quickStats.overallCpuUsage else i.summary.quickStats.overallCpuUsage
                        )
                        memory_used += (
                            0
                            if not i.summary.quickStats.overallMemoryUsage
                            else i.summary.quickStats.overallMemoryUsage
                        )
                    ds_used = ds_sum - ds_free
                    cpu_sum = h.summary.totalCpu
                    cpu_free = cpu_sum - cpu_used
                    memory_sum = h.summary.totalMemory / 1024 / 1024
                    memory_free = memory_sum - memory_used
                    data = {
                        "ds_sum": "%.2f" % (float(ds_sum) / 1024 / 1024 / 1024),
                        "ds_used": "%.2f" % (float(ds_used) / 1024 / 1024 / 1024),
                        "ds_free": "%.2f" % (float(ds_free) / 1024 / 1024 / 1024),
                        "ds_per": int(float("%.2f" % (float(ds_used) / ds_sum)) * 100),
                        "CPU_sum": "%.2f" % (float(cpu_sum) / 1000),
                        "CPU_used": "%.2f" % (float(cpu_used) / 1000),
                        "CPU_free": "%.2f" % (float(cpu_free) / 1000),
                        "CPU_per": int(float("%.2f" % (float(cpu_used) / cpu_sum)) * 100),
                        "memory_sum": "%.2f" % (float(memory_sum) / 1024),
                        "memory_used": "%.2f" % (float(memory_used) / 1024),
                        "memory_free": "%.2f" % (float(memory_free) / 1000),
                        "memory_per": int(float("%.2f" % (float(memory_used) / memory_sum)) * 100),
                    }
                    return {"result": True, "data": data}
            return {"result": False, "message": "未匹配到该集群！"}
        except Exception as e:
            logger.exception("get_cluster_data")
            return {"result": False, "message": str(e)}

    def list_clusters(self, ids):
        """
        Get cluster list.
        :rtype: dict
        """
        content = self.content
        try:
            cluster_obj = content.viewManager.CreateContainerView(content.rootFolder, [vim.ComputeResource], True).view
            cluster_list = []
            for h in cluster_obj:
                if ids:
                    if h._moId == ids[0]:
                        cluster_instance = self._format_resource_result("cluster", h)
                        if cluster_instance:
                            cluster_list = [cluster_instance]
                else:
                    cluster_instance = self._format_resource_result("cluster", h)
                    if cluster_instance:
                        cluster_list.append(cluster_instance)
            return {"result": True, "data": cluster_list}
        except Exception as e:
            logger.exception("get_cluster_info")
            return {"result": False, "message": str(e)}

    def __cluster_format(self, cluster_obj):
        pass

    @classmethod
    def _get_vmware_metrics(cls, content):
        # create a mapping from performance stats to their counterIDs
        # counter_info: [performance stat => counterId]
        # performance stat example: cpu.usagemhz.LATEST
        perf_manager = content.perfManager
        counters = perf_manager.perfCounter
        counter_info = {}
        for counter in counters:
            counter_full_name = f"{counter.groupInfo.key}.{counter.nameInfo.key}.{counter.rollupType}"
            counter_info[counter_full_name] = counter.key
        return counter_info

    # ------------------***** storage *****-------------------
    def get_local_storage(self, **kwargs):
        """
        Get local storage list from all datacenters.
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        datacenter_rs = self.list_regions()
        all_datacenter_store_list = []
        if datacenter_rs["result"]:
            datacenter_list = datacenter_rs["data"]
            for cur_datacenter in datacenter_list:
                cur_datacenter_store_rs = self.get_local_storage_detail(cur_datacenter.get("id"))
                if cur_datacenter_store_rs["result"]:
                    all_datacenter_store_list.extend(cur_datacenter_store_rs["data"])
            return {"result": True, "data": all_datacenter_store_list}
        else:
            return {"result": False, "message": "获取数据中心失败！"}

    def get_local_storage_detail(self, region):
        """
        Get local storage list under a specific datacenter.
        :param dc_id: the ID of a specific datacenter.
        :rtype: dict
        """
        dc = self._get_obj_bymoId(self.content, [vim.Datacenter], region)
        # container1 = self.content.viewManager.CreateContainerView(dc.datastoreFolder, [vim.StoragePod], True).view
        container2 = self.content.viewManager.CreateContainerView(dc.datastoreFolder, [vim.Datastore], True).view
        # datastore_list = [{"id": i._moId, "name": i.name, "type": "StoragePod"} for i in container1]
        result_data = []
        for i in container2:
            if not isinstance(i.parent, vim.StoragePod):
                private_storage_instance = self._format_resource_result("private_storage", i)
                if private_storage_instance:
                    result_data.append(private_storage_instance)
        return {"result": True, "data": result_data}

        # return {"result": True, "data": datastore_list}

    def list_private_storages(self, ids=None):
        """
        ids => region
        """
        all_datacenter_store_list = []
        try:
            if ids:
                cur_datacenter_store_rs = self.get_local_storage_detail(ids[0])
                if cur_datacenter_store_rs["result"] and cur_datacenter_store_rs["data"]:
                    all_datacenter_store_list.extend(cur_datacenter_store_rs["data"])
            else:
                datacenter_rs = self.list_regions()
                if datacenter_rs["result"]:
                    datacenter_list = datacenter_rs["data"]
                    for cur_datacenter in datacenter_list:
                        cur_datacenter_store_rs = self.get_local_storage_detail(cur_datacenter.get("resource_id"))
                        if cur_datacenter_store_rs["result"] and cur_datacenter_store_rs["data"]:
                            all_datacenter_store_list.extend(cur_datacenter_store_rs["data"])
            return {"result": True, "data": all_datacenter_store_list}
        except Exception as e:
            logger.exception("get_private_storage_info")
            return {"result": False, "message": str(e)}

    # ------------------***** vmware private *****-------------
    # 关闭虚拟机电源
    def poweroff_vm(self, vmargs):
        """
        Power off a specific vm.
        :param vmargs: type: dict.
            keys:
                ---------------
                vm_moId: the ID of a specific vm.
                ---------------
        :rtype: dict
        """
        content = self.content
        try:
            vm = self._get_obj_bymoId(content, [vim.VirtualMachine], vmargs["vm_moId"])
            task = vm.PowerOff()
            task_result = self._wait_for_task(task)
            return task_result
        except Exception as e:
            error_msg = e.message if e.message else str(e)
            return {"result": False, "message": error_msg}

    # 重置虚拟机
    def reset_vm(self, vmargs):
        """
        Reset a specific vm.
        :param vmargs: type: dict.
            keys:
                ---------------
                vm_moId: the ID of a specific vm.
                ---------------
        :rtype: dict
        """
        content = self.content
        try:
            vm = self._get_obj_bymoId(content, [vim.VirtualMachine], vmargs["vm_moId"])
            task = vm.Reset()
            task_result = self._wait_for_task(task)
            return task_result
        except Exception as e:
            error_msg = e.message if e.message else str(e)
            return {"result": False, "message": error_msg}

    # 挂起虚拟机
    def suspend_vm(self, vmargs):
        """
        Suspend a specific vm.
        :param vmargs: type: dict.
            keys:
                ---------------
                vm_moId: the ID of a specific vm.
                ---------------
        :rtype: dict
        """
        content = self.content
        try:
            vm = self._get_obj_bymoId(content, [vim.VirtualMachine], vmargs["vm_moId"])
            task = vm.Suspend()
            task_result = self._wait_for_task(task)
            return task_result
        except Exception as e:
            error_msg = e.message if e.message else str(e)
            return {"result": False, "message": error_msg}

    # 移除虚拟机
    def remove_vm(self, vmargs):
        """
        Remove a specific vm(the disks of the vm will be delete.
        :param vmargs: type: dict.
            keys:
                ---------------
                * vm_moId: the ID of a specific vm.
                ---------------
        :rtype: dict
        """
        content = self.content
        try:
            vm = self._get_obj_bymoId(content, [vim.VirtualMachine], vmargs["vm_moId"])
            vm.UnregisterVM()
            return {"result": True}
        except Exception as e:
            error_msg = e.message if e.message else str(e)
            return {"result": False, "message": error_msg}

    def _get_child_folder(self, folder):
        folder_child = []
        folder_temp = folder.childEntity
        for i in folder_temp:
            if hasattr(i, "childEntity"):
                child_obj = {"moId": i._moId, "name": i.name, "children": self._get_child_folder(i), "id": i._moId}
                folder_child.append(child_obj)
        return folder_child

    # 获取文件夹
    def get_folder_info(self, dc_id):
        content = self.content
        try:
            dc = self._get_obj_bymoId(content, [vim.Datacenter], dc_id)
            folder = dc.vmFolder
            folder_list = self._get_child_folder(folder)
            if not len(folder_list):
                fo_id = folder._moId
                folder_list = [{"moId": fo_id, "name": folder.name, "children": [], "id": fo_id}]
            return {"result": True, "data": folder_list}
        except Exception as e:
            logger.exception("get_folder")
            return {"result": False, "message": str(e)}

    # 获取主机和群集
    def get_hc_info(self, dc_id):
        content = self.content
        try:
            dc = self._get_obj_bymoId(content, [vim.Datacenter], dc_id)
            container = content.viewManager.CreateContainerView(dc.hostFolder, [vim.ComputeResource], True)
            hc_data = []
            for i in container.view:
                hc_id = i._moId
                if isinstance(i, vim.ClusterComputeResource):
                    hc_data.append({"hc_moId": hc_id, "hc_name": i.name, "type": "ClusterComputer"})
                else:
                    hc_data.append({"hc_moId": hc_id, "hc_name": i.name, "type": "Computer"})
            return {"result": True, "data": hc_data}
        except Exception as e:
            logger.exception("get_hc_info")
            return {"result": False, "message": str(e)}

    # 获取hc存储
    def get_ds_info(self, hc_id):
        content = self.content
        try:
            hc = self._get_obj_bymoId(content, [vim.ClusterComputeResource], hc_id)
            if not hc:
                hc = self._get_obj_bymoId(content, [vim.ComputeResource], hc_id)
            datastore = hc.datastore
            datastore_list = []
            for i in datastore:
                if isinstance(i.parent, vim.StoragePod):
                    i = i.parent
                summary = i.summary
                ds_id = i._moId
                if hasattr(summary, "accessible"):
                    if summary.accessible:
                        if {"ds_moId": ds_id, "ds_name": i.name} not in datastore_list:
                            datastore_list.append({"ds_moId": ds_id, "ds_name": i.name})
                else:
                    if {"ds_moId": ds_id, "ds_name": i.name} not in datastore_list:
                        datastore_list.append({"ds_moId": ds_id, "ds_name": i.name})
            return {"result": True, "data": datastore_list}
        except Exception as e:
            logger.exception("get_ds_info")
            return {"result": False, "message": str(e)}

    def get_datacenters(self):
        """
        Get datacenter list.
        :rtype: dict
        """
        try:
            container = self.content.viewManager.CreateContainerView(self.content.rootFolder, [vim.Datacenter], True)
            dc_data = []
            for i in container.view:
                dc_data.append({"dc_moId": i._moId, "dc_name": i.name})
            return {"result": True, "data": dc_data}
        except Exception as e:
            logger.exception("get_datacenter_info error")
            return {"result": False, "message": str(e)}

    def remove_custom_field(self, key):
        """
        Remove a custom field.
        :param key: the key of a specific custom field. type int
        :rtype: dict
        """
        service_instance = self.si
        try:
            custom_fields_manage = service_instance.RetrieveServiceContent().customFieldsManager
            custom_fields_manage.RemoveCustomFieldDef(key)
            return {"result": True}
        except Exception as e:
            logger.exception("Remove a custom[key:" + key + "] field!")
            error_msg = e.message if e.message else str(e)
            return {"result": False, "message": error_msg}

    def update_custom_field(self, vm_id, key, value):
        """
        Assigns a value to a custom field on an entity.
        :param vm_id: the ID of a specific vm.
        :param key: the key of a specific custom field. type int
        :param value: the value of a specific custom field. type string
        :rtype: dict
        """
        service_instance = self.si
        content = self.content
        try:
            vm_obj = self._get_obj_bymoId(content, [vim.VirtualMachine], vm_id)
            custom_fields_manage = service_instance.RetrieveServiceContent().customFieldsManager
            custom_fields_manage.SetField(vm_obj, key, value)
            return {"result": True}
        except Exception as e:
            logger.exception("Assigns a value to a custom field[key=" + key + ", value=" + value + "] failed")
            error_msg = e.message if e.message else str(e)
            return {"result": False, "message": error_msg}

    def get_self_define_properties(self, **kwargs):
        """
        Get self_define property list.
        :param kwargs: accept multiple key value pair arguments.
        ----------------
        * type: the type of tag.(required) eg. vim.VirtualMachine
        ----------------
        :rtype: dict
        """
        service_instance = self.si
        try:
            custom_fields_manage = service_instance.RetrieveServiceContent().customFieldsManager
            vm_self_define_property_list = []
            if kwargs.get("type"):
                for cur_custom_field_obj in custom_fields_manage.field:
                    if cur_custom_field_obj.managedObjectType == kwargs.get("type"):
                        vm_self_define_property_list.append(
                            {"key": cur_custom_field_obj.key, "name": cur_custom_field_obj.name}
                        )
            else:
                for cur_custom_field_obj in custom_fields_manage.field:
                    vm_self_define_property_list.append(
                        {"key": cur_custom_field_obj.key, "name": cur_custom_field_obj.name}
                    )
            return {"result": True, "data": vm_self_define_property_list}
        except Exception as e:
            logger.exception("get vm self_define property list failed!")
            error_msg = e.message if e.message else str(e)
            return {"result": False, "message": error_msg}

    def get_vm_self_define_properties(self, vm_id):
        """
        Get self_define property list from a specific vm.
        :param vm_id: the ID of a specific vm.
        :rtype: dict
        """
        content = self.content
        try:
            vm_obj = self._get_obj_bymoId(content, [vim.VirtualMachine], vm_id)
            self_define_property_list = []
            for cur_custom_obj in vm_obj.summary.customValue:
                if cur_custom_obj.value:
                    self_define_property_list.append({"key": cur_custom_obj.key, "value": cur_custom_obj.value})
            vm_label_list_rs = self.get_tags(type=vim.VirtualMachine)
            if vm_label_list_rs["result"]:
                for cur_obj in self_define_property_list:
                    for vl in vm_label_list_rs["data"]:
                        if cur_obj.get("key") == vl.get("key"):
                            cur_obj.update({"name": vl.get("name")})
                            break
            return {"result": True, "data": self_define_property_list}
        except Exception as e:
            logger.exception("get vm[" + vm_id + "] self_define properties failed!")
            error_msg = e.message if e.message else str(e)
            return {"result": False, "message": error_msg}

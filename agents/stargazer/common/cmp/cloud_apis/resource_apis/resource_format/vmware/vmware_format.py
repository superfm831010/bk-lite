# -*- coding: utf-8 -*-
"""Vmware数据格式转换"""
import threading

from loguru import logger

from common.cmp.cloud_apis.cloud_object.base import (
    VM,
    VPC,
    Cluster,
    Disk,
    HostMachine,
    Image,
    PrivateStorage,
    Region,
    Snapshot,
    Subnet,
    Zone,
)

# from common.cmp.cloud_apis.resource_apis.constant import VmwareVirtualMachineStatus
from common.cmp.cloud_apis.resource_apis.resource_format.vmware.vmware_format_utils import (
    format_disk_status,
    format_disk_type,
    format_image_status,
    format_image_type,
    format_instance_status,
    format_snapshot_status,
    format_snapshot_type,
    format_subnet_status,
    format_vpc_status,
)


class VmWareResourceFormat:
    _instance_lock = threading.Lock()

    def __init__(self, account_id="", cloud_type="", region_id="", zone_id=""):
        self.account_id = account_id
        self.cloud_type = cloud_type
        self.region_id = region_id
        self.zone_id = zone_id

    def format_vm(self, object_json, **kwargs):
        vm_config = object_json.config
        vm_hardware = vm_config.hardware
        vm_id = object_json._moId
        name = object_json.name
        # status = getattr(VmwareVirtualMachineStatus, object_json.runtime.powerState + "_cn", "未知状态")
        status = format_instance_status(object_json.runtime.powerState)
        vcpus = vm_hardware.numCPU
        mem = vm_hardware.memoryMB
        uuid_raw_list = vm_config.uuid.split("-")
        uuid = ""
        for n, i in enumerate(uuid_raw_list):
            a1 = i[:2]
            a2 = i[2:4]
            a3 = i[4:6]
            a4 = i[6:]
            if n < 3:
                uuid += a4 + a3 + a2 + a1 + "-"
            else:
                uuid += a1 + a2 + a3 + a4 + "-"
        uuid = uuid[:-1]
        host_obj = object_json.summary.runtime.host
        # region_obj = object_json.parent.parent
        zone_obj = host_obj.parent
        region_obj = zone_obj.parent.parent
        # disk_list = []
        # disk_object_rs = self.get_vm_disks(object_json._moId)
        # if disk_object_rs["result"]:
        #     disk_list = disk_object_rs["data"]
        # handle nic
        inner_ip_list = []
        nic_list = []
        for cur_net in object_json.guest.net:
            if cur_net.network:
                if cur_net.ipAddress:
                    for i in cur_net.ipAddress:
                        if len(i) <= 15:
                            inner_ip_list.append(i)
                    # inner_ip_list.append(cur_net.ipAddress[0])
                nic_list.append(
                    {
                        # "ip": cur_net.ipAddress[0] if cur_net.ipAddress else "",
                        "ip": inner_ip_list[0] if inner_ip_list else "",
                        "mac": cur_net.macAddress,
                        "name": cur_net.network,
                    }
                )
        # handle snapshot
        # snapshot_list = None
        # snapshot_obj_rs = self.get_vm_snapshots({"vm_id": vm_id, "vm_name": name})
        # if snapshot_obj_rs["result"]:
        #     snapshot_list = snapshot_obj_rs["data"]

        return VM(
            cloud_type=self.cloud_type,
            resource_id=vm_id,
            resource_name=name,
            status=status,
            uuid=uuid,
            vcpus=vcpus,
            memory=mem,
            # instance_type=kwargs.get("InstanceType", ""),
            # image={"id": vm_config.guestFullName, "name": vm_config.guestId}, # TODO 这里可能反了
            image=vm_config.guestId,
            os_name=vm_config.guestFullName,
            inner_ip=inner_ip_list,
            public_ip=[],
            # charge_type=format_instance_charge_type(object_json["InstanceChargeType"]),
            # internet_accessible=object_json.get("InternetChargeType"),
            tag=[],
            zone=zone_obj._moId,
            region=region_obj._moId,
            create_time="",
            # expired_time=handle_time_str(object_json.get("ExpiredTime", "")),
            extra={},
        ).to_dict()
        # return VM(
        #             id=vm_id,
        #             name=name,
        #             status=status,
        #             platform_type=CloudType.VMWARE.value,
        #             vcpus=vcpus,
        #             mem=mem,
        #             uuid=uuid,
        #             flavor_info={},
        #             image_info={"id": vm_config.guestFullName, "name": vm_config.guestId},
        #             os_name=vm_config.guestFullName,
        #             disk_info=disk_list,
        #             inner_ip=inner_ip_list,
        #             public_ip=[],
        #             nic_info=nic_list,
        #             security_group_info=[],
        #             project_info={},
        #             tags=[],
        #             description=vm_config.annotation,
        #             snapshot_info=snapshot_list,
        #             host_id=host_obj._moId,
        #             host_name=host_obj.name,
        #             created_time="",
        #             updated_time="",
        #             region_info={"id": region_obj._moId, "name": region_obj.name},
        #             region_id=region_obj._moId,
        #             region_name=region_obj.name,
        #             charge_type="",
        #             end_time="",
        #             zone_info={"id": zone_obj._moId, "name": zone_obj.name},
        #             zone_id=zone_obj._moId,
        #             zone_name=zone_obj.name,
        #             extra={},
        #         ).to_dict()

    def format_image(self, object_json, **kwargs):
        vm_config = object_json.config
        # region_obj = object_json.parent.parent
        return Image(
            cloud_type=self.cloud_type,
            resource_id=object_json._moId,
            resource_name=object_json.name,
            # desc=object_json.get("Description", ""),
            os_name=vm_config.guestFullName,
            tag=[],
            status=format_image_status(),
            create_time="",
            # platform=CloudType.VMWARE.value,
            image_type=format_image_type(),
            # arch=object_json.get("Architecture", ""),
            # image_family=object_json.get("ImageFamily", ""),
            # image_version=object_json.get("ImageVersion", ""),
            os_type="",
            # os_name=object_json.get("OSName", ""),
            # os_name_en=object_json.get("OSNameEn", ""),
            extra={},
        ).to_dict()
        # return Image(
        #     id=template_obj._moId,
        #     name=template_obj.name,
        #     image_size="",
        #     status="可用",
        #     platform_type=CloudType.VMWARE.value,
        #     image_platform=vm_config.guestFullName,
        #     image_type="私有",
        #     tags=[],
        #     description=vm_config.annotation,
        #     created_time="",
        #     updated_time="",
        #     os_arch="",
        #     os_bit="",
        #     os_type="",
        #     image_format="",
        #     project_info={},
        #     region_info={"id": region_obj._moId, "name": region_obj.name},
        #     zone_info={},
        #     visibility="",
        #     extra={},
        # ).to_dict()

    def format_vpc(self, object_json, **kwargs):
        vswitch_obj = object_json["cur_vswitch"]
        host_obj = object_json["cur_host"]
        if vswitch_obj:
            zone_obj = host_obj.parent
            region_obj = zone_obj.parent.parent
            return VPC(
                cloud_type=self.cloud_type,
                resource_id="{}({})".format(
                    vswitch_obj.name.replace("/", "").replace(".", "").replace(" ", ""), host_obj.name
                ),
                resource_name=vswitch_obj.name,
                status=format_vpc_status(),
                host=host_obj._moId,
                # router=object_json.get("VRouterId", ""),
                # router_tables=object_json.get("RouterTableIds", ""),
                resource_group="",
                create_time="",
                # cidr=object_json.get("CidrBlock", ""),
                # cidr_v6=object_json.get("Ipv6CidrBlock", ""),
                region=region_obj._moId,
                zone=zone_obj._moId,
                # desc=object_json.get("Description", ""),
                tag=[],
                extra={"mtu": vswitch_obj.mtu},
            ).to_dict()
            # return VPC(
            #     id=vswitch_obj.name.replace("/", "").replace(".", ""),
            #     name=vswitch_obj.name,
            #     status="可用",
            #     platform_type=CloudType.VMWARE.value,
            #     router_info=[],
            #     network_addr="",
            #     is_default=None,
            #     region_info={"id": region_obj._moId, "name": region_obj.name},
            #     zone_info={"id": zone_obj._moId, "name": zone_obj.name},
            #     vm_host_id=host_obj._moId,
            #     project_info={},
            #     description="",
            #     tags=[],
            #     updated_time="",
            #     created_time="",
            #     resource_group="",
            #     extra={"mtu": vswitch_obj.mtu},
            # ).to_dict()
        else:
            return None

    def format_subnet(self, object_json, **kwargs):
        portgroup_obj = object_json["cur_portgroup"]
        host_pg_list = object_json["host_pg_list"]
        host_obj = object_json["cur_host"]
        if portgroup_obj:
            zone_obj = host_obj.parent
            region_obj = zone_obj.parent.parent
            portgroup_name = portgroup_obj.key.split("key-vim.host.PortGroup-")[1]
            # portgroup_id = None
            # vm_num = 0
            for cur_pg in host_pg_list:
                if cur_pg.get("name") == portgroup_name:
                    portgroup_id = cur_pg.get("id")
                    vm_num = cur_pg.get("vm_num")
                    break
            else:
                return None
            return Subnet(
                cloud_type=self.cloud_type,
                resource_id=portgroup_id,
                resource_name="{}({})".format(portgroup_name, host_obj.name),
                vpc="{}({})".format(
                    portgroup_obj.vswitch.split("key-vim.host.VirtualSwitch-")[1]
                    .replace("/", "")
                    .replace(".", "")
                    .replace(" ", ""),
                    host_obj.name,
                ),
                status=format_subnet_status(),
                # cidr=object_json.get("CidrBlock", ""),
                # cidr_v6=object_json.get("Ipv6CidrBlock", ""),
                # router_table_id=object_json["RouteTable"].get("RouteTableId", ""),
                # is_default=object_json.get("IsDefault", False),
                # resource_group=object_json.get("ResourceGroupId", ""),
                tag=[],
                # desc=object_json.get("Description", ""),
                region=region_obj._moId,
                zone=zone_obj._moId,
                extra={"vm_num": vm_num},
            ).to_dict()
            # return Subnet(
            #     id=portgroup_id,
            #     name=portgroup_name,
            #     status="可用",
            #     platform_type=CloudType.VMWARE.value,
            #     updated_time="",
            #     created_time="",
            #     tags=[],
            #     description="",
            #     vm_host_id=host_obj._moId,
            #     project_info={},
            #     region_info={"id": region_obj._moId, "name": region_obj.name},
            #     zone_info={"id": zone_obj._moId, "name": region_obj.name},
            #     extra={
            #         "vm_num": vm_num,
            #     },
            # ).to_dict()
        else:
            return None

    def format_disk(self, object_json, **kwargs):
        disk_obj = object_json["dev"]
        vm_obj = object_json["vm_obj"]

        if disk_obj:
            data_store = disk_obj.backing.datastore
            region_obj = data_store.parent.parent
            return Disk(
                cloud_type=self.cloud_type,
                resource_id=disk_obj.backing.uuid,
                resource_name=disk_obj.deviceInfo.label,
                # desc=object_json.get("Description", ""),
                disk_type=format_disk_type(disk_obj.unitNumber),
                disk_size=int(disk_obj.capacityInKB / 1024 / 1024),
                charge_type="",
                # portable=object_json.get("Portable", True),
                status=format_disk_status(),
                is_attached=True,
                server_id=vm_obj._moId,
                # delete_with_instance=object_json.get("DeleteWithInstance", True),
                zone=data_store._moId,
                region=region_obj._moId,
                extra={
                    "provisioned": "精简置备" if getattr(disk_obj.backing, "thinProvisioned", None) else "厚置备",
                    "fileName": disk_obj.backing.fileName,
                    "unitNumber": disk_obj.unitNumber,
                },
            ).to_dict()
            # return Disk(
            #     id=disk_obj.backing.uuid,
            #     name=disk_obj.deviceInfo.label,
            #     device_type="",
            #     status="使用中",
            #     disk_size=int(disk_obj.capacityInKB / 1024 / 1024),
            #     platform_type=CloudType.VMWARE.value,
            #     is_attached=True,
            #     disk_type="系统盘" if disk_obj.unitNumber == 0 else "数据盘",
            #     description="",
            #     encrypted="",
            #     tags=[],
            #     disk_format="",
            #     project_info={},
            #     region_info={"id": region_obj._moId, "name": region_obj.name},
            #     zone_id=data_store._moId,
            #     zone_name=data_store.name,
            #     server_id=vm_obj._moId,
            #     server_name=vm_obj.name,
            #     snapshot_info=[],
            #     charge_type="",
            #     end_time="",
            #     created_time="",
            #     updated_time="",
            #     extra={
            #         "provisioned": "精简置备" if disk_obj.backing.thinProvisioned else "厚置备",
            #         "fileName": disk_obj.backing.fileName,
            #         "unitNumber": disk_obj.unitNumber,
            #     },
            # ).to_dict()
        else:
            return None

    def format_snapshot(self, object_json, **kwargs):
        vm_param_obj = object_json["vm_param_obj"]
        cur_obj = object_json["cur_obj"]
        cur_snapshot_obj = cur_obj.snapshot
        region_obj = cur_obj.vm.parent.parent.parent
        zone_obj = cur_obj.vm.resourcePool.parent
        return Snapshot(
            cloud_type=self.cloud_type,
            resource_id=cur_snapshot_obj._moId,
            resource_name=cur_obj.name,
            desc=cur_obj.description,
            tag=[],
            snapshot_type=format_snapshot_type(),
            disk_id="",
            # disk_size=object_json.get("SourceDiskSize", 0),
            status=format_snapshot_status(),
            server_id=vm_param_obj["vm_id"],
            # disk_type=format_disk_type(object_json.get("SourceDiskType", "")),
            create_time=cur_obj.createTime.strftime("%Y-%m-%d %H:%M:%S"),
            region=region_obj._moId,
            zone=zone_obj._moId,
            extra={},
        ).to_dict()
        # Snapshot(
        #         id=cur_snapshot_obj._moId,
        #         name=cur_obj.name,
        #         snapshot_type="虚拟机",
        #         snapshot_size=0,
        #         disk_id="",
        #         disk_name="",
        #         server_id=vm_param_obj["vm_id"],
        #         server_name=vm_param_obj["vm_name"],
        #         status="创建成功",
        #         platform_type=CloudType.VMWARE.value,
        #         encrypted="",
        #         tags=[],
        #         description=cur_obj.description,
        #         created_time=cur_obj.createTime.strftime("%Y-%m-%d %H:%M:%S"),
        #         updated_time="",
        #         project_info="",
        #         region_info={"id": region_obj._moId, "name": region_obj.name},
        #         zone_info={"id": zone_obj._moId, "name": zone_obj.name},
        #         extra={},
        #     ).to_dict()

    def format_region(self, object_json, **kwargs):
        return Region(
            resource_id=object_json._moId, resource_name=object_json.name, cloud_type=self.cloud_type, extra={}
        ).to_dict()

    def format_zone(self, object_json, **kwargs):
        obj = object_json["obj"]
        region_id = object_json["region_id"]
        region_name = object_json["region_name"]
        return Zone(
            region=region_id,
            cloud_type=self.cloud_type,
            resource_id=obj._moId,
            resource_name=obj.name,
            extra={"dc_id": region_id, "dc_name": region_name},
        ).to_dict()

    def format_cluster(self, object_json, **kwargs):
        if not object_json:
            return None

        host_list = object_json.host
        vm_num = 0
        for i in host_list:
            for k in i.vm:
                try:
                    if not k.config.template:
                        vm_num += 1
                except Exception:
                    logger.error("format_cluster——not found attribute template: {}".format(k.name))
        ds_list = object_json.datastore
        ds_sum = 0
        ds_free = 0
        for i in ds_list:
            ds_sum += i.summary.capacity
            ds_free += i.summary.freeSpace
        # CPU、内存情况
        cpu_used = 0
        memory_used = 0
        for i in host_list:
            cpu_used += 0 if not i.summary.quickStats.overallCpuUsage else i.summary.quickStats.overallCpuUsage
            memory_used += 0 if not i.summary.quickStats.overallMemoryUsage else i.summary.quickStats.overallMemoryUsage
        ds_used = ds_sum - ds_free
        cpu_sum = object_json.summary.totalCpu
        cpu_free = cpu_sum - cpu_used
        memory_sum = object_json.summary.totalMemory / 1024 / 1024
        memory_free = memory_sum - memory_used
        # self._get_obj_bymoId(content, [vim.ClusterComputeResource], args["hc_moId"])
        return Cluster(
            resource_id=object_json._moId,
            resource_name=object_json.name,
            cloud_type=self.cloud_type,
            status=object_json.overallStatus,
            ds_num=len(object_json.datastore),
            vm_num=vm_num,
            net_num=len(object_json.network),
            ds_sum="%.2f" % (float(ds_sum) / 1024 / 1024 / 1024),
            ds_usage="%.2f" % (float(ds_used) / 1024 / 1024 / 1024),
            ds_free="%.2f" % (float(ds_free) / 1024 / 1024 / 1024),
            cpu_sum="%.2f" % (float(cpu_sum) / 1000),
            cpu_usage="%.2f" % (float(cpu_used) / 1000),
            cpu_free="%.2f" % (float(cpu_free) / 1000),
            memory_sum="%.2f" % (float(memory_sum) / 1024),
            memory_usage="%.2f" % (float(memory_used) / 1024),
            memory_free="%.2f" % (float(memory_free) / 1000),
        ).to_dict()

    def format_host(self, object_json, **kwargs):
        h = object_json["h"]
        c = object_json["c"]

        if not h:
            return None
        zone_obj = h.parent
        region_obj = zone_obj.parent.parent

        host_id = h._moId
        vm_num = 0
        run_vm_num = 0
        for v in h.vm:
            try:
                if not v.config.template:
                    try:
                        if v.runtime.powerState == "poweredOn":
                            run_vm_num += 1
                    except Exception:
                        pass
                    vm_num += 1
            except Exception:
                logger.error("format_host——not found attribute template: {}".format(v.name))
        # 存储情况
        ds_list = h.datastore
        ds_sum = 0
        ds_free = 0
        for i in ds_list:
            ds_sum += i.summary.capacity
            ds_free += i.summary.freeSpace
        # CPU、内存情况
        cpu_used = 0 if not h.summary.quickStats.overallCpuUsage else h.summary.quickStats.overallCpuUsage
        memory_used = 0 if not h.summary.quickStats.overallMemoryUsage else h.summary.quickStats.overallMemoryUsage
        ds_used = ds_sum - ds_free
        cpu_sum = h.summary.hardware.cpuMhz * h.summary.hardware.numCpuCores
        cpu_free = cpu_sum - cpu_used
        memory_sum = h.summary.hardware.memorySize / 1024 / 1024
        memory_free = memory_sum - memory_used

        return HostMachine(
            resource_id=host_id,
            resource_name=h.name,
            cloud_type=self.cloud_type,
            status=h.overallStatus,
            connect_status=h.runtime.connectionState,
            power_status=h.runtime.powerState,
            running_instances=run_vm_num,
            total_instances=vm_num,
            cpu="%.2f" % (float(cpu_sum) / 1000),
            memory="%.2f" % (float(memory_sum) / 1024),
            local_storage="%.2f" % (float(ds_sum) / 1024 / 1024 / 1024),
            cpu_usage="%.2f" % (float(cpu_used) / 1000),
            memory_usage="%.2f" % (float(memory_used) / 1024),
            local_storage_usage="%.2f" % (float(ds_used) / 1024 / 1024 / 1024),
            cpu_free="%.2f" % (float(cpu_free) / 1000),
            memory_free="%.2f" % (float(memory_free) / 1000),
            local_storage_free="%.2f" % (float(ds_free) / 1024 / 1024 / 1024),
            cluster_id=c._moId,
            zone=zone_obj._moId,
            region=region_obj._moId,
        ).to_dict()

    def format_private_storage(self, object_json, **kwargs):
        if not object_json:
            return None

        allocated_capacity = (
            (object_json.summary.capacity - object_json.summary.freeSpace + (object_json.summary.uncommitted or 0))
            / 1024
            / 1024
            / 1024
        )

        return PrivateStorage(
            status="AVAILABLE" if object_json.overallStatus else "ERROR",
            resource_id=object_json._moId,
            resource_name=object_json.name,
            cloud_type=self.cloud_type,
            capacity=round(object_json.summary.capacity / 1024 / 1024 / 1024, 2),
            used_capacity=round((object_json.summary.capacity - object_json.summary.freeSpace) / 1024 / 1024 / 1024, 2),
            allocated_capacity=round(allocated_capacity, 2),
            host_id=",".join([cur_host.key._moId for cur_host in object_json.host]),
            host_name=",".join([cur_host.key.name for cur_host in object_json.host]),
        ).to_dict()

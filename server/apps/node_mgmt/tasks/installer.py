from celery import shared_task

from apps.core.exceptions.base_app_exception import BaseAppException
from apps.node_mgmt.constants import CONTROLLER_INSTALL_DIR, COLLECTOR_INSTALL_DIR, LINUX_OS, \
    CONTROLLER_DIR_DELETE_COMMAND, NODE_SERVER_URL_KEY
from apps.node_mgmt.models import ControllerTask, CollectorTask, PackageVersion, Node, NodeCollectorInstallStatus, \
    Collector, SidecarEnv
from apps.node_mgmt.utils.installer import exec_command_to_remote, download_to_local, \
    exec_command_to_local, get_install_command, get_uninstall_command, unzip_file, transfer_file_to_remote
from apps.node_mgmt.utils.token_auth import generate_token
from config.components.nats import NATS_NAMESPACE


@shared_task
def install_controller(task_id):
    """安装控制器"""
    task_obj = ControllerTask.objects.filter(id=task_id).first()
    if not task_obj:
        raise BaseAppException("Task not found")
    package_obj = PackageVersion.objects.filter(id=task_obj.package_version_id).first()
    if not package_obj:
        raise BaseAppException("Package version not found")
    file_key = f"{package_obj.os}/{package_obj.object}/{package_obj.version}/{package_obj.name}"
    task_obj.status = "running"
    task_obj.save()

    # 获取所有节点
    nodes = task_obj.controllertasknode_set.all()

    # 获取控制器下发目录
    dir_map = CONTROLLER_INSTALL_DIR.get(package_obj.os)
    controller_install_dir, controller_storage_dir = dir_map["install_dir"], dir_map["storage_dir"]

    # 获取安装命令所需参数
    sidecar_token = generate_token({"username": "admin"})
    obj = SidecarEnv.objects.filter(cloud_region=task_obj.cloud_region_id, key=NODE_SERVER_URL_KEY).first()
    server_url = obj.value if obj else "null"

    base_action, base_massage, unzip_name, base_run = "", "", "", True

    try:
        base_action = "download"
        download_to_local(
            task_obj.work_node,
            NATS_NAMESPACE,
            file_key,
            package_obj.name,
            controller_storage_dir,
        )

        base_action = "unzip"
        resp = unzip_file(
            task_obj.work_node,
            f"{controller_storage_dir}/{package_obj.name}",
            controller_storage_dir,
        )
        unzip_name = resp
    except Exception as e:
        base_run = False
        base_massage = str(e)

    for node_obj in nodes:

        if not base_run:
            node_obj.status = "error"
            node_obj.result = {"action": base_action, "message": base_massage}
            node_obj.save()
            continue

        action, message = "", ""
        try:
            action = "send"
            transfer_file_to_remote(
                task_obj.work_node,
                f"{controller_storage_dir}/{unzip_name}",
                controller_install_dir,
                node_obj.ip,
                node_obj.username,
                node_obj.password,
                node_obj.port,
            )

            action = "run"
            groups = ",".join([str(i) for i in node_obj.organizations])
            install_command = get_install_command(
                package_obj.os, package_obj.name, task_obj.cloud_region_id,sidecar_token, server_url, groups, node_obj.node_name)
            exec_command_to_remote(task_obj.work_node, node_obj.ip, node_obj.username, node_obj.password, install_command, node_obj.port)
            node_obj.status = "success"
        except Exception as e:
            message = str(e)
            node_obj.status = "error"

        node_obj.result = {"action": action, "message": message}
        node_obj.save()

    # 更新任务状态
    task_obj.status = "finished"
    task_obj.save()


@shared_task
def uninstall_controller(task_id):
    """卸载控制器"""
    task_obj = ControllerTask.objects.filter(id=task_id).first()
    if not task_obj:
        return
    task_obj.status = "running"
    task_obj.save()

    # 获取所有节点
    nodes = task_obj.controllertasknode_set.all()
    for node_obj in nodes:
        action, message = "", ""
        try:
            action = "stop_run"
            # 获取卸载命令
            uninstall_command = get_uninstall_command(node_obj.os)
            # 执行卸载脚步
            exec_command_to_remote(task_obj.work_node, node_obj.ip, node_obj.username, node_obj.password, uninstall_command, node_obj.port)
            # 删除控制器安装目录
            action = "delete_dir"
            exec_command_to_remote(
                task_obj.work_node,
                node_obj.ip,
                node_obj.username,
                node_obj.password,
                CONTROLLER_DIR_DELETE_COMMAND.get(node_obj.os),
                node_obj.port,
            )
            # 删除node实例
            action = "delete_node"
            Node.objects.filter(cloud_region_id=task_obj.cloud_region_id, ip=node_obj.ip).delete()
            node_obj.status = "success"

        except Exception as e:
            message = str(e)
            node_obj.status = "error"

        node_obj.result = {"action": action, "message": message}
        node_obj.save()

    # 更新任务状态
    task_obj.status = "finished"
    task_obj.save()


@shared_task
def install_collector(task_id):
    """安装采集器"""
    task_obj = CollectorTask.objects.filter(id=task_id).first()
    if not task_obj:
        raise BaseAppException("Task not found")
    package_obj = PackageVersion.objects.filter(id=task_obj.package_version_id).first()
    if not package_obj:
        raise BaseAppException("Package version not found")
    file_key = f"{package_obj.os}/{package_obj.object}/{package_obj.version}/{package_obj.name}"
    task_obj.status = "running"
    task_obj.save()

    # 获取采集器下发目录
    collector_install_dir = COLLECTOR_INSTALL_DIR.get(package_obj.os)

    # 获取所有节点
    nodes = task_obj.collectortasknode_set.all()
    for node_obj in nodes:
        action, message = "", ""
        try:
            # 下发采集器
            action = "send"
            download_to_local(
                node_obj.node_id,
                NATS_NAMESPACE,
                file_key,
                package_obj.name,
                collector_install_dir,
            )
            # Linux操作系统赋予执行权限
            if package_obj.os in LINUX_OS:
                action = "set_exe"
                exec_command_to_local(node_obj.node_id, f"chmod +x {collector_install_dir}/{package_obj.name}")
            node_obj.status = "success"
        except Exception as e:
            message = str(e)
            node_obj.status = "error"

        result = {"action": action, "message": message}
        collector_obj = Collector.objects.filter(node_operating_system=package_obj.os, name=package_obj.object).first()
        NodeCollectorInstallStatus.objects.update_or_create(
            node_id=node_obj.node_id,
            collector_id=collector_obj.id,
            defaults={
                "node_id": node_obj.node_id,
                "collector_id": collector_obj.id,
                "status": node_obj.status,
                "result": result,
            },
        )

        node_obj.result = result
        node_obj.save()

    # 更新任务状态
    task_obj.status = "finished"
    task_obj.save()


@shared_task
def uninstall_collector(task_id):
    """卸载采集器"""
    pass

import uuid

import pytest
from django.core.cache import cache
from django.test.utils import override_settings

from apps.node_mgmt.constants.node import NodeConstants
from apps.node_mgmt.models.cloud_region import CloudRegion
from apps.node_mgmt.models.installer import (
    CollectorTask,
    CollectorTaskNode,
    ControllerTask,
)
from apps.node_mgmt.models.package import PackageVersion
from apps.node_mgmt.models.sidecar import Collector, Node
from apps.node_mgmt.services.installer import InstallerService
from apps.node_mgmt.tasks.installer import install_collector


@pytest.mark.django_db
def test_install_controller_forces_default_work_node():
    cloud = CloudRegion.objects.create(name="default", introduction="default cloud region!")
    nodes = [
        {
            "ip": "10.0.0.1",
            "node_name": "test-node",
            "os": NodeConstants.LINUX_OS,
            "organizations": [],
            "port": 22,
            "username": "root",
            "password": "passw0rd",
        }
    ]

    task_id = InstallerService.install_controller(cloud.id, "管理网", 1, nodes)
    task = ControllerTask.objects.get(id=task_id)

    assert task.work_node == NodeConstants.DEFAULT_WORK_NODE


@pytest.mark.django_db
def test_uninstall_controller_forces_default_work_node():
    cloud = CloudRegion.objects.create(name="default-2", introduction="other cloud region")

    task_id = InstallerService.uninstall_controller(cloud.id, "业务网", [])
    task = ControllerTask.objects.get(id=task_id)

    assert task.work_node == NodeConstants.DEFAULT_WORK_NODE


@pytest.mark.django_db
@override_settings(CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}})
def test_install_collector_targets_node_executor(monkeypatch):
    cache.clear()

    cloud = CloudRegion.objects.create(name="collector-region", introduction="region")
    node = Node.objects.create(
        id=uuid.uuid4().hex,
        name="node-a",
        ip="10.0.0.2",
        operating_system=NodeConstants.LINUX_OS,
        collector_configuration_directory="/etc/collectors",
        cloud_region=cloud,
    )
    package = PackageVersion.objects.create(
        type="collector",
        os=NodeConstants.LINUX_OS,
        object="fusion-collector",
        version="1.0.0",
        name="fusion.zip",
    )
    Collector.objects.create(
        id="collector-1",
        name=package.object,
        service_type="exec",
        node_operating_system=NodeConstants.LINUX_OS,
        executable_path="/opt/fusion",
        execute_parameters="",
        introduction="",
    )
    task = CollectorTask.objects.create(type="install", package_version_id=package.id, status="waiting")
    CollectorTaskNode.objects.create(task=task, node=node, status="waiting")

    calls = {"download": None, "unzip": None, "chmod": None}

    def fake_download(instance_id, *_args, **_kwargs):
        calls["download"] = instance_id

    def fake_unzip(instance_id, *_args, **_kwargs):
        calls["unzip"] = instance_id
        return "fusion"

    def fake_exec(instance_id, *_args, **_kwargs):
        calls["chmod"] = instance_id

    monkeypatch.setattr("apps.node_mgmt.tasks.installer.download_to_local", fake_download)
    monkeypatch.setattr("apps.node_mgmt.tasks.installer.unzip_file", fake_unzip)
    monkeypatch.setattr("apps.node_mgmt.tasks.installer.exec_command_to_local", fake_exec)

    install_collector(task.id)

    assert calls["download"] == node.id
    assert calls["unzip"] == node.id
    assert calls["chmod"] == node.id

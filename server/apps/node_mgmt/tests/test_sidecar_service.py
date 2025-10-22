import pytest
from django.test import RequestFactory
from django.test.utils import override_settings

from apps.core.utils.crypto.aes_crypto import AESCryptor
from apps.node_mgmt.models.cloud_region import CloudRegion, SidecarEnv
from apps.node_mgmt.models.sidecar import CollectorConfiguration, Collector, Node
from apps.node_mgmt.services.sidecar import Sidecar


@pytest.mark.django_db
@override_settings(CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}})
def test_sidecar_configuration_renders_secret_values():
    cloud = CloudRegion.objects.create(id=1, name="default", introduction="")
    SidecarEnv.objects.create(
        key="NATS_PASSWORD",
        value=AESCryptor().encode("secret-pass"),
        type="secret",
        cloud_region=cloud,
        is_pre=True,
    )
    SidecarEnv.objects.create(
        key="NATS_USERNAME",
        value="admin",
        cloud_region=cloud,
        is_pre=True,
    )
    SidecarEnv.objects.create(
        key="NATS_SERVERS",
        value="127.0.0.1:4222",
        cloud_region=cloud,
        is_pre=True,
    )
    Collector.objects.create(
        id="natsexecutor_linux",
        name="natsexecutor",
        service_type="exec",
        node_operating_system="linux",
        executable_path="/opt/fusion-collectors/bin/nats-executor",
        execute_parameters="",
        validation_parameters="",
        default_template="",
        introduction="",
        icon="",
        controller_default_run=False,
        enabled_default_config=False,
        default_config={},
    )
    node = Node.objects.create(
        id="node-123",
        name="node",
        ip="10.0.0.2",
        operating_system="linux",
        collector_configuration_directory="/opt/collector",
        cloud_region=cloud,
    )
    configuration = CollectorConfiguration.objects.create(
        id="config-1",
        name="natsexecutor",
        config_template='nats: "tls://${NATS_USERNAME}:${NATS_PASSWORD}@${NATS_SERVERS}"',
        collector_id="natsexecutor_linux",
        cloud_region=cloud,
    )

    request = RequestFactory().get("/")
    response = Sidecar.get_node_config(request, node.id, configuration.id)

    payload = response.content.decode()
    assert "secret-pass" in payload
    assert "${NATS_PASSWORD}" not in payload

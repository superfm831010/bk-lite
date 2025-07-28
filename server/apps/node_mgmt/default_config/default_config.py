import os
from apps.core.logger import node_logger as logger
from apps.node_mgmt.models import Collector, CollectorConfiguration


def create_default_config(node):

        collector_objs = Collector.objects.filter(enabled_default_config=True, node_operating_system=node.operating_system)

        # todo 云区域环境变量
        default_sidecar_mode = os.getenv("SIDECAR_INPUT_MODE", "nats")

        for collector_obj in collector_objs:
            try:

                if not collector_obj.default_config:
                    continue

                config_template = collector_obj.default_config.get(default_sidecar_mode, None)

                if not config_template:
                    continue

                # 如果已经存在关联的配置就跳过
                if CollectorConfiguration.objects.filter(collector=collector_obj, nodes=node).exists():
                    logger.info(f"Node {node.id} already has a configuration for collector {collector_obj.name}, skipping.")
                    continue

                configuration = CollectorConfiguration.objects.create(
                    name=f'{collector_obj.name}-{node.id}',
                    collector=collector_obj,
                    config_template=config_template,
                    is_pre=True,
                )
                configuration.nodes.add(node)

            except Exception as e:
                logger.error(f"create node {node.id} {collector_obj.name} default configuration failed {e}")

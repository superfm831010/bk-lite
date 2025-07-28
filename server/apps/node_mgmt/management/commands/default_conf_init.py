from apps.node_mgmt.models.sidecar import Node
from apps.node_mgmt.default_config.default_config import create_default_config
from django.core.management import BaseCommand
from apps.core.logger import node_logger as logger


class Command(BaseCommand):
    help = "节点默认配置初始化"

    def handle(self, *args, **options):
        logger.info("开始初始化节点默认配置...")
        nodes = Node.objects.all()
        for node in nodes:
            try:
                create_default_config(node)
            except Exception as e:
                logger.error(f"初始化节点 {node.id} 默认配置失败: {e}")
        logger.info("节点默认配置初始化完成！")
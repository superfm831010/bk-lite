import logging

from django.core.management import BaseCommand

from apps.playground.models import PlayGroundCategory
from apps.playground.init_constant import CATEGORY_INIT_DATA
class Command(BaseCommand):
    help = "初始化分类"

    def handle(self, *args, **options):
        logging.info("开始初始化分类")
        try:
            for item in CATEGORY_INIT_DATA:
                obj,created = PlayGroundCategory.objects.get_or_create(
                    name=item["name"],
                    description=item["description"],
                    parent=item["parent"],
                    created_by=item["created_by"],
                    updated_by = item["updated_by"]
                )
                if created:
                    logging.info(f"初始化分类成功: {item['name']}")
                else:
                    logging.info(f"分类已存在: {item['name']}")
        except Exception as e:
            logging.error(f"初始化分类失败: {e}")

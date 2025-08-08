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
                if not item["name"] or "name" not in item:
                    logging.error("分类名称不能为空")
                    continue
                else:
                    _, created = PlayGroundCategory.objects.get_or_create(
                        name=item["name"],
                        description=item.get("description", None),
                        parent=item.get("parent", None),
                        created_by=item.get("created_by","system"),
                        updated_by=item.get("updated_by","system")
                    )
                    if created:
                        logging.info(f"初始化分类成功: {item['name']}")
                    else:
                        logging.info(f"分类已存在: {item['name']}")
        except Exception as e:
            logging.error(f"初始化分类失败: {e}")

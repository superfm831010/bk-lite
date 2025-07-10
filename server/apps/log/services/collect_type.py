from apps.core.exceptions.base_app_exception import BaseAppException
from apps.log.models import CollectInstance, CollectInstanceOrganization
from apps.log.plugins.controller import Controller


class CollectTypeService:
    @staticmethod
    def get_collect_type(collect_type: str) -> str:
        """
        Get the collect type based on the provided string.

        Args:
            collect_type (str): The type of collection.

        Returns:
            str: The corresponding collect type.
        """
        return collect_type.lower() if collect_type else "unknown"

    @staticmethod
    def batch_create_collect_configs(data: dict) -> list:
        """
        Batch create collect configurations based on the provided data.

        Args:
            data (dict): The data containing collector, collect_type, configs, and instances.

        Returns:
            list: A list of created collect configurations.
        """

        # 过滤已存在的实例
        objs = CollectInstance.objects.filter(id__in=[instance["instance_id"] for instance in data["instances"]])
        instance_set = {obj.id for obj in objs}

        # 格式化实例id,将实例id统一为字符串元祖（支持多维度组成的实例id）
        new_instances, old_instances = [], []
        for instance in data["instances"]:
            if instance["instance_id"] in instance_set:
                old_instances.append(instance)
            else:
                new_instances.append(instance)

        data["instances"] = new_instances

        # 实例更新
        instance_map = {
            instance["instance_id"]: {
                "id": instance["instance_id"],
                "name": instance["instance_name"],
                "collect_type_id": data["collect_type_id"],
                "group_ids": instance["group_ids"],
            }
            for instance in data["instances"]
        }

        creates, assos = [], []
        for instance_id, instance_info in instance_map.items():
            group_ids = instance_info.pop("group_ids")
            for group_id in group_ids:
                assos.append((instance_id, group_id))
            creates.append(CollectInstance(**instance_info))

        CollectInstance.objects.bulk_create(creates, batch_size=200)

        CollectInstanceOrganization.objects.bulk_create(
            [CollectInstanceOrganization(collect_instance_id=asso[0], organization=asso[1]) for asso in assos],
            batch_size=200
        )

        # 实例配置
        Controller(data).controller()

        if old_instances:
            raise BaseAppException(
                f"以下实例已存在：{'、'.join([instance['instance_name'] for instance in old_instances])}")
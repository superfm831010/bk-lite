from collections import defaultdict

import toml
import yaml
from django.db import transaction

from apps.core.exceptions.base_app_exception import BaseAppException
from apps.log.models import CollectInstance, CollectInstanceOrganization, CollectConfig, CollectType, \
    StreamCollectInstance
from apps.log.plugins.controller import Controller
from apps.rpc.node_mgmt import NodeMgmt


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
                "node_id": instance["node_ids"][0],
                "group_ids": instance["group_ids"],
                "stream_ids": instance.get("stream_ids", []),
            }
            for instance in data["instances"]
        }

        creates, assos, streams_assos = [], [], []
        for instance_id, instance_info in instance_map.items():
            group_ids = instance_info.pop("group_ids")
            streams = instance_info.pop("stream_ids", [])
            if not streams:
                raise BaseAppException("streams is required for collect instance")
            for group_id in group_ids:
                assos.append((instance_id, group_id))
            for stream in streams:
                streams_assos.append((instance_id, stream))
            creates.append(CollectInstance(**instance_info))

        CollectInstance.objects.bulk_create(creates, batch_size=200)

        if assos:
            CollectInstanceOrganization.objects.bulk_create(
                [CollectInstanceOrganization(collect_instance_id=asso[0], organization=asso[1]) for asso in assos],
                batch_size=200
            )
        if streams_assos:
            StreamCollectInstance.objects.bulk_create(
                [StreamCollectInstance(stream_id=stream_asso[1], collect_instance_id=stream_asso[0]) for stream_asso in streams_assos],
                batch_size=200, ignore_conflicts=True
            )

        # 实例配置
        Controller(data).controller()

        if old_instances:
            raise BaseAppException(
                f"以下实例已存在：{'、'.join([instance['instance_name'] for instance in old_instances])}")

    @staticmethod
    def set_instances_organizations(instance_ids, organizations):
        """设置监控对象实例组织"""
        if not instance_ids or not organizations:
            return

        with transaction.atomic():
            # 删除旧的组织关联
            CollectInstanceOrganization.objects.filter(
                collect_instance_id__in=instance_ids
            ).delete()

            # 添加新的组织关联
            creates = []
            for instance_id in instance_ids:
                for org in organizations:
                    creates.append(CollectInstanceOrganization(
                        collect_instance_id=instance_id,
                        organization=org
                    ))
            CollectInstanceOrganization.objects.bulk_create(creates, ignore_conflicts=True)

    @staticmethod
    def update_instance_config(child_info, base_info):

        child_env = None

        if base_info:
            config_obj = CollectConfig.objects.filter(id=base_info["id"]).first()
            if config_obj:
                content = yaml.dump(base_info["content"], default_flow_style=False)
                env_config = base_info.get("env_config")
                if env_config:
                    child_env = {k: v for k, v in env_config.items()}
                NodeMgmt().update_config_content(base_info["id"], content, env_config)

        if child_info or child_env:
            config_obj = CollectConfig.objects.filter(id=child_info["id"]).first()
            if not config_obj:
                return
            content = toml.dumps(child_info["content"]) if child_info else None
            NodeMgmt().update_child_config_content(child_info["id"], content, child_env)

    @staticmethod
    def update_instance_config_v2(child_info, base_info, instance_id, collect_type_id, stream_ids):
        """ 更新对象实例配置 """
        child_env = None
        collect_type_obj = CollectType.objects.filter(id=collect_type_id).first()
        if not collect_type_obj:
            raise BaseAppException("collect_type does not exist")

        # 更新实例数据流
        if not stream_ids:
            raise BaseAppException("streams is required for collect instance")

        StreamCollectInstance.objects.filter(collect_instance_id=instance_id).delete()
        StreamCollectInstance.objects.bulk_create(
            [StreamCollectInstance(stream_id=stream_id, collect_instance_id=instance_id) for stream_id in stream_ids],
            ignore_conflicts=True
        )

        col_obj = Controller(
            {
                "collector": collect_type_obj.collector,
                "collect_type": collect_type_obj.name,
                "collect_type_id": collect_type_id,
                "instances": [{"instance_id": instance_id}],
            }
        )

        if base_info:
            config_obj = CollectConfig.objects.filter(id=base_info["id"]).first()
            if config_obj:
                content = col_obj.render_config_template_content("base", base_info["content_data"], instance_id)
                env_config = base_info.get("env_config")
                if env_config:
                    child_env = {k: v for k, v in env_config.items()}
                NodeMgmt().update_config_content(base_info["id"], content, env_config)

        if child_info or child_env:
            config_obj = CollectConfig.objects.filter(id=child_info["id"]).first()
            if not config_obj:
                return
            content = col_obj.render_config_template_content("child", child_info["content_data"], instance_id)
            NodeMgmt().update_child_config_content(child_info["id"], content, child_env)

    @staticmethod
    def update_instance(instance_id, name, organizations):
        """更新监控对象实例"""
        instance = CollectInstance.objects.filter(id=instance_id).first()
        if not instance:
            raise BaseAppException("collect instance does not exist")
        if name:
            instance.name = name
            instance.save()

        # 更新组织信息
        instance.collectinstanceorganization_set.all().delete()
        for org in organizations:
            instance.collectinstanceorganization_set.create(organization=org)

    @staticmethod
    def search_instance(collect_type_id, name, page, page_size):
        queryset = CollectInstance.objects.select_related("collect_type")
        if collect_type_id:
            queryset = queryset.filter(collect_type_id=collect_type_id)
        if name:
            queryset = queryset.filter(name__icontains=name)

        # 计算总数
        total_count = queryset.count()
        # 计算分页
        start = (page - 1) * page_size
        end = page * page_size
        # 获取当前页的数据
        data_list = queryset.values("id", "name", "node_id", "collect_type_id", "collect_type__name", "collect_type__collector")[start:end]

        instance_ids = [item["id"] for item in data_list]

        # 补充组织与配置
        org_map = defaultdict(list)
        org_objs = CollectInstanceOrganization.objects.filter(
            collect_instance_id__in=instance_ids
        ).values_list("collect_instance_id", "organization")
        for instance_id, organization in org_objs:
            org_map[instance_id].append(organization)

        conf_map = defaultdict(list)
        conf_objs = CollectConfig.objects.filter(
            collect_instance_id__in=instance_ids
        ).values_list("collect_instance", "id")
        for instance_id, config_id in conf_objs:
            conf_map[instance_id].append(config_id)

        nodes = NodeMgmt().node_list(dict(page_size=-1))
        node_map = {node["id"]: node["name"] for node in nodes["nodes"]}

        assos = StreamCollectInstance.objects.filter(collect_instance_id__in=instance_ids)
        stream_map = {}
        for asso in assos:
            if asso.collect_instance_id not in stream_map:
                stream_map[asso.collect_instance_id] = set()
            stream_map[asso.collect_instance_id].add(asso.stream_id)

        items = []
        for info in data_list:
            info.update(
                organization=org_map.get(info["id"]),
                config_id=conf_map.get(info["id"]),
                node_name=node_map.get(info["node_id"], ""),
                stream_ids=list(stream_map.get(info["id"], [])),
            )
            items.append(info)

        data = {"count": total_count, "items": items}

        return data
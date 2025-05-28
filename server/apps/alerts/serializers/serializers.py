# -- coding: utf-8 --
# @File: serializers.py
# @Time: 2025/5/14 16:22
# @Author: windyzhao
from django.utils import timezone
from rest_framework import serializers

from apps.alerts.models import AlertSource, Alert


class AlertSourceModelSerializer(serializers.ModelSerializer):
    """
    Serializer for AlertSource model.
    """

    class Meta:
        model = AlertSource
        fields = "__all__"
        extra_kwargs = {
            # "secret": {"write_only": True},
            # "config": {"write_only": True},
            "last_active_time": {"write_only": True},
            "is_delete": {"write_only": True},
        }


class AlertModelSerializer(serializers.ModelSerializer):
    """
    Serializer for Alert model.
    """
    event_count = serializers.SerializerMethodField()
    source_names = serializers.SerializerMethodField()
    # 持续时间
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Alert
        fields = "__all__"
        extra_kwargs = {
            "raw_data": {"write_only": True},
            "is_delete": {"write_only": True},
            "source": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    @staticmethod
    def get_duration(obj):
        """
        当前时间- 创建时间
        """
        """
            当前时间- 创建时间
            """
        if not obj.created_at:
            return "0s"

        # 计算持续时间
        now = timezone.now()
        duration = now - obj.created_at
        total_seconds = int(duration.total_seconds())

        # 计算各个时间单位
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        # 构建格式化字符串
        result = ""
        if days > 0:
            result += f"{days}d"
        if hours > 0:
            result += f"{hours}h"
        if minutes > 0:
            result += f"{minutes}m"
        if seconds > 0 or result == "":  # 如果没有其他时间单位，至少显示秒
            result += f"{seconds}s"

        return result

    @staticmethod
    def get_source_names(obj):
        """
        Get the names of the sources associated with the alert.
        """
        # 如果使用了注解
        if hasattr(obj, 'source_names_annotated'):
            return obj.source_names_annotated or ""
        # fallback
        return ", ".join(source.name for source in obj.source.all())

    @staticmethod
    def get_event_count(obj):
        """
        Get the count of events associated with the alert.
        """
        # 如果使用了注解
        if hasattr(obj, 'event_count_annotated'):
            return obj.event_count_annotated
        # fallback
        return len(obj.event_set.all())

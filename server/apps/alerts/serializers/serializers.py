# -- coding: utf-8 --
# @File: serializers.py
# @Time: 2025/5/14 16:22
# @Author: windyzhao
from django.utils import timezone
from rest_framework import serializers

from apps.alerts.constants import AlertStatus
from apps.alerts.models import AlertSource, Alert, Event, Level, AlertAssignment, AlertShield


class AlertSourceModelSerializer(serializers.ModelSerializer):
    """
    Serializer for AlertSource model.
    """
    event_count = serializers.SerializerMethodField()
    last_event_time = serializers.SerializerMethodField()

    class Meta:
        model = AlertSource
        fields = "__all__"
        extra_kwargs = {
            # "secret": {"write_only": True},
            # "config": {"write_only": True},
            "last_active_time": {"write_only": True},
            "is_delete": {"write_only": True},
        }

    @staticmethod
    def get_event_count(obj):
        return obj.event_set.count()

    @staticmethod
    def get_last_event_time(obj):
        """
        获取最近一次事件时间
        """
        format_time = "%Y-%m-%d %H:%M:%S"
        last_event = obj.event_set.order_by('-received_at').first()
        if not last_event or not last_event.received_at:
            return ""
        # 如果需要格式化时间，可以在这里进行
        return last_event.received_at.strftime(format_time)


class EventModelSerializer(serializers.ModelSerializer):
    """
    Serializer for Event model.
    """

    # 格式化时间字段
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    source_name = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'
        extra_kwargs = {
            # "events": {"write_only": True},  # events 字段只读
            "start_time": {"read_only": True},
            "end_time": {"read_only": True},
            "labels": {"write_only": True},
            # "raw_data": {"write_only": True},
            "search_vector": {"write_only": True},
            # "labels": {"write_only": True},
        }

    @staticmethod
    def get_source_name(obj):
        """
        Get the names of the sources associated with the alert.
        通过 Alert -> Events -> AlertSource 获取告警源名称
        """
        # 如果使用了注解（推荐）
        return obj.source.name


class AlertModelSerializer(serializers.ModelSerializer):
    """
    Serializer for Alert model.
    """
    event_count = serializers.SerializerMethodField()
    source_names = serializers.SerializerMethodField()
    # 持续时间
    duration = serializers.SerializerMethodField()
    operator_user = serializers.SerializerMethodField()

    # 格式化时间字段
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    first_event_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    last_event_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Alert
        exclude = ["events"]
        extra_kwargs = {
            # "events": {"write_only": True},  # events 字段只读
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "operator": {"write_only": True},
            "search_vector": {"write_only": True},
            "labels": {"write_only": True},
        }

    @staticmethod
    def get_duration(obj):
        """
        当前时间- 创建时间
        """
        if not obj.created_at or obj.status not in AlertStatus.ACTIVATE_STATUS:
            return "--"

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
            result += f"{days}d "
        if hours > 0:
            result += f"{hours}h "
        if minutes > 0:
            result += f"{minutes}m "
        if seconds > 0 or result == "":
            result += f"{seconds}s"

        return result

    @staticmethod
    def get_source_names(obj):
        """
        Get the names of the sources associated with the alert.
        通过 Alert -> Events -> AlertSource 获取告警源名称
        """
        # 如果使用了注解（推荐）
        if hasattr(obj, 'source_names_annotated') and obj.source_names_annotated:
            return obj.source_names_annotated

        # fallback: 通过关联查询获取
        try:
            # Alert -> Events -> AlertSource
            source_names = set()  # 使用set去重
            for event in obj.events.all():
                if event.source:
                    source_names.add(event.source.name)
            return ", ".join(sorted(source_names))
        except Exception:
            return ""

    @staticmethod
    def get_event_count(obj):
        """
        Get the count of events associated with the alert.
        """
        # 如果使用了注解（推荐）
        if hasattr(obj, 'event_count_annotated'):
            return obj.event_count_annotated

        # fallback: 直接计数
        try:
            return obj.events.count()
        except Exception:
            return 0

    @staticmethod
    def get_operator_user(obj):
        if not obj.operator:
            return ""
        return ", ".join(obj.operator)


class LevelModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class AlertAssignmentModelSerializer(serializers.ModelSerializer):
    """
    Serializer for AlertAssignment model.
    This serializer is used to assign alerts to users or teams.
    """

    class Meta:
        model = AlertAssignment
        fields = "__all__"
        extra_kwargs = {
            # 'alert_id': {'read_only': True},
            # 'status': {'required': True},
            # 'operator': {'required': True},
        }


class AlertShieldModelSerializer(serializers.ModelSerializer):
    """
    Serializer for AlertAssignment model.
    This serializer is used to assign alerts to users or teams.
    """

    class Meta:
        model = AlertShield
        fields = "__all__"
        extra_kwargs = {
            # 'alert_id': {'read_only': True},
            # 'status': {'required': True},
            # 'operator': {'required': True},
        }

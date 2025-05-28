# -- coding: utf-8 --
# @File: filters.py
# @Time: 2025/5/9 15:06
# @Author: windyzhao
from django_filters import FilterSet, CharFilter
from apps.alerts.models import AlertSource, Alert


class AlertSourceModelFilter(FilterSet):
    # inst_id = NumberFilter(field_name="inst_id", lookup_expr="exact", label="实例ID")
    search = CharFilter(field_name="name", lookup_expr="icontains", label="名称")

    class Meta:
        model = AlertSource
        fields = ["search"]


class AlertModelFilter(FilterSet):
    """
    exact	精确匹配（默认值）	alert_id=123 → 只匹配 alert_id 为 "123" 的记录
    icontains	包含匹配（不区分大小写）	name="test" → 匹配包含 "test" 的所有记录
    contains	包含匹配（区分大小写）	同上，但区分大小写
    startswith	以...开头	匹配以指定字符串开头的记录
    endswith	以...结尾	匹配以指定字符串结尾的记录
    gt	大于	数值比较
    lt	小于	数值比较
    in	在列表中	匹配列表中的任意值
    """
    # inst_id = NumberFilter(field_name="inst_id", lookup_expr="exact", label="实例ID")
    title = CharFilter(field_name="title", lookup_expr="icontains", label="名称")
    content = CharFilter(field_name="content", lookup_expr="icontains", label="内容")
    alert_id = CharFilter(field_name="alert_id", lookup_expr="exact", label="告警ID")

    class Meta:
        model = Alert
        fields = ["search"]

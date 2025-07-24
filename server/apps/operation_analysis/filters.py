# -- coding: utf-8 --
# @File: filters.py
# @Time: 2025/7/14 16:02
# @Author: windyzhao

from django_filters import FilterSet, CharFilter

from apps.operation_analysis.models import DataSourceAPIModel, Dashboard


class DataSourceAPIModelFilter(FilterSet):
    search = CharFilter(field_name="name", lookup_expr="icontains", label="名称")

    class Meta:
        model = DataSourceAPIModel
        fields = ["search"]


class DashboardModelFilter(FilterSet):
    search = CharFilter(field_name="name", lookup_expr="icontains", label="名称")

    class Meta:
        model = Dashboard
        fields = ["search"]

# -- coding: utf-8 --
# @File: filters.py
# @Time: 2025/7/14 16:02
# @Author: windyzhao

from django_filters import FilterSet, CharFilter

from apps.operation_analysis.models import DataSourceAPIModel, Dashboard, Directory, Topology, NameSpace


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


class DirectoryModelFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains", label="名称")

    class Meta:
        model = Directory
        fields = ["name"]


class TopologyModelFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains", label="名称")

    class Meta:
        model = Topology
        fields = ["name"]


class NameSpaceModelFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains", label="名称")

    class Meta:
        model = NameSpace
        fields = ["name"]

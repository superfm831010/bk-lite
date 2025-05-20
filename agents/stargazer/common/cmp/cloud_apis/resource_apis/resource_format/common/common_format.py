# -*- coding: utf-8 -*-
# @Time : 2021-01-21 16:42
import threading

from common.cmp.cloud_apis.exceptions import RewriteException


class FormatResource:
    """格式化资源数据"""

    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """
        支持多线程的单例模式
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        """
        if not hasattr(FormatResource, "_instance"):
            with FormatResource._instance_lock:
                if not hasattr(FormatResource, "_instance"):
                    FormatResource._instance = object.__new__(cls)
        return FormatResource._instance

    def format_domain(self, object_json, **kwargs):
        """
        区域格式转换
        """
        raise RewriteException()

    def format_project(self, object_json, **kwargs):
        """
        区域格式转换
        """
        raise RewriteException()

    def format_region(self, object_json, **kwargs):
        """
        区域格式转换
        """
        raise RewriteException()

    def format_zone(self, object_json, **kwargs):
        """
        可用区格式转换
        """
        raise RewriteException()

    def format_instance_type_family(self, object_json, **kwargs):
        """
        规格族格式转换
        """
        raise RewriteException()

    def format_instance_type(self, object_json, **kwargs):
        """
        规格格式转换
        """
        raise RewriteException()

    def format_vm(self, object_json, **kwargs):
        """
        虚拟机格式转换
        """
        raise RewriteException()

    def format_disk(self, object_json, **kwargs):
        """
        磁盘格式转换
        """
        raise RewriteException()

    def format_snapshot(self, object_json, **kwargs):
        """
        快照格式转换
        """
        raise RewriteException()

    def format_image(self, object_json, **kwargs):
        """
        镜像格式转换
        """
        raise RewriteException()

    def format_vpc(self, object_json, **kwargs):
        """
        VPC格式转换
        """
        raise RewriteException()

    def format_subnet(self, object_json, **kwargs):
        """
        子网格式转换
        """
        raise RewriteException()

    def format_eip(self, object_json, **kwargs):
        """
        弹性公网IP格式转换
        """
        raise RewriteException()

    def format_security_group(self, object_json, **kwargs):
        """
        安全组格式转换
        """
        raise RewriteException()

    def format_security_group_rule(self, object_json, **kwargs):
        """
        安全组规则格式转换
        """
        raise RewriteException()

    def format_bucket(self, object_json, **kwargs):
        """
        存储桶格式转换
        """
        raise RewriteException()

# # -- coding: utf-8 --
# # @File: init_tag.py
# # @Time: 2025/9/3 15:27
# # @Author: windyzhao
#
#
# from django.core.management import BaseCommand
#
# from apps.operation_analysis.models import
# from apps.core.logger import operation_analysis_logger as logger
#
#
#
# class Command(BaseCommand):
#     help = "初始化源API数据"
#
#     def add_arguments(self, parser):
#         parser.add_argument(
#             '--force-update', '--update',
#             action='store_true',
#             dest='force_update',
#             help='强制更新已存在的数据源配置',
#         )
#
#     @staticmethod
#     def get_default_namespace():
#         """
#         获取默认命名空间名称
#         :return: 默认命名空间名称
#         """
#         instance = NameSpace.objects.filter(name="默认命名空间")
#         if instance.exists():
#             return instance.first().id
#         return
#
#     def handle(self, *args, **options):
#         logger.info("===开始初始化源API数据===")
#         force_update = options['force_update']
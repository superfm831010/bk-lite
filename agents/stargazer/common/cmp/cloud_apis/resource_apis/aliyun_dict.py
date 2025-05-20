# -*- coding: utf-8 -*-
"""阿里云各种枚举属性的映射字典 中英文对照"""
from common.cmp.cloud_apis.resource_apis.resource_format.aliyun.aliyun_constant import AliyunBucketType, AliyunDiskCategory

# 磁盘类型
disk_category_dict = {
    AliyunDiskCategory.CLOUD.value: "普通云盘",
    AliyunDiskCategory.CLOUD_ESSD.value: "ESSD云盘",
    AliyunDiskCategory.CLOUD_SSD.value: "SSD云盘",
    AliyunDiskCategory.CLOUD_EFFICIENCY.value: "高效云盘",
}

# 对象存储 中英文对照
object_storage_type_dict = {
    AliyunBucketType.STANDARD.value: "标准存储",
    AliyunBucketType.IA.value: "低频存储",
    AliyunBucketType.ARCHIVE.value: "归档存储",
    AliyunBucketType.COLD_ARCHIVE.value: "冷归档存储",
}

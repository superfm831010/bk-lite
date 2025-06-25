# -- coding: utf-8 --
# @File: agg_rules.py
# @Time: 2025/6/16 15:23
# @Author: windyzhao

LAYERED_GROUPING_STRATEGY = {
    "levels": [
        {
            "name": "full_metadata",
            "priority": 1,
            "required_fields": ["item", "resource_id", "resource_type", "source__name"],
            "optional_fields": ["level"],
        },
        {
            "name": "partial_metadata",
            "priority": 2,
            "required_fields": ["item"],  # 至少需要metric_name/item
            "optional_fields": ["resource_type", "source__name"],
        },
        {
            "name": "title_severity",
            "priority": 3,
            "required_fields": ["title", "level"],
            "optional_fields": [],
            "grouping_template": "{normalize_title(title)}-{level}"
        },
        {
            "name": "fallback",
            "priority": 4,
            "required_fields": [],
            "optional_fields": [],
            "grouping_template": "{raw_event_text[:100]}"
        }
    ],
    "title_normalization": {
        "remove_patterns": [
            r'\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}',  # 移除时间戳
            r'ID:\s*\w+',  # 移除ID信息
            r'\b\d+\.\d+\.\d+\.\d+\b',  # 移除IP地址
        ],
        "replace_patterns": [
            (r'\s+', ' '),  # 多个空格替换为单个
            (r'[^\w\s-]', ''),  # 移除特殊字符
        ]
    }
}

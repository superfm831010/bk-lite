#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试时间字段向后兼容性
"""


def test_sort_config():
    """测试排序配置的向后兼容性逻辑"""

    def create_sort_config(sort_field, sort_order):
        """模拟创建排序配置的逻辑"""
        sort_config = {sort_field: {"order": sort_order}}

        # 如果是时间字段排序，添加缺失值处理
        if 'created_time' in sort_field or 'updated_time' in sort_field:
            sort_config[sort_field]["missing"] = "_last" if sort_order == 'asc' else "_first"
            print(
                f"时间字段排序，添加兼容性处理: 缺失值放在{'最后' if sort_order == 'asc' else '最前'}")

        return sort_config

    # 测试不同的排序字段
    test_cases = [
        ("metadata.created_time", "desc"),
        ("metadata.created_time", "asc"),
        ("metadata.updated_time", "desc"),
        ("metadata.title", "asc"),  # 非时间字段
        ("text", "desc"),  # 非时间字段
    ]

    print("=== 测试时间字段向后兼容性 ===")

    for sort_field, sort_order in test_cases:
        print(f"\n测试: {sort_field} {sort_order}")
        config = create_sort_config(sort_field, sort_order)
        print(f"配置: {config}")

    print("\n✅ 向后兼容性测试完成！")


if __name__ == "__main__":
    test_sort_config()

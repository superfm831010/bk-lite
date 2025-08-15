#!/usr/bin/env python3
"""
测试新的LATS SSE处理器设计
"""
from src.api.agent.lats_sse_handler import (
    _is_internal_evaluation_data,
    _is_comprehensive_answer,
    _is_substantial_response,
    _handle_initial_response_message,
    _handle_expand_message,
    _handle_tools_message
)
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


class MockAIMessage:
    def __init__(self, content):
        self.content = content


class MockToolMessage:
    def __init__(self, content):
        self.content = content


def test_evaluation_data_detection():
    print("🧪 测试内部评估数据检测\n")

    test_cases = [
        ('{"reflections":"The response provides...","score":10,"found_solution":true}', True, "JSON评估数据"),
        ('{"score": 9, "evaluation": "good"}', True, "评分JSON"),
        ('DM数据库是一款企业级关系型数据库管理系统', False, "正常回答内容"),
        ('根据您的问题，我来为您介绍DM数据库...', False, "实质回答内容"),
        ('reflections: some text', False, "非JSON格式"),
        ('[{"score": 8}]', True, "JSON数组评估"),
    ]

    for content, expected, description in test_cases:
        result = _is_internal_evaluation_data(content)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {description}: {result}")
        if result != expected:
            print(f"    期望: {expected}, 实际: {result}")


def test_comprehensive_answer_detection():
    print("\n🧪 测试综合答案检测\n")

    test_cases = [
        ("短回答", False, "内容过短"),
        ("DM数据库（达梦数据库）是由达梦公司开发的一款具有完全自主知识产权的高性能数据库管理系统。它支持SQL标准，具有高可靠性、高性能、可扩展性强等特点，广泛应用于金融、电信、政府等关键业务领域。", True, "综合性数据库介绍"),
        ("简单的是或否回答", False, "简单回答"),
        ("DM数据库是一个数据库。", False, "过于简单"),
    ]

    for content, expected, description in test_cases:
        result = _is_comprehensive_answer(content)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {description}: {result}")


def test_node_message_handling():
    print("\n🧪 测试节点消息处理\n")

    lats_state = {
        'is_searching': False,
        'has_initial_response': False,
        'search_iterations': 0,
        'final_solution_found': False
    }

    # 测试初始响应消息
    print("📋 初始响应节点测试:")
    initial_content = "DM数据库是一款企业级关系型数据库管理系统，具有高性能、高可用性等特点。"
    result = _handle_initial_response_message(
        "AIMessage", initial_content, lats_state)
    print(f"  AI消息处理: {'✅' if result else '❌'}")
    if result:
        print(f"    输出: {result[:100]}...")

    # 测试扩展节点消息
    print("\n📋 扩展节点测试:")
    json_eval = '{"reflections":"The response provides...","score":10,"found_solution":true}'
    result = _handle_expand_message("AIMessage", json_eval, lats_state, 1)
    print(f"  JSON评估过滤: {'✅' if result is None else '❌'}")

    comprehensive_answer = "根据您的问题，DM数据库（达梦数据库）是由达梦公司自主研发的关系型数据库管理系统。它具有以下主要特点：1. 完全自主知识产权 2. 支持标准SQL语法 3. 高性能和高可用性 4. 广泛应用于金融、电信等行业"
    result = _handle_expand_message(
        "AIMessage", comprehensive_answer, lats_state, 1)
    print(f"  综合答案处理: {'✅' if result and '最终答案' in result else '❌'}")
    if result:
        print(f"    输出: {result[:100]}...")


def test_substantial_response():
    print("\n🧪 测试实质内容检测\n")

    test_cases = [
        ("很短", False, "内容过短"),
        ("System: 这是系统消息", False, "系统消息"),
        ("tool_call: some function", False, "工具调用"),
        ("这是一个有实质内容的回答，包含了用户需要的信息", True, "实质回答"),
        ("DM数据库是一款专业的数据库管理系统", True, "有效回答"),
    ]

    for content, expected, description in test_cases:
        result = _is_substantial_response(content)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {description}: {result}")


if __name__ == "__main__":
    test_evaluation_data_detection()
    test_comprehensive_answer_detection()
    test_substantial_response()
    test_node_message_handling()

    print("\n" + "="*60)
    print("🎯 新设计的优势:")
    print("  ✅ 完全基于节点类型进行处理，避免关键词硬编码")
    print("  ✅ 智能过滤JSON评估数据，只输出对用户有价值的内容")
    print("  ✅ 根据内容结构和长度判断是否为综合性答案")
    print("  ✅ 状态感知的消息处理，更准确的输出控制")
    print("  ✅ 可扩展的节点处理架构，便于维护和扩展")

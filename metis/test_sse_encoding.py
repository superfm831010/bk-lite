#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试SSE编码修复
"""
import json


def test_sse_encoding():
    """测试SSE数据编码"""
    # 测试中文内容
    content = "🔍 **正在启动 LATS 智能搜索...**\n\n🧠 初始化语言辅助树搜索引擎\n\n💡 准备生成多个候选解决方案"

    # 创建响应对象
    response = {
        "id": "test-chat-id",
        "object": "chat.completion.chunk",
        "created": 1692123456,
        "model": "test-model",
        "choices": [{
            "delta": {
                "role": "assistant",
                "content": content
            },
            "index": 0,
            "finish_reason": None
        }]
    }

    # 使用ensure_ascii=False序列化
    json_str = json.dumps(response, ensure_ascii=False, separators=(',', ':'))
    sse_data = f"data: {json_str}\n\n"

    print("原始内容:")
    print(content)
    print("\nSSE数据:")
    print(sse_data)
    print("\nSSE数据编码为UTF-8:")
    print(sse_data.encode('utf-8'))
    print("\nSSE数据编码为UTF-8后解码:")
    print(sse_data.encode('utf-8').decode('utf-8'))

    # 验证是否包含中文字符
    assert "智能搜索" in sse_data
    assert "🔍" in sse_data
    print("\n✅ 编码测试通过！")


if __name__ == "__main__":
    test_sse_encoding()

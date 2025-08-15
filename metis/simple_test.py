#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

# 测试中文内容
content = "🔍 正在启动 LATS 智能搜索"

response = {
    "id": "test",
    "content": content
}

# 序列化
json_str = json.dumps(response, ensure_ascii=False)
print("JSON:", json_str)
print("UTF-8编码:", json_str.encode('utf-8'))
print("测试通过")

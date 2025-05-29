# -- coding: utf-8 --
# @File: mock.py
# @Time: 2025/5/20 11:24
# @Author: windyzhao


import random
import time
import uuid
import json
from datetime import datetime, timedelta


def generate_mock_events(num_events=100):
    # 基础数据模板
    base_event = {
        "title": "CPU Usage High",
        "description": "CPU usage exceeded 80%",
        "value": 85.0,
        "item": "cpu_usage",
        "level": "fatal",
        "start_time": "1747277570",
        "end_time": "1747277574",
        "labels": {
            "instance": "server1"
        },
        "annotations": {
            "alertname": "HighCPUUsage"
        },
        "external_id": "sasasa",
        "status": "firing",
        "resource_id": 1,
        "resource_type": "host",
        "resource_name": "host-1",
    }

    # 可能的变量值
    levels = ["fatal", "critical", "warning", "info"]
    statuses = ["firing", "resolved"]
    server_prefixes = ["web", "db", "app", "cache", "lb"]

    events = []

    for i in range(num_events):
        # 复制基础事件
        event = base_event.copy()

        now = int(time.time())
        start_time = now - random.randint(0, 5 * 60)
        duration = random.randint(1, 60)  # 1-300秒
        end_time = start_time + duration

        # 随机CPU使用率描述
        cpu_usage = random.randint(65, 100)
        if cpu_usage >= 95:
            level = "fatal"
        elif cpu_usage >= 90:
            level = "critical"
        elif cpu_usage >= 80:
            level = "warning"
        else:
            level = "info"

        # 服务器名称
        server_type = random.choice(server_prefixes)
        server_num = random.randint(1, 100)

        # 更新事件数据
        event["title"] = f"CPU Usage {level.capitalize()}"
        event["description"] = f"CPU usage exceeded {cpu_usage}%"
        event["level"] = level
        event["start_time"] = str(start_time)
        event["end_time"] = str(end_time)
        event["labels"] = {
            "instance": f"{server_type}-{server_num}",
            "region": random.choice(["us-east", "us-west", "eu-central", "ap-southeast"])
        }
        event["annotations"] = {
            "alertname": "HighCPUUsage",
            "summary": f"High CPU usage detected on {server_type}-{server_num}",
            "severity": level
        }
        event["external_id"] = str(uuid.uuid4())
        event["status"] = random.choice(statuses)
        event["value"] = float(cpu_usage)
        event["item"] = "cpu_usage"
        event["resource_id"] = server_num
        event["resource_type"] = "host"
        event["resource_name"] = f"{server_type}-{server_num}"

        events.append(event)

    # 构建最终数据结构
    result = {
        "source_type": "monitor",
        "source_id": "monitor",
        "events": events
    }

    return result


if __name__ == "__main__":
    # 生成100个mock事件
    mock_data = generate_mock_events(100)

    # 保存到JSON文件
    with open("mock_monitor_events.json", "w") as f:
        json.dump(mock_data, f, indent=2)

    print("Mock数据已生成并保存到 mock_monitor_events.json 文件")
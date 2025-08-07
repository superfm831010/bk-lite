# -- coding: utf-8 --
# @File: init_constants.py
# @Time: 2025/7/24 17:01
# @Author: windyzhao


INIT_SOURCE_API_DATA = [
    {
        "name": "告警趋势",
        "desc": "查询告警趋势的数据",
        "rest_api": "alert/get_alert_trend_data",
        "params": {
            "group_by": "聚合类型",  # 默认天(day)，可选类型(minute, hour, day, week, month)
            "filters": "过滤条件",
            # {"start_time": "开始时间，格式为 'YYYY-MM-DD HH:MM:SS'",  "end_time": "结束时间，格式为 'YYYY-MM-DD HH:MM:SS'"}
        }

    }
]

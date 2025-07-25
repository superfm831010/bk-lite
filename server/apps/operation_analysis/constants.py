# -- coding: utf-8 --
# @File: constants.py
# @Time: 2025/7/14 16:02
# @Author: windyzhao


class DashboardType:
    """
    仪表盘类型
    gauge（仪表盘）
    line(折线图)
    bar(柱状图)
    pie（饼图）
    scatter（散点图）
    map（地图）
    text（文本）
    """
    GAUGE = "gauge"
    LINE = "line"
    BAR = "bar"
    PIE = "pie"
    SCATTER = "scatter"
    MAP = "map"
    TEXT = "text"

    CHOICES = [
        (GAUGE, "仪表盘"),
        (LINE, "折线图"),
        (BAR, "柱状图"),
        (PIE, "饼图"),
        (SCATTER, "散点图"),
        (MAP, "地图"),
        (TEXT, "文本")
    ]

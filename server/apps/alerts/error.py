# -- coding: utf-8 --
# @File: error.py
# @Time: 2025/6/17 14:27
# @Author: windyzhao

class AuthenticationSourceError(Exception):
    """自定义认证异常"""

    def __init__(self, msg):
        self.message = msg


class ShieldNotFoundError(Exception):
    """自定义异常：没有活跃的屏蔽策略"""

    def __init__(self, message="No active shields found"):
        self.message = message
        super().__init__(self.message)


class EventNotFoundError(Exception):
    """自定义异常：没有事件可供屏蔽"""

    def __init__(self, message="No Events found for shielding"):
        self.message = message
        super().__init__(self.message)


class AlertNotFoundError(Exception):
    """自定义异常：没有告警可供分派"""

    def __init__(self, message="No Alert found for Assignment"):
        self.message = message
        super().__init__(self.message)

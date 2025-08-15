# victoriametrics服务信息
import os

VICTORIALOGS_HOST = os.getenv("VICTORIALOGS_HOST")
VICTORIALOGS_USER = os.getenv("VICTORIALOGS_USER")
VICTORIALOGS_PWD = os.getenv("VICTORIALOGS_PWD")

# 策略相关常量
POLICY_MODULE = "policy"
# 数据流相关常量
STREAM_MODULE = "stream"
DEFAULT_PERMISSION = ['View', 'Operate']

# 告警状态
ALERT_STATUS_NEW = "new"
ALERT_STATUS_CLOSED = "closed"
ALERT_STATUS_CHOICES = [
    (ALERT_STATUS_NEW, "活跃"),
    (ALERT_STATUS_CLOSED, "关闭"),
]

# 告警类型
KEYWORD = "keyword"
AGGREGATE = "aggregate"
ALERT_TYPE = [KEYWORD, AGGREGATE]

# 告警级别
ALERT_LEVEL_INFO = "info"
ALERT_LEVEL_WARNING = "warning"
ALERT_LEVEL_ERROR = "error"
ALERT_LEVEL_CRITICAL = "critical"

# 通知类型
NOTICE_TYPE_EMAIL = "email"
NOTICE_TYPE_SMS = "sms"
NOTICE_TYPE_WEBHOOK = "webhook"

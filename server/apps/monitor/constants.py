import os

# victoriametrics服务信息
VICTORIAMETRICS_HOST = os.getenv("VICTORIAMETRICS_HOST")
VICTORIAMETRICS_USER = os.getenv("VICTORIAMETRICS_USER")
VICTORIAMETRICS_PWD = os.getenv("VICTORIAMETRICS_PWD")
# 添加SSL验证配置，支持环境变量控制
VICTORIAMETRICS_SSL_VERIFY = os.getenv("VICTORIAMETRICS_SSL_VERIFY", "false").lower() == "true"

MONITOR_OBJ_KEYS = ["name", "type", "default_metric", "instance_id_keys", "supplementary_indicators"]

# 阀值对比方法
THRESHOLD_METHODS = {
    ">": lambda x, y: x > y,
    "<": lambda x, y: x < y,
    "=": lambda x, y: x == y,
    "!=": lambda x, y: x != y,
    ">=": lambda x, y: x >= y,
    "<=": lambda x, y: x <= y,
}

# 告警等级权重
LEVEL_WEIGHT = {
    "warning": 2,
    "error": 3,
    "critical": 4,
    "no_data": 5,
}

# 对象顺序key
OBJ_ORDER = "OBJ_ORDER"

# 对象默认顺序
DEFAULT_OBJ_ORDER = [
  {"name_list": ["Host"], "type": "OS"},
  {"name_list": ["Website", "Ping"], "type": "Web"},
  {"name_list": ["ElasticSearch", "Mongodb", "Mysql", "Postgres", "Redis", "Oracle"], "type": "Database"},
  {"name_list": ["RabbitMQ", "Nginx", "Apache", "ClickHouse", "Consul", "Tomcat", "Zookeeper", "ActiveMQ", "MinIO", "Jetty", "WebLogic"], "type": "Middleware"},
  {"name_list": ["Switch", "Router", "Firewall", "Loadbalance", "Detection Device", "Scanning Device"], "type": "Network Device"},
  {"name_list": ["Bastion Host", "Storage", "Hardware Server"], "type": "Hardware Device"},
  {"name_list": ["Docker", "Docker Container"], "type": "Container Management"},
  {"name_list": ["Cluster", "Pod", "Node"], "type": "K8S"},
  {"name_list": ["vCenter", "ESXI", "VM", "DataStorage"], "type": "VMWare"},
  {"name_list": ["TCP", "CVM"], "type": "Tencent Cloud"},
  {"name_list": ["JVM", "SNMP Trap"], "type": "Other"}
]

# 阈值告警类型， 无数据告警类型
THRESHOLD = "threshold"
NO_DATA = "no_data"

DEFAULT_PERMISSION = ['View', 'Operate']
INSTANCE_MODULE = "instance"
POLICY_MODULE = "policy"
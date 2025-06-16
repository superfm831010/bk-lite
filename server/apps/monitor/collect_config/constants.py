ONLY_CONFIG = {}
ONLY_CHILD_CONFIG = {
    ("Telegraf", "host"): "toml",
    ("Telegraf", "ping"): "toml",
    ("Telegraf", "web"): "toml",
    ("Telegraf", "trap"): "toml",
    ("Telegraf", "ipmi"): "toml",
    ("Telegraf", "snmp"): "toml",
    ("Telegraf", "middleware"): "toml",
    ("Telegraf", "docker"): "toml",
    ("Telegraf", "database"): "toml",
    ("Telegraf", "http"): "toml",
    ("Telegraf", "jmx"): "toml",
    ("Telegraf", "exporter"): "toml",
    ("Telegraf", "bkpull"): "toml",
}
CONFIG_AND_CHILD_CONFIG = {
    ("ActiveMQ-JMX", "jmx"): "yaml",
    ("JBoss-JMX", "jmx"): "yaml",
    ("Jetty-JMX", "jmx"): "yaml",
    ("TongWeb6-JMX", "jmx"): "yaml",
    ("TongWeb7-JMX", "jmx"): "yaml",
    ("WebLogic-JMX", "jmx"): "yaml",
    ("JVM-JMX", "jmx"): "yaml",
    ("Tomcat-JMX", "jmx"): "yaml",
    ("Oracle-Exporter", "exporter"): "yaml",
}

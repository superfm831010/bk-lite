from apps.node_mgmt.models.sidecar import Collector


COLLECTORS = [
    {
        "id": "telegraf_linux",
        "name": "Telegraf",
        "controller_default_run": False,
        "icon": "shujucaiji",
        "node_operating_system": "linux",
        "service_type": "exec",
        "executable_path": "/opt/fusion-collectors/bin/telegraf",
        "execute_parameters": "--config %s",
        "validation_parameters": "--config %s --test",
        "default_template": "",
        "introduction": "Telegraf is a lightweight and efficient metrics collector that supports real-time collection, processing, and transmission of multi-source data, widely used in monitoring and data analysis scenarios."
    },
    {
        "id": "telegraf_windows",
        "name": "Telegraf",
        "controller_default_run": False,
        "icon": "shujucaiji",
        "node_operating_system": "windows",
        "service_type": "exec",
        "executable_path": "C:\\Program Files\\Telegraf\\telegraf.exe",
        "execute_parameters": "-config C:\\Program Files\\Telegraf\\telegraf.conf",
        "validation_parameters": "-test -config C:\\Program Files\\Telegraf\\telegraf.conf",
        "default_template": "",
        "introduction": "Telegraf is a lightweight and efficient metrics collector that supports real-time collection, processing, and transmission of multi-source data, widely used in monitoring and data analysis scenarios."
    },
    {
        "id": "natsexecutor_linux",
        "name": "NATS-Executor",
        "controller_default_run": True,
        "icon": "caijixinxi",
        "node_operating_system": "linux",
        "service_type": "exec",
        "executable_path": "/opt/fusion-collectors/bin/nats-executor",
        "execute_parameters": "--config %s",
        "validation_parameters": "",
        "default_template": "",
        "introduction": "NATS Executor is a task scheduling and management tool that automates data storage, backup, and distributed file processing tasks."
    },
    {
        "id": "natsexecutor_windows",
        "name": "NATS-Executor",
        "controller_default_run": True,
        "icon": "caijixinxi",
        "node_operating_system": "windows",
        "service_type": "exec",
        "executable_path": "C:\\Program Files\\NATS\\nats-executor.exe",
        "execute_parameters": "-config C:\\Program Files\\NATS\\nats-executor.conf",
        "validation_parameters": "",
        "default_template": "",
        "introduction": "NATS Executor is a task scheduling and management tool that automates data storage, backup, and distributed file processing tasks."
    },
    {
        "id": "jmx_jvm_linux",
        "name": "JVM-JMX",
        "controller_default_run": False,
        "icon": "",
        "node_operating_system": "linux",
        "service_type": "exec",
        "executable_path": "/usr/bin/java",
        "execute_parameters": "-jar jmx_jvm.jar 40000 %s",
        "validation_parameters": "",
        "default_template": "",
        "introduction": "JVM-JMX is a Java Management Extensions (JMX) monitoring tool that collects and monitors JVM metrics, providing real-time performance insights."
    },
    {
        "id": "jmx_tomcat_linux",
        "name": "JMX-Tomcat",
        "controller_default_run": False,
        "icon": "",
        "node_operating_system": "linux",
        "service_type": "exec",
        "executable_path": "/usr/bin/java",
        "execute_parameters": "-jar jmx_tomcat.jar 40100 %s",
        "validation_parameters": "",
        "default_template": "",
        "introduction": "JMX-Tomcat is a Java Management Extensions (JMX) monitoring tool that collects and monitors Tomcat server metrics, providing real-time performance insights."
    },
    {
        "id": "jmx_jboss_linux",
        "name": "JMX-JBoss",
        "controller_default_run": False,
        "icon": "",
        "node_operating_system": "linux",
        "service_type": "exec",
        "executable_path": "/usr/bin/java",
        "execute_parameters": "-jar jmx_jboss.jar 40200 %s",
        "validation_parameters": "",
        "default_template": "",
        "introduction": "JMX-JBoss is a Java Management Extensions (JMX) monitoring tool that collects and monitors JBoss server metrics, providing real-time performance insights."
    },
    {
        "id": "jmx_jetty_linux",
        "name": "JMX-Jetty",
        "controller_default_run": False,
        "icon": "",
        "node_operating_system": "linux",
        "service_type": "exec",
        "executable_path": "/usr/bin/java",
        "execute_parameters": "-jar jmx_jetty.jar 40300 %s",
        "validation_parameters": "",
        "default_template": "",
        "introduction": "JMX-Jetty is a Java Management Extensions (JMX) monitoring tool that collects and monitors Jetty server metrics, providing real-time performance insights."
    },
    {
        "id": "jmx_activemq_linux",
        "name": "JMX-ActiveMQ",
        "controller_default_run": False,
        "icon": "",
        "node_operating_system": "linux",
        "service_type": "exec",
        "executable_path": "/usr/bin/java",
        "execute_parameters": "-jar jmx_activemq.jar 40400 %s",
        "validation_parameters": "",
        "default_template": "",
        "introduction": "JMX-ActiveMQ is a Java Management Extensions (JMX) monitoring tool that collects and monitors ActiveMQ server metrics, providing real-time performance insights."
    },
    {
        "id": "jmx_weblogic_linux",
        "name": "JMX-WebLogic",
        "controller_default_run": False,
        "icon": "",
        "node_operating_system": "linux",
        "service_type": "exec",
        "executable_path": "/usr/bin/java",
        "execute_parameters": "-jar jmx_weblogic.jar 40500 %s",
        "validation_parameters": "",
        "default_template": "",
        "introduction": "JMX-WebLogic is a Java Management Extensions (JMX) monitoring tool that collects and monitors WebLogic server metrics, providing real-time performance insights."
    },
    {
        "id": "jmx_tongweb6_linux",
        "name": "JMX-TongWeb6",
        "controller_default_run": False,
        "icon": "",
        "node_operating_system": "linux",
        "service_type": "exec",
        "executable_path": "/usr/bin/java",
        "execute_parameters": "-jar jmx_tongweb6.jar 40600 %s",
        "validation_parameters": "",
        "default_template": "",
        "introduction": "JMX-TongWeb6 is a Java Management Extensions (JMX) monitoring tool that collects and monitors TongWeb6 server metrics, providing real-time performance insights."
    },
    {
        "id": "jmx_tongweb7_linux",
        "name": "JMX-TongWeb7",
        "controller_default_run": False,
        "icon": "",
        "node_operating_system": "linux",
        "service_type": "exec",
        "executable_path": "/usr/bin/java",
        "execute_parameters": "-jar jmx_tongweb7.jar 40700 %s",
        "validation_parameters": "",
        "default_template": "",
        "introduction": "JMX-TongWeb7 is a Java Management Extensions (JMX) monitoring tool that collects and monitors TongWeb7 server metrics, providing real-time performance insights."
    },
]


def collector_init():
    """
    初始化采集器
    """
    old_collector = Collector.objects.all()
    old_collector_set = {i.id for i in old_collector}

    create_collectors, update_collectors = [], []

    for collector_info in COLLECTORS:
        if collector_info["id"] in old_collector_set:
            update_collectors.append(collector_info)
        else:
            create_collectors.append(collector_info)

    if create_collectors:
        Collector.objects.bulk_create([Collector(**i) for i in create_collectors])

    if update_collectors:
        Collector.objects.bulk_update([Collector(**i) for i in update_collectors], ["service_type", "executable_path", "execute_parameters", "validation_parameters", "default_template", "introduction"])

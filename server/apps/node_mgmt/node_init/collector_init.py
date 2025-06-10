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
        "executable_path": "C:\\bklite\\fusion-collectors\\bin\\telegraf.exe",
        "execute_parameters": "-config %s",
        "validation_parameters": "--config %s --test",
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
        "executable_path": "C:\\bklite\\fusion-collectors\\bin\\nats-executor.exe",
        "execute_parameters": "--config %s",
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
        "execute_parameters": "-jar /opt/fusion-collectors/bin/jmx_jvm.jar $LISTEN_HOST %s",
        "validation_parameters": "",
        "default_template": "",
        "introduction": "JVM-JMX is a Java Management Extensions (JMX) monitoring tool that collects and monitors JVM metrics, providing real-time performance insights."
    },
    {
        "id": "jmx_tomcat_linux",
        "name": "Tomcat-JMX",
        "controller_default_run": False,
        "icon": "",
        "node_operating_system": "linux",
        "service_type": "exec",
        "executable_path": "/usr/bin/java",
        "execute_parameters": "-jar /opt/fusion-collectors/bin/jmx_tomcat.jar $LISTEN_HOST %s",
        "validation_parameters": "",
        "default_template": "",
        "introduction": "JMX-Tomcat is a Java Management Extensions (JMX) monitoring tool that collects and monitors Tomcat server metrics, providing real-time performance insights."
    },
    {
        "id": "jmx_jboss_linux",
        "name": "JBoss-JMX",
        "controller_default_run": False,
        "icon": "",
        "node_operating_system": "linux",
        "service_type": "exec",
        "executable_path": "/usr/bin/java",
        "execute_parameters": "-jar /opt/fusion-collectors/bin/jmx_jboss.jar $LISTEN_HOST %s",
        "validation_parameters": "",
        "default_template": "",
        "introduction": "JMX-JBoss is a Java Management Extensions (JMX) monitoring tool that collects and monitors JBoss server metrics, providing real-time performance insights."
    },
    {
        "id": "jmx_jetty_linux",
        "name": "Jetty-JMX",
        "controller_default_run": False,
        "icon": "",
        "node_operating_system": "linux",
        "service_type": "exec",
        "executable_path": "/usr/bin/java",
        "execute_parameters": "-jar /opt/fusion-collectors/bin/jmx_jetty.jar $LISTEN_HOST %s",
        "validation_parameters": "",
        "default_template": "",
        "introduction": "JMX-Jetty is a Java Management Extensions (JMX) monitoring tool that collects and monitors Jetty server metrics, providing real-time performance insights."
    },
    {
        "id": "jmx_activemq_linux",
        "name": "ActiveMQ-JMX",
        "controller_default_run": False,
        "icon": "",
        "node_operating_system": "linux",
        "service_type": "exec",
        "executable_path": "/usr/bin/java",
        "execute_parameters": "-jar /opt/fusion-collectors/bin/jmx_activemq.jar $LISTEN_HOST %s",
        "validation_parameters": "",
        "default_template": "",
        "introduction": "JMX-ActiveMQ is a Java Management Extensions (JMX) monitoring tool that collects and monitors ActiveMQ server metrics, providing real-time performance insights."
    },
    {
        "id": "jmx_weblogic_linux",
        "name": "WebLogic-JMX",
        "controller_default_run": False,
        "icon": "",
        "node_operating_system": "linux",
        "service_type": "exec",
        "executable_path": "/usr/bin/java",
        "execute_parameters": "-jar /opt/fusion-collectors/bin/jmx_weblogic.jar $LISTEN_HOST %s",
        "validation_parameters": "",
        "default_template": "",
        "introduction": "JMX-WebLogic is a Java Management Extensions (JMX) monitoring tool that collects and monitors WebLogic server metrics, providing real-time performance insights."
    },
    {
        "id": "jmx_tongweb6_linux",
        "name": "TongWeb6-JMX",
        "controller_default_run": False,
        "icon": "",
        "node_operating_system": "linux",
        "service_type": "exec",
        "executable_path": "/usr/bin/java",
        "execute_parameters": "-jar /opt/fusion-collectors/bin/jmx_tongweb6.jar $LISTEN_HOST %s",
        "validation_parameters": "",
        "default_template": "",
        "introduction": "JMX-TongWeb6 is a Java Management Extensions (JMX) monitoring tool that collects and monitors TongWeb6 server metrics, providing real-time performance insights."
    },
    {
        "id": "jmx_tongweb7_linux",
        "name": "TongWeb7-JMX",
        "controller_default_run": False,
        "icon": "",
        "node_operating_system": "linux",
        "service_type": "exec",
        "executable_path": "/usr/bin/java",
        "execute_parameters": "-jar /opt/fusion-collectors/bin/jmx_tongweb7.jar $LISTEN_HOST %s",
        "validation_parameters": "",
        "default_template": "",
        "introduction": "JMX-TongWeb7 is a Java Management Extensions (JMX) monitoring tool that collects and monitors TongWeb7 server metrics, providing real-time performance insights."
    },
    {
        "id": "exporter_oracle_linux",
        "name": "Oracle-Exporter",
        "controller_default_run": False,
        "icon": "",
        "node_operating_system": "linux",
        "service_type": "exec",
        "executable_path": "/opt/fusion-collectors/bin/oracle_exporter",
        "execute_parameters": "--host $HOST --port $PORT --web.listen-address 127.0.0.1:$LISTEN_PORT",
        "validation_parameters": "",
        "default_template": "",
        "introduction": "Oracle Exporter is a monitoring tool that collects and exports Oracle database metrics, providing insights into database performance and health."
    }
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

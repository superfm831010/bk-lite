import { useTranslation } from '@/utils/i18n';
import { useMemo } from 'react';

const DISPLAY_PLUGINS: string[] = [
  'Telegraf',
  'Vector',
  'Beat',
  'Export',
  'JMX',
];

const COLLECTOR_LABEL: Record<string, string[]> = {
  Telegraf: ['Telegraf'],
  Vector: ['Vector'],
  Beat: ['Auditbeat', 'Metricbeat', 'Winlogbeat', 'Packetbeat', 'Filebeat'],
  JMX: [
    'Tomcat-JMX',
    'ActiveMQ-JMX',
    'JBoss-JMX',
    'Jetty-JMX',
    'TongWeb6-JMX',
    'TongWeb7-JMX',
    'WebLogic-JMX',
    'JVM-JMX',
  ],
  Export: [
    'RabbitMQ-Exporter',
    'Nginx-Exporter',
    'Apache-Exporter',
    'Zookeeper-Exporter',
    'Kafka-Exporter',
    'IBM MQ-Exporter',
    'IIS-Exporter',
    'WebLogic-Exporter',
    'ElasticSearch-Exporter',
    'Mongodb-Exporter',
    'Mysql-Exporter',
    'Postgres-Exporter',
    'Redis-Exporter',
    'MSSQL-Exporter',
    'Oracle-Exporter',
    'DaMeng-Exporter',
    'openGauss-Exporter',
    'Gbase8a-Exporter',
    'HANA-Exporter',
    'GrenPlum-Exporter',
    'DB2-Exporter',
    'Excahnge-Exporter',
    'AD-Exporter',
  ],
  'BK-pull': [
    'Nacosbk-Bk-pull',
    'MinIO-Bk-pull',
    'etcd-Bk-pull',
    'JBoss-Bk-pull',
    'WebSphere-Bk-pull',
    'TiDB-BK-pull',
  ],
};

const useMenuItem = () => {
  const { t } = useTranslation();
  return useMemo(
    () => [
      {
        key: 'edit',
        role: 'Edit',
        title: 'edit',
        config: {
          title: 'editCollector',
          type: 'edit',
        },
      },
      {
        key: 'upload',
        role: 'AddPacket',
        title: 'uploadPackage',
        config: {
          title: 'uploadPackage',
          type: 'upload',
        },
      },
    ],
    [t]
  );
};

export { COLLECTOR_LABEL, useMenuItem, DISPLAY_PLUGINS };

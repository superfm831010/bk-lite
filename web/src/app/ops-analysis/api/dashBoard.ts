export const useDashBoardApi = () => {
  async function getTrendData() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          data: {
            dates: [
              '2025/07/10',
              '2025/07/11',
              '2025/07/12',
              '2025/07/13',
              '2025/07/14',
              '2025/07/15',
              '2025/07/16',
            ],
            values: [45, 120, 85, 200, 160, 180, 220],
          },
        });
      }, 500);
    });
  }

  async function getDataSources() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          data: [
            { label: 'MySQL数据库', value: 'mysql_source', type: 'database' },
            { label: 'Redis缓存', value: 'redis_source', type: 'cache' },
            { label: 'Elasticsearch日志', value: 'es_source', type: 'log' },
            {
              label: 'Prometheus监控',
              value: 'prometheus_source',
              type: 'metrics',
            },
            { label: 'Kafka消息队列', value: 'kafka_source', type: 'message' },
          ],
        });
      }, 300);
    });
  }

  async function getOsData() {
    // 模拟操作系统分布数据
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          data: [
            { value: 78, name: 'Linux' },
            { value: 30, name: 'Windows' },
            { value: 22, name: 'AIX' },
            { value: 8, name: 'Other' },
          ],
        });
      }, 400);
    });
  }

  async function getDataSourceAttrs(dataSourceValue: string) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const attrMap: Record<string, any[]> = {
          mysql_source: [
            { label: 'CPU使用率', value: 'cpu_usage' },
            { label: '内存使用率', value: 'memory_usage' },
            { label: '连接数', value: 'connections' },
            { label: '查询数', value: 'queries' },
          ],
          redis_source: [
            { label: '内存使用率', value: 'memory_usage' },
            { label: '键数量', value: 'key_count' },
            { label: '命中率', value: 'hit_rate' },
            { label: '连接数', value: 'connections' },
          ],
          es_source: [
            { label: '索引大小', value: 'index_size' },
            { label: '文档数量', value: 'doc_count' },
            { label: '查询响应时间', value: 'query_time' },
            { label: '节点状态', value: 'node_status' },
          ],
          prometheus_source: [
            { label: 'CPU指标', value: 'cpu_metrics' },
            { label: '内存指标', value: 'memory_metrics' },
            { label: '网络指标', value: 'network_metrics' },
            { label: '磁盘指标', value: 'disk_metrics' },
          ],
          kafka_source: [
            { label: '消息数量', value: 'message_count' },
            { label: '分区数', value: 'partition_count' },
            { label: '消费者延迟', value: 'consumer_lag' },
            { label: '吞吐量', value: 'throughput' },
          ],
        };

        resolve({
          data: attrMap[dataSourceValue] || [],
        });
      }, 200);
    });
  }

  return {
    getTrendData,
    getDataSources,
    getOsData,
    getDataSourceAttrs,
  };
};

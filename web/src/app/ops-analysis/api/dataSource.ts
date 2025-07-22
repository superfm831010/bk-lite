import useApiClient from '@/utils/request';

export const useDataSourceApi = () => {
  const { get, post, put, del } = useApiClient();

  const getDataSourceList = async (params?: any) => {
    return get('/operation_analysis/api/data_source/', { params });
  };

  const createDataSource = async (data: any) => {
    return post('/operation_analysis/api/data_source/', data);
  };

  const updateDataSource = async (id: number, data: any) => {
    return put(`/operation_analysis/api/data_source/${id}/`, data);
  };

  const deleteDataSource = async (id: number) => {
    return del(`/operation_analysis/api/data_source/${id}/`);
  };

  const getDataSourceDetail = async (id: number) => {
    return get(`/operation_analysis/api/data_source/${id}/`);
  };

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
    getDataSourceList,
    createDataSource,
    updateDataSource,
    deleteDataSource,
    getDataSourceDetail,
    getDataSourceAttrs,
  };
};

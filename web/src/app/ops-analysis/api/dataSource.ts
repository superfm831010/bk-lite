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

  const getSourceDataByApiId = async (id: number, params: any) => {
    return post(`/operation_analysis/api/data_source/get_source_data/${id}/`, params);
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
          ]
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
    getSourceDataByApiId
  };
};

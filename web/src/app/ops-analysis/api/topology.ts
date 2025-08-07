import useApiClient from '@/utils/request';

export const useTopologyApi = () => {
  const { get, post, put, del } = useApiClient();

  const getTopologyDetail = async (id: string | number) => {
    return get(`/operation_analysis/api/topology/${id}/`);
  };

  const saveTopology = async (id: string | number, data: any) => {
    return put(`/operation_analysis/api/topology/${id}/`, data);
  };

  const createTopology = async (data: any) => {
    return post('/operation_analysis/api/topology/', data);
  };

  const deleteTopology = async (id: string | number) => {
    return del(`/operation_analysis/api/topology/${id}/`);
  };

  return {
    getTopologyDetail,
    saveTopology,
    createTopology,
    deleteTopology,
  };
};

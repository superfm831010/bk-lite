import { SearchParams } from '@/app/log/types/search';
import useApiClient from '@/utils/request';

const useSearchApi = () => {
  const { post, get } = useApiClient();

  const getLogs = async (data: SearchParams) => {
    return await post(`/log/search/search/`, data);
  };

  const getHits = async (data: SearchParams) => {
    return await post(`/log/search/hits/`, data);
  };

  const getLogTail = async (params = {}) => {
    return await get(`/log/search/tail/`, { params });
  };

  return {
    getLogs,
    getHits,
    getLogTail,
  };
};

export default useSearchApi;

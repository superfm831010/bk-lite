import useApiClient from '@/utils/request';

export const useAlarmApi = () => {
  const { get, post } = useApiClient();

  const getAlarmList = async (params: any) => {
    return get('/alerts/api/alerts/', { params });
  };

  const getEventList = async (params: any) => {
    return get('/alerts/api/events/', { params });
  };

  const alertActionOperate = async (actionType: string, params: any) => {
    return post(`/alerts/api/alerts/operator/${actionType}/`, params);
  };

  return { getAlarmList, getEventList, alertActionOperate };
};

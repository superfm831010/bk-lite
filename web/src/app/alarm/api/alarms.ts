import useApiClient from '@/utils/request';

export const useAlarmApi = () => {
  const { get } = useApiClient();

  const getAlarmList = async (params: any) => {
    return get('/alerts/api/alerts/', { params });
  };

  const getEventList = async (params: any) => {
    return get('/alerts/api/events/', { params });
  };

  return { getAlarmList, getEventList };
};

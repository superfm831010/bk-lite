import useApiClient from '@/utils/request';

export const useSourceApi = () => {
  const { get } = useApiClient();
  
  const getAlertSources = async () => get('/alerts/api/alert_source/');

  return { getAlertSources };
};

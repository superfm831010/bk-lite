import useApiClient from '@/utils/request';

export const useSourceApi = () => {
  const { get } = useApiClient();

  const getAlertSources = async () => get('/alerts/api/alert_source/');

  const getAlertSourcesDetail = async (id: number | string) =>
    get(`/alerts/api/alert_source/${id}`);

  return { getAlertSources, getAlertSourcesDetail };
};

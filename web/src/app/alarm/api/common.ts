import useApiClient from '@/utils/request';
import { LevelItem } from '@/app/alarm/types/index';

export const useCommonApi = () => {
  const { get } = useApiClient();

  const getUserList = (params: { page_size: number; page: number }) =>
    get('/core/api/user_group/user_list/', { params });

  const getLevelList = () => get<LevelItem[]>('/alerts/api/level/');

  return { getUserList, getLevelList };
};

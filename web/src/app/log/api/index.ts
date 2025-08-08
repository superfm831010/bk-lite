import useApiClient from '@/utils/request';

const useLogApi = () => {
  const { get } = useApiClient();

  const getAllUsers = async () => {
    return await get(`/log/system_mgmt/user_all/`);
  };

  return {
    getAllUsers,
  };
};

export default useLogApi;

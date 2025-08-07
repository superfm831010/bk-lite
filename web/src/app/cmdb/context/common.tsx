'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import useApiClient from '@/utils/request';
import { UserItem } from '@/app/cmdb/types/assetManage';
import Spin from '@/components/spin';
import { usePathname } from 'next/navigation';
import { useAliveController } from 'react-activation';
interface CommonContextType {
  userList: UserItem[];
}

const CommonContext = createContext<CommonContextType | null>(null);

const CommonContextProvider = ({ children }: { children: React.ReactNode }) => {
  const [userList, setUserList] = useState<UserItem[]>([]);
  const [pageLoading, setPageLoading] = useState(false);
  const { get } = useApiClient();
  const { drop } = useAliveController();
  const pathname = usePathname();

  useEffect(() => {
    fetchUserList();
  }, []);

  useEffect(() => {
    if (drop && !pathname.startsWith('/cmdb/assetData')) {
      drop('assetData');
    }
  }, [pathname]);

  const fetchUserList = async () => {
    setPageLoading(true);
    try {
      const response = await get('/core/api/user_group/user_list/', {
        params: {
          page_size: 10000,
          page: 1,
        },
      });

      const userData: UserItem[] = response.users || [];
      setUserList(userData);
    } catch (error) {
      console.error('Failed to fetch user list:', error);
      setUserList([]);
    } finally {
      setPageLoading(false);
    }
  };
  return pageLoading ? (
    <Spin></Spin>
  ) : (
    <CommonContext.Provider
      value={{
        userList,
      }}
    >
      {children}
    </CommonContext.Provider>
  );
};

export const useCommon = () => useContext(CommonContext);

export default CommonContextProvider;

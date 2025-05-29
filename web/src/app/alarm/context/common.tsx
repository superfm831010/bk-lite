'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import { UserItem } from '@/app/alarm/types/types';
import useApiClient from '@/utils/request';
import Spin from '@/components/spin';

interface CommonContextType {
  userList: UserItem[];
}

const CommonContext = createContext<CommonContextType | null>(null);

const CommonContextProvider = ({ children }: { children: React.ReactNode }) => {
  const [userList, setUserList] = useState<UserItem[]>([]);
  const [pageLoading, setPageLoading] = useState(false);
  const { get } = useApiClient();

  useEffect(() => {
    getPermissionGroups();
  }, []);
  ;

  const getPermissionGroups = async () => {
    setPageLoading(true);
    try {
      const getUserList = get('/core/api/user_group/user_list/', {
        params: {
          page_size: 10000,
          page: 1,
        },
      });
      Promise.all([getUserList])
        .then((res) => {
          const userData: UserItem[] = res[0].users;
          setUserList(userData);
        })
        .finally(() => {
          setPageLoading(false);
        });
    } catch {
      setPageLoading(false);
    }
  };
  return pageLoading ? <Spin></Spin> : (
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

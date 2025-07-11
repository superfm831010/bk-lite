'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import useApiClient from '@/utils/request';
import { UserItem, Organization } from '@/app/log/types';
import Spin from '@/components/spin';
import { useUserInfoContext } from '@/context/userInfo';
import { transformTreeData } from '@/app/log/utils/common';

interface CommonContextType {
  userList: UserItem[];
  authOrganizations: Organization[];
}

const CommonContext = createContext<CommonContextType | null>(null);

const CommonContextProvider = ({ children }: { children: React.ReactNode }) => {
  const { isLoading } = useApiClient();
  const commonContext = useUserInfoContext();
  const [userList, setUserList] = useState<UserItem[]>([]);
  const [pageLoading, setPageLoading] = useState(false);

  useEffect(() => {
    if (isLoading) return;
    initData();
  }, [isLoading]);

  const initData = () => {
    setUserList([]);
    setPageLoading(false);
  };
  return pageLoading ? (
    <Spin />
  ) : (
    <CommonContext.Provider
      value={{
        userList,
        authOrganizations: transformTreeData(
          commonContext?.groups || []
        ) as any,
      }}
    >
      {children}
    </CommonContext.Provider>
  );
};

export const useCommon = () => useContext(CommonContext);

export default CommonContextProvider;

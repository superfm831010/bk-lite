import React, { createContext, useContext, useState, useEffect } from 'react';
import useApiClient from '@/utils/request';
import { Group, UserInfoContextType } from '@/types/index'
import { convertTreeDataToGroupOptions } from '@/utils/index'
import Cookies from 'js-cookie';
import { useSession } from 'next-auth/react';

const UserInfoContext = createContext<UserInfoContextType | undefined>(undefined);

export const UserInfoProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { get } = useApiClient();
  const { data: session, status } = useSession();
  const [selectedGroup, setSelectedGroupState] = useState<Group | null>(null);
  const [userId, setUserId] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [roles, setRoles] = useState<string[]>([]);
  const [groups, setGroups] = useState<Group[]>([]);
  const [flatGroups, setFlatGroups] = useState<Group[]>([]);
  const [isSuperUser, setIsSuperUser] = useState<boolean>(true);
  const [isFirstLogin, setIsFirstLogin] = useState<boolean>(true);

  useEffect(() => {
    console.log('Session:', session);
    if (status === 'authenticated' && session && session.user?.id) {
      const fetchLoginInfo = async () => {
        setLoading(true);
        try {
          const data = await get('/core/api/login_info/');
          if (!data) {
            console.error('Failed to fetch login info: No data received');
            setLoading(false);
            return;
          }
          
          const { group_list: groupList, roles, is_superuser, is_first_login, user_id } = data;
          setGroups(groupList || []);
          setRoles(roles || []);
          setIsSuperUser(!!is_superuser);
          setIsFirstLogin(!!is_first_login);
          setUserId(user_id || '');

          if (groupList?.length) {
            const flattenedGroups = convertTreeDataToGroupOptions(groupList);
            setFlatGroups(flattenedGroups);

            const groupIdFromCookie = Cookies.get('current_team');
            const initialGroup = flattenedGroups.find((group: Group) => group.id === groupIdFromCookie) || flattenedGroups[0];
            setSelectedGroupState(initialGroup);
            Cookies.set('current_team', initialGroup.id);
          }
        } catch (err) {
          console.error('Failed to fetch login_info:', err);
        } finally {
          setLoading(false);
        }
      };

      fetchLoginInfo();
    }
  }, [status, session]);

  const setSelectedGroup = (group: Group) => {
    setSelectedGroupState(group);
    Cookies.set('current_team', group.id);
  };

  return (
    <UserInfoContext.Provider value={{ loading, roles, groups, selectedGroup, flatGroups, isSuperUser, isFirstLogin, userId, setSelectedGroup }}>
      {children}
    </UserInfoContext.Provider>
  );
};

export const useUserInfoContext = () => {
  const context = useContext(UserInfoContext);
  if (!context) {
    throw new Error('useUserInfoContext must be used within a UserInfoProvider');
  }
  return context;
};

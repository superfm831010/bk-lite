import React, { useState, useCallback, useMemo } from 'react';
import { Dropdown, Space, Avatar, Menu, MenuProps, message } from 'antd';
import { usePathname, useRouter } from 'next/navigation';
import { useSession, signOut } from 'next-auth/react';
import { DownOutlined } from '@ant-design/icons';
import { useTranslation } from '@/utils/i18n';
import VersionModal from './versionModal';
import ThemeSwitcher from '@/components/theme';
import { useUserInfoContext } from '@/context/userInfo';
import { clearAuthToken } from '@/utils/crossDomainAuth';

interface GroupItemProps {
  id: string;
  name: string;
  isSelected: boolean;
  onClick: (id: string) => void;
}

const GroupItem: React.FC<GroupItemProps> = ({ id, name, isSelected, onClick }) => (
  <Space className="w-full" onClick={() => onClick(id)}>
    <span
      className={`inline-block w-2 h-2 rounded-full ${
        isSelected ? 'bg-[var(--color-success)]' : 'bg-[var(--color-fill-4)]'
      }`}
    />
    <span className="text-sm">{name}</span>
  </Space>
);

const UserInfo: React.FC = () => {
  const { data: session } = useSession();
  const { t } = useTranslation();
  const pathname = usePathname();
  const router = useRouter();
  const { flatGroups, selectedGroup, setSelectedGroup, displayName, isSuperUser } = useUserInfoContext();

  const [versionVisible, setVersionVisible] = useState<boolean>(false);
  const [dropdownVisible, setDropdownVisible] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const username = displayName || session?.user?.username || 'Test';

  const federatedLogout = useCallback(async () => {
    setIsLoading(true);
    try {
      // Call logout API for server-side cleanup
      await fetch('/api/auth/federated-logout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      // Clear authentication token
      clearAuthToken();
      
      // Use NextAuth's signOut to clear client session
      await signOut({ redirect: false });
      
      // Build login page URL with current page as callback URL after successful login
      const currentPageUrl = `${window.location.origin}${pathname}`;
      const loginUrl = `/auth/signin?callbackUrl=${encodeURIComponent(currentPageUrl)}`;
      
      // Redirect to login page
      window.location.href = loginUrl;
    } catch (error) {
      console.error('Logout error:', error);
      message.error(t('common.logoutFailed'));
      
      // Even if API call fails, still clear token and redirect to login page
      clearAuthToken();
      await signOut({ redirect: false });
      
      const currentPageUrl = `${window.location.origin}${pathname}`;
      const loginUrl = `/auth/signin?callbackUrl=${encodeURIComponent(currentPageUrl)}`;
      window.location.href = loginUrl;
    } finally {
      setIsLoading(false);
    }
  }, [pathname, t]);

  const handleChangeGroup = useCallback(async (key: string) => {
    const nextGroup = flatGroups.find(group => group.id === key);
    if (!nextGroup) return;

    setSelectedGroup(nextGroup);
    setDropdownVisible(false);

    const pathSegments = pathname ? pathname.split('/').filter(Boolean) : [];
    if (pathSegments.length > 2) {
      router.push(`/${pathSegments.slice(0, 2).join('/')}`);
    } else {
      window.location.reload();
    }
  }, [flatGroups, pathname, router]);

  const dropdownItems: MenuProps['items'] = useMemo(() => {
    const items: MenuProps['items'] = [
      {
        key: 'themeSwitch',
        label: <ThemeSwitcher />,
      },
      { type: 'divider' },
      {
        key: 'version',
        label: (
          <div className="w-full flex justify-between items-center">
            <span>{t('common.version')}</span>
            <span className="text-xs text-[var(--color-text-4)]">3.1.0</span>
          </div>
        ),
      },
      { type: 'divider' },
      {
        key: 'groups',
        label: (
          <div className="w-full flex justify-between items-center">
            <span>{t('common.group')}</span>
            <span className="text-xs text-[var(--color-text-4)]">{selectedGroup?.name}</span>
          </div>
        ),
        children: flatGroups
          .filter((group) => isSuperUser || session?.user?.username === 'kayla' || group.name !== 'OpsPilotGuest')
          .map((group) => ({
            key: group.id,
            label: (
              <GroupItem
                id={group.id}
                name={group.name}
                isSelected={selectedGroup?.name === group.name}
                onClick={handleChangeGroup}
              />
            ),
          })),
        popupClassName: 'user-groups-submenu'
      },
      { type: 'divider' },
      {
        key: 'logout',
        label: t('common.logout'),
        disabled: isLoading,
      },
    ];

    return items;
  }, [selectedGroup, flatGroups, isLoading]);

  const handleMenuClick = ({ key }: any) => {
    if (key === 'version') setVersionVisible(true);
    if (key === 'logout') federatedLogout();
    setDropdownVisible(false);
  };

  const userMenu = (
    <Menu
      className="min-w-[180px]"
      onClick={handleMenuClick}
      items={dropdownItems}
      subMenuOpenDelay={0.1}
      subMenuCloseDelay={0.1}
    />
  );

  return (
    <div className='flex items-center'>
      {username && (
        <Dropdown
          overlay={userMenu}
          trigger={['click']}
          visible={dropdownVisible}
          onVisibleChange={setDropdownVisible}
        >
          <a className='cursor-pointer' onClick={(e) => e.preventDefault()}>
            <Space className='text-sm'>
              <Avatar size={20} style={{ backgroundColor: 'var(--color-primary)', verticalAlign: 'middle' }}>
                {username.charAt(0).toUpperCase()}
              </Avatar>
              {username}
              <DownOutlined style={{ fontSize: '10px' }} />
            </Space>
          </a>
        </Dropdown>
      )}
      <VersionModal visible={versionVisible} onClose={() => setVersionVisible(false)} />
    </div>
  );
};

export default UserInfo;

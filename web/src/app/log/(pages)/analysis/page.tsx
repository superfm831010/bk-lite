'use client';

import React, { useState, useRef, useMemo } from 'react';
import Dashboard, { DashboardRef } from './dashBoard';
import { useTranslation } from '@/utils/i18n';
import { LeftOutlined, RightOutlined } from '@ant-design/icons';
import { Button, Input } from 'antd';
import { useBuildInDashBoards } from '../../hooks/analysis';
const { Search } = Input;

const Analysis: React.FC = () => {
  const { t } = useTranslation();
  const menuItems = useBuildInDashBoards();
  const [collapsed, setCollapsed] = useState(false);
  const dashboardRef = useRef<DashboardRef>(null);
  const [searchText, setSearchText] = useState<string>('');
  const [dashboardId, setDashboardId] = useState<string>(menuItems[0].id);

  const selectedDashboard = useMemo(() => {
    return menuItems.find((item) => item.id === dashboardId) || menuItems[0];
  }, [dashboardId, menuItems]);

  // 搜索过滤后的菜单项
  const filteredMenuItems = useMemo(() => {
    if (!searchText) return menuItems;
    const keyword = searchText.trim().toLowerCase();
    return menuItems.filter((item) =>
      item.name.toLowerCase().includes(keyword)
    );
  }, [searchText, menuItems]);

  const handleSearch = (val: string) => {
    setSearchText(val);
  };

  const handleItemClick = (item: string) => {
    setDashboardId(item);
  };

  return (
    <div
      className="flex w-full h-[calc(100vh-90px)] relative rounded-lg"
      style={{ minWidth: collapsed ? 0 : 200 }}
    >
      <div
        className={`h-full border-r border-[var(--color-border-1)] relative transition-all duration-300 ${
          collapsed ? 'w-0 min-w-0' : 'w-[200px] min-w-[200px]'
        }`}
        style={{
          width: collapsed ? 0 : 200,
          minWidth: collapsed ? 0 : 200,
          maxWidth: collapsed ? 0 : 200,
          flexShrink: 0,
        }}
      >
        <div className="w-full h-full overflow-x-hidden bg-[var(--color-bg-1)]">
          <div className="p-[20px]">
            <Search
              className="mb-[20px]"
              allowClear
              enterButton
              placeholder={t('common.searchPlaceHolder')}
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
              onSearch={handleSearch}
            ></Search>
            <ul>
              {filteredMenuItems.map((item) => (
                <li
                  key={item.id}
                  className={`p-2 mb-1 cursor-pointer rounded transition-all duration-200 hover:bg-[var(--color-fill-1)] text-center overflow-hidden whitespace-nowrap text-ellipsis ${
                    dashboardId === item.id
                      ? 'text-[var(--color-primary)] bg-[var(--color-fill-1)]'
                      : ''
                  }`}
                  onClick={() => handleItemClick(item.id)}
                  title={item.name}
                >
                  {item.name}
                </li>
              ))}
            </ul>
          </div>
        </div>
        <Button
          type="text"
          onClick={() => setCollapsed(!collapsed)}
          className={`absolute z-10 w-6 h-6 top-4 p-0 border border-[var(--color-border-3)] bg-[var(--color-bg-1)] flex items-center justify-center cursor-pointer rounded-full transition-all duration-300 ${
            collapsed
              ? 'left-0 border-l-0 rounded-tl-none rounded-bl-none'
              : 'left-[100%] -translate-x-1/2'
          }`}
        >
          {collapsed ? <RightOutlined /> : <LeftOutlined />}
        </Button>
      </div>
      <div className="h-full flex-1 flex" style={{ minWidth: 0 }}>
        <Dashboard
          ref={dashboardRef}
          selectedDashboard={selectedDashboard}
          editable={false}
        />
      </div>
    </div>
  );
};

export default Analysis;

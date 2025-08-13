'use client';

import React, { useState, useRef } from 'react';
import Sidebar from '../../components/sidebar';
import Dashboard from './dashBoard/index';
import Topology from './topology/index';
import { useTranslation } from '@/utils/i18n';
import { DirectoryType, SidebarRef } from '@/app/ops-analysis/types';
import { LeftOutlined, RightOutlined } from '@ant-design/icons';
import { Button, Empty, Modal } from 'antd';
import { useRouter, usePathname } from 'next/navigation';

interface ViewLayoutProps {
  children: React.ReactNode;
}

const ViewLayout: React.FC<ViewLayoutProps> = ({ children }) => {
  const { t } = useTranslation();
  const router = useRouter();
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);
  const [selectedType, setSelectedType] = useState<DirectoryType>('directory');
  const [selectedItem, setSelectedItem] = useState<{
    dashboard: any;
    topology: any;
  }>({
    dashboard: null,
    topology: null,
  });
  const dashboardRef = useRef<any>(null);
  const topologyRef = useRef<any>(null);
  const sidebarRef = useRef<SidebarRef>(null);
  const previousSelectionRef = useRef<{
    type: DirectoryType;
    item: any;
  } | null>(null);

  const isInSettings = pathname.includes('/settings');

  const handleSidebarDataUpdate = (updatedItem: any) => {
    if (
      selectedItem.dashboard &&
      updatedItem.id === selectedItem.dashboard.id
    ) {
      setSelectedItem((prev) => ({ ...prev, dashboard: updatedItem }));
    }
    if (selectedItem.topology && updatedItem.id === selectedItem.topology.id) {
      setSelectedItem((prev) => ({ ...prev, topology: updatedItem }));
    }
  };

  // 检查是否需要显示未保存更改提示
  const checkUnsavedChanges = () => {
    if (selectedType === 'dashboard' && dashboardRef.current) {
      return dashboardRef.current.hasUnsavedChanges();
    }
    if (selectedType === 'topology' && topologyRef.current) {
      return topologyRef.current.hasUnsavedChanges();
    }
    return false;
  };

  // 处理导航
  const handleNavigation = (type: DirectoryType, itemInfo: any) => {
    const isLeavingContentPage =
      (selectedType === 'dashboard' || selectedType === 'topology') &&
      (type === 'settings' ||
        type !== selectedType ||
        (type === selectedType &&
          itemInfo?.id !== selectedItem[selectedType]?.id));

    if (isLeavingContentPage && checkUnsavedChanges()) {
      // 记录当前选中状态
      previousSelectionRef.current = {
        type: selectedType,
        item: selectedItem[selectedType],
      };

      Modal.confirm({
        title: t('opsAnalysisSidebar.unsavedChanges'),
        content: t('opsAnalysisSidebar.unsavedChangesWarning'),
        okText: t('common.confirm'),
        cancelText: t('common.cancel'),
        okType: 'danger',
        centered: true,
        onOk: () => {
          performNavigation(type, itemInfo);
        },
        onCancel: () => {
          if (previousSelectionRef.current && sidebarRef.current) {
            const { item: prevItem } = previousSelectionRef.current;
            if (prevItem) {
              setTimeout(() => {
                sidebarRef.current?.setSelectedKeys([prevItem.id]);
              }, 0);
            }
          }
        },
      });
    } else {
      performNavigation(type, itemInfo);
    }
  };

  // 执行导航
  const performNavigation = (type: DirectoryType, itemInfo: any) => {
    setSelectedType(type);
    setSelectedItem({
      dashboard: type === 'dashboard' ? itemInfo : null,
      topology: type === 'topology' ? itemInfo : null,
    });
    if (type === 'settings') {
      router.push('/ops-analysis/view/settings/dataSource');
    } else {
      router.push('/ops-analysis/view');
    }
  };

  return (
    <div
      className="flex w-full h-[calc(100vh-90px)] relative rounded-lg"
      style={{ minWidth: collapsed ? 0 : 280 }}
    >
      <div
        className={`h-full border-r border-[var(--color-border-1)] relative transition-all duration-300 ${
          collapsed ? 'w-0 min-w-0' : 'w-[280px] min-w-[280px]'
        }`}
        style={{
          width: collapsed ? 0 : 280,
          minWidth: collapsed ? 0 : 280,
          maxWidth: collapsed ? 0 : 280,
          flexShrink: 0,
        }}
      >
        <div className="w-full h-full overflow-hidden bg-[var(--color-bg-1)]">
          <Sidebar
            ref={sidebarRef}
            onSelect={handleNavigation}
            onDataUpdate={handleSidebarDataUpdate}
          />
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
        {isInSettings ? (
          children
        ) : selectedType === 'topology' ? (
          <Topology
            ref={topologyRef}
            selectedTopology={selectedItem.topology}
          />
        ) : selectedType === 'dashboard' ? (
          <Dashboard
            ref={dashboardRef}
            selectedDashboard={selectedItem.dashboard}
          />
        ) : (
          <Empty
            className="w-full mt-[20vh]"
            description={t('opsAnalysisSidebar.selectItem')}
          />
        )}
      </div>
    </div>
  );
};

export default ViewLayout;

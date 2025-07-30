'use client';

import React, { useState } from 'react';
import Sidebar from './components/sidebar';
import Dashboard from './dashBoard/index';
import Topology from './topology/index';
import Datasource from './dataSource/index';
import { DirectoryType } from '@/app/ops-analysis/types';
import { LeftOutlined, RightOutlined } from '@ant-design/icons';
import { Button, Empty } from 'antd';

const ViewPage: React.FC = () => {
  const [collapsed, setCollapsed] = useState(false);
  const [selectedType, setSelectedType] = useState<DirectoryType>('group');
  const [selectedDashboard, setSelectedDashboard] = useState<any>(null);
  const [selectedTopology, setSelectedTopology] = useState<any>(null);

  return (
    <div
      className="flex w-full h-[calc(100vh-90px)] relative bg-[var(--color-bg-1)] rounded-lg"
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
        <div className="w-full h-full overflow-hidden">
          <Sidebar
            onSelect={(type, itemInfo) => {
              setSelectedType(type);
              if (type === 'dashboard' && itemInfo) {
                setSelectedDashboard(itemInfo);
                setSelectedTopology(null);
              } else if (type === 'topology' && itemInfo) {
                setSelectedTopology(itemInfo);
                setSelectedDashboard(null);
              } else {
                setSelectedDashboard(null);
                setSelectedTopology(null);
              }
            }}
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
        {selectedType === 'topology' ? (
          <Topology selectedTopology={selectedTopology} />
        ) : selectedType === 'dashboard' ? (
          <Dashboard selectedDashboard={selectedDashboard} />
        ) : selectedType === 'datasource' ? (
          <Datasource />
        ) : (
          <Empty
            className="w-full mt-[20vh]"
            description="请选择仪表盘或拓扑"
          />
        )}
      </div>
    </div>
  );
};

export default ViewPage;

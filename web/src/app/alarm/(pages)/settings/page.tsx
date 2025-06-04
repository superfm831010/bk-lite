'use client';

import React, { useState } from 'react';
import { Tabs } from 'antd';
import { useTranslation } from '@/utils/i18n';
import AlertAssign from './alertAssign/page';
import ShieldStrategy from './shieldStrategy/page';
import Introduction from '@/app/alarm/components/introduction';

const SettingsPage: React.FC = () => {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState('AlertAssign');
  const handleTabChange = (key: string) => setActiveTab(key);

  const tabItems = [
    { key: 'AlertAssign', label: t('settings.alertAssign') },
    { key: 'ShieldStrategy', label: t('settings.shieldStrategy') },
  ];

  return (
    <div className="flex flex-col h-full w-full">
      <Tabs activeKey={activeTab} onChange={handleTabChange} items={tabItems} />
      <Introduction
        title={
          activeTab === 'AlertAssign'
            ? t('settings.alertAssign')
            : t('settings.shieldStrategy')
        }
        message={
          activeTab === 'AlertAssign'
            ? t('settings.assignStrategyMessage')
            : t('settings.shieldStrategyMessage')
        }
      />
      {activeTab === 'AlertAssign' ? <AlertAssign /> : <ShieldStrategy />}
    </div>
  );
};

export default SettingsPage;

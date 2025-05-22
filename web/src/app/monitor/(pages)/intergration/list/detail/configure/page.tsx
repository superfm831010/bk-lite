'use client';
import React, { useState, useMemo } from 'react';
import { Spin, Segmented } from 'antd';
import ManualConfiguration from './manual';
import AutomaticConfiguration from './automatic';
import { useTranslation } from '@/utils/i18n';
import { useSearchParams } from 'next/navigation';
import configureStyle from './index.module.scss';
import { getConfigByPluginName } from '@/app/monitor/utils/common';

const Configure: React.FC = () => {
  const { t } = useTranslation();
  const searchParams = useSearchParams();
  const pluginName = searchParams.get('collect_type') || '';
  const [pageLoading, setPageLoading] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<string>('automatic');

  const onTabChange = (val: string) => {
    setPageLoading(false);
    setActiveTab(val);
  };

  const showInterval = useMemo(() => {
    return getConfigByPluginName(pluginName, 'collect_type') !== 'jmx';
  }, [pluginName]);

  const isK8s = useMemo(() => {
    return getConfigByPluginName(pluginName, 'collect_type') === 'k8s';
  }, [pluginName]);

  return (
    <>
      {!isK8s ?
        <div className={configureStyle.configure}>
          <Segmented
            className="mb-[20px]"
            value={activeTab}
            options={[
              { label: t('monitor.intergrations.automatic'), value: 'automatic' },
              { label: t('monitor.intergrations.manual'), value: 'manual' },
            ]}
            onChange={onTabChange}
          />
          <Spin spinning={pageLoading}>
            {activeTab === 'manual' ? (
              <ManualConfiguration showInterval={showInterval} />
            ) : (
              <AutomaticConfiguration showInterval={showInterval} />
            )}
          </Spin>
        </div> : t('monitor.intergrations.note')}
    </>
  );
};

export default Configure;

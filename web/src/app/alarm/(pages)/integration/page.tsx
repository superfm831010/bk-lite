'use client';

import React, { useState, useEffect } from 'react';
import alertStyle from './page.module.scss';
import { useSourceApi } from '@/app/alarm/api/sources';
import { Spin, Empty } from 'antd';
import { useTranslation } from '@/utils/i18n';

const IntegrationPage: React.FC = () => {
  const { getAlertSources } = useSourceApi();
  const [sources, setSources] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const { t } = useTranslation();

  useEffect(() => {
    getSourcesList();
  }, []);

  const getSourcesList = async () => {
    setLoading(true);
    try {
      const res = await getAlertSources();
      if (res) {
        setSources(res);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full flex-1">
      <Spin spinning={loading}>
        {!loading && sources.length === 0 ? (
          <Empty description={t('common.noData')} className="mt-[24vh]" />
        ) : (
          <div
            className={`${alertStyle.container} grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 2xl:grid-cols-6 gap-6`}
          >
            {sources.map((src) => (
              <div key={src.source_id} className={alertStyle.card}>
                <div className={alertStyle.cardContent}>
                  <img
                    src="/app/restful.png"
                    alt={src.description}
                    className={alertStyle.logo}
                  />
                  <span className={alertStyle.name}>{src.name}</span>
                  <span className={alertStyle.info}>
                    {t('integration.description')}：{src.description}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </Spin>
    </div>
  );
};

export default IntegrationPage;

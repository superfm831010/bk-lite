'use client';

import React, { useState, useEffect } from 'react';
import alertStyle from './page.module.scss';
import { useSourceApi } from '@/app/alarm/api/sources';
import { Spin, Empty } from 'antd';
import { useRouter } from 'next/navigation';
import { useTranslation } from '@/utils/i18n';
import { SourceItem } from '@/app/alarm/types/integration';

const IntegrationPage: React.FC = () => {
  const { getAlertSources } = useSourceApi();
  const [sources, setSources] = useState<SourceItem[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const { t } = useTranslation();
  const router = useRouter();

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
          <div className={alertStyle.container}>
            {sources.map((src: SourceItem) => (
              <div
                key={src.source_id}
                className={alertStyle.card}
                onClick={() =>
                  router.push(`/alarm/integration/detail?source_id=${src.id}`)
                }
              >
                <div className={alertStyle.cardContent}>
                  <div className="flex items-center gap-3 mb-2 px-8 py-4 rounded bg-[#99aaf2]">
                    <img
                      src={src.logo || ''}
                      alt={src.description}
                      className={alertStyle.logo}
                    />
                    <span className={alertStyle.name}>{src.name}</span>
                  </div>
                  <span className={alertStyle.info}>
                    {t('integration.eventCount')}：
                    {[undefined, null, ''].includes(src.event_count as any)
                      ? '--'
                      : src.event_count}
                  </span>
                  <span className={alertStyle.info}>
                    {t('integration.lastEventTime')}：
                    {src.last_event_time || '--'}
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

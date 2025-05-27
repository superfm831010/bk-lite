'use client';

import React, { useState, useEffect } from 'react';
import alertStyle from './page.module.scss';
import { useSourceApi } from '@/app/alarm/api/sources';
import { Drawer, message, Spin, Empty, Descriptions } from 'antd';
import { CopyOutlined } from '@ant-design/icons';
import { useTranslation } from '@/utils/i18n';
import { Source } from '@/app/alarm/types/integration';

const IntegrationPage: React.FC = () => {
  const { getAlertSources } = useSourceApi();
  const [sources, setSources] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [drawerVisible, setDrawerVisible] = useState<boolean>(false);
  const [selectedSource, setSelectedSource] = useState<Source | null>(null);
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

  const copySecret = (text: string) => {
    navigator.clipboard.writeText(text);
    message.success(t('common.copied'));
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
            {sources.map((src: Source) => (
              <div
                key={src.source_id}
                className={alertStyle.card}
                onClick={() => {
                  setSelectedSource(src);
                  setDrawerVisible(true);
                }}
              >
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

      <Drawer
        title={selectedSource?.name}
        placement="right"
        width={620}
        onClose={() => setDrawerVisible(false)}
        open={drawerVisible}
      >
        {selectedSource && (
          <>
            <h4 className="mb-2 font-medium pl-2 border-l-4 border-blue-400 inline-block leading-tight">
              {t('integration.baseInfo')}
            </h4>
            <Descriptions bordered size="small" column={1} labelStyle={{ width: 120 }}>
              <Descriptions.Item label="ID">
                {selectedSource.source_id}
              </Descriptions.Item>
              <Descriptions.Item label={t('integration.description')}>
                {selectedSource.description}
              </Descriptions.Item>
              <Descriptions.Item label={t('integration.secret')}>
                {'******************'}
                <CopyOutlined
                  className="ml-[10px]"
                  onClick={() => copySecret(selectedSource.secret)}
                />
              </Descriptions.Item>
            </Descriptions>

            <h4 className="mt-6 mb-2 font-medium pl-2 border-l-4 border-blue-400 inline-block leading-tight">
              {t('integration.eventFieldsMapping')}
            </h4>
            <Descriptions bordered size="small" column={1} labelStyle={{ width: 120 }}>
              {Object.entries(selectedSource.config.event_fields_mapping).map(
                ([field, val]) => (
                  <Descriptions.Item key={field} label={field}>
                    {val}
                  </Descriptions.Item>
                )
              )}
            </Descriptions>

            <h4 className="mt-6 mb-2 font-medium pl-2 border-l-4 border-blue-400 inline-block leading-tight">
              {t('integration.eventFieldsDescription')}
            </h4>
            <Descriptions bordered size="small" column={1} labelStyle={{ width: 120 }}>
              {Object.entries(selectedSource.config.event_fields_desc_mapping).map(
                ([field, desc]) => (
                  <Descriptions.Item key={field} label={field}>
                    {desc}
                  </Descriptions.Item>
                )
              )}
            </Descriptions>
          </>
        )}
      </Drawer>
    </div>
  );
};

export default IntegrationPage;

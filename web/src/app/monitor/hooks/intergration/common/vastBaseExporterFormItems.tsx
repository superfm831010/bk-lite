import React from 'react';
import { Form, Input, InputNumber, Select } from 'antd';
import { useTranslation } from '@/utils/i18n';
import Password from '@/app/monitor/components/password';
const { Option } = Select;
import {
  TIMEOUT_UNITS,
  CONNECTION_LIFETIME_UNITS,
} from '@/app/monitor/constants/monitor';

const useVastBaseExporterFormItems = () => {
  const { t } = useTranslation();

  return {
    getCommonFormItems: (mode?: 'manual' | 'auto' | 'edit') => {
      return (
        <>
          <Form.Item label={t('monitor.intergrations.username')} required>
            <Form.Item
              noStyle
              name={`${mode === 'auto' ? 'ENV_' : ''}SQL_EXPORTER_USER`}
              rules={[
                {
                  required: true,
                  message: t('common.required'),
                },
              ]}
            >
              <Input className="w-[300px] mr-[10px]" />
            </Form.Item>
            <span className="text-[12px] text-[var(--color-text-3)]">
              {t('monitor.intergrations.usernameDes')}
            </span>
          </Form.Item>
          <Form.Item label={t('monitor.intergrations.password')} required>
            <Form.Item
              noStyle
              name={`${mode === 'auto' ? 'ENV_' : ''}SQL_EXPORTER_PASS`}
              rules={[
                {
                  required: true,
                  message: t('common.required'),
                },
              ]}
            >
              <Password className="w-[300px] mr-[10px]" />
            </Form.Item>
            <span className="text-[12px] text-[var(--color-text-3)]">
              {t('monitor.intergrations.passwordDes')}
            </span>
          </Form.Item>
          <Form.Item label={t('monitor.intergrations.dbName')} required>
            <Form.Item
              noStyle
              name={`${mode === 'auto' ? 'ENV_' : ''}SQL_EXPORTER_DB_NAME`}
              rules={[
                {
                  required: true,
                  message: t('common.required'),
                },
              ]}
            >
              <Input className="w-[300px] mr-[10px]" />
            </Form.Item>
            <span className="text-[12px] text-[var(--color-text-3)]">
              {t('monitor.intergrations.dbNameDes')}
            </span>
          </Form.Item>
          <Form.Item label={t('monitor.intergrations.timeout')}>
            <Form.Item
              noStyle
              name={`${mode === 'auto' ? 'ENV_' : ''}SCRAPE_TIMEOUT`}
            >
              <InputNumber
                className="mr-[10px]"
                min={1}
                precision={0}
                addonAfter={
                  <Select style={{ width: 116 }} defaultValue="s">
                    {TIMEOUT_UNITS.map((item: string) => (
                      <Option key={item} value={item}>
                        {item}
                      </Option>
                    ))}
                  </Select>
                }
              />
            </Form.Item>
            <span className="text-[12px] text-[var(--color-text-3)]">
              {t('monitor.intergrations.timeoutDes')}
            </span>
          </Form.Item>
          <Form.Item label={t('monitor.intergrations.collectorRefs')} required>
            <Form.Item
              noStyle
              name={`${mode === 'auto' ? 'ENV_' : ''}COLLECTOR_REFS`}
              rules={[
                {
                  required: true,
                  message: t('common.required'),
                },
              ]}
            >
              <Input className="w-[300px] mr-[10px]" />
            </Form.Item>
            <span className="text-[12px] text-[var(--color-text-3)]">
              {t('monitor.intergrations.collectorRefsDes')}
            </span>
          </Form.Item>
          <Form.Item label={t('monitor.intergrations.connectionTime')}>
            <Form.Item
              noStyle
              name={`${mode === 'auto' ? 'ENV_' : ''}MAX_CONNECTION_LIFETIME`}
            >
              <InputNumber
                className="mr-[10px]"
                min={1}
                precision={0}
                addonAfter={
                  <Select style={{ width: 116 }} defaultValue="m">
                    {CONNECTION_LIFETIME_UNITS.map((item: string) => (
                      <Option key={item} value={item}>
                        {item}
                      </Option>
                    ))}
                  </Select>
                }
              />
            </Form.Item>
            <span className="text-[12px] text-[var(--color-text-3)]">
              {t('monitor.intergrations.connectionTimeDes')}
            </span>
          </Form.Item>
          <Form.Item label={t('monitor.intergrations.dbType')} required>
            <Form.Item
              noStyle
              name={`${mode === 'auto' ? 'ENV_' : ''}SQL_EXPORTER_DB_TYPE`}
              rules={[
                {
                  required: true,
                  message: t('common.required'),
                },
              ]}
            >
              <Input className="w-[300px] mr-[10px]" />
            </Form.Item>
            <span className="text-[12px] text-[var(--color-text-3)]">
              {t('monitor.intergrations.dbTypeDes')}
            </span>
          </Form.Item>
        </>
      );
    },
  };
};

export { useVastBaseExporterFormItems };

import React from 'react';
import { Form, Input, InputNumber, Select } from 'antd';
import { useTranslation } from '@/utils/i18n';
import Password from '@/app/monitor/components/password';
const { Option } = Select;
import { TIMEOUT_UNITS } from '@/app/monitor/constants/monitor';

const useRabbitMQExporterFormItems = () => {
  const { t } = useTranslation();

  return {
    getCommonFormItems: (mode?: 'manual' | 'auto' | 'edit') => {
      return (
        <>
          <Form.Item label={t('monitor.intergrations.username')} required>
            <Form.Item
              noStyle
              name={`${mode === 'auto' ? 'ENV_' : ''}RABBIT_USER`}
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
              name={`${mode === 'auto' ? 'ENV_' : ''}RABBIT_PASSWORD`}
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
          <Form.Item label={t('monitor.intergrations.condition')} required>
            <Form.Item
              noStyle
              name={`${mode === 'auto' ? 'ENV_' : ''}RABBIT_CONNECTION`}
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
              {t('monitor.intergrations.conditionDes')}
            </span>
          </Form.Item>
          <Form.Item required label={t('monitor.intergrations.timeout')}>
            <Form.Item
              noStyle
              name={`${mode === 'auto' ? 'ENV_' : ''}RABBIT_TIMEOUT`}
              rules={[
                {
                  required: true,
                  message: t('common.required'),
                },
              ]}
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
        </>
      );
    },
  };
};
export { useRabbitMQExporterFormItems };

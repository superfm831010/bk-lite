import React from 'react';

import { Form, Input } from 'antd';
import { useTranslation } from '@/utils/i18n';
// import { M_TIMEOUT_UNITS } from '@/app/log/constants';

const useFileVectorFormItems = () => {
  const { t } = useTranslation();

  return {
    getCommonFormItems: (disabledFormItems: Record<string, boolean> = {}) => {
      return (
        <>
          <Form.Item
            label={t('log.integration.filePath')}
            required={true}
            name="file_path"
            rules={[
              {
                required: true,
                message: t('common.required'),
              },
            ]}
          >
            <Input
              className="w-[300px] mr-[10px]"
              disabled={disabledFormItems.file_path}
            />
          </Form.Item>
          {/* <Form.Item
            label={
              <span className="w-[100px]">
                {t('log.integration.multiline')}
              </span>
            }
            name="multiline"
            rules={[
              ({ getFieldValue }) => ({
                validator() {
                  const multiline = getFieldValue('multiline') || {};
                  const hasAny = Object.values(multiline).some(
                    (v) => v && v !== ''
                  );
                  const hasAll =
                    multiline.start_pattern &&
                    multiline.condition_pattern &&
                    multiline.mode &&
                    multiline.timeout_ms;

                  if (hasAny && !hasAll) {
                    return Promise.reject(
                      new Error(t('log.integration.multilineAllRequired'))
                    );
                  }
                  return Promise.resolve();
                },
              }),
            ]}
          >
            <Form.Item
              className="mb-[10px]"
              name={['multiline', 'start_pattern']}
              layout="vertical"
            >
              <Input
                placeholder={t('log.integration.startPattern')}
                className="w-[300px]"
              />
            </Form.Item>
            <Form.Item
              className="mb-[10px]"
              name={['multiline', 'condition_pattern']}
              layout="vertical"
            >
              <Input
                placeholder={t('log.integration.conditionPattern')}
                className="w-[300px]"
              />
            </Form.Item>
            <Form.Item
              className="mb-[10px]"
              name={['multiline', 'mode']}
              layout="vertical"
            >
              <Select
                placeholder={t('log.integration.mode')}
                style={{ width: 300 }}
                options={[
                  { label: 'continue_past', value: 'continue_past' },
                  { label: 'continue_through', value: 'continue_through' },
                  { label: 'halt_before', value: 'halt_before' },
                  { label: 'halt_with', value: 'halt_with' },
                ]}
              />
            </Form.Item>
            <Form.Item
              className="mb-[10px]"
              name={['multiline', 'timeout_ms']}
              layout="vertical"
            >
              <InputNumber
                className="mr-[10px]"
                placeholder={t('log.integration.timeoutMs')}
                min={1}
                precision={0}
                addonAfter={
                  <Select style={{ width: 116 }} defaultValue="ms">
                    {M_TIMEOUT_UNITS.map((item: string) => (
                      <Option key={item} value={item}>
                        {item}
                      </Option>
                    ))}
                  </Select>
                }
              />
            </Form.Item>
          </Form.Item> */}
        </>
      );
    },
  };
};
export { useFileVectorFormItems };

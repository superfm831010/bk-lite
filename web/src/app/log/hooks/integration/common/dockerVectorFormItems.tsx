import React from 'react';
import { Form, Input } from 'antd';
import { useTranslation } from '@/utils/i18n';

const useDockerVectorFormItems = () => {
  const { t } = useTranslation();

  return {
    getCommonFormItems: (disabledFormItems: Record<string, boolean> = {}) => {
      return (
        <>
          <Form.Item
            label={t('log.integration.host')}
            required={true}
            name="docker_host"
            rules={[
              {
                required: true,
                message: t('common.required'),
              },
            ]}
          >
            <Input
              className="w-[300px] mr-[10px]"
              disabled={disabledFormItems.docker_host}
            />
          </Form.Item>
        </>
      );
    },
  };
};
export { useDockerVectorFormItems };

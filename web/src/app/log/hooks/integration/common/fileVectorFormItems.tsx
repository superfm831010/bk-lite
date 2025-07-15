import React from 'react';
import { Form, Input } from 'antd';
import { useTranslation } from '@/utils/i18n';

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
        </>
      );
    },
  };
};
export { useFileVectorFormItems };

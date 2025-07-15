import React from 'react';
import { Form, Input, Select } from 'antd';
import { useTranslation } from '@/utils/i18n';

const useDockerVectorFormItems = () => {
  const { t } = useTranslation();

  return {
    getCommonFormItems: (
      extra: {
        disabledFormItems: Record<string, boolean>;
        hiddenFormItems: Record<string, boolean>;
      } = {
        disabledFormItems: {},
        hiddenFormItems: {},
      }
    ) => {
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
              disabled={extra.disabledFormItems.docker_host}
            />
          </Form.Item>
          {!extra.hiddenFormItems.include_containers && (
            <Form.Item
              label={t('log.integration.includeContainers')}
              name="include_containers"
            >
              <Select
                mode="tags"
                style={{ width: '300px' }}
                placeholder={t('log.integration.containerPlaceholder')}
                disabled={extra.disabledFormItems.include_containers}
              />
            </Form.Item>
          )}
          {!extra.hiddenFormItems.exclude_containers && (
            <Form.Item
              label={t('log.integration.excludeContainers')}
              name="exclude_containers"
            >
              <Select
                mode="tags"
                style={{ width: '300px' }}
                placeholder={t('log.integration.containerPlaceholder')}
                disabled={extra.disabledFormItems.exclude_containers}
              />
            </Form.Item>
          )}
          {!extra.hiddenFormItems.start_pattern && (
            <Form.Item
              label={t('log.integration.startPattern')}
              name="start_pattern"
            >
              <Input
                className="w-[300px] mr-[10px]"
                disabled={extra.disabledFormItems.start_pattern}
              />
            </Form.Item>
          )}
        </>
      );
    },
  };
};
export { useDockerVectorFormItems };

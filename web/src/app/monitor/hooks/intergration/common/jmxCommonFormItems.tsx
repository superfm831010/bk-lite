import React from 'react';
import { Form, Input } from 'antd';
import { useTranslation } from '@/utils/i18n';
import Password from '@/app/monitor/components/password';

const useJmxCommonFormItems = () => {
  const { t } = useTranslation();

  return {
    getCommonFormItems: (disabledFormItems: Record<string, boolean> = {}) => {
      return (
        <>
          <Form.Item label={t('monitor.intergrations.username')}>
            <Form.Item noStyle name="username">
              <Input
                className="w-[300px] mr-[10px]"
                disabled={disabledFormItems.username}
              />
            </Form.Item>
            <span className="text-[12px] text-[var(--color-text-3)]">
              {t('monitor.intergrations.usernameDes')}
            </span>
          </Form.Item>
          <Form.Item label={t('monitor.intergrations.password')}>
            <Form.Item noStyle name="password">
              <Password
                className="w-[300px] mr-[10px]"
                disabled={disabledFormItems.password}
              />
            </Form.Item>
            <span className="text-[12px] text-[var(--color-text-3)]">
              {t('monitor.intergrations.passwordDes')}
            </span>
          </Form.Item>
        </>
      );
    },
  };
};
export { useJmxCommonFormItems };

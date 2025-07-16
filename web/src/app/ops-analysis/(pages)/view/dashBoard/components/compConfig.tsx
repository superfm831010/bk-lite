import React, { useEffect } from 'react';
import { Drawer, Button, Form, Input } from 'antd';
import { useTranslation } from '@/utils/i18n';
import { ComponentConfigProps } from '@/app/ops-analysis/types/dashBoard';
import { getWidgetConfig } from './registry';

const ComponentConfig: React.FC<ComponentConfigProps> = ({
  open,
  item,
  onConfirm,
  onClose,
}) => {
  const { t } = useTranslation();
  const [form] = Form.useForm();

  let WidgetConfigForm: any = null;
  if (item?.widget) {
    WidgetConfigForm = getWidgetConfig(item.widget);
    console.log('WidgetConfigForm:', WidgetConfigForm);
  }

  useEffect(() => {
    if (open && item) {
      form.setFieldsValue({
        name: item.title,
        ...(item.config || {}),
      });
    }
  }, [open, item, form]);

  const handleConfirm = async () => {
    try {
      const values = await form.validateFields();
      onConfirm?.(values);
    } catch (error) {
      console.error('Form validation failed:', error);
    }
  };

  return (
    <Drawer
      title={t('dashboard.componentConfig')}
      placement="right"
      width={640}
      open={open}
      onClose={onClose}
      footer={
        <div style={{ textAlign: 'right' }}>
          <Button type="primary" onClick={handleConfirm}>
            {t('common.confirm')}
          </Button>
          <Button style={{ marginLeft: 8 }} onClick={onClose}>
            {t('common.cancel')}
          </Button>
        </div>
      }
    >
      <Form form={form} labelCol={{ span: 4 }}>
        <Form.Item
          label={t('dashboard.widgetName')}
          name="name"
          rules={[{ required: true, message: t('dashboard.inputName') }]}
        >
          <Input placeholder={t('dashboard.inputName')} />
        </Form.Item>

        {(() => {
          if (item?.widget && WidgetConfigForm) {
            return <WidgetConfigForm form={form} />;
          }
          return null;
        })()}
      </Form>
    </Drawer>
  );
};

export default ComponentConfig;

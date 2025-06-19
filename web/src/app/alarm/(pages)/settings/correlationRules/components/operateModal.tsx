'use client';

import React, { useEffect } from 'react';
import type { AlertShieldListItem } from '@/app/alarm/types/settings';
import { Drawer, Form, Input, Button, Select } from 'antd';
import { useTranslation } from '@/utils/i18n';

interface OperateModalProps {
  open: boolean;
  currentRow?: AlertShieldListItem | null;
  onClose: () => void;
  onSuccess: (name: string) => void;
}

const OperateModal: React.FC<OperateModalProps> = ({
  open,
  currentRow,
  onClose,
  onSuccess,
}) => {
  const { t } = useTranslation();
  const [form] = Form.useForm();
  const selectedType = Form.useWatch('type', form);
  const imageMap: Record<string, string> = {
    dim_aggregate: '/app/dim_aggregate.png',
    biz_availability: '/app/biz_availability.png',
  };

  useEffect(() => {
    if (open) {
      if (currentRow) {
        form.setFieldsValue({ name: currentRow.name });
      } else {
        form.resetFields();
      }
    }
  }, [open, currentRow, form]);

  const handleFinish = (values: any) => {
    onSuccess(values.name);
    form.resetFields();
  };

  return (
    <Drawer
      title={
        currentRow
          ? `${t('settings.correlationRules')} - ${currentRow.name}`
          : t('settings.correlationRules')
      }
      width={720}
      open={open}
      onClose={onClose}
      footer={
        <div style={{ textAlign: 'right' }}>
          <Button onClick={onClose} style={{ marginRight: 8 }}>
            {t('common.cancel')}
          </Button>
          <Button type="primary" onClick={() => form.submit()}>
            {currentRow ? t('common.confirm') : t('common.confirm')}
          </Button>
        </div>
      }
    >
      <Form
        form={form}
        layout="horizontal"
        labelCol={{ span: 4 }}
        onFinish={handleFinish}
      >
        <Form.Item
          name="name"
          label={t('settings.assignName')}
          rules={[{ required: true, message: t('common.inputMsg') }]}
        >
          <Input placeholder={t('common.inputMsg')} />
        </Form.Item>

        <Form.Item
          name="type"
          label={t('settings.correlation.type')}
          rules={[{ required: true, message: t('common.selectMsg') }]}
        >
          <Select
            placeholder={t('common.selectMsg')}
            options={[
              { label: '对象维度聚合', value: 'dim_aggregate' },
              { label: '业务可用性-拨测', value: 'biz_availability' },
            ]}
          />
        </Form.Item>
        <Form.Item label={t('settings.correlation.explain')} className="mb-6">
          <div className="border border-gray-300 p-4 rounded-lg space-y-4">
            <div>
              <div className="font-medium mb-2">
                {t('settings.correlation.example')}
              </div>
              <img
                src={imageMap[selectedType] ?? ''}
                alt={selectedType}
                className="w-full h-auto"
              />
            </div>
            <div>
              <div className="font-medium mb-2">
                {t('settings.correlation.describe')}
              </div>
              <p>Mock description text to be replaced later.</p>
            </div>
          </div>
        </Form.Item>
        <Form.Item name="scope" label={t('settings.correlation.scope')}>
          <span>All</span>
        </Form.Item>
      </Form>
    </Drawer>
  );
};

export default OperateModal;

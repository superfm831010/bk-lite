'use client';

import React, { useEffect, useState } from 'react';
import type {
  AggregationRule,
  CorrelationRule,
} from '@/app/alarm/types/settings';
import { Drawer, Form, Input, Button, Select, message } from 'antd';
import { useTranslation } from '@/utils/i18n';
import { useSettingApi } from '@/app/alarm/api/settings';

interface OperateModalProps {
  open: boolean;
  currentRow?: CorrelationRule | null;
  onClose: () => void;
  onSuccess: () => void;
}

const OperateModal: React.FC<OperateModalProps> = ({
  open,
  currentRow,
  onClose,
  onSuccess,
}) => {
  const { t } = useTranslation();
  const [form] = Form.useForm();
  const [submitLoading, setSubmitLoading] = useState(false);
  const [aggOptions, setAggOptions] = useState<
    { label: string; value: string; id: number; disabled?: boolean }[]
  >([]);
  const [optionsLoading, setOptionsLoading] = useState(false);
  const selectedType = Form.useWatch('ruleId', form);
  const { getAggregationRule, createCorrelationRule, updateCorrelationRule } =
    useSettingApi();
  const locale = localStorage.getItem('locale') || 'en';
  const imageMap: Record<string, string> = {
    high_level_event_aggregation: '/app/high_level_event_aggregation.png',
    website_monitoring_alert: '/app/website_monitoring_alert.png',
  };

  useEffect(() => {
    if (open) {
      form.resetFields();
      fetchAggregationRule();
    }
  }, [open, form]);

  useEffect(() => {
    if (open && currentRow && aggOptions.length) {
      const initialRuleId = aggOptions.find(
        (opt) => opt.id === currentRow.aggregation_rules?.[0]
      )?.value;
      form.setFieldsValue({
        name: currentRow.name,
        ruleId: initialRuleId,
      });
    }
  }, [aggOptions, open, currentRow, form]);

  const fetchAggregationRule = async () => {
    setOptionsLoading(true);
    try {
      const res = await getAggregationRule({
        page: 1,
        page_size: 10000,
        type: 'alert',
      });
      setAggOptions(
        (res?.items || []).map((item: AggregationRule) => ({
          id: item.id,
          value: item.rule_id,
          label: locale === 'zh' ? item.description : item.name,
          disabled: !!item.correlation_name,
        }))
      );
    } catch {
      setAggOptions([]);
    } finally {
      setOptionsLoading(false);
    }
  };

  const handleFinish = async (values: any) => {
    setSubmitLoading(true);
    const selectedOpt = aggOptions.find((opt) => opt.value === values.ruleId);
    const params = {
      name: values.name,
      aggregation_rules: [selectedOpt?.id],
      scope: 'all',
      rule_type: 'alert',
    };
    try {
      if (currentRow?.id) {
        await updateCorrelationRule(currentRow.id, params);
        message.success(t('common.successOperate'));
      } else {
        await createCorrelationRule(params);
        message.success(t('common.successOperate'));
      }
      form.resetFields();
      onSuccess();
      onClose();
    } catch {
      message.error(t('common.operateFailed'));
    } finally {
      setSubmitLoading(false);
    }
  };

  return (
    <Drawer
      title={
        currentRow
          ? `${t('settings.correlationRules')} - ${currentRow.name}`
          : t('settings.correlationRules')
      }
      width={700}
      open={open}
      onClose={onClose}
      footer={
        <div>
          <Button
            type="primary"
            loading={submitLoading}
            style={{ marginRight: 8 }}
            onClick={() => form.submit()}
          >
            {t('common.confirm')}
          </Button>
          <Button onClick={onClose} disabled={submitLoading}>
            {t('common.cancel')}
          </Button>
        </div>
      }
    >
      <Form
        form={form}
        layout="horizontal"
        labelCol={{ span: 3 }}
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
          name="ruleId"
          label={t('settings.correlation.type')}
          rules={[{ required: true, message: t('common.selectMsg') }]}
        >
          <Select
            loading={optionsLoading}
            placeholder={t('common.selectMsg')}
            options={aggOptions}
            disabled={!!currentRow}
          />
        </Form.Item>
        {selectedType && imageMap[selectedType] ? (
          <Form.Item
            label={t('settings.correlation.explain')}
            className="ml-10"
            labelCol={{ span: 24 }}
          >
            <div className="border border-gray-300 p-4 rounded-lg space-y-4">
              <div>
                <div className="font-medium mb-2">
                  {t('settings.correlation.example')}
                </div>
                <img
                  src={imageMap[selectedType || 'high_level_event_aggregation']}
                  alt={selectedType}
                  className="w-full h-auto"
                />
              </div>
              <div>
                <div className="font-medium mb-2">
                  {t('settings.correlation.describe')}
                </div>
                <p style={{ whiteSpace: 'pre-line' }}>
                  {selectedType === 'high_level_event_aggregation'
                    ? t('settings.correlation.dimDescribeContent')
                    : t('settings.correlation.bizDescribeContent')}
                </p>
              </div>
            </div>
          </Form.Item>
        ) : null}
        <Form.Item name="scope" label={t('settings.correlation.scope')}>
          <span>{t('common.all')}</span>
        </Form.Item>
      </Form>
    </Drawer>
  );
};

export default OperateModal;

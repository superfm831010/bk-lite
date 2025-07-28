'use client';

import React, { useEffect, useState } from 'react';
import { useTranslation } from '@/utils/i18n';
import { useSettingApi } from '@/app/alarm/api/settings';
import type {
  AggregationRule,
  CorrelationRule,
} from '@/app/alarm/types/settings';
import {
  Drawer,
  Form,
  Input,
  Button,
  Select,
  Radio,
  InputNumber,
  message,
} from 'antd';

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
  const [optionsLoading, setOptionsLoading] = useState(false);
  const selectedType = Form.useWatch('ruleId', form);
  const windowType = Form.useWatch('windowType', form);
  const { getAggregationRule, createCorrelationRule, updateCorrelationRule } =
    useSettingApi();
  const [aggOptions, setAggOptions] = useState<
    {
      label: string;
      value: string;
      id: number;
      image: string;
      describeContent: string;
      disabled?: boolean;
    }[]
  >([]);

  const selOption = aggOptions.find((opt) => opt.value === selectedType);

  const locale = localStorage.getItem('locale') || 'en';

  const windowImageMap: Record<string, string> = {
    sliding: '/app/sliding_window.png',
    fixed: '/app/fixed_window.png',
    session: '/app/session_window.png',
  };

  useEffect(() => {
    if (open) {
      form.resetFields();
      fetchAggregationRule();
    }
  }, [open, form]);

  useEffect(() => {
    if (open && currentRow && aggOptions.length) {

      const winType = currentRow.window_type;
      let winTime: number | undefined;
      let waitTime: number | undefined;

      const initialRuleId = aggOptions.find(
        (opt) => opt.id === currentRow.aggregation_rules?.[0]
      )?.value;

      if (winType === 'session') {
        winTime = currentRow.session_timeout
          ? parseInt(currentRow.session_timeout, 10)
          : undefined;
        waitTime = currentRow.waiting_time
          ? parseInt(currentRow.waiting_time, 10)
          : undefined;
      } else {
        winTime = currentRow.window_size
          ? parseInt(currentRow.window_size, 10)
          : undefined;
      }
      form.setFieldsValue({
        name: currentRow.name,
        ruleId: initialRuleId,
        windowType: winType,
        windowTime: winTime,
        waitingTime: waitTime,
      });
    }
  }, [aggOptions, open, currentRow, form]);

  useEffect(() => {
    if (!currentRow && selectedType) {
      let defaultType = 'sliding';
      let defaultTime = 10;
      let defaultWaitingTime = 10;
      if (selectedType === 'critical_event_aggregation') {
        defaultType = 'fixed';
        defaultTime = 1;
      } else if (selectedType === 'error_scenario_handling') {
        defaultType = 'session';
        defaultTime = 10;
        defaultWaitingTime = 10;
      }
      form.setFieldsValue({
        windowType: defaultType,
        windowTime: defaultTime,
        waitingTime: defaultWaitingTime,
      });
    }
  }, [selectedType, form, currentRow]);

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
          label: item.name,
          image: item.image,
          describeContent:
            locale === 'en' ? item.description?.en : item.description?.zh,
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
    const apiWinType = values.windowType;
    const timeStr = `${values.windowTime}min`;
    const params: any = {
      name: values.name,
      aggregation_rules: [selectedOpt?.id],
      scope: 'all',
      rule_type: 'alert',
      window_type: apiWinType,
    };
    if (apiWinType === 'session') {
      params.session_timeout = timeStr;
      params.waiting_time = `${values.waitingTime}min`;
    } else {
      params.window_size = timeStr;
    }
    try {
      if (currentRow?.id) {
        await updateCorrelationRule(currentRow.id, params);
      } else {
        await createCorrelationRule(params);
      }
      message.success(t('alarmCommon.successOperate'));
      form.resetFields();
      onSuccess();
      onClose();
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
      width={720}
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
        labelCol={{ span: locale === 'en' ? 4 : 3 }}
        onFinish={handleFinish}
      >
        <Form.Item
          name="name"
          label={t('settings.assignName')}
          rules={[{ required: true, message: t('common.inputTip') }]}
        >
          <Input placeholder={t('common.inputTip')} />
        </Form.Item>

        <Form.Item
          name="ruleId"
          label={t('settings.correlation.type')}
          rules={[{ required: true, message: t('common.selectTip') }]}
        >
          <Select
            loading={optionsLoading}
            placeholder={t('common.selectTip')}
            options={aggOptions}
            disabled={!!currentRow || optionsLoading}
          />
        </Form.Item>

        {selOption && (
          <Form.Item
            className={`${locale === 'en' ? 'ml-28' : 'ml-20'} mt-[-10px]`}
            labelCol={{ span: 24 }}
          >
            <div className="border border-gray-300 p-4 rounded-lg space-y-4">
              <div>
                <div className="font-medium mb-2">
                  {t('settings.correlation.example')}
                </div>
                <img
                  src={selOption.image}
                  alt={selOption.value}
                  className="w-full h-auto"
                />
              </div>
              <div>
                <div className="font-medium mb-2">
                  {t('settings.correlation.describe')}
                </div>
                <p style={{ whiteSpace: 'pre-line', textIndent: '2ch' }}>
                  {selOption.describeContent}
                </p>
              </div>
            </div>
          </Form.Item>
        )}
        <Form.Item name="scope" label={t('settings.correlation.scope')}>
          <span>{t('alarmCommon.all')}</span>
        </Form.Item>
        <Form.Item
          name="windowType"
          label={t('settings.correlation.windowType')}
          initialValue="sliding"
          className="mb-2"
          rules={[{ required: true, message: t('common.selectTip') }]}
        >
          <Radio.Group>
            <Radio value="sliding">
              {t('settings.correlation.slidingWindow')}
            </Radio>
            <Radio value="fixed">{t('settings.correlation.fixedWindow')}</Radio>
            <Radio value="session">
              {t('settings.correlation.sessionWindow')}
            </Radio>
          </Radio.Group>
        </Form.Item>
        {windowType && windowImageMap[windowType] && (
          <Form.Item
            className={`${locale === 'en' ? 'ml-28' : 'ml-20'}`}
            labelCol={{ span: 24 }}
          >
            <div className="border border-gray-300 p-4 rounded-lg space-y-4">
              <div>
                <div className="font-medium mb-2">
                  {t('settings.correlation.example')}
                </div>
                <img
                  src={windowImageMap[windowType]}
                  alt={windowType}
                  className="w-full h-auto"
                />
              </div>
              <div>
                <div className="font-medium mb-2">
                  {t('settings.correlation.describe')}
                </div>
                <p style={{ whiteSpace: 'pre-line', textIndent: '2ch' }}>
                  {t(`settings.correlation.${windowType}Msg`)}
                </p>
              </div>
            </div>
          </Form.Item>
        )}
        <Form.Item
          name="windowTime"
          initialValue={10}
          rules={[{ required: true, message: t('common.inputTip') }]}
          label={
            windowType === 'session'
              ? t('settings.correlation.timeOut')
              : t('settings.correlation.windowTime')
          }
        >
          <InputNumber
            min={0}
            style={{ width: '140px' }}
            addonAfter={t('settings.correlation.min')}
          />
        </Form.Item>
        {windowType === 'session' && (
          <Form.Item
            name="waitingTime"
            initialValue={10}
            rules={[{ required: true, message: t('common.inputTip') }]}
            label={t('settings.correlation.waitingTime')}
          >
            <InputNumber
              min={0}
              style={{ width: '140px' }}
              addonAfter={t('settings.correlation.min')}
            />
          </Form.Item>
        )}
      </Form>
    </Drawer>
  );
};

export default OperateModal;

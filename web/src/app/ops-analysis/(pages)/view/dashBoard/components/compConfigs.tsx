import React, { useEffect, useState } from 'react';
import TimeSelector from '@/components/time-selector';
import dayjs from 'dayjs';
import { Form, Input, Radio } from 'antd';
import { useTranslation } from '@/utils/i18n';

interface WidgetConfigProps {
  form: any;
  initialValues?: any;
}

const FormTimeSelector: React.FC<{
  value?: any;
  onChange?: (value: any) => void;
}> = ({ value, onChange }) => {
  const [selectValue, setSelectValue] = useState(10080);
  const [rangeValue, setRangeValue] = useState<any>(null);

  useEffect(() => {
    if (value !== undefined) {
      if (Array.isArray(value)) {
        setSelectValue(0);
        setRangeValue(value);
      } else {
        setSelectValue(value);
        setRangeValue(null);
      }
    } else {
      onChange?.(10080);
    }
  }, [value, onChange]);

  const handleChange = (range: number[], originValue: number | null) => {
    if (originValue === 0) {
      setSelectValue(0);
      setRangeValue(range);
      onChange?.(range);
    } else if (originValue !== null) {
      setSelectValue(originValue);
      setRangeValue(null);
      onChange?.(originValue);
    }
  };

  const formatRangeValue = (value: any): [dayjs.Dayjs, dayjs.Dayjs] | null => {
    if (Array.isArray(value) && value.length === 2) {
      return [dayjs(value[0]), dayjs(value[1])];
    }
    return null;
  };

  return (
    <div className="w-[350px]">
      <TimeSelector
        onlyTimeSelect
        defaultValue={{
          selectValue: selectValue,
          rangePickerVaule: formatRangeValue(rangeValue),
        }}
        onChange={handleChange}
      />
    </div>
  );
};

// 公共的过滤配置组件
const FilterConfig: React.FC<{ form: any }> = ({ form }) => {
  const { t } = useTranslation();

  return (
    <div className="mb-6">
      <div className="font-bold text-[var(--color-text-1)] mb-4">
        {t('dashboard.filterSettings')}
      </div>
      <Form.Item
        label={t('dashboard.filterType')}
        name="filterType"
        initialValue="selector"
        rules={[{ required: true, message: t('common.selectMsg') }]}
      >
        <Radio.Group
          onChange={(e) => {
            if (e.target.value === 'selector') {
              form.setFieldValue('timeRange', undefined);
            } else {
              form.setFieldValue('timeRange', 10080);
            }
          }}
        >
          <Radio value="selector">{t('dashboard.selector')}</Radio>
          <Radio value="fixed">{t('dashboard.fixed')}</Radio>
        </Radio.Group>
      </Form.Item>

      <Form.Item
        noStyle
        shouldUpdate={(prevValues, currentValues) =>
          prevValues.filterType !== currentValues.filterType
        }
      >
        {() => {
          const filterType = form.getFieldValue('filterType');
          return filterType === 'fixed' ? (
            <Form.Item
              label={t('dashboard.timeRange')}
              name="timeRange"
              rules={[{ required: true, message: t('common.selectMsg') }]}
            >
              <FormTimeSelector />
            </Form.Item>
          ) : null;
        }}
      </Form.Item>
    </div>
  );
};

// 操作系统类型占比表单配置
export const OsPieConfig: React.FC<WidgetConfigProps> = ({ form }) => {
  return (
    <>
      <FilterConfig form={form} />
    </>
  );
};

// Alarm趋势/天表单配置
export const TrendLineConfig: React.FC<WidgetConfigProps> = ({ form }) => {
  const { t } = useTranslation();
  return (
    <>
      <div className="font-bold text-[var(--color-text-1)] mb-4">
        {t('dashboard.styleSettings')}
      </div>
      <Form.Item
        label={t('dashboard.lineColor')}
        name="lineColor"
        initialValue="#1890ff"
      >
        <Input type="color" style={{ width: 60, height: 32, padding: 2 }} />
      </Form.Item>

      <FilterConfig form={form} />
    </>
  );
};

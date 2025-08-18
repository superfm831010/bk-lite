import React, { useState, useEffect } from 'react';
import dayjs from 'dayjs';
import TimeSelector from '@/components/time-selector';
import { Form, Input, Select, DatePicker, Switch, InputNumber } from 'antd';
import { useTranslation } from '@/utils/i18n';
import { DatasourceItem, ParamItem } from '@/app/ops-analysis/types/dataSource';

const FormTimeSelector: React.FC<{
  value?: any;
  disabled?: boolean;
  onChange?: (value: any) => void;
}> = ({ value, disabled = false, onChange }) => {
  const [selectValue, setSelectValue] = useState(value ?? 10080);
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
    }
  }, [value]);

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
    <div
      className="w-full"
      style={disabled ? { pointerEvents: 'none', opacity: 0.6 } : undefined}
    >
      <TimeSelector
        onlyTimeSelect
        className="w-full"
        defaultValue={{
          selectValue: selectValue,
          rangePickerVaule: formatRangeValue(rangeValue),
        }}
        onChange={handleChange}
      />
    </div>
  );
};

interface DataSourceParamsConfigProps {
  selectedDataSource?: DatasourceItem;
  readonly?: boolean;
  includeFilterTypes?: string[]; // 需要显示的参数类型，默认显示所有
  fieldPrefix?: string; // 字段前缀，默认为 'params'
  form?: any; // 可选的外部 Form 实例
  preserveValues?: boolean; // 是否保持已有的表单值，默认 false
}

const DataSourceParamsConfig: React.FC<DataSourceParamsConfigProps> = ({
  selectedDataSource,
  readonly = false,
  includeFilterTypes = ['params', 'fixed', 'filter'],
  fieldPrefix = 'params',
  preserveValues = false,
}) => {
  const { t } = useTranslation();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (
    !selectedDataSource?.params ||
    !Array.isArray(selectedDataSource.params) ||
    selectedDataSource.params.length === 0
  ) {
    return null;
  }

  // 过滤需要配置的参数
  const configParams = selectedDataSource.params.filter((param: ParamItem) =>
    includeFilterTypes.includes(param.filterType || 'fixed')
  );

  if (configParams.length === 0) {
    return null;
  }

  const renderParamInput = (param: ParamItem) => {
    const { type = 'string', filterType, options } = param;
    const isDisabled = readonly || filterType === 'fixed';

    // 如果有选项，显示下拉选择器
    if (options && Array.isArray(options) && options.length > 0) {
      return (
        <Select
          placeholder={t('common.selectTip')}
          style={{ width: '100%' }}
          disabled={isDisabled}
          options={options}
        />
      );
    }

    switch (type) {
      case 'timeRange':
        return <FormTimeSelector disabled={isDisabled} />;
      case 'date':
        return (
          <DatePicker
            showTime
            placeholder={t('common.selectTip')}
            style={{ width: '100%' }}
            format="YYYY-MM-DD HH:mm:ss"
            disabled={isDisabled}
          />
        );
      case 'boolean':
        return <Switch disabled={isDisabled} />;
      case 'number':
        return (
          <InputNumber
            placeholder={t('common.inputTip')}
            style={{ width: '100%' }}
            disabled={isDisabled}
          />
        );
      case 'string':
      default:
        return (
          <Input
            placeholder={t('common.inputTip')}
            style={{ width: '100%' }}
            disabled={isDisabled}
          />
        );
    }
  };

  const getParamInitialValue = (param: ParamItem) => {
    const { type = 'string', value } = param;

    switch (type) {
      case 'boolean':
        return value ?? false;
      case 'number':
        return value ?? 0;
      case 'timeRange':
        return value ?? 10080; // 默认7天（10080分钟）
      case 'date':
        return value ? dayjs(value) : null; // 转换为dayjs对象
      case 'string':
      default:
        return value ?? '';
    }
  };

  return (
    <>
      {configParams.map((param: ParamItem) => {
        const fieldName = [fieldPrefix, param.name];
        const initialValue = getParamInitialValue(param);

        return (
          <Form.Item
            key={`${selectedDataSource?.id || 'default'}-${param.name}`} 
            label={param.alias_name || param.name}
            name={fieldName}
            initialValue={!preserveValues && mounted ? initialValue : undefined} // 只在初次挂载且不保持值时设置初始值
            tooltip={param.desc || undefined}
            rules={[
              {
                required: param.required,
                message: `请配置${param.alias_name || param.name}`,
              },
            ]}
          >
            {renderParamInput(param)}
          </Form.Item>
        );
      })}
    </>
  );
};

export default DataSourceParamsConfig;

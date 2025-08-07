import React, { useEffect, useState } from 'react';
import dayjs from 'dayjs';
import TimeSelector from '@/components/time-selector';
import { useTranslation } from '@/utils/i18n';
import { ComponentConfigProps } from '@/app/ops-analysis/types/dashBoard';
import { useDataSourceApi } from '@/app/ops-analysis/api/dataSource';
import { DatasourceItem, ParamItem } from '@/app/ops-analysis/types/dataSource';
import {
  Drawer,
  Button,
  Form,
  Input,
  Select,
  Radio,
  Switch,
  DatePicker,
} from 'antd';

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
    <div className="w-full">
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

const DataSourceSelect: React.FC<{
  loading?: boolean;
  placeholder?: string;
  style?: any;
  value?: any;
  disabled?: boolean;
  dataSources?: DatasourceItem[];
  onChange?: (value: any) => void;
  onDataSourceChange?: (dataSource: DatasourceItem | undefined) => void;
}> = ({
  loading = false,
  placeholder,
  style = { width: '100%' },
  value,
  disabled = false,
  dataSources = [],
  onChange,
  onDataSourceChange,
}) => {
  const formatOptions = (sources: DatasourceItem[]) => {
    return sources.map((item) => ({
      label: `${item.name}（${item.rest_api}）`,
      value: item.id,
      title: item.desc,
    }));
  };

  const handleChange = (val: any) => {
    onChange?.(val);
    const selectedSource = dataSources.find((item) => item.id === val);
    onDataSourceChange?.(selectedSource);
  };

  return (
    <Select
      loading={loading}
      options={formatOptions(dataSources)}
      placeholder={placeholder}
      style={style}
      value={value}
      disabled={disabled}
      onChange={handleChange}
    />
  );
};

const DynamicParamsConfig: React.FC<{
  selectedDataSource?: DatasourceItem;
}> = ({ selectedDataSource }) => {
  const { t } = useTranslation();

  if (
    !selectedDataSource?.params ||
    !Array.isArray(selectedDataSource.params) ||
    selectedDataSource.params.length === 0
  ) {
    return null;
  }

  // 筛选出需要配置的参数
  const configParams = selectedDataSource.params.filter(
    (param: ParamItem) => param.filterType === 'params'
  );

  if (configParams.length === 0) {
    return null;
  }

  const renderParamInput = (param: ParamItem) => {
    const { type = 'string' } = param;

    switch (type) {
      case 'timeRange':
        return <FormTimeSelector />;
      case 'date':
        return (
          <DatePicker
            showTime
            placeholder={t('common.selectTip')}
            style={{ width: '100%' }}
            format="YYYY-MM-DD HH:mm:ss"
          />
        );
      case 'boolean':
        return <Switch />;
      case 'number':
        return (
          <Input
            type="number"
            placeholder={t('common.inputTip')}
            style={{ width: '100%' }}
          />
        );
      case 'string':
      default:
        return (
          <Input placeholder={t('common.inputTip')} style={{ width: '100%' }} />
        );
    }
  };

  const getParamInitialValue = (param: ParamItem) => {
    const { type = 'string', value, userValue } = param;
    // 优先使用用户配置的值，如果没有则使用默认值
    const finalValue = userValue !== undefined ? userValue : value;

    switch (type) {
      case 'boolean':
        return finalValue ?? false;
      case 'number':
        return finalValue ?? 0;
      case 'timeRange':
        return finalValue ?? 10080; // 默认7天（10080分钟）
      case 'date':
        return finalValue ? dayjs(finalValue) : null; // 转换为dayjs对象
      case 'string':
      default:
        return finalValue ?? '';
    }
  };

  return (
    <div className="mb-6">
      <div className="font-bold text-[var(--color-text-1)] mb-4">
        {t('dashboard.paramSettings')}
      </div>
      {configParams.map((param: ParamItem) => {
        return (
          <Form.Item
            key={param.name}
            label={param.alias_name || param.name}
            name={['params', param.name]}
            initialValue={getParamInitialValue(param)}
            tooltip={param.desc || undefined}
          >
            {renderParamInput(param)}
          </Form.Item>
        );
      })}
    </div>
  );
};

const ComponentConfig: React.FC<ComponentConfigProps> = ({
  open,
  item,
  onConfirm,
  onClose,
}) => {
  const { t } = useTranslation();
  const [form] = Form.useForm();
  const [dataSources, setDataSources] = useState<DatasourceItem[]>([]);
  const [dataSourcesLoading, setDataSourcesLoading] = useState(false);
  const [selectedDataSource, setSelectedDataSource] = useState<
    DatasourceItem | undefined
  >();
  const { getDataSourceList } = useDataSourceApi();

  useEffect(() => {
    const fetchDataSources = async () => {
      try {
        setDataSourcesLoading(true);
        const data: DatasourceItem[] = await getDataSourceList();
        setDataSources(data || []);
      } catch (error) {
        console.error('获取数据源失败:', error);
        setDataSources([]);
      } finally {
        setDataSourcesLoading(false);
      }
    };
    fetchDataSources();
  }, []);

  useEffect(() => {
    if (open && item && dataSources.length > 0) {
      const formValues: any = {
        name: item.title,
        ...(item.config || {}),
      };

      let targetDataSource: DatasourceItem | undefined;

      if (formValues.dataSource) {
        targetDataSource = dataSources.find(
          (ds) => ds.id === formValues.dataSource
        );
      } else if (item.widget === 'trendLine') {
        targetDataSource = dataSources.find(
          (el: DatasourceItem) => el.rest_api === 'alert/get_alert_trend_data'
        );
        if (targetDataSource) {
          formValues.dataSource = targetDataSource.id;
        }
        formValues.chartType = 'line';
      } else if (item.widget === 'osPie') {
        formValues.chartType = 'pie';
      }
      // 设置选中的数据源
      if (targetDataSource) {
        setSelectedDataSource(targetDataSource);

        if (
          item.config?.params &&
          targetDataSource.params &&
          Array.isArray(targetDataSource.params)
        ) {
          const paramsValues = { ...item.config.params };

          // 处理日期类型的参数，转换为dayjs对象
          targetDataSource.params.forEach((param) => {
            if (param.type === 'date' && paramsValues[param.name]) {
              paramsValues[param.name] = dayjs(paramsValues[param.name]);
            }
          });

          formValues.params = paramsValues;
        }
      } else {
        setSelectedDataSource(undefined);
      }

      form.setFieldsValue(formValues);
    } else if (!open) {
      form.resetFields();
      setSelectedDataSource(undefined);
    }
  }, [open, item, form, dataSources]);

  const handleConfirm = async () => {
    try {
      const values = await form.validateFields();

      if (
        values.params &&
        selectedDataSource?.params &&
        Array.isArray(selectedDataSource.params)
      ) {
        const processedParams = { ...values.params };
        selectedDataSource.params.forEach((param) => {
          if (
            param.type === 'date' &&
            processedParams[param.name] !== undefined
          ) {
            // DatePicker 返回的是 dayjs 对象，需要转换为字符串
            const dateValue = processedParams[param.name];
            if (dateValue && typeof dateValue.format === 'function') {
              processedParams[param.name] = dateValue.format(
                'YYYY-MM-DD HH:mm:ss'
              );
            }
          }
        });
        values.params = processedParams;
      }

      // 保存数据源参数配置，供 useWidgetData 使用
      if (selectedDataSource?.params) {
        const dataSourceParams = selectedDataSource.params.map((param) => {
          // 如果用户配置了参数值，将其保存到 userValue 字段
          const userValue = values.params?.[param.name];
          return {
            ...param,
            userValue: userValue !== undefined ? userValue : param.userValue,
          };
        });
        values.dataSourceParams = dataSourceParams;
      }

      // 删除 params 字段，统一使用 dataSourceParams
      delete values.params;

      onConfirm?.(values);
    } catch (error) {
      console.error('Form validation failed:', error);
    }
  };

  return (
    <Drawer
      title={t('dashboard.componentConfig')}
      placement="right"
      width={600}
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
        <div className="mb-6">
          <div className="font-bold text-[var(--color-text-1)] mb-4">
            {t('dashboard.basicSettings')}
          </div>
          <Form.Item
            label={t('dashboard.widgetName')}
            name="name"
            rules={[{ required: true, message: t('dashboard.inputName') }]}
          >
            <Input placeholder={t('dashboard.inputName')} />
          </Form.Item>
        </div>

        {/* 数据源部分 */}
        <div className="mb-6">
          <div className="font-bold text-[var(--color-text-1)] mb-4">
            {t('dashboard.dataSource')}
          </div>
          <Form.Item
            label={t('dashboard.dataSourceType')}
            name="dataSource"
            rules={[{ required: true, message: t('common.selectTip') }]}
          >
            <DataSourceSelect
              placeholder={t('common.selectTip')}
              disabled={item?.widget === 'trendLine'}
              dataSources={dataSources}
              loading={dataSourcesLoading}
              onDataSourceChange={setSelectedDataSource}
            />
          </Form.Item>
        </div>

        {/* 动态参数配置 */}
        <DynamicParamsConfig selectedDataSource={selectedDataSource} />

        {/* 图表类型部分 */}
        <div className="mb-6">
          <div className="font-bold text-[var(--color-text-1)] mb-4">
            {t('dashboard.chartType')}
          </div>
          <Form.Item
            label={t('dashboard.chartTypeLabel')}
            name="chartType"
            rules={[{ required: true, message: t('common.selectTip') }]}
            initialValue="line"
          >
            <Radio.Group
              disabled={['trendLine', 'osPie'].includes(item?.widget || '')}
            >
              <Radio.Button value="line">
                {t('dashboard.lineChart')}
              </Radio.Button>
              <Radio.Button value="bar">{t('dashboard.barChart')}</Radio.Button>
              <Radio.Button value="pie">{t('dashboard.pieChart')}</Radio.Button>
            </Radio.Group>
          </Form.Item>
        </div>
      </Form>
    </Drawer>
  );
};

export default ComponentConfig;

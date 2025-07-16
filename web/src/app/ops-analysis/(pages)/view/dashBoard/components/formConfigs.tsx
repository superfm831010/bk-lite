import React, { useEffect, useState } from 'react';
import { Form, Input, Select, Radio, DatePicker } from 'antd';
import { useTranslation } from '@/utils/i18n';
import { useDashBoardApi } from '@/app/ops-analysis/api/dashBoard';

const { RangePicker } = DatePicker;

interface WidgetConfigProps {
  form: any;
  initialValues?: any;
}

const DataSourceSelect: React.FC<{
  placeholder?: string;
  style?: any;
  value?: any;
  onChange?: (value: any) => void;
}> = ({ placeholder, style = { width: 200 }, value, onChange }) => {
  const [dataSources, setDataSources] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const { getDataSources } = useDashBoardApi();

  useEffect(() => {
    const fetchDataSources = async () => {
      try {
        setLoading(true);
        const response: any = await getDataSources();
        setDataSources(response.data);
      } catch (error) {
        console.error('获取数据源失败:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDataSources();
  }, []);

  return (
    <Select
      loading={loading}
      options={dataSources}
      placeholder={placeholder}
      style={style}
      value={value}
      onChange={onChange}
    />
  );
};

const DataSourceAttrSelect: React.FC<{
  placeholder?: string;
  style?: any;
  value?: any;
  onChange?: (value: any) => void;
  dataSourceValue?: string;
}> = ({
  placeholder,
  style = { width: 200 },
  value,
  onChange,
  dataSourceValue,
}) => {
  const [attrs, setAttrs] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const { getDataSourceAttrs } = useDashBoardApi();

  useEffect(() => {
    if (!dataSourceValue) {
      setAttrs([]);
      return;
    }

    const fetchAttrs = async () => {
      try {
        setLoading(true);
        const response: any = await getDataSourceAttrs(dataSourceValue);
        setAttrs(response.data);
      } catch (error) {
        console.error('获取数据源属性失败:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAttrs();
  }, [dataSourceValue]);

  return (
    <Select
      loading={loading}
      options={attrs}
      placeholder={placeholder}
      style={style}
      value={value}
      onChange={onChange}
      disabled={!dataSourceValue}
    />
  );
};

// 操作系统类型占比
export const OsPieConfig: React.FC<WidgetConfigProps> = () => {
  const { t } = useTranslation();
  return (
    <>
      <Form.Item
        label={t('dashboard.dataSource')}
        name="dataSource"
        rules={[{ required: true, message: t('dashboard.selectDataSource') }]}
      >
        <DataSourceSelect placeholder={t('dashboard.selectDataSource')} />
      </Form.Item>

      <Form.Item
        noStyle
        shouldUpdate={(prev, current) => prev.dataSource !== current.dataSource}
      >
        {({ getFieldValue }) => {
          const dataSourceValue = getFieldValue('dataSource');
          return (
            <Form.Item
              label="数据源属性"
              name="dataSourceAttr"
              rules={[{ required: true, message: '请选择数据源属性' }]}
            >
              <DataSourceAttrSelect
                placeholder="请选择数据源属性"
                dataSourceValue={dataSourceValue}
              />
            </Form.Item>
          );
        }}
      </Form.Item>
    </>
  );
};

// Alarm趋势/天
export const TrendLineConfig: React.FC<WidgetConfigProps> = () => {
  const { t } = useTranslation();

  return (
    <>
      <Form.Item
        label={t('dashboard.dataSource')}
        name="dataSource"
        rules={[{ required: true, message: t('dashboard.selectDataSource') }]}
      >
        <DataSourceSelect placeholder={t('dashboard.selectDataSource')} />
      </Form.Item>

      <Form.Item
        noStyle
        shouldUpdate={(prev, current) => prev.dataSource !== current.dataSource}
      >
        {({ getFieldValue }) => {
          const dataSourceValue = getFieldValue('dataSource');
          return (
            <Form.Item
              label="数据源属性"
              name="dataSourceAttr"
              rules={[{ required: true, message: '请选择数据源属性' }]}
            >
              <DataSourceAttrSelect
                placeholder="请选择数据源属性"
                dataSourceValue={dataSourceValue}
              />
            </Form.Item>
          );
        }}
      </Form.Item>

      <Form.Item
        label={t('dashboard.lineColor')}
        name="lineColor"
        initialValue="#1890ff"
      >
        <Input type="color" style={{ width: 60, height: 32, padding: 2 }} />
      </Form.Item>

      <Form.Item
        label={t('dashboard.filterType')}
        name="filterType"
        initialValue="selector"
        rules={[{ required: true }]}
      >
        <Radio.Group>
          <Radio value="selector">{t('dashboard.selector')}</Radio>
          <Radio value="fixed">{t('dashboard.fixed')}</Radio>
        </Radio.Group>
      </Form.Item>

      <Form.Item
        noStyle
        shouldUpdate={(prev, current) => prev.filterType !== current.filterType}
      >
        {({ getFieldValue }) => {
          if (getFieldValue('filterType') === 'fixed') {
            return (
              <Form.Item
                label={t('dashboard.timeRange')}
                name="timeRange"
                rules={[{ required: true }]}
              >
                <RangePicker showTime />
              </Form.Item>
            );
          }
          return null;
        }}
      </Form.Item>
    </>
  );
};

import React, { useEffect, useState } from 'react';
import { Drawer, Button, Form, Input, Select, Radio } from 'antd';
import { useTranslation } from '@/utils/i18n';
import { ComponentConfigProps } from '@/app/ops-analysis/types/dashBoard';
import { getWidgetConfig } from './registry';
import { useDataSourceApi } from '@/app/ops-analysis/api/dataSource';
import { DatasourceItem } from '@/app/ops-analysis/types/dataSource';

const DataSourceSelect: React.FC<{
  placeholder?: string;
  style?: any;
  value?: any;
  onChange?: (value: any) => void;
}> = ({ placeholder, style = { width: '100%' }, value, onChange }) => {
  const [dataSources, setDataSources] = useState<DatasourceItem[]>([]);
  const [loading, setLoading] = useState(false);
  const { getDataSourceList } = useDataSourceApi();

  useEffect(() => {
    const fetchDataSources = async () => {
      try {
        setLoading(true);
        const data: any = await getDataSourceList();
        setDataSources(data || []);
      } catch (error) {
        console.error('获取数据源失败:', error);
        setDataSources([]);
      } finally {
        setLoading(false);
      }
    };

    fetchDataSources();
  }, []);

  const formatOptions = (sources: DatasourceItem[]) => {
    return sources.map((item) => ({
      label: `${item.name}（${item.rest_api}）`,
      value: item.id,
      title: item.desc,
    }));
  };

  return (
    <Select
      loading={loading}
      options={formatOptions(dataSources)}
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
  dataSourceValue?: string;
  onChange?: (value: any) => void;
}> = ({
  placeholder,
  style = { width: '100%' },
  value,
  dataSourceValue,
  onChange,
}) => {
  const [attrs, setAttrs] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const { getDataSourceAttrs } = useDataSourceApi();

  useEffect(() => {
    if (!dataSourceValue) {
      setAttrs([]);
      return;
    }
    const fetchAttrs = async () => {
      try {
        setLoading(true);
        const response: any = await getDataSourceAttrs(dataSourceValue);
        setAttrs(response.data || []);
      } catch (error) {
        console.error('获取数据源属性失败:', error);
        setAttrs([]);
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
  }

  useEffect(() => {
    if (open && item) {
      form.setFieldsValue({
        name: item.title,
        ...(item.config || {}),
      });
    } else {
      form.resetFields();
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
        <div className="mb-6">
          <div className="font-bold text-gray-800 mb-4">
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
          <div className="font-bold text-gray-800 mb-4">
            {t('dashboard.dataSource')}
          </div>
          <Form.Item
            label={t('dashboard.dataSourceType')}
            name="dataSource"
            rules={[
              { required: true, message: t('dashboard.selectDataSource') },
            ]}
          >
            <DataSourceSelect placeholder={t('dashboard.selectDataSource')} />
          </Form.Item>
          <Form.Item
            noStyle
            shouldUpdate={(prev, current) =>
              prev.dataSource !== current.dataSource
            }
          >
            {({ getFieldValue }) => {
              const dataSourceValue = getFieldValue('dataSource');
              return (
                <Form.Item
                  label={t('dashboard.dataSourceAttr')}
                  name="dataSourceAttr"
                  rules={[{ required: true, message: t('common.selectMsg') }]}
                >
                  <DataSourceAttrSelect
                    placeholder={t('common.selectMsg')}
                    dataSourceValue={dataSourceValue}
                  />
                </Form.Item>
              );
            }}
          </Form.Item>
        </div>

        {/* 图表类型部分 */}
        <div className="mb-6">
          <div className="font-bold text-gray-800 mb-4">
            {t('dashboard.chartType')}
          </div>
          <Form.Item
            label={t('dashboard.chartTypeLabel')}
            name="chartType"
            rules={[
              { required: true, message: t('dashboard.selectChartType') },
            ]}
            initialValue="line"
          >
            <Radio.Group>
              <Radio.Button value="line">
                {t('dashboard.lineChart')}
              </Radio.Button>
              <Radio.Button value="bar">{t('dashboard.barChart')}</Radio.Button>
              <Radio.Button value="pie">{t('dashboard.pieChart')}</Radio.Button>
            </Radio.Group>
          </Form.Item>
        </div>

        {item?.widget && WidgetConfigForm && <WidgetConfigForm form={form} />}
      </Form>
    </Drawer>
  );
};

export default ComponentConfig;

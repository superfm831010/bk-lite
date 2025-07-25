import React, { useEffect, useState } from 'react';
import { Drawer, Button, Form, Input, Select, Radio } from 'antd';
import { useTranslation } from '@/utils/i18n';
import { ComponentConfigProps } from '@/app/ops-analysis/types/dashBoard';
import { getWidgetConfig } from './registry';
import { useDataSourceApi } from '@/app/ops-analysis/api/dataSource';
import { DatasourceItem } from '@/app/ops-analysis/types/dataSource';

const DataSourceSelect: React.FC<{
  loading?: boolean;
  placeholder?: string;
  style?: any;
  value?: any;
  disabled?: boolean;
  dataSources?: DatasourceItem[];
  onChange?: (value: any) => void;
}> = ({
  loading = false,
  placeholder,
  style = { width: '100%' },
  value,
  disabled = false,
  dataSources = [],
  onChange,
}) => {
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
      disabled={disabled}
      onChange={onChange}
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
  const [dataSources, setDataSources] = useState<DatasourceItem[]>([]);
  const [dataSourcesLoading, setDataSourcesLoading] = useState(false);
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
    if (open && item) {
      const formValues: any = {
        name: item.title,
        ...(item.config || {}),
      };

      if (item.widget === 'trendLine') {
        const targetDataSource = dataSources.find(
          (el: DatasourceItem) => el.rest_api === 'alert/get_alert_trend_data'
        );
        if (targetDataSource) {
          formValues.dataSource = targetDataSource.id;
        }
        formValues.chartType = 'line';
      } else if (item.widget === 'osPie') {
        formValues.chartType = 'pie';
      }
      form.setFieldsValue(formValues);
    } else {
      form.resetFields();
    }
  }, [open, item, form, dataSources]);

  const handleConfirm = async () => {
    try {
      const values = await form.validateFields();
      onConfirm?.(values);
    } catch (error) {
      console.error('Form validation failed:', error);
    }
  };

  let WidgetConfigForm: any = null;
  if (item?.widget) {
    WidgetConfigForm = getWidgetConfig(item.widget);
  }

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
            rules={[{ required: true, message: t('common.selectMsg') }]}
          >
            <DataSourceSelect
              placeholder={t('common.selectMsg')}
              disabled={item?.widget === 'trendLine'}
              dataSources={dataSources}
              loading={dataSourcesLoading}
            />
          </Form.Item>
        </div>

        {/* 图表类型部分 */}
        <div className="mb-6">
          <div className="font-bold text-[var(--color-text-1)] mb-4">
            {t('dashboard.chartType')}
          </div>
          <Form.Item
            label={t('dashboard.chartTypeLabel')}
            name="chartType"
            rules={[{ required: true, message: t('common.selectMsg') }]}
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

        {item?.widget && WidgetConfigForm && <WidgetConfigForm form={form} />}
      </Form>
    </Drawer>
  );
};

export default ComponentConfig;

import React, { useEffect } from 'react';
import { useTranslation } from '@/utils/i18n';
import {
  ViewConfigProps,
  LayoutItem,
} from '@/app/ops-analysis/types/dashBoard';
import { TopologyNodeData } from '@/app/ops-analysis/types/topology';
import { useDataSourceManager } from '@/app/ops-analysis/hooks/useDataSource';
import { Drawer, Button, Form, Input, Radio } from 'antd';
import DataSourceParamsConfig from '@/app/ops-analysis/components/paramsConfig';
import DataSourceSelect from '@/app/ops-analysis/components/dataSourceSelect';

const ViewConfig: React.FC<ViewConfigProps> = ({
  open,
  item: widgetItem,
  onConfirm,
  onClose,
}) => {
  const { t } = useTranslation();
  const [form] = Form.useForm();
  const {
    dataSources,
    dataSourcesLoading,
    selectedDataSource,
    setSelectedDataSource,
    findDataSource,
    setDefaultParamValues,
    restoreUserParamValues,
    processFormParamsForSubmit,
  } = useDataSourceManager();

  const isTopologyFormat = (item: any): item is TopologyNodeData => {
    return item && 'type' in item && item.type === 'chart';
  };

  const isDashboardFormat = (item: any): item is LayoutItem => {
    return item && 'i' in item && 'widget' in item;
  };

  const extractItemConfig = (item: any) => {
    if (isTopologyFormat(item)) {
      return {
        name: item.name,
        widget: item.widget,
        dataSource: item.dataSource || item.valueConfig?.dataSource,
        chartType: item.valueConfig?.chartType,
        dataSourceParams:
          item.dataSourceParams || item.valueConfig?.dataSourceParams || [],
        ...item.valueConfig,
      };
    } else if (isDashboardFormat(item)) {
      return {
        name: item.config?.name || item.title,
        widget: item.widget,
        dataSource: item.config?.dataSource,
        chartType: item.config?.chartType,
        dataSourceParams: item.config?.dataSourceParams || [],
        ...item.config,
      };
    }
    return {
      name: '',
      widget: '',
      dataSource: undefined,
      chartType: 'line',
      dataSourceParams: [],
    };
  };

  const initializeNewItemForm = (widget: string): void => {
    const formValues: any = {
      name: '',
      chartType: 'line',
    };
    if (widget === 'trendLine') {
      const trendDataSource = dataSources.find(
        (ds) => ds.rest_api === 'alert/get_alert_trend_data'
      );
      if (trendDataSource) {
        formValues.dataSource = trendDataSource.id;
        setSelectedDataSource(trendDataSource);
      }
      formValues.chartType = 'line';
    } else if (widget === 'errorBar') {
      formValues.chartType = 'bar';
    } else if (widget === 'osPie') {
      formValues.chartType = 'pie';
    }

    form.setFieldsValue(formValues);
  };

  const initializeEditItemForm = (widgetItem: any): void => {
    const itemConfig = extractItemConfig(widgetItem);

    const formValues: any = {
      ...itemConfig,
      name: itemConfig.name || '',
      chartType: itemConfig.chartType || 'line',
      dataSource: itemConfig.dataSource,
    };

    const targetDataSource = findDataSource(
      itemConfig.widget || '',
      itemConfig.dataSource
    );

    if (targetDataSource) {
      setSelectedDataSource(targetDataSource);

      formValues.params = formValues.params || {};

      if (targetDataSource.params?.length) {
        setDefaultParamValues(targetDataSource.params, formValues.params);

        if (itemConfig.dataSourceParams?.length) {
          restoreUserParamValues(
            itemConfig.dataSourceParams,
            formValues.params
          );
        }
      }
    } else {
      setSelectedDataSource(undefined);
    }

    form.setFieldsValue(formValues);
  };

  const initializeFormValues = (): void => {
    if (dataSources.length === 0) return;

    const isNewItem =
      !widgetItem ||
      (isDashboardFormat(widgetItem) && !widgetItem.title) ||
      (isTopologyFormat(widgetItem) && !widgetItem.name);

    if (isNewItem) {
      const widget = widgetItem?.widget || '';
      initializeNewItemForm(widget);
    } else {
      initializeEditItemForm(widgetItem);
    }
  };

  const resetForm = (): void => {
    form.resetFields();
    setSelectedDataSource(undefined);
  };

  useEffect(() => {
    if (open && dataSources.length > 0) {
      initializeFormValues();
    } else if (!open) {
      resetForm();
    }
  }, [open, widgetItem, form, dataSources]);

  const handleConfirm = async () => {
    try {
      const values = await form.validateFields();

      if (values.params && selectedDataSource?.params) {
        values.dataSourceParams = processFormParamsForSubmit(
          values.params,
          selectedDataSource.params
        );
        delete values.params;
      }

      onConfirm?.(values);
    } catch (error) {
      console.error('Form validation failed:', error);
    }
  };

  return (
    <Drawer
      title={t('dashboard.viewConfig')}
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
              dataSources={dataSources}
              loading={dataSourcesLoading}
              onDataSourceChange={setSelectedDataSource}
            />
          </Form.Item>
        </div>

        <div className="mb-6">
          <div className="font-bold text-[var(--color-text-1)] mb-4">
            {t('dashboard.paramSettings')}
          </div>
          <DataSourceParamsConfig
            selectedDataSource={selectedDataSource}
            includeFilterTypes={['params', 'fixed']}
          />
        </div>

        <div className="mb-6">
          <div className="font-bold text-[var(--color-text-1)] mb-4">
            {t('dashboard.chartTypeLabel')}
          </div>
          <Form.Item
            label={t('dashboard.chartTypeLabel')}
            name="chartType"
            rules={[{ required: true, message: t('common.selectTip') }]}
            initialValue="line"
          >
            <Radio.Group
              disabled={['trendLine'].includes(widgetItem?.widget || '')}
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

export default ViewConfig;

import React, { useEffect, useState, useRef, useCallback } from 'react';
import { useDataSourceManager } from '@/app/ops-analysis/hooks/useDataSource';
import { useDataSourceApi } from '@/app/ops-analysis/api/dataSource';
import { NodeConfPanelProps } from '@/app/ops-analysis/types/topology';
import { iconList } from '@/app/cmdb/utils/common';
import { NODE_DEFAULTS } from '../constants/nodeDefaults';
import { processDataSourceParams } from '@/app/ops-analysis/utils/widgetDataTransform';
import DataSourceParamsConfig from '@/app/ops-analysis/components/paramsConfig';
import DataSourceSelect from '@/app/ops-analysis/components/dataSourceSelect';
import SelectIcon, {
  SelectIconRef,
} from '@/app/cmdb/(pages)/assetManage/management/list/selectIcon';
import {
  Form,
  Input,
  InputNumber,
  Upload,
  Radio,
  Checkbox,
  Spin,
  Button,
  Drawer,
} from 'antd';
import {
  UploadOutlined,
  AppstoreOutlined,
  ReloadOutlined,
} from '@ant-design/icons';

const NodeConfPanel: React.FC<NodeConfPanelProps> = ({
  nodeType,
  readonly = false,
  initialValues,
  visible = false,
  title,
  onClose,
  onConfirm,
  onCancel,
}) => {
  const [form] = Form.useForm();
  const [logoPreview, setLogoPreview] = useState<string>('');
  const [logoType, setLogoType] = useState<'default' | 'custom'>('default');
  const [selectedIcon, setSelectedIcon] = useState<string>('');
  const [dataFields, setDataFields] = useState<string[]>([]);
  const [selectedFields, setSelectedFields] = useState<string[]>([]);
  const [loadingData, setLoadingData] = useState(false);
  const [currentDataSource, setCurrentDataSource] = useState<number | null>(
    null
  );
  const selectIconRef = useRef<SelectIconRef>(null);
  const { getSourceDataByApiId } = useDataSourceApi();

  const {
    dataSources,
    dataSourcesLoading,
    selectedDataSource,
    setSelectedDataSource,
    processFormParamsForSubmit,
    setDefaultParamValues,
    restoreUserParamValues,
  } = useDataSourceManager();

  // 初始化新增模式
  const initializeNewNode = useCallback(() => {
    const defaultValues: any = {
      logoType: 'default',
      logoIcon: 'cc-host',
      logoUrl: '',
      fontSize: NODE_DEFAULTS.SINGLE_VALUE_NODE.fontSize,
      textColor: NODE_DEFAULTS.SINGLE_VALUE_NODE.textColor,
      backgroundColor: NODE_DEFAULTS.SINGLE_VALUE_NODE.backgroundColor,
      borderColor: NODE_DEFAULTS.SINGLE_VALUE_NODE.borderColor,
      selectedFields: [],
    };

    if (nodeType === 'icon') {
      defaultValues.name = '';
      defaultValues.width = NODE_DEFAULTS.ICON_NODE.width;
      defaultValues.height = NODE_DEFAULTS.ICON_NODE.height;
    }

    setSelectedIcon('cc-host');
    setLogoType('default');
    setLogoPreview('');
    setCurrentDataSource(null);
    setSelectedDataSource(undefined);
    setDataFields([]);
    setSelectedFields([]);

    form.setFieldsValue(defaultValues);
  }, [form, setSelectedDataSource, nodeType]);

  // 初始化编辑模式
  const initializeEditNode = useCallback(
    (values: any) => {
      const formValues: any = {
        name: values.name,
        logoType: values.logoType,
        logoIcon: values.logoType === 'default' ? values.logoIcon : undefined,
        logoUrl: values.logoType === 'custom' ? values.logoUrl : undefined,
        width: values.width,
        height: values.height,
        dataSource: values.dataSource,
        selectedFields: values.selectedFields,
        fontSize: values.fontSize,
        textColor: values.textColor,
        backgroundColor: values.backgroundColor,
        borderColor: values.borderColor,
      };

      setSelectedIcon(values.logoIcon || 'cc-host');
      setLogoType(values.logoType || 'default');
      setCurrentDataSource(values.dataSource || null);
      setSelectedFields(values.selectedFields || []);

      if (values.logoUrl) {
        setLogoPreview(values.logoUrl);
      }

      if (values.dataSource && dataSources.length > 0) {
        const selectedSource = dataSources.find(
          (ds) => ds.id === values.dataSource
        );
        setSelectedDataSource(selectedSource);

        formValues.params = formValues.params || {};

        if (selectedSource?.params?.length) {
          setDefaultParamValues(selectedSource.params, formValues.params);

          if (values.dataSourceParams?.length) {
            restoreUserParamValues(values.dataSourceParams, formValues.params);
          }
        }
      } else {
        setSelectedDataSource(undefined);
      }

      form.setFieldsValue(formValues);
    },
    [
      form,
      dataSources,
      setSelectedDataSource,
      setDefaultParamValues,
      restoreUserParamValues,
    ]
  );

  useEffect(() => {
    if (dataSources.length > 0 || !dataSourcesLoading) {
      if (initialValues) {
        initializeEditNode(initialValues);
      } else {
        initializeNewNode();
      }
    }
  }, [initialValues, dataSourcesLoading]);

  const handleLogoUpload = (file: any) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      setLogoPreview(e.target?.result as string);
      form.setFieldsValue({ logoUrl: e.target?.result });
    };
    reader.readAsDataURL(file);
    return false;
  };

  const handleLogoTypeChange = (e: any) => {
    const type = e.target.value;
    setLogoType(type);

    if (type === 'default') {
      setLogoPreview('');
      form.setFieldsValue({ logoUrl: undefined });
    } else {
      setSelectedIcon('');
      form.setFieldsValue({ logoIcon: undefined });
    }
  };

  const handleSelectIcon = () => {
    if (selectIconRef.current) {
      selectIconRef.current.showModal({
        title: '选择图标',
        defaultIcon: selectedIcon || 'server',
      });
    }
  };

  const handleIconSelect = (iconKey: string) => {
    setSelectedIcon(iconKey);
    form.setFieldsValue({ logoIcon: iconKey });
  };

  const getIconUrl = (iconKey: string) => {
    const iconItem = iconList.find((item) => item.key === iconKey);
    return iconItem
      ? `/app/assets/assetModelIcon/${iconItem.url}.svg`
      : `/app/assets/assetModelIcon/cc-default_默认.svg`;
  };

  const handleDataSourceChange = useCallback(
    (dataSourceId: number) => {
      setCurrentDataSource(dataSourceId);
      const selectedSource = dataSources.find((ds) => ds.id === dataSourceId);
      setSelectedDataSource(selectedSource);
      setDataFields([]);
      setSelectedFields([]);

      const currentValues = form.getFieldsValue();
      form.setFieldsValue({
        ...currentValues,
        selectedFields: [],
      });

      if (selectedSource?.params?.length) {
        const params = currentValues.params || {};
        setDefaultParamValues(selectedSource.params, params);
        form.setFieldsValue({
          ...currentValues,
          selectedFields: [],
          params: params,
        });
      }
    },
    [dataSources, setSelectedDataSource, form, setDefaultParamValues]
  );

  const getObjectFields = useCallback(
    (obj: any, prefix = '', level = 0): string[] => {
      if (
        level >= 2 ||
        typeof obj !== 'object' ||
        obj === null ||
        Array.isArray(obj)
      ) {
        return prefix ? [prefix] : [];
      }

      const fields: string[] = [];

      Object.keys(obj).forEach((key) => {
        const value = obj[key];
        const currentPath = prefix ? `${prefix}.${key}` : key;

        if (
          typeof value === 'object' &&
          value !== null &&
          !Array.isArray(value) &&
          level < 1
        ) {
          const subFields = getObjectFields(value, currentPath, level + 1);
          fields.push(...subFields);
        } else {
          fields.push(currentPath);
        }
      });

      return fields;
    },
    []
  );

  const fetchDataFields = useCallback(async () => {
    if (!currentDataSource) {
      return;
    }
    setLoadingData(true);
    try {
      const formValues = form.getFieldsValue();
      const userParams = formValues?.params || {};
      const requestParams = processDataSourceParams({
        sourceParams: selectedDataSource?.params,
        userParams: userParams,
      });
      const data: any = await getSourceDataByApiId(
        currentDataSource,
        requestParams
      );

      let fields: string[] = [];

      if (Array.isArray(data) && data.length > 0) {
        const firstRow = data[0];

        if (
          typeof firstRow === 'object' &&
          firstRow !== null &&
          !Array.isArray(firstRow)
        ) {
          fields = getObjectFields(firstRow);
        } else if (Array.isArray(firstRow)) {
          fields = firstRow.map((_, index) => `字段${index + 1}`);
        } else {
          fields = ['数据值'];
        }
      } else if (
        typeof data === 'object' &&
        data !== null &&
        !Array.isArray(data)
      ) {
        fields = getObjectFields(data);
      }

      setDataFields(fields);
    } catch (error) {
      console.error('获取数据字段失败:', error);
      setDataFields([]);
    } finally {
      setLoadingData(false);
    }
  }, [
    currentDataSource,
    form,
    selectedDataSource?.params,
    getSourceDataByApiId,
    getObjectFields,
  ]);

  const handleFieldChange = useCallback(
    (checkedValues: string[]) => {
      setSelectedFields(checkedValues);
      form.setFieldsValue({ selectedFields: checkedValues });
    },
    [form]
  );

  const handleConfirm = async () => {
    try {
      const values = await form.validateFields();
      // 处理数据源参数转换
      if (values.params && selectedDataSource?.params) {
        values.dataSourceParams = processFormParamsForSubmit(
          values.params,
          selectedDataSource.params
        );
        delete values.params;
      }

      if (onConfirm) {
        onConfirm(values);
      }
    } catch (error) {
      console.error('表单验证失败:', error);
    }
  };

  const handleCancel = () => {
    if (onCancel) {
      onCancel();
    } else if (onClose) {
      onClose();
    }
  };

  return (
    <Drawer
      title={title || `${nodeType === 'single-value' ? '单值' : '图标'}节点`}
      placement="right"
      width={600}
      open={visible}
      onClose={onClose}
      footer={
        readonly ? (
          <div className="flex justify-end">
            <Button onClick={handleCancel}>关闭</Button>
          </div>
        ) : (
          <div className="flex justify-end space-x-2">
            <Button type="primary" onClick={handleConfirm}>
              确认
            </Button>
            <Button onClick={handleCancel}>取消</Button>
          </div>
        )
      }
    >
      <div>
        <Form form={form} labelCol={{ span: 4 }} layout="horizontal">
          <div>
            {/* 图标类型显示名称和Logo配置 */}
            {nodeType === 'icon' && (
              <>
                <div className="font-bold text-[var(--color-text-1)] mb-4">
                  基础设置
                </div>
                <Form.Item
                  label="名称"
                  name="name"
                  rules={[{ required: true, message: '请输入节点名称' }]}
                >
                  <Input placeholder="请输入节点名称" disabled={readonly} />
                </Form.Item>

                <Form.Item
                  label="Logo类型"
                  name="logoType"
                  initialValue="default"
                >
                  <Radio.Group
                    onChange={handleLogoTypeChange}
                    disabled={readonly}
                  >
                    <Radio value="default">默认</Radio>
                    <Radio value="custom">自定义</Radio>
                  </Radio.Group>
                </Form.Item>

                <Form.Item
                  label=" "
                  colon={false}
                  name={logoType === 'default' ? 'logoIcon' : 'logoUrl'}
                  dependencies={['logoType']}
                >
                  {logoType === 'default' ? (
                    <div className="flex items-center space-x-3">
                      <div
                        onClick={handleSelectIcon}
                        className="w-20 h-20 border-2 border-dashed border-[#d9d9d9] hover:border-[#40a9ff] cursor-pointer flex flex-col items-center justify-center rounded-lg transition-colors duration-200 bg-[#fafafa] hover:bg-[#f0f0f0]"
                      >
                        {selectedIcon ? (
                          <img
                            src={getIconUrl(selectedIcon)}
                            alt="已选择的图标"
                            className="w-12 h-12 object-cover"
                          />
                        ) : (
                          <>
                            <AppstoreOutlined className="text-xl text-[#8c8c8c] mb-1" />
                            <span className="text-xs text-[#8c8c8c]">
                              选择图标
                            </span>
                          </>
                        )}
                      </div>
                    </div>
                  ) : (
                    <div className="flex items-center space-x-3">
                      <Upload
                        accept="image/*"
                        showUploadList={false}
                        beforeUpload={handleLogoUpload}
                      >
                        <div className="w-20 h-20 border-2 border-dashed border-[#d9d9d9] hover:border-[#40a9ff] cursor-pointer flex flex-col items-center justify-center rounded-lg transition-colors duration-200 bg-[#fafafa] hover:bg-[#f0f0f0]">
                          {logoPreview ? (
                            <img
                              src={logoPreview}
                              alt="已上传的图片"
                              className="w-12 h-12 object-cover rounded-lg"
                            />
                          ) : (
                            <>
                              <UploadOutlined className="text-xl text-[#8c8c8c] mb-1" />
                              <span className="text-xs text-[#8c8c8c]">
                                上传图片
                              </span>
                            </>
                          )}
                        </div>
                      </Upload>
                    </div>
                  )}
                </Form.Item>
              </>
            )}
          </div>

          {nodeType === 'single-value' && (
            <>
              <div className="mb-6">
                <div className="font-bold text-[var(--color-text-1)] mb-4">
                  数据源
                </div>
                <Form.Item
                  label="数据源类型"
                  name="dataSource"
                  rules={[{ required: true, message: '请选择数据源' }]}
                >
                  <DataSourceSelect
                    loading={dataSourcesLoading}
                    dataSources={dataSources}
                    placeholder="请选择数据源"
                    style={{ width: '100%' }}
                    onChange={handleDataSourceChange}
                    disabled={readonly}
                  />
                </Form.Item>
              </div>
              <div className="mb-6">
                <div className="font-bold text-[var(--color-text-1)] mb-4">
                  参数设置
                </div>
                <Spin size="small" spinning={dataSourcesLoading}>
                  <DataSourceParamsConfig
                    selectedDataSource={selectedDataSource}
                    readonly={readonly || dataSourcesLoading}
                    includeFilterTypes={['params', 'fixed', 'filter']}
                    fieldPrefix="params"
                  />
                </Spin>
              </div>
              <div className="mb-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="font-bold text-[var(--color-text-1)]">
                    数据设置
                  </div>
                  <Button
                    type="text"
                    icon={<ReloadOutlined />}
                    onClick={fetchDataFields}
                    loading={loadingData}
                    disabled={
                      !currentDataSource || readonly || dataSourcesLoading
                    }
                    size="small"
                    title="刷新数据字段"
                  />
                </div>

                {dataFields.length > 0 ? (
                  <div className="border border-gray-200 rounded-lg p-4 bg-gray-50">
                    <div className="text-sm text-gray-600 mb-3">
                      选择要显示的数据字段：
                    </div>
                    <Form.Item name="selectedFields" noStyle>
                      <Checkbox.Group
                        options={dataFields.map((field) => ({
                          label: (
                            <span
                              className={
                                field.includes('.')
                                  ? 'text-blue-600'
                                  : 'text-gray-800'
                              }
                            >
                              {field.includes('.') ? (
                                <>
                                  {field.split('.').map((part, index, arr) => (
                                    <span key={index}>
                                      {index > 0 && (
                                        <span className="text-gray-400 mx-1">
                                          .
                                        </span>
                                      )}
                                      <span
                                        className={
                                          index === arr.length - 1
                                            ? 'font-medium'
                                            : 'text-gray-600'
                                        }
                                      >
                                        {part}
                                      </span>
                                    </span>
                                  ))}
                                </>
                              ) : (
                                field
                              )}
                            </span>
                          ),
                          value: field,
                        }))}
                        value={selectedFields}
                        onChange={handleFieldChange}
                        className="flex flex-col space-y-2"
                      />
                    </Form.Item>
                  </div>
                ) : dataSourcesLoading ? (
                  <div className="text-center py-4 text-gray-500">
                    <div className="flex items-center justify-center">
                      <Spin size="small" className="mr-2" />
                    </div>
                  </div>
                ) : currentDataSource ? (
                  <div className="text-center py-4 text-gray-500">
                    {loadingData ? (
                      <div className="flex items-center justify-center">
                        <Spin size="small" className="mr-2" />
                        <span>正在获取数据字段...</span>
                      </div>
                    ) : (
                      <span>点击刷新按钮获取数据字段</span>
                    )}
                  </div>
                ) : (
                  <div className="text-center py-4 text-gray-500">
                    请先选择数据源
                  </div>
                )}
              </div>
            </>
          )}

          <div className="mb-6">
            <div className="font-bold text-[var(--color-text-1)] mb-4">
              节点样式
            </div>
            {nodeType === 'single-value' && (
              <>
                <Form.Item label="字体大小" name="fontSize">
                  <InputNumber
                    defaultValue={NODE_DEFAULTS.SINGLE_VALUE_NODE.fontSize}
                    min={10}
                    max={48}
                    step={1}
                    addonAfter="px"
                    disabled={readonly}
                    placeholder="请输入字体大小"
                    style={{ width: '120px' }}
                  />
                </Form.Item>

                <Form.Item label="文本颜色" name="textColor">
                  <Input
                    type="color"
                    defaultValue={NODE_DEFAULTS.SINGLE_VALUE_NODE.textColor}
                    className="w-20 h-8"
                    disabled={readonly}
                  />
                </Form.Item>
                <Form.Item label="背景颜色" name="backgroundColor">
                  <Input
                    type="color"
                    defaultValue={
                      NODE_DEFAULTS.SINGLE_VALUE_NODE.backgroundColor
                    }
                    className="w-20 h-8"
                    disabled={readonly}
                  />
                </Form.Item>

                <Form.Item label="边框颜色" name="borderColor">
                  <Input
                    type="color"
                    defaultValue={NODE_DEFAULTS.SINGLE_VALUE_NODE.borderColor}
                    className="w-20 h-8"
                    disabled={readonly}
                  />
                </Form.Item>
              </>
            )}
            {nodeType === 'icon' && (
              <>
                <Form.Item label="图标宽度" name="width">
                  <InputNumber
                    defaultValue={NODE_DEFAULTS.ICON_NODE.width}
                    min={20}
                    max={300}
                    step={1}
                    addonAfter="px"
                    disabled={readonly}
                    placeholder="请输入图标宽度"
                    style={{ width: '120px' }}
                  />
                </Form.Item>

                <Form.Item label="图标高度" name="height">
                  <InputNumber
                    defaultValue={NODE_DEFAULTS.ICON_NODE.height}
                    min={20}
                    max={300}
                    step={1}
                    addonAfter="px"
                    disabled={readonly}
                    placeholder="请输入图标高度"
                    style={{ width: '120px' }}
                  />
                </Form.Item>
              </>
            )}
          </div>
        </Form>

        <SelectIcon ref={selectIconRef} onSelect={handleIconSelect} />
      </div>
    </Drawer>
  );
};

export default NodeConfPanel;

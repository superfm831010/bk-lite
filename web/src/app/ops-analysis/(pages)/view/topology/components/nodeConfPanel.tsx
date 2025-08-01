import React, { useEffect, useState, useRef } from 'react';
import { useDataSourceApi } from '@/app/ops-analysis/api/dataSource';
import { DatasourceItem } from '@/app/ops-analysis/types/dataSource';
import { iconList } from '@/app/cmdb/utils/common';
import SelectIcon, {
  SelectIconRef,
} from '@/app/cmdb/(pages)/assetManage/management/list/selectIcon';
import {
  Form,
  Input,
  InputNumber,
  Select,
  Upload,
  Radio,
  Checkbox,
  Spin,
  Button,
} from 'antd';
import {
  UploadOutlined,
  AppstoreOutlined,
  ReloadOutlined,
} from '@ant-design/icons';
interface NodeConfPanelProps {
  nodeType: 'single-value' | 'icon';
  onFormReady?: (formInstance: any) => void;
  readonly?: boolean;
  initialValues?: {
    name?: string;
    logoType?: 'default' | 'custom';
    logoIcon?: string;
    logoUrl?: string;
    dataSource?: number;
    selectedFields?: string[];
    fontSize?: number;
  };
}

const NodeConfPanel: React.FC<NodeConfPanelProps> = ({
  nodeType,
  onFormReady,
  readonly = false,
  initialValues,
}) => {
  const [form] = Form.useForm();
  const [dataSources, setDataSources] = useState<DatasourceItem[]>([]);
  const [dataSourcesLoading, setDataSourcesLoading] = useState(false);
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
  const { getDataSourceList, getSourceDataByApiId } = useDataSourceApi();

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
    if (onFormReady) {
      onFormReady(form);
    }

    if (initialValues) {
      setSelectedIcon(initialValues.logoIcon || 'cc-host');
      setLogoType(initialValues.logoType || 'default');
      setCurrentDataSource(initialValues.dataSource || null);
      setSelectedFields(initialValues.selectedFields || []);

      if (initialValues.logoUrl) {
        setLogoPreview(initialValues.logoUrl);
      }

      form.setFieldsValue({
        name: initialValues.name || '',
        logoType: initialValues.logoType || 'default',
        logoIcon: initialValues.logoIcon || 'cc-host',
        logoUrl: initialValues.logoUrl,
        dataSource: initialValues.dataSource,
        selectedFields: initialValues.selectedFields || [],
      });
    } else {
      setSelectedIcon('cc-host');
    }
  }, [form, onFormReady, initialValues]);

  const formatDataSourceOptions = (sources: DatasourceItem[]) => {
    return sources.map((item) => ({
      label: `${item.name}（${item.rest_api}）`,
      value: item.id,
      title: item.desc,
    }));
  };

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

  const handleDataSourceChange = (dataSourceId: number) => {
    setCurrentDataSource(dataSourceId);
  };

  const fetchDataFields = async () => {
    if (!currentDataSource) {
      return;
    }
    setLoadingData(true);
    try {
      const data: any = await getSourceDataByApiId(currentDataSource);
      if (Array.isArray(data) && data.length > 0) {
        const firstRow = data[0];
        if (Array.isArray(firstRow)) {
          const fields = firstRow.map((_, index) => `字段${index + 1}`);
          setDataFields(fields);
        }
      } else {
        setDataFields([]);
      }
    } catch (error) {
      console.error('获取数据字段失败:', error);
      setDataFields([]);
    } finally {
      setLoadingData(false);
    }
  };

  const handleFieldChange = (checkedValues: string[]) => {
    setSelectedFields(checkedValues);
    form.setFieldsValue({ selectedFields: checkedValues });
  };

  return (
    <div>
      <Form
        form={form}
        labelCol={{ span: 4 }}
        layout="horizontal"
        initialValues={{
          logoType: initialValues?.logoType || 'default',
          logoIcon: initialValues?.logoIcon || 'cc-host',
          name: initialValues?.name || '',
          logoUrl: initialValues?.logoUrl,
          dataSource: initialValues?.dataSource,
          selectedFields: initialValues?.selectedFields || [],
          fontSize: initialValues?.fontSize || 14,
        }}
      >
        <div className="mb-6">
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

          {/* 图标类型显示Logo配置 */}
          {nodeType === 'icon' && (
            <>
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
                <Select
                  loading={dataSourcesLoading}
                  options={formatDataSourceOptions(dataSources)}
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
              <div className="text-center py-4 text-[var(--color-text-2)]">
                TODO-参数配置
              </div>
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
                  disabled={!currentDataSource || readonly}
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
                        label: field,
                        value: field,
                      }))}
                      value={selectedFields}
                      onChange={handleFieldChange}
                      className="flex flex-col space-y-2"
                    />
                  </Form.Item>
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
                  defaultValue={14}
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
                  defaultValue="#333333"
                  className="w-20 h-8"
                  disabled={readonly}
                />
              </Form.Item>
            </>
          )}

          <Form.Item label="背景颜色" name="backgroundColor">
            <Input
              type="color"
              defaultValue="#ffffff"
              className="w-20 h-8"
              disabled={readonly}
            />
          </Form.Item>

          <Form.Item label="边框颜色" name="borderColor">
            <Input
              type="color"
              defaultValue="#d9d9d9"
              className="w-20 h-8"
              disabled={readonly}
            />
          </Form.Item>
        </div>
      </Form>

      <SelectIcon ref={selectIconRef} onSelect={handleIconSelect} />
    </div>
  );
};

export default NodeConfPanel;

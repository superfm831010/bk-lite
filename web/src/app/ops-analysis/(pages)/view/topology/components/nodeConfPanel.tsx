import React, { useEffect, useState, useRef } from 'react';
import { Form, Input, Select, Upload, Radio } from 'antd';
import { UploadOutlined, AppstoreOutlined } from '@ant-design/icons';
import { useDataSourceApi } from '@/app/ops-analysis/api/dataSource';
import { DatasourceItem } from '@/app/ops-analysis/types/dataSource';
import { iconList } from '@/app/cmdb/utils/common';
import SelectIcon, {
  SelectIconRef,
} from '@/app/cmdb/(pages)/assetManage/management/list/selectIcon';

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
  const selectIconRef = useRef<SelectIconRef>(null);
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
    if (onFormReady) {
      onFormReady(form);
    }

    // 设置初始值
    if (initialValues) {
      setSelectedIcon(initialValues.logoIcon || 'cc-host');
      setLogoType(initialValues.logoType || 'default');
      if (initialValues.logoUrl) {
        setLogoPreview(initialValues.logoUrl);
      }

      // 设置表单初始值
      form.setFieldsValue({
        name: initialValues.name || '',
        logoType: initialValues.logoType || 'default',
        logoIcon: initialValues.logoIcon || 'cc-host',
        logoUrl: initialValues.logoUrl,
        dataSource: initialValues.dataSource,
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
    // 根据iconKey在iconList中查找对应的url
    const iconItem = iconList.find((item) => item.key === iconKey);
    return iconItem
      ? `/app/assets/assetModelIcon/${iconItem.url}.svg`
      : `/app/assets/assetModelIcon/cc-default_默认.svg`;
  };

  const handleDataSourceChange = (dataSourceId: number) => {
    // TODO: 后续接入接口时处理数据源变化
    console.log('选择了数据源:', dataSourceId);
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
          <div className="text-center py-8 text-[var(--color-text-2)]">
            TODO-参数配置
          </div>
        </div>

        <div className="mb-6">
          <div className="font-bold text-[var(--color-text-1)] mb-4">
            节点样式
          </div>
          {nodeType === 'single-value' && (
            <>
              <Form.Item label="字体大小" name="fontSize">
                <Select
                  defaultValue="14"
                  disabled={readonly}
                  options={[
                    { label: '12px', value: '12' },
                    { label: '14px', value: '14' },
                    { label: '16px', value: '16' },
                    { label: '18px', value: '18' },
                    { label: '20px', value: '20' },
                  ]}
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

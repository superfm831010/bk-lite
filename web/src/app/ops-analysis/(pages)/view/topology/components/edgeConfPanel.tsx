import React, { useEffect } from 'react';
import { useTranslation } from '@/utils/i18n';
import { mockInterfaces } from '../../mockData';
import {
  Drawer,
  Form,
  Select,
  Input,
  Button,
  Space,
  Typography,
  Radio,
} from 'antd';

interface InterfaceConfig {
  type: 'existing' | 'custom';
  value: string;
}

interface EdgeConfigPanelProps {
  visible: boolean;
  readonly?: boolean;
  edgeData: {
    id: string;
    lineType: string;
    lineName?: string;
    sourceNode: {
      id: string;
      name: string;
    };
    targetNode: {
      id: string;
      name: string;
    };
    sourceInterface?: InterfaceConfig;
    targetInterface?: InterfaceConfig;
  } | null;
  onLineTypeChange: (lineType: string) => void;
  onLineNameChange?: (lineName: string) => void;
  onClose: () => void;
  onConfirm?: (values: any) => void;
}

const EdgeConfigPanel: React.FC<EdgeConfigPanelProps> = ({
  visible,
  readonly = false,
  edgeData,
  onLineTypeChange,
  onLineNameChange,
  onClose,
  onConfirm,
}) => {
  const [form] = Form.useForm();
  const { t } = useTranslation();

  useEffect(() => {
    if (edgeData) {
      const initialValues = {
        lineType: edgeData.lineType || 'network line',
        lineName: edgeData.lineName || '',
        sourceInterfaceType: edgeData.sourceInterface?.type || 'existing',
        sourceInterfaceValue: edgeData.sourceInterface?.value || '',
        targetInterfaceType: edgeData.targetInterface?.type || 'existing',
        targetInterfaceValue: edgeData.targetInterface?.value || '',
      };
      form.setFieldsValue(initialValues);
    }
  }, [edgeData, form]);

  const handleFinish = (values: any) => {
    if (onConfirm) {
      const result = {
        ...values,
        sourceInterface: {
          type: values.sourceInterfaceType,
          value: values.sourceInterfaceValue,
        },
        targetInterface: {
          type: values.targetInterfaceType,
          value: values.targetInterfaceValue,
        },
      };
      onConfirm(result);
    } else {
      if (values.lineType !== edgeData?.lineType) {
        onLineTypeChange(values.lineType);
      }
      if (values.lineName !== edgeData?.lineName && onLineNameChange) {
        onLineNameChange(values.lineName || '');
      }
    }
    onClose();
  };

  // 线条类型变化
  const handleLineTypeChange = (lineType: string) => {
    if (lineType === 'network line') {
      form.setFieldValue('lineName', '');
    }
  };

  // 渲染接口配置组件
  const renderInterfaceConfig = (
    nodeType: 'source' | 'target',
    nodeName: string
  ) => {
    const isSource = nodeType === 'source';
    const interfaceTypeField = isSource
      ? 'sourceInterfaceType'
      : 'targetInterfaceType';
    const interfaceValueField = isSource
      ? 'sourceInterfaceValue'
      : 'targetInterfaceValue';
    const nodeLabel = isSource ? t('topology.node1') : t('topology.node2');

    return (
      <div>
        <Typography.Text
          strong
          style={{
            fontSize: 14,
            color: 'var(--color-text-3)',
            marginBottom: 8,
            display: 'block',
          }}
        >
          {nodeLabel}
        </Typography.Text>
        <div
          style={{
            padding: '16px',
            backgroundColor: 'var(--color-fill-1)',
            borderRadius: '8px',
            marginTop: '6px',
            border: '1px solid var(--color-border-2)',
          }}
        >
          <Form.Item
            label={`${t('topology.nodeName')}：`}
            style={{ marginBottom: 8 }}
          >
            <Typography.Text strong>{nodeName}</Typography.Text>
          </Form.Item>

          <div style={{ marginTop: 16 }}>
            <Form.Item
              name={interfaceTypeField}
              label={`${t('topology.interface')}：`}
              style={{ marginBottom: 8 }}
            >
              <Radio.Group disabled={readonly}>
                <Radio value="existing">
                  {t('topology.existingInterface')}
                </Radio>
                <Radio value="custom">{t('topology.customInterface')}</Radio>
              </Radio.Group>
            </Form.Item>

            <Form.Item
              noStyle
              shouldUpdate={(prevValues, currentValues) =>
                prevValues[interfaceTypeField] !==
                currentValues[interfaceTypeField]
              }
            >
              {({ getFieldValue }) => {
                const interfaceType = getFieldValue(interfaceTypeField);
                return interfaceType === 'existing' ? (
                  <Form.Item
                    name={interfaceValueField}
                    rules={[{ required: true, message: t('common.selectMsg') }]}
                    style={{ marginBottom: '10px' }}
                  >
                    <Select
                      placeholder={t('common.selectMsg')}
                      options={mockInterfaces}
                      disabled={readonly}
                    />
                  </Form.Item>
                ) : (
                  <Form.Item
                    name={interfaceValueField}
                    rules={[{ required: true, message: t('common.inputMsg') }]}
                    style={{ marginBottom: '10px' }}
                  >
                    <Input
                      placeholder={t('common.inputMsg')}
                      disabled={readonly}
                    />
                  </Form.Item>
                );
              }}
            </Form.Item>
          </div>
        </div>
      </div>
    );
  };

  // 渲染线条名称配置
  const renderLineNameConfig = () => (
    <Form.Item
      noStyle
      shouldUpdate={(prevValues, currentValues) =>
        prevValues.lineType !== currentValues.lineType
      }
    >
      {({ getFieldValue }) => {
        const lineType = getFieldValue('lineType');
        return lineType === 'line' ? (
          <Form.Item
            label={t('topology.lineName')}
            name="lineName"
            rules={[{ required: true, message: t('common.inputMsg') }]}
          >
            <Input placeholder={t('common.inputMsg')} disabled={readonly} />
          </Form.Item>
        ) : null;
      }}
    </Form.Item>
  );

  // 渲染网络线配置
  const renderNetworkLineConfig = () => (
    <Form.Item
      noStyle
      shouldUpdate={(prevValues, currentValues) =>
        prevValues.lineType !== currentValues.lineType
      }
    >
      {({ getFieldValue }) => {
        const lineType = getFieldValue('lineType');
        return lineType === 'network line' && edgeData ? (
          <div style={{ marginTop: '24px' }}>
            <Space direction="vertical" size="middle" style={{ width: '100%' }}>
              {renderInterfaceConfig('source', edgeData.sourceNode.name)}
              {renderInterfaceConfig('target', edgeData.targetNode.name)}
            </Space>
          </div>
        ) : null;
      }}
    </Form.Item>
  );

  if (!edgeData) return null;

  return (
    <Drawer
      title={readonly ? t('topology.edgeView') : t('topology.edgeConfig')}
      placement="right"
      width={600}
      open={visible}
      onClose={onClose}
      bodyStyle={{ padding: 0 }}
      footer={
        <div style={{ textAlign: 'right', padding: '16px 24px' }}>
          <Space>
            <Button onClick={onClose}>
              {readonly ? t('common.close') : t('common.cancel')}
            </Button>
            {!readonly && (
              <Button type="primary" onClick={() => form.submit()}>
                {t('common.confirm')}
              </Button>
            )}
          </Space>
        </div>
      }
    >
      <div style={{ padding: '24px' }}>
        <Form
          form={form}
          layout="vertical"
          onFinish={handleFinish}
          initialValues={{
            lineType: edgeData?.lineType || 'network line',
            lineName: edgeData?.lineName || '',
            sourceInterfaceType: edgeData?.sourceInterface?.type || 'existing',
            sourceInterfaceValue: edgeData?.sourceInterface?.value || '',
            targetInterfaceType: edgeData?.targetInterface?.type || 'existing',
            targetInterfaceValue: edgeData?.targetInterface?.value || '',
          }}
        >
          {/* 线条类型选择 */}
          <Form.Item
            label={t('topology.lineType')}
            name="lineType"
            rules={[{ required: true, message: t('common.selectMsg') }]}
          >
            <Select
              placeholder={t('common.selectMsg')}
              onChange={handleLineTypeChange}
              disabled={readonly}
            >
              <Select.Option value="network line">
                {t('topology.networkLine')}
              </Select.Option>
              <Select.Option value="line">{t('topology.line')}</Select.Option>
            </Select>
          </Form.Item>

          {/* 线条名称配置 */}
          {renderLineNameConfig()}

          {/* 网络线配置 */}
          {renderNetworkLineConfig()}
        </Form>
      </div>
    </Drawer>
  );
};

export default EdgeConfigPanel;

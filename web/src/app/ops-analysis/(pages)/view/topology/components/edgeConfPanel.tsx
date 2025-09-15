import React, { useEffect } from 'react';
import { useTranslation } from '@/utils/i18n';
import { COLORS } from '../constants/nodeDefaults';
import { EdgeConfigPanelProps } from '@/app/ops-analysis/types/topology';
import {
  Drawer,
  Form,
  Select,
  Input,
  Button,
  Space,
  Typography,
  Radio,
  ColorPicker,
} from 'antd';

const EdgeConfigPanel: React.FC<EdgeConfigPanelProps> = ({
  visible,
  readonly = false,
  edgeData,
  onClose,
  onConfirm,
}) => {
  const [form] = Form.useForm();
  const { t } = useTranslation();
  const interfacesList: any = [];

  useEffect(() => {
    if (edgeData) {
      const initialValues = {
        lineType: edgeData.lineType || 'common_line',
        lineName: edgeData.lineName || '',
        lineColor: edgeData.styleConfig?.lineColor || COLORS.EDGE.DEFAULT,
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
        styleConfig: {
          lineColor:
            typeof values.lineColor === 'object'
              ? values.lineColor.toHexString()
              : values.lineColor || COLORS.EDGE.DEFAULT,
        },
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
    }
    onClose();
  };

  // 线条类型变化
  const handleLineTypeChange = (lineType: string) => {
    if (lineType === 'network_line') {
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
                    rules={[{ required: true, message: t('common.selectTip') }]}
                    style={{ marginBottom: '10px' }}
                  >
                    <Select
                      placeholder={t('common.selectTip')}
                      options={interfacesList}
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
        return lineType === 'common_line' ? (
          <Form.Item label={t('topology.lineName')} name="lineName">
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
        return lineType === 'network_line' && edgeData ? (
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
      title={readonly ? t('topology.edgeView') : t('topology.edgeSetting')}
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
          layout="horizontal"
          labelCol={{ span: 5 }}
          onFinish={handleFinish}
          initialValues={{
            lineType: edgeData?.lineType || 'common_line',
            lineName: edgeData?.lineName || '',
            sourceInterfaceType: edgeData?.sourceInterface?.type || 'existing',
            sourceInterfaceValue: edgeData?.sourceInterface?.value || '',
            targetInterfaceType: edgeData?.targetInterface?.type || 'existing',
            targetInterfaceValue: edgeData?.targetInterface?.value || '',
          }}
        >
          <div className="font-bold text-[var(--color-text-1)] mb-4">
            {t('topology.nodeConfig.basicSettings')}
          </div>
          {/* 线条类型选择 */}
          <Form.Item
            label={t('topology.lineType')}
            name="lineType"
            rules={[{ required: true, message: t('common.selectTip') }]}
          >
            <Select
              placeholder={t('common.selectTip')}
              onChange={handleLineTypeChange}
              disabled={readonly}
            >
              <Select.Option value="common_line">
                {t('topology.commonLine')}
              </Select.Option>
              <Select.Option value="network_line">
                {t('topology.networkLine')}
              </Select.Option>
            </Select>
          </Form.Item>

          {/* 线条名称配置 */}
          {renderLineNameConfig()}

          <div className="mb-6">
            <div className="font-bold text-[var(--color-text-1)] mb-4">
              {t('topology.styleSettings')}
            </div>

            <Form.Item
              label={t('topology.edgeConfig.lineColor')}
              name="lineColor"
            >
              <ColorPicker
                disabled={readonly}
                size="small"
                showText
                allowClear
                format="hex"
              />
            </Form.Item>
          </div>

          {/* 网络线配置 */}
          {renderNetworkLineConfig()}
        </Form>
      </div>
    </Drawer>
  );
};

export default EdgeConfigPanel;

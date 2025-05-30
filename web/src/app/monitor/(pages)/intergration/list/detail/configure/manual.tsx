import React, { useState, useEffect, useMemo } from 'react';
import { Form, Button, message, InputNumber, Select } from 'antd';
import { useTranslation } from '@/utils/i18n';
import {
  deepClone,
  getConfigByPluginName,
  getConfigByObjectName,
} from '@/app/monitor/utils/common';
import { TIMEOUT_UNITS } from '@/app/monitor/constants/monitor';
import { useSearchParams } from 'next/navigation';
import useApiClient from '@/utils/request';
import useMonitorApi from '@/app/monitor/api';
import { useFormItems } from '@/app/monitor/hooks/intergration';
import CodeEditor from '@/app/monitor/components/codeEditor';
import { TableDataItem } from '@/app/monitor/types';
const { Option } = Select;
import Permission from '@/components/permission';
import { IntergrationAccessProps } from '@/app/monitor/types/monitor';

const AutomaticConfiguration: React.FC<IntergrationAccessProps> = ({
  showInterval = true,
}) => {
  const [form] = Form.useForm();
  const { t } = useTranslation();
  const searchParams = useSearchParams();
  const { isLoading } = useApiClient();
  const { checkMonitorInstance } = useMonitorApi();
  const pluginName = searchParams.get('collect_type') || '';
  const objId = searchParams.get('id') || '';
  const objectName = searchParams.get('name') || '';
  const [confirmLoading, setConfirmLoading] = useState<boolean>(false);
  const [configMsg, setConfigMsg] = useState<string>('');

  const collectType = useMemo(() => {
    return getConfigByPluginName(pluginName, 'collect_type');
  }, [pluginName]);

  const instanceType = useMemo(() => {
    return getConfigByObjectName(objectName, 'instance_type');
  }, [objectName]);

  const configTypes = useMemo(() => {
    return getConfigByPluginName(pluginName, 'config_type');
  }, [pluginName]);

  // 使用自定义 Hook
  const { formItems, configText } = useFormItems({
    collectType,
    columns: [],
    pluginName,
  });

  useEffect(() => {
    if (isLoading) return;
    initData();
  }, [isLoading]);

  const initData = () => {
    form.setFieldsValue({
      interval: collectType === 'http' ? 60 : 10,
    });
    switch (collectType) {
      case 'host':
        form.setFieldsValue({
          metric_type: configTypes.filter((item: string) => item !== 'gpu'),
        });
        break;
      case 'ipmi':
        form.setFieldsValue({
          protocol: 'lanplus',
        });
        break;
      case 'snmp':
        form.setFieldsValue({
          port: 161,
          version: 2,
          timeout: 10,
        });
      case 'middleware':
        form.setFieldsValue({
          timeout: 10,
        });
    }
  };

  const handleSave = () => {
    form.validateFields().then((values) => {
      // 处理表单提交逻辑
      const _values = deepClone(values);
      _values.instance_id = getInstId(_values);
      _values.instance_type = instanceType;
      _values.collect_type = collectType;
      _values.config_type = configTypes[0] || '';
      getConfigText(_values);
    });
  };

  const getInstId = (row: TableDataItem) => {
    if (['snmp', 'ipmi'].includes(collectType)) {
      return objectName + '-' + (row.monitor_ip || '');
    }
    if (pluginName === 'Tencent Cloud') {
      return row.monitor_url;
    }
    switch (collectType) {
      case 'host':
        return row.monitor_ip;
      case 'trap':
        return 'trap' + row.monitor_ip;
      case 'database':
        return row.server || `${row.host}:${row.port}`;
      case 'http':
        return `vc-${row.host}`;
      case 'docker':
        return row.endpoint;
      default:
        return row.monitor_url;
    }
  };

  const getConfigText = async (params: TableDataItem) => {
    try {
      setConfirmLoading(true);
      await checkMonitorInstance(objId, {
        instance_id: params.instance_id,
        instance_name: params.instance_id,
      });
      let _configMsg = deepClone(configText);
      if (collectType === 'snmp') {
        _configMsg = _configMsg[`v${params.version}`];
      }
      if (collectType === 'host') {
        _configMsg = params.metric_type.reduce((pre: string, cur: string) => {
          return (pre += _configMsg[cur]);
        }, '');
      }
      setConfigMsg(replaceTemplate(_configMsg || '', params));
      message.success(t('common.successfullyAdded'));
    } finally {
      setConfirmLoading(false);
    }
  };

  const replaceTemplate = (
    template: string,
    data: { [key: string]: string | number }
  ): string => {
    return Object.keys(data).reduce((acc, key) => {
      // 使用正则表达式来匹配模板字符串中的 ${key} 或 $key
      const regex = new RegExp(`\\$${key}`, 'g');
      // 替换匹配到的内容为对象中的值
      return acc.replace(regex, (data[key] || 'null').toString());
    }, template);
  };

  return (
    <div className="px-[10px]">
      <Form form={form} name="basic" layout="vertical">
        {formItems && (
          <p className="mb-[20px]">
            {t('monitor.intergrations.configureStepIntro')}
          </p>
        )}
        {formItems}
        {showInterval && (
          <Form.Item required label={t('monitor.intergrations.interval')}>
            <Form.Item
              noStyle
              name="interval"
              rules={[
                {
                  required: true,
                  message: t('common.required'),
                },
              ]}
            >
              <InputNumber
                className="mr-[10px]"
                min={1}
                precision={0}
                addonAfter={
                  <Select style={{ width: 116 }} defaultValue="s">
                    {TIMEOUT_UNITS.map((item: string) => (
                      <Option key={item} value={item}>
                        {item}
                      </Option>
                    ))}
                  </Select>
                }
              />
            </Form.Item>
            <span className="text-[12px] text-[var(--color-text-3)]">
              {t('monitor.intergrations.intervalDes')}
            </span>
          </Form.Item>
        )}
      </Form>
      <Permission requiredPermissions={['Add']}>
        <Button type="primary" loading={confirmLoading} onClick={handleSave}>
          {t('monitor.intergrations.generateConfiguration')}
        </Button>
      </Permission>
      {!!configMsg && (
        <CodeEditor
          className="mt-[10px]"
          mode="python"
          theme="monokai"
          name="editor"
          width="100%"
          height="300px"
          readOnly
          value={configMsg}
          showCopy
        />
      )}
    </div>
  );
};

export default AutomaticConfiguration;

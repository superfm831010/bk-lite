import { ModalRef, ModalProps, TableDataItem } from '@/app/monitor/types';
import { Form, Button, message, InputNumber, Select, Spin } from 'antd';
import { cloneDeep } from 'lodash';
import React, {
  useState,
  useRef,
  useImperativeHandle,
  forwardRef,
} from 'react';
import { useTranslation } from '@/utils/i18n';
import { useFormItems } from '@/app/monitor/hooks/intergration';
import OperateModal from '@/components/operate-modal';
import useApiClient from '@/utils/request';
import useMonitorApi from '@/app/monitor/api';
import {
  OBJECT_CONFIG_MAP,
  TIMEOUT_UNITS,
} from '@/app/monitor/constants/monitor';
const { Option } = Select;

const UpdateConfig = forwardRef<ModalRef, ModalProps>(({ onSuccess }, ref) => {
  const [form] = Form.useForm();
  const { t } = useTranslation();
  const { post } = useApiClient();
  const { getConfigContent } = useMonitorApi();
  const formRef = useRef(null);
  const [pluginName, setPluginName] = useState<string>('');
  const [collectType, setCollectType] = useState<string>('');
  const [confirmLoading, setConfirmLoading] = useState<boolean>(false);
  const [modalVisible, setModalVisible] = useState<boolean>(false);
  const [title, setTitle] = useState<string>('');
  const [configForm, setConfigForm] = useState<TableDataItem>({});
  const [pageLoading, setPageLoading] = useState<boolean>(false);

  useImperativeHandle(ref, () => ({
    showModal: ({ form, title }) => {
      const _form = cloneDeep(form);
      setTitle(title);
      setModalVisible(true);
      setConfirmLoading(false);
      getContent(_form);
    },
  }));

  const getContent = async (data: any) => {
    setPageLoading(true);
    try {
      const res = await getConfigContent({
        ids: data.config_ids,
      });
      setConfigForm(res);
      const plugins = OBJECT_CONFIG_MAP[data.objName].plugins || {};
      const _PluginName = Object.keys(plugins).find(
        (key) =>
          plugins[key]?.collect_type === data.collect_type &&
          (plugins[key]?.config_type || []).includes(data.config_type)
      );
      setCollectType(data.collect_type);
      setPluginName(_PluginName as string);
      initData(res || {}, {
        plugin_name: _PluginName,
        collect_type: data.collect_type,
      });
    } finally {
      setPageLoading(false);
    }
  };

  // 根据自定义hook，生成不同的模板
  const { formItems } = useFormItems({
    collectType,
    columns: [],
    pluginName,
    mode: 'edit',
  });

  const initData = (row: TableDataItem, config: TableDataItem) => {
    const formData: Record<string, any> = cloneDeep(
      row?.child?.content?.config || {}
    );
    const base: Record<string, any> = cloneDeep(row?.base?.content || {});
    const envConfig: Record<string, any> = cloneDeep(
      row?.base?.env_config || {}
    );
    if (formData.interval) {
      formData.interval = +formData.interval.replace('s', '');
    }
    if (formData.timeout) {
      formData.timeout = +formData.timeout.replace('s', '');
    }
    if (
      [
        'Switch SNMP General',
        'Firewall SNMP General',
        'Detection Device SNMP General',
        'Loadbalance SNMP General',
        'Router SNMP General',
        'Scanning Device SNMP General',
        'Bastion Host SNMP General',
        'Storage SNMP General',
        'Hardware Server SNMP General',
      ].includes(config.plugin_name)
    ) {
      formData.monitor_ip =
        extractMongoDBUrl(formData.agents?.[0] || '').host || '';
      formData.port = extractMongoDBUrl(formData.agents?.[0] || '').port || '';
    }
    if (['Hardware Server IPMI', 'Storage IPMI'].includes(config.plugin_name)) {
      Object.assign(formData, extractIPMIUrl(formData.servers?.[0] || ''));
    }
    if (['Website', 'Ping', 'Apache', 'Nginx'].includes(config.plugin_name)) {
      formData.monitor_url = formData.urls?.[0] || '';
    }
    if (['Tomcat', 'RabbitMQ', 'ActiveMQ'].includes(config.plugin_name)) {
      formData.monitor_url = formData.url || '';
    }
    if (['Zookeeper', 'ClickHouse'].includes(config.plugin_name)) {
      formData.monitor_url = formData.servers?.[0] || '';
    }
    if (['MongoDB', 'Redis'].includes(config.plugin_name)) {
      Object.assign(formData, extractMongoDBUrl(formData.servers?.[0] || ''));
    }
    if (['VMWare', 'Tencent Cloud'].includes(config.plugin_name)) {
      Object.assign(formData, extractVmvareUrl(formData));
    }
    if (config.collect_type === 'jmx') {
      formData.monitor_url = base.jmxUrl || '';
      formData.username = base.username;
      formData.password = base.password;
      formData.LISTEN_PORT = envConfig.LISTEN_PORT || null;
    }
    if (config.collect_type === 'exporter') {
      Object.assign(formData, envConfig);
    }
    switch (config.plugin_name) {
      case 'ElasticSearch':
        formData.server = formData.servers?.[0];
        break;
      case 'Mysql':
        Object.assign(formData, extractMysqlUrl(formData.servers?.[0] || ''));
        break;
      case 'Postgres':
        Object.assign(formData, extractPostgresUrl(formData.address || ''));
        break;
      case 'Consul':
        formData.monitor_url = formData.address || '';
        break;
      case 'Host':
        formData.metric_type = [formData.tags?.config_type];
        formData.monitor_ip =
          (formData.tags?.instance_id || '').split('-')?.[0] || '';
        break;
      case 'SNMP Trap':
        formData.monitor_ip =
          (formData.tags?.instance_id || '')
            .split('-')?.[0]
            ?.replace('trap', '') || '';
        break;
      default:
        break;
    }
    form.setFieldsValue(formData);
  };

  const extractMongoDBUrl = (url: string) => {
    const regex = /\/\/(?:(.+):(.+)@)?([^:]+):(\d+)/;
    const matches = url.match(regex);
    if (matches) {
      const [, username, password, host, port] = matches;
      const result: any = {};
      if (host) {
        result.host = host;
      }
      if (port) {
        result.port = port;
      }
      if (username && password) {
        result.username = username;
        result.password = password;
      }
      return result;
    }
    return {};
  };

  const extractMysqlUrl = (url: string) => {
    const regex = /^([^:]+):([^@]+)@tcp\(([^:]+):(\d+)\)/;
    const matches = url.match(regex);
    if (!matches || matches.length < 5) {
      return {};
    }
    return {
      username: matches[1],
      password: matches[2],
      host: matches[3],
      port: matches[4],
    };
  };

  const extractPostgresUrl = (url: string) => {
    const result = {
      host: '',
      port: '',
      username: '',
      password: '',
    };
    const regex =
      /(?:host=([^\s]+))|(?:port=([^\s]+))|(?:user=([^\s]+))|(?:password=([^\s]+))/g;
    let match;
    while ((match = regex.exec(url)) !== null) {
      if (match[1]) result.host = match[1];
      if (match[2]) result.port = match[2];
      if (match[3]) result.username = match[3];
      if (match[4]) result.password = match[4];
    }
    return result;
  };

  const extractIPMIUrl = (url: string) => {
    const regex = /([^:]+):([^@]+)@([^()]+)\(([^)]+)\)/;
    const match = url.match(regex);
    if (!match || match.length < 5) {
      return {};
    }
    return {
      monitor_ip: match[4],
      protocol: match[3],
      username: match[1],
      password: match[2],
    };
  };

  const extractVmvareUrl = (obj: any) => {
    try {
      return {
        ...obj.http_headers,
        host: obj.tags.instance_id.replace('vc-', ''),
      };
    } catch {
      return {};
    }
  };

  const handleCancel = () => {
    form.resetFields();
    setModalVisible(false);
    setPageLoading(false);
  };

  const handleSubmit = () => {
    form.validateFields().then((values) => {
      operateConfig(values);
    });
  };

  const operateConfig = async (params: TableDataItem) => {
    if (collectType !== 'jmx') {
      if (
        [
          'Switch SNMP General',
          'Firewall SNMP General',
          'Detection Device SNMP General',
          'Loadbalance SNMP General',
          'Router SNMP General',
          'Scanning Device SNMP General',
          'Bastion Host SNMP General',
          'Storage SNMP General',
          'Hardware Server SNMP General',
        ].includes(pluginName)
      ) {
        delete params.monitor_ip;
        delete params.port;
        Object.assign(configForm.child.content.config, params);
      }
      switch (pluginName) {
        case 'ElasticSearch':
          configForm.child.content.config.servers = [params.server];
          break;
        default:
          break;
      }
      if (params.timeout) {
        configForm.child.content.config.timeout = params.timeout + 's';
      }
    }
    ['LISTEN_PORT', 'HOST', 'PASSWORD', 'PORT', 'SERVICE_NAME', 'USER'].forEach(
      (item) => {
        if (params[item]) {
          configForm.base.env_config[item] = params[item];
        }
      }
    );
    configForm.child.content.config.interval = params.interval + 's';
    try {
      setConfirmLoading(true);
      await post(
        '/monitor/api/node_mgmt/update_instance_collect_config/',
        configForm
      );
      message.success(t('common.successfullyModified'));
      handleCancel();
      onSuccess();
    } catch (error) {
      console.log(error);
    } finally {
      setConfirmLoading(false);
    }
  };

  return (
    <OperateModal
      width={700}
      title={title}
      visible={modalVisible}
      onCancel={handleCancel}
      footer={
        <div>
          <Button
            className="mr-[10px]"
            type="primary"
            loading={confirmLoading}
            disabled={pageLoading}
            onClick={handleSubmit}
          >
            {t('common.confirm')}
          </Button>
          <Button onClick={handleCancel}>{t('common.cancel')}</Button>
        </div>
      }
    >
      <Spin spinning={pageLoading}>
        <div className="px-[10px]">
          <Form ref={formRef} form={form} name="basic" layout="vertical">
            {formItems}
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
          </Form>
        </div>
      </Spin>
    </OperateModal>
  );
});

UpdateConfig.displayName = 'UpdateConfig';

export default UpdateConfig;

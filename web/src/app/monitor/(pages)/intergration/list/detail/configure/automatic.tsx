import React, { useState, useRef, useEffect, useMemo } from 'react';
import { Form, Input, Select, Button, message, InputNumber } from 'antd';
import { useTranslation } from '@/utils/i18n';
import CustomTable from '@/components/custom-table';
import { v4 as uuidv4 } from 'uuid';
import {
  deepClone,
  getConfigByPluginName,
  getConfigByObjectName,
} from '@/app/monitor/utils/common';
import {
  useMiddleWareFields,
  TIMEOUT_UNITS,
} from '@/app/monitor/constants/monitor';
import { useSearchParams, useRouter } from 'next/navigation';
import useApiClient from '@/utils/request';
import useMonitorApi from '@/app/monitor/api';
import { useCommon } from '@/app/monitor/context/common';
import { Organization, TableDataItem } from '@/app/monitor/types';
import {
  IntergrationAccessProps,
  IntergrationMonitoredObject,
} from '@/app/monitor/types/monitor';
import { useUserInfoContext } from '@/context/userInfo';
import { useColumnsAndFormItems } from '@/app/monitor/hooks/intergration';
import Permission from '@/components/permission';

const { Option } = Select;

const AutomaticConfiguration: React.FC<IntergrationAccessProps> = ({
  showInterval = true,
}) => {
  const [form] = Form.useForm();
  const { t } = useTranslation();
  const searchParams = useSearchParams();
  const { isLoading } = useApiClient();
  const { getMonitorNodeList, updateNodeChildConfig } = useMonitorApi();
  const commonContext = useCommon();
  const router = useRouter();
  const userContext = useUserInfoContext();
  const currentGroup = useRef(userContext?.selectedGroup);
  const groupId = [currentGroup?.current?.id || ''];
  const authList = useRef(commonContext?.authOrganizations || []);
  const organizationList: Organization[] = authList.current;
  const pluginName = searchParams.get('collect_type') || '';
  const objectName = searchParams.get('name') || '';
  const objectId = searchParams.get('id') || '';
  const [dataSource, setDataSource] = useState<IntergrationMonitoredObject[]>(
    []
  );
  const [nodeList, setNodeList] = useState<TableDataItem[]>([]);
  const [confirmLoading, setConfirmLoading] = useState<boolean>(false);
  const [nodesLoading, setNodesLoading] = useState<boolean>(false);
  const middleWareFieldsMap = useMiddleWareFields();

  const columns: any[] = [
    {
      title: t('monitor.intergrations.node'),
      dataIndex: 'node_ids',
      key: 'node_ids',
      width: 200,
      render: (_: unknown, record: TableDataItem, index: number) => (
        <Select
          showSearch
          loading={nodesLoading}
          value={record.node_ids}
          onChange={(val) => handleFilterNodeChange(val, index)}
          filterOption={(input, option: any) =>
            (option?.label || '').toLowerCase().includes(input.toLowerCase())
          }
          options={getFilterNodes(record.node_ids).map((item) => ({
            value: item.id,
            label: `${item.name}（${item.ip}）`,
          }))}
        ></Select>
      ),
    },
    {
      title: t('monitor.intergrations.node'),
      dataIndex: 'node_ids',
      key: 'node_ids',
      width: 200,
      render: (_: unknown, record: TableDataItem, index: number) => (
        <Select
          showSearch
          mode="tags"
          maxTagCount="responsive"
          loading={nodesLoading}
          value={record.node_ids}
          onChange={(val) => handleNodeChange(val, index)}
          filterOption={(input, option: any) =>
            (option?.label || '').toLowerCase().includes(input.toLowerCase())
          }
          options={nodeList.map((item) => ({
            value: item.id,
            label: `${item.name}（${item.ip}）`,
          }))}
        ></Select>
      ),
    },
    {
      title: 'IP',
      dataIndex: 'ip',
      key: 'ip',
      width: 200,
      render: (_: unknown, record: TableDataItem, index: number) => (
        <Input
          value={record.ip}
          onChange={(e) =>
            handleFieldAndInstNameChange(e, {
              index,
              field: 'ip',
            })
          }
        />
      ),
    },
    {
      title: middleWareFieldsMap[pluginName] || middleWareFieldsMap.default,
      dataIndex: 'url',
      key: 'url',
      width: 200,
      render: (_: unknown, record: TableDataItem, index: number) => (
        <Input
          value={record.url}
          onChange={(e) =>
            handleFieldAndInstNameChange(e, {
              index,
              field: 'url',
            })
          }
        />
      ),
    },
    {
      title: t('monitor.intergrations.instanceName'),
      dataIndex: 'instance_name',
      key: 'instance_name',
      width: 200,
      render: (_: unknown, record: TableDataItem, index: number) => (
        <Input
          value={record.instance_name}
          onChange={(e) =>
            handleInputChange(e, {
              index,
              field: 'instance_name',
            })
          }
        />
      ),
    },
    {
      title: t('common.group'),
      dataIndex: 'group_ids',
      key: 'group_ids',
      width: 200,
      render: (_: unknown, record: TableDataItem, index: number) => (
        <Select
          showSearch
          mode="tags"
          maxTagCount="responsive"
          value={record.group_ids}
          onChange={(val) => handleGroupChange(val, index)}
        >
          {organizationList.map((item) => (
            <Option key={item.value} value={item.value}>
              {item.label}
            </Option>
          ))}
        </Select>
      ),
    },
    {
      title: t('common.action'),
      key: 'action',
      dataIndex: 'action',
      width: 160,
      fixed: 'right',
      render: (_: unknown, record: TableDataItem, index: number) => (
        <>
          <Button
            type="link"
            className="mr-[10px]"
            onClick={() => handleAdd(record.key)}
          >
            {t('common.add')}
          </Button>
          {!['host', 'trap'].includes(collectType) && (
            <Button
              type="link"
              className="mr-[10px]"
              onClick={() => handleCopy(record as IntergrationMonitoredObject)}
            >
              {t('common.copy')}
            </Button>
          )}
          {!!index && (
            <Button type="link" onClick={() => handleDelete(record.key)}>
              {t('common.delete')}
            </Button>
          )}
        </>
      ),
    },
    {
      title: t('monitor.intergrations.endpoint'),
      dataIndex: 'endpoint',
      key: 'endpoint',
      width: 200,
      render: (_: unknown, record: TableDataItem, index: number) => (
        <Input
          value={record.endpoint}
          onChange={(e) =>
            handleFieldAndInstNameChange(e, {
              index,
              field: 'endpoint',
            })
          }
        />
      ),
    },
    {
      title: t('monitor.intergrations.servers'),
      dataIndex: 'server',
      key: 'server',
      width: 200,
      render: (_: unknown, record: TableDataItem, index: number) => (
        <Input
          value={record.server}
          onChange={(e) =>
            handleFieldAndInstNameChange(e, {
              index,
              field: 'server',
            })
          }
        />
      ),
    },
    {
      title: t('monitor.intergrations.host'),
      dataIndex: 'host',
      key: 'host',
      width: 200,
      render: (_: unknown, record: TableDataItem, index: number) => (
        <Input
          value={record.host}
          onChange={(e) =>
            handleFieldAndInstNameChange(e, {
              index,
              field: 'host',
              dataIndex: 'port',
            })
          }
        />
      ),
    },
    {
      title: t('monitor.intergrations.port'),
      dataIndex: 'port',
      key: 'port',
      width: 200,
      render: (_: unknown, record: TableDataItem, index: number) => (
        <InputNumber
          value={record.port}
          className="w-full"
          min={1}
          precision={0}
          onChange={(val) =>
            handlePortAndInstNameChange(val, {
              index,
              field: 'port',
              dataIndex: 'host',
            })
          }
        />
      ),
    },
    {
      title: t('monitor.intergrations.host'),
      dataIndex: 'host',
      key: 'host',
      width: 200,
      render: (_: unknown, record: TableDataItem, index: number) => (
        <Input
          value={record.host}
          onChange={(e) =>
            handleFieldAndInstNameChange(e, {
              index,
              field: 'host',
            })
          }
        />
      ),
    },
    {
      title: middleWareFieldsMap.default,
      dataIndex: 'jmx_url',
      key: 'jmx_url',
      width: 200,
      render: (_: unknown, record: TableDataItem, index: number) => (
        <Input
          value={record.jmx_url}
          onChange={(e) =>
            handleFieldAndInstNameChange(e, {
              index,
              field: 'jmx_url',
            })
          }
        />
      ),
    },
    {
      title: t('monitor.intergrations.listeningPort'),
      dataIndex: 'ENV_LISTEN_PORT',
      key: 'ENV_LISTEN_PORT',
      width: 200,
      render: (_: unknown, record: TableDataItem, index: number) => (
        <InputNumber
          value={record.ENV_LISTEN_PORT}
          className="w-full"
          min={1}
          precision={0}
          onChange={(e) =>
            handleInputChange(e, {
              index,
              field: 'ENV_LISTEN_PORT',
            })
          }
        />
      ),
    },
    {
      title: t('monitor.intergrations.host'),
      dataIndex: 'ENV_HOST',
      key: 'ENV_HOST',
      width: 200,
      render: (_: unknown, record: TableDataItem, index: number) => (
        <Input
          value={record.ENV_HOST}
          onChange={(e) =>
            handleFieldAndInstNameChange(e, {
              index,
              field: 'ENV_HOST',
              dataIndex: 'ENV_PORT',
            })
          }
        />
      ),
    },
    {
      title: t('monitor.intergrations.port'),
      dataIndex: 'ENV_PORT',
      key: 'ENV_PORT',
      width: 200,
      render: (_: unknown, record: TableDataItem, index: number) => (
        <InputNumber
          value={record.ENV_PORT}
          className="w-full"
          min={1}
          precision={0}
          onChange={(val) =>
            handlePortAndInstNameChange(val, {
              index,
              field: 'ENV_PORT',
              dataIndex: 'ENV_HOST',
            })
          }
        />
      ),
    },
  ];

  const collectType = useMemo(() => {
    return getConfigByPluginName(pluginName, 'collect_type');
  }, [pluginName]);

  const instType = useMemo(() => {
    return getConfigByObjectName(objectName, 'instance_type');
  }, [objectName]);

  const configTypes = useMemo(() => {
    return getConfigByPluginName(pluginName, 'config_type');
  }, [pluginName]);

  const initItems = useMemo(() => {
    const initItem = {
      key: uuidv4(),
      node_ids: null,
      instance_name: null,
      group_ids: groupId,
    };
    if (['web', 'ping', 'middleware'].includes(collectType)) {
      return { ...initItem, url: null };
    }
    if (['snmp', 'ipmi'].includes(collectType)) {
      return { ...initItem, ip: null };
    }
    if (collectType === 'jmx') {
      return { ...initItem, jmx_url: null, ENV_LISTEN_PORT: null };
    }
    if (collectType === 'docker') {
      return { ...initItem, endpoint: null };
    }
    if (['database', 'bkpull'].includes(collectType)) {
      return pluginName === 'ElasticSearch'
        ? { ...initItem, server: null }
        : { ...initItem, host: null, port: null };
    }
    if (collectType === 'exporter') {
      return {
        ...initItem,
        ENV_LISTEN_PORT: null,
        ENV_HOST: null,
        ENV_PORT: null,
      };
    }
    if (pluginName === 'VMWare') {
      return { ...initItem, host: null };
    }
    return initItem as IntergrationMonitoredObject;
  }, [collectType, groupId, pluginName]);

  // 使用自定义 Hook
  const { displaycolumns, formItems } = useColumnsAndFormItems({
    collectType,
    columns,
    pluginName,
  });

  useEffect(() => {
    if (isLoading) return;
    setDataSource([initItems]);
    getNodeList();
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

  const getNodeList = async () => {
    setNodesLoading(true);
    try {
      const data = await getMonitorNodeList({
        cloud_region_id: 0,
        page: 1,
        page_size: -1,
        is_active: true,
      });
      setNodeList(data.nodes || []);
    } finally {
      setNodesLoading(false);
    }
  };

  const getFilterNodes = (id: string) => {
    if (['ipmi', 'snmp'].includes(collectType)) {
      return nodeList;
    }
    const nodeIds = dataSource
      .map((item) => item.node_ids)
      .filter((item) => item !== id);
    const _nodeList = nodeList.filter(
      (item) => !nodeIds.includes(item.id as string)
    );
    return _nodeList;
  };

  const handleAdd = (key: string) => {
    const index = dataSource.findIndex((item) => item.key === key);
    const newData: IntergrationMonitoredObject = {
      ...initItems,
      key: uuidv4(),
    };
    const updatedData = [...dataSource];
    updatedData.splice(index + 1, 0, newData); // 在当前行下方插入新数据
    setDataSource(updatedData);
  };

  const handleCopy = (row: IntergrationMonitoredObject) => {
    const index = dataSource.findIndex((item) => item.key === row.key);
    const newData: IntergrationMonitoredObject = { ...row, key: uuidv4() };
    const updatedData = [...dataSource];
    updatedData.splice(index + 1, 0, newData);
    setDataSource(updatedData);
  };

  const handleDelete = (key: string) => {
    setDataSource(dataSource.filter((item) => item.key !== key));
  };

  const handleSave = () => {
    form.validateFields().then((values) => {
      // 处理表单提交逻辑
      const _values = deepClone(values);
      delete _values.metric_type;
      delete _values.nodes;
      const params = {
        configs: getConfigs(_values),
        collect_type: collectType,
        monitor_object_id: +objectId,
        collector: getConfigByPluginName(pluginName, 'collector'),
        instances: dataSource.map((item) => {
          const { key, ...rest } = item;
          values.key = key;
          return {
            ...rest,
            node_ids: [item.node_ids].flat(),
            instance_type: instType,
            instance_id: getInstId(item),
          };
        }),
      };
      addNodesConfig(params);
    });
  };

  const getConfigs = (row: TableDataItem) => {
    if (row.timeout) {
      row.timeout = row.timeout + 's';
    }
    if (collectType === 'host') {
      return form.getFieldValue('metric_type').map((item: string) => ({
        type: item,
        ...row,
      }));
    }
    if (collectType === 'http') {
      row.custom_headers = { username: row.username, password: row.password };
      delete row.username;
      delete row.password;
    }
    return [{ type: configTypes[0], ...row }];
  };

  const getInstId = (row: IntergrationMonitoredObject) => {
    const target: any = nodeList.find((item) => row.node_ids === item.id);
    if (['snmp', 'ipmi'].includes(collectType)) {
      return objectName + '-' + (row.ip || '');
    }
    if (pluginName === 'Tencent Cloud' || collectType === 'docker') {
      return row.instance_name;
    }
    switch (collectType) {
      case 'host':
        return target?.ip + '-' + target?.cloud_region;
      case 'trap':
        return 'trap' + target?.ip + '-' + target?.cloud_region;
      case 'database':
        return row.server || `${row.host}:${row.port}`;
      case 'http':
        return `vc-${row.host}`;
      case 'jmx':
        return row.jmx_url;
      case 'exporter':
        return `${row.ENV_HOST}:${row.ENV_PORT}`;
      case 'bkpull':
        return `${row.host}:${row.port}`;
      default:
        return row.url;
    }
  };

  const addNodesConfig = async (params = {}) => {
    try {
      setConfirmLoading(true);
      await updateNodeChildConfig(params);
      message.success(t('common.addSuccess'));
      const searchParams = new URLSearchParams({
        objId: objectId,
      });
      const targetUrl = `/monitor/intergration/list?${searchParams.toString()}`;
      router.push(targetUrl);
    } finally {
      setConfirmLoading(false);
    }
  };

  const handleFilterNodeChange = (val: string, index: number) => {
    const _dataSource = deepClone(dataSource);
    _dataSource[index].node_ids = val;
    if (['host', 'trap'].includes(collectType)) {
      _dataSource[index].instance_name =
        nodeList.find((item) => item.id === val)?.name || '';
    }
    setDataSource(_dataSource);
  };

  const handleNodeChange = (val: string[], index: number) => {
    const _dataSource = deepClone(dataSource);
    _dataSource[index].node_ids = val;
    setDataSource(_dataSource);
  };

  const handleGroupChange = (val: string[], index: number) => {
    const _dataSource = deepClone(dataSource);
    _dataSource[index].group_ids = val;
    setDataSource(_dataSource);
  };

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement>,
    config: {
      index: number;
      field: string;
    }
  ) => {
    const _dataSource = deepClone(dataSource);
    _dataSource[config.index][config.field] = e?.target?.value || e;
    setDataSource(_dataSource);
  };

  const handlePortAndInstNameChange = (
    val: number,
    config: {
      index: number;
      field: string;
      dataIndex: string;
    }
  ) => {
    const _dataSource = deepClone(dataSource);
    const host = _dataSource[config.index][config.dataIndex] || '';
    _dataSource[config.index][config.field] = val;
    _dataSource[config.index].instance_name = `${host}:${val || ''}`;
    setDataSource(_dataSource);
  };

  const handleFieldAndInstNameChange = (
    e: React.ChangeEvent<HTMLInputElement>,
    config: {
      index: number;
      field: string;
      dataIndex?: string;
    }
  ) => {
    const _dataSource = deepClone(dataSource);
    if (['port', 'ENV_PORT'].includes(config.dataIndex as string)) {
      const port = _dataSource[config.index][config.dataIndex as string] || '';
      _dataSource[config.index][config.field] = e.target.value;
      _dataSource[config.index].instance_name = `${e.target.value}:${port}`;
      setDataSource(_dataSource);
      return;
    }
    _dataSource[config.index][config.field] = _dataSource[
      config.index
    ].instance_name = e.target.value;
    setDataSource(_dataSource);
  };

  return (
    <div className="px-[10px]">
      <Form form={form} name="basic" layout="vertical">
        <b className="text-[14px] flex mb-[10px] ml-[-10px]">
          {t('monitor.intergrations.configuration')}
        </b>
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
        <b className="text-[14px] flex mb-[10px] ml-[-10px]">
          {t('monitor.intergrations.basicInformation')}
        </b>
        <Form.Item
          label={t('monitor.intergrations.MonitoredObject')}
          name="nodes"
          rules={[
            {
              required: true,
              validator: async () => {
                if (!dataSource.length) {
                  return Promise.reject(new Error(t('common.required')));
                }
                if (
                  dataSource.some((item) =>
                    Object.values(item).some((value) => !value)
                  )
                ) {
                  return Promise.reject(new Error(t('common.required')));
                }
                return Promise.resolve();
              },
            },
          ]}
        >
          <CustomTable
            scroll={{ y: 'calc(100vh - 490px)', x: 'calc(100vw - 320px)' }}
            dataSource={dataSource}
            columns={displaycolumns}
            rowKey="key"
            pagination={false}
          />
        </Form.Item>
        <Form.Item>
          <Permission requiredPermissions={['Add']}>
            <Button
              type="primary"
              loading={confirmLoading}
              onClick={handleSave}
            >
              {t('common.confirm')}
            </Button>
          </Permission>
        </Form.Item>
      </Form>
    </div>
  );
};

export default AutomaticConfiguration;

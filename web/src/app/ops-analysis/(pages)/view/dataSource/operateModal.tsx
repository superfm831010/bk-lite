import React, { useEffect } from 'react';
import { Drawer, Form, Input, Select, Button, DatePicker, Switch } from 'antd';
import dayjs, { Dayjs } from 'dayjs';
import { useTranslation } from '@/utils/i18n';
import CustomTable from '@/components/custom-table';
import { OperateModalProps } from '@/app/ops-analysis/types/dataSource';

const natsOptions = [
  { label: 'NATS-A', value: 'nats-a' },
  { label: 'NATS-B', value: 'nats-b' },
];

const paramsMock = [
  { key: 'param1', value: 'value1', type: 'string' },
  { key: 'param2', value: '2024-07-14', type: 'date' },
  { key: 'param3', value: true, type: 'boolean' },
  { key: 'param4', value: 123, type: 'number' },
];

const OperateModal: React.FC<OperateModalProps> = ({
  open,
  currentRow,
  onClose,
  onSuccess,
}) => {
  const { t } = useTranslation();
  const [form] = Form.useForm();
  const [showParams, setShowParams] = React.useState(false);
  const [params, setParams] = React.useState(paramsMock);

  useEffect(() => {
    if (open) {
      form.resetFields();
      if (currentRow) {
        form.setFieldsValue(currentRow);
        setShowParams(
          currentRow.nats === 'nats-a' || currentRow.nats === 'nats-b'
        );
      } else {
        setShowParams(false);
      }
    }
  }, [open, currentRow, form]);

  const handleNatsChange = (val: string) => {
    setShowParams(!!val);
    setParams(paramsMock);
  };
  const handleAliasChange = (val: string, key: string) => {
    setParams((prev) =>
      prev.map((item) => (item.key === key ? { ...item, alias: val } : item))
    );
  };
  const handleDefaultChange = (val: any, key: string, type: string) => {
    setParams((prev) =>
      prev.map((item) => {
        if (item.key !== key) return item;
        let newValue = val;
        if (type === 'boolean') {
          newValue = val;
        } else if (type === 'number') {
          newValue = Number(val);
        } else if (type === 'date') {
          if (!val) {
            newValue = '';
          } else if (val.format) {
            newValue = val.format('YYYY-MM-DD');
          } else {
            newValue = val;
          }
        }
        return { ...item, value: newValue };
      })
    );
  };

  const columns = [
    { title: t('dataSource.name'), dataIndex: 'key', key: 'key', width: 120 },
    {
      title: t('dataSource.aliasName'),
      dataIndex: 'alias',
      key: 'alias',
      width: 150,
      render: (_: any, record: any) => (
        <Input
          value={record.alias ?? record.key}
          onChange={(e) => handleAliasChange(e.target.value, record.key)}
          placeholder="Alias Name"
          size="small"
        />
      ),
    },
    {
      title: t('dataSource.defaultValue'),
      dataIndex: 'value',
      key: 'value',
      width: 180,
      render: (text: any, record: any) => {
        if (record.type === 'date') {
          return (
            <DatePicker
              value={text ? dayjs(text) : undefined}
              onChange={(date: Dayjs | null) =>
                handleDefaultChange(date, record.key, 'date')
              }
              size="small"
              style={{ width: '100%' }}
            />
          );
        }
        if (record.type === 'boolean') {
          return (
            <Switch
              checked={!!text}
              onChange={(val: boolean) =>
                handleDefaultChange(val, record.key, 'boolean')
              }
              size="small"
            />
          );
        }
        if (record.type === 'number') {
          return (
            <Input
              type="number"
              value={text}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                handleDefaultChange(e.target.value, record.key, 'number')
              }
              placeholder="Default value"
              size="small"
            />
          );
        }
        return (
          <Input
            value={text}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              handleDefaultChange(e.target.value, record.key, 'string')
            }
            placeholder="Default value"
            size="small"
          />
        );
      },
    },
  ];

  const onFinish = () => {
    onClose();
    onSuccess && onSuccess();
  };

  return (
    <Drawer
      title={
        currentRow
          ? `${t('common.edit')} ${t('dataSource.title')} - ${currentRow.name}`
          : `${t('common.edit')} ${t('dataSource.title')}`
      }
      placement="right"
      width={680}
      open={open}
      onClose={onClose}
      footer={
        <div style={{ textAlign: 'right' }}>
          <Button type="primary" onClick={() => form.submit()}>
            {t('common.confirm')}
          </Button>
          <Button style={{ marginLeft: 8 }} onClick={onClose}>
            {t('common.cancel')}
          </Button>
        </div>
      }
    >
      <Form
        form={form}
        layout="horizontal"
        labelCol={{ span: 3 }}
        onFinish={onFinish}
      >
        <Form.Item
          name="nats"
          label={t('dataSource.nats')}
          rules={[{ required: true, message: t('common.selectMsg') }]}
        >
          <Select
            options={natsOptions}
            onChange={handleNatsChange}
            placeholder={t('common.selectMsg')}
          />
        </Form.Item>
        <Form.Item
          name="name"
          label={t('dataSource.name')}
          rules={[{ required: true, message: t('common.inputMsg') }]}
        >
          <Input placeholder={t('common.inputMsg')} />
        </Form.Item>
        <Form.Item name="describe" label={t('dataSource.describe')}>
          <Input.TextArea rows={3} placeholder={t('common.inputMsg')} />
        </Form.Item>
        {showParams && (
          <Form.Item label={t('dataSource.params')} colon={false}>
            <CustomTable
              columns={columns}
              dataSource={params}
              rowKey="key"
              pagination={false}
              size="small"
            />
          </Form.Item>
        )}
      </Form>
    </Drawer>
  );
};

export default OperateModal;

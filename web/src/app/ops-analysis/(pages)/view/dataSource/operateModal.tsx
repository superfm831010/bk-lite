import React, { useEffect } from 'react';
import dayjs, { Dayjs } from 'dayjs';
import { v4 as uuidv4 } from 'uuid';
import CustomTable from '@/components/custom-table';
import { PlusOutlined, MinusCircleOutlined } from '@ant-design/icons';
import { useDataSourceApi } from '@/app/ops-analysis/api/dataSource';
import { useTranslation } from '@/utils/i18n';
import {
  OperateModalProps,
  ParamItem,
} from '@/app/ops-analysis/types/dataSource';
import {
  Drawer,
  Form,
  Input,
  Select,
  Button,
  DatePicker,
  Switch,
  message,
} from 'antd';

const paramTypeOptions = [
  { label: '字符串', value: 'string' },
  { label: '数字', value: 'number' },
  { label: '日期', value: 'date' },
  { label: '布尔', value: 'boolean' },
];

const OperateModal: React.FC<OperateModalProps> = ({
  open,
  currentRow,
  onClose,
  onSuccess,
}) => {
  const { t } = useTranslation();
  const [form] = Form.useForm();
  const [params, setParams] = React.useState<ParamItem[]>([]);
  const [loading, setLoading] = React.useState(false);
  const [duplicateNames, setDuplicateNames] = React.useState<string[]>([]);
  const { createDataSource, updateDataSource } = useDataSourceApi();

  useEffect(() => {
    if (open) {
      form.resetFields();
      setParams([]);
      setDuplicateNames([]);
      if (currentRow) {
        form.setFieldsValue(currentRow);
        if (currentRow.params && Array.isArray(currentRow.params)) {
          setParams(
            currentRow.params.map((param: any) => ({
              ...param,
              type: param.type || 'string',
              id: param.id || uuidv4(), // 为现有参数生成ID
            }))
          );
        }
      }
    }
  }, [open, currentRow, form]);

  // 检查参数名重复
  const checkDuplicateNames = (currentParams: ParamItem[]) => {
    const nameCount: { [key: string]: number } = {};
    const duplicates: string[] = [];

    currentParams.forEach((param) => {
      if (param.name && param.name.trim()) {
        nameCount[param.name] = (nameCount[param.name] || 0) + 1;
      }
    });

    Object.keys(nameCount).forEach((name) => {
      if (nameCount[name] > 1) {
        duplicates.push(name);
      }
    });

    setDuplicateNames(duplicates);
    return duplicates.length === 0;
  };

  const handleAliasChange = (val: string, id: string) => {
    setParams((prev: ParamItem[]) =>
      prev.map((item) => (item.id === id ? { ...item, alias_name: val } : item))
    );
  };

  const handleDefaultChange = (val: any, id: string, type: string) => {
    setParams((prev: ParamItem[]) =>
      prev.map((item) => {
        if (item.id !== id) return item;
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

  const handleTypeChange = (val: string, id: string) => {
    setParams((prev: ParamItem[]) =>
      prev.map((item) => {
        if (item.id !== id) return item;
        let newValue: any = '';
        if (val === 'boolean') {
          newValue = false;
        } else if (val === 'number') {
          newValue = 0;
        } else if (val === 'date') {
          newValue = '';
        }
        return { ...item, type: val, value: newValue };
      })
    );
  };

  const handleAddParam = () => {
    const newParam: ParamItem = {
      id: uuidv4(),
      name: '',
      value: '',
      type: 'string',
      alias_name: '',
    };
    setParams([...params, newParam]);
  };

  const handleDeleteParam = (id: string) => {
    const newParams = params.filter((item) => item.id !== id);
    setParams(newParams);
    checkDuplicateNames(newParams);
  };

  const handleParamNameChange = (val: string, id: string) => {
    const newParams = params.map((item) => {
      if (item.id === id) {
        return {
          ...item,
          name: val,
          // 如果别名为空或等于旧的参数名，则同步更新别名
          alias_name:
            !item.alias_name || item.alias_name === item.name
              ? val
              : item.alias_name,
        };
      }
      return item;
    });
    setParams(newParams);
  };

  const handleParamNameBlur = (val: string, id: string) => {
    const newParams = params.map((item) => {
      if (item.id === id) {
        return { ...item, name: val.trim() };
      }
      return item;
    });
    setParams(newParams);
    checkDuplicateNames(newParams);
  };

  const columns = [
    {
      title: t('dataSource.name'),
      dataIndex: 'name',
      key: 'name',
      width: 120,
      render: (_: any, record: ParamItem) => (
        <Input
          value={record.name}
          placeholder="名称"
          onChange={(e) => handleParamNameChange(e.target.value, record.id!)}
          onBlur={(e) => handleParamNameBlur(e.target.value, record.id!)}
          status={duplicateNames.includes(record.name) ? 'error' : undefined}
        />
      ),
    },
    {
      title: t('dataSource.aliasName'),
      dataIndex: 'alias_name',
      key: 'alias_name',
      width: 120,
      render: (_: any, record: ParamItem) => (
        <Input
          value={record.alias_name || record.name}
          placeholder="别名"
          onChange={(e) => handleAliasChange(e.target.value, record.id!)}
        />
      ),
    },
    {
      title: '参数类型',
      dataIndex: 'type',
      key: 'type',
      width: 120,
      render: (_: any, record: ParamItem) => (
        <Select
          value={record.type || 'string'}
          options={paramTypeOptions}
          style={{ width: '100%' }}
          onChange={(val) => handleTypeChange(val, record.id!)}
        />
      ),
    },
    {
      title: t('dataSource.defaultValue'),
      dataIndex: 'value',
      key: 'value',
      width: 150,
      render: (text: any, record: ParamItem) => {
        const type = record.type || 'string';
        if (type === 'date') {
          return (
            <DatePicker
              value={text ? dayjs(text) : undefined}
              onChange={(date: Dayjs | null) =>
                handleDefaultChange(date, record.id!, 'date')
              }
              style={{ width: '100%' }}
            />
          );
        }
        if (type === 'boolean') {
          return (
            <Switch
              checked={!!text}
              onChange={(val: boolean) =>
                handleDefaultChange(val, record.id!, 'boolean')
              }
            />
          );
        }
        if (type === 'number') {
          return (
            <Input
              type="number"
              value={text}
              placeholder="默认值"
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                handleDefaultChange(e.target.value, record.id!, 'number')
              }
            />
          );
        }
        return (
          <Input
            value={text}
            placeholder="默认值"
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              handleDefaultChange(e.target.value, record.id!, 'string')
            }
          />
        );
      },
    },
    {
      title: '操作',
      key: 'action',
      width: 80,
      render: (_: any, record: ParamItem) => (
        <Button
          type="text"
          danger
          size="small"
          icon={<MinusCircleOutlined />}
          onClick={() => handleDeleteParam(record.id!)}
        />
      ),
    },
  ];

  const onFinish = async (values: any) => {
    try {
      setLoading(true);

      // 检查参数名是否有重复
      if (!checkDuplicateNames(params)) {
        message.error('参数名不允许重复');
        setLoading(false);
        return;
      }

      // 检查是否有空的参数名
      const hasEmptyName = params.some(
        (param) => !param.name || !param.name.trim()
      );
      if (hasEmptyName) {
        message.error('参数名不能为空');
        setLoading(false);
        return;
      }

      const submitData = {
        ...values,
        // 提交时去除id字段，只保留业务字段
        params: params.map((param) => ({
          name: param.name,
          alias_name: param.alias_name,
          type: param.type,
          value: param.value,
        })),
      };

      if (currentRow) {
        await updateDataSource(currentRow.id, submitData);
        message.success('更新数据源成功');
      } else {
        await createDataSource(submitData);
        message.success('创建数据源成功');
      }

      onClose();
      onSuccess && onSuccess();
    } catch (error: any) {
      message.error(error.message || '操作失败');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Drawer
      title={
        currentRow
          ? `${t('common.edit')}${t('dataSource.title')} - ${currentRow.name}`
          : `${t('common.add')}${t('dataSource.title')}`
      }
      placement="right"
      width={750}
      open={open}
      onClose={onClose}
      footer={
        <div style={{ textAlign: 'right' }}>
          <Button
            type="primary"
            loading={loading}
            onClick={() => form.submit()}
          >
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
          name="rest_api"
          label="NATS"
          rules={[{ required: true, message: t('common.inputMsg') }]}
        >
          <Input placeholder={t('common.inputMsg')} />
        </Form.Item>
        <Form.Item
          name="name"
          label={t('dataSource.name')}
          rules={[{ required: true, message: t('common.inputMsg') }]}
        >
          <Input placeholder={t('common.inputMsg')} />
        </Form.Item>
        <Form.Item name="desc" label={t('dataSource.describe')}>
          <Input.TextArea rows={3} placeholder={t('common.inputMsg')} />
        </Form.Item>
        <Form.Item label={t('dataSource.params')} colon={false}>
          <div style={{ marginBottom: 16 }}>
            <Button
              type="dashed"
              onClick={handleAddParam}
              icon={<PlusOutlined />}
              block
            >
              添加参数
            </Button>
          </div>
          {params.length > 0 && (
            <>
              <CustomTable
                rowKey="id"
                columns={columns}
                dataSource={params}
                pagination={false}
              />
              {duplicateNames.length > 0 && (
                <div
                  style={{
                    color: '#ff4d4f',
                    fontSize: '12px',
                    marginTop: '8px',
                    padding: '4px 8px',
                    backgroundColor: '#fff2f0',
                    border: '1px solid #ffccc7',
                    borderRadius: '4px',
                  }}
                >
                  参数名重复：{duplicateNames.join('、')}
                </div>
              )}
            </>
          )}
        </Form.Item>
      </Form>
    </Drawer>
  );
};

export default OperateModal;

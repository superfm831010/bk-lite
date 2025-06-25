'use client';

import React, { useState, useEffect } from 'react';
import PermissionWrapper from '@/components/permission';
import { useCommon } from '@/app/alarm/context/common';
import { useTranslation } from '@/utils/i18n';
import {
  Card,
  Typography,
  Form,
  InputNumber,
  Select,
  Checkbox,
  Button,
  Space,
  Switch,
} from 'antd';

interface Config {
  interval: number;
  persons: string[];
  method: string[];
}

export default function UnallocatedNotificationConfig() {
  const { t } = useTranslation();
  const { userList } = useCommon();
  const [editMode, setEditMode] = useState(false);
  const [expanded, setExpanded] = useState(true);
  const [config, setConfig] = useState<Config>({
    interval: 60,
    persons: [],
    method: ['email'],
  });
  const [form] = Form.useForm<Config>();

  useEffect(() => {
    form.setFieldsValue(config);
  }, [form, config]);

  const assigneeOptions = userList.map((u) => ({
    label: `${u.display_name} (${u.username})`,
    value: u.username,
  }));

  const enterEdit = () => {
    setEditMode(true);
  };

  const cancelEdit = () => {
    form.setFieldsValue(config);
    setEditMode(false);
  };

  const confirmEdit = async () => {
    const values = await form.validateFields();
    setConfig(values);
    setEditMode(false);
  };

  return (
    <Card style={{ height: '100%' }}>
      <div className="h-full w-[600px]">
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            marginBottom: 10,
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <div
              style={{
                width: 4,
                height: 16,
                backgroundColor: '#1890ff',
                marginRight: 8,
              }}
            />
            <Typography.Title level={4} style={{ margin: 0, fontSize: '16px' }}>
              {t('settings.globalConfig.title')}
            </Typography.Title>
          </div>
          <Switch
            size="small"
            className="ml-[24px]"
            checked={expanded}
            onChange={(checked) => setExpanded(checked)}
          />
        </div>
        {expanded && (
          <div className="ml-[12px]">
            <div className="mb-[20px] text-[var(--color-text-3)]">
              {t('settings.globalConfig.description')}
            </div>
            <Form
              form={form}
              layout="horizontal"
              initialValues={config}
              style={{ maxWidth: 500 }}
            >
              <Form.Item
                name="interval"
                label={t('settings.globalConfig.intervalLabel')}
                rules={[
                  {
                    required: true,
                    message:
                      t('common.inputMsg') +
                      t('settings.globalConfig.intervalLabel'),
                  },
                ]}
              >
                <InputNumber
                  min={1}
                  addonAfter={t('settings.globalConfig.intervalMinutes')}
                  disabled={!editMode}
                  style={{ width: '160px' }}
                />
              </Form.Item>

              <Form.Item
                name="persons"
                label={t('settings.globalConfig.personnelLabel')}
                rules={[
                  {
                    required: true,
                    message:
                      t('common.selectMsg') +
                      t('settings.globalConfig.personnelLabel'),
                  },
                ]}
              >
                <Select
                  mode="multiple"
                  showSearch
                  placeholder={t('settings.globalConfig.personnelPlaceholder')}
                  options={assigneeOptions}
                  disabled={!editMode}
                  filterOption={(input: string, option?: any) =>
                    !!option?.label?.toLowerCase().includes(input.toLowerCase())
                  }
                />
              </Form.Item>

              <Form.Item
                name="method"
                label={t('settings.globalConfig.notificationMethodLabel')}
                rules={[
                  {
                    required: true,
                    message:
                      t('common.selectMsg') +
                      t('settings.globalConfig.notificationMethodLabel'),
                  },
                ]}
              >
                <Checkbox.Group
                  options={[
                    { label: t('settings.globalConfig.email'), value: 'email' },
                    {
                      label: t('settings.globalConfig.wechat'),
                      value: 'wechat',
                    },
                  ]}
                  disabled={!editMode}
                />
              </Form.Item>

              <Form.Item>
                <Space>
                  {editMode ? (
                    <>
                      <Button type="primary" onClick={confirmEdit}>
                        {t('common.confirm')}
                      </Button>
                      <Button onClick={cancelEdit}>{t('common.cancel')}</Button>
                    </>
                  ) : (
                    <PermissionWrapper requiredPermissions={['Edit']}>
                      <Button type="primary" onClick={enterEdit}>
                        {t('common.edit')}
                      </Button>
                    </PermissionWrapper>
                  )}
                </Space>
              </Form.Item>
            </Form>
          </div>
        )}
      </div>
    </Card>
  );
}

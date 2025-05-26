'use client';

import React, { useState, useEffect } from 'react';
import { Switch, message, Modal, Form, Input, Segmented, Menu, InputNumber, Button } from 'antd';
import { useTranslation } from '@/utils/i18n';
import EntityList from '@/components/entity-list';
import { useSecurityApi } from '@/app/system-manager/api/security';

interface AuthSource {
  id: string;
  name: string;
  description: string;
  icon: string;
  tagList?: string[];
}

const SecurityPage: React.FC = () => {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState('1');
  const [otpEnabled, setOtpEnabled] = useState(false);
  const [pendingOtpEnabled, setPendingOtpEnabled] = useState(false);
  const [loading, setLoading] = useState(false);
  const [loginExpiredTime, setLoginExpiredTime] = useState<string>('24');
  const [pendingLoginExpiredTime, setPendingLoginExpiredTime] = useState<string>('24');
  const [authSources, setAuthSources] = useState<AuthSource[]>([
    {
      id: '1',
      name: '微信开放平台',
      description: '支持微信平台扫码登陆！！！',
      icon: 'weixingongzhonghao',
      tagList: ['OAuth2.0']
    }
  ]);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [editingSource, setEditingSource] = useState<AuthSource | null>(null);
  const [form] = Form.useForm();
  const { getSystemSettings, updateOtpSettings } = useSecurityApi();

  useEffect(() => {
    fetchSystemSettings();
  }, []);

  const fetchSystemSettings = async () => {
    try {
      setLoading(true);
      const settings = await getSystemSettings();
      const otpValue = settings.enable_otp === '1';
      setOtpEnabled(otpValue);
      setPendingOtpEnabled(otpValue);
      const expiredTime = settings.login_expired_time || '24';
      setLoginExpiredTime(expiredTime);
      setPendingLoginExpiredTime(expiredTime);
    } catch (error) {
      console.error('Failed to fetch system settings:', error);
      message.error(t('common.fetchFailed'));
    } finally {
      setLoading(false);
    }
  };

  const handleOtpChange = (checked: boolean) => {
    setPendingOtpEnabled(checked);
  };

  const handleLoginExpiredTimeChange = (value: string) => {
    setPendingLoginExpiredTime(value);
  };

  const handleSaveSettings = async () => {
    try {
      setLoading(true);
      await updateOtpSettings({ 
        enableOtp: pendingOtpEnabled ? '1' : '0', 
        loginExpiredTime: pendingLoginExpiredTime 
      });
      setOtpEnabled(pendingOtpEnabled);
      setLoginExpiredTime(pendingLoginExpiredTime);
      message.success(t('common.updateSuccess'));
    } catch (error) {
      console.error('Failed to update settings:', error);
      setPendingOtpEnabled(otpEnabled);
      setPendingLoginExpiredTime(loginExpiredTime);
    } finally {
      setLoading(false);
    }
  };

  const handleEditSource = (source: AuthSource) => {
    setEditingSource(source);
    form.setFieldsValue(source);
    setIsModalVisible(true);
  };

  const handleDeleteSource = (source: AuthSource) => {
    Modal.confirm({
      title: t('common.confirm'),
      content: t('common.deleteConfirm').replace('{name}', source.name),
      onOk: () => {
        setAuthSources(authSources.filter(item => item.id !== source.id));
        message.success(t('common.deleteSuccess'));
      }
    });
  };

  const handleModalOk = () => {
    form.validateFields().then(values => {
      if (editingSource) {
        // Edit existing source
        setAuthSources(authSources.map(item => 
          item.id === editingSource.id ? { ...item, ...values } : item
        ));
        message.success(t('common.updateSuccess'));
      } else {
        const newSource = {
          id: Date.now().toString(),
          ...values,
          tagList: ['OAuth2.0']
        };
        setAuthSources([...authSources, newSource]);
        message.success(t('common.addSuccess'));
      }
      setIsModalVisible(false);
    });
  };

  const menuActions = (item: AuthSource) => (
    <Menu>
      <Menu.Item key="edit" onClick={() => handleEditSource(item)}>
        {t('common.edit')}
      </Menu.Item>
      <Menu.Item key="delete" onClick={() => handleDeleteSource(item)}>
        {t('common.delete')}
      </Menu.Item>
    </Menu>
  );

  const tabContent = {
    '1': (
      <div className="bg-[var(--color-bg)] p-4 rounded-lg shadow-sm mb-4">
        <h3 className="text-base font-semibold mb-4">{t('system.security.loginSettings')}</h3>
        <div className="flex items-center mb-4">
          <span className="text-xs mr-4">{t('system.security.otpSetting')}</span>
          <Switch 
            size="small" 
            checked={pendingOtpEnabled} 
            onChange={handleOtpChange}
            loading={loading}
          />
        </div>
        <div className="flex items-center mb-4">
          <span className="text-xs mr-4">{t('system.security.loginExpiredTime')}</span>
          <InputNumber
            min="1"
            value={pendingLoginExpiredTime}
            onChange={(value) => handleLoginExpiredTimeChange(value?.toString() || '24')}
            disabled={loading}
            addonAfter={t('system.security.hours')}
            style={{ width: '180px' }}                           
          />
        </div>
        <div className="mt-6">
          <Button 
            type="primary" 
            loading={loading} 
            onClick={handleSaveSettings}
          >
            {t('common.save')}
          </Button>
        </div>
      </div>
    ),
    '2': (
      <EntityList
        data={authSources}
        loading={false}
        search={false}
        menuActions={menuActions}
        onCardClick={handleEditSource}
      />
    )
  };

  return (
    <div className="w-full">
      <Segmented
        options={[
          { label: t('system.security.settings'), value: '1' },
          { label: t('system.security.authSources'), value: '2' }
        ]}
        value={activeTab}
        onChange={(value) => setActiveTab(value as string)}
        className="mb-4"
      />
      
      {tabContent[activeTab as '1' | '2']}

      <Modal
        title={editingSource ? t('common.edit') : t('common.add')}
        open={isModalVisible}
        onOk={handleModalOk}
        onCancel={() => setIsModalVisible(false)}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label={t('common.name')}
            rules={[{ required: true, message: t('common.required') }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="description"
            label={t('common.description')}
          >
            <Input.TextArea rows={3} />
          </Form.Item>
          <Form.Item
            name="icon"
            label={t('common.icon')}
            rules={[{ required: true, message: t('common.required') }]}
            initialValue="weixin"
          >
            <Input />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default SecurityPage;

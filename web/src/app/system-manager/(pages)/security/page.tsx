'use client';

import React, { useState, useEffect } from 'react';
import { Switch, message, Form, Input, Segmented, Menu, InputNumber, Button, Alert } from 'antd';
import { CopyOutlined } from '@ant-design/icons';
import { useTranslation } from '@/utils/i18n';
import EntityList from '@/components/entity-list';
import OperateModal from '@/components/operate-modal';
import { useSecurityApi } from '@/app/system-manager/api/security';
import { AuthSource } from '@/app/system-manager/types/security';
import { enhanceAuthSourcesList } from '@/app/system-manager/utils/authSourceUtils';
import wechatAuthImg from '@/app/system-manager/img/wechat_auth.png';

const SecurityPage: React.FC = () => {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState('1');
  const [otpEnabled, setOtpEnabled] = useState(false);
  const [pendingOtpEnabled, setPendingOtpEnabled] = useState(false);
  const [loading, setLoading] = useState(false);
  const [authSourcesLoading, setAuthSourcesLoading] = useState(false);
  const [loginExpiredTime, setLoginExpiredTime] = useState<string>('24');
  const [pendingLoginExpiredTime, setPendingLoginExpiredTime] = useState<string>('24');
  const [authSources, setAuthSources] = useState<AuthSource[]>([]);
  const [authSourcesLoaded, setAuthSourcesLoaded] = useState(false);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [editingSource, setEditingSource] = useState<AuthSource | null>(null);
  const [modalLoading, setModalLoading] = useState(false);
  const [form] = Form.useForm();
  const { getSystemSettings, updateOtpSettings, getAuthSources, updateAuthSource } = useSecurityApi();

  useEffect(() => {
    fetchSystemSettings();
  }, []);

  useEffect(() => {
    if (activeTab === '2' && !authSourcesLoaded) {
      fetchAuthSources();
    }
  }, [activeTab, authSourcesLoaded]);

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
    } finally {
      setLoading(false);
    }
  };

  const fetchAuthSources = async () => {
    try {
      setAuthSourcesLoading(true);
      const data = await getAuthSources();
      const enhancedData = enhanceAuthSourcesList(data || []);
      console.log('Fetched auth sources:', enhancedData);
      setAuthSources(enhancedData);
      setAuthSourcesLoaded(true);
    } catch (error) {
      console.error('Failed to fetch auth sources:', error);
      setAuthSources([]);
      setAuthSourcesLoaded(true);
    } finally {
      setAuthSourcesLoading(false);
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
    form.setFieldsValue({
      name: source.name,
      app_id: source.app_id,
      app_secret: source.app_secret,
      enabled: source.enabled,
      redirect_uri: source.other_config.redirect_uri,
      callback_url: source.other_config.callback_url
    });
    setIsModalVisible(true);
  };

  const handleModalOk = async () => {
    try {
      setModalLoading(true);
      const values = await form.validateFields();
      if (editingSource) {
        const updateData = {
          name: values.name,
          app_id: values.app_id,
          app_secret: values.app_secret,
          other_config: {
            callback_url: values.callback_url || editingSource.other_config.callback_url,
            redirect_uri: values.redirect_uri
          },
          enabled: values.enabled
        };
        
        await updateAuthSource(editingSource.id, updateData);
        
        const updatedSource = { ...editingSource, ...updateData };
        const enhancedSource = enhanceAuthSourcesList([updatedSource])[0];
        
        setAuthSources(authSources.map(item => 
          item.id === editingSource.id 
            ? enhancedSource
            : item
        ));
        
        message.success(t('common.updateSuccess'));
        setIsModalVisible(false);
        setEditingSource(null);
        form.resetFields();
      }
    } catch (error) {
      console.error('Failed to update auth source:', error);
      message.error(t('common.updateFailed'));
    } finally {
      setModalLoading(false);
    }
  };

  const handleModalCancel = () => {
    if (modalLoading) return; // 防止在loading时关闭
    setIsModalVisible(false);
    setEditingSource(null);
    form.resetFields();
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text).then(() => {
      message.success(t('common.copySuccess'));
    }).catch(() => {
      message.error(t('common.copyFailed'));
    });
  };

  const menuActions = (item: AuthSource) => (
    <Menu>
      <Menu.Item key="edit" onClick={() => handleEditSource(item)}>
        {t('common.edit')}
      </Menu.Item>
    </Menu>
  );

  const handleTabChange = (value: string) => {
    setActiveTab(value);
  };

  const getAuthImageSrc = (sourceType: string) => {
    const imageMap: Record<string, string> = {
      wechat: wechatAuthImg.src,
      // 添加其他认证方式的图片
    };
    return imageMap[sourceType] || undefined;
  };

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
            onClick={handleSaveSettings}
            loading={loading}
          >
            {t('common.save')}
          </Button>
        </div>
      </div>
    ),
    '2': (
      <EntityList
        data={authSources}
        loading={authSourcesLoading}
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
        onChange={handleTabChange}
        className="mb-4"
      />
      
      {tabContent[activeTab as '1' | '2']}

      <OperateModal
        title={t('common.edit')}
        open={isModalVisible}
        onOk={handleModalOk}
        onCancel={handleModalCancel}
        width={800}
        confirmLoading={modalLoading}
        maskClosable={!modalLoading}
      >
        <Alert type="info" showIcon message={t('system.security.informationTip')} className='mb-4'  />
        <div className="flex gap-6">
          <div className="flex-1">
            <Form form={form} layout="vertical">
              <Form.Item
                name="name"
                label={t('system.security.loginMethodName')}
                rules={[{ required: true, message: `${t('common.inputMsg')} ${t('system.security.loginMethodName')}` }]}
              >
                <Input placeholder={`${t('common.inputMsg')} ${t('system.security.loginMethodName')}`} />
              </Form.Item>
              
              <Form.Item
                name="app_id"
                label={t('system.security.appId')}
                rules={[{ required: true, message: `${t('common.inputMsg')} ${t('system.security.appId')}` }]}
              >
                <Input placeholder={`${t('common.inputMsg')} ${t('system.security.appId')}`} />
              </Form.Item>
              
              <Form.Item
                name="app_secret"
                label={t('system.security.appSecret')}
                rules={[{ required: true, message: `${t('common.inputMsg')} ${t('system.security.appSecret')}` }]}
              >
                <Input.Password placeholder={`${t('common.inputMsg')} ${t('system.security.appSecret')}`} />
              </Form.Item>
              
              <Form.Item
                name="redirect_uri"
                label={t('system.security.redirectUri')}
              >
                <Input 
                  suffix={
                    <Button 
                      type="text" 
                      icon={<CopyOutlined />} 
                      size="small"
                      onClick={() => copyToClipboard(form.getFieldValue('redirect_uri') || '')}
                    />
                  }
                />
              </Form.Item>
              
              <Form.Item
                name="callback_url"
                label={t('system.security.callbackUrl')}
              >
                <Input 
                  suffix={
                    <Button 
                      type="text" 
                      icon={<CopyOutlined />} 
                      size="small"
                      onClick={() => copyToClipboard(form.getFieldValue('callback_url') || '')}
                    />
                  }
                />
              </Form.Item>

              <Form.Item
                name="enabled"
                label={t('system.security.enabled')}
                valuePropName="checked"
              >
                <Switch size="small" />
              </Form.Item>
            </Form>
          </div>
          
          <div className="w-64 flex justify-center items-start pt-8">
            {editingSource && getAuthImageSrc(editingSource.source_type) && (
              <img 
                src={getAuthImageSrc(editingSource.source_type)}
                alt={`${editingSource.source_type} auth`}
                className="max-w-full h-auto"
                onError={(e) => {
                  e.currentTarget.style.display = 'none';
                }}
              />
            )}
          </div>
        </div>
      </OperateModal>
    </div>
  );
};

export default SecurityPage;

'use client';

import React, { useState, useEffect } from 'react';
import { Switch, message, Form, Segmented, Menu, InputNumber, Button, Alert } from 'antd';
import { PlusOutlined, CopyOutlined } from '@ant-design/icons';
import { useTranslation } from '@/utils/i18n';
import EntityList from '@/components/entity-list';
import OperateModal from '@/components/operate-modal';
import DynamicForm from '@/components/dynamic-form';
import { useSecurityApi } from '@/app/system-manager/api/security';
import { AuthSource } from '@/app/system-manager/types/security';
import PermissionWrapper from '@/components/permission';
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
  const [dynamicForm] = Form.useForm();
  const { getSystemSettings, updateOtpSettings, getAuthSources, updateAuthSource, createAuthSource } = useSecurityApi();

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

  const getNewAuthSourceFormFields = () => [
    {
      name: 'name',
      type: 'input',
      label: t('system.security.authSourceName'),
      placeholder: `${t('common.inputMsg')}${t('system.security.authSourceName')}`,
      rules: [{ required: true, message: `${t('common.inputMsg')}${t('system.security.authSourceName')}` }]
    },
    {
      name: 'source_type',
      type: 'select',
      label: t('system.security.authSourceType'),
      placeholder: `${t('common.select')}${t('system.security.authSourceType')}`,
      options: [
        { value: 'bklite', label: 'BK-Lite认证源' }
      ],
      rules: [{ required: true, message: `${t('common.select')}${t('system.security.authSourceType')}` }]
    },
    {
      name: 'namespace',
      type: 'input',
      label: t('system.security.namespace'),
      placeholder: `${t('common.inputMsg')}${t('system.security.namespace')}`
    },
    {
      name: 'domain',
      type: 'input',
      label: t('system.security.domain'),
      placeholder: `${t('common.inputMsg')}${t('system.security.domain')}`
    },
    {
      name: 'org_root_dn',
      type: 'input',
      label: t('system.security.orgRootDn'),
      placeholder: `${t('common.inputMsg')}${t('system.security.orgRootDn')}`
    },
    {
      name: 'user_init_role',
      type: 'input',
      label: t('system.security.userInitRole'),
      placeholder: `${t('common.inputMsg')}${t('system.security.userInitRole')}`
    },
    {
      name: 'sync_enabled',
      type: 'switch',
      label: t('system.security.syncEnabled'),
      size: 'small',
      initialValue: false
    },
    {
      name: 'description',
      type: 'textarea',
      label: t('common.description'),
      placeholder: `${t('common.inputMsg')}${t('common.description')}`,
      rows: 4
    }
  ];

  const getWeChatFormFields = () => [
    {
      name: 'name',
      type: 'input',
      label: t('system.security.loginMethodName'),
      placeholder: `${t('common.inputMsg')}${t('system.security.loginMethodName')}`,
      rules: [{ required: true, message: `${t('common.inputMsg')}${t('system.security.loginMethodName')}` }]
    },
    {
      name: 'app_id',
      type: 'input',
      label: t('system.security.appId'),
      placeholder: `${t('common.inputMsg')}${t('system.security.appId')}`,
      rules: [{ required: true, message: `${t('common.inputMsg')}${t('system.security.appId')}` }]
    },
    {
      name: 'app_secret',
      type: 'editablePwd',
      label: t('system.security.appSecret'),
      placeholder: `${t('common.inputMsg')}${t('system.security.appSecret')}`,
      rules: [{ required: true, message: `${t('common.inputMsg')}${t('system.security.appSecret')}` }]
    },
    {
      name: 'redirect_uri',
      type: 'input',
      label: t('system.security.redirectUri'),
      placeholder: `${t('common.inputMsg')}${t('system.security.redirectUri')}`,
      suffix: <CopyOutlined onClick={() => copyToClipboard(dynamicForm.getFieldValue('redirect_uri'))} />
    },
    {
      name: 'enabled',
      type: 'switch',
      label: t('system.security.enabled'),
      initialValue: true,
      size: 'small'
    }
  ];

  const handleAddAuthSource = () => {
    setEditingSource(null);
    dynamicForm.resetFields();
    setIsModalVisible(true);
  };

  const handleAuthSourceSubmit = async () => {
    try {
      setModalLoading(true);
      
      if (editingSource) {
        const values = await dynamicForm.validateFields();
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
      } else {
        const values = await dynamicForm.validateFields();
        const createData = {
          name: values.name,
          source_type: values.source_type,
          namespace: values.namespace,
          domain: values.domain,
          org_root_dn: values.org_root_dn,
          user_init_role: values.user_init_role,
          sync_enabled: values.sync_enabled || false,
          description: values.description
        };
        
        const newSource = await createAuthSource(createData);
        const enhancedSource = enhanceAuthSourcesList([newSource])[0];
        
        setAuthSources([...authSources, enhancedSource]);
        message.success(t('common.createSuccess'));
      }
      
      setIsModalVisible(false);
      setEditingSource(null);
      dynamicForm.resetFields();
    } catch (error) {
      console.error('Failed to save auth source:', error);
      message.error(editingSource ? t('common.updateFailed') : t('common.createFailed'));
    } finally {
      setModalLoading(false);
    }
  };

  const handleModalCancel = () => {
    if (modalLoading) return;
    setIsModalVisible(false);
    setEditingSource(null);
    dynamicForm.resetFields();
  };

  const handleEditSource = (source: AuthSource) => {
    setEditingSource(source);
    
    if (source.source_type === 'wechat') {
      dynamicForm.setFieldsValue({
        name: source.name,
        app_id: source.app_id,
        app_secret: source.app_secret,
        enabled: source.enabled,
        redirect_uri: source.other_config.redirect_uri,
        callback_url: source.other_config.callback_url
      });
    } else {
      dynamicForm.setFieldsValue({
        name: source.name,
        source_type: source.source_type,
      });
    }
    
    setIsModalVisible(true);
  };

  const handleSearch = (searchTerm: string) => {
    console.log('Searching for:', searchTerm);
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
      <PermissionWrapper requiredPermissions={['Edit']}>
        <Menu.Item key="edit" onClick={() => handleEditSource(item)}>
          {t('common.edit')}
        </Menu.Item>
      </PermissionWrapper>
    </Menu>
  );

  const handleTabChange = (value: string) => {
    setActiveTab(value);
  };

  const getAuthImageSrc = (sourceType: string) => {
    const imageMap: Record<string, string> = {
      wechat: wechatAuthImg.src,
    };
    return imageMap[sourceType] || undefined;
  };

  const operateSection = (
    <PermissionWrapper requiredPermissions={['Add']}>
      <Button 
        type="primary" 
        icon={<PlusOutlined />}
        onClick={handleAddAuthSource}
        className="ml-2"
      >
        {t('common.add')}
      </Button>
    </PermissionWrapper>
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
          <PermissionWrapper requiredPermissions={['Edit']}>
            <Button 
              type="primary" 
              onClick={handleSaveSettings}
              loading={loading}
            >
              {t('common.save')}
            </Button>
          </PermissionWrapper>
        </div>
      </div>
    ),
    '2': (
      <EntityList
        data={authSources}
        loading={authSourcesLoading}
        search
        onSearch={handleSearch}
        menuActions={menuActions}
        onCardClick={handleEditSource}
        operateSection={operateSection}
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
        title={editingSource ? t('common.edit') : t('common.add')}
        open={isModalVisible}
        onOk={handleAuthSourceSubmit}
        onCancel={handleModalCancel}
        width={editingSource?.source_type === 'wechat' ? 1000 : 800}
        confirmLoading={modalLoading}
        maskClosable={!modalLoading}
      >
        {editingSource?.source_type === 'wechat' && (
          <div className="flex">
            <div className="flex-1">
              <Alert type="info" showIcon message={t('system.security.informationTip')} className='mb-4' />
              <DynamicForm
                form={dynamicForm}
                fields={getWeChatFormFields()}
              />
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
        )}
        {!editingSource?.source_type && (
          <DynamicForm
            form={dynamicForm}
            fields={getNewAuthSourceFormFields()}
          />
        )}
      </OperateModal>
    </div>
  );
};

export default SecurityPage;

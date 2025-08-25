import React, { useState, useEffect } from 'react';
import { Form, Input as AntdInput, Switch, message, Select } from 'antd';
import { useTranslation } from '@/utils/i18n';
import { useUserInfoContext } from '@/context/userInfo';
import { Model, ModelConfig, ModelGroup } from '@/app/opspilot/types/provider';
import { CONFIG_MAP, MODEL_CATEGORY_OPTIONS, getProviderType } from '@/app/opspilot/constants/provider';
import OperateModal from '@/components/operate-modal';
import EditablePasswordField from '@/components/dynamic-form/editPasswordField';
import GroupTreeSelect from '@/components/group-tree-select';
import { useProviderApi } from '@/app/opspilot/api/provider';

interface ProviderModalProps {
  visible: boolean;
  mode: 'add' | 'edit';
  filterType: string;
  model?: Model | null;
  confirmLoading: boolean;
  onOk: (values: any) => Promise<void>;
  onCancel: () => void;
}

const ProviderModal: React.FC<ProviderModalProps> = ({
  visible,
  mode,
  filterType,
  model,
  confirmLoading,
  onOk,
  onCancel,
}) => {
  const [form] = Form.useForm();
  const { t } = useTranslation();
  const { selectedGroup } = useUserInfoContext();
  const { fetchModelGroups } = useProviderApi();
  const [modelGroups, setModelGroups] = useState<ModelGroup[]>([]);
  const [groupsLoading, setGroupsLoading] = useState<boolean>(false);

  // Fetch model groups when modal opens
  useEffect(() => {
    if (visible) {
      const fetchGroups = async () => {
        setGroupsLoading(true);
        try {
          const providerType = getProviderType(filterType);
          const groups = await fetchModelGroups('', providerType);
          setModelGroups(groups);
        } catch (error) {
          console.error('Failed to fetch model groups:', error);
          message.error(t('common.fetchFailed'));
        } finally {
          setGroupsLoading(false);
        }
      };
      fetchGroups();
    }
  }, [visible, filterType]);

  React.useEffect(() => {
    if (!visible) return;
    if (mode === 'edit' && model) {
      const configField = CONFIG_MAP[filterType];
      const config = model[configField as keyof Model] as ModelConfig | undefined;
      form.setFieldsValue({
        name: model.name || '',
        modelName: (model[configField as keyof Model] as ModelConfig)?.model || '',
        model_type: model.model_type || '',
        label: model.label || '',
        team: model.team,
        apiKey: filterType === 'llm_model' ? model.llm_config?.openai_api_key || '' : config?.api_key || '',
        url: filterType === 'llm_model' ? model.llm_config?.openai_base_url || '' : config?.base_url || '',
        enabled: model.enabled || false,
        consumer_team: model.consumer_team ?? '',
      });
    } else {
      form.resetFields();
      form.setFieldsValue({
        enabled: true
      });
    }
  }, [visible, mode, model, form, filterType]);

  const handleOk = () => {
    form.validateFields()
      .then(onOk)
      .catch((info) => {
        message.error(t('common.valFailed'));
        console.error(info);
      });
  };

  return (
    <OperateModal
      title={t(mode === 'add' ? 'common.add' : 'common.edit')}
      visible={visible}
      confirmLoading={confirmLoading}
      onOk={handleOk}
      onCancel={onCancel}
      okText={t('common.confirm')}
      cancelText={t('common.cancel')}
      destroyOnClose
    >
      <Form form={form} layout="vertical">
        <Form.Item
          name="name"
          label={t('provider.form.name')}
          rules={[{ required: true, message: `${t('common.input')}${t('provider.form.name')}` }]}
        >
          <AntdInput placeholder={`${t('common.input')}${t('provider.form.name')}`} />
        </Form.Item>

        {filterType !== 'ocr_provider' && (
          <Form.Item
            name="modelName"
            label={t('provider.form.modelName')}
            rules={[{ required: true, message: `${t('common.input')}${t('provider.form.modelName')}` }]}
          >
            <AntdInput placeholder={`${t('common.input')}${t('provider.form.modelName')}`} />
          </Form.Item>
        )}

        <Form.Item
          name="model_type"
          label={t('provider.form.type')}
          rules={[{ required: true, message: `${t('common.selectMsg')}${t('provider.form.type')}` }]}
        >
          <Select 
            placeholder={`${t('common.selectMsg')}${t('provider.form.type')}`}
            loading={groupsLoading}
            showSearch
            filterOption={(input, option) =>
              (option?.children as unknown as string)?.toLowerCase().includes(input.toLowerCase())
            }
            notFoundContent={groupsLoading ? t('common.loading') : t('common.noData')}
          >
            {modelGroups.map((group) => (
              <Select.Option key={group.id} value={group.id}>
                {group.display_name || group.name}
              </Select.Option>
            ))}
          </Select>
        </Form.Item>

        {filterType === 'llm_model' && (
          <Form.Item
            name="label"
            label={t('provider.form.label')}
            rules={[{ required: true, message: `${t('common.selectMsg')}${t('provider.form.label')}` }]}
          >
            <Select 
              placeholder={`${t('common.selectMsg')}${t('provider.form.label')}`}
              showSearch
              filterOption={(input, option) =>
                (option?.children as unknown as string)?.toLowerCase().includes(input.toLowerCase())
              }
            >
              {MODEL_CATEGORY_OPTIONS.map((option) => (
                <Select.Option key={option.value} value={option.value}>
                  {option.label}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>
        )}

        <Form.Item
          name="url"
          label={t('provider.form.url')}
          rules={[{ required: true, message: `${t('common.inputMsg')}${t('provider.form.url')}` }]}
        >
          <AntdInput placeholder={`${t('common.inputMsg')} ${t('provider.form.url')}`} />
        </Form.Item>
        <Form.Item
          name="apiKey"
          label={t('provider.form.key')}
          rules={[{ required: true, message: `${t('common.inputMsg')}${t('provider.form.key')}` }]}
        >
          <EditablePasswordField
            value={form.getFieldValue('apiKey')}
            onChange={(value) => form.setFieldsValue({ apiKey: value })}
          />
        </Form.Item>
        <Form.Item
          name="enabled"
          label={t('provider.form.enabled')}
          valuePropName="checked"
        >
          <Switch size="small" />
        </Form.Item>
        <Form.Item
          name="team"
          label={t('provider.form.group')}
          rules={[{ required: true, message: `${t('common.selectMsg')}${t('provider.form.group')}` }]}
          initialValue={selectedGroup ? [selectedGroup?.id] : []}
        >
          <GroupTreeSelect
            value={form.getFieldValue('team') || []}
            onChange={(value) => form.setFieldsValue({ team: value })}
            placeholder={`${t('common.selectMsg')}${t('provider.form.group')}`}
            multiple={true}
          />
        </Form.Item>
        <Form.Item
          name="consumer_team"
          label={t('provider.form.consumerTeam')}>
          <GroupTreeSelect
            value={form.getFieldValue('consumer_team') ? [form.getFieldValue('consumer_team')] : []}
            onChange={(value) => form.setFieldsValue({ consumer_team: value[0] || '' })}
            placeholder={`${t('common.selectMsg')}${t('provider.form.consumerTeam')}`}
            multiple={false}
          />
        </Form.Item>
      </Form>
    </OperateModal>
  );
};

export default ProviderModal;

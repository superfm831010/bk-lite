import OperateModal from "@/components/operate-modal";
import { useTranslation } from "@/utils/i18n";
import usePlayroundApi from '@/app/playground/api';
import { forwardRef, useImperativeHandle, useState, useRef, useMemo, useCallback, useEffect } from 'react';
import { Button, Form, FormInstance, Input, message, Select, Switch } from 'antd';
import { ModalRef } from "@/app/playground/types";
import { CONTENT_MAP } from "@/app/playground/constants";
const { TextArea } = Input;

interface ModalProps {
  id: number;
  name: string;
  description?: string;
  parent?: number;
  is_active?: boolean;
  url?: string;
  level?: number;
  config?: object;
}

const ManageModal = forwardRef<ModalRef, any>(({ nodes, activeTag, onSuccess }, ref) => {
  const { t } = useTranslation();
  const formRef = useRef<FormInstance>(null);
  const { createCategory, createCapability, updateCapability, updateCategory } = usePlayroundApi();
  const [open, setOpen] = useState<boolean>(false);
  const [confirm, setConfirm] = useState<boolean>(false);
  const [isAddChildren, setIsAddChildren] = useState<boolean>(false);
  const [title, setTitle] = useState<string>('add');
  const [type, setType] = useState<string>('');
  const [formData, setFormData] = useState<ModalProps | null>(null);
  const CategoryType = ['addCategory', 'updateCategory'];
  const CapabilityType = ['addCapability', 'updateCapability'];

  useImperativeHandle(ref, () => ({
    showModal: ({ type, title, form }) => {
      setOpen(true);
      setType(type);
      setTitle(title as string);
      setFormData(form);
    }
  }));

  useEffect(() => {
    if (open) {
      initForm();
    }
  }, [open]);

  const parentOptions = useMemo(() => {
    return nodes.map((item: any) => ({
      label: item.name,
      value: item.key
    }));
  }, [nodes]);

  const initForm = useCallback(() => {
    if (!formRef.current) return;
    formRef.current?.resetFields();
    if (type.trim().startsWith('update')) {
      if (formData?.level === 0) setIsAddChildren(true);
      formRef.current?.setFieldsValue({
        name: formData?.name,
        description: formData?.description,
        parent: formData?.level === 0 ? null : formData?.parent,
        url: formData?.url,
        is_active: formData?.is_active
      });
    } else if (formData && type.trim().startsWith('add')) {
      setIsAddChildren(true);
      formRef.current?.setFieldsValue({
        parent: formData?.id
      });
    }
  }, [type, formData]);

  const handleAdd: Record<string, any> = {
    'addCategory': async (data: any) => await createCategory(data),
    'addCapability': async (data: any) => await createCapability(data),
    'updateCategory': async (id: number, data: any) => await updateCategory(id, data),
    'updateCapability': async (id: number, data: any) => await updateCapability(id, data),
  };


  const handleSubmit = async () => {
    setConfirm(true);
    try {
      const data = await formRef.current?.validateFields();
      const [id] = activeTag;
      const config = type.endsWith('Capability') ? { config: CONTENT_MAP['anomaly_detection'] } : {};
      const params = {
        category: id,
        ...data,
        ...config
      }
      if(!id) return message.error('未选择类别');
      if (type.trim().startsWith('add')) {
        await handleAdd[type](params);
      } else {
        await handleAdd[type](formData?.id, params);
      }
      setOpen(false);
      message.success(`common.${title}Success`);
      onSuccess();
    } catch (e) {
      console.log(e);
    } finally {
      setConfirm(false);
    }
  };

  const handleCancel = () => {
    setOpen(false);
    setConfirm(false);
    setIsAddChildren(false);
    setFormData(null);
  };

  return (
    <OperateModal
      title={t(`common.${title}`)}
      open={open}
      onCancel={handleCancel}
      footer={[
        <Button key="submit" loading={confirm} type="primary" onClick={handleSubmit}>
          {t('common.confirm')}
        </Button>,
        <Button key="cancel" onClick={handleCancel}>
          {t('common.cancel')}
        </Button>,
      ]}
    >
      <Form ref={formRef} layout="vertical">
        <Form.Item
          name='name'
          label={t(`common.name`)}
          rules={[{ required: true, message: t('common.inputMsg') }]}
        >
          <Input placeholder={t(`common.inputMsg`)} />
        </Form.Item>
        {CategoryType.includes(type) && (
          <Form.Item
            name='parent'
            label={t(`manage.parentCategory`)}
          >
            <Select disabled={isAddChildren} options={parentOptions} allowClear />
          </Form.Item>
        )}
        {CapabilityType.includes(type) && (
          <>
            <Form.Item
              name='url'
              label={t(`playground-common.url`)}
              rules={[{ required: true, message: t('common.inputMsg') }]}
            >
              <Input placeholder={t(`common.inputMsg`)} />
            </Form.Item>
            <Form.Item
              name='is_active'
              label={t(`playground-common.onlineStatus`)}
              rules={[{ required: true, message: t('common.selectMsg') }]}
              layout="horizontal"
            >
              <Switch checkedChildren="是" unCheckedChildren="否" />
            </Form.Item>
          </>
        )}
        <Form.Item
          name='description'
          label={t(`common.description`)}
        >
          <TextArea rows={3} />
        </Form.Item>
      </Form>
    </OperateModal>
  )
})

ManageModal.displayName = 'ManageModal';
export default ManageModal;
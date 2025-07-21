import OperateModal from "@/components/operate-modal";
import { useTranslation } from "@/utils/i18n";
import usePlayroundApi from '@/app/playground/api';
import { forwardRef, useImperativeHandle, useState, useRef } from 'react';
import { Button, Form, FormInstance, Input, message, Select, Switch } from 'antd';
import { ModalRef } from "@/app/playground/types";
const { TextArea } = Input;

interface ModalProps {
  name: string;
  description?: string;
  parent?: number;
  is_active?: boolean;
  url?: string;
  config?: object;
}

const ManageModal = forwardRef<ModalRef, any>(({ }, ref) => {
  const { t } = useTranslation();
  const formRef = useRef<FormInstance>(null);
  const { createCategory } = usePlayroundApi();
  const [open, setOpen] = useState<boolean>(false);
  const [confirm, setConfirm] = useState<boolean>(false);
  const [title, setTitle] = useState<string>('add');
  const [type, setType] = useState<string>('');
  const [formData, setFormData] = useState<ModalProps | null>(null);
  const CategoryType = ['addCategory', 'updateCategory', 'delCategory'];
  const CapabilityType = ['addCapability', 'updateCategory', 'delCategory'];

  useImperativeHandle(ref, () => ({
    showModal: ({ type, title, form }) => {
      setOpen(true);
      setType(type);
      setTitle(title as string);
      setFormData(form);
      console.log(type, title, form);
    }
  }));

  const handleSubmit = async () => {
    setConfirm(true);
    try {
      if(type === 'addCategory' || type === 'addCapability') {
        const data = await formRef.current?.validateFields();
        await createCategory(data);
        setOpen(false);
        message.success('添加成功');
      }
    } catch (e) {
      console.log(e)
    } finally {
      setConfirm(false);
    }
    console.log(formData);
  };

  const handleCancel = () => {
    setOpen(false);
    setConfirm(false);
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
            label='父类'
          >
            <Select options={[]} />
          </Form.Item>
        )}
        {CapabilityType.includes(type) && (
          <>
            <Form.Item
              name='url'
              label={'url'}
              rules={[{ required: true, message: t('common.inputMsg') }]}
            >
              <Input placeholder={t(`common.inputMsg`)} />
            </Form.Item>
            <Form.Item
              name='is_active'
              label={t(`common.status`)}
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
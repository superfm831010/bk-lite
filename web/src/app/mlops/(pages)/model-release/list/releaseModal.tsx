'use client';
import { ModalRef } from "@/app/mlops/types";
import { forwardRef, useImperativeHandle, useState, useRef } from "react";
import OperateModal from '@/components/operate-modal';
import { Form, FormInstance, Select, Button, Input } from "antd";
import { useTranslation } from "@/utils/i18n";
// import useMlopsApi from "@/app/mlops/api";
const { TextArea } = Input;

const ReleaseModal = forwardRef<ModalRef, any>(({ }, ref) => {
  const { t } = useTranslation();
  const formRef = useRef<FormInstance>(null);
  const [formData, setFormData] = useState(null);
  const [modalOpen, setModalOpen] = useState<boolean>(false);
  const [confirmLoading, setConfirmLoading] = useState<boolean>(false);

  useImperativeHandle(ref, () => ({
    showModal: ({ form }) => {
      setFormData(form);
      setModalOpen(true);
      setConfirmLoading(false);
    }
  }));

  const handleConfirm = () => {
    try {
      const data = formRef.current?.validateFields();
      console.log(formData, data);
      setConfirmLoading(true);
      // setModalOpen(false);
    } catch (e) {
      console.log(e);
    } finally {
      setConfirmLoading(false);
    }
  };

  const handleCancel = () => {
    setModalOpen(false);
  };

  return (
    <>
      <OperateModal
        title={t(`model-release.modalTitle`)}
        open={modalOpen}
        onCancel={() => setModalOpen(false)}
        footer={[
          <Button key='submit' type="primary" onClick={handleConfirm} loading={confirmLoading}>{t(`common.confirm`)}</Button>,
          <Button key='cancel' onClick={handleCancel}>{t(`common.cancel`)}</Button>
        ]}
      >
        <Form ref={formRef} layout="vertical">
          <Form.Item
            name='name'
            label='模型名称'
            rules={[{ required: true, message: t('common.inputMsg') }]}
          >
            <Input placeholder={t(`common.inputMsg`)} />
          </Form.Item>
          <Form.Item
            name='version'
            label='版本'
            rules={[{ required: true, message: t('common.selectMsg') }]}
          >
            <Select
              options={[
                { label: 'v1', value: 'v1' }
              ]}
              placeholder={t('common.selectMsg')}
            />
          </Form.Item>
          <Form.Item
            name='description'
            label='模型介绍'
            rules={[{ required: true, message: t('common.inputMsg') }]}
          >
            <TextArea placeholder={t(`common.inputMsg`)} rows={4} maxLength={6} />
          </Form.Item>
        </Form>
      </OperateModal>
    </>
  )
});

ReleaseModal.displayName = 'ReleaseModal';
export default ReleaseModal;
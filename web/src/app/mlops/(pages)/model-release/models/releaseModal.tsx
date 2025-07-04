'use client';
import { ModalRef } from "@/app/mlops/types";
import { forwardRef, useImperativeHandle, useState, useRef } from "react";
import OperateModal from '@/components/operate-modal';
import { Form, FormInstance, Select, Button } from "antd";
import { useTranslation } from "@/utils/i18n";
import useMlopsApi from "@/app/mlops/api";

const ReleaseModal = forwardRef<ModalRef, any>(({ }, ref) => {
  const { t } = useTranslation();
  const { getOneAnomalyTask } = useMlopsApi();
  const formRef = useRef<FormInstance>(null);
  const [formData, setFormData] = useState(null);
  const [modalOpen, setModalOpen] = useState<boolean>(false);
  const [confirmLoading, setConfirmLoading] = useState<boolean>(false);

  useImperativeHandle(ref, () => ({
    showModal: ({ form }) => {
      setFormData(form);
      setModalOpen(true);
      setConfirmLoading(false);
      getTaskInfo(form?.id)
    }
  }));

  const getTaskInfo = async (id: number) => {
    const data = await getOneAnomalyTask(id);
    console.log(data);
  }

  const handleConfirm = () => {
    console.log(formData);
    setConfirmLoading(true);
    setModalOpen(false);
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
        </Form>
      </OperateModal>
    </>
  )
});

ReleaseModal.displayName = 'ReleaseModal';
export default ReleaseModal;
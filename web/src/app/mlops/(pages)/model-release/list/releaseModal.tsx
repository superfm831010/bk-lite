'use client';
import { ModalRef, Option } from "@/app/mlops/types";
import { forwardRef, useImperativeHandle, useState, useRef, useEffect } from "react";
import OperateModal from '@/components/operate-modal';
import { Form, FormInstance, Select, Button, Input, InputNumber, message } from "antd";
import { useTranslation } from "@/utils/i18n";
import useMlopsModelReleaseApi from "@/app/mlops/api/modelRelease";
const { TextArea } = Input;

interface ReleaseModalProps {
  trainjobs: Option[],
  onSuccess: () => void;
  activeTag: string[];
}

const ReleaseModal = forwardRef<ModalRef, ReleaseModalProps>(({ trainjobs, activeTag, onSuccess }, ref) => {
  const { t } = useTranslation();
  const { addAnomalyServings, updateAnomalyServings } = useMlopsModelReleaseApi();
  const formRef = useRef<FormInstance>(null);
  const [type, setType] = useState<string>('add');
  const [formData, setFormData] = useState<any>(null);
  const [modalOpen, setModalOpen] = useState<boolean>(false);
  const [confirmLoading, setConfirmLoading] = useState<boolean>(false);

  useImperativeHandle(ref, () => ({
    showModal: ({ type, form }) => {
      setType(type);
      setFormData(form);
      setModalOpen(true);
      setConfirmLoading(false);
    }
  }));

  useEffect(() => {
    if (modalOpen) {
      initializeForm();
    }
  }, [modalOpen])

  const initializeForm = () => {
    if (!formRef.current) return;
    formRef.current.resetFields();
    if (type === 'add') {
      formRef.current.setFieldsValue({
        model_version: 'latest',
        anomaly_threshold: 0.5
      })
    } else {
      formRef.current.setFieldsValue({
        ...formData,
        status: formData.status === 'active' ? true : false
      })
    }
  };

  const handleAddMap: Record<string, (params: any) => Promise<void>> = {
    'anomaly': async (params: any) => {
      await addAnomalyServings(params);
    },
  };

  const handleUpdateMap: Record<string, (id: number, params: any) => Promise<void>> = {
    'anomaly': async (id: number, params: any) => {
      await updateAnomalyServings(id, params);
    },
  };

  const handleConfirm = async () => {
    setConfirmLoading(true);
    try {
      const [tagName] = activeTag;
      const data = await formRef.current?.validateFields();

      if (type === 'add') {
        await handleAddMap[tagName]({ status: 'active', ...data });
        message.success(t(`model-release.publishSuccess`));
      } else {
        await handleUpdateMap[tagName](formData?.id, data);
        message.success(t(`common.updateSuccess`));
      }
      setModalOpen(false);
      onSuccess();
    } catch (e) {
      console.log(e);
      message.error(t(`common.error`));
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
            label={t(`model-release.modelName`)}
            rules={[{ required: true, message: t('common.inputMsg') }]}
          >
            <Input placeholder={t(`common.inputMsg`)} />
          </Form.Item>
          <Form.Item
            name='anomaly_detection_train_job'
            label={t(`traintask.traintask`)}
            rules={[{ required: true, message: t('common.inputMsg') }]}
          >
            <Select options={trainjobs} placeholder={t(`model-release.selectTraintask`)} />
          </Form.Item>
          <Form.Item
            name='model_version'
            label={t(`model-release.modelVersion`)}
            rules={[{ required: true, message: t('common.inputMsg') }]}
          >
            <Input placeholder={t(`model-release.inputVersionMsg`)} />
          </Form.Item>
          <Form.Item
            name='anomaly_threshold'
            label={t(`model-release.modelThreshold`)}
            rules={[{ required: true, message: t('common.inputMsg') }]}
          >
            <InputNumber className="w-full" placeholder={t(`model-release.inputThreshold`)} />
          </Form.Item>
          {/* <Form.Item
            name='status'
            label={t(`mlops-common.status`)}
            layout="horizontal"
          >
            <Switch checkedChildren="是" unCheckedChildren="否" />
          </Form.Item> */}
          <Form.Item
            name='description'
            label={t(`model-release.modelDescription`)}
            rules={[{ required: true, message: t('common.inputMsg') }]}
          >
            <TextArea placeholder={t(`common.inputMsg`)} rows={4} />
          </Form.Item>
        </Form>
      </OperateModal>
    </>
  )
});

ReleaseModal.displayName = 'ReleaseModal';
export default ReleaseModal;
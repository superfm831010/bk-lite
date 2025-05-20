import React, {
  forwardRef,
  useEffect,
  // useEffect,
  useImperativeHandle,
  useRef,
  useState,
} from 'react';

import { Form, Input, FormInstance, message } from 'antd';
// import useApiClient from '@/utils/request';
import { useTranslation } from '@/utils/i18n';
import {
  ModalRef,
  ModalSuccess,
  TableDataItem,
} from '@/app/node-manager/types';
import OperateModal from '@/components/operate-modal';
import useApiCloudRegion from '@/app/node-manager/api/cloudRegion';

const CloudRegionModal = forwardRef<ModalRef, ModalSuccess>(
  ({ onSuccess }, ref) => {
    const { t } = useTranslation();
    // const { isLoading } = useApiClient();
    const { updateCloudIntro } = useApiCloudRegion();
    const cloudRegionFormRef = useRef<FormInstance>(null);
    const [openEditCloudRegion, setOpenEditCloudRegion] = useState(false);
    const [confirmLoading, setConfirmLoading] = useState<boolean>(false);
    const [title, setTitle] = useState<string>('editform');
    const [formData, setFormData] = useState<TableDataItem>();

    useImperativeHandle(ref, () => ({
      showModal: ({ type, title, form }) => {
        setTitle(title as string);
        setOpenEditCloudRegion(true);
        if (type === 'edit') {
          setFormData(form);
        }
      }
    }));

    useEffect(() => {
      cloudRegionFormRef.current?.resetFields();
      cloudRegionFormRef.current?.setFieldsValue(formData);
      console.log(formData);
    }, [cloudRegionFormRef, formData])

    const handleFormOkClick = async () => {
      setConfirmLoading(true);
      try {
        const { cloudRegion } = cloudRegionFormRef.current?.getFieldsValue();
        await updateCloudIntro(cloudRegion.id, {
          introduction: cloudRegion.introduction,
        });
        message.success(t('common.updateSuccess'));
        onSuccess();
        setOpenEditCloudRegion(false);
      } finally {
        setConfirmLoading(false);
      }
    };

    const handleCancel = () => {
      setOpenEditCloudRegion(false);
      cloudRegionFormRef.current?.resetFields();
      setConfirmLoading(false);
    };

    return (
      <div>
        <OperateModal
          title={t(`node-manager.cloudregion.${title}.title`)}
          open={openEditCloudRegion}
          okText={t('common.confirm')}
          cancelText={t('common.cancel')}
          confirmLoading={confirmLoading}
          onCancel={handleCancel}
          onOk={handleFormOkClick}
        >
          <Form layout="vertical" ref={cloudRegionFormRef} name="nest-messages">
            <Form.Item name={['cloudRegion', 'id']} hidden>
              <Input />
            </Form.Item>
            <Form.Item name={['cloudRegion', 'name']} label={t('common.name')}>
              <Input disabled placeholder={t('common.inputMsg')} />
            </Form.Item>
            <Form.Item
              name={['cloudRegion', 'introduction']}
              label={t('node-manager.cloudregion.editform.Introduction')}
            >
              <Input.TextArea rows={5} placeholder={t('common.inputMsg')} />
            </Form.Item>
          </Form>
        </OperateModal>
      </div>
    )
  });

CloudRegionModal.displayName = 'CloudRegionModal';
export default CloudRegionModal;
'use client';

import React, {
  useState,
  useRef,
  forwardRef,
  useImperativeHandle,
  useEffect,
} from 'react';
import { Button, Form, message, Input } from 'antd';
import OperateModal from '@/components/operate-modal';
import type { FormInstance } from 'antd';
import useMonitorApi from '@/app/monitor/api';
import { ModalRef, Organization } from '@/app/monitor/types';
import { InstanceInfo } from '@/app/monitor/types/monitor';
import { useTranslation } from '@/utils/i18n';
import { deepClone } from '@/app/monitor/utils/common';
import CustomCascader from '@/components/custom-cascader';

interface ModalProps {
  onSuccess: () => void;
  organizationList: Organization[];
}

const EditInstance = forwardRef<ModalRef, ModalProps>(
  ({ onSuccess, organizationList }, ref) => {
    const { updateInstanceChildConfig } = useMonitorApi();
    const { t } = useTranslation();
    const formRef = useRef<FormInstance>(null);
    const [visible, setVisible] = useState<boolean>(false);
    const [confirmLoading, setConfirmLoading] = useState<boolean>(false);
    const [configForm, setConfigForm] = useState<InstanceInfo>({});
    const [title, setTitle] = useState<string>('');

    useImperativeHandle(ref, () => ({
      showModal: ({ title, form }) => {
        // 开启弹窗的交互
        setTitle(title);
        setConfigForm(deepClone(form));
        setVisible(true);
      },
    }));

    useEffect(() => {
      if (visible) {
        formRef.current?.resetFields();
        formRef.current?.setFieldsValue({
          instance_name: configForm.instance_name,
          organization: (configForm.organization || []).map((item) =>
            Number(item)
          ),
        });
      }
    }, [visible, configForm]);

    const handleOperate = async (params: InstanceInfo) => {
      if (params) {
        console.log(params);
        return;
      }
      try {
        setConfirmLoading(true);
        await updateInstanceChildConfig(params as any);
        message.success(t('common.successfullyModified'));
        handleCancel();
        onSuccess();
      } catch (error) {
        console.log(error);
      } finally {
        setConfirmLoading(false);
      }
    };

    const handleSubmit = () => {
      formRef.current?.validateFields().then((values) => {
        handleOperate({
          ...values,
          id: configForm.instance_id,
        });
      });
    };

    const handleCancel = () => {
      setVisible(false);
    };

    return (
      <div>
        <OperateModal
          width={600}
          title={title}
          visible={visible}
          onCancel={handleCancel}
          footer={
            <div>
              <Button
                className="mr-[10px]"
                type="primary"
                loading={confirmLoading}
                onClick={handleSubmit}
              >
                {t('common.confirm')}
              </Button>
              <Button onClick={handleCancel}>{t('common.cancel')}</Button>
            </div>
          }
        >
          <Form ref={formRef} name="basic" layout="vertical">
            <Form.Item<InstanceInfo>
              label={t('monitor.intergrations.instanceName')}
              name="instance_name"
              rules={[{ required: true, message: t('common.required') }]}
            >
              <Input />
            </Form.Item>
            <Form.Item<InstanceInfo>
              label={t('monitor.group')}
              name="organization"
              rules={[{ required: true, message: t('common.required') }]}
            >
              <CustomCascader
                multiple
                showSearch
                allowClear
                maxTagCount="responsive"
                options={organizationList}
              />
            </Form.Item>
          </Form>
        </OperateModal>
      </div>
    );
  }
);
EditInstance.displayName = 'EditInstance';
export default EditInstance;

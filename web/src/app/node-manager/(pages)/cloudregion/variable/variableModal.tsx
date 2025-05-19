'use client';
import React, {
  useState,
  useRef,
  forwardRef,
  useImperativeHandle,
  useEffect,
  useMemo,
} from 'react';
import { Input, Form, message } from 'antd';
import OperateModal from '@/components/operate-modal';
import type { FormInstance } from 'antd';
import { useTranslation } from '@/utils/i18n';
import { ModalSuccess, ModalRef } from '@/app/node-manager/types';
import type { TableDataItem } from '@/app/node-manager/types';
import useApiCloudRegion from '@/app/node-manager/api/cloudRegion';
import useCloudId from '@/app/node-manager/hooks/useCloudRegionId';

const VariableModal = forwardRef<ModalRef, ModalSuccess>(
  ({ onSuccess }, ref) => {
    const { createVariable, updateVariable } = useApiCloudRegion();
    const cloudId = useCloudId();
    const { t } = useTranslation();
    const formRef = useRef<FormInstance>(null);
    const [variableVisible, setVariableVisible] = useState<boolean>(false);
    const [variableFormData, setVariableFormData] = useState<TableDataItem>();
    const [type, setType] = useState<string>('add');
    const [confirmLoading, setConfirmLoading] = useState<boolean>(false);

    const isAdd = useMemo(() => {
      return type === 'add';
    }, [type]);

    useImperativeHandle(ref, () => ({
      showModal: ({ type, form }) => {
        // 开启弹窗的交互
        setVariableVisible(true);
        setType(type);
        setVariableFormData(form);
      },
    }));

    //初始化表单的数据
    useEffect(() => {
      if (variableVisible) {
        formRef.current?.resetFields();
        formRef.current?.setFieldsValue(variableFormData);
      }
    }, [variableVisible, variableFormData]);

    //关闭用户的弹窗(取消和确定事件)
    const handleCancel = () => {
      setVariableVisible(false);
    };

    //添加变量
    const handleConfirm = async () => {
      formRef.current?.validateFields().then((values) => {
        operateVariable(values);
      });
    };

    const operateVariable = async (values: TableDataItem) => {
      setConfirmLoading(true);
      try {
        const { name, value, description } = values;
        const tempdata = {
          key: name,
          value,
          description,
          cloud_region_id: cloudId,
        };
        const request = isAdd
          ? createVariable(tempdata)
          : updateVariable(variableFormData?.key, tempdata);
        const msg = t(`common.${isAdd ? 'addSuccess' : 'updateSuccess'}`);
        await request;
        message.success(msg);
        onSuccess();
        setVariableVisible(false);
      } finally {
        setConfirmLoading(false);
      }
    };

    return (
      <OperateModal
        title={t(`common.${type}`)}
        open={variableVisible}
        okText={t('common.confirm')}
        cancelText={t('common.cancel')}
        confirmLoading={confirmLoading}
        onCancel={handleCancel}
        onOk={handleConfirm}
      >
        <Form ref={formRef} layout="vertical" colon={false}>
          <Form.Item
            name="name"
            label={t('common.name')}
            rules={[
              {
                pattern: /^[A-Za-z0-9_]+$/,
                message: t(
                  'node-manager.cloudregion.variable.variableNameTips'
                ),
              },
              {
                required: true,
                message: t('common.inputMsg'),
              },
            ]}
          >
            <Input placeholder={t('common.inputMsg')} />
          </Form.Item>
          <Form.Item
            name="value"
            label={t('node-manager.cloudregion.variable.value')}
            rules={[
              {
                required: true,
                message: t('common.inputMsg'),
              },
            ]}
          >
            <Input placeholder={t('common.inputMsg')} />
          </Form.Item>
          <Form.Item
            name="description"
            label={t('node-manager.cloudregion.variable.desc')}
          >
            <Input.TextArea rows={5} placeholder={t('common.inputMsg')} />
          </Form.Item>
        </Form>
      </OperateModal>
    );
  }
);
VariableModal.displayName = 'variableModal';
export default VariableModal;

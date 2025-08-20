"use client";
import { ModalRef } from '@/app/monitor/types';
import OperateModal from '@/components/operate-modal';
import { useTranslation } from '@/utils/i18n';
import { Button, Form, FormInstance, Input, Select, Switch } from 'antd';
import React, { useImperativeHandle, forwardRef, useRef, useEffect } from 'react';
import { useRasaFormManager } from '@/app/mlops/hooks/manage/useRasaForm';

interface RasaModalProps {
  selectKey: string;
  folder_id: string;
  onSuccess: () => void;
}

const RasaModal = forwardRef<ModalRef, RasaModalProps>(({ selectKey, folder_id, onSuccess }, ref) => {
  const { t } = useTranslation();
  const formRef = useRef<FormInstance>(null);

  const {
    visiable,
    confirmLoading,
    entityType,
    slotType,
    title,
    formData,
    showModal,
    handleSubmit,
    handleCancel,
    onEntityTypeChange,
    onSlotPredictionChange,
    onSlotTypeChange,
    handleKeyDown,
    handleNameChange,
    validateSampleList,
    renderElement,
    modalElement
  } = useRasaFormManager({
    selectKey,
    folder_id,
    formRef,
    onSuccess
  });

  useImperativeHandle(ref, () => ({
    showModal
  }));

  // 当模态框显示且有formData时，设置表单数据
  useEffect(() => {
    if (visiable && formRef.current && formData) {
      formRef.current?.resetFields();
      formRef.current?.setFieldValue('name', formData?.name);

      if (formData?.entity_type) {
        formRef.current?.setFieldValue('entity_type', formData?.entity_type);
        onEntityTypeChange(formData?.entity_type);
      } else if (formData?.slot_type) {
        formRef.current?.setFieldValue('slot_type', formData?.slot_type);
        formRef.current?.setFieldValue('is_apply', formData?.is_apply);
      }
    }
  }, [formData, visiable]);

  return (
    <>
      <OperateModal
        title={t(`datasets.${title}`)}
        open={visiable}
        onCancel={handleCancel}
        footer={[
          <Button key='confirm' type='primary' loading={confirmLoading} onClick={handleSubmit}>
            {t(`common.confirm`)}
          </Button>,
          <Button key='cancel' type='default' onClick={handleCancel}>
            {t(`common.cancel`)}
          </Button>,
        ]}
      >
        <Form ref={formRef} layout='vertical'>
          <Form.Item
            name='name'
            label={t(`common.name`)}
            rules={[
              { required: true, message: t('common.inputMsg') },
            ]}
          >
            <Input
              placeholder={"仅允许输入英文"}
              onKeyDown={handleKeyDown}
              onChange={handleNameChange}
            />
          </Form.Item>

          {selectKey === 'entity' && (
            <>
              <Form.Item
                name='entity_type'
                label={t(`common.type`)}
                rules={[
                  { required: true, message: t('common.selectMsg') },
                ]}
              >
                <Select
                  placeholder={t(`common.selectMsg`)}
                  options={[
                    { label: 'Text(需要在语料中特殊标志)', value: 'Text' },
                    { label: 'Lookup(单独定义值列表，适合枚举类型内容)', value: 'Lookup' }
                  ]}
                  onChange={onEntityTypeChange}
                />
              </Form.Item>
              {entityType === 'Lookup' && (
                <Form.Item
                  label={'样例'}
                  rules={[{ required: true, validator: validateSampleList }]}
                >
                  {renderElement}
                </Form.Item>
              )}
            </>
          )}
          {
            selectKey === 'slot' && (
              <>
                <Form.Item
                  name="slot_type"
                  label={t(`common.type`)}
                  rules={[
                    { required: true, message: t(`common.selectMsg`) }
                  ]}
                >
                  <Select options={[
                    {
                      label: 'text(记录普通文本)',
                      value: 'text'
                    },
                    {
                      label: 'categorical(记录分类类别，枚举)',
                      value: 'categorical'
                    },
                    {
                      label: 'float(记录数值类型，浮点型)',
                      value: 'float'
                    },
                    {
                      label: 'list(保存多个值的列表)',
                      value: 'list'
                    },
                    {
                      label: 'bool(布尔值，是或者否)',
                      value: 'bool'
                    },
                    {
                      label: 'int(记录数值类型，整数型)',
                      value: 'int'
                    }
                  ]} onChange={onSlotTypeChange} />
                </Form.Item>
                <Form.Item
                  name={'is_apply'}
                  label={'是否应用对话预测'}
                  rules={[
                    { required: true, message: t(`common.selectMsg`) }
                  ]}
                >
                  <Switch onChange={onSlotPredictionChange} />
                </Form.Item>
                {slotType === 'categorical' && (
                  <Form.Item
                    label={'类别'}
                    rules={[{ required: true, validator: validateSampleList }]}
                  >
                    {renderElement}
                  </Form.Item>
                )}
              </>
            )
          }
          {(!['entity', 'slot'].includes(selectKey)) && (
            <Form.Item
              label={selectKey === 'rule' ? '步骤' : '样例'}
              rules={[{ required: true, validator: validateSampleList }]}
            >
              {renderElement}
            </Form.Item>
          )}
        </Form>
      </OperateModal>
      {modalElement}
    </>
  );
});

RasaModal.displayName = 'RasaModal';
export default RasaModal;
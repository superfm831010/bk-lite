'use client';

import React, {
  useState,
  useRef,
  forwardRef,
  useImperativeHandle,
  useEffect,
  useMemo,
} from 'react';
import { Button, Form, message, Input, Select } from 'antd';
import { PlusOutlined, CloseOutlined } from '@ant-design/icons';
import OperateModal from '@/components/operate-modal';
import type { FormInstance } from 'antd';
import useLogApi from '@/app/log/api/integration';
import { ModalRef } from '@/app/log/types';
import { FilterItem, InstanceInfo } from '@/app/log/types/integration';
import { useTranslation } from '@/utils/i18n';
import GroupTreeSelector from '@/components/group-tree-select';
import { cloneDeep } from 'lodash';
const { Option } = Select;
import groupingStyle from './index.module.scss';
import {
  useConditionList,
  useTermList,
} from '@/app/log/hooks/integration/common/other';
import { ListItem } from '@/types';

interface ModalProps {
  onSuccess: () => void;
}

const EditInstance = forwardRef<ModalRef, ModalProps>(({ onSuccess }, ref) => {
  const { updateMonitorInstance, setInstancesGroup } = useLogApi();
  const { t } = useTranslation();
  const CONDITION_LIST = useConditionList();
  const TERM_LIST = useTermList();
  const formRef = useRef<FormInstance>(null);
  const [visible, setVisible] = useState<boolean>(false);
  const [confirmLoading, setConfirmLoading] = useState<boolean>(false);
  const [configForm, setConfigForm] = useState<InstanceInfo>({});
  const [title, setTitle] = useState<string>('');
  const [modalType, setModalType] = useState<string>('');
  const [term, setTerm] = useState<string | null>(null);
  const [conditions, setConditions] = useState<FilterItem[]>([
    {
      name: null,
      method: null,
      value: '',
    },
  ]);
  const [labels, setLabels] = useState<string[]>([]);

  const isEdit = useMemo(() => {
    return modalType === 'edit';
  }, [modalType]);

  useImperativeHandle(ref, () => ({
    showModal: ({ title, form, type }) => {
      // 开启弹窗的交互
      setTitle(title);
      setModalType(type);
      setConfigForm(cloneDeep(form));
      setVisible(true);
      if (type === 'edit') {
        setConditions([
          {
            name: null,
            method: '=',
            value: '123',
          },
        ]);
        setTerm('and');
      }
    },
  }));

  useEffect(() => {
    if (visible) {
      formRef.current?.resetFields();
      formRef.current?.setFieldsValue({
        name: configForm.instance_name,
        organizations: (configForm.organization || []).map((item) =>
          Number(item)
        ),
      });
      setLabels([]);
    }
  }, [visible, configForm]);

  const handleOperate = async (params: any) => {
    try {
      setConfirmLoading(true);
      const request = isEdit ? updateMonitorInstance : setInstancesGroup;
      await request(params);
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
      let params = { ...values, instance_id: configForm.instance_id };
      if (!isEdit) {
        params = {
          instance_ids: configForm.keys,
          organizations: values.organizations,
        };
      }
      handleOperate(params);
    });
  };

  const handleCancel = () => {
    setVisible(false);
    setConditions([
      {
        name: null,
        method: null,
        value: '',
      },
    ]);
    setTerm(null);
  };

  const handleLabelChange = (val: string, index: number) => {
    const _conditions = cloneDeep(conditions);
    _conditions[index].name = val;
    setConditions(_conditions);
  };

  const handleConditionChange = (val: string, index: number) => {
    const _conditions = cloneDeep(conditions);
    _conditions[index].method = val;
    setConditions(_conditions);
  };

  const handleValueChange = (
    e: React.ChangeEvent<HTMLInputElement>,
    index: number
  ) => {
    const _conditions = cloneDeep(conditions);
    _conditions[index].value = e.target.value;
    setConditions(_conditions);
  };

  const addConditionItem = () => {
    const _conditions = cloneDeep(conditions);
    _conditions.push({
      name: null,
      method: null,
      value: '',
    });
    setConditions(_conditions);
  };

  const deleteConditionItem = (index: number) => {
    const _conditions = cloneDeep(conditions);
    _conditions.splice(index, 1);
    setConditions(_conditions);
  };

  // 自定义验证条件列表
  const validateDimensions = async () => {
    if (!conditions.length || !term) {
      return Promise.reject(new Error(t('common.required')));
    }
    if (
      conditions.length &&
      conditions.some((item) => {
        return Object.values(item).some((tex) => !tex);
      })
    ) {
      return Promise.reject(new Error(t('log.integration.conditionValidate')));
    }
    return Promise.resolve();
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
            label={t('common.name')}
            name="name"
            rules={[{ required: true, message: t('common.required') }]}
          >
            <Input />
          </Form.Item>
          <Form.Item<InstanceInfo>
            label={t('log.integration.rule')}
            name="rule"
            rules={[{ required: true, validator: validateDimensions }]}
          >
            <div className="flex items-center mb-[20px]">
              <span>{t('log.integration.meetRule')}</span>
              <Select
                className="ml-[8px] flex-1"
                placeholder={t('log.integration.rule')}
                showSearch
                value={term}
                onChange={(val) => setTerm(val)}
              >
                {TERM_LIST.map((item: ListItem) => (
                  <Option value={item.id} key={item.id}>
                    {item.name}
                  </Option>
                ))}
              </Select>
            </div>
            <div className={groupingStyle.conditionItem}>
              {conditions.length ? (
                <ul className={groupingStyle.conditions}>
                  {conditions.map((conditionItem, index) => (
                    <li
                      className={`${groupingStyle.itemOption} ${groupingStyle.filter}`}
                      key={index}
                    >
                      <Select
                        style={{
                          width: '180px',
                        }}
                        placeholder={t('log.label')}
                        showSearch
                        value={conditionItem.name}
                        onChange={(val) => handleLabelChange(val, index)}
                      >
                        {labels.map((item: string) => (
                          <Option value={item} key={item}>
                            {item}
                          </Option>
                        ))}
                      </Select>
                      <Select
                        style={{
                          width: '118px',
                        }}
                        placeholder={t('log.term')}
                        value={conditionItem.method}
                        onChange={(val) => handleConditionChange(val, index)}
                      >
                        {CONDITION_LIST.map((item: ListItem) => (
                          <Option value={item.id} key={item.id}>
                            {item.name}
                          </Option>
                        ))}
                      </Select>
                      <Input
                        style={{
                          width: '180px',
                        }}
                        placeholder={t('log.value')}
                        value={conditionItem.value}
                        onChange={(e) => handleValueChange(e, index)}
                      ></Input>
                      {!!index && (
                        <Button
                          icon={<CloseOutlined />}
                          onClick={() => deleteConditionItem(index)}
                        />
                      )}
                      <Button
                        icon={<PlusOutlined />}
                        onClick={addConditionItem}
                      />
                    </li>
                  ))}
                </ul>
              ) : (
                <Button icon={<PlusOutlined />} onClick={addConditionItem} />
              )}
            </div>
          </Form.Item>
          <Form.Item<InstanceInfo>
            label={t('log.group')}
            name="organizations"
            rules={[{ required: true, message: t('common.required') }]}
          >
            <GroupTreeSelector />
          </Form.Item>
        </Form>
      </OperateModal>
    </div>
  );
});
EditInstance.displayName = 'EditInstance';
export default EditInstance;

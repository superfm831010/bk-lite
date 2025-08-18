"use client";
import { ModalRef } from '@/app/monitor/types';
import OperateModal from '@/components/operate-modal';
import { useTranslation } from '@/utils/i18n';
import { Button, Form, FormInstance, Input, message, Select } from 'antd';
import { PlusOutlined, MinusOutlined } from '@ant-design/icons';
import React, { useState, useImperativeHandle, forwardRef, useRef, useEffect } from 'react';
import { cloneDeep } from 'lodash';
import useMlopsManageApi from '@/app/mlops/api/manage';
import { Option } from '@/types';
// import useRasaForm from "@/app/mlops/hooks/manage/useRasaForm";

interface RasaModalProps {
  selectKey: string;
  folder_id: string;
  onSuccess: () => void;
}

interface FormData {
  id?: string;
  name?: string;
  dataset?: string;
  example?: string[];
  steps?: { intent?: string; response?: string }[];
  entity_type?: string;
}

interface SampleItem {
  type: 'intent' | 'response';
  select: string;
}

interface IntentResponseItem {
  name: string;
}

// 样式常量
const styles = {
  inputWidth: 'w-[79%]',
  selectWidth: '!w-[80px] mr-2',
  buttonMargin: 'ml-[10px]',
  listItemSpacing: 'mb-[10px]'
};

const RasaModal = forwardRef<ModalRef, RasaModalProps>(({ selectKey, folder_id, onSuccess }, ref) => {
  const { t } = useTranslation();
  const {
    getRasaIntentFileList,
    getRasaResponseFileList,
    addRasaIntentFile,
    updateRasaIntentFile,
    addRasaResponseFile,
    updateRasaResponseFile,
    addRasaRuleFile,
    updateRasaRuleFile,
    addRasaStoryFile,
    updateRasaStoryFile,
    addRasaEntityFile,
    updateRasaEntityFile
  } = useMlopsManageApi();
  const formRef = useRef<FormInstance>(null);
  const [sampleList, setSampleList] = useState<(string | SampleItem | null)[]>([]);
  const [visiable, setVisiable] = useState<boolean>(false);
  const [confirmLoading, setConfirmLoading] = useState<boolean>(false);
  const [type, setType] = useState<string>('add');
  const [entityType, setEntityType] = useState<string>('Text');
  const [title, setTitle] = useState<string>('addintent');
  const [formData, setFormData] = useState<FormData | null>(null);
  const [options, setOptions] = useState<Record<string, Option[]>>({
    intent: [],
    response: []
  });

  const renderActionButtons = (index: number) => (
    <>
      <Button
        icon={<PlusOutlined />}
        className={styles.buttonMargin}
        onClick={addSampleList}
      />
      {!!index && (
        <Button
          icon={<MinusOutlined />}
          className={styles.buttonMargin}
          onClick={() => deleteSampleList(index)}
        />
      )}
    </>
  );

  const renderSelectRow = (item: any, index: number) => (
    <>
      <Select
        className={styles.selectWidth}
        defaultValue={item?.type || 'intent'}
        onChange={(value) => onTypeChange(value, index)}
        options={[
          { label: '意图', value: 'intent' },
          { label: '响应', value: 'response' }
        ]}
      />
      <Select
        className={styles.inputWidth}
        value={item?.select}
        options={options[item?.type as string]}
        onChange={(value: any) => {
          onSelectSampleChange(value, index);
        }}
      />
      {renderActionButtons(index)}
    </>
  );

  const typeElementMap: Record<string, (item: any, index: number) => React.JSX.Element> = {
    'intent': (item: any, index: number) => (
      <>
        <Input
          className={styles.inputWidth}
          value={item as string}
          onChange={(e) => {
            onSampleListChange(e, index);
          }}
        />
        {renderActionButtons(index)}
      </>
    ),
    'response': (item: any, index: number) => (
      <>
        <Select key="text" className={styles.selectWidth} defaultValue="text" options={[
          {
            label: '文本',
            value: 'text'
          }
        ]} />
        <Input
          className={styles.inputWidth}
          placeholder={t(`common.inputMsg`)}
          value={item as string}
          onChange={(e) => {
            onSampleListChange(e, index);
          }}
        />
        {renderActionButtons(index)}
      </>
    ),
    'rule': (item: any, index: number) => renderSelectRow(item, index),
    'story': (item: any, index: number) => renderSelectRow(item, index),
    'entity': (item: any, index: number) => (
      <>
        <Input
          className={styles.inputWidth}
          placeholder={t(`common.inputMsg`)}
          value={item as string}
          onChange={(e) => {
            onSampleListChange(e, index);
          }}
        />
        {renderActionButtons(index)}
      </>
    )
  }

  useImperativeHandle(ref, () => ({
    showModal: ({ type, title, form }) => {
      setTitle(title);
      setType(type);
      setFormData(form);
      setVisiable(true);
    }
  }));

  const handleAddMap: Record<string, any> = {
    'intent': addRasaIntentFile,
    'response': addRasaResponseFile,
    'rule': addRasaRuleFile,
    'story': addRasaStoryFile,
    'entity': addRasaEntityFile,
  };

  const handleUpdateMap: Record<string, any> = {
    'intent': updateRasaIntentFile,
    'response': updateRasaResponseFile,
    'rule': updateRasaRuleFile,
    'story': updateRasaStoryFile,
    'entity': updateRasaEntityFile
  };

  useEffect(() => {
    if (!['rule', 'story'].includes(selectKey)) {
      return;
    }

    const fetchOptions = async () => {
      try {
        const [intentList, responseList] = await Promise.all([
          getRasaIntentFileList({ dataset: folder_id }),
          getRasaResponseFileList({ dataset: folder_id })
        ]);
        const intentOption = (intentList as IntentResponseItem[])?.map((item) => ({
          label: item.name,
          value: item.name
        })) || [];
        const responseOption = (responseList as IntentResponseItem[])?.map((item) => ({
          label: item.name,
          value: item.name
        })) || [];
        setOptions({
          intent: intentOption,
          response: responseOption
        });
      } catch (e) {
        console.log(e);
        message.error(t(`common.fetchFailed`));
      }
    };

    fetchOptions();
  }, [selectKey]);

  useEffect(() => {
    if (visiable && formRef.current) {
      const isRule = ['rule', 'story'].includes(selectKey);

      formRef.current?.resetFields();
      formRef.current?.setFieldValue('name', formData?.name);

      if (isRule) {
        const list = formData?.steps?.map((item: any) => {
          return {
            type: (item?.intent ? 'intent' : 'response') as 'intent' | 'response',
            select: item?.intent || item?.response
          }
        });

        setSampleList(list || [{ type: 'intent' as const, select: '' }]);
      } else {
        setSampleList(formData?.example || [null]);
        if(formData?.entity_type) {
          formRef.current?.setFieldValue('entity_type', formData?.entity_type);
          setEntityType(formData?.entity_type);
        }
      }
    }
  }, [formData, visiable, selectKey]);

  const handleSubmit = async () => {
    setConfirmLoading(true)
    try {
      let params = {};
      const data = await formRef.current?.validateFields();
      if (type === 'add') {
        if (['rule', 'story'].includes(selectKey)) {
          params = {
            ...data,
            dataset: formData?.dataset,
            steps: sampleList.map((item: any) => ({
              [item?.type]: item.select
            }))
          };
        } else {
          params = {
            ...data,
            dataset: formData?.dataset,
            example: entityType === 'Text' ? [] : sampleList
          };
        }
        console.log(params);
        await handleAddMap[selectKey](params);
        message.success(t(`common.addSuccess`));
        onSuccess();
      } else {
        if (['rule', 'story'].includes(selectKey)) {
          params = {
            ...data,
            steps: sampleList.map((item: any) => ({
              [item?.type]: item.select
            }))
          }
        } else {
          params = {
            ...data,
            example: (selectKey !== 'entity' || entityType === 'Lookup') ? sampleList : []
          }
        }
        await handleUpdateMap[selectKey](formData?.id, params);
        message.success(t(`common.updateSuccess`));
      }
      onSuccess();
      setVisiable(false);
    } catch (e) {
      console.log(e);
      message.error(t(`common.error`))
    } finally {
      setConfirmLoading(false);
    }
  };

  const handleCancel = () => {
    setVisiable(false);
    setEntityType('');
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    const allowedKeys = [
      'Backspace', 'Delete', 'Tab', 'Escape', 'Enter',
      'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown',
      'Home', 'End', 'PageUp', 'PageDown'
    ];

    if (allowedKeys.includes(e.key) || e.ctrlKey || e.metaKey) {
      return;
    }

    const regex = /^[a-zA-Z\s]$/;
    if (!regex.test(e.key)) {
      e.preventDefault();
    }
  };

  const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    const filteredValue = value.replace(/[^a-zA-Z\s]/g, '');

    if (filteredValue !== value) {
      formRef.current?.setFieldsValue({
        name: filteredValue
      });
    }
  };

  const onTypeChange = (value: string, index: number) => {
    const keys = cloneDeep(sampleList);
    keys[index] = {
      type: value as 'intent' | 'response',
      select: ''
    };
    setSampleList(keys);
  };

  const onSelectSampleChange = (value: string, index: number) => {
    const keys = cloneDeep(sampleList);
    const item = keys[index];
    if (item && typeof item === 'object' && 'select' in item) {
      item.select = value;
    }
    setSampleList(keys);
  };

  const onSampleListChange = (
    e: React.ChangeEvent<HTMLInputElement>,
    index: number
  ) => {
    const keys = cloneDeep(sampleList);
    keys[index] = e.target.value;
    setSampleList(keys);
  };

  const onEntityTypeChange = (value: string) => {
    setEntityType(value);
    if (value === 'Lookup') {
      const data = formData?.example?.length ? formData.example : [null];
      setSampleList(data);
    }
  };

  const addSampleList = () => {
    const keys = cloneDeep(sampleList);
    const data = ['rule', 'story'].includes(selectKey) ?
      { type: 'intent' as const, select: '' } :
      null;
    keys.push(data);
    setSampleList(keys);
  };

  const deleteSampleList = (index: number) => {
    const keys = cloneDeep(sampleList);
    keys.splice(index, 1);
    setSampleList(keys);
  };

  const validateSampleList = async () => {
    if (sampleList.some((item) => !item)) {
      return Promise.reject(new Error(t('common.valueValidate')));
    }
    return Promise.resolve();
  };

  return (
    <OperateModal
      title={t(`datasets.${title}`)}
      open={visiable}
      onCancel={() => handleCancel()}
      footer={[
        <Button key='confirm' type='primary' loading={confirmLoading} onClick={handleSubmit}>{t(`common.confirm`)}</Button>,
        <Button key='cancel' type='default' onClick={handleCancel}>{t(`common.cancel`)}</Button>,
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
          <Input placeholder={"仅允许输入英文"} onKeyDown={handleKeyDown} onChange={handleNameChange} />
        </Form.Item>
        {selectKey === 'entity' && (
          <Form.Item
            name='entity_type'
            label={t(`common.type`)}
            rules={[
              { required: true, message: t('common.selectMsg') },
            ]}
          >
            <Select placeholder={t(`common.selectMsg`)} options={
              [
                { label: 'Text(需要在语料中特殊标志)', value: 'Text' },
                { label: 'Lookup(单独定义值列表，适合枚举类型内容)', value: 'Lookup' }
              ]
            } onChange={onEntityTypeChange} />
          </Form.Item>
        )}
        {(selectKey !== 'entity' || entityType !== 'Text') && (
          <Form.Item
            label={selectKey === 'rule' ? '步骤' : '样例'}
            // name="samples"
            rules={[{ required: true, validator: validateSampleList }]}
          >
            <ul>
              {sampleList.map((item, index) => (
                <li
                  className={`flex ${index + 1 !== sampleList?.length && styles.listItemSpacing}`}
                  key={index}
                >
                  {typeElementMap[selectKey](item, index)}
                </li>
              ))}
            </ul>
          </Form.Item>
        )}
      </Form>
    </OperateModal>
  )
});

RasaModal.displayName = 'RasaModel';
export default RasaModal;
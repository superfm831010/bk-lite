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

interface RasaModalProps {
  selectKey: string;
  onSuccess: () => void;
}

const RasaModal = forwardRef<ModalRef, RasaModalProps>(({ selectKey, onSuccess }, ref) => {
  const { t } = useTranslation();
  const {
    getRasaIntentFileList,
    getRasaResponseFileList,
    addRasaIntentFile,
    updateRasaIntentFile,
    addRasaResponseFile,
    updateRasaResponseFile,
    addRasaRuleFile,
    updateRasaRuleFile
  } = useMlopsManageApi();
  const formRef = useRef<FormInstance>(null);
  const [sampleList, setSampleList] = useState<any[]>([]);
  const [visiable, setVisiable] = useState<boolean>(false);
  const [confirmLoading, setConfirmLoading] = useState<boolean>(false);
  const [type, setType] = useState<string>('add');
  const [title, setTitle] = useState<string>('addintent');
  const [formData, setFormData] = useState<any>(null);
  const [options, setOptions] = useState<Record<string, Option[]>>({
    intent: [],
    response: []
  });

  const typeElementMap: Record<string, (item: any, index: number) => React.JSX.Element> = {
    'intent': (item: any, index: number) => (
      <>
        <Input
          className="w-[79%]"
          value={item as string}
          onChange={(e) => {
            onSampleListChange(e, index);
          }}
        />
        <Button
          icon={<PlusOutlined />}
          className="ml-[10px]"
          onClick={addSampleList}
        ></Button>
        {!!index && (
          <Button
            icon={<MinusOutlined />}
            className="ml-[10px]"
            onClick={() => deleteSampleList(index)}
          ></Button>
        )}
      </>
    ),
    'response': (item: any, index: number) => (
      <>
        <Select key="text" className='!w-[80px] mr-2' defaultValue="text" options={[
          {
            label: '文本',
            value: 'text'
          }
        ]} />
        <Input
          className="w-[79%]"
          value={item as string}
          onChange={(e) => {
            onSampleListChange(e, index);
          }}
        />
        <Button
          icon={<PlusOutlined />}
          className="ml-[10px]"
          onClick={addSampleList}
        ></Button>
        {!!index && (
          <Button
            icon={<MinusOutlined />}
            className="ml-[10px]"
            onClick={() => deleteSampleList(index)}
          ></Button>
        )}
      </>
    ),
    'rule': (item: any, index: number) => (<>
      <Select key="rule" className='!w-[80px] mr-2' defaultValue={item.type} onChange={(value) => onTypeChange(value, index)} options={[
        {
          label: '意图',
          value: 'intent'
        },
        {
          label: '响应',
          value: 'response'
        }
      ]} />
      <Select
        className="w-[79%]"
        value={item?.select}
        options={options[item.type as string]}
        onChange={(value: any) => {
          onSelectSampleChange(value, index);
        }}
      />
      <Button
        icon={<PlusOutlined />}
        className="ml-[10px]"
        onClick={addSampleList}
      ></Button>
      {!!index && (
        <Button
          icon={<MinusOutlined />}
          className="ml-[10px]"
          onClick={() => deleteSampleList(index)}
        ></Button>
      )}
    </>),
    'story': (item: any, index: number) => (<>
      <Select key="story" className='!w-[80px] mr-2' defaultValue="intent" onChange={(value) => onTypeChange(value, index)} options={[
        {
          label: '意图',
          value: 'intent'
        },
        {
          label: '响应',
          value: 'response'
        }
      ]} />
      <Select
        className="w-[79%]"
        value={item?.select}
        onChange={(value: any) => {
          onSelectSampleChange(value, index);
        }}
      />
      <Button
        icon={<PlusOutlined />}
        className="ml-[10px]"
        onClick={addSampleList}
      ></Button>
      {!!index && (
        <Button
          icon={<MinusOutlined />}
          className="ml-[10px]"
          onClick={() => deleteSampleList(index)}
        ></Button>
      )}
    </>)
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
    'story': () => { }
  };

  const handleUpdateMap: Record<string, any> = {
    'intent': updateRasaIntentFile,
    'response': updateRasaResponseFile,
    'rule': updateRasaRuleFile,
    'story': () => { }
  };

  useEffect(() => {
    if (['rule', 'story'].includes(selectKey)) {
      getAllOptions();
    }
  }, [selectKey]);

  useEffect(() => {
    if (visiable && formRef.current) {
      const isRule = ['rule', 'story'].includes(selectKey);
      
      formRef.current?.resetFields();
      formRef.current?.setFieldValue('name', formData?.name);

      if(isRule) {
        const list = formData?.steps?.map((item: any) => {
          return {
            type: item?.intent ? 'intent' : 'response',
            select: item?.intent || item?.response
          }
        });

        setSampleList(list || [{ type: 'intent', select: '' }]);
      } else {
        setSampleList(formData?.example || [null])
      }
    }
  }, [formData, visiable]);

  const getAllOptions = async () => {
    try {
      const [intentList, responseList] = await Promise.all([getRasaIntentFileList({}), getRasaResponseFileList({})]);
      const intentOption = intentList?.map((item: any) => ({
        label: item.name,
        value: item.name
      }));
      const responseOption = responseList?.map((item: any) => ({
        label: item.name,
        value: item.name
      }));
      setOptions({
        intent: intentOption,
        response: responseOption
      });
    } catch (e) {
      console.log(e);
      message.error(t(`common.fetchFailed`));
    }
  };

  const handleSubmit = async () => {
    console.log(type);
    setConfirmLoading(true)
    try {
      let params = {};
      const { name } = await formRef.current?.validateFields();
      if (type === 'add') {
        if (['rule', 'story'].includes(selectKey)) {
          params = {
            name,
            dataset: formData?.dataset,
            steps: sampleList.map((item: any) => ({
              [item?.type]: item.select
            }))
          };
        } else {
          params = {
            name,
            dataset: formData?.dataset,
            example: sampleList
          };
        }
        handleAddMap[selectKey](params);
        message.success(t(`common.addSuccess`));
      } else {
        if (['rule', 'story'].includes(selectKey)) {
          params = {
            name,
            steps: sampleList.map((item: any) => ({
              [item?.type]: item.select
            }))
          }
        } else {
          params = {
            name,
            example: sampleList
          }
        }
        handleUpdateMap[selectKey](formData?.id, params);
        message.success(t(`common.updateSuccess`));
      }
      
      onSuccess();
      setVisiable(false);
    } catch (e) {
      console.log(e);
    } finally {
      setConfirmLoading(false);
    }
  };

  const handleCancel = () => {
    setVisiable(false);
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

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
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
      type: value,
      select: '',
      options: options[value]
    };
    setSampleList(keys);
  };

  const onSelectSampleChange = (value: string, index: number) => {
    const keys = cloneDeep(sampleList);
    keys[index].select = value;
    console.log(keys[index])
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

  const addSampleList = () => {
    const keys = cloneDeep(sampleList);
    const data = ['rule', 'story'].includes(selectKey) ? { type: 'intent', select: '' } : null;
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
          <Input placeholder={"仅允许输入英文"} onKeyDown={handleKeyDown} onChange={handleChange} />
        </Form.Item>
        <Form.Item
          label={selectKey === 'rule' ? '步骤' : '样例'}
          name="samples"
          rules={[{ required: true, validator: validateSampleList }]}
        >
          <ul>
            {sampleList.map((item, index) => (
              <li
                className={`flex ${index + 1 !== sampleList?.length && 'mb-[10px]'}`}
                key={index}
              >
                {typeElementMap[selectKey](item, index)}
              </li>
            ))}
          </ul>
        </Form.Item>
      </Form>
    </OperateModal>
  )
});

RasaModal.displayName = 'RasaModel';
export default RasaModal;
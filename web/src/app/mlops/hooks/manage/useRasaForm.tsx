import { useState, useMemo, useEffect, useRef, useCallback } from "react";
import { Input, Button, Select, message, FormInstance } from "antd";
import { PlusOutlined, MinusOutlined } from "@ant-design/icons";
import { cloneDeep } from 'lodash';
import { Option } from "@/types";
import { useTranslation } from "@/utils/i18n";
import useMlopsManageApi from "@/app/mlops/api/manage";
import EntitySelectModal from "./entitySelectModal";
import { ModalRef } from "../../types";

interface SampleItem {
  type: 'intent' | 'response';
  select: string;
}

interface IntentResponseItem {
  name: string;
}

const styles = {
  inputWidth: 'w-[79%]',
  selectWidth: '!w-[80px] mr-2',
  buttonMargin: 'ml-[10px]',
  listItemSpacing: 'mb-[10px]'
};

const useRasaIntentForm = (
  {
    // folder_id,
    formData,
    visiable,
    onTextSelection
  }: {
    folder_id: number;
    selectKey: string;
    formData?: any;
    visiable?: boolean;
    onTextSelection?: (data: any) => void;
  }
) => {
  // const modalRef = useRef<ModalRef>(null);
  const [sampleList, setSampleList] = useState<(string | null)[]>([]);
  const selectedTextRef = useRef<any>(null);

  // 当模态框显示且有formData时，初始化sampleList
  useEffect(() => {
    if (visiable && formData) {
      setSampleList(formData?.example_count ? formData?.example : [null]);
    } else if (visiable) {
      setSampleList([null]);
    }
  }, [formData, visiable]);

  // 添加选择检测函数
  const handleTextSelection = useCallback((index: number, event: React.SyntheticEvent) => {
    const input = event.target as HTMLInputElement;

    const start = input.selectionStart;
    const end = input.selectionEnd;

    if (start !== null && end !== null && start !== end) {
      const text = input.value.substring(start, end);
      if (text.trim()) {
        const textInfo = {
          text: text.trim(),
          start,
          end,
          inputIndex: index
        };
        selectedTextRef.current = textInfo;
        onTextSelection?.(textInfo)
        // modalRef.current?.showModal({ type: '' });
      }
    }
  }, [onTextSelection]);

  const addSampleList = () => {
    const keys = cloneDeep(sampleList);
    keys.push(null);
    setSampleList(keys);
  };

  const deleteSampleList = (index: number) => {
    const keys = cloneDeep(sampleList);
    keys.splice(index, 1);
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

  const handleEntitySelect = useCallback((entityName: string) => {
    const currentSelectedText = selectedTextRef.current;
    if (currentSelectedText) {
      const { text, start, end, inputIndex } = currentSelectedText;
      const currentValue = sampleList[inputIndex] as string;

      const newValue =
        currentValue.substring(0, start) +
        `[${text}](${entityName})` +
        currentValue.substring(end);
      const keys = cloneDeep(sampleList);
      keys[inputIndex] = newValue;
      setSampleList(keys);
      selectedTextRef.current = null;
    }
  }, [sampleList]);

  const renderElement = useMemo(() => (
    <>
      <ul>
        {sampleList.map((item, index) => (
          <li
            className={`flex ${index + 1 !== sampleList?.length && styles.listItemSpacing}`}
            key={index}
          >
            <Input
              className={styles.inputWidth}
              value={item as string}
              onChange={(e) => {
                onSampleListChange(e, index);
              }}
              onSelect={(e) => handleTextSelection(index, e)}
            />
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
          </li>
        ))}
      </ul>
      {/* <EntitySelectModal ref={modalRef} dataset={folder_id} onSuccess={handleEntitySelect} /> */}
    </>
  ), [sampleList, handleTextSelection]);

  return {
    sampleList,
    renderElement,
    handleEntitySelect
  }
};

const useRasaResponseForm = ({
  formData,
  visiable
}: {
  selectKey: string;
  formData?: any;
  visiable?: boolean;
}) => {
  const [sampleList, setSampleList] = useState<(string | null)[]>([]);

  // 当模态框显示且有formData时，初始化sampleList
  useEffect(() => {
    if (visiable && formData) {
      setSampleList(formData?.example_count ? formData?.example : [null]);
    } else if (visiable) {
      setSampleList([null]);
    }
  }, [formData, visiable]);

  const addSampleList = () => {
    const keys = cloneDeep(sampleList);
    keys.push(null);
    setSampleList(keys);
  };

  const deleteSampleList = (index: number) => {
    const keys = cloneDeep(sampleList);
    keys.splice(index, 1);
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

  const renderElement = useMemo(() => (
    <ul>
      {sampleList.map((item, index) => (
        <li
          className={`flex ${index + 1 !== sampleList?.length && styles.listItemSpacing}`}
          key={index}
        >
          <Select key="text" className={styles.selectWidth} defaultValue="text" options={[
            {
              label: '文本',
              value: 'text'
            }
          ]} />
          <Input
            className={styles.inputWidth}
            value={item as string}
            onChange={(e) => {
              onSampleListChange(e, index);
            }}
          />
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
        </li>
      ))}
    </ul>
  ), [sampleList]);

  return {
    sampleList,
    renderElement,
  }
};

const useRasaRuleForm = ({
  folder_id,
  selectKey,
  formData,
  visiable
}: {
  folder_id: number;
  selectKey: string;
  formData?: any;
  visiable?: boolean;
}) => {
  const { t } = useTranslation();
  const { getRasaIntentFileList, getRasaResponseFileList } = useMlopsManageApi();
  const [sampleList, setSampleList] = useState<(SampleItem | null)[]>([]);
  const [options, setOptions] = useState<Record<string, Option[]>>({
    intent: [],
    response: []
  });

  // 当模态框显示且有formData时，初始化sampleList
  useEffect(() => {
    if (visiable && formData?.steps) {
      const list = formData.steps.map((item: any) => {
        return {
          type: (item?.intent ? 'intent' : 'response') as 'intent' | 'response',
          select: item?.intent || item?.response
        }
      });
      setSampleList(list);
    } else if (visiable) {
      setSampleList([{ type: 'intent' as const, select: '' }]);
    }
  }, [formData, visiable]);

  useEffect(() => {
    // 只有当前selectKey是rule时才发送请求
    if (selectKey !== 'rule') return;

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
  }, [selectKey])

  const addSampleList = () => {
    const keys = cloneDeep(sampleList);
    keys.push({ type: 'intent' as const, select: '' });
    setSampleList(keys);
  };

  const deleteSampleList = (index: number) => {
    const keys = cloneDeep(sampleList);
    keys.splice(index, 1);
    setSampleList(keys);
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

  const renderElement = useMemo(() => (
    <ul>
      {sampleList.map((item, index) => (
        <li
          className={`flex ${index + 1 !== sampleList?.length && styles.listItemSpacing}`}
          key={index}
        >
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
        </li>
      ))}
    </ul>
  ), [sampleList]);

  return {
    sampleList,
    renderElement
  }
};

const useRasaStoryForm = ({
  folder_id,
  selectKey,
  formData,
  visiable
}: {
  folder_id: number;
  selectKey: string;
  formData?: any;
  visiable?: boolean;
}) => {
  const { t } = useTranslation();
  const { getRasaIntentFileList, getRasaResponseFileList } = useMlopsManageApi();
  const [sampleList, setSampleList] = useState<(SampleItem | null)[]>([]);
  const [options, setOptions] = useState<Record<string, Option[]>>({
    intent: [],
    response: []
  });

  // 当模态框显示且有formData时，初始化sampleList
  useEffect(() => {
    if (visiable && formData?.steps) {
      const list = formData.steps.map((item: any) => {
        return {
          type: (item?.intent ? 'intent' : 'response') as 'intent' | 'response',
          select: item?.intent || item?.response
        }
      });
      setSampleList(list);
    } else if (visiable) {
      setSampleList([{ type: 'intent' as const, select: '' }]);
    }
  }, [formData, visiable]);

  useEffect(() => {
    // 只有当前selectKey是story时才发送请求
    if (selectKey !== 'story') return;

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
  }, [selectKey])

  const addSampleList = () => {
    const keys = cloneDeep(sampleList);
    keys.push({ type: 'intent' as const, select: '' });
    setSampleList(keys);
  };

  const deleteSampleList = (index: number) => {
    const keys = cloneDeep(sampleList);
    keys.splice(index, 1);
    setSampleList(keys);
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

  const renderElement = useMemo(() => (
    <ul>
      {sampleList.map((item, index) => (
        <li
          className={`flex ${index + 1 !== sampleList?.length && styles.listItemSpacing}`}
          key={index}
        >
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
        </li>
      ))}
    </ul>
  ), [sampleList]);

  return {
    sampleList,
    renderElement
  }
};

const useRasaEntityForm = ({
  // selectKey,
  formData,
  visiable,
  entityType,
}: {
  selectKey: string;
  formData?: any;
  visiable?: boolean;
  entityType?: string;
}) => {
  const [sampleList, setSampleList] = useState<(string | null)[]>([]);
  // 当模态框显示且有formData时，初始化sampleList
  useEffect(() => {
    if (visiable && formData) {
      setSampleList(formData?.example || [null]);
    } else if (visiable) {
      setSampleList([null]);
    }
  }, [formData, visiable]);

  useEffect(() => {
    if (entityType === 'Lookup') {
      const data = formData?.example?.length ? formData.example : [null];
      console.log(data);
      setSampleList(data);
    }
  }, [entityType])

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
    keys.push(null);
    setSampleList(keys);
  };

  const deleteSampleList = (index: number) => {
    const keys = cloneDeep(sampleList);
    keys.splice(index, 1);
    setSampleList(keys);
  };

  const renderElement = useMemo(() => (
    <ul>
      {sampleList.map((item, index) => (
        <li
          className={`flex ${index + 1 !== sampleList?.length && styles.listItemSpacing}`}
          key={index}
        >
          <Input
            className={styles.inputWidth}
            value={item as string}
            onChange={(e) => {
              onSampleListChange(e, index);
            }}
          />
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
        </li>
      ))}
    </ul>
  ), [sampleList]);

  return {
    sampleList,
    renderElement
  }
};

const useRasaSlotForm = ({
  formData,
  visiable,
}: {
  selectKey: string;
  formData?: any;
  visiable?: boolean;
  slotType?: string;
}) => {
  const [sampleList, setSampleList] = useState<(string | null)[]>([]);

  // 当模态框显示且有formData时，初始化sampleList
  useEffect(() => {
    if (visiable && formData) {
      setSampleList(formData?.example || [null]);
    } else if (visiable) {
      setSampleList([null]);
    }
  }, [formData, visiable]);

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
    keys.push(null);
    setSampleList(keys);
  };

  const deleteSampleList = (index: number) => {
    const keys = cloneDeep(sampleList);
    keys.splice(index, 1);
    setSampleList(keys);
  };

  const renderElement = useMemo(() => (
    <>
      <ul>
        {sampleList.map((item, index) => (
          <li
            className={`flex ${index + 1 !== sampleList?.length && styles.listItemSpacing}`}
            key={index}
          >
            <Input
              className={styles.inputWidth}
              value={item as string}
              onChange={(e) => {
                onSampleListChange(e, index);
              }}
            />
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
          </li>
        ))}
      </ul>
    </>
  ), [sampleList])

  return {
    sampleList,
    renderElement
  }
};

// 输入验证hooks
const useInputValidation = () => {
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

  const handleNameChange = (formRef: React.RefObject<FormInstance>, e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    const filteredValue = value.replace(/[^a-zA-Z\s]/g, '');

    if (filteredValue !== value) {
      formRef.current?.setFieldsValue({
        name: filteredValue
      });
    }
  };

  return { handleKeyDown, handleNameChange };
};

// API映射hooks
const useRasaApiMethods = () => {
  const {
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

  const handleAddMap: Record<string, any> = {
    'intent': addRasaIntentFile,
    'response': addRasaResponseFile,
    'rule': addRasaRuleFile,
    'story': addRasaStoryFile,
    'entity': addRasaEntityFile,
    'slot': () => { }
  };

  const handleUpdateMap: Record<string, any> = {
    'intent': updateRasaIntentFile,
    'response': updateRasaResponseFile,
    'rule': updateRasaRuleFile,
    'story': updateRasaStoryFile,
    'entity': updateRasaEntityFile,
    'slot': () => { }
  };

  return { handleAddMap, handleUpdateMap };
};

// 表单数据处理hooks
const useRasaFormData = () => {
  const { t } = useTranslation();

  const validateSampleList = async (sampleList: any[]) => {
    if (sampleList.some((item) => !item)) {
      return Promise.reject(new Error(t('common.valueValidate')));
    }
    return Promise.resolve();
  };

  const prepareFormParams = (
    type: string,
    selectKey: string,
    data: any,
    sampleList: any[],
    formData: any,
    entityType?: string
  ) => {
    let params = {};

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
    } else {
      if (['rule', 'story'].includes(selectKey)) {
        params = {
          ...data,
          steps: sampleList.map((item: any) => ({
            [item?.type]: item.select
          }))
        };
      } else {
        params = {
          ...data,
          example: (selectKey !== 'entity' || entityType === 'Lookup') ? sampleList : []
        };
      }
    }

    return params;
  };

  return { validateSampleList, prepareFormParams };
};

// 完整的Rasa表单管理hooks
const useRasaFormManager = ({
  selectKey,
  folder_id,
  formRef,
  onSuccess
}: {
  selectKey: string;
  folder_id: string;
  formRef: React.RefObject<FormInstance>;
  onSuccess: () => void;
}) => {
  const { t } = useTranslation();
  const modalRef = useRef<ModalRef>(null);
  const [visiable, setVisiable] = useState<boolean>(false);
  const [confirmLoading, setConfirmLoading] = useState<boolean>(false);
  const [type, setType] = useState<string>('add');
  const [entityType, setEntityType] = useState<string>('Text');
  const [slotType, setSlotType] = useState<string>('text');
  const [slotPrediction, setSlotPrediction] = useState<boolean>(false);
  const [title, setTitle] = useState<string>('addintent');
  const [formData, setFormData] = useState<any>(null);

  // 新增：管理实体选择相关状态
  const [selectedTextForEntity, setSelectedTextForEntity] = useState<any>(null);

  const { handleAddMap, handleUpdateMap } = useRasaApiMethods();
  const { validateSampleList, prepareFormParams } = useRasaFormData();
  const { handleKeyDown, handleNameChange } = useInputValidation();

  // 文字选择回调函数
  const handleTextSelection = useCallback((textData: any) => {
    setSelectedTextForEntity(textData);
    modalRef.current?.showModal({ type: '' });
  }, []);

  // 始终调用所有的 hooks，但只使用需要的
  const intentForm = useRasaIntentForm({
    folder_id: Number(folder_id),
    selectKey,
    formData,
    visiable,
    onTextSelection: selectKey === 'intent' ? handleTextSelection : undefined
  });
  const responseForm = useRasaResponseForm({ selectKey, formData, visiable });
  const ruleForm = useRasaRuleForm({ folder_id: Number(folder_id), selectKey, formData, visiable });
  const storyForm = useRasaStoryForm({ folder_id: Number(folder_id), selectKey, formData, visiable });
  const entityForm = useRasaEntityForm({ selectKey, formData, visiable, entityType });
  const slotForm = useRasaSlotForm({ selectKey, formData, visiable });

  // 处理从Modal传来的实体选择
  const handleEntitySelectFromModal = useCallback((entityName: string) => {
    if (selectKey === 'intent' && intentForm.handleEntitySelect) {
      intentForm.handleEntitySelect(entityName);
    }
    // 清除选择状态
    setSelectedTextForEntity(null);
  }, [selectKey, intentForm]);

  const getCurrentForm = () => {
    switch (selectKey) {
      case 'intent':
        return intentForm;
      case 'response':
        return responseForm;
      case 'rule':
        return ruleForm;
      case 'story':
        return storyForm;
      case 'entity':
        return entityForm;
      case 'slot':
        return slotForm;
      default:
        return intentForm;
    }
  };

  const currentForm = getCurrentForm();

  const showModal = ({ type, title, form }: { type: string; title: string; form: any }) => {
    setTitle(title);
    setType(type);
    setFormData(form);
    setVisiable(true);
  };

  const handleSubmit = async () => {
    setConfirmLoading(true);
    try {
      const data = await formRef.current?.validateFields();
      const params = prepareFormParams(type, selectKey, data, currentForm.sampleList, formData, entityType);
      console.log(params);
      if (type === 'add') {
        await handleAddMap[selectKey](params);
        message.success(t(`common.addSuccess`));
      } else {
        await handleUpdateMap[selectKey](formData?.id, params);
        message.success(t(`common.updateSuccess`));
      }

      onSuccess();
      setVisiable(false);
    } catch (e) {
      console.log(e);
      message.error(t(`common.error`));
    } finally {
      setConfirmLoading(false);
    }
  };

  const handleCancel = () => {
    setVisiable(false);
    setEntityType('Text');
  };

  const onEntityTypeChange = (value: string) => {
    setEntityType(value);
  };

  const onSlotTypeChange = (value: string) => {
    setSlotType(value);
  };

  const onSlotPredictionChange = (value: boolean) => {
    setSlotPrediction(value)
  };

  // 创建Modal元素，只在需要时渲染
  const modalElement = useMemo(() => {
    // 只有当selectKey是intent时才渲染EntitySelectModal
    if (selectKey === 'intent') {
      return (
        <EntitySelectModal 
          ref={modalRef} 
          dataset={Number(folder_id)} 
          onSuccess={handleEntitySelectFromModal}
        />
      );
    }
    return null;
  }, [selectKey, folder_id, handleEntitySelectFromModal, selectedTextForEntity]);

  return {
    visiable,
    confirmLoading,
    type,
    entityType,
    slotType,
    slotPrediction,
    title,
    formData,
    showModal,
    handleSubmit,
    handleCancel,
    onEntityTypeChange,
    onSlotTypeChange,
    onSlotPredictionChange,
    handleKeyDown,
    handleNameChange: (e: React.ChangeEvent<HTMLInputElement>) => handleNameChange(formRef, e),
    validateSampleList: () => validateSampleList(currentForm.sampleList),
    renderElement: currentForm.renderElement,
    sampleList: currentForm.sampleList,
    modalElement
  };
};

export {
  useRasaIntentForm,
  useRasaResponseForm,
  useRasaRuleForm,
  useRasaStoryForm,
  useRasaEntityForm,
  useInputValidation,
  useRasaApiMethods,
  useRasaFormData,
  useRasaFormManager
}

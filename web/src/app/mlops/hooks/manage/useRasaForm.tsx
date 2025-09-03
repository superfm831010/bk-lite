import { useState, useMemo, useEffect, useRef, useCallback } from "react";
import { Input, Button, Select, message, FormInstance, Checkbox } from "antd";
import { PlusOutlined, MinusOutlined } from "@ant-design/icons";
import { cloneDeep } from 'lodash';
import { Option } from "@/types";
import { useTranslation } from "@/utils/i18n";
import useMlopsManageApi from "@/app/mlops/api/manage";
import EntitySelectModal from "./entitySelectModal";
import { ModalRef } from "@/app/mlops/types";

interface SampleItem {
  type: 'intent' | 'response' | 'form';
  select: string;
}

interface IntentResponseItem {
  name: string;
}

interface FormManageItem {
  type: string;
  name: string;
  isRequired: boolean;
}

interface SlotOption {
  label: string,
  value: any,
  slot_type: string
}

const styles = {
  inputWidth: '!w-[79%]',
  selectWidth: '!w-[80px] mr-2',
  selectMiddle: '!w-[60%]',
  buttonMargin: 'ml-[10px]',
  listItemSpacing: 'mb-[10px]'
};

const useRasaIntentForm = (
  {
    formData,
    visiable,
    onTextSelection,
    selectKey
  }: {
    folder_id: number;
    selectKey: string;
    formData?: any;
    visiable?: boolean;
    onTextSelection?: (data: any) => void;
  }
) => {
  const { t } = useTranslation();
  const [sampleList, setSampleList] = useState<(string | null)[]>([]);
  const [editingIndex, setEditingIndex] = useState<number | null>(null);
  const selectedTextRef = useRef<any>(null);
  const isInitializedRef = useRef<boolean>(false); // 添加初始化标记

  useEffect(() => {
    // 🔧 只在当前选择类型为 intent 时才执行
    if (selectKey !== 'intent') {
      return;
    }
    
    // 只在首次显示时或formData真正改变时初始化
    if (visiable && !isInitializedRef.current) {
      if (formData) {
        setSampleList(formData?.example_count ? formData?.example : [null]);
      } else {
        setSampleList([null]);
      }
      isInitializedRef.current = true;
    }
    
    // 当模态框关闭时重置初始化标记
    if (!visiable) {
      isInitializedRef.current = false;
    }
  }, [formData, visiable, selectKey]);

  // 添加选择检测函数
  const handleTextSelection = useCallback((index: number, event: React.SyntheticEvent) => {
    const input = event.target as HTMLInputElement;

    const start = input.selectionStart;
    const end = input.selectionEnd;

    if (start !== null && end !== null && start !== end) {
      const text = input.value.substring(start, end);

      if (text.trim()) {
        const textInfo = {
          text: text,
          start,
          end,
          inputIndex: index,
          fullInputValue: input.value
        };
        selectedTextRef.current = textInfo;
        onTextSelection?.(textInfo)
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
    setSampleList(prevList => {
      const keys = cloneDeep(prevList);
      keys[index] = e.target.value;
      return keys;
    });
  };

  const handleEntitySelect = useCallback((entityName: string) => {
    const currentSelectedText = selectedTextRef.current;
    if (currentSelectedText) {
      const { text, start, end, inputIndex, fullInputValue } = currentSelectedText;
      // 使用存储的输入框值，而不是sampleList中的值
      const currentValue = fullInputValue || '';

      // 使用trim后的文本作为实体内容，但保持原始的start和end位置
      const trimmedText = text.trim();
      const newValue =
        currentValue.substring(0, start) +
        `[${trimmedText}](${entityName})` +
        currentValue.substring(end);

      setSampleList(prevList => {
        const keys = cloneDeep(prevList);
        keys[inputIndex] = newValue;
        return keys;
      });
      selectedTextRef.current = null;
      // 添加实体后切换到显示模式
      setEditingIndex(null);
    }
  }, []); // 移除sampleList依赖，使用函数式更新

  const renderElement = useMemo(() => {
    // 解析实体文字函数
    const parseEntityText = (text: string) => {
      if (!text) return [];

      const entityRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
      const parts = [];
      let lastIndex = 0;
      let match;

      while ((match = entityRegex.exec(text)) !== null) {
        if (match.index > lastIndex) {
          parts.push({
            type: 'text',
            content: text.slice(lastIndex, match.index)
          });
        }

        parts.push({
          type: 'entity',
          content: match[1],
          entityName: match[2]
        });

        lastIndex = match.index + match[0].length;
      }

      if (lastIndex < text.length) {
        parts.push({
          type: 'text',
          content: text.slice(lastIndex)
        });
      }

      return parts;
    };

    return (
      <>
        <ul>
          {sampleList.map((item, index) => {
            const parts = parseEntityText(item as string);
            const hasEntities = parts.some((part: any) => part.type === 'entity');
            const isEditing = editingIndex === index;

            return (
              <li
                className={`flex ${index + 1 !== sampleList?.length && styles.listItemSpacing}`}
                key={index}
              >
                {!hasEntities || isEditing ? (
                  <Input
                    className={styles.inputWidth}
                    value={item as string || ''}
                    onChange={(e) => onSampleListChange(e, index)}
                    onSelect={(e) => handleTextSelection(index, e)}
                    onBlur={() => setEditingIndex(null)}
                    autoFocus={isEditing}
                    placeholder={t(`common.inputMsg`)}
                  />
                ) : (
                  <div
                    className={`${styles.inputWidth} border border-gray-300 rounded-md px-3 py-1 min-h-[32px] bg-white flex items-center cursor-text hover:border-blue-400`}
                    onClick={() => setEditingIndex(index)}
                  >
                    {parts.map((part: any, partIndex: number) => (
                      <span
                        key={partIndex}
                        className={
                          part.type === 'entity'
                            ? 'text-blue-600'
                            : 'text-gray-900'
                        }
                        title={part.type === 'entity' ? `实体: ${part.entityName}` : undefined}
                      >
                        {part.content}
                      </span>
                    ))}
                  </div>
                )}

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
            );
          })}
        </ul>
      </>
    );
  }, [sampleList, handleTextSelection, editingIndex, onSampleListChange]);

  return {
    sampleList,
    renderElement,
    handleEntitySelect
  }
};

const useRasaResponseForm = ({
  formData,
  visiable,
  selectKey
}: {
  selectKey: string;
  formData?: any;
  visiable?: boolean;
}) => {
  const { t } = useTranslation();
  const [sampleList, setSampleList] = useState<(string | null)[]>([]);

  // 当模态框显示且有formData时，初始化sampleList
  useEffect(() => {
    // 🔧 只在当前选择类型为 response 时才执行
    if (selectKey !== 'response') {
      return;
    }
    
    if (visiable && formData) {
      setSampleList(formData?.example_count ? formData?.example : [null]);
    } else if (visiable) {
      setSampleList([null]);
    }
  }, [formData, visiable, selectKey]);

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
              label: t(`mlops-common.text`),
              value: 'text'
            }
          ]} />
          <Input
            className={styles.selectMiddle}
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
  const { getRasaIntentFileList, getRasaResponseFileList, getRasaFormList } = useMlopsManageApi();
  const [sampleList, setSampleList] = useState<(SampleItem | null)[]>([]);
  const [options, setOptions] = useState<Record<string, Option[]>>({
    intent: [],
    response: [],
    form: []
  });

  useEffect(() => {
    // 🔧 只在当前选择类型为 rule 时才执行
    if (selectKey !== 'rule') {
      return;
    }
    
    if (visiable && formData?.steps) {
      const list = formData.steps.map((item: any) => {
        return {
          type: item?.type,
          select: item?.name
        }
      });
      setSampleList(list);
    } else if (visiable) {
      setSampleList([{ type: 'intent' as const, select: '' }]);
    }
  }, [formData, visiable, selectKey]);

  useEffect(() => {
    if (selectKey !== 'rule') return;

    const fetchOptions = async () => {
      try {
        const [intentList, responseList, formList] = await Promise.all([
          getRasaIntentFileList({ dataset: folder_id }),
          getRasaResponseFileList({ dataset: folder_id }),
          getRasaFormList({ dataset: folder_id })
        ]);
        const intentOption = (intentList as IntentResponseItem[])?.map((item) => ({
          label: item.name,
          value: item.name
        })) || [];
        const responseOption = (responseList as IntentResponseItem[])?.map((item) => ({
          label: item.name,
          value: item.name
        })) || [];
        const formOption = (formList as IntentResponseItem[])?.map((item) => ({
          label: item.name,
          value: item.name
        })) || [];
        setOptions({
          intent: intentOption,
          response: responseOption,
          form: formOption
        });
      } catch(e) {
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
      type: value as 'intent' | 'response' | 'form',
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
            value={item?.type || 'intent'}
            onChange={(value) => onTypeChange(value, index)}
            options={[
              { label: t(`datasets.intent`), value: 'intent' },
              { label: t(`datasets.response`), value: 'response' },
              { label: t(`datasets.form`), value: 'form' }
            ]}
          />
          <Select
            className={styles.selectMiddle}
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
      } catch {
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
            value={item?.type || 'intent'}
            onChange={(value) => onTypeChange(value, index)}
            options={[
              { label: t(`datasets.intent`), value: 'intent' },
              { label: t(`datasets.response`), value: 'response' }
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
  selectKey,
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
  useEffect(() => {
    // 🔧 只在当前选择类型为 entity 时才执行
    if (selectKey !== 'entity') {
      return;
    }
    
    if (visiable && formData) {
      setSampleList(formData?.example || [null]);
    } else if (visiable) {
      setSampleList([null]);
    }
  }, [formData, visiable, selectKey]);

  useEffect(() => {
    // 🔧 只在当前选择类型为 entity 时才执行
    if (selectKey !== 'entity') {
      return;
    }
    
    if (entityType === 'Lookup') {
      const data = formData?.example?.length ? formData.example : [null];
      setSampleList(data);
    }
  }, [entityType, selectKey])

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

  useEffect(() => {
    if (visiable && formData?.values) {
      setSampleList(formData?.values.length ?  formData?.values : [null]);
    } else if (!visiable) {
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

const useRasaForms = ({
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
  const { getRasaSlotList } = useMlopsManageApi();
  const [sampleList, setSampleList] = useState<(FormManageItem | null)[]>([]);
  const [options, setOptions] = useState<SlotOption[]>([]);

  useEffect(() => {
    // 🔧 只在当前选择类型为 form 时才执行
    if (selectKey !== 'form') {
      return;
    }
    
    if (visiable && formData?.slots) {
      const list = formData.slots.map((item: any) => {
        return {
          name: item?.name,
          type: item?.type,
          isRequired: item?.isRequired
        }
      });
      setSampleList(list);
    } else if (visiable) {
      setSampleList([{ type: 'text', name: '', isRequired: false }]);
    }
  }, [formData, visiable, selectKey]);

  useEffect(() => {
    if (selectKey !== 'form') return;

    const fetchOptions = async () => {
      try {
        const data = await getRasaSlotList({ dataset: folder_id });
        if (!data) return;
        const _options = data?.map((item: any) => {
          return {
            label: item?.name,
            value: item?.name,
            slot_type: item?.slot_type
          }
        });
        setOptions(_options || []);
      } catch(e) {
        console.log(e);
        message.error(t(`common.fetchFailed`));
      }
    };

    fetchOptions();
  }, [selectKey])

  const addSampleList = () => {
    const keys = cloneDeep(sampleList);
    keys.push({ type: '', name: '', isRequired: false });
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
      type: value as string,
      name: '',
      isRequired: false
    };
    setSampleList(keys);
  };

  const onSelectSampleChange = (value: string, index: number) => {
    const keys = cloneDeep(sampleList);
    const item = keys[index];
    if (item && typeof item === 'object' && 'name' in item) {
      item.name = value;
    }
    setSampleList(keys);
  };

  const onCheckSampleChange = (value: boolean, index: number) => {
    const keys = cloneDeep(sampleList);
    const item = keys[index];
    if (item && typeof item === 'object' && 'isRequired' in item) {
      item.isRequired = value;
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
            value={item?.type || 'text'}
            onChange={(value) => onTypeChange(value, index)}
            options={[
              {
                label: 'text(记录普通文本)',
                value: 'text'
              },
              {
                label: 'categorical(记录分类类别，枚举)',
                value: 'categorical'
              },
              {
                label: 'float(记录数值类型)',
                value: 'float'
              },
              {
                label: 'list(保存多个值的列表)',
                value: 'list'
              },
              {
                label: 'bool(布尔值，是或者否)',
                value: 'bool'
              }
            ]}
          />
          <Select
            className={`!w-[45%]`}
            value={item?.name}
            options={options.filter(itm => itm?.slot_type === item?.type)}
            onChange={(value: any) => {
              onSelectSampleChange(value, index);
            }}
          />
          <Checkbox
            checked={item?.isRequired}
            onChange={(e) => onCheckSampleChange(e.target.checked, index)}
            className="flex justify-center items-center ml-2"
          >{t(`mlops-common.required`)}</Checkbox>
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
  ), [sampleList, options]);

  return {
    sampleList,
    renderElement
  }
};

// 输入验证hooks
const useInputValidation = (selectKey: string) => {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    const allowedKeys = [
      'Backspace', 'Delete', 'Tab', 'Escape', 'Enter',
      'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown',
      'Home', 'End', 'PageUp', 'PageDown', 'Shift'
    ];

    if (allowedKeys.includes(e.key) || e.ctrlKey || e.metaKey) {
      return;
    }

    // 如果是rule类型，允许所有字符（包括中文）
    if (selectKey === 'rule') {
      return;
    }

    const regex = /^[a-zA-Z0-9_\-\s]$/;
    if (!regex.test(e.key)) {
      e.preventDefault();
    }
  };

  const handleNameChange = (formRef: React.RefObject<FormInstance>, e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;

    // 如果是rule类型，不过滤任何字符
    if (selectKey === 'rule') {
      return;
    }

    const filteredValue = value.replace(/[^a-zA-Z0-9_\-\s]/g, '');

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
    updateRasaEntityFile,
    addRasaSlotFile,
    updateRasaSlotFile,
    addRasaFormFile,
    updateRasaFormFile
  } = useMlopsManageApi();

  const handleAddMap: Record<string, any> = {
    'intent': addRasaIntentFile,
    'response': addRasaResponseFile,
    'rule': addRasaRuleFile,
    'story': addRasaStoryFile,
    'entity': addRasaEntityFile,
    'slot': addRasaSlotFile,
    'form': addRasaFormFile
  };

  const handleUpdateMap: Record<string, any> = {
    'intent': updateRasaIntentFile,
    'response': updateRasaResponseFile,
    'rule': updateRasaRuleFile,
    'story': updateRasaStoryFile,
    'entity': updateRasaEntityFile,
    'slot': updateRasaSlotFile,
    'form': updateRasaFormFile
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
    entityType?: string,
    slotType?: string,
  ) => {
    let params = {};

    if (type === 'add') {
      if (selectKey === 'rule') {
        params = {
          ...data,
          dataset: formData?.dataset,
          steps: sampleList.map((item: any) => ({
            type: item?.type,
            name: item?.select
          }))
        };
      } else if (selectKey === 'story') {
        params = {
          ...data,
          dataset: formData?.dataset,
          steps: []
        };
      } else if (selectKey === 'slot') {
        params = {
          ...data,
          dataset: formData?.dataset,
          values: slotType === 'categorical' ? sampleList : []
        }
      } else if (selectKey === 'entity') {
        params = {
          ...data,
          dataset: formData?.dataset,
          example: entityType === 'Text' ? [] : sampleList
        };
      } else if (['response', 'intent'].includes(selectKey)) {
        params = {
          ...data,
          dataset: formData?.dataset,
          example: sampleList
        };
      } else if (selectKey === 'form') {
        params = {
          ...data,
          dataset: formData?.dataset,
          slots: sampleList
        }
      } else {
        params = {
          ...data,
          dataset: formData?.dataset,
          example: sampleList
        };
      }
    } else {
      if (selectKey === 'rule') {
        params = {
          ...data,
          steps: sampleList.map((item: any) => ({
            type: item?.type,
            name: item?.select
          }))
        };
      } else if (selectKey === 'slot') {
        params = {
          ...data,
          values: slotType === 'categorical' ? sampleList : []
        }
      } else if (selectKey === 'entity') {
        params = {
          ...data,
          example: (entityType === 'Lookup') ? sampleList : []
        };
      } else if (selectKey === 'intent' || selectKey === 'response') {
        params = {
          ...data,
          example: sampleList
        };
      } else if (selectKey === 'form') {
        params = {
          ...data,
          slots: sampleList
        }
      } else {
        params = {
          ...data,
          example: sampleList
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
  const { handleKeyDown, handleNameChange } = useInputValidation(selectKey);

  // 文字选择回调函数
  const handleTextSelection = useCallback((textData: any) => {
    setSelectedTextForEntity(textData);
    modalRef.current?.showModal({ type: '' });
  }, []);

  // 🔧 所有 hooks 都调用，但在各个hook内部会检查是否为当前激活类型
  const intentForm = useRasaIntentForm({
    folder_id: Number(folder_id),
    selectKey,
    formData,
    visiable,
    onTextSelection: selectKey === 'intent' ? handleTextSelection : undefined
  });
  
  const responseForm = useRasaResponseForm({ 
    selectKey, 
    formData, 
    visiable
  });
  
  const ruleForm = useRasaRuleForm({ 
    folder_id: Number(folder_id), 
    selectKey, 
    formData, 
    visiable
  });
  
  const storyForm = useRasaStoryForm({ 
    folder_id: Number(folder_id), 
    selectKey, 
    formData, 
    visiable
  });
  
  const entityForm = useRasaEntityForm({ 
    selectKey, 
    formData, 
    visiable, 
    entityType
  });
  
  const slotForm = useRasaSlotForm({ 
    selectKey, 
    formData, 
    visiable
  });
  
  const formForm = useRasaForms({ 
    folder_id: Number(folder_id), 
    selectKey, 
    formData, 
    visiable
  });

  // 处理从Modal传来的实体选择
  const handleEntitySelectFromModal = useCallback((entityName: string) => {
    if (selectKey === 'intent' && intentForm.handleEntitySelect) {
      intentForm.handleEntitySelect(entityName);
    }
    // 清除选择状态
    setSelectedTextForEntity(null);
  }, [selectKey, intentForm.handleEntitySelect]);

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
      case 'form':
        return formForm;
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
      const params = prepareFormParams(type, selectKey, data, currentForm.sampleList, formData, entityType, slotType);
      if (type === 'add') {
        await handleAddMap[selectKey](params);
        message.success(t(`common.addSuccess`));
      } else {
        await handleUpdateMap[selectKey](formData?.id, params);
        message.success(t(`common.updateSuccess`));
      }

      onSuccess();
      setVisiable(false);
    } catch(e) {
      console.log(e);
      message.error(t(`common.error`));
    } finally {
      setConfirmLoading(false);
    }
  };

  const handleCancel = () => {
    setVisiable(false);
    setEntityType('Text');
    setSlotType('text');
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

import { Tree, Dropdown, Menu, Button, Input, Spin, message } from "antd";
import { Key, useState, useMemo, useCallback, useRef, useEffect } from "react";
import PermissionWrapper from '@/components/permission';
import { MoreOutlined, PlusOutlined } from "@ant-design/icons";
import { useTranslation } from "@/utils/i18n";
import StoryFlow from "./StoryFlow";
import contentStyle from './index.module.scss';
import EntitySelectModal from "@/app/mlops/hooks/manage/entitySelectModal";
import useMlopsManageApi from "@/app/mlops/api/manage";

// 专门为 EntitySelectModal 定义的 ref 接口
interface EntityModalRef {
  showModal: () => void;
}

interface IntentTreeProps {
  menu: string;
  dataset: string;
  data: any[];
  loading: boolean;
  handleAdd: () => void;
  handleEdit: (record: any) => void;
  handleDel: (id: number) => void;
  onSuccess: () => void;
}

const SUPPORTED_ITEMS = ['intent', 'response', 'story'] as const;

const ExampleContent = ({ menu, data, dataset, loading, handleAdd, handleEdit, handleDel, onSuccess }: IntentTreeProps) => {
  const { t } = useTranslation();
  const { updateRasaIntentFile, updateRasaResponseFile } = useMlopsManageApi();
  const [selectKey, setSelectKey] = useState<Key[]>([]);
  const [searchValue, setSearchValue] = useState<string>('');
  const [exampleText, setExampleText] = useState<string>('');
  const [editingExample, setEditingExample] = useState<boolean>(false);
  const selectedTextRef = useRef<any>(null);
  const textareaRef = useRef<any>(null);
  const entityModalRef = useRef<EntityModalRef>(null);

  const supportedItems = useMemo(() => SUPPORTED_ITEMS, []);

  const getExamplesByMenu = useCallback((menu: string, selectedData: any): string => {
    if (supportedItems.includes(menu as any)) {
      return selectedData?.example?.join('\n') || '';
    }
    return '';
  }, [supportedItems]);

  const filterTreeData = useCallback((data: any[], searchValue: string) => {
    if (!searchValue.trim()) return data;

    const searchTerm = searchValue.toLowerCase().trim();

    return data.filter((item: any) => {
      const itemName = item?.name?.toLowerCase() || '';


      return itemName.includes(searchTerm) ||
        searchTerm.split('').every(char => itemName.includes(char));
    });
  }, []);

  const treeData = useMemo(() => {
    const rawData = data?.map((item: any, index: number) => ({
      key: `${menu}_${item?.id || index}`,
      name: item?.name,
      title: item,
      ...item
    })) || [];

    return filterTreeData(rawData, searchValue);
  }, [data, menu, searchValue, filterTreeData]);

  const currentExampleText = useMemo(() => {
    if (!selectKey.length) return '';

    const [key] = selectKey;
    const id = treeData.find((item: any) => item.key === key)?.id;
    const selectedData = data?.find((item: any) => item?.id === id);

    return getExamplesByMenu(menu, selectedData);
  }, [selectKey, treeData, data, menu, getExamplesByMenu]);

  useEffect(() => {
    if (!editingExample) {
      setExampleText(currentExampleText);
    }
  }, [currentExampleText, editingExample]);

  // 当选择项变化时，退出编辑模式并更新内容
  useEffect(() => {
    setEditingExample(false);
    setExampleText(currentExampleText);
  }, [selectKey, currentExampleText]);

  // 处理文字选中
  const handleTextSelection = useCallback(() => {
    if (!textareaRef.current || menu !== 'intent') return;

    // 获取原生的 textarea DOM 元素
    const textareaComponent = textareaRef.current;
    const nativeTextarea = textareaComponent.resizableTextArea?.textArea;

    if (!nativeTextarea) return;

    const start = nativeTextarea.selectionStart;
    const end = nativeTextarea.selectionEnd;

    if (start !== null && end !== null && start !== end) {
      const text = nativeTextarea.value.substring(start, end);

      if (text.trim()) {
        const textInfo = {
          text: text.trim(),
          start,
          end,
          fullInputValue: nativeTextarea.value
        };
        selectedTextRef.current = textInfo;

        // 使用实体选择模态框
        if (entityModalRef.current) {
          entityModalRef.current.showModal();
        }
      }
    }
  }, [menu]);

  // 处理实体选择
  const handleEntitySelect = useCallback((entityName: string) => {
    const currentSelectedText = selectedTextRef.current;
    if (currentSelectedText && textareaRef.current) {
      const { text, start, end, fullInputValue } = currentSelectedText;

      const newValue =
        fullInputValue.substring(0, start) +
        `[${text}](${entityName})` +
        fullInputValue.substring(end);

      setExampleText(newValue);
      selectedTextRef.current = null;
    }
  }, []);

  // 保存样例文本
  const handleSaveExample = useCallback(async () => {
    if (!selectKey.length) return;

    const [key] = selectKey;
    const id = treeData.find((item: any) => item.key === key)?.id;
    const selectedData = data?.find((item: any) => item?.id === id);

    if (selectedData) {
      const examples = exampleText.split('\n').filter(line => line.trim());
      try {
        if (menu === 'intent') {
          await updateRasaIntentFile(id, { example: examples })
        } else if (menu === 'response') {
          await updateRasaResponseFile(id, { example: examples })
        }
        onSuccess();
      } catch (e) {
        console.log(e);
        message.error(t(`common.updateFailed`));
      } finally {
        setEditingExample(false);
      }
    }
  }, [selectKey, treeData, data, exampleText]);

  // 解析实体文字函数
  const parseEntityText = useCallback((text: string) => {
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
  }, []);

  // 渲染带实体高亮的文本
  const renderHighlightedText = useCallback((text: string) => {
    const parts = parseEntityText(text);

    return parts.map((part, index) => (
      part.type === 'entity' ? (
        <span
          key={index}
          className="text-[var(--color-text-active)] font-medium"
          title={`实体: ${part.entityName}`}
        >
          {part.content}
        </span>
      ) : (
        <span key={index}>{part.content}</span>
      )
    ));
  }, [parseEntityText]);

  const currentStory = useMemo(() => {
    if (!selectKey.length && menu !== 'story') return [];

    const [key] = selectKey;
    const id = treeData.find((item: any) => item.key === key)?.id;
    const selectedData = data?.find((item: any) => item?.id === id);
    return selectedData;
  }, [selectKey, treeData, data, menu]);

  // 高亮搜索关键词的渲染函数
  const highlightText = useCallback((text: string, searchValue: string) => {
    if (!searchValue.trim() || !text) return text;

    const regex = new RegExp(`(${searchValue.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
    const parts = text.split(regex);

    return parts.map((part, index) =>
      regex.test(part) ? (
        <span key={index}>
          {part}
        </span>
      ) : part
    );
  }, []);

  // 使用useCallback优化渲染函数，添加搜索高亮
  const renderTitle = useCallback((data: any) => {
    const displayName = data?.name || '--';
    const highlightedName = highlightText(displayName, searchValue);

    return (
      <div className='w-full flex justify-between'>
        <span className='truncate w-[120px]' title={displayName}>{highlightedName}</span>
        <span>
          <Dropdown
            overlay={
              <Menu
                onClick={(e) => e.domEvent.preventDefault()}
              >
                <Menu.Item
                  key="edit"
                  className='!p-0'
                  onClick={(e) => {
                    e.domEvent.stopPropagation();
                    handleEdit(data);
                  }}>
                  <PermissionWrapper requiredPermissions={['File Edit']} className='!block'>
                    <Button type='text' className='w-full'>{t(`common.edit`)}</Button>
                  </PermissionWrapper>
                </Menu.Item>
                <Menu.Item
                  key="delete"
                  className='!p-0'
                  onClick={() => {
                    handleDel(data?.id)
                  }}>
                  <PermissionWrapper requiredPermissions={['File Delete']} className='!block'>
                    <Button type='text' className='w-full'>{t(`common.delete`)}</Button>
                  </PermissionWrapper>
                </Menu.Item>
              </Menu>
            }
            trigger={['click']}
          >
            <MoreOutlined
              className="cursor-pointer"
              onClick={(e) => {
                e.stopPropagation();
                e.preventDefault();
              }}
            />
          </Dropdown>
        </span>
      </div>
    )
  }, [handleEdit, handleDel, t, highlightText, searchValue]);

  // 使用useCallback优化事件处理
  const onChange = useCallback((value: string) => {
    setSearchValue(value);
    // 如果搜索框清空，清除选中状态
    if (!value.trim()) {
      setSelectKey([]);
    } else {
      // 实时搜索：输入时自动过滤并选择第一个结果
      const filteredData = filterTreeData(data?.map((item: any, index: number) => ({
        key: `${menu}_${item?.id || index}`,
        name: item?.name,
        title: item,
        ...item
      })) || [], value);

      if (filteredData.length > 0) {
        setSelectKey([filteredData[0].key]);
      }
    }
  }, [data, menu, filterTreeData]);

  const onSearch = useCallback((value: string) => {
    // 支持搜索按钮点击，与onChange保持一致的逻辑
    if (value.trim() && treeData.length > 0) {
      setSelectKey([treeData[0].key]);
    }
  }, [treeData]); 
  
  const onSelect = useCallback((key: Key[]) => {
    if (key.length) setSelectKey(key);
  }, []);

  return (
    <>
      <div className={`${contentStyle.flowContainer}`}>
        <Spin spinning={loading}>
          <div className="flex h-full">
            <div className="w-[180px] mr-4 flex flex-col">
              <div className="flex mb-1 flex-shrink-0">
                <Input.Search
                  size="small"
                  className="flex-1"
                  placeholder={`${t('common.search')}...`}
                  allowClear
                  enterButton
                  onSearch={onSearch}
                  onChange={(e) => onChange(e.target.value)}
                  value={searchValue}
                />
                <Button type="primary" size="small" className="ml-1" icon={<PlusOutlined />} onClick={handleAdd} />
              </div>
              {searchValue && treeData.length === 0 && (
                <div className="text-gray-400 text-center py-2 text-sm">
                  {t(`mlops-common.noSearchData`)}
                </div>
              )}
              <div className="flex-1 overflow-y-auto">
                <Tree
                  className="w-full h-full"
                  showLine
                  blockNode
                  expandAction={false}
                  defaultExpandAll
                  autoExpandParent
                  treeData={treeData}
                  titleRender={(nodeData: any) => renderTitle(nodeData)}
                  onSelect={onSelect}
                  selectedKeys={selectKey}
                />
              </div>
            </div>
            <div className="flex-1 h-full">
              {
                menu === 'story' ? (
                  <StoryFlow
                    dataset={dataset}
                    currentStory={currentStory}
                    onSuccess={onSuccess}
                  />
                ) : supportedItems.includes(menu as any) ? (
                  <div className="h-full flex flex-col border border-gray-200 rounded">
                    {/* 头部工具栏 */}
                    <div className="flex justify-between items-center p-3 border-b border-gray-200 bg-gray-50">
                      <h3 className="text-sm font-medium text-gray-800">
                        {t(`datasets.example`)} ({menu})
                      </h3>
                      <div className="flex space-x-2">
                        {editingExample ? (
                          <>
                            <Button
                              size="small"
                              onClick={() => {
                                setEditingExample(false);
                                setExampleText(currentExampleText);
                              }}
                            >
                              {t('common.cancel')}
                            </Button>
                            <Button
                              type="primary"
                              size="small"
                              onClick={handleSaveExample}
                            >
                              {t('common.save')}
                            </Button>
                          </>
                        ) : (
                          <Button
                            type="primary"
                            size="small"
                            onClick={() => setEditingExample(true)}
                          >
                            {t('common.edit')}
                          </Button>
                        )}
                      </div>
                    </div>

                    {/* 内容区域 */}
                    <div className="flex-1 p-3 overflow-hidden">
                      {editingExample ? (
                        <Input.TextArea
                          ref={textareaRef}
                          value={exampleText}
                          onChange={(e) => setExampleText(e.target.value)}
                          onMouseUp={handleTextSelection}
                          onKeyUp={handleTextSelection}
                          placeholder={t(`datasets.editEaxmpleTip`)}
                          className="w-full h-full resize-none border-0 focus:shadow-none"
                          style={{ height: '100%' }}
                        />
                      ) : (
                        <div className="w-full h-full overflow-y-auto overflow-x-hidden whitespace-pre-wrap p-2 bg-gray-50 rounded border">
                          {currentExampleText ? (
                            currentExampleText.split('\n').map((line, index) => (
                              <div key={index} className="mb-2 last:mb-0 break-words">
                                {menu === 'intent' ? renderHighlightedText(line) : line}
                              </div>
                            ))
                          ) : (
                            <div className="text-gray-400 text-center py-8">
                              {t(`common.noData`)}
                            </div>
                          )}
                        </div>
                      )}
                    </div>

                    {/* 底部提示 */}
                    {menu === 'intent' && (
                      <div className="px-3 py-2 border-t border-gray-200 bg-gray-50">
                        <div className="text-xs text-gray-500">
                          {t(`datasets.selectEntityTip`)}
                        </div>
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="h-full flex items-center justify-center text-gray-400">
                    不支持的数据类型
                  </div>
                )
              }
            </div>
          </div>
        </Spin>
      </div>

      {/* 实体选择模态框 */}
      <EntitySelectModal
        ref={entityModalRef}
        dataset={dataset}
        onSuccess={handleEntitySelect}
      />
    </>
  );
};

export default ExampleContent;
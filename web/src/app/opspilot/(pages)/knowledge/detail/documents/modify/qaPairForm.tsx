import React, { useState, useEffect, forwardRef, useImperativeHandle, useCallback, useMemo, useRef } from 'react';
import { Form, Select, InputNumber, Tabs, message, Button, Drawer, Space, Tag, Divider, Empty } from 'antd';
import { PlusOutlined, CloseOutlined, ClearOutlined } from '@ant-design/icons';
import { useTranslation } from '@/utils/i18n';
import { useKnowledgeApi } from '@/app/opspilot/api/knowledge';
import { useSkillApi } from '@/app/opspilot/api/skill';
import { useSearchParams } from 'next/navigation';
import CustomTable from '@/components/custom-table';

const { TabPane } = Tabs;

interface QAPairFormData {
  llmModel: number;
  qaCount: number;
  selectedDocuments: string[];
}

interface DocumentItem {
  key: string;
  title: string;
  description?: string;
}

interface QAPairFormProps {
  initialData?: Partial<QAPairFormData>;
  onFormChange?: (isValid: boolean) => void;
  onFormDataChange?: (data: QAPairFormData) => void;
}

const QAPairForm = forwardRef<any, QAPairFormProps>(({ 
  initialData, 
  onFormChange = () => {}, 
  onFormDataChange = () => {} 
}, ref) => {
  const [form] = Form.useForm();
  const { t } = useTranslation();
  const searchParams = useSearchParams();
  const id = searchParams ? searchParams.get('id') : null;
  const { fetchDocuments, createQAPairs } = useKnowledgeApi();
  const { fetchLlmModels: fetchLlmModelsApi } = useSkillApi();

  const [llmModels, setLlmModels] = useState<any[]>([]);
  const [documentData, setDocumentData] = useState<{[key: string]: DocumentItem[]}>({
    file: [],
    web_page: [],
    manual: []
  });
  const [documentTotalCounts, setDocumentTotalCounts] = useState<{[key: string]: number}>({
    file: 0,
    web_page: 0,
    manual: 0
  });
  const [selectedDocuments, setSelectedDocuments] = useState<string[]>([]);
  const [activeDocumentTab, setActiveDocumentTab] = useState<string>('file');
  const [loading, setLoading] = useState<boolean>(false);
  const [drawerVisible, setDrawerVisible] = useState<boolean>(false);
  const [tempSelectedDocuments, setTempSelectedDocuments] = useState<string[]>([]);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [pageSize, setPageSize] = useState<number>(10);
  
  const formValuesRef = useRef({
    llmModel: 0,
    qaCount: 10
  });
  const onFormChangeRef = useRef(onFormChange);
  const onFormDataChangeRef = useRef(onFormDataChange);

  useEffect(() => {
    onFormChangeRef.current = onFormChange;
    onFormDataChangeRef.current = onFormDataChange;
  }, [onFormChange, onFormDataChange]);

  useImperativeHandle(ref, () => ({
    validateFields: () => form.validateFields(),
    getFieldsValue: () => ({
      ...formValuesRef.current,
      selectedDocuments
    }),
    createQAPairs: handleCreateQAPairs
  }));

  const fetchLlmModels = useCallback(async () => {
    try {
      const models = await fetchLlmModelsApi();
      setLlmModels(models);
      
      // Set default LLM model to first item if no initial data
      if (!initialData?.llmModel && models.length > 0) {
        const defaultValues = {
          llmModel: models[0].id,
          qaCount: 10
        };
        form.setFieldsValue(defaultValues);
        formValuesRef.current = defaultValues;
      }
    } catch {
      message.error(t('common.fetchFailed'));
    }
  }, [initialData, form]);

  const fetchDocumentsByType = useCallback(async (type: string, page: number, pageSize: number) => {
    if (!id) return;
    
    setLoading(true);
    try {
      const result = await fetchDocuments({
        knowledge_source_type: type,
        knowledge_base_id: id,
        page,
        page_size: pageSize
      });
      
      const processedItems = result.items.map((item: any) => ({
        key: item.id.toString(),
        title: item.name,
      }));
      
      setDocumentData(prev => ({
        ...prev,
        [type]: processedItems
      }));
      
      setDocumentTotalCounts(prev => ({
        ...prev,
        [type]: result.count || result.items.length
      }));
      
    } catch {
      message.error('获取文档列表失败');
    } finally {
      setLoading(false);
    }
  }, [id, fetchDocuments]);

  useEffect(() => {
    if (drawerVisible && activeDocumentTab && id) {
      fetchDocumentsByType(activeDocumentTab, currentPage, pageSize);
    }
  }, [drawerVisible, activeDocumentTab, currentPage, pageSize, id]);

  useEffect(() => {
    fetchLlmModels();
  }, []);

  useEffect(() => {
    if (initialData) {
      const values = {
        llmModel: initialData.llmModel || 0,
        qaCount: initialData.qaCount || 10
      };
      form.setFieldsValue(values);
      formValuesRef.current = values;
      
      if (initialData.selectedDocuments) {
        setSelectedDocuments(initialData.selectedDocuments);
      }
    }
  }, [initialData, form]);

  const handleDocumentSelect = useCallback((keys: React.Key[]) => {
    setTempSelectedDocuments(keys.map(key => key.toString()));
  }, []);

  const handleTempRemoveDocument = useCallback((documentKey: string) => {
    setTempSelectedDocuments(prev => prev.filter(key => key !== documentKey));
  }, []);

  const handleTempClearAllDocuments = useCallback(() => {
    setTempSelectedDocuments([]);
  }, []);

  const getSelectedDocumentInfo = useCallback((documentKey: string) => {
    for (const type in documentData) {
      const doc = documentData[type].find(item => item.key === documentKey);
      if (doc) {
        return { ...doc, type };
      }
    }
    return null;
  }, [documentData]);

  const tempSelectedDocumentsList = useMemo(() => {
    return tempSelectedDocuments.map(key => {
      const docInfo = getSelectedDocumentInfo(key);
      return docInfo ? { ...docInfo } : { key, title: `文档 ${key}`, type: 'unknown' };
    }).filter(Boolean);
  }, [tempSelectedDocuments]);

  const getDocumentTypeLabel = useCallback((type: string) => {
    switch (type) {
      case 'file':
        return t('knowledge.localFile');
      case 'web_page':
        return t('knowledge.webLink');
      case 'manual':
        return t('knowledge.cusText');
      default:
        return type;
    }
  }, []);

  const handleFormValuesChange = useCallback((_: any, allValues: any) => {
    const newValues = {
      llmModel: allValues.llmModel || 0,
      qaCount: allValues.qaCount || 10
    };
    formValuesRef.current = newValues;
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      const isValid = !!(
        formValuesRef.current.llmModel && 
        formValuesRef.current.qaCount && 
        selectedDocuments.length > 0
      );
      
      onFormChangeRef.current(isValid);
      onFormDataChangeRef.current({
        ...formValuesRef.current,
        selectedDocuments
      });
    }, 100);
    
    return () => clearTimeout(timer);
  }, [selectedDocuments, formValuesRef.current.llmModel, formValuesRef.current.qaCount]);

  const handleTabChange = useCallback((tabKey: string) => {
    setActiveDocumentTab(tabKey);
    setCurrentPage(1);
  }, []);

  const handlePaginationChange = useCallback((page: number, size: number) => {
    setCurrentPage(page);
    if (size !== pageSize) {
      setPageSize(size);
      setCurrentPage(1);
    }
  }, [pageSize]);

  const paginatedDocuments = useMemo(() => {
    return documentData[activeDocumentTab] || [];
  }, [documentData, activeDocumentTab]);

  const columns = useMemo(() => [{
    title: t('knowledge.documents.name'),
    dataIndex: 'title',
    key: 'title',
    render: (text: string) => (
      <div>
        <div className="font-medium">{text}</div>
      </div>
    ),
  }], [t]);

  // Create QA pairs based on selected documents and form data
  const handleCreateQAPairs = useCallback(async () => {
    if (!id || selectedDocuments.length === 0 || !formValuesRef.current.llmModel) {
      message.error('请确保已选择文档和LLM模型');
      return;
    }

    try {
      await form.validateFields();
      
      setLoading(true);
      
      // Build document list with metadata
      const documentList = selectedDocuments.map(docKey => {
        const docInfo = getSelectedDocumentInfo(docKey);
        return {
          name: docInfo?.title || `文档-${docKey}`,
          document_id: parseInt(docKey),
          document_source: docInfo?.type || 'file'
        };
      });

      const payload = {
        knowledge_base_id: parseInt(id),
        llm_model_id: formValuesRef.current.llmModel,
        qa_count: formValuesRef.current.qaCount,
        document_list: documentList
      };

      await createQAPairs(payload);
      message.success('问答对创建成功');
      
      // Return success to parent component
      return Promise.resolve();
      
    } catch (error) {
      message.error('问答对创建失败');
      throw error;
    } finally {
      setLoading(false);
    }
  }, [id, selectedDocuments, form, createQAPairs, getSelectedDocumentInfo]);

  return (
    <div className="max-w-4xl mx-auto p-6">
      <Form
        form={form}
        layout="vertical"
        initialValues={{ qaCount: 10, ...initialData }}
        onValuesChange={handleFormValuesChange}
      >
        <Form.Item
          name="llmModel"
          label={t('knowledge.qaPairs.llmModel')}
          rules={[{ required: true }]}
        >
          <Select
            placeholder={t('common.select')}
            loading={loading}
            size="large"
          >
            {llmModels.map(model => (
              <Select.Option key={model.id} value={model.id}>
                {model.name}
              </Select.Option>
            ))}
          </Select>
        </Form.Item>

        <Form.Item
          name="qaCount"
          label={t('knowledge.qaPairs.qaCount')}
          rules={[{ required: true }]}
        >
          <InputNumber
            min={1}
            max={1000}
            className="w-full"
            size="large"
          />
        </Form.Item>

        <Form.Item
          label={
            <div className="flex items-center">
              <span>{t('knowledge.qaPairs.targetDocuments')}</span>
              <Space className="ml-4">
                <span className="text-blue-500">
                  ({selectedDocuments.length}) {t('knowledge.qaPairs.documentsSelected')}
                </span>
                <Button
                  type="primary"
                  icon={<PlusOutlined />}
                  size="small"
                  onClick={() => {
                    setTempSelectedDocuments(selectedDocuments);
                    setDrawerVisible(true);
                  }}
                >
                  {t('common.add')}
                </Button>
              </Space>
            </div>
          }
          required
        >
          <div style={{ display: 'none' }}>
            <input value={selectedDocuments.join(',')} readOnly />
          </div>
        </Form.Item>
      </Form>

      <Drawer
        title={t('knowledge.qaPairs.selectDocuments')}
        placement="right"
        width={900}
        onClose={() => setDrawerVisible(false)}
        open={drawerVisible}
        footer={
          <div className="flex justify-end space-x-2">
            <Button onClick={() => setDrawerVisible(false)}>
              {t('common.cancel')}
            </Button>
            <Button 
              type="primary" 
              onClick={() => {
                setSelectedDocuments(tempSelectedDocuments);
                setDrawerVisible(false);
                message.success(`已选择 ${tempSelectedDocuments.length} 个文档`);
              }}
            >
              {t('common.confirm')} ({tempSelectedDocuments.length})
            </Button>
          </div>
        }
      >
        <div className="flex gap-4" style={{ height: 'calc(100vh - 160px)' }}>
          <div className="w-3/5 border rounded-lg p-4 bg-gray-50 flex flex-col">
            <Tabs
              activeKey={activeDocumentTab}
              onChange={handleTabChange}
              size="small"
            >
              <TabPane tab={t('knowledge.localFile')} key="file" />
              <TabPane tab={t('knowledge.webLink')} key="web_page" />
              <TabPane tab={t('knowledge.cusText')} key="manual" />
            </Tabs>
            
            <div className="flex-1 mt-4">
              <CustomTable
                size="small"
                columns={columns}
                dataSource={paginatedDocuments}
                rowSelection={{
                  type: 'checkbox',
                  selectedRowKeys: tempSelectedDocuments,
                  onChange: handleDocumentSelect,
                  preserveSelectedRowKeys: true,
                }}
                pagination={{
                  current: currentPage,
                  total: documentTotalCounts[activeDocumentTab],
                  pageSize: pageSize,
                  showSizeChanger: true,
                  onChange: handlePaginationChange,
                }}
                loading={loading}
                scroll={{ 
                  y: 'calc(100vh - 370px)',
                }}
              />
            </div>
          </div>

          <div className="w-2/5 flex flex-col">
            <div className="border rounded-lg p-4 bg-white h-full flex flex-col">
              <div className="flex items-center justify-between mb-2">
                <h4 className="text-base font-medium m-0">
                  {t('knowledge.qaPairs.pendingDocuments')} ({tempSelectedDocuments.length})
                </h4>
                {tempSelectedDocuments.length > 0 && (
                  <Button
                    type="text"
                    size="small"
                    icon={<ClearOutlined />}
                    onClick={handleTempClearAllDocuments}
                    className="text-red-500 hover:text-red-700"
                  >
                    {t('common.clear')}
                  </Button>
                )}
              </div>
              
              <Divider className="my-2" />
              
              <div className="flex-1 overflow-auto">
                {tempSelectedDocumentsList.length === 0 ? (
                  <Empty 
                    description="请从左侧表格选择文档"
                    image={Empty.PRESENTED_IMAGE_SIMPLE}
                    className="mt-8"
                  />
                ) : (
                  <div className="space-y-2">
                    {tempSelectedDocumentsList.map(doc => (
                      <div
                        key={doc.key}
                        className="flex items-start justify-between p-3 bg-blue-50 rounded-md hover:bg-blue-100 transition-colors border border-blue-200"
                      >
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1">
                            <Tag 
                              color="blue"
                              className="text-xs"
                            >
                              {getDocumentTypeLabel(doc.type)}
                            </Tag>
                          </div>
                          <div 
                            className="text-sm font-medium text-gray-900 truncate"
                            title={doc.title}
                          >
                            {doc.title}
                          </div>
                        </div>
                        <Button
                          type="text"
                          size="small"
                          icon={<CloseOutlined />}
                          onClick={() => handleTempRemoveDocument(doc.key)}
                          className="text-gray-400 hover:text-red-500 flex-shrink-0 ml-2"
                          style={{ minWidth: 'auto', padding: '4px' }}
                        />
                      </div>
                    ))}
                  </div>
                )}
              </div>
              
              {tempSelectedDocuments.length > 0 && (
                <div className="mt-4 pt-3 border-t border-gray-200 flex-shrink-0">
                  <div className="text-xs text-blue-600 text-center">
                    点击&ldquo;确认&rdquo;按钮后生效
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </Drawer>
    </div>
  );
});

QAPairForm.displayName = 'QAPairForm';

export default QAPairForm;
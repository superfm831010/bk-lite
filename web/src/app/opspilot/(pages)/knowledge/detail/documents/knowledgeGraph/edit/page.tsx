'use client';
import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Form, Button, Select, Switch, message, Space, Tag, Empty, Drawer, Tabs, Divider } from 'antd';
import { SaveOutlined, PlusOutlined, CloseOutlined, ClearOutlined } from '@ant-design/icons';
import { useTranslation } from '@/utils/i18n';
import PermissionWrapper from '@/components/permission';
import CustomTable from '@/components/custom-table';
import { useKnowledgeApi } from '@/app/opspilot/api/knowledge';
import { useSkillApi } from '@/app/opspilot/api/skill';

const { TabPane } = Tabs;

interface GraphConfig {
  selectedDocuments: string[];
  llmModel: number;
  rerankModel: number;
  embedModel: number;
  enableRerank: boolean;
  enableRebuildGroup: boolean;
}

interface DocumentItem {
  key: string;
  title: string;
  description: string;
  status: string;
  type?: string;
}

const KnowledgeGraphEditPage: React.FC = () => {
  const { t } = useTranslation();
  const router = useRouter();
  const searchParams = useSearchParams();
  const [form] = Form.useForm();
  
  const id = searchParams?.get('id');
  
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [llmModels, setLlmModels] = useState<any[]>([]);
  const [rerankModels, setRerankModels] = useState<any[]>([]);
  const [embedModels, setEmbedModels] = useState<any[]>([]);
  
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
  const [tempSelectedDocuments, setTempSelectedDocuments] = useState<string[]>([]);
  const [drawerVisible, setDrawerVisible] = useState<boolean>(false);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [pageSize, setPageSize] = useState<number>(10);
  const [activeDocumentTab, setActiveDocumentTab] = useState<string>('file');
  
  const [config, setConfig] = useState<GraphConfig>({
    selectedDocuments: [],
    llmModel: 0,
    rerankModel: 0,
    embedModel: 0,
    enableRerank: false,
    enableRebuildGroup: false,
  });

  const { fetchDocuments, fetchSemanticModels, fetchEmbeddingModels, saveKnowledgeGraph } = useKnowledgeApi();
  const { fetchLlmModels: fetchLlmModelsApi } = useSkillApi();

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
        status: item.train_status_display,
        type: type
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
      message.error(t('common.fetchFailed'));
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    if (drawerVisible && id) {
      fetchDocumentsByType(activeDocumentTab, currentPage, pageSize);
    }
  }, [drawerVisible, currentPage, pageSize, id, activeDocumentTab]);

  useEffect(() => {
    const initializeData = async () => {
      setLoading(true);
      try {
        const [llmData, rerankData, embedData] = await Promise.all([
          fetchLlmModelsApi(),
          fetchSemanticModels(),
          fetchEmbeddingModels()
        ]);
        
        setLlmModels(llmData);
        setRerankModels(rerankData);
        setEmbedModels(embedData);
        
        const defaultConfig = {
          selectedDocuments: [],
          llmModel: llmData.length > 0 ? llmData[0].id : 0,
          rerankModel: rerankData.length > 0 ? rerankData[0].id : 0,
          embedModel: embedData.length > 0 ? embedData[0].id : 0,
          enableRerank: false,
          enableRebuildGroup: false,
        };
        
        setConfig(defaultConfig);
        form.setFieldsValue(defaultConfig);
        
      } catch (error) {
        console.error('Failed to initialize data:', error);
        message.error(t('common.initializeFailed'));
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      initializeData();
    } else {
      setLoading(false);
      message.error(t('common.missingId'));
    }
  }, [id]);

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
      return docInfo ? { ...docInfo } : { key, title: `文档 ${key}`, type: 'unknown', description: '', status: '' };
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

  const handleSave = async () => {
    try {
      const values = await form.validateFields();
      setSaving(true);
      
      const saveParams = {
        knowledge_base: Number(id),
        llm_model: values.llmModel,
        rerank_model: values.rerankModel,
        embed_model: values.embedModel,
        rebuild_community: values.enableRebuildGroup,
        doc_list: selectedDocuments.map(docKey => {
          const docInfo = getSelectedDocumentInfo(docKey);
          return {
            id: Number(docKey),
            source: docInfo?.type || 'file'
          };
        })
      };
      
      console.log('保存知识图谱配置:', saveParams);
      
      await saveKnowledgeGraph(saveParams);
      
      message.success(t('knowledge.knowledgeGraph.rebuildSuccess'));
      router.back();
      
    } catch (error) {
      console.error('Failed to save config:', error);
      message.error(t('common.saveFailed'));
    } finally {
      setSaving(false);
    }
  };

  const handleBack = () => {
    router.back();
  };

  const handleFormChange = (changedValues: any, allValues: any) => {
    setConfig(prev => ({ ...prev, ...allValues }));
  };

  const handleTabChange = (key: string) => {
    setActiveDocumentTab(key);
    setCurrentPage(1);
    fetchDocumentsByType(key, 1, pageSize);
  };

  const handlePaginationChange = (page: number, pageSize?: number) => {
    setCurrentPage(page);
    if (pageSize) setPageSize(pageSize);
    fetchDocumentsByType(activeDocumentTab, page, pageSize || 10);
  };

  const paginatedDocuments = useMemo(() => {
    return documentData[activeDocumentTab] || [];
  }, [documentData, activeDocumentTab]);

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <Form
        form={form}
        layout="vertical"
        onValuesChange={handleFormChange}
        initialValues={config}
      >
        <Form.Item
          name="llmModel"
          label={t('knowledge.knowledgeGraph.llmModel')}
          rules={[{ required: true, message: t('common.pleaseSelect') + t('knowledge.knowledgeGraph.llmModel') }]}
        >
          <Select placeholder={t('common.pleaseSelect') + t('knowledge.knowledgeGraph.llmModel')} loading={llmModels.length === 0}>
            {llmModels.map(model => (
              <Select.Option key={model.id} value={model.id}>
                {model.name}
              </Select.Option>
            ))}
          </Select>
        </Form.Item>

        <Form.Item
          name="rerankModel"
          label={t('knowledge.knowledgeGraph.rerankModel')}
          rules={[{ required: true, message: t('common.pleaseSelect') + t('knowledge.knowledgeGraph.rerankModel') }]}
        >
          <Select placeholder={t('common.pleaseSelect') + t('knowledge.knowledgeGraph.rerankModel')} loading={rerankModels.length === 0}>
            {rerankModels.map(model => (
              <Select.Option key={model.id} value={model.id}>
                {model.name}
              </Select.Option>
            ))}
          </Select>
        </Form.Item>

        <Form.Item
          name="embedModel"
          label={t('knowledge.form.embedModel')}
          rules={[{ required: true, message: t('common.pleaseSelect') + t('knowledge.form.embedModel') }]}
        >
          <Select placeholder={t('common.pleaseSelect') + t('knowledge.form.embedModel')} loading={embedModels.length === 0}>
            {embedModels.map(model => (
              <Select.Option key={model.id} value={model.id}>
                {model.name}
              </Select.Option>
            ))}
          </Select>
        </Form.Item>

        <Form.Item
          name="enableRebuildGroup"
          label={t('knowledge.knowledgeGraph.rebuild')}
          valuePropName="checked"
        >
          <Switch size="small" />
        </Form.Item>
        <Form.Item
          label={
            <div className="flex items-center">
              <span>{t('knowledge.knowledgeGraph.selectDocuments')}</span>
              <Space className="ml-4">
                <span className="text-blue-500">
                  ({selectedDocuments.length}) {t('knowledge.knowledgeGraph.documentsSelected')}
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
                  {t('knowledge.knowledgeGraph.selectDocuments')}
                </Button>
              </Space>
            </div>
          }
        >
          <div style={{ display: 'none' }}>
            <input value={selectedDocuments.join(',')} readOnly />
          </div>
        </Form.Item>
      </Form>

      <div className="fixed bottom-6 right-6 z-50">
        <div className="flex gap-3 pb-4">
          <Button onClick={handleBack}>
            {t('common.cancel')}
          </Button>
          <PermissionWrapper requiredPermissions={['Edit']}>
            <Button
              type="primary"
              icon={<SaveOutlined />}
              onClick={handleSave}
              loading={saving}
            >
              {t('common.save')}
            </Button>
          </PermissionWrapper>
        </div>
      </div>

      <Drawer
        title={t('knowledge.knowledgeGraph.selectDocuments')}
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
                message.success(t('common.saveSuccess').replace('{count}', tempSelectedDocuments.length.toString()));
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
                columns={[
                  {
                    title: t('knowledge.knowledgeGraph.documentName'),
                    dataIndex: 'title',
                    key: 'title',
                  },
                  {
                    title: t('knowledge.knowledgeGraph.documentStatus'),
                    dataIndex: 'status',
                    key: 'status',
                  },
                ]}
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
                    description={t('knowledge.qaPairs.noDocumentsSelected')}
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
                            <Tag color="blue" className="text-xs">
                              {getDocumentTypeLabel(doc.type || '')}
                            </Tag>
                            <Tag color={doc.status === '已完成' ? 'green' : 'orange'} className="text-xs">
                              {doc.status}
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
                    {t('knowledge.qaPairs.confirmToApply')}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </Drawer>
    </div>
  );
};

export default KnowledgeGraphEditPage;
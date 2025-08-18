'use client';

import React, { useState, useEffect, forwardRef, useImperativeHandle, useRef } from 'react';
import { Form, Select, InputNumber, message, Spin, Tag } from 'antd';
import { RobotOutlined, QuestionCircleOutlined } from '@ant-design/icons';
import { useTranslation } from '@/utils/i18n';
import { useKnowledgeApi } from '@/app/opspilot/api/knowledge';
import { useSkillApi } from '@/app/opspilot/api/skill';
import OperateModal from '@/components/operate-modal';
import type {
  GenerateQAPairModalProps,
  ModalRef,
  DocumentInfo,
  FormData,
  ChunkItem
} from '@/app/opspilot/types/knowledge';

const GenerateQAPairModal = forwardRef<ModalRef, GenerateQAPairModalProps>(
  ({ onSuccess }, ref) => {
    const [form] = Form.useForm();
    const { t } = useTranslation();
    const { createQAPairsByChunk, getInstanceDetail } = useKnowledgeApi();
    const { fetchLlmModels: fetchLlmModelsApi } = useSkillApi();

    const [visible, setVisible] = useState<boolean>(false);
    const [confirmLoading, setConfirmLoading] = useState<boolean>(false);
    const [loading, setLoading] = useState<boolean>(false);
    const [llmModelsLoading, setLlmModelsLoading] = useState<boolean>(false);
    const [llmModels, setLlmModels] = useState<any[]>([]);
    const [documentId, setDocumentId] = useState<string>('');
    const [selectedChunkIds, setSelectedChunkIds] = useState<string[]>([]);
    const [selectedChunks, setSelectedChunks] = useState<ChunkItem[]>([]);
    const [documentInfo, setDocumentInfo] = useState<DocumentInfo | null>(null);

    const formRef = useRef<FormData>({
      llmModel: 0,
      qaCount: 1
    });

    const fetchDocumentDetail = async (docId: string) => {
      try {
        setLoading(true);
        const detail = await getInstanceDetail(parseInt(docId));
        console.log('Document detail fetched:', detail);
        setDocumentInfo(detail);
      } catch (error) {
        console.error('Failed to fetch document detail:', error);
        message.error('获取文档信息失败');
      } finally {
        setLoading(false);
      }
    };

    useImperativeHandle(ref, () => ({
      showModal: ({ documentId, selectedChunkIds = [], selectedChunks = [] }) => {
        setDocumentId(documentId);
        setSelectedChunkIds(selectedChunkIds);
        setSelectedChunks(selectedChunks);
        setVisible(true);
        
        // 打开弹窗时立即获取文档详情
        if (documentId) {
          fetchDocumentDetail(documentId);
        }
        
        // 重置表单到默认值
        form.resetFields();
        formRef.current = {
          llmModel: 0,
          qaCount: 1
        };
      }
    }));

    // 获取LLM模型列表
    const fetchLlmModels = async () => {
      setLlmModelsLoading(true);
      try {
        const models = await fetchLlmModelsApi();
        setLlmModels(models);
        
        // 设置默认模型
        if (models.length > 0) {
          const defaultValues = {
            llmModel: models[0].id,
            qaCount: 1
          };
          form.setFieldsValue(defaultValues);
          formRef.current = defaultValues;
        }
      } catch {
        message.error(t('common.fetchFailed'));
      } finally {
        setLlmModelsLoading(false);
      }
    };

    useEffect(() => {
      if (visible) {
        fetchLlmModels();
      }
    }, [visible]);

    // 处理表单值变化
    const handleFormValuesChange = (changedValues: any, allValues: FormData) => {
      formRef.current = {
        llmModel: allValues.llmModel || 0,
        qaCount: allValues.qaCount || 1
      };
    };

    // 处理确认操作
    const handleConfirm = async () => {
      try {
        await form.validateFields();
        
        console.log('Debug - Validation check:', {
          documentId,
          selectedChunkIds,
          selectedChunks,
          selectedChunksLength: selectedChunks.length,
          formRefCurrent: formRef.current,
          llmModel: formRef.current.llmModel,
          documentInfo
        });
        
        if (!documentId) {
          message.error('文档ID不存在');
          return;
        }
        
        if (!documentInfo) {
          message.error('文档信息未加载');
          return;
        }
        
        if (selectedChunks.length === 0) {
          message.error('请先选择分块');
          return;
        }
        
        if (!formRef.current.llmModel || formRef.current.llmModel === 0) {
          message.error('请选择LLM模型');
          return;
        }

        setConfirmLoading(true);

        // 使用已获取的文档详情和传递过来的chunk数据构建请求参数
        const payload = {
          name: documentInfo.name,
          knowledge_base_id: documentInfo.knowledge_base_id,
          document_id: parseInt(documentId),
          document_source: documentInfo.knowledge_source_type,
          qa_count: formRef.current.qaCount,
          llm_model_id: formRef.current.llmModel,
          chunk_list: selectedChunks.map(chunk => ({
            content: chunk.content,
            id: chunk.id
          }))
        };

        console.log('Debug - Request payload:', payload);

        await createQAPairsByChunk(payload);
        message.success(t('knowledge.qaPairs.generateSuccess'));
        
        handleCancel();
        onSuccess?.();
        
      } catch (error) {
        console.error('Generate QA pairs error:', error);
        message.error(t('knowledge.qaPairs.generateFailed'));
      } finally {
        setConfirmLoading(false);
      }
    };

    // 处理取消操作
    const handleCancel = () => {
      setVisible(false);
      setDocumentId('');
      setSelectedChunkIds([]);
      setSelectedChunks([]);
      setDocumentInfo(null);
      form.resetFields();
    };

    return (
      <OperateModal
        title={
          <div className="flex items-center">
            <RobotOutlined className="mr-2 text-blue-500" />
            {t('knowledge.qaPairs.generateTitle')}
          </div>
        }
        open={visible}
        confirmLoading={confirmLoading}
        onOk={handleConfirm}
        onCancel={handleCancel}
        okText={t('knowledge.qaPairs.startGenerate')}
        cancelText={t('common.cancel')}
        cancelButtonProps={{ disabled: confirmLoading }}
        width={580}
        destroyOnClose
      >
        <Spin spinning={loading}>
          <div className="space-y-6">
            <Form
              form={form}
              layout="vertical"
              onValuesChange={handleFormValuesChange}
              initialValues={{
                qaCount: 1
              }}
            >
              <Form.Item
                name="llmModel"
                label={
                  <div className="flex items-center">
                    <RobotOutlined className="mr-1" />
                    {t('knowledge.qaPairs.llmModel')}
                  </div>
                }
                rules={[{ required: true, message: t('common.required') }]}
              >
                <Select
                  placeholder={t('knowledge.qaPairs.selectLlmModel')}
                  loading={llmModelsLoading}
                  size="large"
                  showSearch
                  optionFilterProp="label"
                  filterOption={(input, option) =>
                    (option?.label ?? '').toLowerCase().includes(input.toLowerCase())
                  }
                  options={llmModels.map(model => ({
                    key: model.id,
                    value: model.id,
                    label: model.name,
                    children: (
                      <div className="flex items-center">
                        <RobotOutlined className="mr-2 text-blue-500" />
                        {model.name}
                      </div>
                    )
                  }))}
                />
              </Form.Item>

              <Form.Item
                name="qaCount"
                label={
                  <div className="flex items-center">
                    <QuestionCircleOutlined className="mr-1" />
                    {t('knowledge.qaPairs.qaCount')}
                  </div>
                }
                rules={[
                  { required: true, message: t('common.required') },
                  { 
                    type: 'number', 
                    min: 1, 
                    max: 1000, 
                    message: t('knowledge.qaPairs.qaCountRange') 
                  }
                ]}
              >
                <InputNumber
                  min={1}
                  max={1000}
                  className="w-full"
                  size="large"
                  placeholder={t('knowledge.qaPairs.enterQaCount')}
                />
              </Form.Item>
            </Form>

            <div className="flex items-center">
              <Tag color="green" className="flex items-center">
                <span className="mr-1">{t('knowledge.qaPairs.selectedChunks')}:</span>
                <span className="font-semibold">{selectedChunks.length}</span>
              </Tag>
            </div>
          </div>
        </Spin>
      </OperateModal>
    );
  }
);

GenerateQAPairModal.displayName = 'GenerateQAPairModal';

export default GenerateQAPairModal;
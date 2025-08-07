import React, { useState, useEffect } from 'react';
import { Drawer, Button, Input, Popconfirm, message } from 'antd';
import { EditOutlined, CheckOutlined, DeleteOutlined } from '@ant-design/icons';
import { useTranslation } from '@/utils/i18n';

const { TextArea } = Input;

interface QADetailDrawerProps {
  visible: boolean;
  qaPair: {
    id: string;
    question: string;
    answer: string;
  } | null;
  onClose: () => void;
  onUpdate: (updatedQA: {
    id: string;
    question: string;
    answer: string;
  }) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
}

const QADetailDrawer: React.FC<QADetailDrawerProps> = ({
  visible,
  qaPair,
  onClose,
  onUpdate,
  onDelete,
}) => {
  const { t } = useTranslation();
  const [editingQuestion, setEditingQuestion] = useState(false);
  const [editingAnswer, setEditingAnswer] = useState(false);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [updateLoading, setUpdateLoading] = useState(false);
  const [deleteLoading, setDeleteLoading] = useState(false);

  useEffect(() => {
    if (visible && qaPair) {
      setQuestion(qaPair.question);
      setAnswer(qaPair.answer);
      setEditingQuestion(false);
      setEditingAnswer(false);
    }
  }, [visible, qaPair]);

  const handleQuestionEditToggle = () => {
    setEditingQuestion(!editingQuestion);
  };

  const handleAnswerEditToggle = () => {
    setEditingAnswer(!editingAnswer);
  };

  const handleQuestionUpdate = async () => {
    if (!qaPair) return;
    
    setUpdateLoading(true);
    try {
      await onUpdate({
        ...qaPair,
        question
      });
      message.success(t('common.updateSuccess'));
      setEditingQuestion(false);
    } catch (error) {
      console.error('Failed to update question:', error);
      message.error(t('common.updateFailed'));
    } finally {
      setUpdateLoading(false);
    }
  };

  const handleAnswerUpdate = async () => {
    if (!qaPair) return;
    
    setUpdateLoading(true);
    try {
      await onUpdate({
        ...qaPair,
        answer
      });
      message.success(t('common.updateSuccess'));
      setEditingAnswer(false);
    } catch (error) {
      console.error('Failed to update answer:', error);
      message.error(t('common.updateFailed'));
    } finally {
      setUpdateLoading(false);
    }
  };

  const handleDeleteConfirm = async () => {
    if (!qaPair) return;
    
    setDeleteLoading(true);
    try {
      await onDelete(qaPair.id);
      message.success(t('common.delSuccess'));
      onClose();
    } catch (error) {
      console.error('Failed to delete QA pair:', error);
      message.error(t('common.delFailed'));
    } finally {
      setDeleteLoading(false);
    }
  };

  if (!qaPair) return null;

  return (
    <Drawer
      title={t('knowledge.qaPairs.detail')}
      placement="right"
      width={600}
      open={visible}
      onClose={onClose}
      footer={
        <div className="flex justify-end space-x-2">
          <Popconfirm
            title={t('common.delConfirm')}
            onConfirm={handleDeleteConfirm}
            okText={t('common.yes')}
            cancelText={t('common.no')}
          >
            <Button
              danger
              icon={<DeleteOutlined />}
              loading={deleteLoading}
            >
              {t('common.delete')}
            </Button>
          </Popconfirm>
          <Button onClick={onClose}>
            {t('common.close')}
          </Button>
        </div>
      }
    >
      <div className="space-y-6">
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <h3 className="font-medium flex items-center">
              Q:
            </h3>
            <Button
              type="text"
              icon={editingQuestion ? <CheckOutlined /> : <EditOutlined />}
              onClick={editingQuestion ? handleQuestionUpdate : handleQuestionEditToggle}
              loading={updateLoading}
            >
            </Button>
          </div>
          
          {editingQuestion ? (
            <TextArea
              rows={4}
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              autoFocus
              placeholder={t('common.inputMsg') + t('knowledge.qaPairs.question')}
            />
          ) : (
            <div className="p-3 bg-gray-50 rounded-md min-h-[80px]">
              {question || '--'}
            </div>
          )}
        </div>

        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <h3 className="font-medium flex items-center">
              A:
            </h3>
            <Button
              type="text"
              icon={editingAnswer ? <CheckOutlined /> : <EditOutlined />}
              onClick={editingAnswer ? handleAnswerUpdate : handleAnswerEditToggle}
              loading={updateLoading}
            >
            </Button>
          </div>
          
          {editingAnswer ? (
            <TextArea
              rows={6}
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              autoFocus
              placeholder={t('common.inputMsg') + t('knowledge.qaPairs.answer')}
            />
          ) : (
            <div className="p-3 bg-gray-50 rounded-md min-h-[120px]">
              {answer || '--'}
            </div>
          )}
        </div>
      </div>
    </Drawer>
  );
};

export default QADetailDrawer;
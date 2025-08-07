import React, { useState, useEffect } from 'react';
import { Drawer, Button, Input, Popconfirm, message } from 'antd';
import { EditOutlined, CheckOutlined, DeleteOutlined, CloseOutlined } from '@ant-design/icons';
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
  const [originalQuestion, setOriginalQuestion] = useState('');
  const [originalAnswer, setOriginalAnswer] = useState('');
  const [updateLoading, setUpdateLoading] = useState(false);
  const [deleteLoading, setDeleteLoading] = useState(false);

  useEffect(() => {
    if (visible && qaPair) {
      setQuestion(qaPair.question);
      setAnswer(qaPair.answer);
      setOriginalQuestion(qaPair.question);
      setOriginalAnswer(qaPair.answer);
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

  const handleQuestionCancel = () => {
    setQuestion(originalQuestion);
    setEditingQuestion(false);
  };

  const handleAnswerCancel = () => {
    setAnswer(originalAnswer);
    setEditingAnswer(false);
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
      setOriginalQuestion(question);
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
      setOriginalAnswer(answer);
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
      title={t('common.viewDetails')}
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
            <div className="flex items-center gap-1">
              {editingQuestion ? (
                <>
                  <Button
                    type="text"
                    icon={<CheckOutlined />}
                    onClick={handleQuestionUpdate}
                    loading={updateLoading}
                    size="small"
                    className="text-green-600"
                  />
                  <Button
                    type="text"
                    icon={<CloseOutlined />}
                    onClick={handleQuestionCancel}
                    size="small"
                    className="text-red-500"
                  />
                </>
              ) : (
                <Button
                  type="text"
                  icon={<EditOutlined />}
                  onClick={handleQuestionEditToggle}
                  size="small"
                />
              )}
            </div>
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

        {/* 答案编辑区域 */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <h3 className="font-medium flex items-center">
              A:
            </h3>
            <div className="flex items-center gap-1">
              {editingAnswer ? (
                <>
                  <Button
                    type="text"
                    icon={<CheckOutlined />}
                    onClick={handleAnswerUpdate}
                    loading={updateLoading}
                    size="small"
                    className="text-green-600"
                  />
                  <Button
                    type="text"
                    icon={<CloseOutlined />}
                    onClick={handleAnswerCancel}
                    size="small"
                    className="text-red-500"
                  />
                </>
              ) : (
                <Button
                  type="text"
                  icon={<EditOutlined />}
                  onClick={handleAnswerEditToggle}
                  size="small"
                />
              )}
            </div>
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
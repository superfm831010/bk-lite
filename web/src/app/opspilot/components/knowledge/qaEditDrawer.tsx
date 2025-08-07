import React, { useEffect } from 'react';
import { 
  Form, 
  Input, 
  Button, 
  Drawer 
} from 'antd';
import { useTranslation } from '@/utils/i18n';

const { TextArea } = Input;

interface QAItem {
  question: string;
  answer: string;
}

interface QAEditDrawerProps {
  visible: boolean;
  onClose: () => void;
  onSubmit: (qaItem: QAItem) => Promise<void>;
  onSubmitAndContinue?: (qaItem: QAItem) => Promise<void>;
  title?: string;
  initialData?: QAItem;
  showContinueButton?: boolean;
  loading?: boolean;
}

const QAEditDrawer: React.FC<QAEditDrawerProps> = ({
  visible,
  onClose,
  onSubmit,
  onSubmitAndContinue,
  title,
  initialData,
  showContinueButton = false,
  loading = false
}) => {
  const { t } = useTranslation();
  const [form] = Form.useForm();

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      await onSubmit(values);
      form.resetFields();
      onClose();
    } catch (error) {
      console.error('Submit failed:', error);
    }
  };

  const handleSubmitAndContinue = async () => {
    if (!onSubmitAndContinue) return;
    
    try {
      const values = await form.validateFields();
      await onSubmitAndContinue(values);
      form.resetFields();
    } catch (error) {
      console.error('Submit and continue failed:', error);
    }
  };

  useEffect(() => {
    if (visible && initialData) {
      form.setFieldsValue(initialData);
    } else if (visible) {
      form.resetFields();
    }
  }, [visible, initialData, form]);

  return (
    <Drawer
      title={title || `${t('common.add')}${t('knowledge.qaPairs.title')}`}
      placement="right"
      width={500}
      open={visible}
      onClose={onClose}
      footer={
        <div className="flex justify-end space-x-2">
          <Button 
            onClick={onClose}
            disabled={loading}
          >
            {t('common.cancel')}
          </Button>
          <Button 
            type="primary" 
            onClick={handleSubmit}
            loading={loading}
          >
            {t('common.confirm')}
          </Button>
          {showContinueButton && onSubmitAndContinue && (
            <Button 
              type="primary" 
              onClick={handleSubmitAndContinue}
              loading={loading}
            >
              {t('knowledge.qaPairs.confirmAndAddNext')}
            </Button>
          )}
        </div>
      }
      maskClosable={!loading}
    >
      <Form 
        form={form} 
        layout="vertical"
        disabled={loading}
      >
        <Form.Item
          name="question"
          label={t('knowledge.qaPairs.question')}
          rules={[
            { required: true, message: t('common.required') }
          ]}
        >
          <TextArea
            rows={4}
            placeholder={t('common.inputMsg') + t('knowledge.qaPairs.question')}
          />
        </Form.Item>

        <Form.Item
          name="answer"
          label={t('knowledge.qaPairs.answer')}
          rules={[
            { required: true, message: t('common.required') }
          ]}
        >
          <TextArea
            rows={8}
            placeholder={t('common.inputMsg') + t('knowledge.qaPairs.answer')}
          />
        </Form.Item>
      </Form>
    </Drawer>
  );
};

export default QAEditDrawer;
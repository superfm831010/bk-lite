"use client";
import OperateModal from '@/components/operate-modal';
import { useState, useImperativeHandle, forwardRef } from 'react';
import { useTranslation } from '@/utils/i18n';
import useMlopsApi from '@/app/mlops/api';
import { Upload, Button, message, type UploadFile, type UploadProps } from 'antd';
import { InboxOutlined } from '@ant-design/icons';
import { ModalConfig, ModalRef, TableData, TrainDataParams } from '@/app/mlops/types';
const { Dragger } = Upload;

interface UploadModalProps {
  onSuccess: () => void
}

const UploadModal = forwardRef<ModalRef, UploadModalProps>(({ onSuccess }, ref) => {
  const { t } = useTranslation();
  const { addAnomalyTrainData } = useMlopsApi();
  const [visiable, setVisiable] = useState<boolean>(false);
  const [confirmLoading, setConfirmLoading] = useState<boolean>(false);
  const [fileList, setFileList] = useState<UploadFile<any>[]>([]);
  const [formData, setFormData] = useState<TableData>();

  useImperativeHandle(ref, () => ({
    showModal: ({ form }: ModalConfig) => {
      setVisiable(true);
      setFormData(form);
      console.log(form);
    }
  }));

  const handleChange: UploadProps['onChange'] = ({ fileList }) => {
    setFileList(fileList);
  };

  const props: UploadProps = {
    name: 'file',
    multiple: false,
    maxCount: 1,
    fileList: fileList,
    onChange: handleChange,
    beforeUpload: (file) => {
      const isCSV = file.type === "text/csv" || file.name.endsWith('.csv');
      if (!isCSV) {
        message.warning(t('datasets.uploadWarn'))
      }
      return isCSV;
    },
    accept: '.csv'
  };

  const handleFileRead = (text: string) => {
    // 统一换行符为 \n
    const lines = text.replace(/\r\n|\r|\n/g, '\n')?.split('\n').filter(line => line.trim() !== '');
    if (!lines.length) return [];
    const headers = ['timestamp', 'value'];
    const data = lines.slice(1).map(line => {
      const values = line.split(',');
      return headers.reduce((obj: Record<string, any>, key, idx) => {
        obj[key] = key === 'timestamp'
          ? new Date(values[idx]).getTime() / 1000
          : Number(values[idx]);
        return obj;
      }, {});
    });
    return data as TrainDataParams[];
  }

  const handleSubmit = async () => {
    setConfirmLoading(true);
    try {
      const file: UploadFile<any> = fileList[0];
      if (!file?.originFileObj) {
        setConfirmLoading(false);
        return message.error(t('datasets.pleaseUpload'));
      }
      const text = await file?.originFileObj.text();
      const data: TrainDataParams[] = handleFileRead(text);
      const params = {
        dataset: formData?.dataset_id,
        name:file.name,
        train_data: data,
        metadata: {},
        is_train_data: true,
        is_val_data: false,
        is_test_data: false,
      }
      await addAnomalyTrainData(params);
      setConfirmLoading(false);
      setVisiable(false);
      message.success(t('datasets.uploadSuccess'));
      onSuccess();
    } catch (e) {
      console.log(e)
    } finally {
      setConfirmLoading(false);
      setFileList([]);
    }
    // message.error(`${error.message}`);
  };

  const handleCancel = () => {
    setVisiable(false);
    setFileList([])
  };

  const downloadTemplate = async () => {
    // if (data) {
    //   const url = URL.createObjectURL(data);
    //   const a = document.createElement('a');
    //   a.href = url;
    //   a.download = 'template.csv';
    //   document.body.appendChild(a);
    //   a.click();
    //   document.body.removeChild(a);
    //   URL.revokeObjectURL(url);
    // } else {
    //   message.error(t('datasets.downloadError'));
    // }
    console.log('download');
  }

  return (
    <OperateModal
      title={t(`datasets.upload`)}
      open={visiable}
      onCancel={() => handleCancel()}
      footer={[
        <Button key="submit" loading={confirmLoading} type="primary" onClick={handleSubmit}>
          {t('common.confirm')}
        </Button>,
        <Button key="cancel" onClick={handleCancel}>
          {t('common.cancel')}
        </Button>,
      ]}
    >
      <Dragger {...props}>
        <p className="ant-upload-drag-icon">
          <InboxOutlined />
        </p>
        <p className="ant-upload-text">{t('datasets.uploadText')}</p>
      </Dragger>
      <p>{t('datasets.downloadText')}<Button type='link' onClick={downloadTemplate}>{t('datasets.template')}</Button></p>
    </OperateModal>
  )
});

UploadModal.displayName = 'UploadModal';
export default UploadModal;
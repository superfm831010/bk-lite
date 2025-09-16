"use client";
import OperateModal from '@/components/operate-modal';
import { useState, useImperativeHandle, forwardRef } from 'react';
import { useTranslation } from '@/utils/i18n';
import { exportToCSV } from '@/app/mlops/utils/common';
import useMlopsManageApi from '@/app/mlops/api/manage';
import { Upload, Button, message, Checkbox, type UploadFile, type UploadProps } from 'antd';
import { InboxOutlined } from '@ant-design/icons';
import { ModalConfig, ModalRef, TableData } from '@/app/mlops/types';
import { TrainDataParams } from '@/app/mlops/types/manage';
import { useSearchParams } from 'next/navigation';
const { Dragger } = Upload;

interface UploadModalProps {
  onSuccess: () => void
}

const UploadModal = forwardRef<ModalRef, UploadModalProps>(({ onSuccess }, ref) => {
  const { t } = useTranslation();
  const searchParams = useSearchParams();
  const activeType = searchParams.get('activeTap') || '';
  const { addAnomalyTrainData, addTimeSeriesPredictTrainData, addLogClusteringTrainData } = useMlopsManageApi();
  const [visiable, setVisiable] = useState<boolean>(false);
  const [confirmLoading, setConfirmLoading] = useState<boolean>(false);
  const [fileList, setFileList] = useState<UploadFile<any>[]>([]);
  const [checkedType, setCheckedType] = useState<string[]>([]);
  const [selectTags, setSelectTags] = useState<{
    [key: string]: boolean
  }>({});
  const [formData, setFormData] = useState<TableData>();

  useImperativeHandle(ref, () => ({
    showModal: ({ form }: ModalConfig) => {
      setVisiable(true);
      setFormData(form);
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
      if (activeType !== 'log_clustering') {
        const isCSV = file.type === "text/csv" || file.name.endsWith('.csv');
        if (!isCSV) {
          message.warning(t('datasets.uploadWarn'))
        }
        return isCSV;
      } else {
        const isTxt = file.type === 'text/plain' || file.name.endsWith('.txt');
        if (!isTxt) {
          message.warning(t('datasets.uploadWarn'))
        }
        return isTxt;
      }

    },
    accept: activeType !== 'log_clustering' ? '.csv' : '.txt'
  };

  const handleFileRead = (text: string, type: string) => {
    // 统一换行符为 \n
    const lines = text.replace(/\r\n|\r|\n/g, '\n')?.split('\n').filter(line => line.trim() !== '');
    if (!lines.length) return [];
    if (type !== 'log_clustering') {
      const headers = type === 'anomaly' ? ['timestamp', 'value', 'label'] : lines[0]?.split(',');
      const data = lines.slice(1).map((line, index) => {
        const values = line.split(',');
        return headers.reduce((obj: Record<string, any>, key, idx) => {
          obj[key] = key === 'timestamp'
            ? new Date(values[idx]).getTime() / 1000
            : Number(values[idx]);
          obj['index'] = index;
          return obj;
        }, {});
      });
      return data as TrainDataParams[];
    }
    return lines;
  };

  const onSelectChange = (value: string[]) => {
    setCheckedType(value);
    const object = value.reduce((prev: object, current: string) => {
      return {
        ...prev,
        [current]: true
      };
    }, {});
    setSelectTags(object);
  };

  const handleSubmit = async () => {
    setConfirmLoading(true);
    try {
      const file: UploadFile<any> = fileList[0];
      if (!file?.originFileObj) {
        setConfirmLoading(false);
        return message.error(t('datasets.pleaseUpload'));
      }
      if (formData?.activeTap === 'anomaly') {
        const text = await file?.originFileObj.text();
        const data: TrainDataParams[] = handleFileRead(text, formData?.activeTap) as TrainDataParams[];
        const train_data = data.map(item => ({ timestamp: item.timestamp, value: item.value }));
        const points = data.filter(item => item?.label === 1).map(k => k.index);
        const params = {
          dataset: formData?.dataset_id,
          name: file.name,
          train_data: train_data,
          metadata: {
            anomaly_point: points
          },
          ...selectTags
        };
        await addAnomalyTrainData(params);
        setConfirmLoading(false);
        setVisiable(false);
        message.success(t('datasets.uploadSuccess'));
        onSuccess();
      } else if (formData?.activeTap === 'timeseries_predict') {
        const text = await file?.originFileObj.text();
        const data: TrainDataParams[] = handleFileRead(text, formData?.activeTap) as TrainDataParams[];
        const params = {
          dataset: formData?.dataset_id,
          name: file.name,
          train_data: data,
          ...selectTags
        };
        await addTimeSeriesPredictTrainData(params);
        setConfirmLoading(false);
        setVisiable(false);
        message.success(t('datasets.uploadSuccess'));
        onSuccess();
      } else {
        const text = await file?.originFileObj.text();
        const data: string[] = handleFileRead(text, formData?.activeTap) as string[];
        const params = {
          dataset: formData?.dataset_id,
          name: file.name,
          train_data: data,
          ...selectTags
        };
        await addLogClusteringTrainData(params);
        setConfirmLoading(false);
        setVisiable(false);
        message.success(t('datasets.uploadSuccess'));
        onSuccess();
      }
    } catch (e) {
      console.log(e);
    } finally {
      setConfirmLoading(false);
      setFileList([]);
    }
  };

  const handleCancel = () => {
    setVisiable(false);
    setFileList([]);
    setCheckedType([]);
  };

  const downloadTemplate = async () => {
    const data = [
      {
        "value": 27.43789942218143,
        "timestamp": 1704038400
      },
      {
        "value": 26.033612999373652,
        "timestamp": 1704038460
      },
      {
        "value": 36.30777324191053,
        "timestamp": 1704038520
      },
      {
        "value": 33.70226097527219,
        "timestamp": 1704038580
      }
    ];
    const columns = [
      {
        title: t('common.time'),
        key: 'timestamp',
        dataIndex: 'timestamp',
        width: 80,
        align: 'center',
      },
      {
        title: t('datasets.value'),
        key: 'value',
        dataIndex: 'value',
        align: 'center',
        width: 30,
      },
    ]
    const blob = exportToCSV(data, columns);
    if (blob) {
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'template.csv';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } else {
      message.error(t('datasets.downloadError'));
    }
  };

  const CheckedType = () => (
    <div className='text-left flex justify-between items-center'>
      <div className='flex-1'>
        <span className='leading-[32px] mr-2'>{t(`mlops-common.type`) + ": "} </span>
        <Checkbox.Group onChange={onSelectChange} value={checkedType}>
          <Checkbox value={'is_train_data'}>{t(`datasets.train`)}</Checkbox>
          <Checkbox value={'is_val_data'}>{t(`datasets.validate`)}</Checkbox>
          <Checkbox value={'is_test_data'}>{t(`datasets.test`)}</Checkbox>
        </Checkbox.Group>
      </div>
      <Button key="submit" className='mr-2' loading={confirmLoading} type="primary" onClick={handleSubmit}>
        {t('common.confirm')}
      </Button>
      <Button key="cancel" onClick={handleCancel}>
        {t('common.cancel')}
      </Button>
    </div>
  );

  return (
    <OperateModal
      title={t(`datasets.upload`)}
      open={visiable}
      onCancel={() => handleCancel()}
      footer={[
        <CheckedType key="checked" />,
      ]}
    >
      <Dragger {...props}>
        <p className="ant-upload-drag-icon">
          <InboxOutlined />
        </p>
        <p className="ant-upload-text">{t('datasets.uploadText')}</p>
      </Dragger>
      <p>{t(`datasets.${activeType !== 'log_clustering' ? 'downloadCSV' : 'downloadTxt'}`)}<Button type='link' onClick={downloadTemplate}>{t('datasets.template')}</Button></p>
    </OperateModal>
  )
});

UploadModal.displayName = 'UploadModal';
export default UploadModal;
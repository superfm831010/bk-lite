"use client";
import OperateModal from '@/components/operate-modal';
import { Form, Input, Button, Select, FormInstance, message } from 'antd';
import { useState, useImperativeHandle, useEffect, useRef, useCallback, forwardRef } from 'react';
import { useTranslation } from '@/utils/i18n';
import { DataSet, ModalRef, Option, TrainJob, TrainTaskModalProps, AlgorithmParam } from '@/app/mlops/types';

const algorithmsParam: AlgorithmParam[] = [
  { name: 'n_estimators', type: 'value', default: 100 },
  { name: 'max_samples', type: 'value', default: 'auto' },
  { name: 'contamination', type: 'value', default: 'auto' },
  { name: 'max_features', type: 'value', default: 1.0 },
  { name: 'bootstrap', type: 'enum', default: 'False' },
  { name: 'n_jobs', type: 'value', default: 'None', },
  { name: 'random_state', type: 'value', default: 'None' },
  { name: 'verbose', type: 'value', default: 0 },
  { name: 'warm_start', type: 'enum', default: 'False' }
];

const TrainTaskModal = forwardRef<ModalRef, TrainTaskModalProps>(({ onSuccess, datasets, trainData }, ref) => {
  const { t } = useTranslation();
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [type, setType] = useState<string>('add');
  const [title, setTitle] = useState<string>('addtask');
  const [datasetItems, setDatasetItems] = useState<Option[]>([]);
  const [formData, setFormData] = useState<TrainJob | null>(null);
  const [confirmLoading, setConfirmLoading] = useState<boolean>(false);
  const [selectLoading, setSelectLoading] = useState<boolean>(false);
  const [traindataOption, setTrainDataOption] = useState<Option[]>([]);
  const [isShow, setIsShow] = useState<boolean>(false);
  const [showParams, setShowParams] = useState<boolean>(false);
  const formRef = useRef<FormInstance>(null);

  useImperativeHandle(ref, () => ({
    showModal: ({ type, title, form }) => {
      const items = datasets.map((item: DataSet) => {
        return {
          value: item.id,
          label: item.name
        }
      }) || [];
      console.log(form);
      setSelectLoading(false);
      setType(type);
      setTitle(title as string);
      setFormData(form);
      setDatasetItems(items as Option[]);
      setIsModalOpen(true);
    }
  }));

  useEffect(() => {
    if (isModalOpen) {
      initializeForm();
    }
  }, [isModalOpen]);

  const initializeForm = useCallback(() => {
    const defaultParams: Record<string, any> = {};
    algorithmsParam.forEach(item => {
      defaultParams[item.name] = item.default;
    });
    if (!formRef.current) return;
    formRef.current.resetFields();

    if (type === 'add') {
      formRef.current.setFieldsValue({});
    } else if (formData) {
      setIsShow(true);
      renderFileOption(formData.dataset_id);
      formRef.current.setFieldsValue({
        name: formData.name,
        type: formData.type,
        dataset_id: formData.dataset_id,
        train_data_id: formData.train_data_id,
        params: defaultParams
      });
    }
  }, [type, formData]);

  const renderFileOption = useCallback((data: number) => {
    if (!formRef.current) return;
    const option: Option[] = trainData
      .filter((item: any) => item.dataset_id === data)
      .map((item: any) => ({
        label: item?.name,
        value: item?.id
      }));
    setTrainDataOption(option);
  }, [trainData]);

  const renderItem = useCallback((param: AlgorithmParam[]) => {
    return param.map((item) => (
      <Form.Item key={item.name} name={['params', item.name]} label={item.name} rules={[{ required: true, message: t('common.inputMsg') }]}>
        {item.type === 'value' ? <Input /> :
          <Select
            options={[
              { value: 'False', label: 'False' },
              { value: 'True', label: 'True' },
            ]}
          />
        }
      </Form.Item>
    ))
  }, [t]);

  const onTypeChange = () => {
    if (!formRef.current) return;
    setIsShow(true);
  }

  const handleSubmit = useCallback(async () => {
    if (confirmLoading) return;
    setConfirmLoading(true);
    try {
      const value = await formRef.current?.validateFields();
      let result = value;
      if (type === 'add') {
        result = [];
      } else {
        result = [];
      }
      if (result.error) {
        message.error(result.error.message);
        return;
      }
      setIsModalOpen(false);
      message.success(`datasets.${type}Success`)
      onSuccess();
    } catch (e) {
      console.log(e);
    } finally {
      setConfirmLoading(false);
    }
  }, [type, formData, onSuccess]);

  const handleCancel = () => {
    setIsModalOpen(false);
    formRef.current?.resetFields();
    setShowParams(false);
    setIsShow(false);
  };

  return (
    <>
      <OperateModal
        title={t(`traintask.${title}`)}
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        footer={[
          <Button key="submit" loading={confirmLoading} type="primary" onClick={handleSubmit}>
            {t('common.confirm')}
          </Button>,
          <Button key="cancel" onClick={handleCancel}>
            {t('common.cancel')}
          </Button>,
        ]}
      >
        <Form
          ref={formRef}
          layout="vertical"
        >
          <Form.Item
            name='name'
            label={t('common.name')}
            rules={[{ required: true, message: t('common.inputMsg') }]}
          >
            <Input placeholder={t('common.inputMsg')} />
          </Form.Item>
          <Form.Item
            name='type'
            label={t('common.type')}
            rules={[{ required: true, message: t('common.inputMsg') }]}
          >
            <Select placeholder={t('common.inputMsg')} onChange={onTypeChange} options={[
              { value: 'anomaly', label: t('datasets.anomaly') },
            ]} />
          </Form.Item>
          {isShow && (<>
            <Form.Item
              name='dataset_id'
              label={t('traintask.datasets')}
              rules={[{ required: true, message: t('traintask.selectDatasets') }]}
            >
              <Select placeholder={t('traintask.selectDatasets')} options={datasetItems} onChange={renderFileOption} />
            </Form.Item>
            <Form.Item
              name='train_data_id'
              label={t('traintask.trainfile')}
              rules={[{ required: true, message: t('common.inputMsg') }]}
            >
              <Select placeholder={t('common.inputMsg')} loading={selectLoading} options={traindataOption} />
            </Form.Item>
            <Form.Item
              name='algorithms'
              label={t('traintask.algorithms')}
              rules={[{ required: true, message: t('common.inputMsg') }]}
            >
              <Select placeholder={t('common.inputMsg')} onChange={() => { setShowParams(true) }} options={[
                { value: 'isolationForst', label: `IsolationForst` },
              ]} />
            </Form.Item>
            {showParams && renderItem(algorithmsParam)}
          </>)}
        </Form>
      </OperateModal>
    </>
  );
});

TrainTaskModal.displayName = 'TrainTaskModal';
export default TrainTaskModal;
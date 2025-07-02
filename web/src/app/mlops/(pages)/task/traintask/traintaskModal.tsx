"use client";
import OperateModal from '@/components/operate-modal';
import { Form, Input, Button, Select, FormInstance, message, Divider, InputNumber } from 'antd';
import { useState, useImperativeHandle, useEffect, useRef, useCallback, forwardRef } from 'react';
import { useTranslation } from '@/utils/i18n';
import useMlopsApi from '@/app/mlops/api';
import { DataSet, ModalRef, Option, TrainJob, TrainTaskModalProps, AlgorithmParam, TrainData } from '@/app/mlops/types';
import RangeInput from '@/app/mlops/components/RangeInput';
import { AlgorithmsParams, AlgorithmsType } from '@/app/mlops/constants';
import { JointContent } from 'antd/es/message/interface';

const TrainTaskModal = forwardRef<ModalRef, TrainTaskModalProps>(({ onSuccess }, ref) => {
  const { t } = useTranslation();
  const { addAnomalyTrainTask, getAnomalyTrainData, getAnomalyDatasetsList, updateAnomalyTrainTask, getAnomalyTrainDataInfo } = useMlopsApi();
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [type, setType] = useState<string>('add');
  const [title, setTitle] = useState<string>('addtask');
  const [datasetItems, setDatasetItems] = useState<Option[]>([]);
  const [formData, setFormData] = useState<TrainJob | null>(null);
  const [confirmLoading, setConfirmLoading] = useState<boolean>(false);
  const [datasetLoading, setDatasetLoading] = useState<boolean>(false);
  const [selectLoading, setSelectLoading] = useState<boolean>(false);
  const [traindataOption, setTrainDataOption] = useState<{
    trainOption: Option[],
    valOption: Option[],
    testOption: Option[],
  }>({
    trainOption: [],
    valOption: [],
    testOption: []
  });
  const [isShow, setIsShow] = useState<boolean>(false);
  const [showParams, setShowParams] = useState<boolean>(false);
  const formRef = useRef<FormInstance>(null);

  useImperativeHandle(ref, () => ({
    showModal: ({ type, title, form }) => {
      console.log(form)
      getDataSets();
      setSelectLoading(false);
      setType(type);
      setTitle(title as string);
      setFormData(form);
      setIsModalOpen(true);
    }
  }));

  useEffect(() => {
    if (isModalOpen) {
      initializeForm();
    }
  }, [isModalOpen]);

  const getDataSets = async () => {
    setDatasetLoading(true);
    try {
      const data = await getAnomalyDatasetsList({});
      const items = data.map((item: DataSet) => {
        return {
          value: item.id,
          label: item.name
        }
      }) || [];
      setDatasetItems(items);
    } catch (e) {
      console.log(e);
    } finally {
      setDatasetLoading(false);
    }
  };

  const initializeForm = useCallback(async () => {
    const defaultParams: Record<string, any> = {};

    AlgorithmsParams['RandomForest'].forEach(item => {
      defaultParams[item.name] = item.default;
    });

    if (!formRef.current) return;
    formRef.current.resetFields();

    if (type === 'add') {
      formRef.current.setFieldsValue({
        hyperopt_config: defaultParams
      });
    } else if (formData) {
      const dataset = await searchDatasetId(formData.train_data_id as number);
      const hyperopt_config = hyperoptConversion(formData.hyperopt_config);
      setIsShow(true);
      setShowParams(true);
      renderFileOption(dataset);
      formRef.current.setFieldsValue({
        name: formData.name,
        type: formData.type,
        dataset_id: dataset,
        max_evals: formData.max_evals,
        algorithm: formData.algorithm,
        train_data_id: formData.train_data_id,
        val_data_id: formData.val_data_id,
        test_data_id: formData.test_data_id,
        hyperopt_config
      });
    }
  }, [type, formData]);

  const searchDatasetId = async (traindataId: number) => {
    if (!traindataId) return;
    const { dataset } = await getAnomalyTrainDataInfo(traindataId, false, false);
    return dataset || null;
  };

  const hyperoptConversion = (params: object) => {
    if (!params) return;
    const hyperopt_config: Record<string, any> = {};
    Object.entries(params).forEach(([key, value]) => {
      if (value?.type === 'randint') {
        hyperopt_config[key] = [value?.min, value?.max];
      } else if (value?.type === 'choice') {
        hyperopt_config[key] = value?.choice[0];
      }
    });

    return hyperopt_config;
  };

  const renderFileOption = useCallback(async (data: number) => {
    if (!formRef.current || !data) return;
    const param = { dataset: data };
    setSelectLoading(true);
    try {
      formRef.current.resetFields(['train_data_id', 'val_data_id', 'test_data_id']);
      const trainData = await getAnomalyTrainData(param);
      const options = {
        trainOption: trainData.filter((item: TrainData) => item.is_train_data).map((item: TrainData) => ({ label: item.name, value: item.id })),
        valOption: trainData.filter((item: TrainData) => item.is_val_data).map((item: TrainData) => ({ label: item.name, value: item.id })),
        testOption: trainData.filter((item: TrainData) => item.is_test_data).map((item: TrainData) => ({ label: item.name, value: item.id })),
      };
      setTrainDataOption(options);
    } catch (e) {
      message.error(e as JointContent)
    } finally {
      setSelectLoading(false);
    }
  }, [datasetItems]);

  const renderItem = useCallback((param: AlgorithmParam[]) => {
    return param.map((item) => (
      <Form.Item key={item.name} name={['hyperopt_config', item.name]} label={item.name} rules={[{ required: true, message: t('common.inputMsg') }]}>
        {item.type === 'randint' ?
          <RangeInput className='ml-2' value={item.default as [number, number]} /> :
          <Select className='ml-2' options={item.options} />
        }
      </Form.Item>
    ))
  }, [t]);

  const onTypeChange = () => {
    if (!formRef.current) return;
    setIsShow(true);
    setShowParams(true);
  };

  const renderParams = (object: Record<string, any>) => {
    const hyperopt_config: Record<string, any> = {};
    Object.keys(object).forEach((item: string) => {
      if (AlgorithmsType['RandomForest'][item] == 'randint') {
        hyperopt_config[item] = {
          type: 'randint',
          min: object[item][0],
          max: object[item][1]
        }
      } else if (AlgorithmsType['RandomForest'][item] == 'choice') {
        hyperopt_config[item] = {
          type: 'choice',
          choice: [object[item]]
        }
      }
    });
    return hyperopt_config;
  };

  const handleSubmit = useCallback(async () => {
    if (confirmLoading) return;
    setConfirmLoading(true);
    try {
      const value = await formRef.current?.validateFields();
      const hyperopt_config = renderParams(value?.hyperopt_config);
      const params = {
        ...value,
        status: 'pending',
        hyperopt_config,
        description: value.name || ''
      };
      if (type === 'add') {
        console.log(params);
        await addAnomalyTrainTask(params);
      } else {
        await updateAnomalyTrainTask(formData?.id as string, value)
      }
      setIsModalOpen(false);
      message.success(t(`datasets.${type}Success`));
      onSuccess();
    } catch (e) {
      console.log(e);
      message.error('error');
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
          {/* <Form.Item
            name='type'
            label={t('common.type')}
            rules={[{ required: true, message: t('common.inputMsg') }]}
          >
            <Select placeholder={t('common.inputMsg')} onChange={onTypeChange} options={[
              { value: 'anomaly', label: t('datasets.anomaly') },
            ]} />
          </Form.Item> */}
          <Form.Item
            name='algorithm'
            label={t('traintask.algorithms')}
            rules={[{ required: true, message: t('common.inputMsg') }]}
          >
            <Select placeholder={t('common.inputMsg')} onChange={onTypeChange} options={[
              { value: 'RandomForest', label: `RandomForest` },
            ]} />
          </Form.Item>
          <Form.Item
            name='max_evals'
            label={t('traintask.maxEvals')}
            rules={[{ required: true, message: t('common.inputMsg') }]}
          >
            <InputNumber style={{ width: '100%' }} placeholder={t('common.inputMsg')} />
          </Form.Item>
          <Form.Item
            name='dataset_id'
            label={t('traintask.datasets')}
            rules={[{ required: true, message: t('traintask.selectDatasets') }]}
          >
            <Select placeholder={t('traintask.selectDatasets')} loading={datasetLoading} options={datasetItems} onChange={renderFileOption} />
          </Form.Item>
          {isShow && (<>
            <Divider orientation='start' orientationMargin={'0'} plain style={{ borderColor: '#d1d5db' }}>训练文件</Divider>
            <Form.Item
              name='train_data_id'
              className='ml-2'
              label={t('datasets.train')}
              rules={[{ required: true, message: t('common.inputMsg') }]}
            >
              <Select placeholder={t('common.inputMsg')} loading={selectLoading} options={traindataOption.trainOption} />
            </Form.Item>
            <Form.Item
              name='val_data_id'
              className='ml-2'
              label={t('datasets.validate')}
              rules={[{ required: true, message: t('common.inputMsg') }]}
            >
              <Select placeholder={t('common.inputMsg')} loading={selectLoading} options={traindataOption.valOption} />
            </Form.Item>
            <Form.Item
              name='test_data_id'
              className='ml-2'
              label={t('datasets.test')}
              rules={[{ required: true, message: t('common.inputMsg') }]}
            >
              <Select placeholder={t('common.inputMsg')} loading={selectLoading} options={traindataOption.testOption} />
            </Form.Item>
            {
              showParams && (
                <>
                  <Divider orientation='start' orientationMargin={'0'} plain style={{ borderColor: '#d1d5db' }}>超参数</Divider>
                  {renderItem(AlgorithmsParams['RandomForest'])}
                </>
              )
            }
          </>)}
        </Form>
      </OperateModal>
    </>
  );
});

TrainTaskModal.displayName = 'TrainTaskModal';
export default TrainTaskModal;
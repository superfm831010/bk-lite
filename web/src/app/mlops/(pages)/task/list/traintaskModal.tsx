"use client";
import OperateModal from '@/components/operate-modal';
import {
  Form,
  Input,
  Button,
  Select,
  FormInstance,
  message,
  Divider,
  InputNumber
} from 'antd';
import {
  useState,
  useImperativeHandle,
  useEffect,
  useRef,
  useCallback,
  forwardRef
} from 'react';
import { useTranslation } from '@/utils/i18n';
import useMlopsTaskApi from '@/app/mlops/api/task';
import useTrainDataLoader from '@/app/mlops/hooks/task/useTrainDataLoader';
import useParamsUtil from '@/app/mlops/hooks/task/useParamsUtil';
import { ModalRef, Option } from '@/app/mlops/types';
import { TrainJob, TrainTaskModalProps, AlgorithmParam } from '@/app/mlops/types/task';
import RangeInput from '@/app/mlops/components/range-input';
import { ALGORITHMS_PARAMS } from '@/app/mlops/constants';

interface ModalState {
  isOpen: boolean;
  type: string;
  title: string;
}

const TrainTaskModal = forwardRef<ModalRef, TrainTaskModalProps>(({ datasetOptions, activeTag, onSuccess }, ref) => {
  const { t } = useTranslation();
  const { addAnomalyTrainTask, updateAnomalyTrainTask } = useMlopsTaskApi();
  const { loadTrainOptions, getDatasetByTrainId } = useTrainDataLoader();
  const { hyperoptConversion, renderParams } = useParamsUtil();
  const [modalState, setModalState] = useState<ModalState>({
    isOpen: false,
    type: 'add',
    title: 'addtask',
  });
  const [formData, setFormData] = useState<TrainJob | null>(null);
  const [loadingState, setLoadingState] = useState<{
    confirm: boolean,
    dataset: boolean,
    select: boolean
  }>({
    confirm: false,
    dataset: false,
    select: false
  })
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
  const formRef = useRef<FormInstance>(null);

  useImperativeHandle(ref, () => ({
    showModal: ({ type, title, form }) => {
      setLoadingState((prev) => ({ ...prev, select: false }));
      setFormData(form);
      setModalState({
        isOpen: true,
        type,
        title: title as string,
      })
    }
  }));

  useEffect(() => {
    if (formData && modalState.isOpen) {
      initializeForm(formData);
    }
  }, [modalState.isOpen, formData]);


  const initializeForm = useCallback(async (formData: TrainJob) => {
    const defaultParams: Record<string, any> = {};
    ALGORITHMS_PARAMS['RandomForest'].forEach(item => {
      defaultParams[item.name] = item.default;
    });

    if (!formRef.current) return;
    formRef.current.resetFields();

    if (modalState.type === 'add') {
      formRef.current.setFieldsValue({
        hyperopt_config: defaultParams
      });
    } else if (formData) {
      const immediateData = {
        name: formData.name,
        type: formData.type,
        max_evals: formData.max_evals,
        algorithm: formData.algorithm,
        hyperopt_config: hyperoptConversion(formData.hyperopt_config)
      };

      formRef.current.setFieldsValue(immediateData);
      setIsShow(true);
      handleAsyncDataLoading(formData.train_data_id as number, formData);
    }
  }, [modalState.type]);

  const handleAsyncDataLoading = useCallback(async (trainDataId: number, formData: TrainJob) => {
    if (!trainDataId) return;

    setLoadingState((prev) => ({ ...prev, select: true }));

    try {
      const dataset = await getDatasetByTrainId(formData.train_data_id as number);

      if (dataset && formRef.current) {
        formRef.current.setFieldsValue({
          dataset_id: dataset
        });

        await renderOptions(dataset);
      }
    } catch (e) {
      console.log(e);
    } finally {
      setLoadingState(prev => ({ ...prev, select: false }));
    }
  }, [getDatasetByTrainId, loadTrainOptions]);

  // 渲染文件选项
  const renderOptions = useCallback(async (dataset: number) => {
    if(!formRef.current || !dataset) return;
    // 加载训练数据选项
    const trainOptions = await loadTrainOptions(dataset);
    setTrainDataOption(trainOptions);
    formRef.current.setFieldsValue({
      train_data_id: formData?.train_data_id,
      val_data_id: formData?.val_data_id,
      test_data_id: formData?.test_data_id,
    });
  }, [loadTrainOptions]);

  // 渲染超参数表单项
  const renderItem = useCallback((param: AlgorithmParam[]) => {
    return param.map((item) => (
      <Form.Item key={item.name} name={['hyperopt_config', item.name]} label={item.name} rules={[{ required: true, message: t('common.inputMsg') }]}>
        {item.type === 'randint' ?
          <RangeInput className='ml-2' value={item.default as [number, number]} /> :
          <Select className='ml-2' mode="multiple" options={item.options} />
        }
      </Form.Item>
    ))
  }, [t]);

  // 算法变化
  const onTypeChange = () => {
    if (!formRef.current) return;
    setIsShow(true);
  };

  const handleAddMap: Record<string, any> = {
    'anomaly': async (params: any) => {
      await addAnomalyTrainTask(params);
    }
  };

  const handleUpdateMap: Record<string, any> = {
    'anomaly': async (id: string, params: any) => {
      await updateAnomalyTrainTask(id, params);
    }
  };

  const handleSubmit = useCallback(async () => {
    if (loadingState.confirm) return;
    setLoadingState((prev) => ({ ...prev, confirm: true }));
    try {
      const [tagName] = activeTag;
      const value = await formRef.current?.validateFields();
      const hyperopt_config = renderParams(value?.hyperopt_config);
      const params = {
        ...value,
        status: 'pending',
        hyperopt_config,
        description: value.name || ''
      };
      if (modalState.type === 'add') {
        await handleAddMap[tagName](params);
      } else {
        await handleUpdateMap[tagName](formData?.id as string, params)
      }
      setModalState((prev) => ({ ...prev, isOpen: false }));
      message.success(t(`datasets.${modalState.type}Success`));
      onSuccess();
    } catch (e) {
      console.log(e);
      message.error(t(`common.${modalState.type}Failed`));
    } finally {
      setLoadingState((prev) => ({ ...prev, confirm: false }));
    }
  }, [modalState.type, formData, onSuccess]);

  const handleCancel = () => {
    setModalState((prev) => ({
      ...prev,
      isOpen: false
    }))
    formRef.current?.resetFields();
    setTrainDataOption({
      trainOption: [],
      valOption: [],
      testOption: []
    });
    setIsShow(false);
  };

  return (
    <>
      <OperateModal
        title={t(`traintask.${modalState.title}`)}
        open={modalState.isOpen}
        onCancel={handleCancel}
        footer={[
          <Button key="submit" loading={loadingState.confirm} type="primary" onClick={handleSubmit}>
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
            name='algorithm'
            label={t('traintask.algorithms')}
            rules={[{ required: true, message: t('common.inputMsg') }]}
          >
            <Select placeholder={t('traintask.selectAlgorithmsMsg')} onChange={onTypeChange} options={[
              { value: 'RandomForest', label: `RandomForest` },
            ]} />
          </Form.Item>
          <Form.Item
            name='max_evals'
            label={t('traintask.maxEvals')}
            rules={[{ required: true, message: t('common.inputMsg') }]}
          >
            <InputNumber style={{ width: '100%' }} placeholder={t('traintask.maxEvalsMsg')} />
          </Form.Item>
          <Form.Item
            name='dataset_id'
            label={t('traintask.datasets')}
            rules={[{ required: true, message: t('traintask.selectDatasets') }]}
          >
            <Select placeholder={t('traintask.selectDatasets')} loading={loadingState.select} options={datasetOptions} onChange={renderOptions} />
          </Form.Item>
          {isShow && (<>
            <Divider orientation='start' orientationMargin={'0'} plain style={{ borderColor: '#d1d5db' }}>{t(`traintask.trainfile`)}</Divider>
            <Form.Item
              name='train_data_id'
              className='ml-2'
              label={t('datasets.train')}
              rules={[{ required: true, message: t('common.selectMsg') }]}
            >
              <Select placeholder={t('common.selectMsg')} loading={loadingState.select} options={traindataOption.trainOption} />
            </Form.Item>
            <Form.Item
              name='val_data_id'
              className='ml-2'
              label={t('datasets.validate')}
              rules={[{ required: true, message: t('common.selectMsg') }]}
            >
              <Select placeholder={t('common.selectMsg')} loading={loadingState.select} options={traindataOption.valOption} />
            </Form.Item>
            <Form.Item
              name='test_data_id'
              className='ml-2'
              label={t('datasets.test')}
              rules={[{ required: true, message: t('common.selectMsg') }]}
            >
              <Select placeholder={t('common.selectMsg')} loading={loadingState.select} options={traindataOption.testOption} />
            </Form.Item>
            {
              <>
                <Divider orientation='start' orientationMargin={'0'} plain style={{ borderColor: '#d1d5db' }}>{t(`traintask.hyperopt`)}</Divider>
                {renderItem(ALGORITHMS_PARAMS['RandomForest'])}
              </>
            }
          </>)}
        </Form>
      </OperateModal>
    </>
  );
});

TrainTaskModal.displayName = 'TrainTaskModal';
export default TrainTaskModal;
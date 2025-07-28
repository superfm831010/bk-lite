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
import useMlopsManageApi from '@/app/mlops/api/manage';
import { ModalRef, Option } from '@/app/mlops/types';
import { TrainData } from '@/app/mlops/types/manage';
import { TrainJob, TrainTaskModalProps, AlgorithmParam } from '@/app/mlops/types/task';
import RangeInput from '@/app/mlops/components/range-input';
import { ALGORITHMS_PARAMS, ALGORITHMS_TYPE } from '@/app/mlops/constants';
import { JointContent } from 'antd/es/message/interface';

interface ModalState {
  isOpen: boolean;
  type: string;
  title: string;
  formData: TrainJob | null
}

const TrainTaskModal = forwardRef<ModalRef, TrainTaskModalProps>(({ datasetOptions, activeTag, onSuccess }, ref) => {
  const { t } = useTranslation();
  const { addAnomalyTrainTask, updateAnomalyTrainTask } = useMlopsTaskApi();
  const { getAnomalyTrainData, getAnomalyTrainDataInfo } = useMlopsManageApi();
  const [modalState, setModalState] = useState<ModalState>({
    isOpen: false,
    type: 'add',
    title: 'addtask',
    formData: null
  });
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
      console.log(form)
      setLoadingState((prev) => ({ ...prev, select: false }))
      setModalState({
        isOpen: true,
        type,
        title: title as string,
        formData: form
      })
    }
  }));

  useEffect(() => {
    if (modalState.isOpen) {
      initializeForm();
    }
  }, [modalState.isOpen]);


  const initializeForm = useCallback(async () => {
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
    } else if (modalState.formData) {
      const { formData } = modalState;

      const immediateData = {
        name: formData.name,
        type: formData.type,
        max_evals: formData.max_evals,
        algorithm: formData.algorithm,
        hyperopt_config: hyperoptConversion(formData.hyperopt_config)
      };

      formRef.current.setFieldsValue(immediateData);
      setIsShow(true);
      handleAsyncDataLoading(formData.train_data_id as number);
    }
  }, [modalState.type, modalState.formData]);

  const handleAsyncDataLoading = useCallback(async (trainDataId: number) => {
    if (!trainDataId) return;

    setLoadingState((prev) => ({ ...prev, select: true }));

    try {
      // 获取数据集ID
      const dataset = await searchDatasetId(trainDataId);

      if (dataset && formRef.current) {
        formRef.current.setFieldsValue({
          dataset_id: dataset
        });

        // 加载训练数据选项
        await renderFileOption(dataset);
      }
    } catch (e) {
      console.log(e);
    } finally {
      setLoadingState(prev => ({ ...prev, select: false }));
    }
  }, [])

  const searchDatasetId = useCallback(async (traindataId: number) => {
    if (!formRef.current || !traindataId) return;

    setLoadingState((prev) => ({ ...prev, select: true }));
    try {
      const { dataset } = await getAnomalyTrainDataInfo(traindataId, false, false);
      return dataset || null;
    } catch (e) {
      console.log(e);
      return null;
    }
  }, [getAnomalyTrainDataInfo]);

  // 生成训练文件选项
  const renderFileOption = useCallback(async (data: number) => {
    if (!formRef.current || !data) return;
    const param = { dataset: data };
    const { formData } = modalState;
    setLoadingState(prev => ({ ...prev, select: true }));
    try {
      const trainData = await getAnomalyTrainData(param);
      const options = {
        trainOption: trainData.filter((item: TrainData) => item.is_train_data).map((item: TrainData) => ({ label: item.name, value: item.id })),
        valOption: trainData.filter((item: TrainData) => item.is_val_data).map((item: TrainData) => ({ label: item.name, value: item.id })),
        testOption: trainData.filter((item: TrainData) => item.is_test_data).map((item: TrainData) => ({ label: item.name, value: item.id })),
      };
      setTrainDataOption(options);
      console.log(formData);
      formRef.current.setFieldsValue({
        train_data_id: formData?.train_data_id,
        val_data_id: formData?.val_data_id,
        test_data_id: formData?.test_data_id,
      });
    } catch (e) {
      message.error(e as JointContent)
    } finally {
      setLoadingState((prev) => ({ ...prev, select: false }));
    }
  }, [getAnomalyTrainData]);

  // 超参数转换成表单数据
  const hyperoptConversion = (params: object) => {
    if (!params) return;
    const hyperopt_config: Record<string, any> = {};
    Object.entries(params).forEach(([key, value]) => {
      if (value?.type === 'randint') {
        hyperopt_config[key] = [value?.min, value?.max];
      } else if (value?.type === 'choice') {
        hyperopt_config[key] = value?.choice;
      }
    });
    return hyperopt_config;
  };

  // 表单数据转为请求参数
  const renderParams = (object: Record<string, any>) => {
    const hyperopt_config: Record<string, any> = {};
    Object.keys(object).forEach((item: string) => {
      if (ALGORITHMS_TYPE['RandomForest'][item] == 'randint') {
        hyperopt_config[item] = {
          type: 'randint',
          min: object[item][0],
          max: object[item][1]
        }
      } else if (ALGORITHMS_TYPE['RandomForest'][item] == 'choice') {
        hyperopt_config[item] = {
          type: 'choice',
          choice: object[item]
        }
      }
    });
    return hyperopt_config;
  };

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
        await handleUpdateMap[tagName](modalState.formData?.id as string, params)
      }
      setModalState((prev) => ({ ...prev, isOpen: false }))
      message.success(t(`datasets.${modalState.type}Success`));
      onSuccess();
    } catch (e) {
      console.log(e);
    } finally {
      setLoadingState((prev) => ({ ...prev, confirm: false }));
    }
  }, [modalState.type, modalState.formData, onSuccess]);

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
            <Select placeholder={t('traintask.selectDatasets')} loading={loadingState.select} options={datasetOptions} onChange={renderFileOption} />
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
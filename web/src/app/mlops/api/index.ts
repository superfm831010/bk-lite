import useApiClient from '@/utils/request';
import { TrainDataParams } from '../types';

interface TrainDataBrochure {
  dataset: number;
  name: string;
  train_data: TrainDataParams[];
  metadata: object;
  is_train_data: boolean;
  is_val_data: boolean;
  is_test_data: boolean;
}

interface LabelData {
  timestamp: string;
  value: string;
  label: number;
}

interface TrainTaskParams {
  name: string;
  description?: string;
  status: string;
  algorithm: string;
  train_data_id: number;
  val_data_id: number;
  text_data_id: number;
  max_evals: 0;
  hyperopt_config: object;
  windows_size?: number;
}

interface AnomalyDetectionReason {
  model_name: string;
  model_version: string;
  algorithmn: string;
  data: LabelData[];
  anomaly_threshold: number;
}

const useMlopsApi = () => {
  const {
    get,
    post,
    del,
    put,
    patch
  } = useApiClient();

  // 获取异常检测数据集列表
  const getAnomalyDatasetsList = async ({
    page = 1,
    page_size = -1
  }: {
    page?: number,
    page_size?: number
  }) => {
    return await get(`/mlops/anomaly_detection_datasets/?page=${page}&page_size=${page_size}`);
  };

  // 获取指定异常检测数据集详情
  const getOneAnomalyDataset = async (id: number) => {
    return await get(`/mlops/anomaly_detection_datasets/${id}/`);
  };

  // 查询指定数据集下的样本列表
  const getAnomalyTrainData = async ({
    dataset,
    page = 1,
    page_size = -1
  }: {
    dataset?: string | number;
    page?: number;
    page_size?: number;
  }) => {
    return await get(`/mlops/anomaly_detection_train_data/?dataset=${dataset}&page=${page}&page_size=${page_size}`);
  };

  // 获取指定异常检测样本的详情
  const getAnomalyTrainDataInfo = async (id: number | string, include_train_data?: boolean, include_metadata?: boolean) => {
    return await get(`/mlops/anomaly_detection_train_data/${id}?include_train_data=${include_train_data}&include_metadata=${include_metadata}`);
  };

  // 获取异常检测训练任务列表
  const getAnomalyTaskList = async ({
    page = 1,
    page_size = -1
  }: {
    page?: number,
    page_size?: number
  }) => {
    return await get(`/mlops/anomaly_detection_train_jobs/?page=${page}&page_size=${page_size}`);
  };

  // 查询指定的异常检测任务
  const getOneAnomalyTask = async (id: number | string) => {
    return await get(`/mlops/anomaly_detection_train_jobs/${id}`)
  };

  // 新增异常检测数据集
  const addAnomalyDatasets = async (params: {
    name: string;
    description: string;
  }) => {
    return await post(`/mlops/anomaly_detection_datasets/`, params);
  };

  // 新增异常数据检测集样本
  const addAnomalyTrainData = async (params: TrainDataBrochure) => {
    return await post(`/mlops/anomaly_detection_train_data`, params);
  };

  // 新建异常检测训练任务
  const addAnomalyTrainTask = async (params: TrainTaskParams) => {
    return await post(`/mlops/anomaly_detection_train_jobs/`, params)
  };

  // 启动异常检测训练任务
  const startAnomalyTrainTask = async (id: number | string) => {
    return await post(`/mlops/anomaly_detection_train_jobs/${id}/train/`);
  };

  // 异常检测推理
  const anomalyDetectionReason = async (params: AnomalyDetectionReason) => {
    return await post(`/mlops/anomaly_detection_train_jobs/predict/`, params);
  };


  // 更新异常检测数据集
  const updateAnomalyDatasets = async (id: number, params: {
    name: string;
    description: string;
  }) => {
    return await put(`/mlops/anomaly_detection_datasets/${id}`, params);
  };

  // 比纳基异常检测训练任务
  const updateAnomalyTrainTask = async (id: string, params: TrainTaskParams) => {
    return await patch(`/mlops/anomaly_detection_train_jobs/${id}/`, params);
  };

  // 标注数据
  const labelingData = async (id: string, params: {
    metadata: {
      anomaly_point: number[]
    },
    is_train_data: boolean,
    is_val_data: boolean,
    is_test_data: boolean
  }) => {
    return await patch(`/mlops/anomaly_detection_train_data/${id}/`, params)
  };

  // 删除异常检测数据集
  const deleteAnomalyDatasets = async (id: number) => {
    return await del(`/mlops/anomaly_detection_datasets/${id}`);
  };

  // 删除训练数据
  const deleteAnomalyTrainData = async (id: number) => {
    return await del(`/mlops/anomaly_detection_train_data/${id}/`);
  };

  // 删除异常检测训练任务
  const deleteAnomalyTrainTask = async (id: string) => {
    return await del(`/mlops/anomaly_detection_train_jobs/${id}/`);
  };

  return {
    getAnomalyDatasetsList,
    getOneAnomalyDataset,
    getAnomalyTrainData,
    getAnomalyTrainDataInfo,
    getAnomalyTaskList,
    getOneAnomalyTask,
    addAnomalyTrainTask,
    addAnomalyDatasets,
    addAnomalyTrainData,
    startAnomalyTrainTask,
    anomalyDetectionReason,
    updateAnomalyDatasets,
    updateAnomalyTrainTask,
    deleteAnomalyDatasets,
    deleteAnomalyTrainData,
    deleteAnomalyTrainTask,
    labelingData
  };
}

export default useMlopsApi;
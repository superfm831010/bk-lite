import useApiClient from "@/utils/request";
import { TrainDataParams } from '@/app/mlops/types/manage';

interface TrainDataBrochure {
  dataset: number;
  name: string;
  train_data: TrainDataParams[];
  metadata: object;
  is_train_data?: boolean;
  is_val_data?: boolean;
  is_test_data?: boolean;
}

const useMlopsManageApi = () => {
  const {
    get,
    post,
    put,
    del,
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

  // 更新异常检测数据集
  const updateAnomalyDatasets = async (id: number, params: {
    name: string;
    description: string;
  }) => {
    return await put(`/mlops/anomaly_detection_datasets/${id}`, params);
  };

  // 标注数据
  const labelingData = async (id: string, params: {
    metadata?: {
      anomaly_point: number[]
    },
    is_train_data?: boolean,
    is_val_data?: boolean,
    is_test_data?: boolean
  }) => {
    return await patch(`/mlops/anomaly_detection_train_data/${id}/`, params);
  };

  // 删除异常检测数据集
  const deleteAnomalyDatasets = async (id: number) => {
    return await del(`/mlops/anomaly_detection_datasets/${id}`);
  };

  // 删除训练数据
  const deleteAnomalyTrainData = async (id: number) => {
    return await del(`/mlops/anomaly_detection_train_data/${id}/`);
  };

  return {
    getAnomalyDatasetsList,
    getOneAnomalyDataset,
    getAnomalyTrainData,
    getAnomalyTrainDataInfo,
    addAnomalyDatasets,
    addAnomalyTrainData,
    updateAnomalyDatasets,
    labelingData,
    deleteAnomalyDatasets,
    deleteAnomalyTrainData,
  }
};

export default useMlopsManageApi;
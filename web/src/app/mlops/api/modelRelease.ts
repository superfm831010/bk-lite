import useApiClient from '@/utils/request';

interface LabelData {
  timestamp: string;
  value: string;
  label: number;
}

interface AnomalyDetectionReason {
  model_name: string;
  model_version: string;
  algorithm: string;
  data: LabelData[];
  anomaly_threshold: number;
}

const useMlopsModelReleaseApi = () => {
  const {
    get,
    post,
    del,
    // put,
    patch
  } = useApiClient();

  // 获取能力发布列表
  const getAnomalyServingsList = async (params: {
    name?: string;
    anomaly_detection_train_job?: number;
    status?: string;
    page?: number;
    page_size?: number;
  }) => {
    const searchParams = new URLSearchParams();

    // 只添加有值的参数
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        searchParams.append(key, value.toString());
      }
    });

    return await get(`/mlops/anomaly_detection_servings/?${searchParams}`);
  };

  // 查询单个能力发布
  const getOneAnomalyServing = async (id: number) => {
    return await get(`/mlops/anomaly_detection_servings/${id}/`);
  };

  // 新增能力发布
  const addAnomalyServings = async (params: {
    name: string;
    description: string;
    model_version: string;
    anomaly_detection_train_job: string;
    status: string;
    anomaly_threshold: number;
  }) => {
    return await post(`/mlops/anomaly_detection_servings/`, params);
  };

  // 异常检测推理
  const anomalyDetectionReason = async (params: AnomalyDetectionReason) => {
    return await post(`/mlops/anomaly_detection_servings/predict/`, params);
  };

  // 编辑能力发布
  const updateAnomalyServings = async (id: number, params: {
    name?: string;
    description?: string;
    model_version?: string;
    anomaly_detection_train_job?: string;
    status?: string;
    anomaly_threshold?: number;
  }) => {
    return await patch(`/mlops/anomaly_detection_servings/${id}/`, params);
  };

  // 删除能力发布
  const deleteAnomalyServing = async (id: number) => {
    return await del(`/mlops/anomaly_detection_servings/${id}/`);
  };

  return {
    getAnomalyServingsList,
    getOneAnomalyServing,
    addAnomalyServings,
    anomalyDetectionReason,
    updateAnomalyServings,
    deleteAnomalyServing
  };
};

export default useMlopsModelReleaseApi;
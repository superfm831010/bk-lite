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

  // 获取时序预测能力列表
  const getTimeSeriesPredictServingsList = async ({
    page,
    page_size
  }: {
    page?: number,
    page_size?: number
  }) => {
    return await get(`/mlops/timeseries_predict_servings/?page=${page}&page_size=${page_size}`);
  };

  // 获取日志聚类能力列表
  const getLogClusteringServingsList = async ({
    page,
    page_size
  }: {
    page?: number,
    page_size?: number
  }) => {
    return await get(`/mlops/log_clustering_servings/?page=${page}&page_size=${page_size}`);
  };

  // 查询单个能力发布
  const getOneAnomalyServing = async (id: number) => {
    return await get(`/mlops/anomaly_detection_servings/${id}/`);
  };

  // 查询单个时序预测能力
  const getOneTimeSeriesPredictServing = async (id: number) => {
    return await get(`/mlops/timeseries_predict_servings/${id}/`);
  };

  // 查询单个日志聚类能力
  const getOneLogClusteringServing = async (id: number) => {
    return await get(`/mlops/log_clustering_servings/${id}/`);
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

  // 新增时序预测能力
  const addTimeseriesPredictServings = async (params: {
    name: string;
    description: string;
    model_version: string;
    time_series_predict_train_job: string;
    status: string;
    anomaly_threshold: number;
  }) => {
    return await post(`/mlops/timeseries_predict_servings/`, params);
  };

  // 新增日志聚类能力
  const addLogClusteringServings = async (params: {
    name: string;
    description: string;
    model_version: string;
    log_clustering_train_job: string;
    status: string;
    anomaly_threshold: number;
  }) => {
    return await post(`/mlops/log_clustering_servings/`, params);
  };

  // 异常检测推理
  const anomalyDetectionReason = async (params: AnomalyDetectionReason) => {
    return await post(`/mlops/anomaly_detection_servings/predict/`, params);
  };

  // 时序预测推理
  const timeseriesPredictReason = async (params: AnomalyDetectionReason) => {
    return await post(`/mlops/timeseries_predict_servings/predict/`, params);
  };

  // 日志聚类推理
  const logClusteringReason = async (params: AnomalyDetectionReason) => {
    return await post(`/mlops/log_clustering_servings/predict/`, params);
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

  // 编辑时序预测能力
  const updateTimeSeriesPredictServings = async (id: number, params: {
    name?: string;
    description?: string;
    model_version?: string;
    anomaly_detection_train_job?: string;
    status?: string;
    anomaly_threshold?: number;
  }) => {
    return await patch(`/mlops/timeseries_predict_servings/${id}/`, params);
  };

  // 编辑日志聚类能力
  const updateLogClusteringServings = async (id: number, params: {
    name?: string;
    description?: string;
    model_version?: string;
    anomaly_detection_train_job?: string;
    status?: string;
    anomaly_threshold?: number;
  }) => {
    return await patch(`/mlops/log_clustering_servings/${id}/`, params);
  };

  // 删除能力发布
  const deleteAnomalyServing = async (id: number) => {
    return await del(`/mlops/anomaly_detection_servings/${id}/`);
  };

  // 删除时序预测能力
  const deleteTimeSeriesPredictServing = async (id: number) => {
    return await del(`/mlops/timeseries_predict_servings/${id}`);
  };

  // 删除日志聚类能力
  const deleteLogClusteringServing = async (id: number) => {
    return await del(`/mlops/log_clustering_servings/${id}`);
  };

  return {
    getAnomalyServingsList,
    getOneAnomalyServing,
    getTimeSeriesPredictServingsList,
    getLogClusteringServingsList,
    getOneTimeSeriesPredictServing,
    getOneLogClusteringServing,
    addAnomalyServings,
    addLogClusteringServings,
    addTimeseriesPredictServings,
    anomalyDetectionReason,
    timeseriesPredictReason,
    logClusteringReason,
    updateAnomalyServings,
    updateTimeSeriesPredictServings,
    updateLogClusteringServings,
    deleteAnomalyServing,
    deleteTimeSeriesPredictServing,
    deleteLogClusteringServing
  };
};

export default useMlopsModelReleaseApi;
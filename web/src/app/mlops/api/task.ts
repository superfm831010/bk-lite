import useApiClient from '@/utils/request';

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



const useMlopsTaskApi = () => {
  const {
    get,
    post,
    // put,
    del,
    patch
  } = useApiClient();

  // 获取异常检测训练任务列表
  const getAnomalyTaskList = async ({
    name = '',
    page = 1,
    page_size = -1
  }: {
    name?: string,
    page?: number,
    page_size?: number
  }) => {
    return await get(`/mlops/anomaly_detection_train_jobs/?name=${name}&page=${page}&page_size=${page_size}`);
  };

  // 获取Rasa流水线
  const getRasaPipelines = async ({
    name = '',
    page = 1,
    page_size = -1
  }: {
    name?: string,
    page?: number,
    page_size?: number
  }) => {
    return await get(`/mlops/rasa_pipelines/?name=${name}&page=${page}&page_size=${page_size}`);
  };

  // 查询指定的异常检测任务
  const getOneAnomalyTask = async (id: number | string) => {
    return await get(`/mlops/anomaly_detection_train_jobs/${id}`)
  };

  // 获取训练状态数据
  const getTrainTaskState = async (id: number) => {
    return await get(`/mlops/anomaly_detection_train_jobs/${id}/runs_data_list/`)
  };
  
  // 获取状态指标
  const getTrainTaskMetrics = async (id: string) => {
    return await get(`/mlops/anomaly_detection_train_jobs/runs_metrics_list/${id}`)
  };

  // 获取具体指标信息
  const getTrainTaskMetricsDetail = async (id: string, metrics_name: string) => {
    return await get(`/mlops/anomaly_detection_train_jobs/runs_metrics_history/${id}/${metrics_name}`);
  };

  // 新建异常检测训练任务
  const addAnomalyTrainTask = async (params: TrainTaskParams) => {
    return await post(`/mlops/anomaly_detection_train_jobs/`, params)
  };

  // 启动异常检测训练任务
  const startAnomalyTrainTask = async (id: number | string) => {
    return await post(`/mlops/anomaly_detection_train_jobs/${id}/train/`);
  };

  // 编辑异常检测训练任务
  const updateAnomalyTrainTask = async (id: string, params: TrainTaskParams) => {
    return await patch(`/mlops/anomaly_detection_train_jobs/${id}/`, params);
  };

  // 删除异常检测训练任务
  const deleteAnomalyTrainTask = async (id: string) => {
    return await del(`/mlops/anomaly_detection_train_jobs/${id}/`);
  };

  return {
    getAnomalyTaskList,
    getOneAnomalyTask,
    getTrainTaskState,
    getTrainTaskMetrics,
    getTrainTaskMetricsDetail,
    getRasaPipelines,
    addAnomalyTrainTask,
    startAnomalyTrainTask,
    updateAnomalyTrainTask,
    deleteAnomalyTrainTask,
  }

};

export default useMlopsTaskApi;
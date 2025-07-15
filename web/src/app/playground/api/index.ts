import useApiClient from "@/utils/request";

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

const usePlayroundApi = () => {
  const { post } = useApiClient();

  // 异常检测推理
  const anomalyDetectionReason = async (params: AnomalyDetectionReason) => {
    return await post(`/mlops/anomaly_detection_train_jobs/predict/`, params);
  };

  return {
    anomalyDetectionReason
  }

};

export default usePlayroundApi;
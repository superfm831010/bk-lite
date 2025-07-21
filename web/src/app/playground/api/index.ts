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
  const {
    get,
    post,
    patch,
    del
  } = useApiClient();

  // 获取分类列表
  const getCategoryList = async () => {
    return await get(`/playground/category/`);
  };

  // 查询单个类别
  const getCategoryDetail = async (id: number) => {
    return await get(`/playground/category/${id}`);
  };

  // 查询能力演示列表
  const getCapabilityList = async () => {
    return await get(`/playground/capability/`);
  };

  // 查询单个能力演示
  const getCapabilityDetail = async (id: number) => {
    return await get(`/playground/capability/${id}`);
  };

  // 创建分类
  const createCategory = async (params: {
    name: string,
    description: string,
    parant: number
  }) => {
    return await post(`/playground/category/`, params);
  };

  // 修改类别
  const updateCategory = async (id: number, params: {
    name: string,
    description: string,
    parent: number
  }) => {
    return await patch(`/playground/category/${id}/`, params)
  };

  // 创建能力演示
  const createCapability = async (params: {
    name: string,
    description: string,
    config: object,
    is_active: boolean,
    url: string
  }) => {
    return await post(`/playground/capability/`, params);
  };

  // 编辑能力演示
  const updateCapability = async (id: number, params: {
    name: string,
    description: string,
    config: object,
    is_active: boolean,
    url: string,
  }) => {
    return await patch(`/playground/capability/${id}/`, params);
  };

  // 异常检测推理
  const anomalyDetectionReason = async (params: AnomalyDetectionReason) => {
    return await post(`/mlops/anomaly_detection_servings/predict/`, params);
  };

  // 删除类别
  const deleteCategory = async (id: number) => {
    return await del(`/playground/category/${id}/`);
  };

  // 删除演示能力
  const deleteCapability = async (id: number) => {
    return await del(`/playground/capability/${id}`);
  };

  return {
    getCategoryList,
    getCategoryDetail,
    getCapabilityList,
    getCapabilityDetail,
    createCategory,
    createCapability,
    updateCategory,
    updateCapability,
    anomalyDetectionReason,
    deleteCategory,
    deleteCapability
  }

};

export default usePlayroundApi;
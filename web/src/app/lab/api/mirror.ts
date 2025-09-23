import useApiClient from "@/utils/request";

const useLabManage = () => {
  const { get, put, post, del } = useApiClient();

  // 获取全部镜像列表
  const getImageList = async (params?: any) => {
    return await get(`/lab/images/`, params);
  };

  // 新增镜像
  const addImage = async (data: any) => {
    return await post(`/lab/images/`, data);
  };

  // 更新镜像
  const updateImage = async (id: number | string, data: any) => {
    return await put(`/lab/images/${id}/`, data);
  };

  // 删除镜像
  const deleteImage = async (id: number | string) => {
    return await del(`/lab/images/${id}/`);
  };

  // 获取IDE镜像列表
  const getIdeImages = async () => {
    return await get(`/lab/images/ide_images/`);
  };

  // 获取基础设施镜像列表
  const getInfraImages = async () => {
    return await get(`/lab/images/infra_images/`);
  };

  // 获取镜像实例列表
  const getImageInstances = async (id: number | string) => {
    return await get(`/lab/images/${id}/instances/`);
  };

  return {
    getImageList,
    addImage,
    updateImage,
    deleteImage,
    getIdeImages,
    getInfraImages,
    getImageInstances,
  };
};

export default useLabManage;
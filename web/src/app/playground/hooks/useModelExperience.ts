import useApiClient from "@/utils/request";
import { useCallback, useEffect, useState } from "react";

const useModelExperience = () => {
  const [modelExpList, setModelExpList] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const { get } = useApiClient();

  const getAllActiveMenu = useCallback(async () => {
    // 🎯 避免重复请求
    if (loading || modelExpList.length > 0) return;

    setLoading(true);
    try {
      const [categoryList, capabilityList] = await Promise.all([
        await get(`/playground/category/`),
        await get(`/playground/capability/`)
      ]);

      const data = categoryList.map((item: any) => {
        const children = capabilityList.filter((child: any) => {
          const { id } = child.category;
          return (item.id === id) && child?.is_active;
        }).map((child: any) => {
          return {
            id: child.id,
            name: child?.name,
            description: child?.description,
            url: child?.url + `?page=anomaly-detection&id=${child?.id}`,
          }
        });

        return {
          category_id: item.id,
          name: item.name,
          description: item.description,
          children
        }
      });

      setModelExpList(data);
      console.log(data);
    } catch (e) {
      console.log(e);
      setModelExpList([]);
    } finally {
      setLoading(false);
    }
  }, [get, loading, modelExpList.length]);

  useEffect(() => {
    getAllActiveMenu();
  }, [getAllActiveMenu]);

  return {
    modelExpList,
    loading
  }
};

export default useModelExperience;
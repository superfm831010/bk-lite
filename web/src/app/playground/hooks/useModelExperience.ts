import useApiClient from "@/utils/request";
import { useEffect, useState } from "react";

const useModelExperience = (shouldLoad: boolean = true) => {
  const [modelExpList, setModelExpList] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { get } = useApiClient();

  useEffect(() => {
    if (!shouldLoad) {
      setLoading(false);
      return;
    }

    let isCancelled = false;
    setLoading(true);

    const loadData = async () => {
      try {
        const [categoryList, capabilityList] = await Promise.all([
          get(`/playground/category/`),
          get(`/playground/capability/`)
        ]);

        if (isCancelled) return;

        if (!categoryList || !capabilityList) {
          throw new Error('fetch menu error');
        }

        const data = categoryList.map((item: any) => {
          const children = capabilityList.filter((child: any) => {
            const categoryId = child.category?.id || child.category;
            return (item.id === categoryId) && child?.is_active;
          }).map((child: any) => ({
            id: child.id,
            name: child?.name || 'Unnamed',
            description: child?.description || '',
            url: `${child?.url}?page=anomaly-detection&id=${child?.id}&name=${child?.name}`,
          }));

          return {
            category_id: item.id,
            name: item.name || 'Unnamed Category',
            description: item.description || '',
            children
          };
        });

        setModelExpList(data);

      } catch (e) {
        if (!isCancelled) {
          setError(e instanceof Error ? e.message : 'Unknown error');
        }
      } finally {
        if (!isCancelled) {
          setLoading(false);
        }
      }
    };

    loadData();

    return () => {
      isCancelled = true;
    };
  }, [shouldLoad, get]);

  const reload = () => {
    if (!shouldLoad) return;
    
    setLoading(true);
    setError(null);
    setModelExpList([]);
  };

  return {
    modelExpList,
    loading,
    error,
    reload
  };
};

export default useModelExperience;
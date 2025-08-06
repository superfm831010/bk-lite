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
        const servingsList = await get(`/mlops/anomaly_detection_servings/`);

        if (isCancelled) return;

        if (!servingsList) {
          throw new Error('fetch menu error');
        }

        const data = servingsList.map((item: any) => {
          return {
            id: item.id,
            name: item?.name || 'Unnamed',
            description: item?.description || '',
            url: `/playground/home?page=anomaly-detection&id=${item?.id}&name=${item?.name}&description=${item.description}`,
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
import useMlopsManageApi from "@/app/mlops/api/manage"
import { useCallback } from "react";
import { TrainData } from "@/app/mlops/types/manage";


const useTrainDataLoader = () => {
  const { getAnomalyTrainData, getAnomalyTrainDataInfo } = useMlopsManageApi();

  const loadTrainOptions = useCallback(async (datasetId: number) => {
    const trainData = await getAnomalyTrainData({ dataset: datasetId });

    return {
      trainOption: trainData.filter((item: TrainData) => item.is_train_data).map((item: TrainData) => ({
        label: item.name,
        value: item.id
      })),
      valOption: trainData.filter((item: TrainData) => item.is_val_data).map((item: TrainData) => ({
        label: item.name,
        value: item.id
      })),
      testOption: trainData.filter((item: TrainData) => item.is_test_data).map((item: TrainData) => ({
        label: item.name,
        value: item.id
      }))
    }
  }, [getAnomalyTrainData]);

  const getDatasetByTrainId = useCallback(async (trianDataId: number) => {
    const { dataset } = await getAnomalyTrainDataInfo(trianDataId, false, false);
    return dataset;
  }, [getAnomalyTrainDataInfo]);

  return {loadTrainOptions, getDatasetByTrainId}
};

export default useTrainDataLoader;
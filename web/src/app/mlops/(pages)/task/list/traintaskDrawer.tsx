import { Button, Drawer, message, } from "antd";
import { useTranslation } from "@/utils/i18n";
// import { Tooltip } from 'antd';
import useMlopsTaskApi from "@/app/mlops/api/task";
// import SimpleLineChart from "@/app/mlops/components/charts/simpleLineChart";
import TrainTaskHistory from "./traintaskHistory";
import TrainTaskDetail from "./traintaskDetail";
import { useEffect, useMemo, useState } from "react";

const TrainTaskDrawer = ({ open, onCancel, selectId }:
  {
    open: boolean,
    onCancel: () => void,
    selectId: number | null
  }) => {
  const { t } = useTranslation();
  const { getTrainTaskState } = useMlopsTaskApi();
  const [showList, setShowList] = useState<boolean>(true);
  const [tableLoading, setTableLoading] = useState<boolean>(false);
  const [historyData, setHistoryData] = useState<any[]>([]);
  const [activeRunID, setActiveRunID] = useState<string>('');

  const currentDetail = useMemo(() => {
    return historyData?.find((item: any) => item.run_id === activeRunID);
  }, [activeRunID]);

  useEffect(() => {
    if (open) {
      getStateData();
    }
  }, [open]);

  const getStateData = async () => {
    setTableLoading(true);
    try {
      const { data } = await getTrainTaskState(selectId as number);
      setHistoryData(data);
      // setHistoryData(Object.entries(data?.metrics_history) || []);
    } catch (e) {
      console.log(e);
      message.error(t(`traintask.getTrainStatusFailed`));
    } finally {
      setTableLoading(false);
    }
  };

  const openDetail = (record: any) => {
    setActiveRunID(record?.run_id);
    setShowList(false);
  };

  return (
    <Drawer
      width={960}
      title={t('traintask.trainDetail')}
      open={open}
      onClose={() => {
        setShowList(true);
        onCancel();
      }}
      footer={
        <Button onClick={() => {
          setShowList(true);
          onCancel();
        }}>
          {t('common.cancel')}
        </Button>
      }
    >
      <div className="flex flex-wrap justify-between">
        {showList ?
          <TrainTaskHistory
            data={historyData}
            loading={tableLoading}
            openDetail={openDetail}
          /> :
          <TrainTaskDetail backToList={() => setShowList(true)} metricData={currentDetail} />}
      </div>
    </Drawer>
  );
};

export default TrainTaskDrawer;
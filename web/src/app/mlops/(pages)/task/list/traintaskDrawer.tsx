import { Button, Drawer } from "antd";
import { useTranslation } from "@/utils/i18n";

const TrainTaskDrawer = ({ open, onCancel, selectId }:
  {
    open: boolean,
    onCancel: () => void,
    selectId: number | null
  }) => {
  const { t } = useTranslation();
  console.log(selectId);

  return (
    <Drawer
      width={800}
      title={t('traintask.trainDetail')}
      open={open}
      onClose={onCancel}
      footer={
        <Button onClick={onCancel}>
          {t('common.cancel')}
        </Button>
      }
    >
    </Drawer>
  );
};

export default TrainTaskDrawer;
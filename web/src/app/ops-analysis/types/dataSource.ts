export interface DatasourceItem {
  id: number;
  name: string;
  describe?: string;
  nats?: string;
  created_time?: string;
}

export interface OperateModalProps {
  open: boolean;
  currentRow?: any;
  onClose: () => void;
  onSuccess?: () => void;
}
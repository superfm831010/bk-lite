export interface DatasourceItem {
  id: number;
  created_at: string;
  updated_at: string;
  created_by: string;
  updated_by: string;
  domain: string;
  updated_by_domain: string;
  name: string;
  rest_api: string;
  desc: string;
  is_active: boolean;
  params: ParamItem[];
}

export interface OperateModalProps {
  open: boolean;
  currentRow?: DatasourceItem;
  onClose: () => void;
  onSuccess?: () => void;
}

export interface ParamItem {
  name: string;
  value: any;
  alias_name: string;
  type?: string; 
  id?: string;
  desc?: string;
  required?: boolean;
  options?: Array<{ label: string; value: any }>;
}

import type { MenuProps } from 'antd';
import { JSX } from 'react';

export interface Option {
  label: string;
  value: string | number;
}

export interface EntityListProps<T> {
  data: T[];
  loading: boolean;
  searchSize?: 'large' | 'middle' | 'small';
  singleActionType?: 'button' | 'icon';
  filterOptions?: Option[];
  filter?: boolean;
  filterLoading?: boolean;
  operateSection?: React.ReactNode;
  infoText?: string | ((data: any) => string);
  menuActions?: (item: T) => MenuProps['items'];
  singleAction?: (item: T) => { text: string, onClick: (item: T) => void };
  openModal?: (item?: T) => void;
  onSearch?: (value: string) => void;
  onCardClick?: (item: T) => void;
  changeFilter?: (value: string[]) => void;
}

export interface TourItem {
  title: string;
  description: string;
  cover?: string;
  target: string;
  mask?: any;
  order: number;
}

export interface MenuItem {
  name: string;
  display_name?: string;
  url: string;
  icon: string;
  title: string;
  operation: string[];
  tour?: TourItem;
  isNotMenuItem?: boolean;
  children?: MenuItem[];
}

export interface ColumnItem {
  title: string;
  dataIndex: string;
  key: string;
  render?: (_: unknown, record: any) => JSX.Element;
  [key: string]: unknown;
}

export interface GroupFieldItem {
  title: string;
  key: string;
  child: ColumnItem[];
}

export interface MetricItem {
  id: number;
  metric_group: number;
  metric_object: number;
  name: string;
  type: string;
  display_name?: string;
  display_description?: string;
  instance_id_keys?: string[];
  dimensions: any[];
  query?: string;
  unit?: string;
  displayType?: string;
  description?: string;
  viewData?: any[];
  style?: {
    width: string;
    height: string;
  };
  [key: string]: unknown;
}

export interface ListItem {
  title?: string;
  label?: string;
  name?: string;
  display_name?: string;
  id?: string | number;
  value?: string | number;
}

export interface TabItem {
  key: string;
  label: string;
  name?: string;
  children?: JSX.Element | string;
}

export interface ChartData {
  timestamp: number;
  value1?: number;
  value2?: number;
  details?: Record<string, any>;
  [key: string]: unknown;
}

export interface TableDataItem {
  id?: number | string;
  [key: string]: any;
}

export interface ThresholdField {
  level: string;
  method: string;
  value: number | null;
}

export interface LevelMap {
  critical: string;
  error: string;
  warning: string;
  [key: string]: unknown;
}


//调用弹窗的类型
export interface ModalRef {
  showModal: (config: ModalConfig) => void;
}

export interface AnomalyDataSet {
  id: number,
  tenant_id: number,
  description: string,
  has_labels: boolean,
  created_at: string,
  user_id: string,
  [key: string]: any
}

export interface UserProfile {
  id: string,
  first_name: string,
  last_name: string
}

//调用弹窗接口传入的类型
export interface ModalConfig {
  type: string;
  title?: string;
  form?: any;
  key?: string;
  ids?: string[];
  selectedsystem?: string;
  nodes?: string[];
}

//调用弹窗的类型
export interface ModalRef {
  showModal: (config: ModalConfig) => void;
}

export interface UserProfile {
  id: string,
  first_name: string,
  last_name: string
}

export interface Pagination {
  current: number;
  total: number;
  pageSize: number;
}

export enum TrainingStatus {
  'not_stared',
  'in_progress',
  'completed',
  'failed'
}

export interface AnomalyTrainData {
  id: number;
  tenant_id: number;
  dataset_id: number;
  name: string,
  storage_path: string,
  metadata: any;
  user_id: string;
  latest_status?: TrainingStatus;
}

export interface LabelData {
  timestamp: string,
  value: number,
  label?: number
}

export interface TableData {
  id: number,
  name: string,
  anomaly?: number,
  [key: string]: any
}

export interface DataSet {
  id: number;
  name: string;
  description: string;
  icon: string;
  creator: string;
  // user_id: string;
  tenant_id: number;
}

export interface TrainJob {
  id: string | number,
  user_id: string,
  dataset_id: number,
  name: string,
  type: string,
  status: string,
  created_at: string,
  [key:string]: any
}

export interface TrainTaskModalProps {
  options?: any;
  onSuccess: () => void;
  [key: string]: any
}

export interface TrainDataModalProps {
  options?: any;
  onSuccess: () => void;
  trainData: TrainData[];
  [key: string]: any
}

export interface AlgorithmParam {
  name: string;
  type: 'value' | 'enum';
  default: string | number;
}

export interface TrainData {
  id: number;
  name: string;
  dataset_id: string | number;
}

export interface TrainDataParams {
  timestamp: string;
  value: number;
  label?: number;
  index?: number;
}

export interface TrainTaskHistory {
  id: number;
  job_id: number;
  tenant_id: number;
  train_data_id: number;
  user_id: string;
  parameters: string;
  status: string;
  created_at?: string;
  started_at?: string;
  updated_at?: string;
  completed_at?: string;
  anomaly_detection_train_jobs: {
    name: string;
  }
}
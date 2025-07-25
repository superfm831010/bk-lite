import { Dayjs } from 'dayjs';

export type FilterType = 'selector' | 'fixed';

export interface WidgetConfig {
  dataSource?: string;
  lineColor?: string;
  barColor?: string;
  pageSize?: number;
  showHeader?: boolean;
  filterType?: FilterType;
  timeRange?: [Dayjs, Dayjs];
  instanceList?: string[];
}

export interface LayoutItem {
  i: string;
  x: number;
  y: number;
  w: number;
  h: number;
  widget: string;
  title: string;
  description?: string;
  config?: WidgetConfig;
}

export interface ComponentConfigProps {
  open: boolean;
  item?: LayoutItem;
  onConfirm?: (values: any) => void;
  onClose?: () => void;
}

export interface ComponentSelectorProps {
  visible: boolean;
  onAdd: (widget: string, config?: any) => void;
  onCancel: () => void;
}

export interface BaseWidgetProps {
  config?: any;
  globalTimeRange?: any;
  globalInstances?: string[];
  refreshKey?: number; 
  onDataChange?: (data: any) => void;
}

export interface WidgetMeta {
  id: string;
  name: string;
  description: string;
  icon: string;
  category: string;
  defaultConfig?: any;
}

export interface WidgetDefinition {
  meta: WidgetMeta;
  component: React.ComponentType<BaseWidgetProps>;
  configComponent?: React.ComponentType<any>;
}

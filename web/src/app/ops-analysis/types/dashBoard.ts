import { Dayjs } from 'dayjs';
import { TopologyNodeData } from './topology';
export type FilterType = 'selector' | 'fixed';

export interface DataSourceParam {
  name: string;
  type: string;
  value: any;
  alias_name: string;
  filterType: 'params' | 'fixed' | 'filter';
}

export interface WidgetConfig {
  name?: string;
  chartType?: string;
  dataSource?: string | number;
  lineColor?: string;
  barColor?: string;
  pageSize?: number;
  showHeader?: boolean;
  filterType?: FilterType;
  timeRange?: [Dayjs, Dayjs];
  instanceList?: string[];
  params?: { [key: string]: any };
  dataSourceParams?: any[];
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

export type ViewConfigItem = LayoutItem | TopologyNodeData;

export interface ViewConfigProps {
  open: boolean;
  item?: ViewConfigItem;
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
  refreshKey?: number;
  onDataChange?: (data: any) => void;
  onReady?: (hasData?: boolean) => void;
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
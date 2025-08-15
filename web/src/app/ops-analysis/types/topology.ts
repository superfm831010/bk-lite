import { DirItem } from './index';
import { DataSourceParam } from './dashBoard';


export interface EdgeData {
  id?: string;
  lineType: 'common_line' | 'network_line';
  lineName?: string;
  config?: any;
  sourceNode: { id: string; name: string };
  targetNode: { id: string; name: string };
  sourceInterface?: InterfaceConfig;
  targetInterface?: InterfaceConfig;
}

export interface EdgeCreationData {
  lineType: 'common_line' | 'network_line';
  lineName?: string;
  sourceInterface?: string;
  targetInterface?: string;
  config?: any;
}

export interface NodeConfPanelProps {
  nodeType: 'single-value' | 'icon' | 'chart';
  readonly?: boolean;
  visible?: boolean;
  title?: string;
  onClose?: () => void;
  onConfirm?: (values: any) => void;
  onCancel?: () => void;
  initialValues?: {
    name?: string;
    logoType?: 'default' | 'custom';
    logoIcon?: string;
    logoUrl?: string;
    dataSource?: number;
    selectedFields?: string[];
    fontSize?: number;
    textColor?: string;
    backgroundColor?: string;
    borderColor?: string;
    dataSourceParams?: DataSourceParam[];
    filterParams?: Record<string, any>;
    chartWidget?: string;
    valueConfig?: any;
  };
}

export interface ContextMenuProps {
  visible: boolean;
  position: { x: number; y: number };
  isEditMode?: boolean;
  onMenuClick: (e: { key: string }) => void;
}
interface InterfaceConfig {
  type: 'existing' | 'custom';
  value: string;
}

export interface EdgeConfigPanelProps {
  visible: boolean;
  readonly?: boolean;
  edgeData: EdgeData | null;
  onClose: () => void;
  onConfirm?: (values: any) => void;
}

export interface SidebarProps {
  collapsed: boolean;
  isEditMode?: boolean;
  setCollapsed: (collapsed: boolean) => void;
  onShowNodeConfig?: (nodeType: NodeType, dropPosition?: DropPosition) => void;
  onAddChartNode?: (widget: string, config?: any, dropPosition?: DropPosition) => void;
}

export interface NodeType {
  id: string;
  name: string;
  icon: React.ReactNode;
  description: string;
}

export interface DropPosition {
  x: number;
  y: number;
}

export interface TextEditInputProps {
  isEditingText: boolean;
  editPosition: { x: number; y: number };
  inputWidth: number;
  tempTextInput: string;
  setTempTextInput: (text: string) => void;
  finishTextEdit: () => void;
  cancelTextEdit: () => void;
}

export interface ToolbarProps {
  isSelectMode: boolean;
  isEditMode?: boolean;
  selectedTopology?: DirItem | null;
  onZoomIn: () => void;
  onZoomOut: () => void;
  onEdit: () => void;
  onSave: () => void;
  onFit: () => void;
  onDelete: () => void;
  onSelectMode: () => void;
  onAddText: () => void;
}

export interface TopologyNodeData {
  type: string;
  name: string;
  widget?: string;
  dataSource?: number;
  dataSourceParams?: DataSourceParam[];
  valueConfig?: {
    name?: string;
    dataSource?: number;
    chartType?: string;
    dataSourceParams?: DataSourceParam[];
    [key: string]: any;
  };
  config?: {
    width?: number;
    height?: number;
    [key: string]: any;
  };
  [key: string]: any;
}


export interface TopologyEdgeData {
  id: string;
  source: string;
  target: string;
  sourcePort: string;
  targetPort: string;
  lineType: 'common_line' | 'network_line';
  lineName: string;
  sourceInterface?: string;
  targetInterface?: string;
  config?: any;
}
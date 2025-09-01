import { DirItem } from './index';
import { DataSourceParam } from './dashBoard';
import type { Graph as X6Graph, Cell, Node, Edge } from '@antv/x6';

// 基础几何类型
export interface Point {
  x: number;
  y: number;
}

// 状态管理相关类型
export interface GraphState {
  instance: X6Graph | null;
  scale: number;
  selectedCells: string[];
  isSelectMode: boolean;
  isEditMode: boolean;
  collapsed: boolean;
}

export interface ContextMenuState {
  nodeId: string;
  visible: boolean;
  position: { x: number; y: number };
}

export interface TextEditState {
  isEditing: boolean;
  nodeId: string | null;
  tempInput: string;
  position: { x: number; y: number };
  inputWidth: number;
  originalText: string;
}

export interface EdgeConfigState {
  visible: boolean;
  data: EdgeData | null;
}

export interface NodeEditState {
  visible: boolean;
  data: any;
}

// 节点相关类型扩展
export interface TopologyNodeData {
  type: string;
  name: string;
  widget?: string;
  position: Point;
  valueConfig?: {
    chartType?: string;
    dataSource?: number;
    dataSourceParams?: DataSourceParam[];
    selectedFields?: string[];
  };
  styleConfig?: {
    width?: number;
    height?: number;
    backgroundColor?: string;
    borderColor?: string;
    borderWidth?: number;
    lineType?: 'solid' | 'dashed' | 'dotted';
    shapeType?: 'rectangle' | 'circle';
    textColor?: string;
    fontSize?: number;
    fontWeight?: string | number;
  };
  logoType?: string;
  logoIcon?: string;
  logoUrl?: string;
  selectedFields?: string[];
  width?: number;
  height?: number;
  id?: string;
  x?: number;
  y?: number;
}

// 图形实例操作类型
export interface GraphOperations {
  getCells(): Cell[];
  getNodes(): Node[];
  getEdges(): Edge[];
  getCellById(id: string): Cell | null;
  clientToLocal(clientX: number, clientY: number): Point;
  addEdge(edgeConfig: any): Edge;
}

// 状态管理相关类型
export interface TopologyState {
  graphInstance: X6Graph | null;
  contextMenuNodeId: string | null;
  setContextMenuVisible: (visible: boolean) => void;
  isEditMode: boolean;
  currentEdgeData: EdgeData | null;
  setCurrentEdgeData: (data: EdgeData | null) => void;
  isDrawingRef: React.MutableRefObject<boolean>;
  drawingEdgeRef: React.MutableRefObject<Edge | null>;
  updateDrawingState: (isDrawing: boolean) => void;
  setEdgeConfigVisible: (visible: boolean) => void;
}

// 菜单操作类型
export interface MenuClickEvent {
  key: string;
}

// 端口配置类型
export interface PortPosition {
  x: number;
  y: number;
}

export interface PortPositions {
  top: PortPosition;
  bottom: PortPosition;
  left: PortPosition;
  right: PortPosition;
}

// Hook 返回类型
export interface UseContextMenuAndModalReturn {
  handleEdgeConfigConfirm: (values: { lineType: 'common_line' | 'network_line'; lineName?: string }) => void;
  closeEdgeConfig: () => void;
  handleMenuClick: (event: MenuClickEvent) => void;
}


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
  nodeType: 'single-value' | 'icon' | 'chart' | 'basic-shape';
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
    borderWidth?: number;
    lineType?: 'solid' | 'dashed' | 'dotted';
    width?: number;
    height?: number;
    shapeType?: 'rectangle' | 'circle';
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
  graphInstance?: X6Graph;
  setCollapsed: (collapsed: boolean) => void;
  onShowNodeConfig?: (nodeType: NodeType, dropPosition?: DropPosition) => void;
  onShowChartSelector?: (dropPosition?: DropPosition) => void;
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
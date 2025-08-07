import { DirItem } from './index';
export interface EdgeData {
  id?: string;
  lineType: 'line' | 'network line';
  lineName?: string;
  config?: any;
  sourceNode: { id: string; name: string };
  targetNode: { id: string; name: string };
  sourceInterface?: InterfaceConfig;
  targetInterface?: InterfaceConfig;
}

export interface EdgeCreationData {
  lineType: 'line' | 'network line';
  lineName?: string;
  sourceInterface?: string;
  targetInterface?: string;
  config?: any;
}

export interface NodeConfPanelProps {
  nodeType: 'single-value' | 'icon';
  onFormReady?: (formInstance: any) => void;
  readonly?: boolean;
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
    query?: string;
    unit?: string;
    threshold?: number;
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
  onAddNode?: (nodeConfig: any) => void;
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
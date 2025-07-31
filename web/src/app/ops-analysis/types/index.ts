export type DirectoryType = 'directory' | 'dashboard' | 'topology' | 'datasource';
export type CreateDirectoryType = 'directory' | 'dashboard' | 'topology';
export type ModalAction = 'addRoot' | 'addChild' | 'edit';

export interface DirItem {
  id: string;
  data_id: string; 
  name: string;
  type: DirectoryType;
  children?: DirItem[];
  desc?: string;
}

export interface SidebarProps {
  onSelect?: (type: DirectoryType, itemInfo?: DirItem) => void;
  onDataUpdate?: (updatedItem: DirItem) => void;
}

export interface SidebarRef {
  clearSelection: () => void;
}

export interface ApiDirectoryItem {
  id: string;
  name: string;
  data_id: string;
  type: string;
  children?: ApiDirectoryItem[];
}

export type DirectoryType = 'group' | 'dashboard' | 'topology' | 'datasource';
export type ModalAction = 'addRoot' | 'addChild' | 'edit';

export interface DirItem {
  id: string;
  name: string;
  type: DirectoryType;
  children?: DirItem[];
  description?: string;
}

export interface SidebarProps {
  onSelect?: (type: DirectoryType, itemInfo?: DirItem) => void;
}

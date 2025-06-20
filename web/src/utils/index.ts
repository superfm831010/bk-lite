import { Group } from '@/types/index'

interface TreeSelectDataItem {
  title: string;
  value: number;
  key: number;
  disabled: boolean;
  children?: TreeSelectDataItem[];
}

/**
 * 将 group_tree 数据转换为 TreeSelect 组件需要的格式
 * @param groupTree 组织树形数据
 * @returns TreeSelect 所需的数据格式
 */
export const convertGroupTreeToTreeSelectData = (groupTree: Group[]): TreeSelectDataItem[] => {
  const convert = (groups: Group[]): TreeSelectDataItem[] => {
    return groups.map(group => ({
      title: group.name,
      value: Number(group.id),
      key: Number(group.id),
      disabled: !group.hasAuth,
      children: group.subGroups && group.subGroups.length > 0 
        ? convert(group.subGroups) 
        : undefined
    }));
  };
  
  return convert(groupTree);
};

/**
 * 获取树形数据中所有节点的 key
 * @param treeData 树形数据
 * @returns 所有节点的 key 数组
 */
export const getAllTreeKeys = (treeData: any[]): number[] => {
  const keys: number[] = [];
  const traverse = (nodes: any[]) => {
    nodes.forEach(node => {
      keys.push(node.key);
      if (node.children && node.children.length > 0) {
        traverse(node.children);
      }
    });
  };
  traverse(treeData);
  return keys;
};

/**
 * 将树形结构的数组平铺为一维数组
 * @param treeData 树形结构数据
 * @returns 平铺的一维数组
 */
export const convertTreeDataToGroupOptions = (treeData: Group[]): Group[] => {
  const flatData: Group[] = [];

  const flatten = (list: Group[]) => {
    list.forEach(item => {
      flatData.push(item);
      if (item.children) {
        flatten(item.children);
      }
    });
  };
  flatten(treeData);
  return flatData;
};

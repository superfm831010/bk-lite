import React from 'react';
import { Input, Tree } from 'antd';
import type { DataNode } from 'antd/lib/tree';

interface InstanceTreeProps {
  treeData: DataNode[];
  inputValue: string;
  placeholder?: string;
  onSearch: (value: string) => void;
  onInputChange: (value: string) => void;
  onSelect: (keys: React.Key[], info: { node: DataNode }) => void;
}

const InstanceTree: React.FC<InstanceTreeProps> = ({
  treeData,
  inputValue,
  placeholder = '搜索',
  onSearch,
  onInputChange,
  onSelect,
}) => (
  <div className="w-[200px] p-4 pl-2 overflow-auto bg-gray-50 border-r border-[var(--color-border-2)]">
    <div className="flex items-center mb-4 pl-2">
      <Input
        placeholder={placeholder}
        allowClear
        className="flex-1"
        value={inputValue}
        onChange={(e) => onInputChange(e.target.value)}
        onPressEnter={(e) => onSearch(e.currentTarget.value)}
        onClear={() => onSearch('')}
      />
    </div>
    <Tree
      defaultExpandAll
      blockNode
      treeData={treeData}
      style={{
        backgroundColor: 'rgb(249 250 251 / var(--tw-bg-opacity, 1))',
      }}
      onSelect={onSelect}
    />
  </div>
);

export default InstanceTree;

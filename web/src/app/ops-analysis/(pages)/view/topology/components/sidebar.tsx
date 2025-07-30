import React, { useMemo } from 'react';
import CustomTable from '@/components/custom-table';
import type { DataNode } from 'antd/lib/tree';
import { Button, Input, Tree, Modal } from 'antd';
import { RightOutlined, LeftOutlined } from '@ant-design/icons';
import { filterTree } from '../utils/topologyUtils';
import { mockGroups } from '../../mockData';
import { useTranslation } from '@/utils/i18n';

interface SidebarProps {
  collapsed: boolean;
  searchTerm: string;
  inputValue: string;
  modalVisible: boolean;
  instanceOptions: Array<{ id: string; name: string }>;
  selectedRowKeys: React.Key[];
  setCollapsed: (collapsed: boolean) => void;
  setSearchTerm: (term: string) => void;
  setInputValue: (value: string) => void;
  onTreeSelect: (keys: React.Key[], info: { node: DataNode }) => void;
  onModalOk: () => void;
  onModalCancel: () => void;
  onSelect: (keys: React.Key[]) => void;
}

const Sidebar: React.FC<SidebarProps> = ({
  collapsed,
  searchTerm,
  inputValue,
  modalVisible,
  instanceOptions,
  selectedRowKeys,
  setCollapsed,
  setSearchTerm,
  setInputValue,
  onTreeSelect,
  onModalOk,
  onModalCancel,
  onSelect,
}) => {
  const filteredTreeData = useMemo(
    () => filterTree(mockGroups, searchTerm),
    [searchTerm]
  );
  const { t } = useTranslation();

  return (
    <>
      <div
        className={`h-full border-r border-[var(--color-border-2)] bg-[var(--color-fill-1)] transition-[width] duration-300 flex-shrink-0 relative ${
          collapsed ? 'w-0' : 'w-50'
        }`}
      >
        <Button
          type="text"
          icon={collapsed ? <RightOutlined /> : <LeftOutlined />}
          onClick={() => setCollapsed(!collapsed)}
          className="absolute top-5 bg-[var(--color-bg-1)] rounded-full shadow-sm border border-[var(--color-border-1)] hover:border-blue-300 !p-0"
          style={{
            width: '24px',
            height: '24px',
            minWidth: '24px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: 0,
            zIndex: 10,
            right: collapsed ? '-24px' : '-12px',
            borderRadius: collapsed ? '0 50% 50% 0' : '50%'
          }}
        />

        {!collapsed && (
          <div className="h-full p-4 opacity-100 transition-opacity duration-300">
            <div className="h-full overflow-auto">
              <div className="flex items-center mb-4">
                <Input
                  placeholder={t('common.search')}
                  allowClear
                  className="flex-1"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onPressEnter={(e) => setSearchTerm(e.currentTarget.value)}
                  onClear={() => setSearchTerm('')}
                />
              </div>
              <Tree
                defaultExpandAll
                blockNode
                treeData={filteredTreeData}
                className="bg-transparent"
                onSelect={onTreeSelect}
              />
            </div>
          </div>
        )}
      </div>

      <Modal
        title="选择实例"
        width={600}
        open={modalVisible}
        onOk={onModalOk}
        onCancel={onModalCancel}
        style={{ top: '20%' }}
        styles={{ body: { height: '40vh', overflowY: 'auto' } }}
      >
        <CustomTable
          rowKey="id"
          columns={[{ title: '名称', dataIndex: 'name' }]}
          dataSource={instanceOptions}
          pagination={false}
          scroll={{ y: 300 }}
          rowSelection={{
            selectedRowKeys,
            onChange: onSelect,
          }}
        />
      </Modal>
    </>
  );
};

export default Sidebar;

import React from 'react';
import { Modal, Table } from 'antd';

interface InstanceModalProps {
  visible: boolean;
  dataSource: Array<{ id: string; name: string }>;
  selectedRowKeys: React.Key[];
  onOk: () => void;
  onCancel: () => void;
  onSelect: (keys: React.Key[]) => void;
}

const InstanceModal: React.FC<InstanceModalProps> = ({
  visible,
  dataSource,
  selectedRowKeys,
  onOk,
  onCancel,
  onSelect,
}) => (
  <Modal
    title="选择实例"
    width={600}
    open={visible}
    onOk={onOk}
    onCancel={onCancel}
  >
    <Table
      rowKey="id"
      columns={[{ title: '名称', dataIndex: 'name' }]}
      dataSource={dataSource}
      pagination={false}
      scroll={{ y: 300 }}
      rowSelection={{
        selectedRowKeys,
        onChange: onSelect,
      }}
    />
  </Modal>
);

export default InstanceModal;

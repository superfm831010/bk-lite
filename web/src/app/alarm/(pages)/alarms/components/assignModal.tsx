import React, { useState } from 'react';
import { Modal, Select } from 'antd';
import { useCommon } from '@/app/alarm/context/common';
import { UserItem } from '@/app/alarm/types';

interface AlarmAssignModalProps {
  visible: boolean;
  onCancel: () => void;
  onSuccess: (selectedUserIds: (number|string)[]) => void;
}

const AlarmAssignModal: React.FC<AlarmAssignModalProps> = ({
  visible,
  onCancel,
  onSuccess,
}) => {
  const common = useCommon();
  const userList: UserItem[] = common?.userList || [];
  const [selectedIds, setSelectedIds] = useState<(number|string)[]>([]);

  const options = userList.map((u: UserItem) => ({
    label: `${u.display_name} (${u.username})`,
    value: u.id,
  }));

  const handleOk = () => {
    onSuccess(selectedIds);
    setSelectedIds([]);
    onCancel();
  };

  return (
    <Modal
      title="分配告警给用户"
      open={visible}
      onOk={handleOk}
      onCancel={() => {
        setSelectedIds([]);
        onCancel();
      }}
    >
      <Select
        mode="multiple"
        style={{ width: '100%' }}
        placeholder="请选择用户"
        options={options}
        value={selectedIds}
        onChange={(val) => setSelectedIds(val)}
      />
    </Modal>
  );
};

export default AlarmAssignModal;

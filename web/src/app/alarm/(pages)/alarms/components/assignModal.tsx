import React, { useState } from 'react';
import OperateModal from '@/components/operate-modal';
import { Select } from 'antd';
import { useCommon } from '@/app/alarm/context/common';
import { UserItem } from '@/app/alarm/types/types';
import { useTranslation } from '@/utils/i18n';

interface AlarmAssignModalProps {
  actionType?: 'dispatch' | 'assign';
  visible: boolean;
  onCancel: () => void;
  onSuccess: (selectedUserIds: (number | string)[]) => void;
}

const AlarmAssignModal: React.FC<AlarmAssignModalProps> = ({
  visible,
  actionType,
  onCancel,
  onSuccess,
}) => {
  const common = useCommon();
  const userList: UserItem[] = common?.userList || [];
  const [selectedIds, setSelectedIds] = useState<(number | string)[]>([]);
  const { t } = useTranslation();

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
    <OperateModal
      title={t(`alarms.${actionType}`)}
      open={visible}
      onOk={handleOk}
      onCancel={() => {
        setSelectedIds([]);
        onCancel();
      }}
    >
      <div className="flex justify-between items-center mt-2 mb-4">
        <label className="block mr-2">{t('alarms.user')}</label>
        <Select
          allowClear
          showSearch
          mode="multiple"
          optionFilterProp="label"
          style={{ width: '100%', flex: 1 }}
          placeholder={t('common.pleaseSelect')} 
          options={options}
          value={selectedIds}
          filterOption={(input, option) =>
            (option?.label as string)?.toLowerCase().includes(input.toLowerCase())
          }
          onChange={(val) => setSelectedIds(val)}
        />
      </div>
    </OperateModal>
  );
};

export default AlarmAssignModal;

import React from 'react';
import LogicalRule from './ logicalRule';
import { Drawer } from 'antd';

interface OperateModalProps {
  open: boolean;
  currentRow?: any;
  onClose: () => void;
}

const OperateModalPage: React.FC<OperateModalProps> = ({
  open,
  currentRow,
  onClose,
}) => {
  console.log('currentRow', currentRow);
  return (
    <Drawer
      title={''}
      placement="right"
      width={720}
      open={open}
      onClose={onClose}
    >
      <LogicalRule />
    </Drawer>
  );
};

export default OperateModalPage;

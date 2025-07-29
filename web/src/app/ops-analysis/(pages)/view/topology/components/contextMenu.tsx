import React from 'react';
import { Menu, Dropdown } from 'antd';
import { useTranslation } from '@/utils/i18n';

interface ContextMenuProps {
  visible: boolean;
  position: { x: number; y: number };
  isEditMode?: boolean;
  onMenuClick: (e: { key: string }) => void;
}

const ContextMenu: React.FC<ContextMenuProps> = ({
  visible,
  position,
  isEditMode = false,
  onMenuClick,
}) => {
  const { t } = useTranslation();

  const menu = isEditMode ? (
    <Menu onClick={onMenuClick}>
      <Menu.Item key="none">无箭头连接</Menu.Item>
      <Menu.Item key="single">单向连接</Menu.Item>
      <Menu.Item key="double">双向连接</Menu.Item>
    </Menu>
  ) : (
    <Menu onClick={onMenuClick}>
      <Menu.Item key="viewAlarms">{t('topology.viewAlarmList')}</Menu.Item>
      <Menu.Item key="viewMonitor">
        {t('topology.viewMonitorDetails')}
      </Menu.Item>
    </Menu>
  );

  if (!visible) return null;
  return (
    <Dropdown
      overlay={menu}
      open={visible}
      getPopupContainer={() => document.body}
    >
      <div
        style={{
          position: 'fixed',
          left: position.x,
          top: position.y,
          width: 1,
          height: 1,
        }}
      />
    </Dropdown>
  );
};

export default ContextMenu;

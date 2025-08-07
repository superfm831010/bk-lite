import React from 'react';
import { Menu, Dropdown } from 'antd';
import { useTranslation } from '@/utils/i18n';
import type { ContextMenuProps } from '@/app/ops-analysis/types/topology';
import {
  VerticalAlignTopOutlined,
  UpOutlined,
  DownOutlined,
  LinkOutlined,
  ArrowRightOutlined,
  SwapOutlined,
} from '@ant-design/icons';


const ContextMenu: React.FC<ContextMenuProps> = ({
  visible,
  position,
  isEditMode = false,
  onMenuClick,
}) => {
  const { t } = useTranslation();

  const menu = isEditMode ? (
    <Menu onClick={onMenuClick}>
      <Menu.Item key="bringToFront" icon={<VerticalAlignTopOutlined />}>
        置顶
      </Menu.Item>
      <Menu.Item key="bringForward" icon={<UpOutlined />}>
        上移一层
      </Menu.Item>
      <Menu.Item key="sendBackward" icon={<DownOutlined />}>
        下移一层
      </Menu.Item>
      <Menu.Divider />
      <Menu.Item key="none" icon={<LinkOutlined />}>
        无箭头连接
      </Menu.Item>
      <Menu.Item key="single" icon={<ArrowRightOutlined />}>
        单向连接
      </Menu.Item>
      <Menu.Item key="double" icon={<SwapOutlined />}>
        双向连接
      </Menu.Item>
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

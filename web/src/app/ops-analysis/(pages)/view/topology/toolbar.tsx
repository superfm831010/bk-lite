import React from 'react';
import { Button, Tooltip } from 'antd';
import { useTranslation } from '@/utils/i18n';
import {
  ZoomInOutlined,
  ZoomOutOutlined,
  EditOutlined,
  SaveOutlined,
  FullscreenOutlined,
  DeleteOutlined,
  SelectOutlined,
} from '@ant-design/icons';

interface Props {
  onZoomIn: () => void;
  onZoomOut: () => void;
  onEdit: () => void;
  onSave: () => void;
  onFit: () => void;
  onDelete: () => void;
  onSelectMode: () => void;
  isSelectMode: boolean;
}

const TopologyToolbar: React.FC<Props> = ({
  onZoomIn,
  onZoomOut,
  onEdit,
  onSave,
  onFit,
  onDelete,
  onSelectMode,
  isSelectMode,
}) => {
  const { t } = useTranslation();

  return (
    <div className="pl-8 mb-4 flex items-center space-x-4 rounded-lg shadow-sm">
      <Tooltip title={t('common.edit')}>
        <Button
          type="text"
          icon={<EditOutlined style={{ fontSize: 18 }} />}
          onClick={onEdit}
        />
      </Tooltip>
      <Tooltip title={t('dashboard.save')}>
        <Button
          type="text"
          icon={<SaveOutlined style={{ fontSize: 18 }} />}
          onClick={onSave}
        />
      </Tooltip>
      <Tooltip title={t('dashboard.zoomIn')}>
        <Button
          type="text"
          icon={<ZoomInOutlined style={{ fontSize: 18 }} />}
          onClick={onZoomIn}
        />
      </Tooltip>
      <Tooltip title={t('dashboard.zoomOut')}>
        <Button
          type="text"
          icon={<ZoomOutOutlined style={{ fontSize: 18 }} />}
          onClick={onZoomOut}
        />
      </Tooltip>
      <Tooltip title={t('dashboard.fitView')}>
        <Button
          type="text"
          icon={<FullscreenOutlined style={{ fontSize: 18 }} />}
          onClick={onFit}
        />
      </Tooltip>
      <Tooltip title={t('dashboard.selectMode')}>
        <Button
          type={isSelectMode ? 'primary' : 'text'}
          icon={<SelectOutlined style={{ fontSize: 18 }} />}
          onClick={onSelectMode}
        />
      </Tooltip>
      <Tooltip title={t('dashboard.deleteSelected')}>
        <Button
          type="text"
          icon={<DeleteOutlined style={{ fontSize: 18 }} />}
          onClick={onDelete}
          danger
        />
      </Tooltip>
    </div>
  );
};

export default TopologyToolbar;

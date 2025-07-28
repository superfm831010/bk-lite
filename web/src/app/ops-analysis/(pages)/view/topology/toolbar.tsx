import React from 'react';
import { Button, Tooltip } from 'antd';
import { useTranslation } from '@/utils/i18n';
import {
  ZoomInOutlined,
  ZoomOutOutlined,
  EditOutlined,
  FullscreenOutlined,
  DeleteOutlined,
  SelectOutlined,
  FontSizeOutlined,
} from '@ant-design/icons';

interface Props {
  isSelectMode: boolean;
  isEditMode?: boolean;
  onZoomIn: () => void;
  onZoomOut: () => void;
  onEdit: () => void;
  onSave: () => void;
  onFit: () => void;
  onDelete: () => void;
  onSelectMode: () => void;
  onAddText: () => void;
}

const TopologyToolbar: React.FC<Props> = ({
  isSelectMode,
  isEditMode = false,
  onZoomIn,
  onZoomOut,
  onEdit,
  onSave,
  onFit,
  onDelete,
  onSelectMode,
  onAddText,
}) => {
  const { t } = useTranslation();

  return (
    <div className="w-full pl-6 pb-2 mb-2 flex items-center rounded-lg shadow-sm justify-between">
      <div className="space-x-4">
        <Tooltip title={t('topology.zoomIn')}>
          <Button
            type="text"
            icon={<ZoomInOutlined style={{ fontSize: 16 }} />}
            onClick={onZoomIn}
          />
        </Tooltip>
        <Tooltip title={t('topology.zoomOut')}>
          <Button
            type="text"
            icon={<ZoomOutOutlined style={{ fontSize: 16 }} />}
            onClick={onZoomOut}
          />
        </Tooltip>
        <Tooltip title={t('topology.fitView')}>
          <Button
            type="text"
            icon={<FullscreenOutlined style={{ fontSize: 16 }} />}
            onClick={onFit}
          />
        </Tooltip>
        {isEditMode && (
          <>
            <Tooltip title={t('topology.addText')}>
              <Button
                type="text"
                icon={<FontSizeOutlined style={{ fontSize: 16 }} />}
                onClick={onAddText}
              />
            </Tooltip>
            <Tooltip title={t('topology.selectMode')}>
              <Button
                type="text"
                icon={<SelectOutlined style={{ fontSize: 16 }} />}
                onClick={onSelectMode}
                style={{
                  backgroundColor: isSelectMode ? '#f5f5f5' : 'transparent',
                  color: isSelectMode ? '#595959' : undefined,
                }}
              />
            </Tooltip>
            <Tooltip title={t('topology.deleteSelected')}>
              <Button
                type="text"
                icon={<DeleteOutlined style={{ fontSize: 16 }} />}
                onClick={onDelete}
              />
            </Tooltip>
          </>
        )}
      </div>
      {isEditMode ? (
        <Button type="primary" onClick={onSave}>
          {t('common.save')}
        </Button>
      ) : (
        <Tooltip title={t('common.edit')} className="mr-2">
          <Button
            type="text"
            icon={<EditOutlined style={{ fontSize: 16 }} />}
            onClick={onEdit}
          />
        </Tooltip>
      )}
    </div>
  );
};

export default TopologyToolbar;

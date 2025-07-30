import React from 'react';
import { Button, Tooltip } from 'antd';
import { useTranslation } from '@/utils/i18n';
import { DirItem } from '@/app/ops-analysis/types';
import {
  ZoomInOutlined,
  ZoomOutOutlined,
  FullscreenOutlined,
  DeleteOutlined,
  SelectOutlined,
  FontSizeOutlined,
  EditOutlined,
} from '@ant-design/icons';

interface Props {
  isSelectMode: boolean;
  isEditMode?: boolean;
  selectedTopology?: DirItem | null;
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
  selectedTopology,
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
    <div className="w-full mb-4 flex items-center justify-between rounded-lg shadow-sm bg-[var(--color-bg-1)] p-4 border border-[var(--color-border-2)]">
      {/* 左侧：拓扑信息 */}
      <div className="flex-1 mr-8">
        {selectedTopology && (
          <div>
            <h2 className="text-xl font-semibold mb-1 text-[var(--color-text-1)] flex items-center">
              {selectedTopology.name}
            </h2>
            {selectedTopology.description && (
              <p className="text-sm text-[var(--color-text-2)]">
                {selectedTopology.description}
              </p>
            )}
          </div>
        )}
      </div>

      {/* 右侧：工具栏 */}
      <div className="flex items-center space-x-1 rounded-lg p-2">
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
                  backgroundColor: isSelectMode ? '#1677ff15' : 'transparent',
                  color: isSelectMode ? '#1677ff' : undefined,
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

        <div>
          {isEditMode ? (
            <Button type="primary" onClick={onSave} className="!ml-[20px]">
              {t('common.save')}
            </Button>
          ) : (
            <Tooltip title={t('common.edit')}>
              <Button
                type="text"
                icon={<EditOutlined style={{ fontSize: 16 }} />}
                onClick={onEdit}
              />
            </Tooltip>
          )}
        </div>
      </div>
    </div>
  );
};

export default TopologyToolbar;

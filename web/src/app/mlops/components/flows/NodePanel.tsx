import React, { useState } from 'react';
import { Button } from 'antd';
import { NodeType } from '@/app/mlops/types';
import { UpOutlined, DownOutlined } from '@ant-design/icons';
import Icon from '@/components/icon';
import { useTranslation } from '@/utils/i18n';

interface NodePanelProps {
  nodeTypes: NodeType[];
  onDragStart: (event: React.DragEvent, nodeType: string) => void;
}

const NodePanel: React.FC<NodePanelProps> = ({ onDragStart, nodeTypes }) => {
  const { t } = useTranslation();
  const [showPanel, setShowPanel] = useState<boolean>(true);

  return (
    <div className={`w-full h-[80px] absolute ${showPanel ? 'bottom-0' : 'bottom-[-80px]'} transition-all duration-300 ease-in-out z-10 bg-[var(--color-bg-4)] border-t border-gray-200 shadow-lg`}>
      {/* 切换按钮 */}
      <div className='absolute top-0 left-[50%] translate-x-[-50%] translate-y-[-60%] z-20'>
        <Button
          className='border border-gray-200 shadow-md hover:shadow-lg transition-shadow duration-200'
          size='small'
          icon={showPanel ? <DownOutlined /> : <UpOutlined />}
          shape='circle'
          onClick={() => setShowPanel(x => !x)}
        />
      </div>

      {/* 顶部提示 */}
      <div className="px-6 py-1 border-t border-gray-100 flex-shrink-0">
        <div className="text-xs text-gray-500 text-left">
          {t(`mlops-common.nodePanelMsg`)}
        </div>
      </div>

      {/* 面板内容 */}
      <div className="flex flex-col">
        {/* 面板标题 */}
        {/* <div className="px-6 py-2 border-b border-gray-100 flex-shrink-0">
          <h3 className="text-sm font-medium text-gray-800">{t(`mlops-common.nodeSelect`)}</h3>
        </div> */}

        {/* 节点列表 - 横向滚动布局 */}
        <div className="flex-1 px-6 py-1 overflow-hidden">
          <div className="flex space-x-3 overflow-x-auto items-center">
            {nodeTypes.map((nodeType: NodeType) => (
              <div
                key={nodeType.type}
                className="flex flex-row items-center justify-start min-w-[140px] w-[140px] h-[40px] px-3 py-2 rounded-lg border border-gray-200 bg-[var(--color-bg)] hover:bg-gray-50 hover:border-blue-300 transition-all cursor-grab active:cursor-grabbing select-none shadow-sm hover:shadow-md"
                draggable
                onDragStart={(event) => onDragStart(event, nodeType.type)}
              >
                <Icon type={nodeType.icon} className='!w-6 !h-6 mr-3 text-blue-600 flex-shrink-0' />
                <span className="text-xs text-gray-700 font-medium leading-tight flex-1">
                  {nodeType.label}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default NodePanel;
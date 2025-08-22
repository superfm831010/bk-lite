import React, { useState } from 'react';
import { Button } from 'antd';
import { LeftOutlined, RightOutlined } from '@ant-design/icons';

interface NodeType {
  type: string;
  label: string;
  color: string;
}

interface NodePanelProps {
  nodeTypes: NodeType[];
  onDragStart: (event: React.DragEvent, nodeType: string) => void;
}

const NodePanel: React.FC<NodePanelProps> = ({ onDragStart, nodeTypes }) => {
  const [showTab, setShowTable] = useState<boolean>(true);
  return (
    <div className={`w-[220px] h-full absolute ${showTab ? 'left-0': 'left-[-220px]'} transition-all duration-300 ease-in-out z-10 bg-white border-r border-gray-200 shadow-lg`}>
      {/* 切换按钮 */}
      <div className='absolute top-[50%] right-0 translate-x-[60%] translate-y-[-50%] z-20'>
        <Button
          className='border-0 shadow-md hover:shadow-lg transition-shadow duration-200'
          size='small'
          icon={showTab ? <LeftOutlined /> : <RightOutlined />}
          shape='circle'
          onClick={() => setShowTable(x => !x)}
        />
      </div>
      
      {/* 面板标题 */}
      <div className="px-4 py-3 border-b border-gray-100">
        <h3 className="text-base font-medium text-gray-800">节点选择</h3>
      </div>
      
      {/* 节点列表 */}
      <div className="px-4 py-4 space-y-2">
        {nodeTypes.map((nodeType: NodeType) => (
          <div
            key={nodeType.type}
            className="flex items-center space-x-3 p-3 rounded-md border border-gray-200 hover:border-gray-300 hover:bg-gray-50 transition-colors cursor-grab active:cursor-grabbing select-none"
            draggable
            onDragStart={(event) => onDragStart(event, nodeType.type)}
          >
            <div className={`w-2 h-2 rounded-full ${nodeType.color || 'bg-blue-500'}`}></div>
            <span className="text-sm text-gray-700">{nodeType.label}</span>
          </div>
        ))}
      </div>
      
      {/* 底部提示 */}
      <div className="absolute bottom-4 left-4 right-4">
        <div className="text-xs text-gray-500 text-center">
          拖拽节点到画布创建
        </div>
      </div>
    </div>
  )
};

export default NodePanel;
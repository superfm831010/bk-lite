// CustomNodes.tsx
import React from 'react';
import { Handle, Position, NodeProps, Node, useNodeConnections } from '@xyflow/react';
import Icon from '@/components/icon';
import { useTranslation } from '@/utils/i18n';

interface NodeData {
  id: string;
  position: any;
  data: any;
  [key: string]: any
}

type IntentNode = Node<NodeData, 'intent'>;
type ResponseNode = Node<NodeData, 'response'>;
type SlotNode = Node<NodeData, 'slot'>;
type AppNode = IntentNode | ResponseNode | SlotNode;

// 意图节点
export const IntentNode = ({ data, selected }: NodeProps<AppNode>) => {
  const { t } = useTranslation();
  const targetsConnections = useNodeConnections({
    handleType: 'target'
  });
  const sourceConnections = useNodeConnections({
    handleType: 'source'
  });

  return (
    <div className={`
      relative min-w-[140px] bg-white border border-gray-200 
      rounded-lg shadow-sm hover:shadow-md
      transition-all duration-200 ease-in-out
      ${selected 
      ? 'shadow-md' 
      : 'hover:border-gray-300'
    }
    `}>
      {/* 顶部颜色条 */}
      <div className="h-1 bg-blue-500 rounded-t-lg"></div>
      
      {/* 内容区域 */}
      <div className="px-4 py-3">
        <div className="flex items-center space-x-3">
          <div className="flex-shrink-0">
            <div className="w-8 h-8 bg-blue-900 rounded-full flex items-center justify-center">
              <Icon type='tijiaoxiangfa' className='!w-4 !h-4 text-white' />
            </div>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-900 truncate">
              {data?.name || t(`datasets.intentNode`)}
            </p>
            <p className="text-xs text-gray-500">Intent</p>
          </div>
        </div>
      </div>
      
      <Handle 
        type="source" 
        position={Position.Top} 
        isConnectable={sourceConnections.length < 1}
        className="!w-2 !h-2 !bg-blue-700 !border-0 !rounded-full"
      />
      <Handle 
        type="target" 
        position={Position.Bottom} 
        isConnectable={targetsConnections.length < 1}
        className="!w-2 !h-2 !bg-blue-700 !border-0 !rounded-full"
      />
    </div>
  );
};

// 槽节点
export const SlotNode = ({ data, selected }: NodeProps<AppNode>) => {
  const { t } = useTranslation();
  const targetsConnections = useNodeConnections({
    handleType: 'target'
  });
  const sourceConnections = useNodeConnections({
    handleType: 'source'
  });

  return (
    <div className={`
      relative min-w-[140px] bg-white border border-gray-200 
      rounded-lg shadow-sm hover:shadow-md
      transition-all duration-200 ease-in-out
      ${selected 
      ? 'shadow-md' 
      : 'hover:border-gray-300'
    }
    `}>
      {/* 顶部颜色条 */}
      <div className="h-1 bg-emerald-500 rounded-t-lg"></div>
      
      {/* 内容区域 */}
      <div className="px-4 py-3">
        <div className="flex items-center space-x-3">
          <div className="flex-shrink-0">
            <div className="w-8 h-8 bg-emerald-700 rounded-full flex items-center justify-center">
              <Icon type='dangqianbianliang' className='!w-4 !h-4 text-white' />
            </div>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-900 truncate">
              {data?.name || t(`datasets.slotNode`)}
            </p>
            <p className="text-xs text-gray-500">Slot</p>
          </div>
        </div>
      </div>
      
      <Handle 
        type="source" 
        position={Position.Top} 
        isConnectable={sourceConnections.length < 1}
        className="!w-2 !h-2 !bg-emerald-700 !border-0 !rounded-full"
      />
      <Handle 
        type="target" 
        position={Position.Bottom} 
        isConnectable={targetsConnections.length < 1}
        className="!w-2 !h-2 !bg-emerald-700 !border-0 !rounded-full"
      />
    </div>
  );
};


// 响应节点
export const ResponseNode = ({ data, selected }: NodeProps<AppNode>) => {
  const { t } = useTranslation();
  const targetsConnections = useNodeConnections({
    handleType: 'target'
  });
  const sourceConnections = useNodeConnections({
    handleType: 'source'
  });

  return (
    <div className={`
      relative min-w-[140px] bg-white border border-gray-200 
      rounded-lg shadow-sm hover:shadow-md
      transition-all duration-200 ease-in-out
      ${selected 
      ? 'shadow-md' 
      : 'hover:border-gray-300'
    }
    `}>
      {/* 顶部颜色条 */}
      <div className="h-1 bg-purple-500 rounded-t-lg"></div>
      
      {/* 内容区域 */}
      <div className="px-4 py-3">
        <div className="flex items-center space-x-3">
          <div className="flex-shrink-0">
            <div className="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
              <Icon type='huifu-copy' className='!w-4 !h-4 text-white' />
            </div>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-900 truncate">
              {data?.name || t(`datasets.responseNode`)}
            </p>
            <p className="text-xs text-gray-500">Response</p>
          </div>
        </div>
      </div>
      
      <Handle 
        type="source" 
        position={Position.Top} 
        isConnectable={sourceConnections.length < 1}
        className="!w-2 !h-2 !bg-purple-500 !border-0 !rounded-full"
      />
      <Handle 
        type="target" 
        position={Position.Bottom} 
        isConnectable={targetsConnections.length < 1}
        className="!w-2 !h-2 !bg-purple-500 !border-0 !rounded-full"
      />
    </div>
  );
};

export const FormNode = ({ data, selected }: NodeProps<AppNode>) => {
  const { t } = useTranslation();
  const targetsConnections = useNodeConnections({
    handleType: 'target'
  });
  const sourceConnections = useNodeConnections({
    handleType: 'source'
  });

  return (
    <div className={`
      relative min-w-[140px] bg-white border border-gray-200 
      rounded-lg shadow-sm hover:shadow-md
      transition-all duration-200 ease-in-out
      ${selected 
      ? 'shadow-md' 
      : 'hover:border-gray-300'
    }
    `}>
      {/* 顶部颜色条 */}
      <div className="h-1 bg-orange-500 rounded-t-lg"></div>
      
      {/* 内容区域 */}
      <div className="px-4 py-3">
        <div className="flex items-center space-x-3">
          <div className="flex-shrink-0">
            <div className="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center">
              <Icon type='biaodan' className='!w-4 !h-4 text-white' />
            </div>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-900 truncate">
              {data?.name || t(`datasets.formNode`)}
            </p>
            <p className="text-xs text-gray-500">Form</p>
          </div>
        </div>
      </div>
      
      <Handle 
        type="source" 
        position={Position.Top}
        isConnectable={sourceConnections.length < 1}
        className="!w-2 !h-2 !bg-orange-500 !border-0 !rounded-full"
      />
      <Handle 
        type="target" 
        position={Position.Bottom}
        isConnectable={targetsConnections.length < 1}
        className="!w-2 !h-2 !bg-orange-500 !border-0 !rounded-full"
      />
    </div>
  );
};
// CustomNodes.tsx
import React from 'react';
import { Handle, Position, NodeProps, Node, useNodeConnections } from '@xyflow/react';
import Icon from '@/components/icon';

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
  const targetsConnections = useNodeConnections({
    handleType: 'target'
  });
  // const sourceConnections = useNodeConnections({
  //   handleType: 'source'
  // });


  return (
    <div className={`px-4 py-2 shadow-md rounded-md text-[var(--color-text-1)] border-2 ${selected ? 'border-indigo-700' : 'border-indigo-500'}`}>

      {data.label && <div className="font-bold">{data.label}</div>}
      {data.name &&
        <div className="flex justify-center items-center">
          <Icon type='tijiaoxiangfa' className='mr-2 !w-4 !h-4' />
          <span className='text-xs'>{data?.name}</span>
        </div>
      }
      {/* <Handle type="source" position={Position.Top} isConnectable={sourceConnections.length < 1} /> */}
      <Handle type="target" position={Position.Bottom} isConnectable={targetsConnections.length < 1} />
    </div>
  );
};

// 槽节点
export const SlotNode = ({ data, selected }: NodeProps<AppNode>) => {
  const targetsConnections = useNodeConnections({
    handleType: 'target'
  });
  const sourceConnections = useNodeConnections({
    handleType: 'source'
  });

  return (
    <div className={`px-4 py-2 shadow-md rounded-md text-[var(--color-text-1)] border-2 ${selected ? 'border-green-700' : 'border-green-500'}`}>
      {data.label && <div className="font-bold">{data.label}</div>}
      {data.name && <div className="flex justify-center items-center">
        <Icon type='dangqianbianliang' className='mr-2 !w-4 !h-4' />
        <span className='text-xs'>{data?.name}</span>
      </div>}
      <Handle type="source" position={Position.Top} isConnectable={sourceConnections.length < 1} />
      <Handle type="target" position={Position.Bottom} isConnectable={targetsConnections.length < 1} />
    </div>
  );
};


// 响应节点
export const ResponseNode = ({ data, selected }: NodeProps<AppNode>) => {
  const targetsConnections = useNodeConnections({
    handleType: 'target'
  });
  const sourceConnections = useNodeConnections({
    handleType: 'source'
  });

  return (
    <div className={`px-4 py-2 shadow-md rounded-md text-[var(--color-text-1)] border-2 ${selected ? 'border-sky-600' : 'border-sky-400'}`}>
      {data.label && <div className="font-bold">{data.label}</div>}
      {data.name &&
        <div className="flex justify-center items-center">
          <Icon type='huifu-copy' className='mr-2 !w-4 !h-4' />
          <span className='text-xs'>{data?.name}</span>
        </div>
      }
      <Handle type="source" position={Position.Top} isConnectable={sourceConnections.length < 1} />
      <Handle type="target" position={Position.Bottom} isConnectable={targetsConnections.length < 1} />
    </div>
  );
};

export const FormNode = ({ data, selected }: NodeProps<AppNode>) => {
  const targetsConnections = useNodeConnections({
    handleType: 'target'
  });
  const sourceConnections = useNodeConnections({
    handleType: 'source'
  });

  return (
    <div className={`px-4 py-2 shadow-md rounded-md text-[var(--color-text-1)] border-2 ${selected ? 'border-red-700' : 'border-red-500'}`}>
      
      {data.label && <div className="font-bold">{data.label}</div>}
      {data.name &&
        <div className="flex justify-center items-center">
          <Icon type='biaodan' className='mr-2 !w-4 !h-4' />
          <span className='text-xs'>{data?.name}</span>
        </div>
      }
      <Handle type="source" position={Position.Top} isConnectable={sourceConnections.length < 1} />
      <Handle type="target" position={Position.Bottom} isConnectable={targetsConnections.length < 1} />
    </div>
  );
};
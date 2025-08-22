// CustomNodes.tsx
import React from 'react';
import { Handle, Position, NodeProps, Node, useNodeConnections } from '@xyflow/react';

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
    <div className={`px-4 py-2 shadow-md rounded-md bg-blue-500 text-white border-2 ${
      selected ? 'border-blue-700' : 'border-blue-500'
    }`}>
      <div className="font-bold">{data.label}</div>
      {data.id && <div className="text-xs">意图: {data?.id}</div>}
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
    <div className={`px-4 py-2 shadow-md rounded-md bg-green-500 text-white border-2 ${
      selected ? 'border-green-700' : 'border-green-500'
    }`}>
      <div className="font-bold">{data.label}</div>
      {data.id && <div className="text-xs">槽: {data?.id}</div>}
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
    <div className={`px-4 py-2 shadow-md rounded-md bg-purple-500 text-white border-2 ${
      selected ? 'border-purple-700' : 'border-purple-500'
    }`}>
      <div className="font-bold">{data.label}</div>
      {data.id && <div className="text-xs">响应: {data?.id}</div>}
      <Handle type="source" position={Position.Top} isConnectable={sourceConnections.length < 1} />
      <Handle type="target" position={Position.Bottom} isConnectable={targetsConnections.length < 1} />
    </div>
  );
};
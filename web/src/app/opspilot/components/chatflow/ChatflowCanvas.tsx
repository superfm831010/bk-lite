'use client';

import React, { useCallback, useMemo } from 'react';
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Connection,
  Edge,
  Node,
  NodeTypes,
  MarkerType,
  Handle,
  Position,
  BackgroundVariant,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { useTranslation } from '@/utils/i18n';
import Icon from '@/components/icon';

// 节点类型定义
interface ChatflowNodeData {
  label: string;
  type: string;
  config?: any;
}

// 定时触发节点
const CeleryNode = ({ data }: { data: ChatflowNodeData; id: string }) => {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-white border-2 border-blue-400 min-w-[120px]">
      <div className="flex items-center">
        <Icon type="time" className="text-blue-500 mr-2" />
        <div className="font-semibold text-blue-700">{data.label}</div>
      </div>
      <Handle type="source" position={Position.Right} className="w-3 h-3 !bg-blue-500" />
    </div>
  );
};

// HTTP请求节点
const HttpNode = ({ data }: { data: ChatflowNodeData; id: string }) => {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-white border-2 border-cyan-400 min-w-[120px]">
      <div className="flex items-center">
        <Icon type="api" className="text-cyan-500 mr-2" />
        <div className="font-semibold text-cyan-700">{data.label}</div>
      </div>
      <Handle type="target" position={Position.Left} className="w-3 h-3 !bg-cyan-500" />
      <Handle type="source" position={Position.Right} className="w-3 h-3 !bg-cyan-500" />
    </div>
  );
};

// REST API节点
const RestfulNode = ({ data }: { data: ChatflowNodeData; id: string }) => {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-white border-2 border-green-400 min-w-[120px]">
      <div className="flex items-center">
        <Icon type="link" className="text-green-500 mr-2" />
        <div className="font-semibold text-green-700">{data.label}</div>
      </div>
      <Handle type="target" position={Position.Left} className="w-3 h-3 !bg-green-500" />
    </div>
  );
};

// OpenAI API节点
const OpenaiNode = ({ data }: { data: ChatflowNodeData; id: string }) => {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-white border-2 border-emerald-400 min-w-[120px]">
      <div className="flex items-center">
        <Icon type="openai" className="text-emerald-500 mr-2" />
        <div className="font-semibold text-emerald-700">{data.label}</div>
      </div>
      <Handle type="target" position={Position.Left} className="w-3 h-3 !bg-emerald-500" />
    </div>
  );
};

// 智能体节点
const AgentsNode = ({ data }: { data: ChatflowNodeData; id: string }) => {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-white border-2 border-purple-400 min-w-[120px]">
      <div className="flex items-center">
        <Icon type="theory" className="text-purple-500 mr-2" />
        <div className="font-semibold text-purple-700">{data.label}</div>
      </div>
      <Handle type="target" position={Position.Left} className="w-3 h-3 !bg-purple-500" />
      <Handle type="source" position={Position.Right} className="w-3 h-3 !bg-purple-500" />
    </div>
  );
};

// Prompt追加节点
const PromptNode = ({ data }: { data: ChatflowNodeData; id: string }) => {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-white border-2 border-indigo-400 min-w-[120px]">
      <div className="flex items-center">
        <Icon type="edit" className="text-indigo-500 mr-2" />
        <div className="font-semibold text-indigo-700">{data.label}</div>
      </div>
      <Handle type="target" position={Position.Left} className="w-3 h-3 !bg-indigo-500" />
      <Handle type="source" position={Position.Right} className="w-3 h-3 !bg-indigo-500" />
    </div>
  );
};

// 知识追加节点
const KnowledgeNode = ({ data }: { data: ChatflowNodeData; id: string }) => {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-white border-2 border-yellow-400 min-w-[120px]">
      <div className="flex items-center">
        <Icon type="book" className="text-yellow-500 mr-2" />
        <div className="font-semibold text-yellow-700">{data.label}</div>
      </div>
      <Handle type="target" position={Position.Left} className="w-3 h-3 !bg-yellow-500" />
      <Handle type="source" position={Position.Right} className="w-3 h-3 !bg-yellow-500" />
    </div>
  );
};

// 条件分支节点
const ConditionNode = ({ data }: { data: ChatflowNodeData; id: string }) => {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-white border-2 border-red-400 min-w-[120px]">
      <div className="flex items-center">
        <Icon type="branch" className="text-red-500 mr-2" />
        <div className="font-semibold text-red-700">{data.label}</div>
      </div>
      <Handle type="target" position={Position.Left} className="w-3 h-3 !bg-red-500" />
      <Handle type="source" position={Position.Right} className="w-3 h-3 !bg-red-500 translate-y-[-8px]" />
      <Handle type="source" position={Position.Right} className="w-3 h-3 !bg-red-500 translate-y-[8px]" />
    </div>
  );
};

interface ChatflowCanvasProps {
  value?: any;
  onChange?: (value: any) => void;
}

const ChatflowCanvas: React.FC<ChatflowCanvasProps> = ({ value, onChange }) => {
  const { t } = useTranslation();
  
  // 初始节点 - 使用实际有用的节点类型
  const initialNodes: Node[] = [
    {
      id: 'celery-1',
      type: 'celery',
      position: { x: 100, y: 200 },
      data: { label: t('chatflow.celery'), type: 'celery' },
    },
    {
      id: 'agents-1',
      type: 'agents',
      position: { x: 400, y: 200 },
      data: { label: t('chatflow.agents'), type: 'agents' },
    },
    {
      id: 'http-1',
      type: 'http',
      position: { x: 700, y: 200 },
      data: { label: t('chatflow.http'), type: 'http' },
    },
  ];

  // 初始连线
  const initialEdges: Edge[] = [
    {
      id: 'e1-2',
      source: 'celery-1',
      target: 'agents-1',
      markerEnd: {
        type: MarkerType.ArrowClosed,
        width: 20,
        height: 20,
        color: '#b1b1b7',
      },
    },
    {
      id: 'e2-3',
      source: 'agents-1',
      target: 'http-1',
      markerEnd: {
        type: MarkerType.ArrowClosed,
        width: 20,
        height: 20,
        color: '#b1b1b7',
      },
    },
  ];

  const [nodes, , onNodesChange] = useNodesState(value?.nodes || initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(value?.edges || initialEdges);

  // 节点类型定义 - 移除未使用的节点类型
  const nodeTypes: NodeTypes = useMemo(() => ({
    celery: CeleryNode,
    http: HttpNode,
    restful: RestfulNode,
    openai: OpenaiNode,
    agents: AgentsNode,
    prompt: PromptNode,
    knowledge: KnowledgeNode,
    condition: ConditionNode,
  }), []);

  // 连接节点
  const onConnect = useCallback(
    (params: Connection) => {
      const newEdge = {
        ...params,
        markerEnd: {
          type: MarkerType.ArrowClosed,
          width: 20,
          height: 20,
          color: '#b1b1b7',
        },
      };
      setEdges((eds) => addEdge(newEdge, eds));
    },
    [setEdges]
  );

  // 通知父组件数据变化
  React.useEffect(() => {
    if (onChange) {
      onChange({ nodes, edges });
    }
  }, [nodes, edges, onChange]);

  return (
    <div className="w-full h-[600px] border rounded-lg overflow-hidden">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        fitView
        attributionPosition="bottom-left"
      >
        <MiniMap />
        <Controls />
        <Background variant={BackgroundVariant.Dots} gap={12} size={1} />
      </ReactFlow>
    </div>
  );
};

export default ChatflowCanvas;
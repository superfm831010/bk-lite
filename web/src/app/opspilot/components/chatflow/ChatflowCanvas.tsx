'use client';

import React, { useCallback, useState, useMemo } from 'react';
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
  EdgeTypes,
  MarkerType,
  Handle,
  Position,
  BackgroundVariant,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { Modal, Select, Form, Input } from 'antd';
import { useTranslation } from '@/utils/i18n';
import Icon from '@/components/icon';

const { Option } = Select;

// 节点类型定义
interface ChatflowNodeData {
  label: string;
  type: 'input' | 'output' | 'agent' | 'action' | 'condition' | 'variable';
  config?: any;
}

// 自定义输入节点
const InputNode = ({ data }: { data: ChatflowNodeData; id: string }) => {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-white border-2 border-blue-400 min-w-[120px]">
      <div className="flex items-center">
        <Icon type="jishuqianyan" className="text-blue-500 mr-2" />
        <div className="font-semibold text-blue-700">{data.label}</div>
      </div>
      <Handle type="source" position={Position.Right} className="w-3 h-3 !bg-blue-500" />
    </div>
  );
};

// 自定义输出节点
const OutputNode = ({ data }: { data: ChatflowNodeData; id: string }) => {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-white border-2 border-green-400 min-w-[120px]">
      <div className="flex items-center">
        <Icon type="jishuqianyan" className="text-green-500 mr-2" />
        <div className="font-semibold text-green-700">{data.label}</div>
      </div>
      <Handle type="target" position={Position.Left} className="w-3 h-3 !bg-green-500" />
    </div>
  );
};

// 自定义智能体节点
const AgentNode = ({ data }: { data: ChatflowNodeData; id: string }) => {
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

// 自定义动作节点
const ActionNode = ({ data }: { data: ChatflowNodeData; id: string }) => {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-white border-2 border-orange-400 min-w-[120px]">
      <div className="flex items-center">
        <Icon type="tool" className="text-orange-500 mr-2" />
        <div className="font-semibold text-orange-700">{data.label}</div>
      </div>
      <Handle type="target" position={Position.Left} className="w-3 h-3 !bg-orange-500" />
      <Handle type="source" position={Position.Right} className="w-3 h-3 !bg-orange-500" />
    </div>
  );
};

// 自定义连线中间的添加按钮
const CustomEdge = ({ id, sourceX, sourceY, targetX, targetY, markerEnd, onAddNode }: any) => {
  const edgePath = `M${sourceX},${sourceY} L${targetX},${targetY}`;
  const midX = (sourceX + targetX) / 2;
  const midY = (sourceY + targetY) / 2;

  return (
    <>
      <path id={id} d={edgePath} stroke="#b1b1b7" strokeWidth={2} fill="none" markerEnd={markerEnd} />
      <circle
        cx={midX}
        cy={midY}
        r="12"
        fill="white"
        stroke="#b1b1b7"
        strokeWidth="2"
        className="cursor-pointer hover:fill-blue-50"
        onClick={() => onAddNode(midX, midY, id)}
      />
      <text
        x={midX}
        y={midY + 2}
        textAnchor="middle"
        fontSize="12"
        fill="#666"
        className="cursor-pointer pointer-events-none"
      >
        +
      </text>
    </>
  );
};

interface ChatflowCanvasProps {
  value?: any;
  onChange?: (value: any) => void;
}

const ChatflowCanvas: React.FC<ChatflowCanvasProps> = ({ value, onChange }) => {
  const { t } = useTranslation();
  
  // 初始节点
  const initialNodes: Node[] = [
    {
      id: 'input-1',
      type: 'input',
      position: { x: 100, y: 200 },
      data: { label: t('chatflow.input'), type: 'input' },
    },
    {
      id: 'agent-1',
      type: 'agent',
      position: { x: 400, y: 200 },
      data: { label: t('chatflow.agent'), type: 'agent' },
    },
    {
      id: 'output-1',
      type: 'output',
      position: { x: 700, y: 200 },
      data: { label: t('chatflow.output'), type: 'output' },
    },
  ];

  // 初始连线
  const initialEdges: Edge[] = [
    {
      id: 'e1-2',
      source: 'input-1',
      target: 'agent-1',
      type: 'custom',
      markerEnd: {
        type: MarkerType.ArrowClosed,
        width: 20,
        height: 20,
        color: '#b1b1b7',
      },
    },
    {
      id: 'e2-3',
      source: 'agent-1',
      target: 'output-1',
      type: 'custom',
      markerEnd: {
        type: MarkerType.ArrowClosed,
        width: 20,
        height: 20,
        color: '#b1b1b7',
      },
    },
  ];

  const [nodes, setNodes, onNodesChange] = useNodesState(value?.nodes || initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(value?.edges || initialEdges);
  const [isAddNodeModalVisible, setIsAddNodeModalVisible] = useState(false);
  const [newNodePosition, setNewNodePosition] = useState({ x: 0, y: 0 });
  const [selectedEdgeId, setSelectedEdgeId] = useState<string>('');
  const [form] = Form.useForm();

  // 节点类型定义
  const nodeTypes: NodeTypes = useMemo(() => ({
    input: InputNode,
    output: OutputNode,
    agent: AgentNode,
    action: ActionNode,
  }), []);

  // 边类型定义
  const edgeTypes: EdgeTypes = useMemo(() => ({
    custom: (props) => <CustomEdge {...props} onAddNode={handleAddNodeToEdge} />,
  }), []);

  // 连接节点
  const onConnect = useCallback(
    (params: Connection) => {
      const newEdge = {
        ...params,
        type: 'custom',
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

  // 在连线中间添加节点
  const handleAddNodeToEdge = useCallback((x: number, y: number, edgeId: string) => {
    setNewNodePosition({ x: x - 60, y: y - 20 }); // 调整位置使节点居中
    setSelectedEdgeId(edgeId);
    setIsAddNodeModalVisible(true);
  }, []);

  // 添加新节点
  const handleAddNode = useCallback(() => {
    form.validateFields().then((values) => {
      const nodeId = `${values.type}-${Date.now()}`;
      const newNode: Node = {
        id: nodeId,
        type: values.type,
        position: newNodePosition,
        data: { 
          label: values.label || t(`chatflow.${values.type}`), 
          type: values.type,
          config: values.config 
        },
      };

      // 找到要分割的边
      const targetEdge = edges.find(edge => edge.id === selectedEdgeId);
      if (targetEdge) {
        // 移除原边
        setEdges((eds) => eds.filter(edge => edge.id !== selectedEdgeId));
        
        // 添加两条新边
        const edge1: Edge = {
          id: `${targetEdge.source}-${nodeId}`,
          source: targetEdge.source,
          target: nodeId,
          type: 'custom',
          markerEnd: {
            type: MarkerType.ArrowClosed,
            width: 20,
            height: 20,
            color: '#b1b1b7',
          },
        };
        
        const edge2: Edge = {
          id: `${nodeId}-${targetEdge.target}`,
          source: nodeId,
          target: targetEdge.target,
          type: 'custom',
          markerEnd: {
            type: MarkerType.ArrowClosed,
            width: 20,
            height: 20,
            color: '#b1b1b7',
          },
        };
        
        setEdges((eds) => [...eds, edge1, edge2]);
      }

      setNodes((nds) => [...nds, newNode]);
      setIsAddNodeModalVisible(false);
      form.resetFields();
    });
  }, [form, newNodePosition, selectedEdgeId, edges, setEdges, setNodes, t]);

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
        edgeTypes={edgeTypes}
        fitView
        attributionPosition="bottom-left"
      >
        <MiniMap />
        <Controls />
        <Background variant={BackgroundVariant.Dots} gap={12} size={1} />
      </ReactFlow>

      <Modal
        title={t('chatflow.addNode')}
        open={isAddNodeModalVisible}
        onOk={handleAddNode}
        onCancel={() => {
          setIsAddNodeModalVisible(false);
          form.resetFields();
        }}
        okText={t('common.confirm')}
        cancelText={t('common.cancel')}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="type"
            label={t('chatflow.nodeProperties.type')}
            rules={[{ required: true, message: t('common.selectMsg') + t('chatflow.nodeProperties.type') }]}
          >
            <Select placeholder={t('common.selectMsg') + t('chatflow.nodeProperties.type')}>
              <Option value="agent">{t('chatflow.agent')}</Option>
              <Option value="action">{t('chatflow.action')}</Option>
            </Select>
          </Form.Item>
          
          <Form.Item
            name="label"
            label={t('chatflow.nodeProperties.name')}
            rules={[{ required: true, message: t('common.inputMsg') + t('chatflow.nodeProperties.name') }]}
          >
            <Input placeholder={t('common.inputMsg') + t('chatflow.nodeProperties.name')} />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default ChatflowCanvas;
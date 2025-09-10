'use client';

import React, { useCallback, useState, useMemo, useRef, useEffect } from 'react';
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
  Handle,
  Position,
  BackgroundVariant,
  ReactFlowProvider,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { Modal, message } from 'antd';
import { useTranslation } from '@/utils/i18n';
import Icon from '@/components/icon';
import NodeConfigDrawer from './NodeConfigDrawer';
import styles from './ChatflowEditor.module.scss';

// 节点类型定义
interface ChatflowNodeData {
  label: string;
  type: 'timeTrigger' | 'restfulApi' | 'openaiApi' | 'agents' | 'ifCondition' | 'httpRequest' | 'promptAppend' | 'knowledgeAppend';
  config?: any;
  description?: string;
}

const nodeConfig = {
  timeTrigger: { icon: 'a-icon-dingshichufa1x', color: 'green' },
  restfulApi: { icon: 'RESTfulAPI', color: 'purple' },
  openaiApi: { icon: 'icon-test2', color: 'blue' },
  agents: { icon: 'zhinengti', color: 'orange' },
  ifCondition: { icon: 'tiaojianfenzhi', color: 'yellow' },
  httpRequest: { icon: 'HTTP', color: 'cyan' },
  promptAppend: { icon: 'prompt_o', color: 'purple' },
  knowledgeAppend: { icon: 'zhishiku2', color: 'green' },
};

// 通用节点组件
const BaseNode = ({ 
  data, 
  id, 
  selected, 
  onConfig, 
  icon, 
  color = 'blue',
  hasInput = false,
  hasOutput = true,
  hasMultipleOutputs = false
}: { 
  data: ChatflowNodeData; 
  id: string; 
  selected?: boolean;
  onConfig: (id: string) => void;
  icon: string;
  color?: string;
  hasInput?: boolean;
  hasOutput?: boolean;
  hasMultipleOutputs?: boolean;
}) => {
  const handleColorClasses = {
    green: '!bg-green-500',
    purple: '!bg-purple-500',
    blue: '!bg-blue-500',
    orange: '!bg-orange-500', 
    yellow: '!bg-yellow-500',
    cyan: '!bg-cyan-500',
  };

  // 点击节点处理函数
  const handleNodeClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    onConfig(id);
  };

  return (
    <div 
      className={`${styles.nodeContainer} ${selected ? styles.selected : ''} group relative cursor-pointer`}
      onClick={handleNodeClick}
    >
      {hasInput && (
        <Handle 
          type="target" 
          position={Position.Left} 
          className={`w-2.5 h-2.5 ${handleColorClasses[color as keyof typeof handleColorClasses] || handleColorClasses.blue} !border-2 !border-white shadow-md`} 
        />
      )}
      
      <div className={styles.nodeHeader}>
        <Icon type={icon} className={`${styles.nodeIcon} text-${color}-500`} />
        <span className={styles.nodeTitle}>{data.label}</span>
      </div>
      
      <div className={styles.nodeContent}>
        <p className={styles.nodeDescription}>
          {data.config?.description || data.description || ''}
        </p>
      </div>
      
      {hasOutput && !hasMultipleOutputs && (
        <Handle 
          type="source" 
          position={Position.Right} 
          className={`w-2.5 h-2.5 ${handleColorClasses[color as keyof typeof handleColorClasses] || handleColorClasses.blue} !border-2 !border-white shadow-md`} 
        />
      )}
      
      {hasMultipleOutputs && (
        <>
          <Handle 
            type="source" 
            position={Position.Right} 
            className={`w-2.5 h-2.5 ${handleColorClasses[color as keyof typeof handleColorClasses] || handleColorClasses.blue} !border-2 !border-white shadow-md`} 
            id="true" 
          />
          <Handle 
            type="source" 
            position={Position.Bottom} 
            className={`w-2.5 h-2.5 ${handleColorClasses[color as keyof typeof handleColorClasses] || handleColorClasses.blue} !border-2 !border-white shadow-md`} 
            id="false" 
          />
        </>
      )}
    </div>
  );
};

// 具体节点组件
const TimeTriggerNode = (props: any) => (
  <BaseNode {...props} icon={nodeConfig.timeTrigger.icon} color={nodeConfig.timeTrigger.color} hasOutput={true} />
);

const RestfulApiNode = (props: any) => (
  <BaseNode {...props} icon={nodeConfig.restfulApi.icon} color={nodeConfig.restfulApi.color} hasOutput={true} />
);

const OpenAIApiNode = (props: any) => (
  <BaseNode {...props} icon={nodeConfig.openaiApi.icon} color={nodeConfig.openaiApi.color} hasOutput={true} />
);

const AgentsNode = (props: any) => (
  <BaseNode {...props} icon={nodeConfig.agents.icon} color={nodeConfig.agents.color} hasInput={true} hasOutput={true} />
);

const HttpRequestNode = (props: any) => (
  <BaseNode {...props} icon={nodeConfig.httpRequest.icon} color={nodeConfig.httpRequest.color} hasInput={true} hasOutput={true} />
);

const IfConditionNode = (props: any) => (
  <BaseNode {...props} icon={nodeConfig.ifCondition.icon} color={nodeConfig.ifCondition.color} hasInput={true} hasMultipleOutputs={true} />
);

const PromptAppendNode = (props: any) => (
  <BaseNode {...props} icon={nodeConfig.promptAppend.icon} color={nodeConfig.promptAppend.color} hasInput={true} hasOutput={true} />
);

const KnowledgeAppendNode = (props: any) => (
  <BaseNode {...props} icon={nodeConfig.knowledgeAppend.icon} color={nodeConfig.knowledgeAppend.color} hasInput={true} hasOutput={true} />
);

interface ChatflowEditorProps {
  onSave?: (nodes: Node[], edges: Edge[]) => void;
  initialData?: { nodes: Node[], edges: Edge[] };
}

const ChatflowEditor: React.FC<ChatflowEditorProps> = ({ onSave, initialData }) => {
  const { t } = useTranslation();
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const [reactFlowInstance, setReactFlowInstance] = useState<any>(null);
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [isConfigDrawerVisible, setIsConfigDrawerVisible] = useState(false);

  // 初始节点 - 空画布
  const getInitialNodes = useCallback((): Node[] => [], []);

  const getInitialEdges = useCallback((): Edge[] => [], []);

  // 使用外部传入的 initialData 或默认数据
  const [nodes, setNodes, onNodesChange] = useNodesState(
    initialData?.nodes?.length ? initialData.nodes : getInitialNodes()
  );
  const [edges, setEdges, onEdgesChange] = useEdgesState(
    initialData?.edges?.length ? initialData.edges : getInitialEdges()
  );

  // 添加一个 ref 来跟踪是否正在同步外部数据，避免循环调用
  const isSyncingExternalData = useRef(false);
  
  // 监听 initialData 变化，当外部数据更新时同步更新内部状态
  useEffect(() => {
    if (initialData && !isSyncingExternalData.current) {
      isSyncingExternalData.current = true;
      setNodes(initialData.nodes || []);
      setEdges(initialData.edges || []);
      // 延迟重置标志，确保状态更新完成
      setTimeout(() => {
        isSyncingExternalData.current = false;
      }, 0);
    }
  }, [initialData, setNodes, setEdges]);

  // 当 nodes 或 edges 发生变化时，自动调用 onSave 同步数据
  // 添加防抖和初始化标志，避免无限循环
  const [isInitialized, setIsInitialized] = useState(false);
  
  useEffect(() => {
    // 如果正在同步外部数据，则不触发 onSave
    if (isSyncingExternalData.current) {
      return;
    }
    
    // 首次加载时标记为已初始化
    if (!isInitialized) {
      setIsInitialized(true);
      return;
    }
    
    // 只有在初始化完成后且不是同步外部数据时才调用 onSave
    if (isInitialized && onSave) {
      onSave(nodes, edges);
    }
  }, [nodes, edges, onSave, isInitialized]);

  // 节点删除处理 - 提前声明
  const handleDeleteNode = useCallback((nodeId: string) => {
    Modal.confirm({
      title: t('chatflow.messages.deleteConfirm'),
      onOk: () => {
        setNodes((nds) => nds.filter((n) => n.id !== nodeId));
        setEdges((eds) => eds.filter((e) => e.source !== nodeId && e.target !== nodeId));
        setIsConfigDrawerVisible(false);
        message.success(t('chatflow.messages.nodeDeleted'));
      }
    });
  }, [setNodes, setEdges, t]);

  // 节点配置处理 - 提前声明
  const handleConfigNode = useCallback((nodeId: string) => {
    console.log('点击节点配置:', nodeId); // 添加调试日志
    const node = nodes.find(n => n.id === nodeId);
    if (node) {
      console.log('找到节点:', node); // 添加调试日志
      setSelectedNode(node);
      setIsConfigDrawerVisible(true);
    } else {
      console.log('未找到节点:', nodeId); // 添加调试日志
    }
  }, [nodes]);

  // 自定义节点类型
  const nodeTypes: NodeTypes = useMemo(() => {
    const createNodeComponent = (Component: React.ComponentType<any>) => {
      const NodeComponentWithProps = (props: any) => (
        <Component 
          {...props} 
          onDelete={handleDeleteNode} 
          onConfig={handleConfigNode}
        />
      );
      NodeComponentWithProps.displayName = `NodeComponent(${Component.displayName || Component.name})`;
      return NodeComponentWithProps;
    };

    return {
      timeTrigger: createNodeComponent(TimeTriggerNode),
      restfulApi: createNodeComponent(RestfulApiNode),
      openaiApi: createNodeComponent(OpenAIApiNode),
      agents: createNodeComponent(AgentsNode),
      ifCondition: createNodeComponent(IfConditionNode),
      httpRequest: createNodeComponent(HttpRequestNode),
      promptAppend: createNodeComponent(PromptAppendNode),
      knowledgeAppend: createNodeComponent(KnowledgeAppendNode),
    };
  }, [handleDeleteNode, handleConfigNode]);

  // ReactFlow 实例初始化
  const onInit = useCallback((instance: any) => {
    setReactFlowInstance(instance);
  }, []);

  // 处理连接
  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  // 拖拽处理
  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault();
      
      try {
        const reactFlowBounds = reactFlowWrapper.current?.getBoundingClientRect();
        const type = event.dataTransfer.getData('application/reactflow');

        if (!type || !reactFlowBounds || !reactFlowInstance) {
          return;
        }

        // 计算相对于 ReactFlow 容器的位置
        const dropPosition = {
          x: event.clientX - reactFlowBounds.left,
          y: event.clientY - reactFlowBounds.top,
        };

        // 将屏幕坐标转换为流程图坐标
        const flowPosition = reactFlowInstance.screenToFlowPosition(dropPosition);

        // 获取当前视口信息
        const viewport = reactFlowInstance.getViewport();
        const zoom = viewport.zoom;
        
        // 计算容器的可视区域范围（考虑缩放和平移）
        const containerWidth = reactFlowBounds.width;
        const containerHeight = reactFlowBounds.height;
        
        // 估算节点大小（默认节点大小约为 160x80）
        const nodeWidth = 160;
        const nodeHeight = 80;
        
        // 计算可视区域的边界（流程图坐标系）
        const visibleBounds = {
          left: -viewport.x / zoom,
          top: -viewport.y / zoom,
          right: (-viewport.x + containerWidth) / zoom,
          bottom: (-viewport.y + containerHeight) / zoom,
        };

        // 确保节点在可视区域内
        flowPosition.x = Math.max(
          visibleBounds.left + 20, // 左边距
          Math.min(flowPosition.x, visibleBounds.right - nodeWidth - 20) // 右边距
        );
        
        flowPosition.y = Math.max(
          visibleBounds.top + 20, // 上边距
          Math.min(flowPosition.y, visibleBounds.bottom - nodeHeight - 20) // 下边距
        );

        const getNodeLabel = (nodeType: string) => {
          try {
            return t(`chatflow.${nodeType}`) || nodeType;
          } catch {
            return nodeType;
          }
        };

        const newNode: Node = {
          id: `${type}-${Date.now()}`,
          type,
          position: flowPosition,
          data: { 
            label: getNodeLabel(type),
            type: type as ChatflowNodeData['type'],
            config: {},
            description: ''
          },
        };

        setNodes((nds) => nds.concat(newNode));
        message.success(`成功添加${getNodeLabel(type)}节点`);
        
      } catch (error) {
        console.error('拖拽放置错误:', error);
        message.error('拖拽失败');
      }
    },
    [reactFlowInstance, setNodes, t]
  );

  // 保存配置
  const handleSaveConfig = useCallback((nodeId: string, values: any) => {
    const { name, description, ...config } = values;
    
    setNodes((nds) => 
      nds.map((node) => 
        node.id === nodeId 
          ? { 
            ...node, 
            data: { 
              ...node.data, 
              label: name || node.data.label,
              description,
              config 
            } 
          }
          : node
      )
    );
    setIsConfigDrawerVisible(false);
  }, [setNodes]);

  return (
    <div className={styles.chatflowEditor}>
      <div className={styles.flowContainer} ref={reactFlowWrapper}>
        <ReactFlowProvider>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onInit={onInit}
            onDrop={onDrop}
            onDragOver={onDragOver}
            nodeTypes={nodeTypes}
            fitView
            attributionPosition="bottom-left"
          >
            <MiniMap />
            <Controls />
            <Background variant={BackgroundVariant.Dots} gap={12} size={1} />
          </ReactFlow>
        </ReactFlowProvider>
      </div>

      {/* 节点配置侧边栏 */}
      <NodeConfigDrawer
        visible={isConfigDrawerVisible}
        node={selectedNode}
        onClose={() => setIsConfigDrawerVisible(false)}
        onSave={handleSaveConfig}
        onDelete={handleDeleteNode}
      />
    </div>
  );
};

export default ChatflowEditor;
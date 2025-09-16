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

// 节点类型定义 - 使用索引签名使其兼容 ReactFlow 的 Node 类型
interface ChatflowNodeData {
  label: string;
  type: 'celery' | 'restful' | 'openai' | 'agents' | 'condition' | 'http' | 'prompt' | 'knowledge';
  config?: any;
  description?: string;
  [key: string]: unknown; // 添加索引签名以兼容 Record<string, unknown>
}

// 类型守卫函数，用于检查节点是否为 ChatflowNode
const isChatflowNode = (node: Node): node is ChatflowNode => {
  return node.data && 
         typeof (node.data as any).label === 'string' && 
         typeof (node.data as any).type === 'string';
}

// 扩展Node类型以包含具体的data类型
interface ChatflowNode extends Node {
  data: ChatflowNodeData;
}

const nodeConfig = {
  celery: { icon: 'a-icon-dingshichufa1x', color: 'green' },
  restful: { icon: 'RESTfulAPI', color: 'purple' },
  openai: { icon: 'icon-test2', color: 'blue' },
  agents: { icon: 'zhinengti', color: 'orange' },
  condition: { icon: 'tiaojianfenzhi', color: 'yellow' },
  http: { icon: 'HTTP', color: 'cyan' },
  prompt: { icon: 'prompt_o', color: 'purple' },
  knowledge: { icon: 'zhishiku2', color: 'green' },
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
  const { t } = useTranslation();
  
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

  // 格式化配置信息显示
  const formatConfigInfo = () => {
    const config = data.config;
    
    if (!config || Object.keys(config).length === 0) {
      return t('chatflow.notConfigured');
    }

    switch (data.type) {
      case 'celery':
        if (config.frequency) {
          const frequencyMap: { [key: string]: string } = {
            'daily': t('chatflow.daily'),
            'weekly': t('chatflow.weekly'), 
            'monthly': t('chatflow.monthly')
          };
          const timeStr = config.time ? ` ${config.time.format ? config.time.format('HH:mm') : config.time}` : '';
          const weekdayStr = config.weekday !== undefined ? ` ${t('chatflow.weekday')}${config.weekday}` : '';
          const dayStr = config.day ? ` ${config.day}${t('chatflow.day')}` : '';
          
          return `${frequencyMap[config.frequency] || config.frequency}${timeStr}${weekdayStr}${dayStr}`;
        }
        return t('chatflow.triggerFrequency') + ': --';

      case 'http':
        if (config.method && config.url) {
          return `${config.method} ${config.url}`;
        } else if (config.method) {
          return config.method;
        } else if (config.url) {
          return config.url;
        }
        return t('chatflow.httpMethod') + ': --';

      case 'agents':
        if (config.agent) {
          // 优先使用保存的智能体名称，如果没有则显示ID
          const agentDisplayName = config.agentName || config.agent;
          return t('chatflow.selectedAgent') + `: ${agentDisplayName}`;
        }
        return t('chatflow.selectedAgent') + ': --';

      case 'condition':
        if (config.conditionField && config.conditionOperator && config.conditionValue) {
          return `${config.conditionField} ${config.conditionOperator} ${config.conditionValue}`;
        }
        return t('chatflow.condition') + ': --';

      case 'prompt':
        if (config.prompt) {
          const previewText = config.prompt.length > 20 ? 
            config.prompt.substring(0, 20) + '...' : 
            config.prompt;
          return `Prompt: ${previewText}`;
        }
        return 'Prompt: --';

      case 'knowledge':
        // 这里可以显示上传的文件数量或知识库信息
        return t('chatflow.knowledgeBase') + ': --';

      case 'restful':
      case 'openai':
        return t('chatflow.apiInterface');

      default:
        return t('chatflow.notConfigured');
    }
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
        <div className={styles.nodeConfigInfo}>
          {formatConfigInfo()}
        </div>
        {data.description && (
          <p className={styles.nodeDescription}>
            {data.description}
          </p>
        )}
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
          {/* True 输出点 - 右侧上方，绿色 */}
          <Handle 
            type="source" 
            position={Position.Right} 
            className="w-2.5 h-2.5 !bg-green-500 !border-2 !border-white shadow-md" 
            id="true"
            style={{ top: '30%' }}
          />
          {/* False 输出点 - 右侧下方，红色 */}
          <Handle 
            type="source" 
            position={Position.Right} 
            className="w-2.5 h-2.5 !bg-red-500 !border-2 !border-white shadow-md" 
            id="false"
            style={{ top: '70%' }}
          />
        </>
      )}
    </div>
  );
};

// 具体节点组件
const TimeTriggerNode = (props: any) => (
  <BaseNode {...props} icon={nodeConfig.celery.icon} color={nodeConfig.celery.color} hasOutput={true} />
);

const RestfulApiNode = (props: any) => (
  <BaseNode {...props} icon={nodeConfig.restful.icon} color={nodeConfig.restful.color} hasOutput={true} />
);

const OpenAIApiNode = (props: any) => (
  <BaseNode {...props} icon={nodeConfig.openai.icon} color={nodeConfig.openai.color} hasOutput={true} />
);

const AgentsNode = (props: any) => (
  <BaseNode {...props} icon={nodeConfig.agents.icon} color={nodeConfig.agents.color} hasInput={true} hasOutput={true} />
);

const HttpRequestNode = (props: any) => (
  <BaseNode {...props} icon={nodeConfig.http.icon} color={nodeConfig.http.color} hasInput={true} hasOutput={true} />
);

const IfConditionNode = (props: any) => (
  <BaseNode 
    {...props} 
    icon={nodeConfig.condition.icon} 
    color={nodeConfig.condition.color} 
    hasInput={true} 
    hasOutput={false}
    hasMultipleOutputs={true} 
  />
);

const PromptAppendNode = (props: any) => (
  <BaseNode {...props} icon={nodeConfig.prompt.icon} color={nodeConfig.prompt.color} hasInput={true} hasOutput={true} />
);

const KnowledgeAppendNode = (props: any) => (
  <BaseNode {...props} icon={nodeConfig.knowledge.icon} color={nodeConfig.knowledge.color} hasInput={true} hasOutput={true} />
);

interface ChatflowEditorProps {
  onSave?: (nodes: Node[], edges: Edge[]) => void;
  initialData?: { nodes: Node[], edges: Edge[] } | null;
}

const ChatflowEditor: React.FC<ChatflowEditorProps> = ({ onSave, initialData }) => {
  const { t } = useTranslation();
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const [reactFlowInstance, setReactFlowInstance] = useState<any>(null);
  const [selectedNode, setSelectedNode] = useState<ChatflowNode | null>(null);
  const [isConfigDrawerVisible, setIsConfigDrawerVisible] = useState(false);
  const [selectedNodes, setSelectedNodes] = useState<Node[]>([]);
  const [selectedEdges, setSelectedEdges] = useState<Edge[]>([]);
  const [viewport, setViewport] = useState({ x: 0, y: 0, zoom: 0.8 });

  // 使用外部传入的 initialData 或默认数据
  const [nodes, setNodes, onNodesChange] = useNodesState(
    initialData?.nodes && Array.isArray(initialData.nodes) ? initialData.nodes : []
  );
  const [edges, setEdges, onEdgesChange] = useEdgesState(
    initialData?.edges && Array.isArray(initialData.edges) ? initialData.edges : []
  );

  // 添加一个 ref 来跟踪是否正在同步外部数据，避免循环调用
  const isSyncingExternalData = useRef(false);
  
  // 监听 initialData 变化，当外部数据更新时同步更新内部状态
  useEffect(() => {
    console.log('ChatflowEditor useEffect - initialData changed:', initialData);
    
    if (initialData && !isSyncingExternalData.current) {
      isSyncingExternalData.current = true;
      
      // 安全地设置节点数据
      const safeNodes = Array.isArray(initialData.nodes) ? initialData.nodes : [];
      const safeEdges = Array.isArray(initialData.edges) ? initialData.edges : [];
      
      console.log('Setting nodes and edges:', { nodes: safeNodes.length, edges: safeEdges.length });
      
      // 只有当数据真的发生变化时才更新
      setNodes(prev => {
        const prevStr = JSON.stringify(prev.map(n => ({ id: n.id, position: n.position, data: n.data })));
        const newStr = JSON.stringify(safeNodes.map(n => ({ id: n.id, position: n.position, data: n.data })));
        return prevStr !== newStr ? safeNodes : prev;
      });
      
      setEdges(prev => {
        const prevStr = JSON.stringify(prev);
        const newStr = JSON.stringify(safeEdges);
        return prevStr !== newStr ? safeEdges : prev;
      });
      
      // 重置同步标志
      setTimeout(() => {
        isSyncingExternalData.current = false;
      }, 100);
    }
  }, [initialData]);

  // 当 nodes 或 edges 发生变化时，自动调用 onSave 同步数据
  // 添加防抖和初始化标志，避免无限循环
  const [isInitialized, setIsInitialized] = useState(false);
  const lastSaveData = useRef<string>('');
  
  useEffect(() => {
    // 如果正在同步外部数据，则不触发 onSave
    if (isSyncingExternalData.current) {
      return;
    }
    
    // 首次加载时标记为已初始化，但不触发保存
    if (!isInitialized) {
      setIsInitialized(true);
      return;
    }
    
    // 只有在有实际数据变化时才调用 onSave
    if (isInitialized && onSave) {
      // 使用数据指纹避免重复保存相同数据
      const currentData = JSON.stringify({ 
        nodes: nodes.map(n => ({ id: n.id, type: n.type, position: n.position, data: n.data })), 
        edges: edges.map(e => ({ id: e.id, source: e.source, target: e.target }))
      });
      
      if (currentData !== lastSaveData.current && (nodes.length > 0 || edges.length > 0)) {
        lastSaveData.current = currentData;
        
        // 使用防抖延迟避免频繁调用
        const timeoutId = setTimeout(() => {
          console.log('ChatflowEditor: 保存数据变化', { nodes: nodes.length, edges: edges.length });
          onSave(nodes, edges);
        }, 500);
        
        return () => clearTimeout(timeoutId);
      }
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
    if (node && isChatflowNode(node)) {
      console.log('找到节点:', node); // 添加调试日志
      setSelectedNode(node);
      setIsConfigDrawerVisible(true);
    } else {
      console.log('未找到节点或节点类型不匹配:', nodeId); // 添加调试日志
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
      celery: createNodeComponent(TimeTriggerNode),
      restful: createNodeComponent(RestfulApiNode),
      openai: createNodeComponent(OpenAIApiNode),
      agents: createNodeComponent(AgentsNode),
      condition: createNodeComponent(IfConditionNode),
      http: createNodeComponent(HttpRequestNode),
      prompt: createNodeComponent(PromptAppendNode),
      knowledge: createNodeComponent(KnowledgeAppendNode),
    };
  }, [handleDeleteNode, handleConfigNode]);

  // ReactFlow 实例初始化
  const onInit = useCallback((instance: any) => {
    setReactFlowInstance(instance);
    // 初始化时设置视窗状态
    const currentViewport = instance.getViewport();
    setViewport(currentViewport);
  }, []);

  // 视窗变化处理
  const onMove = useCallback((event: any, newViewport: any) => {
    setViewport(newViewport);
  }, []);

  // 处理连接
  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  // 处理节点和连线选择变化
  const onSelectionChange = useCallback((params: { nodes: Node[]; edges: Edge[] }) => {
    setSelectedNodes(params.nodes);
    setSelectedEdges(params.edges);
  }, []);

  // 键盘事件处理
  const handleKeyDown = useCallback((event: KeyboardEvent) => {
    // 检查是否按下了Delete键或Backspace键
    if ((event.key === 'Delete' || event.key === 'Backspace') && (selectedNodes.length > 0 || selectedEdges.length > 0)) {
      // 阻止默认行为（避免浏览器返回上一页）
      event.preventDefault();
      
      // 处理节点和连线删除
      const hasNodes = selectedNodes.length > 0;
      const hasEdges = selectedEdges.length > 0;
      
      if (hasNodes) {
        // 节点删除需要确认对话框
        let title = '';
        let content = '';
        
        if (selectedNodes.length === 1) {
          const nodeToDelete = selectedNodes[0];
          title = t('chatflow.messages.deleteConfirm');
          content = `${t('chatflow.messages.deleteNodeContent')} ${nodeToDelete.data.label}`;
        } else {
          title = t('chatflow.messages.deleteMultipleConfirm');
          content = `${t('chatflow.messages.deleteMultipleContent')} ${selectedNodes.length}`;
        }

        Modal.confirm({
          title,
          content,
          okText: t('common.confirm'),
          cancelText: t('common.cancel'),
          okButtonProps: { danger: true },
          onOk: () => {
            // 删除选中的节点
            const selectedNodeIds = selectedNodes.map(node => node.id);
            setNodes((nds) => nds.filter((n) => !selectedNodeIds.includes(n.id)));
            // 删除与节点相关的连线
            setEdges((eds) => eds.filter((e) => !selectedNodeIds.includes(e.source) && !selectedNodeIds.includes(e.target)));
            
            // 同时删除选中的连线（如果有）
            if (hasEdges) {
              const selectedEdgeIds = selectedEdges.map(edge => edge.id);
              setEdges((eds) => eds.filter((e) => !selectedEdgeIds.includes(e.id)));
            }
            
            // 清空选择状态
            setSelectedNodes([]);
            setSelectedEdges([]);
            setIsConfigDrawerVisible(false);
            
            // 显示删除成功消息
            if (hasEdges) {
              message.success(`${t('chatflow.messages.itemsDeleted')} ${selectedNodes.length} ${t('chatflow.messages.nodes')} ${selectedEdges.length} ${t('chatflow.messages.edges')}`);
            } else {
              message.success(`${t('chatflow.messages.multipleNodesDeleted')} ${selectedNodes.length}`);
            }
          }
        });
      } else if (hasEdges) {
        // 只有连线的情况，直接删除不需要确认
        const selectedEdgeIds = selectedEdges.map(edge => edge.id);
        setEdges((eds) => eds.filter((e) => !selectedEdgeIds.includes(e.id)));
        
        // 清空选择状态
        setSelectedEdges([]);
        
        // 显示删除成功消息
        message.success(`${t('chatflow.messages.edgesDeleted')} ${selectedEdges.length}`);
      }
    }
  }, [selectedNodes, selectedEdges, setNodes, setEdges, t]);

  // 监听键盘事件
  useEffect(() => {
    // 确保组件聚焦时才监听键盘事件
    const flowContainer = reactFlowWrapper.current;
    if (flowContainer) {
      // 设置tabIndex使div可以接收键盘事件
      flowContainer.tabIndex = 0;
      flowContainer.addEventListener('keydown', handleKeyDown);
      
      return () => {
        flowContainer.removeEventListener('keydown', handleKeyDown);
      };
    }
  }, [handleKeyDown]);

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

        // 计算鼠标相对于 ReactFlow 容器的精确位置
        const mouseX = event.clientX - reactFlowBounds.left;
        const mouseY = event.clientY - reactFlowBounds.top;

        // 检查鼠标是否在画布范围内
        if (mouseX < 0 || mouseY < 0 || mouseX > reactFlowBounds.width || mouseY > reactFlowBounds.height) {
          // 鼠标超出画布范围，取消拖放
          return;
        }

        // 直接将屏幕坐标转换为流程图坐标系，使用ReactFlow的内置方法
        const flowPosition = reactFlowInstance.screenToFlowPosition({
          x: event.clientX,
          y: event.clientY,
        });

        // 节点尺寸（用于调整放置位置，让节点中心对齐鼠标）
        const nodeWidth = 160;
        const nodeHeight = 80;
        
        // 调整位置，让节点中心对齐鼠标位置
        const adjustedPosition = {
          x: flowPosition.x - nodeWidth / 2,
          y: flowPosition.y - nodeHeight / 2,
        };

        const getNodeLabel = (nodeType: string) => {
          try {
            return t(`chatflow.${nodeType}`);
          } catch {
            return nodeType;
          }
        };

        const newNode: ChatflowNode = {
          id: `${type}-${Date.now()}`,
          type,
          position: adjustedPosition,
          data: { 
            label: getNodeLabel(type),
            type: type as ChatflowNodeData['type'],
            config: {},
            description: ''
          },
        };

        setNodes((nds) => nds.concat(newNode));
        // message.success(`${t('chatflow.messages.nodeAdded')} ${getNodeLabel(type)}`);
        
      } catch (error) {
        console.error('拖拽放置错误:', error);
        message.error(t('chatflow.messages.dragFailed'));
      }
    },
    [reactFlowInstance, setNodes, t]
  );

  // 保存配置
  const handleSaveConfig = useCallback((nodeId: string, values: any) => {
    const { name, ...config } = values;
    
    setNodes((nds) => 
      nds.map((node) => 
        node.id === nodeId 
          ? { 
            ...node, 
            data: { 
              ...node.data, 
              label: name || node.data.label,
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
      <div 
        className={styles.flowContainer} 
        ref={reactFlowWrapper}
        onFocus={() => {
          // 当容器获得焦点时，确保可以接收键盘事件
          if (reactFlowWrapper.current) {
            reactFlowWrapper.current.focus();
          }
        }}
        style={{ outline: 'none' }} // 移除焦点时的轮廓线
      >
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
            onSelectionChange={onSelectionChange}
            nodeTypes={nodeTypes}
            defaultViewport={viewport}
            onMove={onMove}
            minZoom={0.1}
            maxZoom={2}
            attributionPosition="bottom-left"
            fitView={false}
            fitViewOptions={{
              padding: 0.2,
              includeHiddenNodes: false,
            }}
          >
            <MiniMap 
              nodeColor="#1890ff"
              nodeStrokeColor="#f0f0f0"
              nodeStrokeWidth={1}
              maskColor="rgba(255, 255, 255, 0.8)"
              pannable={true}
              zoomable={true}
              ariaLabel="流程图缩略图"
            />
            <Controls />
            <Background variant={BackgroundVariant.Dots} gap={12} size={1} />
          </ReactFlow>
        </ReactFlowProvider>
      </div>

      {/* 节点配置侧边栏 */}
      <NodeConfigDrawer
        visible={isConfigDrawerVisible}
        node={selectedNode}
        nodes={Array.isArray(nodes) ? nodes.filter(isChatflowNode) : []} // 确保传递正确格式的数组
        onClose={() => setIsConfigDrawerVisible(false)}
        onSave={handleSaveConfig}
        onDelete={handleDeleteNode}
      />
    </div>
  );
};

export default ChatflowEditor;

// 导出类型映射函数供其他组件使用
export type { ChatflowNodeData };
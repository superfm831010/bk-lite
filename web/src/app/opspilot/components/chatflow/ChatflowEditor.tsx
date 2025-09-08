'use client';

import React, { useCallback, useState, useMemo, useRef } from 'react';
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
import { Button, Modal, Select, Form, Input, message, Dropdown, InputNumber } from 'antd';
import { MoreOutlined, DeleteOutlined, SettingOutlined } from '@ant-design/icons';
import { useTranslation } from '@/utils/i18n';
import Icon from '@/components/icon';
import styles from './ChatflowEditor.module.scss';

const { Option } = Select;
const { TextArea } = Input;

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

// 节点操作菜单组件
const NodeMenu = ({ nodeId, onDelete, onConfig }: { 
  nodeId: string; 
  onDelete: (id: string) => void;
  onConfig: (id: string) => void;
}) => {
  const { t } = useTranslation();
  
  const menuItems = [
    {
      key: 'config',
      icon: <SettingOutlined />,
      label: t('chatflow.configNode'),
      onClick: () => onConfig(nodeId),
    },
    {
      key: 'delete',
      icon: <DeleteOutlined />,
      label: t('chatflow.deleteNode'),
      danger: true,
      onClick: () => onDelete(nodeId),
    },
  ];

  return (
    <Dropdown menu={{ items: menuItems }} trigger={['click']} placement="bottomRight">
      <Button 
        type="text" 
        size="small" 
        icon={<MoreOutlined />}
        className="absolute top-1 right-1 opacity-0 group-hover:opacity-100 transition-opacity z-10"
      />
    </Dropdown>
  );
};

// 通用节点组件
const BaseNode = ({ 
  data, 
  id, 
  selected, 
  onDelete, 
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
  onDelete: (id: string) => void;
  onConfig: (id: string) => void;
  icon: string;
  color?: string;
  hasInput?: boolean;
  hasOutput?: boolean;
  hasMultipleOutputs?: boolean;
}) => {
  return (
    <div className={`${styles.nodeContainer} ${selected ? styles.selected : ''} group relative`}>
      <NodeMenu nodeId={id} onDelete={onDelete} onConfig={onConfig} />
      
      {hasInput && (
        <Handle type="target" position={Position.Left} className={styles.handle} />
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
        <Handle type="source" position={Position.Right} className={styles.handle} />
      )}
      
      {hasMultipleOutputs && (
        <>
          <Handle type="source" position={Position.Right} className={styles.handle} id="true" />
          <Handle type="source" position={Position.Bottom} className={styles.handle} id="false" />
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
}

const ChatflowEditor: React.FC<ChatflowEditorProps> = ({ onSave }) => {
  const { t } = useTranslation();
  const [configForm] = Form.useForm();
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const [reactFlowInstance, setReactFlowInstance] = useState<any>(null);
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [isConfigModalVisible, setIsConfigModalVisible] = useState(false);

  // 初始节点 - 默认流程：定时触发 -> HTTP请求 -> 智能体
  const getInitialNodes = useCallback((): Node[] => [
    {
      id: 'trigger-1',
      type: 'timeTrigger',
      position: { x: 100, y: 200 },
      data: { 
        label: t('chatflow.timeTrigger'), 
        type: 'timeTrigger',
        config: { cronExpression: '0 */5 * * * *' },
        description: '每5分钟执行一次'
      },
    },
    {
      id: 'http-1',
      type: 'httpRequest',
      position: { x: 350, y: 200 },
      data: { 
        label: t('chatflow.httpRequest'), 
        type: 'httpRequest',
        config: { url: 'https://api.example.com/data', method: 'GET' },
        description: 'GET请求获取数据'
      },
    },
    {
      id: 'agent-1',
      type: 'agents',
      position: { x: 600, y: 200 },
      data: { 
        label: t('chatflow.agents'), 
        type: 'agents',
        config: { knowledgeBase: '运维知识库', model: 'gpt-4' },
        description: '基于知识库的智能问答'
      },
    },
  ], [t]);

  const getInitialEdges = useCallback((): Edge[] => [
    {
      id: 'e1-2',
      source: 'trigger-1',
      target: 'http-1',
      type: 'smoothstep',
    },
    {
      id: 'e2-3',
      source: 'http-1',
      target: 'agent-1',
      type: 'smoothstep',
    },
  ], []);

  const [nodes, setNodes, onNodesChange] = useNodesState(getInitialNodes());
  const [edges, setEdges, onEdgesChange] = useEdgesState(getInitialEdges());

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
  }, []);

  // ReactFlow 实例初始化
  const onInit = useCallback((instance: any) => {
    setReactFlowInstance(instance);
  }, []);

  // 处理连接
  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  // 节点删除处理
  const handleDeleteNode = useCallback((nodeId: string) => {
    Modal.confirm({
      title: t('chatflow.messages.deleteConfirm'),
      onOk: () => {
        setNodes((nds) => nds.filter((n) => n.id !== nodeId));
        setEdges((eds) => eds.filter((e) => e.source !== nodeId && e.target !== nodeId));
        message.success(t('chatflow.messages.nodeDeleted'));
      }
    });
  }, [setNodes, setEdges, t]);

  // 节点配置处理
  const handleConfigNode = useCallback((nodeId: string) => {
    const node = nodes.find(n => n.id === nodeId);
    if (node) {
      setSelectedNode(node);
      configForm.setFieldsValue({
        name: node.data.label,
        description: node.data.description,
        ...(node.data.config || {})
      });
      setIsConfigModalVisible(true);
    }
  }, [nodes, configForm]);

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
  const handleSaveConfig = () => {
    if (!selectedNode) return;
    
    configForm.validateFields().then((values) => {
      const { name, description, ...config } = values;
      
      setNodes((nds) => 
        nds.map((node) => 
          node.id === selectedNode.id 
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
      setIsConfigModalVisible(false);
      message.success(t('chatflow.messages.nodeConfigured'));
    });
  };

  // 保存工作流
  const handleSave = () => {
    if (onSave) {
      onSave(nodes, edges);
    }
    message.success(t('chatflow.messages.saveSuccess'));
  };

  // 重置画布
  const handleClear = () => {
    setNodes(getInitialNodes());
    setEdges(getInitialEdges());
    message.success('已重置为初始状态');
  };

  // 根据节点类型渲染配置表单
  const renderConfigForm = () => {
    if (!selectedNode) return null;

    const nodeType = selectedNode.data.type;
    
    switch (nodeType) {
      case 'timeTrigger':
        return (
          <>
            <Form.Item name="cronExpression" label={t('chatflow.nodeProperties.cronExpression')}>
              <Input placeholder="0 */5 * * * *" />
            </Form.Item>
            <Form.Item name="timezone" label="时区">
              <Select defaultValue="Asia/Shanghai">
                <Option value="Asia/Shanghai">Asia/Shanghai</Option>
                <Option value="UTC">UTC</Option>
              </Select>
            </Form.Item>
          </>
        );
      
      case 'httpRequest':
        return (
          <>
            <Form.Item name="url" label={t('chatflow.nodeProperties.url')} rules={[{ required: true }]}>
              <Input placeholder="https://api.example.com" />
            </Form.Item>
            <Form.Item name="method" label={t('chatflow.nodeProperties.method')}>
              <Select defaultValue="GET">
                <Option value="GET">GET</Option>
                <Option value="POST">POST</Option>
                <Option value="PUT">PUT</Option>
                <Option value="DELETE">DELETE</Option>
              </Select>
            </Form.Item>
            <Form.Item name="headers" label={t('chatflow.nodeProperties.headers')}>
              <TextArea rows={3} placeholder='{"Content-Type": "application/json"}' />
            </Form.Item>
            <Form.Item name="timeout" label={t('chatflow.nodeProperties.timeout')}>
              <InputNumber min={1} max={300} defaultValue={30} addonAfter="秒" />
            </Form.Item>
          </>
        );
      
      case 'agents':
        return (
          <>
            <Form.Item name="model" label={t('chatflow.nodeProperties.model')}>
              <Select defaultValue="gpt-4">
                <Option value="gpt-4">GPT-4</Option>
                <Option value="gpt-3.5-turbo">GPT-3.5 Turbo</Option>
              </Select>
            </Form.Item>
            <Form.Item name="knowledgeBase" label={t('chatflow.nodeProperties.knowledgeBase')}>
              <Select mode="multiple" placeholder="选择知识库">
                <Option value="ops-kb">运维知识库</Option>
                <Option value="tech-kb">技术文档库</Option>
              </Select>
            </Form.Item>
            <Form.Item name="temperature" label={t('chatflow.nodeProperties.temperature')}>
              <InputNumber min={0} max={1} step={0.1} defaultValue={0.7} />
            </Form.Item>
            <Form.Item name="prompt" label={t('chatflow.nodeProperties.prompt')}>
              <TextArea rows={4} placeholder="系统提示词..." />
            </Form.Item>
          </>
        );

      case 'restfulApi':
        return (
          <>
            <Form.Item name="url" label={t('chatflow.nodeProperties.url')} rules={[{ required: true }]}>
              <Input placeholder="https://api.example.com" />
            </Form.Item>
            <Form.Item name="method" label={t('chatflow.nodeProperties.method')}>
              <Select defaultValue="GET">
                <Option value="GET">GET</Option>
                <Option value="POST">POST</Option>
                <Option value="PUT">PUT</Option>
                <Option value="DELETE">DELETE</Option>
              </Select>
            </Form.Item>
            <Form.Item name="headers" label={t('chatflow.nodeProperties.headers')}>
              <TextArea rows={3} placeholder='{"Content-Type": "application/json"}' />
            </Form.Item>
          </>
        );

      case 'openaiApi':
        return (
          <>
            <Form.Item name="apiKey" label="API Key" rules={[{ required: true }]}>
              <Input.Password placeholder="sk-..." />
            </Form.Item>
            <Form.Item name="model" label={t('chatflow.nodeProperties.model')}>
              <Select defaultValue="gpt-4">
                <Option value="gpt-4">GPT-4</Option>
                <Option value="gpt-3.5-turbo">GPT-3.5 Turbo</Option>
              </Select>
            </Form.Item>
            <Form.Item name="temperature" label={t('chatflow.nodeProperties.temperature')}>
              <InputNumber min={0} max={1} step={0.1} defaultValue={0.7} />
            </Form.Item>
          </>
        );

      case 'promptAppend':
        return (
          <>
            <Form.Item name="prompt" label={t('chatflow.nodeProperties.prompt')} rules={[{ required: true }]}>
              <TextArea rows={4} placeholder="请输入要追加的提示词..." />
            </Form.Item>
            <Form.Item name="position" label="追加位置">
              <Select defaultValue="before">
                <Option value="before">前置</Option>
                <Option value="after">后置</Option>
              </Select>
            </Form.Item>
          </>
        );

      case 'knowledgeAppend':
        return (
          <>
            <Form.Item name="knowledgeBase" label={t('chatflow.nodeProperties.knowledgeBase')} rules={[{ required: true }]}>
              <Select mode="multiple" placeholder="选择知识库">
                <Option value="ops-kb">运维知识库</Option>
                <Option value="tech-kb">技术文档库</Option>
                <Option value="faq-kb">FAQ知识库</Option>
              </Select>
            </Form.Item>
            <Form.Item name="similarity" label="相似度阈值">
              <InputNumber min={0} max={1} step={0.1} defaultValue={0.8} />
            </Form.Item>
            <Form.Item name="maxResults" label="最大结果数">
              <InputNumber min={1} max={10} defaultValue={3} />
            </Form.Item>
          </>
        );

      case 'ifCondition':
        return (
          <>
            <Form.Item name="condition" label="条件表达式" rules={[{ required: true }]}>
              <Input placeholder="response.status === 200" />
            </Form.Item>
            <Form.Item name="trueLabel" label="True分支标签">
              <Input placeholder="成功" />
            </Form.Item>
            <Form.Item name="falseLabel" label="False分支标签">
              <Input placeholder="失败" />
            </Form.Item>
          </>
        );
      
      default:
        return null;
    }
  };

  return (
    <div className={styles.chatflowEditor}>
      <div className={styles.toolbar}>
        <div className={styles.toolbarLeft}>
          <Button onClick={handleClear}>
            {t('chatflow.clear')}
          </Button>
        </div>
        <div className={styles.toolbarRight}>
          <Button type="primary" onClick={handleSave}>
            {t('chatflow.save')}
          </Button>
        </div>
      </div>

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

      {/* 节点配置模态框 */}
      <Modal
        title={`${t('chatflow.configNode')} - ${selectedNode?.data.label}`}
        open={isConfigModalVisible}
        onOk={handleSaveConfig}
        onCancel={() => setIsConfigModalVisible(false)}
        okText={t('common.confirm')}
        cancelText={t('common.cancel')}
        width={600}
      >
        <Form form={configForm} layout="vertical">
          <Form.Item name="name" label={t('chatflow.nodeProperties.name')}>
            <Input />
          </Form.Item>
          <Form.Item name="description" label={t('chatflow.nodeProperties.description')}>
            <TextArea rows={2} />
          </Form.Item>
          {renderConfigForm()}
        </Form>
      </Modal>
    </div>
  );
};

export default ChatflowEditor;
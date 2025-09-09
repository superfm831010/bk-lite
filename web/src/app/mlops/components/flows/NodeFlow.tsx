import {
  ReactFlow,
  Node,
  Edge,
  addEdge,
  Connection,
  useNodesState,
  // ReactFlowProvider,
  ReactFlowInstance,
  Background,
  Controls,
  MiniMap,
  Panel,
  getOutgoers,
  useEdgesState,
  useReactFlow,
  NodeTypes,
  IsValidConnection,
  EdgeTypes
} from '@xyflow/react';
import { Button } from 'antd';
import { IntentNode, ResponseNode, SlotNode, FormNode, ActionNode, CheckPoint } from './CustomNodes';
import CustomEdge from './ButtonEdge';
import '@xyflow/react/dist/style.css';
import { useCallback, useMemo, useState, useEffect } from 'react';
import { NodeType, NodeData } from '@/app/mlops/types';
import { useTranslation } from '@/utils/i18n';
import NodePanel from './NodePanel';
import NodeDetailDrawer from './NodeDetail';
import flowStyle from './index.module.scss';

const NodeFlow = ({
  initialNodes,
  initialEdges,
  nodeTypes,
  dataset,
  panel = [],
  handleSaveFlow
}: {
  initialNodes: Node<NodeData>[],
  initialEdges: Edge[],
  nodeTypes: NodeType[],
  dataset: string,
  panel?: React.ReactNode[],
  handleSaveFlow: (data: any) => void;
}) => {
  const { t } = useTranslation();
  const { getNodes, getEdges, screenToFlowPosition } = useReactFlow();
  const [rfInstance, setRfInstance] = useState<ReactFlowInstance<Node<NodeData>> | null>(null);
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [detailOpen, setDetailOpen] = useState<boolean>(false);
  const [currentNode, setCurrentNode] = useState<Node | null>(null);

  useEffect(() => {
    setNodes(initialNodes);
    setEdges(initialEdges);
  }, [initialNodes, initialEdges, setNodes, setEdges]);

  // 处理链接线
  const onConnect = useCallback(
    (params: Connection) => {
      // console.log(params);
      const sourceNode = nodes.find((item) => item.id === params.source);
      const targetNode = nodes.find((item) => item.id === params.target);
      console.log(sourceNode, targetNode);
      console.log(params);
      if (params.source === params.target) return;
      setEdges((eds) => addEdge({ ...params, animated: true, type: 'buttonedge' }, eds));
      setNodes((nds) =>
        nds.map((node) => {
          if (node.id === params.source || node.id === params.target) {
            return {
              ...node,
              data: {
                ...node.data,
                source: node.id === params.source ? [...node.data.source, {
                  id: targetNode?.id,
                  name: targetNode?.data.name,
                  type: targetNode?.type
                }] : node.data?.source,
                target: node.id === params.target ? [...node.data.target, {
                  id: sourceNode?.id,
                  name: sourceNode?.data.name,
                  type: sourceNode?.type
                }] : node.data?.target
              }
            }
          }
          return node;
        })
      );
    },
    [setEdges]
  );

  // 处理拖拽开始
  const onDragStart = (event: React.DragEvent, nodeType: string) => {
    event.dataTransfer.setData('application/reactflow', nodeType);
    event.dataTransfer.effectAllowed = 'move';
  };

  // 处理拖拽悬停
  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  // 处理拖拽放下
  const onDrop = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    const type = event.dataTransfer.getData('application/reactflow');

    // 校验节点类型
    if (typeof type === 'undefined' || !type) {
      return;
    }

    // 计算放下位置
    const position = screenToFlowPosition({
      x: event.clientX,
      y: event.clientY
    });

    if (!position) return;

    // 创建新节点
    const newNode: Node<NodeData> = {
      id: `${type}_${Date.now()}`,
      type,
      position,
      data: { ...getDefaultNodeData(type) }
    };

    setNodes((nds) => nds.concat(newNode));
  }, [setNodes, screenToFlowPosition]);

  const onSave = useCallback(() => {
    if (rfInstance) {
      const flow = rfInstance.toObject();
      handleSaveFlow(flow);
    }
  }, [rfInstance, handleSaveFlow]);

  const onRestore = useCallback(() => {
    setNodes(initialNodes);
    setEdges(initialEdges);
  }, [setNodes]);

  // 选中节点处理
  const handleNodeClick = (event: React.MouseEvent, node: Node) => {
    if (node) {
      setDetailOpen(true);
      setCurrentNode(node);
    }
  };

  // 更改节点详情处理
  const handleChangeNodeDetail = (name: string) => {
    const _nodes = nodes.map((item) => {
      if (item.id === currentNode?.id) {
        const node = {
          ...item,
          id: `${item.type}_${name}_${Date.now()}`,
          data: {
            id: `${item.type}_${name}`,
            name: name,
            source: [],
            target: []
          }
        };
        setCurrentNode(node);
        return node;
      }
      return {
        ...item,
        data: {
          ...item.data,
          source: item.data.source.filter((item: string) => item !== currentNode?.id),
          target: item.data?.target.filter((item: string) => item !== currentNode?.id),
        }
      };
    });
    const _edges = edges.filter(item => ![item.source, item.target].includes(currentNode?.id as string));
    setEdges(_edges);
    setNodes(_nodes);
  };

  // 删除节点处理
  const handleDelNode = () => {
    const _nodes = nodes.filter((item) => item.id !== currentNode?.id).map((item) => {
      return {
        ...item,
        data: {
          ...item.data,
          source: item.data?.source.filter((item: string) => item !== currentNode?.id),
          target: item.data?.target.filter((item: string) => item !== currentNode?.id),
        }
      }
    });
    const _edges = edges.filter((item) => ![item.source, item.target].includes(currentNode?.id as string));
    setNodes(_nodes);
    setEdges(_edges);
  };

  // 循环链接判断
  const isValidConnection: IsValidConnection<Edge> = useCallback(
    (connection) => {
      const nodes = getNodes();
      const edges = getEdges();
      const target = nodes.find((node) => node.id === connection.target);
      const hasCycle = (node: any, visited = new Set()) => {
        if (visited.has(node.id)) return false;

        visited.add(node.id);

        for (const outgoer of getOutgoers(node, nodes, edges)) {
          if (outgoer.id === connection.source) return true;
          if (hasCycle(outgoer, visited)) return true;
        }
      };

      if (target?.id === connection.source) return false;
      return !hasCycle(target);
    },
    [getNodes, getEdges],
  );

  // 获取默认节点数据
  const getDefaultNodeData = (type: string) => {
    return {
      type: type,
      name: '',
      target: [],
      source: []
    }
  };

  const customNodeTypes: NodeTypes = useMemo(() => ({
    intent: IntentNode,
    response: ResponseNode,
    slot: SlotNode,
    form: FormNode,
    action: ActionNode,
    checkpoint: CheckPoint
  }), []);

  const edgeTypes: EdgeTypes = useMemo(() => ({
    buttonedge: CustomEdge,
  }), []);

  // 根据 CustomNodes 中的颜色定义节点颜色
  const getNodeColor = useCallback((node: Node<NodeData>) => {
    switch (node.type) {
      case 'intent':
        return '#0ea5e9'; // sky-500 - 天蓝色
      case 'response':
        return '#14b8a6'; // teal-500 - 青绿色
      case 'slot':
        return '#22c55e'; // green-500 - 绿色
      case 'form':
        return '#ef4444'; // red-500 - 红色
      case 'action':
        return '#3b82f6'; // blue-500 - 蓝色
      case 'checkpoint':
        return '#f97316'; // orange-500 - 橙色
      default:
        return '#64748b'; // slate-500 - 默认灰色
    }
  }, []);

  // 根据节点状态调整颜色透明度
  const getNodeColorWithState = useCallback((node: Node<NodeData>) => {
    const baseColor = getNodeColor(node);

    // 如果节点没有名称，显示为半透明
    if (!node.data?.name) {
      return baseColor + '80'; // 添加50%透明度
    }

    // 如果节点被选中，增加亮度
    if (node.selected) {
      return baseColor;
    }

    return baseColor;
  }, [getNodeColor]);

  return (
    <div className={`${flowStyle.flowContainer} flex w-full h-full relative`}>
      {/*节点面板 */}
      <NodePanel onDragStart={onDragStart} nodeTypes={nodeTypes} />
      {/* 节点详情 */}
      <NodeDetailDrawer
        open={detailOpen}
        dataset={dataset}
        node={currentNode as Node}
        handleDelNode={handleDelNode}
        onChange={handleChangeNodeDetail}
        onClose={() => setDetailOpen(false)}
      />
      <ReactFlow<Node<NodeData>>
        nodes={nodes}
        edges={edges}
        onNodeClick={handleNodeClick}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onInit={setRfInstance}
        isValidConnection={isValidConnection}
        onDrop={onDrop}
        onDragOver={onDragOver}
        fitView
        nodeTypes={customNodeTypes}
        edgeTypes={edgeTypes}
        proOptions={{ hideAttribution: true }}
      >
        <Background />
        <Panel position='top-right'>
          <Button
            key="save"
            size="small"
            color="default"
            variant="outlined"
            className="mr-2 text-xs"
            onClick={onSave}
          >{t(`common.save`)}</Button>
          <Button
            key="reset"
            size="small"
            variant="outlined"
            className="mr-2 text-xs"
            onClick={onRestore}
          >{t(`mlops-common.reset`)}</Button>
          {panel?.length > 0 && panel}
        </Panel>
        <Controls position='top-left' orientation="horizontal" />
        {/* 优化后的 MiniMap */}
        <MiniMap
          nodeColor={getNodeColorWithState}
          nodeStrokeColor={(node: Node<NodeData>) => {
            if (node.selected) {
              return '#1f2937'; // 深灰色边框表示选中
            }
            return node.data?.name ? '#ffffff' : '#e5e7eb'; // 有名称显示白边框，无名称显示灰边框
          }}
          nodeBorderRadius={6}
          maskColor="rgba(15, 23, 42, 0.15)" // 深色半透明遮罩
          maskStrokeColor="#334155"
          maskStrokeWidth={1.5}
          position="bottom-right"
          style={{
            backgroundColor: 'rgba(248, 250, 252, 0.98)', // 几乎不透明的浅色背景
            border: '1px solid #cbd5e1',
            borderRadius: '16px',
            // boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
            backdropFilter: 'blur(12px) saturate(150%)',
            width: 200,
            height: 160,
            // padding: '8px',
          }}
          pannable
          zoomable
          inversePan
          zoomStep={0.5}
        />
      </ReactFlow>
    </div>
  )
};

export default NodeFlow;
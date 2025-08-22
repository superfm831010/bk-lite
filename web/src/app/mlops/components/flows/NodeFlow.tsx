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
  // MiniMap,
  Panel,
  getOutgoers,
  useEdgesState,
  useReactFlow,
  NodeTypes,
  IsValidConnection
} from '@xyflow/react';
import { Button } from 'antd';
import { IntentNode, ResponseNode, SlotNode } from './CustomNodes';
import '@xyflow/react/dist/style.css';
import { useCallback, useMemo, useState } from 'react';
import { useTranslation } from '@/utils/i18n';
import NodePanel from './NodePanel';
import NodeDetailDrawer from './NodeDetail';

interface NodeType {
  type: string;
  label: string;
  color: string;
}

const NodeFlow = ({
  initialNodes,
  initialEdges,
  nodeTypes,
  dataset,
  panel,
  handleSaveFlow
}: {
  initialNodes: Node[],
  initialEdges: Edge[],
  nodeTypes: NodeType[],
  dataset: string,
  panel?: React.ReactNode[],
  handleSaveFlow: (data: any) => void;
}) => {
  const { t } = useTranslation();
  const { getNodes, getEdges, screenToFlowPosition } = useReactFlow();
  const [rfInstance, setRfInstance] = useState<ReactFlowInstance | null>(null);
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [detailOpen, setDetailOpen] = useState<boolean>(false);
  const [currentNode, setCurrentNode] = useState<Node | null>(null);

  // 处理链接线
  const onConnect = useCallback(
    (params: Connection) => {
      console.log(params);
      setEdges((eds) => addEdge(params, eds));
      setNodes((nds) => 
        nds.map((node) => {
          if(node.id === params.source) {
            return {
              ...node,
              data: {
                ...node.data,
                source: params.target
              }
            }
          }
          return node;
        })
      );
      setNodes((nds) => 
        nds.map((node) => {
          if(node.id === params.target) {
            return {
              ...node,
              data: {
                ...node.data,
                target: params.source,
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
    // const reactFlowBounds = reactFlowWrapper.current?.getBoundingClientRect();
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
    const newNode: Node = {
      id: `${type}_${Date.now()}`,
      type,
      position,
      data: { label: `${getNodeLabel(type)}`, ...getDefaultNodeData(type) }
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

  // 获取节点标签
  const getNodeLabel = (type: string) => {
    const labels: Record<string, string> = {
      intent: '意图节点',
      response: '响应节点',
      slot: '槽节点'
    };

    return labels[type] || '默认节点';
  };

  // 选中节点处理
  const handleNodeClick = (event: React.MouseEvent, node: Node) => {
    if (node) {
      setDetailOpen(true);
      setCurrentNode(node);
    }

    console.log(node);
  };

  // 更改节点详情处理
  const handleChangeNodeDetail = (data: any) => {
    console.log(data);
    const _nodes = nodes.map((item) => {
      if (item.id === currentNode?.id) {
        return {
          ...item,
          id: data?.name,
          data: {
            id: data?.name,
          }
        }
      }
      return {
        ...item,
        data: {
          ...item.data,
          source: item.data?.source === currentNode?.id ? data.name : item.data?.source,
          target: item.data?.target === currentNode?.id ? data.name : item.data?.target,
        }
      };
    });
    const _edges = edges.map((item) => {
      if(item.target === currentNode?.id) {
        return {
          ...item,
          target: data?.name
        }
      }
      if(item.source === currentNode?.id) {
        return {
          ...item,
          source: data?.name
        }
      }
      return item;
    })

    setEdges(_edges);
    setNodes(_nodes);
  };

  // 删除节点处理
  const handleDelNode = () => {
    const _nodes = nodes.filter((item) => item.id !== currentNode?.id);
    setNodes(_nodes);
  };

  // 循环链接判断
  const isValidConnection: IsValidConnection<Edge> = useCallback(
    (connection) => {
      // we are using getNodes and getEdges helpers here
      // to make sure we create isValidConnection function only once
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
    switch (type) {
      case 'intent':
        return {};
      case 'response':
        return {};
      default:
        return {}
    }
  };

  const customNodeTypes: NodeTypes = useMemo(() => ({
    intent: IntentNode,
    response: ResponseNode,
    slot: SlotNode
  }), [])

  return (
    <div className='flex w-full h-full relative'>
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
      <ReactFlow
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
      >
        <Background />
        {panel?.length && (
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
            >重置</Button>
            {panel}
          </Panel>
        )}
        <Controls />
        {/* <MiniMap /> */}
      </ReactFlow>
    </div>
  )
};

export default NodeFlow;
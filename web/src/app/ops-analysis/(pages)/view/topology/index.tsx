import React, { useEffect, useRef, useState, useMemo } from 'react';
import TopologyToolbar from './toolbar';
import ContextMenu from './contextMenu';
import InstanceModal from './instanceModal';
import InstanceTree from './instanceTree';
import type { Graph as X6Graph, Edge } from '@antv/x6';
import type { DataNode } from 'antd/lib/tree';
import { Graph } from '@antv/x6';
import { Selection } from '@antv/x6-plugin-selection';
import { Button } from 'antd';
import { RightOutlined, LeftOutlined } from '@ant-design/icons';
import { useTranslation } from '@/utils/i18n';
import {
  getNodeStyle,
  getEdgeStyle,
  addEdgeTools,
  showPorts,
  hideAllPorts,
  filterTree,
  isPortClicked,
} from './topologyUtils';
import {
  mockGroups,
  mockInstances,
  mockInitialNodes,
  mockInitialEdges,
} from '../mockData';

const Topology: React.FC = () => {
  const { t } = useTranslation();
  const containerRef = useRef<HTMLDivElement>(null);
  const [graphInstance, setGraphInstance] = useState<Graph | null>(null);
  const [scale, setScale] = useState(1);
  const [modalVisible, setModalVisible] = useState(false);
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);
  const [isSelectMode, setIsSelectMode] = useState(true);
  const [selectedCells, setSelectedCells] = useState<string[]>([]);
  const [isDrawing, setIsDrawing] = useState(false);
  const drawingEdgeRef = useRef<Edge | null>(null);
  const [contextMenuNodeId, setContextMenuNodeId] = useState<string>('');
  const [instanceOptions, setInstanceOptions] = useState<
    Array<{ id: string; name: string }>
  >([]);
  const [contextMenuVisible, setContextMenuVisible] = useState(false);
  const [contextMenuPosition, setContextMenuPosition] = useState({
    x: 0,
    y: 0,
  });
  const [searchTerm, setSearchTerm] = useState('');
  const [inputValue, setInputValue] = useState('');
  const [collapsed, setCollapsed] = useState(false);

  useEffect(() => {
    if (!containerRef.current) return;
    const graph: X6Graph = new Graph({
      container: containerRef.current,
      grid: true,
      panning: true,
      mousewheel: { enabled: true, modifiers: 'ctrl' },
      connecting: {
        anchor: 'center',
        connectionPoint: { name: 'boundary' },
        allowBlank: false,
        highlight: true,
        snap: true,
        createEdge: () =>
          graph.createEdge({ shape: 'edge', ...getEdgeStyle('single') }),
        validateMagnet: ({ magnet }) =>
          magnet && magnet.getAttribute('magnet') === 'true',
      },
    });

    graph.use(
      new Selection({
        enabled: true,
        rubberband: true,
        showNodeSelectionBox: true,
        modifiers: 'shift',
        filter: (cell) => cell.isNode() || cell.isEdge(),
      })
    );

    setGraphInstance(graph);

    mockInitialNodes.forEach((nodeConfig: any) =>
      graph.addNode({ ...nodeConfig, ...getNodeStyle() })
    );
    mockInitialEdges.forEach((edgeConfig: any) => {
      const edge = graph.addEdge({ ...edgeConfig, ...getEdgeStyle('single') });
      addEdgeTools(edge);
    });

    const hideCtx = () => setContextMenuVisible(false);
    document.addEventListener('click', hideCtx);
    graph.on('blank:click', hideCtx);
    graph.on('node:contextmenu', ({ e, node }) => {
      e.preventDefault();
      setContextMenuVisible(true);
      setContextMenuPosition({ x: e.clientX, y: e.clientY });
      setContextMenuNodeId(node.id);
    });
    graph.on('edge:connected', ({ edge }) => {
      if (!edge) return;
      edge.setAttrs(getEdgeStyle('single').attrs);
      addEdgeTools(edge);
    });
    graph.on('selection:changed', ({ selected }) => {
      setSelectedCells(selected.map((cell) => cell.id));
      selected.forEach((cell) => cell.isEdge() && addEdgeTools(cell));
    });
    graph.on('edge:click', ({ edge }) => addEdgeTools(edge));

    // 锚点显示/隐藏
    graph.on('node:mouseenter', ({ node }) => {
      hideAllPorts(graph);
      showPorts(graph, node);
    });
    graph.on('edge:mouseenter', ({ edge }) => {
      hideAllPorts(graph);
      showPorts(graph, edge);
    });
    graph.on('node:mouseleave', () => hideAllPorts(graph));
    graph.on('edge:mouseleave', () => hideAllPorts(graph));
    graph.on('blank:click', () => hideAllPorts(graph));

    // 端口点击校验
    graph.on('node:mousedown', ({ e, node, x, y }) => {
      if (!isPortClicked(node, x, y)) e.stopPropagation();
    });

    // 初始化端口隐藏
    graph
      .getNodes()
      .forEach((node) =>
        ['top', 'bottom', 'left', 'right'].forEach((port) =>
          node.setPortProp(port, 'attrs/circle/opacity', 0)
        )
      );

    return () => {
      document.removeEventListener('click', hideCtx);
      graph.off('blank:click', hideCtx);
      graph.dispose();
    };
  }, []);

  useEffect(() => {
    setInputValue(searchTerm);
  }, [searchTerm]);

  const zoomIn = () => {
    if (graphInstance) {
      const next = scale + 0.1;
      graphInstance.zoom(next, { absolute: true });
      setScale(next);
    }
  };

  const zoomOut = () => {
    if (graphInstance) {
      const next = scale - 0.1 > 0.1 ? scale - 0.1 : 0.1;
      graphInstance.zoom(next, { absolute: true });
      setScale(next);
    }
  };

  const handleFit = () => {
    if (graphInstance && containerRef.current) {
      graphInstance.zoomToFit({ padding: 20, maxScale: 1 });
      setScale(1);
    }
  };

  const handleDelete = () => {
    if (graphInstance && selectedCells.length > 0) {
      graphInstance.removeCells(selectedCells);
      setSelectedCells([]);
    }
  };

  const handleSelectMode = () => {
    setIsSelectMode(!isSelectMode);
    if (graphInstance) {
      graphInstance.enableSelection();
    }
  };

  // 处理树节点选择
  const onTreeSelect = (keys: React.Key[], info: { node: DataNode }) => {
    const key = keys[0] as string;
    if (!info.node.children) {
      setInstanceOptions(mockInstances[key] || []);
      setSelectedRowKeys([]);
      setModalVisible(true);
    }
  };

  const onModalOk = () => {
    if (graphInstance && selectedRowKeys.length > 0) {
      selectedRowKeys.forEach((id, idx) => {
        const inst = instanceOptions.find((i) => i.id === id);
        if (inst) {
          graphInstance.addNode({
            x: 50 + (idx % 3) * 180,
            y: 50 + Math.floor(idx / 3) * 120,
            label: inst.name,
            ...getNodeStyle(),
          });
        }
      });
    }
    setModalVisible(false);
  };

  const onModalCancel = () => setModalVisible(false);

  // 处理右键菜单选择
  const handleMenuClick = ({ key }: { key: string }) => {
    setContextMenuVisible(false);

    if (graphInstance) {
      // 设置当前连接类型
      const connectionType = key as 'none' | 'single' | 'double';

      // 开始连接
      const edge = graphInstance.addEdge({
        source: { cell: contextMenuNodeId },
        target: { x: contextMenuPosition.x, y: contextMenuPosition.y },
        ...getEdgeStyle(connectionType),
        data: { connectionType },
      });

      drawingEdgeRef.current = edge;
      setIsDrawing(true);

      // 监听鼠标移动更新目标位置
      const onMouseMove = (e: MouseEvent) => {
        if (!drawingEdgeRef.current || !isDrawing || !graphInstance) return;

        // 将鼠标位置转换为画布坐标
        const localPoint = graphInstance.clientToLocal(e.clientX, e.clientY);
        drawingEdgeRef.current.setTarget(localPoint);
      };

      // 监听鼠标释放完成连接
      const onMouseUp = (e: MouseEvent) => {
        if (!drawingEdgeRef.current || !isDrawing || !graphInstance) return;

        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
        setIsDrawing(false);

        // 将鼠标位置转换为画布坐标
        const localPoint = graphInstance.clientToLocal(e.clientX, e.clientY);

        // 查找目标节点
        const nearestPort: string | null = null;
        let targetCell: any = null;
        graphInstance.getNodes().forEach((node) => {
          const bbox = node.getBBox();
          if (
            localPoint.x >= bbox.x &&
            localPoint.x <= bbox.x + bbox.width &&
            localPoint.y >= bbox.y &&
            localPoint.y <= bbox.y + bbox.height
          ) {
            targetCell = node;
          }
        });

        if (
          targetCell &&
          'id' in targetCell &&
          targetCell.id !== contextMenuNodeId &&
          nearestPort
        ) {
          drawingEdgeRef.current.setTarget({
            cell: targetCell.id,
            port: nearestPort,
          });
        } else {
          drawingEdgeRef.current.remove();
        }

        drawingEdgeRef.current = null;
      };

      document.addEventListener('mousemove', onMouseMove);
      document.addEventListener('mouseup', onMouseUp);
    }
  };

  // 过滤树节点
  const filteredTreeData = useMemo(
    () => filterTree(mockGroups, searchTerm),
    [searchTerm]
  );

  return (
    <div className="flex-1 p-4 pb-0 overflow-auto flex flex-col ">
      <TopologyToolbar
        onEdit={() => console.log('Edit clicked')}
        onSave={() => console.log('Save clicked')}
        onZoomIn={zoomIn}
        onZoomOut={zoomOut}
        onFit={handleFit}
        onDelete={handleDelete}
        onSelectMode={handleSelectMode}
        isSelectMode={isSelectMode}
      />

      <div className="flex-1 flex overflow-hidden relative">
        {!collapsed && (
          <InstanceTree
            placeholder={t('common.searchPlaceHolder')}
            treeData={filteredTreeData}
            inputValue={inputValue}
            onSearch={setSearchTerm}
            onInputChange={setInputValue}
            onSelect={onTreeSelect}
          />
        )}
        <Button
          type="text"
          className={`absolute z-10 w-6 h-6 top-[20px] p-0 border border-[var(--color-border-3)] bg-[var(--color-bg-1)] flex items-center justify-center cursor-pointer rounded-full transition-all duration-300 ${
            collapsed
              ? 'left-0 border-l-0 rounded-tl-none rounded-bl-none'
              : 'left-[200px] -translate-x-1/2'
          }`}
          onClick={() => setCollapsed(!collapsed)}
        >
          {collapsed ? <RightOutlined /> : <LeftOutlined />}
        </Button>
        <div className="flex-1 bg-white relative">
          <div ref={containerRef} className="absolute inset-0" />
        </div>
      </div>

      <InstanceModal
        visible={modalVisible}
        dataSource={instanceOptions}
        selectedRowKeys={selectedRowKeys}
        onOk={onModalOk}
        onCancel={onModalCancel}
        onSelect={setSelectedRowKeys}
      />

      <ContextMenu
        visible={contextMenuVisible}
        position={contextMenuPosition}
        onMenuClick={handleMenuClick}
      />
    </div>
  );
};

export default Topology;

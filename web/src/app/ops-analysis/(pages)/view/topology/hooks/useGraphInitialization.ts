import { useEffect } from 'react';
import { Graph } from '@antv/x6';
import { Selection } from '@antv/x6-plugin-selection';
import type { Graph as X6Graph, Edge } from '@antv/x6';
import {
  getNodeStyle,
  getEdgeStyle,
  addEdgeTools,
  showPorts,
  hideAllPorts,
} from '../utils/topologyUtils';
import {
  mockInitialNodes,
  mockInitialEdges,
} from '../../mockData';

export const useGraphInitialization = (
  containerRef: React.RefObject<HTMLDivElement>,
  setGraphInstance: (graph: Graph | null) => void,
  setContextMenuVisible: (visible: boolean) => void,
  setContextMenuPosition: (position: { x: number; y: number }) => void,
  setContextMenuNodeId: (id: string) => void,
  setSelectedCells: (cells: string[]) => void,
  openEdgeConfig: (edge: Edge, sourceNode: any, targetNode: any) => void,
  startTextEdit: (nodeId: string, currentText: string) => void,
  finishTextEdit: () => void,
  isEditModeRef: React.MutableRefObject<boolean>
) => {
  useEffect(() => {
    if (!containerRef.current) return;

    const graph: X6Graph = new Graph({
      container: containerRef.current,
      grid: true,
      panning: true,
      mousewheel: { enabled: true, modifiers: 'ctrl' },
      connecting: {
        anchor: {
          name: 'center',
          args: {
            dx: 0,
            dy: 0,
          },
        },
        connectionPoint: {
          name: 'anchor',
        },
        allowBlank: false,
        allowMulti: true,
        allowLoop: false,
        highlight: true,
        snap: {
          radius: 20,
        },
        createEdge: () =>
          graph.createEdge({ shape: 'edge', ...getEdgeStyle('single') }),
        validateMagnet: ({ magnet }) => {
          return (
            isEditModeRef.current && magnet.getAttribute('magnet') === 'true'
          );
        },
        validateConnection: ({
          sourceMagnet,
          targetMagnet,
          sourceView,
          targetView,
        }) => {
          if (!isEditModeRef.current) return false;

          // 必须连接到磁吸点（端口）
          if (!sourceMagnet || !targetMagnet) return false;

          // 源和目标必须是不同的节点
          if (sourceView === targetView) return false;

          // 检查源节点和目标节点不是文本节点
          const sourceNode = sourceView?.cell;
          const targetNode = targetView?.cell;

          if (
            sourceNode?.getData()?.type === 'text' ||
            targetNode?.getData()?.type === 'text'
          ) {
            return false;
          }

          // 确保连接的是有效的端口
          const sourceMagnetType = sourceMagnet.getAttribute('magnet');
          const targetMagnetType = targetMagnet.getAttribute('magnet');

          return sourceMagnetType === 'true' && targetMagnetType === 'true';
        },
      },
      interacting: {
        nodeMovable: true,
        edgeMovable: true,
        arrowheadMovable: true,
        vertexMovable: false,
        vertexAddable: false,
        vertexDeletable: false,
        magnetConnectable: true,
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

    // 添加初始节点和边
    mockInitialNodes.forEach((nodeConfig: any) => {
      graph.addNode({
        ...nodeConfig,
        ...getNodeStyle(),
      });
    });

    mockInitialEdges.forEach((edgeConfig: any) => {
      const edge = graph.addEdge({
        ...edgeConfig,
        ...getEdgeStyle('single'),
      });
      addEdgeTools(edge);
    });

    // 设置事件监听器
    const hideCtx = () => setContextMenuVisible(false);
    document.addEventListener('click', hideCtx);

    // 右键菜单事件
    graph.on('node:contextmenu', ({ e, node }) => {
      e.preventDefault();
      setContextMenuVisible(true);
      setContextMenuPosition({ x: e.clientX, y: e.clientY });
      setContextMenuNodeId(node.id);
    });

    // 边连接事件
    graph.on('edge:connected', ({ edge, isNew }: any) => {
      console.log('Edge connected:', { edge: edge.id, isNew });
      if (!edge || !isEditModeRef.current) return;

      // 设置边的样式
      edge.setAttrs(getEdgeStyle('single').attrs);

      // 添加边的工具
      addEdgeTools(edge);

      // 设置默认数据
      edge.setData({
        lineType: 'network line',
        lineName: '',
      });
    });

    graph.on('edge:disconnected', ({ edge }: any) => {
      console.log('Edge disconnected:', edge.id);
    });

    graph.on('edge:change:source edge:change:target', ({ edge }: any) => {
      console.log('Edge endpoint changed:', edge.id);
    });

    // 连接开始时显示所有端口
    graph.on('edge:connecting', () => {
      if (isEditModeRef.current) {
        graph.getNodes().forEach((node: any) => {
          const nodeData = node.getData();
          if (nodeData?.type !== 'text') {
            showPorts(graph, node);
          }
        });
      }
    });

    // 连接结束时隐藏端口
    graph.on('edge:connected edge:disconnected', () => {
      setTimeout(() => {
        hideAllPorts(graph);
      }, 100);
    });

    // 选择变化事件
    graph.on('selection:changed', ({ selected }) => {
      // 只有在编辑模式下才处理选择变化
      if (!isEditModeRef.current) return;

      setSelectedCells(selected.map((cell) => cell.id));
      // 只有当选择了单个边时才打开配置面板
      if (selected.length === 1 && selected[0].isEdge()) {
        const edge = selected[0];
        addEdgeTools(edge);
        // 选中边时打开配置面板
        const sourceId = edge.getSourceCellId();
        const targetId = edge.getTargetCellId();
        const sourceNode = graph.getCellById(sourceId);
        const targetNode = graph.getCellById(targetId);
        if (sourceNode && targetNode) {
          openEdgeConfig(edge, sourceNode, targetNode);
        }
      } else {
        // 多选或选择节点时，只添加工具
        selected.forEach((cell) => {
          if (cell.isEdge()) {
            addEdgeTools(cell);
          }
        });
      }
    });

    // 双击边进入编辑模式（添加拐点）
    graph.on('edge:dblclick', ({ edge }) => {
      addEdgeTools(edge);
    });

    // 双击文本节点进入编辑模式
    graph.on('node:dblclick', ({ node }) => {
      const nodeData = node.getData();
      if (nodeData?.type === 'text') {
        const currentText = String(
          node.getAttrs()?.label?.text || '双击编辑文本'
        );

        const textToEdit =
          nodeData?.isPlaceholder || currentText === '双击编辑文本'
            ? ''
            : currentText;
        startTextEdit(node.id, textToEdit);
      }
    });

    // 点击画布空白处完成文本编辑
    graph.on('blank:click', () => {
      hideAllPorts(graph);
      setContextMenuVisible(false);

      // 如果正在编辑文本，完成编辑
      setTimeout(() => {
        finishTextEdit();
      }, 0);
    });

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

    // 初始化端口透明度
    graph.getNodes().forEach((node) => {
      // 只为有端口的节点设置透明度（排除文本节点）
      const nodeData = node.getData();
      if (nodeData?.type !== 'text') {
        ['top', 'bottom', 'left', 'right'].forEach((port) =>
          node.setPortProp(port, 'attrs/circle/opacity', 0)
        );
      }
    });

    return () => {
      document.removeEventListener('click', hideCtx);
      graph.dispose();
    };
  }, [
    containerRef,
    setGraphInstance,
    setContextMenuVisible,
    setContextMenuPosition,
    setContextMenuNodeId,
    setSelectedCells,
    openEdgeConfig,
    startTextEdit,
    finishTextEdit,
    isEditModeRef,
  ]);
};

import { useCallback, useEffect } from 'react';
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

export const useGraphOperations = (
  containerRef: React.RefObject<HTMLDivElement>,
  state: any
) => {
  const {
    graphInstance,
    setGraphInstance,
    scale,
    setScale,
    selectedCells,
    setSelectedCells,
    setIsEditMode,
    setContextMenuVisible,
    setContextMenuPosition,
    setContextMenuNodeId,
    isEditModeRef,
    finishTextEditRef,
    startTextEditRef,
    isEditingText,
    setOriginalText,
    setEditPosition,
    setInputWidth,
    setIsEditingText,
    setEditingNodeId,
    setTempTextInput,
    setCurrentEdgeData,
    setEdgeConfigVisible,
  } = state;

  // 初始化图形
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
          args: { dx: 0, dy: 0 },
        },
        connectionPoint: { name: 'anchor' },
        allowBlank: false,
        allowMulti: true,
        allowLoop: false,
        highlight: true,
        snap: { radius: 20 },
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
          if (!sourceMagnet || !targetMagnet) return false;
          if (sourceView === targetView) return false;

          const sourceNode = sourceView?.cell;
          const targetNode = targetView?.cell;

          if (
            sourceNode?.getData()?.type === 'text' ||
            targetNode?.getData()?.type === 'text'
          ) {
            return false;
          }

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

    // 绑定事件
    bindGraphEvents(graph);

    return () => {
      graph.dispose();
    };
  }, []);

  // 绑定图形事件
  const bindGraphEvents = (graph: X6Graph) => {
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
    graph.on('edge:connected', ({ edge }: any) => {
      if (!edge || !isEditModeRef.current) return;
      edge.setAttrs(getEdgeStyle('single').attrs);
      addEdgeTools(edge);
      edge.setData({
        lineType: 'network line',
        lineName: '',
      });
    });

    // 连接开始/结束时的端口显示
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

    graph.on('edge:connected edge:disconnected', () => {
      setTimeout(() => {
        hideAllPorts(graph);
      }, 100);
    });

    // 选择变化事件
    graph.on('selection:changed', ({ selected }) => {
      if (!isEditModeRef.current) return;

      setSelectedCells(selected.map((cell) => cell.id));

      if (selected.length === 1 && selected[0].isEdge()) {
        const edge = selected[0];
        addEdgeTools(edge);

        const sourceId = edge.getSourceCellId();
        const targetId = edge.getTargetCellId();
        const sourceNode = graph.getCellById(sourceId);
        const targetNode = graph.getCellById(targetId);

        if (sourceNode && targetNode) {
          openEdgeConfig(edge, sourceNode, targetNode);
        }
      } else {
        selected.forEach((cell) => {
          if (cell.isEdge()) {
            addEdgeTools(cell);
          }
        });
      }
    });

    // 双击事件
    graph.on('edge:dblclick', ({ edge }) => {
      addEdgeTools(edge);
    });

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
        startTextEditRef.current?.(node.id, textToEdit);
      }
    });

    // 空白点击事件
    graph.on('blank:click', () => {
      hideAllPorts(graph);
      setContextMenuVisible(false);
      setTimeout(() => {
        finishTextEditRef.current?.();
      }, 0);
    });

    // 鼠标进入/离开事件
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
      const nodeData = node.getData();
      if (nodeData?.type !== 'text') {
        ['top', 'bottom', 'left', 'right'].forEach((port) =>
          node.setPortProp(port, 'attrs/circle/opacity', 0)
        );
      }
    });
  };

  // 打开边配置
  const openEdgeConfig = (edge: Edge, sourceNode: any, targetNode: any) => {
    const edgeData = {
      id: edge.id,
      lineType: edge.getData()?.lineType || 'network line',
      lineName: edge.getData()?.lineName || '',
      sourceNode: {
        id: sourceNode.id,
        name: sourceNode.getLabel?.() || sourceNode.label || sourceNode.id,
      },
      targetNode: {
        id: targetNode.id,
        name: targetNode.getLabel?.() || targetNode.label || targetNode.id,
      },
    };
    setCurrentEdgeData(edgeData);
    setEdgeConfigVisible(true);
  };

  // 图形操作方法
  const zoomIn = useCallback(() => {
    if (graphInstance) {
      const next = scale + 0.1;
      graphInstance.zoom(next, { absolute: true });
      setScale(next);
    }
  }, [graphInstance, scale, setScale]);

  const zoomOut = useCallback(() => {
    if (graphInstance) {
      const next = scale - 0.1 > 0.1 ? scale - 0.1 : 0.1;
      graphInstance.zoom(next, { absolute: true });
      setScale(next);
    }
  }, [graphInstance, scale, setScale]);

  const handleFit = useCallback(() => {
    if (graphInstance && containerRef.current) {
      graphInstance.zoomToFit({ padding: 20, maxScale: 1 });
      setScale(1);
    }
  }, [graphInstance, setScale]);

  const handleDelete = useCallback(() => {
    if (graphInstance && selectedCells.length > 0) {
      graphInstance.removeCells(selectedCells);
      setSelectedCells([]);
    }
  }, [graphInstance, selectedCells, setSelectedCells]);

  const handleSelectMode = useCallback(() => {
    if (graphInstance) {
      graphInstance.enableSelection();
    }
  }, [graphInstance]);

  const handleSave = useCallback(() => {
    console.log('保存拓扑图...');
    setIsEditMode(false);
    isEditModeRef.current = false;

    if (graphInstance) {
      graphInstance.disablePlugins(['selection']);

      if (isEditingText) {
        setIsEditingText(false);
        setEditingNodeId(null);
        setTempTextInput('');
        setEditPosition({ x: 0, y: 0 });
        setInputWidth(120);
        setOriginalText('');
      }

      setContextMenuVisible(false);
      graphInstance.cleanSelection();
      setSelectedCells([]);
    }
  }, [graphInstance, isEditingText, setIsEditMode]);

  return {
    zoomIn,
    zoomOut,
    handleFit,
    handleDelete,
    handleSelectMode,
    handleSave,
  };
};

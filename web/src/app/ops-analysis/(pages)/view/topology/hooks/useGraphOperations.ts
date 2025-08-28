/**
 * useGraphOperations Hook
 * 
 * 拓扑图操作管理核心 Hook，负责图形的初始化、事件处理、节点操作和用户交互
 * 
 * 主要功能：
 * 1. 图形初始化 - 创建 X6 图形实例，配置画布属性和插件
 * 2. 事件绑定 - 处理节点/边的点击、双击、右键菜单、鼠标悬停等交互事件
 * 3. 节点操作 - 添加、更新、删除各类型节点（图标、文本、单值、图表）
 * 4. 数据更新 - 单值节点数据实时更新，图表节点数据加载
 * 5. 视图控制 - 缩放、适应画布、选择模式等视图操作
 * 6. 编辑模式 - 支持拖拽连线、节点编辑、文本编辑等编辑功能
 * 
 * 依赖关系：
 * - useGraphData: 处理数据序列化、保存和加载功能
 * - topologyUtils: 提供节点样式、边样式等工具函数
 * - X6 图形库: 提供底层图形渲染和交互能力
 * 
 * @param containerRef - 图形容器的 React ref
 * @param state - 组件状态管理对象，包含各种状态和状态更新函数
 * @returns 图形操作相关的方法集合
 */

import { useCallback, useEffect } from 'react';
import type { Graph as X6Graph } from '@antv/x6';
import ChartNode from '../components/chartNode';
import { formatTimeRange } from '@/app/ops-analysis/utils/widgetDataTransform';
import { Graph } from '@antv/x6';
import { iconList } from '@/app/cmdb/utils/common';
import { register } from '@antv/x6-react-shape';
import { Selection } from '@antv/x6-plugin-selection';
import { Transform } from '@antv/x6-plugin-transform';
import { COLORS, NODE_DEFAULTS } from '../constants/nodeDefaults';
import { useDataSourceApi } from '@/app/ops-analysis/api/dataSource';
import { TopologyNodeData } from '@/app/ops-analysis/types/topology';
import { DataSourceParam } from '@/app/ops-analysis/types/dashBoard';
import { v4 as uuidv4 } from 'uuid';
import {
  getEdgeStyle,
  hideAllPorts,
  hideAllEdgeTools,
  showPorts,
  showEdgeTools,
  addEdgeTools,
  getValueByPath,
  formatDisplayValue,
  updateNodeProperties,
  createPortConfig,
  adjustSingleValueNodeSize,
} from '../utils/topologyUtils';
import { registerNodes, createNodeByType } from '../utils/registerNode';
import { useGraphData } from './useGraphData';

export const useGraphOperations = (
  containerRef: React.RefObject<HTMLDivElement>,
  state: any
) => {
  useEffect(() => {
    register({
      shape: 'react-shape',
      width: NODE_DEFAULTS.CHART_NODE.width,
      height: NODE_DEFAULTS.CHART_NODE.height,
      component: ChartNode,
    });
  }, []);

  const { getSourceDataByApiId } = useDataSourceApi();

  // 样式重置和高亮的公共函数
  const resetAllStyles = useCallback((graph: X6Graph) => {
    graph.getNodes().forEach((node: any) => {
      const nodeData = node.getData();
      if (nodeData?.type !== 'text') {
        node.setAttrByPath('body/stroke', nodeData.config?.borderColor || '#ddd');
        node.setAttrByPath('body/strokeWidth', 1);
      }
    });

    // 重置所有边样式
    graph.getEdges().forEach((edge: any) => {
      edge.setAttrs({
        line: {
          ...edge.getAttrs().line,
          stroke: COLORS.EDGE.DEFAULT,
          strokeWidth: 1,
        },
      });
    });
  }, []);

  const highlightCell = useCallback((cell: any) => {
    if (cell.isNode()) {
      const nodeData = cell.getData();
      if (nodeData?.type !== 'text') {
        cell.setAttrByPath('body/stroke', '#1890ff');
        cell.setAttrByPath('body/strokeWidth', 1);
      }
    } else if (cell.isEdge()) {
      cell.setAttrs({
        line: {
          ...cell.getAttrs().line,
          stroke: COLORS.EDGE.SELECTED,
          strokeWidth: 1,
        },
      });
      addEdgeTools(cell);
    }
  }, []);

  const highlightNode = useCallback((node: any) => {
    const nodeData = node.getData();
    if (nodeData?.type !== 'text') {
      node.setAttrByPath('body/stroke', '#1890ff');
      node.setAttrByPath('body/strokeWidth', 1);
    }
  }, []);

  const resetNodeStyle = useCallback((node: any) => {
    const nodeData = node.getData();
    if (nodeData?.type !== 'text') {
      node.setAttrByPath('body/stroke', nodeData.config?.borderColor || '#ddd');
      node.setAttrByPath('body/strokeWidth', 1);
    }
  }, []);

  const {
    graphInstance,
    setGraphInstance,
    scale,
    setScale,
    selectedCells,
    setSelectedCells,
    setIsEditMode,
    isEditModeRef,
    isEditingText,
    setOriginalText,
    setEditPosition,
    setInputWidth,
    setIsEditingText,
    setEditingNodeId,
    setTempTextInput,
    setContextMenuVisible,
    setContextMenuPosition,
    setContextMenuNodeId,
    setEditingNodeData,
    setNodeEditVisible,
    setCurrentEdgeData,
    setEdgeConfigVisible,
    startTextEditRef,
    finishTextEditRef,
  } = state;

  const updateSingleNodeData = useCallback(async (nodeConfig: TopologyNodeData) => {
    if (!nodeConfig || !graphInstance) return;

    const node = graphInstance.getCellById(nodeConfig.id);
    if (!node) return;

    if (nodeConfig.type !== 'single-value' || !nodeConfig.dataSource || !nodeConfig.selectedFields?.length) {
      return;
    }

    try {
      let requestParams = {};

      if (nodeConfig.dataSourceParams && Array.isArray(nodeConfig.dataSourceParams)) {
        requestParams = nodeConfig.dataSourceParams.reduce((acc: any, param: DataSourceParam) => {
          if (param.value !== undefined) {
            acc[param.name] = (param.type === 'timeRange')
              ? formatTimeRange(param.value)
              : param.value;
          }
          return acc;
        }, {});
      }

      const resData = await getSourceDataByApiId(nodeConfig.dataSource, requestParams);
      if (resData && Array.isArray(resData) && resData.length > 0) {
        const latestData = resData[resData.length - 1];
        const field = nodeConfig.selectedFields[0];
        const value = getValueByPath(latestData, field);

        let displayValue;
        if (typeof value === 'number') {
          displayValue = value.toFixed(2);
        } else {
          displayValue = formatDisplayValue(value);
        }

        const currentNodeData = node.getData();
        const updatedData = {
          ...currentNodeData,
          isLoading: false,
          hasError: false,
        };
        node.setData(updatedData);
        node.setAttrByPath('label/text', displayValue);

        // 调整节点大小以适应文本内容
        adjustSingleValueNodeSize(node, displayValue);
      } else {
        throw new Error('无数据');
      }
    } catch (error) {
      console.error('更新单值节点数据失败:', error);
      const currentNodeData = node.getData();
      const updatedData = {
        ...currentNodeData,
        isLoading: false,
        hasError: true,
      };
      node.setData(updatedData);
      node.setAttrByPath('label/text', '无数据');

      // 调整节点大小以适应错误文本
      adjustSingleValueNodeSize(node, '无数据');
    }
  }, [graphInstance, getSourceDataByApiId]);

  const startLoadingAnimation = useCallback((node: any) => {
    const loadingStates = ['○ ○ ○', '● ○ ○', '○ ● ○', '○ ○ ●', '○ ○ ○'];
    let currentIndex = 0;

    const updateLoading = () => {
      const nodeData = node.getData();
      if (!nodeData?.isLoading) {
        return;
      }

      const currentLoadingText = loadingStates[currentIndex];
      node.setAttrByPath('label/text', currentLoadingText);

      // 调整节点大小以适应loading文本
      adjustSingleValueNodeSize(node, currentLoadingText, 80);

      currentIndex = (currentIndex + 1) % loadingStates.length;

      setTimeout(updateLoading, 300);
    };

    setTimeout(updateLoading, 300);
  }, []);

  const handleSave = useCallback(() => {
    setIsEditMode(false);
    isEditModeRef.current = false;

    if (graphInstance) {
      graphInstance.disablePlugins(['selection']);
      hideAllPorts(graphInstance);
      hideAllEdgeTools(graphInstance);

      graphInstance.getEdges().forEach((edge: any) => {
        edge.setAttrs({
          line: {
            ...edge.getAttrs().line,
            stroke: COLORS.EDGE.DEFAULT,
            strokeWidth: 1,
          },
        });
      });

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

  // 使用数据操作hooks
  const dataOperations = useGraphData(graphInstance, updateSingleNodeData, startLoadingAnimation, handleSave);

  const bindGraphEvents = (graph: X6Graph) => {
    const hideCtx = () => setContextMenuVisible(false);
    document.addEventListener('click', hideCtx);

    graph.on('node:contextmenu', ({ e, node }) => {
      e.preventDefault();
      setContextMenuVisible(true);
      setContextMenuPosition({ x: e.clientX, y: e.clientY });
      setContextMenuNodeId(node.id);
    });

    graph.on('node:click', ({ e, node }) => {
      if (e.shiftKey) {
        return;
      }

      const clickedNodeData = node.getData();

      if (clickedNodeData?.type === 'chart') {
        const chartNodeData = {
          ...clickedNodeData,
          id: node.id,
          label: node.prop('label'),
        };
        setEditingNodeData(chartNodeData);
        if (state.setViewConfigVisible) {
          state.setViewConfigVisible(true);
        }
      } else if (clickedNodeData?.type !== 'text') {
        const iconWidth = clickedNodeData.config?.width;
        const iconHeight = clickedNodeData.config?.height;
        setEditingNodeData({
          ...clickedNodeData,
          id: node.id,
          label: node.prop('label'),
          width: iconWidth,
          height: iconHeight,
        });
        setNodeEditVisible(true);
      }
    });

    graph.on('edge:click', ({ e, edge }) => {
      if (e.shiftKey) {
        return;
      }
      const edgeData = edge.getData();
      const sourceNode = edge.getSourceNode();
      const targetNode = edge.getTargetNode();

      if (edgeData && sourceNode && targetNode) {
        const sourceNodeData = sourceNode.getData();
        const targetNodeData = targetNode.getData();

        setCurrentEdgeData({
          id: edge.id,
          lineType: edgeData.lineType || 'common_line',
          lineName: edgeData.lineName || '',
          sourceNode: {
            id: sourceNode.id,
            name: sourceNodeData?.name || sourceNode.id,
          },
          targetNode: {
            id: targetNode.id,
            name: targetNodeData?.name || targetNode.id,
          },
          sourceInterface: edgeData.sourceInterface,
          targetInterface: edgeData.targetInterface,
        });
        setEdgeConfigVisible(true);
      }
    });

    graph.on('edge:connected', ({ edge }: any) => {
      if (!edge || !isEditModeRef.current) return;
      edge.setAttrs(getEdgeStyle('single').attrs);
      addEdgeTools(edge);
      edge.setData({
        lineType: 'common_line',
        lineName: '',
      });
    });

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
      hideAllPorts(graph);
    });

    graph.on('selection:changed', ({ selected }) => {
      if (!isEditModeRef.current) return;

      setSelectedCells(selected.map((cell) => cell.id));
      // 重置所有样式
      resetAllStyles(graph);
      // 高亮选中的元素
      selected.forEach(highlightCell);
    });

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

    graph.on('blank:click', () => {
      hideAllPorts(graph);
      hideAllEdgeTools(graph);
      setContextMenuVisible(false);

      // 重置所有样式
      resetAllStyles(graph);

      graph.cleanSelection();
      setSelectedCells([]);

      setTimeout(() => {
        finishTextEditRef.current?.();
      }, 0);
    });

    graph.on('node:mouseenter', ({ node }) => {
      hideAllPorts(graph);
      hideAllEdgeTools(graph);
      const nodeData = node.getData();
      if (nodeData?.type !== 'text') {
        showPorts(graph, node);
        const isSelected = selectedCells.includes(node.id);
        if (!isSelected) {
          highlightNode(node);
        }
      }
    });

    graph.on('edge:mouseenter', ({ edge }) => {
      hideAllPorts(graph);
      hideAllEdgeTools(graph);
      showPorts(graph, edge);
      showEdgeTools(edge);
    });

    graph.on('node:mouseleave', ({ node }) => {
      hideAllPorts(graph);
      hideAllEdgeTools(graph);
      const isSelected = selectedCells.includes(node.id);
      if (!isSelected) {
        resetNodeStyle(node);
      }
    });

    graph.on('edge:mouseleave', () => {
      hideAllPorts(graph);
      hideAllEdgeTools(graph);
    });

    // 统一的节点尺寸更新处理函数
    const handleNodeSizeUpdate = (node: any, isRealtime = false) => {
      const nodeData = node.getData();
      if (!nodeData?.config) return;

      const size = node.getSize();
      const updatedConfig = {
        ...nodeData,
        config: {
          ...nodeData.config,
          width: size.width,
          height: size.height,
        },
      };

      node.setData(updatedConfig);

      if (nodeData.type === 'icon' || nodeData.type === 'single-value') {
        if (!isRealtime) {
          updateNodeProperties(node, updatedConfig, iconList);
        }
      } else if (nodeData.type === 'chart') {
        const chartPortConfig = createPortConfig();
        node.prop('ports', chartPortConfig);
      }
    };

    // 拖拽过程中的实时更新
    graph.on('node:resize', ({ node }) => {
      handleNodeSizeUpdate(node, true);
    });

    // 拖拽结束后的最终更新
    graph.on('node:resized', ({ node }) => {
      handleNodeSizeUpdate(node, false);
    });

    graph.getNodes().forEach((node) => {
      const nodeData = node.getData();
      if (nodeData?.type !== 'text') {
        ['top', 'bottom', 'left', 'right'].forEach((port) =>
          node.setPortProp(port, 'attrs/circle/opacity', 0)
        );
      }
    });
  };

  // 图形初始化
  useEffect(() => {
    if (!containerRef.current) return;

    // 首先注册所有节点类型
    registerNodes();

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
        connectionPoint: { name: 'boundary' },
        connector: { name: 'normal' },
        router: { name: 'manhattan' },
        allowBlank: false,
        allowMulti: true,
        allowLoop: false,
        highlight: true,
        snap: { radius: 20 },
        createEdge: () =>
          graph.createEdge({
            shape: 'edge',
            ...getEdgeStyle('single')
          }),
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
        showNodeSelectionBox: false,
        modifiers: 'shift',
        filter: (cell) => cell.isNode() || cell.isEdge(),
      })
    );

    // 节点缩放插件
    graph.use(
      new Transform({
        resizing: {
          enabled: (node) => {
            const nodeData = node.getData();
            return nodeData?.type !== 'text';
          },
          minWidth: 32,
          minHeight: 32,
          preserveAspectRatio: (node) => {
            const nodeData = node.getData();
            return nodeData?.type === 'icon' || nodeData?.type === 'single-value';
          },
        },
        rotating: false,
      })
    );

    bindGraphEvents(graph);
    setGraphInstance(graph);

    return () => {
      graph.dispose();
    };
  }, []);

  // 基础图形操作
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

  // 添加节点到画布
  const addNode = useCallback((nodeType: string, formValues: any, position: { x: number; y: number }) => {
    if (!graphInstance) {
      return null;
    }

    // 创建基础节点配置
    const nodeConfig: TopologyNodeData = {
      id: `node_${uuidv4()}`,
      type: nodeType,
      x: position.x,
      y: position.y,
      ...formValues,
    };

    // 使用注册的节点创建节点数据
    const nodeData = createNodeByType(nodeConfig, iconList);

    const addedNode = graphInstance.addNode(nodeData);

    // 如果是单值节点，调整大小以适应初始文本（节点名称）
    if (nodeConfig.type === 'single-value') {
      adjustSingleValueNodeSize(addedNode, nodeConfig.name || '单值节点');
    }

    // 如果是单值节点且有数据源，启动loading动画并更新数据显示
    if (nodeConfig.type === 'single-value' && nodeConfig.dataSource && nodeConfig.selectedFields?.length) {
      startLoadingAnimation(addedNode);
      updateSingleNodeData({ ...nodeConfig, id: addedNode.id });
    }

    return addedNode.id;
  }, [graphInstance, updateSingleNodeData, startLoadingAnimation]);

  const handleNodeUpdate = useCallback(async (values: any) => {
    if (!values) {
      return;
    }
    try {
      const updatedConfig = {
        id: state.editingNodeData.id,
        type: state.editingNodeData.type,
        name: values.name || state.editingNodeData.name,
        logoType: values.logoType || state.editingNodeData.logoType,
        logoIcon: values.logoIcon || state.editingNodeData.logoIcon,
        logoUrl: values.logoUrl || state.editingNodeData.logoUrl,
        dataSource: values.dataSource || state.editingNodeData.dataSource,
        dataSourceParams: values.dataSourceParams || state.editingNodeData.dataSourceParams,
        selectedFields: values.selectedFields || state.editingNodeData.selectedFields,
        config: {
          textColor: values.textColor || state.editingNodeData.config?.textColor,
          fontSize: values.fontSize || state.editingNodeData.config?.fontSize,
          backgroundColor: values.backgroundColor || state.editingNodeData.config?.backgroundColor,
          borderColor: values.borderColor || state.editingNodeData.config?.borderColor,
          width: values.width || state.editingNodeData.config?.width,
          height: values.height || state.editingNodeData.config?.height,
        },
      };

      if (!graphInstance) {
        return;
      }

      const node = graphInstance.getCellById(updatedConfig.id);
      if (!node) {
        return;
      }
      updateNodeProperties(node, updatedConfig, iconList);

      if (updatedConfig.type === 'single-value' && updatedConfig.dataSource && updatedConfig.selectedFields?.length) {
        updateSingleNodeData(updatedConfig);
      }

      state.setNodeEditVisible(false);
      state.setEditingNodeData(null);
    } catch (error) {
      console.error('节点更新失败:', error);
    }
  }, [graphInstance, updateSingleNodeData, state]);

  const handleViewConfigConfirm = useCallback((values: any) => {
    if (state.editingNodeData && graphInstance) {
      const node = graphInstance.getCellById(
        state.editingNodeData.id
      );
      if (node) {
        const updatedData = {
          ...state.editingNodeData,
          dataSource: values.dataSource,
          dataSourceParams: values.dataSourceParams,
          name: values.name || state.editingNodeData.name,
          valueConfig: {
            ...state.editingNodeData.valueConfig,
            chartType: values.chartType,
            dataSource: values.dataSource,
            dataSourceParams: values.dataSourceParams,
            name: values.name || state.editingNodeData.name,
          },
          isLoading: !!values.dataSource,
          hasError: false,
        };
        node.setData(updatedData);

        if (state.editingNodeData.type === 'chart' && values.dataSource) {
          dataOperations.loadChartNodeData(state.editingNodeData.id, updatedData.valueConfig);
        }
      }
    }
    state.setViewConfigVisible(false);
  }, [graphInstance, state, dataOperations]);

  const handleAddChartNode = useCallback(async (
    widget: string,
    config?: any,
    position?: { x: number; y: number }
  ) => {
    if (!graphInstance) {
      return null;
    }

    const defaultPosition = position || { x: 300, y: 200 };

    const chartNodeConfig: any = {
      widget: widget,
      name: config?.name,
      valueConfig: config.valueConfig,
      type: 'chart',
      dataSource: config?.dataSource,
      dataSourceParams: config?.dataSourceParams || [],
      isLoading: !!config?.dataSource,
      rawData: null,
      hasError: false,
    };

    const nodeId = addNode('chart', chartNodeConfig, defaultPosition);

    if (config?.dataSource && nodeId) {
      dataOperations.loadChartNodeData(nodeId, chartNodeConfig);
    }

    return nodeId;
  }, [graphInstance, addNode, dataOperations]);

  // 手动调整画布大小
  const resizeCanvas = useCallback((width?: number, height?: number) => {
    if (!graphInstance || !containerRef.current) return;

    if (width && height) {
      graphInstance.resize(width, height);
    } else {
      // 自动获取容器大小
      const rect = containerRef.current.getBoundingClientRect();
      graphInstance.resize(rect.width, rect.height);
    }
  }, [graphInstance]);

  return {
    zoomIn,
    zoomOut,
    handleFit,
    handleDelete,
    handleSelectMode,
    handleSave,
    addNode,
    handleNodeUpdate,
    handleViewConfigConfirm,
    handleAddChartNode,
    resizeCanvas,
    ...dataOperations,
  };
};

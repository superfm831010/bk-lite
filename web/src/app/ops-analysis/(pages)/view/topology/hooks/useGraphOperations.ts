
/**
 * 拓扑图操作管理核心 Hook，负责图形的初始化、事件处理、节点操作和用户交互
 */

import { useCallback, useEffect } from 'react';
import type { Graph as X6Graph } from '@antv/x6';
import { v4 as uuidv4 } from 'uuid';
import { formatTimeRange } from '@/app/ops-analysis/utils/widgetDataTransform';
import { Graph } from '@antv/x6';
import { Selection } from '@antv/x6-plugin-selection';
import { Transform } from '@antv/x6-plugin-transform';
import { MiniMap } from '@antv/x6-plugin-minimap';
import { COLORS } from '../constants/nodeDefaults';
import { useDataSourceApi } from '@/app/ops-analysis/api/dataSource';
import { TopologyNodeData } from '@/app/ops-analysis/types/topology';
import { DataSourceParam } from '@/app/ops-analysis/types/dashBoard';
import { updateNodeAttributes, registerNodes, createNodeByType } from '../utils/registerNode';
import { registerEdges } from '../utils/registerEdge';
import { useGraphData } from './useGraphData';
import {
  getEdgeStyle,
  hideAllPorts,
  hideAllEdgeTools,
  showPorts,
  showEdgeTools,
  addEdgeTools,
  getValueByPath,
  formatDisplayValue,
  createPortConfig,
  adjustSingleValueNodeSize,
} from '../utils/topologyUtils';

export const useGraphOperations = (
  containerRef: React.RefObject<HTMLDivElement>,
  state: any,
  minimapContainerRef?: React.RefObject<HTMLDivElement>,
  minimapVisible?: boolean
) => {
  const { getSourceDataByApiId } = useDataSourceApi();

  const resetAllStyles = useCallback((graph: X6Graph) => {
    graph.getNodes().forEach((node: any) => {
      const nodeData = node.getData();
      if (nodeData?.type !== 'text') {
        node.setAttrByPath('body/stroke', nodeData.styleConfig?.borderColor);
      }
    });

    graph.getEdges().forEach((edge: any) => {
      edge.setAttrs({
        line: {
          ...edge.getAttrs().line,
          stroke: COLORS.EDGE.DEFAULT,
        },
      });
    });
  }, []);

  const highlightCell = useCallback((cell: any) => {
    if (cell.isNode()) {
      const nodeData = cell.getData();
      if (nodeData?.type !== 'text') {
        cell.setAttrByPath('body/stroke', '#1890ff');
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
    }
  }, []);

  const resetNodeStyle = useCallback((node: any) => {
    const nodeData = node.getData();
    if (nodeData?.type !== 'text') {
      node.setAttrByPath('body/stroke', nodeData.styleConfig?.borderColor || '#ddd');
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
    setContextMenuTargetType,
    setCurrentEdgeData,
    startTextEditRef,
    finishTextEditRef,
  } = state;

  const updateSingleNodeData = useCallback(async (nodeConfig: TopologyNodeData) => {
    if (!nodeConfig || !graphInstance) return;

    const node = graphInstance.getCellById(nodeConfig.id);
    const { valueConfig } = nodeConfig || {};
    if (!node) return;

    if (nodeConfig.type !== 'single-value' || !valueConfig?.dataSource || !valueConfig?.selectedFields?.length) {
      return;
    }

    try {
      let requestParams = {};

      if (valueConfig.dataSourceParams && Array.isArray(valueConfig.dataSourceParams)) {
        requestParams = valueConfig.dataSourceParams.reduce((acc: any, param: DataSourceParam) => {
          if (param.value !== undefined) {
            acc[param.name] = (param.type === 'timeRange')
              ? formatTimeRange(param.value)
              : param.value;
          }
          return acc;
        }, {});
      }

      const resData = await getSourceDataByApiId(valueConfig.dataSource, requestParams);
      if (resData && Array.isArray(resData) && resData.length > 0) {
        const latestData = resData[resData.length - 1];
        const field = valueConfig.selectedFields[0];
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

  // 缩略图插件初始化函数
  const initMiniMap = useCallback((graph: X6Graph) => {
    if (minimapContainerRef?.current && minimapVisible) {
      graph.disposePlugins(['minimap']);
      graph.use(
        new MiniMap({
          container: minimapContainerRef.current,
          width: 210,
          height: 144,
          padding: 0,
          scalable: true,
          minScale: 0.01,
          maxScale: 16,
          graphOptions: {
            grid: false,
            background: false,
          },
        })
      );
    }
  }, [minimapContainerRef, minimapVisible]);

  // 监听缩略图可见性变化，重新初始化缩略图
  useEffect(() => {
    if (graphInstance) {
      if (minimapVisible) {
        setTimeout(() => {
          initMiniMap(graphInstance);
        }, 100);
      } else {
        try {
          graphInstance.disposePlugins(['minimap']);
        } catch (e) {
          console.log(e);
        }
      }
    }
  }, [graphInstance, minimapVisible, initMiniMap]);

  const dataOperations = useGraphData(graphInstance, updateSingleNodeData, startLoadingAnimation, handleSave);

  const bindGraphEvents = (graph: X6Graph) => {
    const hideCtx = () => setContextMenuVisible(false);
    document.addEventListener('click', hideCtx);

    graph.on('node:contextmenu', ({ e, node }) => {
      e.preventDefault();
      setContextMenuVisible(true);
      setContextMenuPosition({ x: e.clientX, y: e.clientY });
      setContextMenuNodeId(node.id);
      setContextMenuTargetType('node');
    });

    graph.on('node:click', ({ e }) => {
      if (e.shiftKey) {
        return;
      }
      // 移除直接打开配置面板的逻辑，改为通过右键菜单的"编辑"选项
    });

    graph.on('edge:contextmenu', ({ e, edge }) => {
      e.preventDefault();
      setContextMenuVisible(true);
      setContextMenuPosition({ x: e.clientX, y: e.clientY });
      setContextMenuNodeId(edge.id);
      setContextMenuTargetType('edge');

      // 设置边数据用于配置
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

    // 监听边的拐点变化并保存
    graph.on('edge:change:vertices', ({ edge }: any) => {
      if (!edge || !isEditModeRef.current) return;

      const vertices = edge.getVertices();
      const currentData = edge.getData() || {};

      edge.setData({
        ...currentData,
        vertices: vertices
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
      resetAllStyles(graph);
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

    const handleNodeSizeUpdate = (node: any, isRealtime = false) => {
      const nodeData = node.getData();

      const size = node.getSize();
      const updatedConfig = {
        ...nodeData,
        styleConfig: {
          ...(nodeData.styleConfig || {}),
          width: size.width,
          height: size.height,
        },
      };

      node.setData(updatedConfig);

      if (nodeData.type === 'icon' || nodeData.type === 'single-value') {
        if (!isRealtime) {
          updateNodeAttributes(node, updatedConfig);
        }
      } else if (nodeData.type === 'chart') {
        const chartPortConfig = createPortConfig();
        node.prop('ports', chartPortConfig);
      }
    };

    graph.on('node:resize', ({ node }) => {
      handleNodeSizeUpdate(node, true);
    });

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

  useEffect(() => {
    if (!containerRef.current) return;

    registerNodes();
    registerEdges();

    const graph: X6Graph = new Graph({
      container: containerRef.current,
      width: containerRef.current.clientWidth,
      height: containerRef.current.clientHeight,
      grid: true,
      panning: true,
      autoResize: true,
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
      interacting: () => ({
        nodeMovable: state.isEditModeRef.current,
        edgeMovable: state.isEditModeRef.current,
        arrowheadMovable: state.isEditModeRef.current,
        vertexMovable: state.isEditModeRef.current,
        vertexAddable: state.isEditModeRef.current,
        vertexDeletable: state.isEditModeRef.current,
        magnetConnectable: state.isEditModeRef.current,
      }),
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

  const addNewNode = useCallback((nodeConfig: any) => {
    if (!graphInstance) {
      return null;
    }
    const nodeData = createNodeByType(nodeConfig);
    const { valueConfig } = nodeConfig || {};
    const addedNode = graphInstance.addNode(nodeData);
    if (nodeConfig.type === 'single-value') {
      adjustSingleValueNodeSize(addedNode, nodeConfig.name || '单值节点');
    }
    if (nodeConfig.type === 'single-value' && valueConfig?.dataSource && valueConfig?.selectedFields?.length) {
      startLoadingAnimation(addedNode);
      updateSingleNodeData({ ...nodeConfig, id: addedNode.id });
    }
    return addedNode.id;
  }, [graphInstance, updateSingleNodeData, startLoadingAnimation]);

  const handleNodeUpdate = useCallback(async (values: any) => {
    if (!values) {
      return;
    }
    const editingNode = state.editingNodeData;
    const { valueConfig, styleConfig } = editingNode || {};
    try {
      const updatedConfig = {
        id: editingNode.id,
        type: editingNode.type,
        name: values.name || editingNode.name,
        description: values.description || editingNode.description || '',
        position: editingNode.position,
        logoType: values.logoType || editingNode.logoType,
        logoIcon: values.logoIcon || editingNode.logoIcon,
        logoUrl: values.logoUrl || editingNode.logoUrl,
        valueConfig: {
          selectedFields: values.selectedFields || valueConfig?.selectedFields,
          chartType: values.chartType || valueConfig?.chartType,
          dataSource: values.dataSource || valueConfig?.dataSource,
          dataSourceParams: values.dataSourceParams || valueConfig?.dataSourceParams,
        },
        styleConfig: {
          textColor: values.textColor || styleConfig?.textColor,
          fontSize: values.fontSize || styleConfig?.fontSize,
          backgroundColor: values.backgroundColor || styleConfig?.backgroundColor,
          borderColor: values.borderColor || styleConfig?.borderColor,
          borderWidth: values.borderWidth || styleConfig?.borderWidth,
          width: values.width || styleConfig?.width,
          height: values.height || styleConfig?.height,
          lineType: values.lineType || styleConfig?.lineType,
          shapeType: values.shapeType || styleConfig?.shapeType,
        },
      };

      if (!graphInstance) {
        return;
      }

      const node = graphInstance.getCellById(updatedConfig.id);
      if (!node) {
        return;
      }
      updateNodeAttributes(node, updatedConfig);

      if (updatedConfig.type === 'single-value' && updatedConfig.valueConfig?.dataSource && updatedConfig.valueConfig?.selectedFields?.length) {
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
          name: values.name || state.editingNodeData.name,
          valueConfig: {
            chartType: values.chartType,
            dataSource: values.dataSource,
            dataSourceParams: values.dataSourceParams,
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


  const handleAddChartNode = useCallback(async (values: any) => {
    if (!graphInstance) {
      return null;
    }
    const nodeConfig = {
      id: `node_${uuidv4()}`,
      type: 'chart',
      name: values.name,
      description: values.description || '',
      position: state.editingNodeData.position,
      styleConfig: {},
      valueConfig: {
        chartType: values.chartType,
        dataSource: values.dataSource,
        dataSourceParams: values.dataSourceParams,
      },
    };
    const nodeId = addNewNode(nodeConfig);
    if (nodeConfig.valueConfig?.dataSource && nodeId) {
      dataOperations.loadChartNodeData(nodeId, nodeConfig.valueConfig);
    }
  }, [graphInstance, addNewNode, dataOperations]);


  const resizeCanvas = useCallback((width?: number, height?: number) => {
    if (!graphInstance) return;
    if (width && height) {
      graphInstance.resize(width, height);
    } else {
      graphInstance.resize();
    }
  }, [graphInstance]);

  const toggleEditMode = useCallback(() => {
    const newEditMode = !state.isEditMode;
    state.setIsEditMode(newEditMode);
    state.isEditModeRef.current = newEditMode;

    if (graphInstance) {
      if (newEditMode) {
        graphInstance.enablePlugins(['selection']);
      } else {
        graphInstance.disablePlugins(['selection']);

        if (state.isEditingText) {
          state.setIsEditingText(false);
          state.setEditingNodeId(null);
          state.setTempTextInput('');
          state.setEditPosition({ x: 0, y: 0 });
          state.setInputWidth(120);
          state.setOriginalText('');
        }

        state.setContextMenuVisible(false);
        graphInstance.cleanSelection();
        state.setSelectedCells([]);
      }
    }
  }, [state, graphInstance]);

  const getEditNodeInitialValues = useCallback(() => {
    if (!state.editingNodeData) return {};

    const editingNodeData = state.editingNodeData;
    const baseValues = {
      name: editingNodeData.name
    };

    const styleConfig = editingNodeData.styleConfig || {};
    const valueConfig = editingNodeData.valueConfig || {};
    switch (editingNodeData.type) {
      case 'single-value':
        return {
          ...baseValues,
          fontSize: styleConfig.fontSize,
          textColor: styleConfig.textColor,
          backgroundColor: styleConfig.backgroundColor,
          borderColor: styleConfig.borderColor,
          selectedFields: valueConfig.selectedFields || [],
          dataSource: valueConfig.dataSource,
          dataSourceParams: valueConfig.dataSourceParams || {},
        };

      case 'icon':
        return {
          ...baseValues,
          logoType: editingNodeData.logoType || 'default',
          logoIcon: editingNodeData.logoType === 'default' ? editingNodeData.logoIcon : 'cc-host',
          logoUrl: editingNodeData.logoType === 'custom' ? editingNodeData.logoUrl : undefined,
          width: styleConfig.width,
          height: styleConfig.height,
          backgroundColor: styleConfig.backgroundColor,
          borderColor: styleConfig.borderColor,
          borderWidth: styleConfig.borderWidth,
        };

      case 'basic-shape':
        return {
          ...baseValues,
          width: styleConfig.width,
          height: styleConfig.height,
          backgroundColor: styleConfig.backgroundColor,
          borderColor: styleConfig.borderColor,
          borderWidth: styleConfig.borderWidth,
          lineType: styleConfig.lineType,
          shapeType: styleConfig.shapeType,
        };

      default:
        return baseValues;
    }
  }, [state.editingNodeData]);

  const handleNodeEditClose = useCallback(() => {
    state.setNodeEditVisible(false);
    state.setEditingNodeData(null);
  }, [state]);

  return {
    zoomIn,
    zoomOut,
    handleFit,
    handleDelete,
    handleSelectMode,
    handleSave,
    addNewNode,
    handleNodeUpdate,
    handleViewConfigConfirm,
    handleAddChartNode,
    resizeCanvas,
    toggleEditMode,
    getEditNodeInitialValues,
    handleNodeEditClose,
    ...dataOperations,
  };
};

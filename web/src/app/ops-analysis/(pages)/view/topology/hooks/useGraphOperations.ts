import { useCallback, useEffect, useState } from 'react';
import type { Graph as X6Graph, Edge } from '@antv/x6';
import { formatTimeRange } from '@/app/ops-analysis/hooks/useWidgetData';
import { Graph } from '@antv/x6';
import { Selection } from '@antv/x6-plugin-selection';
import { message } from 'antd';
import { COLORS } from '../constants/nodeDefaults';
import { iconList } from '@/app/cmdb/utils/common';
import { useTopologyApi } from '@/app/ops-analysis/api/topology';
import { useDataSourceApi } from '@/app/ops-analysis/api/dataSource';
import {
  getEdgeStyle,
  getEdgeStyleWithLabel,
  addEdgeTools,
  showPorts,
  hideAllPorts,
  getSingleValueNodeStyle,
  getIconNodeStyle,
  getTextNodeStyle,
  getLogoUrl,
  showEdgeTools,
  hideAllEdgeTools,
  getValueByPath,
  formatDisplayValue,
  updateNodeProperties,
  normalizeNodeConfig,
} from '../utils/topologyUtils';

export const useGraphOperations = (
  containerRef: React.RefObject<HTMLDivElement>,
  state: any
) => {
  const [loading, setLoading] = useState(false);

  const { getSourceDataByApiId } = useDataSourceApi();

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
    setNodeEditVisible,
    setEditingNodeData,
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
    bindGraphEvents(graph);


    return () => {
      graph.dispose();
    };
  }, []);

  // 加载拓扑数据
  const loadTopologyData = useCallback((data: { nodes: any[], edges: any[] }) => {
    if (!graphInstance) return;
    graphInstance.clearCells();

    data.nodes.forEach((nodeConfig) => {
      // 对加载的节点配置进行标准化，确保数据完整性
      const normalizedConfig = normalizeNodeConfig(nodeConfig);
      let nodeData: any;

      if (normalizedConfig.type === 'single-value') {
        nodeData = getSingleValueNodeStyle(normalizedConfig);
      } else if (normalizedConfig.type === 'text') {
        nodeData = getTextNodeStyle(normalizedConfig);
      } else {
        const logoUrl = getLogoUrl(normalizedConfig, iconList);
        nodeData = getIconNodeStyle(normalizedConfig, logoUrl);
      }

      graphInstance.addNode(nodeData);

      if (normalizedConfig.type === 'single-value' && normalizedConfig.dataSource && normalizedConfig.selectedFields?.length) {
        setTimeout(() => {
          updateNodeData(normalizedConfig);
        }, 100);
      }
    });

    data.edges.forEach((edgeConfig) => {
      const edgeData = {
        lineType: edgeConfig.lineType as 'line' | 'network line',
        lineName: edgeConfig.lineName,
        sourceInterface: edgeConfig.sourceInterface,
        targetInterface: edgeConfig.targetInterface,
        config: edgeConfig.config,
      };

      const edge = graphInstance.createEdge({
        id: edgeConfig.id,
        source: edgeConfig.source,
        target: edgeConfig.target,
        sourcePort: edgeConfig.sourcePort,
        targetPort: edgeConfig.targetPort,
        shape: 'edge',
        ...getEdgeStyleWithLabel(edgeData, 'single'),
        data: edgeData,
      });

      graphInstance.addEdge(edge);
    });

    setTimeout(() => {
      graphInstance.centerContent();
    }, 100);
  }, [graphInstance, normalizeNodeConfig]);


  // 更新单值数据显示
  const updateNodeData = useCallback(async (nodeConfig: any) => {
    if (!nodeConfig || !graphInstance) return;

    const node = graphInstance.getCellById(nodeConfig.id);
    if (!node) return;

    const nodeData = nodeConfig.data || nodeConfig;
    if (nodeData.type !== 'single-value' || !nodeData.dataSource || !nodeData.selectedFields?.length) {
      return;
    }

    try {
      let requestParams = {};

      if (nodeData.dataSourceParams && Array.isArray(nodeData.dataSourceParams)) {
        requestParams = nodeData.dataSourceParams.reduce((acc: any, param: any) => {
          if (param.value !== undefined) {
            acc[param.name] = (param.type === 'timeRange')
              ? formatTimeRange(param.value)
              : param.value;
          }
          return acc;
        }, {});
      }

      const data = await getSourceDataByApiId(nodeData.dataSource, requestParams);

      let displayText = nodeData.name;

      if (data) {
        const selectedField = nodeData.selectedFields[0];
        if (selectedField) {
          let value;

          if (Array.isArray(data) && data.length > 0) {
            value = getValueByPath(data[0], selectedField);
          } else if (typeof data === 'object') {
            value = getValueByPath(data, selectedField);
          }

          if (value !== undefined) {
            displayText = formatDisplayValue(value);
          }
        }
      }

      node.setAttrByPath('label/text', displayText);

    } catch {
      node.setAttrByPath('label/text', nodeData.name);
    }
  }, [graphInstance, getSourceDataByApiId]);

  const serializeTopologyData = useCallback(() => {
    if (!graphInstance) return { nodes: [], edges: [] };

    const nodes = graphInstance.getNodes().map((node: any) => {
      const nodeData = node.getData();
      const position = node.getPosition();

      const serializedNode: any = {
        id: node.id,
        x: position.x,
        y: position.y,
        type: nodeData.type,
        name: nodeData.name,
      };

      if (nodeData.dataSource) {
        serializedNode.dataSource = nodeData.dataSource;
      }

      if (nodeData.dataSourceParams) {
        serializedNode.dataSourceParams = nodeData.dataSourceParams;
      }

      if (nodeData.selectedFields) {
        serializedNode.selectedFields = nodeData.selectedFields;
      }

      if (nodeData.type === 'icon') {
        serializedNode.logo = nodeData.logo;
        serializedNode.logoType = nodeData.logoType;
        serializedNode.width = nodeData.width || nodeData.config?.width;
        serializedNode.height = nodeData.height || nodeData.config?.height;
        if (nodeData.config) {
          serializedNode.config = {
            backgroundColor: nodeData.config.backgroundColor,
            borderColor: nodeData.config.borderColor,
            textColor: nodeData.config.textColor,
            fontSize: nodeData.config.fontSize,
            width: nodeData.config.width,
            height: nodeData.config.height,
          };
        }
      } else if (nodeData.type === 'single-value') {
        if (nodeData.config) {
          serializedNode.config = {
            textColor: nodeData.config.textColor,
            fontSize: nodeData.config.fontSize,
            backgroundColor: nodeData.config.backgroundColor,
            borderColor: nodeData.config.borderColor,
          };
        }
      } else if (nodeData.type === 'text') {
        if (nodeData.config) {
          serializedNode.config = {
            fontSize: nodeData.config.fontSize,
            fontWeight: nodeData.config.fontWeight,
            textColor: nodeData.config.textColor,
          };
        }
      }

      return serializedNode;
    });

    const edges = graphInstance.getEdges().map((edge: any) => {
      const edgeData = edge.getData();
      const sourcePort = edge.getSourcePortId();
      const targetPort = edge.getTargetPortId();

      return {
        id: edge.id,
        source: edge.getSourceCellId(),
        target: edge.getTargetCellId(),
        sourcePort,
        targetPort,
        lineType: edgeData?.lineType || 'network line',
        lineName: edgeData?.lineName || '',
        sourceInterface: edgeData?.sourceInterface,
        targetInterface: edgeData?.targetInterface,
        config: edgeData?.config
          ? {
            strokeColor: edgeData.config.strokeColor,
            strokeWidth: edgeData.config.strokeWidth,
          }
          : undefined,
      };
    });

    return { nodes, edges };
  }, [graphInstance]);

  const { saveTopology, getTopologyDetail } = useTopologyApi();

  const handleSaveTopology = useCallback(async (selectedTopology: any) => {
    if (!selectedTopology?.data_id) {
      message.error('请先选择要保存的拓扑图');
      return;
    }

    setLoading(true);
    try {
      const topologyData = serializeTopologyData();
      const saveData = {
        name: selectedTopology.name,
        view_sets: {
          nodes: topologyData.nodes,
          edges: topologyData.edges,
        },
      };
      await saveTopology(selectedTopology.data_id, saveData);

      handleSave();

      message.success('拓扑图保存成功');
    } catch (error) {
      console.error('保存拓扑图失败:', error);
    } finally {
      setLoading(false);
    }
  }, [serializeTopologyData, saveTopology]);

  const handleLoadTopology = useCallback(async (topologyId: string | number) => {
    if (!graphInstance) {
      return;
    }

    setLoading(true);
    try {
      const topologyData = await getTopologyDetail(topologyId);

      const viewSets = topologyData.view_sets || {};
      loadTopologyData(viewSets);
    } catch (error) {
      console.error('加载拓扑图失败:', error);
    } finally {
      setLoading(false);
    }
  }, [graphInstance]);

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
      const nodeData = node.getData();
      if (nodeData?.type !== 'text') {
        const iconWidth = nodeData.config?.width;
        const iconHeight = nodeData.config?.height;

        setEditingNodeData({
          ...nodeData,
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
          lineType: edgeData.lineType || 'network line',
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
        lineType: 'network line',
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
      setTimeout(() => {
        hideAllPorts(graph);
      }, 100);
    });

    graph.on('selection:changed', ({ selected }) => {
      if (!isEditModeRef.current) return;

      setSelectedCells(selected.map((cell) => cell.id));

      graph.getNodes().forEach((node: any) => {
        const nodeData = node.getData();
        if (nodeData?.type !== 'text') {
          node.setAttrByPath('body/stroke', nodeData.config?.borderColor || '#ddd');
          node.setAttrByPath('body/strokeWidth', 1);
        }
      });

      graph.getEdges().forEach((edge: any) => {
        edge.setAttrs({
          line: {
            ...edge.getAttrs().line,
            stroke: edge.getAttrs().line?.stroke || COLORS.EDGE.DEFAULT,
            strokeWidth: edge.getAttrs().line?.strokeWidth || 1,
          },
        });
      });

      selected.forEach((cell) => {
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
      });

      if (selected.length === 1 && selected[0].isEdge()) {
        const edge = selected[0];
        const sourceId = edge.getSourceCellId();
        const targetId = edge.getTargetCellId();
        const sourceNode = graph.getCellById(sourceId);
        const targetNode = graph.getCellById(targetId);

        if (sourceNode && targetNode) {
          openEdgeConfig(edge, sourceNode, targetNode);
        }
      }
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

      graph.getNodes().forEach((node: any) => {
        const nodeData = node.getData();
        if (nodeData?.type !== 'text') {
          node.setAttrByPath('body/stroke', nodeData.config?.borderColor || '#ddd');
          node.setAttrByPath('body/strokeWidth', 1);
        }
      });

      graph.getEdges().forEach((edge: any) => {
        edge.setAttrs({
          line: {
            ...edge.getAttrs().line,
            stroke: COLORS.EDGE.DEFAULT,
            strokeWidth: 1,
          },
        });
      });

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
          node.setAttrByPath('body/stroke', '#1890ff');
          node.setAttrByPath('body/strokeWidth', 1);
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
      const nodeData = node.getData();
      if (nodeData?.type !== 'text') {
        // 只有在未选中状态才恢复默认边框
        const isSelected = selectedCells.includes(node.id);
        if (!isSelected) {
          node.setAttrByPath('body/stroke', nodeData.config?.borderColor || '#ddd');
          node.setAttrByPath('body/strokeWidth', 1);
        }
      }
    });

    graph.on('edge:mouseleave', () => {
      hideAllPorts(graph);
      hideAllEdgeTools(graph);
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

  const openEdgeConfig = (edge: Edge, sourceNode: any, targetNode: any) => {
    const edgeData = edge.getData();
    const sourceNodeData = sourceNode.getData?.() || {};
    const targetNodeData = targetNode.getData?.() || {};

    const currentEdgeData = {
      id: edge.id,
      lineType: edgeData?.lineType || 'network line',
      lineName: edgeData?.lineName || '',
      sourceNode: {
        id: sourceNode.id,
        name: sourceNodeData.name || sourceNode.id,
      },
      targetNode: {
        id: targetNode.id,
        name: targetNodeData.name || targetNode.id,
      },
      sourceInterface: edgeData?.sourceInterface,
      targetInterface: edgeData?.targetInterface,
    };
    setCurrentEdgeData(currentEdgeData);
    setEdgeConfigVisible(true);
  };

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

  // 添加节点到画布
  const addNode = useCallback((nodeType: string, formValues: any, position: { x: number; y: number }) => {
    if (!graphInstance) {
      return;
    }

    // 创建基础节点配置
    const baseConfig = {
      id: `node_${Date.now()}`,
      type: nodeType,
      x: position.x,
      y: position.y,
      ...formValues,
    };

    // 标准化节点配置
    const normalizedConfig = normalizeNodeConfig(baseConfig);

    let nodeData: any;

    if (normalizedConfig.type === 'single-value') {
      nodeData = getSingleValueNodeStyle(normalizedConfig);
    } else if (normalizedConfig.type === 'text') {
      nodeData = getTextNodeStyle(normalizedConfig);
    } else {
      const logoUrl = getLogoUrl(normalizedConfig, iconList);
      nodeData = getIconNodeStyle(normalizedConfig, logoUrl);
    }

    graphInstance.addNode(nodeData);

    // 如果是单值节点且有数据源，更新数据显示
    if (normalizedConfig.type === 'single-value' && normalizedConfig.dataSource && normalizedConfig.selectedFields?.length) {
      setTimeout(() => {
        updateNodeData(normalizedConfig);
      }, 500);
    }
  }, [graphInstance, normalizeNodeConfig, updateNodeData]);

  const updateNode = useCallback((nodeConfig: any) => {
    if (!graphInstance) {
      return;
    }

    const node = graphInstance.getCellById(nodeConfig.id);
    if (!node) {
      return;
    }

    updateNodeProperties(node, nodeConfig, iconList);
  }, [graphInstance]);

  const handleNodeUpdate = useCallback(async (values: any) => {
    if (!values) {
      return;
    }

    try {
      const updatedConfig = normalizeNodeConfig(values, state.editingNodeData);

      updateNode(updatedConfig);

      if (updatedConfig.type === 'single-value' && updatedConfig.dataSource && updatedConfig.selectedFields?.length) {
        setTimeout(() => {
          updateNodeData(updatedConfig);
        }, 500);
      }

      state.setNodeEditVisible(false);
      state.setEditingNodeData(null);
    } catch (error) {
      console.error('节点更新失败:', error);
    }
  }, [normalizeNodeConfig, updateNode, updateNodeData, state]);

  return {
    zoomIn,
    zoomOut,
    handleFit,
    handleDelete,
    handleSelectMode,
    handleSave,
    addNode,
    handleNodeUpdate,
    serializeTopologyData,
    handleSaveTopology,
    handleLoadTopology,
    loading,
    setLoading
  };
};

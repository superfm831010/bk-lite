import { useCallback, useEffect, useState } from 'react';
import type { Graph as X6Graph, Edge } from '@antv/x6';
import { Graph } from '@antv/x6';
import { Selection } from '@antv/x6-plugin-selection';
import { message } from 'antd';
import { COLORS, FORM_DEFAULTS } from '../constants/nodeDefaults';
import { iconList } from '@/app/cmdb/utils/common';
import { useTopologyApi } from '@/app/ops-analysis/api/topology';
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
} from '../utils/topologyUtils';

export const useGraphOperations = (
  containerRef: React.RefObject<HTMLDivElement>,
  state: any
) => {
  // 内部状态管理
  const [nodeEditFormInstance, setNodeEditFormInstance] = useState<any>(null);
  const [loading, setLoading] = useState(false);

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
    // 清空当前图形
    graphInstance.clearCells();

    // 加载节点
    data.nodes.forEach((nodeConfig) => {
      let nodeData: any;

      if (nodeConfig.type === 'single-value') {
        nodeData = getSingleValueNodeStyle(nodeConfig);
      } else if (nodeConfig.type === 'text') {
        nodeData = getTextNodeStyle(nodeConfig);
      } else {
        const logoUrl = getLogoUrl(nodeConfig, iconList);
        nodeData = getIconNodeStyle(nodeConfig, logoUrl);
      }

      graphInstance.addNode(nodeData);
    });

    // 加载边
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

    // 自适应画布
    setTimeout(() => {
      graphInstance.centerContent();
    }, 100);
  }, [graphInstance]);

  // 序列化图形数据，只保存样式相关的config
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

      // 根据节点类型保存相应配置，只保存样式相关字段
      if (nodeData.type === 'icon') {
        serializedNode.logo = nodeData.logo;
        serializedNode.logoType = nodeData.logoType;
        if (nodeData.config) {
          // 只保存样式相关的配置
          serializedNode.config = {
            backgroundColor: nodeData.config.backgroundColor,
            borderColor: nodeData.config.borderColor,
            textColor: nodeData.config.textColor,
            fontSize: nodeData.config.fontSize,
          };
        }
      } else if (nodeData.type === 'single-value') {
        serializedNode.dataSource = nodeData.dataSource;
        if (nodeData.config) {
          // 只保存样式相关的配置
          serializedNode.config = {
            textColor: nodeData.config.textColor,
            fontSize: nodeData.config.fontSize,
            backgroundColor: nodeData.config.backgroundColor,
            borderColor: nodeData.config.borderColor,
          };
        }
      } else if (nodeData.type === 'text') {
        if (nodeData.config) {
          // 只保存样式相关的配置
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
            // 只保存样式相关的配置
            strokeColor: edgeData.config.strokeColor,
            strokeWidth: edgeData.config.strokeWidth,
          }
          : undefined,
      };
    });

    return { nodes, edges };
  }, [graphInstance]);

  // API相关操作
  const { saveTopology, getTopologyDetail } = useTopologyApi();

  // 保存拓扑图
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

      // 调用原有的保存逻辑（退出编辑模式等）
      handleSave();

      message.success('拓扑图保存成功');
    } catch (error) {
      console.error('保存拓扑图失败:', error);
    } finally {
      setLoading(false);
    }
  }, [serializeTopologyData, saveTopology]);

  // 加载拓扑图数据
  const handleLoadTopology = useCallback(async (topologyId: string | number) => {
    // 如果 graphInstance 为 null，说明组件还没有完全初始化，直接返回
    if (!graphInstance) {
      return;
    }

    setLoading(true);
    try {
      const data = await getTopologyDetail(topologyId);
      const viewSets = data.view_sets || {};
      loadTopologyData(viewSets);
    } catch (error) {
      console.error('加载拓扑图失败:', error);
    } finally {
      setLoading(false);
    }
  }, [graphInstance, loadTopologyData, getTopologyDetail, setLoading]);

  // 绑定图形事件
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
        setEditingNodeData({
          ...nodeData,
          id: node.id,
          label: node.prop('label'),
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
        if (cell.isEdge()) {
          cell.setAttrs({
            line: {
              ...cell.getAttrs().line,
              stroke: COLORS.EDGE.SELECTED,
              strokeWidth: 2,
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
      hideAllEdgeTools(graph);
      setContextMenuVisible(false);

      // 清除所有边的高亮效果
      graph.getEdges().forEach((edge: any) => {
        edge.setAttrs({
          line: {
            ...edge.getAttrs().line,
            stroke: COLORS.EDGE.DEFAULT,
            strokeWidth: 2,
          },
        });
      });

      graph.cleanSelection();
      setSelectedCells([]);

      setTimeout(() => {
        finishTextEditRef.current?.();
      }, 0);
    });

    // 鼠标进入/离开事件
    graph.on('node:mouseenter', ({ node }) => {
      hideAllPorts(graph);
      hideAllEdgeTools(graph);
      showPorts(graph, node);
    });

    graph.on('edge:mouseenter', ({ edge }) => {
      hideAllPorts(graph);
      hideAllEdgeTools(graph);
      showPorts(graph, edge);
      showEdgeTools(edge);
    });

    graph.on('node:mouseleave', () => {
      hideAllPorts(graph);
      hideAllEdgeTools(graph);
    });

    graph.on('edge:mouseleave', () => {
      hideAllPorts(graph);
      hideAllEdgeTools(graph);
    });

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
  const addNode = useCallback((nodeConfig: any) => {
    if (!graphInstance) {
      return;
    }

    let nodeData: any;

    if (nodeConfig.type === 'single-value') {
      nodeData = getSingleValueNodeStyle(nodeConfig);
    } else {
      const logoUrl = getLogoUrl(nodeConfig, iconList);
      nodeData = getIconNodeStyle(nodeConfig, logoUrl);
    }

    graphInstance.addNode(nodeData);
  }, [graphInstance]);

  // 更新节点
  const updateNode = useCallback((nodeConfig: any) => {
    if (!graphInstance) {
      return;
    }

    const node = graphInstance.getCellById(nodeConfig.id);
    if (!node) {
      return;
    }

    // 更新节点标签
    node.setLabel(nodeConfig.name);

    if (nodeConfig.type === 'single-value') {
      // 单值节点 - 只更新文本相关属性
      node.setData({
        type: nodeConfig.type,
        name: nodeConfig.name,
        dataSource: nodeConfig.dataSource,
        config: nodeConfig.config,
      });

      // 更新单值节点的文本样式
      node.setAttrByPath('label/text', nodeConfig.name);
      if (nodeConfig.config?.textColor) {
        node.setAttrByPath('label/fill', nodeConfig.config.textColor);
      }
      if (nodeConfig.config?.fontSize) {
        node.setAttrByPath('label/fontSize', nodeConfig.config.fontSize);
      }
      if (nodeConfig.config?.backgroundColor) {
        node.setAttrByPath('body/fill', nodeConfig.config.backgroundColor);
      }
      if (nodeConfig.config?.borderColor) {
        node.setAttrByPath('body/stroke', nodeConfig.config.borderColor);
      }
    } else {
      // 图标节点 - 更新logo和其他属性
      const logoUrl = getLogoUrl(nodeConfig, iconList);

      node.setData({
        type: nodeConfig.type,
        name: nodeConfig.name,
        logo: nodeConfig.logo,
        logoType: nodeConfig.logoType,
        config: nodeConfig.config,
      });

      // 更新节点图标
      node.setAttrByPath('icon/xlink:href', logoUrl);
    }

  }, [graphInstance]);

  // 处理节点更新（编辑模式）
  const handleNodeUpdate = useCallback(async (nodeEditFormInstance: any) => {
    if (!nodeEditFormInstance) {
      return;
    }

    try {
      const values = await nodeEditFormInstance.validateFields();

      let updatedConfig: any;

      if (state.editingNodeData.type === 'single-value') {
        updatedConfig = {
          id: state.editingNodeData.id,
          type: state.editingNodeData.type,
          name: values.name,
          dataSource: values.dataSource,
          config: {
            query: values.query || FORM_DEFAULTS.SINGLE_VALUE.query,
            unit: values.unit || FORM_DEFAULTS.SINGLE_VALUE.unit,
            threshold: values.threshold || FORM_DEFAULTS.SINGLE_VALUE.threshold,
            textColor: values.textColor || FORM_DEFAULTS.SINGLE_VALUE.textColor,
            fontSize: values.fontSize || FORM_DEFAULTS.SINGLE_VALUE.fontSize,
            backgroundColor: values.backgroundColor || FORM_DEFAULTS.SINGLE_VALUE.backgroundColor,
            borderColor: values.borderColor || FORM_DEFAULTS.SINGLE_VALUE.borderColor,
          },
        };
      } else {
        // 图标节点 - 保持原有逻辑
        updatedConfig = {
          id: state.editingNodeData.id,
          type: state.editingNodeData.type,
          name: values.name,
          logo: values.logoType === 'default' ? values.logoIcon : values.logoUrl,
          logoType: values.logoType,
          dataSource: values.dataSource,
          config: {
            backgroundColor: values.backgroundColor || FORM_DEFAULTS.ICON_NODE.backgroundColor,
            borderColor: values.borderColor || FORM_DEFAULTS.ICON_NODE.borderColor,
          },
        };
      }

      updateNode(updatedConfig);

      state.setNodeEditVisible(false);
      state.setEditingNodeData(null);
    } catch (error) {
      console.error('表单验证失败:', error);
    }
  }, [updateNode, state]);

  return {
    zoomIn,
    zoomOut,
    handleFit,
    handleDelete,
    handleSelectMode,
    handleSave,
    addNode,
    updateNode,
    handleNodeUpdate,
    loadTopologyData,
    serializeTopologyData,
    handleSaveTopology,
    handleLoadTopology,
    nodeEditFormInstance,
    setNodeEditFormInstance,
    loading,
    setLoading
  };
};

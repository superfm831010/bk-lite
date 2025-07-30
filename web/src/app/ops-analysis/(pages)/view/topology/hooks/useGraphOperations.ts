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
import { iconList } from '@/app/cmdb/utils/common';

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

    // 节点点击事件 - 查看/编辑节点
    graph.on('node:click', ({ node }) => {
      const nodeData = node.getData();
      // 排除文本节点
      if (nodeData?.type !== 'text') {
        setEditingNodeData({
          ...nodeData,
          id: node.id,
          label: node.prop('label'),
        });
        setNodeEditVisible(true);
      }
    });

    // 边点击事件 - 查看/编辑边
    graph.on('edge:click', ({ edge }) => {
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

    const getLogoUrl = (nodeConfig: any) => {
      if (nodeConfig.logoType === 'default' && nodeConfig.logo) {
        const iconItem = iconList.find((item) => item.key === nodeConfig.logo);
        if (iconItem) {
          const url = `/app/assets/assetModelIcon/${iconItem.url}.svg`;
          return url;
        }
        const fallbackUrl = `/app/assets/assetModelIcon/${nodeConfig.logo}.svg`;
        return fallbackUrl;
      } else if (nodeConfig.logoType === 'custom' && nodeConfig.logo) {
        return nodeConfig.logo;
      }
      // 默认图标
      const defaultUrl = '/app/assets/assetModelIcon/cc-default_默认.svg';
      return defaultUrl;
    };

    let nodeData: any;

    if (nodeConfig.type === 'single-value') {
      // 单值节点 - 纯文本显示
      nodeData = {
        id: nodeConfig.id,
        x: nodeConfig.x || 100,
        y: nodeConfig.y || 100,
        shape: 'rect',
        width: 120,
        height: 40,
        label: nodeConfig.name,
        data: {
          type: nodeConfig.type,
          name: nodeConfig.name,
          dataSource: nodeConfig.dataSource,
          config: nodeConfig.config,
        },
        attrs: {
          body: {
            fill: '#ffffff',
            stroke: '#d9d9d9',
            strokeWidth: 1,
            rx: 6,
            ry: 6,
          },
          label: {
            text: nodeConfig.name,
            fill: '#333333',
            fontSize: 14,
            fontFamily: 'Arial, sans-serif',
            textAnchor: 'middle',
            textVerticalAnchor: 'middle',
          },
        },
        ports: {
          groups: {
            top: {
              position: { name: 'absolute', args: { x: 60, y: 0 } },
              attrs: {
                circle: {
                  magnet: true,
                  stroke: '#1890FF',
                  r: 6,
                  fill: '#FFFFFF',
                  opacity: 0,
                },
              },
            },
            bottom: {
              position: { name: 'absolute', args: { x: 60, y: 40 } },
              attrs: {
                circle: {
                  magnet: true,
                  stroke: '#1890FF',
                  r: 6,
                  fill: '#FFFFFF',
                  opacity: 0,
                },
              },
            },
            left: {
              position: { name: 'absolute', args: { x: 0, y: 20 } },
              attrs: {
                circle: {
                  magnet: true,
                  stroke: '#1890FF',
                  r: 6,
                  fill: '#FFFFFF',
                  opacity: 0,
                },
              },
            },
            right: {
              position: { name: 'absolute', args: { x: 120, y: 20 } },
              attrs: {
                circle: {
                  magnet: true,
                  stroke: '#1890FF',
                  r: 6,
                  fill: '#FFFFFF',
                  opacity: 0,
                },
              },
            },
          },
          items: [
            { id: 'top', group: 'top' },
            { id: 'bottom', group: 'bottom' },
            { id: 'left', group: 'left' },
            { id: 'right', group: 'right' },
          ],
        },
      };
    } else {
      // 图标节点 - 显示logo和名称
      const baseNodeStyle = getNodeStyle();
      const logoUrl = getLogoUrl(nodeConfig);

      nodeData = {
        id: nodeConfig.id,
        x: nodeConfig.x || 100,
        y: nodeConfig.y || 100,
        label: nodeConfig.name,
        data: {
          type: nodeConfig.type,
          name: nodeConfig.name,
          logo: nodeConfig.logo,
          logoType: nodeConfig.logoType,
          config: nodeConfig.config,
        },
        ...baseNodeStyle,
        // 覆盖图标的 URL
        attrs: {
          ...baseNodeStyle.attrs,
          icon: {
            ...baseNodeStyle.attrs.icon,
            'xlink:href': logoUrl,
          },
        },
      };
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

    // 获取logo URL
    const getLogoUrl = (nodeConfig: any) => {
      if (nodeConfig.logoType === 'default' && nodeConfig.logo) {
        const iconItem = iconList.find((item: any) => item.key === nodeConfig.logo);
        if (iconItem) {
          return `/app/assets/assetModelIcon/${iconItem.url}.svg`;
        }
        return `/app/assets/assetModelIcon/${nodeConfig.logo}.svg`;
      } else if (nodeConfig.logoType === 'custom' && nodeConfig.logo) {
        return nodeConfig.logo;
      }
      return '/app/assets/assetModelIcon/cc-default_默认.svg';
    };

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
      const logoUrl = getLogoUrl(nodeConfig);

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

      const updatedConfig = {
        id: state.editingNodeData.id,
        type: state.editingNodeData.type,
        name: values.name,
        logo: values.logoType === 'default' ? values.logoIcon : values.logoUrl,
        logoType: values.logoType,
        dataSource: values.dataSource,
        config: values,
      };

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
  };
};

import React, {
  useRef,
  useState,
  useEffect,
  useMemo,
  useCallback,
} from 'react';
import { Button } from 'antd';
import { RightOutlined, LeftOutlined } from '@ant-design/icons';
import { Graph } from '@antv/x6';
import { Selection } from '@antv/x6-plugin-selection';
import { useTranslation } from '@/utils/i18n';
import type { DataNode } from 'antd/lib/tree';
import type { Graph as X6Graph, Edge } from '@antv/x6';
import TopologyToolbar from './toolbar';
import InstanceTree from './instanceTree';
import InstanceModal from './instanceModal';
import ContextMenu from './contextMenu';
import EdgeConfigPanel from './edgeConfPanel';
import {
  getNodeStyle,
  getEdgeStyle,
  getTextNodeStyle,
  addEdgeTools,
  showPorts,
  hideAllPorts,
  filterTree,
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
  const [isEditMode, setIsEditMode] = useState(false);
  const [selectedCells, setSelectedCells] = useState<string[]>([]);
  const isDrawingRef = useRef(false);
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

  const [isEditingText, setIsEditingText] = useState(false);
  const [editingNodeId, setEditingNodeId] = useState<string | null>(null);
  const [tempTextInput, setTempTextInput] = useState('');
  const [editPosition, setEditPosition] = useState({ x: 0, y: 0 });

  const finishTextEditRef = useRef<(() => void) | null>(null);
  const startTextEditRef = useRef<((nodeId: string, currentText: string) => void) | null>(null);
  const isEditModeRef = useRef(isEditMode);

  const [edgeConfigVisible, setEdgeConfigVisible] = useState(false);
  const [currentEdgeData, setCurrentEdgeData] = useState<{
    id: string;
    lineType: string;
    lineName?: string;
    sourceNode: { id: string; name: string };
    targetNode: { id: string; name: string };
  } | null>(null);

  const updateDrawingState = (drawing: boolean) => {
    isDrawingRef.current = drawing;
  };

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

  const handleLineTypeChange = (lineType: string) => {
    if (currentEdgeData && graphInstance) {
      const edge = graphInstance.getCellById(currentEdgeData.id) as Edge;
      if (edge) {
        edge.setData({ ...edge.getData(), lineType });

        if (lineType === 'network line') {
          edge.setAttrs({
            line: {
              stroke: '#1890FF',
              strokeWidth: 2,
              strokeDasharray: '5,5',
            },
          });
          const labels = edge.getLabels();
          if (labels && labels.length > 0) {
            for (let i = labels.length - 1; i >= 0; i--) {
              edge.removeLabelAt(i);
            }
          }
        } else {
          edge.setAttrs({
            line: {
              stroke: '#8C8C8C',
              strokeWidth: 2,
              strokeDasharray: '',
            },
          });
        }
        setCurrentEdgeData({
          ...currentEdgeData,
          lineType,
        });
      }
    }
  };

  // 处理线条名称变更
  const handleLineNameChange = (lineName: string) => {
    if (currentEdgeData && graphInstance) {
      const edge = graphInstance.getCellById(currentEdgeData.id) as Edge;
      if (edge) {
        edge.setData({ ...edge.getData(), lineName });

        if (currentEdgeData.lineType === 'line') {
          if (lineName.trim()) {
            edge.setLabels([
              {
                attrs: {
                  text: {
                    text: lineName,
                    fill: '#333',
                    fontSize: 12,
                    textAnchor: 'middle',
                    textVerticalAnchor: 'middle',
                  },
                  rect: {
                    fill: 'white',
                    stroke: '#d9d9d9',
                    strokeWidth: 1,
                    rx: 4,
                    ry: 4,
                  },
                },
                position: 0.5,
              },
            ]);
          } else {
            const labels = edge.getLabels();
            if (labels && labels.length > 0) {
              for (let i = labels.length - 1; i >= 0; i--) {
                edge.removeLabelAt(i);
              }
            }
          }
        }

        setCurrentEdgeData({
          ...currentEdgeData,
          lineName,
        });
      }
    }
  };

  // 统一处理连线配置确认
  const handleEdgeConfigConfirm = (values: {
    lineType: string;
    lineName?: string;
  }) => {
    if (currentEdgeData && graphInstance) {
      const edge = graphInstance.getCellById(currentEdgeData.id) as Edge;
      if (edge) {
        // 更新边的数据
        edge.setData({ ...edge.getData(), ...values });

        // 根据线条类型更新样式
        if (values.lineType === 'network line') {
          // network line 类型时清除 label
          const labels = edge.getLabels();
          if (labels && labels.length > 0) {
            for (let i = labels.length - 1; i >= 0; i--) {
              edge.removeLabelAt(i);
            }
          }
        } else if (values.lineType === 'line') {
          // 如果有线条名称，显示在中心
          if (values.lineName && values.lineName.trim()) {
            edge.setLabels([
              {
                attrs: {
                  text: {
                    text: values.lineName,
                    fill: '#333',
                    fontSize: 12,
                    textAnchor: 'middle',
                    textVerticalAnchor: 'middle',
                  },
                  rect: {
                    fill: 'white',
                    stroke: '#d9d9d9',
                    strokeWidth: 1,
                    rx: 4,
                    ry: 4,
                  },
                },
                position: 0.5,
              },
            ]);
          } else {
            const labels = edge.getLabels();
            if (labels && labels.length > 0) {
              for (let i = labels.length - 1; i >= 0; i--) {
                edge.removeLabelAt(i);
              }
            }
          }
        }

        // 更新当前状态
        setCurrentEdgeData({
          ...currentEdgeData,
          ...values,
        });
      }
    }
  };

  // 关闭连线配置面板
  const closeEdgeConfig = () => {
    setEdgeConfigVisible(false);
    setCurrentEdgeData(null);
  };

  const handleAddText = useCallback(() => {
    if (!isEditMode || !graphInstance) return;

    const textNode = graphInstance.addNode({
      x: 100 + Math.random() * 50,
      y: 100 + Math.random() * 50,
      label: '双击编辑文本',
      data: { type: 'text', isPlaceholder: true },
      ...getTextNodeStyle(),
    });

    setTimeout(() => {
      startTextEditRef.current?.(textNode.id, '');
    }, 100);
  }, [isEditMode, graphInstance]);

  const startTextEdit = useCallback(
    (nodeId: string, currentText: string) => {
      if (!isEditMode || !graphInstance || !containerRef.current) return;

      const node = graphInstance.getCellById(nodeId);
      if (node) {
        const bbox = node.getBBox();
        const translate = graphInstance.translate();
        const scale = graphInstance.scale();

        const nodeCenterX = bbox.x + bbox.width / 2;
        const nodeCenterY = bbox.y + bbox.height / 2;

        const screenX = (nodeCenterX + translate.tx) * scale.sx;
        const screenY = (nodeCenterY + translate.ty) * scale.sy;

        const relativeX = screenX;
        const relativeY = screenY;

        setEditPosition({ x: relativeX, y: relativeY });
      }

      setIsEditingText(true);
      setEditingNodeId(nodeId);
      setTempTextInput(currentText);
    },
    [isEditMode, graphInstance]
  );

  const finishTextEdit = useCallback(() => {
    if (!graphInstance || !editingNodeId || !isEditingText) return;

    const node = graphInstance.getCellById(editingNodeId);
    if (node) {
      const finalText = tempTextInput.trim();
      const nodeData = node.getData() || {};

      if (finalText) {
        node.setAttrs({
          label: {
            text: finalText,
          },
        });

        const textWidth = finalText.length * 14 + 20;
        const nodeWidth = Math.max(80, Math.min(300, textWidth));
        node.prop('size', { width: nodeWidth, height: 40 });

        node.setData({ ...nodeData, isPlaceholder: false });
      } else {
        if (nodeData.isPlaceholder) {
          node.setAttrs({
            label: {
              text: '双击编辑文本',
            },
          });
          node.prop('size', { width: 120, height: 40 });
        } else {
          node.setAttrs({
            label: {
              text: '文本',
            },
          });
          node.prop('size', { width: 80, height: 40 });
        }
      }
    }

    setIsEditingText(false);
    setEditingNodeId(null);
    setTempTextInput('');
    setEditPosition({ x: 0, y: 0 });
  }, [graphInstance, editingNodeId, tempTextInput, isEditingText]);

  finishTextEditRef.current = finishTextEdit;
  startTextEditRef.current = startTextEdit;
  isEditModeRef.current = isEditMode;

  const cancelTextEdit = useCallback(() => {
    setIsEditingText(false);
    setEditingNodeId(null);
    setTempTextInput('');
    setEditPosition({ x: 0, y: 0 });
  }, []);

  // 切换编辑模式
  const toggleEditMode = useCallback(() => {
    const newEditMode = !isEditMode;
    setIsEditMode(newEditMode);

    if (graphInstance) {
      if (newEditMode) {
        graphInstance.enablePlugins(['selection']);
      } else {
        graphInstance.disablePlugins(['selection']);

        if (isEditingText) {
          cancelTextEdit();
        }

        setContextMenuVisible(false);

        graphInstance.cleanSelection();
        setSelectedCells([]);
      }
    }
  }, [isEditMode, graphInstance, isEditingText, cancelTextEdit]);

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

    const hideCtx = () => setContextMenuVisible(false);
    document.addEventListener('click', hideCtx);
    graph.on('node:contextmenu', ({ e, node }) => {
      if (!isEditModeRef.current) return;

      e.preventDefault();
      setContextMenuVisible(true);
      setContextMenuPosition({ x: e.clientX, y: e.clientY });
      setContextMenuNodeId(node.id);
    });

    // 添加更多连接相关的事件监听
    graph.on('edge:connecting', () => {
      console.log('Edge connecting started');
    });

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
        startTextEditRef.current?.(node.id, textToEdit);
      }
    });

    // 点击画布空白处完成文本编辑
    graph.on('blank:click', () => {
      hideAllPorts(graph);
      setContextMenuVisible(false);

      // 如果正在编辑文本，完成编辑
      // 使用 timeout 来确保状态更新正确处理
      setTimeout(() => {
        finishTextEditRef.current?.();
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

    // 移除之前的 blank:click 事件处理，我们会在下面重新定义

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
  }, []);

  useEffect(() => {
    setInputValue(searchTerm);
  }, [searchTerm]);

  useEffect(() => {
    if (graphInstance && containerRef.current) {
      console.log('Collapsed state changed:', collapsed);

      // 使用 ResizeObserver 监听容器尺寸变化
      const resizeObserver = new ResizeObserver((entries) => {
        for (const entry of entries) {
          console.log('Container size changed:', entry.contentRect);
          graphInstance.resize();
        }
      });

      resizeObserver.observe(containerRef.current);

      // 备用方案：延迟调用 resize
      const timer = setTimeout(() => {
        console.log('Fallback resize triggered');
        graphInstance.resize();
      }, 50);

      return () => {
        resizeObserver.disconnect();
        clearTimeout(timer);
      };
    }
  }, [collapsed, graphInstance]);

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

      // 获取起始节点
      const sourceNode = graphInstance.getCellById(contextMenuNodeId);
      if (!sourceNode) return;

      // 获取当前鼠标位置
      const getCurrentMousePosition = (e: MouseEvent) => {
        return graphInstance.clientToLocal(e.clientX, e.clientY);
      };

      let tempEdge: Edge | null = null;

      // 监听键盘事件处理取消连线
      const onKeyDown = (e: KeyboardEvent) => {
        if (e.key === 'Escape' && tempEdge && isDrawingRef.current) {
          e.preventDefault();
          e.stopPropagation();

          // 取消连线
          document.removeEventListener('mousemove', onMouseMove);
          document.removeEventListener('mouseup', onMouseUp);
          document.removeEventListener('keydown', onKeyDown);

          if (tempEdge) {
            tempEdge.remove();
          }

          updateDrawingState(false);
          drawingEdgeRef.current = null;
          tempEdge = null;
        }
      };

      // 监听鼠标移动开始绘制
      const onMouseMove = (e: MouseEvent) => {
        if (!graphInstance) return;

        const currentPoint = getCurrentMousePosition(e);

        if (!tempEdge) {
          // 创建临时连线
          tempEdge = graphInstance.addEdge({
            source: { cell: contextMenuNodeId },
            target: currentPoint,
            ...getEdgeStyle(connectionType),
            data: { connectionType, isTemporary: true },
            zIndex: 1000,
          });
          drawingEdgeRef.current = tempEdge;
          updateDrawingState(true);
        } else {
          // 更新目标位置
          tempEdge.setTarget(currentPoint);
        }
      };

      // 监听鼠标释放完成连接
      const onMouseUp = (e: MouseEvent) => {
        if (!tempEdge || !isDrawingRef.current || !graphInstance) {
          return;
        }

        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
        document.removeEventListener('keydown', onKeyDown);
        updateDrawingState(false);

        // 将鼠标位置转换为画布坐标
        const localPoint = getCurrentMousePosition(e);

        // 查找目标节点
        let targetCell: any = null;
        let targetPort: string | null = null;

        graphInstance.getNodes().forEach((node) => {
          if (node.id === contextMenuNodeId) return; // 跳过起始节点

          const bbox = node.getBBox();

          // 检查是否在节点范围内
          if (
            localPoint.x >= bbox.x &&
            localPoint.x <= bbox.x + bbox.width &&
            localPoint.y >= bbox.y &&
            localPoint.y <= bbox.y + bbox.height
          ) {
            targetCell = node;

            // 计算图标区域的实际位置（基于节点样式中的图标定义）
            const iconX = bbox.x + 25; // 图标相对节点的 x 偏移
            const iconY = bbox.y + 5; // 图标相对节点的 y 偏移
            const iconWidth = 70; // 图标宽度
            const iconHeight = 50; // 图标高度

            // 检查是否点击在图标区域内
            if (
              localPoint.x >= iconX &&
              localPoint.x <= iconX + iconWidth &&
              localPoint.y >= iconY &&
              localPoint.y <= iconY + iconHeight
            ) {
              // 基于图标区域计算锚点位置
              const ports = ['top', 'bottom', 'left', 'right'];
              const portPositions = {
                top: { x: iconX + iconWidth / 2, y: iconY },
                bottom: { x: iconX + iconWidth / 2, y: iconY + iconHeight },
                left: { x: iconX, y: iconY + iconHeight / 2 },
                right: { x: iconX + iconWidth, y: iconY + iconHeight / 2 },
              };

              let minDistance = Infinity;
              let nearestPort = 'top';

              ports.forEach((port) => {
                const portPos =
                  portPositions[port as keyof typeof portPositions];
                const distance = Math.sqrt(
                  Math.pow(localPoint.x - portPos.x, 2) +
                    Math.pow(localPoint.y - portPos.y, 2)
                );

                // 如果距离小于锚点半径（6px），认为是点击在锚点上
                if (distance <= 6) {
                  targetPort = port;
                  return;
                }

                // 记录最近的锚点
                if (distance < minDistance) {
                  minDistance = distance;
                  nearestPort = port;
                }
              });

              // 如果没有直接点击锚点，则使用最近的锚点
              if (!targetPort) {
                targetPort = nearestPort;
              }
            } else {
              // 如果点击在节点范围内但不在图标区域内，不设置目标端口
              targetCell = null;
            }
          }
        });

        // 移除临时连线
        if (tempEdge) {
          tempEdge.remove();
        }

        // 如果找到目标节点，创建正式连线
        if (targetCell && targetCell.id !== contextMenuNodeId && targetPort) {
          // 为起始节点选择最佳端口
          const sourceNode = graphInstance.getCellById(contextMenuNodeId);
          if (sourceNode) {
            const sourceBbox = sourceNode.getBBox();
            const targetBbox = targetCell.getBBox();

            // 计算两个节点中心点的方向
            const dx =
              targetBbox.x +
              targetBbox.width / 2 -
              (sourceBbox.x + sourceBbox.width / 2);
            const dy =
              targetBbox.y +
              targetBbox.height / 2 -
              (sourceBbox.y + sourceBbox.height / 2);

            let sourcePort = 'right';
            // 根据方向选择起始端口
            if (Math.abs(dx) > Math.abs(dy)) {
              sourcePort = dx > 0 ? 'right' : 'left';
            } else {
              sourcePort = dy > 0 ? 'bottom' : 'top';
            }

            const finalEdge = graphInstance.addEdge({
              source: { cell: contextMenuNodeId, port: sourcePort },
              target: { cell: targetCell.id, port: targetPort },
              ...getEdgeStyle(connectionType),
              data: { connectionType, lineType: 'network line' },
            });
            addEdgeTools(finalEdge);

            // 连线完成后自动打开配置面板
            openEdgeConfig(finalEdge, sourceNode, targetCell);
          }
        }

        // 重置连线状态
        drawingEdgeRef.current = null;
        tempEdge = null;
      };

      document.addEventListener('mousemove', onMouseMove);
      document.addEventListener('mouseup', onMouseUp);
      document.addEventListener('keydown', onKeyDown);

      // 确保容器获得焦点以接收键盘事件
      if (containerRef.current) {
        containerRef.current.focus();
      }
    }
  };

  // 保存拓扑图
  const handleSave = useCallback(() => {
    // 这里可以添加具体的保存逻辑
    // 比如：保存节点位置、连线关系等到后端
    console.log('保存拓扑图...');

    // 保存完成后自动退出编辑模式
    setIsEditMode(false);

    // 禁用选择功能
    if (graphInstance) {
      graphInstance.disablePlugins(['selection']);

      // 取消当前的文本编辑
      if (isEditingText) {
        cancelTextEdit();
      }

      // 隐藏右键菜单
      setContextMenuVisible(false);

      // 清除选择
      graphInstance.cleanSelection();
      setSelectedCells([]);
    }
  }, [graphInstance, isEditingText, cancelTextEdit]);

  // 过滤树节点
  const filteredTreeData = useMemo(
    () => filterTree(mockGroups, searchTerm),
    [searchTerm]
  );

  return (
    <div className="flex-1 p-4 pb-0 overflow-auto flex flex-col ">
      <TopologyToolbar
        onEdit={toggleEditMode}
        onSave={handleSave}
        onZoomIn={zoomIn}
        onZoomOut={zoomOut}
        onFit={handleFit}
        onDelete={handleDelete}
        onSelectMode={handleSelectMode}
        onAddText={handleAddText}
        isSelectMode={isSelectMode}
        isEditMode={isEditMode}
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
          <div ref={containerRef} className="absolute inset-0" tabIndex={-1} />

          {/* 文本编辑输入框 - 放在画布容器内 */}
          {isEditingText && editingNodeId && (
            <div
              className="absolute z-50 bg-white border border-gray-300 rounded px-2 py-1 shadow-lg"
              style={{
                left: `${editPosition.x}px`,
                top: `${editPosition.y}px`,
                transform: 'translate(-50%, -50%)',
                minWidth: '120px',
              }}
            >
              <input
                type="text"
                value={tempTextInput}
                onChange={(e) => setTempTextInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    finishTextEdit();
                  } else if (e.key === 'Escape') {
                    cancelTextEdit();
                  }
                }}
                onBlur={finishTextEdit}
                onFocus={(e) => e.target.select()}
                autoFocus
                className="w-full outline-none text-sm"
                placeholder="输入文本内容"
              />
            </div>
          )}
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

      <EdgeConfigPanel
        visible={edgeConfigVisible}
        onClose={closeEdgeConfig}
        edgeData={currentEdgeData}
        onLineTypeChange={handleLineTypeChange}
        onLineNameChange={handleLineNameChange}
        onConfirm={handleEdgeConfigConfirm}
      />
    </div>
  );
};

export default Topology;

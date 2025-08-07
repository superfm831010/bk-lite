import { useCallback } from 'react';
import { message } from 'antd';
import type { Edge } from '@antv/x6';
import { getEdgeStyle, addEdgeTools } from '../utils/topologyUtils';

/**
 * 上下文菜单和模态框操作的自定义Hook
 * 负责处理右键菜单点击、连线配置、节点层级操作等功能
 */
export const useContextMenuAndModal = (
  containerRef: React.RefObject<HTMLDivElement>,
  state: any
) => {
  const {
    graphInstance,
    contextMenuNodeId,
    setContextMenuVisible,
    isEditMode,
    currentEdgeData,
    setCurrentEdgeData,
    isDrawingRef,
    drawingEdgeRef,
    updateDrawingState,
  } = state;

  // 统一处理连线配置确认
  const handleEdgeConfigConfirm = useCallback(
    (values: { lineType: string; lineName?: string }) => {
      if (currentEdgeData && graphInstance) {
        const edge = graphInstance.getCellById(currentEdgeData.id) as Edge;
        if (edge) {
          edge.setData({ ...edge.getData(), ...values });

          if (values.lineType === 'network line') {
            const labels = edge.getLabels();
            if (labels && labels.length > 0) {
              for (let i = labels.length - 1; i >= 0; i--) {
                edge.removeLabelAt(i);
              }
            }
          } else if (values.lineType === 'line') {
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

          setCurrentEdgeData({ ...currentEdgeData, ...values });
        }
      }
    },
    [currentEdgeData, graphInstance, setCurrentEdgeData]
  );

  // 关闭连线配置面板
  const closeEdgeConfig = useCallback(() => {
    state.setEdgeConfigVisible(false);
    setCurrentEdgeData(null);
  }, [setCurrentEdgeData, state]);

  /**
   * 处理视图模式下的菜单点击
   * @param key 菜单项的key
   * @param sourceNode 源节点
   */
  const handleViewModeMenuClick = useCallback(
    (key: string, sourceNode: any) => {
      const nodeName = sourceNode.getAttrs()?.label?.text || sourceNode.id;

      if (key === 'viewAlarms') {
        console.log('查看告警列表:', nodeName);
      } else if (key === 'viewMonitor') {
        console.log('查看监控详情:', nodeName);
      }
    },
    []
  );

  /**
   * 处理节点层级操作（置顶、上移、下移）
   * @param key 操作类型
   * @param targetNode 目标节点
   * @returns 是否处理了层级操作
   */
  const handleNodeLayerOperation = useCallback(
    (key: string, targetNode: any) => {
      if (key === 'bringToFront') {
        targetNode.toFront();
        message.success('节点已置顶');
        return true;
      } else if (key === 'bringForward') {
        const currentZIndex = targetNode.getZIndex() || 0;
        const maxZIndex = Math.max(
          ...graphInstance.getCells().map((cell: any) => cell.getZIndex() || 0)
        );

        if (currentZIndex < maxZIndex) {
          targetNode.setZIndex(currentZIndex + 1);
          message.success(`节点上移一层，当前层级: ${currentZIndex + 1}`);
        } else {
          message.info('节点已在最顶层');
        }
        return true;
      } else if (key === 'sendBackward') {
        const currentZIndex = targetNode.getZIndex() || 0;
        const minZIndex = Math.min(
          ...graphInstance.getCells().map((cell: any) => cell.getZIndex() || 0)
        );

        if (currentZIndex > minZIndex && currentZIndex > 0) {
          const newZIndex = Math.max(0, currentZIndex - 1);
          targetNode.setZIndex(newZIndex);
          message.success(`节点下移一层，当前层级: ${newZIndex}`);
        } else {
          message.info('节点已在最底层');
        }
        return true;
      }
      return false;
    },
    [graphInstance]
  );

  /**
   * 处理连线绘制功能
   * @param connectionType 连接类型（无箭头、单向、双向）
   */
  const handleConnectionDrawing = useCallback(
    (connectionType: 'none' | 'single' | 'double') => {
      const sourceNode = graphInstance.getCellById(contextMenuNodeId);
      if (!sourceNode) return;

      const getCurrentMousePosition = (e: MouseEvent) => {
        return graphInstance.clientToLocal(e.clientX, e.clientY);
      };

      let tempEdge: Edge | null = null;

      const onKeyDown = (e: KeyboardEvent) => {
        if (e.key === 'Escape' && tempEdge && isDrawingRef.current) {
          e.preventDefault();
          e.stopPropagation();

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

      const onMouseMove = (e: MouseEvent) => {
        if (!graphInstance) return;

        const currentPoint = getCurrentMousePosition(e);

        if (!tempEdge) {
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
          tempEdge.setTarget(currentPoint);
        }
      };

      const onMouseUp = (e: MouseEvent) => {
        if (!tempEdge || !isDrawingRef.current || !graphInstance) {
          return;
        }

        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
        document.removeEventListener('keydown', onKeyDown);
        updateDrawingState(false);

        const localPoint = getCurrentMousePosition(e);

        // 查找目标节点和端口的逻辑
        let targetCell: any = null;
        let targetPort: string | null = null;

        graphInstance.getNodes().forEach((node: any) => {
          if (node.id === contextMenuNodeId) return;

          const bbox = node.getBBox();

          if (
            localPoint.x >= bbox.x &&
            localPoint.x <= bbox.x + bbox.width &&
            localPoint.y >= bbox.y &&
            localPoint.y <= bbox.y + bbox.height
          ) {
            targetCell = node;

            // 基于图标区域计算端口位置（正方形分布）
            const iconX = bbox.x + 25;
            const iconY = bbox.y + 5;
            const iconWidth = 60;
            const iconHeight = 60;

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
              const portPos = portPositions[port as keyof typeof portPositions];
              const distance = Math.sqrt(
                Math.pow(localPoint.x - portPos.x, 2) +
                Math.pow(localPoint.y - portPos.y, 2)
              );

              if (distance <= 6) {
                targetPort = port;
                return;
              }

              if (distance < minDistance) {
                minDistance = distance;
                nearestPort = port;
              }
            });

            if (!targetPort) {
              targetPort = nearestPort;
            }
          }
        });

        if (tempEdge) {
          tempEdge.remove();
        }

        if (targetCell && targetCell.id !== contextMenuNodeId && targetPort) {
          const sourceNode = graphInstance.getCellById(contextMenuNodeId);
          if (sourceNode) {
            const sourceBbox = sourceNode.getBBox();
            const targetBbox = targetCell.getBBox();

            const dx = targetBbox.x + targetBbox.width / 2 - (sourceBbox.x + sourceBbox.width / 2);
            const dy = targetBbox.y + targetBbox.height / 2 - (sourceBbox.y + sourceBbox.height / 2);

            let sourcePort = 'right';
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

            // 打开配置面板
            const edgeData = {
              id: finalEdge.id,
              lineType: 'network line',
              lineName: '',
              sourceNode: {
                id: sourceNode.id,
                name: sourceNode.getLabel?.() || sourceNode.label || sourceNode.id,
              },
              targetNode: {
                id: targetCell.id,
                name: targetCell.getLabel?.() || targetCell.label || targetCell.id,
              },
            };
            setCurrentEdgeData(edgeData);
            state.setEdgeConfigVisible(true);
          }
        }

        drawingEdgeRef.current = null;
        tempEdge = null;
      };

      document.addEventListener('mousemove', onMouseMove);
      document.addEventListener('mouseup', onMouseUp);
      document.addEventListener('keydown', onKeyDown);

      if (containerRef.current) {
        containerRef.current.focus();
      }
    },
    [
      graphInstance,
      containerRef,
      contextMenuNodeId,
      isDrawingRef,
      drawingEdgeRef,
      updateDrawingState,
      setCurrentEdgeData,
      state,
    ]
  );

  /**
   * 处理右键菜单点击的主函数
   * 根据不同模式和操作类型分发到对应的处理函数
   */
  const handleMenuClick = useCallback(
    ({ key }: { key: string }) => {
      setContextMenuVisible(false);

      if (!graphInstance) return;

      // 视图模式下的菜单处理
      if (!isEditMode) {
        const sourceNode = graphInstance.getCellById(contextMenuNodeId);
        if (!sourceNode) return;

        handleViewModeMenuClick(key, sourceNode);
        return;
      }

      // 编辑模式下处理层级操作
      const targetNode = graphInstance.getCellById(contextMenuNodeId);
      if (!targetNode) return;

      // 尝试处理层级操作
      if (handleNodeLayerOperation(key, targetNode)) {
        return;
      }

      // 处理连线操作
      const connectionType = key as 'none' | 'single' | 'double';
      if (['none', 'single', 'double'].includes(connectionType)) {
        handleConnectionDrawing(connectionType);
      }
    },
    [
      graphInstance,
      contextMenuNodeId,
      setContextMenuVisible,
      isEditMode,
      handleViewModeMenuClick,
      handleNodeLayerOperation,
      handleConnectionDrawing,
    ]
  );

  return {
    handleEdgeConfigConfirm,
    closeEdgeConfig,
    handleMenuClick
  };
};

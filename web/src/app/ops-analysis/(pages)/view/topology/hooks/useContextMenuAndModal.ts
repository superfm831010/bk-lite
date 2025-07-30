import { useCallback } from 'react';
import type { Edge } from '@antv/x6';
import { getEdgeStyle, addEdgeTools } from '../utils/topologyUtils';

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

  // 处理线条类型变更
  const handleLineTypeChange = useCallback(
    (lineType: string) => {
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
            // 清除标签
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
          setCurrentEdgeData({ ...currentEdgeData, lineType });
        }
      }
    },
    [currentEdgeData, graphInstance, setCurrentEdgeData]
  );

  // 处理线条名称变更
  const handleLineNameChange = useCallback(
    (lineName: string) => {
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

          setCurrentEdgeData({ ...currentEdgeData, lineName });
        }
      }
    },
    [currentEdgeData, graphInstance, setCurrentEdgeData]
  );

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

  // 处理右键菜单点击
  const handleMenuClick = useCallback(
    ({ key }: { key: string }) => {
      setContextMenuVisible(false);

      if (!graphInstance) return;

      // 视图模式下的菜单处理
      if (!isEditMode) {
        const sourceNode = graphInstance.getCellById(contextMenuNodeId);
        if (!sourceNode) return;

        const nodeName = sourceNode.getAttrs()?.label?.text || sourceNode.id;

        if (key === 'viewAlarms') {
          console.log('查看告警列表:', nodeName);
        } else if (key === 'viewMonitor') {
          console.log('查看监控详情:', nodeName);
        }
        return;
      }

      // 编辑模式下的连线逻辑
      const connectionType = key as 'none' | 'single' | 'double';
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
            const iconX = bbox.x + 25;
            const iconY = bbox.y + 5;
            const iconWidth = 70;
            const iconHeight = 50;

            if (
              localPoint.x >= iconX &&
              localPoint.x <= iconX + iconWidth &&
              localPoint.y >= iconY &&
              localPoint.y <= iconY + iconHeight
            ) {
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
            } else {
              targetCell = null;
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
      setContextMenuVisible,
      isEditMode,
      isDrawingRef,
      drawingEdgeRef,
      updateDrawingState,
      setCurrentEdgeData,
      state,
    ]
  );

  return {
    handleLineTypeChange,
    handleLineNameChange,
    handleEdgeConfigConfirm,
    closeEdgeConfig,
    handleMenuClick
  };
};

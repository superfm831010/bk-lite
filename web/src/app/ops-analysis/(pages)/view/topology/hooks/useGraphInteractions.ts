/**
 * 拓扑图交互功能管理 Hook，专注于处理用户交互操作和模态框管理
 */
import { v4 as uuidv4 } from 'uuid';
import type { Edge, Node, Cell } from '@antv/x6';
import { useCallback } from 'react';
import { message } from 'antd';
import { getEdgeStyle, addEdgeTools, createEdgeLabel } from '../utils/topologyUtils';
import {
  TopologyState,
  MenuClickEvent,
  UseContextMenuAndModalReturn,
  Point,
  EdgeData
} from '@/app/ops-analysis/types/topology';

const getNodeName = (node: Cell): string => {
  const nodeData = (node as any).getData?.();
  if (nodeData?.name) return nodeData.name;

  const attrs = (node as any).getAttrs?.();
  if (attrs?.label?.text) return attrs.label.text;

  return node.id;
};

const removeAllEdgeLabels = (edge: Edge) => {
  const labels = edge.getLabels();
  if (labels?.length) {
    for (let i = labels.length - 1; i >= 0; i--) {
      edge.removeLabelAt(i);
    }
  }
};

export const useContextMenuAndModal = (
  containerRef: React.RefObject<HTMLDivElement>,
  state: TopologyState
): UseContextMenuAndModalReturn => {
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

  const handleEdgeConfigConfirm = useCallback(
    (values: { lineType: 'common_line' | 'network_line'; lineName?: string }) => {
      if (!currentEdgeData?.id || !graphInstance) return;

      const edge = graphInstance.getCellById(currentEdgeData.id) as Edge;
      if (!edge) return;

      edge.setData({ ...edge.getData(), ...values });

      if (values.lineType === 'network_line') {
        removeAllEdgeLabels(edge);
      } else if (values.lineType === 'common_line') {
        if (values.lineName?.trim()) {
          edge.setLabels([createEdgeLabel(values.lineName)]);
        } else {
          removeAllEdgeLabels(edge);
        }
      }

      setCurrentEdgeData({
        ...currentEdgeData,
        lineType: values.lineType,
        lineName: values.lineName
      });
    },
    [currentEdgeData, graphInstance, setCurrentEdgeData]
  );

  const closeEdgeConfig = useCallback(() => {
    state.setEdgeConfigVisible(false);
    setCurrentEdgeData(null);
  }, [setCurrentEdgeData, state]);

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

  const handleNodeLayerOperation = useCallback(
    (key: string, targetNode: Cell) => {
      if (!graphInstance) return false;

      const currentZIndex = targetNode.getZIndex() || 0;
      const cells = graphInstance.getCells();

      if (key === 'bringToFront') {
        targetNode.toFront();
        message.success('节点已置顶');
        return true;
      }

      if (key === 'bringForward') {
        const maxZIndex = Math.max(...cells.map(cell => cell.getZIndex() || 0));

        if (currentZIndex < maxZIndex) {
          targetNode.setZIndex(currentZIndex + 1);
          message.success(`节点上移一层，当前层级: ${currentZIndex + 1}`);
        } else {
          message.info('节点已在最顶层');
        }
        return true;
      }

      if (key === 'sendBackward') {
        const minZIndex = Math.min(...cells.map(cell => cell.getZIndex() || 0));

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

  const handleConnectionDrawing = useCallback(
    (connectionType: 'none' | 'single' | 'double') => {
      if (!graphInstance || !contextMenuNodeId) return;

      const sourceNode = graphInstance.getCellById(contextMenuNodeId);
      if (!sourceNode) return;

      const getCurrentMousePosition = (e: MouseEvent): Point => {
        if (!graphInstance) throw new Error('Graph instance is null');
        return graphInstance.clientToLocal(e.clientX, e.clientY);
      };

      let tempEdge: Edge | null = null;

      const cleanup = () => {
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
        document.removeEventListener('keydown', onKeyDown);

        tempEdge?.remove();
        updateDrawingState(false);
        drawingEdgeRef.current = null;
        tempEdge = null;
      };

      const onKeyDown = (e: KeyboardEvent) => {
        if (e.key === 'Escape' && tempEdge && isDrawingRef.current) {
          e.preventDefault();
          e.stopPropagation();
          cleanup();
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
        if (!tempEdge || !isDrawingRef.current || !graphInstance || !contextMenuNodeId) {
          return;
        }

        cleanup();

        const localPoint = getCurrentMousePosition(e);

        let targetCell: Node | null = null;
        for (const node of graphInstance.getNodes()) {
          if (node.id === contextMenuNodeId) continue;

          const bbox = node.getBBox();
          if (
            localPoint.x >= bbox.x &&
            localPoint.x <= bbox.x + bbox.width &&
            localPoint.y >= bbox.y &&
            localPoint.y <= bbox.y + bbox.height
          ) {
            targetCell = node;
            break;
          }
        }

        if (targetCell && targetCell.id !== contextMenuNodeId) {
          const sourceNode = graphInstance.getCellById(contextMenuNodeId);
          if (sourceNode) {
            const finalEdge = graphInstance.addEdge({
              id: `edge_${uuidv4()}`,
              source: { cell: contextMenuNodeId },
              target: { cell: targetCell.id },
              ...getEdgeStyle(connectionType),
              data: { connectionType, lineType: 'common_line' },
            });
            addEdgeTools(finalEdge);

            const edgeData: EdgeData = {
              id: finalEdge.id,
              lineType: 'common_line' as const,
              lineName: '',
              sourceNode: {
                id: sourceNode.id,
                name: getNodeName(sourceNode),
              },
              targetNode: {
                id: targetCell.id,
                name: getNodeName(targetCell),
              },
            };
            setCurrentEdgeData(edgeData);
            state.setEdgeConfigVisible(true);
          }
        }
      };

      document.addEventListener('mousemove', onMouseMove);
      document.addEventListener('mouseup', onMouseUp);
      document.addEventListener('keydown', onKeyDown);

      containerRef.current?.focus();
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

  const handleMenuClick = useCallback(
    ({ key }: MenuClickEvent) => {
      setContextMenuVisible(false);

      if (!graphInstance || !contextMenuNodeId) return;

      if (!isEditMode) {
        const sourceNode = graphInstance.getCellById(contextMenuNodeId);
        if (!sourceNode) return;

        handleViewModeMenuClick(key, sourceNode);
        return;
      }

      const targetNode = graphInstance.getCellById(contextMenuNodeId);
      if (!targetNode) return;

      if (handleNodeLayerOperation(key, targetNode)) {
        return;
      }

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
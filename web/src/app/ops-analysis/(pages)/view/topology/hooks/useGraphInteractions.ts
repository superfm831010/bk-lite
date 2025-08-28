/**
 * useGraphInteractions Hook 
 * 
 * 拓扑图交互功能管理 Hook，专注于处理用户交互操作和模态框管理
 * 
 * 主要功能：
 * 1. 右键菜单处理 - 处理节点右键菜单的点击事件和不同模式下的菜单操作
 * 2. 连线配置管理 - 管理连线的配置确认、类型设置和标签编辑
 * 3. 节点层级操作 - 处理节点的置顶、上移、下移等层级调整功能
 * 4. 手动连线绘制 - 支持用户手动绘制连线，包括拖拽连线和端口自动识别
 * 5. 视图模式交互 - 处理查看模式下的告警查看、监控详情等操作
 * 6. 键盘交互支持 - 支持 ESC 键取消连线绘制等键盘操作
 * 
 * 交互模式：
 * - 编辑模式：支持连线绘制、节点层级调整、连线配置等编辑功能
 * - 查看模式：支持告警查看、监控详情等只读操作
 * 
 * 连线功能：
 * - 三种连线类型：无箭头、单向箭头、双向箭头
 * - 智能端口识别：自动计算最近端口或精确端口匹配
 * - 实时预览：连线绘制过程中提供实时视觉反馈
 * - 键盘取消：支持 ESC 键中断连线绘制
 * 
 * 层级管理：
 * - 置顶操作：将节点移动到最顶层
 * - 上移下移：逐层调整节点显示优先级
 * - 智能提示：显示当前层级状态和操作结果
 * 
 * @param containerRef - 图形容器的 React ref，用于焦点管理和事件监听
 * @param state - 拓扑状态管理对象，包含图形实例和各种状态变量
 * @returns 交互操作相关的方法集合，包括菜单处理、连线配置等功能
 */

import { useCallback } from 'react';
import { message } from 'antd';
import { v4 as uuidv4 } from 'uuid';
import type { Edge, Node, Cell } from '@antv/x6';
import { getEdgeStyle, addEdgeTools, createEdgeLabel } from '../utils/topologyUtils';
import {
  TopologyState,
  MenuClickEvent,
  UseContextMenuAndModalReturn,
  Point,
  EdgeData
} from '@/app/ops-analysis/types/topology';

/**
 * 上下文菜单和模态框操作的自定义Hook
 * 负责处理右键菜单点击、连线配置、节点层级操作等功能
 */
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

  // 统一处理连线配置确认
  const handleEdgeConfigConfirm = useCallback(
    (values: { lineType: 'common_line' | 'network_line'; lineName?: string }) => {
      if (currentEdgeData?.id && graphInstance) {
        const edge = graphInstance.getCellById(currentEdgeData.id) as Edge;
        if (edge) {
          edge.setData({ ...edge.getData(), ...values });

          if (values.lineType === 'network_line') {
            const labels = edge.getLabels();
            if (labels && labels.length > 0) {
              for (let i = labels.length - 1; i >= 0; i--) {
                edge.removeLabelAt(i);
              }
            }
          } else if (values.lineType === 'common_line') {
            if (values.lineName && values.lineName.trim()) {
              edge.setLabels([createEdgeLabel(values.lineName)]);
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
            lineType: values.lineType,
            lineName: values.lineName
          });
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
    (key: string, targetNode: Cell) => {
      if (!graphInstance) return false;

      if (key === 'bringToFront') {
        targetNode.toFront();
        message.success('节点已置顶');
        return true;
      } else if (key === 'bringForward') {
        const currentZIndex = targetNode.getZIndex() || 0;
        const maxZIndex = Math.max(
          ...graphInstance.getCells().map((cell: Cell) => cell.getZIndex() || 0)
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
          ...graphInstance.getCells().map((cell: Cell) => cell.getZIndex() || 0)
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
      if (!graphInstance || !contextMenuNodeId) return;

      const sourceNode = graphInstance.getCellById(contextMenuNodeId);
      if (!sourceNode) return;

      const getCurrentMousePosition = (e: MouseEvent): Point => {
        if (!graphInstance) throw new Error('Graph instance is null');
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
        if (!tempEdge || !isDrawingRef.current || !graphInstance || !contextMenuNodeId) {
          return;
        }

        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
        document.removeEventListener('keydown', onKeyDown);
        updateDrawingState(false);

        const localPoint = getCurrentMousePosition(e);

        // 查找目标节点的逻辑
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

        if (tempEdge) {
          tempEdge.remove();
        }

        if (targetCell && targetCell.id !== contextMenuNodeId) {
          const sourceNode = graphInstance.getCellById(contextMenuNodeId);
          if (sourceNode && targetCell) {
            const finalEdge = graphInstance.addEdge({
              id: `edge_${uuidv4()}`,
              source: { cell: contextMenuNodeId },
              target: { cell: targetCell.id },
              ...getEdgeStyle(connectionType),
              data: { connectionType, lineType: 'common_line' },
            });
            addEdgeTools(finalEdge);

            // 获取节点名称的辅助函数
            const getNodeName = (node: Cell): string => {
              const nodeData = (node as any).getData?.();
              if (nodeData?.name) return nodeData.name;
              const attrs = (node as any).getAttrs?.();
              if (attrs?.label?.text) return attrs.label.text;
              return node.id;
            };

            // 打开配置面板
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
    ({ key }: MenuClickEvent) => {
      setContextMenuVisible(false);

      if (!graphInstance || !contextMenuNodeId) return;

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

import React, {
  useRef,
  useEffect,
  forwardRef,
  useImperativeHandle,
  useState,
  useCallback,
} from 'react';
import './topology.scss';
import { Spin } from 'antd';
import { useTopologyState } from './hooks/useTopologyState';
import { useGraphOperations } from './hooks/useGraphOperations';
import { useTextOperations } from './hooks/useTextOperations';
import { useContextMenuAndModal } from './hooks/useGraphInteractions';
import { DirItem } from '@/app/ops-analysis/types';
import { NodeType, DropPosition } from '@/app/ops-analysis/types/topology';
import TopologyToolbar from './components/toolbar';
import ContextMenu from './components/contextMenu';
import EdgeConfigPanel from './components/edgeConfPanel';
import NodeSidebar from './components/nodeSidebar';
import TextEditInput from './components/textEditInput';
import NodeConfPanel from './components/nodeConfPanel';
import ViewConfig from '../dashBoard/components/viewConfig';
import ViewSelector from '../dashBoard/components/viewSelector';
interface TopologyProps {
  selectedTopology?: DirItem | null;
}

export interface TopologyRef {
  hasUnsavedChanges: () => boolean;
}

const Topology = forwardRef<TopologyRef, TopologyProps>(
  ({ selectedTopology }, ref) => {
    const containerRef = useRef<HTMLDivElement>(null);
    const canvasContainerRef = useRef<HTMLDivElement>(null);
    const [addNodeVisible, setAddNodeVisible] = useState(false);
    const [selectedNodeType, setSelectedNodeType] = useState<NodeType | null>(
      null
    );
    const [dropPosition, setDropPosition] = useState<DropPosition | null>(null);
    const [viewSelectorVisible, setViewSelectorVisible] = useState(false);
    const [chartDropPosition, setChartDropPosition] = useState<{
      x: number;
      y: number;
    } | null>(null);
    const state = useTopologyState();

    const {
      zoomIn,
      zoomOut,
      handleFit,
      handleDelete,
      addNode,
      handleNodeUpdate,
      handleViewConfigConfirm,
      handleAddChartNode,
      handleSaveTopology,
      handleLoadTopology,
      resizeCanvas,
      loading,
    } = useGraphOperations(containerRef, state);

    const { handleAddText, finishTextEdit, cancelTextEdit } = useTextOperations(
      containerRef,
      state
    );

    const { handleEdgeConfigConfirm, closeEdgeConfig, handleMenuClick } =
      useContextMenuAndModal(containerRef, state);

    // 监听画布容器大小变化，自动调整画布大小
    const handleCanvasResize = useCallback(() => {
      if (resizeCanvas && canvasContainerRef.current) {
        // 稍微延迟以确保DOM已经更新
        setTimeout(() => {
          if (canvasContainerRef.current) {
            const rect = canvasContainerRef.current.getBoundingClientRect();
            resizeCanvas(rect.width, rect.height);
          }
        }, 100);
      }
    }, [resizeCanvas]);

    // 使用 ResizeObserver 监听容器大小变化
    useEffect(() => {
      if (!canvasContainerRef.current) return;

      const resizeObserver = new ResizeObserver(() => {
        // 防抖处理
        clearTimeout((window as any).topologyResizeTimeout);
        (window as any).topologyResizeTimeout = setTimeout(() => {
          handleCanvasResize();
        }, 150);
      });

      resizeObserver.observe(canvasContainerRef.current);

      return () => {
        resizeObserver.disconnect();
        clearTimeout((window as any).topologyResizeTimeout);
      };
    }, [handleCanvasResize]);

    // 监听侧边栏收起展开，重新调整画布大小
    useEffect(() => {
      handleCanvasResize();
    }, [state.collapsed, handleCanvasResize]);

    const handleShowNodeConfig = (
      nodeType: NodeType,
      position?: DropPosition
    ) => {
      setSelectedNodeType(nodeType);
      setDropPosition(position || { x: 300, y: 200 });
      setAddNodeVisible(true);
    };

    const handleShowChartSelector = (position?: DropPosition) => {
      setChartDropPosition(position || { x: 300, y: 200 });
      setViewSelectorVisible(true);
    };

    const handleChartSelectorConfirm = (layoutItem: any) => {
      if (chartDropPosition) {
        const chartNodeData = {
          widget: layoutItem.widget,
          name: layoutItem.title,
          type: 'chart',
          config: layoutItem.config,
          position: chartDropPosition,
          isNewNode: true,
        };

        state.setEditingNodeData(chartNodeData);
        state.setViewConfigVisible(true);
      }
      setViewSelectorVisible(false);
      setChartDropPosition(null);
    };

    const handleChartSelectorCancel = () => {
      setViewSelectorVisible(false);
      setChartDropPosition(null);
    };

    const handleTopologyViewConfigConfirm = async (values: any) => {
      if (state.editingNodeData) {
        // 检查是否是新节点
        if (state.editingNodeData.isNewNode && state.editingNodeData.position) {
          // 创建新的图表节点配置
          const chartNodeConfig = {
            name: values.name || state.editingNodeData.name,
            dataSource: values.dataSource,
            dataSourceParams: values.dataSourceParams || [],
            valueConfig: {
              chartType: values.chartType,
              dataSource: values.dataSource,
              dataSourceParams: values.dataSourceParams,
              name: values.name || state.editingNodeData.name,
            },
          };

          await handleAddChartNode(
            state.editingNodeData.widget,
            chartNodeConfig,
            state.editingNodeData.position
          );

          state.setEditingNodeData(null);
          state.setViewConfigVisible(false);
        } else {
          await handleViewConfigConfirm(values);
        }
      }
    };
    const handleNodeEditClose = () => {
      if (addNodeVisible) {
        setAddNodeVisible(false);
        setSelectedNodeType(null);
        setDropPosition(null);
      } else {
        state.setNodeEditVisible(false);
        state.setEditingNodeData(null);
      }
    };

    const handleNodeConfirm = async (values: any) => {
      if (addNodeVisible) {
        if (!selectedNodeType || !dropPosition) return;
        addNode(selectedNodeType.id, values, dropPosition);
      } else {
        await handleNodeUpdate(values);
      }
      handleNodeEditClose();
    };

    const getNodeInitialValues = () => {
      return addNodeVisible ? undefined : state.getEditNodeInitialValues();
    };

    const getNodeType = () => {
      return addNodeVisible
        ? (selectedNodeType?.id as 'single-value' | 'icon')
        : (state.editingNodeData?.type as 'single-value' | 'icon');
    };

    const getNodeTitle = () => {
      return state.isEditMode ? '编辑节点' : '查看节点';
    };

    const getNodeReadonly = () => {
      return addNodeVisible ? false : !state.isEditMode;
    };

    const handleSave = () => {
      if (selectedTopology) {
        handleSaveTopology(selectedTopology);
      }
    };

    const hasUnsavedChanges = () => {
      return state.isEditMode;
    };

    useImperativeHandle(ref, () => ({
      hasUnsavedChanges,
    }));

    useEffect(() => {
      if (selectedTopology?.data_id && state.graphInstance) {
        handleLoadTopology(selectedTopology.data_id);
      }
    }, [selectedTopology?.data_id, state.graphInstance]);

    useEffect(() => {
      state.resetAllStates();
    }, [selectedTopology?.data_id]);

    const handleSelectMode = () => {
      state.setIsSelectMode(!state.isSelectMode);
      if (state.graphInstance) {
        state.graphInstance.enableSelection();
      }
    };

    return (
      <div className="flex-1 p-4 pb-0 overflow-auto flex flex-col bg-[var(--color-bg-1)]">
        {/* 工具栏 */}
        <TopologyToolbar
          selectedTopology={selectedTopology}
          onEdit={state.toggleEditMode}
          onSave={handleSave}
          onZoomIn={zoomIn}
          onZoomOut={zoomOut}
          onFit={handleFit}
          onDelete={handleDelete}
          onSelectMode={handleSelectMode}
          onAddText={handleAddText}
          isSelectMode={state.isSelectMode}
          isEditMode={state.isEditMode}
        />

        <div className="flex-1 flex overflow-hidden">
          {/* 侧边栏 */}
          <NodeSidebar
            collapsed={state.collapsed}
            setCollapsed={state.setCollapsed}
            onShowNodeConfig={handleShowNodeConfig}
            onShowChartSelector={handleShowChartSelector}
            isEditMode={state.isEditMode}
          />

          {/* 画布容器 */}
          <div
            ref={canvasContainerRef}
            className="flex-1 bg-[var(--color-bg-1)] relative"
          >
            {loading && (
              <div
                className="absolute inset-0 flex items-center justify-center backdrop-blur-sm z-10"
                style={{
                  backgroundColor: 'var(--color-bg-1)',
                  opacity: 0.8,
                }}
              >
                <Spin size="large" />
              </div>
            )}
            <div
              ref={containerRef}
              className="absolute inset-0"
              tabIndex={-1}
            />
            <TextEditInput
              isEditingText={state.isEditingText}
              editPosition={state.editPosition}
              inputWidth={state.inputWidth}
              tempTextInput={state.tempTextInput}
              setTempTextInput={state.setTempTextInput}
              finishTextEdit={finishTextEdit}
              cancelTextEdit={cancelTextEdit}
            />
          </div>
        </div>

        <ContextMenu
          visible={state.contextMenuVisible}
          position={state.contextMenuPosition}
          onMenuClick={handleMenuClick}
          isEditMode={state.isEditMode}
        />

        <EdgeConfigPanel
          visible={state.edgeConfigVisible}
          readonly={!state.isEditMode}
          onClose={closeEdgeConfig}
          edgeData={state.currentEdgeData}
          onConfirm={handleEdgeConfigConfirm}
        />

        <NodeConfPanel
          visible={state.nodeEditVisible || addNodeVisible}
          title={getNodeTitle()}
          nodeType={getNodeType()}
          readonly={getNodeReadonly()}
          initialValues={getNodeInitialValues()}
          onClose={handleNodeEditClose}
          onConfirm={handleNodeConfirm}
          onCancel={handleNodeEditClose}
        />

        <ViewSelector
          visible={viewSelectorVisible}
          onOpenConfig={handleChartSelectorConfirm}
          onCancel={handleChartSelectorCancel}
        />

        <ViewConfig
          open={state.viewConfigVisible}
          item={state.editingNodeData}
          onClose={() => state.setViewConfigVisible(false)}
          onConfirm={handleTopologyViewConfigConfirm}
        />
      </div>
    );
  }
);

Topology.displayName = 'Topology';

export default Topology;

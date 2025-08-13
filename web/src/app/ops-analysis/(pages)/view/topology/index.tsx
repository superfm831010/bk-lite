import React, {
  useRef,
  useEffect,
  forwardRef,
  useImperativeHandle,
  useState,
} from 'react';
import { Spin } from 'antd';
import { useTopologyState } from './hooks/useTopologyState';
import { useGraphOperations } from './hooks/useGraphOperations';
import { useTextOperations } from './hooks/useTextOperations';
import { useContextMenuAndModal } from './hooks/useContextMenuAndModal';
import { DirItem } from '@/app/ops-analysis/types';
import { NodeType, DropPosition } from '@/app/ops-analysis/types/topology';
import TopologyToolbar from './components/toolbar';
import ContextMenu from './components/contextMenu';
import EdgeConfigPanel from './components/edgeConfPanel';
import Sidebar from './components/nodeSidebar';
import TextEditInput from './components/textEditInput';
import NodeConfPanel from './components/nodeConfPanel';

interface TopologyProps {
  selectedTopology?: DirItem | null;
}

export interface TopologyRef {
  hasUnsavedChanges: () => boolean;
}

const Topology = forwardRef<TopologyRef, TopologyProps>(
  ({ selectedTopology }, ref) => {
    const containerRef = useRef<HTMLDivElement>(null);
    const [addNodeVisible, setAddNodeVisible] = useState(false);
    const [selectedNodeType, setSelectedNodeType] = useState<NodeType | null>(
      null
    );
    const [dropPosition, setDropPosition] = useState<DropPosition | null>(null);

    const state = useTopologyState();

    const {
      zoomIn,
      zoomOut,
      handleFit,
      handleDelete,
      addNode,
      handleNodeUpdate,
      handleSaveTopology,
      handleLoadTopology,
      loading,
    } = useGraphOperations(containerRef, state);

    const { handleAddText, finishTextEdit, cancelTextEdit } = useTextOperations(
      containerRef,
      state
    );

    const { handleEdgeConfigConfirm, closeEdgeConfig, handleMenuClick } =
      useContextMenuAndModal(containerRef, state);

    // 处理显示节点配置
    const handleShowNodeConfig = (
      nodeType: NodeType,
      position?: DropPosition
    ) => {
      setSelectedNodeType(nodeType);
      setDropPosition(position || { x: 300, y: 200 });
      setAddNodeVisible(true);
    };

    // 处理新增节点确认
    const handleAddNodeConfirm = async (values: any) => {
      if (!selectedNodeType || !dropPosition) return;

      addNode(selectedNodeType.id, values, dropPosition);
      setAddNodeVisible(false);
      setSelectedNodeType(null);
      setDropPosition(null);
    };

    // 处理新增节点取消
    const handleAddNodeCancel = () => {
      setAddNodeVisible(false);
      setSelectedNodeType(null);
      setDropPosition(null);
    };

    // 处理节点编辑确认（包装器）
    const handleNodeEditConfirm = async (values: any) => {
      await handleNodeUpdate(values);
      state.handleNodeEditClose();
    };

    // 创建保存函数的包装器
    const handleSave = () => {
      handleSaveTopology(selectedTopology);
    };

    // 是否处于编辑模式
    const hasUnsavedChanges = () => {
      return state.isEditMode;
    };

    // 暴露方法给父组件
    useImperativeHandle(ref, () => ({
      hasUnsavedChanges,
    }));

    useEffect(() => {
      if (selectedTopology?.data_id && state.graphInstance) {
        handleLoadTopology(selectedTopology.data_id);
      }
    }, [selectedTopology?.data_id, state.graphInstance]);

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
          <Sidebar
            collapsed={state.collapsed}
            setCollapsed={state.setCollapsed}
            onShowNodeConfig={handleShowNodeConfig}
            isEditMode={state.isEditMode}
          />

          {/* 画布容器 */}
          <div className="flex-1 bg-[var(--color-bg-1)] relative">
            {loading && (
              <div className="h-full flex items-center justify-center">
                <Spin size="large" />
              </div>
            )}
            <div
              ref={containerRef}
              className="absolute inset-0"
              tabIndex={-1}
            />
            {/* 文本编辑输入框 */}
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

        {/* 右键菜单 */}
        <ContextMenu
          visible={state.contextMenuVisible}
          position={state.contextMenuPosition}
          onMenuClick={handleMenuClick}
          isEditMode={state.isEditMode}
        />

        {/* 边配置面板 */}
        <EdgeConfigPanel
          visible={state.edgeConfigVisible}
          readonly={!state.isEditMode}
          onClose={closeEdgeConfig}
          edgeData={state.currentEdgeData}
          onConfirm={handleEdgeConfigConfirm}
        />

        {/* 节点配置面板 - 统一处理编辑和新增 */}
        <NodeConfPanel
          visible={state.nodeEditVisible || addNodeVisible}
          title={state.isEditMode ? '编辑节点' : '查看节点'}
          nodeType={
            addNodeVisible
              ? (selectedNodeType?.id as 'single-value' | 'icon')
              : (state.editingNodeData?.type as 'single-value' | 'icon')
          }
          readonly={addNodeVisible ? false : !state.isEditMode}
          initialValues={
            addNodeVisible ? undefined : state.getEditNodeInitialValues()
          }
          onClose={
            addNodeVisible ? handleAddNodeCancel : state.handleNodeEditClose
          }
          onConfirm={
            addNodeVisible ? handleAddNodeConfirm : handleNodeEditConfirm
          }
          onCancel={
            addNodeVisible ? handleAddNodeCancel : state.handleNodeEditClose
          }
        />
      </div>
    );
  }
);

Topology.displayName = 'Topology';

export default Topology;

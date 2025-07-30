import React, { useRef, useState } from 'react';
import { Button, Drawer } from 'antd';
import { useTopologyState } from './hooks/useTopologyState';
import { useGraphOperations } from './hooks/useGraphOperations';
import { useTextOperations } from './hooks/useTextOperations';
import { useContextMenuAndModal } from './hooks/useContextMenuAndModal';
import { DirItem } from '@/app/ops-analysis/types';
import TopologyToolbar from './components/toolbar';
import ContextMenu from './components/contextMenu';
import EdgeConfigPanel from './components/edgeConfPanel';
import Sidebar from './components/sidebar';
import TextEditInput from './components/textEditInput';
import NodeConfPanel from './components/nodeConfPanel';

interface TopologyProps {
  selectedTopology?: DirItem | null;
}

const Topology: React.FC<TopologyProps> = ({ selectedTopology }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [nodeEditFormInstance, setNodeEditFormInstance] = useState<any>(null);

  const state = useTopologyState();

  const {
    zoomIn,
    zoomOut,
    handleFit,
    handleDelete,
    handleSave,
    addNode,
    handleNodeUpdate,
  } = useGraphOperations(containerRef, state);

  const { handleAddText, finishTextEdit, cancelTextEdit } = useTextOperations(
    containerRef,
    state
  );

  const {
    handleLineTypeChange,
    handleLineNameChange,
    handleEdgeConfigConfirm,
    closeEdgeConfig,
    handleMenuClick,
  } = useContextMenuAndModal(containerRef, state);

  const handleSelectMode = () => {
    state.setIsSelectMode(!state.isSelectMode);
    if (state.graphInstance) {
      state.graphInstance.enableSelection();
    }
  };

  return (
    <div className="flex-1 p-4 pb-0 overflow-auto flex flex-col">
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
          onAddNode={addNode}
          isEditMode={state.isEditMode}
        />

        {/* 画布容器 */}
        <div className="flex-1 bg-[var(--color-bg-1)] relative">
          <div ref={containerRef} className="absolute inset-0" tabIndex={-1} />

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
        onLineTypeChange={handleLineTypeChange}
        onLineNameChange={handleLineNameChange}
        onConfirm={handleEdgeConfigConfirm}
      />

      {/* 节点编辑面板 */}
      <Drawer
        title={state.isEditMode ? '编辑节点' : '查看节点'}
        placement="right"
        width={600}
        open={state.nodeEditVisible}
        onClose={state.handleNodeEditClose}
        footer={
          state.isEditMode ? (
            <div className="flex justify-end space-x-2">
              <Button
                type="primary"
                onClick={() => handleNodeUpdate(nodeEditFormInstance)}
              >
                确认
              </Button>
              <Button onClick={state.handleNodeEditClose}>取消</Button>
            </div>
          ) : (
            <div className="flex justify-end">
              <Button onClick={state.handleNodeEditClose}>关闭</Button>
            </div>
          )
        }
      >
        {state.editingNodeData && (
          <NodeConfPanel
            nodeType={state.editingNodeData.type as 'single-value' | 'icon'}
            onFormReady={setNodeEditFormInstance}
            readonly={!state.isEditMode}
            initialValues={state.getEditNodeInitialValues()}
          />
        )}
      </Drawer>
    </div>
  );
};

export default Topology;

import React, { useRef } from 'react';
import { useTopologyState } from './hooks/useTopologyState';
import { useGraphOperations } from './hooks/useGraphOperations';
import { useTextOperations } from './hooks/useTextOperations';
import { useContextMenuAndModal } from './hooks/useContextMenuAndModal';
import TopologyToolbar from './components/toolbar';
import ContextMenu from './components/contextMenu';
import EdgeConfigPanel from './components/edgeConfPanel';
import Sidebar from './components/sidebar';
import TextEditInput from './components/textEditInput';

const Topology: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);

  const state = useTopologyState();

  const { zoomIn, zoomOut, handleFit, handleDelete, handleSave } =
    useGraphOperations(containerRef, state);

  const { handleAddText, finishTextEdit, cancelTextEdit } = useTextOperations(
    containerRef,
    state
  );

  const {
    handleLineTypeChange,
    handleLineNameChange,
    handleEdgeConfigConfirm,
    closeEdgeConfig,
    onTreeSelect,
    onModalOk,
    onModalCancel,
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
          searchTerm={state.searchTerm}
          setSearchTerm={state.setSearchTerm}
          inputValue={state.inputValue}
          setInputValue={state.setInputValue}
          modalVisible={state.modalVisible}
          instanceOptions={state.instanceOptions}
          selectedRowKeys={state.selectedRowKeys}
          onTreeSelect={onTreeSelect}
          onModalOk={onModalOk}
          onModalCancel={onModalCancel}
          onSelect={state.setSelectedRowKeys}
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
        onClose={closeEdgeConfig}
        edgeData={state.currentEdgeData}
        onLineTypeChange={handleLineTypeChange}
        onLineNameChange={handleLineNameChange}
        onConfirm={handleEdgeConfigConfirm}
      />
    </div>
  );
};

export default Topology;

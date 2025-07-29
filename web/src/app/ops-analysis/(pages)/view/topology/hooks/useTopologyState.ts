import { useState, useRef, useCallback } from 'react';
import type { Graph, Edge } from '@antv/x6';

export interface EdgeData {
  id: string;
  lineType: string;
  lineName?: string;
  sourceNode: { id: string; name: string };
  targetNode: { id: string; name: string };
}

export const useTopologyState = () => {
  // 图形相关状态
  const [graphInstance, setGraphInstance] = useState<Graph | null>(null);
  const [scale, setScale] = useState(1);
  const [selectedCells, setSelectedCells] = useState<string[]>([]);
  const [isSelectMode, setIsSelectMode] = useState(true);
  const [isEditMode, setIsEditMode] = useState(false);
  const [collapsed, setCollapsed] = useState(false);

  // 模态框和实例相关状态
  const [modalVisible, setModalVisible] = useState(false);
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);
  const [instanceOptions, setInstanceOptions] = useState<
    Array<{ id: string; name: string }>
  >([]);

  // 右键菜单状态
  const [contextMenuNodeId, setContextMenuNodeId] = useState<string>('');
  const [contextMenuVisible, setContextMenuVisible] = useState(false);
  const [contextMenuPosition, setContextMenuPosition] = useState({
    x: 0,
    y: 0,
  });

  // 搜索相关状态
  const [searchTerm, setSearchTerm] = useState('');
  const [inputValue, setInputValue] = useState('');

  // 文本编辑相关状态
  const [isEditingText, setIsEditingText] = useState(false);
  const [editingNodeId, setEditingNodeId] = useState<string | null>(null);
  const [tempTextInput, setTempTextInput] = useState('');
  const [editPosition, setEditPosition] = useState({ x: 0, y: 0 });
  const [inputWidth, setInputWidth] = useState(120);
  const [originalText, setOriginalText] = useState('');

  // 边配置相关状态
  const [edgeConfigVisible, setEdgeConfigVisible] = useState(false);
  const [currentEdgeData, setCurrentEdgeData] = useState<EdgeData | null>(null);

  // Refs
  const isDrawingRef = useRef(false);
  const drawingEdgeRef = useRef<Edge | null>(null);
  const finishTextEditRef = useRef<(() => void) | null>(null);
  const startTextEditRef = useRef<((nodeId: string, currentText: string) => void) | null>(null);
  const isEditModeRef = useRef(isEditMode);

  // 更新绘制状态
  const updateDrawingState = useCallback((drawing: boolean) => {
    isDrawingRef.current = drawing;
  }, []);

  // 切换编辑模式
  const toggleEditMode = useCallback(() => {
    const newEditMode = !isEditMode;
    setIsEditMode(newEditMode);
    isEditModeRef.current = newEditMode;

    if (graphInstance) {
      if (newEditMode) {
        graphInstance.enablePlugins(['selection']);
      } else {
        graphInstance.disablePlugins(['selection']);

        if (isEditingText) {
          // 取消文本编辑
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
    }
  }, [isEditMode, graphInstance, isEditingText]);

  return {
    // 图形相关
    graphInstance,
    setGraphInstance,
    scale,
    setScale,
    selectedCells,
    setSelectedCells,
    isSelectMode,
    setIsSelectMode,
    isEditMode,
    setIsEditMode,
    collapsed,
    setCollapsed,
    toggleEditMode,

    // 模态框和实例
    modalVisible,
    setModalVisible,
    selectedRowKeys,
    setSelectedRowKeys,
    instanceOptions,
    setInstanceOptions,

    // 右键菜单
    contextMenuNodeId,
    setContextMenuNodeId,
    contextMenuVisible,
    setContextMenuVisible,
    contextMenuPosition,
    setContextMenuPosition,

    // 搜索
    searchTerm,
    setSearchTerm,
    inputValue,
    setInputValue,

    // 文本编辑
    isEditingText,
    setIsEditingText,
    editingNodeId,
    setEditingNodeId,
    tempTextInput,
    setTempTextInput,
    editPosition,
    setEditPosition,
    inputWidth,
    setInputWidth,
    originalText,
    setOriginalText,

    // 边配置
    edgeConfigVisible,
    setEdgeConfigVisible,
    currentEdgeData,
    setCurrentEdgeData,

    // Refs
    isDrawingRef,
    drawingEdgeRef,
    finishTextEditRef,
    startTextEditRef,
    isEditModeRef,
    updateDrawingState,
  };
};

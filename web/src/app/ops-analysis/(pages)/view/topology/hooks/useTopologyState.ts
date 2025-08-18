import { useState, useRef, useCallback } from 'react';
import type { Graph, Edge } from '@antv/x6';
import { FORM_DEFAULTS } from '../constants/nodeDefaults';
import { EdgeData } from '@/app/ops-analysis/types/topology';

export const useTopologyState = () => {
  // 图形相关状态
  const [graphInstance, setGraphInstance] = useState<Graph | null>(null);
  const [scale, setScale] = useState(1);
  const [selectedCells, setSelectedCells] = useState<string[]>([]);
  const [isSelectMode, setIsSelectMode] = useState(true);
  const [isEditMode, setIsEditMode] = useState(false);
  const [collapsed, setCollapsed] = useState(true);

  // 右键菜单状态
  const [contextMenuNodeId, setContextMenuNodeId] = useState<string>('');
  const [contextMenuVisible, setContextMenuVisible] = useState(false);
  const [contextMenuPosition, setContextMenuPosition] = useState({
    x: 0,
    y: 0,
  });

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

  // 节点编辑相关状态
  const [nodeEditVisible, setNodeEditVisible] = useState(false);
  const [editingNodeData, setEditingNodeData] = useState<any>(null);

  const [viewConfigVisible, setViewConfigVisible] = useState(false);

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

  // 获取编辑节点的初始值
  const getEditNodeInitialValues = useCallback(() => {
    if (!editingNodeData) return {};

    if (editingNodeData.type === 'single-value') {
      const config = editingNodeData.config || {};
      return {
        name: editingNodeData.name,
        dataSource: editingNodeData.dataSource,
        dataSourceParams: editingNodeData.dataSourceParams || {}, 
        selectedFields: editingNodeData.selectedFields || [], 
        fontSize: config.fontSize || FORM_DEFAULTS.SINGLE_VALUE.fontSize,
        textColor: config.textColor || FORM_DEFAULTS.SINGLE_VALUE.textColor,
        backgroundColor: config.backgroundColor || FORM_DEFAULTS.SINGLE_VALUE.backgroundColor,
        borderColor: config.borderColor || FORM_DEFAULTS.SINGLE_VALUE.borderColor
      };
    }

    return {
      name: editingNodeData.name,
      logoType: editingNodeData.logoType || 'default',
      logoIcon:
        editingNodeData.logoType === 'default'
          ? editingNodeData.logoIcon
          : 'cc-host',
      logoUrl:
        editingNodeData.logoType === 'custom'
          ? editingNodeData.logoUrl
          : undefined,
      width: editingNodeData.width || editingNodeData.config?.width || FORM_DEFAULTS.ICON_NODE.width,
      height: editingNodeData.height || editingNodeData.config?.height || FORM_DEFAULTS.ICON_NODE.height,
      dataSourceParams: editingNodeData.dataSourceParams || {}, 
      selectedFields: editingNodeData.selectedFields || [],
      backgroundColor: editingNodeData.config?.backgroundColor || FORM_DEFAULTS.ICON_NODE.backgroundColor,
      borderColor: editingNodeData.config?.borderColor || FORM_DEFAULTS.ICON_NODE.borderColor,
    };
  }, [editingNodeData]);

  // 关闭节点编辑面板
  const handleNodeEditClose = useCallback(() => {
    setNodeEditVisible(false);
    setEditingNodeData(null);
  }, []);

  // 重置所有状态
  const resetAllStates = useCallback(() => {
    // 重置编辑相关状态
    setIsEditMode(false);
    isEditModeRef.current = false;
    setIsSelectMode(true);

    // 重置选择状态
    setSelectedCells([]);

    // 重置右键菜单状态
    setContextMenuVisible(false);
    setContextMenuNodeId('');
    setContextMenuPosition({ x: 0, y: 0 });

    // 重置文本编辑状态
    setIsEditingText(false);
    setEditingNodeId(null);
    setTempTextInput('');
    setEditPosition({ x: 0, y: 0 });
    setInputWidth(120);
    setOriginalText('');

    // 重置边配置状态
    setEdgeConfigVisible(false);
    setCurrentEdgeData(null);

    // 重置节点编辑状态
    setNodeEditVisible(false);
    setEditingNodeData(null);
    setViewConfigVisible(false);

    // 重置绘制状态
    isDrawingRef.current = false;
    drawingEdgeRef.current = null;
    finishTextEditRef.current = null;
    startTextEditRef.current = null;

    // 清理图形选择状态
    if (graphInstance) {
      graphInstance.disablePlugins(['selection']);
      graphInstance.cleanSelection();
    }
  }, [graphInstance]);

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

    // 右键菜单
    contextMenuNodeId,
    setContextMenuNodeId,
    contextMenuVisible,
    setContextMenuVisible,
    contextMenuPosition,
    setContextMenuPosition,

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

    // 节点编辑
    nodeEditVisible,
    setNodeEditVisible,
    editingNodeData,
    setEditingNodeData,
    getEditNodeInitialValues,
    handleNodeEditClose,

    // viewConfig
    viewConfigVisible,
    setViewConfigVisible,

    // 重置状态
    resetAllStates,

    // Refs
    isDrawingRef,
    drawingEdgeRef,
    finishTextEditRef,
    startTextEditRef,
    isEditModeRef,
    updateDrawingState,
  };
};

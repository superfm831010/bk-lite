import { useCallback } from 'react';
import { createNodeByType } from '../utils/registerNode';

export const useTextOperations = (
  containerRef: React.RefObject<HTMLDivElement>,
  state: any
) => {
  const {
    graphInstance,
    isEditMode,
    isEditingText,
    editingNodeId,
    tempTextInput,
    originalText,
    setIsEditingText,
    setEditingNodeId,
    setTempTextInput,
    setEditPosition,
    setInputWidth,
    setOriginalText,
    startTextEditRef,
    finishTextEditRef,
  } = state;

  // 添加文本节点
  const handleAddText = useCallback(() => {
    if (!isEditMode || !graphInstance) return;

    const textNodeConfig = {
      id: `text_${Date.now()}`,
      type: 'text',
      x: 100 + Math.random() * 50,
      y: 100 + Math.random() * 50,
      name: '双击编辑文本',
    };

    const nodeData = createNodeByType(textNodeConfig);
    const textNode = graphInstance.addNode(nodeData);

    setTimeout(() => {
      startTextEditRef.current?.(textNode.id, '');
    }, 100);
  }, [isEditMode, graphInstance, startTextEditRef]);

  // 开始文本编辑
  const startTextEdit = useCallback(
    (nodeId: string, currentText: string) => {
      if (!isEditMode || !graphInstance || !containerRef.current) return;

      const node = graphInstance.getCellById(nodeId);
      if (node) {
        const bbox = node.getBBox();
        const translate = graphInstance.translate();
        const scale = graphInstance.scale();

        const nodeCenterX = bbox.x + bbox.width / 2;
        const nodeCenterY = bbox.y + bbox.height / 2;

        const screenX = (nodeCenterX + translate.tx) * scale.sx;
        const screenY = (nodeCenterY + translate.ty) * scale.sy;

        setEditPosition({ x: screenX, y: screenY });

        // 计算输入框宽度
        const textDisplayWidth = Math.max(currentText.length * 14 + 20, 100);
        const nodeWidth = bbox.width * scale.sx;
        const calculatedWidth = Math.max(textDisplayWidth, nodeWidth);
        setInputWidth(calculatedWidth);

        // 保存原始文本
        setOriginalText(currentText);

        // 隐藏节点的文本内容，避免与输入框重叠
        node.setAttrs({
          label: { text: '' },
        });
      }

      setIsEditingText(true);
      setEditingNodeId(nodeId);
      setTempTextInput(currentText);
    },
    [
      isEditMode,
      graphInstance,
      containerRef,
      setEditPosition,
      setInputWidth,
      setOriginalText,
      setIsEditingText,
      setEditingNodeId,
      setTempTextInput,
    ]
  );

  // 完成文本编辑
  const finishTextEdit = useCallback(() => {
    if (!graphInstance || !editingNodeId || !isEditingText) return;

    const node = graphInstance.getCellById(editingNodeId);
    if (node) {
      const finalText = tempTextInput.trim();
      const nodeData = node.getData() || {};

      if (finalText) {
        node.setAttrs({
          label: { text: finalText },
        });

        const textWidth = finalText.length * 14 + 20;
        const nodeWidth = Math.max(80, Math.min(300, textWidth));
        node.prop('size', { width: nodeWidth, height: 40 });
        node.setData({ ...nodeData, isPlaceholder: false });
      } else {
        if (nodeData.isPlaceholder) {
          node.setAttrs({
            label: { text: '双击编辑文本' },
          });
          node.prop('size', { width: 120, height: 40 });
        } else {
          node.setAttrs({
            label: { text: '文本' },
          });
          node.prop('size', { width: 80, height: 40 });
        }
      }
    }

    setIsEditingText(false);
    setEditingNodeId(null);
    setTempTextInput('');
    setEditPosition({ x: 0, y: 0 });
    setInputWidth(120);
    setOriginalText('');
  }, [
    graphInstance,
    editingNodeId,
    tempTextInput,
    isEditingText,
    setIsEditingText,
    setEditingNodeId,
    setTempTextInput,
    setEditPosition,
    setInputWidth,
    setOriginalText,
  ]);

  // 取消文本编辑
  const cancelTextEdit = useCallback(() => {
    // 恢复原始文本
    if (graphInstance && editingNodeId && originalText !== '') {
      const node = graphInstance.getCellById(editingNodeId);
      if (node) {
        node.setAttrs({
          label: { text: originalText },
        });
      }
    }

    setIsEditingText(false);
    setEditingNodeId(null);
    setTempTextInput('');
    setEditPosition({ x: 0, y: 0 });
    setInputWidth(120);
    setOriginalText('');
  }, [
    graphInstance,
    editingNodeId,
    originalText,
    setIsEditingText,
    setEditingNodeId,
    setTempTextInput,
    setEditPosition,
    setInputWidth,
    setOriginalText,
  ]);

  // 设置 refs
  startTextEditRef.current = startTextEdit;
  finishTextEditRef.current = finishTextEdit;

  return {
    handleAddText,
    startTextEdit,
    finishTextEdit,
    cancelTextEdit,
  };
};

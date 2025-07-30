import React, { useState, useEffect } from 'react';
import { Button, Drawer } from 'antd';
import {
  RightOutlined,
  LeftOutlined,
  NumberOutlined,
  AppstoreOutlined,
} from '@ant-design/icons';
import NodeConfPanel from './nodeConfPanel';

interface SidebarProps {
  collapsed: boolean;
  isEditMode?: boolean;
  setCollapsed: (collapsed: boolean) => void;
  onAddNode?: (nodeConfig: any) => void;
}

interface NodeType {
  id: string;
  name: string;
  icon: React.ReactNode;
  description: string;
}

interface DropPosition {
  x: number;
  y: number;
}

const Sidebar: React.FC<SidebarProps> = ({ 
  collapsed, 
  isEditMode = false,
  setCollapsed, 
  onAddNode, 
}) => {
  const [drawerVisible, setDrawerVisible] = useState(false);
  const [selectedNodeType, setSelectedNodeType] = useState<NodeType | null>(
    null
  );
  const [formInstance, setFormInstance] = useState<any>(null);
  const [dropPosition, setDropPosition] = useState<DropPosition | null>(null);

  const nodeTypes: NodeType[] = [
    {
      id: 'single-value',
      name: '单值',
      icon: <NumberOutlined className="text-blue-500" />,
      description: '添加单个数值显示节点',
    },
    {
      id: 'icon',
      name: '图标',
      icon: <AppstoreOutlined className="text-green-500" />,
      description: '添加图标类型节点',
    },
  ];

  const handleNodeTypeClick = (nodeType: NodeType) => {
    if (!isEditMode) {
      return; 
    }
    setDropPosition({ x: 300, y: 200 });
    setSelectedNodeType(nodeType);
    setDrawerVisible(true);
  };

  const handleDragStart = (e: React.DragEvent, nodeType: NodeType) => {
    if (!isEditMode) {
      e.preventDefault();
      return;
    }
    
    setSelectedNodeType(nodeType);
    e.dataTransfer.setData('application/json', JSON.stringify({
      type: 'node',
      nodeTypeId: nodeType.id,
      nodeTypeName: nodeType.name,
      nodeTypeDescription: nodeType.description
    }));
    
    e.dataTransfer.effectAllowed = 'copy';
    
    // 改进拖拽时的视觉反馈，避免影响原始元素
    if (e.dataTransfer.setDragImage) {
      const dragImage = e.currentTarget.cloneNode(true) as HTMLElement;
      dragImage.style.transform = 'rotate(5deg)';
      dragImage.style.opacity = '0.8';
      dragImage.style.position = 'absolute';
      dragImage.style.top = '-1000px';
      dragImage.style.left = '-1000px';
      dragImage.style.width = '150px';
      dragImage.style.pointerEvents = 'none';
      
      document.body.appendChild(dragImage);
      e.dataTransfer.setDragImage(dragImage, 75, 20);
      
      setTimeout(() => {
        if (document.body.contains(dragImage)) {
          document.body.removeChild(dragImage);
        }
      }, 0);
    }
  };

  const handleDragEnd = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrawerClose = () => {
    setDrawerVisible(false);
    setSelectedNodeType(null);
    setFormInstance(null);
    setDropPosition(null);
  };

  const handleConfirm = async () => {
    if (!formInstance) {
      return;
    }
    try {
      const values = await formInstance.validateFields();
      
      const nodeConfig = {
        id: `node_${Date.now()}`,
        type: selectedNodeType?.id,
        name: values.name,
        logo: values.logoType === 'default' ? values.logoIcon : values.logoUrl,
        logoType: values.logoType,
        dataSource: values.dataSource,
        config: values,
        // 使用拖拽落下的位置，或者默认位置
        x: dropPosition?.x || Math.random() * 200 + 200,
        y: dropPosition?.y || Math.random() * 150 + 150,
      };

      if (onAddNode) {
        onAddNode(nodeConfig);
      }

      handleDrawerClose();
    } catch (error) {
      console.error('表单验证失败:', error);
    }
  };

  const handleCancel = () => {
    handleDrawerClose();
  };

  const handleToggleCollapsed = () => {
    setCollapsed(!collapsed);
  };

  useEffect(() => {
    if (isEditMode) {
      setCollapsed(false);
    } else {
      setCollapsed(true);
    }
  }, [isEditMode, setCollapsed]);

  // 添加全局拖拽监听器
  useEffect(() => {
    const handleGlobalDrop = (e: DragEvent) => {
      e.preventDefault();
      
      try {
        const data = e.dataTransfer?.getData('application/json');
        if (data) {
          const dropData = JSON.parse(data);
          
          if (dropData.type === 'node' && dropData.nodeTypeId) {
            const nodeType = nodeTypes.find(nt => nt.id === dropData.nodeTypeId);
            
            if (nodeType) {
              // 尝试多个可能的画布元素选择器
              const canvasSelectors = [
                '.x6-graph-scroller',
                '.x6-graph',
                '[data-testid="graph-container"]',
                '.topology-canvas',
                '#topology-container'
              ];
              
              let canvasElement = null;
              for (const selector of canvasSelectors) {
                canvasElement = document.querySelector(selector);
                if (canvasElement) break;
              }
              
              if (canvasElement) {
                const rect = canvasElement.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                // 记录拖拽落下的位置
                setDropPosition({ x, y });
                setSelectedNodeType(nodeType);
                setDrawerVisible(true);
              } else {
                // 即使没找到画布元素，也要打开弹窗
                setDropPosition({ x: 300, y: 200 });
                setSelectedNodeType(nodeType);
                setDrawerVisible(true);
              }
            }
          }
        }
      } catch (error) {
        console.error('解析拖拽数据失败:', error);
      }
    };

    const handleGlobalDragOver = (e: DragEvent) => {
      e.preventDefault();
    };

    document.addEventListener('drop', handleGlobalDrop);
    document.addEventListener('dragover', handleGlobalDragOver);

    return () => {
      document.removeEventListener('drop', handleGlobalDrop);
      document.removeEventListener('dragover', handleGlobalDragOver);
    };
  }, [nodeTypes]);

  return (
    <>
      <div
        className={`h-full border-r border-[var(--color-border-1)] bg-[var(--color-fill-1)] transition-[width] duration-300 flex-shrink-0 relative ${
          collapsed ? 'w-0' : 'w-48'
        }`}
      >
        <Button
          type="text"
          icon={collapsed ? <RightOutlined /> : <LeftOutlined />}
          onClick={handleToggleCollapsed}
          className="absolute top-5 bg-[var(--color-bg-1)] rounded-full shadow-sm border border-[var(--color-border-1)] hover:border-blue-300 !p-0"
          style={{
            width: '24px',
            height: '24px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: 0,
            zIndex: 10,
            right: collapsed ? '-24px' : '-12px',
            borderRadius: collapsed ? '0 50% 50% 0' : '50%',
          }}
        />

        {!collapsed && (
          <div className="h-full p-4 opacity-100 transition-opacity duration-300">
            <div className="h-full overflow-auto">
              <div className="space-y-2">
                {nodeTypes.map((nodeType) => (
                  <div
                    key={nodeType.id}
                    className={`p-2 rounded-lg border transition-all duration-200 ${
                      isEditMode
                        ? 'border-[var(--color-border-2)] hover:border-blue-300 cursor-grab active:cursor-grabbing bg-[var(--color-bg-1)] hover:bg-[var(--color-fill-2)]'
                        : 'border-[var(--color-border-3)] cursor-not-allowed bg-[var(--color-fill-1)] opacity-50'
                    }`}
                    draggable={isEditMode}
                    onClick={() => handleNodeTypeClick(nodeType)}
                    onDragStart={(e) => handleDragStart(e, nodeType)}
                    onDragEnd={handleDragEnd}
                  >
                    <div className="flex items-center space-x-3">
                      <div>{nodeType.icon}</div>
                      <div className="flex-1 text-[var(--color-text-2)]">
                        {nodeType.name}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 节点配置面板 */}
      <Drawer
        title={
          selectedNodeType ? `${selectedNodeType.name}节点` : '节点配置'
        }
        placement="right"
        width={600}
        open={drawerVisible}
        onClose={handleDrawerClose}
        footer={
          <div className="flex justify-end space-x-2">
            <Button type="primary" onClick={handleConfirm}>
              确认
            </Button>
            <Button onClick={handleCancel}>
              取消
            </Button>
          </div>
        }
      >
        {selectedNodeType ? (
          <NodeConfPanel
            nodeType={selectedNodeType.id as 'single-value' | 'icon'}
            onFormReady={setFormInstance}
          />
        ) : (
          <div>请选择节点类型</div>
        )}
      </Drawer>
    </>
  );
};

export default Sidebar;

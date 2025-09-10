'use client';

import React, { useState } from 'react';
import { Form, Input, Select, Collapse, Alert } from 'antd';
import { CaretRightOutlined } from '@ant-design/icons';
import { useTranslation } from '@/utils/i18n';
import ChatflowEditor from '@/app/opspilot/components/chatflow/ChatflowEditor';
import Icon from '@/components/icon';

const { Option } = Select;
const { TextArea } = Input;
const { Panel } = Collapse;

const nodeCategories = [
  {
    key: 'triggers',
    labelKey: 'chatflow.triggers',
    items: [
      { type: 'timeTrigger', icon: 'a-icon-dingshichufa1x', labelKey: 'chatflow.timeTrigger' },
      { type: 'restfulApi', icon: 'RESTfulAPI', labelKey: 'chatflow.restfulApi' },
      { type: 'openaiApi', icon: 'icon-test2', labelKey: 'chatflow.openaiApi' },
    ]
  },
  {
    key: 'agents',
    labelKey: 'chatflow.agents',
    items: [
      { type: 'agents', icon: 'zhinengti', labelKey: 'chatflow.agents' }
    ]
  },
  {
    key: 'logic',
    labelKey: 'chatflow.logicNodes',
    items: [
      { type: 'ifCondition', icon: 'tiaojianfenzhi', labelKey: 'chatflow.ifCondition' }
    ]
  },
  {
    key: 'actions',
    labelKey: 'chatflow.actionNodes',
    items: [
      { type: 'httpRequest', icon: 'HTTP', labelKey: 'chatflow.httpRequest' },
      { type: 'promptAppend', icon: 'prompt_o', labelKey: 'chatflow.promptAppend' },
      { type: 'knowledgeAppend', icon: 'zhishiku2', labelKey: 'chatflow.knowledgeAppend' }
    ]
  }
];

// 节点库项目组件 - 增强版本
const NodeLibraryItem = ({ type, icon, label, onDragStart }: {
  type: string;
  icon: string;
  label: string;
  onDragStart: (event: React.DragEvent, nodeType: string) => void;
}) => {
  const handleDragStart = (event: React.DragEvent<HTMLDivElement>) => {
    console.log('开始拖拽节点:', type);
    event.dataTransfer.setData('application/reactflow', type);
    event.dataTransfer.effectAllowed = 'move';
    
    // 添加视觉反馈
    const target = event.currentTarget as HTMLDivElement;
    target.style.opacity = '0.5';
    
    // 调用父组件的处理函数
    onDragStart(event, type);
  };

  const handleDragEnd = (event: React.DragEvent<HTMLDivElement>) => {
    console.log('拖拽结束:', type);
    const target = event.currentTarget as HTMLDivElement;
    target.style.opacity = '1';
  };

  return (
    <div
      className="flex items-center p-2 text-[var(--color-text-2)] border border-gray-200 rounded cursor-grab hover:border-blue-400 hover:bg-blue-50 hover:text-[var(--color-primary)] transition-all duration-200 flex-1"
      draggable
      onDragStart={handleDragStart}
      onDragEnd={handleDragEnd}
    >
      <Icon type={icon} className="text-blue-500 mr-2 text-sm flex-shrink-0" />
      <span className="text-xs truncate">{label}</span>
    </div>
  );
};

interface ChatflowSettingsProps {
  form: any;
  groups: any[];
  onClear?: () => void;
  onSaveWorkflow?: (nodes: any[], edges: any[]) => void;
  workflowData?: { nodes: any[], edges: any[] };
}

const ChatflowSettings: React.FC<ChatflowSettingsProps> = ({ 
  form, 
  groups, 
  onClear, 
  onSaveWorkflow,
  workflowData 
}) => {
  const { t } = useTranslation();
  const [isInfoCollapsed, setIsInfoCollapsed] = useState(false);
  const [isNodesCollapsed, setIsNodesCollapsed] = useState(false);

  const onDragStart = (event: React.DragEvent, nodeType: string) => {
    event.dataTransfer.setData('application/reactflow', nodeType);
    event.dataTransfer.effectAllowed = 'move';
  };

  return (
    <div className="w-full flex h-full">
      {/* Left Panel - Information Column */}
      <div className={`transition-all duration-300 ease-in-out pr-4 border-r border-[var(--color-border-2)] overflow-y-auto h-[calc(100vh-200px)] ${
        isInfoCollapsed ? 'w-0 pr-0 opacity-0' : 'w-1/5'
      }`}>
        <div className="mb-6">
          <h2 className="font-semibold mb-2 text-sm text-[var(--color-text-1)]">{t('studio.information')}</h2>
          <div className="p-2">
            <Form form={form} labelCol={{ flex: '0 0 60px' }} wrapperCol={{ flex: '1' }}>
              <Form.Item
                label={t('studio.form.name')}
                name="name"
                rules={[{ required: true, message: `${t('common.inputMsg')}${t('studio.form.name')}` }]}
              >
                <Input />
              </Form.Item>
              <Form.Item
                label={t('studio.form.group')}
                name="group"
                rules={[{ required: true, message: `${t('common.inputMsg')}${t('studio.form.group')}` }]}
              >
                <Select mode="multiple">
                  {groups.map((group) => (
                    <Option key={group.id} value={group.id}>
                      {group.name}
                    </Option>
                  ))}
                </Select>
              </Form.Item>
              <Form.Item
                label={t('studio.form.introduction')}
                name="introduction"
                rules={[{ required: true, message: `${t('common.inputMsg')}${t('studio.form.introduction')}` }]}
              >
                <TextArea rows={4} />
              </Form.Item>
            </Form>
          </div>
        </div>
      </div>

      {/* Information Column Toggle Button */}
      <div className="relative">
        <button
          onClick={() => setIsInfoCollapsed(!isInfoCollapsed)}
          className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 z-10 w-6 h-6 border border-gray-300 rounded-full shadow-sm hover:bg-gray-50 flex items-center justify-center transition-colors"
          style={{ left: '0px' }}
        >
          <Icon 
            type={isInfoCollapsed ? 'icon-test1' : 'icon-test'} 
            className="text-gray-500 text-lg"
          />
        </button>
      </div>

      {/* Middle Panel - Node Library Column */}
      <div className={`transition-all duration-300 ease-in-out border-r border-[var(--color-border-2)] overflow-y-auto h-[calc(100vh-200px)] ${
        isNodesCollapsed ? 'w-0 pr-0 opacity-0' : 'w-1/5'
      }`}>
        <div className="mb-6">
          <h2 className="font-semibold mb-2 pl-2 text-sm text-[var(--color-text-1)]">{t('chatflow.nodes')}</h2>
          <div className="p-2">
            <Alert message={t('chatflow.messages.dragToCreate')} type="info" showIcon />
            
            <Collapse 
              size="small" 
              ghost
              defaultActiveKey={['triggers', 'agents', 'logic', 'actions']}
              expandIcon={({ isActive }) => <CaretRightOutlined rotate={isActive ? 90 : 0} />}
            >
              {nodeCategories.map((category) => (
                <Panel 
                  key={category.key}
                  header={
                    <div className="flex items-center">
                      <span className="text-xs mt-[3px]">{t(category.labelKey)}</span>
                    </div>
                  }
                >
                  <div className="grid grid-cols-2 gap-2">
                    {category.items.map((item) => (
                      <NodeLibraryItem
                        key={item.type}
                        type={item.type}
                        icon={item.icon}
                        label={t(item.labelKey)}
                        onDragStart={onDragStart}
                      />
                    ))}
                  </div>
                </Panel>
              ))}
            </Collapse>
          </div>
        </div>
      </div>

      {/* Node Library Column Toggle Button */}
      <div className="relative">
        <button
          onClick={() => setIsNodesCollapsed(!isNodesCollapsed)}
          className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 z-10 w-6 h-6 border border-gray-300 rounded-full shadow-sm hover:bg-gray-50 flex items-center justify-center transition-colors"
          style={{ left: '0px' }}
        >
          <Icon 
            type={isNodesCollapsed ? 'icon-test1' : 'icon-test'} 
            className="text-gray-500 text-lg"
          />
        </button>
      </div>

      {/* Right Panel - Chatflow Canvas */}
      <div className={`flex-1 pl-4 transition-all duration-300 ease-in-out ${
        isInfoCollapsed && isNodesCollapsed ? 'pl-8' : 
          (isInfoCollapsed || isNodesCollapsed) ? 'pl-6' : 'pl-4'
      }`}>
        <div className="flex items-center mb-2">
          <h2 className="font-semibold text-sm text-[var(--color-text-1)] mr-2">{t('chatflow.canvas')}</h2>
          {onClear && (
            <button
              onClick={onClear}
              className="text-gray-500 hover:text-red-500 transition-colors p-1 rounded hover:bg-red-50"
              title={t('chatflow.clear')}
            >
              <Icon type="shanchu" className="text-lg" />
            </button>
          )}
        </div>
        <div className="border rounded-md shadow-sm bg-white h-[calc(100vh-230px)]">
          <ChatflowEditor 
            onSave={onSaveWorkflow} 
            initialData={workflowData}
          />
        </div>
      </div>
    </div>
  );
};

export default ChatflowSettings;
'use client';

import React, { useState } from 'react';
import { Drawer, Form, Input, Select, InputNumber, Button, message, TimePicker, Upload, Radio } from 'antd';
import { DeleteOutlined, InboxOutlined, CopyOutlined } from '@ant-design/icons';
import { Node } from '@xyflow/react';
import type { UploadProps, UploadFile as AntdUploadFile } from 'antd';

// Extend UploadFile to include the 'content' property
interface UploadFile extends AntdUploadFile {
  content?: string;
}
import { useSkillApi } from '@/app/opspilot/api/skill';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import dayjs from 'dayjs';

const { Option } = Select;
const { TextArea } = Input;

// Node data type definition
interface ChatflowNodeData {
  label: string;
  type: string;
  config?: any;
}

// Extended Node type with specific data type
interface ChatflowNode extends Omit<Node, 'data'> {
  data: ChatflowNodeData;
}

interface NodeConfigDrawerProps {
  visible: boolean;
  node: ChatflowNode | null;
  nodes?: ChatflowNode[];
  onClose: () => void;
  onSave: (nodeId: string, config: any) => void;
  onDelete: (nodeId: string) => void;
}

const NodeConfigDrawer: React.FC<NodeConfigDrawerProps> = ({
  visible,
  node,
  nodes = [],
  onClose,
  onSave,
  onDelete
}) => {
  const [form] = Form.useForm();
  const [frequency, setFrequency] = useState('daily');
  const [paramRows, setParamRows] = useState<Array<{ key: string, value: string }>>([]);
  const [headerRows, setHeaderRows] = useState<Array<{ key: string, value: string }>>([]);
  const [uploadedFiles, setUploadedFiles] = useState<UploadFile[]>([]);
  const [skills, setSkills] = useState<any[]>([]);
  const [loadingSkills, setLoadingSkills] = useState(false);

  const { fetchSkill } = useSkillApi();
  const searchParams = useSearchParams();
  const botId = searchParams ? searchParams.get('id') : '1';

  // Load LLM model list
  const loadLlmModels = async () => {
    try {
      setLoadingSkills(true);
      const skills = await fetchSkill({is_template: 0});
      setSkills(skills || []);
    } catch (error) {
      console.error('获取智能体列表失败:', error);
      message.error('获取智能体列表失败');
    } finally {
      setLoadingSkills(false);
    }
  };

  // 复制API URL到剪贴板
  const copyApiUrl = async () => {
    const apiUrl = `http://bklite.canwya.net/api/v1/opspilot/bot_mgmt/execute_chat_flow/?bot_id=${botId || '1'}&node_id=${node?.id || 'abcdef'}`;
    
    try {
      await navigator.clipboard.writeText(apiUrl);
      message.success('API链接已复制到剪贴板');
    } catch {
      const textArea = document.createElement('textarea');
      textArea.value = apiUrl;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      message.success('API链接已复制到剪贴板');
    }
  };

  React.useEffect(() => {
    if (node && visible) {
      const config = node.data.config || {};
      
      // Force form reset to ensure latest node data
      form.resetFields();
      
      // Handle time field conversion to correct dayjs object
      const formValues: any = {
        name: node.data.label,
        ...config
      };

      // Time format handling for celery nodes
      if (node.data.type === 'celery' && config.time) {
        try {
          // String format (e.g., "14:30") to dayjs object
          if (typeof config.time === 'string') {
            const timeStr = config.time.includes(':') ? config.time : `${config.time}:00`;
            const today = new Date().toISOString().split('T')[0];
            formValues.time = dayjs(`${today} ${timeStr}`, 'YYYY-MM-DD HH:mm');
          } else if (config.time && typeof config.time === 'object' && config.time._isAMomentObject) {
            // Convert moment to dayjs
            formValues.time = dayjs(config.time.format('HH:mm'), 'HH:mm');
          } else if (config.time && typeof config.time === 'object' && config.time.$d) {
            // Already dayjs object
            formValues.time = config.time;
          } else {
            formValues.time = dayjs(config.time);
          }
        } catch (error) {
          console.warn('时间格式转换失败:', config.time, error);
          formValues.time = undefined;
        }
      }
      
      form.setFieldsValue(formValues);

      if (config.frequency) {
        setFrequency(config.frequency);
      } else {
        setFrequency('daily');
      }
      
      // Initialize params and headers based on node type
      const needsParamsAndHeaders = ['http', 'restful', 'openai'];
      
      if (needsParamsAndHeaders.includes(node.data.type)) {
        if ((config as any).params && Array.isArray((config as any).params) && (config as any).params.length > 0) {
          setParamRows([...(config as any).params]);
        } else {
          setParamRows([{ key: '', value: '' }]);
        }
        
        if ((config as any).headers && Array.isArray((config as any).headers) && (config as any).headers.length > 0) {
          setHeaderRows([...(config as any).headers]);
        } else {
          setHeaderRows([{ key: '', value: '' }]);
        }
      } else {
        if ((config as any).params && Array.isArray((config as any).params)) {
          setParamRows([...(config as any).params]);
        } else {
          setParamRows([]);
        }
        
        if ((config as any).headers && Array.isArray((config as any).headers)) {
          setHeaderRows([...(config as any).headers]);
        } else {
          setHeaderRows([]);
        }
      }

      // Initialize uploaded files for agents nodes
      if (node.data.type === 'agents') {
        if (config.uploadedFiles && Array.isArray(config.uploadedFiles)) {
          // Convert saved file data back to upload file format
          const convertedFiles = config.uploadedFiles.map((file: any, index: number) => ({
            uid: file.uid || `file-${index}`,
            name: file.name,
            status: 'done' as const,
            content: file.content,
            response: {
              fileId: file.uid || `file-${index}`,
              fileName: file.name,
              content: file.content
            }
          }));
          setUploadedFiles(convertedFiles);
        } else {
          setUploadedFiles([]);
        }
        loadLlmModels();
      } else {
        setUploadedFiles([]);
      }
    } else {
      // Reset all states when drawer closes
      form.resetFields();
      setParamRows([]);
      setHeaderRows([]);
      setFrequency('daily');
      setUploadedFiles([]);
    }
  }, [node, visible, form]);

  // Save configuration
  const handleSave = () => {
    if (!node) return;

    form.validateFields().then((values) => {
      const configData = {
        ...values,
        params: paramRows.filter(row => row.key && row.value),
        headers: headerRows.filter(row => row.key && row.value)
      };

      // Save uploaded files for agents nodes
      if (node.data.type === 'agents') {
        // Only save name and content from uploaded files
        configData.uploadedFiles = uploadedFiles.map(file => ({
          name: file.name,
          content: file.response?.content || file.content || ''
        }));
      }

      // Save time in HH:mm format for celery nodes
      if (node.data.type === 'celery' && configData.time) {
        try {
          if (configData.time && typeof configData.time === 'object' && configData.time.format) {
            configData.time = configData.time.format('HH:mm');
          }
        } catch (error) {
          console.warn('时间格式保存失败:', configData.time, error);
        }
      }

      onSave(node.id, configData);
      message.success('节点配置已保存');
    });
  };

  const handleDelete = () => {
    if (!node) return;
    onDelete(node.id);
    onClose();
  };

  const handleFrequencyChange = (value: string) => {
    setFrequency(value);
    form.setFieldsValue({
      time: undefined,
      weekday: undefined,
      day: undefined
    });
  };

  const addParamRow = () => {
    setParamRows([...paramRows, { key: '', value: '' }]);
  };

  const removeParamRow = (index: number) => {
    if (paramRows.length > 1) {
      setParamRows(paramRows.filter((_, i) => i !== index));
    }
  };

  const updateParamRow = (index: number, field: 'key' | 'value', value: string) => {
    const newRows = [...paramRows];
    newRows[index][field] = value;
    setParamRows(newRows);
  };

  const addHeaderRow = () => {
    setHeaderRows([...headerRows, { key: '', value: '' }]);
  };

  const removeHeaderRow = (index: number) => {
    if (headerRows.length > 1) {
      setHeaderRows(headerRows.filter((_, i) => i !== index));
    }
  };

  const updateHeaderRow = (index: number, field: 'key' | 'value', value: string) => {
    const newRows = [...headerRows];
    newRows[index][field] = value;
    setHeaderRows(newRows);
  };

  // File upload configuration
  const uploadProps: UploadProps = {
    name: 'file',
    multiple: true,
    accept: '.md',
    fileList: uploadedFiles,
    beforeUpload: (file) => {
      if (!file.name.toLowerCase().endsWith('.md')) {
        message.error('只支持上传 .md 格式的文件');
        return false;
      }
      
      const isLt10M = file.size / 1024 / 1024 < 10;
      if (!isLt10M) {
        message.error('文件大小不能超过 10MB');
        return false;
      }
      
      return true;
    },
    onChange: (info) => {
      setUploadedFiles([...info.fileList]);
    },
    onRemove: (file) => {
      const newFileList = uploadedFiles.filter(item => item.uid !== file.uid);
      setUploadedFiles(newFileList);
      message.success('文件删除成功');
    },
    customRequest: async ({ file, onSuccess, onError }) => {
      try {
        // Read file content
        const fileContent = await new Promise<string>((resolve, reject) => {
          const reader = new FileReader();
          reader.onload = (e) => resolve(e.target?.result as string);
          reader.onerror = reject;
          reader.readAsText(file as File);
        });

        // Generate UID for the file
        const fileUid = `file-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

        // Create file object with content
        const fileWithContent = {
          uid: fileUid,
          name: (file as File).name,
          content: fileContent,
          status: 'done' as const,
          response: {
            fileId: fileUid,
            fileName: (file as File).name,
            content: fileContent
          }
        };

        onSuccess && onSuccess(fileWithContent.response);
      } catch (error) {
        console.error('File read error:', error);
        onError && onError(new Error('读取文件内容失败'));
      }
    }
  };

  // Get trigger nodes list for condition branch configuration
  const getTriggerNodes = () => {
    const triggerTypes = ['celery', 'restful', 'openai'];
    
    // Safety checks
    if (!nodes) {
      console.warn('NodeConfigDrawer: nodes is null or undefined');
      return [];
    }
    
    if (!Array.isArray(nodes)) {
      console.warn('NodeConfigDrawer: nodes is not an array:', typeof nodes, nodes);
      return [];
    }
    
    try {
      return nodes.filter(n => {
        // Ensure node has correct data structure
        if (!n || !n.data || typeof n.data.type !== 'string') {
          console.warn('NodeConfigDrawer: Invalid node structure:', n);
          return false;
        }
        return triggerTypes.includes(n.data.type);
      });
    } catch (error) {
      console.error('NodeConfigDrawer: Error filtering trigger nodes:', error);
      return [];
    }
  };

  const renderConfigForm = () => {
    if (!node) return null;

    const nodeType = node.data.type;

    return (
      <>
        {/* Common node name configuration for all node types */}
        <Form.Item name="name" label="节点名称" rules={[{ required: true, message: '请输入节点名称' }]}>
          <Input placeholder="请输入节点名称" />
        </Form.Item>

        {/* Common input and output parameters for all node types */}
        <Form.Item name="inputParams" label="输入参数" rules={[{ required: true, message: '请输入输入参数' }]}>
          <Input placeholder="请输入输入参数" />
        </Form.Item>
        
        <Form.Item name="outputParams" label="输出参数" rules={[{ required: true, message: '请输入输出参数' }]}>
          <Input placeholder="请输入输出参数" />
        </Form.Item>

        {/* Render specific configuration based on node type */}
        {(() => {
          switch (nodeType) {
            case 'celery':
              return (
                <>
                  <Form.Item name="frequency" label="触发频率" rules={[{ required: true }]}>
                    <Select placeholder="选择触发频率" onChange={handleFrequencyChange}>
                      <Option value="daily">每日触发</Option>
                      <Option value="weekly">每周触发</Option>
                      <Option value="monthly">每月触发</Option>
                    </Select>
                  </Form.Item>

                  {frequency === 'daily' && (
                    <Form.Item name="time" label="触发时间" rules={[{ required: true }]}>
                      <TimePicker
                        format="HH:mm"
                        placeholder="选择时间"
                        className="w-full"
                      />
                    </Form.Item>
                  )}

                  {frequency === 'weekly' && (
                    <>
                      <Form.Item name="weekday" label="星期" rules={[{ required: true }]}>
                        <Select placeholder="选择星期">
                          <Option value={1}>星期一</Option>
                          <Option value={2}>星期二</Option>
                          <Option value={3}>星期三</Option>
                          <Option value={4}>星期四</Option>
                          <Option value={5}>星期五</Option>
                          <Option value={6}>星期六</Option>
                          <Option value={0}>星期日</Option>
                        </Select>
                      </Form.Item>
                      <Form.Item name="time" label="触发时间" rules={[{ required: true }]}>
                        <TimePicker
                          format="HH:mm"
                          placeholder="选择时间"
                          className="w-full"
                        />
                      </Form.Item>
                    </>
                  )}

                  {frequency === 'monthly' && (
                    <>
                      <Form.Item name="day" label="日期" rules={[{ required: true }]}>
                        <Select placeholder="选择日期">
                          {Array.from({ length: 31 }, (_, i) => (
                            <Option key={i + 1} value={i + 1}>{i + 1}日</Option>
                          ))}
                        </Select>
                      </Form.Item>
                      <Form.Item name="time" label="触发时间" rules={[{ required: true }]}>
                        <TimePicker
                          format="HH:mm"
                          placeholder="选择时间"
                          className="w-full"
                        />
                      </Form.Item>
                    </>
                  )}

                  <Form.Item name="message" label="触发输入语" rules={[{ required: true }]}>
                    <TextArea rows={3} placeholder="请输入初始message内容..." />
                  </Form.Item>
                </>
              );

            case 'http':
              return (
                <>
                  <Form.Item label="API" required>
                    <div className="flex gap-2">
                      <Form.Item name="method" noStyle rules={[{ required: true }]}>
                        <Select style={{ width: 100 }} placeholder="方法">
                          <Option value="GET">GET</Option>
                          <Option value="POST">POST</Option>
                          <Option value="PUT">PUT</Option>
                          <Option value="DELETE">DELETE</Option>
                        </Select>
                      </Form.Item>
                      <Form.Item name="url" noStyle rules={[{ required: true }]}>
                        <Input placeholder="输入URL" className="flex-1" />
                      </Form.Item>
                    </div>
                  </Form.Item>

                  <Form.Item label="请求参数">
                    <div className="space-y-2">
                      <div className="grid gap-2 text-sm text-gray-500 mb-1 grid-cols-[1fr_1fr_60px]">
                        <span>变量名</span>
                        <span>变量值</span>
                        <span>操作</span>
                      </div>
                      {paramRows.map((row, index) => (
                        <div key={index} className="grid gap-2 items-center grid-cols-[1fr_1fr_60px]">
                          <Input
                            placeholder="输入参数名"
                            value={row.key}
                            onChange={(e) => updateParamRow(index, 'key', e.target.value)}
                          />
                          <div className="flex items-center gap-1">
                            <span className="text-xs bg-[var(--color-fill-1)] px-1 rounded">str</span>
                            <Input
                              placeholder="输入或引用参数值"
                              value={row.value}
                              onChange={(e) => updateParamRow(index, 'value', e.target.value)}
                            />
                          </div>
                          <div className="flex gap-1">
                            <Button
                              type="text"
                              size="small"
                              icon="+"
                              onClick={addParamRow}
                            />
                            <Button
                              type="text"
                              size="small"
                              icon="-"
                              onClick={() => removeParamRow(index)}
                              disabled={paramRows.length === 1}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </Form.Item>

                  <Form.Item label="请求头">
                    <div className="space-y-2">
                      <div className="grid gap-2 text-sm text-gray-500 mb-1 grid-cols-[1fr_1fr_60px]">
                        <span>变量名</span>
                        <span>变量值</span>
                        <span>操作</span>
                      </div>
                      {headerRows.map((row, index) => (
                        <div key={index} className="grid gap-2 items-center grid-cols-[1fr_1fr_60px]">
                          <Input
                            placeholder="输入参数名"
                            value={row.key}
                            onChange={(e) => updateHeaderRow(index, 'key', e.target.value)}
                          />
                          <div className="flex items-center gap-1">
                            <span className="text-xs bg-[var(--color-fill-1)] px-1 rounded">str</span>
                            <Input
                              placeholder="输入或引用参数值"
                              value={row.value}
                              onChange={(e) => updateHeaderRow(index, 'value', e.target.value)}
                            />
                          </div>
                          <div className="flex gap-1">
                            <Button
                              type="text"
                              size="small"
                              icon="+"
                              onClick={addHeaderRow}
                            />
                            <Button
                              type="text"
                              size="small"
                              icon="-"
                              onClick={() => removeHeaderRow(index)}
                              disabled={headerRows.length === 1}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </Form.Item>

                  <Form.Item name="requestBody" label="请求体">
                    <Select defaultValue="JSON" className="w-full mb-2">
                      <Option value="JSON">JSON</Option>
                    </Select>
                    <TextArea rows={6} placeholder="请输入JSON格式的请求体" />
                  </Form.Item>

                  <Form.Item name="timeout" label="超时设置（秒）">
                    <InputNumber min={1} max={300} className="w-full" />
                  </Form.Item>

                  <Form.Item name="outputMode" label="输出模式">
                    <Radio.Group>
                      <Radio value="stream">流式（SSE）</Radio>
                      <Radio value="once">一次性返回</Radio>
                    </Radio.Group>
                  </Form.Item>
                </>
              );

            case 'agents':
              // Handle agent selection, save both name and ID
              const handleAgentChange = (agentId: string) => {
                const selectedAgent = skills.find(model => model.id === agentId);
                if (selectedAgent) {
                  form.setFieldsValue({
                    agent: agentId,
                    agentName: selectedAgent.name
                  });
                }
              };

              return (
                <>
                  <Form.Item name="agent" label="选择智能体" rules={[{ required: true }]}>
                    <Select 
                      placeholder="请选择智能体"
                      loading={loadingSkills}
                      disabled={loadingSkills}
                      showSearch
                      onChange={handleAgentChange}
                      filterOption={(input, option) =>
                        option?.label?.toString().toLowerCase().includes(input.toLowerCase()) ?? false
                      }
                    >
                      {skills.map((model) => (
                        <Option key={model.id} value={model.id} label={model.name}>
                          {model.name}
                        </Option>
                      ))}
                    </Select>
                  </Form.Item>
                  {/* Hidden field to save agent name */}
                  <Form.Item name="agentName" className="hidden">
                    <Input />
                  </Form.Item>

                  {/* Prompt 追加功能 */}
                  <Form.Item 
                    name="prompt" 
                    label="Prompt"
                    tooltip="在流程流转过程中，需要追加更多的指令，让智能体的执行更符合预期和使用场景">
                    <TextArea rows={4} placeholder="请输入Prompt内容..." />
                  </Form.Item>

                  {/* 知识追加功能 */}
                  <Form.Item 
                    label="上传知识"
                    tooltip="在流程流转过程中，需要追加更多知识，这些知识会作为智能体执行的前提条件进行输入">
                    <Upload.Dragger {...uploadProps}>
                      <p className="ant-upload-drag-icon">
                        <InboxOutlined />
                      </p>
                      <p className="ant-upload-text">点击或拖拽文件到此区域上传</p>
                      <p className="ant-upload-hint">支持单个或批量上传，仅支持 .md 格式文件</p>
                    </Upload.Dragger>
                  </Form.Item>
                </>
              );

            case 'restful':
              return (
                <>
                  <div className="p-4 bg-blue-50 border border-blue-200 rounded-md text-xs leading-5">
                    <p className="text-[var(--color-text-2)] mb-2">
                      对外提供REST接口，适合以外部系统/应用进行调用。当画布保存后，可点击节点查询对应的调用参数如下
                    </p>
                    <div className="mt-2 mb-2 relative">
                      <Input.TextArea
                        readOnly
                        value={`http://bklite.canwya.net/api/v1/opspilot/bot_mgmt/execute_chat_flow/?bot_id=${botId || '1'}&node_id=${node?.id || 'abcdef'}`}
                        autoSize={{ minRows: 2, maxRows: 4 }}
                        className="font-mono text-xs text-[var(--color-text-2)] bg-white pr-10 border-none"
                      />
                      <Button
                        type="text"
                        icon={<CopyOutlined />}
                        size="small"
                        onClick={copyApiUrl}
                        className="absolute top-2 right-2 z-10 text-[var(--color-text-3)] hover:text-[var(--color-primary)]"
                        title="复制链接"
                      />
                    </div>
                    <span className="text-[var(--color-text-2)]">更多详细介绍，可前往“接口文档”进行查看</span>
                    <Link href="/opspilot/studio/detail/api" target="_blank" className="text-blue-500 hover:underline">
                      查看接口文档 →
                    </Link>
                  </div>
                </>
              );

            case 'openai':
              return (
                <>
                  <div className="p-4 bg-blue-50 border border-blue-200 rounded-md text-xs leading-5">
                    <p className="text-[var(--color-text-2)] mb-2">
                      对外提供的接口，可通过OpenAI的方式进行流程调用，支持SSE流式设置。当画布保存后，可点击节点查看对应调用参数如下
                    </p>
                    <div className="mt-2 mb-2 relative">
                      <Input.TextArea
                        readOnly
                        value={`http://bklite.canwya.net/api/v1/opspilot/bot_mgmt/execute_chat_flow/?bot_id=${botId || '1'}&node_id=${node?.id || 'abcdef'}`}
                        autoSize={{ minRows: 2, maxRows: 4 }}
                        className="font-mono text-xs text-[var(--color-text-2)] bg-white pr-10 border-none"
                      />
                      <Button
                        type="text"
                        icon={<CopyOutlined />}
                        size="small"
                        onClick={copyApiUrl}
                        className="absolute top-2 right-2 z-10 text-[var(--color-text-3)] hover:text-[var(--color-primary)]"
                        title="复制链接"
                      />
                    </div>
                    <span className="text-[var(--color-text-2)]">更多详细介绍，可前往“接口文档”进行查看</span>
                    <Link href="/opspilot/studio/detail/api" target="_blank" className="text-blue-500 hover:underline">
                      查看接口文档 →
                    </Link>
                  </div>
                </>
              );

            case 'condition':
              const triggerNodes = getTriggerNodes();
              
              return (
                <>
                  <div className="mb-4">
                    <h4 className="text-sm font-medium mb-3">分支条件</h4>
                    <div className="grid grid-cols-3 gap-2">
                      <Form.Item name="conditionField" rules={[{ required: true }]}>
                        <Select placeholder="触发类型">
                          <Option value="triggerType">触发类型</Option>
                        </Select>
                      </Form.Item>
                      <Form.Item name="conditionOperator" rules={[{ required: true }]}>
                        <Select placeholder="条件">
                          <Option value="equals">等于</Option>
                          <Option value="notEquals">不等于</Option>
                        </Select>
                      </Form.Item>
                      <Form.Item name="conditionValue" rules={[{ required: true }]}>
                        <Select placeholder="选择值">
                          {triggerNodes.length === 0 ? (
                            <Option value="" disabled>暂无触发器节点</Option>
                          ) : (
                            triggerNodes.map((triggerNode) => (
                              <Option key={triggerNode.id} value={triggerNode.id}>
                                {triggerNode.data.label}
                              </Option>
                            ))
                          )}
                        </Select>
                      </Form.Item>
                    </div>
                    <div className="mt-4 p-3 bg-[var(--color-fill-1)] rounded-md">
                      <p className="text-xs text-gray-600 mb-2">连接说明：</p>
                      <div className="flex items-center gap-2 text-xs">
                        <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                        <span>右侧上方连接点：条件为 True 时的执行路径</span>
                      </div>
                      <div className="flex items-center gap-2 text-xs mt-1">
                        <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                        <span>右侧下方连接点：条件为 False 时的执行路径</span>
                      </div>
                    </div>
                  </div>
                </>
              );

            default:
              return null;
          }
        })()}
      </>
    );
  };

  return (
    <Drawer
      title={String(node?.data.label || '')}
      open={visible}
      onClose={onClose}
      width={480}
      placement="right"
      footer={
        <div className="flex justify-end gap-2">
          <Button
            danger
            icon={<DeleteOutlined />}
            onClick={handleDelete}
          >
            删除
          </Button>
          <Button onClick={onClose}>
            取消
          </Button>
          <Button type="primary" onClick={handleSave}>
            确认
          </Button>
        </div>
      }
    >
      <Form form={form} layout="vertical">
        {renderConfigForm()}
      </Form>
    </Drawer>
  );
};

export default NodeConfigDrawer;
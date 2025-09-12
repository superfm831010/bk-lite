'use client';

import React, { useState } from 'react';
import { Drawer, Form, Input, Select, InputNumber, Button, message, TimePicker, Upload, Radio } from 'antd';
import { DeleteOutlined, InboxOutlined } from '@ant-design/icons';
import { Node } from '@xyflow/react';
import type { UploadProps, UploadFile } from 'antd';
import { useSkillApi } from '@/app/opspilot/api/skill';

const { Option } = Select;
const { TextArea } = Input;

// 节点数据类型定义
interface ChatflowNodeData {
  label: string;
  type: string;
  config?: any;
}

// 扩展Node类型以包含具体的data类型
interface ChatflowNode extends Omit<Node, 'data'> {
  data: ChatflowNodeData;
}

interface NodeConfigDrawerProps {
  visible: boolean;
  node: ChatflowNode | null;
  nodes?: ChatflowNode[]; // 使用更具体的类型
  onClose: () => void;
  onSave: (nodeId: string, config: any) => void;
  onDelete: (nodeId: string) => void;
}

const NodeConfigDrawer: React.FC<NodeConfigDrawerProps> = ({
  visible,
  node,
  nodes = [], // 接收画布节点数据
  onClose,
  onSave,
  onDelete
}) => {
  const [form] = Form.useForm();
  const [frequency, setFrequency] = useState('daily');
  const [paramRows, setParamRows] = useState<Array<{ key: string, value: string }>>([]);
  const [headerRows, setHeaderRows] = useState<Array<{ key: string, value: string }>>([]);
  const [uploadedFiles, setUploadedFiles] = useState<UploadFile[]>([]);
  const [llmModels, setLlmModels] = useState<any[]>([]);
  const [loadingLlmModels, setLoadingLlmModels] = useState(false);

  const { fetchLlmModels } = useSkillApi();

  // 获取LLM模型列表
  const loadLlmModels = async () => {
    try {
      setLoadingLlmModels(true);
      const models = await fetchLlmModels();
      setLlmModels(models || []);
    } catch (error) {
      console.error('获取智能体列表失败:', error);
      message.error('获取智能体列表失败');
    } finally {
      setLoadingLlmModels(false);
    }
  };

  React.useEffect(() => {
    if (node && visible) {
      const config = node.data.config || {};
      
      // 强制重置表单，确保每次打开都是最新的节点数据
      form.resetFields();
      
      // 设置表单值，包括节点名称（来自node.data.label）和其他配置
      form.setFieldsValue({
        name: node.data.label, // 回显节点名称
        ...config
      });

      // 设置频率状态
      if ((config as any).frequency) {
        setFrequency((config as any).frequency);
      } else {
        setFrequency('daily'); // 重置为默认值
      }
      
      // 设置参数和请求头 - 根据节点类型决定是否显示和初始化
      const needsParamsAndHeaders = ['http', 'restful', 'openai'];
      
      if (needsParamsAndHeaders.includes(node.data.type)) {
        // 需要显示参数和请求头的节点类型
        if ((config as any).params && Array.isArray((config as any).params) && (config as any).params.length > 0) {
          setParamRows([...(config as any).params]); // 使用展开运算符确保是新数组
        } else {
          // 如果没有保存的参数，初始化一个空行供用户填写
          setParamRows([{ key: '', value: '' }]);
        }
        
        if ((config as any).headers && Array.isArray((config as any).headers) && (config as any).headers.length > 0) {
          setHeaderRows([...(config as any).headers]); // 使用展开运算符确保是新数组
        } else {
          // 如果没有保存的请求头，初始化一个空行供用户填写
          setHeaderRows([{ key: '', value: '' }]);
        }
      } else {
        // 其他节点类型不显示参数和请求头，但保留数据结构
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

      // 如果是智能体节点，加载LLM模型列表
      if (node.data.type === 'agents') {
        loadLlmModels();
      }
    } else {
      // 当抽屉关闭时，重置所有状态
      form.resetFields();
      setParamRows([]);
      setHeaderRows([]);
      setFrequency('daily');
    }
  }, [node, visible, form]);

  // 保存配置
  const handleSave = () => {
    if (!node) return;

    form.validateFields().then((values) => {
      const configData = {
        ...values,
        // 确保所有节点都有 params 和 headers 配置
        params: paramRows.filter(row => row.key && row.value),
        headers: headerRows.filter(row => row.key && row.value)
      };

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

  // 文件上传配置
  const uploadProps: UploadProps = {
    name: 'file',
    multiple: true,
    accept: '.md',
    fileList: uploadedFiles,
    beforeUpload: (file) => {
      // 检查文件类型
      if (!file.name.toLowerCase().endsWith('.md')) {
        message.error('只支持上传 .md 格式的文件');
        return false;
      }
      
      // 检查文件大小（例如限制为10MB）
      const isLt10M = file.size / 1024 / 1024 < 10;
      if (!isLt10M) {
        message.error('文件大小不能超过 10MB');
        return false;
      }
      
      return true;
    },
    onChange: (info) => {
      const { status } = info.file;
      
      if (status === 'uploading') {
        setUploadedFiles([...info.fileList]);
      } else if (status === 'done') {
        message.success(`${info.file.name} 文件上传成功`);
        setUploadedFiles([...info.fileList]);
      } else if (status === 'error') {
        message.error(`${info.file.name} 文件上传失败`);
        setUploadedFiles(info.fileList.filter(file => file.uid !== info.file.uid));
      }
    },
    onRemove: (file) => {
      const newFileList = uploadedFiles.filter(item => item.uid !== file.uid);
      setUploadedFiles(newFileList);
      message.success('文件删除成功');
    },
    customRequest: async ({ file, onSuccess, onError }) => {
      try {
        // 这里应该调用真实的上传API
        // const formData = new FormData();
        // formData.append('file', file);
        // const response = await fetch('/api/upload/knowledge', {
        //   method: 'POST',
        //   body: formData
        // });
        
        // 模拟上传过程
        setTimeout(() => {
          onSuccess && onSuccess({
            fileId: Date.now().toString(),
            fileName: (file as File).name,
            url: URL.createObjectURL(file as File)
          });
        }, 1000);
      } catch (error) {
        console.error('Upload error:', error);
        onError && onError(new Error('上传失败'));
      }
    }
  };

  // 获取触发器节点列表（用于条件分支配置）
  const getTriggerNodes = () => {
    const triggerTypes = ['celery', 'restful', 'openai'];
    return nodes.filter(n => triggerTypes.includes(n.data.type));
  };

  const renderConfigForm = () => {
    if (!node) return null;

    const nodeType = node.data.type;

    return (
      <>
        {/* 通用节点名称配置 - 所有节点类型都需要 */}
        <Form.Item name="name" label="节点名称" rules={[{ required: true, message: '请输入节点名称' }]}>
          <Input placeholder="请输入节点名称" />
        </Form.Item>

        {/* 根据节点类型渲染特定配置 */}
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
                        style={{ width: '100%' }}
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
                          style={{ width: '100%' }}
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
                          style={{ width: '100%' }}
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
                        <Input placeholder="输入URL" style={{ flex: 1 }} />
                      </Form.Item>
                    </div>
                  </Form.Item>

                  <Form.Item label="请求参数">
                    <div className="space-y-2">
                      <div className="grid gap-2 text-sm text-gray-500 mb-1" style={{ gridTemplateColumns: '1fr 1fr 60px' }}>
                        <span>变量名</span>
                        <span>变量值</span>
                        <span>操作</span>
                      </div>
                      {paramRows.map((row, index) => (
                        <div key={index} className="grid gap-2 items-center" style={{ gridTemplateColumns: '1fr 1fr 60px' }}>
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
                      <div className="grid gap-2 text-sm text-gray-500 mb-1" style={{ gridTemplateColumns: '1fr 1fr 60px' }}>
                        <span>变量名</span>
                        <span>变量值</span>
                        <span>操作</span>
                      </div>
                      {headerRows.map((row, index) => (
                        <div key={index} className="grid gap-2 items-center" style={{ gridTemplateColumns: '1fr 1fr 60px' }}>
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
                    <Select defaultValue="JSON" style={{ width: '100%', marginBottom: 8 }}>
                      <Option value="JSON">JSON</Option>
                    </Select>
                    <TextArea rows={6} placeholder="请输入JSON格式的请求体" />
                  </Form.Item>

                  <Form.Item name="timeout" label="超时设置（秒）">
                    <InputNumber min={1} max={300} style={{ width: '100%' }} />
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
              // 处理智能体选择，同时保存名称和ID
              const handleAgentChange = (agentId: string) => {
                const selectedAgent = llmModels.find(model => model.id === agentId);
                if (selectedAgent) {
                  // 同时设置agent和agentName字段
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
                      loading={loadingLlmModels}
                      showSearch
                      onChange={handleAgentChange}
                      filterOption={(input, option) =>
                        option?.label?.toString().toLowerCase().includes(input.toLowerCase()) ?? false
                      }
                    >
                      {llmModels.map((model) => (
                        <Option key={model.id} value={model.id} label={model.name}>
                          {model.name}
                        </Option>
                      ))}
                    </Select>
                  </Form.Item>
                  {/* 隐藏字段保存智能体名称 */}
                  <Form.Item name="agentName" style={{ display: 'none' }}>
                    <Input />
                  </Form.Item>
                </>
              );

            case 'restful':
              return (
                <>
                  <div className="p-4 bg-blue-50 border border-blue-200 rounded-md">
                    <p className="text-sm text-gray-600 mb-2">
                      对外提供REST接口，适合以外部系统/应用进行调用，可指定&ldquo;接口文档&rdquo;查看具体步骤和参数
                    </p>
                    <a href="#" className="text-blue-500 text-sm hover:underline">
                      查看接口文档 →
                    </a>
                  </div>
                </>
              );

            case 'openai':
              return (
                <>
                  <div className="p-4 bg-blue-50 border border-blue-200 rounded-md">
                    <p className="text-sm text-gray-600 mb-2">
                      对外提供的接口，可通过OpenAI的方式进行流程调用，支持SSE、流式设置完成后，可前往&ldquo;接口文档&rdquo;查看具体步骤和参数
                    </p>
                    <a href="#" className="text-blue-500 text-sm hover:underline">
                      查看接口文档 →
                    </a>
                  </div>
                </>
              );

            case 'prompt':
              return (
                <>
                  <div className="mb-4">
                    <p className="text-sm text-gray-600 mb-3">
                      在流程流转过程中，需要追加更多的指令，让智能体的执行更符合预期和使用场景
                    </p>
                  </div>
                  <Form.Item name="prompt" label="Prompt" rules={[{ required: true }]}>
                    <TextArea rows={6} placeholder="请输入Prompt内容..." />
                  </Form.Item>
                </>
              );

            case 'knowledge':
              return (
                <>
                  <div className="mb-4">
                    <p className="text-sm text-gray-600 mb-3">
                      在流程流转过程中，需要追加更多知识，这些知识会作为智能体执行的前提条件进行输入
                    </p>
                  </div>
                  <Form.Item label="上传知识">
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
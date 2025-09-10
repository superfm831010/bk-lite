'use client';

import React, { useState } from 'react';
import { Drawer, Form, Input, Select, InputNumber, Button, message, TimePicker, Upload, Radio } from 'antd';
import { DeleteOutlined, InboxOutlined } from '@ant-design/icons';
import { Node } from '@xyflow/react';
import type { UploadProps, UploadFile } from 'antd';

const { Option } = Select;
const { TextArea } = Input;

interface NodeConfigDrawerProps {
  visible: boolean;
  node: Node | null;
  onClose: () => void;
  onSave: (nodeId: string, config: any) => void;
  onDelete: (nodeId: string) => void;
}

const NodeConfigDrawer: React.FC<NodeConfigDrawerProps> = ({
  visible,
  node,
  onClose,
  onSave,
  onDelete
}) => {
  const [form] = Form.useForm();
  const [frequency, setFrequency] = useState('daily');
  const [paramRows, setParamRows] = useState<Array<{ key: string, value: string }>>([{ key: '', value: '' }]);
  const [headerRows, setHeaderRows] = useState<Array<{ key: string, value: string }>>([{ key: '', value: '' }]);
  const [uploadedFiles, setUploadedFiles] = useState<UploadFile[]>([]);

  React.useEffect(() => {
    if (node && visible) {
      const config = node.data.config || {};
      form.setFieldsValue(config);

      // 设置频率状态
      if ((config as any).frequency) {
        setFrequency((config as any).frequency);
      }
      
      // 设置参数和请求头
      if ((config as any).params) {
        setParamRows((config as any).params);
      }
      if ((config as any).headers) {
        setHeaderRows((config as any).headers);
      }
    }
  }, [node, visible, form]);

  const handleSave = () => {
    if (!node) return;

    form.validateFields().then((values) => {
      const configData = {
        ...values,
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

  const renderConfigForm = () => {
    if (!node) return null;

    const nodeType = node.data.type;

    switch (nodeType) {
      case 'timeTrigger':
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

      case 'httpRequest':
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
                      <span className="text-xs bg-gray-100 px-1 rounded">str</span>
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
                      <span className="text-xs bg-gray-100 px-1 rounded">str</span>
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
        return (
          <>
            <Form.Item name="agent" label="选择智能体" rules={[{ required: true }]}>
              <Select placeholder="请选择智能体">
                <Option value="ops-agent">运维助手</Option>
                <Option value="monitor-agent">监控助手</Option>
                <Option value="security-agent">安全助手</Option>
                <Option value="analysis-agent">分析助手</Option>
              </Select>
            </Form.Item>
          </>
        );

      case 'restfulApi':
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

      case 'openaiApi':
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

      case 'promptAppend':
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

      case 'knowledgeAppend':
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

      case 'ifCondition':
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
                    <Option value="timeTrigger">定时触发</Option>
                    <Option value="restfulApi">Restful API</Option>
                    <Option value="openaiApi">OpenAI API</Option>
                  </Select>
                </Form.Item>
              </div>
            </div>
          </>
        );

      default:
        return null;
    }
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
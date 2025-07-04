'use client';
import React, { useState, useEffect } from 'react';
import { Button, Empty, message, Alert } from 'antd';
import { SettingOutlined, ReloadOutlined } from '@ant-design/icons';
import PermissionWrapper from '@/components/permission';
import { useRouter } from 'next/navigation';
import KnowledgeGraphView from './knowledgeGraphView';

interface KnowledgeGraphPageProps {
  knowledgeBaseId: string | null;
}

const generateMockGraphData = () => {
  return {
    nodes: [
      { id: '1', label: '人工智能', type: 'concept' as const, category: 'technology' },
      { id: '2', label: '机器学习', type: 'concept' as const, category: 'technology' },
      { id: '3', label: '深度学习', type: 'concept' as const, category: 'technology' },
      { id: '4', label: 'OpenAI', type: 'entity' as const, category: 'organization' },
      { id: '5', label: 'GPT模型', type: 'entity' as const, category: 'model' },
      { id: '6', label: 'AI技术白皮书', type: 'document' as const, category: 'document' },
      { id: '7', label: '神经网络', type: 'concept' as const, category: 'technology' },
      { id: '8', label: 'Transformer', type: 'entity' as const, category: 'architecture' },
      { id: '9', label: '自然语言处理', type: 'concept' as const, category: 'field' },
      { id: '10', label: 'BERT', type: 'entity' as const, category: 'model' },
      { id: '11', label: '计算机视觉', type: 'concept' as const, category: 'field' },
      { id: '12', label: 'ResNet', type: 'entity' as const, category: 'model' },
      { id: '13', label: 'CNN', type: 'concept' as const, category: 'technology' },
      { id: '14', label: 'RNN', type: 'concept' as const, category: 'technology' },
      { id: '15', label: 'LSTM', type: 'entity' as const, category: 'model' }
    ],
    edges: [
      { id: 'e1', source: '2', target: '1', label: '属于', type: 'relation' as const, weight: 0.9 },
      { id: 'e2', source: '3', target: '2', label: '属于', type: 'relation' as const, weight: 0.8 },
      { id: 'e3', source: '5', target: '4', label: '开发者', type: 'relation' as const, weight: 0.7 },
      { id: 'e4', source: '5', target: '3', label: '基于', type: 'relation' as const, weight: 0.9 },
      { id: 'e5', source: '6', target: '1', label: '描述', type: 'reference' as const, weight: 0.6 },
      { id: 'e6', source: '7', target: '2', label: '实现方式', type: 'relation' as const, weight: 0.8 },
      { id: 'e7', source: '8', target: '7', label: '架构类型', type: 'relation' as const, weight: 0.7 },
      { id: 'e8', source: '5', target: '8', label: '使用', type: 'relation' as const, weight: 0.9 },
      { id: 'e9', source: '9', target: '1', label: '应用领域', type: 'relation' as const, weight: 0.8 },
      { id: 'e10', source: '10', target: '9', label: '用于', type: 'relation' as const, weight: 0.7 },
      { id: 'e11', source: '10', target: '8', label: '基于', type: 'relation' as const, weight: 0.8 },
      { id: 'e12', source: '11', target: '1', label: '应用领域', type: 'relation' as const, weight: 0.8 },
      { id: 'e13', source: '12', target: '11', label: '用于', type: 'relation' as const, weight: 0.7 },
      { id: 'e14', source: '13', target: '11', label: '技术基础', type: 'relation' as const, weight: 0.8 },
      { id: 'e15', source: '14', target: '9', label: '技术基础', type: 'relation' as const, weight: 0.8 },
      { id: 'e16', source: '15', target: '14', label: '改进版本', type: 'relation' as const, weight: 0.9 },
      { id: 'e17', source: '12', target: '13', label: '基于', type: 'relation' as const, weight: 0.9 }
    ]
  };
};

const KnowledgeGraphPage: React.FC<KnowledgeGraphPageProps> = ({ knowledgeBaseId }) => {
  const router = useRouter();
  
  const [hasGraph, setHasGraph] = useState(false);
  const [loading, setLoading] = useState(true);
  const [graphData, setGraphData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const initializeGraph = async () => {
    setLoading(true);
    setError(null);
    
    try {
      if (!knowledgeBaseId) {
        throw new Error('知识库ID不存在');
      }

      console.log('正在初始化知识图谱...');
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const mockData = generateMockGraphData();
      console.log('生成的图谱数据:', mockData);
      
      if (mockData.nodes.length === 0) {
        throw new Error('没有可用的图谱数据');
      }
      
      setGraphData(mockData);
      setHasGraph(true);
      console.log('知识图谱初始化成功');
      
    } catch (error: any) {
      console.error('Failed to initialize graph:', error);
      setError(error.message || '初始化知识图谱失败');
      setHasGraph(false);
      setGraphData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    console.log('KnowledgeGraphPage mounted, knowledgeBaseId:', knowledgeBaseId);
    
    if (knowledgeBaseId) {
      initializeGraph();
    } else {
      setLoading(false);
      setError('请选择一个知识库');
    }
  }, [knowledgeBaseId]);

  const handleSettingsClick = () => {
    router.push(`/opspilot/knowledge/detail/documents/knowledgeGraph/edit?id=${knowledgeBaseId}`);
  };

  const handleNodeClick = (node: any) => {
    console.log('Node clicked:', node);
    message.info(`点击了节点: ${node.label} (类型: ${node.type})`);
  };

  const handleEdgeClick = (edge: any) => {
    console.log('Edge clicked:', edge);
    message.info(`点击了关系: ${edge.label || '未知关系'} (${edge.source} → ${edge.target})`);
  };

  const handleRefresh = () => {
    initializeGraph();
  };

  if (!knowledgeBaseId) {
    return (
      <div className="knowledge-graph-container h-96 flex items-center justify-center">
        <Empty
          description="请先选择一个知识库"
          image={Empty.PRESENTED_IMAGE_SIMPLE}
        />
      </div>
    );
  }

  if (error && !loading) {
    return (
      <div className="knowledge-graph-container p-4">
        <Alert
          message="知识图谱加载失败"
          description={error}
          type="error"
          showIcon
          action={
            <Button size="small" onClick={handleRefresh}>
              重试
            </Button>
          }
        />
      </div>
    );
  }

  return (
    <div className="knowledge-graph-container" style={{ height: 'calc(100vh - 300px)', minHeight: '600px' }}>
      {hasGraph && graphData ? (
        <div className="graph-display h-full relative">
          {/* 右上角设置按钮 */}
          <div style={{ 
            position: 'absolute', 
            top: 16, 
            right: 16, 
            zIndex: 1000,
            display: 'flex',
            gap: '8px'
          }}>
            <Button
              icon={<ReloadOutlined />}
              onClick={handleRefresh}
              title="刷新图谱"
            />
            <Button
              type="primary"
              icon={<SettingOutlined />}
              onClick={handleSettingsClick}
            >
              设置
            </Button>
          </div>
          
          {/* 知识图谱可视化组件 */}
          <KnowledgeGraphView
            data={graphData}
            loading={loading}
            height={600}
            onNodeClick={handleNodeClick}
            onEdgeClick={handleEdgeClick}
          />
          
          {/* 左下角状态信息 */}
          <div style={{ 
            position: 'absolute', 
            bottom: 16, 
            left: 16, 
            background: 'rgba(255, 255, 255, 0.9)',
            padding: '8px 12px',
            borderRadius: '6px',
            fontSize: '12px',
            color: '#666',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)'
          }}>
            <div>节点: {graphData.nodes?.length || 0}</div>
            <div>关系: {graphData.edges?.length || 0}</div>
          </div>
        </div>
      ) : (
        <div className="flex items-center justify-center h-full">
          {loading ? (
            <div className="text-center">
              <div className="mb-4">
                <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
              </div>
              <div className="text-gray-600">正在加载知识图谱...</div>
            </div>
          ) : (
            <Empty
              description="暂无知识图谱数据"
              image={Empty.PRESENTED_IMAGE_SIMPLE}
            >
              <div className="flex gap-2">
                <Button onClick={handleRefresh}>
                  刷新
                </Button>
                <PermissionWrapper requiredPermissions={['Edit']}>
                  <Button type="primary" onClick={handleSettingsClick}>
                    创建图谱
                  </Button>
                </PermissionWrapper>
              </div>
            </Empty>
          )}
        </div>
      )}
    </div>
  );
};

export default KnowledgeGraphPage;
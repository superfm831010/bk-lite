'use client';
import React, { useEffect, useRef, useState } from 'react';
import { Spin } from 'antd';

export interface GraphNode {
  id: string;
  label: string;
  type: 'concept' | 'entity' | 'document';
  category?: string;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  label?: string;
  type: 'relation' | 'reference';
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

interface KnowledgeGraphViewProps {
  data: GraphData;
  loading?: boolean;
  height?: number;
  onNodeClick?: (node: GraphNode) => void;
  onEdgeClick?: (edge: GraphEdge) => void;
  useMockData?: boolean;
}

// Mock数据生成函数
const generateMockData = (): GraphData => {
  const nodes: GraphNode[] = [
    { id: '1', label: 'DevOps', type: 'concept', category: 'methodology' },
    { id: '2', label: 'CI/CD', type: 'concept', category: 'process' },
    { id: '3', label: 'Jenkins', type: 'entity', category: 'tool' },
    { id: '4', label: 'Docker', type: 'entity', category: 'tool' },
    { id: '5', label: 'Kubernetes', type: 'entity', category: 'platform' },
    { id: '6', label: '监控指南', type: 'document', category: 'documentation' },
    { id: '7', label: '部署流程', type: 'document', category: 'process' },
    { id: '8', label: '微服务', type: 'concept', category: 'architecture' },
    { id: '9', label: 'API网关', type: 'entity', category: 'component' },
    { id: '10', label: '日志系统', type: 'entity', category: 'monitoring' },
  ];

  const edges: GraphEdge[] = [
    { id: 'e1', source: '1', target: '2', label: '包含', type: 'relation' },
    { id: 'e2', source: '2', target: '3', label: '使用', type: 'relation' },
    { id: 'e3', source: '2', target: '4', label: '依赖', type: 'relation' },
    { id: 'e4', source: '4', target: '5', label: '部署到', type: 'relation' },
    { id: 'e5', source: '6', target: '5', label: '相关', type: 'reference' },
    { id: 'e6', source: '7', target: '2', label: '描述', type: 'reference' },
    { id: 'e7', source: '1', target: '8', label: '支持', type: 'relation' },
    { id: 'e8', source: '8', target: '9', label: '需要', type: 'relation' },
    { id: 'e9', source: '8', target: '10', label: '产生', type: 'relation' },
  ];

  return { nodes, edges };
};

const KnowledgeGraphView: React.FC<KnowledgeGraphViewProps> = ({
  data,
  loading = false,
  height = 500,
  onNodeClick,
  onEdgeClick,
  useMockData = false,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const graphRef = useRef<any>(null);
  const [initError, setInitError] = useState<string | null>(null);
  const [isInitializing, setIsInitializing] = useState(false);

  // 使用mock数据或传入的数据
  const graphData = useMockData || (!data.nodes.length && !loading) ? generateMockData() : data;

  const getNodeStyle = (type: string, label: string) => {
    const baseStyle = {
      size: 40,
      labelText: label,
      labelPosition: 'bottom' as const,
      lineWidth: 2,
    };

    switch (type) {
      case 'concept':
        return {
          ...baseStyle,
          fill: '#5B8FF9',
          stroke: '#3A7FE8',
        };
      case 'entity':
        return {
          ...baseStyle,
          fill: '#61DDAA',
          stroke: '#4CAF7A',
        };
      case 'document':
        return {
          ...baseStyle,
          fill: '#FFB84D',
          stroke: '#FF9900',
        };
      default:
        return {
          ...baseStyle,
          fill: '#C6E5FF',
          stroke: '#5B8FF9',
        };
    }
  };

  const getEdgeStyle = (type: string, label?: string) => {
    const baseStyle = {
      lineWidth: 2,
      labelText: label || '',
      labelFontSize: 10,
      stroke: '#e2e2e2', // 默认stroke颜色
    };

    switch (type) {
      case 'reference':
        return {
          ...baseStyle,
          stroke: '#999',
          lineDash: [4, 4],
        };
      default:
        return {
          ...baseStyle,
          lineDash: undefined, // 明确设置为undefined，保持类型一致
        };
    }
  };

  const createGraph = async () => {
    if (!containerRef.current || loading || !graphData.nodes.length || isInitializing || graphRef.current) {
      return;
    }

    setIsInitializing(true);
    setInitError(null);

    try {
      console.log('Starting graph initialization...');
      
      const container = containerRef.current;
      const width = container.offsetWidth || 800;

      // 动态导入 G6
      const G6Module = await import('@antv/g6');
      
      // G6 5.x 使用 Graph 类
      const Graph = G6Module.Graph || G6Module.default?.Graph || G6Module.default;
      
      if (!Graph) {
        throw new Error('G6 Graph constructor not found');
      }

      // 处理数据格式 - G6 5.x 格式
      const processedData = {
        nodes: graphData.nodes.map(node => {
          const style = getNodeStyle(node.type, node.label);
          return {
            id: node.id,
            data: {
              label: node.label,
              type: node.type,
              category: node.category,
            },
            style: {
              fill: style.fill,
              stroke: style.stroke,
              lineWidth: style.lineWidth,
              size: style.size,
              labelText: style.labelText,
              labelPosition: style.labelPosition,
            },
          };
        }),
        edges: graphData.edges.map(edge => {
          const style = getEdgeStyle(edge.type, edge.label);
          return {
            id: edge.id,
            source: edge.source,
            target: edge.target,
            data: {
              label: edge.label,
              type: edge.type,
            },
            style: {
              stroke: style.stroke,
              lineWidth: style.lineWidth,
              labelText: style.labelText,
              labelFontSize: style.labelFontSize,
              ...(style.lineDash && { lineDash: style.lineDash }),
            },
          };
        }),
      };

      // 创建图实例 - G6 5.x API
      const graph = new Graph({
        container: container,
        width,
        height,
        data: processedData,
        layout: {
          type: 'force',
          preventOverlap: true,
          nodeSize: 40,
          linkDistance: 150,
          nodeStrength: -100,
          edgeStrength: 0.8,
          gravity: 0.1,
        },
        behaviors: [
          'drag-canvas',
          'zoom-canvas',
          'drag-element',
          'click-select',
        ],
        autoFit: 'view',
      });

      // 绑定事件
      if (onNodeClick) {
        graph.on('node:click', (event: any) => {
          try {
            const nodeData = event.target?.model?.data || event.itemModel?.data;
            if (nodeData) {
              onNodeClick({
                id: event.target?.model?.id || event.itemId,
                label: nodeData.label,
                type: nodeData.type,
                category: nodeData.category,
              });
            }
          } catch (error) {
            console.warn('Error handling node click:', error);
          }
        });
      }

      if (onEdgeClick) {
        graph.on('edge:click', (event: any) => {
          try {
            const edgeData = event.target?.model?.data || event.itemModel?.data;
            if (edgeData) {
              onEdgeClick({
                id: event.target?.model?.id || event.itemId,
                source: event.target?.model?.source || '',
                target: event.target?.model?.target || '',
                label: edgeData.label,
                type: edgeData.type,
              });
            }
          } catch (error) {
            console.warn('Error handling edge click:', error);
          }
        });
      }

      // 渲染图
      await graph.render();
      
      graphRef.current = graph;
      
      console.log('Graph initialization completed successfully');

    } catch (error) {
      console.error('Failed to create G6 graph:', error);
      setInitError(error instanceof Error ? error.message : 'Unknown error occurred');
    } finally {
      setIsInitializing(false);
    }
  };

  useEffect(() => {
    // 只在没有图实例或数据变化时才重新创建
    if (!graphRef.current && !loading && graphData.nodes.length > 0) {
      const timer = setTimeout(() => {
        createGraph();
      }, 100);

      return () => clearTimeout(timer);
    }
  }, [useMockData]); // 只依赖useMockData，避免频繁重新创建

  // 组件卸载时清理图实例
  useEffect(() => {
    return () => {
      if (graphRef.current) {
        try {
          graphRef.current.destroy();
        } catch (e) {
          console.warn('Error destroying graph on cleanup:', e);
        }
        graphRef.current = null;
      }
    };
  }, []);

  // 处理窗口大小变化
  useEffect(() => {
    const handleResize = () => {
      if (graphRef.current && containerRef.current) {
        try {
          const newWidth = containerRef.current.offsetWidth;
          graphRef.current.setSize([newWidth, height]);
        } catch (error) {
          console.warn('Error handling resize:', error);
        }
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [height]);

  if (loading || isInitializing) {
    return (
      <div className="flex items-center justify-center" style={{ height }}>
        <Spin size="large" tip="加载知识图谱中..." />
      </div>
    );
  }

  if (initError) {
    return (
      <div className="flex flex-col items-center justify-center text-gray-500" style={{ height }}>
        <div className="text-red-500 mb-2">图谱初始化失败</div>
        <div className="text-sm">{initError}</div>
        <button 
          className="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          onClick={() => {
            setInitError(null);
            createGraph();
          }}
        >
          重试
        </button>
      </div>
    );
  }

  if (!graphData.nodes.length) {
    return (
      <div className="flex items-center justify-center text-gray-500" style={{ height }}>
        暂无知识图谱数据
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      className="w-full border border-gray-200 rounded bg-white"
      style={{ height, minHeight: height }}
    />
  );
};

export default KnowledgeGraphView;
/**
 * useGraphData Hook
 * 
 * 拓扑图数据管理核心 Hook，专注于数据持久化、序列化和加载功能
 * 
 * 主要功能：
 * 1. 数据序列化 - 将图形实例中的节点和边数据转换为可存储的JSON格式
 * 2. 数据持久化 - 保存拓扑图配置到后端服务，支持版本管理和云端同步
 * 3. 数据加载 - 从后端加载拓扑图配置并恢复到图形实例中
 * 4. 图表数据管理 - 处理图表节点的数据源配置和实时数据更新
 * 5. 节点样式重建 - 根据配置重新构建各类型节点的样式和属性
 * 6. 边线配置恢复 - 恢复连线的样式、标签和自定义属性
 * 
 * 数据流程：
 * - 序列化：图形实例 → JSON数据 → 后端存储
 * - 反序列化：后端数据 → JSON配置 → 图形实例重建
 * 
 * 支持的节点类型：
 * - icon: 图标节点，支持自定义图标、颜色、尺寸等配置
 * - single-value: 单值显示节点，支持数据源绑定和实时更新
 * - text: 文本节点，支持字体样式和颜色配置
 * - chart: 图表节点，支持多种图表类型和数据可视化
 * 
 * 支持的边线类型：
 * - common_line: 普通连线，支持标签和自定义样式
 * - network_line: 网络连线，专用于网络拓扑场景
 * 
 * @param graphInstance - X6图形实例，用于操作图形元素
 * @param updateSingleNodeData - 单值节点数据更新回调函数
 * @param startLoadingAnimation - 启动loading动画的回调函数
 * @param handleSaveCallback - 保存完成后的回调函数，用于状态同步
 * @returns 数据操作相关的方法集合和加载状态
 */

import { useCallback, useState } from 'react';
import type { Graph as X6Graph } from '@antv/x6';
import { message } from 'antd';
import { fetchWidgetData } from '@/app/ops-analysis/utils/widgetDataTransform';
import { useTopologyApi } from '@/app/ops-analysis/api/topology';
import { useDataSourceApi } from '@/app/ops-analysis/api/dataSource';
import { TopologyNodeData } from '@/app/ops-analysis/types/topology';
import { DirItem } from '@/app/ops-analysis/types';
import {
  getEdgeStyleWithLabel,
  getSingleValueNodeStyle,
  getIconNodeStyle,
  getChartNodeStyle,
  getTextNodeStyle,
  getLogoUrl,
} from '../utils/topologyUtils';
import { iconList } from '@/app/cmdb/utils/common';

/**
 * 图形数据操作相关的自定义Hook
 * 负责数据的加载、保存、序列化等操作
 */
export const useGraphData = (
  graphInstance: X6Graph | null,
  updateSingleNodeData: (nodeConfig: TopologyNodeData) => void,
  startLoadingAnimation: (node: any) => void,
  handleSaveCallback?: () => void
) => {
  const [loading, setLoading] = useState(false);
  const { saveTopology, getTopologyDetail } = useTopologyApi();
  const { getSourceDataByApiId } = useDataSourceApi();

  const serializeTopologyData = useCallback(() => {
    if (!graphInstance) return { nodes: [], edges: [] };

    const nodes = graphInstance.getNodes().map((node: any) => {
      const nodeData = node.getData();
      const position = node.getPosition();

      const serializedNode: TopologyNodeData = {
        id: node.id,
        x: position.x,
        y: position.y,
        type: nodeData.type,
        name: nodeData.name,
      };

      if (nodeData.dataSource) {
        serializedNode.dataSource = nodeData.dataSource;
      }

      if (nodeData.dataSourceParams) {
        serializedNode.dataSourceParams = nodeData.dataSourceParams;
      }

      if (nodeData.selectedFields) {
        serializedNode.selectedFields = nodeData.selectedFields;
      }

      if (nodeData.type === 'icon') {
        serializedNode.logoType = nodeData.logoType;
        serializedNode.logoIcon = nodeData.logoType === 'default' ? nodeData.logoIcon : undefined;
        serializedNode.logoUrl = nodeData.logoType === 'custom' ? nodeData.logoUrl : undefined;
        if (nodeData.config) {
          serializedNode.config = {
            backgroundColor: nodeData.config.backgroundColor,
            borderColor: nodeData.config.borderColor,
            textColor: nodeData.config.textColor,
            fontSize: nodeData.config.fontSize,
            width: nodeData.config.width,
            height: nodeData.config.height,
          };
        }
      } else if (nodeData.type === 'single-value') {
        if (nodeData.config) {
          serializedNode.config = {
            textColor: nodeData.config.textColor,
            fontSize: nodeData.config.fontSize,
            backgroundColor: nodeData.config.backgroundColor,
            borderColor: nodeData.config.borderColor,
          };
        }
      } else if (nodeData.type === 'text') {
        if (nodeData.config) {
          serializedNode.config = {
            fontSize: nodeData.config.fontSize,
            fontWeight: nodeData.config.fontWeight,
            textColor: nodeData.config.textColor,
          };
        }
      } else if (nodeData.type === 'chart') {
        serializedNode.widget = nodeData.widget;
        if (nodeData.valueConfig) {
          serializedNode.valueConfig = nodeData.valueConfig;
        }
        if (nodeData.config) {
          serializedNode.config = {
            width: nodeData.config.width,
            height: nodeData.config.height,
            ...nodeData.config,
          };
        }
      }

      return serializedNode;
    });

    const edges = graphInstance.getEdges().map((edge: any) => {
      const edgeData = edge.getData();
      const sourcePort = edge.getSourcePortId();
      const targetPort = edge.getTargetPortId();

      return {
        id: edge.id,
        source: edge.getSourceCellId(),
        target: edge.getTargetCellId(),
        sourcePort,
        targetPort,
        lineType: edgeData?.lineType || 'common_line',
        lineName: edgeData?.lineName || '',
        sourceInterface: edgeData?.sourceInterface,
        targetInterface: edgeData?.targetInterface,
        config: edgeData?.config
          ? {
            strokeColor: edgeData.config.strokeColor,
            strokeWidth: edgeData.config.strokeWidth,
          }
          : undefined,
      };
    });

    return { nodes, edges };
  }, [graphInstance]);

  const handleSaveTopology = useCallback(async (selectedTopology: DirItem) => {
    if (!selectedTopology?.data_id) {
      message.error('请先选择要保存的拓扑图');
      return;
    }

    setLoading(true);
    try {
      const topologyData = serializeTopologyData();
      const saveData = {
        name: selectedTopology.name,
        view_sets: {
          nodes: topologyData.nodes,
          edges: topologyData.edges,
        },
      };
      await saveTopology(selectedTopology.data_id, saveData);

      // 调用保存完成回调
      handleSaveCallback?.();

      message.success('拓扑图保存成功');
    } catch (error) {
      console.error('保存拓扑图失败:', error);
    } finally {
      setLoading(false);
    }
  }, [serializeTopologyData, saveTopology, handleSaveCallback]);

  const handleLoadTopology = useCallback(async (topologyId: string | number) => {
    if (!graphInstance) {
      return;
    }

    setLoading(true);
    try {
      const topologyData = await getTopologyDetail(topologyId);

      const viewSets = topologyData.view_sets || {};
      loadTopologyData(viewSets);
      // 适应画布
      graphInstance.zoomToFit({ padding: 20, maxScale: 1 });
    } catch (error) {
      console.error('加载拓扑图失败:', error);
    } finally {
      setLoading(false);
    }
  }, [graphInstance]);

  // 加载图表节点数据
  const loadChartNodeData = useCallback(async (nodeId: string, valueConfig: any) => {
    if (!graphInstance || !valueConfig.dataSource) {
      return;
    }

    const node = graphInstance.getCellById(nodeId);
    if (!node) {
      return;
    }

    try {
      const chartData = await fetchWidgetData({
        config: valueConfig,
        globalTimeRange: undefined,
        getSourceDataByApiId,
      });

      if (chartData) {
        const currentNodeData = node.getData();
        const updatedData = {
          ...currentNodeData,
          isLoading: false,
          rawData: chartData,
          hasError: false,
        };
        node.setData(updatedData);
      }
    } catch {
      const currentNodeData = node.getData();
      const updatedData = {
        ...currentNodeData,
        isLoading: false,
        hasError: true,
      };
      node.setData(updatedData);
    }
  }, [graphInstance, getSourceDataByApiId]);

  // 加载拓扑数据到画布
  const loadTopologyData = useCallback((data: { nodes: any[], edges: any[] }) => {
    if (!graphInstance) return;
    graphInstance.clearCells();

    const chartNodesToLoad: Array<{ nodeId: string; config: any }> = [];

    data.nodes.forEach((nodeConfig) => {
      let nodeData: any;

      if (nodeConfig.type === 'single-value') {
        nodeData = getSingleValueNodeStyle(nodeConfig);
      } else if (nodeConfig.type === 'text') {
        nodeData = getTextNodeStyle(nodeConfig);
      } else if (nodeConfig.type === 'chart') {
        const valueConfig = {
          ...nodeConfig,
          widget: nodeConfig.widget,
          isLoading: !!nodeConfig.dataSource,
          rawData: null,
          hasError: false,
        };
        nodeData = getChartNodeStyle(valueConfig);

        if (nodeConfig.dataSource) {
          chartNodesToLoad.push({
            nodeId: nodeConfig.id,
            config: valueConfig,
          });
        }
      } else {
        const logoUrl = getLogoUrl(nodeConfig, iconList);
        nodeData = getIconNodeStyle(nodeConfig, logoUrl);
      }

      graphInstance.addNode(nodeData);

      if (nodeConfig.type === 'single-value' && nodeConfig.dataSource && nodeConfig.selectedFields?.length) {
        const addedNode = graphInstance.getCellById(nodeConfig.id);
        if (addedNode) {
          startLoadingAnimation(addedNode);
          updateSingleNodeData(nodeConfig);
        }
      }
    });

    data.edges.forEach((edgeConfig) => {
      const edgeData: any = {
        lineType: edgeConfig.lineType as 'common_line' | 'network_line',
        lineName: edgeConfig.lineName,
        sourceInterface: edgeConfig.sourceInterface,
        targetInterface: edgeConfig.targetInterface,
        config: edgeConfig.config,
      };

      const edge = graphInstance.createEdge({
        id: edgeConfig.id,
        source: edgeConfig.source,
        target: edgeConfig.target,
        sourcePort: edgeConfig.sourcePort,
        targetPort: edgeConfig.targetPort,
        shape: 'edge',
        ...getEdgeStyleWithLabel(edgeData, 'single'),
        data: edgeData,
      });

      graphInstance.addEdge(edge);
    });

    chartNodesToLoad.forEach(({ nodeId, config }) => {
      loadChartNodeData(nodeId, config);
    });

  }, [graphInstance, updateSingleNodeData, loadChartNodeData, startLoadingAnimation]);

  return {
    loading,
    setLoading,
    serializeTopologyData,
    handleSaveTopology,
    handleLoadTopology,
    loadChartNodeData,
    loadTopologyData,
  };
};

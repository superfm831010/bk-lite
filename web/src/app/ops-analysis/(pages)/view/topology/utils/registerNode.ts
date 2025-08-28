/**
 * 拓扑图节点注册工厂
 * 根据当前项目的节点类型(icon, single-value, text, chart)注册对应的节点形状
 */

import ChartNode from '../components/chartNode';
import { Graph } from '@antv/x6';
import { register } from '@antv/x6-react-shape';
import { NODE_DEFAULTS } from '../constants/nodeDefaults';
import { createPortConfig } from './topologyUtils';

// 节点类型映射
const NODE_TYPE_MAP = {
  'icon': 'icon-node',
  'single-value': 'single-value-node',
  'text': 'text-node',
  'chart': 'chart-node'
} as const;

// 默认图标路径
const DEFAULT_ICON_PATH = '/app/assets/assetModelIcon/cc-default_默认.svg';

/**
 * 注册图标节点
 */
const registerIconNode = () => {
  const { ICON_NODE } = NODE_DEFAULTS;

  Graph.registerNode('icon-node', {
    inherit: 'rect',
    width: ICON_NODE.width,
    height: ICON_NODE.height,
    markup: [
      { tagName: 'rect', selector: 'body' },
      { tagName: 'image', selector: 'image' },
      { tagName: 'text', selector: 'label' }
    ],
    attrs: {
      body: {
        fill: ICON_NODE.backgroundColor,
        stroke: ICON_NODE.borderColor,
        strokeWidth: ICON_NODE.strokeWidth,
        rx: ICON_NODE.borderRadius,
        ry: ICON_NODE.borderRadius,
        magnet: true,
      },
      image: {
        refWidth: '70%',
        refHeight: '70%',
        refX: '50%',
        refY: '50%',
        refX2: '-36%',
        refY2: '-35%',
        'xlink:href': DEFAULT_ICON_PATH
      },
      label: {
        fill: ICON_NODE.textColor,
        fontSize: ICON_NODE.fontSize,
        fontWeight: ICON_NODE.fontWeight,
        textAnchor: 'middle',
        textVerticalAnchor: 'top',
        refX: '50%',
        refY: '100%',
        refY2: '20',
        textWrap: { width: '90%', ellipsis: true }
      }
    },
    ports: createPortConfig()
  });
};

/**
 * 注册单值节点
 */
const registerSingleValueNode = () => {
  const { SINGLE_VALUE_NODE } = NODE_DEFAULTS;

  Graph.registerNode('single-value-node', {
    inherit: 'rect',
    width: SINGLE_VALUE_NODE.width,
    height: SINGLE_VALUE_NODE.height,
    markup: [
      { tagName: 'rect', selector: 'body' },
      { tagName: 'text', selector: 'label' }
    ],
    attrs: {
      body: {
        fill: SINGLE_VALUE_NODE.backgroundColor,
        stroke: SINGLE_VALUE_NODE.borderColor,
        strokeWidth: SINGLE_VALUE_NODE.strokeWidth,
        rx: SINGLE_VALUE_NODE.borderRadius,
        ry: SINGLE_VALUE_NODE.borderRadius,
        magnet: true,
      },
      label: {
        fill: SINGLE_VALUE_NODE.textColor,
        fontSize: SINGLE_VALUE_NODE.fontSize,
        fontFamily: SINGLE_VALUE_NODE.fontFamily,
        textAnchor: 'middle',
        textVerticalAnchor: 'middle',
        refX: '50%',
        refY: '50%',
        textWrap: { width: '90%', ellipsis: true }
      }
    },
    ports: createPortConfig()
  });
};

/**
 * 注册文本节点
 */
const registerTextNode = () => {
  const { TEXT_NODE } = NODE_DEFAULTS;

  Graph.registerNode('text-node', {
    inherit: 'rect',
    width: TEXT_NODE.width,
    height: TEXT_NODE.height,
    markup: [
      { tagName: 'rect', selector: 'body' },
      { tagName: 'text', selector: 'label' }
    ],
    attrs: {
      body: {
        fill: TEXT_NODE.backgroundColor,
        stroke: TEXT_NODE.borderColor,
        strokeWidth: TEXT_NODE.strokeWidth
      },
      label: {
        fill: TEXT_NODE.textColor,
        fontSize: TEXT_NODE.fontSize,
        fontWeight: TEXT_NODE.fontWeight,
        textAnchor: 'start',
        textVerticalAnchor: 'top',
        refX: 0,
        refY: 0,
        textWrap: { width: '100%', height: '100%' }
      }
    },
    ports: { groups: {}, items: [] } // 文本节点不需要连接端口
  });
};

/**
 * 注册图表节点
 */
const registerChartNode = () => {
  const { CHART_NODE } = NODE_DEFAULTS;

  register({
    shape: 'chart-node',
    width: CHART_NODE.width,
    height: CHART_NODE.height,
    component: ChartNode,
    ports: createPortConfig()
  });
};

// 记录已注册的节点类型
const registeredNodes = new Set<string>();

/**
 * 注册所有节点类型
 */
export const registerNodes = () => {
  try {
    // 检查是否已经注册过，避免重复注册
    if (!registeredNodes.has('icon-node')) {
      registerIconNode();
      registeredNodes.add('icon-node');
    }

    if (!registeredNodes.has('single-value-node')) {
      registerSingleValueNode();
      registeredNodes.add('single-value-node');
    }

    if (!registeredNodes.has('text-node')) {
      registerTextNode();
      registeredNodes.add('text-node');
    }

    if (!registeredNodes.has('chart-node')) {
      registerChartNode();
      registeredNodes.add('chart-node');
    }

  } catch (error) {
    console.error('节点注册失败:', error);
  }
};

/**
 * 根据节点类型获取对应的注册节点名称
 */
export const getRegisteredNodeShape = (nodeType: string): string => {
  return NODE_TYPE_MAP[nodeType as keyof typeof NODE_TYPE_MAP] || 'icon-node';
};

/**
 * 获取图标URL
 */
const getIconUrl = (nodeConfig: any, iconList?: any[]): string => {
  if (nodeConfig.logoType === 'default' && nodeConfig.logoIcon) {
    if (iconList) {
      const iconItem = iconList.find(item => item.key === nodeConfig.logoIcon);
      return iconItem
        ? `/app/assets/assetModelIcon/${iconItem.url}.svg`
        : `/app/assets/assetModelIcon/${nodeConfig.logoIcon}.svg`;
    }
    return `/app/assets/assetModelIcon/${nodeConfig.logoIcon}.svg`;
  }

  if (nodeConfig.logoType === 'custom' && nodeConfig.logoUrl) {
    return nodeConfig.logoUrl;
  }

  return DEFAULT_ICON_PATH;
};

/**
 * 创建基础节点数据
 */
const createBaseNodeData = (nodeConfig: any, shape: string) => ({
  id: nodeConfig.id,
  shape,
  x: nodeConfig.x || 100,
  y: nodeConfig.y || 100,
  label: nodeConfig.name || '',
  data: {
    type: nodeConfig.type,
    name: nodeConfig.name,
    config: nodeConfig.config || {},
    ...nodeConfig
  }
});

/**
 * 创建图标节点
 */
const createIconNode = (nodeConfig: any, baseNodeData: any, iconList?: any[]) => {
  const logoUrl = getIconUrl(nodeConfig, iconList);
  const { ICON_NODE } = NODE_DEFAULTS;

  return {
    ...baseNodeData,
    width: nodeConfig.config?.width || ICON_NODE.width,
    height: nodeConfig.config?.height || ICON_NODE.height,
    attrs: {
      body: {
        fill: nodeConfig.config?.backgroundColor || ICON_NODE.backgroundColor,
        stroke: nodeConfig.config?.borderColor || ICON_NODE.borderColor
      },
      image: { 'xlink:href': logoUrl },
      label: {
        fill: nodeConfig.config?.textColor || ICON_NODE.textColor,
        fontSize: nodeConfig.config?.fontSize || ICON_NODE.fontSize,
        fontWeight: ICON_NODE.fontWeight,
        textAnchor: 'middle',
        textVerticalAnchor: 'top',
        refX: '50%',
        refY: '100%',
        refY2: '20',
        textWrap: { width: '90%', ellipsis: true }
      }
    },
    ports: createPortConfig()
  };
};

/**
 * 创建单值节点
 */
const createSingleValueNode = (nodeConfig: any, baseNodeData: any) => {
  const { SINGLE_VALUE_NODE } = NODE_DEFAULTS;
  const hasDataSource = nodeConfig.dataSource && nodeConfig.selectedFields?.length > 0;

  return {
    ...baseNodeData,
    width: nodeConfig.config?.width || SINGLE_VALUE_NODE.width,
    height: nodeConfig.config?.height || SINGLE_VALUE_NODE.height,
    data: {
      ...baseNodeData.data,
      dataSource: nodeConfig.dataSource,
      dataSourceParams: nodeConfig.dataSourceParams || [],
      selectedFields: nodeConfig.selectedFields || [],
      isLoading: hasDataSource,
      hasError: false
    },
    attrs: {
      body: {
        fill: nodeConfig.config?.backgroundColor || SINGLE_VALUE_NODE.backgroundColor,
        stroke: nodeConfig.config?.borderColor || SINGLE_VALUE_NODE.borderColor
      },
      label: {
        fill: nodeConfig.config?.textColor || SINGLE_VALUE_NODE.textColor,
        fontSize: nodeConfig.config?.fontSize || SINGLE_VALUE_NODE.fontSize
      }
    },
    ports: createPortConfig()
  };
};

/**
 * 创建文本节点
 */
const createTextNode = (nodeConfig: any, baseNodeData: any) => {
  const { TEXT_NODE } = NODE_DEFAULTS;

  return {
    ...baseNodeData,
    data: {
      ...baseNodeData.data,
      isPlaceholder: !nodeConfig.name || nodeConfig.name === '双击编辑文本'
    },
    attrs: {
      label: {
        fill: nodeConfig.config?.textColor || TEXT_NODE.textColor,
        fontSize: nodeConfig.config?.fontSize || TEXT_NODE.fontSize,
        text: nodeConfig.name || '双击编辑文本'
      }
    }
  };
};

/**
 * 创建图表节点
 */
const createChartNode = (nodeConfig: any, baseNodeData: any) => {
  const { CHART_NODE } = NODE_DEFAULTS;

  return {
    ...baseNodeData,
    width: nodeConfig.config?.width || CHART_NODE.width,
    height: nodeConfig.config?.height || CHART_NODE.height,
    data: {
      ...baseNodeData.data,
      widget: nodeConfig.widget,
      valueConfig: nodeConfig.valueConfig,
      dataSource: nodeConfig.dataSource,
      dataSourceParams: nodeConfig.dataSourceParams || [],
      isLoading: !!nodeConfig.dataSource,
      rawData: null,
      hasError: false
    },
    ports: createPortConfig()
  };
};

/**
 * 使用注册的节点创建节点数据
 */
export const createNodeByType = (nodeConfig: any, iconList?: any[]): any => {
  const shape = getRegisteredNodeShape(nodeConfig.type);
  const baseNodeData = createBaseNodeData(nodeConfig, shape);

  // 根据节点类型创建特定节点
  const nodeCreators = {
    'icon': () => createIconNode(nodeConfig, baseNodeData, iconList),
    'single-value': () => createSingleValueNode(nodeConfig, baseNodeData),
    'text': () => createTextNode(nodeConfig, baseNodeData),
    'chart': () => createChartNode(nodeConfig, baseNodeData)
  };

  return nodeCreators[nodeConfig.type as keyof typeof nodeCreators]?.() || baseNodeData;
};

/**
 * 更新图标节点属性
 */
const updateIconNodeAttributes = (node: any, nodeConfig: any, iconList?: any[]) => {
  const { ICON_NODE } = NODE_DEFAULTS;
  const logoUrl = getIconUrl(nodeConfig, iconList);

  node.setAttrs({
    body: {
      fill: nodeConfig.config?.backgroundColor || ICON_NODE.backgroundColor,
      stroke: nodeConfig.config?.borderColor || ICON_NODE.borderColor,
    },
    image: {
      'xlink:href': logoUrl
    },
    label: {
      fill: nodeConfig.config?.textColor || ICON_NODE.textColor,
      fontSize: nodeConfig.config?.fontSize || ICON_NODE.fontSize,
    }
  });

  // 如果尺寸发生变化，更新节点尺寸和端口
  if (nodeConfig.config?.width && nodeConfig.config?.height) {
    const { width: currentWidth, height: currentHeight } = node.getSize();

    if (currentWidth !== nodeConfig.config.width || currentHeight !== nodeConfig.config.height) {
      node.resize(nodeConfig.config.width, nodeConfig.config.height);
      node.prop('ports', createPortConfig()); // 重新计算端口位置
    }
  }
};

/**
 * 更新单值节点属性
 */
const updateSingleValueNodeAttributes = (node: any, nodeConfig: any) => {
  const { SINGLE_VALUE_NODE } = NODE_DEFAULTS;

  node.setAttrs({
    body: {
      fill: nodeConfig.config?.backgroundColor || SINGLE_VALUE_NODE.backgroundColor,
      stroke: nodeConfig.config?.borderColor || SINGLE_VALUE_NODE.borderColor,
    },
    label: {
      fill: nodeConfig.config?.textColor || SINGLE_VALUE_NODE.textColor,
      fontSize: nodeConfig.config?.fontSize || SINGLE_VALUE_NODE.fontSize,
    }
  });
};

/**
 * 更新文本节点属性
 */
const updateTextNodeAttributes = (node: any, nodeConfig: any) => {
  const { TEXT_NODE } = NODE_DEFAULTS;

  node.setAttrs({
    body: {
      fill: nodeConfig.config?.backgroundColor || TEXT_NODE.backgroundColor,
      stroke: nodeConfig.config?.borderColor || TEXT_NODE.borderColor,
    },
    label: {
      fill: nodeConfig.config?.textColor || TEXT_NODE.textColor,
      fontSize: nodeConfig.config?.fontSize || TEXT_NODE.fontSize,
      text: nodeConfig.name || '双击编辑文本',
    }
  });
};

/**
 * 动态更新节点属性（用于配置面板更新）
 */
export const updateNodeAttributes = (node: any, nodeConfig: any, iconList?: any[]): void => {
  if (!node || !nodeConfig) return;

  node.setData({
    ...node.getData(),
    ...nodeConfig,
    config: nodeConfig.config || {}
  });

  const updateStrategies = {
    'icon': () => updateIconNodeAttributes(node, nodeConfig, iconList),
    'single-value': () => updateSingleValueNodeAttributes(node, nodeConfig),
    'text': () => updateTextNodeAttributes(node, nodeConfig)
  };

  updateStrategies[nodeConfig.type as keyof typeof updateStrategies]?.();
};
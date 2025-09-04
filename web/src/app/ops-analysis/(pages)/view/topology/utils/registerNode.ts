import ChartNode from '../components/chartNode';
import { Graph } from '@antv/x6';
import { register } from '@antv/x6-react-shape';
import { NODE_DEFAULTS } from '../constants/nodeDefaults';
import { createPortConfig } from './topologyUtils';

const NODE_TYPE_MAP = {
  'icon': 'icon-node',
  'single-value': 'single-value-node',
  'text': 'text-node',
  'chart': 'chart-node',
  'basic-shape': 'basic-shape-node'
} as const;

const DEFAULT_ICON_PATH = '/app/assets/assetModelIcon/cc-default_默认.svg';

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
        ry: ICON_NODE.borderRadius
      },
      image: {
        fill: ICON_NODE.backgroundColor,
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
    ports: { groups: {}, items: [] }
  });
};

const registerBasicShapeNode = () => {
  const { BASIC_SHAPE_NODE } = NODE_DEFAULTS;

  Graph.registerNode('basic-shape-node', {
    inherit: 'rect',
    width: BASIC_SHAPE_NODE.width,
    height: BASIC_SHAPE_NODE.height,
    markup: [
      { tagName: 'rect', selector: 'body' }
    ],
    attrs: {
      body: {
        fill: BASIC_SHAPE_NODE.backgroundColor,
        stroke: BASIC_SHAPE_NODE.borderColor,
        strokeWidth: BASIC_SHAPE_NODE.borderWidth,
        rx: BASIC_SHAPE_NODE.borderRadius,
        ry: BASIC_SHAPE_NODE.borderRadius,
      }
    },
    ports: createPortConfig()
  });
};

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

const registeredNodes = new Set<string>();

export const registerNodes = () => {
  try {
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

    if (!registeredNodes.has('basic-shape-node')) {
      registerBasicShapeNode();
      registeredNodes.add('basic-shape-node');
    }

    if (!registeredNodes.has('chart-node')) {
      registerChartNode();
      registeredNodes.add('chart-node');
    }

  } catch (error) {
    console.error('节点注册失败:', error);
  }
};

export const getRegisteredNodeShape = (nodeType: string): string => {
  return NODE_TYPE_MAP[nodeType as keyof typeof NODE_TYPE_MAP] || 'icon-node';
};

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

const createIconNode = (nodeConfig: any, baseNodeData: any, iconList?: any[]) => {
  const logoUrl = getIconUrl(nodeConfig, iconList);

  return {
    ...baseNodeData,
    width: nodeConfig.styleConfig?.width,
    height: nodeConfig.styleConfig?.height,
    attrs: {
      image: {
        'xlink:href': logoUrl
      }
    },
    ports: createPortConfig()
  };
};

const createSingleValueNode = (nodeConfig: any, baseNodeData: any) => {
  const valueConfig = nodeConfig.valueConfig || {};
  const hasDataSource = valueConfig.dataSource && valueConfig.selectedFields?.length > 0;

  return {
    ...baseNodeData,
    data: {
      ...baseNodeData.data,
      dataSource: valueConfig.dataSource,
      dataSourceParams: valueConfig.dataSourceParams || [],
      selectedFields: valueConfig.selectedFields || [],
      isLoading: hasDataSource,
      hasError: false
    },
    attrs: {
      body: {
        fill: nodeConfig.styleConfig?.backgroundColor,
        stroke: nodeConfig.styleConfig?.borderColor
      },
      label: {
        fill: nodeConfig.styleConfig?.textColor,
        fontSize: nodeConfig.styleConfig?.fontSize
      }
    },
    ports: createPortConfig()
  };
};

const createTextNode = (nodeConfig: any, baseNodeData: any) => {

  return {
    ...baseNodeData,
    data: {
      ...baseNodeData.data,
      isPlaceholder: !nodeConfig.name || nodeConfig.name === '双击编辑文本'
    },
    attrs: {
      label: {
        fill: nodeConfig.styleConfig?.textColor,
        fontSize: nodeConfig.styleConfig?.fontSize,
        text: nodeConfig.name || '双击编辑文本'
      }
    }
  };
};

const createBasicShapeNode = (nodeConfig: any, baseNodeData: any) => {
  const { BASIC_SHAPE_NODE } = NODE_DEFAULTS;

  const getShapeSpecificAttrs = (shapeType: string) => {
    // 直接使用配置对象中的值
    const backgroundColor = nodeConfig.styleConfig?.backgroundColor;
    const borderColor = nodeConfig.styleConfig?.borderColor;
    const borderWidth = nodeConfig.styleConfig?.borderWidth;
    const lineType = nodeConfig.styleConfig?.lineType;

    // 支持透明背景 - 处理ColorPicker的透明值
    const isTransparent = !backgroundColor ||
      backgroundColor === 'transparent' ||
      backgroundColor === 'none' ||
      backgroundColor === '' ||
      backgroundColor === 'rgba(0,0,0,0)';

    const baseAttrs: any = {
      fill: isTransparent ? BASIC_SHAPE_NODE.backgroundColor : backgroundColor,
      fillOpacity: isTransparent ? 0 : 1,
      stroke: borderColor,
      strokeWidth: borderWidth,
    };

    if (lineType === 'dashed') {
      baseAttrs.strokeDasharray = '5,5';
    } else if (lineType === 'dotted') {
      baseAttrs.strokeDasharray = '2,2';
    } else {
      baseAttrs.strokeDasharray = 'none';
    }

    switch (shapeType) {
      case 'circle':
        return {
          ...baseAttrs,
          rx: '50%',
          ry: '50%'
        };
      case 'rectangle':
      default:
        return {
          ...baseAttrs,
          rx: BASIC_SHAPE_NODE.borderRadius,
          ry: BASIC_SHAPE_NODE.borderRadius
        };
    }
  };

  const shapeType = nodeConfig.styleConfig?.shapeType;
  const width = nodeConfig.styleConfig?.width;
  const height = nodeConfig.styleConfig?.height;

  return {
    ...baseNodeData,
    width: width,
    height: height,
    attrs: {
      body: getShapeSpecificAttrs(shapeType)
    },
    ports: createPortConfig()
  };
};

const createChartNode = (nodeConfig: any, baseNodeData: any) => {
  return {
    ...baseNodeData,
    width: nodeConfig.styleConfig?.width,
    height: nodeConfig.styleConfig?.height,
    data: {
      ...baseNodeData.data,
      valueConfig: nodeConfig.valueConfig,
      isLoading: !!nodeConfig.valueConfig.dataSource,
      rawData: null,
      hasError: false
    },
    ports: createPortConfig()
  };
};

export const createNodeByType = (nodeConfig: any, iconList?: any[]): any => {
  const shape = getRegisteredNodeShape(nodeConfig.type);
  const baseNodeData = {
    id: nodeConfig.id,
    x: nodeConfig.position?.x || nodeConfig.x,
    y: nodeConfig.position?.y || nodeConfig.y,
    shape,
    label: nodeConfig.name || '',
    data: { ...nodeConfig },
  };
  switch (nodeConfig.type) {
    case 'icon':
      return createIconNode(nodeConfig, baseNodeData, iconList);
    case 'single-value':
      return createSingleValueNode(nodeConfig, baseNodeData);
    case 'text':
      return createTextNode(nodeConfig, baseNodeData);
    case 'basic-shape':
      return createBasicShapeNode(nodeConfig, baseNodeData);
    case 'chart':
      return createChartNode(nodeConfig, baseNodeData);
    default:
      return baseNodeData;
  }
};

const updateIconNodeAttributes = (node: any, nodeConfig: any, iconList?: any[]) => {
  const logoUrl = getIconUrl(nodeConfig, iconList);
  node.setAttrs({
    image: {
      'xlink:href': logoUrl
    },
    label: {
      fill: nodeConfig.styleConfig?.textColor
    }
  });

  if (nodeConfig.styleConfig?.width && nodeConfig.styleConfig?.height) {
    const { width: currentWidth, height: currentHeight } = node.getSize();

    if (currentWidth !== nodeConfig.styleConfig.width || currentHeight !== nodeConfig.styleConfig.height) {
      node.resize(nodeConfig.styleConfig.width, nodeConfig.styleConfig.height);
      node.prop('ports', createPortConfig());
    }
  }
};

const updateSingleValueNodeAttributes = (node: any, nodeConfig: any) => {
  node.setAttrs({
    body: {
      fill: nodeConfig.styleConfig?.backgroundColor,
      stroke: nodeConfig.styleConfig?.borderColor,
    },
    label: {
      fill: nodeConfig.styleConfig?.textColor,
      fontSize: nodeConfig.styleConfig?.fontSize,
    }
  });
};

const updateTextNodeAttributes = (node: any, nodeConfig: any) => {
  node.setAttrs({
    body: {
      fill: nodeConfig.styleConfig?.backgroundColor,
      stroke: nodeConfig.styleConfig?.borderColor,
    },
    label: {
      fill: nodeConfig.styleConfig?.textColor,
      fontSize: nodeConfig.styleConfig?.fontSize,
      text: nodeConfig.name || '双击编辑文本',
    }
  });
};

const updateBasicShapeNodeAttributes = (node: any, nodeConfig: any) => {
  const { BASIC_SHAPE_NODE } = NODE_DEFAULTS;

  const getShapeSpecificAttrs = (shapeType: string) => {
    // 直接使用配置对象中的值
    const backgroundColor = nodeConfig.styleConfig?.backgroundColor;
    const borderColor = nodeConfig.styleConfig?.borderColor;
    const borderWidth = nodeConfig.styleConfig?.borderWidth;
    const lineType = nodeConfig.styleConfig?.lineType;

    // 支持透明背景 - 处理ColorPicker的透明值
    const isTransparent = !backgroundColor ||
      backgroundColor === 'transparent' ||
      backgroundColor === 'none' ||
      backgroundColor === '' ||
      backgroundColor === 'rgba(0,0,0,0)';

    const baseAttrs: any = {
      fill: isTransparent ? BASIC_SHAPE_NODE.backgroundColor : backgroundColor,
      fillOpacity: isTransparent ? 0 : 1,
      stroke: borderColor,
      strokeWidth: borderWidth,
    };

    // 根据线条类型设置 strokeDasharray
    if (lineType === 'dashed') {
      baseAttrs.strokeDasharray = '5,5';
    } else if (lineType === 'dotted') {
      baseAttrs.strokeDasharray = '2,2';
    } else {
      // 实线类型，确保清除 strokeDasharray
      baseAttrs.strokeDasharray = 'none';
    }

    switch (shapeType) {
      case 'circle':
        return {
          ...baseAttrs,
          rx: '50%',
          ry: '50%'
        };
      case 'rectangle':
      default:
        return {
          ...baseAttrs,
          rx: BASIC_SHAPE_NODE.borderRadius,
          ry: BASIC_SHAPE_NODE.borderRadius
        };
    }
  };

  const shapeType = nodeConfig.styleConfig?.shapeType;

  node.setAttrs({
    body: getShapeSpecificAttrs(shapeType)
  });

  const width = nodeConfig.styleConfig?.width;
  const height = nodeConfig.styleConfig?.height;
  if (width && height) {
    const { width: currentWidth, height: currentHeight } = node.getSize();

    if (currentWidth !== width || currentHeight !== height) {
      node.resize(width, height);
      node.prop('ports', createPortConfig());
    }
  }
};

export const updateNodeAttributes = (node: any, nodeConfig: any, iconList?: any[]): void => {
  if (!node || !nodeConfig) return;

  node.setLabel(nodeConfig.name);
  node.setData({
    ...node.getData(),
    ...nodeConfig,
  });

  const updateStrategies = {
    'icon': () => updateIconNodeAttributes(node, nodeConfig, iconList),
    'single-value': () => updateSingleValueNodeAttributes(node, nodeConfig),
    'text': () => updateTextNodeAttributes(node, nodeConfig),
    'basic-shape': () => updateBasicShapeNodeAttributes(node, nodeConfig)
  };

  updateStrategies[nodeConfig.type as keyof typeof updateStrategies]?.();
};
import { EdgeCreationData } from '@/app/ops-analysis/types/topology';
import { NODE_DEFAULTS, PORT_DEFAULTS, COLORS, SPACING } from '../constants/nodeDefaults';

const CONTENT_PENDING = 2;
const PORT_RADIUS = PORT_DEFAULTS.RADIUS;

// 通用工具函数
export const getValueByPath = (obj: any, path: string): any => {
  if (!obj || !path) return undefined;

  return path.split('.').reduce((current, key) => {
    return current && current[key] !== undefined ? current[key] : undefined;
  }, obj);
};

export const formatDisplayValue = (value: any): string => {
  if (value === null || value === undefined) return '-';
  if (typeof value === 'object') return JSON.stringify(value);
  return String(value);
};

// 创建端口组的通用函数
const createPortGroup = (x: number, y: number, fillColor = PORT_DEFAULTS.FILL_COLOR) => ({
  position: { name: 'absolute', args: { x, y } },
  attrs: {
    circle: {
      magnet: PORT_DEFAULTS.MAGNET,
      stroke: PORT_DEFAULTS.STROKE_COLOR,
      r: PORT_DEFAULTS.RADIUS,
      fill: fillColor,
      opacity: PORT_DEFAULTS.OPACITY.HIDDEN,
    },
  },
});

// 创建标准端口配置的通用函数
const createPortConfig = (width: number, height: number, fillColor = PORT_DEFAULTS.FILL_COLOR) => ({
  groups: {
    top: createPortGroup(width / 2, 0, fillColor),
    bottom: createPortGroup(width / 2, height, fillColor),
    left: createPortGroup(0, height / 2, fillColor),
    right: createPortGroup(width, height / 2, fillColor),
  },
  items: [
    { id: 'top', group: 'top' },
    { id: 'bottom', group: 'bottom' },
    { id: 'left', group: 'left' },
    { id: 'right', group: 'right' },
  ],
});

// 创建高级端口配置的函数（用于图标节点的复杂端口位置计算）
const createAdvancedPortConfig = (layout: any) => ({
  groups: {
    top: createPortGroup(layout.ports.top.x, layout.ports.top.y, '#FFFFFF'),
    bottom: createPortGroup(layout.ports.bottom.x, layout.ports.bottom.y, '#FFFFFF'),
    left: createPortGroup(layout.ports.left.x, layout.ports.left.y, '#FFFFFF'),
    right: createPortGroup(layout.ports.right.x, layout.ports.right.y, '#FFFFFF'),
  },
  items: [
    { id: 'top', group: 'top' },
    { id: 'bottom', group: 'bottom' },
    { id: 'left', group: 'left' },
    { id: 'right', group: 'right' },
  ],
});

// 创建基础属性配置的通用函数
const createBaseAttrs = (config: {
  backgroundColor: string;
  borderColor: string;
  textColor: string;
  fontSize: number;
  width: number;
  height: number;
  borderRadius?: number;
}) => ({
  body: {
    fill: config.backgroundColor,
    stroke: config.borderColor,
    strokeWidth: 1,
    rx: config.borderRadius || 4,
    ry: config.borderRadius || 4,
  },
  label: {
    fill: config.textColor,
    fontSize: config.fontSize,
    textAnchor: 'middle',
    textVerticalAnchor: 'middle',
  },
});

export const getNodeStyle = () => {
  const defaults = NODE_DEFAULTS.ICON_NODE;
  const layout = calculateNodeLayout(defaults.width, defaults.height);

  return {
    width: layout.nodeWidth,
    height: layout.nodeHeight,
    markup: [
      {
        tagName: 'rect',
        selector: 'body',
      },
      {
        tagName: 'image',
        selector: 'icon',
      },
      {
        tagName: 'rect',
        selector: 'label-bg',
      },
      {
        tagName: 'text',
        selector: 'label',
      },
    ],
    attrs: {
      body: {
        x: layout.body.x,
        y: layout.body.y,
        width: layout.body.width,
        height: layout.body.height,
        fill: '#ffffff',
        stroke: '#ddd',
        strokeWidth: 1,
        rx: 4,
        ry: 4,
      },
      icon: {
        x: layout.icon.x,
        y: layout.icon.y,
        width: layout.icon.width,
        height: layout.icon.height,
      },
      label: {
        fill: defaults.textColor,
        fontSize: 14,
        fontWeight: defaults.fontWeight,
        x: layout.label.x,
        y: layout.label.y,
        textAnchor: 'middle',
        textVerticalAnchor: 'middle',
      },
    },
    ports: createAdvancedPortConfig(layout),
  };
};

export const createEdgeLabel = (text: string = '') => {
  return {
    attrs: {
      text: {
        text,
        fill: '#333',
        fontSize: 12,
        textAnchor: 'middle',
        textVerticalAnchor: 'middle',
      },
    },
    position: 0.5,
  };
};

export const getEdgeStyle = (connectionType: 'none' | 'single' | 'double') => {
  const arrowConfig = {
    none: { sourceMarker: null, targetMarker: null },
    single: { sourceMarker: null, targetMarker: { name: 'block', size: 8 } },
    double: {
      sourceMarker: { name: 'block', size: 8 },
      targetMarker: { name: 'block', size: 8 },
    },
  };

  return {
    attrs: {
      line: {
        stroke: COLORS.EDGE.DEFAULT,
        strokeWidth: SPACING.STROKE_WIDTH.THIN,
        ...arrowConfig[connectionType],
      },
    },
    labels: [],
  };
};

export const getEdgeStyleWithLabel = (
  edgeData: EdgeCreationData,
  connectionType: 'none' | 'single' | 'double' = 'single'
): any => {
  const baseStyle = getEdgeStyle(connectionType);

  if (edgeData.lineType === 'common_line' && edgeData.lineName) {
    (baseStyle as any).labels = [createEdgeLabel(edgeData.lineName)];
  } else {
    (baseStyle as any).labels = [];
  }

  return baseStyle;
};

// 创建边工具配置的通用函数
const createEdgeToolConfig = (opacity: number) => ({
  vertices: {
    name: 'vertices',
    args: {
      attrs: {
        fill: COLORS.PRIMARY,
        opacity,
      },
      snapRadius: 20,
      addable: true,
      removable: true,
      removeRedundancies: true,
    },
  },
  sourceArrowhead: {
    name: 'source-arrowhead',
    args: {
      attrs: {
        d: 'M 0 -6 A 6 6 0 1 0 0 6 A 6 6 0 1 0 0 -6',
        fill: COLORS.PRIMARY,
        stroke: COLORS.BACKGROUND.WHITE,
        strokeWidth: SPACING.STROKE_WIDTH.THIN,
        cursor: 'move',
        opacity,
      },
    },
  },
  targetArrowhead: {
    name: 'target-arrowhead',
    args: {
      attrs: {
        d: 'M 0 -6 A 6 6 0 1 0 0 6 A 6 6 0 1 0 0 -6',
        fill: COLORS.PRIMARY,
        stroke: COLORS.BACKGROUND.WHITE,
        strokeWidth: SPACING.STROKE_WIDTH.THIN,
        cursor: 'move',
        opacity,
      },
    },
  },
});

export const addEdgeTools = (edge: any) => {
  const toolConfig = createEdgeToolConfig(PORT_DEFAULTS.OPACITY.HIDDEN);

  // 添加顶点编辑工具（默认透明）
  edge.addTools(toolConfig.vertices);
  // 添加源端点工具（起点，默认透明）
  edge.addTools(toolConfig.sourceArrowhead);
  // 添加目标端点工具（终点，默认透明）
  edge.addTools(toolConfig.targetArrowhead);
};

// 显示边工具
export const showEdgeTools = (edge: any) => {
  edge.removeTools();

  const toolConfig = createEdgeToolConfig(PORT_DEFAULTS.OPACITY.VISIBLE);

  edge.addTools(toolConfig.vertices);
  edge.addTools(toolConfig.sourceArrowhead);
  edge.addTools(toolConfig.targetArrowhead);
};

// 隐藏边工具
export const hideEdgeTools = (edge: any) => {
  edge.removeTools();
};

// 隐藏所有边的工具
export const hideAllEdgeTools = (graph: any) => {
  graph.getEdges().forEach((edge: any) => {
    hideEdgeTools(edge);
  });
};

export const showPorts = (graph: any, cell: any) => {
  if (cell.isNode()) {
    // 只为有端口的节点显示端口（排除文本节点）
    const nodeData = cell.getData();
    if (nodeData?.type !== 'text') {
      ['top', 'bottom', 'left', 'right'].forEach((port) =>
        cell.setPortProp(port, 'attrs/circle/opacity', PORT_DEFAULTS.OPACITY.VISIBLE)
      );
    }
  } else if (cell.isEdge()) {
    ['top', 'bottom', 'left', 'right'].forEach((port) => {
      const sourceNode = graph.getCellById(cell.getSourceCellId());
      const targetNode = graph.getCellById(cell.getTargetCellId());
      // 检查节点是否有端口
      if (sourceNode && sourceNode.getData()?.type !== 'text') {
        sourceNode.setPortProp(port, 'attrs/circle/opacity', PORT_DEFAULTS.OPACITY.VISIBLE);
      }
      if (targetNode && targetNode.getData()?.type !== 'text') {
        targetNode.setPortProp(port, 'attrs/circle/opacity', PORT_DEFAULTS.OPACITY.VISIBLE);
      }
    });
  }
};

export const hideAllPorts = (graph: any) => {
  graph.getNodes().forEach((node: any) => {
    // 只为有端口的节点隐藏端口（排除文本节点）
    const nodeData = node.getData();
    if (nodeData?.type !== 'text') {
      ['top', 'bottom', 'left', 'right'].forEach((port: string) =>
        node.setPortProp(port, 'attrs/circle/opacity', PORT_DEFAULTS.OPACITY.HIDDEN)
      );
    }
  });
};

// 文本节点样式配置
export const getTextNodeStyle = (nodeConfig?: any) => {
  const defaults = NODE_DEFAULTS.TEXT_NODE;

  const baseStyle = {
    width: defaults.width,
    height: defaults.height,
    markup: [
      {
        tagName: 'rect',
        selector: 'body',
      },
      {
        tagName: 'text',
        selector: 'label',
      },
    ],
    attrs: {
      body: {
        fill: defaults.backgroundColor,
        stroke: defaults.borderColor,
        strokeWidth: defaults.strokeWidth,
      },
      label: {
        fill: defaults.textColor,
        fontSize: defaults.fontSize,
        fontWeight: defaults.fontWeight,
        textAnchor: 'middle',
        textVerticalAnchor: 'middle',
        refX: '50%',
        refY: '50%',
      },
    },
    ports: { groups: {}, items: [] },
  };

  if (!nodeConfig) {
    return baseStyle;
  }

  return {
    id: nodeConfig.id,
    x: nodeConfig.x || 100,
    y: nodeConfig.y || 100,
    label: nodeConfig.name,
    data: {
      type: nodeConfig.type,
      name: nodeConfig.name,
      config: nodeConfig.config,
      isPlaceholder: false,
    },
    ...baseStyle,
  };
};

// 获取logo URL的辅助函数
export const getLogoUrl = (nodeConfig: any, iconList: any[]) => {
  if (nodeConfig.logoType === 'default' && nodeConfig.logoIcon) {
    const iconItem = iconList.find((item) => item.key === nodeConfig.logoIcon);
    if (iconItem) {
      return `/app/assets/assetModelIcon/${iconItem.url}.svg`;
    }
    return `/app/assets/assetModelIcon/${nodeConfig.logoIcon}.svg`;
  } else if (nodeConfig.logoType === 'custom' && nodeConfig.logoUrl) {
    return nodeConfig.logoUrl;
  }
  return '/app/assets/assetModelIcon/cc-default_默认.svg';
};

// 单值节点样式配置
export const getSingleValueNodeStyle = (nodeConfig: any) => {
  const config = nodeConfig.config || {};
  const defaults = NODE_DEFAULTS.SINGLE_VALUE_NODE;

  // 使用表单值、配置值或默认值
  const styleConfig = {
    textColor: nodeConfig.textColor || config.textColor || defaults.textColor,
    backgroundColor: nodeConfig.backgroundColor || config.backgroundColor || defaults.backgroundColor,
    borderColor: nodeConfig.borderColor || config.borderColor || defaults.borderColor,
    fontSize: nodeConfig.fontSize || config.fontSize || defaults.fontSize,
    width: defaults.width,
    height: defaults.height,
    borderRadius: defaults.borderRadius,
  };

  const baseAttrs = createBaseAttrs(styleConfig);

  // 判断是否需要显示loading状态
  const hasDataSource = nodeConfig.dataSource && nodeConfig.selectedFields?.length > 0;
  return {
    id: nodeConfig.id,
    x: nodeConfig.x || 100,
    y: nodeConfig.y || 100,
    shape: 'rect',
    width: styleConfig.width,
    height: styleConfig.height,
    label: nodeConfig.name,
    data: {
      type: nodeConfig.type || 'single-value',
      name: nodeConfig.name,
      dataSource: nodeConfig.dataSource,
      dataSourceParams: nodeConfig.dataSourceParams || {},
      selectedFields: nodeConfig.selectedFields || [],
      isLoading: hasDataSource,
      config: {
        ...styleConfig,
        ...config,
      },
    },
    attrs: {
      ...baseAttrs,
      label: {
        ...baseAttrs.label,
        text: nodeConfig.name,
        fontFamily: defaults.fontFamily,
      },
    },
    ports: createPortConfig(styleConfig.width, styleConfig.height),
  };
};

// 统一的节点布局计算函数
export const calculateNodeLayout = (iconWidth: number, iconHeight: number) => {
  const nodeWidth = iconWidth + CONTENT_PENDING;
  const nodeHeight = iconHeight + CONTENT_PENDING;

  return {
    nodeWidth,
    nodeHeight,
    body: {
      x: 0,
      y: 0,
      width: iconWidth - PORT_RADIUS,
      height: iconHeight - PORT_RADIUS,
    },
    icon: {
      x: CONTENT_PENDING / 2,
      y: CONTENT_PENDING / 2,
      width: iconWidth,
      height: iconHeight,
    },
    label: {
      x: CONTENT_PENDING,
      y: iconHeight / 2 + 26,
    },
    ports: {
      top: { x: iconWidth / 2 + PORT_RADIUS / 2, y: 0 },
      bottom: { x: iconWidth / 2 + PORT_RADIUS / 2, y: iconHeight + PORT_RADIUS },
      left: { x: 0, y: iconHeight / 2 + PORT_RADIUS / 2 },
      right: { x: iconWidth + PORT_RADIUS, y: iconHeight / 2 + PORT_RADIUS / 2 },
    }
  };
};

// 更新节点尺寸和端口位置的工具函数
const updateNodeSizeAndPorts = (node: any, iconWidth: number, iconHeight: number) => {
  const layout = calculateNodeLayout(iconWidth, iconHeight);

  node.resize(layout.nodeWidth, layout.nodeHeight);

  node.setAttrByPath('body/x', layout.body.x);
  node.setAttrByPath('body/y', layout.body.y);
  node.setAttrByPath('body/width', layout.body.width);
  node.setAttrByPath('body/height', layout.body.height);

  // 更新图标位置和大小
  node.setAttrByPath('icon/x', layout.icon.x);
  node.setAttrByPath('icon/y', layout.icon.y);
  node.setAttrByPath('icon/width', layout.icon.width);
  node.setAttrByPath('icon/height', layout.icon.height);

  // 更新标签位置
  node.setAttrByPath('label/x', layout.label.x);
  node.setAttrByPath('label/y', layout.label.y);

  // 更新端口位置
  node.prop('ports/groups/top/position/args', layout.ports.top);
  node.prop('ports/groups/bottom/position/args', layout.ports.bottom);
  node.prop('ports/groups/left/position/args', layout.ports.left);
  node.prop('ports/groups/right/position/args', layout.ports.right);
};

// 通用节点更新函数
export const updateNodeProperties = (node: any, nodeConfig: any, iconList: any[]) => {
  node.setLabel(nodeConfig.name);
  node.setData({
    type: nodeConfig.type,
    name: nodeConfig.name,
    logoType: nodeConfig.logoType,
    logoIcon:
      nodeConfig.logoType === 'default'
        ? nodeConfig.logoIcon
        : 'cc-host',
    logoUrl:
      nodeConfig.logoType === 'custom'
        ? nodeConfig.logoUrl
        : undefined,
    dataSource: nodeConfig.dataSource,
    dataSourceParams: nodeConfig.dataSourceParams,
    selectedFields: nodeConfig.selectedFields || [],
    config: {
      ...nodeConfig.config,
      width: nodeConfig.width,
      height: nodeConfig.height,
    },
  });

  if (nodeConfig.type === 'single-value') {
    // 更新单值节点属性
    node.setAttrByPath('label/text', nodeConfig.name);
    if (nodeConfig.config?.textColor) {
      node.setAttrByPath('label/fill', nodeConfig.config.textColor);
    }
    if (nodeConfig.config?.fontSize) {
      node.setAttrByPath('label/fontSize', nodeConfig.config.fontSize);
    }
    if (nodeConfig.config?.backgroundColor) {
      node.setAttrByPath('body/fill', nodeConfig.config.backgroundColor);
    }
    if (nodeConfig.config?.borderColor) {
      node.setAttrByPath('body/stroke', nodeConfig.config.borderColor);
    }
  } else {
    // 更新图标节点属性
    const logoUrl = getLogoUrl(nodeConfig, iconList);
    node.setAttrByPath('icon/xlink:href', logoUrl);

    if (nodeConfig.width && nodeConfig.height) {
      updateNodeSizeAndPorts(node, nodeConfig.width, nodeConfig.height);
      node.setAttrByPath('icon/xlink:href', logoUrl);
    }

    const defaults = NODE_DEFAULTS.ICON_NODE;
    const backgroundColor = nodeConfig.config?.backgroundColor || defaults.backgroundColor;
    const borderColor = nodeConfig.config?.borderColor || defaults.borderColor;

    node.setAttrByPath('body/fill', backgroundColor);
    node.setAttrByPath('body/stroke', borderColor);

    if (nodeConfig.config?.textColor) {
      node.setAttrByPath('label/fill', nodeConfig.config.textColor);
    }
    if (nodeConfig.config?.fontSize) {
      node.setAttrByPath('label/fontSize', nodeConfig.config.fontSize);
    }
  }
};

// 图标节点样式配置
export const getIconNodeStyle = (nodeConfig: any, logoUrl: string) => {
  const baseNodeStyle = getNodeStyle();
  const config = nodeConfig.config || {};
  const defaults = NODE_DEFAULTS.ICON_NODE;

  const iconWidth = nodeConfig.width || config.width || defaults.width;
  const iconHeight = nodeConfig.height || config.height || defaults.height;
  const layout = calculateNodeLayout(iconWidth, iconHeight);
  const logoType = nodeConfig.logoType || 'default';

  return {
    id: nodeConfig.id,
    x: nodeConfig.x,
    y: nodeConfig.y,
    width: layout.nodeWidth,
    height: layout.nodeHeight,
    label: nodeConfig.name,
    markup: baseNodeStyle.markup,
    data: {
      type: nodeConfig.type || 'icon',
      name: nodeConfig.name,
      logoType: logoType,
      logoIcon:
        logoType === 'default'
          ? nodeConfig.logoIcon
          : 'cc-host',
      logoUrl:
        logoType === 'custom'
          ? nodeConfig.logoUrl
          : undefined,
      dataSourceParams: nodeConfig.dataSourceParams || {},
      selectedFields: nodeConfig.selectedFields || [],
      config: {
        width: iconWidth,
        height: iconHeight,
        ...config,
      },
    },
    // 覆盖图标的 URL 和位置
    attrs: {
      ...baseNodeStyle.attrs,
      body: {
        ...baseNodeStyle.attrs.body,
        x: layout.body.x,
        y: layout.body.y,
        width: layout.body.width,
        height: layout.body.height,
        fill: '#ffffff',
        stroke: '#ddd',
      },
      icon: {
        ...baseNodeStyle.attrs.icon,
        'xlink:href': logoUrl,
        x: layout.icon.x,
        y: layout.icon.y,
        width: layout.icon.width,
        height: layout.icon.height,
      },
      label: {
        ...baseNodeStyle.attrs.label,
        x: layout.label.x,
        y: layout.label.y,
        fill: '#666666',
        fontSize: 14,
      },
    },
    ports: createAdvancedPortConfig(layout),
  };
};

// 图表节点样式配置
export const getChartNodeStyle = (nodeConfig: any) => {
  const config = nodeConfig.config || {};
  const defaults = NODE_DEFAULTS.CHART_NODE;

  const styleConfig = {
    backgroundColor: nodeConfig.backgroundColor || config.backgroundColor || defaults.backgroundColor,
    borderColor: nodeConfig.borderColor || config.borderColor || defaults.borderColor,
    textColor: nodeConfig.textColor || config.textColor || defaults.textColor,
    fontSize: nodeConfig.fontSize || config.fontSize || defaults.fontSize,
    width: nodeConfig.width || config.width || defaults.width,
    height: nodeConfig.height || config.height || defaults.height,
  };

  return {
    id: nodeConfig.id,
    x: nodeConfig.x,
    y: nodeConfig.y,
    width: styleConfig.width,
    height: styleConfig.height,
    shape: 'react-shape',
    data: {
      type: nodeConfig.type || 'chart',
      name: nodeConfig.name,
      widget: nodeConfig.widget,
      valueConfig: nodeConfig.valueConfig || {},
      dataSource: nodeConfig.dataSource,
      dataSourceParams: nodeConfig.dataSourceParams || [],
      selectedFields: nodeConfig.selectedFields || [],
      config: {
        ...styleConfig,
        ...config,
      },
    },
    ports: createPortConfig(styleConfig.width, styleConfig.height),
  };
};

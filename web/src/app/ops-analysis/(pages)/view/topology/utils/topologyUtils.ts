import { EdgeCreationData } from '@/app/ops-analysis/types/topology';
import { NODE_DEFAULTS, PORT_DEFAULTS, COLORS, SPACING, FORM_DEFAULTS } from '../constants/nodeDefaults';
const CONTENT_PENDING = 5;
const PORT_RADIUS = PORT_DEFAULTS.RADIUS;

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

export const getNodeStyle = () => {
  const defaults = NODE_DEFAULTS.ICON_NODE;

  return {
    width: defaults.width,
    height: defaults.height,
    markup: [
      {
        tagName: 'rect',
        selector: 'body', // 添加边框容器
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
        width: defaults.width,
        height: defaults.height,
        fill: 'transparent',
        stroke: '#ddd', // 默认边框颜色
        strokeWidth: 1,
        rx: 4, // 圆角
        ry: 4,
      },
      icon: {
        x: 30,
        y: 10,
        width: 60,
        height: 60,
      },
      label: {
        fill: defaults.textColor,
        fontSize: defaults.fontSize,
        fontWeight: defaults.fontWeight,
        x: 0,
        y: 30,
        textAnchor: 'middle',
        textVerticalAnchor: 'middle',
      },
    },
    ports: {
      groups: {
        top: {
          position: { name: 'absolute', args: { x: defaults.width / 2, y: 5 } },
          attrs: {
            circle: {
              magnet: PORT_DEFAULTS.MAGNET,
              stroke: PORT_DEFAULTS.STROKE_COLOR,
              r: PORT_DEFAULTS.RADIUS,
              fill: PORT_DEFAULTS.FILL_COLOR,
              opacity: PORT_DEFAULTS.OPACITY.HIDDEN,
            },
          },
        },
        bottom: {
          position: { name: 'absolute', args: { x: defaults.width / 2, y: 75 } },
          attrs: {
            circle: {
              magnet: PORT_DEFAULTS.MAGNET,
              stroke: PORT_DEFAULTS.STROKE_COLOR,
              r: PORT_DEFAULTS.RADIUS,
              fill: PORT_DEFAULTS.FILL_COLOR,
              opacity: PORT_DEFAULTS.OPACITY.HIDDEN,
            },
          },
        },
        left: {
          position: { name: 'absolute', args: { x: 25, y: 40 } },
          attrs: {
            circle: {
              magnet: PORT_DEFAULTS.MAGNET,
              stroke: PORT_DEFAULTS.STROKE_COLOR,
              r: PORT_DEFAULTS.RADIUS,
              fill: PORT_DEFAULTS.FILL_COLOR,
              opacity: PORT_DEFAULTS.OPACITY.HIDDEN,
            },
          },
        },
        right: {
          position: { name: 'absolute', args: { x: 95, y: 40 } },
          attrs: {
            circle: {
              magnet: PORT_DEFAULTS.MAGNET,
              stroke: PORT_DEFAULTS.STROKE_COLOR,
              r: PORT_DEFAULTS.RADIUS,
              fill: PORT_DEFAULTS.FILL_COLOR,
              opacity: PORT_DEFAULTS.OPACITY.HIDDEN,
            },
          },
        },
      },
      items: [
        { id: 'top', group: 'top' },
        { id: 'bottom', group: 'bottom' },
        { id: 'left', group: 'left' },
        { id: 'right', group: 'right' },
      ],
    },
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
        strokeWidth: SPACING.STROKE_WIDTH.DEFAULT,
        ...arrowConfig[connectionType],
      },
    },
    labels: [
      {
        position: 0.5,
        attrs: {
          label: {
            text: '',
            fill: COLORS.TEXT.SECONDARY,
            fontSize: 12,
            textAnchor: 'middle',
            textVerticalAnchor: 'middle',
            background: {
              fill: COLORS.BACKGROUND.WHITE,
              stroke: COLORS.BORDER.DEFAULT,
              rx: SPACING.BORDER_RADIUS.SMALL,
              ry: SPACING.BORDER_RADIUS.SMALL,
              padding: SPACING.PADDING.SMALL,
            },
          },
        },
      },
    ],
  };
};

export const getEdgeStyleWithLabel = (
  edgeData: EdgeCreationData,
  connectionType: 'none' | 'single' | 'double' = 'single'
): any => {
  const baseStyle = getEdgeStyle(connectionType);

  if (edgeData.lineType === 'line' && edgeData.lineName) {
    baseStyle.labels[0].attrs.label.text = edgeData.lineName;
  } else {
    baseStyle.labels = [];
  }

  return baseStyle;
};

export const addEdgeTools = (edge: any) => {
  // 添加顶点编辑工具（默认透明）
  edge.addTools({
    name: 'vertices',
    args: {
      attrs: {
        fill: COLORS.PRIMARY,
        opacity: PORT_DEFAULTS.OPACITY.HIDDEN,
      },
      snapRadius: 20,
      addable: true,
      removable: true,
      removeRedundancies: true,
    },
  });

  // 添加源端点工具（起点，默认透明）
  edge.addTools({
    name: 'source-arrowhead',
    args: {
      attrs: {
        d: 'M 0 -6 A 6 6 0 1 0 0 6 A 6 6 0 1 0 0 -6',
        fill: COLORS.PRIMARY,
        stroke: COLORS.BACKGROUND.WHITE,
        strokeWidth: SPACING.STROKE_WIDTH.THIN,
        cursor: 'move',
        opacity: PORT_DEFAULTS.OPACITY.HIDDEN,
      },
    },
  });

  // 添加目标端点工具（终点，默认透明）
  edge.addTools({
    name: 'target-arrowhead',
    args: {
      attrs: {
        d: 'M 0 -6 A 6 6 0 1 0 0 6 A 6 6 0 1 0 0 -6',
        fill: COLORS.PRIMARY,
        stroke: COLORS.BACKGROUND.WHITE,
        strokeWidth: SPACING.STROKE_WIDTH.THIN,
        cursor: 'move',
        opacity: PORT_DEFAULTS.OPACITY.HIDDEN,
      },
    },
  });
};

// 显示边工具
export const showEdgeTools = (edge: any) => {
  edge.removeTools();

  edge.addTools({
    name: 'vertices',
    args: {
      attrs: {
        fill: COLORS.PRIMARY,
        opacity: PORT_DEFAULTS.OPACITY.VISIBLE,
      },
      snapRadius: 20,
      addable: true,
      removable: true,
      removeRedundancies: true,
    },
  });

  // 添加可见的源端点工具
  edge.addTools({
    name: 'source-arrowhead',
    args: {
      attrs: {
        d: 'M 0 -6 A 6 6 0 1 0 0 6 A 6 6 0 1 0 0 -6',
        fill: COLORS.PRIMARY,
        stroke: COLORS.BACKGROUND.WHITE,
        strokeWidth: SPACING.STROKE_WIDTH.THIN,
        cursor: 'move',
        opacity: PORT_DEFAULTS.OPACITY.VISIBLE,
      },
    },
  });

  // 添加可见的目标端点工具
  edge.addTools({
    name: 'target-arrowhead',
    args: {
      attrs: {
        d: 'M 0 -6 A 6 6 0 1 0 0 6 A 6 6 0 1 0 0 -6',
        fill: COLORS.PRIMARY,
        stroke: COLORS.BACKGROUND.WHITE,
        strokeWidth: SPACING.STROKE_WIDTH.THIN,
        cursor: 'move',
        opacity: PORT_DEFAULTS.OPACITY.VISIBLE,
      },
    },
  });
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

// 添加文本节点样式配置
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
    ports: {
      groups: {},
      items: [],
    },
  };
  if (!nodeConfig) {
    return baseStyle;
  }

  const nodeData = {
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

  return nodeData;
};

// 获取logo URL的辅助函数
export const getLogoUrl = (nodeConfig: any, iconList: any[]) => {
  if (nodeConfig.logoType === 'default' && nodeConfig.logo) {
    const iconItem = iconList.find((item) => item.key === nodeConfig.logo);
    if (iconItem) {
      return `/app/assets/assetModelIcon/${iconItem.url}.svg`;
    }
    return `/app/assets/assetModelIcon/${nodeConfig.logo}.svg`;
  } else if (nodeConfig.logoType === 'custom' && nodeConfig.logo) {
    return nodeConfig.logo;
  }
  return '/app/assets/assetModelIcon/cc-default_默认.svg';
};

// 单值节点样式配置
export const getSingleValueNodeStyle = (nodeConfig: any) => {
  const config = nodeConfig.config || {};
  const defaults = NODE_DEFAULTS.SINGLE_VALUE_NODE;

  // 使用配置值或默认值
  const textColor = config.textColor || defaults.textColor;
  const backgroundColor = config.backgroundColor || defaults.backgroundColor;
  const borderColor = config.borderColor || defaults.borderColor;
  const fontSize = config.fontSize || defaults.fontSize;

  return {
    id: nodeConfig.id,
    x: nodeConfig.x || 100,
    y: nodeConfig.y || 100,
    shape: 'rect',
    width: defaults.width,
    height: defaults.height,
    label: nodeConfig.name,
    data: {
      type: nodeConfig.type,
      name: nodeConfig.name,
      dataSource: nodeConfig.dataSource,
      dataSourceParams: nodeConfig.dataSourceParams || {},
      selectedFields: nodeConfig.selectedFields || [], 
      config: nodeConfig.config,
    },
    attrs: {
      body: {
        fill: backgroundColor,
        stroke: borderColor,
        strokeWidth: defaults.strokeWidth,
        rx: defaults.borderRadius,
        ry: defaults.borderRadius,
      },
      label: {
        text: nodeConfig.name,
        fill: textColor,
        fontSize: fontSize,
        fontFamily: defaults.fontFamily,
        textAnchor: 'middle',
        textVerticalAnchor: 'middle',
      },
    },
    ports: {
      groups: {
        top: {
          position: { name: 'absolute', args: { x: defaults.width / 2, y: 0 } },
          attrs: {
            circle: {
              magnet: PORT_DEFAULTS.MAGNET,
              stroke: PORT_DEFAULTS.STROKE_COLOR,
              r: PORT_DEFAULTS.RADIUS,
              fill: PORT_DEFAULTS.FILL_COLOR,
              opacity: PORT_DEFAULTS.OPACITY.HIDDEN,
            },
          },
        },
        bottom: {
          position: { name: 'absolute', args: { x: defaults.width / 2, y: defaults.height } },
          attrs: {
            circle: {
              magnet: PORT_DEFAULTS.MAGNET,
              stroke: PORT_DEFAULTS.STROKE_COLOR,
              r: PORT_DEFAULTS.RADIUS,
              fill: PORT_DEFAULTS.FILL_COLOR,
              opacity: PORT_DEFAULTS.OPACITY.HIDDEN,
            },
          },
        },
        left: {
          position: { name: 'absolute', args: { x: 0, y: defaults.height / 2 } },
          attrs: {
            circle: {
              magnet: PORT_DEFAULTS.MAGNET,
              stroke: PORT_DEFAULTS.STROKE_COLOR,
              r: PORT_DEFAULTS.RADIUS,
              fill: PORT_DEFAULTS.FILL_COLOR,
              opacity: PORT_DEFAULTS.OPACITY.HIDDEN,
            },
          },
        },
        right: {
          position: { name: 'absolute', args: { x: defaults.width, y: defaults.height / 2 } },
          attrs: {
            circle: {
              magnet: PORT_DEFAULTS.MAGNET,
              stroke: PORT_DEFAULTS.STROKE_COLOR,
              r: PORT_DEFAULTS.RADIUS,
              fill: PORT_DEFAULTS.FILL_COLOR,
              opacity: PORT_DEFAULTS.OPACITY.HIDDEN,
            },
          },
        },
      },
      items: [
        { id: 'top', group: 'top' },
        { id: 'bottom', group: 'bottom' },
        { id: 'left', group: 'left' },
        { id: 'right', group: 'right' },
      ],
    },
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
      y: iconHeight / 2 + CONTENT_PENDING * 4,
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
  // 更新节点标签
  node.setLabel(nodeConfig.name);

  // 更新节点数据
  node.setData({
    type: nodeConfig.type,
    name: nodeConfig.name,
    logo: nodeConfig.logo,
    logoType: nodeConfig.logoType,
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

    if (nodeConfig.width && nodeConfig.height) {
      updateNodeSizeAndPorts(node, nodeConfig.width, nodeConfig.height);
    }

    // 更新图标URL
    node.setAttrByPath('icon/xlink:href', logoUrl);

    // 更新背景色和边框色
    if (nodeConfig.config?.backgroundColor) {
      node.setAttrByPath('body/fill', nodeConfig.config.backgroundColor);
    }
    if (nodeConfig.config?.borderColor) {
      node.setAttrByPath('body/stroke', nodeConfig.config.borderColor);
    }
  }
};

// 图标节点样式配置
export const getIconNodeStyle = (nodeConfig: any, logoUrl: string) => {
  const baseNodeStyle = getNodeStyle();

  const iconWidth = nodeConfig.width || nodeConfig.config?.width;
  const iconHeight = nodeConfig.height || nodeConfig.config?.height;
  const layout = calculateNodeLayout(iconWidth, iconHeight);

  return {
    id: nodeConfig.id,
    x: nodeConfig.x,
    y: nodeConfig.y,
    width: layout.nodeWidth,
    height: layout.nodeHeight,
    label: nodeConfig.name,
    markup: baseNodeStyle.markup,
    data: {
      type: nodeConfig.type,
      name: nodeConfig.name,
      logo: nodeConfig.logo,
      logoType: nodeConfig.logoType,
      dataSourceParams: nodeConfig.dataSourceParams || {},
      selectedFields: nodeConfig.selectedFields || [],
      config: {
        ...nodeConfig.config,
        width: iconWidth,
        height: iconHeight,
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
        fill: nodeConfig.config?.backgroundColor || 'transparent',
        stroke: nodeConfig.config?.borderColor || '#ddd',
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
        fill: nodeConfig.config?.textColor || baseNodeStyle.attrs.label.fill,
        fontSize: nodeConfig.config?.fontSize || baseNodeStyle.attrs.label.fontSize,
      },
    },
    ports: {
      ...baseNodeStyle.ports,
      groups: (() => {
        return {
          top: {
            position: { name: 'absolute', args: layout.ports.top },
            attrs: {
              ...baseNodeStyle.ports.groups.top.attrs,
              circle: {
                ...baseNodeStyle.ports.groups.top.attrs.circle,
                fill: '#ffffff',
              }
            },
          },
          bottom: {
            position: { name: 'absolute', args: layout.ports.bottom },
            attrs: {
              ...baseNodeStyle.ports.groups.bottom.attrs,
              circle: {
                ...baseNodeStyle.ports.groups.bottom.attrs.circle,
                fill: '#ffffff',
              }
            },
          },
          left: {
            position: { name: 'absolute', args: layout.ports.left },
            attrs: {
              ...baseNodeStyle.ports.groups.left.attrs,
              circle: {
                ...baseNodeStyle.ports.groups.left.attrs.circle,
                fill: '#ffffff',
              }
            },
          },
          right: {
            position: { name: 'absolute', args: layout.ports.right },
            attrs: {
              ...baseNodeStyle.ports.groups.right.attrs,
              circle: {
                ...baseNodeStyle.ports.groups.right.attrs.circle,
                fill: '#ffffff',
              }
            },
          },
        };
      })(),
      items: [
        { id: 'top', group: 'top' },
        { id: 'bottom', group: 'bottom' },
        { id: 'left', group: 'left' },
        { id: 'right', group: 'right' },
      ],
    },
  };
};

/**
 * 标准化节点配置
 */
export const normalizeNodeConfig = (values: any, baseConfig?: any) => {
  const baseData = baseConfig || {};

  if (values.type === "single-value" || baseData.type === "single-value") {
    return {
      id: baseData.id || values.id,
      type: "single-value",
      name: values.name,
      x: values.x || baseData.x,
      y: values.y || baseData.y,
      dataSource: values.dataSource,
      dataSourceParams: values.dataSourceParams,
      selectedFields: values.selectedFields || [],
      config: {
        query: values.query || FORM_DEFAULTS.SINGLE_VALUE.query,
        unit: values.unit || FORM_DEFAULTS.SINGLE_VALUE.unit,
        threshold: values.threshold || FORM_DEFAULTS.SINGLE_VALUE.threshold,
        textColor: values.textColor || FORM_DEFAULTS.SINGLE_VALUE.textColor,
        fontSize: values.fontSize || FORM_DEFAULTS.SINGLE_VALUE.fontSize,
        backgroundColor: values.backgroundColor || FORM_DEFAULTS.SINGLE_VALUE.backgroundColor,
        borderColor: values.borderColor || FORM_DEFAULTS.SINGLE_VALUE.borderColor,
      },
    };
  } else {
    return {
      id: baseData.id || values.id,
      type: values.type || "icon",
      name: values.name,
      x: values.x || baseData.x,
      y: values.y || baseData.y,
      logo: values.logoType === "default" ? values.logoIcon : values.logoUrl,
      logoType: values.logoType,
      width: values.width || baseData.width || FORM_DEFAULTS.ICON_NODE.width,
      height: values.height || baseData.height || FORM_DEFAULTS.ICON_NODE.height,
      dataSource: values.dataSource,
      dataSourceParams: values.dataSourceParams,
      selectedFields: values.selectedFields || [],
      config: {
        backgroundColor: values.backgroundColor || FORM_DEFAULTS.ICON_NODE.backgroundColor,
        borderColor: values.borderColor || FORM_DEFAULTS.ICON_NODE.borderColor,
        textColor: values.textColor,
        fontSize: values.fontSize,
        width: values.width || baseData.width || FORM_DEFAULTS.ICON_NODE.width,
        height: values.height || baseData.height || FORM_DEFAULTS.ICON_NODE.height,
      },
    };
  }
};

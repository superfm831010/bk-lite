import { EdgeCreationData } from '@/app/ops-analysis/types/topology';

export const getNodeStyle = () => {
  const defaults = NODE_DEFAULTS.ICON_NODE;

  return {
    width: defaults.width,
    height: defaults.height,
    markup: [
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

import { NODE_DEFAULTS, PORT_DEFAULTS, COLORS, SPACING } from '../constants/nodeDefaults';

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

// 图标节点样式配置
export const getIconNodeStyle = (nodeConfig: any, logoUrl: string) => {
  const baseNodeStyle = getNodeStyle();

  return {
    id: nodeConfig.id,
    x: nodeConfig.x || 100,
    y: nodeConfig.y || 100,
    label: nodeConfig.name,
    data: {
      type: nodeConfig.type,
      name: nodeConfig.name,
      logo: nodeConfig.logo,
      logoType: nodeConfig.logoType,
      config: nodeConfig.config,
    },
    ...baseNodeStyle,
    // 覆盖图标的 URL
    attrs: {
      ...baseNodeStyle.attrs,
      icon: {
        ...baseNodeStyle.attrs.icon,
        'xlink:href': logoUrl,
      },
    },
  };
};

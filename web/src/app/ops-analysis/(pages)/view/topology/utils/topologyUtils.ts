export const getNodeStyle = () => ({
  width: 120,
  height: 120,
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
      fill: '#262626',
      fontSize: 12,
      fontWeight: 500,
      x: 0,
      y: 30,
      textAnchor: 'middle',
      textVerticalAnchor: 'middle',
    },
  },
  ports: {
    groups: {
      top: {
        position: { name: 'absolute', args: { x: 60, y: 5 } }, 
        attrs: {
          circle: {
            magnet: true,
            stroke: '#1890FF',
            r: 4,
            fill: '#FFFFFF',
            opacity: 0,
          },
        },
      },
      bottom: {
        position: { name: 'absolute', args: { x: 60, y: 75 } },
        attrs: {
          circle: {
            magnet: true,
            stroke: '#1890FF',
            r: 4,
            fill: '#FFFFFF',
            opacity: 0,
          },
        },
      },
      left: {
        position: { name: 'absolute', args: { x: 25, y: 40 } }, 
        attrs: {
          circle: {
            magnet: true,
            stroke: '#1890FF',
            r: 4,
            fill: '#FFFFFF',
            opacity: 0,
          },
        },
      },
      right: {
        position: { name: 'absolute', args: { x: 95, y: 40 } }, 
        attrs: {
          circle: {
            magnet: true,
            stroke: '#1890FF',
            r: 4,
            fill: '#FFFFFF',
            opacity: 0,
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
});

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
        stroke: '#a7b5c4',
        strokeWidth: 2,
        ...arrowConfig[connectionType],
      },
    },
    labels: [
      {
        position: 0.5,
        attrs: {
          label: {
            text: '',
            fill: '#595959',
            fontSize: 12,
            textAnchor: 'middle',
            textVerticalAnchor: 'middle',
            background: {
              fill: 'white',
              stroke: '#d9d9d9',
              rx: 4,
              ry: 4,
              padding: 4,
            },
          },
        },
      },
    ],
  };
};

export const addEdgeTools = (edge: any) => {
  // 添加顶点编辑工具（默认透明）
  edge.addTools({
    name: 'vertices',
    args: {
      attrs: {
        fill: '#1890FF',
        opacity: 0, 
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
        fill: '#1890FF',
        stroke: '#ffffff',
        strokeWidth: 1,
        cursor: 'move',
        opacity: 0,
      },
    },
  });

  // 添加目标端点工具（终点，默认透明）
  edge.addTools({
    name: 'target-arrowhead',
    args: {
      attrs: {
        d: 'M 0 -6 A 6 6 0 1 0 0 6 A 6 6 0 1 0 0 -6',
        fill: '#1890FF',
        stroke: '#ffffff',
        strokeWidth: 1,
        cursor: 'move',
        opacity: 0, 
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
        fill: '#1890FF',
        opacity: 1,
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
        fill: '#1890FF',
        stroke: '#ffffff',
        strokeWidth: 1,
        cursor: 'move',
        opacity: 1,
      },
    },
  });

  // 添加可见的目标端点工具
  edge.addTools({
    name: 'target-arrowhead',
    args: {
      attrs: {
        d: 'M 0 -6 A 6 6 0 1 0 0 6 A 6 6 0 1 0 0 -6',
        fill: '#1890FF',
        stroke: '#ffffff',
        strokeWidth: 1,
        cursor: 'move',
        opacity: 1,
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
        cell.setPortProp(port, 'attrs/circle/opacity', 1)
      );
    }
  } else if (cell.isEdge()) {
    ['top', 'bottom', 'left', 'right'].forEach((port) => {
      const sourceNode = graph.getCellById(cell.getSourceCellId());
      const targetNode = graph.getCellById(cell.getTargetCellId());
      // 检查节点是否有端口
      if (sourceNode && sourceNode.getData()?.type !== 'text') {
        sourceNode.setPortProp(port, 'attrs/circle/opacity', 1);
      }
      if (targetNode && targetNode.getData()?.type !== 'text') {
        targetNode.setPortProp(port, 'attrs/circle/opacity', 1);
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
        node.setPortProp(port, 'attrs/circle/opacity', 0)
      );
    }
  });
};

// 添加文本节点样式配置
export const getTextNodeStyle = () => ({
  width: 120,
  height: 40,
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
      fill: 'transparent',
      stroke: 'transparent',
      strokeWidth: 1,
    },
    label: {
      fill: '#262626',
      fontSize: 14,
      fontWeight: 400,
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
});

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
export const getSingleValueNodeStyle = (nodeConfig: any) => ({
  id: nodeConfig.id,
  x: nodeConfig.x || 100,
  y: nodeConfig.y || 100,
  shape: 'rect',
  width: 120,
  height: 40,
  label: nodeConfig.name,
  data: {
    type: nodeConfig.type,
    name: nodeConfig.name,
    dataSource: nodeConfig.dataSource,
    config: nodeConfig.config,
  },
  attrs: {
    body: {
      fill: '#ffffff',
      stroke: '#d9d9d9',
      strokeWidth: 1,
      rx: 6,
      ry: 6,
    },
    label: {
      text: nodeConfig.name,
      fill: '#333333',
      fontSize: 14,
      fontFamily: 'Arial, sans-serif',
      textAnchor: 'middle',
      textVerticalAnchor: 'middle',
    },
  },
  ports: {
    groups: {
      top: {
        position: { name: 'absolute', args: { x: 60, y: 0 } },
        attrs: {
          circle: {
            magnet: true,
            stroke: '#1890FF',
            r: 4,
            fill: '#FFFFFF',
            opacity: 0,
          },
        },
      },
      bottom: {
        position: { name: 'absolute', args: { x: 60, y: 40 } },
        attrs: {
          circle: {
            magnet: true,
            stroke: '#1890FF',
            r: 4,
            fill: '#FFFFFF',
            opacity: 0,
          },
        },
      },
      left: {
        position: { name: 'absolute', args: { x: 0, y: 20 } },
        attrs: {
          circle: {
            magnet: true,
            stroke: '#1890FF',
            r: 4,
            fill: '#FFFFFF',
            opacity: 0,
          },
        },
      },
      right: {
        position: { name: 'absolute', args: { x: 120, y: 20 } },
        attrs: {
          circle: {
            magnet: true,
            stroke: '#1890FF',
            r: 4,
            fill: '#FFFFFF',
            opacity: 0,
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
});

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

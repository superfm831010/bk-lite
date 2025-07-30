export const getNodeStyle = () => ({
  width: 120,
  height: 80,
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
      x: 25,
      y: 5,
      width: 70,
      height: 50,
      'xlink:href':
        'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNzAiIGhlaWdodD0iNTAiIHZpZXdCb3g9IjAgMCA3MCA1MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cmVjdCB3aWR0aD0iNzAiIGhlaWdodD0iNTAiIHJ4PSI4IiBmaWxsPSIjZjBmOGZmIiBzdHJva2U9IiMxODkwRkYiIHN0cm9rZS13aWR0aD0iMiIvPgogIDxyZWN0IHg9IjE1IiB5PSIxMiIgd2lkdGg9IjQwIiBoZWlnaHQ9IjI2IiByeD0iNCIgZmlsbD0iIzE4OTBGRiIvPgogIDxjaXJjbGUgY3g9IjI1IiBjeT0iMjUiIHI9IjQiIGZpbGw9IndoaXRlIi8+CiAgPGNpcmNsZSBjeD0iMzUiIGN5PSIyMCIgcj0iMyIgZmlsbD0id2hpdGUiLz4KICA8Y2lyY2xlIGN4PSI0NSIgY3k9IjMwIiByPSIzIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K',
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
            r: 6,
            fill: '#FFFFFF',
            opacity: 0,
          },
        },
      },
      bottom: {
        position: { name: 'absolute', args: { x: 60, y: 55 } },
        attrs: {
          circle: {
            magnet: true,
            stroke: '#1890FF',
            r: 6,
            fill: '#FFFFFF',
            opacity: 0,
          },
        },
      },
      left: {
        position: { name: 'absolute', args: { x: 25, y: 30 } }, 
        attrs: {
          circle: {
            magnet: true,
            stroke: '#1890FF',
            r: 6,
            fill: '#FFFFFF',
            opacity: 0,
          },
        },
      },
      right: {
        position: { name: 'absolute', args: { x: 95, y: 30 } }, 
        attrs: {
          circle: {
            magnet: true,
            stroke: '#1890FF',
            r: 6,
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
        stroke: '#8C8C8C',
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
  edge.addTools({
    name: 'vertices',
    args: {
      attrs: { fill: '#1890FF' },
      snapRadius: 20,
      addable: true,
      removable: true,
      removeRedundancies: true,
    },
  });

  const data = edge.getData() || {};
  const connectionType = data.connectionType || 'single';

  if (connectionType === 'single' || connectionType === 'double') {
    edge.addTools({
      name: 'target-arrowhead',
      args: {
        attrs: {
          d: 'M 0 -6 A 6 6 0 1 0 0 6 A 6 6 0 1 0 0 -6',
          fill: '#1890FF',
        },
      },
    });
  }

  if (connectionType === 'double') {
    edge.addTools({
      name: 'source-arrowhead',
      args: {
        attrs: {
          d: 'M 0 -6 A 6 6 0 1 0 0 6 A 6 6 0 1 0 0 -6',
          fill: '#1890FF',
        },
      },
    });
  }
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
  // 文本节点不需要连接端口
  ports: {
    groups: {},
    items: [],
  },
});

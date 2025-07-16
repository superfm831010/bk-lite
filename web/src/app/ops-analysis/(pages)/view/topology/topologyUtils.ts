import type { Graph as X6Graph, Edge, Node } from '@antv/x6';
import type { DataNode } from 'antd/lib/tree';

export const getNodeStyle = () => ({
  width: 120,
  height: 60,
  attrs: {
    body: {
      fill: '#FFFFFF',
      stroke: '#1890FF',
      strokeWidth: 2,
      rx: 8,
      ry: 8,
      magnet: true,
    },
    label: {
      fill: '#262626',
      fontSize: 14,
      fontWeight: 500,
      refX: 0.5,
      refY: 0.5,
      textAnchor: 'middle',
      textVerticalAnchor: 'middle',
    },
    port: {
      r: 6,
      magnet: true,
      stroke: '#1890FF',
      strokeWidth: 2,
      fill: '#FFFFFF',
      opacity: 0,
    },
  },
  ports: {
    groups: {
      top: {
        position: 'top',
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
        position: 'bottom',
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
        position: 'left',
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
        position: 'right',
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
            text:
                            connectionType === 'none'
                              ? '连接'
                              : connectionType === 'single'
                                ? '单向'
                                : '双向',
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

export const showPorts = (graph: X6Graph, cell: Node | Edge) => {
  if (cell.isNode()) {
    ['top', 'bottom', 'left', 'right'].forEach((port) =>
      cell.setPortProp(port, 'attrs/circle/opacity', 1)
    );
  } else if (cell.isEdge()) {
    ['top', 'bottom', 'left', 'right'].forEach((port) => {
      const sourceNode: any = graph.getCellById(cell.getSourceCellId());
      const targetNode: any = graph.getCellById(cell.getTargetCellId());
      sourceNode && sourceNode.setPortProp(port, 'attrs/circle/opacity', 1);
      targetNode && targetNode.setPortProp(port, 'attrs/circle/opacity', 1);
    });
  }
};

export const hideAllPorts = (graph: X6Graph) => {
  graph.getNodes().forEach((node) =>
    ['top', 'bottom', 'left', 'right'].forEach((port) =>
      node.setPortProp(port, 'attrs/circle/opacity', 0)
    )
  );
};

export const filterTree = (nodes: DataNode[], searchTerm: string): DataNode[] => {
  return nodes
    .filter(
      (node) =>
        typeof node.title === 'string' &&
                node.title.toLowerCase().includes(searchTerm.toLowerCase())
    )
    .map((node) => ({
      ...node,
      children: node.children ? filterTree(node.children, searchTerm) : undefined,
    }));
};

export const isPortClicked = (node: Node, x: number, y: number): boolean => {
  const bbox = node.getBBox();
  const centerX = bbox.x + bbox.width / 2;
  const centerY = bbox.y + bbox.height / 2;
  const relativeX = x - centerX;
  const relativeY = y - centerY;
  const ports = node.getPorts() || [];
  const portsPosition = node.getPortsPosition('absolute');
  for (const port of ports) {
    const portPosition = portsPosition[port.id!]?.position;
    if (portPosition) {
      const distance = Math.sqrt(
        Math.pow(relativeX - portPosition.x, 2) +
                Math.pow(relativeY - portPosition.y, 2)
      );
      if (distance <= 10) return true;
    }
  }
  return false;
};

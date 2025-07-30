// 初始 mock 节点配置
export const mockInitialNodes = [
  {
    id: 'node1',
    x: 100,
    y: 80,
    label: 'Web Server',
  },
  {
    id: 'node2',
    x: 350,
    y: 80,
    label: 'Database',
  },
  {
    id: 'node3',
    x: 100,
    y: 220,
    label: 'Load Balancer',
  },
  {
    id: 'node4',
    x: 350,
    y: 220,
    label: 'Cache Server',
  },
];

// 初始 mock 连线配置
export const mockInitialEdges = [
  {
    source: { cell: 'node1', port: 'right' },
    target: { cell: 'node2', port: 'left' },
    attrs: { line: { stroke: '#8C8C8C', strokeWidth: 2 } },
  },
  {
    source: { cell: 'node2', port: 'bottom' },
    target: { cell: 'node4', port: 'top' },
    attrs: { line: { stroke: '#8C8C8C', strokeWidth: 2 } },
  },
  {
    source: { cell: 'node1', port: 'bottom' },
    target: { cell: 'node3', port: 'top' },
    attrs: { line: { stroke: '#8C8C8C', strokeWidth: 2 } },
  },
  {
    source: { cell: 'node3', port: 'right' },
    target: { cell: 'node4', port: 'left' },
    attrs: { line: { stroke: '#8C8C8C', strokeWidth: 2 } },
  },
];


export const mockDirs = [
  {
    id: '1',
    name: 'Group 1',
    type: 'group',
    children: [
      {
        id: '2',
        name: 'Dashboard 1',
        type: 'dashboard',
        description: '示例仪表1的描述长文本',
      },
      {
        id: '3',
        name: 'Topology 1',
        type: 'topology',
        description: '示例拓扑 1 - 展示系统架构和服务间关系',
      },
      {
        id: '6',
        name: 'Subgroup 1-1',
        type: 'group',
        children: [
          {
            id: '7',
            name: 'Dashboard 1-1',
            type: 'dashboard',
            description: '示例仪表 1-1',
          },
        ],
      },
    ],
  },
  {
    id: '4',
    name: 'Group 2',
    type: 'group',
    children: [
      {
        id: '5',
        name: 'Dashboard 2',
        type: 'dashboard',
        description: '示例仪表 2',
      },
      {
        id: '8',
        name: 'Network Topology',
        type: 'topology',
        description: '网络拓扑图 - 显示网络设备和连接关系',
      },
    ],
  },
];


export const mockInterfaces = [
  { value: 'eth0', label: 'eth0 (以太网接口)' },
  { value: 'eth1', label: 'eth1 (以太网接口)' },
  { value: 'wlan0', label: 'wlan0 (无线接口)' },
  { value: 'lo', label: 'lo (回环接口)' },
  { value: 'vlan10', label: 'vlan10 (虚拟接口)' },
];
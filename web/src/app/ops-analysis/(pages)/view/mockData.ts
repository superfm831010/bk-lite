import type { DataNode } from 'antd/lib/tree';

// Mock 实例组与实例数据
export const mockGroups: DataNode[] = [
  {
    title: 'Group A',
    key: 'gA',
    children: [
      { title: 'Subgroup A1', key: 'gA1' },
      { title: 'Subgroup A2', key: 'gA2' },
    ],
  },
  {
    title: 'Group B',
    key: 'gB',
    children: [{ title: 'Subgroup B1', key: 'gB1' }],
  },
];

// Mock instances data
export const mockInstances: Record<
  string,
  Array<{ id: string; name: string }>
> = {
  gA1: [
    { id: 'i1', name: 'Instance A1-1' },
    { id: 'i2', name: 'Instance A1-2' },
  ],
  gA2: [{ id: 'i3', name: 'Instance A2-1' }],
  gB1: [{ id: 'i4', name: 'Instance B1-1' }],
};

// 初始 mock 节点配置
export const mockInitialNodes = [
  {
    id: 'node1',
    x: 100,
    y: 80,
    width: 100,
    height: 40,
    label: 'Node 1',
    attrs: {
      body: {
        fill: '#FFFFFF',
        stroke: '#1890FF',
        strokeWidth: 2,
        rx: 6,
        ry: 6,
        magnet: true,
      },
      label: { fill: '#262626', fontSize: 14, fontWeight: 500 },
    },
  },
  {
    id: 'node2',
    x: 300,
    y: 80,
    width: 100,
    height: 40,
    label: 'Node 2',
    attrs: {
      body: {
        fill: '#FFFFFF',
        stroke: '#1890FF',
        strokeWidth: 2,
        rx: 6,
        ry: 6,
        magnet: true,
      },
      label: { fill: '#262626', fontSize: 14, fontWeight: 500 },
    },
  },
  {
    id: 'node3',
    x: 100,
    y: 200,
    width: 100,
    height: 40,
    label: 'Node 3',
    attrs: {
      body: {
        fill: '#FFFFFF',
        stroke: '#1890FF',
        strokeWidth: 2,
        rx: 6,
        ry: 6,
        magnet: true,
      },
      label: { fill: '#262626', fontSize: 14, fontWeight: 500 },
    },
  },
  {
    id: 'node4',
    x: 300,
    y: 200,
    width: 100,
    height: 40,
    label: 'Node 4',
    attrs: {
      body: {
        fill: '#FFFFFF',
        stroke: '#1890FF',
        strokeWidth: 2,
        rx: 6,
        ry: 6,
        magnet: true,
      },
      label: { fill: '#262626', fontSize: 14, fontWeight: 500 },
    },
  },
];

// 初始 mock 连线配置
export const mockInitialEdges = [
  {
    source: { cell: 'node1' },
    target: { cell: 'node2' },
    attrs: { line: { stroke: '#8C8C8C', strokeWidth: 2 } },
  },
  {
    source: { cell: 'node2' },
    target: { cell: 'node4' },
    attrs: { line: { stroke: '#8C8C8C', strokeWidth: 2 } },
  },
  {
    source: { cell: 'node1' },
    target: { cell: 'node3' },
    attrs: { line: { stroke: '#8C8C8C', strokeWidth: 2 } },
  },
  {
    source: { cell: 'node3' },
    target: { cell: 'node4' },
    attrs: { line: { stroke: '#8C8C8C', strokeWidth: 2 } },
  },
];

export const widget1Option = {
  title: { text: 'Bar Chart' },
  tooltip: {},
  xAxis: { data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'] },
  yAxis: {},
  series: [
    { name: 'Sales', type: 'bar', data: [120, 200, 150, 80, 70, 110, 130] },
  ],
};

export const widget3Tasks: string[] = ['Task 1', 'Task 2', 'Task 3'];

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
        description: '示例仪表 1',
      },
      {
        id: '3',
        name: 'Topology 1',
        type: 'topology',
        description: '示例拓扑 1',
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
    ],
  },
];

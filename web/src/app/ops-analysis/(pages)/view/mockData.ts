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

// 图标映射表 - 可用的系统图标
export const availableIcons = {
  // 网络设备
  router: 'cc-router',
  switch: 'cc-switch2',
  firewall: 'cc-firewall',
  loadbalancer: 'cc-balance',

  // 服务器和计算
  server: 'cc-host',
  hardserver: 'cc-hard-server',
  cloudserver: 'cc-cloud-server',
  cloudhost: 'cc-cloud-host',

  // 数据库
  database: 'cc-db',
  mysql: 'cc-mysql',
  oracle: 'cc-oracle',
  postgresql: 'cc-postgresql',
  mongodb: 'cc-mongodb',
  redis: 'cc-redis',
  sqlserver: 'cc-sql-server',
  db2: 'cc-db2',

  // 中间件和应用
  nginx: 'cc-nginx',
  apache: 'cc-apache',
  tomcat: 'cc-tomcat',
  iis: 'cc-iis',
  weblogic: 'cc-weblogic',
  websphere: 'cc-websphere',

  // 容器和云
  docker: 'cc-docker',
  k8s: 'cc-k8s-cluster',
  pod: 'cc-pod',
  cloud: 'cc-cloud',

  // 消息队列
  kafka: 'cc-kafka',
  rabbitmq: 'cc-rabbitmq',
  ibmmq: 'cc-ibmmq',

  // 监控和管理
  elasticsearch: 'cc-elasticsearch',
  zookeeper: 'cc-zookeeper',
  nacos: 'cc-nacos',

  // 存储
  storage: 'cc-storage',
  minio: 'cc-minio',

  // 网络
  subnet: 'cc-subnet',
  ip: 'cc-ip',

  // 基础设施
  datacenter: 'cc-datacenter-dc',
  rack: 'cc-datacenter-rack',
  room: 'cc-datacenter-room',

  // 安全
  security: 'cc-security-equipment',
  certificate: 'cc-certificate',

  // 其他
  equipment: 'cc-equipment',
  module: 'cc-module',
  default: 'cc-default'
};

// 模拟拓扑节点数据
export const mockTopologyNodes = [
  // 核心网络设备
  {
    id: 'node-1',
    x: 200,
    y: 100,
    type: 'icon',
    name: '核心路由器',
    logo: 'cc-router',
    logoType: 'default',
    config: {
      description: '核心网络路由器设备',
      ip: '192.168.1.1',
      location: '机房A-01'
    }
  },
  {
    id: 'node-2',
    x: 100,
    y: 250,
    type: 'icon',
    name: '交换机-01',
    logo: 'cc-switch2',
    logoType: 'default',
    config: {
      description: '接入层交换机',
      ip: '192.168.1.10',
      location: '机房A-02'
    }
  },
  {
    id: 'node-3',
    x: 300,
    y: 250,
    type: 'icon',
    name: '交换机-02',
    logo: 'cc-switch2',
    logoType: 'default',
    config: {
      description: '接入层交换机',
      ip: '192.168.1.11',
      location: '机房A-03'
    }
  },
  // 服务器节点
  {
    id: 'node-4',
    x: 50,
    y: 400,
    type: 'icon',
    name: 'Web服务器',
    logo: 'cc-host',
    logoType: 'default',
    config: {
      description: 'Web应用服务器',
      ip: '192.168.1.100',
      cpu: '8核',
      memory: '16GB'
    }
  },
  {
    id: 'node-5',
    x: 150,
    y: 400,
    type: 'icon',
    name: '数据库服务器',
    logo: 'cc-db',
    logoType: 'default',
    config: {
      description: '数据库服务器集群',
      ip: '192.168.1.101',
      cpu: '16核',
      memory: '32GB'
    }
  },
  {
    id: 'node-6',
    x: 250,
    y: 400,
    type: 'icon',
    name: '应用服务器',
    logo: 'cc-hard-server',
    logoType: 'default',
    config: {
      description: '业务应用服务器',
      ip: '192.168.1.102',
      cpu: '12核',
      memory: '24GB'
    }
  },
  {
    id: 'node-7',
    x: 350,
    y: 400,
    type: 'icon',
    name: '缓存服务器',
    logo: 'cc-redis',
    logoType: 'default',
    config: {
      description: 'Redis缓存服务器',
      ip: '192.168.1.103',
      cpu: '8核',
      memory: '16GB'
    }
  },
  // 监控节点（单值类型）
  {
    id: 'node-8',
    x: 450,
    y: 150,
    type: 'single-value',
    name: 'CPU使用率',
    dataSource: 'prometheus',
    config: {
      query: 'cpu_usage_percent',
      unit: '%',
      threshold: 80,
      textColor: '#1890ff',
      fontSize: 12,
      backgroundColor: '#f0f8ff',
      borderColor: '#1890ff'
    }
  },
  {
    id: 'node-9',
    x: 450,
    y: 220,
    type: 'single-value',
    name: '内存使用率',
    dataSource: 'prometheus',
    config: {
      query: 'memory_usage_percent',
      unit: '%',
      threshold: 90,
      textColor: '#52c41a',
      fontSize: 12,
      backgroundColor: '#f6ffed',
      borderColor: '#52c41a'
    }
  },
  {
    id: 'node-10',
    x: 450,
    y: 290,
    type: 'single-value',
    name: '网络流量',
    dataSource: 'prometheus',
    config: {
      query: 'network_traffic_mbps',
      unit: 'Mbps',
      threshold: 100,
      textColor: '#fa8c16',
      fontSize: 12,
      backgroundColor: '#fff7e6',
      borderColor: '#fa8c16'
    }
  },
  // 外部服务
  {
    id: 'node-11',
    x: 200,
    y: 550,
    type: 'icon',
    name: '防火墙',
    logo: 'cc-firewall',
    logoType: 'default',
    config: {
      description: '边界防火墙设备',
      ip: '192.168.1.1',
      model: 'FortiGate 100F'
    }
  },
  {
    id: 'node-12',
    x: 80,
    y: 100,
    type: 'icon',
    name: '负载均衡器',
    logo: 'cc-balance',
    logoType: 'default',
    config: {
      description: 'F5负载均衡设备',
      ip: '192.168.1.5',
      model: 'F5 BIG-IP'
    }
  },
  // 新增节点 - 更多设备类型
  {
    id: 'node-13',
    x: 450,
    y: 550,
    type: 'icon',
    name: 'Nginx代理',
    logo: 'cc-nginx',
    logoType: 'default',
    config: {
      description: 'Nginx反向代理服务器',
      ip: '192.168.1.110',
      version: '1.20.2'
    }
  },
  {
    id: 'node-14',
    x: 300,
    y: 550,
    type: 'icon',
    name: '存储设备',
    logo: 'cc-storage',
    logoType: 'default',
    config: {
      description: '网络存储设备',
      ip: '192.168.1.200',
      capacity: '10TB'
    }
  },
  {
    id: 'node-15',
    x: 100,
    y: 550,
    type: 'icon',
    name: 'Docker容器',
    logo: 'cc-docker',
    logoType: 'default',
    config: {
      description: 'Docker容器平台',
      ip: '192.168.1.150',
      version: '20.10.0'
    }
  }
];

// 模拟拓扑边数据
export const mockTopologyEdges = [
  // 核心路由器连接
  {
    id: 'edge-1',
    source: 'node-1',
    target: 'node-2',
    sourcePort: 'bottom',
    targetPort: 'top',
    lineType: 'network line',
    lineName: '千兆以太网',
    sourceInterface: 'eth0',
    targetInterface: 'eth1',
    config: {
      bandwidth: '1Gbps',
      protocol: 'Ethernet'
    }
  },
  {
    id: 'edge-2',
    source: 'node-1',
    target: 'node-3',
    sourcePort: 'bottom',
    targetPort: 'top',
    lineType: 'network line',
    lineName: '千兆以太网',
    sourceInterface: 'eth1',
    targetInterface: 'eth1',
    config: {
      bandwidth: '1Gbps',
      protocol: 'Ethernet'
    }
  },
  // 交换机到服务器连接
  {
    id: 'edge-3',
    source: 'node-2',
    target: 'node-4',
    sourcePort: 'bottom',
    targetPort: 'top',
    lineType: 'network line',
    lineName: '100M以太网',
    sourceInterface: 'eth2',
    targetInterface: 'eth0',
    config: {
      bandwidth: '100Mbps',
      protocol: 'Ethernet'
    }
  },
  {
    id: 'edge-4',
    source: 'node-2',
    target: 'node-5',
    sourcePort: 'bottom',
    targetPort: 'top',
    lineType: 'network line',
    lineName: '100M以太网',
    sourceInterface: 'eth3',
    targetInterface: 'eth0',
    config: {
      bandwidth: '100Mbps',
      protocol: 'Ethernet'
    }
  },
  {
    id: 'edge-5',
    source: 'node-3',
    target: 'node-6',
    sourcePort: 'bottom',
    targetPort: 'top',
    lineType: 'network line',
    lineName: '100M以太网',
    sourceInterface: 'eth2',
    targetInterface: 'eth0',
    config: {
      bandwidth: '100Mbps',
      protocol: 'Ethernet'
    }
  },
  {
    id: 'edge-6',
    source: 'node-3',
    target: 'node-7',
    sourcePort: 'bottom',
    targetPort: 'top',
    lineType: 'network line',
    lineName: '100M以太网',
    sourceInterface: 'eth3',
    targetInterface: 'eth0',
    config: {
      bandwidth: '100Mbps',
      protocol: 'Ethernet'
    }
  },
  // 服务器间连接
  {
    id: 'edge-7',
    source: 'node-4',
    target: 'node-5',
    sourcePort: 'right',
    targetPort: 'left',
    lineType: 'data line',
    lineName: '数据连接',
    sourceInterface: 'eth1',
    targetInterface: 'eth1',
    config: {
      protocol: 'TCP/IP',
      port: '3306'
    }
  },
  {
    id: 'edge-8',
    source: 'node-6',
    target: 'node-7',
    sourcePort: 'right',
    targetPort: 'left',
    lineType: 'data line',
    lineName: '缓存连接',
    sourceInterface: 'eth1',
    targetInterface: 'eth1',
    config: {
      protocol: 'Redis',
      port: '6379'
    }
  },
  // 负载均衡器连接
  {
    id: 'edge-9',
    source: 'node-12',
    target: 'node-1',
    sourcePort: 'right',
    targetPort: 'left',
    lineType: 'network line',
    lineName: '上行链路',
    sourceInterface: 'eth0',
    targetInterface: 'eth2',
    config: {
      bandwidth: '10Gbps',
      protocol: 'Ethernet'
    }
  },
  // 防火墙连接
  {
    id: 'edge-10',
    source: 'node-2',
    target: 'node-11',
    sourcePort: 'bottom',
    targetPort: 'top',
    lineType: 'security line',
    lineName: '安全连接',
    sourceInterface: 'eth4',
    targetInterface: 'eth0',
    config: {
      protocol: 'Security',
      vlan: '100'
    }
  },
  {
    id: 'edge-11',
    source: 'node-3',
    target: 'node-11',
    sourcePort: 'bottom',
    targetPort: 'top',
    lineType: 'security line',
    lineName: '安全连接',
    sourceInterface: 'eth4',
    targetInterface: 'eth1',
    config: {
      protocol: 'Security',
      vlan: '100'
    }
  },
  // 监控连接（虚拟连接，表示监控关系）
  {
    id: 'edge-12',
    source: 'node-1',
    target: 'node-8',
    sourcePort: 'right',
    targetPort: 'left',
    lineType: 'monitoring line',
    lineName: '监控连接',
    config: {
      type: 'monitoring',
      protocol: 'SNMP'
    }
  },
  {
    id: 'edge-13',
    source: 'node-1',
    target: 'node-9',
    sourcePort: 'right',
    targetPort: 'left',
    lineType: 'monitoring line',
    lineName: '监控连接',
    config: {
      type: 'monitoring',
      protocol: 'SNMP'
    }
  },
  {
    id: 'edge-14',
    source: 'node-1',
    target: 'node-10',
    sourcePort: 'right',
    targetPort: 'left',
    lineType: 'monitoring line',
    lineName: '监控连接',
    config: {
      type: 'monitoring',
      protocol: 'SNMP'
    }
  },
  // 新增连接
  {
    id: 'edge-15',
    source: 'node-6',
    target: 'node-13',
    sourcePort: 'right',
    targetPort: 'left',
    lineType: 'network line',
    lineName: '代理连接',
    sourceInterface: 'eth2',
    targetInterface: 'eth0',
    config: {
      protocol: 'HTTP',
      port: '80,443'
    }
  },
  {
    id: 'edge-16',
    source: 'node-5',
    target: 'node-14',
    sourcePort: 'right',
    targetPort: 'left',
    lineType: 'data line',
    lineName: '数据备份',
    sourceInterface: 'eth2',
    targetInterface: 'eth0',
    config: {
      protocol: 'iSCSI',
      purpose: 'backup'
    }
  },
  {
    id: 'edge-17',
    source: 'node-11',
    target: 'node-15',
    sourcePort: 'left',
    targetPort: 'right',
    lineType: 'security line',
    lineName: '容器安全',
    sourceInterface: 'eth2',
    targetInterface: 'eth0',
    config: {
      protocol: 'Security',
      policy: 'container-security'
    }
  }
];

// 模拟线条类型配置
export const mockLineTypes = [
  {
    value: 'network line',
    label: '网络线路',
    color: '#1890FF',
    style: 'solid',
    description: '物理网络连接'
  },
  {
    value: 'data line',
    label: '数据线路',
    color: '#52C41A',
    style: 'solid',
    description: '应用数据传输'
  },
  {
    value: 'security line',
    label: '安全线路',
    color: '#FA8C16',
    style: 'dashed',
    description: '安全策略连接'
  },
  {
    value: 'monitoring line',
    label: '监控线路',
    color: '#722ED1',
    style: 'dotted',
    description: '监控数据采集'
  },
  {
    value: 'backup line',
    label: '备份线路',
    color: '#13C2C2',
    style: 'dashed',
    description: '数据备份传输'
  }
];

// 模拟数据源配置
export const mockDataSources = [
  {
    value: 'prometheus',
    label: 'Prometheus',
    type: 'metrics',
    description: '时间序列监控数据'
  },
  {
    value: 'elasticsearch',
    label: 'Elasticsearch',
    type: 'logs',
    description: '日志搜索分析'
  },
  {
    value: 'grafana',
    label: 'Grafana',
    type: 'dashboard',
    description: '可视化仪表板'
  },
  {
    value: 'zabbix',
    label: 'Zabbix',
    type: 'monitoring',
    description: '基础设施监控'
  },
  {
    value: 'custom_api',
    label: '自定义API',
    type: 'api',
    description: '自定义数据接口'
  }
];

// 模拟设备类型配置
export const mockDeviceTypes = [
  {
    icon: 'cc-router',
    name: '路由器',
    category: 'network',
    description: '网络路由设备'
  },
  {
    icon: 'cc-switch2',
    name: '交换机',
    category: 'network',
    description: '网络交换设备'
  },
  {
    icon: 'cc-host',
    name: '服务器',
    category: 'compute',
    description: '计算服务器'
  },
  {
    icon: 'cc-mysql',
    name: '数据库',
    category: 'storage',
    description: '数据库服务器'
  },
  {
    icon: 'cc-firewall',
    name: '防火墙',
    category: 'security',
    description: '网络安全设备'
  },
  {
    icon: 'cc-balance',
    name: '负载均衡器',
    category: 'network',
    description: '负载均衡设备'
  },
  {
    icon: 'cc-redis',
    name: '缓存服务器',
    category: 'storage',
    description: '缓存存储服务'
  },
  {
    icon: 'cc-equipment',
    name: '监控设备',
    category: 'monitoring',
    description: '系统监控设备'
  }
];

// 拓扑模板配置 - 用于快速创建拓扑图
export const topologyTemplates = [
  {
    id: 'basic-network',
    name: '基础网络架构',
    description: '包含路由器、交换机、服务器的基础网络拓扑',
    category: 'network',
    thumbnail: '/assets/templates/basic-network.png',
    nodes: [
      // 使用 mockTopologyNodes 中的前6个节点
      ...mockTopologyNodes.slice(0, 6)
    ],
    edges: [
      // 使用对应的边连接
      ...mockTopologyEdges.slice(0, 8)
    ]
  },
  {
    id: 'monitoring-dashboard',
    name: '监控仪表板',
    description: '包含监控指标和设备状态的拓扑视图',
    category: 'monitoring',
    thumbnail: '/assets/templates/monitoring-dashboard.png',
    nodes: [
      // 核心设备 + 监控节点
      mockTopologyNodes[0], // 核心路由器
      ...mockTopologyNodes.slice(7, 10) // 监控节点
    ],
    edges: [
      // 监控连接
      ...mockTopologyEdges.slice(11, 14)
    ]
  },
  {
    id: 'full-infrastructure',
    name: '完整基础设施',
    description: '完整的IT基础设施拓扑图，包含所有设备类型',
    category: 'infrastructure',
    thumbnail: '/assets/templates/full-infrastructure.png',
    nodes: mockTopologyNodes,
    edges: mockTopologyEdges
  }
];

// 快速访问的节点类型配置
export const quickNodeTypes = [
  {
    type: 'icon',
    name: '服务器',
    icon: 'cc-host',
    category: 'compute',
    defaultConfig: {
      type: 'icon',
      logo: 'cc-host',
      logoType: 'default',
      config: {
        description: '服务器设备',
        cpu: '8核',
        memory: '16GB'
      }
    }
  },
  {
    type: 'icon',
    name: '数据库',
    icon: 'cc-mysql',
    category: 'storage',
    defaultConfig: {
      type: 'icon',
      logo: 'cc-mysql',
      logoType: 'default',
      config: {
        description: '数据库服务器',
        dbType: 'MySQL',
        version: '8.0'
      }
    }
  },
  {
    type: 'icon',
    name: '路由器',
    icon: 'cc-router',
    category: 'network',
    defaultConfig: {
      type: 'icon',
      logo: 'cc-router',
      logoType: 'default',
      config: {
        description: '网络路由器',
        model: 'Generic Router',
        ports: '24端口'
      }
    }
  },
  {
    type: 'icon',
    name: '交换机',
    icon: 'cc-switch2',
    category: 'network',
    defaultConfig: {
      type: 'icon',
      logo: 'cc-switch2',
      logoType: 'default',
      config: {
        description: '网络交换机',
        model: 'Generic Switch',
        ports: '48端口'
      }
    }
  },
  {
    type: 'single-value',
    name: 'CPU监控',
    icon: 'monitoring',
    category: 'monitoring',
    defaultConfig: {
      type: 'single-value',
      dataSource: 'prometheus',
      config: {
        query: 'cpu_usage_percent',
        unit: '%',
        threshold: 80,
        textColor: '#1890ff',
        fontSize: 12,
        backgroundColor: '#f0f8ff',
        borderColor: '#1890ff'
      }
    }
  },
  {
    type: 'single-value',
    name: '内存监控',
    icon: 'monitoring',
    category: 'monitoring',
    defaultConfig: {
      type: 'single-value',
      dataSource: 'prometheus',
      config: {
        query: 'memory_usage_percent',
        unit: '%',
        threshold: 90,
        textColor: '#52c41a',
        fontSize: 12,
        backgroundColor: '#f6ffed',
        borderColor: '#52c41a'
      }
    }
  }
];
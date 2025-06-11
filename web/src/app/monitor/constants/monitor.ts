import { useTranslation } from '@/utils/i18n';
import { useMemo } from 'react';
import { ListItem } from '@/types';
import {
  LevelMap,
  UnitMap,
  StateMap,
  ObjectIconMap,
} from '@/app/monitor/types/monitor';

const useFrequencyList = (): ListItem[] => {
  const { t } = useTranslation();
  return useMemo(
    () => [
      { label: t('common.timeSelector.off'), value: 0 },
      { label: '1m', value: 60000 },
      { label: '5m', value: 300000 },
      { label: '10m', value: 600000 },
    ],
    [t]
  );
};

const useTimeRangeList = (): ListItem[] => {
  const { t } = useTranslation();
  return useMemo(
    () => [
      { label: t('common.timeSelector.15Minutes'), value: 15 },
      { label: t('common.timeSelector.30Minutes'), value: 30 },
      { label: t('common.timeSelector.1Hour'), value: 60 },
      { label: t('common.timeSelector.6Hours'), value: 360 },
      { label: t('common.timeSelector.12Hours'), value: 720 },
      { label: t('common.timeSelector.1Day'), value: 1440 },
      { label: t('common.timeSelector.7Days'), value: 10080 },
      { label: t('common.timeSelector.30Days'), value: 43200 },
      { label: t('common.timeSelector.custom'), value: 0 },
    ],
    [t]
  );
};

const useConditionList = (): ListItem[] => {
  const { t } = useTranslation();
  return useMemo(
    () => [
      { id: '=', name: '=' },
      { id: '!=', name: '!=' },
      { id: '=~', name: t('monitor.include') },
      { id: '!~', name: t('monitor.exclude') },
    ],
    [t]
  );
};

const useStateMap = (): StateMap => {
  const { t } = useTranslation();
  return useMemo(
    () => ({
      new: t('monitor.events.new'),
      recovered: t('monitor.events.recovery'),
      closed: t('monitor.events.closed'),
    }),
    [t]
  );
};

const useLevelList = (): ListItem[] => {
  const { t } = useTranslation();
  return useMemo(
    () => [
      { label: t('monitor.events.critical'), value: 'critical' },
      { label: t('monitor.events.error'), value: 'error' },
      { label: t('monitor.events.warning'), value: 'warning' },
    ],
    [t]
  );
};

const useMethodList = (): ListItem[] => {
  const { t } = useTranslation();
  return useMemo(
    () => [
      { label: 'SUM', value: 'sum', title: t('monitor.events.sumTitle') },
      {
        label: 'SUM_OVER_TIME',
        value: 'sum_over_time',
        title: t('monitor.events.sumOverTimeTitle'),
      },
      { label: 'MAX', value: 'max', title: t('monitor.events.maxTitle') },
      {
        label: 'MAX_OVER_TIME',
        value: 'max_over_time',
        title: t('monitor.events.maxOverTimeTitle'),
      },
      { label: 'MIN', value: 'min', title: t('monitor.events.minTitle') },
      {
        label: 'MIN_OVER_TIME',
        value: 'min_over_time',
        title: t('monitor.events.minOverTimeTitle'),
      },
      { label: 'AVG', value: 'avg', title: t('monitor.events.avgTitle') },
      {
        label: 'AVG_OVER_TIME',
        value: 'avg_over_time',
        title: t('monitor.events.avgOverTimeTitle'),
      },
      { label: 'COUNT', value: 'count', title: t('monitor.events.countTitle') },
      {
        label: 'LAST_OVER_TIME',
        value: 'last_over_time',
        title: t('monitor.events.lastOverTimeTitle'),
      },
    ],
    [t]
  );
};

const useScheduleList = (): ListItem[] => {
  const { t } = useTranslation();
  return useMemo(
    () => [
      { label: t('monitor.events.minutes'), value: 'min' },
      { label: t('monitor.events.hours'), value: 'hour' },
      { label: t('monitor.events.days'), value: 'day' },
    ],
    [t]
  );
};

const useInterfaceLabelMap = (): ObjectIconMap => {
  const { t } = useTranslation();
  return useMemo(
    () => ({
      interface: t('monitor.views.interface'),
      ifOperStatus: t('monitor.views.ifOperStatus'),
      ifHighSpeed: t('monitor.views.ifHighSpeed'),
      ifInErrors: t('monitor.views.ifInErrors'),
      ifOutErrors: t('monitor.views.ifOutErrors'),
      ifInUcastPkts: t('monitor.views.ifInUcastPkts'),
      ifOutUcastPkts: t('monitor.views.ifOutUcastPkts'),
      ifInOctets: t('monitor.views.ifInOctets'),
      ifOutOctets: t('monitor.views.ifOutOctets'),
    }),
    [t]
  );
};

const LEVEL_MAP: LevelMap = {
  critical: '#F43B2C',
  error: '#D97007',
  warning: '#FFAD42',
};

const UNIT_LIST = [
  {
    label: 'Misc',
    children: [
      { label: 'none', value: 'none', unit: '' },
      {
        label: 'short',
        value: 'short',
        unit: '',
      },
      { label: 'percent (0-100)', value: 'percent', unit: '%' },
      { label: 'percent (0.0-1.0)', value: 'percentunit', unit: '%' },
    ],
  },
  {
    label: 'Data (IEC)',
    children: [
      { label: 'bits', value: 'bits', unit: 'b' },
      { label: 'bytes', value: 'bytes', unit: 'B' },
      { label: 'kibibytes', value: 'kibibytes', unit: 'KiB' },
      { label: 'mebibytes', value: 'mebibytes', unit: 'MiB' },
      { label: 'gibibytes', value: 'gibibytes', unit: 'GiB' },
      { label: 'tebibytes', value: 'tebibytes', unit: 'TiB' },
      { label: 'pebibytes', value: 'pebibytes', unit: 'PiB' },
    ],
  },
  {
    label: 'Data (Metric)',
    children: [
      { label: 'bits', value: 'decbits', unit: 'b' },
      { label: 'bytes', value: 'decbytes', unit: 'B' },
      { label: 'kibibytes', value: 'deckbytes', unit: 'KB' },
      { label: 'mebibytes', value: 'decmbytes', unit: 'MB' },
      { label: 'gibibytes', value: 'decgbytes', unit: 'GB' },
      { label: 'tebibytes', value: 'dectbytes', unit: 'TB' },
      { label: 'pebibytes', value: 'decpbytes', unit: 'PB' },
    ],
  },
  {
    label: 'Data Rate',
    children: [
      { label: 'packets/sec', value: 'pps', unit: 'p/s' },
      { label: 'bits/sec', value: 'bps', unit: 'b/s' },
      { label: 'bytes/min', value: 'bytes/min', unit: 'B/min' },
      { label: 'bytes/sec', value: 'Bps', unit: 'B/s' },
      { label: 'kilobytes/sec', value: 'KBs', unit: 'KB/s' },
      { label: 'kilobits/sec', value: 'Kbits', unit: 'Kb/s' },
      { label: 'megabytes/sec', value: 'MBs', unit: 'MB/s' },
      { label: 'megabits/sec', value: 'Mbits', unit: 'Mb/s' },
      { label: 'gigabytes/sec', value: 'GBs', unit: 'GB/s' },
      { label: 'gigabits/sec', value: 'Gbits', unit: 'Gb/s' },
      { label: 'terabytes/sec', value: 'TBs', unit: 'TB/s' },
      { label: 'terabits/sec', value: 'Tbits', unit: 'Tb/s' },
      { label: 'petabytes/sec', value: 'PBs', unit: 'PB/s' },
      { label: 'petabits/sec', value: 'Pbits', unit: 'Pb/s' },
      { label: 'milliseconds/sec', value: 'mss', unit: 'ms/s' },
    ],
  },
  {
    label: 'Temperature',
    children: [
      { label: 'Celsius (°C)', value: 'celsius', unit: '°C' },
      { label: 'Fahrenheit (°F)', value: 'fahrenheit', unit: '°F' },
      { label: 'Kelvin (K)', value: 'kelvin', unit: 'K' },
    ],
  },
  {
    label: 'Time',
    children: [
      { label: 'Hertz (1/s)', value: 'hertz', unit: 'Hz' },
      { label: 'Kilohertz (1000/s)', value: 'kilohertz', unit: 'KHz' },
      { label: 'Megahertz (1000000/s)', value: 'megahertz', unit: 'MHz' },
      { label: 'nanoseconds (ns)', value: 'ns', unit: 'ns' },
      { label: 'microseconds (µs)', value: 'µs', unit: 'µs' },
      { label: 'milliseconds (ms)', value: 'ms', unit: 'ms' },
      { label: 'centisecond (cs)', value: 'cs', unit: 'cs' },
      { label: 'seconds (s)', value: 's', unit: 's' },
      { label: 'minutes (m)', value: 'm', unit: 'min' },
      { label: 'hours (h)', value: 'h', unit: 'hour' },
      { label: 'days (d)', value: 'd', unit: 'day' },
    ],
  },
  {
    label: 'Throughput',
    children: [
      { label: 'counts/sec (cps)', value: 'cps', unit: 'cps' },
      { label: 'ops/sec (ops)', value: 'ops', unit: 'ops' },
      { label: 'requests/sec (rps)', value: 'reqps', unit: 'reqps' },
      { label: 'reads/sec (rps)', value: 'rps', unit: 'rps' },
      { label: 'writes/sec (wps)', value: 'wps', unit: 'wps' },
      { label: 'I/O ops/sec (iops)', value: 'iops', unit: 'iops' },
      { label: 'counts/min (cpm)', value: 'cpm', unit: 'cpm' },
      { label: 'ops/min (opm)', value: 'opm', unit: 'opm' },
      { label: 'reads/min (rpm)', value: 'rpm', unit: 'rpm' },
      { label: 'writes/min (wpm)', value: 'wpm', unit: 'wpm' },
    ],
  },
  {
    label: 'Other',
    children: [
      { label: 'Watts (W)', value: 'watts', unit: 'W' },
      { label: 'Volts (V)', value: 'volts', unit: 'V' },
    ],
  },
];

const useMiddleWareFields = (): ObjectIconMap => {
  const { t } = useTranslation();
  return useMemo(
    () => ({
      ClickHouse: t('monitor.intergrations.servers'),
      Consul: t('monitor.intergrations.address'),
      Zookeeper: t('monitor.intergrations.servers'),
      default: t('monitor.intergrations.url'),
      defaultDes: t('monitor.intergrations.urlDes'),
      ClickHouseDes: t('monitor.intergrations.serversDes'),
      ConsulDes: t('monitor.intergrations.addressDes'),
      ZookeeperDes: t('monitor.intergrations.serversDes'),
    }),
    [t]
  );
};

const SCHEDULE_UNIT_MAP: UnitMap = {
  minMin: 1,
  minMax: 59,
  hourMin: 1,
  hourMax: 23,
  dayMin: 1,
  dayMax: 1,
};

const PERIOD_LIST: ListItem[] = [
  { label: '1min', value: 60 },
  { label: '5min', value: 300 },
  { label: '15min', value: 900 },
  { label: '30min', value: 1800 },
  { label: '1hour', value: 3600 },
  { label: '6hour', value: 21600 },
  { label: '12hour', value: 43200 },
  { label: '24hour', value: 86400 },
];

const COMPARISON_METHOD: ListItem[] = [
  { label: '>', value: '>' },
  { label: '<', value: '<' },
  { label: '=', value: '=' },
  { label: '≠', value: '!=' },
  { label: '≥', value: '>=' },
  { label: '≤', value: '<=' },
];

const APPOINT_METRIC_IDS: string[] = [
  'cluster_pod_count',
  'cluster_node_count',
];

const TIMEOUT_UNITS: string[] = ['s'];

const OBJECT_CONFIG_MAP: any = {
  Host: {
    instance_type: 'os',
    icon: 'Host',
    dashboardDisplay: [
      {
        indexId: 'env.procs',
        displayType: 'single',
        sortIndex: 0,
        displayDimension: [],
        style: {
          height: '200px',
          width: '15%',
        },
      },
      {
        indexId: 'load1',
        displayType: 'dashboard',
        sortIndex: 1,
        displayDimension: [],
        segments: [
          { value: 1, color: '#27C274' }, // 绿色区域
          { value: 2, color: '#FF9214' }, // 黄色区域
          { value: 4, color: '#D97007' }, // 黄色区域
          { value: 20, color: '#F43B2C' }, // 红色区域
        ],
        style: {
          height: '200px',
          width: '15%',
        },
      },
      {
        indexId: 'load5',
        displayType: 'dashboard',
        sortIndex: 2,
        displayDimension: [],
        segments: [
          { value: 1.5, color: '#27C274' }, // 绿色区域
          { value: 3, color: '#FF9214' }, // 黄色区域
          { value: 5, color: '#D97007' }, // 黄色区域
          { value: 20, color: '#F43B2C' }, // 红色区域
        ],
        style: {
          height: '200px',
          width: '15%',
        },
      },
      {
        indexId: 'disk.used',
        displayType: 'table',
        sortIndex: 3,
        displayDimension: ['Device', 'Value'],
        style: {
          height: '200px',
          width: '48%',
        },
      },
      {
        indexId: 'cpu_summary.usage',
        displayType: 'lineChart',
        sortIndex: 4,
        displayDimension: ['cpu'],
        style: {
          height: '200px',
          width: '32%',
        },
      },
      {
        indexId: 'disk.is_use',
        displayType: 'lineChart',
        sortIndex: 5,
        displayDimension: ['device'],
        style: {
          height: '200px',
          width: '32%',
        },
      },
      {
        indexId: 'mem.pct_used',
        displayType: 'lineChart',
        sortIndex: 6,
        displayDimension: ['device'],
        style: {
          height: '200px',
          width: '32%',
        },
      },
      {
        indexId: 'io.util',
        displayType: 'lineChart',
        sortIndex: 7,
        displayDimension: ['device'],
        style: {
          height: '200px',
          width: '32%',
        },
      },
      {
        indexId: 'net.speed_sent',
        displayType: 'lineChart',
        sortIndex: 8,
        displayDimension: ['device'],
        style: {
          height: '200px',
          width: '32%',
        },
      },
      {
        indexId: 'net.speed_recv',
        displayType: 'lineChart',
        sortIndex: 9,
        displayDimension: ['device'],
        style: {
          height: '200px',
          width: '32%',
        },
      },
    ],
    tableDiaplay: [
      { type: 'progress', key: 'cpu_summary.usage' },
      { type: 'progress', key: 'mem.pct_used' },
      { type: 'value', key: 'load5' },
    ],
    groupIds: {
      list: ['instance_id'],
      default: ['instance_id'],
    },
    plugins: {
      Host: {
        collect_type: 'host',
        config_type: [
          'cpu',
          'disk',
          'diskio',
          'mem',
          'net',
          'processes',
          'system',
          'gpu',
        ],
        collector: 'Telegraf',
        manualCfgText: '',
      },
    },
  },
  Cluster: {
    instance_type: 'k8s',
    icon: 'ks',
    dashboardDisplay: [
      {
        indexId: 'cluster_pod_count',
        displayType: 'single',
        sortIndex: 0,
        displayDimension: [],
        style: {
          height: '200px',
          width: '15%',
        },
      },
      {
        indexId: 'cluster_node_count',
        displayType: 'single',
        sortIndex: 1,
        displayDimension: [],
        style: {
          height: '200px',
          width: '15%',
        },
      },
      {
        indexId: 'k8s_cluster',
        displayType: 'lineChart',
        sortIndex: 2,
        displayDimension: [],
        style: {
          height: '200px',
          width: '32%',
        },
      },
    ],
    tableDiaplay: [
      { type: 'value', key: 'cluster_pod_count' },
      { type: 'value', key: 'cluster_node_count' },
    ],
    groupIds: {
      list: ['instance_id'],
      default: ['instance_id'],
    },
    plugins: {
      K8S: {
        collect_type: 'k8s',
        config_type: ['k8s'],
        collector: 'Telegraf',
        manualCfgText: '',
      },
    },
  },
  Pod: {
    instance_type: '',
    icon: 'ks',
    dashboardDisplay: [
      {
        indexId: 'pod_status',
        displayType: 'single',
        sortIndex: 0,
        displayDimension: [],
        style: {
          height: '200px',
          width: '15%',
        },
      },
      {
        indexId: 'pod_cpu_utilization',
        displayType: 'lineChart',
        sortIndex: 1,
        displayDimension: [],
        style: {
          height: '200px',
          width: '32%',
        },
      },
      {
        indexId: 'pod_memory_utilization',
        displayType: 'lineChart',
        sortIndex: 2,
        displayDimension: [],
        style: {
          height: '200px',
          width: '32%',
        },
      },
      {
        indexId: 'pod_io_writes',
        displayType: 'lineChart',
        sortIndex: 3,
        displayDimension: [],
        style: {
          height: '200px',
          width: '32%',
        },
      },
      {
        indexId: 'pod_io_read',
        displayType: 'lineChart',
        sortIndex: 4,
        displayDimension: [],
        style: {
          height: '200px',
          width: '32%',
        },
      },
    ],
    tableDiaplay: [
      { type: 'enum', key: 'pod_status' },
      { type: 'progress', key: 'pod_cpu_utilization' },
      { type: 'progress', key: 'pod_memory_utilization' },
    ],
    groupIds: {
      // list: ['instance_id', 'uid'],
      // default: ['instance_id', 'uid'],
      list: ['uid'],
      default: ['uid'],
    },
    plugins: {},
  },
  Node: {
    instance_type: '',
    icon: 'ks',
    dashboardDisplay: [
      {
        indexId: 'node_status_condition',
        displayType: 'single',
        sortIndex: 0,
        displayDimension: [],
        style: {
          height: '200px',
          width: '15%',
        },
      },
      {
        indexId: 'node_cpu_load1',
        displayType: 'dashboard',
        sortIndex: 1,
        displayDimension: [],
        segments: [
          { value: 1, color: '#27C274' }, // 绿色区域
          { value: 2, color: '#FF9214' }, // 黄色区域
          { value: 4, color: '#D97007' }, // 黄色区域
          { value: 20, color: '#F43B2C' }, // 红色区域
        ],
        style: {
          height: '200px',
          width: '15%',
        },
      },
      {
        indexId: 'node_cpu_load5',
        displayType: 'dashboard',
        sortIndex: 2,
        displayDimension: [],
        segments: [
          { value: 1.5, color: '#27C274' }, // 绿色区域
          { value: 3, color: '#FF9214' }, // 黄色区域
          { value: 5, color: '#D97007' }, // 黄色区域
          { value: 20, color: '#F43B2C' }, // 红色区域
        ],
        style: {
          height: '200px',
          width: '15%',
        },
      },
      {
        indexId: 'node_cpu_utilization',
        displayType: 'lineChart',
        sortIndex: 3,
        displayDimension: [],
        style: {
          height: '200px',
          width: '32%',
        },
      },
      {
        indexId: 'node_app_memory_utilization',
        displayType: 'lineChart',
        sortIndex: 4,
        displayDimension: [],
        style: {
          height: '200px',
          width: '32%',
        },
      },
      {
        indexId: 'node_io_current',
        displayType: 'lineChart',
        sortIndex: 5,
        displayDimension: [],
        style: {
          height: '200px',
          width: '32%',
        },
      },
      {
        indexId: 'node_network_receive',
        displayType: 'lineChart',
        sortIndex: 6,
        displayDimension: [],
        style: {
          height: '200px',
          width: '32%',
        },
      },
      {
        indexId: 'node_network_transmit',
        displayType: 'lineChart',
        sortIndex: 7,
        displayDimension: [],
        style: {
          height: '200px',
          width: '32%',
        },
      },
    ],
    tableDiaplay: [
      { type: 'enum', key: 'node_status_condition' },
      { type: 'progress', key: 'node_cpu_utilization' },
      { type: 'progress', key: 'node_memory_utilization' },
    ],
    groupIds: {
      // list: ['instance_id', 'node'],
      // default: ['instance_id', 'node'],
      list: ['node'],
      default: ['node'],
    },
    plugins: {},
  },
  Website: {
    instance_type: 'web',
    icon: 'wangzhan',
    dashboardDisplay: [
      {
        indexId: 'http_success.rate',
        displayType: 'single',
        sortIndex: 0,
        displayDimension: [],
        style: {
          height: '200px',
          width: '15%',
        },
      },
      {
        indexId: 'http_duration',
        displayType: 'single',
        sortIndex: 1,
        displayDimension: [],
        style: {
          height: '200px',
          width: '15%',
        },
      },
      {
        indexId: 'http_ssl',
        displayType: 'single',
        sortIndex: 2,
        displayDimension: [],
        style: {
          height: '200px',
          width: '15%',
        },
      },
      {
        indexId: 'http_status_code',
        displayType: 'lineChart',
        sortIndex: 3,
        displayDimension: [],
        style: {
          height: '200px',
          width: '48%',
        },
      },
      {
        indexId: 'http_dns.lookup.time',
        displayType: 'lineChart',
        sortIndex: 4,
        displayDimension: [],
        style: {
          height: '200px',
          width: '48%',
        },
      },
    ],
    tableDiaplay: [
      { type: 'enum', key: 'http_success.rate' },
      { type: 'value', key: 'http_duration' },
      { type: 'enum', key: 'http_code' },
    ],
    groupIds: {
      list: ['instance_id'],
      // list: ['instance_id', 'instance_name', 'host'],
      default: ['instance_id'],
    },
    plugins: {
      Website: {
        collect_type: 'web',
        config_type: ['http_response'],
        collector: 'Telegraf',
        manualCfgText: '',
      },
    },
  },
  Ping: {
    instance_type: 'ping',
    icon: 'wangzhan',
    dashboardDisplay: [
      {
        indexId: 'ping_response_time',
        displayType: 'single',
        sortIndex: 0,
        displayDimension: [],
        style: {
          height: '200px',
          width: '15%',
        },
      },
      {
        indexId: 'ping_error_response_code',
        displayType: 'single',
        sortIndex: 1,
        displayDimension: [],
        style: {
          height: '200px',
          width: '15%',
        },
      },
    ],
    tableDiaplay: [
      { type: 'value', key: 'ping_response_time' },
      { type: 'enum', key: 'ping_error_response_code' },
    ],
    groupIds: {},
    plugins: {
      Ping: {
        collect_type: 'ping',
        config_type: ['ping'],
        collector: 'Telegraf',
        manualCfgText: '',
      },
    },
  },
  Switch: {
    instance_type: 'switch',
    icon: 'Switch',
    dashboardDisplay: [
      {
        indexId: 'sysUpTime',
        displayType: 'single',
        sortIndex: 0,
        displayDimension: [],
        style: {
          height: '200px',
          width: '15%',
        },
      },
      {
        indexId: 'iftotalInOctets',
        displayType: 'lineChart',
        sortIndex: 1,
        displayDimension: [],
        style: {
          height: '200px',
          width: '40%',
        },
      },
      {
        indexId: 'iftotalOutOctets',
        displayType: 'lineChart',
        sortIndex: 2,
        displayDimension: [],
        style: {
          height: '200px',
          width: '40%',
        },
      },
      {
        indexId: 'interfaces',
        displayType: 'multipleIndexsTable',
        sortIndex: 3,
        displayDimension: [
          'ifOperStatus',
          'ifHighSpeed',
          'ifInErrors',
          'ifOutErrors',
          'ifInUcastPkts',
          'ifOutUcastPkts',
          'ifInOctets',
          'ifOutOctets',
        ],
        style: {
          height: '400px',
          width: '100%',
        },
      },
    ],
    tableDiaplay: [
      { type: 'value', key: 'iftotalInOctets' },
      { type: 'value', key: 'iftotalOutOctets' },
      { type: 'value', key: 'sysUpTime' },
    ],
    groupIds: {
      list: ['instance_id'],
      default: ['instance_id'],
    },
    plugins: {
      'Switch SNMP General': {
        collect_type: 'snmp',
        config_type: ['switch'],
        collector: 'Telegraf',
        manualCfgText: '',
      },
    },
  },
  Router: {
    instance_type: 'router',
    icon: 'luyouqi',
    dashboardDisplay: [
      {
        indexId: 'sysUpTime',
        displayType: 'single',
        sortIndex: 0,
        displayDimension: [],
        style: {
          height: '200px',
          width: '15%',
        },
      },
      {
        indexId: 'iftotalInOctets',
        displayType: 'lineChart',
        sortIndex: 1,
        displayDimension: [],
        style: {
          height: '200px',
          width: '40%',
        },
      },
      {
        indexId: 'iftotalOutOctets',
        displayType: 'lineChart',
        sortIndex: 2,
        displayDimension: [],
        style: {
          height: '200px',
          width: '40%',
        },
      },
      {
        indexId: 'interfaces',
        displayType: 'multipleIndexsTable',
        sortIndex: 3,
        displayDimension: [
          'ifOperStatus',
          'ifHighSpeed',
          'ifInErrors',
          'ifOutErrors',
          'ifInUcastPkts',
          'ifOutUcastPkts',
          'ifInOctets',
          'ifOutOctets',
        ],
        style: {
          height: '400px',
          width: '100%',
        },
      },
    ],
    tableDiaplay: [
      { type: 'value', key: 'iftotalInOctets' },
      { type: 'value', key: 'iftotalOutOctets' },
      { type: 'value', key: 'sysUpTime' },
    ],
    groupIds: {
      list: ['instance_id'],
      default: ['instance_id'],
    },
    plugins: {
      'Router SNMP General': {
        collect_type: 'snmp',
        config_type: ['router'],
        collector: 'Telegraf',
        manualCfgText: '',
      },
    },
  },
  Firewall: {
    instance_type: 'firewall',
    icon: 'Firewall',
    dashboardDisplay: [
      {
        indexId: 'sysUpTime',
        displayType: 'single',
        sortIndex: 0,
        displayDimension: [],
        style: {
          height: '200px',
          width: '15%',
        },
      },
      {
        indexId: 'iftotalInOctets',
        displayType: 'lineChart',
        sortIndex: 1,
        displayDimension: [],
        style: {
          height: '200px',
          width: '40%',
        },
      },
      {
        indexId: 'iftotalOutOctets',
        displayType: 'lineChart',
        sortIndex: 2,
        displayDimension: [],
        style: {
          height: '200px',
          width: '40%',
        },
      },
      {
        indexId: 'interfaces',
        displayType: 'multipleIndexsTable',
        sortIndex: 3,
        displayDimension: [
          'ifOperStatus',
          'ifHighSpeed',
          'ifInErrors',
          'ifOutErrors',
          'ifInUcastPkts',
          'ifOutUcastPkts',
          'ifInOctets',
          'ifOutOctets',
        ],
        style: {
          height: '400px',
          width: '100%',
        },
      },
    ],
    tableDiaplay: [
      { type: 'value', key: 'iftotalInOctets' },
      { type: 'value', key: 'iftotalOutOctets' },
      { type: 'value', key: 'sysUpTime' },
    ],
    groupIds: {
      list: ['instance_id'],
      default: ['instance_id'],
    },
    plugins: {
      'Firewall SNMP General': {
        collect_type: 'snmp',
        config_type: ['firewall'],
        collector: 'Telegraf',
        manualCfgText: '',
      },
    },
  },
  Loadbalance: {
    instance_type: 'loadbalance',
    icon: 'Loadbalance',
    dashboardDisplay: [
      {
        indexId: 'sysUpTime',
        displayType: 'single',
        sortIndex: 0,
        displayDimension: [],
        style: {
          height: '200px',
          width: '15%',
        },
      },
      {
        indexId: 'iftotalInOctets',
        displayType: 'lineChart',
        sortIndex: 1,
        displayDimension: [],
        style: {
          height: '200px',
          width: '40%',
        },
      },
      {
        indexId: 'iftotalOutOctets',
        displayType: 'lineChart',
        sortIndex: 2,
        displayDimension: [],
        style: {
          height: '200px',
          width: '40%',
        },
      },
      {
        indexId: 'interfaces',
        displayType: 'multipleIndexsTable',
        sortIndex: 3,
        displayDimension: [
          'ifOperStatus',
          'ifHighSpeed',
          'ifInErrors',
          'ifOutErrors',
          'ifInUcastPkts',
          'ifOutUcastPkts',
          'ifInOctets',
          'ifOutOctets',
        ],
        style: {
          height: '400px',
          width: '100%',
        },
      },
    ],
    tableDiaplay: [
      { type: 'value', key: 'iftotalInOctets' },
      { type: 'value', key: 'iftotalOutOctets' },
      { type: 'value', key: 'sysUpTime' },
    ],
    groupIds: {
      list: ['instance_id'],
      default: ['instance_id'],
    },
    plugins: {
      'Loadbalance SNMP General': {
        collect_type: 'snmp',
        config_type: ['loadbalance'],
        collector: 'Telegraf',
        manualCfgText: '',
      },
    },
  },
  'Detection Device': {
    instance_type: 'detection_device',
    icon: 'shebei-shebeixinxi',
    dashboardDisplay: [
      {
        indexId: 'sysUpTime',
        displayType: 'single',
        sortIndex: 0,
        displayDimension: [],
        style: {
          height: '200px',
          width: '15%',
        },
      },
      {
        indexId: 'iftotalInOctets',
        displayType: 'lineChart',
        sortIndex: 1,
        displayDimension: [],
        style: {
          height: '200px',
          width: '40%',
        },
      },
      {
        indexId: 'iftotalOutOctets',
        displayType: 'lineChart',
        sortIndex: 2,
        displayDimension: [],
        style: {
          height: '200px',
          width: '40%',
        },
      },
      {
        indexId: 'interfaces',
        displayType: 'multipleIndexsTable',
        sortIndex: 3,
        displayDimension: [
          'ifOperStatus',
          'ifHighSpeed',
          'ifInErrors',
          'ifOutErrors',
          'ifInUcastPkts',
          'ifOutUcastPkts',
          'ifInOctets',
          'ifOutOctets',
        ],
        style: {
          height: '400px',
          width: '100%',
        },
      },
    ],
    tableDiaplay: [
      { type: 'value', key: 'iftotalInOctets' },
      { type: 'value', key: 'iftotalOutOctets' },
      { type: 'value', key: 'sysUpTime' },
    ],
    groupIds: {},
    plugins: {
      'Detection Device SNMP General': {
        collect_type: 'snmp',
        config_type: ['detection_device'],
        collector: 'Telegraf',
        manualCfgText: '',
      },
    },
  },
  'Scanning Device': {
    instance_type: 'scanning_device',
    icon: 'shebei-shebeixinxi',
    dashboardDisplay: [
      {
        indexId: 'sysUpTime',
        displayType: 'single',
        sortIndex: 0,
        displayDimension: [],
        style: {
          height: '200px',
          width: '15%',
        },
      },
      {
        indexId: 'iftotalInOctets',
        displayType: 'lineChart',
        sortIndex: 1,
        displayDimension: [],
        style: {
          height: '200px',
          width: '40%',
        },
      },
      {
        indexId: 'iftotalOutOctets',
        displayType: 'lineChart',
        sortIndex: 2,
        displayDimension: [],
        style: {
          height: '200px',
          width: '40%',
        },
      },
      {
        indexId: 'interfaces',
        displayType: 'multipleIndexsTable',
        sortIndex: 3,
        displayDimension: [
          'ifOperStatus',
          'ifHighSpeed',
          'ifInErrors',
          'ifOutErrors',
          'ifInUcastPkts',
          'ifOutUcastPkts',
          'ifInOctets',
          'ifOutOctets',
        ],
        style: {
          height: '400px',
          width: '100%',
        },
      },
    ],
    tableDiaplay: [
      { type: 'value', key: 'iftotalInOctets' },
      { type: 'value', key: 'iftotalOutOctets' },
      { type: 'value', key: 'sysUpTime' },
    ],
    groupIds: {},
    plugins: {
      'Scanning Device SNMP General': {
        collect_type: 'snmp',
        config_type: ['scanning_device'],
        collector: 'Telegraf',
        manualCfgText: '',
      },
    },
  },
  'Bastion Host': {
    instance_type: 'bastion_host',
    icon: 'shebei-shebeixinxi',
    dashboardDisplay: [
      {
        indexId: 'sysUpTime',
        displayType: 'single',
        sortIndex: 0,
        displayDimension: [],
        style: {
          height: '200px',
          width: '15%',
        },
      },
      {
        indexId: 'iftotalInOctets',
        displayType: 'lineChart',
        sortIndex: 1,
        displayDimension: [],
        style: {
          height: '200px',
          width: '40%',
        },
      },
      {
        indexId: 'iftotalOutOctets',
        displayType: 'lineChart',
        sortIndex: 2,
        displayDimension: [],
        style: {
          height: '200px',
          width: '40%',
        },
      },
      {
        indexId: 'interfaces',
        displayType: 'multipleIndexsTable',
        sortIndex: 3,
        displayDimension: [
          'ifOperStatus',
          'ifHighSpeed',
          'ifInErrors',
          'ifOutErrors',
          'ifInUcastPkts',
          'ifOutUcastPkts',
          'ifInOctets',
          'ifOutOctets',
        ],
        style: {
          height: '400px',
          width: '100%',
        },
      },
    ],
    tableDiaplay: [
      { type: 'value', key: 'iftotalInOctets' },
      { type: 'value', key: 'iftotalOutOctets' },
      { type: 'value', key: 'sysUpTime' },
    ],
    groupIds: {},
    plugins: {
      'Bastion Host SNMP General': {
        collect_type: 'snmp',
        config_type: ['bastion_host'],
        collector: 'Telegraf',
        manualCfgText: '',
      },
    },
  },
  Storage: {
    instance_type: 'storage',
    icon: 'shebei-shebeixinxi',
    dashboardDisplay: [],
    tableDiaplay: [
      { type: 'value', key: 'iftotalInOctets' },
      { type: 'value', key: 'iftotalOutOctets' },
      { type: 'value', key: 'sysUpTime' },
      { type: 'enum', key: 'ipmi_power_watts' },
      { type: 'value', key: 'ipmi_temperature_celsius' },
      { type: 'value', key: 'ipmi_voltage_volts' },
    ],
    groupIds: {},
    plugins: {
      'Storage SNMP General': {
        collect_type: 'snmp',
        config_type: ['storage'],
        collector: 'Telegraf',
        manualCfgText: '',
      },
      'Storage IPMI': {
        collect_type: 'ipmi',
        config_type: ['storage'],
        collector: 'Telegraf',
        manualCfgText: '',
      },
    },
  },
  'Hardware Server': {
    instance_type: 'hardware_server',
    icon: 'shebei-shebeixinxi',
    dashboardDisplay: [],
    tableDiaplay: [
      { type: 'value', key: 'iftotalInOctets' },
      { type: 'value', key: 'iftotalOutOctets' },
      { type: 'value', key: 'sysUpTime' },
      { type: 'enum', key: 'ipmi_power_watts' },
      { type: 'value', key: 'ipmi_temperature_celsius' },
      { type: 'value', key: 'ipmi_voltage_volts' },
    ],
    groupIds: {},
    plugins: {
      'Hardware Server SNMP General': {
        collect_type: 'snmp',
        config_type: ['hardware_server'],
        collector: 'Telegraf',
        manualCfgText: '',
      },
      'Hardware Server IPMI': {
        collect_type: 'ipmi',
        config_type: ['hardware_server'],
        collector: 'Telegraf',
        manualCfgText: '',
      },
    },
  },
  'Audit System': {
    instance_type: '',
    icon: 'AuditSystem',
    dashboardDisplay: [
      {
        indexId: 'sysUpTime',
        displayType: 'single',
        sortIndex: 0,
        displayDimension: [],
        style: {
          height: '200px',
          width: '15%',
        },
      },
      {
        indexId: 'iftotalInOctets',
        displayType: 'lineChart',
        sortIndex: 1,
        displayDimension: [],
        style: {
          height: '200px',
          width: '40%',
        },
      },
      {
        indexId: 'iftotalOutOctets',
        displayType: 'lineChart',
        sortIndex: 2,
        displayDimension: [],
        style: {
          height: '200px',
          width: '40%',
        },
      },
      {
        indexId: 'interfaces',
        displayType: 'multipleIndexsTable',
        sortIndex: 3,
        displayDimension: [
          'ifOperStatus',
          'ifHighSpeed',
          'ifInErrors',
          'ifOutErrors',
          'ifInUcastPkts',
          'ifOutUcastPkts',
          'ifInOctets',
          'ifOutOctets',
        ],
        style: {
          height: '400px',
          width: '100%',
        },
      },
    ],
    tableDiaplay: [
      { type: 'value', key: 'iftotalInOctets' },
      { type: 'value', key: 'iftotalOutOctets' },
      { type: 'value', key: 'sysUpTime' },
    ],
    groupIds: {},
    plugins: {},
  },
  'SNMP Trap': {
    instance_type: 'snmp_trap',
    icon: 'Host',
    groupIds: {},
    dashboardDisplay: [],
    tableDiaplay: [],
    plugins: {
      'SNMP Trap': {
        collect_type: 'trap',
        config_type: ['snmp_trap'],
        collector: 'Telegraf',
        manualCfgText: '',
      },
    },
  },
  Docker: {
    instance_type: 'docker',
    icon: 'Docker',
    dashboardDisplay: [],
    tableDiaplay: [{ type: 'value', key: 'docker_n_containers' }],
    groupIds: {},
    plugins: {
      Docker: {
        collect_type: 'docker',
        config_type: ['docker'],
        collector: 'Telegraf',
        manualCfgText: '',
      },
    },
  },
  'Docker Container': {
    instance_type: 'docker',
    icon: 'Docker',
    dashboardDisplay: [],
    tableDiaplay: [
      { type: 'enum', key: 'docker_container_status' },
      { type: 'value', key: 'docker_container_cpu_usage_percent' },
      { type: 'value', key: 'docker_container_mem_usage_percent' },
    ],
    groupIds: {},
    plugins: {},
  },
  RabbitMQ: {
    instance_type: 'rabbitmq',
    icon: 'rabbitmq',
    dashboardDisplay: [],
    tableDiaplay: [{ type: 'value', key: 'rabbitmq_overview_messages_ready' }],
    groupIds: {},
    plugins: {
      RabbitMQ: {
        collect_type: 'middleware',
        config_type: ['rabbitmq'],
        collector: 'Telegraf',
        manualCfgText: `[[inputs.$config_type]]
    url = "$monitor_url"
    username = "$username"
    password = "$password"
    interval = "$intervals"
    tags = { "instance_id"="$instance_id", "instance_type"="$instance_type", "collect_type"="$collect_type" }`,
      },
    },
  },
  Nginx: {
    instance_type: 'nginx',
    icon: 'nginx',
    dashboardDisplay: [],
    tableDiaplay: [
      { type: 'value', key: 'nginx_requests' },
      { type: 'value', key: 'nginx_active' },
    ],
    groupIds: {},
    plugins: {
      Nginx: {
        collect_type: 'middleware',
        config_type: ['nginx'],
        collector: 'Telegraf',
        manualCfgText: `[[inputs.$config_type]]
    urls = ["$monitor_url"]
    interval = "$intervals"
    tags = { "instance_id"="$instance_id", "instance_type"="$instance_type", "collect_type"="$collect_type" }`,
      },
    },
  },
  ActiveMQ: {
    instance_type: 'activemq',
    icon: '02_ActiveMQ',
    dashboardDisplay: [],
    tableDiaplay: [{ type: 'value', key: 'activemq_topic_consumer_count' }],
    groupIds: {},
    plugins: {
      ActiveMQ: {
        collect_type: 'middleware',
        config_type: ['activemq'],
        collector: 'Telegraf',
        manualCfgText: `[[inputs.$config_type]]
    url = "$monitor_url"
    username = "$username"
    password = "$password"
    interval = "$intervals"
    tags = { "instance_id"="$instance_id", "instance_type"="$instance_type", "collect_type"="$collect_type" }`,
      },
      'ActiveMQ-JMX': {
        collect_type: 'jmx',
        config_type: ['activemq'],
        collector: 'ActiveMQ-JMX',
        manualCfgText: `username: $username
password: $password
jmxUrl: $monitor_url
ssl: false
startDelaySeconds: 0
lowercaseOutputName: true
lowercaseOutputLabelNames: true
blacklistObjectNames:
  - "org.apache.activemq:clientId=*,*"
whitelistObjectNames:
  - "org.apache.activemq:destinationType=Queue,*"
  - "org.apache.activemq:destinationType=Topic,*"
  - "org.apache.activemq:type=Broker,brokerName=*"
  - "org.apache.activemq:type=Topic,brokerName=*"
  - "java.lang:*"

rules:
  - pattern: java.lang<type=Memory><HeapMemoryUsage>max
    name: jvm_memory_heap_usage_max
  - pattern: java.lang<type=Memory><HeapMemoryUsage>used
    name: jvm_memory_heap_usage_used
  - pattern: java.lang<type=Memory><HeapMemoryUsage>committed
    name: jvm_memory_heap_usage_committed
  - pattern: java.lang<type=Memory><HeapMemoryUsage>init
    name: jvm_memory_heap_usage_init
  - pattern: java.lang<type=Memory><NonHeapMemoryUsage>max
    name: jvm_memory_nonheap_usage_max
  - pattern: java.lang<type=Memory><NonHeapMemoryUsage>used
    name: jvm_memory_nonheap_usage_used
  - pattern: java.lang<type=Memory><NonHeapMemoryUsage>committed
    name: jvm_memory_nonheap_usage_committed
  - pattern: java.lang<type=Memory><NonHeapMemoryUsage>init
    name: jvm_memory_nonheap_usage_init

  - pattern: org.apache.activemq<type=Broker, brokerName=(\S*), destinationType=Queue, destinationName=(\S*)><>(\w+)
    name: activemq_queue_$3
    attrNameSnakeCase: true
    labels:
      destination: $2

  - pattern: org.apache.activemq<type=Broker, brokerName=(\S*), destinationType=Topic, destinationName=(\S*)><>(\w+)
    name: activemq_topic_$3
    attrNameSnakeCase: true
    labels:
      destination: $2

  - pattern: org.apache.activemq<type=Broker, brokerName=(\S*)><>CurrentConnectionsCount
    name: activemq_connections
    type: GAUGE

  - pattern: org.apache.activemq<type=Broker, brokerName=(\S*)><>Total(.*)Count
    name: activemq_$2_total
    type: COUNTER

  - pattern: org.apache.activemq<type=Broker, brokerName=(\S*)><>(.*)PercentUsage
    name: activemq_$2_usage_ratio
    type: GAUGE
    valueFactor: 0.01
`,
      },
    },
  },
  Apache: {
    instance_type: 'apache',
    icon: 'apache',
    dashboardDisplay: [],
    tableDiaplay: [
      { type: 'value', key: 'apache_uptime' },
      { type: 'value', key: 'apache_req_per_sec' },
      { type: 'progress', key: 'apache_cpu_load' },
    ],
    groupIds: {},
    plugins: {
      Apache: {
        collect_type: 'middleware',
        config_type: ['apache'],
        collector: 'Telegraf',
        manualCfgText: `[[inputs.$config_type]]
    urls = ["$monitor_url"]
    interval = "$intervals"
    tags = { "instance_id"="$instance_id", "instance_type"="$instance_type", "collect_type"="$collect_type" }`,
      },
    },
  },
  ClickHouse: {
    instance_type: 'clickhouse',
    icon: 'zhongjianjian',
    dashboardDisplay: [],
    tableDiaplay: [
      { type: 'value', key: 'clickhouse_events_query' },
      { type: 'value', key: 'clickhouse_events_inserted_rows' },
      { type: 'value', key: 'clickhouse_asynchronous_metrics_load_average1' },
    ],
    groupIds: {},
    plugins: {
      ClickHouse: {
        collect_type: 'middleware',
        config_type: ['clickhouse'],
        collector: 'Telegraf',
        manualCfgText: `[[inputs.$config_type]]
    servers = ["$monitor_url"]
    username = "default"
    interval = "$intervals"
    tags = { "instance_id"="$instance_id", "instance_type"="$instance_type", "collect_type"="$collect_type" }`,
      },
    },
  },
  Consul: {
    instance_type: 'consul',
    icon: 'zhongjianjian',
    dashboardDisplay: [],
    tableDiaplay: [
      { type: 'enum', key: 'consul_health_checks_status' },
      { type: 'value', key: 'consul_health_checks_passing' },
    ],
    groupIds: {},
    plugins: {
      Consul: {
        collect_type: 'middleware',
        config_type: ['consul'],
        collector: 'Telegraf',
        manualCfgText: `[[inputs.$config_type]]
    address = "$monitor_url"
    interval = "$intervals"
    tags = { "instance_id"="$instance_id", "instance_type"="$instance_type", "collect_type"="$collect_type" }`,
      },
    },
  },
  Zookeeper: {
    instance_type: 'zookeeper',
    icon: 'Zookeeper',
    dashboardDisplay: [],
    tableDiaplay: [
      { type: 'value', key: 'zookeeper_uptime' },
      { type: 'value', key: 'zookeeper_avg_latency' },
    ],
    groupIds: {},
    plugins: {
      Zookeeper: {
        collect_type: 'middleware',
        config_type: ['zookeeper'],
        collector: 'Telegraf',
        manualCfgText: `[[inputs.$config_type]]
    servers = ["$monitor_url"]
    timeout = "$timeouts"
    interval = "$intervals"
    tags = { "instance_id"="$instance_id", "instance_type"="$instance_type", "collect_type"="$collect_type" }`,
      },
    },
  },
  Tomcat: {
    instance_type: 'tomcat',
    icon: 'Tomcat',
    dashboardDisplay: [],
    tableDiaplay: [
      { type: 'value', key: 'tomcat_connector_request_count' },
      { type: 'value', key: 'tomcat_connector_current_threads_busy' },
      { type: 'value', key: 'tomcat_connector_error_count' },
    ],
    groupIds: {},
    plugins: {
      Tomcat: {
        collect_type: 'middleware',
        config_type: ['tomcat'],
        collector: 'Telegraf',
        manualCfgText: `[[inputs.$config_type]]
    url = "$monitor_url"
    username = "$username"
    password = "$password"
    interval = "$intervals"
    tags = { "instance_id"="$instance_id", "instance_type"="$instance_type", "collect_type"="$collect_type" }`,
      },
      'Tomcat-JMX': {
        collect_type: 'jmx',
        config_type: ['tomcat'],
        collector: 'Tomcat-JMX',
        manualCfgText: `username: $username
password: $password
jmxUrl: $monitor_url
ssl: false
lowercaseOutputLabelNames: true
lowercaseOutputName: true
whitelistObjectNames: ["java.lang:type=OperatingSystem", "Catalina:*"]
blacklistObjectNames: []
rules:
  - pattern: 'Catalina<type=Server><>serverInfo: (.+)'
    name: tomcat_serverinfo
    value: 1
    labels:
      serverInfo: "$1"
    type: COUNTER
  - pattern: 'Catalina<type=GlobalRequestProcessor, name=\"(\w+-\w+)-(\d+)\"><>(\w+):'
    name: tomcat_$3_total
    labels:
      port: "$2"
      protocol_type: "$1"
    help: Tomcat global $3
    type: COUNTER
  - pattern: 'Catalina<j2eeType=Servlet, WebModule=//([-a-zA-Z0-9+&@#/%?=~_|!:.,;]*[-a-zA-Z0-9+&@#/%=~_|]), name=([-a-zA-Z0-9+/$%~_-|!.]*), J2EEApplication=none, J2EEServer=none><>(requestCount|processingTime|errorCount):'
    name: tomcat_servlet_$3_total
    labels:
      module: "$1"
      servlet: "$2"
    help: Tomcat servlet $3 total
    type: COUNTER
  - pattern: 'Catalina<type=ThreadPool, name="(\w+-\w+)-(\d+)"><>(currentThreadCount|currentThreadsBusy|keepAliveCount|connectionCount|acceptCount|acceptorThreadCount|pollerThreadCount|maxThreads|minSpareThreads):'
    name: tomcat_threadpool_$3
    labels:
      port: "$2"
      protocol_type: "$1"
    help: Tomcat threadpool $3
    type: GAUGE
  - pattern: 'Catalina<type=Manager, host=([-a-zA-Z0-9+&@#/%?=~_|!:.,;]*[-a-zA-Z0-9+&@#/%=~_|]), context=([-a-zA-Z0-9+/$%~_-|!.]*)><>(processingTime|sessionCounter|rejectedSessions|expiredSessions):'
    name: tomcat_session_$3_total
    labels:
      context: "$2"
      host: "$1"
    help: Tomcat session $3 total
    type: COUNTER

  # tomcat6适配
  - pattern: 'Catalina<type=GlobalRequestProcessor, name=(\w+)-(\d+)><>(\w+):'
    name: tomcat_$3_total
    labels:
      port: "$2"
      protocol_type: "$1"
    help: Tomcat global $3
    type: COUNTER

  - pattern: 'Catalina<type=ThreadPool, name=(\w+)-(\d+)><>(running|currentThreadCount|currentThreadsBusy|maxThreads):'
    name: tomcat_threadpool_$3
    labels:
      port: "$2"
      protocol_type: "$1"
    help: Tomcat threadpool $3
    type: GAUGE

  - pattern: 'Catalina<type=Manager, path=/([-a-zA-Z0-9+&@#/%?=~_|!:.,;]*[-a-zA-Z0-9+&@#/%=~_|]), host=([-a-zA-Z0-9+&@#/%?=~_|!:.,;]*[-a-zA-Z0-9+&@#/%=~_|])><>(processingTime|sessionCounter|rejectedSessions|expiredSessions):'
    name: tomcat_session_$3_total
    labels:
      context: "$2"
      host: "$1"
    help: Tomcat session $3 total
    type: COUNTER`,
      },
    },
  },
  TongWeb: {
    instance_type: 'tongweb',
    icon: 'tongWeb',
    dashboardDisplay: [],
    tableDiaplay: [],
    groupIds: {},
    plugins: {
      'TongWeb6-JMX': {
        collect_type: 'jmx',
        config_type: ['tongweb6'],
        collector: 'TongWeb6-JMX',
        manualCfgText: `username: $username
password: $password
jmxUrl: $monitor_url
ssl: false
startDelaySeconds: 0
lowercaseOutputName: true
lowercaseOutputLabelNames: true
whitelistObjectNames:
  - TWNT:*
  - monitor:*


rules:
  # runtime
  - pattern: monitor<name=runtime, group=jvm><Uptime>(count)
    name: tongweb6_monitor_runtime_uptime
    help: 实例已运行时间(ms)

  # http-connector
  - pattern: monitor<name=(.+), group=http-connector><(.+)>(count)
    name: tongweb6_monitor_http_connector_$2
    labels:
      name_info: $1

  # GlobalRequestProcessor
  - pattern: TWNT<type=GlobalRequestProcessor, name=(.+)><>(requestCount|maxTime|bytesReceived|bytesSent|processingTime|errorCount)
    name: tongweb6_global_request_processor_$2
    labels:
      name_info: $1

  # Manager
  - pattern: TWNT<type=Manager, context=(.+), host=(.+)><>(activeSessions|expiredSessions|maxActive|processingTime|rejectedSessions|sessionAverageAliveTime|sessionMaxAliveTime)
    name: tongweb6_manager_$3
    labels:
      host_info: $1
      context_info: $2

  # ThreadPool
  - pattern: TWNT<type=ThreadPool, name=(.+)><>(currentThreadsBusy|currentThreadsHang|keepAliveCount)
    name: tongweb6_thread_pool_$2
    labels:
      name_info: $1`,
      },
      'TongWeb7-JMX': {
        collect_type: 'jmx',
        config_type: ['tongweb7'],
        collector: 'TongWeb7-JMX',
        manualCfgText: `username: $username
password: $password
jmxUrl: $monitor_url
ssl: false
startDelaySeconds: 0
lowercaseOutputName: true
lowercaseOutputLabelNames: true

# 白名单限制采集范围
whitelistObjectNames:
  - TONGWEB:type=Connector,port=*
  - TONGWEB:type=GlobalRequestProcessor,name=*
  - TONGWEB:type=Manager,host=*,context=*
  - TONGWEB:type=ThreadPool,name=*

rules:
  # Connector
  - pattern: TONGWEB<type=Connector, port=(.+)><>(maxPostSize|maxSavePostSize|maxParameterCount|asyncTimeout)
    name: tongweb7_Connector_$2
    labels:
      port: $1

  # GlobalRequestProcessor
  - pattern: TONGWEB<type=GlobalRequestProcessor, name=(.+)><>(requestCount|maxTime|bytesReceived|bytesSent|processingTime|errorCount)
    name: tongweb7_GlobalRequestProcessor_$2
    labels:
      name_info: $1

  # Manager
  - pattern: TONGWEB<type=Manager, host=(.+), context=(.+)><>(rejectedSessions|activeSessions|sessionMaxAliveTime|sessionAverageAliveTime|maxActive|expiredSessions)
    name: tongweb7_Manager_$3
    labels:
      host_info: $1
      context_info: $2

  # ThreadPool
  - pattern: TONGWEB<type=ThreadPool, name=(.+)><>(currentThreadsBusy|currentThreadCount|currentThreadsHang|keepAliveCount|queueSize)
    name: tongweb7_ThreadPool_$2
    labels:
      name_info: $1`,
      },
    },
  },
  JBoss: {
    instance_type: 'jboss',
    icon: 'Jboss',
    dashboardDisplay: [],
    tableDiaplay: [],
    groupIds: {},
    plugins: {
      'JBoss-JMX': {
        collect_type: 'jmx',
        config_type: ['jboss'],
        collector: 'JBoss-JMX',
        manualCfgText: `username: $username
password: $password
jmxUrl: $monitor_url
ssl: false
lowercaseOutputName: true
lowercaseOutputLabelNames: true
whitelistObjectNames:
 - "jboss.as:subsystem=messaging-activemq,server=*,jms-queue=*"
 - "jboss.as:subsystem=messaging-activemq,server=*,jms-topic=*"
 - "jboss.as:subsystem=datasources,data-source=*,statistics=*"
 - "jboss.as:subsystem=datasources,xa-data-source=*,statistics=*"
 - "jboss.as:subsystem=transactions*"
 - "jboss.as:subsystem=undertow,server=*,http-listener=*"
 - "jboss.as:subsystem=undertow,server=*,https-listener=*"
 # - "java.lang:*"
rules:
  - pattern: "^jboss.as<subsystem=messaging-activemq, server=.+, jms-(queue|topic)=(.+)><>(.+):"
    attrNameSnakeCase: true
    name: wildfly_messaging_$3
    labels:
      $1: $2

  - pattern: "^jboss.as<subsystem=datasources, (?:xa-)*data-source=(.+), statistics=(.+)><>(.+):"
    attrNameSnakeCase: true
    name: wildfly_datasource_$2_$3
    labels:
      source_name: $1

  - pattern: "^jboss.as<subsystem=transactions><>number_of_(.+):"
    attrNameSnakeCase: true
    name: wildfly_transaction_$1

  - pattern: "^jboss.as<subsystem=undertow, server=(.+), (http[s]?-listener)=(.+)><>(bytes_.+|error_count|processing_time|request_count):"
    attrNameSnakeCase: true
    name: wildfly_undertow_$4
    labels:
      server_name: $1
      listener: $3`,
      },
    },
  },
  Jetty: {
    instance_type: 'jetty',
    icon: 'jetty',
    dashboardDisplay: [],
    tableDiaplay: [],
    groupIds: {},
    plugins: {
      'Jetty-JMX': {
        collect_type: 'jmx',
        config_type: ['jetty'],
        collector: 'Jetty-JMX',
        manualCfgText: `username: $username
password: $password
jmxUrl: $monitor_url
ssl: false
startDelaySeconds: 0
lowercaseOutputName: true
lowercaseOutputLabelNames: true
rules:
  - pattern: java.lang<type=Memory><HeapMemoryUsage>max
    name: jvm_memory_heap_usage_max
  - pattern: java.lang<type=Memory><HeapMemoryUsage>used
    name: jvm_memory_heap_usage_used
  - pattern: java.lang<type=Memory><HeapMemoryUsage>committed
    name: jvm_memory_heap_usage_committed
  - pattern: java.lang<type=Memory><HeapMemoryUsage>init
    name: jvm_memory_heap_usage_init
  - pattern: java.lang<type=Memory><NonHeapMemoryUsage>max
    name: jvm_memory_nonheap_usage_max
  - pattern: java.lang<type=Memory><NonHeapMemoryUsage>used
    name: jvm_memory_nonheap_usage_used
  - pattern: java.lang<type=Memory><NonHeapMemoryUsage>committed
    name: jvm_memory_nonheap_usage_committed
  - pattern: java.lang<type=Memory><NonHeapMemoryUsage>init
    name: jvm_memory_nonheap_usage_init
  - pattern: org.eclipse.jetty.io<type=arraybytebufferpool, id=0><>heapMemory
    name: jetty_bufferpool_heapMemory
  - pattern: org.eclipse.jetty.deploy<type=deploymentmanager, id=(.+)><>stopTimeout
    name: jetty_deploymentmanager_stopTimeout
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.deploy.providers<type=webappprovider, id=(.+)><>stopTimeout
    name: jetty_webappprovider_stopTimeout
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.io<type=arraybytebufferpool, id=(.+)><>heapMemory
    name: jetty_arraybufferpool_heapMemory
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.io<type=arraybytebufferpool, id=(.+)><>directByteBufferCount
    name: jetty_arraybufferpool_directByteBufferCount
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.io<type=arraybytebufferpool, id=(.+)><>directMemory
    name: jetty_arraybufferpool_directMemory
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.io<type=arraybytebufferpool, id=(.+)><>heapByteBufferCount
    name: jetty_arraybufferpool_heapByteBufferCount
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.io<context=(.+), type=managedselector, id=(.+)><>stopTimeout
    name: jetty_managedselector_stopTimeout
    labels:
      context: "$1"
      id:  "$2"
  - pattern: org.eclipse.jetty.io<context=(.+), type=managedselector, id=(.+)><>averageSelectedKeys
    name: jetty_managedselector_averageSelectedKeys
    labels:
      context: "$1"
      id: "$2"
  - pattern: org.eclipse.jetty.io<context=(.+), type=managedselector, id=(.+)><>maxSelectedKeys
    name: jetty_managedselector_maxSelectedKeys
    labels:
      context: "$1"
      id: "$2"
  - pattern: org.eclipse.jetty.io<context=(.+), type=managedselector, id=(.+)><>selectCount
    name: jetty_managedselector_selectCount
    labels:
      context: "$1"
      id: "$2"
  - pattern: org.eclipse.jetty.io<context=(.+), type=managedselector, id=(.+)><>totalKeys
    name: jetty_managedselector_totalKeys
    labels:
      context: "$1"
      id: "$2"
  - pattern: org.eclipse.jetty.server<context=(.+), type=httpconfiguration, id=(.+)><>responseHeaderSize
    name: jetty_httpconfiguration_responseHeaderSize
    labels:
      context: "$1"
      id: "$2"
  - pattern: org.eclipse.jetty.server<context=(.+), type=httpconfiguration, id=(.+)><>requestHeaderSize
    name: jetty_httpconfiguration_requestHeaderSize
    labels:
      context: "$1"
      id: "$2"
  - pattern: org.eclipse.jetty.server<context=(.+), type=httpconfiguration, id=(.+)><>maxErrorDispatches
    name: jetty_httpconfiguration_maxErrorDispatches
    labels:
      context: "$1"
      id: "$2"
  - pattern: org.eclipse.jetty.server<context=(.+), type=httpconfiguration, id=(.+)><>idleTimeout
    name: jetty_httpconfiguration_idleTimeout
    labels:
      context: "$1"
      id: "$2"
  - pattern: org.eclipse.jetty.server<context=(.+), type=httpconfiguration, id=(.+)><>outputBufferSize
    name: jetty_httpconfiguration_outputBufferSize
    labels:
      context: "$1"
      id: "$2"
  - pattern: org.eclipse.jetty.server<context=(.+), type=httpconfiguration, id=(.+)><>headerCacheSize
    name: jetty_httpconfiguration_headerCacheSize
    labels:
      context: "$1"
      id: "$2"
  - pattern: org.eclipse.jetty.server<context=(.+), type=httpconfiguration, id=(.+)><>minRequestDataRate
    name: jetty_httpconfiguration_minRequestDataRate
    labels:
      context: "$1"
      id: "$2"
  - pattern: org.eclipse.jetty.server<context=(.+), type=httpconfiguration, id=(.+)><>outputAggregationSize
    name: jetty_httpconfiguration_outputAggregationSize
    labels:
      context: "$1"
      id: "$2"
  - pattern: org.eclipse.jetty.server<context=(.+), type=httpconfiguration, id=(.+)><>blockingTimeout
    name: jetty_httpconfiguration_blockingTimeout
    labels:
      context: "$1"
      id: "$2"
  - pattern: org.eclipse.jetty.server<context=(.+), type=httpconfiguration, id=(.+)><>minResponseDataRate
    name: jetty_httpconfiguration_minResponseDataRate
    labels:
      context: "$1"
      id: "$2"
  - pattern: org.eclipse.jetty.server<context=(.+), type=serverconnector, id=(.+)><>stopTimeout
    name: jetty_serverconnector_stopTimeout
    labels:
      context: "$1"
      id: "$2"
  - pattern: org.eclipse.jetty.server<context=(.+), type=serverconnector, id=(.+)><>acceptQueueSize
    name: jetty_serverconnector_acceptQueueSize
    labels:
      context: "$1"
      id: "$2"
  - pattern: org.eclipse.jetty.server<context=(.+), type=serverconnector, id=(.+)><>acceptedReceiveBufferSize
    name: jetty_serverconnector_acceptedReceiveBufferSize
    labels:
      context: "$1"
      id: "$2"
  - pattern: org.eclipse.jetty.server<context=(.+), type=serverconnector, id=(.+)><>acceptedSendBufferSize
    name: jetty_serverconnector_acceptedSendBufferSize
    labels:
      context: "$1"
      id: "$2"
  - pattern: org.eclipse.jetty.server<context=(.+), type=serverconnector, id=(.+)><>idleTimeout
    name: jetty_serverconnector_idleTimeout
    labels:
      context: "$1"
      id: "$2"
  - pattern: org.eclipse.jetty.server<context=(.+), type=serverconnector$serverconnectormanager, id=(.+)><>selectorCount
    name: jetty_serverconnector_selectorCount
    labels:
      context: "$1"
      id: "$2"
  - pattern: org.eclipse.jetty.server<context=(.+), type=serverconnector$serverconnectormanager, id=(.+)><>connectTimeout
    name: jetty_serverconnector_connectTimeout
    labels:
      context: "$1"
      id: "$2"
  - pattern: org.eclipse.jetty.util.thread<type=queuedthreadpool, id=(.+)><>threadsPriority
    name: jetty_queuedthreadpool_threadsPriority
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.util.thread<type=queuedthreadpool, id=(.+)><>queueSize
    name: jetty_queuedthreadpool_queueSize
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.util.thread<type=queuedthreadpool, id=(.+)><>availableReservedThreads
    name: jetty_queuedthreadpool_availableReservedThreads
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.util.thread<type=queuedthreadpool, id=(.+)><>stopTimeout
    name: jetty_queuedthreadpool_stopTimeout
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.util.thread<type=queuedthreadpool, id=(.+)><>utilizedThreads
    name: jetty_queuedthreadpool_utilizedThreads
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.util.thread<type=queuedthreadpool, id=(.+)><>utilizationRate
    name: jetty_queuedthreadpool_utilizationRate
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.util.thread<type=queuedthreadpool, id=(.+)><>minThreads
    name: jetty_queuedthreadpool_minThreads
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.util.thread<type=queuedthreadpool, id=(.+)><>maxReservedThreads
    name: jetty_queuedthreadpool_maxReservedThreads
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.util.thread<type=queuedthreadpool, id=(.+)><>threads
    name: jetty_queuedthreadpool_threads
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.util.thread<type=queuedthreadpool, id=(.+)><>reservedThreads
    name: jetty_queuedthreadpool_reservedThreads
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.util.thread<type=queuedthreadpool, id=(.+)><>readyThreads
    name: jetty_queuedthreadpool_readyThreads
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.util.thread<type=queuedthreadpool, id=(.+)><>leasedThreads
    name: jetty_queuedthreadpool_leasedThreads
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.util.thread<type=queuedthreadpool, id=(.+)><>maxAvailableThreads
    name: jetty_queuedthreadpool_maxAvailableThreads
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.util.thread<type=queuedthreadpool, id=(.+)><>busyThreads
    name: jetty_queuedthreadpool_busyThreads
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.util.thread<type=queuedthreadpool, id=(.+)><>lowThreadsThreshold
    name: jetty_queuedthreadpool_lowThreadsThreshold
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.util.thread<type=queuedthreadpool, id=(.+)><>idleTimeout
    name: jetty_queuedthreadpool_idleTimeout
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.util.thread<type=queuedthreadpool, id=(.+)><>idleThreads
    name: jetty_queuedthreadpool_idleThreads
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.util.thread<type=queuedthreadpool, id=(.+)><>maxThreads
    name: jetty_queuedthreadpool_maxThreads
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.util.thread<type=queuedthreadpool, id=(.+)><>maxLeasedThreads
    name: jetty_queuedthreadpool_maxLeasedThreads
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.util.thread<type=reservedthreadexecutor, id=(.+)><>pending
    name: jetty_reservedthreadexecutor_pending
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.util.thread<type=reservedthreadexecutor, id=(.+)><>available
    name: jetty_reservedthreadexecutor_available
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.util.thread<type=reservedthreadexecutor, id=(.+)><>idleTimeoutMs
    name: jetty_reservedthreadexecutor_idleTimeoutMs
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.util.thread<type=reservedthreadexecutor, id=(.+)><>capacity
    name: jetty_reservedthreadexecutor_capacity
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.util.thread<type=threadpoolbudget, id=(.+)><>leasedThreads
    name: jetty_threadpoolbudget_leasedThreads
    labels:
      id: "$1"
  - pattern: org.eclipse.jetty.util.thread.strategy<context=(.+), type=eatwhatyoukill, id=(.+)><>stopTimeout
    name: jetty_eatwhatyoukill_stopTimeout
    labels:
      context: "$1"
      id: "$2"
  - pattern: org.eclipse.jetty.util.thread.strategy<context=(.+), type=eatwhatyoukill, id=(.+)><>pCTasksConsumed
    name: jetty_eatwhatyoukill_pCTasksConsumed
    labels:
      context: "$1"
      id: "$2"
  - pattern: org.eclipse.jetty.util.thread.strategy<context=(.+), type=eatwhatyoukill, id=(.+)><>pECTasksExecuted
    name: jetty_eatwhatyoukill_pECTasksExecuted
    labels:
      context: "$1"
      id: "$2"
  - pattern: org.eclipse.jetty.util.thread.strategy<context=(.+), type=eatwhatyoukill, id=(.+)><>ePCTasksConsumed
    name: jetty_eatwhatyoukill_ePCTasksConsumed
    labels:
      context: "$1"
      id: "$2"
  - pattern: org.eclipse.jetty.util.thread.strategy<context=(.+), type=eatwhatyoukill, id=(.+)><>pICTasksExecuted
    name: jetty_eatwhatyoukill_pICTasksExecuted
    labels:
      context: "$1"
      id: "$2"`,
      },
    },
  },
  WebLogic: {
    instance_type: 'weblogic',
    icon: 'weblogic',
    dashboardDisplay: [],
    tableDiaplay: [],
    groupIds: {},
    plugins: {
      'WebLogic-JMX': {
        collect_type: 'jmx',
        config_type: ['weblogic'],
        collector: 'WebLogic-JMX',
        manualCfgText: `username: $username
password: $password
jmxUrl: $monitor_url
ssl: false
startDelaySeconds: 0
lowercaseOutputName: true
lowercaseOutputLabelNames: true
whitelistObjectNames:
  - "com.bea:Name=*,Type=ServerRuntime"
  - "com.bea:ServerRuntime=*,Type=ApplicationRuntime,*"
  - "com.bea:ServerRuntime=*,Type=JDBCDataSourceRuntime,*"
  - "com.bea:ServerRuntime=*,Type=JMSDestinationRuntime,*"
  - "com.bea:ServerRuntime=*,Type=JDBCStoreRuntime,*"
  - "com.bea:ServerRuntime=*,Type=FileStoreRuntime,*"
  - "com.bea:ServerRuntime=*,Type=SAFRemoteEndpointRuntime,*"
  - "com.bea:ServerRuntime=*,Type=ThreadPoolRuntime,*"
  - "com.bea:ServerRuntime=*,Type=JMSRuntime,*"
  - "com.bea:ServerRuntime=*,Type=SAFRuntime,*"
  - "com.bea:ServerRuntime=*,Type=WorkManagerRuntime,*"
  - "com.bea:ServerRuntime=*,Type=MessagingBridgeRuntime,*"
  - "com.bea:ServerRuntime=*,Type=PersistentStoreRuntime,*"
  - "com.bea:ServerRuntime=*,Type=WebServerRuntime,*"


rules:
  # ex: com.bea<ServerRuntime=AdminServer, Name=default, ApplicationRuntime=moduleJMS, Type=WorkManagerRuntime><>CompletedRequests
  - pattern: "^com.bea<ServerRuntime=(.+), Name=(.+), (.+)Runtime=(.*), Type=(.+)Runtime><>(.+):"
    name: weblogic_$3_$5_$6
    attrNameSnakeCase: true
    labels:
      runtime: $1
      name: $2
      application: $4

  # ex: com.bea<ServerRuntime=AdminServer, Name=dsName, Type=JDBCDataSourceRuntime><>Metric
  - pattern: "^com.bea<ServerRuntime=(.+), Name=(.+), Type=(.+)Runtime><>(.+):"
    name: weblogic_$3_$4
    attrNameSnakeCase: true
    labels:
      runtime: $1
      name: $2

  # ex: com.bea<ServerRuntime=AdminServer, Name=bea_wls_cluster_internal, Type=ApplicationRuntime><OverallHealthStateJMX>IsCritical
  - pattern: "^com.bea<ServerRuntime=(.+), Name=(.+), Type=(.+)Runtime><(.+)>(.+):"
    name: weblogic_$3_$4_$5
    attrNameSnakeCase: true
    labels:
      runtime: $1
      name: $2`,
      },
    },
  },
  MongoDB: {
    instance_type: 'mongodb',
    icon: 'mongodb',
    dashboardDisplay: [],
    tableDiaplay: [
      { type: 'value', key: 'mongodb_connections_current' },
      { type: 'value', key: 'mongodb_latency_commands' },
      { type: 'value', key: 'mongodb_resident_megabytes' },
    ],
    groupIds: {},
    plugins: {
      MongoDB: {
        collect_type: 'database',
        config_type: ['mongodb'],
        collector: 'Telegraf',
        manualCfgText: `[[inputs.$config_type]]
    servers = ["mongodb://$host:$port/?connect=direct"]
    interval = "$intervals"
    tags = { "instance_id"="$instance_id", "instance_type"="$instance_type", "collect_type"="$collect_type" }`,
      },
    },
  },
  Mysql: {
    instance_type: 'mysql',
    icon: 'mysql1',
    dashboardDisplay: [],
    tableDiaplay: [
      { type: 'value', key: 'mysql_bytes_received' },
      { type: 'value', key: 'mysql_bytes_sent' },
      { type: 'value', key: 'mysql_connections_total' },
    ],
    groupIds: {},
    plugins: {
      Mysql: {
        collect_type: 'database',
        config_type: ['mysql'],
        collector: 'Telegraf',
        manualCfgText: `[[inputs.$config_type]]
    servers = ["$username:$password@tcp($host:$port)/?tls=false"]
    metric_version = 2
    interval = "$intervals"
    tags = { "instance_id"="$instance_id", "instance_type"="$instance_type", "collect_type"="$collect_type" }`,
      },
    },
  },
  Redis: {
    instance_type: 'redis',
    icon: 'Redis',
    dashboardDisplay: [],
    tableDiaplay: [
      { type: 'value', key: 'redis_used_memory' },
      { type: 'value', key: 'redis_instantaneous_ops_per_sec' },
    ],
    groupIds: {},
    plugins: {
      Redis: {
        collect_type: 'database',
        config_type: ['redis'],
        collector: 'Telegraf',
        manualCfgText: `[[inputs.$config_type]]
    servers = ["tcp://$host:$port"]
    username = "$username"
    password = "$password" 
    interval = "$intervals"
    tags = { "instance_id"="$instance_id", "instance_type"="$instance_type", "collect_type"="$collect_type" }`,
      },
    },
  },
  Oracle: {
    instance_type: 'oracle',
    icon: 'oracle',
    dashboardDisplay: [],
    tableDiaplay: [],
    groupIds: {},
    plugins: {
      'Oracle-Exporter': {
        collect_type: 'exporter',
        config_type: ['oracle'],
        collector: 'Oracle-Exporter',
        manualCfgText: '--',
      },
    },
  },
  Postgres: {
    instance_type: 'postgres',
    icon: 'postgres',
    dashboardDisplay: [],
    tableDiaplay: [
      { type: 'value', key: 'postgresql_active_time' },
      { type: 'value', key: 'postgresql_blks_hit' },
    ],
    groupIds: {},
    plugins: {
      Postgres: {
        collect_type: 'database',
        config_type: ['postgres'],
        collector: 'Telegraf',
        manualCfgText: `[[inputs.$config_type]]
    address = "host=$host port=$port user=$username password=$password sslmode=disable"
    ignored_databases = ["template0", "template1"]
    interval = "$intervals"
    tags = { "instance_id"="$instance_id", "instance_type"="$instance_type", "collect_type"="$collect_type" }`,
      },
    },
  },
  ElasticSearch: {
    instance_type: 'elasticsearch',
    icon: 'elasticsearch-Elasticsearch',
    dashboardDisplay: [],
    tableDiaplay: [
      { type: 'value', key: 'elasticsearch_fs_total_available_in_bytes' },
      { type: 'value', key: 'elasticsearch_http_current_open' },
      { type: 'value', key: 'elasticsearch_indices_docs_count' },
    ],
    groupIds: {},
    plugins: {
      ElasticSearch: {
        collect_type: 'database',
        config_type: ['elasticsearch'],
        collector: 'Telegraf',
        manualCfgText: `[[inputs.$config_type]]
    servers = ["$server"]
    username = "$username"
    password = "$password"
    interval = "$intervals"
    tags = { "instance_id"="$instance_id", "instance_type"="$instance_type", "collect_type"="$collect_type" }`,
      },
    },
  },
  vCenter: {
    instance_type: 'vmware',
    icon: 'vmware',
    dashboardDisplay: [],
    tableDiaplay: [
      { type: 'value', key: 'vmware_esxi_count' },
      { type: 'value', key: 'vmware_datastore_count' },
      { type: 'value', key: 'vmware_vm_count' },
    ],
    groupIds: {},
    plugins: {
      VMWare: {
        collect_type: 'http',
        config_type: ['prometheus'],
        collector: 'Telegraf',
        manualCfgText: `[[inputs.prometheus]]
    urls = ["\${STARGAZER_URL}/api/monitor/vmware/metrics"]
    interval = "$intervals"
    timeout = "30s"
    response_timeout = "30s"
    http_headers = { "username"="$username", "password"="$password", "host"="$host" }
    [inputs.prometheus.tags]
        instance_id = "$instance_id"
        instance_type = "$instance_type"
        collect_type = "http"
        config_type = "prometheus"`,
      },
    },
  },
  ESXI: {
    instance_type: 'vmware',
    icon: 'vmware',
    dashboardDisplay: [],
    tableDiaplay: [
      { type: 'value', key: 'esxi_cpu_usage_average_gauge' },
      { type: 'value', key: 'esxi_mem_usage_average_gauge' },
      { type: 'value', key: 'esxi_disk_read_average_gauge' },
    ],
    groupIds: {},
    plugins: {},
  },
  DataStorage: {
    instance_type: 'vmware',
    icon: 'vmware',
    dashboardDisplay: [],
    tableDiaplay: [
      { type: 'value', key: 'data_storage_disk_used_average_gauge' },
      { type: 'enum', key: 'data_storage_store_accessible_gauge' },
    ],
    groupIds: {},
    plugins: {},
  },
  VM: {
    instance_type: 'vmware',
    icon: 'vmware',
    dashboardDisplay: [],
    tableDiaplay: [
      { type: 'value', key: 'vm_cpu_usage_average_gauge' },
      { type: 'value', key: 'vm_mem_usage_average_gauge' },
      { type: 'value', key: 'vm_disk_io_usage_gauge' },
    ],
    groupIds: {},
    plugins: {},
  },
  JVM: {
    instance_type: 'jvm',
    icon: 'Host',
    dashboardDisplay: [],
    tableDiaplay: [
      { type: 'enum', key: 'jmx_scrape_error_gauge' },
      { type: 'value', key: 'jvm_memory_usage_used_value' },
      { type: 'value', key: 'jvm_memory_usage_max_value' },
      { type: 'value', key: 'jvm_os_memory_physical_free_value' },
      { type: 'value', key: 'jvm_gc_collectiontime_seconds_value' },
    ],
    groupIds: {},
    plugins: {
      JVM: {
        collect_type: 'jmx',
        config_type: ['jvm'],
        collector: 'JMX-JVM',
        manualCfgText: `username: $username
password: $password
jmxUrl: $monitor_url
ssl: false
startDelaySeconds: 0
lowercaseOutputName: true
lowercaseOutputLabelNames: true

# 白名单限制采集范围
whitelistObjectNames:
  - java.lang:type=Memory
  - java.lang:type=Threading
  - java.lang:type=OperatingSystem
  - java.nio:type=BufferPool,name=*
  - java.lang:type=GarbageCollector,name=*
  - java.lang:type=MemoryPool,name=*

rules:
  # 内存相关指标
  - pattern: java.lang<type=Memory><(\w+)MemoryUsage>(\w+)
    name: jvm_memory_usage_$2
    labels:
      type: $1

  # 线程相关指标
  - pattern: java.lang<type=Threading><>ThreadCount
    name: jvm_threads_count
  - pattern: java.lang<type=Threading><>DaemonThreadCount
    name: jvm_threads_daemon_count
  - pattern: java.lang<type=Threading><>PeakThreadCount
    name: jvm_threads_peak_count
  - pattern: java.lang<type=Threading><>TotalStartedThreadCount
    name: jvm_threads_total_started_count
  - pattern: java.lang<type=Threading><>CurrentThreadUserTime
    name: jvm_threads_current_user_time
    valueFactor: 0.001

  # 操作系统指标
  - pattern: java.lang<type=OperatingSystem><>FreePhysicalMemorySize
    name: jvm_os_memory_physical_free
  - pattern: java.lang<type=OperatingSystem><>TotalPhysicalMemorySize
    name: jvm_os_memory_physical_total
  - pattern: java.lang<type=OperatingSystem><>FreeSwapSpaceSize
    name: jvm_os_memory_swap_free
  - pattern: java.lang<type=OperatingSystem><>TotalSwapSpaceSize
    name: jvm_os_memory_swap_total
  - pattern: java.lang<type=OperatingSystem><>CommittedVirtualMemorySize
    name: jvm_os_memory_committed_virtual
  - pattern: java.lang<type=OperatingSystem><>AvailableProcessors
    name: jvm_os_available_processors
  - pattern: java.lang<type=OperatingSystem><>ProcessCpuTime
    name: jvm_os_processcputime_seconds
    valueFactor: 0.000000001

  # BufferPool 指标
  - pattern: java.nio<type=BufferPool, name=(.+)><>Count
    name: jvm_bufferpool_count
    labels:
      type: $1
  - pattern: java.nio<type=BufferPool, name=(.+)><>MemoryUsed
    name: jvm_bufferpool_memoryused
    labels:
      type: $1
  - pattern: java.nio<type=BufferPool, name=(.+)><>TotalCapacity
    name: jvm_bufferpool_totalcapacity
    labels:
      type: $1

  # GC 指标
  - pattern: java.lang<type=GarbageCollector, name=(.+)><>CollectionTime
    name: jvm_gc_collectiontime_seconds
    valueFactor: 0.001
    labels:
      type: $1
  - pattern: java.lang<type=GarbageCollector, name=(.+)><>CollectionCount
    name: jvm_gc_collectioncount
    labels:
      type: $1

  # MemoryPool 指标
  - pattern: java.lang<type=MemoryPool, name=(.+)><Usage>(\w+)
    name: jvm_memorypool_usage_$2
    labels:
      type: $1`,
      },
    },
  },
  TCP: {
    instance_type: 'qcloud',
    icon: 'zonghenengyuanfuwupingtaikuangjiaicon-',
    dashboardDisplay: [],
    tableDiaplay: [
      { type: 'value', key: 'cvm_CPU_Usage' },
      { type: 'value', key: 'cvm_MemUsage' },
      { type: 'value', key: 'cvm_LanOuttraffic' },
      { type: 'value', key: 'cvm_WanOuttraffic' },
    ],
    groupIds: {},
    plugins: {
      'Tencent Cloud': {
        collect_type: 'http',
        config_type: ['prometheus'],
        collector: 'Telegraf',
        manualCfgText: `[[inputs.prometheus]]
    urls = ["\${STARGAZER_URL}/api/monitor/qcloud/metrics"]
    interval = "$intervals"
    timeout = "30s"
    response_timeout = "30s"
    http_headers = { "username"="$username", "password"="$password" }
    [inputs.prometheus.tags]
        instance_id = "$instance_id"
        instance_type = "$instance_type"
        collect_type = "http"
        config_type = "prometheus"`,
      },
    },
  },
  CVM: {
    instance_type: 'qcloud',
    icon: 'zonghenengyuanfuwupingtaikuangjiaicon-',
    dashboardDisplay: [],
    tableDiaplay: [
      { type: 'value', key: 'cvm_CPU_Usage' },
      { type: 'value', key: 'cvm_MemUsage' },
      { type: 'value', key: 'cvm_CvmDiskUsage' },
    ],
    groupIds: {},
    plugins: {},
  },
};

const NODE_STATUS_MAP: ObjectIconMap = {
  normal: 'green',
  inactive: 'yellow',
  unavailable: 'gray',
};

const INIT_VIEW_MODAL_FORM = {
  instance_id_values: [],
  instance_name: '',
  instance_id: '',
  instance_id_keys: [],
  dimensions: [],
  title: '',
};

const STRATEGY_TEMPLATES = [
  'Host',
  'Ping',
  'Website',
  'Switch',
  'Router',
  'Firewall',
  'Loadbalance',
  'Detection Device',
  'Scanning Device',
  'Bastion Host',
  'Storage',
  'Hardware Server',
];

const NEED_TAGS_ENTRY_OBJECTS = ['Docker', 'Cluster', 'vCenter', 'TCP'];

const DERIVATIVE_OBJECTS = [
  'Docker Container',
  'ESXI',
  'VM',
  'DataStorage',
  'Pod',
  'Node',
  'CVM',
];

const OBJECT_DEFAULT_ICON: string = 'ziyuan';

export {
  UNIT_LIST,
  PERIOD_LIST,
  COMPARISON_METHOD,
  LEVEL_MAP,
  SCHEDULE_UNIT_MAP,
  APPOINT_METRIC_IDS,
  TIMEOUT_UNITS,
  NODE_STATUS_MAP,
  INIT_VIEW_MODAL_FORM,
  OBJECT_CONFIG_MAP,
  STRATEGY_TEMPLATES,
  NEED_TAGS_ENTRY_OBJECTS,
  DERIVATIVE_OBJECTS,
  OBJECT_DEFAULT_ICON,
  useMiddleWareFields,
  useInterfaceLabelMap,
  useScheduleList,
  useMethodList,
  useLevelList,
  useConditionList,
  useTimeRangeList,
  useFrequencyList,
  useStateMap,
};

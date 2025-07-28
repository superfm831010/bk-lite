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

const CONNECTION_LIFETIME_UNITS: string[] = ['m'];

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
  CONNECTION_LIFETIME_UNITS,
  NODE_STATUS_MAP,
  INIT_VIEW_MODAL_FORM,
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

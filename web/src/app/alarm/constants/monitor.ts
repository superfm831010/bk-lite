import { useTranslation } from '@/utils/i18n';
import { useMemo } from 'react';
import { ListItem } from '@/types';
import { LevelMap, StateMap } from '@/app/alarm/types/monitor';

const useStateMap = (): StateMap => {
  const { t } = useTranslation();
  return useMemo(
    () => ({
      new: t('monitor.events.new'),
      recovered: t('monitor.events.recovery'),
      closed: t('monitor.events.closed'),
      pending: t('monitor.events.pending'),
      processing: t('monitor.events.processing'),
      unassigned: t('monitor.events.unassigned'),
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

const LEVEL_MAP: LevelMap = {
  critical: '#F43B2C',
  error: '#D97007',
  warning: '#FFAD42',
};

const APPOINT_METRIC_IDS: string[] = [
  'cluster_pod_count',
  'cluster_node_count',
];

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
      { label: 'kibibytes', value: 'kbytes', unit: 'KiB' },
      { label: 'mebibytes', value: 'mbytes', unit: 'MiB' },
      { label: 'gibibytes', value: 'gbytes', unit: 'GiB' },
      { label: 'tebibytes', value: 'tbytes', unit: 'TiB' },
      { label: 'pebibytes', value: 'pbytes', unit: 'PiB' },
    ],
  },
  {
    label: 'Data (Metric)',
    children: [
      { label: 'bits', value: 'decbits', unit: 'b' },
      { label: 'bytes', value: 'decbytes', unit: 'B' },
      { label: 'kilobytes', value: 'deckbytes', unit: 'KB' },
      { label: 'megabytes', value: 'decmbytes', unit: 'MB' },
      { label: 'gigabytes', value: 'decgbytes', unit: 'GB' },
      { label: 'terabytes', value: 'dectbytes', unit: 'TB' },
      { label: 'petabytes', value: 'decpbytes', unit: 'PB' },
    ],
  },
  {
    label: 'Data Rate',
    children: [
      { label: 'packets/sec', value: 'pps', unit: 'p/s' },
      { label: 'bits/sec', value: 'bps', unit: 'b/s' },
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
      { label: 'Hertz (1/s)', value: 'hertz', unit: 'hz' },
      { label: 'nanoseconds (ns)', value: 'ns', unit: 'ns' },
      { label: 'microseconds (µs)', value: 'µs', unit: 'µs' },
      { label: 'milliseconds (ms)', value: 'ms', unit: 'ms' },
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
export { LEVEL_MAP, UNIT_LIST, APPOINT_METRIC_IDS, useLevelList, useStateMap };

'use client';

import React, { useEffect, useState, useRef } from 'react';
import Icon from '@/components/icon';
import useApiClient from '@/utils/request';
import dayjs, { Dayjs } from 'dayjs';
import CustomTable from '@/components/custom-table';
import TimeSelector from '@/components/time-selector';
import Permission from '@/components/permission';
import StackedBarChart from '@/app/alarm/components/stackedBarChart';
import AlertDetail from './components/alertDetail';
import alertStyle from './index.module.scss';
import UserAvatar from '@/app/cmdb/components/userAvatar';
import AlarmFilters from '@/app/alarm/components/alarmFilters/page';
import { useAlarmApi } from '@/app/alarm/api/alarms';
import { useTranslation } from '@/utils/i18n';
import { MetricItem } from '@/app/alarm/types/monitor';
import { AlertOutlined, DownOutlined } from '@ant-design/icons';
import { FiltersConfig } from '@/app/alarm/types/monitor';
import { useLocalizedTime } from '@/hooks/useLocalizedTime';
import { useAlarmTabs } from '@/app/alarm/hooks/event';
import { useCommon } from '@/app/monitor/context/common';
import {
  LEVEL_MAP,
  useLevelList,
  useStateMap,
} from '@/app/alarm/constants/monitor';
import { deepClone, getEnumValueUnit } from '@/app/alarm/utils/common';
import {
  ColumnItem,
  ModalRef,
  Pagination,
  TableDataItem,
  UserItem,
  TabItem,
  TimeSelectorDefaultValue,
} from '@/app/alarm/types';
import {
  Input,
  Button,
  Checkbox,
  Tag,
  message,
  Tabs,
  Spin,
  Tooltip,
  Popconfirm,
  Switch,
  Dropdown,
  MenuProps,
} from 'antd';

const Alert: React.FC = () => {
  const getSettings = () => {
    try {
      return JSON.parse(localStorage.getItem('alarmSettings') || '{}');
    } catch {
      return {};
    }
  };
  const saveSettings = (
    settings: Partial<{ pageSize: number; showChart: boolean }>
  ) => {
    localStorage.setItem(
      'alarmSettings',
      JSON.stringify({ ...getSettings(), ...settings })
    );
  };

  const { isLoading } = useApiClient();
  const { getAlarmList, getMonitorMetrics, patchMonitorAlert } = useAlarmApi();
  const { t } = useTranslation();
  const { convertToLocalizedTime } = useLocalizedTime();
  const STATE_MAP = useStateMap();
  const LEVEL_LIST = useLevelList();
  const commonContext = useCommon();
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const detailRef = useRef<ModalRef>(null);
  const users = useRef(commonContext?.userList || []);
  const userList: UserItem[] = users.current;
  const beginTime: number = dayjs().subtract(10080, 'minute').valueOf();
  const lastTime: number = dayjs().valueOf();
  const tabs: TabItem[] = useAlarmTabs();
  const [searchText, setSearchText] = useState<string>('');
  const [tableLoading, setTableLoading] = useState<boolean>(false);
  const [chartLoading, setChartLoading] = useState<boolean>(false);
  const [tableData, setTableData] = useState<TableDataItem[]>([]);
  const [frequency, setFrequency] = useState<number>(0);
  const [timeRange, setTimeRange] = useState<number[]>([beginTime, lastTime]);
  const [activeTab, setActiveTab] = useState<string>('activeAlarms');
  const [chartData, setChartData] = useState<Record<string, any>[]>([]);
  const [pageLoading, setPageLoading] = useState<boolean>(false);
  const [myAlarms, setMyAlarms] = useState<boolean>(true);
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);
  const [metrics, setMetrics] = useState<MetricItem[]>([]);
  const [confirmLoading, setConfirmLoading] = useState(false);
  const [pagination, setPagination] = useState<Pagination>(() => {
    const { pageSize } = getSettings();
    return {
      current: 1,
      total: 0,
      pageSize: pageSize || 20,
    };
  });
  const timeDefaultValue =
    useRef<TimeSelectorDefaultValue>({
      selectValue: 10080,
      rangePickerVaule: null,
    })?.current || {};
  const [filters, setFilters] = useState<FiltersConfig>({
    level: [],
    state: [],
    notify: [],
    alarm_source: [],
  });
  const [showChart, setShowChart] = useState<boolean>(() => {
    const { showChart } = getSettings();
    return showChart !== undefined ? showChart : true;
  });

  const tableScrollY = showChart
    ? 'calc(100vh - 500px)'
    : 'calc(100vh - 400px)';

  const columns: ColumnItem[] = [
    {
      title: t('monitor.events.level'),
      dataIndex: 'level',
      key: 'level',
      width: 100,
      render: (_, { level }) => (
        <Tag icon={<AlertOutlined />} color={LEVEL_MAP[level] as string}>
          {LEVEL_LIST.find((item) => item.value === level)?.label || '--'}
        </Tag>
      ),
    },
    {
      title: t('common.time'),
      dataIndex: 'updated_at',
      key: 'updated_at',
      width: 160,
      sorter: (a: any, b: any) => a.id - b.id,
      render: (_, { updated_at }) => (
        <>{updated_at ? convertToLocalizedTime(updated_at) : '--'}</>
      ),
    },
    {
      title: t('monitor.events.alertName'),
      dataIndex: 'content',
      key: 'content',
      width: 120,
    },
    {
      title: t('monitor.events.source'),
      dataIndex: 'source',
      key: 'source',
      width: 120,
    },
    {
      title: t('monitor.events.state'),
      dataIndex: 'status',
      key: 'status',
      width: 80,
      render: (_, { status }) => (
        <Tag color={status === 'new' ? 'blue' : 'var(--color-text-4)'}>
          {STATE_MAP[status]}
        </Tag>
      ),
    },
    {
      title: t('monitor.events.notify'),
      dataIndex: 'notify',
      key: 'notify',
      width: 100,
      render: (_, record) => (
        <>
          {t(
            `monitor.events.${
              record.policy?.notice ? 'notified' : 'unnotified'
            }`
          )}
        </>
      ),
    },
    {
      title: t('common.operator'),
      dataIndex: 'operator',
      key: 'operator',
      width: 100,
      render: (_, { operator }) => {
        return operator ? <UserAvatar userName={operator} /> : <>--</>;
      },
    },
    {
      title: t('common.action'),
      key: 'action',
      dataIndex: 'action',
      width: 120,
      fixed: 'right',
      render: (_, record) => (
        <>
          <Button
            className="mr-[10px]"
            type="link"
            onClick={() => openAlertDetail(record)}
          >
            {t('common.detail')}
          </Button>
          <Permission requiredPermissions={['Operate']}>
            <Popconfirm
              title={t('monitor.events.closeTitle')}
              description={t('monitor.events.closeContent')}
              okText={t('common.confirm')}
              cancelText={t('common.cancel')}
              okButtonProps={{ loading: confirmLoading }}
              onConfirm={() => alertCloseConfirm(record.id)}
            >
              <Button type="link" disabled={record.status !== 'new'}>
                {t('common.close')}
              </Button>
            </Popconfirm>
          </Permission>
        </>
      ),
    },
  ];

  const batchMenuItems: MenuProps['items'] = [
    { key: 'close', label: t('monitor.events.close') },
    { key: 'assign', label: t('monitor.events.assign') },
    { key: 'reassign', label: t('monitor.events.reassign') },
    { key: 'acknowledge', label: t('monitor.events.acknowledge') },
  ];

  useEffect(() => {
    if (!frequency) {
      clearTimer();
      return;
    }
    timerRef.current = setInterval(() => {
      getAlarmTableData('timer');
      getChartData('timer');
    }, frequency);
    return () => {
      clearTimer();
    };
  }, [
    frequency,
    timeRange,
    activeTab,
    filters.level,
    filters.state,
    filters.alarm_source,
    pagination.current,
    pagination.pageSize,
  ]);

  useEffect(() => {
    if (isLoading) return;
    getAlarmTableData('refresh');
  }, [
    isLoading,
    timeRange,
    activeTab,
    filters.level,
    filters.state,
    filters.alarm_source,
    pagination.current,
    pagination.pageSize,
  ]);

  useEffect(() => {
    if (isLoading) return;
    getChartData('refresh');
  }, [
    isLoading,
    timeRange,
    filters.state,
    activeTab,
    filters.level,
    filters.alarm_source,
  ]);

  useEffect(() => {
    if (isLoading) return;
    getInitData();
  }, [isLoading]);

  const changeTab = (val: string) => {
    setActiveTab(val);
  };

  const getInitData = () => {
    setPageLoading(true);
    Promise.all([getMetrics()]).finally(() => {
      setPageLoading(false);
    });
  };

  const getMetrics = async () => {
    const data: any = await getMonitorMetrics();
    setMetrics(data);
  };

  const alertCloseConfirm = async (id: string | number) => {
    setConfirmLoading(true);
    try {
      await patchMonitorAlert(id, {
        status: 'closed',
      });
      message.success(t('monitor.events.successfullyClosed'));
      onRefresh();
    } finally {
      setConfirmLoading(false);
    }
  };

  const clearTimer = () => {
    if (timerRef.current) clearInterval(timerRef.current);
    timerRef.current = null;
  };

  const getParams = () => {
    const params: any = {
      status_in: filters.state,
      level_in: filters.level.join(','),
      alarm_source: filters.alarm_source.join(','),
      search: searchText,
      page: pagination.current,
      page_size: pagination.pageSize,
      created_at_after: dayjs(timeRange[0]).toISOString(),
      created_at_before: dayjs(timeRange[1]).toISOString(),
      mine: myAlarms,
    };
    return params;
  };

  const handleTableChange = (pag: any) => {
    saveSettings({ pageSize: pag.pageSize });
    setPagination(pag);
  };

  const getAlarmTableData = async (type: string, text?: string) => {
    const params: any = getParams();
    if (text) {
      params.search = '';
    }
    if (activeTab === 'activeAlarms') {
      params.created_at_before = '';
      params.created_at_after = '';
      if (params.status_in.length && !params.status_in.includes('new')) {
        setTableData([]);
        setPagination((pre) => ({
          ...pre,
          total: 0,
        }));
        return;
      }
      params.status_in = 'new';
    } else {
      if (params.status_in.length === 1 && params.status_in[0] === 'new') {
        setTableData([]);
        setPagination((pre) => ({
          ...pre,
          total: 0,
        }));
        return;
      }
      params.status_in =
        params.status_in.filter((item: any) => item !== 'new').join(',') ||
        'recovered,closed';
    }
    try {
      setTableLoading(type !== 'timer');
      const data = await getAlarmList(params);
      setTableData(data.items);
      setPagination((pre) => ({
        ...pre,
        total: data.count,
      }));
    } finally {
      setTableLoading(false);
    }
  };

  const getChartData = async (type: string) => {
    const params = getParams();
    const chartParams = deepClone(params);
    delete chartParams.page;
    delete chartParams.page_size;
    chartParams.search = '';
    chartParams.type = 'count';
    if (activeTab === 'activeAlarms') {
      chartParams.created_at_before = '';
      chartParams.created_at_after = '';
      if (
        chartParams.status_in.length &&
        !chartParams.status_in.includes('new')
      ) {
        setChartData([]);
        return;
      }
      chartParams.status_in = 'new';
    } else {
      if (
        chartParams.status_in.length === 1 &&
        chartParams.status_in[0] === 'new'
      ) {
        setChartData([]);
        return;
      }
      chartParams.status_in =
        chartParams.status_in.filter((item: any) => item !== 'new').join(',') ||
        'recovered,closed';
    }
    try {
      setChartLoading(type !== 'timer');
      const data = await getAlarmList(chartParams);
      setChartData(
        processDataForStackedBarChart(
          (data.items || []).filter((item: TableDataItem) => !!item.level)
        ) as any
      );
    } finally {
      setChartLoading(false);
    }
  };

  const onFrequencyChange = (val: number) => {
    setFrequency(val);
  };

  const onRefresh = () => {
    getAlarmTableData('refresh');
    getChartData('refresh');
  };

  const openAlertDetail = (row: TableDataItem) => {
    const metricInfo =
      metrics.find(
        (item) => item.id === row.policy?.query_condition?.metric_id
      ) || {};
    detailRef.current?.showModal({
      title: t('monitor.events.alertDetail'),
      type: 'add',
      form: {
        ...row,
        metric: metricInfo,
        alertTitle: row.source,
        alertValue: getEnumValueUnit(metricInfo as MetricItem, row.value),
      },
    });
  };

  const onTimeChange = (val: number[]) => {
    setTimeRange(val);
  };

  const processDataForStackedBarChart = (
    data: TableDataItem,
    desiredSegments = 12
  ) => {
    if (!data?.length) return [];
    // 1. 找到最早时间和最晚时间
    const timestamps = data.map((item: TableDataItem) =>
      dayjs(item.created_at)
    );
    const minTime = timestamps.reduce(
      (min: Dayjs, curr: Dayjs) => (curr.isBefore(min) ? curr : min),
      timestamps[0]
    ); // 最早时间
    const maxTime = timestamps.reduce(
      (max: Dayjs, curr: Dayjs) => (curr.isAfter(max) ? curr : max),
      timestamps[0]
    ); // 最晚时间
    // 2. 计算时间跨度（以分钟为单位）
    const totalMinutes = maxTime.diff(minTime, 'minute');
    // 3. 动态计算时间区间（每段的分钟数）
    const intervalMinutes = Math.max(
      Math.ceil(totalMinutes / desiredSegments),
      1
    ); // 确保 intervalMinutes 至少为 1
    // 4. 按动态时间区间划分数据
    const groupedData = data.reduce(
      (acc: TableDataItem, curr: TableDataItem) => {
        // 根据 created_at 时间戳，计算所属时间区间
        const timestamp = dayjs(curr.created_at).startOf('minute'); // 转为分钟级别时间戳
        const roundedTime = convertToLocalizedTime(
          minTime.add(
            Math.floor(timestamp.diff(minTime, 'minute') / intervalMinutes) *
              intervalMinutes,
            'minute'
          )
        );
        if (!acc[roundedTime]) {
          acc[roundedTime] = {
            time: roundedTime,
            critical: 0,
            error: 0,
            warning: 0,
          };
        }
        // 根据 level 统计数量
        if (curr.level === 'critical') {
          acc[roundedTime].critical += 1;
        } else if (curr.level === 'error') {
          acc[roundedTime].error += 1;
        } else if (curr.level === 'warning') {
          acc[roundedTime].warning += 1;
        }
        return acc;
      },
      {}
    );
    // 5. 将分组后的对象转为数组
    return Object.values(groupedData).sort(
      (a: any, b: any) => dayjs(b.time).valueOf() - dayjs(a.time).valueOf()
    );
  };

  const onFilterChange = (
    checkedValues: string[],
    field: keyof FiltersConfig
  ) => {
    setFilters((pre) => {
      pre[field] = checkedValues;
      return {
        ...pre,
      };
    });
  };

  const clearFilters = (field: keyof FiltersConfig) => {
    setFilters((prev) => ({ ...prev, [field]: [] }));
  };

  const enterText = () => {
    getAlarmTableData('refresh');
  };

  const clearText = () => {
    setSearchText('');
    getAlarmTableData('refresh', 'clear');
  };

  return (
    <div className="w-full">
      <Spin spinning={pageLoading}>
        <div className={alertStyle.alert}>
          <AlarmFilters
            filters={filters}
            onFilterChange={onFilterChange}
            clearFilters={clearFilters}
          />
          <div className={alertStyle.alertContent}>
            <Spin spinning={chartLoading}>
              <div className={alertStyle.chartWrapper}>
                <div className="flex items-center justify-between pb-[12px]">
                  <div className="flex items-center text-[14px] ml-[10px] relative">
                    {t('monitor.events.distributionMap')}
                    <Tooltip
                      placement="top"
                      title={t(`monitor.events.${activeTab}MapTips`)}
                    >
                      <div
                        className="cursor-pointer"
                        style={{
                          transform: 'translateY(-6px)',
                        }}
                      >
                        <Icon
                          type="a-shuoming2"
                          className="text-[14px] text-[var(--color-text-3)]"
                        />
                      </div>
                    </Tooltip>
                    <Switch
                      size="small"
                      checked={showChart}
                      onChange={(checked) => {
                        saveSettings({ showChart: checked });
                        setShowChart(checked);
                      }}
                      className="ml-2"
                    />
                  </div>
                  <TimeSelector
                    defaultValue={timeDefaultValue}
                    onlyRefresh={activeTab === 'activeAlarms'}
                    onChange={(value) => onTimeChange(value)}
                    onFrequenceChange={onFrequencyChange}
                    onRefresh={onRefresh}
                  />
                </div>
                {showChart && (
                  <div className={alertStyle.chart}>
                    <StackedBarChart
                      data={chartData}
                      colors={LEVEL_MAP as any}
                    />
                  </div>
                )}
              </div>
            </Spin>
            <div className={alertStyle.table}>
              <Tabs activeKey={activeTab} items={tabs} onChange={changeTab} />
              <div className="flex items-center justify-between mb-[16px]">
                <div className="flex items-center space-x-4">
                  <Input
                    allowClear
                    className="w-[300px]"
                    placeholder={t('common.searchPlaceHolder')}
                    onChange={(e) => setSearchText(e.target.value)}
                    onPressEnter={enterText}
                    onClear={clearText}
                  />
                  <Checkbox
                    className="ml-2"
                    checked={myAlarms}
                    onChange={(e) => {
                      setMyAlarms(e.target.checked);
                      onRefresh();
                    }}
                  >
                    {t('monitor.events.myAlarms')}
                  </Checkbox>
                  <span className="text-sm text-[var(--color-text-2)] ml-[10px]">
                    {`共检索出 ${pagination.total} 条结果，共选中 ${selectedRowKeys.length} 条告警`}
                  </span>
                </div>
                <Dropdown
                  menu={{ items: batchMenuItems }}
                  trigger={['click']}
                  placement="bottomRight"
                  arrow
                  overlayClassName={alertStyle.batchDropdown}
                >
                  <Button type="primary">
                    {t('monitor.events.batchOperations')}
                    <DownOutlined />
                  </Button>
                </Dropdown>
              </div>
              <CustomTable
                scroll={{ y: tableScrollY, x: 'calc(100vw - 320px)' }}
                columns={columns}
                dataSource={tableData}
                pagination={pagination}
                loading={tableLoading}
                rowKey="id"
                onChange={handleTableChange}
                rowSelection={{
                  selectedRowKeys,
                  onChange: (keys: React.Key[]) => setSelectedRowKeys(keys),
                }}
              />
            </div>
          </div>
        </div>
      </Spin>
      <AlertDetail
        ref={detailRef}
        metrics={metrics}
        userList={userList}
        onSuccess={() => getAlarmTableData('refresh')}
      />
    </div>
  );
};

export default Alert;

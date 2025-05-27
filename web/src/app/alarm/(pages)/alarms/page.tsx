'use client';

import React, { useEffect, useState, useRef } from 'react';
import Icon from '@/components/icon';
import useApiClient from '@/utils/request';
import dayjs, { Dayjs } from 'dayjs';
import TimeSelector from '@/components/time-selector';
import StackedBarChart from '@/app/alarm/components/stackedBarChart';
import alertStyle from './index.module.scss';
import AlarmFilters from '@/app/alarm/components/alarmFilters/page';
import AlarmTable from '@/app/alarm/(pages)/alarms/components/alarmTable';
import SearchFilter from '@/app/cmdb/(pages)/assetData/list/searchFilter';
import AlarmAssignModal from './components/assignModal';
import { UserItem } from '@/app/alarm/types';
import { useCommon } from '@/app/cmdb/context/common';
import { useAlarmApi } from '@/app/alarm/api/alarms';
import { useTranslation } from '@/utils/i18n';
import { MetricItem, FiltersConfig } from '@/app/alarm/types/alarms';
import { DownOutlined } from '@ant-design/icons';
import { useLocalizedTime } from '@/hooks/useLocalizedTime';
import { LEVEL_MAP } from '@/app/alarm/constants/monitor';
import {
  baseStates,
  allStates,
  batchMenuKeys,
} from '@/app/alarm/constants/alarm';
import { deepClone } from '@/app/alarm/utils/common';
import {
  Pagination,
  TableDataItem,
  TabItem,
  TimeSelectorDefaultValue,
} from '@/app/alarm/types';
import {
  Button,
  Checkbox,
  Tabs,
  Spin,
  Tooltip,
  Switch,
  Dropdown,
  MenuProps,
} from 'antd';

const Alert: React.FC = () => {
  const { isLoading } = useApiClient();
  const { getAlarmList, getMonitorMetrics } = useAlarmApi();
  const { t } = useTranslation();
  const { convertToLocalizedTime } = useLocalizedTime();
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const beginTime: number = dayjs().subtract(10080, 'minute').valueOf();
  const lastTime: number = dayjs().valueOf(); 
  const common = useCommon();
  const userList: UserItem[] = common?.userList || [];
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
  const [assignVisible, setAssignVisible] = useState(false);

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

  const [pagination, setPagination] = useState<Pagination>(() => {
    const { pageSize } = getSettings();
    return {
      current: 1,
      total: 0,
      pageSize: pageSize || 20,
    };
  });

  const tabList: TabItem[] = [
    {
      label: t('alarms.activeAlarms'),
      key: 'activeAlarms',
    },
    {
      label: t('alarms.historicalAlarms'),
      key: 'historicalAlarms',
    },
  ]

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

  const batchMenuItems: MenuProps['items'] = batchMenuKeys.map((key) => ({
    key,
    label: t(`alarms.${key}`),
  }));

  const isActiveAlarms = activeTab === 'activeAlarms';

  const stateOptions = (isActiveAlarms ? baseStates : allStates).map((val) => ({
    value: val,
    label: t(`alarms.${val}`),
  }));

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
    setFilters((pre: any) => {
      pre[field] = checkedValues;
      return {
        ...pre,
      };
    });
  };

  const clearFilters = (field: keyof FiltersConfig) => {
    setFilters((prev: any) => ({ ...prev, [field]: [] }));
  };

  const enterText = () => {
    getAlarmTableData('refresh');
  };

  const attrList = [
    { 
      attr_id: 'alarm_name', 
      attr_name: '告警名称', 
      attr_type: 'str', 
      is_required: false, 
      editable: false, 
      option: [] 
    },
    { 
      attr_id: 'alarm_id',   
      attr_name: '告警ID',   
      attr_type: 'str', 
      is_required: false, 
      editable: false, 
      option: [] 
    },
  ];

  const handleBatchMenuClick: MenuProps['onClick'] = ({ key }) => {
    if (key === 'assign') {
      setAssignVisible(true);
    }
  };

  return (
    <div className="w-full">
      <Spin spinning={pageLoading}>
        <div className={alertStyle.alert}>
          <AlarmFilters
            filters={filters}
            onFilterChange={onFilterChange}
            clearFilters={clearFilters}
            stateOptions={stateOptions}
          />
          <div className={alertStyle.alertContent}>
            <Spin spinning={chartLoading}>
              <div className={alertStyle.chartWrapper}>
                <div className="flex items-center justify-between pb-[12px]">
                  <div className="flex items-center text-[14px] ml-[10px] relative">
                    {t('alarms.distributionMap')}
                    <Tooltip
                      placement="top"
                      title={t(`alarms.${activeTab}MapTips`)}
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
                    onlyRefresh={isActiveAlarms}
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
              <Tabs activeKey={activeTab} items={tabList} onChange={changeTab} />
              <div className="flex items-center justify-between mb-[16px] min-w-[1000px]">
                <div className="flex items-center space-x-4">
                  <SearchFilter
                    attrList={attrList}
                    userList={userList}
                    organizationList={[]}
                    showExactSearch={false}
                    onSearch={(val: any) => {
                      setSearchText(val);
                      enterText();
                    }}
                  />
                  {isActiveAlarms && (
                    <Checkbox
                      className="ml-2"
                      checked={myAlarms}
                      onChange={(e) => {
                        setMyAlarms(e.target.checked);
                        onRefresh();
                      }}
                    >
                      {t('alarms.myAlarms')}
                    </Checkbox>
                  )}
                  <span className="text-sm text-[var(--color-text-2)]">
                    {`共检索出 ${pagination.total} 条结果，共选中 ${selectedRowKeys.length} 条告警`}
                  </span>
                </div>

                {isActiveAlarms && (
                  <div className="flex items-center space-x-4">
                    <Button type="primary" variant="solid">
                      {t('alarms.declareIncident')}
                    </Button>
                    <Dropdown
                      menu={{ items: batchMenuItems, onClick: handleBatchMenuClick }}
                      trigger={['click']}
                      placement="bottomRight"
                      arrow
                      overlayClassName={alertStyle.batchDropdown}
                    >
                      <Button type="primary">
                        {t('alarms.batchOperations')}
                        <DownOutlined />
                      </Button>
                    </Dropdown>
                  </div>
                )}
              </div>
              <AlarmTable
                dataSource={tableData}
                pagination={pagination}
                metrics={metrics}
                loading={tableLoading}
                tableScrollY={tableScrollY}
                selectedRowKeys={selectedRowKeys}
                onSelectionChange={setSelectedRowKeys}
                onChange={handleTableChange}
              />
            </div>
          </div>
        </div>
      </Spin>
      <AlarmAssignModal
        visible={assignVisible}
        onCancel={() => setAssignVisible(false)}
        onSuccess={() => {
          onRefresh();
        }}
      />
    </div>
  );
};

export default Alert;

'use client';
import React, { useState, useRef, useEffect, useMemo } from 'react';
import TimeSelector from '@/components/time-selector';
import { ListItem, TimeSelectorDefaultValue, TimeSelectorRef } from '@/types';
import { SearchOutlined, BulbFilled } from '@ant-design/icons';
import dayjs, { Dayjs } from 'dayjs';
import { Card, Input, Button, Select, Segmented, Spin } from 'antd';
import { useTranslation } from '@/utils/i18n';
import searchStyle from './index.module.scss';
import Collapse from '@/components/collapse';
import CustomBarChart from '@/app/log/components/charts/barChart';
import GrammarExplanation from '@/app/log/components/operate-drawer';
import SearchTable from './searchTable';
import LogTerminal from './logTerminal';
import { ChartData, Pagination, TableDataItem } from '@/app/log/types';
import useApiClient from '@/utils/request';
import useSearchApi from '@/app/log/api/search';
import useIntegrationApi from '@/app/log/api/integration';
import { SearchParams } from '@/app/log/types/search';
import { aggregateLogs, escapeArrayToJson } from '@/app/log/utils/common';
import { useLocalizedTime } from '@/hooks/useLocalizedTime';
import MarkdownRenderer from '@/components/markdown';
import { v4 as uuidv4 } from 'uuid';

const { Option } = Select;
const PAGE_LIMIT = 100;

const SearchView: React.FC = () => {
  const { t } = useTranslation();
  const { isLoading } = useApiClient();
  const { getLogStreams } = useIntegrationApi();
  const { getHits, getLogs } = useSearchApi();
  const { convertToLocalizedTime } = useLocalizedTime();
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const timeSelectorRef = useRef<TimeSelectorRef>(null);
  const [frequence, setFrequence] = useState<number>(0);
  const [searchText, setSearchText] = useState<string>('');
  const [tableData, setTableData] = useState<TableDataItem[]>([]);
  const [queryTime, setQueryTime] = useState<Date>(new Date());
  const [queryEndTime, setQueryEndTime] = useState<Date>(new Date());
  const [groupList, setGroupList] = useState<ListItem[]>([]);
  const [groups, setGroups] = useState<React.Key[]>([]);
  const [pagination, setPagination] = useState<Pagination>({
    current: 0,
    total: 0,
    pageSize: PAGE_LIMIT,
  });
  const [hasMore, setHasMore] = useState<boolean>(false);
  const [expand, setExpand] = useState<boolean>(true);
  const [chartData, setChartData] = useState<ChartData[]>([]);
  const [visible, setVisible] = useState<boolean>(false);
  const [activeMenu, setActiveMenu] = useState<string>('list');
  const [pageLoading, setPageLoading] = useState<boolean>(false);
  const [tableLoading, setTableLoading] = useState<boolean>(false);
  const [terminalLoading, setTerminalLoading] = useState<boolean>(false);
  const [timeDefaultValue, setTimeDefaultValue] =
    useState<TimeSelectorDefaultValue>({
      selectValue: 15,
      rangePickerVaule: null,
    });
  const [windowHeight, setWindowHeight] = useState<number>(window.innerHeight);

  const isList = useMemo(() => activeMenu === 'list', [activeMenu]);

  const scrollHeight = useMemo(() => {
    // 根据expand状态和屏幕高度动态计算scroll高度
    const fixedHeight = expand ? 510 : 430;
    return Math.max(200, windowHeight - fixedHeight);
  }, [windowHeight, expand]);

  useEffect(() => {
    if (isLoading) return;
    initData();
  }, [isLoading]);

  useEffect(() => {
    if (!frequence) {
      clearTimer();
      return;
    }
    timerRef.current = setInterval(() => {
      getLogData('timer');
    }, frequence);
    return () => {
      clearTimer();
    };
  }, [frequence, searchText, groups]);

  useEffect(() => {
    const handleResize = () => {
      setWindowHeight(window.innerHeight);
    };
    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  const clearTimer = () => {
    if (timerRef.current) clearInterval(timerRef.current);
    timerRef.current = null;
  };

  // 根据chartList和页数计算时间范围和limit
  const calculateTimeRange = (chartList: ChartData[], page: number) => {
    if (!chartList.length) {
      return null;
    }
    // 计算前面页数已经消费的数据量
    let startIndex = 0;
    if (page > 1) {
      // 找到当前页的起始位置
      for (let pageIdx = 1; pageIdx < page; pageIdx++) {
        let pageLimit = 0;
        let tempIndex = startIndex;
        // 计算这一页的limit
        while (tempIndex < chartList.length && pageLimit < PAGE_LIMIT) {
          pageLimit += chartList[tempIndex].value;
          tempIndex++;
        }
        startIndex = tempIndex;
      }
    }
    // 计算当前页的数据
    let currentPageLimit = 0;
    let endIndex = startIndex;
    while (endIndex < chartList.length && currentPageLimit < PAGE_LIMIT) {
      currentPageLimit += chartList[endIndex].value;
      endIndex++;
    }
    if (currentPageLimit === 0) {
      return null;
    }
    // 检查是否还有下一页 - 计算剩余数据的limit
    let nextPageLimit = 0;
    let nextIndex = endIndex;
    while (nextIndex < chartList.length && nextPageLimit < PAGE_LIMIT) {
      nextPageLimit += chartList[nextIndex].value;
      nextIndex++;
    }
    // 如果是最后一页，hasMore为false，否则判断下一页的limit是否>=PAGE_LIMIT
    const isLastPage = endIndex >= chartList.length;
    const endTime =
      chartList[isLastPage ? endIndex - 1 : endIndex]?.time - PAGE_LIMIT;
    return {
      start_time: new Date(chartList[startIndex]?.time).toISOString(),
      end_time: new Date(
        isLastPage
          ? Number((getParams().step || '').replace('ms', '')) + endTime
          : endTime
      ).toISOString(),
      limit: currentPageLimit,
      hasMore: !isLastPage,
    };
  };

  const onTabChange = async (val: string) => {
    setActiveMenu(val);
  };

  const initData = async () => {
    setPageLoading(true);
    Promise.all([getGroups(), getLogData('init')]).finally(() => {
      setPageLoading(false);
    });
  };

  const getGroups = async () => {
    const data = await getLogStreams({
      page_size: 99999999999,
      page: 1,
    });
    setGroupList(data?.items || []);
  };

  const getLogData = async (type: string, times?: number[]) => {
    try {
      setPageLoading(type !== 'timer');
      setQueryTime(new Date());
      setQueryEndTime(new Date());
      const params = getParams(times);
      const data = await getHits(params);
      const chartList = aggregateLogs(data?.hits);
      const total = chartList.reduce((pre, cur) => (pre += cur.value), 0);
      setChartData(chartList);
      setPagination((pre) => ({
        ...pre,
        total: total,
        current: 1,
      }));
      setHasMore(chartList.length > 0 && total > PAGE_LIMIT);
      setTableData([]); // 重置表格数据
      await getTableData({
        type,
        times,
        chartList,
        total,
      });
    } finally {
      setPageLoading(type === 'init');
      setQueryEndTime(new Date());
    }
  };

  const getTableData = async (extra: {
    type: string;
    chartList: ChartData[];
    times?: number[];
    total?: number;
  }) => {
    setTableLoading(extra.type === 'loadMore');
    try {
      // 根据chartList和pagination计算时间范围
      let params: SearchParams;
      if (extra.type === 'loadMore') {
        // 加载更多时，根据当前页数计算时间范围
        const timeRange = calculateTimeRange(
          extra.chartList,
          pagination.current + 1
        );
        if (!timeRange) {
          setHasMore(false);
          return;
        }
        params = {
          ...getParams(extra.times),
          start_time: timeRange.start_time,
          end_time: timeRange.end_time,
          limit: timeRange.limit,
        };
        setHasMore(timeRange.hasMore);
      } else {
        // 初始加载或刷新时，使用第一页的时间范围
        const timeRange = calculateTimeRange(extra.chartList, 1);
        if (!timeRange) {
          return;
        }
        params = {
          ...getParams(extra.times),
          start_time: timeRange.start_time,
          end_time: timeRange.end_time,
          limit: timeRange.limit,
        };
        setHasMore(timeRange.hasMore);
      }
      const data = await getLogs(params);
      const listData = (data || []).map((item: TableDataItem) => ({
        ...item,
        id: uuidv4(),
      }));
      if (extra.type === 'loadMore') {
        // 加载更多时，追加数据
        setTableData((prev) => [...prev, ...listData]);
        setPagination((pre) => ({
          ...pre,
          current: pre.current + 1,
        }));
        return;
      }
      // 初始加载或刷新时，替换数据
      setTableData(listData);
      setPagination((pre) => ({
        ...pre,
        current: 1,
      }));
    } finally {
      setTableLoading(false);
    }
  };

  const getParams = (seletedTimes?: number[]) => {
    const times = seletedTimes || timeSelectorRef.current?.getValue() || [];
    let text = searchText;
    if (groups?.length >= 1) {
      const groupsText =
        groups.length > 1
          ? `streams:"${escapeArrayToJson(groups)}"`
          : `streams:"${groups[0]}"`;
      text = searchText ? `${groupsText} | ${searchText}` : groupsText;
    }
    const params: SearchParams = {
      start_time: new Date(times[0]).toISOString(),
      end_time: new Date(times[1]).toISOString(),
      field: '_stream',
      fields_limit: 5,
      query: text || '*',
      limit: PAGE_LIMIT,
    };
    params.step = Math.round((times[1] - times[0]) / 100) + 'ms';
    return params;
  };

  const onFrequenceChange = (val: number) => {
    setFrequence(val);
  };

  const onRefresh = () => {
    getLogData('refresh');
  };

  const addToQuery = (row: TableDataItem, type: string) => {
    setSearchText((pre: string) => {
      if (type === 'field') {
        const pattern = /fields/;
        if (pre.match(pattern)) {
          return pre.replace(pattern, `fields ${row.label},`);
        }
        return pre ? `${pre} | fields ${row.label}` : `fields ${row.label}`;
      }
      return pre
        ? `${row.label}:${row.value} | ${pre}`
        : `${row.label}:${row.value}`;
    });
  };

  const onXRangeChange = (arr: [Dayjs, Dayjs]) => {
    setTimeDefaultValue((pre) => ({
      ...pre,
      rangePickerVaule: arr,
      selectValue: 0,
    }));
    const times = arr.map((item) => dayjs(item).valueOf());
    getLogData('refresh', times);
  };

  const loadMore = () => {
    if (!hasMore || tableLoading) return;
    getTableData({
      type: 'loadMore',
      chartList: chartData,
    });
  };

  return (
    <div className={`${searchStyle.search} w-full`}>
      <div className="flex justify-end">
        <TimeSelector
          ref={timeSelectorRef}
          defaultValue={timeDefaultValue}
          onChange={onRefresh}
          onFrequenceChange={onFrequenceChange}
          onRefresh={onRefresh}
        />
      </div>
      <Spin spinning={pageLoading}>
        <Card bordered={false} className={searchStyle.searchCondition}>
          <b className="flex mb-[10px]">{t('log.search.searchCriteria')}</b>
          <div className="flex">
            <Select
              style={{
                width: '250px',
              }}
              showSearch
              allowClear
              mode="tags"
              maxTagCount="responsive"
              placeholder={t('log.search.selectGroup')}
              value={groups}
              onChange={(val) => setGroups(val)}
            >
              {groupList.map((item) => (
                <Option value={item.id} key={item.id}>
                  {item.name}
                </Option>
              ))}
            </Select>
            <Input
              className="flex-1 mx-[8px]"
              placeholder={t('log.search.searchPlaceHolder')}
              value={searchText}
              addonAfter={
                <BulbFilled
                  className="cursor-pointer px-[10px] py-[8px]"
                  style={{ color: 'var(--color-primary)' }}
                  onClick={() => setVisible(true)}
                />
              }
              onChange={(e) => setSearchText(e.target.value)}
              onPressEnter={onRefresh}
            />
            <Button
              type="primary"
              icon={<SearchOutlined />}
              onClick={onRefresh}
            >
              {t('common.search')}
            </Button>
          </div>
        </Card>
        <Card bordered={false}>
          <Collapse
            title={t('log.search.histogram')}
            icon={
              <div>
                <span className="mr-2">
                  <span className="text-[var(--color-text-3)]">
                    {t('log.search.total')}：
                  </span>
                  <span>{pagination.total}</span>
                </span>
                <span className="mr-2">
                  <span className="text-[var(--color-text-3)]">
                    {t('log.search.queryTime')}：
                  </span>
                  <span>{convertToLocalizedTime(String(queryTime))}</span>
                </span>
                <span className="mr-2">
                  <span className="text-[var(--color-text-3)]">
                    {t('log.search.timeConsumption')}：
                  </span>
                  <span>{`${Number(queryEndTime) - Number(queryTime)}ms`}</span>
                </span>
              </div>
            }
            onToggle={(val) => setExpand(val)}
          >
            <CustomBarChart
              className={searchStyle.chart}
              data={chartData}
              onXRangeChange={onXRangeChange}
            />
          </Collapse>
        </Card>
        <Segmented
          className="my-[10px]"
          value={activeMenu}
          options={[
            { value: 'list', label: t('log.search.list') },
            { value: 'overview', label: t('log.search.terminal') },
          ]}
          onChange={onTabChange}
        />
        {isList ? (
          <Card
            bordered={false}
            style={{ minHeight: scrollHeight + 74 + 'px', overflowY: 'hidden' }}
          >
            <SearchTable
              dataSource={tableData}
              loading={tableLoading}
              scroll={{ y: scrollHeight }}
              addToQuery={addToQuery}
              onLoadMore={loadMore}
            />
          </Card>
        ) : (
          <Spin spinning={terminalLoading}>
            <LogTerminal
              className={
                expand ? 'h-[calc(100vh-434px)]' : 'h-[calc(100vh-354px)]'
              }
              searchParams={getParams}
              fetchData={(val) => setTerminalLoading(val)}
            />
          </Spin>
        )}
      </Spin>
      <GrammarExplanation
        title={t('log.search.grammarExplanation')}
        visible={visible}
        width={600}
        onClose={() => setVisible(false)}
        footer={
          <Button onClick={() => setVisible(false)}>
            {t('common.cancel')}
          </Button>
        }
      >
        <MarkdownRenderer filePath="grammar_explanation" fileName="index" />
      </GrammarExplanation>
    </div>
  );
};

export default SearchView;

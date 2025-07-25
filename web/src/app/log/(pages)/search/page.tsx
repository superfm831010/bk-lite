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

const { Option } = Select;

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
  const [allTableData, setAllTableData] = useState<TableDataItem[]>([]);
  const [queryTime, setQueryTime] = useState<Date>(new Date());
  const [queryEndTime, setQueryEndTime] = useState<Date>(new Date());
  //   const [limit, setLimit] = useState<number | null>(1000);
  const [groupList, setGroupList] = useState<ListItem[]>([]);
  const [groups, setGroups] = useState<React.Key[]>([]);
  const [pagination, setPagination] = useState<Pagination>({
    current: 1,
    total: 0,
    pageSize: 20,
  });
  const [expand, setExpand] = useState<boolean>(true);
  const [chartData, setChartData] = useState<ChartData[]>([]);
  const [visible, setVisible] = useState<boolean>(false);
  const [activeMenu, setActiveMenu] = useState<string>('list');
  const [pageLoading, setPageLoading] = useState<boolean>(false);
  const [tableLoading, setTableLoading] = useState<boolean>(false);
  const [timeDefaultValue, setTimeDefaultValue] =
    useState<TimeSelectorDefaultValue>({
      selectValue: 15,
      rangePickerVaule: null,
    });

  const isList = useMemo(() => activeMenu === 'list', [activeMenu]);

  const tableData = useMemo(() => {
    const startIndex = (pagination.current - 1) * pagination.pageSize;
    const endIndex = startIndex + pagination.pageSize;
    return allTableData.slice(startIndex, endIndex);
  }, [pagination.current, pagination.pageSize, allTableData]);

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

  const clearTimer = () => {
    if (timerRef.current) clearInterval(timerRef.current);
    timerRef.current = null;
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
    setPageLoading(type !== 'timer');
    setQueryTime(new Date());
    setQueryEndTime(new Date());
    const params = getParams(times);
    await Promise.all([getHits(params), getLogs(params)])
      .then((res) => {
        const chartData = aggregateLogs(res[0]?.hits);
        const listData = res[1] || [];
        setChartData(chartData);
        setPagination((pre) => {
          return {
            ...pre,
            current: 1,
            total: listData.length,
          };
        });
        setAllTableData(listData);
      })
      .finally(() => {
        setPageLoading(type === 'init');
        setQueryEndTime(new Date());
      });
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
      limit: null,
    };
    params.step = (times[1] - times[0]) / 100 + 'ms';
    return params;
  };

  const onFrequenceChange = (val: number) => {
    setFrequence(val);
  };

  const onRefresh = () => {
    getLogData('refresh');
  };

  const handleTableChange = (pagination: Pagination) => {
    setPagination({
      ...pagination,
      total: allTableData.length,
    });
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
              placeholder={t('common.select')}
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
            {/* <InputNumber
              className="mr-[8px] w-[100px]"
              placeholder={t('log.search.listTotal')}
              value={limit}
              min={0}
              max={10000}
              precision={0}
              controls={false}
              onChange={(val) => setLimit(val)}
            /> */}
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
                  <span>{allTableData?.length || 0}</span>
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
          <Card bordered={false}>
            <SearchTable
              dataSource={tableData}
              pagination={pagination}
              onChange={handleTableChange}
              addToQuery={addToQuery}
              expand={expand}
            />
          </Card>
        ) : (
          <Spin spinning={tableLoading}>
            <LogTerminal
              className="h-[calc(100vh-434px)]"
              searchParams={getParams}
              fetchData={(val) => setTableLoading(val)}
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

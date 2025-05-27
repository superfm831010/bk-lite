'use client';

import React, { useState, useEffect } from 'react';
import AlarmFilters from '@/app/alarm/components/alarmFilters/page';
import CustomTable from '@/components/custom-table';
import alertStyle from './index.module.scss';
import TimeSelector from '@/components/time-selector';
import type { TimeSelectorDefaultValue } from '@/app/alarm/types';
import type { ColumnsType } from 'antd/es/table';
import { useAlarmApi } from '@/app/alarm/api/alarms';
import { Input, Button, Tag, Spin } from 'antd';
import { TableDataItem, Pagination } from '@/app/alarm/types';
import { FiltersConfig } from '@/app/alarm/types/alarms';
import { useTranslation } from '@/utils/i18n';
import { AlertOutlined } from '@ant-design/icons';
import { LEVEL_MAP, useLevelList } from '@/app/alarm/constants/monitor';
import { incidentStates } from '@/app/alarm/constants/alarm';
import { useRouter } from 'next/navigation';

const IncidentsPage: React.FC = () => {
  const { getAlarmList } = useAlarmApi();
  const { t } = useTranslation();
  const router = useRouter(); 
  const LEVEL_LIST = useLevelList();
  const [searchText, setSearchText] = useState('');
  const [data, setData] = useState<TableDataItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState<FiltersConfig>({
    level: [],
    state: [],
    notify: [],
    alarm_source: [],
  });
  const [pagination, setPagination] = useState<Pagination>({
    current: 1,
    total: 0,
    pageSize: 20,
  });

  const timeDefaultValue: TimeSelectorDefaultValue = {
    selectValue: 0,
    rangePickerVaule: null,
  };

  const stateOptions = incidentStates.map((val) => ({
    value: val,
    label: t(`alarms.${val}`),
  }));


  const handleRefresh = () => fetchList(1, pagination.pageSize);

  const columns: ColumnsType<TableDataItem> = [
    {
      title: t('alarms.level'),
      dataIndex: 'level',
      key: 'level',
      width: 100,
      render: (_: any, { level }: any) => (
        <Tag icon={<AlertOutlined />} color={LEVEL_MAP[level] as string}>
          {LEVEL_LIST.find((item) => item.value === level)?.label || '--'}
        </Tag>
      ),
    },
    {
      title: t('alarms.createTime'),
      dataIndex: 'firstAlertTime',
      key: 'firstAlertTime',
      width: 140,
    },
    {
      title: t('alarms.alertName'),
      dataIndex: 'alertName',
      key: 'alertName',
      width: 140,
    },
    {
      title: t('alarms.source'),
      dataIndex: 'source',
      key: 'source',
      width: 140,
    },
    {
      title: t('alarms.state'),
      dataIndex: 'state',
      key: 'state',
      width: 140,
    },
    {
      title: t('alarms.duration'),
      dataIndex: 'duration',
      key: 'duration',
      width: 140,
    },
    {
      title: t('alarms.assignee'),
      dataIndex: 'operator',
      key: 'operator',
      width: 140,
    },
    {
      title: t('common.action'),
      dataIndex: 'action',
      key: 'action',
      width: 120,
      fixed: 'right',
      render: (_: any, record: any) => (
        <Button
          type="link"
          onClick={() => {
            router.push(`/alarm/incidents/detail?name=${record.content}`);
          }}
        >
          {t('common.detail')}
        </Button>
      ),
    },
  ];

  const fetchList = async (page?: number, pageSize?: number) => {
    setLoading(true);
    const res: any = await getAlarmList({
      search: searchText,
      page: page ?? pagination.current,
      page_size: pageSize ?? pagination.pageSize,
      level_in: filters.level.join(','),
      status_in: filters.state.join(','),
      alarm_source: filters.alarm_source.join(','),
    });
    setData(res.items);
    setPagination((p) => ({
      ...p,
      total: res.count,
      current: page ?? p.current,
      pageSize: pageSize ?? p.pageSize,
    }));
    setLoading(false);
  };

  useEffect(() => {
    fetchList(1, pagination.pageSize);
  }, [filters, searchText]);

  const onFilterChange = (vals: string[], field: keyof FiltersConfig) => {
    setFilters((prev) => ({ ...prev, [field]: vals }));
  };
  const clearFilters = (field: keyof FiltersConfig) => {
    setFilters((prev) => ({ ...prev, [field]: [] }));
  };
  const onTableChange = (pag: any) => fetchList(pag.current, pag.pageSize);

  return (
    <div className={alertStyle.container}>
      <div className={alertStyle.filters}>
        <AlarmFilters
          filterSource={false}
          stateOptions={stateOptions}
          filters={filters}
          onFilterChange={onFilterChange}
          clearFilters={clearFilters}
        />
      </div>
      <div className={alertStyle.content}>
        <div className="flex items-center justify-between space-x-2 mb-[16px]">
          <Input
            allowClear
            className="w-[300px]"
            placeholder={t('common.searchPlaceHolder')}
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            onPressEnter={() => fetchList(1, pagination.pageSize)}
          />
          <TimeSelector
            defaultValue={timeDefaultValue}
            onlyRefresh
            onRefresh={handleRefresh}
          />
        </div>
        <Spin spinning={loading}>
          <CustomTable
            rowKey="id"
            scroll={{ y: 'calc(100vh - 280px)', x: 'calc(100vw - 320px)' }}
            columns={columns}
            dataSource={data}
            pagination={pagination}
            loading={loading}
            onChange={onTableChange}
          />
        </Spin>
      </div>
    </div>
  );
};

export default IncidentsPage;

'use client';

import BaseInfo from './baseInfo';
import {
  Drawer,
  Button,
  Tag,
  Tabs,
  Spin,
  Timeline,
  Tooltip,
  message,
} from 'antd';
import { useTranslation } from '@/utils/i18n';
import { AlertOutlined, CopyOutlined } from '@ant-design/icons';
import { useLocalizedTime } from '@/hooks/useLocalizedTime';
import React, {
  useState,
  forwardRef,
  useImperativeHandle,
  useEffect,
  useRef,
} from 'react';
import {
  ModalRef,
  ModalConfig,
  TableDataItem,
  TabItem,
  Pagination,
  TimeLineItem,
} from '@/app/alarm/types';
import { getEnumValueUnit } from '@/app/alarm/utils/common';
import {
  LEVEL_MAP,
  useLevelList,
  useStateMap,
} from '@/app/alarm/constants/monitor';
import { ColumnsType } from 'antd/es/table';
import CustomTable from '@/components/custom-table';
import AlarmAction from './alarmAction';

const mockTimeline: TableDataItem[] = [
  {
    id: 1,
    level: 'critical',
    created_at: '2023-08-01T12:00:00Z',
    content: '触发告警',
    value: 0,
  },
  {
    id: 2,
    level: 'warning',
    created_at: '2023-08-01T12:05:00Z',
    content: '认领告警',
    value: 0,
  },
];

const mockEvents: TableDataItem[] = [
  {
    id: 1,
    level: 'critical',
    created_at: '2023-08-01T12:00:00Z',
    content: '触发告警',
    value: 0,
  },
  {
    id: 2,
    level: 'warning',
    created_at: '2023-08-01T12:05:00Z',
    content: '认领告警',
    value: 0,
  },
];

const AlertDetail = forwardRef<ModalRef, ModalConfig>(({}, ref) => {
  const { t } = useTranslation();
  const { convertToLocalizedTime } = useLocalizedTime();
  const STATE_MAP = useStateMap();
  const LEVEL_LIST = useLevelList();
  const [groupVisible, setGroupVisible] = useState<boolean>(false);
  const [formData, setFormData] = useState<TableDataItem>({});
  const [title, setTitle] = useState<string>('');
  const [activeTab, setActiveTab] = useState<string>('baseInfo');
  const [loading, setLoading] = useState<boolean>(false);
  const [tableLoading, setTableLoading] = useState<boolean>(false);
  const [rawVisible, setRawVisible] = useState<boolean>(false);
  const [rawData, setRawData] = useState<any>({});
  const isBaseInfo = activeTab === 'baseInfo';
  const isEventTab = activeTab === 'event';
  const [timeLineData, setTimeLineData] = useState<TimeLineItem[]>([]);
  const timelineRef = useRef<HTMLDivElement>(null);
  const isFetchingRef = useRef<boolean>(false);
  const [pagination, setPagination] = useState<Pagination>({
    current: 1,
    total: 0,
    pageSize: 100,
  });
  const tabList: TabItem[] = [
    {
      key: 'baseInfo',
      label: t('alarms.summary'),
    },
    {
      key: 'event',
      label: t('alarms.event'),
    },
    {
      key: 'timeline',
      label: t('alarms.changes'),
    },
  ];

  const handleShowRaw = (record: TableDataItem) => {
    setRawData(record);
    setRawVisible(true);
  };

  const eventColumns: ColumnsType<TableDataItem> = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    {
      title: t('common.time'),
      dataIndex: 'created_at',
      key: 'created_at',
      render: (text: string) => (text ? convertToLocalizedTime(text) : '--'),
    },
    { title: t('alarms.event'), dataIndex: 'content', key: 'content' },
    {
      title: t('alarms.level'),
      dataIndex: 'level',
      key: 'level',
      render: (level: string) => (
        <Tag color={LEVEL_MAP[level] as string}>
          {LEVEL_LIST.find((item) => item.value === level)?.label || '--'}
        </Tag>
      ),
    },
    {
      title: t('common.action'),
      key: 'action',
      render: (_: any, record: TableDataItem) => (
        <Button type="link" onClick={() => handleShowRaw(record)}>
          {t('alarms.rawData')}
        </Button>
      ),
    },
  ];

  useImperativeHandle(ref, () => ({
    showModal: ({ title, form }) => {
      setGroupVisible(true);
      setTitle(title);
      setFormData(form);
    },
  }));

  useEffect(() => {
    if (groupVisible) {
      getTableData();
    }
  }, [formData, groupVisible, activeTab]);

  useEffect(() => {
    if (formData?.id) {
      getTableData();
    }
  }, [pagination.current, pagination.pageSize]);

  useEffect(() => {
    if (!tableLoading) {
      isFetchingRef.current = false;
    }
  }, [tableLoading]);

  const getTableData = async () => {
    setTableLoading(true);
    try {
      const data = {
        count: mockTimeline.length,
        results: mockTimeline,
      };
      const _timelineData = data.results.map((item: TableDataItem) => ({
        color: LEVEL_MAP[item.level] || 'gray',
        children: (
          <>
            <span className="font-[600] mr-[10px]">
              {item.created_at ? convertToLocalizedTime(item.created_at) : '--'}
            </span>
            {`${formData.metric?.display_name || item.content}`}
            <span className="text-[var(--color-text-3)] ml-[10px]">
              {getEnumValueUnit(formData.metric, item.value)}
            </span>
          </>
        ),
      }));
      setTimeLineData((prev) => [...prev, ..._timelineData]);
      setPagination((prev: Pagination) => ({
        ...prev,
        total: data.count,
      }));
    } finally {
      setTableLoading(false);
    }
  };

  const loadMore = () => {
    if (pagination.current * pagination.pageSize < pagination.total) {
      isFetchingRef.current = true;
      setPagination((prev) => ({
        ...prev,
        current: prev.current + 1,
      }));
    }
  };

  const handleScroll = () => {
    if (!timelineRef.current) return;
    const { scrollTop, scrollHeight, clientHeight } = timelineRef.current;
    if (
      scrollTop + clientHeight >= scrollHeight - 10 &&
      !tableLoading &&
      !isFetchingRef.current
    ) {
      loadMore();
    }
  };

  const handleCancel = () => {
    setGroupVisible(false);
    setActiveTab('baseInfo');
    setTimeLineData([]);
  };

  const changeTab = (val: string) => {
    setActiveTab(val);
    setTimeLineData([]);
    setPagination({
      current: 1,
      total: 0,
      pageSize: 100,
    });
    setLoading(false);
    setTableLoading(false);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    message.success(t('common.copied'));
  };

  return (
    <Drawer
      title={title}
      open={groupVisible}
      width={800}
      onClose={handleCancel}
      footer={
        <div>
          <Button onClick={handleCancel}>{t('common.close')}</Button>
        </div>
      }
    >
      <div>
        <div className="flex justify-between">
          <div>
            <Tag
              icon={<AlertOutlined />}
              color={LEVEL_MAP[formData.level] as string}
            >
              {LEVEL_LIST.find((item) => item.value === formData.level)
                ?.label || '--'}
            </Tag>
            <b>{formData.content || '--'}</b>
          </div>
          <div>
            <Button type="primary" variant="solid" className="mr-[16px]">
              {t('alarms.declareIncident')}
            </Button>
            <AlarmAction
              row={formData}
              user={{ ...formData.user }}
              menuId={''}
              displayMode="dropdown"
              onSuccess={() => {}}
              fetchAlarmExecute={function (): Promise<any> {
                throw new Error('Function not implemented.');
              }}
              checkPermission={function (): boolean {
                throw new Error('Function not implemented.');
              }}
            />
          </div>
        </div>
        <ul className="flex mt-[16px] mb-[16px] space-x-6">
          <li className="flex items-center space-x-1.5">
            <span className="text-[var(--color-text-3)]">ID：</span>
            <Tooltip title={formData.alarm_id}>
              <span className="font-mono cursor-help">
                {formData.alarm_id?.slice(-6) || '--'}
              </span>
            </Tooltip>
            <CopyOutlined
              className="cursor-pointer"
              onClick={() => copyToClipboard(formData.alarm_id || '')}
            />
          </li>
          <li>
            <span className="text-[var(--color-text-3)]">
              {t('common.time')}：
            </span>
            <span>
              {formData.updated_at
                ? convertToLocalizedTime(formData.updated_at)
                : '--'}
            </span>
          </li>
          <li>
            <span className="text-[var(--color-text-3)]">
              {t('alarms.state')}：
            </span>
            <Tag color={formData.status === 'new' ? 'blue' : 'gray'}>
              {STATE_MAP[formData.status]}
            </Tag>
          </li>
        </ul>
      </div>
      <Tabs activeKey={activeTab} items={tabList} onChange={changeTab} />
      <Spin className="w-full" spinning={loading || tableLoading}>
        {isBaseInfo && <BaseInfo />}
        {isEventTab && (
          <div className="pt-[10px]">
            <CustomTable
              columns={eventColumns}
              dataSource={mockEvents}
              rowKey="id"
              pagination={false}
            />
            <Drawer
              title={t('alarms.rawData')}
              open={rawVisible}
              width={600}
              onClose={() => setRawVisible(false)}
            >
              <pre>{JSON.stringify(rawData, null, 2)}</pre>
            </Drawer>
          </div>
        )}
        {!isBaseInfo && !isEventTab && (
          <div
            className="pt-[10px]"
            style={{ height: 'calc(100vh - 330px)', overflowY: 'auto' }}
            ref={timelineRef}
            onScroll={handleScroll}
          >
            <Timeline items={timeLineData} />
          </div>
        )}
      </Spin>
    </Drawer>
  );
});

AlertDetail.displayName = 'alertDetail';
export default AlertDetail;

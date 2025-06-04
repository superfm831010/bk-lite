'use client';

import BaseInfo from './baseInfo';
import CustomTable from '@/components/custom-table';
import AlarmAction from './alarmAction';
import { ColumnsType } from 'antd/es/table';
import { useTranslation } from '@/utils/i18n';
import { useLocalizedTime } from '@/hooks/useLocalizedTime';
import { useAlarmApi } from '@/app/alarm/api/alarms';
import { useCommon } from '@/app/alarm/context/common';
import { useStateMap } from '@/app/alarm/constants/alarm';
import { Drawer, Button, Tag, Tabs, Timeline, Tooltip, message } from 'antd';
import {
  StateMap,
  EventItem,
  AlarmTableDataItem,
} from '@/app/alarm/types/alarms';
import {
  AlertOutlined,
  CopyOutlined,
  ClockCircleOutlined,
} from '@ant-design/icons';
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
  TabItem,
  Pagination,
  TimeLineItem,
} from '@/app/alarm/types/types';

const AlertDetail = forwardRef<ModalRef, ModalConfig>(
  ({ handleAction }, ref) => {
    const STATE_MAP = useStateMap();
    const { levelList, levelMap, levelListEvent, levelMapEvent } = useCommon();
    const { t } = useTranslation();
    const { convertToLocalizedTime } = useLocalizedTime();
    const { getEventList } = useAlarmApi();
    const [groupVisible, setGroupVisible] = useState<boolean>(false);
    const [formData, setFormData] = useState<AlarmTableDataItem | any>({});
    const [title, setTitle] = useState<string>('');
    const [activeTab, setActiveTab] = useState<string>('baseInfo');
    const [recordLoading, setRecordLoading] = useState<boolean>(false);
    const [eventLoading, setEventLoading] = useState<boolean>(false);
    const [rawVisible, setRawVisible] = useState<boolean>(false);
    const [rawData, setRawData] = useState<any>({});
    const [eventList, setEventList] = useState<EventItem[]>([]);
    const [timeLineData, setTimeLineData] = useState<TimeLineItem[]>([]);
    const timelineRef = useRef<HTMLDivElement>(null);
    const isFetchingRef = useRef<boolean>(false);
    const isBaseInfo = activeTab === 'baseInfo';
    const isEventTab = activeTab === 'event';
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

    const handleShowRaw = (record: AlarmTableDataItem) => {
      setRawData(record);
      setRawVisible(true);
    };

    useEffect(() => {
      if (!groupVisible || !formData.id) {
        return;
      }
      getEventListData({ alert_id: formData.id });
    }, [groupVisible, formData.id]);

    const getEventListData = async (params: any) => {
      setEventLoading(true);
      try {
        const { items, count } = await getEventList({
          ...params,
          page: pagination.current,
          page_size: pagination.pageSize,
        });
        setEventList(items || []);
        setPagination((prev) => ({ ...prev, total: count }));
      } finally {
        setEventLoading(false);
      }
    };

    useEffect(() => {
      if (activeTab === 'event' && groupVisible && formData.id) {
        getEventListData({ alert_id: formData.id });
      }
    }, [pagination.current, pagination.pageSize, activeTab]);

    const eventColumns: ColumnsType<any> = [
      { title: 'ID', dataIndex: 'id', key: 'id', width: 110 },
      {
        title: t('alarms.level'),
        dataIndex: 'level',
        key: 'level',
        width: 110,
        render: (_: any, { level }) => {
          const target = levelListEvent.find(
            (item) => item.level_id === Number(level)
          );
          return (
            <Tag icon={<AlertOutlined />} color={levelMapEvent[level || '']}>
              {target?.level_display_name || '--'}
            </Tag>
          );
        },
      },
      {
        title: t('common.time'),
        dataIndex: 'start_time',
        key: 'start_time',
        width: 180,
        render: (text: string) => (text ? convertToLocalizedTime(text) : '--'),
      },
      {
        title: t('alarms.event'),
        dataIndex: 'title',
        key: 'title',
        width: 220,
      },
      {
        title: t('alarms.object'),
        dataIndex: 'resource_type',
        key: 'resource_type',
        width: 120,
      },
      {
        title: t('alarms.metricName'),
        dataIndex: 'item',
        key: 'item',
        width: 120,
      },
      {
        title: t('alarms.metricValue'),
        dataIndex: 'value',
        key: 'value',
        width: 120,
      },
      {
        title: t('alarms.source'),
        dataIndex: 'source_name',
        key: 'source_name',
        width: 120,
      },
      {
        title: t('common.action'),
        key: 'action',
        fixed: 'right',
        width: 100,
        render: (_: any, record: AlarmTableDataItem) => (
          <Button type="link" onClick={() => handleShowRaw(record)}>
            {t('alarms.rawData')}
          </Button>
        ),
      },
    ];

    useImperativeHandle(ref, () => ({
      showModal: ({ title, form }) => {
        setEventList([]);
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
      if (!recordLoading) {
        isFetchingRef.current = false;
      }
    }, [recordLoading]);

    const getTableData = async () => {
      setRecordLoading(true);
      try {
        const data = {
          count: 0,
          results: [],
        };
        const _timelineData = data.results.map((item: AlarmTableDataItem) => ({
          color: levelMap[item.level] || 'gray',
          children: (
            <>
              <span className="font-[600] mr-[10px]">
                {item.created_at
                  ? convertToLocalizedTime(item.created_at)
                  : '--'}
              </span>
              {`${formData.metric?.display_name || item.content}`}
            </>
          ),
        }));
        setTimeLineData((prev) => [...prev, ..._timelineData]);
        setPagination((prev: Pagination) => ({
          ...prev,
          total: data.count,
        }));
      } finally {
        setRecordLoading(false);
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
        !recordLoading &&
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
        pageSize: 20,
      });
      setRecordLoading(false);
    };

    const copyToClipboard = (text: string) => {
      navigator.clipboard.writeText(text);
      message.success(t('common.copied'));
    };

    return (
      <Drawer
        title={
          <div className="flex items-center">
            <span>{t('alarms.alertDetail')} </span>
            <span className="text-[var(--color-text-2)] text-sm">-{title}</span>
          </div>
        }
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
                color={levelMap[formData.level] as string}
              >
                {levelList.find(
                  (item) => item.level_id === Number(formData.level)
                )?.level_display_name || '--'}
              </Tag>
              <b>{formData.content || '--'}</b>
            </div>
            <div>
              <Button
                color="danger"
                type="dashed"
                variant="solid"
                className="mr-[16px]"
              >
                {t('alarms.declareIncident')}
              </Button>
              <AlarmAction
                rowData={[formData]}
                displayMode="dropdown"
                onAction={handleAction}
              />
            </div>
          </div>
          <ul className="flex mt-[10px] mb-[14px] space-x-4">
            <li>
              <Tag>{STATE_MAP[formData.status as keyof StateMap] || '--'}</Tag>
            </li>
            <li className="flex items-center space-x-1">
              <Tag>
                <Tooltip
                  title={formData.alert_id}
                  styles={{
                    body: {
                      minWidth: 'fit-content',
                      whiteSpace: 'nowrap',
                    },
                  }}
                >
                  <span className="mr-2">ID</span>
                  {formData.alert_id?.slice(-6) || '--'}
                </Tooltip>
                <CopyOutlined
                  className="cursor-pointer ml-2"
                  onClick={() => copyToClipboard(formData.alert_id || '')}
                />
              </Tag>
            </li>
            <li>
              <Tag>
                <span className="mr-3">
                  <ClockCircleOutlined className="mr-[4px]" />
                  {formData.duration}
                </span>
                {formData.first_event_time && formData.last_event_time && (
                  <span>
                    {formData.first_event_time
                      ? convertToLocalizedTime(formData.first_event_time)
                      : ''}
                    <span className="ml-[2px] mr-[2px]">-</span>
                    {formData.last_event_time
                      ? convertToLocalizedTime(formData.last_event_time)
                      : ''}
                  </span>
                )}
              </Tag>
            </li>
          </ul>
        </div>
        <Tabs activeKey={activeTab} items={tabList} onChange={changeTab} />
        {recordLoading}
        <div className="w-full min-h-[300px]">
          {isBaseInfo && <BaseInfo detail={formData} />}
          {isEventTab && (
            <div className="pt-[10px]">
              <CustomTable
                rowKey="id"
                scroll={{ y: 'calc(100vh - 400px)' }}
                loading={eventLoading}
                columns={eventColumns}
                dataSource={eventList}
                pagination={{
                  current: pagination.current,
                  pageSize: pagination.pageSize,
                  total: pagination.total,
                }}
                onChange={(pag) =>
                  setPagination((prev) => ({
                    ...prev,
                    current: pag.current ?? prev.current,
                    pageSize: pag.pageSize ?? prev.pageSize,
                  }))
                }
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
        </div>
      </Drawer>
    );
  }
);

AlertDetail.displayName = 'alertDetail';
export default AlertDetail;

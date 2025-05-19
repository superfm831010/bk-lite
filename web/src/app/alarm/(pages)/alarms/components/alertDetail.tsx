'use client';

import { useAlarmApi } from '@/app/alarm/api/alarms';
import Information from './information';
import OperateModal from '@/app/monitor/components/operate-drawer';
import { Button, Tag, Tabs, Spin, Timeline } from 'antd';
import { useTranslation } from '@/utils/i18n';
// import { SearchParams } from '@/app/alarm/types/monitor';
import { AlertOutlined } from '@ant-design/icons';
import { useLocalizedTime } from '@/hooks/useLocalizedTime';
import { useAlarmTabs } from '@/app/alarm/hooks/event';
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
  ChartData,
  Pagination,
  TimeLineItem,
} from '@/app/alarm/types';
import {
  getEnumValueUnit,
  //   mergeViewQueryKeyValues,
  renderChart,
} from '@/app/alarm/utils/common';
import {
  LEVEL_MAP,
  useLevelList,
  useStateMap,
} from '@/app/alarm/constants/monitor';

const AlertDetail = forwardRef<ModalRef, ModalConfig>(
  ({ objects, metrics, userList, onSuccess }, ref) => {
    const { t } = useTranslation();
    const {
      getAlarmList: getMonitorEventDetail,
      getMonitorObject: getInstanceQuery,
      getMonitorMetrics: getEventRaw,
    } = useAlarmApi();
    const { convertToLocalizedTime } = useLocalizedTime();
    const STATE_MAP = useStateMap();
    const LEVEL_LIST = useLevelList();
    const [groupVisible, setGroupVisible] = useState<boolean>(false);
    const [formData, setFormData] = useState<TableDataItem>({});
    const [title, setTitle] = useState<string>('');
    const [chartData, setChartData] = useState<ChartData[]>([]);
    const [trapData, setTrapData] = useState<TableDataItem>({});
    const [activeTab, setActiveTab] = useState<string>('information');
    const [loading, setLoading] = useState<boolean>(false);
    const [tableLoading, setTableLoading] = useState<boolean>(false);
    const isInformation = activeTab === 'information';
    const tabs: TabItem[] = useAlarmTabs();
    const [timeLineData, setTimeLineData] = useState<TimeLineItem[]>([]);
    const timelineRef = useRef<HTMLDivElement>(null);
    const isFetchingRef = useRef<boolean>(false);
    const [pagination, setPagination] = useState<Pagination>({
      current: 1,
      total: 0,
      pageSize: 100,
    });

    useImperativeHandle(ref, () => ({
      showModal: ({ title, form }) => {
        setGroupVisible(true);
        setTitle(title);
        setFormData(form);
      },
    }));

    useEffect(() => {
      if (groupVisible) {
        if (isInformation) {
          if (formData.policy?.query_condition?.type === 'pmq') {
            getRawData();
            return;
          }
          getChartData();
          return;
        }
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

    // const getParams = () => {
    //   const _query: string = formData.metric?.query || '';
    //   const ids = formData.metric?.instance_id_keys || [];
    //   const params: SearchParams = {
    //     query: _query.replace(
    //       /__\$labels__/g,
    //       mergeViewQueryKeyValues([
    //         { keys: ids || [], values: formData.instance_id_values },
    //       ])
    //     ),
    //   };
    //   const MAX_POINTS = 100; // 最大数据点数
    //   const DEFAULT_STEP = 360; // 默认步长
    //   const startTime = new Date(formData.start_event_time).getTime();
    //   const endTime = formData.end_event_time
    //     ? new Date(formData.end_event_time).getTime()
    //     : new Date().getTime();

    //   if (startTime && endTime) {
    //     params.start = startTime;
    //     params.end = endTime;
    //     params.step = Math.max(
    //       Math.ceil(
    //         (params.end / MAX_POINTS - params.start / MAX_POINTS) / DEFAULT_STEP
    //       ),
    //       1
    //     );
    //   }
    //   return params;
    // };

    const getTableData = async () => {
      setTableLoading(true);
      try {
        const data: any = await getMonitorEventDetail({});
        const _timelineData = data.results.map((item: TableDataItem) => ({
          color: LEVEL_MAP[item.level] || 'gray',
          children: (
            <>
              <span className="font-[600] mr-[10px]">
                {item.created_at
                  ? convertToLocalizedTime(item.created_at)
                  : '--'}
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

    const getChartData = async () => {
      setLoading(true);
      try {
        const responseData: any = await getInstanceQuery();
        const data = responseData.data?.result || [];
        const config = [
          {
            instance_id_values: formData.instance_id_values,
            instance_name: formData.monitor_instance_name,
            instance_id: formData.monitor_instance_id,
            instance_id_keys: formData.metric?.instance_id_keys || [],
            dimensions: formData.metric?.dimensions || [],
            title: formData.metric?.display_name || '--',
          },
        ];
        const _chartData = renderChart(data, config);
        setChartData(_chartData);
      } finally {
        setLoading(false);
      }
    };

    const getRawData = async () => {
      setLoading(true);
      try {
        const responseData: any = await getEventRaw();
        setTrapData(responseData);
      } finally {
        setLoading(false);
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
      // 判断是否接近底部
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
      setActiveTab('information');
      setChartData([]);
      setTrapData({});
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

    const closeModal = () => {
      handleCancel();
      onSuccess();
    };

    return (
      <OperateModal
        title={title}
        open={groupVisible}
        width={800}
        onClose={handleCancel}
        footer={
          <div>
            <Button onClick={handleCancel}>{t('common.cancel')}</Button>
          </div>
        }
      >
        <div>
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
          <ul className="flex mt-[10px]">
            <li className="mr-[20px]">
              <span>{t('common.time')}：</span>
              <span>
                {formData.updated_at
                  ? convertToLocalizedTime(formData.updated_at)
                  : '--'}
              </span>
            </li>
            <li>
              <span>{t('monitor.events.state')}：</span>
              <Tag
                color={
                  formData.status === 'new' ? 'blue' : 'var(--color-text-4)'
                }
              >
                {STATE_MAP[formData.status]}
              </Tag>
            </li>
          </ul>
        </div>
        <Tabs activeKey={activeTab} items={tabs} onChange={changeTab} />
        <Spin className="w-full" spinning={loading || tableLoading}>
          {isInformation ? (
            <Information
              formData={formData}
              objects={objects}
              metrics={metrics}
              userList={userList}
              onClose={closeModal}
              trapData={trapData}
              chartData={chartData}
            />
          ) : (
            <div
              className="pt-[10px]"
              style={{
                height: 'calc(100vh - 276px)',
                overflowY: 'auto',
              }}
              ref={timelineRef}
              onScroll={handleScroll}
            >
              <Timeline items={timeLineData} />
            </div>
          )}
        </Spin>
      </OperateModal>
    );
  }
);

AlertDetail.displayName = 'alertDetail';
export default AlertDetail;

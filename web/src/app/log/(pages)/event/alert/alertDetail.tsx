'use client';

import React, {
  useState,
  forwardRef,
  useImperativeHandle,
  useEffect,
  useRef,
  useMemo,
} from 'react';
import { Button, Tag, Tabs, Spin, Timeline } from 'antd';
import OperateModal from '@/app/log/components/operate-drawer';
import { useTranslation } from '@/utils/i18n';
import {
  ModalRef,
  ModalConfig,
  TableDataItem,
  TabItem,
  Pagination,
  TimeLineItem,
} from '@/app/log/types';
import { AlertOutlined } from '@ant-design/icons';
import { useLocalizedTime } from '@/hooks/useLocalizedTime';
import { useAlertDetailTabs } from '@/app/log/hooks/event';
import useLogEventApi from '@/app/log/api/event';
import Information from './information';
import { LEVEL_MAP } from '@/app/log/constants';
import { useLevelList, useStateMap } from '@/app/log/hooks/event';

const AlertDetail = forwardRef<ModalRef, ModalConfig>(
  ({ userList, onSuccess }, ref) => {
    const { t } = useTranslation();
    const { geEventList, getEventRaw } = useLogEventApi();
    const { convertToLocalizedTime } = useLocalizedTime();
    const STATE_MAP = useStateMap();
    const LEVEL_LIST = useLevelList();
    const [groupVisible, setGroupVisible] = useState<boolean>(false);
    const [formData, setFormData] = useState<TableDataItem>({});
    const [title, setTitle] = useState<string>('');
    const [rawData, setRawData] = useState<TableDataItem[]>([]);
    const [activeTab, setActiveTab] = useState<string>('information');
    const [loading, setLoading] = useState<boolean>(false);
    const [pagination, setPagination] = useState<Pagination>({
      current: 1,
      total: 0,
      pageSize: 100,
    });
    const [tableLoading, setTableLoading] = useState<boolean>(false);
    const tabs: TabItem[] = useAlertDetailTabs();
    const [timeLineData, setTimeLineData] = useState<TimeLineItem[]>([]);
    const timelineRef = useRef<HTMLDivElement>(null);
    const isFetchingRef = useRef<boolean>(false); // 用于标记是否正在加载数据

    useImperativeHandle(ref, () => ({
      showModal: ({ title, form }) => {
        setGroupVisible(true);
        setTitle(title);
        setFormData(form);
        getRawData(form);
      },
    }));

    const isInformation = useMemo(
      () => activeTab === 'information',
      [activeTab]
    );

    useEffect(() => {
      // 当分页加载完成后，重置 isFetchingRef 标志位
      if (!tableLoading) {
        isFetchingRef.current = false;
      }
    }, [tableLoading]);

    const getTableData = async (customPage?: number) => {
      setTableLoading(true);
      const currentPage = customPage || pagination.current;
      const params = {
        page: currentPage,
        page_size: pagination.pageSize,
        alert_id: formData.id,
      };
      try {
        const data = await geEventList(params);
        const _timelineData = data.items.map((item: TableDataItem) => ({
          color: LEVEL_MAP[item.level] || 'gray',
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
        setTableLoading(false);
      }
    };

    const getRawData = async (form: TableDataItem = formData) => {
      setLoading(true);
      try {
        const responseData = await getEventRaw(form.id);
        const isAggregate = form.alert_type === 'aggregate';
        const data = responseData?.raw_data?.data;
        const aggregateData = data?.query_result ? [data?.query_result] : [];
        const result = !isAggregate ? data || [] : aggregateData;
        const rawList = result.map((item: TableDataItem, index: number) => ({
          ...item,
          id: index,
        }));
        setRawData(rawList);
      } finally {
        setLoading(false);
      }
    };

    const loadMore = () => {
      if (pagination.current * pagination.pageSize < pagination.total) {
        isFetchingRef.current = true;
        const nextPage = pagination.current + 1;
        setPagination((prev) => ({
          ...prev,
          current: nextPage,
        }));
        getTableData(nextPage);
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
      setActiveTab('information');
      setRawData([]);
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
      if (val === 'information') {
        getRawData();
        return;
      }
      getTableData();
    };

    const closeModal = () => {
      handleCancel();
      onSuccess();
    };

    return (
      <div>
        <OperateModal
          title={title}
          visible={groupVisible}
          width={900}
          destroyOnClose
          onClose={handleCancel}
          footer={
            <div>
              <Button onClick={handleCancel}>{t('common.cancel')}</Button>
            </div>
          }
        >
          <div>
            <div>
              <div>
                <Tag
                  icon={<AlertOutlined />}
                  color={LEVEL_MAP[formData.level] as string}
                >
                  {LEVEL_LIST.find((item) => item.value === formData.level)
                    ?.label || '--'}
                </Tag>
                <b>{formData.alert_name || '--'}</b>
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
                  <span>{t('log.event.state')}：</span>
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
                  userList={userList}
                  onClose={closeModal}
                  rawData={rawData}
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
          </div>
        </OperateModal>
      </div>
    );
  }
);

AlertDetail.displayName = 'alertDetail';
export default AlertDetail;

'use client';

import React, { useRef } from 'react';
import CustomTable from '@/components/custom-table';
import UserAvatar from '@/app/alarm/components/userAvatar';
import AlertDetail from './alarmDetail';
import AlarmAction from './alarmAction';
import type { ColumnsType } from 'antd/es/table';
import { AlertOutlined } from '@ant-design/icons';
import { Tag, Button, message } from 'antd';
import { ModalRef } from '@/app/alarm/types/types';
import { AlarmTableProps } from '@/app/alarm/types/alarms';
import { TableDataItem } from '@/app/alarm/types/types';
import { useTranslation } from '@/utils/i18n';
import { useLocalizedTime } from '@/hooks/useLocalizedTime';
import {
  useStateMap,
  useLevelList,
  useNotifiedStateMap,
  LEVEL_MAP,
} from '@/app/alarm/constants/alarm';

const AlarmTable: React.FC<AlarmTableProps> = ({
  dataSource,
  pagination,
  loading,
  tableScrollY,
  selectedRowKeys,
  onChange,
  onSelectionChange,
  extraActions,
}) => {
  const { t } = useTranslation();
  const { convertToLocalizedTime } = useLocalizedTime();
  const STATE_MAP = useStateMap();
  const LEVEL_LIST = useLevelList();
  const NOTIFIED_STATE: any = useNotifiedStateMap();
  const detailRef = useRef<ModalRef>(null);

  const columns: ColumnsType<TableDataItem> = [
    {
      title: t('alarms.level'),
      dataIndex: 'level',
      key: 'level',
      width: 100,
      render: (_: any, { level }: TableDataItem) => (
        <Tag icon={<AlertOutlined />} color={LEVEL_MAP[level] as string}>
          {LEVEL_LIST.find((item) => item.value === level)?.label || '--'}
        </Tag>
      ),
    },
    {
      title: t('alarms.firstEventTime'),
      dataIndex: 'first_event_time',
      key: 'first_event_time',
      width: 160,
      render: (_: any, { first_event_time }: TableDataItem) =>
        first_event_time ? convertToLocalizedTime(first_event_time) : '--',
    },
    {
      title: t('alarms.lastEventTime'),
      dataIndex: 'last_event_time',
      key: 'last_event_time',
      width: 160,
      render: (_: any, { last_event_time }: TableDataItem) =>
        last_event_time ? convertToLocalizedTime(last_event_time) : '--',
    },
    {
      title: t('alarms.eventTitle'),
      dataIndex: 'title',
      key: 'title',
      width: 280,
    },
    {
      title: t('alarms.eventCount'),
      dataIndex: 'event_count',
      key: 'event_count',
      width: 100,
    },
    {
      title: t('alarms.source'),
      dataIndex: 'source_names',
      key: 'source_names',
      width: 120,
    },
    {
      title: t('alarms.state'),
      dataIndex: 'status',
      key: 'status',
      width: 80,
      render: (_: any, { status }: TableDataItem) => (
        <Tag color={status === 'new' ? 'blue' : 'var(--color-text-4)'}>
          {STATE_MAP[status as keyof typeof STATE_MAP] || '--'}
        </Tag>
      ),
    },
    {
      title: t('alarms.duration'),
      dataIndex: 'duration',
      key: 'duration',
      width: 180,
    },
    {
      title: t('common.operator'),
      dataIndex: 'operator_user',
      key: 'operator_user',
      width: 100,
      render: (_: any, { operator }: TableDataItem) =>
        operator ? <UserAvatar userName={operator} /> : '--',
    },
    {
      title: t('alarms.notificationStatus'),
      dataIndex: 'notification_status',
      key: 'notification_status',
      width: 150,
      render: (_: any, { notification_status }: TableDataItem) => {
        return notification_status ? (
          <Tag color={notification_status === 'success' ? 'green' : 'red'}>
            {NOTIFIED_STATE[notification_status] || '--'}
          </Tag>
        ) : '--';
      },
    },
    {
      title: t('common.action'),
      key: 'action',
      dataIndex: 'action',
      width: 260,
      fixed: 'right',
      render: (_: any, record: TableDataItem) => (
        <div className="flex items-center">
          <Button
            className="mr-[12px]"
            type="link"
            onClick={() => onOpenDetail(record)}
          >
            {t('common.detail')}
          </Button>
          <AlarmAction
            row={record}
            user={{ ...record.user }}
            menuId={''}
            onSuccess={() => {
              message.success(t('common.success'));
              onChange('refresh');
            }}
            fetchAlarmExecute={function (): Promise<any> {
              throw new Error('Function not implemented.');
            }}
            checkPermission={function (): boolean {
              throw new Error('Function not implemented.');
            }}
          />
          {extraActions && extraActions(record)}
        </div>
      ),
    },
  ];

  const onOpenDetail = (row: TableDataItem) => {
    detailRef.current?.showModal({
      title: row.title,
      form: row,
      type: '',
    });
  };

  return (
    <>
      <CustomTable
        scroll={{ y: tableScrollY, x: 'calc(100vw - 320px)' }}
        columns={columns}
        dataSource={dataSource}
        pagination={pagination}
        loading={loading}
        rowKey="id"
        onChange={onChange}
        rowSelection={{ selectedRowKeys, onChange: onSelectionChange }}
      />
      <AlertDetail ref={detailRef} onSuccess={() => onChange('refresh')} />
    </>
  );
};

export default AlarmTable;

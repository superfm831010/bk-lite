'use client';

import React, { useRef } from 'react';
import CustomTable from '@/components/custom-table';
import UserAvatar from '@/app/cmdb/components/userAvatar';
import AlertDetail from './alarmDetail';
import AlarmAction from './alarmAction';
import type { ColumnsType } from 'antd/es/table';
import { getEnumValueUnit } from '@/app/alarm/utils/common';
import { AlertOutlined } from '@ant-design/icons';
import { Tag, Button, message } from 'antd';
import { ModalRef } from '@/app/alarm/types';
import { useCommon } from '@/app/monitor/context/common';
import { MetricItem } from '@/app/alarm/types/monitor';
import { TableDataItem, Pagination, UserItem } from '@/app/alarm/types';
import { useTranslation } from '@/utils/i18n';
import { useLocalizedTime } from '@/hooks/useLocalizedTime';
import {
  useStateMap,
  useLevelList,
  LEVEL_MAP,
} from '@/app/alarm/constants/monitor';

interface AlarmTableProps {
  dataSource: TableDataItem[];
  pagination: Pagination;
  loading: boolean;
  metrics: any[];
  tableScrollY: string;
  selectedRowKeys: React.Key[];
  onChange: (pag: any) => void;
  onSelectionChange: (keys: React.Key[]) => void;
  extraActions?: (record: TableDataItem) => React.ReactNode;
}

const AlarmTable: React.FC<AlarmTableProps> = ({
  dataSource,
  pagination,
  loading,
  metrics,
  tableScrollY,
  selectedRowKeys,
  onChange,
  onSelectionChange,
  extraActions,
}) => {
  const { t } = useTranslation();
  const { convertToLocalizedTime } = useLocalizedTime();
  const commonContext = useCommon();
  const STATE_MAP = useStateMap();
  const LEVEL_LIST = useLevelList();
  const detailRef = useRef<ModalRef>(null);
  const users = useRef(commonContext?.userList || []);
  const userList: UserItem[] = users.current;

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
      title: t('common.time'),
      dataIndex: 'updated_at',
      key: 'updated_at',
      width: 160,
      render: (_: any, { updated_at }: TableDataItem) =>
        updated_at ? convertToLocalizedTime(updated_at) : '--',
    },
    {
      title: t('alarms.alertName'),
      dataIndex: 'content',
      key: 'content',
      width: 120,
    },
    {
      title: t('alarms.source'),
      dataIndex: 'source',
      key: 'source',
      width: 120,
    },
    {
      title: t('alarms.state'),
      dataIndex: 'status',
      key: 'status',
      width: 80,
      render: (_: any, { status }: TableDataItem) => (
        <Tag color={status === 'new' ? 'blue' : 'var(--color-text-4)'}>
          {STATE_MAP[status]}
        </Tag>
      ),
    },
    {
      title: t('alarms.notify'),
      dataIndex: 'notify',
      key: 'notify',
      width: 100,
      render: (_: any, record: TableDataItem) =>
        t(`alarms.${record.policy?.notice ? 'notified' : 'unnotified'}`),
    },
    {
      title: t('common.operator'),
      dataIndex: 'operator',
      key: 'operator',
      width: 100,
      render: (_: any, { operator }: TableDataItem) =>
        operator ? <UserAvatar userName={operator} /> : '--',
    },
    {
      title: t('common.action'),
      key: 'action',
      dataIndex: 'action',
      width: 200,
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
    const metricInfo =
      metrics.find(
        (item) => item.id === row.policy?.query_condition?.metric_id
      ) || {};
    detailRef.current?.showModal({
      title: t('alarms.alertDetail'),
      type: 'add',
      form: {
        ...row,
        metric: metricInfo,
        alertTitle: row.source,
        alertValue: getEnumValueUnit(metricInfo as MetricItem, row.value),
      },
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
      <AlertDetail
        ref={detailRef}
        metrics={metrics}
        userList={userList}
        onSuccess={() => onChange('refresh')}
      />
    </>
  );
};

export default AlarmTable;

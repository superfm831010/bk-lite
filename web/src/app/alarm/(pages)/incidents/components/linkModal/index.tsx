'use client';

import React, { useState, useEffect } from 'react';
import styles from './index.module.scss';
import CustomTable from '@/components/custom-table';
import type { ColumnsType } from 'antd/es/table';
import type { TableDataItem } from '@/app/alarm/types/types';
import { Drawer, Input, Button } from 'antd';
import { useTranslation } from '@/utils/i18n';

interface OperateModalProps {
  visible: boolean;
  onClose: () => void;
  onLink: (selectedKeys: React.Key[]) => void;
}

const OperateModal: React.FC<OperateModalProps> = ({
  visible,
  onClose,
  onLink,
}) => {
  const { t } = useTranslation();
  const label = t('common.linkAlert');
  const [search, setSearch] = useState('');
  const [selectedKeys, setSelectedKeys] = useState<React.Key[]>([]);

  const alarmTableList: TableDataItem[] = []

  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
    total: alarmTableList.length,
  });

  useEffect(() => {
    setPagination((prev) => ({ ...prev, total: alarmTableList.length }));
  }, [alarmTableList.length]);

  const columns: ColumnsType<TableDataItem> = [
    { title: t('alarms.eventTitle'), dataIndex: 'title', key: 'title' },
    { title: t('alarms.level'), dataIndex: 'level', key: 'level' },
    { title: t('alarms.source'), dataIndex: 'source', key: 'source' },
    {
      title: t('common.action'),
      key: 'action',
      fixed: 'right',
      render: (_: any, record: TableDataItem) => (
        <Button
          type="link"
          onClick={() => onLink([record.id as any])}
        >
          {label}
        </Button>
      ),
    },
  ];

  const onTabTableChange = (pagination: any) => {
    setPagination((prev) => ({ ...prev, current: pagination.current }));
  };

  return (
    <Drawer
      title={label}
      width={660}
      onClose={onClose}
      open={visible}
      className={styles.drawer}
    >
      <div className={styles.header}>
        <Input
          placeholder={t('common.searchPlaceHolder')}
          allowClear
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ width: 240 }}
        />
        <Button
          type="primary"
          disabled={!selectedKeys.length}
          onClick={() => onLink(selectedKeys)}
        >
          {label}
        </Button>
      </div>
      <CustomTable
        rowKey="id"
        columns={columns}
        dataSource={alarmTableList}
        pagination={pagination}
        scroll={{ y: 'calc(100vh - 260px)', x: 'calc(50vw - 320px)' }}
        onChange={onTabTableChange}
        rowSelection={{
          selectedRowKeys: selectedKeys,
          onChange: (keys: React.Key[]) => setSelectedKeys(keys),
        }}
      />
    </Drawer>
  );
};

export default OperateModal;

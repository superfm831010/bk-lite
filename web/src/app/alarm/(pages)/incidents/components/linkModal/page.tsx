import React, { useState, useMemo, useEffect } from 'react';
import styles from './index.module.scss';
import CustomTable from '@/components/custom-table';
import type { ColumnsType } from 'antd/es/table';
import type { TableDataItem } from '@/app/alarm/types';
import { Drawer, Input, Button } from 'antd';
import { useTranslation } from '@/utils/i18n';

interface OperateModalProps {
  mode: 'link' | 'unlink';
  data: TableDataItem[];
  visible: boolean;
  onClose: () => void;
  onLink: (selectedKeys: React.Key[]) => void;
}

const OperateModal: React.FC<OperateModalProps> = ({
  mode,
  visible,
  data,
  onClose,
  onLink,
}) => {
  const { t } = useTranslation();
  const label = mode === 'link' ? t('common.linkAlert') : t('common.unlinkAlert');
  const [search, setSearch] = useState('');
  const [selectedKeys, setSelectedKeys] = useState<React.Key[]>([]);

  const filtered = useMemo(
    () =>
      data.filter((item) =>
        item.title.toLowerCase().includes(search.trim().toLowerCase())
      ),
    [data, search]
  );

  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
    total: filtered.length,
  });

  useEffect(() => {
    setPagination((prev) => ({ ...prev, total: filtered.length }));
  }, [filtered.length]);

  const columns: ColumnsType<TableDataItem> = [
    { title: t('monitor.events.eventTitle'), dataIndex: 'title', key: 'title' },
    { title: t('monitor.events.level'), dataIndex: 'level', key: 'level' },
    { title: t('monitor.events.source'), dataIndex: 'source', key: 'source' },
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
        dataSource={filtered}
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

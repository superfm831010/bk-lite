'use client';

import React, { useState, useEffect } from 'react';
import AlarmTable from '@/app/alarm/(pages)/alarms/components/alarmTable';
import type { TableDataItem } from '@/app/alarm/types/types';
import { Drawer, Input, Button } from 'antd';
import { useTranslation } from '@/utils/i18n';
import { useAlarmApi } from '@/app/alarm/api/alarms';

interface OperateModalProps {
  visible: boolean;
  confirmLoading?: boolean;
  onClose: () => void;
  onLink: (selectedKeys: React.Key[]) => void;
}

const OperateModal: React.FC<OperateModalProps> = ({
  visible,
  confirmLoading = false,
  onClose,
  onLink,
}) => {
  const { t } = useTranslation();
  const { getAlarmList } = useAlarmApi();
  const [alarmTableList, setAlarmTableList] = useState<TableDataItem[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [searchText, setSearchText] = useState('');
  const [selectedKeys, setSelectedKeys] = useState<React.Key[]>([]);
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
    total: 0,
  });

  const fetchAlarmList = async (pag?: {
    current?: number;
    pageSize?: number;
    title?: string;
  }) => {
    try {
      setLoading(true);
      const current = pag?.current ?? pagination.current;
      const pageSizeVal = pag?.pageSize ?? pagination.pageSize;
      const title = pag?.title ?? searchText;
      const res: any = await getAlarmList({
        page: current,
        page_size: pageSizeVal,
        title,
        has_incident: false,
      });
      setAlarmTableList(res.items || []);
      setLoading(false);
      setPagination({
        current,
        pageSize: pageSizeVal,
        total: res.count || 0,
      });
    } catch (error) {
      setLoading(false);
      console.error('Error fetching alarm list:', error);
    }
  };

  useEffect(() => {
    if (visible) {
      setSearchText('');
      setSelectedKeys([]);
      fetchAlarmList({ current: 1, pageSize: pagination.pageSize, title: '' });
    }
  }, [visible]);

  const onTableChange = (pag: { current: number; pageSize: number }) => {
    fetchAlarmList({
      current: pag.current,
      pageSize: pag.pageSize,
      title: searchText,
    });
  };

  return (
    <Drawer
      title={t('common.linkAlert')}
      width={740}
      onClose={onClose}
      open={visible}
    >
      <div
        style={{
          marginBottom: 16,
          display: 'flex',
          gap: 8,
          justifyContent: 'space-between',
        }}
      >
        <Input
          style={{ width: 250 }}
          placeholder={t('common.searchPlaceHolder')}
          allowClear
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
          onPressEnter={() => {
            fetchAlarmList({
              current: 1,
              pageSize: pagination.pageSize,
              title: searchText,
            });
          }}
          onClear={() => {
            setSearchText('');
            fetchAlarmList({
              current: 1,
              pageSize: pagination.pageSize,
              title: '',
            });
          }}
        />
        <Button
          type="primary"
          disabled={!selectedKeys.length}
          onClick={() => onLink(selectedKeys)}
          loading={confirmLoading}
        >
          {t('common.linkAlert')}
        </Button>
      </div>
      <AlarmTable
        dataSource={alarmTableList}
        pagination={pagination}
        loading={loading}
        tableScrollY="calc(100vh - 260px)"
        selectedRowKeys={selectedKeys}
        onSelectionChange={setSelectedKeys}
        onChange={onTableChange}
        onRefresh={() =>
          fetchAlarmList({
            current: pagination.current,
            pageSize: pagination.pageSize,
            title: searchText,
          })
        }
        extraActions={(record) => (
          <Button
            className="mr-2"
            type="link"
            onClick={() => onLink([record.id as number])}
          >
            {t('common.linkAlert')}
          </Button>
        )}
      />
    </Drawer>
  );
};

export default OperateModal;

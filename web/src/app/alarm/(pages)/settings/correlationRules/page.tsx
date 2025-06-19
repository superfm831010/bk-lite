'use client';

import React, { useState, useEffect, useRef } from 'react';
import OperateModal from './components/operateModal';
import CustomTable from '@/components/custom-table';
import PermissionWrapper from '@/components/permission';
import Introduction from '@/app/alarm/components/introduction';
import { Tabs } from 'antd';
import { AlertShieldListItem } from '@/app/alarm/types/settings';
import { useSettingApi } from '@/app/alarm/api/settings';
import { Button, Input, Modal, message } from 'antd';
import { useTranslation } from '@/utils/i18n';

const CorrelationRules: React.FC = () => {
  const { t } = useTranslation();
  const { getShieldList, deleteShield } = useSettingApi();
  const listCount = useRef<number>(0);
  const [tableLoading, setTableLoading] = useState<boolean>(false);
  const [operateVisible, setOperateVisible] = useState<boolean>(false);
  const [searchKey, setSearchKey] = useState<string>('');
  const [dataList, setDataList] = useState<AlertShieldListItem[]>([]);
  const [columns, setColumns] = useState<any[]>([]);
  const [currentRow, setCurrentRow] = useState<AlertShieldListItem | null>(
    null
  );
  const [pagination, setPagination] = useState({
    current: 1,
    total: 0,
    pageSize: 20,
  });
  const [activeTab, setActiveTab] = useState<'Event' | 'Alert'>('Event');

  useEffect(() => {
    getTableList();
  }, []);

  const handleEdit = (type: 'add' | 'edit', row?: AlertShieldListItem) => {
    if (type === 'edit' && row) {
      setCurrentRow(row);
    } else {
      setCurrentRow(null);
    }
    setOperateVisible(true);
  };

  const handleDelete = async (row: AlertShieldListItem) => {
    Modal.confirm({
      title: t('deleteTitle'),
      content: t('deleteContent'),
      okText: t('confirm'),
      cancelText: t('cancel'),
      centered: true,
      onOk: async () => {
        try {
          await deleteShield(row.id);
          message.success(t('successfullyDeleted'));
          if (pagination.current > 1 && listCount.current === 1) {
            setPagination((prev) => ({ ...prev, current: prev.current - 1 }));
            getTableList({
              current: pagination.current - 1,
              pageSize: pagination.pageSize,
            });
          } else {
            getTableList();
          }
        } catch {
          message.error(t('AlertAssign.operateFailed'));
        }
      },
    });
  };

  const getTableList = async (params: any = {}) => {
    try {
      setTableLoading(true);
      const searchVal =
        params.searchKey !== undefined ? params.searchKey : searchKey;
      const queryParams = {
        page: params.current || pagination.current,
        page_size: params.pageSize || pagination.pageSize,
        name: searchVal || undefined,
      };
      const data: any = await getShieldList(queryParams);
      setDataList(data.items || []);
      listCount.current = data.items?.length || 0;
      setPagination((prev) => ({
        ...prev,
        total: data.count || 0,
      }));
    } catch {
      message.error('加载列表失败');
      return { data: [], total: 0, success: false };
    } finally {
      setTableLoading(false);
    }
  };

  const handleFilterChange = () => {
    setPagination({ ...pagination, current: 1 });
    getTableList({
      ...pagination,
      current: 1,
    });
  };

  const handleFilterClear = () => {
    setSearchKey('');
    setPagination((prev) => ({ ...prev, current: 1 }));
    getTableList({
      current: 1,
      pageSize: pagination.pageSize,
      searchKey: '',
    });
  };

  const handleTableChange = (newPagination: any) => {
    const curPage = newPagination;
    setPagination(curPage);
    getTableList({
      ...curPage,
    });
  };

  const buildColumns = () => {
    return [
      {
        title: t('settings.assignName'),
        dataIndex: 'name',
        key: 'name',
        width: 150,
      },
      {
        title: t('settings.correlation.type'),
        dataIndex: 'type',
        key: 'type',
        width: 150,
      },
      {
        title: t('settings.correlation.scope'),
        dataIndex: 'scope',
        key: 'scope',
        width: 150,
      },
      {
        title: t('settings.correlation.lastUpdateTime'),
        dataIndex: 'last_update_time',
        key: 'last_update_time',
        width: 150,
      },
      {
        title: t('settings.assignActions'),
        key: 'operation',
        width: 130,
        render: (text: any, row: AlertShieldListItem) => (
          <div className="flex gap-4">
            <PermissionWrapper requiredPermissions={['Edit']}>
              <Button
                type="link"
                size="small"
                onClick={() => handleEdit('edit', row)}
              >
                {t('edit')}
              </Button>
            </PermissionWrapper>
            <PermissionWrapper requiredPermissions={['Delete']}>
              <Button
                type="link"
                size="small"
                onClick={() => handleDelete(row)}
              >
                {t('delete')}
              </Button>
            </PermissionWrapper>
          </div>
        ),
      },
    ];
  };

  useEffect(() => {
    setColumns(buildColumns());
  }, [searchKey, pagination]);

  return (
    <>
      <Introduction
        title={t('settings.correlationRules')}
        message={t('settings.correlationRulesMessage')}
      />
      <div className="p-4 bg-white rounded-lg shadow">
        <Tabs
          activeKey={activeTab}
          onChange={(key) => setActiveTab(key as 'Event' | 'Alert')}
          className="mb-4"
          items={[
            { key: 'Event', label: t('alarms.event') },
            { key: 'Alert', label: t('alarms.alert') },
          ]}
        />
        {activeTab === 'Event' && (
          <div>
            <div className="nav-box flex justify-between mb-[20px]">
              <div className="flex items-center">
                <Input
                  allowClear
                  value={searchKey}
                  placeholder={t('common.searchPlaceHolder')}
                  style={{ width: 250 }}
                  onChange={(e) => setSearchKey(e.target.value)}
                  onPressEnter={handleFilterChange}
                  onClear={handleFilterClear}
                />
              </div>
              <PermissionWrapper requiredPermissions={['Add']}>
                <Button type="primary" onClick={() => handleEdit('add')}>
                  {t('common.addNew')}
                </Button>
              </PermissionWrapper>
            </div>
            <CustomTable
              size="middle"
              rowKey="id"
              loading={tableLoading}
              columns={columns}
              dataSource={dataList}
              pagination={pagination}
              onChange={handleTableChange}
              scroll={{ y: 'calc(100vh - 520px)' }}
            />
            <OperateModal
              open={operateVisible}
              onClose={() => setOperateVisible(false)}
              currentRow={currentRow}
              onSuccess={() => {
                setPagination((prev) => ({ ...prev, current: 1 }));
                getTableList({ current: 1, pageSize: pagination.pageSize });
              }}
            />
          </div>
        )}
        {activeTab === 'Alert' && (
          <div className="p-4 bg-white rounded-lg shadow text-center">
            {t('settings.correlationAlertPlaceholder')}
          </div>
        )}
      </div>
    </>
  );
};

export default CorrelationRules;

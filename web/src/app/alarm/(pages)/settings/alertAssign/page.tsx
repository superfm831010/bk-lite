'use client';

import React, { useState, useEffect, useRef } from 'react';
import OperateModal from './components/operateModal';
import CustomTable from '@/components/custom-table';
import { AlertAssignListItem } from '@/app/alarm/types/settings';
import PermissionWrapper from '@/components/permission';
import { useSettingApi } from '@/app/alarm/api/settings';
import { Button, Input, Modal, message, Switch } from 'antd';
import { useTranslation } from '@/utils/i18n';

const AlertAssign: React.FC = () => {
  const { t } = useTranslation();
  const { getAlertAssignList, delAlertAssign } = useSettingApi();
  const listCount = useRef<number>(0);
  const [tableLoading, setTableLoading] = useState<boolean>(false);
  const [operateVisible, setOperateVisible] = useState<boolean>(false);
  const [searchKey, setSearchKey] = useState<string>('');
  const [dataList, setDataList] = useState<AlertAssignListItem[]>([]);
  const [columns, setColumns] = useState<any[]>([]);
  const [currentRow, setCurrentRow] = useState<AlertAssignListItem | null>(
    null
  );
  const [pagination, setPagination] = useState({
    current: 1,
    total: 0,
    pageSize: 20,
  });

  useEffect(() => {
    getTableList();
  }, []);

  const handleEdit = (type: 'add' | 'edit', row?: AlertAssignListItem) => {
    if (type === 'edit' && row) {
      setCurrentRow({
        id: row.id,
        assignName: row.assignName,
        assignPersonnel: row.assignPersonnel,
        assignTime: row.assignTime,
        assignStatus: row.assignStatus,
        assignCreateTime: row.assignCreateTime,
        built_in: row.built_in,
      });
    } else {
      setCurrentRow(null);
    }
    setOperateVisible(true);
  };

  const handleDelete = async (row: AlertAssignListItem) => {
    Modal.confirm({
      title: t('deleteTitle'),
      content: t('deleteContent'),
      okText: t('confirm'),
      cancelText: t('cancel'),
      centered: true,
      onOk: async () => {
        try {
          await delAlertAssign(row.id);
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
        searchVal,
      };
      const data: any = await getAlertAssignList({ params: queryParams });
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
    setPagination({ ...pagination, current: 1 });
    getTableList({
      ...pagination,
      current: 1,
    });
  };

  const handleTableChange = (newPagination: any, filters: any) => {
    const curPage = newPagination;
    setPagination(curPage);
    getTableList({
      ...curPage,
      device_type: filters.device_type,
    });
  };

  const handleStatusToggle = async (
    row: AlertAssignListItem,
    checked: boolean
  ) => {
    try {
      message.success(
        checked ? t('settings.enableSuccess') : t('settings.disableSuccess')
      );
      getTableList();
    } catch {
      message.error(t('common.operateFailed'));
    }
  };

  const buildColumns = () => {
    return [
      {
        title: t('settings.assignName'),
        dataIndex: 'assignName',
        key: 'assignName',
      },
      {
        title: t('settings.assignPersonnel'),
        dataIndex: 'assignPersonnel',
        key: 'assignPersonnel',
      },
      {
        title: t('settings.assignTime'),
        dataIndex: 'assignTime',
        key: 'assignTime',
      },
      {
        title: t('settings.assignStatus'),
        dataIndex: 'assignStatus',
        key: 'assignStatus',
      },
      {
        title: t('settings.assignCreateTime'),
        dataIndex: 'assignCreateTime',
        key: 'assignCreateTime',
      },
      {
        title: t('settings.assignStartStop'),
        dataIndex: 'built_in',
        key: 'built_in',
        render: (val: boolean, row: AlertAssignListItem) => (
          <Switch
            checked={val}
            disabled={row.built_in}
            onChange={(checked) => handleStatusToggle(row, checked)}
          />
        ),
      },
      {
        title: t('settings.assignActions'),
        key: 'operation',
        width: 140,
        render: (text: any, row: AlertAssignListItem) => (
          <div className="flex gap-4">
            <PermissionWrapper requiredPermissions={['Edit']}>
              <Button
                type="link"
                size="small"
                disabled={row.built_in}
                onClick={() => handleEdit('edit', row)}
              >
                {t('edit')}
              </Button>
            </PermissionWrapper>
            <PermissionWrapper requiredPermissions={['Delete']}>
              <Button
                type="link"
                size="small"
                disabled={row.built_in}
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
  }, []);

  console.log('currentRow', currentRow);
  //   const handleModalClose = () => {
  //     setOperateVisible(false);
  //     setCurrentRow(null);
  //   };

  //   const handleModalSubmit = () => {
  //     const newPagination = pagination;
  //     if (!currentRow) {
  //       newPagination.current = 1;
  //     }
  //     handleModalClose();
  //     setPagination(newPagination);
  //     getTableList(newPagination);
  //   };

  return (
    <div className="oid-library-container p-4 bg-white rounded-lg shadow">
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
        scroll={{ y: 'calc(100vh - 440px)' }}
      />
      <OperateModal
        open={operateVisible}
        onClose={() => setOperateVisible(false)}
        currentRow={currentRow}
      />
    </div>
  );
};

export default AlertAssign;

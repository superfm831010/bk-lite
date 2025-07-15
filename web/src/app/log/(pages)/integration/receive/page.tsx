'use client';
import React, { useEffect, useState, useRef, useMemo } from 'react';
import {
  Input,
  Button,
  message,
  Dropdown,
  Popconfirm,
  Space,
  Modal,
} from 'antd';
import useApiClient from '@/utils/request';
import useLogApi from '@/app/log/api/integration';
import { useTranslation } from '@/utils/i18n';
import {
  ColumnItem,
  ModalRef,
  Organization,
  Pagination,
  TableDataItem,
} from '@/app/log/types';
import CustomTable from '@/components/custom-table';
import TimeSelector from '@/components/time-selector';
import { DownOutlined } from '@ant-design/icons';
import { useCommon } from '@/app/log/context/common';
import { useAssetMenuItems } from '@/app/log/hooks/integration/common/other';
import { showGroupName } from '@/app/log/utils/common';
import EditConfig from './updateConfig';
import EditInstance from './editInstance';
import Permission from '@/components/permission';
import EllipsisWithTooltip from '@/components/ellipsis-with-tooltip';
import type { TableProps, MenuProps } from 'antd';
const { confirm } = Modal;

type TableRowSelection<T extends object = object> =
  TableProps<T>['rowSelection'];

const Asset = () => {
  const { isLoading } = useApiClient();
  const { getInstanceList, deleteLogInstance } = useLogApi();
  const { t } = useTranslation();
  const commonContext = useCommon();
  const authList = useRef(commonContext?.authOrganizations || []);
  const organizationList: Organization[] = authList.current;
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const configRef = useRef<ModalRef>(null);
  const instanceRef = useRef<ModalRef>(null);
  const assetMenuItems = useAssetMenuItems();
  const [pagination, setPagination] = useState<Pagination>({
    current: 1,
    total: 0,
    pageSize: 20,
  });
  const [tableLoading, setTableLoading] = useState<boolean>(false);
  const [tableData, setTableData] = useState<TableDataItem[]>([]);
  const [searchText, setSearchText] = useState<string>('');
  const [frequence, setFrequence] = useState<number>(0);
  const [confirmLoading, setConfirmLoading] = useState(false);
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);

  const handleAssetMenuClick: MenuProps['onClick'] = (e) => {
    openInstanceModal(
      {
        keys: selectedRowKeys,
      },
      e.key
    );
  };

  const assetMenuProps = {
    items: assetMenuItems,
    onClick: handleAssetMenuClick,
  };

  const columns: ColumnItem[] = [
    {
      title: t('common.name'),
      dataIndex: 'name',
      key: 'name',
      width: 100,
    },
    {
      title: t('common.group'),
      dataIndex: 'organization',
      key: 'organization',
      width: 100,
      render: (_, { organization }) => (
        <EllipsisWithTooltip
          className="w-full overflow-hidden text-ellipsis whitespace-nowrap"
          text={showGroupName(organization, organizationList)}
        />
      ),
    },
    {
      title: t('log.integration.collectionMethod'),
      dataIndex: 'collect_type__name',
      key: 'collect_type__name',
      width: 100,
    },
    {
      title: t('log.integration.collector'),
      dataIndex: 'collect_type__collector',
      key: 'collect_type__collector',
      width: 100,
    },
    {
      title: t('log.integration.collectionNode'),
      dataIndex: 'node_name',
      key: 'node_name',
      width: 100,
    },
    {
      title: t('common.action'),
      key: 'action',
      dataIndex: 'action',
      width: 160,
      fixed: 'right',
      render: (_, record) => (
        <>
          <Permission requiredPermissions={['Edit']}>
            <Button
              type="link"
              onClick={() => openInstanceModal(record, 'edit')}
            >
              {t('common.edit')}
            </Button>
          </Permission>
          <Permission requiredPermissions={['Edit']}>
            <Button
              className="ml-[10px]"
              type="link"
              onClick={() => openConfigModal(record)}
            >
              {t('log.integration.updateConfigration')}
            </Button>
          </Permission>
          <Permission requiredPermissions={['Delete']}>
            <Popconfirm
              title={t('common.deleteTitle')}
              description={t('common.deleteContent')}
              okText={t('common.confirm')}
              cancelText={t('common.cancel')}
              okButtonProps={{ loading: confirmLoading }}
              onConfirm={() => deleteInstConfirm(record)}
            >
              <Button type="link" className="ml-[10px]">
                {t('common.remove')}
              </Button>
            </Popconfirm>
          </Permission>
        </>
      ),
    },
  ];

  const enableOperateAsset = useMemo(() => {
    if (!selectedRowKeys.length) return true;
    return false;
  }, [selectedRowKeys]);

  useEffect(() => {
    if (!isLoading) {
      getAssetInsts();
    }
  }, [isLoading, pagination.current, pagination.pageSize]);

  useEffect(() => {
    if (!frequence) {
      clearTimer();
      return;
    }
    timerRef.current = setInterval(() => {
      getAssetInsts('timer');
    }, frequence);
    return () => {
      clearTimer();
    };
  }, [frequence, pagination.current, pagination.pageSize, searchText]);

  const onRefresh = () => {
    getAssetInsts();
  };

  const showDeleteConfirm = () => {
    confirm({
      title: t('common.delConfirm'),
      content: t('common.delConfirmCxt'),
      centered: true,
      onOk() {
        return new Promise(async (resolve) => {
          try {
            await deleteLogInstance({
              clean_child_config: true,
              instance_ids: selectedRowKeys,
            });
            message.success(t('common.successfullyDeleted'));
            if (pagination?.current) {
              pagination.current > 1 &&
                tableData.length === 1 &&
                pagination.current--;
            }
            setSelectedRowKeys([]);
            getAssetInsts();
          } finally {
            resolve(true);
          }
        });
      },
    });
  };

  const clearTimer = () => {
    if (timerRef.current) clearInterval(timerRef.current);
    timerRef.current = null;
  };

  const onFrequenceChange = (val: number) => {
    setFrequence(val);
  };

  const openConfigModal = (row = {}) => {
    configRef.current?.showModal({
      title: t('log.integration.updateConfigration'),
      type: 'edit',
      form: {
        ...row,
        objName: '',
      },
    });
  };

  const openInstanceModal = (row = {}, type: string) => {
    if (type === 'batchDelete') {
      showDeleteConfirm();
      return;
    }
    instanceRef.current?.showModal({
      title: t(`common.${type}`),
      type,
      form: row,
    });
  };

  const handleTableChange = (pagination: any) => {
    setPagination(pagination);
  };

  const getAssetInsts = async (type?: string) => {
    try {
      setTableLoading(type !== 'timer');
      const params = {
        page: pagination.current,
        page_size: pagination.pageSize,
        name: type === 'clear' ? '' : searchText,
      };
      const data = await getInstanceList(params);
      setTableData(data?.items || []);
      setPagination((prev: Pagination) => ({
        ...prev,
        total: data?.count || 0,
      }));
    } finally {
      setTableLoading(false);
    }
  };

  const deleteInstConfirm = async (row: any) => {
    setConfirmLoading(true);
    try {
      const data = {
        instance_ids: [row.id],
        clean_child_config: true,
      };
      await deleteLogInstance(data);
      message.success(t('common.successfullyDeleted'));
      getAssetInsts();
    } finally {
      setConfirmLoading(false);
    }
  };

  const clearText = () => {
    setSearchText('');
    getAssetInsts('clear');
  };

  //判断是否禁用按钮
  const onSelectChange = (newSelectedRowKeys: React.Key[]) => {
    setSelectedRowKeys(newSelectedRowKeys);
  };

  const rowSelection: TableRowSelection<TableDataItem> = {
    selectedRowKeys,
    onChange: onSelectChange,
  };

  return (
    <div className="bg-[var(--color-bg-1)] h-full p-[20px]">
      <div className="flex justify-between items-center mb-[10px]">
        <Input
          allowClear
          className="w-[320px]"
          placeholder={t('common.searchPlaceHolder')}
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
          onPressEnter={() => getAssetInsts()}
          onClear={clearText}
        ></Input>
        <div className="flex">
          <Dropdown
            className="mr-[8px]"
            overlayClassName="customMenu"
            menu={assetMenuProps}
            disabled={enableOperateAsset}
          >
            <Button>
              <Space>
                {t('common.action')}
                <DownOutlined />
              </Space>
            </Button>
          </Dropdown>
          <TimeSelector
            onlyRefresh
            onFrequenceChange={onFrequenceChange}
            onRefresh={onRefresh}
          />
        </div>
      </div>
      <CustomTable
        scroll={{ y: 'calc(100vh - 320px)', x: 'max-content' }}
        columns={columns}
        dataSource={tableData}
        pagination={pagination}
        loading={tableLoading}
        rowKey="id"
        onChange={handleTableChange}
        rowSelection={rowSelection}
      ></CustomTable>
      <EditConfig ref={configRef} onSuccess={() => getAssetInsts()} />
      <EditInstance
        ref={instanceRef}
        organizationList={organizationList}
        onSuccess={() => getAssetInsts()}
      />
    </div>
  );
};

export default Asset;

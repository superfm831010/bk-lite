'use client'
import { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { useLocalizedTime } from "@/hooks/useLocalizedTime";
import useMlopsTaskApi from '@/app/mlops/api/task';
import useMlopsManageApi from '@/app/mlops/api/manage';
import { Button, Input, Popconfirm, message, Tag, Tree } from 'antd';
import { PlusOutlined, ReloadOutlined } from '@ant-design/icons';
import CustomTable from '@/components/custom-table';
import EllipsisWithTooltip from '@/components/ellipsis-with-tooltip';
import PageLayout from '@/components/page-layout';
import TopSection from '@/components/top-section';
import PermissionWrapper from '@/components/permission';
import TrainTaskModal from './traintaskModal';
import { useTranslation } from '@/utils/i18n';
import { ModalRef, ColumnItem, Option } from '@/app/mlops/types';
import type { TreeDataNode } from 'antd';
import { TrainJob } from '@/app/mlops/types/task';
import { TRAIN_STATUS_MAP, TRAIN_TEXT } from '@/app/mlops/constants';
import { JointContent } from 'antd/es/message/interface';
import { DataSet } from '@/app/mlops/types/manage';
const { Search } = Input;

const getStatusColor = (value: string, TrainStatus: Record<string, string>) => {
  return TrainStatus[value] || '';
};

const getStatusText = (value: string, TrainText: Record<string, string>) => {
  return TrainText[value] || '';
};

const TrainTask = () => {
  const { t } = useTranslation();
  const { convertToLocalizedTime } = useLocalizedTime();
  const { getAnomalyDatasetsList } = useMlopsManageApi();
  const {
    getAnomalyTaskList,
    deleteAnomalyTrainTask,
    startAnomalyTrainTask,
  } = useMlopsTaskApi();
  const modalRef = useRef<ModalRef>(null);
  const [tableData, setTableData] = useState<TrainJob[]>([]);
  const [datasetOptions, setDatasetOptions] = useState<Option[]>([]);
  const [selectedKeys, setSelectedKeys] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [pagination, setPagination] = useState({
    current: 1,
    total: 0,
    pageSize: 10,
  });

  const treeData: TreeDataNode[] = [
    {
      title: t(`traintask.traintask`),
      key: 'traintask',
      selectable: false,
      children: [
        {
          title: t(`datasets.anomaly`),
          key: 'anomaly',
        }
      ]
    }
  ];

  const columns: ColumnItem[] = [
    {
      title: t('common.name'),
      key: 'name',
      dataIndex: 'name',
    },
    {
      title: t('mlops-common.createdAt'),
      key: 'created_at',
      dataIndex: 'created_at',
      render: (_, record) => {
        return (<p>{convertToLocalizedTime(record.created_at, 'YYYY-MM-DD HH:mm:ss')}</p>)
      }
    },
    {
      title: t('mlops-common.creator'),
      key: 'creator',
      dataIndex: 'creator',
      render: (_, { creator }) => {
        return creator ? (
          <div className="flex h-full items-center" title={creator}>
            <span
              className="block w-[18px] h-[18px] leading-[18px] text-center content-center rounded-[50%] mr-2 text-white"
              style={{ background: 'blue' }}
            >
              {creator.slice(0, 1).toLocaleUpperCase()}
            </span>
            <span>
              <EllipsisWithTooltip
                className="w-full overflow-hidden text-ellipsis whitespace-nowrap"
                text={creator}
              />
            </span>
          </div>
        ) : (
          <>--</>
        );
      }
    },
    {
      title: t('mlops-common.status'),
      key: 'status',
      dataIndex: 'status',
      render: (_, record: TrainJob) => {
        return record.status ? (<Tag color={getStatusColor(record.status, TRAIN_STATUS_MAP)} className=''>
          {t(`traintask.${getStatusText(record.status, TRAIN_TEXT)}`)}
        </Tag>) : (<p>--</p>)
      }
    },
    {
      title: t('common.action'),
      key: 'action',
      dataIndex: 'action',
      width: 240,
      fixed: 'right',
      align: 'center',
      render: (_: unknown, record: TrainJob) => (
        <>
          <PermissionWrapper requiredPermissions={['Edit']}>
            <Popconfirm
              title={t('traintask.trainStartTitle')}
              description={t('traintask.trainStartContent')}
              okText={t('common.confirm')}
              cancelText={t('common.cancel')}
              onConfirm={() => onTrainStart(record)}
            >
              <Button
                type="link"
                className="mr-[10px]"
              >
                {t('traintask.train')}
              </Button>
            </Popconfirm>
          </PermissionWrapper>
          <PermissionWrapper requiredPermissions={['Edit']}>
            <Button
              type="link"
              className="mr-[10px]"
              onClick={() => handleEdit(record)}
            >
              {t('common.edit')}
            </Button>
          </PermissionWrapper>
          <PermissionWrapper requiredPermissions={['Delete']}>
            <Popconfirm
              title={t('traintask.delTraintask')}
              description={t(`traintask.delTraintaskContent`)}
              okText={t('common.confirm')}
              cancelText={t('common.cancel')}
              onConfirm={() => onDelete(record)}
            >
              <Button type="link" danger>{t('common.delete')}</Button>
            </Popconfirm>
          </PermissionWrapper>
        </>
      ),
    },
  ];

  const topSection = useMemo(() => {
    return (
      <TopSection title={t('traintask.traintask')} content={t('traintask.description')} />
    );
  }, [t]);

  const leftSection = (
    <div className='w-full'>
      <Tree
        treeData={treeData}
        showLine
        selectedKeys={selectedKeys}
        defaultExpandedKeys={['anomaly']}
        onSelect={(keys) => setSelectedKeys(keys as string[])}
      />
    </div>
  );

  useEffect(() => {
    setSelectedKeys(['anomaly']);
  }, []);

  useEffect(() => {
    getDatasetList();
  }, [selectedKeys])

  useEffect(() => {
    getTasks();
  }, [pagination.current, pagination.pageSize, selectedKeys]);

  const getTasks = async () => {
    const [activeTab] = selectedKeys;
    if (!activeTab) return;
    setLoading(true);
    try {
      if (activeTab === 'anomaly') {
        const { items, count } = await fetchTaskList(pagination.current, pagination.pageSize);
        const _data =
          items?.map((item: any) => ({
            id: item.id,
            name: item.name,
            train_data_id: item.train_data_id,
            val_data_id: item.val_data_id,
            test_data_id: item.test_data_id,
            created_at: item.created_at,
            creator: item?.created_by,
            status: item?.status,
            max_evals: item.max_evals,
            algorithm: item.algorithm,
            hyperopt_config: item.hyperopt_config
          })) || [];
        setTableData(_data as TrainJob[]);
        setPagination(prev => ({
          ...prev,
          total: count || 1,
        }));
      }
    } catch (e) {
      console.log(e);
    } finally {
      setLoading(false);
    }
  };

  const getDatasetList = async () => {
    const [activeTab] = selectedKeys;
    if (!activeTab) return;
    if (activeTab === 'anomaly') {
      const data = await getAnomalyDatasetsList({});
      const items = data.map((item: DataSet) => {
        return {
          value: item.id,
          label: item.name
        }
      }) || [];
      setDatasetOptions(items);
    }
  };

  const fetchTaskList = useCallback(async (page: number = 1, pageSize: number = 10) => {
    const { count, items } = await getAnomalyTaskList({
      page,
      page_size: pageSize
    });
    return {
      items,
      count
    }
  }, [getAnomalyTaskList]);

  const handleAdd = () => {
    if (modalRef.current) {
      modalRef.current.showModal({
        type: 'add',
        title: 'addtask',
        form: {}
      })
    }
  };

  const handleEdit = (record: TrainJob) => {
    if (modalRef.current) {
      modalRef.current.showModal({
        type: 'edit',
        title: 'edittask',
        form: record
      })
    }
  };

  const onTrainStart = async (record: TrainJob) => {
    try {
      await startAnomalyTrainTask(record.id);
    } catch (e) {
      console.log(e);
      message.error(e as JointContent)
    }
  };


  const handleChange = (value: any) => {
    setPagination(value);
  };

  const onSearch = () => {
    getTasks();
  };

  const onDelete = async (record: TrainJob) => {
    try {
      await deleteAnomalyTrainTask(record.id as string)
    } catch (e) {
      console.log(e);
    } finally {
      message.success(t('common.delSuccess'));
      getTasks();
    }
  };

  const onRefresh = () => {
    getTasks();
    getDatasetList();
  };

  return (
    <>
      <PageLayout
        topSection={topSection}
        leftSection={leftSection}
        rightSection={
          (<>
            <div className="flex justify-end items-center mb-4 gap-2">
              <div className="flex">
                <Search
                  className="w-[240px] mr-1.5"
                  placeholder={t('traintask.searchText')}
                  enterButton
                  onSearch={onSearch}
                  style={{ fontSize: 15 }}
                />
                <PermissionWrapper requiredPermissions={['Add']}>
                  <Button type="primary" icon={<PlusOutlined />} className="rounded-md text-xs shadow mr-2" onClick={() => handleAdd()}>
                    {t('common.add')}
                  </Button>
                </PermissionWrapper>
                <ReloadOutlined onClick={onRefresh} />
              </div>
            </div>
            <div className="flex-1 relative">
              <div className='absolute w-full'>
                <CustomTable
                  rowKey="id"
                  className="mt-3"
                  scroll={{ x: '100%', y: 'calc(100vh - 420px)' }}
                  dataSource={tableData}
                  columns={columns}
                  pagination={pagination}
                  loading={loading}
                  onChange={handleChange}
                />
              </div>
            </div>
          </>)
        }
      />
      <TrainTaskModal ref={modalRef} onSuccess={() => onRefresh()} datasetOptions={datasetOptions} />
    </>
  );
};

export default TrainTask;
'use client'
import { useState, useEffect, useRef, useCallback, useMemo } from 'react';
// import { useRouter } from 'next/navigation';
import { useLocalizedTime } from "@/hooks/useLocalizedTime";
import useMlopsApi from '@/app/mlops/api';
import { usePathname } from 'next/navigation';
import { Button, Input, Popconfirm, message, Tag } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import CustomTable from '@/components/custom-table';
import Icon from '@/components/icon';
import TrainTaskModal from './traintaskModal';
import TrainTaskDrawer from './traintaskDrawer';
import { useTranslation } from '@/utils/i18n';
import { ModalRef, ColumnItem, TrainJob, TrainTaskHistory } from '@/app/mlops/types';
import { TrainStatus, TrainText } from '@/app/mlops/constants';
import SubLayout from '@/components/sub-layout';
import { JointContent } from 'antd/es/message/interface';
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
  // const router = useRouter();
  const path = usePathname();
  const { getAnomalyTaskList, deleteAnomalyTrainTask, startAnomalyTrainTask } = useMlopsApi();
  const modalRef = useRef<ModalRef>(null);
  const [tableData, setTableData] = useState<TrainJob[]>([]);
  const [historyData, setHistoryData] = useState<TrainTaskHistory[]>([]);
  const [selectId, setSelectId] = useState<number | null>(null);
  const [open, setOpen] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [pagination, setPagination] = useState({
    current: 1,
    total: 0,
    pageSize: 10,
  });

  const columns: ColumnItem[] = [
    {
      title: t('common.name'),
      key: 'name',
      dataIndex: 'name',
    },
    {
      title: t('common.type'),
      key: 'type',
      dataIndex: 'type',
      render: (_, record) => {
        return (<>{t(`datasets.${record.type}`)}</>)
      }
    },
    {
      title: t('common.createdAt'),
      key: 'created_at',
      dataIndex: 'created_at',
      render: (_, record) => {
        return (<p>{convertToLocalizedTime(record.created_at, 'YYYY-MM-DD HH:mm:ss')}</p>)
      }
    },
    {
      title: t('common.creator'),
      key: 'creator',
      dataIndex: 'creator',
    },
    {
      title: t('common.status'),
      key: 'status',
      dataIndex: 'status',
      render: (_, record: TrainJob) => {
        return record.status ? (<Tag color={getStatusColor(record.status, TrainStatus)} className=''>
          {t(`traintask.${getStatusText(record.status, TrainText)}`)}
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
          <Button
            type="link"
            className="mr-[10px]"
            onClick={() => handleEdit(record)}
          >
            {t('common.edit')}
          </Button>
          <Button
            type="link"
            className="mr-[10px]"
            onClick={() => openHistortDrawer(record)}
          >
            {t('traintask.history')}
          </Button>
          <Popconfirm
            title={t('traintask.deleteTraintask')}
            okText={t('common.confirm')}
            cancelText={t('common.cancel')}
            onConfirm={() => onDelete(record)}
          >
            <Button type="link">{t('common.delete')}</Button>
          </Popconfirm>
        </>
      ),
    },
  ];

  const Topsection = useMemo(() => {
    const name = path.split('/')[2];
    console.log(name);

    return (
      <div className="flex flex-col h-[90px] p-4 overflow-hidden">
        <h1 className="text-lg w-full truncate mb-1">{t('traintask.traintask')}</h1>
        <p className="text-sm overflow-hidden w-full min-w-[1000px] mt-[8px]">
          {t('traintask.description')}
        </p>
      </div>
    );
  }, [t]);

  const Intro = useMemo(() => {
    return (
      <div className="flex h-[58px] flex-row items-center">
        <Icon
          type="yunquyu"
          className="h-16 w-16"
          style={{ height: '36px', width: '36px' }}
        ></Icon>
        <h1 className="ml-2 text-center truncate">{t(`traintask.traintask`)}</h1>
      </div>
    );
  }, []);

  useEffect(() => {
    getTasks();
  }, [pagination.current, pagination.pageSize]);

  const getTasks = async (search: string = '') => {
    setLoading(true);
    try {
      const [{ items, count }, history] = await Promise.all([
        fetchTaskList(search, pagination.current, pagination.pageSize),
        fetchHistory(),
      ]);
      const _data = items?.map((item: any) => ({
        id: item.id,
        name: item.name,
        type: 'anomaly',
        dataset_id: item.dataset_id,
        train_data_id: item.train_data_id,
        created_at: item.created_at,
        creator: item?.created_by || '--',
        status: item?.status || '--',
        user_id: item.user_id
      })) || [];
      setTableData(_data as TrainJob[]);
      setHistoryData(history || []);
      setPagination(prev => ({
        ...prev,
        total: count,
      }));
    } catch (e) {
      console.log(e);
    } finally {
      setLoading(false);
    }
  };

  const fetchTaskList = useCallback(async (search: string = '', page: number = 1, pageSize: number = 10) => {
    console.log(search)
    const { count, items } = await getAnomalyTaskList({
      page,
      page_size: pageSize
    });
    return {
      items,
      count
    }
  }, [getAnomalyTaskList]);

  const fetchHistory = async () => {
    const data = [
      {
        "id": 4,
        "tenant_id": 1,
        "job_id": 5,
        "train_data_id": 17,
        "parameters": "{\"n_estimators\":100,\"max_samples\":\"auto\",\"contamination\":\"auto\",\"max_features\":1,\"bootstrap\":\"False\",\"n_jobs\":\"None\",\"random_state\":\"None\",\"verbose\":0,\"warm_start\":\"False\"}",
        "status": "in_progress",
        "model_path": null,
        "metrics": null,
        "created_at": "2025-06-20T01:43:12.184148+00:00",
        "updated_at": "2025-06-20T01:43:12.184148+00:00",
        "started_at": TrainStatus.pending,
        "completed_at": '',
        "user_id": "7440ea1e-3048-4fba-bc63-102878a5ed5f",
        "anomaly_detection_train_jobs": {
          "name": "test"
        }
      }
    ];
    return data;
  };



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

  const openHistortDrawer = (record: TrainJob) => {
    setSelectId(record.id as number);
    setOpen(true);
  };

  const handleChange = (value: any) => {
    setPagination(value);
  };

  const onSearch = (search: string) => {
    getTasks(search);
  };

  const onDelete = async (record: TrainJob) => {
    try {
      await deleteAnomalyTrainTask(record.id as string)
    } catch (e) {
      console.log(e);
    } finally {
      message.success(t('common.successfullyDeleted'));
      getTasks();
    }
  };

  const onCancel = () => {
    setOpen(false);
  };

  return (
    <>
      <div>
        <SubLayout
          topSection={Topsection}
          intro={Intro}
        >
          <div className="flex justify-end items-center mb-4 gap-2">
            <div className="flex">
              <Search
                className="w-[240px] mr-1.5"
                placeholder={t('traintask.searchText')}
                enterButton
                onSearch={onSearch}
                style={{ fontSize: 15 }}
              />
              <Button type="primary" icon={<PlusOutlined />} className="rounded-md text-xs shadow" onClick={() => handleAdd()}>
                {t('common.add')}
              </Button>
            </div>
          </div>
          <div className="flex-1 relative">
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
        </SubLayout>
      </div>
      <TrainTaskModal ref={modalRef} onSuccess={() => getTasks()} />
      <TrainTaskDrawer open={open} selectId={selectId} onCancel={onCancel} historyData={historyData} />
    </>
  );
};

export default TrainTask;
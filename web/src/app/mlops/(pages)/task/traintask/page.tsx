'use client'
import { useState, useEffect, useRef, useCallback } from 'react';
// import { useRouter } from 'next/navigation';
import { useLocalizedTime } from "@/hooks/useLocalizedTime";
import { getName } from '@/app/mlops/utils/common';
import { Button, Input, Popconfirm, message, Tag } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import CustomTable from '@/components/custom-table';
import TrainTaskModal from './traintaskModal';
import TrainTaskDrawer from './traintaskDrawer';
import { useTranslation } from '@/utils/i18n';
import { ModalRef, ColumnItem, TrainJob, TrainTaskHistory, DataSet, TrainData } from '@/app/mlops/types';
import { TrainStatus, TrainText } from '@/app/mlops/constants';
import SubLayout from '@/components/sub-layout';
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
  const modalRef = useRef<ModalRef>(null);
  const traindataRef = useRef<ModalRef>(null);
  const [user, setUser] = useState<any | null>(null);
  const [tableData, setTableData] = useState<TrainJob[]>([]);
  const [trainData, setTrainData] = useState<TrainData[]>([]);
  const [datasets, setDatasets] = useState<DataSet[]>([]);
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

  const Topsection = () => (
    <div className="flex flex-col h-[90px] p-4 overflow-hidden">
      <h1 className="text-lg w-full truncate mb-1">{t('traintask.traintask')}</h1>
      <p className="text-sm overflow-hidden w-full min-w-[1000px] mt-[8px]">
        {t('traintask.description')}
      </p>
    </div>
  );

  useEffect(() => {
    getTasks();
  }, [pagination.current, pagination.pageSize]);

  useEffect(() => {
    getTrainData();
    getCurrentUser();
  }, []);

  const getTrainStatus = useCallback((targetID: string | number, data: any[] | null) => {
    if (data) {
      const filterArr = data.filter((item) => item.job_id === targetID).sort((a, b) => a.updated_at - b.updated_at);
      const target = filterArr[filterArr.length - 1]?.status;
      return target || '';
    }
    return '';
  }, []);

  const getTasks = async (search: string = '') => {
    setLoading(true);
    try {
      const { data, count } = await fetchTaskList(search, pagination.current, pagination.pageSize);
      const history = (await fetchHistory()) || [];
      const datasets = await getDataSets();
      const users = [
        {
          "id": "b9bef85a-09b6-400f-8fe7-f907ae039900",
          "first_name": "li",
          "last_name": "zhen"
        },
        {
          "id": "783b097d-c279-4c9a-a782-bfcba387309f",
          "first_name": "li",
          "last_name": "zhen"
        },
        {
          "id": "7440ea1e-3048-4fba-bc63-102878a5ed5f",
          "first_name": "li",
          "last_name": "zhen"
        }
      ];
      const _data = data?.map((item: any) => ({
        id: item.id,
        name: item.name,
        type: 'anomaly',
        dataset_id: item.dataset_id,
        train_data_id: item.train_data_id,
        created_at: item.created_at,
        creator: getName(item?.user_id, users),
        status: getTrainStatus(item.id, history),
        user_id: item.user_id
      })) || [];
      setTableData(_data as TrainJob[]);
      setDatasets(datasets);
      setHistoryData(history);
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
    console.log(search, page, pageSize);
    const data = [
      {
        "id": 5,
        "tenant_id": 1,
        "name": "test",
        "description": null,
        "dataset_id": 10,
        "train_data_id": 17,
        "created_at": "2025-06-20T01:23:16.517196+00:00",
        "updated_at": "2025-06-20T01:23:16.517196+00:00",
        "user_id": "7440ea1e-3048-4fba-bc63-102878a5ed5f",
        "icon": '',
        "creator": ''
      }
    ];
    return {
      data,
      count: data.length || 0
    }
  }, []);

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
        "started_at": TrainStatus.not_started,
        "completed_at": '',
        "user_id": "7440ea1e-3048-4fba-bc63-102878a5ed5f",
        "anomaly_detection_train_jobs": {
          "name": "test"
        }
      }
    ];
    return data;
  };

  const getTrainData = async () => {
    console.log('get traindata')
    try {
      const data = [
        {
          "id": 15,
          "tenant_id": 1,
          "dataset_id": 10,
          "name": "anomaly_detection_train_randomforest.csv",
          "storage_path": "test2/anomaly_detection_train_randomforest.csv",
          "metadata": "{\"length\":24}",
          "created_at": "2025-06-10T08:07:08.429366+00:00",
          "updated_at": "2025-06-20T09:03:01.100214+00:00",
          "latest_status": "not_started",
          "latest_run_id": null,
          "user_id": "b9bef85a-09b6-400f-8fe7-f907ae039900"
        },
        {
          "id": 27,
          "tenant_id": 1,
          "dataset_id": 21,
          "name": "2025-06-11-16-55 Chronograf Data.csv",
          "storage_path": "21/2025-06-11-16-55 Chronograf Data.csv",
          "metadata": "{\"length\":20}",
          "created_at": "2025-06-13T07:35:15.164035+00:00",
          "updated_at": "2025-06-13T07:56:36.547247+00:00",
          "latest_status": "not_started",
          "latest_run_id": null,
          "user_id": "7440ea1e-3048-4fba-bc63-102878a5ed5f"
        },
        {
          "id": 28,
          "tenant_id": 1,
          "dataset_id": 5,
          "name": "template.csv",
          "storage_path": "5/template.csv",
          "metadata": null,
          "created_at": "2025-06-17T08:37:37.544231+00:00",
          "updated_at": "2025-06-17T08:37:37.544231+00:00",
          "latest_status": "not_started",
          "latest_run_id": null,
          "user_id": "7440ea1e-3048-4fba-bc63-102878a5ed5f"
        },
        {
          "id": 17,
          "tenant_id": 1,
          "dataset_id": 10,
          "name": "test2.csv",
          "storage_path": "test2/test2.csv",
          "metadata": null,
          "created_at": "2025-06-11T06:19:01.056813+00:00",
          "updated_at": "2025-06-11T06:19:01.056813+00:00",
          "latest_status": "not_started",
          "latest_run_id": null,
          "user_id": "b9bef85a-09b6-400f-8fe7-f907ae039900"
        },
        {
          "id": 18,
          "tenant_id": 1,
          "dataset_id": 11,
          "name": "test2.csv",
          "storage_path": "test3/test2.csv",
          "metadata": null,
          "created_at": "2025-06-13T05:43:39.88061+00:00",
          "updated_at": "2025-06-13T05:43:39.88061+00:00",
          "latest_status": "not_started",
          "latest_run_id": null,
          "user_id": "783b097d-c279-4c9a-a782-bfcba387309f"
        },
        {
          "id": 19,
          "tenant_id": 1,
          "dataset_id": 10,
          "name": "template.csv",
          "storage_path": "10/template.csv",
          "metadata": "{\"length\":3}",
          "created_at": "2025-06-13T06:01:26.545393+00:00",
          "updated_at": "2025-06-20T01:48:35.705002+00:00",
          "latest_status": "not_started",
          "latest_run_id": null,
          "user_id": "783b097d-c279-4c9a-a782-bfcba387309f"
        },
        {
          "id": 14,
          "tenant_id": 1,
          "dataset_id": 10,
          "name": "test1.csv",
          "storage_path": "test2/test1.csv",
          "metadata": "{\"length\":20}",
          "created_at": "2025-06-10T06:32:09.41403+00:00",
          "updated_at": "2025-06-20T01:51:04.029566+00:00",
          "latest_status": "not_started",
          "latest_run_id": null,
          "user_id": "b9bef85a-09b6-400f-8fe7-f907ae039900"
        },
        {
          "id": 16,
          "tenant_id": 1,
          "dataset_id": 10,
          "name": "anomaly_detection_train_unsupervised_iforest.csv",
          "storage_path": "test2/anomaly_detection_train_unsupervised_iforest.csv",
          "metadata": "{\"length\":164}",
          "created_at": "2025-06-10T09:23:03.570951+00:00",
          "updated_at": "2025-06-20T05:40:55.752972+00:00",
          "latest_status": "not_started",
          "latest_run_id": null,
          "user_id": "b9bef85a-09b6-400f-8fe7-f907ae039900"
        },
        {
          "id": 12,
          "tenant_id": 1,
          "dataset_id": 10,
          "name": "anomaly_detection_train_xgbod.csv",
          "storage_path": "test2/anomaly_detection_train_xgbod.csv",
          "metadata": "{\"length\":580}",
          "created_at": "2025-06-06T09:57:52.617701+00:00",
          "updated_at": "2025-06-20T06:49:44.306551+00:00",
          "latest_status": "not_started",
          "latest_run_id": null,
          "user_id": "b9bef85a-09b6-400f-8fe7-f907ae039900"
        }
      ]
      setTrainData(data);
      // if (!error) return setTrainData(data);
      // message.error(error.message);
    } catch (e) {
      console.log(e);
    }
  };

  const getDataSets = async () => {
    const data = [
      {
        "id": 10,
        "tenant_id": 1,
        "name": "test2",
        "description": "测试用例2",
        "has_labels": false,
        "created_at": "2025-05-27T06:08:50.051581+00:00",
        "updated_at": "2025-05-27T06:08:50.051581+00:00",
        "user_id": "b9bef85a-09b6-400f-8fe7-f907ae039900",
        "icon": '',
        "creator": ""
      },
      {
        "id": 11,
        "tenant_id": 1,
        "name": "test3",
        "description": "测试用例3",
        "has_labels": false,
        "created_at": "2025-05-27T06:55:02.078161+00:00",
        "updated_at": "2025-05-27T06:55:02.078161+00:00",
        "user_id": "b9bef85a-09b6-400f-8fe7-f907ae039900",
        "icon": '',
        "creator": ""
      },
      {
        "id": 5,
        "tenant_id": 1,
        "name": "test1",
        "description": "测试用例1",
        "has_labels": false,
        "created_at": "2025-05-27T01:13:03.453362+00:00",
        "updated_at": "2025-05-29T02:23:34.209342+00:00",
        "user_id": "b9bef85a-09b6-400f-8fe7-f907ae039900",
        "icon": '',
        "creator": ""
      },
      {
        "id": 21,
        "tenant_id": 1,
        "name": "信息部网络流出",
        "description": "信息部网络流出",
        "has_labels": false,
        "created_at": "2025-06-13T05:38:56.522515+00:00",
        "updated_at": "2025-06-13T05:38:56.522515+00:00",
        "user_id": "7440ea1e-3048-4fba-bc63-102878a5ed5f",
        "icon": '',
        "creator": ""
      }
    ];
    if (data) return data;
    return [];
  };

  const getCurrentUser = async () => {
    const user = {
      "id": "7440ea1e-3048-4fba-bc63-102878a5ed5f",
      "aud": "authenticated",
      "role": "authenticated",
      "email": "nextbase@weops.com",
      "email_confirmed_at": "2025-06-12T09:36:03.669962Z",
      "phone": "",
      "confirmed_at": "2025-06-12T09:36:03.669962Z",
      "last_sign_in_at": "2025-06-24T08:08:11.57385Z",
      "app_metadata": {
        "perms": [
          "all",
          "profiles.edit"
        ],
        "provider": "email",
        "providers": [
          "email"
        ],
        "tenant_id": 1
      },
      "user_metadata": {
        "email_verified": true
      },
      "identities": [
        {
          "identity_id": "90d77f75-7f98-487d-90a4-7e967bef20c7",
          "id": "7440ea1e-3048-4fba-bc63-102878a5ed5f",
          "user_id": "7440ea1e-3048-4fba-bc63-102878a5ed5f",
          "identity_data": {
            "email": "nextbase@weops.com",
            "email_verified": false,
            "phone_verified": false,
            "sub": "7440ea1e-3048-4fba-bc63-102878a5ed5f"
          },
          "provider": "email",
          "last_sign_in_at": "2025-06-12T09:36:03.664676Z",
          "created_at": "2025-06-12T09:36:03.664735Z",
          "updated_at": "2025-06-12T09:36:03.664735Z",
          "email": "nextbase@weops.com"
        }
      ],
      "created_at": "2025-06-12T09:36:03.652433Z",
      "updated_at": "2025-06-24T08:27:39.018094Z",
      "is_anonymous": false
    };
    setUser(user);
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

  const onTrainStart = (record: any) => {
    if (traindataRef.current) {
      traindataRef.current.showModal({ type: '', form: record });
    }
  };

  const openHistortDrawer = (record: TrainJob) => {
    setSelectId(record.id as number);
    setOpen(true);
  }

  const handleChange = (value: any) => {
    setPagination(value);
  };

  const onSearch = (search: string) => {
    getTasks(search);
  };

  const onDelete = async (record: TrainJob) => {
    try {
      const _data = tableData.filter((item) => item.id !== record.id);
      setTableData(_data);
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
          topSection={<Topsection />}
          intro={<></>}
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
      <TrainTaskModal
        ref={modalRef}
        user={user}
        datasets={datasets}
        trainData={trainData}
        onSuccess={() => getTasks()}
      />
      <TrainTaskDrawer open={open} selectId={selectId} onCancel={onCancel} historyData={historyData} trainData={trainData} />
      {/* <TrainDataModal ref={traindataRef} user={user} trainData={trainData} onSuccess={() => getTasks()} /> */}
    </>
  );
};

export default TrainTask;
import { Button, Drawer, message, TablePaginationConfig, Tag } from "antd";
import { ColumnItem } from "@/app/mlops/types";
import { TrainTaskHistory } from "@/app/mlops/types/task";
import CustomTable from "@/components/custom-table";
import { useTranslation } from "@/utils/i18n";
import useMlopsTaskApi from "@/app/mlops/api/task";
import { useState, useCallback, useMemo, useEffect } from "react";
import { TRAIN_STATUS_MAP, TRAIN_TEXT } from '@/app/mlops/constants';

const getStatusColor = (value: string, TrainStatus: Record<string, string>) => {
  return TrainStatus[value] || '';
};

const getStatusText = (value: string, TrainText: Record<string, string>) => {
  return TrainText[value] || '';
};

const TrainTaskDrawer = ({ open, onCancel, selectId }:
  {
    open: boolean,
    onCancel: () => void,
    selectId: number | null
  }) => {
  const { t } = useTranslation();
  const { getOneAnomalyTask } = useMlopsTaskApi();
  const [historyData, setHistoryData] = useState<TrainTaskHistory[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [pagination, setPagination] = useState({
    current: 1,
    total: 1,
    pageSize: 10,
  });

  useEffect(() => {
    if(open) {
      getHisttoryData(selectId as number)
    }
  }, [open])

  // 使用 useCallback 缓存 renderColumns 函数
  const renderColumns = useCallback((params: object) => {
    const data = Object.keys(params);
    return data.map((value, index) => ({
      title: value,
      key: `param-${value}-${index}`, // 确保 key 唯一
      dataIndex: value,
    }));
  }, []);

  // 使用 useCallback 缓存 expandedRowRender 函数
  const expandedRowRender = useCallback((record: any) => {
    return (
      <CustomTable
        rowKey="key"
        loading={record.loading}
        columns={renderColumns(record.parameters)}
        dataSource={[{ ...record.parameters, key: `params-${record.id}` }]}
        pagination={false}
        size="small"
      />
    );
  }, [renderColumns]);

  // 使用 useMemo 缓存 expandable 配置
  const expandableConfig = useMemo(() => ({
    expandedRowRender,
    rowExpandable: (record: any) => record.parameters && Object.keys(record.parameters).length > 0,
  }), [expandedRowRender]);

  const columns: ColumnItem[] = useMemo(() => [
    {
      title: t('common.name'),
      dataIndex: 'name',
      key: 'name',
      width: 120
    },
    {
      title: t('mlops-common.type'),
      dataIndex: 'type',
      key: 'type',
      width: 120,
      render: (_, record) => (<p>{record?.type ? t(`datasets.${record.type}`) : '--'}</p>),
    },
    {
      title: t('traintask.executionTime'),
      dataIndex: 'started_at',
      key: 'started_at',
      align: 'center',
      width: 150,
      render: (_, record) => (<p>{record?.started_at ? new Date(record?.started_at).toLocaleString() : '--'}</p>),
    },
    {
      title: t('traintask.executionStatus'),
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (_, record: TrainTaskHistory) => {
        return record.status ? (<Tag color={getStatusColor(record.status, TRAIN_STATUS_MAP)} className=''>
          {t(`traintask.${getStatusText(record.status, TRAIN_TEXT)}`)}
        </Tag>) : (<p>--</p>)
      }
    },
    {
      title: t('traintask.executionScore'),
      dataIndex: 'score',
      key: 'score',
      width: 100,
      render: (_, record) => (<p>{record?.score ? record?.score.toFixed(4) : '--'}</p>),
    },
    {
      title: t('traintask.traindata'),
      dataIndex: 'train_data_id',
      key: 'train_data_id',
      width: 100,
      render: () => (<p>{'--'}</p>)
    },
    {
      title: t('traintask.algorithms'),
      dataIndex: 'algorithms',
      key: 'algorithms',
      width: 100
    },
    {
      title: t('common.action'),
      dataIndex: 'action',
      key: 'action',
      width: 120,
      align: 'center',
      render: () => (
        <Button
          type="link"
          size="small"
        >
          {t('traintask.modelDownload')}
        </Button>
      ),
    }
  ], [t]);

  const getHisttoryData = async (id: number) => {
    setLoading(true);
    try {
      const data = await getOneAnomalyTask(id);
      setHistoryData(data);
    }catch (e) {
      console.log(e);
      message.error(t(`common.error`))
    } finally {
      setLoading(false);
    }
  };

  const processedData = useMemo(() => {
    if (selectId === null) return [];
    if (historyData) {
      const processedData = historyData.filter((item) => item.job_id === selectId).map((item, index) => ({
        ...item,
        key: `history-${item.id || index}`, // 确保每行有唯一 key
        type: 'anomaly',
        parameters: item.parameters ? JSON.parse(item.parameters) : {},
        name: item.anomaly_detection_train_jobs?.name || '',
        loading: false, // 修正字段名
      }));

      return processedData.length ? processedData.slice(
        (pagination.current! - 1) * pagination.pageSize!,
        pagination.current! * pagination.pageSize!
      ) : [];
    }
  }, [historyData, pagination.current, pagination.pageSize, selectId]);

  const onChange = (value: TablePaginationConfig) => {
    setPagination((prev) => ({
      ...prev,
      current: value?.current || 1,
      pageSize: value?.pageSize || 10
    }));
  };

  return (
    <Drawer
      width={800}
      title={t('traintask.history')}
      open={open}
      onClose={onCancel}
      footer={
        <Button onClick={onCancel}>
          {t('common.cancel')}
        </Button>
      }
    >
      <CustomTable
        rowKey="key"
        scroll={{ y: 'calc(100vh - 280px)' }}
        loading={loading}
        columns={columns}
        dataSource={processedData}
        expandable={expandableConfig}
        pagination={pagination}
        onChange={onChange}
      />
    </Drawer>
  );
};

export default TrainTaskDrawer;
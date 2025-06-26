import { useCallback, useState, useMemo, useRef, useEffect } from "react";
import { useSearchParams, useRouter } from 'next/navigation';
import useMlopsApi from '@/app/mlops/api';
import CustomTable from "@/components/custom-table";
import UploadModal from "./uploadModal";
import { Input, Button, Popconfirm, Tag } from "antd";
import { useTranslation } from "@/utils/i18n";
import { TypeContent } from "@/app/mlops/constants";
import { ColumnItem, ModalRef, Pagination, TableData } from '@/app/mlops/types';
const { Search } = Input;

const AnomalyDetail = () => {
  const { t } = useTranslation();
  const searchParams = useSearchParams();
  const router = useRouter();
  const { getAnomalyTrainData, deleteAnomalyTrainData } = useMlopsApi();
  const modalRef = useRef<ModalRef>(null);
  const [tableData, setTableData] = useState<TableData[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [confirmLoading, setConfirmLoading] = useState<boolean>(false);
  const [pagination, setPagination] = useState<Pagination>({
    current: 1,
    total: 0,
    pageSize: 10,
  });

  const {
    folder_id,
    folder_name,
    description
  } = useMemo(() => ({
    folder_id: searchParams.get('folder_id'),
    folder_name: searchParams.get('folder_name') || '',
    description: searchParams.get('description') || ''
  }), [searchParams]);

  const columns: ColumnItem[] = useMemo(() => [
    {
      title: t('common.name'),
      key: 'name',
      dataIndex: 'name',
    },
    {
      title: t('datasets.anomalyTitle'),
      key: 'count',
      dataIndex: 'count',
    },
    {
      title: t('datasets.trainFileType'),
      key: 'type',
      dataIndex: 'type',
      render(_, record) {
        const activeTypes = Object.entries(record.type)
          .filter(([, value]) => value === true)
          .map(([key]) => <Tag key={key}>{t(`datasets.${TypeContent[key]}`)}</Tag>);
        return (
          <>
            {activeTypes.length ? activeTypes : '--'}
          </>
        )
      },
    },
    {
      title: t('common.action'),
      key: 'action',
      dataIndex: 'action',
      width: 200,
      fixed: 'right',
      render: (_: unknown, record) => (
        <>
          <Button
            type="link"
            className="mr-[10px]"
            onClick={() => toAnnotation(record)}
          >
            {t('datasets.annotate')}
          </Button>
          <Popconfirm
            title={t('datasets.deleteTitle')}
            description={t('datasets.deleteContent')}
            okText={t('common.confirm')}
            cancelText={t('common.cancel')}
            okButtonProps={{ loading: confirmLoading }}
            onConfirm={() => onDelete(record)}
          >
            <Button type="link">
              {t('common.delete')}
            </Button>
          </Popconfirm>
        </>
      ),
    },
  ], [t]);

  useEffect(() => {
    getDataset();
  }, [pagination.current, pagination.pageSize]);

  const onSearch = (search: string) => {
    getDataset(search);
  };

  const getDataset = useCallback(async (search: string = '') => {
    setLoading(true);
    try {
      console.log(search);
      const { count, items } = await getAnomalyTrainData({
        dataset: folder_id as string,
        page: pagination.current,
        page_size: pagination.pageSize
      });
      const _tableData = items?.map((item: any) => {
        return {
          id: item?.id,
          name: item?.id,
          dataset: item?.dataset,
          count: item?.anomaly_point_count,
          type: {
            is_test_data: item?.is_test_data,
            is_train_data: item?.is_train_data,
            is_val_data: item?.is_val_data
          }
        }
      })
      setTableData(_tableData as TableData[]);
      setPagination((prev) => {
        return {
          ...prev,
          total: count || 0
        }
      });
    }
    catch (e) { console.log(e) }
    finally { setLoading(false); }
  }, [t, searchParams]);

  const onUpload = () => {
    const data = {
      dataset_id: folder_id,
      folder: folder_name,
    };
    modalRef.current?.showModal({ type: 'edit', form: data });
  };

  const onDelete = async (data: any) => {
    setConfirmLoading(true);
    try {
      await deleteAnomalyTrainData(data.id);
    } catch (e) {
      console.log(e);
    } finally {
      setConfirmLoading(false);
      getDataset();
    }
  };

  const toAnnotation = (data: any) => {
    router.push(`/mlops/manage/annotation?id=${data.id}&folder_id=${folder_id}&folder_name=${folder_name}&description=${description}`);
  };

  const handleChange = (value: any) => {
    setPagination(value);
  };

  return (
    <>
      <div className="flex justify-end items-center mb-4 gap-2">
        <div className='flex'>
          <Search
            className="w-[240px] mr-1.5"
            placeholder={t('common.search')}
            enterButton
            onSearch={onSearch}
            style={{ fontSize: 15 }}
          />
          <Button type="primary" className="rounded-md text-xs shadow" onClick={onUpload}>
            {t("datasets.upload")}
          </Button>
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
      <UploadModal ref={modalRef} onSuccess={() => getDataset()} />
    </>
  )
};

export default AnomalyDetail;
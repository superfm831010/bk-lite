'use client';
import { useState, useMemo, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";
import useMlopsTaskApi from "@/app/mlops/api/task";
import useMlopsModelReleaseApi from "@/app/mlops/api/modelRelease";
import CustomTable from "@/components/custom-table";
import Icon from "@/components/icon";
import { useTranslation } from "@/utils/i18n";
import { Button, Popconfirm, Tag, message } from "antd";
import { PlusOutlined } from '@ant-design/icons';
import SubLayout from '@/components/sub-layout';
import ReleaseModal from "./releaseModal";
import { ModalRef, Option, Pagination, TableData } from "@/app/mlops/types";
import { ColumnItem } from "@/types";
import { TrainJob } from "@/app/mlops/types/task";


const ModelRelease = () => {
  const { t } = useTranslation();
  const router = useRouter();
  const { getAnomalyTaskList } = useMlopsTaskApi();
  const { getAnomalyServingsList, deleteAnomalyServing } = useMlopsModelReleaseApi();
  const modalRef = useRef<ModalRef>(null);
  const [trainjobs, setTrainjobs] = useState<Option[]>([]);
  const [tableData, setTableData] = useState<TableData[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [pagination, setPagination] = useState<Pagination>({
    current: 1,
    total: 0,
    pageSize: 20
  });

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

  const columns: ColumnItem[] = [
    {
      title: t(`model-release.modelName`),
      dataIndex: 'name',
      key: 'name'
    },
    {
      title: t(`model-release.modelDescription`),
      dataIndex: 'description',
      key: 'description'
    },
    {
      title: t(`model-release.publishStatus`),
      dataIndex: 'status',
      key: 'status',
      render: (_, record) => (
        <Tag color={record.status === 'active' ? 'success' : 'default'}>{t(`model-release.${record.status}`)}</Tag>
      )
    },
    {
      title: t(`common.action`),
      dataIndex: 'action',
      key: 'action',
      width: 180,
      render: (_, record: TableData) => (<>
        <Button type="link" className="mr-2" onClick={() => handleEdit(record)}>{t(`common.edit`)}</Button>
        <Popconfirm
          title={t(`model-release.delModel`)}
          description={t(`model-release.delModelContent`)}
          okText={t('common.confirm')}
          cancelText={t('common.cancel')}
          onConfirm={() => handleDelete(record.id)}
        >
          <Button type="link" danger>{t(`common.delete`)}</Button>
        </Popconfirm>
      </>)
    }
  ];

  const Topsection = () => {
    return (
      <div className="flex flex-col h-[90px] p-4 overflow-hidden">
        <h1 className="text-lg truncate w-full mb-1">{t('model-release.title')}</h1>
        <p className="text-sm overflow-hidden w-full min-w-[1000px] mt-[8px]">
          {t('model-release.detail')}
        </p>
      </div>
    )
  };

  useEffect(() => {
    getModelServings();
  }, [])

  const publish = (record: any) => {
    modalRef.current?.showModal({ type: 'add', form: record })
  };

  const handleEdit = (record: any) => {
    modalRef.current?.showModal({type: 'edit', form: record});
  };

  const getModelServings = async () => {
    setLoading(true);
    try {
      const params = {
        page: pagination.current,
        page_size: pagination.pageSize,
      };
      const [taskList, { count, items }] = await Promise.all([getAnomalyTaskList({}), getAnomalyServingsList(params)]);
      const _data = taskList.map((item: TrainJob) => ({
        label: item.name,
        value: item.id
      }));
      setTrainjobs(_data);
      setTableData(items);
      setPagination((prev) => ({
        ...prev,
        total: count
      }));
    } catch (e) {
      console.log(e);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteAnomalyServing(id);
      getModelServings();
    } catch (e) {
      console.log(e);
      message.error(t(`common.delFailed`));
    }
  };


  return (
    <div className="w-full relative">
      <SubLayout
        topSection={<Topsection />}
        intro={Intro}
        onBackButtonClick={() => router.back()}
      >
        <div className="flex justify-end mb-2">
          <Button type="primary" icon={<PlusOutlined />} onClick={() => publish({})}>{t(`model-release.modelRelease`)}</Button>
        </div>
        <div className="flex-1 relative">
          <div className="absolute w-full">
            <CustomTable
              scroll={{ x: '100%', y: 'calc(100vh - 420px)' }}
              columns={columns}
              dataSource={tableData}
              loading={loading}
              rowKey='id'
              pagination={pagination}
            />
          </div>
        </div>
      </SubLayout>
      <ReleaseModal ref={modalRef} trainjobs={trainjobs} onSuccess={() => getModelServings()} />
    </div>
  )
};

export default ModelRelease;
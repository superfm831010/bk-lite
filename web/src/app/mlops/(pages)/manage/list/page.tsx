"use client";
import React, { useState, useRef, useEffect, useCallback, useMemo } from 'react';
import { useTranslation } from '@/utils/i18n';
import { useRouter } from 'next/navigation';
import useMlopsManageApi from '@/app/mlops/api/manage';
import {
  Popconfirm,
  message,
  Button,
  Input
} from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import Icon from '@/components/icon';
import CustomTable from '@/components/custom-table';
import DatasetModal from './dataSetsModal';
import SubLayout from '@/components/sub-layout';
// import PermissionWrapper from '@/components/permission';
import { ColumnItem, ModalRef, Pagination } from '@/app/mlops/types';
import { DataSet } from '@/app/mlops/types/manage';
import sideMenuStyle from './index.module.scss';
const { Search } = Input;

const DatasetManagePage = () => {
  const { t } = useTranslation();
  const router = useRouter();
  const { deleteAnomalyDatasets, getAnomalyDatasetsList } = useMlopsManageApi();
  const [datasets, setDatasets] = useState<DataSet[]>([]);
  const [pagination, setPagination] = useState<Pagination>({
    current: 1,
    total: 0,
    pageSize: 20
  });
  const [loading, setLoading] = useState<boolean>(false);
  const [confirmLoading, setConfirmLoading] = useState<boolean>(false);
  const modalRef = useRef<ModalRef>(null);
  const activeTab = 'anomaly';
  const datasetTypes = [
    { key: 'anomaly', value: 'anomaly', label: t('datasets.anomaly') },
    // { key: 'forecast', value: 'forecast', label: t('datasets.forecast') },
    // { key: 'log', value: 'log', label: t('datasets.log') },
  ];

  const columns: ColumnItem[] = [
    {
      title: t(`common.name`),
      dataIndex: 'name',
      key: 'name'
    },
    {
      title: t(`common.description`),
      dataIndex: 'description',
      key: 'description'
    },
    {
      title: t(`common.creator`),
      dataIndex: 'creator',
      key: 'creator'
    },
    {
      title: t(`common.action`),
      dataIndex: 'action',
      key: 'action',
      render: (_, record) => (
        <>
          <Button
            type="link"
            className="mr-[10px]"
            onClick={() => navigateToNode(record)}
          >
            {t('common.detail')}
          </Button>
          <Button
            type="link"
            className="mr-[10px]"
            onClick={() => handleOpenModal('edit', 'editform', record)}
          >
            {t('common.edit')}
          </Button>
          <Popconfirm
            title={t('datasets.delDataset')}
            description={t('datasets.delDatasetInfo')}
            okText={t('common.confirm')}
            cancelText={t('common.cancel')}
            okButtonProps={{ loading: confirmLoading }}
            onConfirm={() => handleDelete(record)}
          >
            <Button type="link" danger>
              {t('common.delete')}
            </Button>
          </Popconfirm>
        </>
      )
    }
  ];

  const Topsection = useMemo(() => {
    return (
      <div className="flex flex-col h-[90px] p-4 overflow-hidden">
        <h1 className="text-lg w-full truncate mb-1">{t('datasets.datasets')}</h1>
        <p className="text-sm overflow-hidden w-full min-w-[1000px] mt-[8px]">
          {t('traintask.description')}
        </p>
      </div>
    )
  }, [t]);

  const Intro = useMemo(() => {
    return (
      <div className="flex h-[58px] flex-row items-center">
        <Icon
          type="yunquyu"
          className="h-16 w-16"
          style={{ height: '36px', width: '36px' }}
        ></Icon>
        <h1 className="ml-2 text-center truncate">{t(`datasets.datasets`)}</h1>
      </div>
    )
  }, [t]);

  useEffect(() => {
    getDataSets();
  }, [])

  const getDataSets = useCallback(async () => {
    setLoading(true);
    try {
      if (activeTab === 'anomaly') {
        const data = await getAnomalyDatasetsList({ page: 1, page_size: -1 });
        const _data: DataSet[] = data?.map((item: any) => {
          return {
            id: item.id,
            name: item.name,
            description: item.description || '--',
            icon: 'chakanshuji',
            creator: item?.created_by || '--',
            tenant_id: item.tenant_id
          }
        }) || [];
        setDatasets(_data);
        setPagination(prev => ({
          ...prev,
          total: _data.length
        }));
      } else {
        setDatasets([]);
      }
    } catch (e) {
      console.log(e);
    } finally {
      setLoading(false);
    }
  }, [activeTab]);

  const navigateToNode = (item: any) => {
    router.push(
      `/mlops/manage/detail?folder_id=${item?.id}&folder_name=${item.name}&description=${item.description}&activeTap=${activeTab}`
    );
  };

  const handleDelete = async (data: any) => {
    setConfirmLoading(true);
    try {
      await deleteAnomalyDatasets(data.id);
      message.success(t('common.successfullyDeleted'));
    } catch (e) {
      console.log(e)
    } finally {
      getDataSets();
      setConfirmLoading(false);
    }
  };

  const handleOpenModal = (type: string, title: string, form: any = {}) => {
    modalRef.current?.showModal({ type, title, form });
  };

  const onSearch = () => {
    getDataSets();
  };

  return (
    <div className={`w-full`}>
      <SubLayout
        topSection={Topsection}
        intro={Intro}
        onBackButtonClick={() => router.back()}
        showBackButton={false}
      >
        <div className={`flex justify-end w-full ${sideMenuStyle.segmented}`}>
          <Search
            className="w-[240px] mr-1.5"
            placeholder={t('common.search')}
            enterButton
            onSearch={onSearch}
            style={{ fontSize: 15 }}
          />
          <Button type="primary" icon={<PlusOutlined />} className="rounded-md text-xs shadow mr-2" onClick={() => handleOpenModal('add', 'addform', {})}>
            {t('common.add')}
          </Button>
        </div>
        <CustomTable
          rowKey="id"
          className="mt-3"
          scroll={{ x: '100%', y: 'calc(100vh - 420px)' }}
          dataSource={datasets}
          columns={columns}
          pagination={pagination}
          loading={loading}
        />
      </SubLayout>
      <DatasetModal
        ref={modalRef}
        options={datasetTypes}
        onSuccess={getDataSets}
      />
    </div>
  );
};

export default DatasetManagePage;

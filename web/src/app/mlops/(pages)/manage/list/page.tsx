"use client";
import React, { useState, useRef, useEffect, useCallback } from 'react';
import { useTranslation } from '@/utils/i18n';
import { useRouter } from 'next/navigation';
import useMlopsManageApi from '@/app/mlops/api/manage';
import {
  message,
  Button,
  Menu,
  Modal,
  Tree
} from 'antd';
import type { TreeDataNode } from 'antd';
import DatasetModal from './dataSetsModal';
import PageLayout from '@/components/page-layout';
import TopSection from '@/components/top-section';
import EntityList from '@/components/entity-list';
import PermissionWrapper from '@/components/permission';
import { ModalRef } from '@/app/mlops/types';
import { DataSet } from '@/app/mlops/types/manage';
const { confirm } = Modal;

const DatasetManagePage = () => {
  const { t } = useTranslation();
  const router = useRouter();
  const { deleteAnomalyDatasets, getAnomalyDatasetsList } = useMlopsManageApi();
  const [datasets, setDatasets] = useState<DataSet[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [selectedKeys, setSelectedKeys] = useState<string[]>([]);
  const modalRef = useRef<ModalRef>(null);
  const activeTab = 'anomaly';
  const datasetTypes = [
    { key: 'anomaly', value: 'anomaly', label: t('datasets.anomaly') },
  ];

  const treeData: TreeDataNode[] = [
    {
      title: t(`datasets.datasets`),
      key: 'datasets',
      selectable: false,
      children: [
        {
          title: t(`datasets.anomaly`),
          key: 'anomaly',
        },
        {
          title: '日志',
          key: 'log'
        }
      ]
    }
  ];

  useEffect(() => {
    setSelectedKeys(['anomaly'])
  }, []);

  useEffect(() => {
    getDataSets();
  }, [selectedKeys])


  const getDataSets = useCallback(async () => {
    const [activeTab] = selectedKeys;
    if (!activeTab) return;
    setLoading(true);
    try {
      if (activeTab === 'anomaly') {
        const data = await getAnomalyDatasetsList({ page: 1, page_size: -1 });
        const _data: DataSet[] = data?.map((item: any) => {
          return {
            id: item.id,
            name: item.name,
            description: item.description || '--',
            icon: 'tucengshuju',
            creator: item?.created_by || '--',
            tenant_id: item.tenant_id
          }
        }) || [];
        setDatasets(_data);
      } else {
        setDatasets([]);
      }
    } catch (e) {
      console.log(e);
    } finally {
      setLoading(false);
    }
  }, [selectedKeys]);

  const navigateToNode = (item: any) => {
    router.push(
      `/mlops/manage/detail?folder_id=${item?.id}&folder_name=${item.name}&description=${item.description}&activeTap=${activeTab}`
    );
  };

  const handleDelete = async (id: number) => {
    confirm({
      title: t('datasets.delDataset'),
      content: t('datasets.delDatasetInfo'),
      okText: t('common.confirm'),
      cancelText: t('common.cancel'),
      onOk: async () => {
        try {
          await deleteAnomalyDatasets(id);
          message.success(t('common.delSuccess'));
        } catch (e) {
          console.log(e);
          message.error(t(`common.delFailed`));
        } finally {
          getDataSets();
        }
      }
    })
  };

  const handleOpenModal = (object: {
    type: string,
    title: string,
    form: any
  }) => {
    modalRef.current?.showModal(object);
  };

  const onSearch = () => {
    // getDataSets();
  };

  const infoText = (item: any) => {
    return <p className='text-right'>所有者: {item.creator}</p>;
  }

  const menuActions = (item: any) => {
    return (
      <Menu onClick={(e) => e.domEvent.preventDefault()}>
        <Menu.Item
          className="!p-0"
          onClick={() =>
            handleOpenModal({ title: 'editform', type: 'edit', form: item })
          }
        >
          <PermissionWrapper
            requiredPermissions={['Edit']}
            className="!block"
          >
            <Button type="text" className="w-full">
              {t(`common.edit`)}
            </Button>
          </PermissionWrapper>
        </Menu.Item>
        {item?.name !== "default" && (
          <Menu.Item
            className="!p-0"
            onClick={() =>
              handleDelete(item.id)
            }
          >
            <PermissionWrapper
              requiredPermissions={['Delete']}
              className="!block"
            >
              <Button type="text" className="w-full">
                {t(`common.delete`)}
              </Button>
            </PermissionWrapper>
          </Menu.Item>
        )}
      </Menu>
    )
  };

  const topSection = (
    <TopSection title={t('datasets.datasets')} content={t('traintask.description')} />
  );

  const leftSection = (
    <div className='w-full'>
      <Tree
        treeData={treeData}
        showLine
        selectedKeys={selectedKeys}
        onSelect={(keys) => setSelectedKeys(keys as string[])}
        defaultExpandedKeys={['datasets']}
      />
    </div>
  );

  const rightSection = (
    <div className='overflow-auto h-[calc(100vh-200px)] pb-2'>
      <EntityList
        data={datasets}
        menuActions={menuActions}
        loading={loading}
        onCardClick={navigateToNode}
        openModal={() => handleOpenModal({ type: 'add', title: 'addform', form: {} })}
        onSearch={onSearch}
        descSlot={infoText}
      />
    </div>
  );

  return (
    <>
      <PageLayout
        topSection={topSection}
        leftSection={leftSection}
        rightSection={rightSection}
      />
      <DatasetModal
        ref={modalRef}
        options={datasetTypes}
        onSuccess={getDataSets}
        activeTag={selectedKeys}
      />
    </>
  );
};

export default DatasetManagePage;

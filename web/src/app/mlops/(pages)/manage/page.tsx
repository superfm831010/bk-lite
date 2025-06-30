"use client";
import React, { useState, useRef, useEffect, useCallback } from 'react';
import { useTranslation } from '@/utils/i18n';
import { useRouter } from 'next/navigation';
// import { getName } from '@/app/mlops/utils/common';
import useMlopsApi from '@/app/mlops/api';
import {
  Segmented,
  Modal,
  Menu,
  message,
  Button
} from 'antd';
import EntityList from '@/components/entity-list';
import DatasetModal from './dataSetsModal';
import PermissionWrapper from '@/components/permission';
import { ModalRef, DataSet } from '@/app/mlops/types';
import sideMenuStyle from './index.module.scss';
const { confirm } = Modal;

const DatasetManagePage = () => {
  const { t } = useTranslation();
  const router = useRouter();
  const { deleteAnomalyDatasets, getAnomalyDatasetsList } = useMlopsApi();
  const [activeTab, setActiveTab] = useState<string>('anomaly');
  const [searchTerm, setSearchTerm] = useState<string>('');
  // const [filterValue, setFilterValue] = useState<string[]>([]);
  const [datasets, setDatasets] = useState<DataSet[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const modalRef = useRef<ModalRef>(null);

  const datasetTypes = [
    { key: 'anomaly', value: 'anomaly', label: t('datasets.anomaly') },
    // { key: 'forecast', value: 'forecast', label: t('datasets.forecast') },
    // { key: 'log', value: 'log', label: t('datasets.log') },
  ];

  const menuActions = (data: DataSet) => {
    return (
      <>
        <Menu onClick={(e) => e.domEvent.preventDefault()}>
          <Menu.Item
            className="!p-0"
            onClick={() => {
              handleOpenModal('edit', 'editform', data)
            }}
          >
            <PermissionWrapper
              requiredPermissions={['Edit']}
              className="!block"
            >
              <Button type="text" className="w-full">
                {t('common.edit')}
              </Button>
            </PermissionWrapper>
          </Menu.Item>
          <Menu.Item
            className="!p-0"
            onClick={() => handleDelete(data)}
          >
            <PermissionWrapper
              requiredPermissions={['Delete']}
              className="!block"
            >
              <Button type="text" className="w-full">
                {t('common.delete')}
              </Button>
            </PermissionWrapper>
          </Menu.Item>
        </Menu>
      </>
    );
  };

  useEffect(() => {
    console.log(searchTerm)
    if (!loading) {
      getDataSets();
    }
  }, [activeTab]);

  const getDataSets = useCallback(async () => {
    setLoading(true);
    try {
      if (activeTab === 'anomaly') {
        const data = await getAnomalyDatasetsList();
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
      } else {
        setDatasets([]);
      }
    } catch (e) {
      console.log(e)
    } finally {
      setLoading(false);
    }
  }, [activeTab]);

  const infoText = (item: any) => {
    console.log(item)
    return (<p className='text-right'>{`Created by: ${item.creator}`}</p>);
  };

  const navigateToNode = (item: any) => {
    router.push(
      `/mlops/manage/detail?folder_id=${item?.id}&folder_name=${item.name}&description=${item.description}&activeTap=${activeTab}`
    );
  };

  const handleTabChange = (key: string) => {
    setActiveTab(key);
    setSearchTerm('');
    // setFilterValue([]);
  };

  const handleDelete = (data: any) => {
    confirm({
      title: t(`datasets.delDataset`),
      content: t(`datasets.delDatasetInfo`),
      okText: t('common.confirm'),
      cancelText: t('common.cancel'),
      centered: true,
      onOk() {
        return new Promise(async (resolve) => {
          try {
            await deleteAnomalyDatasets(data.id);
            message.success(t('common.successfullyDeleted'));
          } catch (e) { console.log(e) }
          finally {
            getDataSets();
            return resolve(true);
          }
        })
      }
    });
  };

  const handleOpenModal = (type: string, title: string, form: any = {}) => {
    modalRef.current?.showModal({ type, title, form });
  };

  return (
    <div className={`p-4 w-full`}>
      <div className={`flex flex-col w-full ${sideMenuStyle.segmented}`}>
        <Segmented
          options={datasetTypes.map((type) => ({
            label: type.label,
            value: type.key,
          }))}
          value={activeTab}
          onChange={handleTabChange}
        />
      </div>
      <EntityList
        data={datasets}
        loading={loading}
        onSearch={setSearchTerm}
        menuActions={menuActions}
        openModal={() => handleOpenModal('add', 'addform')}
        descSlot={infoText}
        onCardClick={(item) => {
          navigateToNode(item);
        }}
      />
      <DatasetModal
        ref={modalRef}
        options={datasetTypes}
        onSuccess={getDataSets}
      />
    </div>
  );
};

export default DatasetManagePage;

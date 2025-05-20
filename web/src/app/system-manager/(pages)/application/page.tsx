'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { message, Menu, Button, Modal } from 'antd';
import { useTranslation } from '@/utils/i18n';
import EntityList from '@/components/entity-list';
import { useClientData } from '@/context/client';
import { ClientData } from '@/types/index';
import ApplicationFormModal from '@/app/system-manager/components/application/modify-applicaiton';

const ApplicationPage = () => {
  const { t } = useTranslation();
  const { getAll, loading } = useClientData();
  const [dataList, setDataList] = useState<ClientData[]>([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [isEdit, setIsEdit] = useState(false);
  const [currentItem, setCurrentItem] = useState<ClientData | null>(null);

  const loadItems = async (searchTerm = '') => {
    try {
      const data: ClientData[] = await getAll();
      
      const filteredData:ClientData[] = data.filter((item: ClientData) => item.name.toLowerCase().includes(searchTerm.toLowerCase()));
      setDataList(filteredData.filter((client: ClientData) => client.name !== 'ops-console').map((item: ClientData) => ({
        ...item,
        icon: item.name,
        is_build_in: item.is_build_in
      })));
    } catch {
      message.error(t('common.fetchFailed'));
    }
  };

  useEffect(() => {
    loadItems();
  }, [getAll]);

  const handleSearch = async (value: string) => {
    await loadItems(value);
  };

  const handleCardClick = (item: any) => {
    router.push(`/system-manager/application/manage?id=${item.id}&clientId=${item.name}`);
  };

  const router = useRouter();

  const handleAddNew = () => {
    setCurrentItem(null);
    setIsEdit(false);
    setModalVisible(true);
  };

  const handleEdit = (item: any) => {
    setCurrentItem(item);
    setIsEdit(true);
    setModalVisible(true);
  };

  const handleDelete = () => {
    Modal.confirm({
      title: t('common.confirmDelete'),
      content: t('common.deleteConfirmContent'),
      okText: t('common.confirm'),
      cancelText: t('common.cancel'),
      onOk: async () => {
        // try {
        //   await deleteClient(item.id);
        //   message.success(t('common.deleteSuccess'));
        //   loadItems();
        // } catch {
        //   message.error(t('common.deleteFailed'));
        // }
      }
    });
  };

  const handleModalClose = () => {
    setModalVisible(false);
  };

  const handleFormSuccess = () => {
    setModalVisible(false);
    loadItems();
  };

  const getMenuActions = (item: any) => {
    return (
      <Menu>
        <Menu.Item key="edit" disabled onClick={() => handleEdit(item)}>
          {t('common.edit')}
        </Menu.Item>
        {!item.is_build_in && (
          <Menu.Item key="delete" onClick={() => handleDelete()}>
            {t('common.delete')}
          </Menu.Item>
        )}
      </Menu>
    );
  };

  const addButton = (
    <Button type="primary" onClick={handleAddNew} className="ml-2" disabled>
      {t('common.add')}
    </Button>
  );

  return (
    <div className='w-full'>
      <EntityList
        data={dataList}
        loading={loading}
        onSearch={handleSearch}
        onCardClick={handleCardClick}
        menuActions={getMenuActions}
        operateSection={addButton}
      />
      
      <ApplicationFormModal 
        visible={modalVisible}
        initialData={
          currentItem
            ? {
              name: currentItem.name,
              display_name: currentItem.name,
              description: currentItem.description || '',
              url: currentItem.url || '',
              icon: currentItem.icon || null,
              tags: currentItem.tags || [],
            } : undefined
        }
        isEdit={isEdit}
        onClose={handleModalClose}
        onSuccess={handleFormSuccess}
      />
    </div>
  );
};

export default ApplicationPage;

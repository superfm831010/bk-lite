'use client';
import React, { useEffect, useRef, useState } from 'react';
import { FormInstance } from 'antd';
import useApiClient from '@/utils/request';
import { Menu } from 'antd';
import cloudRegionStyle from './index.module.scss';
import { useRouter } from 'next/navigation';
import { useTranslation } from '@/utils/i18n';
import useApiCloudRegion from '@/app/node-manager/api/cloudRegion';
import EntityList from '@/components/entity-list';
import PermissionWrapper from '@/components/permission';
import type {
  CloudRegionItem,
  CloudRegionCardProps,
} from '@/app/node-manager/types/cloudregion';
import CloudRegionModal from './cloudregionModal';
import { ModalRef } from '@/app/node-manager/types';

const CloudRegion = () => {
  const { t } = useTranslation();
  const { isLoading } = useApiClient();
  const { getCloudList } = useApiCloudRegion();
  const router = useRouter();
  const cloudRegionFormRef = useRef<FormInstance>(null);
  const modalRef = useRef<ModalRef>(null);
  const divRef = useRef(null);
  const [selectedRegion, setSelectedRegion] =
    useState<CloudRegionCardProps | null>(null);
  const [openEditCloudRegion, setOpenEditCloudRegion] = useState(false);
  const [cloudItems, setCloudItems] = useState<CloudRegionItem[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  // 获取相关的接口
  const fetchCloudRegions = async () => {
    setLoading(true);
    try {
      const data = await getCloudList();
      const regionData = (data || []).map((item: CloudRegionCardProps) => {
        item.description = item.introduction;
        item.icon = 'yunquyu';
        return item;
      });
      setCloudItems(regionData);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!isLoading) {
      fetchCloudRegions();
    }
  }, [isLoading]);

  useEffect(() => {
    if (openEditCloudRegion && selectedRegion) {
      cloudRegionFormRef.current?.setFieldsValue({
        cloudRegion: selectedRegion,
      });
    }
  }, [openEditCloudRegion, selectedRegion]);

  const handleEdit = (row: any) => {
    openModal({
      title: 'editform',
      type: 'edit',
      form: row
    })
    setSelectedRegion(row);
    setOpenEditCloudRegion(true);
  };

  const navigateToNode = (item: CloudRegionItem) => {
    router.push(
      `/node-manager/cloudregion/node?cloud_region_id=1&name=${item.name}`
    );
  };

  const openModal = (config: any) => {
    modalRef.current?.showModal({
      title: config?.title,
      type: config?.type,
      form: config?.form,
    });
  };

  const handleSumbit = () => {
    fetchCloudRegions();
  }

  return (
    <div
      ref={divRef}
      className={`${cloudRegionStyle.cloudregion} w-full h-full`}
    >
      <EntityList
        data={cloudItems}
        loading={loading}
        menuActions={(row) => {
          return (
            <Menu>
              <PermissionWrapper requiredPermissions={['Edit']}>
                <Menu.Item key="edit" onClick={() => handleEdit(row)}>
                  {t('common.edit')}
                </Menu.Item>
              </PermissionWrapper>
            </Menu>
          );
        }}
        openModal={() => {}}
        onCardClick={(item: CloudRegionItem) => {
          navigateToNode(item);
        }}
      ></EntityList>
      {/* 编辑默认云区域弹窗 */}
      <CloudRegionModal ref={modalRef} onSuccess={handleSumbit} />
    </div>
  );
};

export default CloudRegion;

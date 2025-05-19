'use client';
import React, { useEffect, useRef, useState } from 'react';
import { FormInstance, Input, message } from 'antd';
import OperateModal from '@/components/operate-modal';
import useApiClient from '@/utils/request';
import { Form, Menu } from 'antd';
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

const CloudRegion = () => {
  const { t } = useTranslation();
  const { isLoading } = useApiClient();
  const { getCloudList, updateCloudIntro } = useApiCloudRegion();
  const router = useRouter();
  const cloudRegionFormRef = useRef<FormInstance>(null);
  const divRef = useRef(null);
  const [selectedRegion, setSelectedRegion] =
    useState<CloudRegionCardProps | null>(null);
  const [openEditCloudRegion, setOpenEditCloudRegion] = useState(false);
  const [cloudItems, setCloudItems] = useState<CloudRegionItem[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [confirmLoading, setConfirmLoading] = useState<boolean>(false);

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

  const handleFormOkClick = async () => {
    setConfirmLoading(true);
    try {
      const { cloudRegion } = cloudRegionFormRef.current?.getFieldsValue();
      await updateCloudIntro(cloudRegion.id, {
        introduction: cloudRegion.introduction,
      });
      message.success(t('common.updateSuccess'));
      fetchCloudRegions();
      setOpenEditCloudRegion(false);
    } finally {
      setConfirmLoading(false);
    }
  };

  const handleEdit = (row: any) => {
    setSelectedRegion(row);
    setOpenEditCloudRegion(true);
  };

  const navigateToNode = (item: CloudRegionItem) => {
    router.push(
      `/node-manager/cloudregion/node?cloud_region_id=1&name=${item.name}`
    );
  };

  const handleCancel = () => {
    setOpenEditCloudRegion(false);
    setSelectedRegion(null);
    setConfirmLoading(false);
  };

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
      <OperateModal
        title={t('node-manager.cloudregion.editform.title')}
        open={openEditCloudRegion}
        okText={t('common.confirm')}
        cancelText={t('common.cancel')}
        confirmLoading={confirmLoading}
        onCancel={handleCancel}
        onOk={handleFormOkClick}
      >
        <Form layout="vertical" ref={cloudRegionFormRef} name="nest-messages">
          <Form.Item name={['cloudRegion', 'id']} hidden>
            <Input />
          </Form.Item>
          <Form.Item name={['cloudRegion', 'name']} label={t('common.name')}>
            <Input disabled placeholder={t('common.inputMsg')} />
          </Form.Item>
          <Form.Item
            name={['cloudRegion', 'introduction']}
            label={t('node-manager.cloudregion.editform.Introduction')}
          >
            <Input.TextArea rows={5} placeholder={t('common.inputMsg')} />
          </Form.Item>
        </Form>
      </OperateModal>
    </div>
  );
};

export default CloudRegion;

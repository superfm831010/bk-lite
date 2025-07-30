'use client';

import React, { useRef, useState, useEffect } from 'react';
import { Card, Modal, message } from 'antd';
import WithSideMenuLayout from '@/components/sub-layout';
import { useRouter } from 'next/navigation';
import { getIconUrl } from '@/app/cmdb/utils/common';
import Image from 'next/image';
import { EditTwoTone, DeleteTwoTone } from '@ant-design/icons';
import { useSearchParams } from 'next/navigation';
import ModelModal from '../list/modelModal';
import attrLayoutStyle from './layout.module.scss';
import useApiClient from '@/utils/request';
import { ClassificationItem } from '@/app/cmdb/types/assetManage';
import { useTranslation } from '@/utils/i18n';
import PermissionWrapper from '@/components/permission';

const AboutLayout = ({ children }: { children: React.ReactNode }) => {
  const { get, del, isLoading } = useApiClient();
  const { t } = useTranslation();
  const { confirm } = Modal;
  const router = useRouter();
  const searchParams = useSearchParams();
  const objIcon: string = searchParams.get('icn') || '';
  const modelName: string = searchParams.get('model_name') || '';
  const modelId: string = searchParams.get('model_id') || '';
  const classificationId: string = searchParams.get('classification_id') || '';
  const isPre = searchParams.get('is_pre') === 'true';
  const permissionParam = searchParams.get('permission');
  const modelPermission = permissionParam
    ? decodeURIComponent(permissionParam).split(',')
    : [];
  const modelRef = useRef<any>(null);
  const [groupList, setGroupList] = useState<ClassificationItem[]>([]);

  useEffect(() => {
    if (isLoading) return;
    getGroups();
  }, [isLoading, get]);

  const getGroups = async () => {
    try {
      const data = await get('/cmdb/api/classification/');
      setGroupList(data);
    } catch (error) {
      console.log(error);
    }
  };

  const onSuccess = (info: any) => {
    const currentPermission =
      modelPermission.length > 0 ? modelPermission.join(',') : '';
    const params = new URLSearchParams({
      icn: info.icn || objIcon,
      model_name: info.model_name,
      model_id: info.model_id,
      classification_id: info.classification_id,
      is_pre: info.is_pre || searchParams.get('is_pre') || 'false',
      permission: currentPermission,
    }).toString();
    router.replace(`/cmdb/assetManage/management/detail/attributes?${params}`);
  };

  const handleBackButtonClick = () => {
    router.push(`/cmdb/assetManage`);
  };

  const showDeleteConfirm = (row = { model_id: '' }) => {
    confirm({
      title: t('common.deleteTitle'),
      content: t('common.deleteContent'),
      centered: true,
      onOk() {
        return new Promise(async (resolve) => {
          try {
            await del(`/cmdb/api/model/${row.model_id}/`);
            message.success(t('successfullyDeleted'));
            router.push(`/cmdb/assetManage`);
          } finally {
            resolve(true);
          }
        });
      },
    });
  };

  const shoModelModal = (type: string, row = {}) => {
    const title = t(type === 'add' ? 'Model.addModel' : 'Model.editModel');
    modelRef.current?.showModal({
      title,
      type,
      modelForm: row,
      subTitle: '',
    });
  };

  return (
    <div className={`${attrLayoutStyle.attrLayout}`}>
      <Card style={{ width: '100%' }} className="mb-[20px]">
        <header className="flex items-center">
          <Image
            src={getIconUrl({ icn: objIcon, model_id: modelId })}
            className="block mr-[20px]"
            alt={t('picture')}
            width={30}
            height={30}
          />
          <div className="mr-[14px]">
            <div
              className={`text-[14px] font-[800] mb-[2px] ${attrLayoutStyle.ellipsisText} break-all`}
            >
              {modelName}
            </div>
            <div className="text-[var(--color-text-2)] text-[12px] break-all">
              {modelId}
            </div>
          </div>
          {!isPre && (
            <div className="self-start">
              <PermissionWrapper
                requiredPermissions={['Edit Model']}
                instPermissions={modelPermission}
              >
                <EditTwoTone
                  className="edit mr-[10px] text-[14px] cursor-pointer"
                  onClick={() =>
                    shoModelModal('edit', {
                      model_name: modelName,
                      model_id: modelId,
                      classification_id: classificationId,
                      icn: objIcon,
                    })
                  }
                />
              </PermissionWrapper>
              <PermissionWrapper
                requiredPermissions={['Delete Model']}
                instPermissions={modelPermission}
              >
                <DeleteTwoTone
                  className="delete text-[14px] cursor-pointer"
                  onClick={() =>
                    showDeleteConfirm({
                      model_id: modelId,
                    })
                  }
                />
              </PermissionWrapper>
            </div>
          )}
        </header>
      </Card>
      <div
        style={{
          height: 'calc(100vh - 244px)',
          ['--custom-height' as string]: 'calc(100vh - 244px)',
        }}
        className={attrLayoutStyle.attrLayout}
      >
        <WithSideMenuLayout
          showBackButton={true}
          onBackButtonClick={handleBackButtonClick}
        >
          {children}
        </WithSideMenuLayout>
      </div>
      <ModelModal ref={modelRef} groupList={groupList} onSuccess={onSuccess} />
    </div>
  );
};

export default AboutLayout;

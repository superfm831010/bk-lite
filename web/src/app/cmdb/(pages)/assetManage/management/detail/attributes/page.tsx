'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Input, Button, Modal, message } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import CustomTable from '@/components/custom-table';
import AttributesModal from './attributesModal';
import { Tag } from 'antd';
import type { TableColumnsType } from 'antd';
import { ATTR_TYPE_LIST } from '@/app/cmdb/constants/asset';
import { useTranslation } from '@/utils/i18n';
import PermissionWrapper from '@/components/permission';
import { useModelApi } from '@/app/cmdb/api';
import { useModelDetail } from '../context';

const Attributes: React.FC = () => {
  const { confirm } = Modal;
  const { t } = useTranslation();
  const modelDetail = useModelDetail();

  const { getModelAttrList, deleteModelAttr } = useModelApi();

  const modelId = modelDetail?.model_id;
  const modelPermission = modelDetail?.permission || [];
  const attrRef = useRef<any>(null);
  const [searchText, setSearchText] = useState<string>('');
  const [pagination, setPagination] = useState<any>({
    current: 1,
    total: 0,
    pageSize: 20,
  });
  const [loading, setLoading] = useState<boolean>(false);
  const [tableData, setTableData] = useState<any[]>([]);
  const columns: TableColumnsType = [
    {
      title: 'ID',
      dataIndex: 'attr_id',
      key: 'attr_id',
    },
    {
      title: t('name'),
      dataIndex: 'attr_name',
      key: 'attr_name',
    },
    {
      title: t('type'),
      dataIndex: 'attr_type',
      key: 'attr_type',
      render: (_, { attr_type }) => (
        <>
          {ATTR_TYPE_LIST.find((item) => item.id === attr_type)?.name || '--'}
        </>
      ),
    },
    {
      title: t('required'),
      key: 'is_required',
      dataIndex: 'is_required',
      render: (_, { is_required }) => (
        <>
          {
            <Tag color={is_required ? 'green' : 'geekblue'}>
              {t(is_required ? 'yes' : 'no')}
            </Tag>
          }
        </>
      ),
    },
    {
      title: t('editable'),
      key: 'editable',
      dataIndex: 'editable',
      render: (_, { editable }) => (
        <>
          {
            <Tag color={editable ? 'green' : 'geekblue'}>
              {t(editable ? 'yes' : 'no')}
            </Tag>
          }
        </>
      ),
    },
    {
      title: t('unique'),
      key: 'is_unique',
      dataIndex: 'is_unique',
      render: (_, { is_only }) => (
        <>
          {
            <Tag color={is_only ? 'green' : 'geekblue'}>
              {t(is_only ? 'yes' : 'no')}
            </Tag>
          }
        </>
      ),
    },
    {
      title: t('common.actions'),
      key: 'action',
      render: (_, record) => (
        <>
          <PermissionWrapper
            requiredPermissions={['Edit Model']}
            instPermissions={modelPermission}
          >
            <Button
              type="link"
              className="mr-[10px]"
              onClick={() => showAttrModal('edit', record)}
            >
              {t('common.edit')}
            </Button>
          </PermissionWrapper>
          <PermissionWrapper
            requiredPermissions={['Edit Model']}
            instPermissions={modelPermission}
          >
            <Button
              type="link"
              onClick={() =>
                showDeleteConfirm({
                  attr_id: record.attr_id,
                })
              }
            >
              {t('common.delete')}
            </Button>
          </PermissionWrapper>
        </>
      ),
    },
  ];

  useEffect(() => {
    if (modelId) {
      fetchData();
    }
  }, [pagination, modelId]);

  const showAttrModal = (type: string, row = {}) => {
    const title = t(
      type === 'add' ? 'Model.addAttribute' : 'Model.editAttribute'
    );
    attrRef.current?.showModal({
      title,
      type,
      attrInfo: row,
      subTitle: '',
    });
  };

  const showDeleteConfirm = (row = { attr_id: '' }) => {
    confirm({
      title: t('common.delConfirm'),
      content: t('common.delConfirmCxt'),
      okText: t('common.confirm'),
      cancelText: t('common.cancel'),
      centered: true,
      onOk() {
        return new Promise(async (resolve) => {
          try {
            await deleteModelAttr(modelId!, row.attr_id);
            message.success(t('successfullyDeleted'));
            if (pagination.current > 1 && tableData.length === 1) {
              pagination.current--;
            }
            fetchData();
          } finally {
            resolve(true);
          }
        });
      },
    });
  };

  const onSearchTxtChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchText(e.target.value);
  };

  const onTxtPressEnter = () => {
    pagination.current = 1;
    setPagination(pagination);
    fetchData();
  };

  const onTxtClear = () => {
    pagination.current = 1;
    setPagination(pagination);
    fetchData();
  };

  const handleTableChange = (pagination = {}) => {
    setPagination(pagination);
  };

  const fetchData = async () => {
    setLoading(true);
    try {
      const data = await getModelAttrList(modelId!);
      setTableData(data);
      pagination.total = data.length;
      pagination.pageSize = 10;
      setPagination(pagination);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  const updateAttrList = () => {
    fetchData();
  };

  return (
    <div>
      <div>
        <div className="nav-box flex justify-end mb-[16px]">
          <div className="left-side w-[240px] mr-[8px]">
            <Input
              placeholder={t('common.search')}
              value={searchText}
              allowClear
              onChange={onSearchTxtChange}
              onPressEnter={onTxtPressEnter}
              onClear={onTxtClear}
            />
          </div>
          <div className="right-side">
            <PermissionWrapper
              requiredPermissions={['Edit Model']}
              instPermissions={modelPermission}
            >
              <Button
                type="primary"
                className="mr-[8px]"
                icon={<PlusOutlined />}
                onClick={() => showAttrModal('add')}
              >
                {t('common.addNew')}
              </Button>
            </PermissionWrapper>
          </div>
        </div>
        <CustomTable
          size="middle"
          scroll={{ y: 'calc(100vh - 380px)' }}
          columns={columns}
          dataSource={tableData}
          loading={loading}
          rowKey="attr_id"
          onChange={handleTableChange}
        ></CustomTable>
      </div>
      <AttributesModal
        ref={attrRef}
        attrTypeList={ATTR_TYPE_LIST}
        onSuccess={updateAttrList}
      />
    </div>
  );
};

export default Attributes;

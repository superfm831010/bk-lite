"use client";
import React, { useState, useEffect, useRef } from 'react';
import { Input, message, Modal, Tree, Button, Spin, Popconfirm, Dropdown, Menu, Form } from 'antd';
import type { DataNode as TreeDataNode } from 'antd/lib/tree';
import { ColumnsType } from 'antd/es/table';
import TopSection from '@/components/top-section';
import UserModal, { ModalRef } from './userModal';
import PasswordModal, { PasswordModalRef } from '@/app/system-manager/components/user/passwordModal';
import { useTranslation } from '@/utils/i18n';
import { getRandomColor } from '@/app/system-manager/utils';
import CustomTable from '@/components/custom-table';
import { useUserApi } from '@/app/system-manager/api/user/index';
import { OriginalGroup } from '@/app/system-manager/types/group';
import { UserDataType, TableRowSelection } from '@/app/system-manager/types/user';
import PageLayout from '@/components/page-layout';
import styles from './index.module.scss';
import { useGroupApi } from '@/app/system-manager/api/group/index';
import { MoreOutlined, PlusOutlined } from '@ant-design/icons';
import OperateModal from '@/components/operate-modal';

const { Search } = Input;

const User: React.FC = () => {
  const [tableData, setTableData] = useState<UserDataType[]>([]);
  const [selectedTreeKeys, setSelectedTreeKeys] = useState<React.Key[]>([]);
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);
  const [isDeleteDisabled, setIsDeleteDisabled] = useState<boolean>(true);
  const [searchValue, setSearchValue] = useState<string>('');
  const [treeSearchValue, setTreeSearchValue] = useState<string>('');
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [pageSize, setPageSize] = useState<number>(10);
  const [total, setTotal] = useState<number>(0);
  const [treeData, setTreeData] = useState<TreeDataNode[]>([]);
  const [filteredTreeData, setFilteredTreeData] = useState<TreeDataNode[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [addGroupForm] = Form.useForm();
  const [addGroupModalOpen, setAddGroupModalOpen] = useState(false);
  const [addSubGroupModalOpen, setAddSubGroupModalOpen] = useState(false);
  const [currentParentGroupKey, setCurrentParentGroupKey] = useState<string | null>(null);
  const [addGroupLoading, setAddGroupLoading] = useState(false);
  const [renameGroupModalOpen, setRenameGroupModalOpen] = useState(false);
  const [renameGroupLoading, setRenameGroupLoading] = useState(false);
  const [renameGroupKey, setRenameGroupKey] = useState<string | null>(null);
  const [renameGroupForm] = Form.useForm();

  const userModalRef = useRef<ModalRef>(null);
  const passwordModalRef = useRef<PasswordModalRef>(null);

  const { t } = useTranslation();
  const { confirm } = Modal;
  const { getUsersList, getOrgTree, deleteUser } = useUserApi();
  const { addTeamData, updateGroup, deleteTeam } = useGroupApi();

  const columns: ColumnsType<UserDataType> = [
    {
      title: t('system.user.table.username'),
      dataIndex: 'username',
      width: 230,
      fixed: 'left',
      render: (text: string) => {
        const color = getRandomColor();
        return (
          <div className="flex" style={{ height: '17px', lineHeight: '17px' }}>
            <span
              className="h-5 w-5 rounded-[10px] text-center mr-1"
              style={{ color: '#ffffff', backgroundColor: color }}
            >
              {text?.substring(0, 1)}
            </span>
            <span>{text}</span>
          </div>
        );
      },
    },
    {
      title: t('system.user.table.lastName'),
      dataIndex: 'name',
      width: 100,
    },
    {
      title: t('system.user.table.email'),
      dataIndex: 'email',
      width: 185,
    },
    {
      title: t('common.actions'),
      dataIndex: 'key',
      width: 160,
      fixed: 'right',
      render: (key: string) => (
        <>
          <Button type="link" className="mr-[8px]" onClick={() => handleEditUser(key)}>
            {t('common.edit')}
          </Button>
          <Button type="link" className="mr-[8px]" onClick={() => openPasswordModal(key)}>
            {t('system.common.password')}
          </Button>
          <Popconfirm
            title={t('common.delConfirm')}
            okText={t('common.confirm')}
            cancelText={t('common.cancel')}
            onConfirm={() => showDeleteConfirm(key)}
          >
            <Button type="link">{t('common.delete')}</Button>
          </Popconfirm>
        </>
      ),
    },
  ];

  const fetchUsers = async (params: any = {}) => {
    setLoading(true);
    try {
      const res = await getUsersList({
        group_id: selectedTreeKeys[0],
        ...params,
      });
      const data = res.users.map((item: UserDataType) => ({
        key: item.id,
        username: item.username,
        name: item.lastName,
        email: item.email,
        role: item.role,
      }));
      setTableData(data);
      setTotal(res.count);
    } catch {
      message.error(t('common.fetchFailed'));
    } finally {
      setLoading(false);
    }
  };

  const fetchTreeData = async () => {
    try {
      const res = await getOrgTree();
      setTreeData(convertGroups(res));
      setFilteredTreeData(convertGroups(res));
    } catch {
      message.error(t('common.fetchFailed'));
    }
  };

  useEffect(() => {
    fetchUsers({ search: searchValue, page: currentPage, page_size: pageSize });
  }, [currentPage, pageSize, searchValue]);

  useEffect(() => {
    fetchTreeData();
  }, []);

  useEffect(() => {
    setIsDeleteDisabled(selectedRowKeys.length === 0);
  }, [selectedRowKeys]);

  const handleTreeSelect = (selectedKeys: React.Key[]) => {
    setSelectedRowKeys([]);
    setSelectedTreeKeys(selectedKeys);
    fetchUsers({
      search: searchValue,
      page: currentPage,
      page_size: pageSize,
      group_id: selectedKeys[0],
    });
  };

  const handleEditUser = (userId: string) => {
    userModalRef.current?.showModal({ type: 'edit', userId });
  };

  const openPasswordModal = (userId: string) => {
    passwordModalRef.current?.showModal({ userId });
  };

  const convertGroups = (groups: OriginalGroup[]): TreeDataNode[] => {
    return groups.map((group) => ({
      key: group.id,
      title: group.name,
      children: group.subGroups ? convertGroups(group.subGroups) : [],
    }));
  };

  const onSelectChange = (newSelectedRowKeys: React.Key[]) => {
    setSelectedRowKeys(newSelectedRowKeys);
  };

  const rowSelection: TableRowSelection<any> = {
    selectedRowKeys,
    onChange: onSelectChange,
  };

  const showDeleteConfirm = async (key: string) => {
    try {
      await deleteUser({ user_ids: [key] });
      fetchUsers({ search: searchValue, page: currentPage, page_size: pageSize });
      message.success(t('common.delSuccess'));
    } catch {
      message.error(t('common.delFailed'));
    }
  };

  const handleModifyDelete = () => {
    confirm({
      title: t('common.delConfirm'),
      content: t('common.delConfirmCxt'),
      centered: true,
      okText: t('common.confirm'),
      cancelText: t('common.cancel'),
      async onOk() {
        try {
          await deleteUser({ user_ids: selectedRowKeys });
          setSelectedRowKeys([]);
          fetchUsers({ search: searchValue, page: currentPage, page_size: pageSize });
          message.success(t('common.delSuccess'));
        } catch {
          message.error(t('common.delFailed'));
        }
      },
    });
  };

  const openUserModal = (type: 'add') => {
    userModalRef.current?.showModal({
      type,
      groupKeys: type === 'add' ? (selectedTreeKeys as string[]) : [],
    });
  };

  const onSuccessUserModal = () => {
    fetchUsers({ search: searchValue, page: currentPage, page_size: pageSize });
  };

  const handleTreeSearchChange = (value: string) => {
    setTreeSearchValue(value);
    filterTreeData(value);
  };

  const handleUserSearch = (value: string) => {
    setSearchValue(value);
    fetchUsers({ search: value, page: currentPage, page_size: pageSize });
  };

  const filterTreeData = (value: string) => {
    const filterFunc = (data: TreeDataNode[], searchQuery: string): TreeDataNode[] => {
      return data.reduce<TreeDataNode[]>((acc, item) => {
        const children = item.children ? filterFunc(item.children, searchQuery) : [];
        if ((item.title as string).toLowerCase().includes(searchQuery.toLowerCase()) || children.length) {
          acc.push({ ...item, children });
        }
        return acc;
      }, []);
    };
    setFilteredTreeData(filterFunc(treeData, value));
  };

  const handleTableChange = (page: number, pageSize: number) => {
    setCurrentPage(page);
    setPageSize(pageSize);
  };

  const handleAddRootGroup = () => {
    setCurrentParentGroupKey(null);
    setAddGroupModalOpen(true);
  };

  const handleAddSubGroup = (parentGroupKey: string) => {
    setCurrentParentGroupKey(parentGroupKey);
    setAddSubGroupModalOpen(true);
  };

  const onAddGroup = async () => {
    setAddGroupLoading(true);
    try {
      const values = await addGroupForm.validateFields();
      await addTeamData({
        group_name: values.name,
        parent_group_id: currentParentGroupKey || undefined,
      });
      message.success(t('common.addSuccess'));
      fetchTreeData();
      setAddGroupModalOpen(false);
      setAddSubGroupModalOpen(false);
    } catch {
      message.error(t('common.addFailed'));
    } finally {
      setAddGroupLoading(false);
    }
  };

  const handleGroupAction = async (action: string, groupKey: string) => {
    switch (action) {
      case 'addSubGroup':
        handleAddSubGroup(groupKey);
        break;
      case 'rename':
        const group = findNode(treeData, groupKey);
        if (group) {
          renameGroupForm.resetFields();
          setRenameGroupKey(groupKey);
          renameGroupForm.setFieldsValue({ renameTeam: group.title });
          setRenameGroupModalOpen(true);
        }
        break;
      case 'delete':
        confirm({
          title: t('common.delConfirm'),
          content: t('common.delConfirmCxt'),
          centered: true,
          okText: t('common.confirm'),
          cancelText: t('common.cancel'),
          async onOk() {
            handleDeleteGroup(groupKey);
          },
        });
        break;
    }
  };

  const handleDeleteGroup = (key: string) => {
    const group = findNode(treeData, key);
    if (group) {
      deleteGroup(group);
    }
  };

  const deleteGroup = async (group: TreeDataNode) => {
    setLoading(true);
    try {
      await deleteTeam({ id: group.key });
      message.success(t('common.delSuccess'));
      fetchTreeData();
    } catch {
      message.error(t('common.delFailed'));
    } finally {
      setLoading(false);
    }
  };

  const onRenameGroup = async () => {
    setRenameGroupLoading(true);
    try {
      await renameGroupForm.validateFields();
      const values = renameGroupForm.getFieldValue('renameTeam');
      await updateGroup({
        group_id: renameGroupKey,
        group_name: values,
      });
      message.success(t('system.group.renameSuccess'));
      fetchTreeData();
      setRenameGroupModalOpen(false);
    } catch {
      message.error(t('system.group.renameFailed'));
    } finally {
      setRenameGroupLoading(false);
      renameGroupForm.resetFields();
    }
  };

  const findNode = (tree: TreeDataNode[], key: string): TreeDataNode | undefined => {
    for (const node of tree) {
      if (node.key === key) return node;
      if (node.children) {
        const found = findNode(node.children, key);
        if (found) return found;
      }
    }
  };

  const renderGroupActions = (groupKey: string) => (
    <Dropdown
      overlay={
        <Menu
          onClick={({ key }) => handleGroupAction(key, groupKey)}
          items={[
            { key: 'addSubGroup', label: t('system.group.addSubGroups') },
            { key: 'rename', label: t('system.group.rename') },
            { key: 'delete', label: t('common.delete') },
          ]}
        />
      }
      trigger={['click']}
    >
      <MoreOutlined
        className="cursor-pointer"
        onClick={(e) => e.stopPropagation()}
      />
    </Dropdown>
  );

  const renderTreeNode = (nodes: TreeDataNode[]): TreeDataNode[] =>
    nodes.map((node) => ({
      ...node,
      title: (
        <div className="flex justify-between items-center">
          <span className="truncate">
            {typeof node.title === 'function' ? node.title(node) : node.title}
          </span>
          {renderGroupActions(node.key as string)}
        </div>
      ),
      children: node.children ? renderTreeNode(node.children) : [],
    }));

  const topSectionContent = (
    <TopSection title={t('system.user.title')} content={t('system.user.desc')} />
  );

  const leftSectionContent = (
    <div className={`w-full h-full flex flex-col ${styles.userInfo}`}>
      <div className="flex items-center mb-4">
        <Input
          size="small"
          className="flex-1"
          placeholder={`${t('common.search')}...`}
          onChange={(e) => handleTreeSearchChange(e.target.value)}
          value={treeSearchValue}
        />
        <Button type="primary" size="small" icon={<PlusOutlined />} className="ml-2" onClick={handleAddRootGroup}></Button>
      </div>
      <Tree
        className="w-full flex-1 overflow-auto"
        showLine
        blockNode
        expandAction={false}
        defaultExpandAll
        treeData={renderTreeNode(filteredTreeData)}
        onSelect={handleTreeSelect}
      />
    </div>
  );

  const rightSectionContent = (
    <>
      <div className="w-full mb-4 flex justify-end">
        <Search
          allowClear
          enterButton
          className="w-60 mr-2"
          onSearch={handleUserSearch}
          placeholder={`${t('common.search')}...`}
        />
        <Button type="primary" className="mr-2" onClick={() => openUserModal('add')}>
          +{t('common.add')}
        </Button>
        <UserModal ref={userModalRef} treeData={treeData} onSuccess={onSuccessUserModal} />
        <Button onClick={handleModifyDelete} disabled={isDeleteDisabled}>
          {t('common.batchDelete')}
        </Button>
        <PasswordModal ref={passwordModalRef} onSuccess={() => fetchUsers({ search: searchValue, page: currentPage, page_size: pageSize })} />
      </div>
      <Spin spinning={loading}>
        <CustomTable
          scroll={{ y: 'calc(100vh - 360px)' }}
          pagination={{
            pageSize,
            current: currentPage,
            total,
            showSizeChanger: true,
            onChange: handleTableChange,
          }}
          columns={columns}
          dataSource={tableData}
          rowSelection={rowSelection}
        />
      </Spin>
    </>
  );

  return (
    <>
      <PageLayout
        topSection={topSectionContent}
        leftSection={leftSectionContent}
        rightSection={rightSectionContent}
      />
      <OperateModal
        title={t('common.add')}
        open={addGroupModalOpen || addSubGroupModalOpen}
        onOk={onAddGroup}
        confirmLoading={addGroupLoading}
        onCancel={() => {
          setAddGroupModalOpen(false);
          setAddSubGroupModalOpen(false);
          addGroupForm.resetFields();
        }}
        okText={t('common.confirm')}
        cancelText={t('common.cancel')}
      >
        <Form form={addGroupForm}>
          <Form.Item
            name="name"
            label={t('system.group.form.name')}
            rules={[{ required: true, message: t('common.inputRequired') }]}
          >
            <Input placeholder={`${t('common.inputMsg')}${t('system.group.form.name')}`} />
          </Form.Item>
        </Form>
      </OperateModal>
      <OperateModal
        title={t('system.group.rename')}
        closable={false}
        okText={t('common.confirm')}
        cancelText={t('common.cancel')}
        okButtonProps={{ loading: renameGroupLoading }}
        cancelButtonProps={{ disabled: renameGroupLoading }}
        open={renameGroupModalOpen}
        onOk={onRenameGroup}
        onCancel={() => {
          setRenameGroupModalOpen(false);
          renameGroupForm.resetFields();
        }}
      >
        <Form form={renameGroupForm}>
          <Form.Item
            name="renameTeam"
            label={t('system.user.form.name')}
            rules={[{ required: true, message: t('common.inputRequired') }]}
          >
            <Input placeholder={`${t('common.inputMsg')}${t('system.user.form.name')}`} />
          </Form.Item>
        </Form>
      </OperateModal>
    </>
  );
};

export default User;

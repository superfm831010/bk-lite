"use client";
import React, { useState, useEffect, useRef } from 'react';
import { Input, message, Modal, Tree, Button, Spin, Popconfirm, Dropdown, Menu, Form, Tooltip } from 'antd';
import type { DataNode as TreeDataNode } from 'antd/lib/tree';
import { ColumnsType } from 'antd/es/table';
import TopSection from '@/components/top-section';
import UserModal, { ModalRef } from './userModal';
import PasswordModal, { PasswordModalRef } from '@/app/system-manager/components/user/passwordModal';
import { useTranslation } from '@/utils/i18n';
import { useClientData } from '@/context/client';
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
import PermissionWrapper from '@/components/permission';
import EllipsisWithTooltip from '@/components/ellipsis-with-tooltip';
import Icon from '@/components/icon';

interface ExtendedTreeDataNode extends TreeDataNode {
  hasAuth?: boolean;
  children?: ExtendedTreeDataNode[];
}

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
  const [treeData, setTreeData] = useState<ExtendedTreeDataNode[]>([]);
  const [filteredTreeData, setFilteredTreeData] = useState<ExtendedTreeDataNode[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const addGroupFormRef = useRef<any>(null);
  const [addGroupModalOpen, setAddGroupModalOpen] = useState(false);
  const [addSubGroupModalOpen, setAddSubGroupModalOpen] = useState(false);
  const [currentParentGroupKey, setCurrentParentGroupKey] = useState<number | null>(null);
  const [addGroupLoading, setAddGroupLoading] = useState(false);
  const [renameGroupModalOpen, setRenameGroupModalOpen] = useState(false);
  const [renameGroupLoading, setRenameGroupLoading] = useState(false);
  const [renameGroupKey, setRenameGroupKey] = useState<number | null>(null);
  const renameGroupFormRef = useRef<any>(null);
  const { clientData } = useClientData();

  const userModalRef = useRef<ModalRef>(null);
  const passwordModalRef = useRef<PasswordModalRef>(null);

  const { t } = useTranslation();
  const { confirm } = Modal;
  const { getUsersList, getOrgTree, deleteUser } = useUserApi();
  const { addTeamData, updateGroup, deleteTeam } = useGroupApi();

  // Add a map to convert app names to icons
  const appIconMap = new Map(clientData.map((item) => [item.name, item.icon]));

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
      title: t('system.user.table.role'),
      dataIndex: 'roles',
      width: 200,
      render: (roles: string[]) => {
        const groupedRoles = (roles || []).reduce((acc: Record<string, string[]>, role: string) => {
          const [appName, roleName] = [role.split('-').slice(0, -1).join('-'), role.split('-').slice(-1)[0]];
          if (!acc[appName]) acc[appName] = [];
          acc[appName].push(roleName);
          return acc;
        }, {});

        const appEntries = Object.entries(groupedRoles);
        const visibleApps = appEntries.slice(0, 2);
        const hiddenApps = appEntries.slice(2);

        return (
          <div className="flex flex-wrap gap-2">
            {visibleApps.map(([appName, roleNames]) => (
              <div key={appName} className="flex items-center gap-1 rounded-xl border px-2 py-1">
                {appIconMap.get(appName) && (
                  <Tooltip title={appName} placement="top">
                    <div>
                      <Icon type={appName} className="w-4 h-4" />
                    </div>
                  </Tooltip>
                )}
                <span className="text-xs text-[var(--color-text-3)]">{roleNames.join(', ')}</span>
              </div>
            ))}
            {hiddenApps.length > 0 && (
              <Dropdown
                overlay={
                  <Menu>
                    {hiddenApps.map(([appName, roleNames]) => (
                      <Menu.Item key={appName}>
                        <div className="flex items-center gap-1">
                          {appIconMap.get(appName) && (
                            <Tooltip title={appName} placement="top" zIndex={10000}>
                              <div>
                                <Icon type={appName} className="w-4 h-4" />
                              </div>
                            </Tooltip>
                          )}
                          <span>{roleNames.join(', ')}</span>
                        </div>
                      </Menu.Item>
                    ))}
                  </Menu>
                }
                trigger={["click"]}
              >
                <span className="cursor-pointer text-blue-500 ml-1">...</span>
              </Dropdown>
            )}
          </div>
        );
      },
    },
    {
      title: t('common.actions'),
      dataIndex: 'key',
      width: 160,
      fixed: 'right',
      render: (key: string) => (
        <>
          <PermissionWrapper requiredPermissions={['Edit User']}>
            <Button type="link" className="mr-[8px]" onClick={() => handleEditUser(key)}>
              {t('common.edit')}
            </Button>
          </PermissionWrapper>
          <PermissionWrapper requiredPermissions={['Edit User']}>
            <Button type="link" className="mr-[8px]" onClick={() => openPasswordModal(key)}>
              {t('system.common.password')}
            </Button>
          </PermissionWrapper>
          <PermissionWrapper requiredPermissions={['Delete User']}>
            <Popconfirm
              title={t('common.delConfirm')}
              okText={t('common.confirm')}
              cancelText={t('common.cancel')}
              onConfirm={() => showDeleteConfirm(key)}
            >
              <Button type="link">{t('common.delete')}</Button>
            </Popconfirm>
          </PermissionWrapper>
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
        name: item.display_name,
        email: item.email,
        role: item.role,
        roles: item.roles || [],
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

  const nodeExistsInTree = (tree: ExtendedTreeDataNode[], key: React.Key): boolean => {
    for (const node of tree) {
      if (node.key === key) return true;
      if (node.children && node.children.length > 0) {
        if (nodeExistsInTree(node.children, key)) return true;
      }
    }
    return false;
  };

  const handleTreeSelect = (selectedKeys: React.Key[]) => {
    setSelectedRowKeys([]);
    
    if (selectedKeys.length === 0 || !nodeExistsInTree(filteredTreeData, selectedKeys[0])) {
      setSelectedTreeKeys([]);
    } else {
      const selectedNode = findNode(filteredTreeData, selectedKeys[0] as number);
      if (selectedNode && selectedNode.hasAuth === false) {
        return;
      }
      setSelectedTreeKeys(selectedKeys.map(Number));
    }
    
    fetchUsers({
      search: searchValue,
      page: currentPage,
      page_size: pageSize,
      group_id: selectedKeys.length > 0 ? selectedKeys[0] as number : undefined,
    });
  };

  const handleEditUser = (userId: string) => {
    userModalRef.current?.showModal({ type: 'edit', userId });
  };

  const openPasswordModal = (userId: string) => {
    passwordModalRef.current?.showModal({ userId });
  };

  const convertGroups = (groups: OriginalGroup[]): ExtendedTreeDataNode[] => {
    return groups.map((group) => ({
      key: group.id,
      title: group.name,
      hasAuth: group.hasAuth,
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
      groupKeys: type === 'add' ? selectedTreeKeys.map(Number) : [],
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
    const filterFunc = (data: ExtendedTreeDataNode[], searchQuery: string): ExtendedTreeDataNode[] => {
      return data.reduce<ExtendedTreeDataNode[]>((acc, item) => {
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

  const resetAddGroupForm = () => {
    if (addGroupFormRef.current) {
      addGroupFormRef.current.resetFields();
    }
  };

  const resetRenameGroupForm = () => {
    if (renameGroupFormRef.current) {
      renameGroupFormRef.current.resetFields();
    }
  };

  const handleAddRootGroup = () => {
    setCurrentParentGroupKey(null);
    setAddGroupModalOpen(true);
  };

  const handleAddSubGroup = (parentGroupKey: number) => {
    setCurrentParentGroupKey(parentGroupKey);
    setAddSubGroupModalOpen(true);
  };

  const onAddGroup = async () => {
    setAddGroupLoading(true);
    try {
      const values = await addGroupFormRef.current?.validateFields();
      await addTeamData({
        group_name: values.name,
        parent_group_id: currentParentGroupKey || undefined,
      });
      message.success(t('common.saveSuccess'));
      fetchTreeData();
      setAddGroupModalOpen(false);
      setAddSubGroupModalOpen(false);
      // Reset after successful submission
      resetAddGroupForm();
    } catch {
      message.error(t('common.saveFailed'));
    } finally {
      setAddGroupLoading(false);
    }
  };

  const handleGroupAction = async (action: string, groupKey: number) => {
    const node = findNode(treeData, groupKey);
    if (node && node.hasAuth === false) {
      return;
    }

    switch (action) {
      case 'addSubGroup':
        handleAddSubGroup(groupKey);
        break;
      case 'rename':
        const group = findNode(treeData, groupKey);
        if (group) {
          setRenameGroupKey(groupKey);
          setRenameGroupModalOpen(true);
          setTimeout(() => {
            renameGroupFormRef.current?.setFieldsValue({ renameTeam: group.title });
          }, 0);
        }
        break;
      case 'delete':
        const targetGroup = findNode(treeData, groupKey);
        if (targetGroup) {
          const hasChildren = targetGroup.children && targetGroup.children.length > 0;
          const confirmContent = hasChildren 
            ? t('system.group.deleteWithChildrenWarning') + '' + t('common.delConfirmCxt')
            : t('common.delConfirmCxt');
            
          confirm({
            title: t('common.delConfirm'),
            content: confirmContent,
            centered: true,
            okText: t('common.confirm'),
            cancelText: t('common.cancel'),
            async onOk() {
              handleDeleteGroup(groupKey);
            },
          });
        }
        break;
    }
  };

  const handleDeleteGroup = (key: number) => {
    const group = findNode(treeData, key);
    if (group) {
      deleteGroup(group);
    }
  };

  const deleteGroup = async (group: ExtendedTreeDataNode) => {
    setLoading(true);
    try {
      await deleteTeam({ id: group.key });
      message.success(t('common.delSuccess'));
      
      const deletedKey = group.key;
      const isSelectedDeleted = selectedTreeKeys.includes(deletedKey);
      await fetchTreeData();
      
      if (isSelectedDeleted) {
        setSelectedTreeKeys([]);
        setSelectedRowKeys([]);
        fetchUsers({ 
          search: searchValue, 
          page: currentPage, 
          page_size: pageSize,
          group_id: undefined
        });
      }
    } catch {
      message.error(t('common.delFailed'));
    } finally {
      setLoading(false);
    }
  };

  const onRenameGroup = async () => {
    setRenameGroupLoading(true);
    try {
      await renameGroupFormRef.current?.validateFields();
      const values = renameGroupFormRef.current?.getFieldsValue();
      await updateGroup({
        group_id: renameGroupKey,
        group_name: values.renameTeam,
      });
      message.success(t('system.group.renameSuccess'));
      fetchTreeData();
      setRenameGroupModalOpen(false);
      resetRenameGroupForm();
    } catch {
      message.error(t('system.group.renameFailed'));
    } finally {
      setRenameGroupLoading(false);
    }
  };

  const findNode = (tree: ExtendedTreeDataNode[], key: number): ExtendedTreeDataNode | undefined => {
    for (const node of tree) {
      if (node.key === key) return node;
      if (node.children) {
        const found = findNode(node.children, key);
        if (found) return found;
      }
    }
  };

  const renderGroupActions = (groupKey: number) => {
    // 检查节点是否有权限
    const node = findNode(treeData, groupKey);
    if (node && node.hasAuth === false) {
      return null; // 如果没有权限，不显示操作按钮
    }

    return (
      <Dropdown
        overlay={
          <Menu
            onClick={({ key, domEvent }) => {
              domEvent.stopPropagation();
              handleGroupAction(key, groupKey);
            }}
            items={[
              {
                key: 'addSubGroup',
                label: (
                  <PermissionWrapper requiredPermissions={['Add Group']}>
                    {t('system.group.addSubGroups')}
                  </PermissionWrapper>
                ),
              },
              {
                key: 'rename',
                label: (
                  <PermissionWrapper requiredPermissions={['Edit Group']}>
                    {t('system.group.rename')}
                  </PermissionWrapper>
                ),
              },
              {
                key: 'delete',
                label: (
                  <PermissionWrapper requiredPermissions={['Delete Group']}>
                    {t('common.delete')}
                  </PermissionWrapper>
                ),
              },
            ]}
          />
        }
        trigger={['click']}
      >
        <MoreOutlined
          className="cursor-pointer"
          onClick={(e) => {
            e.stopPropagation();
            e.preventDefault();
          }}
        />
      </Dropdown>
    );
  };

  const renderTreeNode = (nodes: ExtendedTreeDataNode[]): ExtendedTreeDataNode[] =>
    nodes.map((node) => ({
      ...node,
      selectable: node.hasAuth !== false,
      title: (
        <div className="flex justify-between items-center w-full pr-1">
          <EllipsisWithTooltip 
            text={typeof node.title === 'function' ? String(node.title(node)) : String(node.title)}
            className={`truncate max-w-[100px] flex-1 ${node.hasAuth === false ? 'opacity-50' : ''}`}
          />
          <span className="flex-shrink-0 ml-2">
            {renderGroupActions(node.key as number)}
          </span>
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
        <PermissionWrapper requiredPermissions={['Add Group']}>
          <Button type="primary" size="small" icon={<PlusOutlined />} className="ml-2" onClick={handleAddRootGroup}></Button>
        </PermissionWrapper>
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
        <PermissionWrapper requiredPermissions={['Add User']}>
          <Button type="primary" className="mr-2" onClick={() => openUserModal('add')}>
            +{t('common.add')}
          </Button>
        </PermissionWrapper>
        <UserModal ref={userModalRef} treeData={treeData} onSuccess={onSuccessUserModal} />
        <PermissionWrapper requiredPermissions={['Delete User']}>
          <Button onClick={handleModifyDelete} disabled={isDeleteDisabled}>
            {t('common.batchDelete')}
          </Button>
        </PermissionWrapper>
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
          resetAddGroupForm();
        }}
        okText={t('common.confirm')}
        cancelText={t('common.cancel')}
        destroyOnClose={true}
      >
        <Form ref={addGroupFormRef}>
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
          resetRenameGroupForm();
        }}
        destroyOnClose={true}
      >
        <Form ref={renameGroupFormRef}>
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

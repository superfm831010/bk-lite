'use client';

import React, { useState, useMemo } from 'react';
import { Form } from 'antd';
import type { DataNode } from 'antd/lib/tree';
import { useTranslation } from '@/utils/i18n';
import { Input, Button, Modal, Dropdown, Menu, Tree, Empty } from 'antd';
import {
  SidebarProps,
  DirItem,
  ModalAction,
  DirectoryType,
} from '@/app/ops-analysis/types';
import {
  PlusOutlined,
  MoreOutlined,
  AreaChartOutlined,
  SettingOutlined,
  DeploymentUnitOutlined,
} from '@ant-design/icons';
import { mockDirs } from '../mockData';

const Sidebar: React.FC<SidebarProps> = ({ onSelect }) => {
  const [form] = Form.useForm();
  const { t } = useTranslation();
  const [dirs, setDirs] = useState<DirItem[]>(mockDirs as DirItem[]);
  const [searchTerm, setSearchTerm] = useState('');
  const [modalVisible, setModalVisible] = useState(false);
  const [modalTitle, setModalTitle] = useState('');
  const [modalAction, setModalAction] = useState<ModalAction>('addRoot');
  const [newItemType, setNewItemType] = useState<DirectoryType>('group');
  const [expandedKeys, setExpandedKeys] = useState<React.Key[]>([]);
  const [currentDir, setCurrentDir] = useState<{
    id: string;
    parentId: string | null;
  } | null>(null);

  const autoExpandAll = (
    items: DirItem[],
    keys: React.Key[] = []
  ): React.Key[] => {
    items.forEach((item) => {
      keys.push(item.id);
      if (item.children) {
        autoExpandAll(item.children, keys);
      }
    });
    return keys;
  };

  const showModal = (
    action: ModalAction,
    title: string,
    defaultValue = '',
    dir: { id: string; parentId: string | null } | null = null,
    itemType: DirectoryType = 'group',
    defaultDesc = ''
  ) => {
    setModalAction(action);
    setModalTitle(title);
    form.setFieldsValue({ name: defaultValue, description: defaultDesc });
    setCurrentDir(dir);
    setNewItemType(itemType);
    setModalVisible(true);
  };

  const handleAddRoot = (nameVal: string, descVal?: string) => {
    const newItem = {
      id: Date.now().toString(),
      name: nameVal,
      type: newItemType,
      description: newItemType !== 'group' ? descVal : undefined,
    } as DirItem;
    setDirs((prev) => {
      const updated = [...prev, newItem];
      setExpandedKeys(autoExpandAll(updated));
      return updated;
    });
  };

  const handleAddChild = (nameVal: string, descVal?: string) => {
    if (!currentDir?.id) return;
    const newChild: DirItem = {
      id: Date.now().toString(),
      name: nameVal,
      type: newItemType,
      description: newItemType !== 'group' ? descVal : undefined,
    };

    const addChildToDir = (items: DirItem[]): DirItem[] => {
      return items.map((item) => {
        if (item.id === currentDir.id) {
          return {
            ...item,
            children: [...(item.children || []), newChild],
          };
        }

        if (item.children) {
          return {
            ...item,
            children: addChildToDir(item.children),
          };
        }

        return item;
      });
    };

    setDirs((prev) => {
      const newDirs = addChildToDir(prev);
      setExpandedKeys(autoExpandAll(newDirs));
      return newDirs;
    });
  };

  const handleEdit = (nameVal: string, descVal?: string) => {
    if (!currentDir) return;

    const editInTree = (items: DirItem[]): DirItem[] => {
      return items.map((d) => {
        if (currentDir.parentId === null) {
          if (d.id === currentDir.id) {
            return {
              ...d,
              name: nameVal,
              description: d.type !== 'group' ? descVal : d.description,
            };
          }
          return d;
        } else {
          if (d.id === currentDir.parentId) {
            return {
              ...d,
              children: d.children?.map((c) => {
                if (c.id === currentDir.id) {
                  return {
                    ...c,
                    name: nameVal,
                    description: c.type !== 'group' ? descVal : c.description,
                  };
                }
                return c;
              }),
            };
          }
          if (d.children) {
            return {
              ...d,
              children: editInTree(d.children),
            };
          }
          return d;
        }
      });
    };

    setDirs((prev) => {
      const newDirs = editInTree(prev);
      setExpandedKeys(autoExpandAll(newDirs));
      return newDirs;
    });
  };

  const handleModalOk = async () => {
    let values;
    try {
      values = await form.validateFields();
    } catch {
      return;
    }
    const nameVal = values.name;
    const descVal = values.description;
    switch (modalAction) {
      case 'addRoot':
        handleAddRoot(nameVal, descVal);
        break;
      case 'addChild':
        handleAddChild(nameVal, descVal);
        break;
      case 'edit':
        handleEdit(nameVal, descVal);
        break;
    }
    handleModalCancel();
  };

  const handleModalCancel = () => {
    setModalVisible(false);
    form.resetFields();
    setCurrentDir(null);
  };

  const handleSearch = (value: string) => setSearchTerm(value);

  const deleteDirectory = (id: string, parentId: string | null) => {
    Modal.confirm({
      title: t('sidebar.confirmDelete'),
      onOk() {
        const deleteFromTree = (items: DirItem[]): DirItem[] => {
          return items
            .filter((d) => d.id !== id)
            .map((d) => ({
              ...d,
              children: d.children ? deleteFromTree(d.children) : undefined,
            }));
        };

        setDirs((prev) => {
          const newDirs =
            parentId === null
              ? prev.filter((d) => d.id !== id)
              : deleteFromTree(prev);
          setExpandedKeys(autoExpandAll(newDirs));
          return newDirs;
        });
      },
    });
  };

  const getDirectoryIcon = (type: DirectoryType) => {
    switch (type) {
      case 'dashboard':
        return <AreaChartOutlined className="mr-1 text-blue-500" />;
      case 'topology':
        return <DeploymentUnitOutlined className="mr-1 text-green-500" />;
      case 'group':
      default:
        return '';
    }
  };

  const menuFor = (item: DirItem, parentId: string | null = null) => {
    const isRoot = parentId === null;
    const isGroup = item.type === 'group';

    return (
      <Menu selectable={false}>
        {isGroup && (
          <>
            <Menu.Item
              key="addDashboard"
              onClick={() => {
                setNewItemType('dashboard');
                showModal(
                  'addChild',
                  t('sidebar.addDash'),
                  '',
                  { id: item.id, parentId },
                  'dashboard'
                );
              }}
            >
              {t('sidebar.addDash')}
            </Menu.Item>
            <Menu.Item
              key="addTopology"
              onClick={() => {
                setNewItemType('topology');
                showModal(
                  'addChild',
                  t('sidebar.addTopo'),
                  '',
                  { id: item.id, parentId },
                  'topology'
                );
              }}
            >
              {t('sidebar.addTopo')}
            </Menu.Item>
          </>
        )}
        {isRoot && (
          <Menu.Item
            key="addGroup"
            onClick={() => {
              setNewItemType('group');
              showModal(
                'addChild',
                t('sidebar.addGroup'),
                '',
                { id: item.id, parentId },
                'group'
              );
            }}
          >
            {t('sidebar.addGroup')}
          </Menu.Item>
        )}

        <Menu.Item
          key="edit"
          onClick={() =>
            showModal(
              'edit',
              item.type === 'group'
                ? t('sidebar.editGroup')
                : item.type === 'dashboard'
                  ? t('sidebar.editDash')
                  : t('sidebar.editTopo'),
              item.name,
              { id: item.id, parentId },
              item.type,
              item.description || ''
            )
          }
        >
          {t('common.edit')}
        </Menu.Item>

        <Menu.Item
          key="delete"
          onClick={() => deleteDirectory(item.id, parentId)}
        >
          {t('common.delete')}
        </Menu.Item>
      </Menu>
    );
  };

  const buildTreeData = (
    items: DirItem[],
    parentId: string | null = null
  ): DataNode[] =>
    items.map((item) => ({
      key: item.id,
      data: { type: item.type },
      title: (
        <span className="flex justify-between items-center">
          <span className="flex items-center">
            {getDirectoryIcon(item.type)}
            <span className={item.type === 'group' ? 'font-medium' : ''}>
              {item.name}
            </span>
          </span>
          <Dropdown
            overlay={menuFor(item, parentId)}
            trigger={['click']}
            placement="bottomLeft"
            getPopupContainer={() => document.body}
          >
            <Button
              type="text"
              icon={<MoreOutlined />}
              onClick={(e) => e.stopPropagation()}
            />
          </Dropdown>
        </span>
      ),
      children: item.children
        ? buildTreeData(item.children, item.id)
        : undefined,
    }));

  const filteredDirs = useMemo(
    () =>
      dirs.filter(
        (d) =>
          d.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          d.children?.some((c) =>
            c.name.toLowerCase().includes(searchTerm.toLowerCase())
          )
      ),
    [dirs, searchTerm]
  );

  React.useEffect(() => {
    setExpandedKeys(autoExpandAll(dirs));
  }, [dirs]);

  const findTypeById = (
    items: DirItem[],
    id: string
  ): DirectoryType | undefined => {
    for (const item of items) {
      if (item.id === id) return item.type;
      if (item.children) {
        const t = findTypeById(item.children, id);
        if (t) return t;
      }
    }
    return undefined;
  };

  const findItemById = (items: DirItem[], id: string): DirItem | undefined => {
    for (const item of items) {
      if (item.id === id) return item;
      if (item.children) {
        const found = findItemById(item.children, id);
        if (found) return found;
      }
    }
    return undefined;
  };

  return (
    <div className="p-4 h-full flex flex-col">
      <h3 className="text-base font-semibold mb-4">{t('sidebar.title')}</h3>
      <div className="flex items-center mb-4">
        <Input.Search
          placeholder={t('common.searchPlaceHolder')}
          allowClear
          className="flex-1"
          onSearch={handleSearch}
        />
        <Button
          type="primary"
          icon={<PlusOutlined />}
          className="ml-2"
          onClick={() => showModal('addRoot', t('sidebar.addDir'))}
        />
      </div>

      <div className="overflow-auto flex-1">
        {filteredDirs.length > 0 ? (
          <Tree
            blockNode
            treeData={buildTreeData(filteredDirs)}
            expandedKeys={expandedKeys}
            onExpand={(keys) => setExpandedKeys(keys)}
            onSelect={(selectedKeys) => {
              const key = (selectedKeys as string[])[0];
              if (onSelect && key) {
                const type = findTypeById(dirs, key);
                if (type && type !== 'group') {
                  const item = findItemById(dirs, key);
                  onSelect(type, item);
                }
              }
            }}
            className="bg-transparent"
          />
        ) : (
          <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} />
        )}
      </div>
      <div className="flex justify-center height-[32px]">
        <Button
          block
          icon={<SettingOutlined />}
          onClick={() => onSelect && onSelect('datasource')}
        >
          设置
        </Button>
      </div>

      <Modal
        title={modalTitle}
        open={modalVisible}
        okText={t('common.confirm')}
        cancelText={t('common.cancel')}
        style={{ top: '35%' }}
        onOk={handleModalOk}
        onCancel={handleModalCancel}
      >
        <Form form={form} className="mt-5" labelCol={{ span: 3 }}>
          <Form.Item
            name="name"
            label={t('sidebar.nameLabel')}
            rules={[{ required: true, message: t('common.inputMsg') }]}
          >
            <Input placeholder={t('sidebar.inputPlaceholder')} />
          </Form.Item>
          {newItemType !== 'group' && (
            <Form.Item name="description" label={t('sidebar.descLabel')}>
              <Input.TextArea
                autoSize={{ minRows: 3 }}
                placeholder={t('common.inputMsg')}
              />
            </Form.Item>
          )}
        </Form>
      </Modal>
    </div>
  );
};

export default Sidebar;
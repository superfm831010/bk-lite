"use client"
import PageLayout from '@/components/page-layout';
import CustomTable from '@/components/custom-table';
import TopSection from '@/components/top-section';
import { ColumnItem } from '@/types';
import type { DataNode as TreeDataNode } from 'antd/lib/tree';
import { Input, Button, Tree, Spin, Dropdown, Menu, Modal, message } from 'antd';
import { PlusOutlined, MoreOutlined } from '@ant-design/icons';
import { useTranslation } from '@/utils/i18n';
import { useEffect, useState, useRef } from 'react';
import usePlayroundApi from '@/app/playground/api';
import ManageModal from './manageModal';
import { ModalRef, TableData } from '@/app/playground/types';
const { Search } = Input;
const { confirm } = Modal;

const PlaygroundManage = () => {
  const { t } = useTranslation();
  const { getCategoryList, getCapabilityList, deleteCategory } = usePlayroundApi();
  const modalRef = useRef<ModalRef>(null)
  const [tableLoading, setTableLoading] = useState<boolean>(false);
  const [treeLoading, setTreeLoading] = useState<boolean>(false);
  const [searchValue, setSearchValue] = useState<string>('');
  // const [selectCategory, setSelectCategory] = useState<number | null>(null);
  const [tableData, setTableData] = useState<TableData[]>([]);
  const [filteredTreeData, setFilteredTreeData] = useState<TreeDataNode[]>([]);
  const columns: ColumnItem[] = [
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name'
    },
    {
      title: '介绍',
      dataIndex: 'description',
      key: 'description'
    },
    {
      title: '地址',
      dataIndex: 'url',
      key: 'url'
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (_, record) => {
        return <p>{record.is_active ? '已上线' : '未上线'}</p>;
      }
    },
    {
      title: t(`common.action`),
      dataIndex: 'action',
      key: 'action',
      render: () => {
        return (
          <>
            <Button type='link' className='mr-2'>修改配置</Button>
            <Button type='link' className='mr-2'>内容</Button>
            <Button type='link' danger>删除</Button>
          </>
        )
      }
    }
  ];

  useEffect(() => {
    getAllCategory();
    getAllCapability();
    setSearchValue('');

    setTableData([
      {
        id: 1,
        name: 'test',
        description: 'test',
        url: '/playground/home?page=anomaly-detection',
        is_active: true
      }
    ])
  }, []);

  const renderNode = (data: any[], isChildren = false) => {
    const filterData = isChildren ? data : data.filter(item => item.level === 0);
    const treeData = filterData.map((item: any) => {
      const { children } = item;
      const node: any = {
        key: item?.id,
        name: item?.name,
        title: renderTitle(item),
        selectable: item.level === 0 ? false : true,
        children: children?.length > 0 ? renderNode(children, true) : [],
      };
      return node;
    });
    
    treeData.sort((a, b) => {
      const aHasChildren = a.children.length > 0;
      const bHasChildren = b.children.length > 0;

      // 1. 有子节点的排在前面
      if (aHasChildren && !bHasChildren) return -1;
      if (!aHasChildren && bHasChildren) return 1;

      // 2. 如果都有子节点或都没有子节点，按名称排序
      return a.name.localeCompare(b.name, 'zh-CN', {
        numeric: true,
        sensitivity: 'base'
      });
    });
    return treeData;
  };

  const getAllCategory = async () => {
    setTreeLoading(true);
    try {
      const data = await getCategoryList();
      const nodes = renderNode(data);
      setFilteredTreeData(nodes);
      console.log(nodes);
    } catch (e) {
      console.log(e)
    } finally {
      setTreeLoading(false);
    }
  };

  const getAllCapability = async () => {
    setTableLoading(true);
    try {
      const data = await getCapabilityList();
      console.log(data);
    } catch (e) {
      console.log(e)
    } finally {
      setTableLoading(false);
    }
  };

  const renderTitle = (data: any) => {
    return (
      <div className='w-full flex justify-between'>
        <span className='truncate'>{data?.name || '--'}</span>
        <span>
          <Dropdown
            overlay={
              <Menu
                onClick={({ key, domEvent }) => {
                  domEvent.stopPropagation();
                  if (key !== 'delete') {
                    openModal({ type: `${key}Category`, title: key, form: data })
                  } else {
                    handleDelCategory(data.id)
                  }
                }}
                items={[
                  {
                    key: 'add',
                    label: t(`common.add`),
                    disabled: data.level !== 0
                  },
                  {
                    key: 'update',
                    label: t(`common.update`)
                  },
                  {
                    key: 'delete',
                    label: t(`common.delete`),
                  }
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
        </span>
      </div>
    )
  };

  const renderTreeNode = () => {
    return filteredTreeData
  };

  const openModal = (data: {
    type: string;
    title: string;
    form: any
  }) => {
    modalRef.current?.showModal(data)
  };


  const onSelect = (keys: any) => {
    console.log(keys);
  };

  const topSection = (
    <TopSection title={'门户管理'} content={'管理门户的所有类别和所有的能力演示菜单。'} />
  );

  const leftSection = (
    <div className={`w-full h-full flex flex-col`}>
      <Spin spinning={treeLoading}>
        <div className='min-h-[370px] overflow-auto'>
          <div className="flex items-center mb-4">
            <Input
              size="small"
              className="flex-1"
              placeholder={`${t('common.search')}`}
              onChange={(e) => console.log(e)}
              value={searchValue}
            />
            <Button type="primary" size="small" icon={<PlusOutlined />} className="ml-2" onClick={() => openModal({ type: 'addCategory', title: 'add', form: null })} />
          </div>
          <Tree
            className="w-full flex-1"
            showLine
            blockNode
            expandAction={false}
            defaultExpandAll
            autoExpandParent
            defaultSelectedKeys={['hardware']}
            treeData={renderTreeNode()}
            onSelect={onSelect}
          />
        </div>
      </Spin>
    </div>
  );

  const onSearch = (search: string) => {
    console.log(search);
  };

  const handleDelCategory = (id: number) => {
    confirm({
      title: `确认要删除此类别吗`,
      okText: t(`common.confirm`),
      cancelText: t(`common.cancel`),
      onOk: async () => {
        try {
          await deleteCategory(id);
          message.success(`删除成功`);
        } catch (e) {
          console.log(e);
          message.error(`删除失败`);
        } finally {
          getAllCategory();
        }
      }
    })
  }

  const rightSection = (
    <>
      <div className='flex justify-end mb-4'>
        <Search className='w-[240px] mr-4' placeholder={t(`common.search`)} enterButton onSearch={onSearch} />
        <Button type='primary' icon={<PlusOutlined />} onClick={() => openModal({ type: 'addCapability', title: 'add', form: null })}>添加</Button>
      </div>
      <CustomTable
        rowKey='id'
        columns={columns}
        loading={tableLoading}
        dataSource={tableData}
      />
    </>
  );

  return (
    <>
      <PageLayout
        rightSection={rightSection}
        leftSection={leftSection}
        topSection={topSection}
      />
      <ManageModal ref={modalRef} nodes={filteredTreeData} />
    </>
  )
};

export default PlaygroundManage;
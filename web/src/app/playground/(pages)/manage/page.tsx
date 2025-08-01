"use client"
import PageLayout from '@/components/page-layout';
import CustomTable from '@/components/custom-table';
import TopSection from '@/components/top-section';
import { ColumnItem } from '@/types';
import type { DataNode as TreeDataNode } from 'antd/lib/tree';
import {
  Input,
  Button,
  Tree,
  Spin,
  Dropdown,
  Menu,
  Modal,
  message,
  Popconfirm,
  Switch,
  // Tag
} from 'antd';
import EllipsisWithTooltip from '@/components/ellipsis-with-tooltip';
import { PlusOutlined, MoreOutlined } from '@ant-design/icons';
import { useTranslation } from '@/utils/i18n';
import { useLocalizedTime } from "@/hooks/useLocalizedTime";
import { useEffect, useState, useRef } from 'react';
import usePlayroundApi from '@/app/playground/api';
import CategoryManageModal from './categoryManageModal';
import SampleManageModal from './sampleManageModal';
import { ModalRef, TableData } from '@/app/playground/types';
const { Search } = Input;
const { confirm } = Modal;

const PlaygroundManage = () => {
  const { t } = useTranslation();
  const { convertToLocalizedTime } = useLocalizedTime();
  const { getCategoryList, getCapabilityList, deleteCategory, deleteCapability } = usePlayroundApi();
  const categoryModalRef = useRef<ModalRef>(null);
  const sampleModalRef = useRef<ModalRef>(null);
  const [tableLoading, setTableLoading] = useState<boolean>(false);
  const [treeLoading, setTreeLoading] = useState<boolean>(false);
  const [confirmLoading, setConfirmLoading] = useState<boolean>(false);
  // const [searchValue, setSearchValue] = useState<string>('');
  const [selectCategory, setSelectCategory] = useState<number[]>([]);
  const [tableData, setTableData] = useState<TableData[]>([]);
  const [filteredTreeData, setFilteredTreeData] = useState<TreeDataNode[]>([]);
  const columns: ColumnItem[] = [
    {
      title: t(`common.name`),
      dataIndex: 'name',
      key: 'name'
    },
    {
      title: t(`common.description`),
      dataIndex: 'description',
      key: 'description'
    },
    {
      title: t(`manage.createAt`),
      dataIndex: 'create_at',
      key: 'create_at',
      render: (_, record) => {
        return (<p>{convertToLocalizedTime(record.created_at, 'YYYY-MM-DD HH:mm:ss')}</p>)
      }
    },
    {
      title: t(`manage.createdBy`),
      dataIndex: 'created_by',
      key: 'created_by',
      render: (_, { creator }) => {
        return creator ? (
          <div className="flex h-full items-center" title={creator}>
            <span
              className="block w-[18px] h-[18px] leading-[18px] text-center content-center rounded-[50%] mr-2 text-white"
              style={{ background: 'blue' }}
            >
              {creator.slice(0, 1).toLocaleUpperCase()}
            </span>
            <span>
              <EllipsisWithTooltip
                className="w-full overflow-hidden text-ellipsis whitespace-nowrap"
                text={creator}
              />
            </span>
          </div>
        ) : (
          <>--</>
        );
      }
    },
    {
      title: t(`manage.sampleStatus`),
      dataIndex: 'status',
      key: 'status',
      render: (_, record) => {
        return <Switch checked={record.is_active} onChange={handleSampleActiveChange} />
      }
    },
    {
      title: t(`common.action`),
      dataIndex: 'action',
      key: 'action',
      render: (_, record) => {
        return (
          <>
            {/* <Button type='link' className='mr-2' onClick={() => openCategoryModal({ type: 'updateCapability', title: 'update', form: record })}>修改配置</Button> */}
            <Popconfirm
              title={t(`manage.delCapability`)}
              description={t(`manage.delCapabilityText`)}
              okText={t('common.confirm')}
              cancelText={t('common.cancel')}
              okButtonProps={{ loading: confirmLoading }}
              onConfirm={() => handleDelCapability(record.id)}
            >
              <Button type='link' danger>{t(`common.delete`)}</Button>
            </Popconfirm>
          </>
        )
      }
    }
  ];

  const CategoryMenuItems = [
    {
      key: 'add',
      label: t(`common.add`),
    },
    {
      key: 'update',
      label: t(`common.update`)
    },
    {
      key: 'delete',
      label: t(`common.delete`),
    }
  ];

  const CapabilityMenuItems = [
    {
      key: 'update',
      label: t(`common.update`)
    },
    {
      key: 'delete',
      label: t(`common.delete`),
    }
  ];

  useEffect(() => {
    getAllTreeData();
    // getAllCapability();
    // setSearchValue('');
    setTableLoading(true);
    setTableData([
      {
        id: 1,
        name: 'test',
        description: 'test',
        create_at: '',
        creator: 'test',
        url: 'http://localhost:3000/playground/home?page=anomaly-detection',
        is_active: true
      }
    ]);
    setTableLoading(false);
  }, []);

  const renderCapabilityNode = (categoryId: number, capabilityData: any[]) => {
    console.log(categoryId, capabilityData);
    const filterData = capabilityData.filter(item => {
      const { id } = item.category;
      return categoryId === id;
    });
    return filterData.map((item: any) => ({
      key: `${item.id}_${item.name}`,
      title: renderCapabilityTitle(item),
      ...item
    }));
  };

  const renderNode = (categoryData: any[], capabilityData: any[]) => {
    const filterData = categoryData.filter(item => item.level === 0);
    const treeData = filterData.map((item: any) => {
      // const { children } = item;
      const node: any = {
        key: item?.id,
        name: item?.name,
        title: renderTitle({ ...item, mode: 'capability' }), // 二层菜单
        selectable: false,
        children: renderCapabilityNode(item?.id, capabilityData),
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

  const getAllTreeData = async () => {
    setTreeLoading(true);
    try {
      const [categoryData, capabilityData] = await Promise.all([getCategoryList(), getCapabilityList()]);
      const nodes = [
        {
          key: 'model_experience',
          name: 'model_experience',
          selectable: false,
          title: renderTitle({
            name: '模型体验',
            // mode: 'category'
          }), // 一层菜单操作
          children: renderNode(categoryData, capabilityData)
        },
        {
          key: 'agent_experience',
          name: 'agent_experience',
          selectable: false,
          title: renderTitle({
            name: '智能体体验',
            // mode: 'category'
          })
        }
      ];;
      setFilteredTreeData(nodes);
    } catch (e) {
      console.log(e)
    } finally {
      setTreeLoading(false);
    }
  };

  // const getAllCapability = async () => {
  //   setTableLoading(true);
  //   try {
  //     const data = await getCapabilityList();
  //     setTableData(data);
  //   } catch (e) {
  //     console.log(e)
  //   } finally {
  //     setTableLoading(false);
  //   }
  // };

  const renderCapabilityTitle = (data: any) => {
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
                    openCategoryModal({ type: `${key}Capability`, title: `${key}Capability`, form: data })
                  } else {
                    handleDelCapability(data?.id)
                  }
                }}
                items={CapabilityMenuItems}
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
    );
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
                  if (key === 'add' && data?.mode === 'capability') {
                    openCategoryModal({ type: `${key}Capability`, title: `${key}Capability`, form: { categoryID: data?.id } })
                  } else if (key !== 'delete') {
                    openCategoryModal({ type: `${key}Category`, title: `${key}Category`, form: data })
                  } else {
                    handleDelCategory(data?.id)
                  }
                }}
                items={
                  data?.mode ? CategoryMenuItems : [{
                    key: 'add',
                    label: t(`common.add`),
                  }]
                }
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

  const openCategoryModal = (data: {
    type: string;
    title: string;
    form: any
  }) => {
    categoryModalRef.current?.showModal(data)
  };

  const openSampleModal = (data: {
    type: string;
    title: string;
    form: any
  }) => {
    sampleModalRef.current?.showModal(data);
  }

  const onSelect = (keys: any) => {
    console.log(keys);
    setSelectCategory(keys);
  };

  const handleSampleActiveChange = (checked: boolean) => {
    console.log(checked);
  };

  const topSection = (
    <TopSection title={t(`manage.manageTitle`)} content={t(`manage.description`)} />
  );

  const leftSection = (
    <div className={`w-full h-full flex flex-col`}>
      <Spin spinning={treeLoading}>
        <div className='min-h-[370px] overflow-auto'>
          {/* <div className="flex items-center mb-4">
            <Input
              size="small"
              className="flex-1"
              placeholder={`${t('common.search')}`}
              onChange={(e) => console.log(e)}
              value={searchValue}
            />
            <Button type="primary" size="small" icon={<PlusOutlined />} className="ml-2" onClick={() => openModal({ type: 'addCategory', title: 'add', form: null })} />
          </div> */}
          <Tree
            className="w-full flex-1"
            showLine
            blockNode
            expandAction={false}
            defaultExpandAll
            autoExpandParent
            // defaultSelectedKeys={['hardware']}
            selectedKeys={selectCategory}
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
      title: t(`manage.delCategory`),
      okText: t(`common.confirm`),
      cancelText: t(`common.cancel`),
      onOk: async () => {
        try {
          await deleteCategory(id);
          message.success(t(`common.delSuccess`));
        } catch (e) {
          console.log(e);
          message.error(t(`common.delFailed`));
        } finally {
          getAllTreeData();
        }
      }
    })
  };

  const handleDelCapability = async (id: number) => {
    setConfirmLoading(true);
    try {
      await deleteCapability(id);
    } catch (e) {
      console.log(e);
    } finally {
      setConfirmLoading(false);
    }
  };

  const rightSection = (
    <>
      <div className='flex justify-end mb-4'>
        <Search className='w-[240px] mr-4' placeholder={t(`common.search`)} enterButton onSearch={onSearch} />
        <Button
          type='primary'
          icon={<PlusOutlined />}
          onClick={() => openSampleModal({ type: 'add', title: 'add', form: { category: selectCategory } })}>
          {t(`common.add`)}
        </Button>
      </div>
      <CustomTable
        rowKey='id'
        columns={columns}
        loading={tableLoading}
        dataSource={tableData}
      />
    </>
  );

  const onSuccess = () => {
    getAllTreeData();
  };

  return (
    <>
      <PageLayout
        rightSection={rightSection}
        leftSection={leftSection}
        topSection={topSection}
      />
      <CategoryManageModal ref={categoryModalRef} onSuccess={onSuccess} />
      <SampleManageModal ref={sampleModalRef} onSuccess={onSuccess} />
    </>
  )
};

export default PlaygroundManage;
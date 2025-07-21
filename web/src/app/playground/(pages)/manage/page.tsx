"use client"
import PageLayout from '@/components/page-layout';
import CustomTable from '@/components/custom-table';
import TopSection from '@/components/top-section';
import { ColumnItem } from '@/types';
import type { DataNode as TreeDataNode } from 'antd/lib/tree';
import { Input, Button, Tree, Spin, Dropdown, Menu } from 'antd';
import { PlusOutlined, MoreOutlined } from '@ant-design/icons';
import { useTranslation } from '@/utils/i18n';
import { useEffect, useState, useRef } from 'react';
import usePlayroundApi from '@/app/playground/api';
import ManageModal from './manageModal';
import { ModalRef, TableData } from '@/app/playground/types';
const { Search } = Input;

const PlaygroundManage = () => {
  const { t } = useTranslation();
  const { getCategoryList, getCapabilityList } = usePlayroundApi();
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
    setFilteredTreeData(
      [{
        key: 'anomaly',
        title: renderTitle('异常检测'),
        selectable: false,
        children: [
          {
            key: 'hardware',
            title: "硬件异常检测"
          }
        ]
      },
      {
        key: 'log',
        title: renderTitle("日志"),
        selectable: false,
        children: [
          {
            key: 'logs',
            title: "日志"
          }
        ]
      }
      ]
    );

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

  const getAllCategory = async () => {
    setTreeLoading(true);
    try {
      const data = await getCategoryList();
      console.log(data);
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

  const renderTitle = (title: string) => {
    return (
      <div className='w-full flex justify-between'>
        <span className='truncate'>{title}</span>
        <span>
          <Dropdown
            overlay={
              <Menu
                onClick={({ key, domEvent }) => {
                  domEvent.stopPropagation();
                  console.log(key);
                }}
                items={[
                  {
                    key: 'add',
                    label: t(`common.add`)
                  },
                  {
                    key: 'update',
                    label: t(`common.update`)
                  },
                  {
                    key: 'delete',
                    label: t(`common.delete`)
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

  const handleAdd = (type: string) => {
    modalRef.current?.showModal({ type: type, title: 'add', form: {} })
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
            <Button type="primary" size="small" icon={<PlusOutlined />} className="ml-2" onClick={() => handleAdd('addCategory')} />
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

  const rightSection = (
    <>
      <div className='flex justify-end mb-4'>
        <Search className='w-[240px] mr-4' placeholder={t(`common.search`)} enterButton onSearch={onSearch} />
        <Button type='primary' icon={<PlusOutlined />} onClick={() => handleAdd('addCapability')}>添加</Button>
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
      <ManageModal ref={modalRef} />
    </>
  )
};

export default PlaygroundManage;
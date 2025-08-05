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
  message,
  Popconfirm,
  Switch,
} from 'antd';
import EllipsisWithTooltip from '@/components/ellipsis-with-tooltip';
import PermissionWrapper from '@/components/permission';
import { PlusOutlined } from '@ant-design/icons';
import { useTranslation } from '@/utils/i18n';
import { useLocalizedTime } from "@/hooks/useLocalizedTime";
import { useEffect, useState, useRef, useMemo } from 'react';
import usePlayroundApi from '@/app/playground/api';
import CategoryManageModal from './categoryManageModal';
import SampleManageModal from './sampleManageModal';
import { ModalRef, TableData } from '@/app/playground/types';
const { Search } = Input;

const PlaygroundManage = () => {
  const { t } = useTranslation();
  const { convertToLocalizedTime } = useLocalizedTime();
  const {
    getServingsList,
    getAllSampleFileList,
    updateSampleFile,
    deleteSampleFile
  } = usePlayroundApi();
  const categoryModalRef = useRef<ModalRef>(null);
  const sampleModalRef = useRef<ModalRef>(null);
  const [tableLoading, setTableLoading] = useState<boolean>(false);
  const [treeLoading, setTreeLoading] = useState<boolean>(false);
  const [confirmLoading, setConfirmLoading] = useState<boolean>(false);
  // const [searchValue, setSearchValue] = useState<string>('');
  const [selectServing, setSelectServing] = useState<number[]>([]);
  const [tableData, setTableData] = useState<TableData[]>([]);
  const [filteredTreeData, setFilteredTreeData] = useState<TreeDataNode[]>([]);
  const columns: ColumnItem[] = [
    {
      title: t(`common.name`),
      dataIndex: 'name',
      key: 'name'
    },
    {
      title: t(`manage.createAt`),
      dataIndex: 'created_at',
      key: 'created_at',
      render: (_, record) => {
        return (<p>{convertToLocalizedTime(record.created_at, 'YYYY-MM-DD HH:mm:ss')}</p>)
      }
    },
    {
      title: t(`manage.createdBy`),
      dataIndex: 'created_by',
      key: 'created_by',
      render: (_, { created_by }) => {
        return created_by ? (
          <div className="flex h-full items-center" title={created_by}>
            <span
              className="block w-[18px] h-[18px] leading-[18px] text-center content-center rounded-[50%] mr-2 text-white"
              style={{ background: 'blue' }}
            >
              {created_by.slice(0, 1).toLocaleUpperCase()}
            </span>
            <span>
              <EllipsisWithTooltip
                className="w-full overflow-hidden text-ellipsis whitespace-nowrap"
                text={created_by}
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
        return <PermissionWrapper requiredPermissions={['Edit']}>
          <Switch checked={record.is_active} onChange={(value: boolean) => handleSampleActiveChange(record?.id, value)} />
        </PermissionWrapper>
      }
    },
    {
      title: t(`common.action`),
      dataIndex: 'action',
      key: 'action',
      render: (_, record) => {
        return (
          <>
            <PermissionWrapper requiredPermissions={['Delete']}>
              <Popconfirm
                title={t(`manage.delCapability`)}
                description={t(`manage.delCapabilityText`)}
                okText={t('common.confirm')}
                cancelText={t('common.cancel')}
                okButtonProps={{ loading: confirmLoading }}
                onConfirm={() => handleDelSampleFile(record.id)}
              >
                <Button type='link' danger>{t(`common.delete`)}</Button>
              </Popconfirm>
            </PermissionWrapper>
          </>
        )
      }
    }
  ];

  const pageData = useMemo(() => {
    return tableData.filter((item: any) => {
      const [serving_id] = selectServing
      return item.serving?.toString() === serving_id;
    })
  }, [tableData, selectServing]);

  useEffect(() => {
    getAllTreeData();
    setTableLoading(true);
    getAllSampleFile();
    setTableLoading(false);
  }, []);

  const renderNode = (servingsList: any[]) => {
    const filterData = servingsList.filter(item => item.status === 'active');
    const treeData = filterData.map((item: any) => {
      const node: any = {
        key: `${item.id}`,
        name: item?.name,
        title: renderTitle(item?.name),
      };
      return node;
    });

    return treeData;
  };

  const renderTitle = (title: string) => {
    return (<div className='w-full flex justify-between'>
      <span className='truncate'>{title}</span>
    </div>)
  }

  const getAllTreeData = async () => {
    setTreeLoading(true);
    try {
      const data = await getServingsList();
      const nodes = [
        {
          key: 'model_experience',
          name: 'model_experience',
          selectable: false,
          title: renderTitle('模型体验'),
          children: [
            {
              key: 'anomaly_detection',
              name: 'anomaly_detection',
              title: renderTitle('异常检测'),
              selectable: false,
              children: renderNode(data)
            }
          ]
        },
        {
          key: 'agent_experience',
          name: 'agent_experience',
          selectable: false,
          title: renderTitle('智能体体验')
        }
      ];
      setFilteredTreeData(nodes);
    } catch (e) {
      console.log(e)
    } finally {
      setTreeLoading(false);
    }
  };

  const getAllSampleFile = async () => {
    setTableLoading(true);
    try {
      const data = await getAllSampleFileList();
      const items = data?.map((item: any) => ({
        id: item?.id,
        name: item?.name,
        created_at: item?.created_at,
        created_by: item?.created_by,
        is_active: item?.is_active,
        serving: item?.serving
      }));
      setTableData(items)
    } catch (e) {
      console.log(e);
      message.error('获取样本文件错误');
    } finally {
      setTableLoading(false);
    }
  };

  const renderTreeNode = () => {
    return filteredTreeData
  };

  const openSampleModal = (data: {
    type: string;
    title: string;
    form: any
  }) => {
    sampleModalRef.current?.showModal(data);
  }

  const onSelect = (keys: any) => {
    setSelectServing(keys);
  };

  const handleSampleActiveChange = async (id: number, checked: boolean) => {
    setTableLoading(true);
    try {
      const params = {
        is_active: checked
      };
      await updateSampleFile(id, params);
    } catch (e) {
      console.log(e);
      message.error(t(`common.updateFailed`));
    } finally {
      getAllSampleFile();
    }
  };

  const topSection = (
    <TopSection title={t(`manage.manageTitle`)} content={t(`manage.description`)} />
  );

  const leftSection = (
    <div className={`w-full h-full flex flex-col`}>
      <Spin spinning={treeLoading}>
        <div className='min-h-[370px] overflow-auto'>

          <Tree
            className="w-full flex-1"
            showLine
            blockNode
            expandAction={false}
            defaultExpandAll
            autoExpandParent
            selectedKeys={selectServing}
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

  const handleDelSampleFile = async (id: number) => {
    setConfirmLoading(true);
    try {
      await deleteSampleFile(id);
    } catch (e) {
      console.log(e);
      message.error(t(`common.delFailed`));
    } finally {
      setConfirmLoading(false);
      getAllSampleFile();
    }
  };

  const rightSection = (
    <>
      <div className='flex justify-end mb-4'>
        <Search className='w-[240px] mr-4' placeholder={t(`common.search`)} enterButton onSearch={onSearch} />
        <PermissionWrapper requiredPermissions={['Add']}>
          <Button
            type='primary'
            icon={<PlusOutlined />}
            disabled={!selectServing.length}
            onClick={() => openSampleModal({ type: 'add', title: 'add', form: { serving_id: selectServing } })}>
            {t(`common.add`)}
          </Button>
        </PermissionWrapper>

      </div>
      <CustomTable
        rowKey='id'
        columns={columns}
        loading={tableLoading}
        dataSource={pageData}
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
      <SampleManageModal ref={sampleModalRef} onSuccess={getAllSampleFile} />
    </>
  )
};

export default PlaygroundManage;
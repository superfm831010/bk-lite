import { Button, message, Popconfirm, Tabs, Breadcrumb, Input } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import CustomTable from "@/components/custom-table";
import RasaModal from "./rasaModel";
import type { TabsProps } from 'antd';
import { useSearchParams } from "next/navigation";
import { useTranslation } from "@/utils/i18n";
import { useEffect, useMemo, useRef, useState } from "react";
import { ColumnItem } from "@/types";
import { ModalRef, TableData } from "@/app/mlops/types";
import useMlopsManageApi from "@/app/mlops/api/manage";
const { Search } = Input;

const RasaDetail = () => {
  const { t } = useTranslation();
  const searchParams = useSearchParams();
  const modalRef = useRef<ModalRef>(null);
  const {
    getRasaIntentFileList,
    deleteRasaIntentFile,
    getRasaResponseFileList,
    deleteRasaResponseFile,
    getRasaRuleFileList,
    deleteRasaRuleFile,
    getRasaStoryFileList,
    deleteRasaStoryFile,
    getRasaEntityList,
    deleteRasaEntityFile
  } = useMlopsManageApi();
  const [selectKey, setSelectKey] = useState<string>('intent');
  const [loading, setLoading] = useState<boolean>(false);
  const [tableData, setTableData] = useState<TableData[]>([]);

  const btnsElements = (record: any) => (<>
    <Button type="link" className="mr-2" onClick={() => handleEdit(record)}>{t(`common.edit`)}</Button>
    <Popconfirm
      title={t(`common.delConfirm`)} 
      description={t(`common.delConfirmCxt`)}
      okText={t('common.confirm')}
      cancelText={t('common.cancel')}
      onConfirm={() => handleDel(record.id)}
    >
      <Button type="link" danger>{t(`common.delete`)}</Button>
    </Popconfirm>
  </>);

  const columnsMap: Record<string, ColumnItem[]> = {
    'intent': [
      {
        title: t(`datasets.intentName`),
        dataIndex: 'name',
        key: 'name'
      },
      {
        title: t(`datasets.exampleNum`),
        dataIndex: 'example_count',
        key: 'example_count'
      },
      {
        title: t(`common.action`),
        dataIndex: 'action',
        key: 'action',
        width: 180,
        render: (_, record) => btnsElements(record)
      }
    ],
    'story': [
      {
        title: t(`datasets.storyName`),
        dataIndex: 'name',
        key: 'name'
      },
      {
        title: t(`datasets.intentNum`),
        dataIndex: 'intent_count',
        key: 'intent_count'
      },
      {
        title: t(`datasets.responseNum`),
        dataIndex: 'response_count',
        key: 'response_count'
      },
      {
        title: t(`common.action`),
        dataIndex: 'action',
        key: 'action',
        width: 180,
        render: (_, record) => btnsElements(record)
      }
    ],
    'response': [
      {
        title: t(`datasets.responseName`),
        dataIndex: 'name',
        key: 'name'
      },
      {
        title: t(`datasets.responseNum`),
        dataIndex: 'example_count',
        key: 'example_count'
      },
      {
        title: t(`common.action`),
        dataIndex: 'action',
        key: 'action',
        width: 180,
        render: (_, record) => btnsElements(record)
      }
    ],
    'rule': [
      {
        title: t(`datasets.ruleName`),
        dataIndex: 'name',
        key: 'name'
      },
      {
        title: t(`datasets.intentNum`),
        dataIndex: 'intent_count',
        key: 'intent_count'
      },
      {
        title: t(`datasets.responseNum`),
        dataIndex: 'response_count',
        key: 'response_count'
      },
      {
        title: t(`common.action`),
        dataIndex: 'action',
        key: 'action',
        width: 180,
        render: (_, record) => btnsElements(record)
      }
    ],
    'entity': [
      {
        title: t(`datasets.entityName`),
        key: 'name',
        dataIndex: 'name'
      },
      {
        title: t(`common.type`),
        key: 'entity_type',
        dataIndex: 'entity_type'
      },
      {
        title: t(`datasets.exampleNum`),
        key: 'example_count',
        dataIndex: 'example_count',
        render: (_, record) => (
          <p className="truncate w-full">{record.example_count || '--'}</p>
        )
      },
      {
        title: t(`common.action`),
        key: 'action',
        dataIndex: 'action',
        render: (_ ,record) => btnsElements(record)
      }
    ]
  };

  const getFileMap: Record<string, any> = {
    'intent': getRasaIntentFileList,
    'response': getRasaResponseFileList,
    'rule': getRasaRuleFileList,
    'story': getRasaStoryFileList,
    'entity': getRasaEntityList
  };

  const delFileMap: Record<string, any> = {
    'intent': deleteRasaIntentFile,
    'response': deleteRasaResponseFile,
    'rule': deleteRasaRuleFile,
    'story': deleteRasaStoryFile,
    'entity': deleteRasaEntityFile
  };

  const {
    folder_id,
    // folder_name,
    // description,
    // activeTap
  } = useMemo(() => ({
    folder_id: searchParams.get('folder_id'),
    folder_name: searchParams.get('folder_name') || '',
    description: searchParams.get('description') || '',
    activeTap: searchParams.get('activeTap') || ''
  }), [searchParams]);

  const items: () => TabsProps['items'] = () => {
    return [
      {
        key: 'intent',
        label: t(`datasets.intent`),
        children: renderTable('intent'),
      },
      {
        key: 'response',
        label: t(`datasets.response`),
        children: renderTable('response'),
      },
      {
        key: 'rule',
        label: t(`datasets.rule`),
        children: renderTable('rule')
      },
      {
        key: 'story',
        label: t(`datasets.story`),
        children: renderTable('story'),
      },
      {
        key: 'entity',
        label: t(`datasets.entity`),
        children: renderTable('entity')
      }
    ]
  };

  useEffect(() => {
    if (selectKey) {
      getTableData();
    }
  }, [selectKey])

  const renderTable = (key: string) => {
    return (
      <CustomTable rowKey="id" loading={loading} columns={columnsMap[key]} dataSource={tableData} />
    )
  };

  const getTableData = async (search: string = '') => {
    setLoading(true);
    try {
      const data = await getFileMap[selectKey]({ name: search, dataset: folder_id });
      setTableData(data);
    } catch (e) {
      console.log(e);
      message.error(t(`common.fetchFailed`));
      setTableData([]);
    } finally {
      setLoading(false);
    }
  };

  const onChange = (key: string) => {
    setSelectKey(key);
  };

  const onSearch = (value: string) => {
    getTableData(value);
  }

  const handleAdd = () => {
    modalRef.current?.showModal({ type: 'add', title: `add${selectKey}`, form: { dataset: folder_id } })
  };

  const handleEdit = (record: any) => {
    modalRef.current?.showModal({ type: 'edit', title: `edit${selectKey}`, form: { ...record } })
  };

  const handleDel = async (id: number) => {
    try {
      await delFileMap[selectKey](id);
      message.success(t(`common.delSuccess`));
    } catch (e) {
      console.log(e);
      message.error(t(`common.delFailed`));
    } finally {
      getTableData();
    }
  };

  return (
    <>
      <div className="w-full h-full relative">
        <div className="absolute right-0 top-8 z-10">
          <Search
            className="w-[240px] mr-1.5"
            placeholder={t('common.search')}
            enterButton
            onSearch={onSearch}
            style={{ fontSize: 15 }}
          />
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            {t(`common.add`)}
          </Button>
        </div>
        <div>
          <Breadcrumb
            separator=">"
            items={[
              {
                title: <a href="/mlops/manage">{t(`datasets.datasets`)}</a>
              },
              {
                title: t(`datasets.datasetsDetail`)
              }
            ]}
          />
        </div>
        <Tabs defaultActiveKey="1" items={items()} onChange={onChange} />
      </div>
      <RasaModal ref={modalRef} selectKey={selectKey} folder_id={folder_id as string} onSuccess={() => getTableData()} />
    </>
  )
};

export default RasaDetail;
'use client';
import React, { useState, useEffect, useCallback } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Input, Button, Modal, message, Tag, Tabs, Tooltip, Dropdown, Menu, Space, Radio, Upload } from 'antd';
import { PlusOutlined, DeleteOutlined, TrademarkOutlined, SyncOutlined, DownOutlined, InboxOutlined } from '@ant-design/icons';
import { useAuth } from '@/context/auth';
import { useTranslation } from '@/utils/i18n';
import { useLocalizedTime } from '@/hooks/useLocalizedTime';
import type { TableColumnsType, PaginationProps } from 'antd';
import CustomTable from '@/components/custom-table';
import PermissionWrapper from '@/components/permission';
import SelectSourceModal from './selectSourceModal';
import { TableData, QAPairData } from '@/app/opspilot/types/knowledge'
import styles from '@/app/opspilot/styles/common.module.scss'
import ActionButtons from '@/app/opspilot/components/knowledge/actionButtons';
import { useKnowledgeApi } from '@/app/opspilot/api/knowledge';
import KnowledgeGraphPage from '@/app/opspilot/components/knowledge/knowledgeGraphPage';
import OperateModal from '@/components/operate-modal';

const { confirm } = Modal;
const { TabPane } = Tabs;
const { Search } = Input;
const { Dragger } = Upload;

const DocumentsPage: React.FC = () => {
  const router = useRouter();
  const { t } = useTranslation();
  const authContext = useAuth();
  const { convertToLocalizedTime } = useLocalizedTime();
  const searchParams = useSearchParams();
  const id = searchParams ? searchParams.get('id') : null;
  const name = searchParams ? searchParams.get('name') : null;
  const desc = searchParams ? searchParams.get('desc') : null;
  const type = searchParams ? searchParams.get('type') : null;

  const [mainTabKey, setMainTabKey] = useState<string>(['knowledge_graph', 'qa_pairs'].includes(type || '') ? type || 'qa_pairs' : 'source_files');
  const [activeTabKey, setActiveTabKey] = useState<string>(() => {
    if (type === 'knowledge_graph' || type === 'qa_pairs') {
      return type;
    }
    if (['file', 'web_page', 'manual'].includes(type || '')) {
      return type || 'file';
    }
    return 'file';
  });

  const [searchText, setSearchText] = useState<string>('');
  const [pagination, setPagination] = useState<PaginationProps>({
    current: 1,
    total: 0,
    pageSize: 20,
  });
  const [loading, setLoading] = useState<boolean>(false);
  const [tableData, setTableData] = useState<TableData[]>([]);
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [isTrainLoading, setIsTrainLoading] = useState(false);
  const [singleTrainLoading, setSingleTrainLoading] = useState<{ [key: string]: boolean }>({});
  const [uploadedFiles, setUploadedFiles] = useState<any[]>([]);

  const [qaPairData, setQaPairData] = useState<QAPairData[]>([]);
  const [qaPairPagination, setQaPairPagination] = useState<PaginationProps>({
    current: 1,
    total: 0,
    pageSize: 20,
  });
  const [qaPairLoading, setQaPairLoading] = useState<boolean>(false);
  const [selectedQAPairKeys, setSelectedQAPairKeys] = useState<React.Key[]>([]);
  const [uploadModalVisible, setUploadModalVisible] = useState(false);
  const [confirmLoading, setConfirmLoading] = useState(false);

  const {
    fetchDocuments,
    batchDeleteDocuments,
    batchTrainDocuments,
    fetchQAPairs,
    deleteQAPair,
    fetchKnowledgeBaseDetails: fetchKnowledgeBaseDetailsApi,
    importQaJson
  } = useKnowledgeApi();

  const randomColors = ['#ff9214', '#875cff', '#00cba6', '#155aef'];

  const [knowledgeBasePermissions, setKnowledgeBasePermissions] = useState<string[]>([]);

  const getRandomColor = () => randomColors[Math.floor(Math.random() * randomColors.length)];

  const fetchKnowledgeBaseDetails = async () => {
    if (!id) return;

    try {
      const details = await fetchKnowledgeBaseDetailsApi(Number(id));
      setKnowledgeBasePermissions(details.permissions || []);
    } catch (error) {
      console.error('Failed to fetch knowledge base details:', error);
      setKnowledgeBasePermissions([]);
    }
  };

  useEffect(() => {
    fetchKnowledgeBaseDetails();
  }, []);

  const columns: TableColumnsType<TableData> = [
    {
      title: t('knowledge.documents.name'),
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <a
          href="#"
          style={{ color: '#155aef' }}
          onClick={() => router.push(`/opspilot/knowledge/detail/documents/result?id=${id}&name=${name}&desc=${desc}&knowledgeId=${record.id}`)}
        >
          {text}
        </a>
      ),
    },
    {
      title: t('knowledge.documents.chunkSize'),
      dataIndex: 'chunk_size',
      key: 'chunk_size',
    },
    {
      title: t('knowledge.documents.createdAt'),
      dataIndex: 'created_at',
      key: 'created_at',
      render: (text) => convertToLocalizedTime(text),
    },
    {
      title: t('knowledge.documents.createdBy'),
      key: 'created_by',
      dataIndex: 'created_by',
      render: (_, { created_by }) => (
        <div>
          <div
            className='inline-block text-center rounded-full text-white mr-2'
            style={{ width: 20, height: 20, backgroundColor: getRandomColor() }}
          >
            {created_by.charAt(0).toUpperCase()}
          </div>
          {created_by}
        </div>
      ),
    },
    {
      title: t('knowledge.documents.status'),
      key: 'train_status',
      dataIndex: 'train_status',
      render: (_, { train_status, train_status_display }) => {
        const statusColors: { [key: string]: string } = {
          '0': 'orange',
          '1': 'green',
          '2': 'red',
        };

        const color = statusColors[train_status] || 'geekblue';
        const text = train_status_display || '--';

        return <Tag color={color}>{text}</Tag>;
      },
    },
    ...(activeTabKey === 'web_page' ? [{
      title: t('knowledge.documents.syncEnabled'),
      key: 'sync_enabled',
      dataIndex: 'sync_enabled',
      render: (_: any, record: TableData) => {
        const syncEnabled = record.sync_enabled;
        const syncTime = record.sync_time;

        if (syncEnabled && syncTime) {
          return (
            <div>
              {syncTime && <div>【{t('knowledge.documents.everyday')} {syncTime}】</div>}
            </div>
          );
        } else {
          return <div>【未定时同步】</div>;
        }
      },
    }] : []),
    {
      title: t('knowledge.documents.extractionMethod'),
      key: 'mode',
      dataIndex: 'mode',
      render: (_, { mode }) => {
        const modeMap: { [key: string]: string } = {
          'full': t('knowledge.documents.fullTextExtraction'),
          'paragraph': t('knowledge.documents.chapterExtraction'),
          'page': t('knowledge.documents.pageExtraction'),
          'excel_full_content_parse': t('knowledge.documents.worksheetExtraction'),
          'excel_header_row_parse': t('knowledge.documents.rowExtraction'),
        };
        const text = modeMap[mode] || t('knowledge.documents.fullTextExtraction');
        return <span>{text}</span>;
      },
    },
    {
      title: t('knowledge.documents.chunkingMethod'),
      key: 'chunk_type',
      dataIndex: 'chunk_type',
      render: (_, { chunk_type }) => {
        const chunkMap: { [key: string]: string } = {
          'fixed_size': t('knowledge.documents.fixedChunk'),
          'recursive': t('knowledge.documents.overlapChunk'),
          'semantic': t('knowledge.documents.semanticChunk'),
          'full': t('knowledge.documents.noChunk'),
        };
        const text = chunkMap[chunk_type] || t('knowledge.documents.fixedChunk');
        return <span>{text}</span>;
      },
    },
    {
      title: t('knowledge.documents.actions'),
      key: 'action',
      render: (_, record) => (
        <ActionButtons
          record={record}
          isFile={activeTabKey === 'file'}
          instPermissions={knowledgeBasePermissions}
          singleTrainLoading={singleTrainLoading}
          onTrain={handleTrain}
          onDelete={handleDelete}
          onSet={handleSetClick}
          onFileAction={handleFile}
        />
      ),
    }
  ];

  const qaPairColumns: TableColumnsType<QAPairData> = [
    {
      title: t('knowledge.qaPairs.name'),
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <a
          href="#"
          style={{ color: '#155aef' }}
          onClick={() => router.push(`/opspilot/knowledge/detail/documents/qapair/result?id=${id}&name=${name}&desc=${desc}&qaPairId=${record.id}`)}
        >
          {text}
        </a>
      ),
    },
    {
      title: t('knowledge.qaPairs.qaCount'),
      dataIndex: 'qa_count',
      key: 'qa_count',
    },
    {
      title: t('knowledge.documents.createdAt'),
      dataIndex: 'created_at',
      key: 'created_at',
      render: (text) => convertToLocalizedTime(text),
    },
    {
      title: t('knowledge.documents.createdBy'),
      key: 'created_by',
      dataIndex: 'created_by',
      render: (_, { created_by }) => (
        <div>
          <div
            className='inline-block text-center rounded-full text-white mr-2'
            style={{ width: 20, height: 20, backgroundColor: getRandomColor() }}
          >
            {created_by.charAt(0).toUpperCase()}
          </div>
          {created_by}
        </div>
      ),
    },
    {
      title: t('knowledge.documents.actions'),
      key: 'action',
      render: (_, record) => (
        <PermissionWrapper
          requiredPermissions={['Delete']}
          instPermissions={knowledgeBasePermissions}>
          <Button
            type="link"
            size="small"
            onClick={() => handleDeleteSingleQAPair(record.id)}
          >
            {t('common.delete')}
          </Button>
        </PermissionWrapper>
      ),
    }
  ];

  // Fetch QA pair data
  const fetchQAPairData = useCallback(async (text = '') => {
    setQaPairLoading(true);
    const { current, pageSize } = qaPairPagination;
    const params = {
      name: text,
      page: current,
      page_size: pageSize,
      knowledge_base_id: id
    };
    try {
      const res = await fetchQAPairs(params);
      const { items: data, count } = res;
      setQaPairData(data);
      setQaPairPagination(prev => ({
        ...prev,
        total: count,
      }));
    } catch {
      message.error(t('common.fetchFailed'));
    } finally {
      setQaPairLoading(false);
    }
  }, [qaPairPagination.current, qaPairPagination.pageSize, id]);

  const handleDeleteSingleQAPair = async (qaPairId: number) => {
    confirm({
      title: t('common.delConfirm'),
      content: t('common.delConfirmCxt'),
      centered: true,
      onOk: async () => {
        try {
          await deleteQAPair(qaPairId);
          fetchQAPairData();
          setSelectedQAPairKeys([]);
          message.success(t('common.delSuccess'));
        } catch {
          message.error(t('common.delFailed'));
        }
      },
    });
  };

  // Batch delete QA pairs
  const handleBatchDeleteQAPairs = async () => {
    if (selectedQAPairKeys.length === 0) {
      message.warning('Please select QA pairs to delete');
      return;
    }

    confirm({
      title: t('common.delConfirm'),
      content: t('common.delConfirmCxt'),
      centered: true,
      onOk: async () => {
        try {
          // Call individual delete API for each item during batch deletion
          await Promise.all(selectedQAPairKeys.map(key => deleteQAPair(Number(key))));
          fetchQAPairData();
          setSelectedQAPairKeys([]);
          message.success(t('common.delSuccess'));
        } catch {
          message.error(t('common.delFailed'));
          setSelectedQAPairKeys([]);
        }
      },
    });
  };

  // Handle QA pair pagination
  const handleQAPairTableChange = (page: number, pageSize?: number) => {
    setQaPairPagination((prev) => ({
      ...prev,
      current: page,
      pageSize: pageSize || prev.pageSize,
    }));
  };

  // QA pair row selection
  const qaPairRowSelection = {
    selectedRowKeys: selectedQAPairKeys,
    onChange: (newSelectedRowKeys: React.Key[]) => {
      setSelectedQAPairKeys(newSelectedRowKeys);
    },
  };

  const handleFile = async (record: TableData, type: string) => {
    if (type === 'preview') {
      window.open(`/opspilot/knowledge/preview?id=${record.id}`);
      return;
    }
    try {
      const response = await fetch(`/opspilot/api/docFile?id=${record.id}`, {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${authContext?.token}`,
        },
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Failed to download file');
      }
      const blob = await response.blob();
      const fileUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = fileUrl;
      link.download = record.name;
      link.click();
      window.URL.revokeObjectURL(fileUrl);
    } catch (error) {
      console.error('Error downloading file:', error);
      alert('Failed to download file');
    }
  }

  const handleSetClick = (record: any) => {
    router.push(`/opspilot/knowledge/detail/documents/modify?type=${activeTabKey}&id=${id}&name=${name}&desc=${desc}&documentIds=${record.id}`);
  };

  const handleDelete = (keys: React.Key[]) => {
    confirm({
      title: t('common.delConfirm'),
      content: t('common.delConfirmCxt'),
      centered: true,
      onOk: async () => {
        try {
          await batchDeleteDocuments(keys, id);
          fetchData();
          setSelectedRowKeys([]);
          message.success(t('common.delSuccess'));
        } catch {
          message.error(t('common.delFailed'));
        }
      },
    });
  };

  const handleTrain = async (keys: React.Key[]) => {
    if (keys.length === 1) {
      setSingleTrainLoading((prev) => ({ ...prev, [keys[0].toString()]: true }));
    } else {
      setIsTrainLoading(true);
    }
    try {
      await batchTrainDocuments(keys);
      message.success(t('common.training'));
      fetchData();
    } catch {
      message.error(t('common.trainFailed'));
    } finally {
      if (keys.length === 1) {
        setSingleTrainLoading((prev) => ({ ...prev, [keys[0].toString()]: false }));
      } else {
        setIsTrainLoading(false);
      }
    }
  };

  const handleBatchSet = async (keys: React.Key[]) => {
    router.push(`/opspilot/knowledge/detail/documents/modify?type=${activeTabKey}&id=${id}&name=${name}&desc=${desc}&documentIds=${keys.join(',')}`);
  };

  const handleSearch = (value: string) => {
    setSearchText(value);
    setPagination((prev) => ({
      ...prev,
      current: 1,
    }));
  };

  const handleTableChange = (page: number, pageSize?: number) => {
    setPagination((prev) => ({
      ...prev,
      current: page,
      pageSize: pageSize || prev.pageSize,
    }));
  };

  const fetchData = useCallback(async (text = '', skipLoading = false) => {
    if (!skipLoading) {
      setLoading(true);
    }
    const { current, pageSize } = pagination;
    const params = {
      name: text,
      page: current,
      page_size: pageSize,
      knowledge_source_type: activeTabKey,
      knowledge_base_id: id
    };
    try {
      const res = await fetchDocuments(params);
      const { items: data } = res;
      setTableData(data);
      setPagination(prev => ({
        ...prev,
        total: res.count,
      }));

      if (data.some((item: any) => item.train_status === 0)) {
        const timer = setTimeout(() => fetchData(text, true), 10000);
        return () => clearTimeout(timer);
      }
    } catch {
      message.error(t('common.fetchFailed'));
    } finally {
      if (!skipLoading) {
        setLoading(false);
      }
    }
  }, [pagination.current, pagination.pageSize, searchText, activeTabKey]);

  useEffect(() => {
    if (mainTabKey === 'source_files') {
      fetchData(searchText);
    }
  }, [id, activeTabKey]);

  useEffect(() => {
    if (mainTabKey === 'qa_pairs') {
      fetchQAPairData(searchText);
    }
  }, [mainTabKey, qaPairPagination.current, qaPairPagination.pageSize, searchText]);

  const rowSelection = {
    selectedRowKeys,
    onChange: (newSelectedRowKeys: React.Key[]) => {
      setSelectedRowKeys(newSelectedRowKeys);
    },
    getCheckboxProps: (record: TableData) => ({
      disabled: record.train_status_display === 'Training',
    }),
  };

  const handleMainTabChange = (key: string) => {
    setMainTabKey(key);
    if (key === 'source_files') {
      setActiveTabKey('file');
    } else if (key === 'qa_pairs') {
      setActiveTabKey('qa_pairs');
    } else if (key === 'knowledge_graph') {
      setActiveTabKey('knowledge_graph');
    }
    setPagination({
      current: 1,
      total: 0,
      pageSize: 20,
    });
  };

  const handleSourceFileTypeChange = (e: any) => {
    const newType = e.target.value;
    setActiveTabKey(newType);
    setPagination({
      current: 1,
      total: 0,
      pageSize: 20,
    });
  };

  const handleAddClick = () => {
    setIsModalVisible(true);
  };

  const handleModalCancel = () => {
    setIsModalVisible(false);
  };

  const handleModalConfirm = (selectedType: string) => {
    setIsModalVisible(false);
    router.push(`/opspilot/knowledge/detail/documents/modify?type=${selectedType}&id=${id}&name=${name}&desc=${desc}`);
  }

  const handleUploadModalConfirm = async () => {
    if (uploadedFiles.length === 0) {
      message.error(t('knowledge.qaPairs.noFileSelected'));
      return;
    }

    try {
      setConfirmLoading(true);
      const formData = new FormData();
      formData.append('knowledge_base_id', id as string);
      uploadedFiles.forEach(file => formData.append('file', file));
      await importQaJson(formData);
      message.success(t('knowledge.qaPairs.importSuccess'));
      fetchQAPairData(searchText);
    } catch {
      message.error(t('knowledge.qaPairs.importFailed'));
    } finally {
      setConfirmLoading(false);
      setUploadModalVisible(false);
      setUploadedFiles([]);
    }
  };

  const handleImportClick = () => {
    setUploadModalVisible(true);
    setUploadedFiles([]);
  };

  const handleFileUpload = (file: any) => {
    setUploadedFiles(prev => [...prev, file]);
    return false;
  };

  const batchOperationMenu = (
    <Menu className={styles.batchOperationMenu}>
      <Menu.Item key="batchTrain">
        <PermissionWrapper
          requiredPermissions={['Train']}
          instPermissions={knowledgeBasePermissions}>
          <Button
            type="text"
            className="w-full"
            icon={<TrademarkOutlined />}
            onClick={() => handleTrain(selectedRowKeys)}
            disabled={!selectedRowKeys.length}
            loading={isTrainLoading}
          >
            {t('common.batchTrain')}
          </Button>
        </PermissionWrapper>
      </Menu.Item>
      <Menu.Item key="batchDelete">
        <PermissionWrapper
          requiredPermissions={['Delete']}
          instPermissions={knowledgeBasePermissions}>
          <Button
            type="text"
            className="w-full"
            icon={<DeleteOutlined />}
            onClick={() => handleDelete(selectedRowKeys)}
            disabled={!selectedRowKeys.length}
          >
            {t('common.batchDelete')}
          </Button>
        </PermissionWrapper>
      </Menu.Item>
      <Menu.Item key="batchSet">
        <PermissionWrapper
          requiredPermissions={['Set']}
          instPermissions={knowledgeBasePermissions}>
          <Button
            type="text"
            className="w-full"
            icon={<TrademarkOutlined />}
            onClick={() => handleBatchSet(selectedRowKeys)}
            disabled={!selectedRowKeys.length}
          >
            {t('knowledge.documents.batchSet')}
          </Button>
        </PermissionWrapper>
      </Menu.Item>
    </Menu>
  );

  const menuProps = (
    <Menu className={styles.batchOperationMenu}>
      <Menu.Item key="create">
        <PermissionWrapper
          requiredPermissions={['Add']}
          instPermissions={knowledgeBasePermissions}>
          <Button
            type="text"
            className="w-full"
            onClick={() => router.push(`/opspilot/knowledge/detail/documents/modify?type=qa_pairs&id=${id}&name=${name}&desc=${desc}`)}
          >
            {t('common.create')}
          </Button>
        </PermissionWrapper>
      </Menu.Item>
      <Menu.Item key="import">
        <PermissionWrapper
          requiredPermissions={['Add']}
          instPermissions={knowledgeBasePermissions}>
          <Button
            type="text"
            className="w-full"
            onClick={handleImportClick}
          >
            {t('common.import')}
          </Button>
        </PermissionWrapper>
      </Menu.Item>
    </Menu>
  );

  return (
    <div style={{ marginTop: '-10px' }}>
      <Tabs activeKey={mainTabKey} onChange={handleMainTabChange}>
        <TabPane tab={t('knowledge.sourceFiles')} key='source_files' />
        <TabPane tab={t('knowledge.qaPairs.title')} key='qa_pairs' />
        <TabPane tab={t('knowledge.knowledgeGraph.title')} key='knowledge_graph' />
      </Tabs>
      <div className='nav-box flex justify-between mb-[20px]'>
        <div className='left-side'>
          {mainTabKey === 'source_files' && (
            <Radio.Group
              value={activeTabKey}
              onChange={handleSourceFileTypeChange}
            >
              <Radio.Button value="file">{t('knowledge.localFile')}</Radio.Button>
              <Radio.Button value="web_page">{t('knowledge.webLink')}</Radio.Button>
              <Radio.Button value="manual">{t('knowledge.cusText')}</Radio.Button>
            </Radio.Group>
          )}
        </div>
        <div className='right-side flex items-center'>
          {mainTabKey !== 'knowledge_graph' && (
            <>
              <Search
                placeholder={`${t('common.search')}...`}
                allowClear
                onSearch={handleSearch}
                enterButton
                className="w-60 mr-[8px]"
              />
              <Tooltip className='mr-[8px]' title={t('common.refresh')}>
                <Button icon={<SyncOutlined />} onClick={() => fetchData()} />
              </Tooltip>
              {activeTabKey !== 'qa_pairs' && (
                <>
                  <PermissionWrapper
                    requiredPermissions={['Add']}
                    instPermissions={knowledgeBasePermissions}>
                    <Button
                      type='primary'
                      className='mr-[8px]'
                      icon={<PlusOutlined />}
                      onClick={handleAddClick}
                    >
                      {t('common.add')}
                    </Button>
                  </PermissionWrapper>
                  <Dropdown overlay={batchOperationMenu}>
                    <Button>
                      <Space>
                        {t('common.batchOperation')}
                        <DownOutlined />
                      </Space>
                    </Button>
                  </Dropdown>
                </>
              )}
              {activeTabKey === 'qa_pairs' && (
                <>
                  <Dropdown overlay={menuProps}>
                    <Button>
                      <Space>
                        {t('common.add')}
                        <DownOutlined />
                      </Space>
                    </Button>
                  </Dropdown>
                  <PermissionWrapper
                    requiredPermissions={['Delete']}
                    instPermissions={knowledgeBasePermissions}>
                    <Button
                      danger
                      icon={<DeleteOutlined />}
                      className="ml-[8px]"
                      onClick={handleBatchDeleteQAPairs}
                    >
                      {t('common.batchDelete')}{selectedQAPairKeys.length > 0 && ` (${selectedQAPairKeys.length})`}
                    </Button>
                  </PermissionWrapper>
                </>
              )}
            </>
          )}
        </div>
      </div>
      {activeTabKey === 'knowledge_graph' ? (
        <KnowledgeGraphPage 
          knowledgeBaseId={id} 
          name={name}
          desc={desc}
          type={activeTabKey}
        />
      ) : activeTabKey === 'qa_pairs' ? (
        <CustomTable
          rowKey="id"
          rowSelection={qaPairRowSelection}
          scroll={{ y: 'calc(100vh - 430px)' }}
          columns={qaPairColumns}
          dataSource={qaPairData}
          pagination={{
            ...qaPairPagination,
            onChange: handleQAPairTableChange
          }}
          loading={qaPairLoading}
        />
      ) : (
        <CustomTable
          rowKey="id"
          rowSelection={rowSelection}
          scroll={{ y: 'calc(100vh - 430px)' }}
          columns={columns}
          dataSource={tableData}
          pagination={{
            ...pagination,
            onChange: handleTableChange
          }}
          loading={loading}
        />
      )}
      {mainTabKey === 'source_files' && (
        <SelectSourceModal
          defaultSelected={activeTabKey}
          visible={isModalVisible}
          onCancel={handleModalCancel}
          onConfirm={handleModalConfirm}
        />
      )}
      <OperateModal
        title={t('common.import')}
        centered
        visible={uploadModalVisible}
        confirmLoading={confirmLoading}
        onOk={handleUploadModalConfirm}
        onCancel={() => setUploadModalVisible(false)}
      >
        <div>
          <Dragger
            accept="application/json"
            beforeUpload={handleFileUpload}
          >
            <p className="ant-upload-drag-icon">
              <InboxOutlined />
            </p>
            <p className="ant-upload-text">{t('knowledge.qaPairs.dragOrClick')}</p>
            <p className="ant-upload-hint">{t('knowledge.qaPairs.uploadHint')}</p>
          </Dragger>
        </div>
      </OperateModal>
    </div>
  );
};

export default DocumentsPage;

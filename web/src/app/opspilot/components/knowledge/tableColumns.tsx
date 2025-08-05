import React from 'react';
import { Tag, Button } from 'antd';
import type { TableColumnsType } from 'antd';
import { TableData, QAPairData } from '@/app/opspilot/types/knowledge';
import PermissionWrapper from '@/components/permission';

interface RouterType {
  push: (url: string) => void;
}

export const getDocumentColumns = (
  t: (key: string) => string,
  activeTabKey: string,
  convertToLocalizedTime: (time: string) => string,
  getRandomColor: () => string,
  knowledgeBasePermissions: string[],
  singleTrainLoading: { [key: string]: boolean },
  onTrain: (keys: React.Key[]) => void,
  onDelete: (keys: React.Key[]) => void,
  onSet: (record: TableData) => void,
  onFileAction: (record: TableData, type: string) => void,
  router: RouterType,
  id: string | null,
  name: string | null,
  desc: string | null,
  ActionButtons: React.ComponentType<any>
): TableColumnsType<TableData> => [
  {
    title: t('knowledge.documents.name'),
    dataIndex: 'name',
    key: 'name',
    render: (text: string, record: TableData) => (
      <a
        href="#"
        style={{ color: '#155aef' }}
        onClick={(e) => {
          e.preventDefault();
          router.push(`/opspilot/knowledge/detail/documents/result?id=${id}&name=${name}&desc=${desc}&knowledgeId=${record.id}`);
        }}
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
    render: (text: string) => convertToLocalizedTime(text),
  },
  {
    title: t('knowledge.documents.createdBy'),
    key: 'created_by',
    dataIndex: 'created_by',
    render: (_: any, record: TableData) => (
      <div>
        <div
          className='inline-block text-center rounded-full text-white mr-2'
          style={{ width: 20, height: 20, backgroundColor: getRandomColor() }}
        >
          {record.created_by.charAt(0).toUpperCase()}
        </div>
        {record.created_by}
      </div>
    ),
  },
  {
    title: t('knowledge.documents.status'),
    key: 'train_status',
    dataIndex: 'train_status',
    render: (_: any, record: TableData) => {
      const statusColors: { [key: string]: string } = {
        '0': 'orange',
        '1': 'green',
        '2': 'red',
      };

      const color = statusColors[record.train_status?.toString()] || 'geekblue';
      const text = record.train_status_display || '--';

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
        return <div>【{t('knowledge.documents.notSync')}】</div>;
      }
    },
  }] : []),
  {
    title: t('knowledge.documents.extractionMethod'),
    key: 'mode',
    dataIndex: 'mode',
    render: (_: any, record: TableData) => {
      const mode = record.mode || 'full';
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
    render: (_: any, record: TableData) => {
      const chunkType = record.chunk_type || 'fixed_size';
      const chunkMap: { [key: string]: string } = {
        'fixed_size': t('knowledge.documents.fixedChunk'),
        'recursive': t('knowledge.documents.overlapChunk'),
        'semantic': t('knowledge.documents.semanticChunk'),
        'full': t('knowledge.documents.noChunk'),
      };
      const text = chunkMap[chunkType] || t('knowledge.documents.fixedChunk');
      return <span>{text}</span>;
    },
  },
  {
    title: t('knowledge.documents.actions'),
    key: 'action',
    render: (_: any, record: TableData) => (
      <ActionButtons
        record={record}
        isFile={activeTabKey === 'file'}
        instPermissions={knowledgeBasePermissions}
        singleTrainLoading={singleTrainLoading}
        onTrain={onTrain}
        onDelete={onDelete}
        onSet={onSet}
        onFileAction={onFileAction}
      />
    ),
  }
];

export const getQAPairColumns = (
  t: (key: string) => string,
  convertToLocalizedTime: (time: string) => string,
  getRandomColor: () => string,
  knowledgeBasePermissions: string[],
  onDeleteSingle: (id: number) => void,
  router: RouterType,
  id: string | null,
  name: string | null,
  desc: string | null
): TableColumnsType<QAPairData> => [
  {
    title: t('knowledge.qaPairs.name'),
    dataIndex: 'name',
    key: 'name',
    render: (text: string, record: QAPairData) => (
      <a
        href="#"
        style={{ color: '#155aef' }}
        onClick={(e) => {
          e.preventDefault();
          router.push(`/opspilot/knowledge/detail/documents/qapair/result?id=${id}&name=${name}&desc=${desc}&qaPairId=${record.id}`);
        }}
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
    render: (text: string) => convertToLocalizedTime(text),
  },
  {
    title: t('knowledge.documents.createdBy'),
    key: 'created_by',
    dataIndex: 'created_by',
    render: (_: any, record: QAPairData) => (
      <div>
        <div
          className='inline-block text-center rounded-full text-white mr-2'
          style={{ width: 20, height: 20, backgroundColor: getRandomColor() }}
        >
          {record.created_by.charAt(0).toUpperCase()}
        </div>
        {record.created_by}
      </div>
    ),
  },
  {
    title: t('knowledge.documents.status'),
    key: 'status',
    dataIndex: 'status',
    render: (_: any, record: QAPairData) => {
      const statusColors: { [key: string]: string } = {
        'pending': 'processing',
        'generating': 'orange',
        'failed': 'red',
        'completed': 'green'
      };

      const color = statusColors[record.status?.toString()] || 'processing';
      const text = t(`knowledge.qaPairs.status.${record.status}`) || '--';

      return <Tag color={color}>{text}</Tag>;
    },
  },
  {
    title: t('knowledge.documents.actions'),
    key: 'action',
    render: (_: any, record: QAPairData) => (
      <PermissionWrapper
        requiredPermissions={['Delete']}
        instPermissions={knowledgeBasePermissions}>
        <Button
          type="link"
          size="small"
          onClick={() => onDeleteSingle(record.id)}
        >
          {t('common.delete')}
        </Button>
      </PermissionWrapper>
    ),
  }
];
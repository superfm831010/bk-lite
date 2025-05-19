'use client';

import React, { useState, useEffect } from 'react';
import CustomTable from '@/components/custom-table';
import styles from './page.module.scss';
import GanttChart from '../components/ganttChart/page';
import LinkModal from '../components/linkModal/page';
import type { ColumnsType } from 'antd/es/table';
import { useParams } from 'next/navigation';
import { useRouter } from 'next/navigation';
import {
  Breadcrumb,
  Descriptions,
  Tabs,
  Timeline,
  Input,
  Button,
  Switch,
  Dropdown,
  type MenuProps,
} from 'antd';
import { ArrowLeftOutlined, DownOutlined } from '@ant-design/icons';
import { useTranslation } from '@/utils/i18n';
import type { TableDataItem } from '@/app/alarm/types';

const { TabPane } = Tabs;

const mockData: TableDataItem[] = [
  {
    id: 1,
    level: 'critical',
    first_event_time: '2023-08-01 08:00',
    last_event_time: '2023-08-01 09:30',
    title: 'CPU 使用率过高',
    count: 3,
    source: 'Server A',
    status: 'new',
    duration: '1h30m',
    operator: 'Alice',
    notify_status: 'notified',
  },
  {
    id: 2,
    level: 'warning',
    first_event_time: '2023-08-01 10:00',
    last_event_time: '2023-08-01 10:20',
    title: '内存使用率临界',
    count: 1,
    source: 'Server B',
    status: 'processing',
    duration: '20m',
    operator: 'Bob',
    notify_status: 'unnotified',
  },
];

const IncidentDetail: React.FC = () => {
  const router = useRouter();
  const { t } = useTranslation();
  const { id } = useParams();
  const [linkMode, setLinkMode] = useState<'link' | 'unlink'>('link');
  const [tableData, setTableData] = useState<any[]>([]);
  const [tabLoading, setTabLoading] = useState<boolean>(false);
  const [searchText, setSearchText] = useState<string>('');
  const [tableVisible, setTableVisible] = useState<boolean>(true);
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);
  const [operateVisible, setOperateVisible] = useState(false);
  const [Pagination, setPagination] = useState<{
    current: number;
    pageSize: number;
    total: number;
  }>({
    current: 1,
    pageSize: 10,
    total: 0,
  });

  const detail = {
    alertName: `Alert #${id}`,
    createTime: '2023-08-01 12:00:00',
    source: 'Server A',
    state: 'new',
    assignee: 'Alice',
    note: '这是一个示例备注。',
  };

  const timeline = [
    { time: '2023-08-01 12:00', event: '触发告警' },
    { time: '2023-08-01 12:05', event: '认领告警' },
  ];

  const descFields = [
    { label: t('monitor.events.createTime'), value: detail.createTime },
    { label: t('monitor.events.source'), value: detail.source },
    {
      label: t('monitor.events.state'),
      value: t(`monitor.events.${detail.state}`) || detail.state,
    },
    { label: t('monitor.events.assignee'), value: detail.assignee },
    { label: t('monitor.events.note'), value: detail.note },
  ];

  const columns: ColumnsType<TableDataItem> = [
    {
      title: t('monitor.events.level'),
      dataIndex: 'level',
      key: 'level',
      width: 100,
    },
    {
      title: t('monitor.events.firstEventTime'),
      dataIndex: 'first_event_time',
      key: 'first_event_time',
      width: 160,
    },
    {
      title: t('monitor.events.lastEventTime'),
      dataIndex: 'last_event_time',
      key: 'last_event_time',
      width: 160,
    },
    {
      title: t('monitor.events.eventTitle'),
      dataIndex: 'title',
      key: 'title',
      width: 200,
    },
    {
      title: t('monitor.events.eventCount'),
      dataIndex: 'count',
      key: 'count',
      width: 100,
    },
    {
      title: t('monitor.events.source'),
      dataIndex: 'source',
      key: 'source',
      width: 120,
    },
    {
      title: t('monitor.events.state'),
      dataIndex: 'status',
      key: 'status',
      width: 100,
    },
    {
      title: t('monitor.events.duration'),
      dataIndex: 'duration',
      key: 'duration',
      width: 100,
    },
    {
      title: t('common.operator'),
      dataIndex: 'operator',
      key: 'operator',
      width: 100,
    },
    {
      title: t('monitor.events.notificationStatus'),
      dataIndex: 'notify_status',
      key: 'notify_status',
      width: 140,
    },
    {
      title: t('common.action'),
      key: 'action',
      dataIndex: 'action',
      width: 120,
      fixed: 'right',
      render: () => (
        <Button
          type="link"
          onClick={() => {
            /* TODO: action */
          }}
        >
          {t('common.detail')}
        </Button>
      ),
    },
  ];

  const fetchList = async (
    page = Pagination.current,
    pageSize = Pagination.pageSize
  ) => {
    setTabLoading(true);
    try {
      const res = {
        items: mockData,
        total: 0,
      };
      setTableData(res.items || []);
      setPagination({ current: page, pageSize, total: res.total || 0 });
    } finally {
      setTabLoading(false);
    }
  };

  useEffect(() => {
    fetchList(1, Pagination.pageSize);
  }, [searchText]);

  const onTabTableChange = (pag: any) => {
    setPagination({
      current: pag.current,
      pageSize: pag.pageSize,
      total: pag.total,
    });
    fetchList(pag.current, pag.pageSize);
  };

  const linkMenuItems: MenuProps['items'] = [
    { key: 'link', label: t('common.linkAlert') },
    { key: 'unlink', label: t('common.unlinkAlert') },
  ];

  const onLinkMenuClick = ({ key }: { key: string }) => {
    setLinkMode(key as 'link' | 'unlink');  
    setOperateVisible(true);
  };

  return (
    <div className={styles.detailContainer}>
      <Breadcrumb className={styles.breadcrumb}>
        <ArrowLeftOutlined
          onClick={() => router.back()}
          className={styles.backIcon}
        />
        <Breadcrumb.Item>{detail.alertName}</Breadcrumb.Item>
      </Breadcrumb>

      <Descriptions
        column={{ xs: 1, sm: 2, md: 3, lg: 3, xl: 4, xxl: 4 }}
        size="middle"
        className={styles.descriptions}
        labelStyle={{ width: '80px' }}
      >
        {descFields.map(({ label, value }, idx) => (
          <Descriptions.Item label={label} key={idx}>
            <div className={styles.fixedContent}>{value}</div>
          </Descriptions.Item>
        ))}
      </Descriptions>

      <div className={styles.tabsWrapper}>
        <Tabs defaultActiveKey="alert">
          <TabPane tab={t('monitor.events.alert')} key="alert">
            <div className={styles.tabContent}>
              <div className={styles.filterRow}>
                <div className={styles.switchWrapper}>
                  <Input
                    allowClear
                    className="w-[300px] mr-[20px]"
                    placeholder={t('common.searchPlaceHolder')}
                    value={searchText}
                    onChange={(e) => setSearchText(e.target.value)}
                    onPressEnter={() => fetchList(1, Pagination.pageSize)}
                  />
                  <Switch
                    checked={tableVisible}
                    onChange={setTableVisible}
                    className={styles.changeSwitch}
                  />
                  <span className={styles.switchLabel}>
                    {t('common.changeView')}
                  </span>
                </div>
                <Dropdown
                  menu={{ items: linkMenuItems, onClick: onLinkMenuClick }}
                  placement="bottomRight"
                >
                  <Button type="primary">
                    {t('monitor.events.batchOperations')} <DownOutlined />
                  </Button>
                </Dropdown>
              </div>
              {tableVisible ? (
                <CustomTable
                  rowKey="id"
                  columns={columns}
                  dataSource={tableData}
                  loading={tabLoading}
                  pagination={Pagination}
                  scroll={{
                    y: 'calc(100vh - 500px)',
                    x: 'calc(100vw - 320px)',
                  }}
                  onChange={onTabTableChange}
                  rowSelection={{
                    selectedRowKeys,
                    onChange: (keys: React.Key[]) => setSelectedRowKeys(keys),
                  }}
                />
              ) : (
                <GanttChart />
              )}
            </div>
          </TabPane>
          <TabPane tab={t('monitor.events.timeline')} key="timeline">
            <Timeline className={styles.timelineContent}>
              {timeline.map((item, idx) => (
                <Timeline.Item key={idx}>
                  <span className="font-medium">{item.time}</span> -{' '}
                  {item.event}
                </Timeline.Item>
              ))}
            </Timeline>
          </TabPane>
        </Tabs>
      </div>
      <LinkModal
        mode={linkMode}
        visible={operateVisible}
        onClose={() => setOperateVisible(false)}
        data={tableData}
        onLink={() => {
          setOperateVisible(false);
        }}
      />
    </div>
  );
};

export default IncidentDetail;

'use client';

import React, { useState, useEffect } from 'react';
import styles from './page.module.scss';
import AlarmTable from '@/app/alarm/(pages)/alarms/components/alarmTable';
import GanttChart from '../components/ganttChart/page';
import LinkModal from '../components/linkModal/page';
import EllipsisWithTooltip from '@/components/ellipsis-with-tooltip';
import type { TableDataItem } from '@/app/alarm/types/types';
import { UserItem } from '@/app/alarm/types/types';
import { useCommon } from '@/app/alarm/context/common';
import { useTranslation } from '@/utils/i18n';
import { useSearchParams } from 'next/navigation';
import { useRouter } from 'next/navigation';
import {
  ArrowLeftOutlined,
  DownOutlined,
  EditOutlined,
  CheckOutlined,
  CloseOutlined,
  AlertOutlined,
  BarsOutlined,
  AppstoreOutlined,
} from '@ant-design/icons';
import {
  Breadcrumb,
  Descriptions,
  Tabs,
  Timeline,
  Input,
  Button,
  Segmented,
  Dropdown,
  Select,
  Tag,
  type MenuProps,
} from 'antd';

const { TabPane } = Tabs;

const mockData: TableDataItem[] = [
  {
    id: 1,
    level: 'fatal',
    first_event_time: '2023-08-01 08:00',
    last_event_time: '2023-08-01 09:30',
    title: 'CPU 使用率过高',
    count: 3,
    source: 'Server A',
    status: 'abnormal',
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
    status: 'autoexecute_executing',
    duration: '20m',
    operator: 'Bob',
    notify_status: 'unnotified',
  },
];

const IncidentDetail: React.FC = () => {
  const { levelList, levelMap, userList } = useCommon();
  const router = useRouter();
  const { t } = useTranslation();
  const searchParams = useSearchParams();
  const incidentName = searchParams.get('name') || '';
  const [tableData, setTableData] = useState<any[]>([]);
  const [tabLoading, setTabLoading] = useState<boolean>(false);
  const [searchText, setSearchText] = useState<string>('');
  const [viewType, setViewType] = useState<'table' | 'gantt'>('table');
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);
  const [operateVisible, setOperateVisible] = useState(false);
  const [editingAssignee, setEditingAssignee] = useState(false);
  const [selectedAssignees, setSelectedAssignees] = useState<string[]>([]);
  const [preAssignees, setPreAssignees] = useState<string[]>([]);
  const [assigneeDisplay, setAssigneeDisplay] = useState<string>('');
  const [pagination, setPagination] = useState<{
    current: number;
    pageSize: number;
    total: number;
  }>({
    current: 1,
    pageSize: 10,
    total: 0,
  });


  const detail = {
    level: 'fatal',
    alertName: `告警 #${incidentName}`,
    createTime: '2023-08-01 12:00:00',
    source: 'Server A',
    state: 'new',
    assignee: '',
    note: '这是一个示例备注。',
  };

  const timeline = [
    { time: '2023-08-01 12:00', event: '触发告警' },
    { time: '2023-08-01 12:05', event: '认领告警' },
  ];

  const descFields = [
    { label: t('alarms.createTime'), value: detail.createTime },
    { label: t('alarms.source'), value: detail.source },
    {
      label: t('alarms.state'),
      value: t(`alarms.${detail.state}`) || detail.state,
    },
    { label: t('alarms.assignee'), value: detail.assignee },
    { label: t('alarms.note'), value: detail.note },
  ];

  const fetchList = async (
    page = pagination.current,
    pageSize = pagination.pageSize
  ) => {
    setTabLoading(true);
    try {
      const res = {
        items: mockData,
        total: mockData.length,
      };
      setTableData(res.items || []);
      setPagination({ current: page, pageSize, total: res.total || 0 });
    } finally {
      setTabLoading(false);
    }
  };

  const userOptions = userList.map((u: UserItem) => ({
    label: `${u.display_name} (${u.username})`,
    value: u.id,
  }));

  useEffect(() => {
    fetchList(1, pagination.pageSize);
  }, []);

  useEffect(() => {
    if (detail.assignee) {
      setSelectedAssignees(detail.assignee.split(','));
      setPreAssignees(detail.assignee.split(','));
    }
  }, [detail.assignee]);

  const confirmAssignee = () => {
    const nameStr = selectedAssignees.map((id) => {
      const user = userList.find((u: UserItem) => u.id === id);
      return user ? `${user.display_name} (${user.username})` : '';
    });
    setPreAssignees(selectedAssignees);
    setAssigneeDisplay(nameStr.join(', '));
    setEditingAssignee(false);
  };
  const cancelAssignee = () => {
    setSelectedAssignees(preAssignees);
    setEditingAssignee(false);
  };

  const onTabTableChange = (pag: any) => {
    setPagination({
      current: pag.current,
      pageSize: pag.pageSize,
      total: pag.total,
    });
    fetchList(pag.current, pag.pageSize);
  };

  const handleUnlink = () => {
    console.log('Unlinking records:', selectedRowKeys);
  };

  const handleLink = (record?: TableDataItem) => {
    console.log('Linking record:', record);
    setOperateVisible(true);
  };

  const statusMenuItems: MenuProps['items'] = [
    { key: 'acknowledge', label: `${t('alarms.acknowledge')}` },
    { key: 'close', label: `${t('common.close')}` },
    { key: 'open', label: `${t('common.open')}` },
  ];

  const renderDescItems = () =>
    descFields.map(({ label, value }, idx) => {
      if (label === t('alarms.state')) {
        return (
          <Descriptions.Item label={label} key={idx}>
            <div className={styles.descContent}>
              {value}
              <Dropdown
                menu={{ items: statusMenuItems }}
                placement="bottomRight"
              >
                <Button size="small" type="primary" style={{ marginLeft: 12 }}>
                  {t('common.action')}
                  <DownOutlined />
                </Button>
              </Dropdown>
            </div>
          </Descriptions.Item>
        );
      }
      if (label === t('alarms.assignee')) {
        return (
          <Descriptions.Item label={label} key={idx}>
            <div
              className={
                styles.descContent + ' flex-1 flex items-center overflow-hidden'
              }
            >
              {editingAssignee ? (
                <>
                  <Select
                    allowClear
                    showSearch
                    options={userOptions}
                    value={selectedAssignees}
                    maxTagCount={1}
                    mode="multiple"
                    className="flex-1 mr-[10px]"
                    filterOption={(input, option) =>
                      (option?.label as string)
                        ?.toLowerCase()
                        .includes(input.toLowerCase())
                    }
                    onChange={setSelectedAssignees}
                  />
                  <Button
                    size="small"
                    type="link"
                    icon={<CheckOutlined />}
                    onClick={confirmAssignee}
                  />
                  <Button
                    size="small"
                    type="link"
                    icon={<CloseOutlined />}
                    onClick={cancelAssignee}
                  />
                </>
              ) : (
                <>
                  <EllipsisWithTooltip
                    className="whitespace-nowrap overflow-hidden text-ellipsis mr-[10px]"
                    text={assigneeDisplay || '--'}
                  ></EllipsisWithTooltip>
                  <Button
                    size="small"
                    type="link"
                    icon={<EditOutlined />}
                    className="mr-[10px]"
                    onClick={() => setEditingAssignee(true)}
                  />
                </>
              )}
            </div>
          </Descriptions.Item>
        );
      }
      return (
        <Descriptions.Item label={label} key={idx}>
          <div className={styles.descContent}>{value}</div>
        </Descriptions.Item>
      );
    });

  return (
    <div className={styles.detailContainer}>
      <Breadcrumb className={styles.breadcrumb}>
        <ArrowLeftOutlined
          onClick={() => router.back()}
          className={styles.backIcon}
        />
        <Breadcrumb.Item>
          <span className="ml-[10px] mr-[10px]">{detail.alertName}</span>
          <Tag
            icon={<AlertOutlined />}
            color={levelMap[detail.level] as string}
          >
            {levelList.find((item) => item.value === detail.level)?.label ||
              detail.level}
          </Tag>
        </Breadcrumb.Item>
      </Breadcrumb>

      <div className={styles.detailContent}>
        <Descriptions
          column={{ xs: 1, sm: 2, md: 3, lg: 3, xl: 4, xxl: 4 }}
          size="default"
          className={styles.descriptions}
        >
          {renderDescItems()}
        </Descriptions>
        <div className={styles.tabsWrapper}>
          <Tabs defaultActiveKey="alert">
            <TabPane tab={t('alarms.alert')} key="alert">
              <div className={styles.tabContent}>
                <div className={styles.filterRow}>
                  <div className={styles.switchWrapper}>
                    <Input
                      allowClear
                      className="w-[300px] mr-[20px]"
                      placeholder={t('common.searchPlaceHolder')}
                      value={searchText}
                      onChange={(e) => setSearchText(e.target.value)}
                      onPressEnter={() => fetchList(1, pagination.pageSize)}
                    />
                    <Segmented
                      defaultValue="table"
                      options={[
                        {
                          value: 'table',
                          label: t('incidents.table'),
                          icon: <AppstoreOutlined />,
                        },
                        {
                          value: 'gantt',
                          label: t('incidents.gantt'),
                          icon: <BarsOutlined />,
                        },
                      ]}
                      onChange={setViewType}
                    />
                  </div>
                  <div>
                    <Button
                      type="primary"
                      className="mr-[12px]"
                      onClick={() => handleLink()}
                    >
                      {t('common.linkAlert')}
                    </Button>
                    <Button type="primary" onClick={() => handleUnlink()}>
                      {t('common.unlinkAlert')}
                    </Button>
                  </div>
                </div>
                {viewType === 'table' ? (
                  <AlarmTable
                    dataSource={tableData}
                    pagination={pagination}
                    loading={tabLoading}
                    tableScrollY="calc(100vh - 500px)"
                    selectedRowKeys={selectedRowKeys}
                    onChange={onTabTableChange}
                    onSelectionChange={setSelectedRowKeys}
                    onRefresh={() => fetchList(1, pagination.pageSize)}
                    extraActions={() => (
                      <Button
                        type="link"
                        className="ml-[8px]"
                        onClick={() => handleUnlink()}
                      >
                        {t('common.unlinkAlert')}
                      </Button>
                    )}
                  />
                ) : (
                  <GanttChart />
                )}
              </div>
            </TabPane>
            <TabPane tab={t('alarms.changes')} key="timeline">
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
      </div>
      <LinkModal
        visible={operateVisible}
        onClose={() => setOperateVisible(false)}
        onLink={() => {
          setOperateVisible(false);
        }}
      />
    </div>
  );
};

export default IncidentDetail;

import React from 'react';
import { Descriptions, Tag } from 'antd';
import { AlertOutlined } from '@ant-design/icons';
import { LEVEL_MAP, useLevelList } from '@/app/alarm/constants/monitor';

const BaseInfo: React.FC = () => {
  const detail = {
    level: 'critical' as keyof typeof LEVEL_MAP,
    alertName: 'CPU 使用率过高',
    createTime: '2023-08-01 12:00:00',
    source: 'Server A',
    state: 'new',
    assignee: 'Alice',
    note: '这是一个示例备注。',
  };
  const LEVEL_LIST = useLevelList();

  return (
    <Descriptions bordered size="small" column={2}>
      <Descriptions.Item label="告警等级">
        <Tag icon={<AlertOutlined />} color={LEVEL_MAP[detail.level] as string}>
          {LEVEL_LIST.find((item) => item.value === detail.level)?.label ||
            detail.level}
        </Tag>
      </Descriptions.Item>
      <Descriptions.Item label="告警名称">
        {detail.alertName}
      </Descriptions.Item>
      <Descriptions.Item label="创建时间">
        {detail.createTime}
      </Descriptions.Item>
      <Descriptions.Item label="来源">
        {detail.source}
      </Descriptions.Item>
      <Descriptions.Item label="状态">
        {detail.state}
      </Descriptions.Item>
      <Descriptions.Item label="处理人">
        {detail.assignee}
      </Descriptions.Item>
      <Descriptions.Item label="备注" span={2}>
        {detail.note}
      </Descriptions.Item>
    </Descriptions>
  );
};

export default BaseInfo;

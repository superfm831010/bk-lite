import React from 'react';
import { Descriptions } from 'antd';
import { useTranslation } from '@/utils/i18n';
import { AlarmTableDataItem } from '@/app/alarm/types/alarms';
import {
  useNotifiedStateMap
} from '@/app/alarm/constants/alarm';

const BaseInfo: React.FC<{ detail: AlarmTableDataItem }> = ({ detail }) => {
  const { t } = useTranslation();
  const NOTIFIED_STATE: any = useNotifiedStateMap();
  const descriptionItems = [
    {
      key: 'operator',
      label: t('common.operator'),
      value: detail.operator_user,
    },
    {
      key: 'source',
      label: t('alarms.source'),
      value: detail.source_names,
    },
    {
      key: 'notificationStatus',
      label: t('alarms.notificationStatus'),
      value: NOTIFIED_STATE[detail.notification_status] || '--',
    },
    {
      key: 'objectType',
      label: t('alarms.objectType'),
      value: detail.resource_type,
    },
    {
      key: 'object',
      label: t('alarms.object'),
      value: detail.resource_name,
    },
  ];
  return (
    <Descriptions
      bordered
      size="small"
      column={1}
      style={{ tableLayout: 'fixed' }}
      labelStyle={{
        width: '120px',
        whiteSpace: 'nowrap',
        overflow: 'hidden',
        textOverflow: 'ellipsis',
      }}
    >
      <Descriptions.Item
        label={t('alarms.content')}
        styles={{
          content: {
            maxHeight: '100px',
            overflowY: 'auto',
            wordBreak: 'break-word',
          },
        }}
      >
        {detail.content || '--'}
      </Descriptions.Item>
      {descriptionItems.map((item) => (
        <Descriptions.Item key={item.key} label={item.label}>
          {item.value || '--'}
        </Descriptions.Item>
      ))}
    </Descriptions>
  );
};

export default BaseInfo;

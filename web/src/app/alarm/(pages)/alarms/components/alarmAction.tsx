'use client';

import React, { useState } from 'react';
import AlarmAssignModal from './assignModal';
import { Button, Dropdown, Menu, Modal, message } from 'antd';
import { useTranslation } from '@/utils/i18n';
import { DownOutlined } from '@ant-design/icons';
import { AlarmActionProps, ActionType } from '@/app/alarm/types/alarms';
import { useAlarmApi } from '@/app/alarm/api/alarms';
import { useSession } from 'next-auth/react';

const AlarmAction: React.FC<AlarmActionProps> = ({
  rowData,
  btnSize = 'middle',
  displayMode = 'inline',
  showAll = false,
  onAction,
}) => {
  const { t } = useTranslation();
  const { data: session } = useSession();
  const { alertActionOperate } = useAlarmApi();
  const [assignVisible, setAssignVisible] = useState(false);
  const [actionType, setActionType] = useState<ActionType>('assign');
  const alertIds = rowData.map((item) => item.alert_id);
  const username = session?.user?.username;

  const isMine = () =>
    rowData.every((item) =>
      item?.operator_user
        ?.split(',')
        .map((name: string) => name.trim())
        .includes(username)
    );

  const allTypes: ActionType[] = [
    'assign',
    'acknowledge',
    'reassign',
    'close',
    'open',
  ];

  const statusActionMap: Record<string, ActionType[]> = {
    unassigned: ['assign'],
    pending: ['acknowledge'],
    processing: ['reassign', 'close'],
    closed: [],
  };

  const validStatusMap: Record<ActionType, string[]> = {
    assign: ['unassigned'],
    acknowledge: ['pending'],
    reassign: ['processing'],
    close: ['processing'],
    open: ['closed'],
  };

  const availableTypes = showAll
    ? allTypes
    : rowData[0]?.status
      ? statusActionMap[rowData[0].status]
      : [];

  const handleOperate = (type: ActionType) => {
    if (!['acknowledge', 'close'].includes(type)) {
      setActionType(type);
      setAssignVisible(true);
      return;
    }
    Modal.confirm({
      title: `${t(`alarms.${type}`)}${t('alarms.alert')}`,
      content: `${t('common.confirm')}${t(`alarms.${type}`)}${t('alarms.alert')} ？`,
      okText: t('confirm'),
      cancelText: t('cancel'),
      centered: true,
      onOk: async () => {
        try {
          const data = await alertActionOperate(type, {
            alert_id: alertIds,
            assignee: [],
          });
          if (Object.values(data).some((res: any) => !res.result)) {
            message.error(
              `${t(`alarms.${type}`)}${t(`alarms.alert`)}${t('common.partialFailure')}`
            );
          } else {
            message.success(t(`alarms.${type}`) + t('common.success'));
            onAction();
          }
        } catch (err) {
          console.error(err);
        }
      },
    });
  };

  const actionButtons = (
    <>
      {availableTypes.map((type) => {
        const allStatusValid = rowData.every((item) =>
          validStatusMap[type].includes(item.status)
        );
        const needMine = ['acknowledge', 'reassign'].includes(type);
        const disabled =
          !rowData.length || !allStatusValid || (needMine && !isMine());
        return (
          <Button
            key={type}
            size={btnSize}
            type="link"
            className="mr10"
            disabled={disabled}
            onClick={() => handleOperate(type)}
          >
            {t(`alarms.${type}`)}
          </Button>
        );
      })}
    </>
  );

  const flattenChildren = (nodes: React.ReactNode): React.ReactElement[] => {
    const items: React.ReactElement[] = [];
    React.Children.forEach(nodes, (child) => {
      if (React.isValidElement(child)) {
        if (child.type === React.Fragment) {
          items.push(...flattenChildren(child.props.children));
        } else {
          items.push(child);
        }
      }
    });
    return items;
  };

  const items = flattenChildren(actionButtons);
  const menuItems = items.map((child, idx) => {
    const isValid = React.isValidElement(child);
    return {
      key: idx.toString(),
      label: (
        <div className="flex flex-col">
          {(() => {
            if (isValid) {
              return React.cloneElement(child as React.ReactElement, {
                type: 'text',
                size: 'small',
              });
            }
            return child;
          })()}
        </div>
      ),
    };
  });

  const dropdown = menuItems.length ? (
    <Dropdown overlay={<Menu items={menuItems} />} trigger={['click']}>
      <Button size={btnSize} type="primary">
        {t('common.actions')}
        <DownOutlined />
      </Button>
    </Dropdown>
  ) : null;

  const inline = <div className="gap-2 flex items-center">{actionButtons}</div>;

  return (
    <>
      {displayMode === 'dropdown' && dropdown ? dropdown : inline}
      <AlarmAssignModal
        alertIds={alertIds}
        visible={assignVisible}
        actionType={actionType}
        onCancel={() => setAssignVisible(false)}
        onSuccess={() => {
          setAssignVisible(false);
          onAction();
        }}
      />
    </>
  );
};

export default AlarmAction;

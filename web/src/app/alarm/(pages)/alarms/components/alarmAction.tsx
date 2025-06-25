'use client';

import React, { useState } from 'react';
import AlarmAssignModal from './assignModal';
import PermissionWrapper from '@/components/permission';
import { Button, Dropdown, Menu, Modal, message } from 'antd';
import { useTranslation } from '@/utils/i18n';
import { DownOutlined } from '@ant-design/icons';
import { AlarmActionProps, ActionType } from '@/app/alarm/types/alarms';
import { useAlarmApi } from '@/app/alarm/api/alarms';
import { useIncidentsApi } from '@/app/alarm/api/incidents';
import { useSession } from 'next-auth/react';

const AlarmAction: React.FC<AlarmActionProps> = ({
  rowData,
  btnSize = 'middle',
  displayMode = 'inline',
  showAll = false,
  from = 'alarm',
  onAction,
}) => {
  const idKeyMap = {
    alarm: 'alert_id',
    incident: 'incident_id',
  };
  const { t } = useTranslation();
  const { data: session } = useSession();
  const { alertActionOperate } = useAlarmApi();
  const { incidentActionOperate } = useIncidentsApi();
  const [assignVisible, setAssignVisible] = useState(false);
  const [actionType, setActionType] = useState<ActionType>('assign');
  const idList = rowData.map((item) => item[idKeyMap[from]]);
  const username = session?.user?.username;

  const isMine = () =>
    rowData.every((item) =>
      item?.operator_user
        ?.split(',')
        .map((name: string) => name.trim())
        .includes(username)
    );

  const apiNameMap = {
    alarm: alertActionOperate,
    incident: incidentActionOperate,
  };

  const allTypes: ActionType[] =
    from === 'alarm'
      ? ['assign', 'acknowledge', 'reassign', 'close']
      : ['acknowledge', 'close', 'reopen'];

  const statusActionMap: Record<string, ActionType[]> =
    from === 'alarm'
      ? {
        unassigned: ['assign'],
        pending: ['acknowledge'],
        processing: ['reassign', 'close'],
        closed: [],
      }
      : {
        pending: ['acknowledge'],
        processing: ['close'],
        closed: ['reopen'],
      };

  const validStatusMap: Record<string, string[]> =
    from === 'alarm'
      ? {
        assign: ['unassigned'],
        acknowledge: ['pending'],
        reassign: ['processing'],
        close: ['processing'],
      }
      : {
        acknowledge: ['pending'],
        close: ['processing'],
        reopen: ['closed'],
      };

  const availableTypes = showAll
    ? allTypes
    : rowData[0]?.status
      ? statusActionMap[rowData[0].status]
      : [];

  const handleOperate = (type: ActionType) => {
    if (!['acknowledge', 'close', 'reopen'].includes(type)) {
      setActionType(type);
      setAssignVisible(true);
      return;
    }
    const fromLabel = `${from === 'alarm' ? t('alarms.alert') : t('alarms.incident')}`;
    Modal.confirm({
      title: `${t(`alarms.${type}`)}${fromLabel}`,
      content: `${t('common.confirm')}${t(`alarms.${type}`)}${fromLabel}？`,
      okText: t('confirm'),
      cancelText: t('cancel'),
      centered: true,
      onOk: async () => {
        try {
          const data = await apiNameMap[from](type, {
            [idKeyMap[from]]: idList,
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
          validStatusMap[type]?.includes(item.status)
        );
        const needMine =
          from === 'alarm' && ['acknowledge', 'reassign'].includes(type);
        const disabled =
          !rowData.length || !allStatusValid || (needMine && !isMine());
        return (
          <PermissionWrapper requiredPermissions={['Edit']} key={type}>
            <Button
              size={btnSize}
              type="link"
              className="mr10"
              disabled={disabled}
              onClick={() => handleOperate(type)}
            >
              {t(`alarms.${type}`)}
            </Button>
          </PermissionWrapper>
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
    <PermissionWrapper requiredPermissions={['Edit']}>
      <Dropdown overlay={<Menu items={menuItems} />} trigger={['click']}>
        <Button size={btnSize} type="primary">
          {t('common.actions')}
          <DownOutlined />
        </Button>
      </Dropdown>
    </PermissionWrapper>
  ) : null;

  const inline = <div className="gap-2 flex items-center">{actionButtons}</div>;

  return (
    <>
      {displayMode === 'dropdown' && dropdown ? dropdown : inline}
      <AlarmAssignModal
        alertIds={idList}
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

'use client';

import React, { useState } from 'react';
import type { TableDataItem, UserItem } from '@/app/alarm/types';
import { Button, Popconfirm, message, Dropdown, Menu } from 'antd';
import { useTranslation } from '@/utils/i18n';
import { DownOutlined } from '@ant-design/icons';

interface AlarmActionProps {
  row: TableDataItem;
  user: UserItem;
  menuId: string | number;
  fetchAlarmExecute: (alarmId: string | number) => Promise<any>;
  checkPermission: (opt: { id: string | number; type: string }) => boolean;
  onSuccess: (type: string, row: TableDataItem) => void;
  displayMode?: 'inline' | 'dropdown';
}

const AlarmAction: React.FC<AlarmActionProps> = ({
  row,
  user,
  menuId,
  fetchAlarmExecute,
  checkPermission,
  onSuccess,
  displayMode = 'inline',
}) => {
  const { t } = useTranslation();
  const [templateName, setTemplateName] = useState<string>('');
  const [visiblePopConfirm, setVisiblePopConfirm] = useState<boolean>(false);

  const isMine = () => {
    const conductor = row.conductor_list || [];
    return conductor.includes(user?.username);
  };

  const handleGetAlarmExecute = async () => {
    if (!checkPermission({ id: menuId, type: 'operateAuth' })) return;
    const res = await fetchAlarmExecute(row.alarm_id);
    if (res.result) {
      setTemplateName(res.data.name || '--');
      setVisiblePopConfirm(true);
    }
  };

  const handleOperate = (type: string) => {
    if (!checkPermission({ id: menuId, type: 'operateAuth' })) return;
    if (['assign', 'close', 'dispatch', 'toOrder'].includes(type)) {
      onSuccess(type, row);
      return;
    }
    message.info(`${t('alarms.confirmOperate')} ${t(`alarms.${type}`)}`);
    message.success(`${t('alarms.successOperate')} ${t(`alarms.${type}`)}`);
    onSuccess(type, row);
  };

  const dispatchStatus = [
    'dispatched',
    'pending_execute',
    'autoexecuting_failure',
    'executing',
  ];

  const actionButtons = (
    <div className="gap-2 flex items-center">
      {['abnormal', 'dispatched'].includes(row.status) && (
        <>
          {row.status === 'abnormal' && (
            <>
              <Button
                type="link"
                className="mr10"
                onClick={() => handleOperate('claim')}
              >
                {t('alarms.claim')}
              </Button>
              <Button
                type="link"
                className="mr10"
                onClick={() => handleOperate('dispatch')}
              >
                {t('alarms.dispatch')}
              </Button>
            </>
          )}
          <Button
            type="link"
            className="mr10"
            onClick={() => handleOperate('toOrder')}
          >
            {t('alarms.toOrder')}
          </Button>
          {row.status === 'abnormal' && (
            <Button
              type="link"
              className="mr10"
              onClick={() => handleOperate('close')}
            >
              {t('common.close')}
            </Button>
          )}
        </>
      )}

      {isMine() && (
        <>
          {row.status === 'dispatched' && (
            <Button
              type="link"
              className="mr10"
              onClick={() => handleOperate('response')}
            >
              {t('alarms.response')}
            </Button>
          )}
          {row.status === 'pending_execute' && (
            <>
              <Popconfirm
                title={
                  <>
                    <div className="mb10">
                      {t('alarms.autoExecuteProcess')}: {templateName || '--'}
                    </div>
                  </>
                }
                open={visiblePopConfirm}
                onConfirm={() => handleOperate('pass')}
                onCancel={() => handleOperate('refuse')}
                okText={t('common.confirm')}
                cancelText={t('common.cancel')}
              >
                <Button
                  type="link"
                  className="mr10"
                  onClick={() => handleGetAlarmExecute()}
                >
                  {t('alarms.pass')}
                </Button>
              </Popconfirm>
              <Button
                type="link"
                className="mr10"
                onClick={() => handleOperate('assign')}
              >
                {t('alarms.assign')}
              </Button>
              <Button
                type="link"
                className="mr10"
                onClick={() => handleOperate('close')}
              >
                {t('common.close')}
              </Button>
            </>
          )}
          {['autoorder_executing', 'autoexecute_executing'].includes(
            row.status
          ) && (
            <Button
              type="link"
              className="mr10"
              onClick={() => handleOperate('close')}
            >
              {t('common.close')}
            </Button>
          )}
          {['dispatched', 'executing', 'autoexecuting_failure'].includes(
            row.status
          ) && (
            <>
              <Button
                type="link"
                className="mr10"
                onClick={() => handleOperate('assign')}
              >
                {t('alarms.assign')}
              </Button>
              {row.status === 'executing' && (
                <Button
                  type="link"
                  className="mr10"
                  onClick={() => handleOperate('toOrder')}
                >
                  {t('alarms.toOrder')}
                </Button>
              )}
              <Button
                type="link"
                className="mr10"
                onClick={() => handleOperate('close')}
              >
                {t('common.close')}
              </Button>
            </>
          )}
        </>
      )}

      {!isMine() && dispatchStatus.includes(row.status) && (
        <Button
          type="link"
          className="mr10"
          onClick={() => handleOperate('dispatch')}
        >
          {t('alarms.dispatch')}
        </Button>
      )}
    </div>
  );

  if (displayMode === 'dropdown') {
    const menuItems = React.Children.toArray(actionButtons.props.children).map(
      (child, idx) => ({ key: idx.toString(), label: child })
    );
    return (
      <Dropdown overlay={<Menu items={menuItems} />} trigger={['click']}>
        <Button>
          {t('common.actions')}
          <DownOutlined />
        </Button>
      </Dropdown>
    );
  }

  return actionButtons;
};

export default AlarmAction;

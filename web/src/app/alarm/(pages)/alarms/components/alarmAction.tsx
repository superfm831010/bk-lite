'use client';

import React, { useState } from 'react';
import { Button, Popconfirm, message, Dropdown, Menu } from 'antd';
import { useTranslation } from '@/utils/i18n';
import { DownOutlined } from '@ant-design/icons';
import { AlarmActionProps } from '@/app/alarm/types/alarms';

const AlarmAction: React.FC<AlarmActionProps> = ({
  row,
  user,
  menuId,
  displayMode = 'inline',
  fetchAlarmExecute,
  checkPermission,
  onSuccess,
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
    <>
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
    </>
  );

  const flattenChildren = (nodes: React.ReactNode): React.ReactElement[] => {
    const items: React.ReactElement[] = [];
    React.Children.forEach(nodes, child => {
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

  if (displayMode === 'dropdown') {
    const items = flattenChildren(actionButtons);
    const menuItems = items.map((child, idx) => ({
      key: idx.toString(),
      label: (
        <div className="flex flex-col">
          {React.isValidElement(child)
            ? React.cloneElement(child as React.ReactElement, { type: 'text', size: 'small' })
            : child}
        </div>
      ),
    }));
    return (
      <Dropdown overlay={<Menu items={menuItems} />} trigger={['click']}>
        <Button type="primary">
          {t('common.actions')}
          <DownOutlined />
        </Button>
      </Dropdown>
    );
  }
  return <div className="gap-2 flex items-center">{actionButtons}</div>;
};

export default AlarmAction;

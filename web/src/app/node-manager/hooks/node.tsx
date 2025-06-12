import { useMemo } from 'react';
import { useTranslation } from '@/utils/i18n';
import { Button, Popconfirm } from 'antd';
import type { TableColumnsType } from 'antd';
import { TableDataItem } from '@/app/node-manager/types';
import { useUserInfoContext } from '@/context/userInfo';
import Permission from '@/components/permission';
import EllipsisWithTooltip from '@/components/ellipsis-with-tooltip';
interface HookParams {
  checkConfig: (row: TableDataItem) => void;
  deleteNode: (row: TableDataItem) => void;
}

export const useColumns = ({
  checkConfig,
  deleteNode,
}: HookParams): TableColumnsType<TableDataItem> => {
  const { showGroupNames } = useGroupNames();
  const { t } = useTranslation();

  const columns = useMemo(
    (): TableColumnsType<TableDataItem> => [
      {
        title: t('node-manager.cloudregion.node.ip'),
        dataIndex: 'ip',
        key: 'ip',
        width: 120,
      },
      {
        title: t('common.name'),
        dataIndex: 'name',
        key: 'name',
        width: 120,
      },
      {
        title: t('node-manager.cloudregion.node.group'),
        dataIndex: 'organization',
        key: 'organization',
        width: 120,
        render: (_, { organization }) => (
          <EllipsisWithTooltip
            className="w-full overflow-hidden text-ellipsis whitespace-nowrap"
            text={showGroupNames(organization)}
          />
        ),
      },
      {
        title: t('common.actions'),
        key: 'action',
        dataIndex: 'action',
        width: 200,
        fixed: 'right',
        render: (key, item) => (
          <>
            <Permission requiredPermissions={['View']}>
              <Button type="link" onClick={() => checkConfig(item)}>
                {t('node-manager.cloudregion.node.checkConfig')}
              </Button>
            </Permission>
            <Permission requiredPermissions={['Delete']}>
              <Popconfirm
                className="ml-[10px]"
                title={t(`common.prompt`)}
                description={t(`node-manager.cloudregion.node.deleteNodeTips`)}
                okText={t('common.confirm')}
                cancelText={t('common.cancel')}
                onConfirm={() => {
                  deleteNode(item);
                }}
              >
                <Button type="link" disabled={item.active}>
                  {t('common.delete')}
                </Button>
              </Popconfirm>
            </Permission>
          </>
        ),
      },
    ],
    [checkConfig, deleteNode, t]
  );
  return columns;
};

export const useGroupNames = () => {
  const commonContext = useUserInfoContext();
  const showGroupNames = (ids: string[]) => {
    if (!ids?.length) return '--';
    const groups = commonContext?.groups || [];
    const groupNames = ids.map(
      (item) => groups.find((group) => Number(group.id) === Number(item))?.name
    );
    return groupNames.filter((item) => !!item).join(',') || '--';
  };
  return {
    showGroupNames,
  };
};

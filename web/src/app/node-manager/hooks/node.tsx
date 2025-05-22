import { useMemo } from 'react';
import { useTranslation } from '@/utils/i18n';
// import { Tag, Tooltip, Button } from 'antd';
import { Button } from 'antd';
import type { TableColumnsType } from 'antd';
import { TableDataItem } from '@/app/node-manager/types/index';
import { useUserInfoContext } from '@/context/userInfo';
import Permission from '@/components/permission';

interface HookParams {
  checkConfig: (row: TableDataItem) => void;
}

export const useColumns = ({
  checkConfig,
}: HookParams): TableColumnsType<TableDataItem> => {
  const { t } = useTranslation();

  const columns = useMemo(
    (): TableColumnsType<TableDataItem> => [
      {
        title: t('node-manager.cloudregion.node.ip'),
        dataIndex: 'ip',
        key: 'ip',
        width: 120
      },
      {
        title: t('common.name'),
        dataIndex: 'name',
        key: 'name',
        width: 120
      },
      // {
      //   title: 'Sidecar',
      //   dataIndex: 'active',
      //   width: 100,
      //   render: (value: string, item) => {
      //     return (
      //       <Tooltip title={`${item.status?.message}`}>
      //         <Tag bordered={false} color={value ? 'success' : 'warning'}>
      //           {t(
      //             `node-manager.cloudregion.node.${value ? 'active' : 'inactive'
      //             }`
      //           )}
      //         </Tag>
      //       </Tooltip>
      //     );
      //   },
      // },
      {
        title: t('common.actions'),
        key: 'action',
        dataIndex: 'action',
        width: 120,
        fixed: 'right',
        render: (key, item) => (
          <Permission requiredPermissions={['View']}>
            <Button type="link" onClick={() => checkConfig(item)}>
              {t('node-manager.cloudregion.node.checkConfig')}
            </Button>
          </Permission>
        ),
      },
    ],
    [checkConfig, t]
  );
  return columns;
};

export const useGroupNames = () => {
  const commonContext = useUserInfoContext();
  const showGroupNames = (ids: string[]) => {
    const groups = commonContext?.groups || [];
    const groupName = ids.map(
      (item) => groups.find((group) => group.id === item)?.name
    );
    return groupName.join(',');
  };
  return {
    showGroupNames,
  };
};

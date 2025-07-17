import React, { useMemo } from 'react';
import { useTranslation } from '@/utils/i18n';
import PermissionWrapper from '@/components/permission';
import type { MenuProps } from 'antd';
import { ListItem } from '@/types';

const useAssetMenuItems = (): MenuProps['items'] => {
  const { t } = useTranslation();
  return useMemo(
    () => [
      {
        label: (
          <PermissionWrapper
            className="customMenuItem"
            requiredPermissions={['Edit']}
          >
            {t('common.batchEdit')}
          </PermissionWrapper>
        ),
        key: 'batchEdit',
      },
      {
        label: (
          <PermissionWrapper
            className="customMenuItem"
            requiredPermissions={['Delete']}
          >
            {t('common.batchDelete')}
          </PermissionWrapper>
        ),
        key: 'batchDelete',
      },
    ],
    [t]
  );
};

const useConditionList = (): ListItem[] => {
  const { t } = useTranslation();
  return useMemo(
    () => [
      { id: '==', name: '=' },
      { id: '!=', name: '!=' },
      { id: 'contains', name: t('log.include') },
      { id: '!contains', name: t('log.exclude') },
    ],
    [t]
  );
};

const useTermList = (): ListItem[] => {
  const { t } = useTranslation();
  return useMemo(
    () => [
      { id: 'OR', name: t('log.integration.anyCondition') },
      { id: 'AND', name: t('log.integration.allConditions') },
    ],
    [t]
  );
};

export { useAssetMenuItems, useConditionList, useTermList };

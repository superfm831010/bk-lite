import { useTranslation } from '@/utils/i18n';
import { useMemo } from 'react';
import { SegmentedItem } from '@/app/node-manager/types';
import PermissionWrapper from '@/components/permission';
import type { MenuProps } from 'antd';

const useTelegrafMap = (): Record<string, Record<string, string>> => {
  const { t } = useTranslation();
  return useMemo(
    () => ({
      1: {
        tagColor: 'default',
        color: '#b2b5bd',
        text: t('node-manager.cloudregion.node.unknown'),
      },
      0: {
        tagColor: 'success',
        color: '#52c41a',
        text: t('node-manager.cloudregion.node.running'),
      },
      2: {
        tagColor: 'error',
        color: '#ff4d4f',
        text: t('node-manager.cloudregion.node.error'),
      },
      4: {
        tagColor: 'default',
        color: '#b2b5bd',
        text: t('node-manager.cloudregion.node.stop'),
      },
      10: {
        tagColor: 'processing',
        color: '#1677ff',
        text: t('node-manager.cloudregion.node.installing'),
        engText: 'Installing',
      },
      11: {
        tagColor: 'success',
        color: '#52c41a',
        text: t('node-manager.cloudregion.node.successInstall'),
        engText: 'Installed successfully',
      },
      12: {
        tagColor: 'error',
        color: '#ff4d4f',
        text: t('node-manager.cloudregion.node.failInstall'),
        engText: 'Installation failed',
      },
    }),
    [t]
  );
};

const useInstallMap = (): Record<string, Record<string, string>> => {
  const { t } = useTranslation();
  return useMemo(
    () => ({
      waiting: {
        color: 'var(--color-primary)',
        text: t('node-manager.cloudregion.node.installing'),
      },
      waitingUninstall: {
        color: 'var(--color-primary)',
        text: t('node-manager.cloudregion.node.uninstalling'),
      },
      success: {
        color: '#52c41a',
        text: t('node-manager.cloudregion.node.successInstall'),
      },
      successUninstall: {
        color: '#52c41a',
        text: t('node-manager.cloudregion.node.successInstall'),
      },
      error: {
        color: '#ff4d4f',
        text: t('node-manager.cloudregion.node.failInstall'),
      },
      errorUninstall: {
        color: '#ff4d4f',
        text: t('node-manager.cloudregion.node.failUninstall'),
      },
    }),
    [t]
  );
};

const useInstallWays = (): SegmentedItem[] => {
  const { t } = useTranslation();
  return useMemo(
    () => [
      {
        label: t('node-manager.cloudregion.node.remoteInstall'),
        value: 'remoteInstall',
      },
      {
        label: t('node-manager.cloudregion.node.manualInstall'),
        value: 'manualInstall',
      },
    ],
    [t]
  );
};

const useCollectorItems = (): MenuProps['items'] => {
  const { t } = useTranslation();
  return useMemo(
    () => [
      {
        label: (
          <PermissionWrapper
            className="customMenuItem"
            requiredPermissions={['OperateCollector']}
          >
            {t('node-manager.cloudregion.node.installCollector')}
          </PermissionWrapper>
        ),
        key: 'installCollector',
      },
      {
        label: (
          <PermissionWrapper
            className="customMenuItem"
            requiredPermissions={['OperateCollector']}
          >
            {t('node-manager.cloudregion.node.startCollector')}
          </PermissionWrapper>
        ),
        key: 'startCollector',
      },
      {
        label: (
          <PermissionWrapper
            className="customMenuItem"
            requiredPermissions={['OperateCollector']}
          >
            {t('node-manager.cloudregion.node.restartCollector')}
          </PermissionWrapper>
        ),
        key: 'restartCollector',
      },
      {
        label: (
          <PermissionWrapper
            className="customMenuItem"
            requiredPermissions={['OperateCollector']}
          >
            {t('node-manager.cloudregion.node.stopCollector')}
          </PermissionWrapper>
        ),
        key: 'stopCollector',
      },
      //   {
      //     label: t('node-manager.cloudregion.node.uninstallCollector'),
      //     key: 'uninstallCollector',
      //   },
    ],
    [t]
  );
};

const useSidecarItems = (): MenuProps['items'] => {
  const { t } = useTranslation();
  return useMemo(
    () => [
      //   {
      //     label: (
      //       <div style={{ whiteSpace: 'nowrap' }}>
      //         {t('node-manager.cloudregion.node.restartSidecar')}
      //       </div>
      //     ),
      //     key: 'restartSidecar',
      //   },
      {
        label: (
          <PermissionWrapper
            className="customMenuItem"
            requiredPermissions={['UninstallController']}
          >
            {t('node-manager.cloudregion.node.uninstallSidecar')}
          </PermissionWrapper>
        ),
        key: 'uninstallSidecar',
      },
    ],
    [t]
  );
};

const OPERATE_SYSTEMS: SegmentedItem[] = [
  {
    label: 'Linux',
    value: 'linux',
  },
  {
    label: 'Windows',
    value: 'windows',
  },
];

const BATCH_FIELD_MAPS: Record<string, string> = {
  os: 'operateSystem',
  organizations: 'organaziton',
  username: 'loginAccount',
  port: 'loginPort',
  password: 'loginPassword',
};

const useMenuItem = () => {
  const { t } = useTranslation();
  return useMemo(
    () => [
      {
        key: 'edit',
        role: 'Edit',
        title: 'edit',
        config: {
          title: 'editform',
          type: 'edit',
        },
      },
      {
        key: 'delete',
        role: 'Delete',
        title: 'delete',
        config: {
          title: 'deleteform',
          type: 'delete',
        },
      },
    ],
    [t]
  );
};

export {
  useTelegrafMap,
  useInstallWays,
  useInstallMap,
  useSidecarItems,
  useCollectorItems,
  useMenuItem,
  OPERATE_SYSTEMS,
  BATCH_FIELD_MAPS,
};

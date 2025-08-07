import { ListItem } from '@/app/log/types';
import { useMemo } from 'react';
import { useTranslation } from '@/utils/i18n';

export const useConditionList = (): ListItem[] => {
  const { t } = useTranslation();
  return useMemo(
    () => [
      { id: '=', name: t('log.equalto') },
      { id: '!=', name: t('log.notequalTo') },
      { id: '>', name: t('log.moreThan') },
      { id: '<', name: t('log.lessThan') },
      { id: 'in', name: t('log.include') },
      { id: 'nin', name: t('log.exclude') },
    ],
    [t]
  );
};

export const useAlgorithmList = (): ListItem[] => {
  const { t } = useTranslation();
  return useMemo(
    () => [
      {
        value: 'keyword',
        icon: 'yuzhiguanli',
        title: t('log.event.keywordAlert'),
        content: t('log.event.keywordAlertDes'),
      },
      {
        value: 'aggregate',
        icon: 'yuzhiguanli',
        title: t('log.event.aggregationAlert'),
        content: t('log.event.aggregationAlertDes'),
      },
    ],
    [t]
  );
};

export const useScheduleList = (): ListItem[] => {
  const { t } = useTranslation();
  return useMemo(
    () => [
      { label: t('monitor.events.minutes'), value: 'min' },
      { label: t('monitor.events.hours'), value: 'hour' },
      { label: t('monitor.events.days'), value: 'day' },
    ],
    [t]
  );
};

export const useLevelList = (): ListItem[] => {
  const { t } = useTranslation();
  return useMemo(
    () => [
      { label: t('monitor.events.critical'), value: 'critical' },
      { label: t('monitor.events.error'), value: 'error' },
      { label: t('monitor.events.warning'), value: 'warning' },
    ],
    [t]
  );
};

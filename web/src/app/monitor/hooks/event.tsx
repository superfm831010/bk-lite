import { useTranslation } from '@/utils/i18n';

export const useAlertDetailTabs = () => {
  const { t } = useTranslation();
  return [
    {
      label: t('common.detail'),
      key: 'information',
    },
    {
      label: t('monitor.events.event'),
      key: 'event',
    },
  ];
};

export const useAlarmTabs = () => {
  const { t } = useTranslation();
  return [
    {
      label: t('monitor.events.activeAlarms'),
      key: 'activeAlarms',
    },
    {
      label: t('monitor.events.historicalAlarms'),
      key: 'historicalAlarms',
    },
  ];
};

export const useStateList = () => {
  const { t } = useTranslation();
  return [
    {
      label: t('monitor.events.new'),
      value: 'new',
    },
    {
      label: t('monitor.events.recovery'),
      value: 'recovered',
    },
    {
      label: t('monitor.events.closed'),
      value: 'closed',
    },
  ];
};

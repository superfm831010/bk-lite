import { useTranslation } from '@/utils/i18n';

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
}
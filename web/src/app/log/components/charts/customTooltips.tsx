import React from 'react';
import { TooltipProps } from 'recharts';
import customTooltipStyle from './index.module.scss';
import { useLocalizedTime } from '@/hooks/useLocalizedTime';
import { useTranslation } from '@/utils/i18n';

interface CustomToolTipProps
  extends Omit<TooltipProps<any, string>, 'visible'> {
  visible?: boolean;
}

const CustomTooltip: React.FC<CustomToolTipProps> = ({
  active,
  payload,
  label,
  visible = true,
}) => {
  const { convertToLocalizedTime } = useLocalizedTime();
  const { t } = useTranslation();
  if (active && payload?.length && visible) {
    return (
      <div className={customTooltipStyle.customTooltip}>
        <p className="label">{`${t('common.time')}：${convertToLocalizedTime(
          label
        )}`}</p>
        <p className="value">{`${t('log.search.logCount')}：${
          payload[0]?.payload.value ?? '--'
        }`}</p>
      </div>
    );
  }
  return null;
};

export default CustomTooltip;

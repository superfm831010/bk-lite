import React from 'react';
import { TooltipProps } from 'recharts';
import customTooltipStyle from './index.module.scss';
import { useLocalizedTime } from '@/hooks/useLocalizedTime';

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
  if (active && payload?.length && visible) {
    return (
      <div className={customTooltipStyle.customTooltip}>
        <p className="label font-[600]">{`${convertToLocalizedTime(
          new Date(label * 1000) + ''
        )}`}</p>
        <div>
          <div className="flex items-center mt-[4px]">
            <span
              style={{
                display: 'inline-block',
                width: '10px',
                height: '10px',
                backgroundColor: 'var(--color-bg-1)',
                borderRadius: '50%',
                marginRight: '5px',
              }}
            ></span>
            <span className="font-[600] ml-[10px]">123</span>
          </div>
        </div>
      </div>
    );
  }
  return null;
};

export default CustomTooltip;

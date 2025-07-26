import React from 'react';
import { InputNumber, Space } from 'antd';
import { useTranslation } from '@/utils/i18n';

interface RangeInputProps {
  value?: [number, number];
  onChange?: (value: [number?, number?]) => void;
  placeholder?: [string, string];
  className?: string;
  min?: number;
  max?: number;
  labels?: [string, string]; // 新增标题配置
}

const RangeInput: React.FC<RangeInputProps> = ({
  value = [],
  onChange,
  placeholder = ['min', 'max'],
  className,
  min,
  max,
  labels = ['最小值', '最大值']
}) => {
  const [minValue, maxValue] = value;
  const { t } = useTranslation();
  
  const handleMinChange = (val: number | null) => {
    onChange?.([val || undefined, maxValue]);
  };

  const handleMaxChange = (val: number | null) => {
    onChange?.([minValue, val || undefined]);
  };

  return (
    <div className={className}>
      <Space.Compact style={{ width: '100%' }}>
        <div style={{ width: '50%' }}>
          <div style={{ 
            fontSize: '12px', 
            color: '#666', 
            marginBottom: '4px',
            textAlign: 'left'
          }}>
            {labels[0]}
          </div>
          <InputNumber
            style={{ width: '100%' }}
            placeholder={t(`mlops-common.${placeholder[0]}`)}
            value={minValue}
            onChange={handleMinChange}
            min={min}
            max={maxValue || max}
          />
        </div>
        <div style={{ width: '50%' }}>
          <div style={{ 
            fontSize: '12px', 
            color: '#666', 
            marginBottom: '4px',
            textAlign: 'left'
          }}>
            {labels[1]}
          </div>
          <InputNumber
            style={{ width: '100%' }}
            placeholder={t(`mlops-common.${placeholder[1]}`)}
            value={maxValue}
            onChange={handleMaxChange}
            min={minValue || min}
            max={max}
          />
        </div>
      </Space.Compact>
    </div>
  );
};

export default RangeInput;
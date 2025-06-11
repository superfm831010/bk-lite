import React from 'react';
import dayjs from 'dayjs';
import { Select, DatePicker, TimePicker } from 'antd';
import { timeInterval, weekList } from '@/app/alarm/constants/settings';

const { Option } = Select;
const { RangePicker } = DatePicker;

export interface EffectiveTimeValue {
  type: 'one' | 'day' | 'week' | 'month';
  week_month: number[];
  start_time: dayjs.Dayjs | string;
  end_time: dayjs.Dayjs | string;
}

interface EffectiveTimeProps {
  value?: EffectiveTimeValue;
  onChange?: (val: EffectiveTimeValue) => void;
}

const defaultValue: EffectiveTimeValue = {
  type: 'day',
  week_month: [],
  start_time: dayjs('00:00:00', 'HH:mm:ss'),
  end_time: dayjs('23:59:59', 'HH:mm:ss'),
};

const EffectiveTime: React.FC<EffectiveTimeProps> = ({ value, onChange }) => {
  const form = value || defaultValue;
  const isEditing = !!value;

  const triggerChange = (changed: Partial<EffectiveTimeValue>) => {
    onChange?.({ ...form, ...changed });
  };

  return (
    <div className="flex" id="effective-time">
      <div className="flex-1 mr-[6px]">
        <Select value={form.type} onChange={(v) => triggerChange({ type: v })}>
          {timeInterval.map((item) => (
            <Option key={item.value} value={item.value}>
              {item.name}
            </Option>
          ))}
        </Select>
      </div>
      <div className="flex-[4] flex">
        {form.type === 'week' && (
          <Select
            mode="multiple"
            maxTagCount={1}
            value={form.week_month}
            onChange={(v) => triggerChange({ week_month: v })}
            className="flex-1"
          >
            {weekList.map((item) => (
              <Option key={item.value} value={item.value}>
                {item.name}
              </Option>
            ))}
          </Select>
        )}
        {form.type === 'month' && (
          <Select
            mode="multiple"
            maxTagCount={2}
            value={form.week_month}
            onChange={(v) => triggerChange({ week_month: v })}
            className="flex-1"
          >
            {[...Array(31)].map((_, i) => (
              <Option key={i + 1} value={i + 1}>
                {i + 1}
              </Option>
            ))}
          </Select>
        )}
        {form.type !== 'one' && (
          <TimePicker.RangePicker
            allowClear={false}
            format="HH:mm:ss"
            className="flex-1 ml-[6px]"
            value={
              isEditing
                ? [
                  dayjs(form.start_time, 'HH:mm:ss'),
                  dayjs(form.end_time, 'HH:mm:ss'),
                ]
                : [dayjs().startOf('day'), dayjs().endOf('day')]
            }
            onChange={(_, dateStrings) =>
              triggerChange({
                start_time: dateStrings[0],
                end_time: dateStrings[1],
              })
            }
          />
        )}
        {form.type === 'one' && (
          <RangePicker
            showTime
            format="YYYY-MM-DD HH:mm:ss"
            allowClear={false}
            className="flex-1 ml-[6px]"
            value={
              form.start_time && form.end_time
                ? [
                  dayjs(form.start_time as string, 'YYYY-MM-DD HH:mm:ss'),
                  dayjs(form.end_time as string, 'YYYY-MM-DD HH:mm:ss'),
                ]
                : [dayjs().startOf('day'), dayjs().add(1, 'month').endOf('day')]
            }
            onChange={(_, dateStrings) => {
              if (dateStrings?.length === 2) {
                triggerChange({
                  start_time: dateStrings[0],
                  end_time: dateStrings[1],
                });
              }
            }}
          />
        )}
      </div>
    </div>
  );
};

export default EffectiveTime;

export { defaultValue as defaultEffectiveTime };

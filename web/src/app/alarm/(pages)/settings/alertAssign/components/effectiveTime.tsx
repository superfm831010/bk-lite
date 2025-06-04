'use client';

import React, { useState } from 'react';
import dayjs, { Dayjs } from 'dayjs';
import { Select, DatePicker, TimePicker } from 'antd';

const { Option } = Select;
const { RangePicker } = DatePicker;

const EffectiveTime: React.FC = () => {
  const [form, setForm] = useState<{
    period: string;
    weekDays: number[];
    monthDays: number[];
    onceTime: [Dayjs, Dayjs];
    clockTime: [string, string];
  }>({
    period: 'everyday',
    weekDays: [1, 2, 3],
    monthDays: [1],
    onceTime: [dayjs(), dayjs().add(1, 'day')],
    clockTime: ['00:00:00', '23:59:59'],
  });

  const timeInterval = [
    { name: '单次', value: 'once' },
    { name: '每天', value: 'everyday' },
    { name: '每周', value: 'every_week' },
    { name: '每月', value: 'every_month' },
  ];

  const weekList = [
    { name: '星期一', value: 1 },
    { name: '星期二', value: 2 },
    { name: '星期三', value: 3 },
    { name: '星期四', value: 4 },
    { name: '星期五', value: 5 },
    { name: '星期六', value: 6 },
    { name: '星期天', value: 7 },
  ];

  const onFormChange = (key: string, value: any) => {
    setForm((prevForm) => ({ ...prevForm, [key]: value }));
  };

  return (
    <div className="flex" id="effective-time">
      <div className="flex-1">
        <Select
          value={form.period}
          onChange={(value) => onFormChange('period', value)}
        >
          {timeInterval.map((item) => (
            <Option key={item.value} value={item.value}>
              {item.name}
            </Option>
          ))}
        </Select>
      </div>
      <div className="flex-[3] flex">
        {form.period === 'every_week' && (
          <Select
            mode="multiple"
            maxTagCount={1}
            value={form.weekDays}
            onChange={(value) => onFormChange('weekDays', value)}
            className="flex-1"
          >
            {weekList.map((item) => (
              <Option key={item.value} value={item.value}>
                {item.name}
              </Option>
            ))}
          </Select>
        )}

        {form.period === 'every_month' && (
          <Select
            mode="multiple"
            maxTagCount={2}
            value={form.monthDays}
            onChange={(value) => onFormChange('monthDays', value)}
            className="flex-1"
          >
            {[...Array(31)].map((_, index) => (
              <Option key={index + 1} value={index + 1}>
                {index + 1}
              </Option>
            ))}
          </Select>
        )}
        {form.period !== 'once' && (
          <TimePicker.RangePicker
            className="flex-1"
            value={[
              dayjs(form.clockTime[0], 'HH:mm:ss'),
              dayjs(form.clockTime[1], 'HH:mm:ss'),
            ]}
            onChange={(_, timeString) => onFormChange('clockTime', timeString)}
          />
        )}
        {form.period === 'once' && (
          <RangePicker
            showTime
            value={form.onceTime}
            className="flex-1"
            onChange={(dates) => {
              if (dates && dates.length === 2) {
                onFormChange('onceTime', dates as [Dayjs, Dayjs]);
              }
            }}
          />
        )}
      </div>
    </div>
  );
};

export default EffectiveTime;

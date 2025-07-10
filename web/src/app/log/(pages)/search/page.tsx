'use client';
import React, { useState, useRef } from 'react';
import TimeSelector from '@/components/time-selector';
import { TimeSelectorRef } from '@/types';
import dayjs from 'dayjs';

const SearchView: React.FC = () => {
  const timeSelectorRef = useRef<TimeSelectorRef>(null);
  const [frequence, setFrequence] = useState<number>(0);
  const dateFormat = 'YYYY-MM-DD HH:MM:SS';

  const onFrequenceChange = (val: number) => {
    setFrequence(val);
  };

  const onRefresh = () => {
    const val = timeSelectorRef.current?.getValue();
    console.log(val, frequence);
  };

  const onTimeChange = () => {
    const val = timeSelectorRef.current?.getValue();
    console.log(val);
  };

  return (
    <div className="w-full">
      <div className="flex justify-end">
        <TimeSelector
          ref={timeSelectorRef}
          defaultValue={{
            selectValue: 0,
            rangePickerVaule: [
              dayjs('2015-06-01 12:00:00', dateFormat),
              dayjs('2015-06-06 12:00:00', dateFormat),
            ],
          }}
          onChange={onTimeChange}
          onFrequenceChange={onFrequenceChange}
          onRefresh={onRefresh}
        />
      </div>
    </div>
  );
};

export default SearchView;

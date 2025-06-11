'use client';

import React, { useMemo, useRef, useState } from 'react';
import dayjs from 'dayjs';
import minMax from 'dayjs/plugin/minMax';
import styles from './index.module.scss';
import AlertDetail from '../../../alarms/components/alarmDetail';
import { AlarmTableDataItem } from '@/app/alarm/types/alarms';
import { ModalRef } from '@/app/alarm/types/types';
import { Tooltip, Checkbox } from 'antd';
import { useCommon } from '@/app/alarm/context/common';
dayjs.extend(minMax);

interface GanttChartProps {
  alarmData: AlarmTableDataItem[];
}

export default function GanttChart({ alarmData }: GanttChartProps) {
  const { levelMap } = useCommon();
  const detailRef = useRef<ModalRef>(null);
  const [selectedTasks, setSelectedTasks] = useState<number[]>([]);

  const times = useMemo(() => {
    const starts = alarmData.map((d) => dayjs(d.first_event_time));
    const ends = alarmData.map((d) => dayjs(d.last_event_time));
    const min = dayjs.min(...starts) ?? dayjs(alarmData[0].first_event_time);
    const max = dayjs.max(...ends) ?? dayjs(alarmData[0].last_event_time);
    const total = max.diff(min);
    return { min, max, total };
  }, [alarmData]);

  const ticks = useMemo(() => {
    const totalMs = times.total;
    const minTicks = 6;
    const count = Math.max(minTicks, minTicks);
    const intervalMs = totalMs / count;
    return Array.from({ length: count + 1 }).map((_, i) => {
      const tm = dayjs(times.min.valueOf() + intervalMs * i);
      const left = (tm.diff(times.min) / totalMs) * 100;
      return { label: tm.format('MM-DD HH:mm'), left };
    });
  }, [times]);

  const onOpenDetail = (task: any) => {
    detailRef.current?.showModal({
      title: task.title,
      type: 'add',
      form: {
        id: task.id,
        level: task.level,
        content: task.title,
      },
    });
  };

  const toggleTask = (id: number) => {
    setSelectedTasks((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  const sortedData = useMemo(
    () =>
      [...alarmData].sort(
        (a: any, b: any) =>
          new Date(a.first_event_time).getTime() -
          new Date(b.first_event_time).getTime()
      ),
    [alarmData]
  );

  return (
    <>
      <div className={styles.chartWrapper}>
        <div className={styles.chartGrid}>
          <div className={styles.emptyHeader} />
          <div className={styles.axis}>
            {ticks.map((t, idx) => (
              <React.Fragment key={idx}>
                {t.left < 100 && (
                  <span
                    className={styles.axisTick}
                    style={{ left: `${t.left}%` }}
                  >
                    {t.label}
                  </span>
                )}
              </React.Fragment>
            ))}
          </div>
          <div>
            {ticks.map((t, idx) => (
              <div
                key={`full-line-${idx}`}
                className={styles.axisLine}
                style={{ left: `${t.left}%` }}
              />
            ))}
          </div>
          <div className={styles.chartContent}>
            {sortedData.map((d) => {
              const s = dayjs(d.first_event_time).diff(times.min);
              const w = dayjs(d.last_event_time).diff(
                dayjs(d.first_event_time)
              );
              const left = (s / times.total) * 100;
              const width = (w / times.total) * 100;
              return (
                <div key={d.id} className={styles.alarmRow}>
                  <Checkbox
                    className={styles.alarmCheckbox}
                    checked={selectedTasks.includes(d.id)}
                    onChange={() => toggleTask(d.id)}
                  />
                  <div className={styles.barContainer}>
                    <Tooltip
                      placement="top"
                      title={
                        <>
                          <div>{d.title}</div>
                          <div>开始: {d.first_event_time}</div>
                          <div>结束: {d.last_event_time}</div>
                          <div>操作者: {d.operator_user}</div>
                        </>
                      }
                    >
                      <div
                        className={styles.bar}
                        style={{
                          left: `${left}%`,
                          width: `${width}%`,
                          backgroundColor: levelMap[d.level] as string,
                        }}
                        onClick={() => onOpenDetail(d)}
                      ></div>

                      <div
                        className={styles.title}
                        style={{
                          left: `${left}%`,
                          right: 0,
                        }}
                      >
                        {d.title}
                      </div>
                    </Tooltip>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
        <AlertDetail ref={detailRef} />
      </div>
    </>
  );
}

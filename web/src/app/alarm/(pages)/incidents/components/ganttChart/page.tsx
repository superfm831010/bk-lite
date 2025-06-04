'use client';

import React, { useMemo, useRef, useState } from 'react';
import dayjs from 'dayjs';
import minMax from 'dayjs/plugin/minMax';
import styles from './index.module.scss';
import AlertDetail from '../../../alarms/components/alarmDetail';
import { ModalRef } from '@/app/alarm/types/types';
import { Tooltip, Checkbox } from 'antd';

dayjs.extend(minMax);

interface Task {
  id: number;
  name: string;
  level: string;
  start: string;
  end: string;
  details: string;
}

const generateMock = (): Task[] => {
  const now = dayjs();
  return Array.from({ length: 5 }).map((_, i) => {
    const start = now.subtract(6 - i, 'hour').toISOString();
    const end = now
      .subtract(6 - i, 'hour')
      .add(Math.random() * 4 + 1, 'hour')
      .toISOString();
    return {
      id: i + 1,
      name: `告警事件${i + 1}`,
      level: '',
      start,
      end,
      details: `来源: Server ${String.fromCharCode(65 + (i % 3))}，次数: ${Math.ceil(
        Math.random() * 5
      )}，时长: ${dayjs(end).diff(dayjs(start), 'minute')}m`,
    };
  });
};

const GanttChart: React.FC = () => {
  const detailRef = useRef<ModalRef>(null);
  const [selectedTasks, setSelectedTasks] = useState<number[]>([]);
  const data = useMemo(generateMock, []);
  const times = useMemo(() => {
    const starts = data.map((d) => dayjs(d.start));
    const ends = data.map((d) => dayjs(d.end));
    const min = dayjs.min(...starts) ?? dayjs(data[0].start);
    const max = dayjs.max(...ends) ?? dayjs(data[0].end);
    const total = max.diff(min);
    return { min, max, total };
  }, [data]);

  const ticks = useMemo(() => {
    const hourMs = 60 * 60 * 1000;
    const count = Math.ceil(times.total / hourMs);
    return Array.from({ length: count + 1 }).map((_, i) => {
      const tm = times.min.add(i, 'hour');
      const left = (tm.diff(times.min) / times.total) * 100;
      return { label: tm.format('MM-DD HH:mm'), left };
    });
  }, [times]);

  const onOpenDetail = (task: Task) => {
    detailRef.current?.showModal({
      title: task.name,
      type: 'add',
      form: {
        id: task.id,
        level: task.level,
        content: task.name,
      },
    });
  };

  const toggleTask = (id: number) => {
    setSelectedTasks((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

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
            {data.map((d) => {
              const s = dayjs(d.start).diff(times.min);
              const w = dayjs(d.end).diff(dayjs(d.start));
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
                      title={
                        <>
                          <div>{d.name}</div>
                          <div>
                            开始: {dayjs(d.start).format('YYYY-MM-DD HH:mm')}
                          </div>
                          <div>
                            结束: {dayjs(d.end).format('YYYY-MM-DD HH:mm')}
                          </div>
                          <div>{d.details}</div>
                        </>
                      }
                      placement="top"
                    >
                      <div
                        className={styles.bar}
                        style={{
                          left: `${left}%`,
                          width: `${width}%`,
                          backgroundColor: '',
                        }}
                        onClick={() => onOpenDetail(d)}
                      >
                        {d.name}
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
};

export default GanttChart;

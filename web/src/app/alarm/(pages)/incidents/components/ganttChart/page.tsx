import React, { useMemo } from 'react';
import dayjs from 'dayjs';
import minMax from 'dayjs/plugin/minMax';
import styles from './index.module.scss';
import { LEVEL_MAP } from '@/app/alarm/constants/monitor';

dayjs.extend(minMax);

interface Task { id: number; name: string; level: keyof typeof LEVEL_MAP; start: string; end: string; }

const generateMock = (): Task[] => {
  const now = dayjs();
  const levels = Object.keys(LEVEL_MAP) as Array<keyof typeof LEVEL_MAP>;
  return Array.from({ length: 5 }).map((_, i) => {
    const level = levels[i % levels.length];
    const start = now.subtract(5 - i, 'hour').toISOString();
    const end = now.subtract(5 - i, 'hour').add(Math.random() * 4 + 1, 'hour').toISOString();
    return { id: i, name: `Alert ${i + 1}`, level, start, end };
  });
};

const GanttChart: React.FC = () => {
  const data = useMemo(generateMock, []);
  const times = useMemo(() => {
    const starts = data.map(d => dayjs(d.start));
    const ends = data.map(d => dayjs(d.end));
    const min = dayjs.min(...starts) ?? dayjs(data[0]?.start);
    const max = dayjs.max(...ends) ?? dayjs(data[0]?.end);
    const total = max.diff(min);
    return { min, total };
  }, [data]);

  return (
    <div className={styles.chart}>
      {data.map((d: any) => {
        const s = dayjs(d.start).diff(times.min);
        const w = dayjs(d.end).diff(dayjs(d.start));
        const left = (s / times.total) * 100;
        const width = (w / times.total) * 100;
        return (
          <div className={styles.row} key={d.id}>
            <div className={styles.label}>
              <span className={styles.levelDot} style={{ backgroundColor: LEVEL_MAP[d.level] as string }} />
              {d.name}
            </div>
            <div className={styles.barContainer}>
              <div
                className={styles.bar}
                style={{
                  left: `${left}%`,
                  width: `${width}%`,
                  backgroundColor: LEVEL_MAP[d.level] as string,
                }}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default GanttChart;

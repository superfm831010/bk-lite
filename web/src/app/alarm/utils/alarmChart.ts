import dayjs from 'dayjs';
import { AlarmTableDataItem } from '@/app/alarm/types/alarms';
import { LevelItem } from '@/app/alarm/types/index';

/**
 * 将告警数据按动态时间区间（秒/分钟/小时/天）分桶，生成适合堆叠柱状图的格式
 * @param data 原始告警列表
 * @param levelList 等级列表，用于初始化各级别统计字段
 * @param convertToLocalizedTime 本地化时间转换函数
 * @param desiredSegments 框定分段数量，默认 12
 */
export function processDataForStackedBarChart(
  data: AlarmTableDataItem[],
  levelList: LevelItem[],
  convertToLocalizedTime: (iso: string) => string,
  desiredSegments = 12
) {
  if (!data?.length) return [];

  // 1. 找最早和最晚时间
  const timestamps = data.map((it) => dayjs(it.created_at));
  const minTime = timestamps.reduce(
    (min, cur) => (cur.isBefore(min) ? cur : min),
    timestamps[0]
  );
  const maxTime = timestamps.reduce(
    (max, cur) => (cur.isAfter(max) ? cur : max),
    timestamps[0]
  );

  // 2. 计算差值：秒/分/小时/天
  const totalSeconds = maxTime.diff(minTime, 'second');
  const totalMinutes = maxTime.diff(minTime, 'minute');
  const totalHours = maxTime.diff(minTime, 'hour');
  const totalDays = maxTime.diff(minTime, 'day');

  // 3. 根据 desiredSegments 选择最合适单位
  let intervalUnit: 'second' | 'minute' | 'hour' | 'day';
  let intervalCount: number;
  if (totalSeconds <= desiredSegments) {
    intervalUnit = 'second';
    intervalCount = 1;
  } else if (totalMinutes <= desiredSegments) {
    intervalUnit = 'minute';
    intervalCount = Math.ceil(totalMinutes / desiredSegments);
  } else if (totalHours <= desiredSegments) {
    intervalUnit = 'hour';
    intervalCount = Math.ceil(totalHours / desiredSegments);
  } else {
    intervalUnit = 'day';
    intervalCount = Math.ceil(totalDays / desiredSegments);
  }

  // 4. 构造均匀时间刻度分段，并初始化所有分段数据为 0
  // 4.1 计算总分段数
  const totalUnits =
    intervalUnit === 'second'
      ? totalSeconds
      : intervalUnit === 'minute'
        ? totalMinutes
        : intervalUnit === 'hour'
          ? totalHours
          : totalDays;
  const segmentsCount = Math.ceil(totalUnits / intervalCount);
  const grouped: Record<string, any> = {};
  for (let i = 0; i <= segmentsCount; i++) {
    const bucketTime = minTime.add(i * intervalCount, intervalUnit);
    const localTime = convertToLocalizedTime(bucketTime.toISOString());
    const fmt =
      intervalUnit === 'day'
        ? dayjs(localTime).format('YYYY-MM-DD')
        : intervalUnit === 'hour'
          ? dayjs(localTime).format('YYYY-MM-DD HH:00')
          : intervalUnit === 'minute'
            ? dayjs(localTime).format('YYYY-MM-DD HH:mm')
            : dayjs(localTime).format('YYYY-MM-DD HH:mm:ss');
    grouped[fmt] = {
      time: fmt,
      ...levelList.reduce(
        (acc, lvl) => {
          acc[lvl.level_display_name] = 0;
          return acc;
        },
        {} as Record<string, number>
      ),
    };
  }

  // 5. 遍历数据，累加到对应分段
  data.forEach((item) => {
    const bucketIndex = Math.floor(
      dayjs(item.first_event_time).diff(minTime, intervalUnit) / intervalCount
    );
    const bucketStart = minTime.add(bucketIndex * intervalCount, intervalUnit);
    const localBucket = convertToLocalizedTime(bucketStart.toISOString());
    const bucketKey =
      intervalUnit === 'day'
        ? dayjs(localBucket).format('YYYY-MM-DD')
        : intervalUnit === 'hour'
          ? dayjs(localBucket).format('YYYY-MM-DD HH:00')
          : intervalUnit === 'minute'
            ? dayjs(localBucket).format('YYYY-MM-DD HH:mm')
            : dayjs(localBucket).format('YYYY-MM-DD HH:mm:ss');
    const lvl = levelList.find((l) => l.level_id === Number(item.level));
    if (lvl && grouped[bucketKey]) {
      grouped[bucketKey][lvl.level_display_name] += 1;
    }
  });

  // 6. 排序并返回数组
  return Object.values(grouped).sort(
    (a: any, b: any) => dayjs(a.time).valueOf() - dayjs(b.time).valueOf()
  );
}

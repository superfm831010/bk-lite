import {
  SubGroupItem,
  ListItem,
  ViewQueryKeyValuePairs,
  ChartData,
} from '@/app/alarm/types';
import {
  MetricItem,
  ChartDataItem,
  ChartProps,
} from '@/app/alarm/types/alarms';
import { UNIT_LIST, APPOINT_METRIC_IDS } from '@/app/alarm/constants/monitor';

// 深克隆
export const deepClone = (obj: any, hash = new WeakMap()) => {
  if (Object(obj) !== obj) return obj;
  if (obj instanceof Set) return new Set(obj);
  if (hash.has(obj)) return hash.get(obj);

  const result =
    obj instanceof Date
      ? new Date(obj)
      : obj instanceof RegExp
        ? new RegExp(obj.source, obj.flags)
        : obj.constructor
          ? new obj.constructor()
          : Object.create(null);

  hash.set(obj, result);

  if (obj instanceof Map) {
    Array.from(obj, ([key, val]) => result.set(key, deepClone(val, hash)));
  }

  // 复制函数
  if (typeof obj === 'function') {
    return function (this: unknown, ...args: unknown[]): unknown {
      return obj.apply(this, args);
    };
  }

  // 递归复制对象的其他属性
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      // File不做处理
      if (obj[key] instanceof File) {
        result[key] = obj[key];
        continue;
      }
      result[key] = deepClone(obj[key], hash);
    }
  }

  return result;
};

// 判断一个字符串是否是字符串的数组
export const isStringArray = (input: string): boolean => {
  try {
    if (typeof input !== 'string') {
      return false;
    }
    const parsed = JSON.parse(input);
    if (!Array.isArray(parsed)) {
      return false;
    }
    return true;
  } catch {
    return false;
  }
};

// 根据指标枚举获取值+单位
export const getEnumValueUnit = (metric: MetricItem, id: number | string) => {
  const { unit: input = '', name } = metric || {};
  if (!id && id !== 0) return '--';
  if (isStringArray(input)) {
    return (
      JSON.parse(input).find((item: ListItem) => item.id === +id)?.name || id
    );
  }
  const unit = findUnitNameById(input);
  return isNaN(+id) || APPOINT_METRIC_IDS.includes(name)
    ? `${id} ${unit}`
    : `${(+id).toFixed(2)} ${unit}`;
};

export const mergeViewQueryKeyValues = (
  pairs: ViewQueryKeyValuePairs[]
): string => {
  const mergedObject: { [key: string]: Set<string> } = {};
  pairs.forEach((pair) => {
    (pair.keys || []).forEach((key, index) => {
      const value = (pair.values || [])[index];
      if (!mergedObject[key]) {
        mergedObject[key] = new Set();
      }
      mergedObject[key].add(value);
    });
  });

  const resultArray: string[] = [];
  for (const key in mergedObject) {
    const values = Array.from(mergedObject[key]).join('|');
    resultArray.push(`${key}=~"${values}"`);
  }

  return resultArray.join(',');
};

export const renderChart = (
  data: ChartDataItem[],
  config: ChartProps[]
): ChartData[] => {
  const result: any[] = [];
  const target = config[0]?.dimensions || [];
  data.forEach((item, index) => {
    item.values.forEach(([timestamp, value]) => {
      const existing = result.find((entry) => entry.time === timestamp);
      let detailValue = Object.entries(item.metric)
        .map(([key, dimenValue]) => ({
          name: key,
          label: target.find((sec) => sec.name === key)?.description || key,
          value: dimenValue,
        }))
        .filter((item) => target.find((tex) => tex.name === item.name));
      if ((!target.length || !detailValue.length) && config[0]?.showInstName) {
        detailValue = [
          {
            name: 'instance_name',
            label: 'Instance',
            value:
              config.find(
                (detail) =>
                  JSON.stringify(detail.instance_id_values) ===
                  JSON.stringify(
                    detail.instance_id_keys.reduce((pre, cur) => {
                      return pre.concat(item.metric[cur] as any);
                    }, [])
                  )
              )?.instance_name || '',
          },
        ];
      }
      if (existing) {
        existing[`value${index + 1}`] = parseFloat(value);
        if (!existing.details[`value${index + 1}`]) {
          existing.details[`value${index + 1}`] = [];
        }
        existing.details[`value${index + 1}`].push(...detailValue);
      } else {
        const details = {
          [`value${index + 1}`]: detailValue,
        };
        result.push({
          time: timestamp,
          title: config[0]?.title || '--',
          [`value${index + 1}`]: parseFloat(value),
          details,
        });
      }
    });
  });
  return result;
};

// 根据id找到单位名称（单个id展示）
export const findUnitNameById = (
  value: unknown,
  arr: Array<any> = UNIT_LIST
) => {
  for (let i = 0; i < arr.length; i++) {
    if (arr[i].value === value) {
      return arr[i].unit;
    }
    if (arr[i].children && arr[i].children?.length) {
      const label: unknown = findUnitNameById(value, arr[i]?.children || []);
      if (label) {
        return label;
      }
    }
  }
  return '';
};

// 根据分组id找出分组名称(多个id展示)
export const showGroupName = (
  groupIds: string[],
  organizationList: Array<SubGroupItem>
) => {
  if (!groupIds?.length) return '--';
  const groupNames: any[] = [];
  groupIds.forEach((el) => {
    groupNames.push(findGroupNameById(organizationList, el));
  });
  return groupNames.filter((item) => !!item).join(',');
};

// 根据分组id找出分组名称(单个id展示)
export const findGroupNameById = (arr: Array<SubGroupItem>, value: unknown) => {
  for (let i = 0; i < arr.length; i++) {
    if (arr[i].value === value) {
      return arr[i].label;
    }
    if (arr[i].children && arr[i].children?.length) {
      const label: unknown = findGroupNameById(arr[i]?.children || [], value);
      if (label) {
        return label;
      }
    }
  }
  return null;
};
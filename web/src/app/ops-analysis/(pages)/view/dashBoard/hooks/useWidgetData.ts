import { useState, useEffect } from 'react';
import dayjs from 'dayjs';
import { useDataSourceApi } from '@/app/ops-analysis/api/dataSource';

interface UseWidgetDataOptions {
  config?: any;
  globalTimeRange?: any;
  refreshKey?: number;
  transformData?: (data: any) => any;
}

interface UseWidgetDataReturn {
  data: any;
  loading: boolean;
  refetch: () => void;
}

// 格式化时间范围参数的工具函数
const formatTimeRange = (timeParams: any): string[] => {
  let startTime, endTime;

  if (timeParams && typeof timeParams === 'number') {
    // 数值类型：表示分钟数
    endTime = dayjs().valueOf();
    startTime = dayjs().subtract(timeParams, 'minute').valueOf();
  } else if (timeParams && Array.isArray(timeParams) && timeParams.length === 2) {
    // 数组类型：[startTime, endTime]
    startTime = timeParams[0];
    endTime = timeParams[1];
  } else if (timeParams && timeParams.start && timeParams.end) {
    // 对象类型：{ start, end }
    startTime = timeParams.start;
    endTime = timeParams.end;
  } else {
    // 默认时间范围：最近7天
    endTime = dayjs().valueOf();
    startTime = dayjs().subtract(7, 'day').valueOf();
  }

  const startTimeStr = dayjs(startTime).format('YYYY-MM-DD HH:mm:ss');
  const endTimeStr = dayjs(endTime).format('YYYY-MM-DD HH:mm:ss');

  return [startTimeStr, endTimeStr];
};

export const useWidgetData = ({
  config,
  globalTimeRange,
  refreshKey,
  transformData,
}: UseWidgetDataOptions): UseWidgetDataReturn => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const { getSourceDataByApiId } = useDataSourceApi();

  const buildRequestParams = () => {
    const params: Record<string, any> = {};
    const dataSourceParams = config?.dataSourceParams;

    if (dataSourceParams && Array.isArray(dataSourceParams)) {
      dataSourceParams.forEach((param: any) => {
        const { name, filterType, value: defaultValue, type, userValue } = param;

        if (filterType === 'fixed') {
          // fixed 类型：使用默认值
          if (type === 'timeRange') {
            params[name] = formatTimeRange(defaultValue);
          } else {
            params[name] = defaultValue;
          }
        } else if (filterType === 'filter') {
          // filter 类型：使用全局筛选器值
          if (type === 'timeRange') {
            params[name] = formatTimeRange(globalTimeRange);
          }
        } else if (filterType === 'params') {
          // params 类型：优先使用用户配置的值，如果没有则使用默认值
          const finalValue = userValue !== undefined && userValue !== null && userValue !== ''
            ? userValue
            : defaultValue;

          if (type === 'timeRange') {
            params[name] = formatTimeRange(finalValue);
          } else {
            params[name] = finalValue;
          }
        }
      });
    }

    return params;
  };

  const fetchData = async () => {
    if (!config?.dataSource) {
      setLoading(false);
      return;
    }
    try {
      setLoading(true);

      const requestParams = buildRequestParams();
      const rawData = await getSourceDataByApiId(config.dataSource, requestParams);

      const processedData = transformData ? transformData(rawData) : rawData;
      setData(processedData);
    } catch (err: any) {
      console.error('获取数据失败:', err);
      setData(null);
    } finally {
      setLoading(false);
    }
  }; useEffect(() => {
    if (config?.dataSource) {
      fetchData();
    }
  }, [config, globalTimeRange, refreshKey]);

  return {
    data,
    loading,
    refetch: fetchData,
  };
};

export const processDataSourceParams = (
  dataSource: any,
  userParams: Record<string, any> = {},
  globalTimeRange?: any
) => {
  if (!dataSource || !dataSource.params || !Array.isArray(dataSource.params)) {
    return userParams;
  }

  const processedParams = { ...userParams };

  dataSource.params.forEach((param: any) => {
    const { name, filterType, value: defaultValue, type } = param;

    if (filterType === 'fixed') {
      if (type === 'timeRange') {
        processedParams[name] = formatTimeRange(defaultValue);
      } else {
        processedParams[name] = defaultValue;
      }
    } else if (filterType === 'filter') {
      if (type === 'timeRange') {
        processedParams[name] = formatTimeRange(globalTimeRange);
      }
    } else if (filterType === 'params') {
      if (processedParams[name] === undefined || processedParams[name] === null || processedParams[name] === '') {
        if (type === 'timeRange') {
          processedParams[name] = formatTimeRange(defaultValue);
        } else {
          processedParams[name] = defaultValue;
        }
      } else if (type === 'timeRange') {
        processedParams[name] = formatTimeRange(processedParams[name]);
      }
    }
  });

  return processedParams;
};

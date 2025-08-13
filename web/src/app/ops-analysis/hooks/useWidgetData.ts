import { useState, useEffect } from 'react';
import dayjs from 'dayjs';
import { useDataSourceApi } from '@/app/ops-analysis/api/dataSource';
import { UseWidgetDataOptions, UseWidgetDataReturn } from '@/app/ops-analysis/types/dashBoard';


export const formatTimeRange = (timeParams: any): string[] => {
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

  const fetchData = async () => {
    if (!config?.dataSource) {
      setLoading(false);
      return;
    }
    try {
      setLoading(true);
      const userParams: any = {}
      config.dataSourceParams?.forEach((param: any) => {
        userParams[param.name] = param.value;
      })
      const requestParams = processDataSourceParams({
        sourceParams: config.dataSourceParams,
        userParams,
        globalTimeRange
      });
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

export const processDataSourceParams = ({
  sourceParams,
  userParams = {},
  globalTimeRange
}: {
  sourceParams: any;
  userParams?: Record<string, any>;
  globalTimeRange?: any;
}) => {

  if (!sourceParams || !Array.isArray(sourceParams)) {
    return userParams;
  }

  const processedParams = { ...userParams };

  sourceParams.forEach((param: any) => {
    const { name, filterType, value: defaultValue, type } = param;
    let finalValue;

    switch (filterType) {
      case 'fixed':
        finalValue = defaultValue;
        break;
      case 'filter':
        // filter 类型：时间范围使用全局时间，非时间范围使用默认值
        finalValue = (type === 'timeRange' && globalTimeRange) ? globalTimeRange : defaultValue;
        break;
      case 'params':
        finalValue = processedParams[name];
        break;
      default:
        finalValue = defaultValue;
    }

    processedParams[name] = (type === 'timeRange')
      ? formatTimeRange(finalValue)
      : finalValue;
  });

  return processedParams;
};

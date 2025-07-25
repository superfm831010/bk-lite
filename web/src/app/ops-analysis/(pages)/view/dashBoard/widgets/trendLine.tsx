import React, { useEffect, useState } from 'react';
import dayjs from 'dayjs';
import ReactEcharts from 'echarts-for-react';
import { Spin } from 'antd';
import { BaseWidgetProps } from '@/app/ops-analysis/types/dashBoard';
import { useDataSourceApi } from '@/app/ops-analysis/api/dataSource';

const TrendLine: React.FC<BaseWidgetProps> = ({
  config,
  globalTimeRange,
  refreshKey,
}) => {
  const [chartData, setChartData] = useState<{
    dates: string[];
    values: number[];
  }>({
    dates: [],
    values: [],
  });
  const [loading, setLoading] = useState(true);
  const { getSourceDataByApiId } = useDataSourceApi();

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const timeParams = config?.timeRange || globalTimeRange;
        let startTime, endTime;
        if (timeParams && typeof timeParams === 'number') {
          endTime = dayjs().valueOf();
          startTime = dayjs().subtract(timeParams, 'minute').valueOf();
        } else if (timeParams && timeParams.start && timeParams.end) {
          startTime = timeParams.start;
          endTime = timeParams.end;
        } else {
          endTime = timeParams[1];
          startTime = timeParams[0];
        }
        const startTimeStr = dayjs(startTime).format('YYYY-MM-DD HH:mm:ss');
        const endTimeStr = dayjs(endTime).format('YYYY-MM-DD HH:mm:ss');
        const data: any = await getSourceDataByApiId(config.dataSource, {
          group_by: config?.groupBy || 'day',
          filters: {
            start_time: startTimeStr,
            end_time: endTimeStr,
          },
        });
        if (Array.isArray(data) && data.length > 0) {
          const dates = data.map((item: any[]) => item[0]);
          const values = data.map((item: any[]) => item[1]);
          setChartData({ dates, values });
        } else {
          setChartData({ dates: [], values: [] });
        }
      } catch (error) {
        console.error('获取趋势数据失败:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [config, globalTimeRange, refreshKey]);

  const option: any = {
    color: [config?.lineColor || '#1890ff'],
    animation: false,
    calculable: true,
    title: { show: false },
    legend: { show: false },
    toolbox: { show: false },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
      },
      enterable: true,
      confine: true,
      extraCssText: 'box-shadow: 0 0 3px rgba(150,150,150, 0.7);',
      textStyle: {
        fontSize: 12,
      },
      formatter: function (params: any) {
        const param = params[0];
        return `
          <div style="padding: 4px 8px;">
            <div style="margin-bottom: 4px; font-weight: bold;">${param.axisValueLabel}</div>
            <div style="display: flex; align-items: center;">
              <span style="display: inline-block; width: 10px; height: 10px; background-color: ${param.color}; border-radius: 50%; margin-right: 6px;"></span>
              <span>${param.seriesName}: ${param.value}</span>
            </div>
          </div>
        `;
      },
    },
    grid: {
      top: 14,
      left: 10,
      right: 20,
      bottom: 10,
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: chartData.dates,
      nameRotate: -90,
      axisLabel: {
        margin: 15,
        textStyle: {
          color: '#666',
        },
      },
      splitLine: {
        lineStyle: {
          color: '#f0f0f0',
        },
      },
    },
    yAxis: {
      type: 'value',
      minInterval: 1,
      axisTick: { show: false },
      axisLine: { show: false },
      axisLabel: {
        formatter: function (value: number) {
          if (value >= 1000) {
            return (value / 1000).toFixed(1) + 'k';
          }
          return value.toString();
        },
        textStyle: {
          color: '#666',
        },
      },
      splitLine: {
        show: true,
        lineStyle: {
          color: '#f0f0f0',
        },
      },
    },
    series: [
      {
        name: '告警数',
        type: 'line',
        data: chartData.values,
        smooth: true,
        symbol: 'circle',
        symbolSize: 6,
        lineStyle: {
          width: 2,
        },
        emphasis: {
          focus: 'series',
        },
      },
    ],
  };

  return (
    <div className="h-full flex flex-col">
      <div className="flex-1">
        {loading ? (
          <div className="h-full flex items-center justify-center">
            <Spin spinning={loading}></Spin>
          </div>
        ) : (
          <ReactEcharts
            option={option}
            style={{ height: '100%', width: '100%' }}
          />
        )}
      </div>
    </div>
  );
};

export default TrendLine;

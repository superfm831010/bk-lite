import React, { useEffect, useState } from 'react';
import ReactEcharts from 'echarts-for-react';
import { Spin } from 'antd';

interface TrendLineProps {
  rawData: any;
  loading?: boolean;
  config?: any;
  onReady?: (ready: boolean) => void;
}

const TrendLine: React.FC<TrendLineProps> = ({
  rawData,
  loading = false,
  config,
  onReady,
}) => {
  const [isDataReady, setIsDataReady] = useState(false);

  const transformData = (rawData: any) => {
    if (Array.isArray(rawData) && rawData.length > 0) {
      const dates = rawData.map((item: any[]) => item[0]);
      const values = rawData.map((item: any[]) => item[1]);
      return { dates, values };
    }
    return { dates: [], values: [] };
  };

  const chartData = transformData(rawData);

  useEffect(() => {
    if (
      chartData &&
      (chartData.dates.length > 0 || chartData.values.length > 0) &&
      !loading
    ) {
      setIsDataReady(true);
      if (onReady) {
        onReady(true);
      }
    } else {
      setIsDataReady(false);
      if (onReady) {
        onReady(false);
      }
    }
  }, [chartData, loading, onReady]);

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
        if (!param) return '';
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
      data: chartData?.dates || [],
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
        data: chartData?.values || [],
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

  if (loading || !isDataReady) {
    return (
      <div className="h-full flex flex-col items-center justify-center">
        <Spin size="small" />
        <div className="text-xs text-gray-500 mt-2">
          {loading ? '数据加载中...' : '暂无数据'}
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      <div className="flex-1">
        <ReactEcharts
          option={option}
          style={{ height: '100%', width: '100%' }}
        />
      </div>
    </div>
  );
};

export default TrendLine;

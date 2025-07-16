import React, { useEffect, useState } from 'react';
import ReactEcharts from 'echarts-for-react';
import { BaseWidgetProps } from '@/app/ops-analysis/types/dashBoard';
import { useDashBoardApi } from '@/app/ops-analysis/api/dashBoard';

const TrendLine: React.FC<BaseWidgetProps> = ({ config, globalTimeRange }) => {
  const [chartData, setChartData] = useState<{
    dates: string[];
    values: number[];
  }>({
    dates: [],
    values: [],
  });
  const [loading, setLoading] = useState(true);
  const { getTrendData } = useDashBoardApi();

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response: any = await getTrendData();
        setChartData(response.data);
      } catch (error) {
        console.error('获取趋势数据失败:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [globalTimeRange]);

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
        type: 'cross', // 交叉指示器
      },
      enterable: true, // 鼠标是否可进入提示框浮层中
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
        name: 'Value',
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
            <div className="text-gray-500">加载中...</div>
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

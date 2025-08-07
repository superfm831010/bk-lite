import React from 'react';
import ReactEcharts from 'echarts-for-react';
import { Spin } from 'antd';
import { BaseWidgetProps } from '@/app/ops-analysis/types/dashBoard';
import { useWidgetData } from '../hooks/useWidgetData';

const OsPie: React.FC<BaseWidgetProps> = ({
  config,
  globalTimeRange,
  refreshKey,
}) => {
  // 数据转换函数：将原始数据转换为饼图需要的格式
  const transformData = (rawData: any) => {
    if (rawData && rawData.data && Array.isArray(rawData.data)) {
      return rawData.data;
    }
    return [];
  };

  const { data: chartData, loading } = useWidgetData({
    config,
    globalTimeRange,
    refreshKey,
    transformData,
  });

  const option: any = {
    animation: true,
    calculable: true,
    title: { show: false },
    tooltip: {
      trigger: 'item',
      enterable: true,
      confine: true,
      extraCssText: 'box-shadow: 0 0 3px rgba(150,150,150, 0.7);',
      textStyle: {
        fontSize: 12,
      },
      formatter: function (params: any) {
        const percent = params.percent || 0;
        return `
          <div style="padding: 4px 8px;">
            <div style="margin-bottom: 4px; font-weight: bold;">${params.seriesName}</div>
            <div style="display: flex; align-items: center;">
              <span style="display: inline-block; width: 10px; height: 10px; background-color: ${params.color}; border-radius: 50%; margin-right: 6px;"></span>
              <span>${params.name}: ${params.value} (${percent.toFixed(1)}%)</span>
            </div>
          </div>
        `;
      },
    },
    legend: {
      top: '3%',
      left: 'center',
      textStyle: {
        color: '#666',
        fontSize: 12,
      },
      itemGap: 20,
    },
    series: [
      {
        name: '操作系统',
        type: 'pie',
        center: ['50%', '56%'],
        radius: ['43%', '65%'],
        avoidLabelOverlap: false,
        label: {
          show: true,
          position: 'center',
          formatter: function () {
            const total = (chartData || []).reduce(
              (sum: number, item: any) => sum + item.value,
              0
            );
            return `{title|总数}\n{value|${total}}`;
          },
          rich: {
            title: {
              fontSize: 14,
              color: '#666',
              lineHeight: 20,
            },
            value: {
              fontSize: 24,
              fontWeight: 'bold',
              color: '#333',
              lineHeight: 32,
            },
          },
        },
        labelLine: {
          show: false,
          length: 10,
          length2: 15,
          smooth: true,
        },
        itemStyle: {
          borderRadius: 4,
          borderColor: '#fff',
          borderWidth: 2,
        },
        data: chartData || [],
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

export default OsPie;

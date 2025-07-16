import React, { useEffect, useState } from 'react';
import ReactEcharts from 'echarts-for-react';
import { BaseWidgetProps } from '@/app/ops-analysis/types/dashBoard';
import { useDashBoardApi } from '@/app/ops-analysis/api/dashBoard';

const OsPie: React.FC<BaseWidgetProps> = ({ globalTimeRange }) => {
  const [chartData, setChartData] = useState<
    Array<{ value: number; name: string }>
  >([]);
  const [loading, setLoading] = useState(true);
  const { getOsData } = useDashBoardApi();

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response: any = await getOsData();
        setChartData(response.data);
      } catch (error) {
        console.error('获取操作系统数据失败:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [globalTimeRange]);

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
        radius: ['38%', '60%'],
        avoidLabelOverlap: false,
        label: {
          show: false,
          position: 'center',
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 24,
            fontWeight: 'bold',
            color: '#333',
          },
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
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
        data: chartData,
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

export default OsPie;

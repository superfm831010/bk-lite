import React from 'react';
import { Spin } from 'antd';
import type { Node } from '@antv/x6';
import ComLine from '../../dashBoard/widgets/comLine';
import ComPie from '../../dashBoard/widgets/comPie';

const componentMap: Record<string, React.ComponentType<any>> = {
  trendLine: ComLine,
  osPie: ComPie,
};

interface ChartNodeProps {
  node: Node;
}

const ChartNode: React.FC<ChartNodeProps> = ({ node }) => {
  const nodeData = node.getData();
  const { widget, chartConfig, config, isLoading, rawData, hasError } =
    nodeData;

  const width = config?.width || 300;
  const height = config?.height || 200;

  const widgetProps = {
    rawData: rawData || null,
    loading: isLoading || false,
    config: {
      lineColor: chartConfig?.lineColor || '#1890ff',
      barColor: chartConfig?.barColor || '#1890ff',
      ...chartConfig,
    },
  };

  const shouldShowLoading = isLoading || (!rawData && !hasError);

  const Component = widget ? componentMap[widget] : null;

  return (
    <div
      style={{
        width: `${width}px`,
        height: `${height}px`,
        border: '1px solid #d9d9d9',
        borderRadius: '6px',
        backgroundColor: '#fff',
        padding: '8px',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <div
        style={{
          flex: 1,
          minHeight: 0,
          position: 'relative',
        }}
      >
        {shouldShowLoading ? (
          <div className="h-full flex flex-col items-center justify-center">
            <Spin size="small" />
            <div className="text-xs text-gray-500 mt-2">
              {hasError ? '数据加载失败' : '图表加载中...'}
            </div>
          </div>
        ) : Component ? (
          <div className="h-full w-full">
            <Component {...widgetProps} />
          </div>
        ) : (
          <div className="h-full flex flex-col items-center justify-center">
            <div className="text-xs text-gray-500">
              未知的组件类型: {widget}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChartNode;

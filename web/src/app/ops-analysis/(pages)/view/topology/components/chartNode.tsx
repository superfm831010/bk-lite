import React from 'react';
import { Spin } from 'antd';
import type { Node } from '@antv/x6';
import { NODE_DEFAULTS } from '../constants/nodeDefaults';
import ComLine from '../../dashBoard/widgets/comLine';
import ComPie from '../../dashBoard/widgets/comPie';
import ComBar from '../../dashBoard/widgets/comBar';

const componentMap: Record<string, React.ComponentType<any>> = {
  line: ComLine,
  pie: ComPie,
  bar: ComBar,
};

interface ChartNodeProps {
  node: Node;
}

const ChartNode: React.FC<ChartNodeProps> = ({ node }) => {
  const nodeData = node.getData();
  const {
    valueConfig,
    config,
    isLoading,
    rawData,
    hasError,
    name: componentName,
  } = nodeData;

  const width = config?.width || NODE_DEFAULTS.CHART_NODE.width;
  const height = config?.height || NODE_DEFAULTS.CHART_NODE.height;

  const widgetProps = {
    rawData: rawData || null,
    loading: isLoading || false,
    config: {
      lineColor: valueConfig?.lineColor || '#1890ff',
      barColor: valueConfig?.barColor || '#1890ff',
      ...valueConfig,
    },
  };

  const shouldShowLoading = isLoading || (!rawData && !hasError);

  const Component = valueConfig.chartType
    ? componentMap[valueConfig.chartType]
    : null;

  return (
    <div
      style={{
        width: `${width}px`,
        height: `${height}px`,
        border: '1px solid var(--color-border-2)',
        borderRadius: '6px',
        backgroundColor: 'var(--color-bg-1)',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {componentName && (
        <div
          style={{
            padding: '12px 12px 0',
            fontSize: '14px',
            color: 'var(--color-text-1)',
          }}
        >
          {componentName}
        </div>
      )}

      <div
        style={{
          flex: 1,
          minHeight: 0,
          position: 'relative',
          padding: '8px',
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
          <div
            className="h-full w-full"
            onClick={(e) => {
              e.stopPropagation();
              e.preventDefault();
            }}
            onMouseDown={(e) => {
              e.stopPropagation();
            }}
          >
            <Component {...widgetProps} />
          </div>
        ) : (
          <div className="h-full flex flex-col items-center justify-center">
            <div className="text-xs text-gray-500">
              未知的组件类型: {valueConfig.chartType}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChartNode;

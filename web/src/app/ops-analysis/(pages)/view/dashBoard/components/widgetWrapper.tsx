import React, { useState, useEffect } from 'react';
import { Spin } from 'antd';
import { BaseWidgetProps } from '@/app/ops-analysis/types/dashBoard';
import { fetchWidgetData } from '../../../../utils/widgetDataTransform';
import { useDataSourceApi } from '@/app/ops-analysis/api/dataSource';
import ComPie from '../widgets/comPie';
import ComLine from '../widgets/comLine';
import ComBar from '../widgets/comBar';

const componentMap: Record<string, React.ComponentType<any>> = {
  line: ComLine,
  pie: ComPie,
  bar: ComBar,
};

interface WidgetWrapperProps extends BaseWidgetProps {
  chartType?: string;
}

const WidgetWrapper: React.FC<WidgetWrapperProps> = ({
  chartType,
  config,
  globalTimeRange,
  refreshKey,
  onReady,
  ...otherProps
}) => {
  const [rawData, setRawData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const { getSourceDataByApiId } = useDataSourceApi();

  const fetchData = async () => {
    if (!config?.dataSource) {
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      const data = await fetchWidgetData({
        config,
        globalTimeRange,
        getSourceDataByApiId,
      });
      setRawData(data);
    } catch (err: any) {
      console.error('获取数据失败:', err);
      setRawData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (config?.dataSource) {
      fetchData();
    }
  }, [config, globalTimeRange, refreshKey]);

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center">
        <Spin spinning={loading}></Spin>
      </div>
    );
  }

  const Component = chartType ? componentMap[chartType] : null;
  if (!Component) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-gray-500">未知的组件类型: {chartType}</div>
      </div>
    );
  }

  return (
    <Component
      rawData={rawData}
      loading={loading}
      config={config}
      globalTimeRange={globalTimeRange}
      refreshKey={refreshKey}
      onReady={onReady}
      {...otherProps}
    />
  );
};

export default WidgetWrapper;

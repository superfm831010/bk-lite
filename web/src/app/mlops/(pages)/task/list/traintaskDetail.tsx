import SimpleLineChart from "@/app/mlops/components/charts/simpleLineChart";
import useMlopsTaskApi from "@/app/mlops/api/task";
import { Button, Spin } from "antd";
import { LeftOutlined } from "@ant-design/icons";
import { useEffect, useState, useRef, useCallback } from "react";

interface TrainTaskDetailProps {
  metricData: any,
  backToList: () => void
}

// 懒加载图表组件
interface LazyChartProps {
  metricName: string;
  runId: string;
  getMetricsDetail: (runId: string, metricsName: string) => Promise<any>;
}

const LazyChart: React.FC<LazyChartProps> = ({ metricName, runId, getMetricsDetail }) => {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const chartRef = useRef<HTMLDivElement>(null);
  const loadingRef = useRef(false);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);
  const enterTimeRef = useRef<number | null>(null);

  // Intersection Observer 实现懒加载
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            // 记录进入视口的时间
            enterTimeRef.current = Date.now();
            
            // 如果正在加载中，不重复发起请求
            if (loadingRef.current) {
              return;
            }

            // 清除之前的延时器
            if (timeoutRef.current) {
              clearTimeout(timeoutRef.current);
            }

            // 延迟执行，给用户滑过去的时间
            timeoutRef.current = setTimeout(() => {
              // 检查是否仍在视口内，且停留时间足够
              const now = Date.now();
              const stayTime = enterTimeRef.current ? now - enterTimeRef.current : 0;
              
              // 只有停留时间超过600ms才加载数据
              if (stayTime >= 600) {
                loadChartData();
              }
            }, 600);
          } else {
            // 离开视口时清除定时器
            if (timeoutRef.current) {
              clearTimeout(timeoutRef.current);
              timeoutRef.current = null;
            }
            enterTimeRef.current = null;
          }
        });
      },
      {
        threshold: 0.1,
        rootMargin: '50px'
      }
    );

    if (chartRef.current) {
      observer.observe(chartRef.current);
    }

    return () => {
      if (chartRef.current) {
        observer.unobserve(chartRef.current);
      }
      // 清理定时器
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  const loadChartData = async () => {
    if (loadingRef.current) return;

    setLoading(true);
    loadingRef.current = true;
    try {
      const detailInfo = await getMetricsDetail(runId, metricName);
      const { metric_history } = detailInfo;
      setData(metric_history);
    } catch (error) {
      console.error(`加载指标 ${metricName} 数据失败:`, error);
      setData([]);
    } finally {
      setLoading(false);
      loadingRef.current = false;
    }
  };

  return (
    <div ref={chartRef} className="w-[400px] mb-6 mx-3 rounded-lg border p-3">
      <div className="mb-3 px-2">
        <h3 className="text-base font-medium text-gray-800 truncate">
          {metricName}
        </h3>
      </div>
      <div className="w-full pr-2 h-[260px]">
        {loading ? (
          <div className="w-full h-full flex items-center justify-center">
            <Spin />
          </div>
        ) : data.length > 0 ? (
          <SimpleLineChart data={data} />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-gray-50">
            <span className="text-sm text-gray-400 text-center px-4">
              暂无数据
            </span>
          </div>
        )}
      </div>
    </div>
  );
};

const TrainTaskDetail = ({
  metricData,
  backToList
}: TrainTaskDetailProps) => {
  const [metrics, setMetricsList] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const { getTrainTaskMetrics, getTrainTaskMetricsDetail } = useMlopsTaskApi();

  // 进入页面时获取指标列表
  useEffect(() => {
    if (metricData?.run_id) {
      getMetricsList();
    }
  }, [metricData?.run_id]);

  const getMetricsList = async () => {
    if (!metricData?.run_id) return;

    setLoading(true);
    try {
      const response = await getTrainTaskMetrics(metricData.run_id);
      if (response?.metrics) {
        setMetricsList(response.metrics);
      }
    } catch (error) {
      console.error('获取指标列表失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const getMetricsDetail = useCallback(async (runId: string, metricsName: string) => {
    const data = await getTrainTaskMetricsDetail(runId, metricsName);
    return data;
  }, [getTrainTaskMetricsDetail]);

  return (
    <>
      <div className="w-full h-full min-h-screen">
        <div className="max-w-7xl mx-auto w-full h-full">
          <div className="mb-6">
            <Button
              variant="link"
              color="default"
              icon={<LeftOutlined />}
              onClick={backToList}
              className="text-gray-600 hover:text-gray-800"
            >
              返回列表
            </Button>
          </div>

          {/* 指标标题 */}
          <div className="mb-6 rounded-lg p-6 ">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              训练指标详情
            </h2>
            {metricData?.run_name && (
              <p className="text-sm text-gray-600">
                任务名称: <span className="font-medium">{metricData.run_name}</span>
              </p>
            )}
            {metricData?.run_id && (
              <p className="text-sm text-gray-600 mt-1">
                任务ID: <span className="font-mono text-xs">{metricData.run_id}</span>
              </p>
            )}
          </div>

          {/* 加载状态 */}
          {loading && (
            <div className="flex w-full h-full items-center justify-center py-16 bg-white rounded-lg shadow-sm">
              <Spin size="large" />
            </div>
          )}

          {/* 指标图表 */}
          {!loading && metrics.length > 0 && (
            <div className="flex flex-wrap gap-6 justify-start items-start">
              {metrics.map((metricName) => (
                <LazyChart
                  key={metricName}
                  metricName={metricName}
                  runId={metricData?.run_id}
                  getMetricsDetail={getMetricsDetail}
                />
              ))}
            </div>
          )}

          {/* 空状态 */}
          {!loading && metrics.length === 0 && (
            <div className="flex flex-col items-center justify-center py-16 bg-white rounded-lg shadow-sm text-gray-500">
              <div className="text-lg mb-2">暂无训练指标</div>
              <div className="text-sm">该任务还没有生成训练指标数据</div>
            </div>
          )}
        </div>
      </div>
    </>
  )
};

export default TrainTaskDetail;
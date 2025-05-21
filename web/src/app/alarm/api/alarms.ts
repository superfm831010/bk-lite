import useApiClient from '@/utils/request';

export const useAlarmApi = () => {
  const { put } = useApiClient();

  // 部分 mock 列表数据
  const mockAlarmData = {
    count: 2,
    items: [
      {
        id: '1',
        level: 'critical',
        updated_at: Date.now(),
        content: 'CPU 使用率过高',
        monitor_instance_name: '实例A',
        source: 'server',
        status: 'dispatched',
        policy: { notice: false },
        operator: 'Alice',
        value: 95,
      },
      {
        id: '2',
        level: 'warning',
        updated_at: Date.now(),
        content: '内存使用率偏高',
        monitor_instance_name: '实例B',
        source: 'vm',
        status: 'dispatched',
        policy: { notice: true },
        operator: 'Bob',
        value: 70,
      },
    ],
  };

  const getAlarmList = async (params: any) => {
    console.log('params', params);
    // TODO: 替换接口 get('/alerts/api/alert/', { params })
    return Promise.resolve(mockAlarmData);
  };

  const getMonitorMetrics = async () => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve([
          { id: 1, name: 'CPU Usage' },
          { id: 2, name: 'Memory Usage' },
          { id: 3, name: 'Disk Space' },
        ]);
      }, 1000);
    });
  };

  const patchMonitorAlert = async (id: string | number | undefined, data: any) => {
    return await put(`/alerts/api/alert_source/${id}/`, data);
  };

  const getMonitorObject = async () => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve([
          { id: 1, name: 'CPU Usage' },
          { id: 2, name: 'Memory Usage' },
          { id: 3, name: 'Disk Space' },
        ]);
      }, 1000);
    });
  };

  return { getAlarmList, getMonitorMetrics, patchMonitorAlert, getMonitorObject };
};

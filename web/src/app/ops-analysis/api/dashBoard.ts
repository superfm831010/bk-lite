export const useDashBoardApi = () => {
  async function getTrendData() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          data: {
            dates: [
              '2025/07/10',
              '2025/07/11',
              '2025/07/12',
              '2025/07/13',
              '2025/07/14',
              '2025/07/15',
              '2025/07/16',
            ],
            values: [45, 120, 85, 200, 160, 180, 220],
          },
        });
      }, 500);
    });
  }

  async function getOsData() {
    // 模拟操作系统分布数据
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          data: [
            { value: 78, name: 'Linux' },
            { value: 30, name: 'Windows' },
            { value: 22, name: 'AIX' },
            { value: 8, name: 'Other' },
          ],
        });
      }, 400);
    });
  }

  async function getInstanceList() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          data: [
            { label: '生产环境-Web服务器-01', value: 'prod-web-01' },
            { label: '生产环境-Web服务器-02', value: 'prod-web-02' },
            { label: '生产环境-数据库服务器-01', value: 'prod-db-01' },
            { label: '测试环境-Web服务器-01', value: 'test-web-01' },
            { label: '测试环境-Web服务器-02', value: 'test-web-02' },
            { label: '开发环境-Web服务器-01', value: 'dev-web-01' },
            { label: '负载均衡器-01', value: 'lb-01' },
            { label: '负载均衡器-02', value: 'lb-02' },
            { label: '缓存服务器-Redis-01', value: 'cache-redis-01' },
            { label: '缓存服务器-Redis-02', value: 'cache-redis-02' },
          ],
        });
      }, 300);
    });
  }

  return {
    getTrendData,
    getOsData,
    getInstanceList,
  };
};

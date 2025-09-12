import { TableDataItem } from '@/app/log/types';
// import { useTranslation } from '@/utils/i18n';
import { v4 as uuidv4 } from 'uuid';

export const usePacketbeatDashboard = () => {
  //   const { t } = useTranslation();

  return {
    name: '内置packetbeat基础视图',
    desc: '',
    id: '1',
    filters: {},
    other: {},
    view_sets: [
      {
        h: 2,
        w: 4,
        x: 0,
        y: 0,
        i: uuidv4(),
        name: '活跃连接数',
        moved: false,
        static: false,
        description: '当前正在活跃的 TCP/UDP 连接数',
        valueConfig: {
          chartType: 'single',
          dataSource: 1,
          getData: (data: TableDataItem) => data[0]?.['active_connections'],
          dataSourceParams: {
            query:
              '{event.dataset="flow", flow.final="false"} | stats count() as active_connections',
          },
        },
      },
      {
        h: 2,
        w: 4,
        x: 8,
        y: 0,
        i: uuidv4(),
        name: '网络总流量',
        moved: false,
        static: false,
        description: '网络总流量（入站 + 出站）字节总和',
        valueConfig: {
          chartType: 'single',
          dataSource: 1,
          getData: (data: TableDataItem) => data[0]?.['total_network_bytes'],
          dataSourceParams: {
            query:
              '{event.dataset="flow"} | stats sum(network.bytes) as total_network_bytes',
          },
        },
      },
      {
        h: 2,
        w: 4,
        x: 4,
        y: 0,
        i: uuidv4(),
        name: 'HTTP 5xx 错误数',
        moved: false,
        static: false,
        description: 'HTTP 5xx 错误总数，用于服务健康监控',
        valueConfig: {
          chartType: 'single',
          dataSource: 1,
          getData: (data: TableDataItem) => data[0]?.['http_5xx_errors'],
          dataSourceParams: {
            query:
              '{event.dataset="http", http.response.status_code=~"5.."} | stats count() as http_5xx_errors',
          },
        },
      },
      {
        h: 3,
        w: 6,
        x: 0,
        y: 2,
        i: uuidv4(),
        name: '网络流量趋势',
        moved: false,
        static: false,
        description: 'HTTP 5xx 错误总数，用于服务健康监控',
        valueConfig: {
          chartType: 'line',
          dataSource: 1,
          dimensions: ['http_5xx_errors'],
          dataSourceParams: {
            query:
              '{event.dataset="http", http.response.status_code=~"5.."} | stats count() as http_5xx_errors',
          },
        },
      },
      {
        h: 3,
        w: 6,
        x: 6,
        y: 2,
        i: uuidv4(),
        name: 'HTTP 请求趋势',
        moved: false,
        static: false,
        description: 'http各个方法的请求数',
        valueConfig: {
          chartType: 'line',
          dataSource: 1,
          dimensions: ['request_count'],
          dataSourceParams: {
            query:
              '{event.dataset="http", http.request.method="GET"} | stats count() as request_count | {event.dataset="http", http.request.method="POST"} | stats count() as request_count',
          },
        },
      },
      {
        h: 4,
        w: 6,
        x: 0,
        y: 5,
        i: uuidv4(),
        name: '网络流量top10',
        moved: false,
        static: false,
        description: '排查主机间流量热点、识别高流量对端或异常流量源',
        valueConfig: {
          chartType: 'table',
          dataSource: 1,
          columns: [
            {
              title: 'source.ip',
              dataIndex: 'source.ip',
              key: 'source.ip',
            },
            {
              title: 'destination.ip',
              dataIndex: 'destination.ip',
              key: 'destination.ip',
            },
            {
              title: 'network.transport',
              dataIndex: 'network.transport',
              key: 'network.transport',
            },
          ],
          dataSourceParams: {
            query:
              '{collect_type="flows"} | json | stats by (source.ip, destination.ip, network.transport) sum(network.bytes) as total_bytes, sum(network.packets) as total_packets | sort by (total_bytes) desc | limit 10',
          },
        },
      },
      {
        h: 4,
        w: 6,
        x: 6,
        y: 5,
        i: uuidv4(),
        name: 'HTTP 服务流量top10',
        moved: false,
        static: false,
        description: 'HTTP 服务负载分析、发现大流量请求的客户端/服务端',
        valueConfig: {
          chartType: 'table',
          dataSource: 1,
          columns: [
            {
              title: 'client.ip',
              dataIndex: 'client.ip',
              key: 'client.ip',
            },
            {
              title: 'server.ip',
              dataIndex: 'server.ip',
              key: 'server.ip',
            },
            {
              title: 'http.request.method',
              dataIndex: 'http.request.method',
              key: 'http.request.method',
            },
          ],
          dataSourceParams: {
            query:
              '{collect_type="http"} | json | stats by (client.ip, server.ip, http.request.method) sum(http.request.bytes) as total_request_bytes,sum(http.response.bytes) as total_response_bytes,count() as request_count | sort by (total_request_bytes) desc | limit 10',
          },
        },
      },
      {
        h: 4,
        w: 6,
        x: 0,
        y: 9,
        i: uuidv4(),
        name: '异常流量日志',
        moved: false,
        static: false,
        description: '大流量连接记录，用于快速发现异常流量或潜在攻击',
        valueConfig: {
          chartType: 'message',
          dataSource: 1,
          columns: [
            {
              title: '_time',
              dataIndex: '_time',
              key: '_time',
            },
            {
              title: 'source.ip',
              dataIndex: 'source.ip',
              key: 'source.ip',
            },
            {
              title: 'destination.ip',
              dataIndex: 'destination.ip',
              key: 'destination.ip',
            },
            {
              title: 'network.transport',
              dataIndex: 'network.transport',
              key: 'network.transport',
            },
            {
              title: 'network.bytes',
              dataIndex: 'network.bytes',
              key: 'network.bytes',
            },
            {
              title: 'network.packets',
              dataIndex: 'network.packets',
              key: 'network.packets',
            },
            {
              title: 'flow.id',
              dataIndex: 'flow.id',
              key: 'flow.id',
            },
          ],
          dataSourceParams: {
            query:
              '{collect_type="flows"} | json | filter network.bytes > 1000000',
          },
        },
      },
      {
        h: 4,
        w: 6,
        x: 6,
        y: 9,
        i: uuidv4(),
        name: 'HTTP 大请求记录',
        moved: false,
        static: false,
        description: '大请求流量 HTTP 请求，用于流量异常分析',
        valueConfig: {
          chartType: 'message',
          dataSource: 1,
          columns: [
            {
              title: '_time',
              dataIndex: '_time',
              key: '_time',
            },
            {
              title: 'client.ip',
              dataIndex: 'client.ip',
              key: 'client.ip',
            },
            {
              title: 'server.ip',
              dataIndex: 'server.ip',
              key: 'server.ip',
            },
            {
              title: 'http.request.method',
              dataIndex: 'http.request.method',
              key: 'http.request.method',
            },
            {
              title: 'http.request.bytes',
              dataIndex: 'http.request.bytes',
              key: 'http.request.bytes',
            },
            {
              title: 'http.response.bytes',
              dataIndex: 'http.response.bytes',
              key: 'http.response.bytes',
            },
            {
              title: 'url.full',
              dataIndex: 'url.full',
              key: 'url.full',
            },
          ],
          dataSourceParams: {
            query:
              '{collect_type="http"}| json | filter http.request.bytes > 10000',
          },
        },
      },
    ],
  };
};

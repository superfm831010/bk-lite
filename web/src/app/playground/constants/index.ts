import { LevelMap } from "@/app/playground/types";

const LEVEL_MAP: LevelMap = {
  critical: '#F43B2C',
  error: '#D97007',
  warning: '#FFAD42',
};

const CONTENT_MAP = {
  'anomaly_detection': {
    bannerTitle: '异常检测',
    bannerInfo: '基于机器学习的智能异常检测服务，能够自动识别时序数据中的异常模式和突变点。支持CSV文件上传，提供实时数据分析和可视化结果，帮助用户快速发现数据中的异常情况。广泛应用于系统监控、质量检测、金融风控、工业设备监控等场景。',
    applicationScenario: [
      {
        title: '系统监控',
        content: '实时监控服务器性能指标、网络流量、应用响应时间等关键指标，及时发现系统异常，确保业务连续性。支持CPU使用率、内存占用、磁盘I/O等多维度监控。'
      },
      {
        title: '工业设备监控',
        content: '对生产线设备的温度、压力、振动等传感器数据进行实时监控，提前预警设备故障风险。通过异常检测算法识别设备性能衰减趋势，实现预测性维护。'
      },
      {
        title: '网络安全',
        content: '分析网络流量模式，识别DDoS攻击、恶意入侵等安全威胁。通过监控网络连接行为、数据传输模式等，及时发现异常访问，保障网络安全。'
      },
      {
        title: '质量检测',
        content: '应用于制造业产品质量控制，检测生产过程中的异常波动。通过分析产品尺寸、重量、成分等关键指标，快速识别不合格产品，提高产品质量。'
      },
    ]
  }
};

export {
  LEVEL_MAP,
  CONTENT_MAP
}
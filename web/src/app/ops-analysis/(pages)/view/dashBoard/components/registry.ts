import { WidgetDefinition } from '@/app/ops-analysis/types/dashBoard';
import OsPie from '../widgets/osPie';
import TrendLine from '../widgets/trendLine';
import {
  OsPieConfig,
  TrendLineConfig,
} from './compConfigs';

export const widgetRegistry: Record<string, WidgetDefinition> = {
  trendLine: {
    meta: {
      id: 'trendLine',
      name: 'Alarm趋势/天',
      description: '按照天的维度对Alarm产生的数量以趋势图的方式呈现',
      icon: 'zhexiantu',
      category: '告警',
      defaultConfig: {
        barColor: '#52c41a',
        filterType: 'selector',
      },
    },
    component: TrendLine,
    configComponent: TrendLineConfig,
  },
  osPie: {
    meta: {
      id: 'osPie',
      name: '操作系统类型占比',
      description: '以操作系统类型的维度对所有主机进行分析',
      icon: 'tubiao2',
      category: '监控',
      defaultConfig: {
        lineColor: '#1890ff',
        filterType: 'selector',
      },
    },
    component: OsPie,
    configComponent: OsPieConfig,
  }
};

export const getWidgetComponent = (widgetType: string) => {
  const definition = widgetRegistry[widgetType];
  return definition?.component || null;
};

export const getWidgetConfig = (widgetType: string) => {
  const definition = widgetRegistry[widgetType];
  return definition?.configComponent || null;
};

export const getWidgetMeta = (widgetType: string) => {
  const definition = widgetRegistry[widgetType];
  return definition?.meta || null;
};

// 获取按分类分组的widgets
export const getWidgetsByCategory = () => {
  const categories: Record<string, any[]> = {};

  Object.values(widgetRegistry).forEach((widget) => {
    const category = widget.meta.category;
    if (!categories[category]) {
      categories[category] = [];
    }
    categories[category].push({
      key: widget.meta.id,
      name: widget.meta.name,
      desc: widget.meta.description,
      icon: widget.meta.icon,
    });
  });

  return categories;
};



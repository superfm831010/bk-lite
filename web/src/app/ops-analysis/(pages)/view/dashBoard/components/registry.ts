import { WidgetDefinition } from '@/app/ops-analysis/types/dashBoard';
import OsPie from '../widgets/osPie';
import TrendLine from '../widgets/trendLine';
import {
  OsPieConfig,
  TrendLineConfig,
} from './formConfigs';

export const widgetRegistry: Record<string, WidgetDefinition> = {
  trendLine: {
    meta: {
      id: 'trendLine',
      name: 'Alarm趋势/天',
      description: '按照天的维度对Alarm产生的数量以趋势图的方式呈现',
      icon: 'zhexiantu',
      category: '告警',
      needsTimeSelector: true,
      needsInstanceSelector: false,
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
      needsTimeSelector: true,
      needsInstanceSelector: false,
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

// 检查是否需要全局时间选择器
export const needsGlobalTimeSelector = (layouts: any[]) => {
  return layouts.some((item) => {
    const meta = getWidgetMeta(item.widget);
    if (!meta?.needsTimeSelector) return false;
    const filterType = item.config?.filterType || meta.defaultConfig?.filterType;
    return filterType === 'selector';
  });
};

// 检查是否需要全局实例选择器
export const needsGlobalInstanceSelector = (layouts: any[]) => {
  return layouts.some((item) => {
    const meta = getWidgetMeta(item.widget);
    if (!meta?.needsInstanceSelector) return false;
    const filterType = item.config?.filterType || meta.defaultConfig?.filterType;
    return filterType === 'selector';
  });
};

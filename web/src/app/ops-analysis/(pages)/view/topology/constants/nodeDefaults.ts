// 节点尺寸配置
export const NODE_DIMENSIONS = {
  ICON_NODE: {
    WIDTH: 100,
    HEIGHT: 100,
  },
  SINGLE_VALUE_NODE: {
    WIDTH: 120,
    HEIGHT: 40,
  },
  TEXT_NODE: {
    WIDTH: 120,
    HEIGHT: 40,
  },
} as const;

// 颜色配置
export const COLORS = {
  // 基础颜色
  PRIMARY: '#1890FF',
  SUCCESS: '#52c41a',
  WARNING: '#fa8c16',
  ERROR: '#ff4d4f',

  // 文本颜色
  TEXT: {
    PRIMARY: '#262626',
    SECONDARY: '#595959',
    DISABLED: '#bfbfbf',
    LIGHT: '#8c8c8c',
  },

  // 背景颜色
  BACKGROUND: {
    WHITE: '#ffffff',
    LIGHT_GRAY: '#f5f5f5',
    GRAY: '#f0f0f0',
    TRANSPARENT: 'transparent',
  },

  // 边框颜色
  BORDER: {
    DEFAULT: '#e0ddddff',
    LIGHT: '#f0f0f0',
    DARK: '#434343',
    PRIMARY: '#1890FF',
  },

  // 端口颜色
  PORT: {
    STROKE: '#1890FF',
    FILL: '#FFFFFF',
  },

  // 边线颜色
  EDGE: {
    DEFAULT: '#a7b5c4',
    SELECTED: '#1890FF',
  },
} as const;

// 字体配置
export const TYPOGRAPHY = {
  FONT_FAMILY: {
    DEFAULT: 'Arial, sans-serif',
    SYSTEM: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
  },

  FONT_SIZE: {
    SMALL: 10,
    DEFAULT: 12,
    MEDIUM: 14,
    LARGE: 16,
    EXTRA_LARGE: 18,

    // 节点特定字体大小
    ICON_LABEL: 12,
    SINGLE_VALUE: 14,
    TEXT_NODE: 14,
  },

  FONT_WEIGHT: {
    NORMAL: 400,
    MEDIUM: 500,
    SEMIBOLD: 600,
    BOLD: 700,
  },
} as const;

// 间距配置
export const SPACING = {
  BORDER_RADIUS: {
    SMALL: 4,
    DEFAULT: 6,
    LARGE: 8,
  },

  STROKE_WIDTH: {
    THIN: 1,
    DEFAULT: 2,
    THICK: 3,
  },

  PORT_RADIUS: 4,

  PADDING: {
    SMALL: 4,
    DEFAULT: 8,
    LARGE: 16,
  },
} as const;

// 节点默认样式配置
export const NODE_DEFAULTS = {
  // 图标节点默认配置
  ICON_NODE: {
    width: NODE_DIMENSIONS.ICON_NODE.WIDTH,
    height: NODE_DIMENSIONS.ICON_NODE.HEIGHT,
    backgroundColor: COLORS.BACKGROUND.WHITE,
    borderColor: COLORS.BORDER.DEFAULT,
    textColor: COLORS.TEXT.PRIMARY,
    fontSize: TYPOGRAPHY.FONT_SIZE.ICON_LABEL,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT.MEDIUM,
    borderRadius: SPACING.BORDER_RADIUS.DEFAULT,
    strokeWidth: SPACING.STROKE_WIDTH.THIN,
    logoType: 'default' as const,
    logoIcon: 'cc-host',
    logoUrl: '',
  },

  // 单值节点默认配置
  SINGLE_VALUE_NODE: {
    width: NODE_DIMENSIONS.SINGLE_VALUE_NODE.WIDTH,
    height: NODE_DIMENSIONS.SINGLE_VALUE_NODE.HEIGHT,
    backgroundColor: COLORS.BACKGROUND.WHITE,
    borderColor: COLORS.BORDER.DEFAULT,
    textColor: COLORS.TEXT.PRIMARY,
    fontSize: TYPOGRAPHY.FONT_SIZE.SINGLE_VALUE,
    fontFamily: TYPOGRAPHY.FONT_FAMILY.DEFAULT,
    borderRadius: SPACING.BORDER_RADIUS.DEFAULT,
    strokeWidth: SPACING.STROKE_WIDTH.THIN,
  },

  // 文本节点默认配置
  TEXT_NODE: {
    width: NODE_DIMENSIONS.TEXT_NODE.WIDTH,
    height: NODE_DIMENSIONS.TEXT_NODE.HEIGHT,
    backgroundColor: COLORS.BACKGROUND.TRANSPARENT,
    borderColor: COLORS.BACKGROUND.TRANSPARENT,
    textColor: COLORS.TEXT.PRIMARY,
    fontSize: TYPOGRAPHY.FONT_SIZE.TEXT_NODE,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT.NORMAL,
    strokeWidth: SPACING.STROKE_WIDTH.THIN,
  },

  // 图表节点默认配置
  CHART_NODE: {
    width: 400,
    height: 220,
    backgroundColor: COLORS.BACKGROUND.WHITE,
    borderColor: COLORS.BORDER.DEFAULT,
    textColor: COLORS.TEXT.PRIMARY,
    fontSize: TYPOGRAPHY.FONT_SIZE.ICON_LABEL,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT.MEDIUM,
    borderRadius: SPACING.BORDER_RADIUS.DEFAULT,
    strokeWidth: SPACING.STROKE_WIDTH.THIN,
  },

  // 基础图形节点默认配置
  BASIC_SHAPE_NODE: {
    width: 120,
    height: 80,
    backgroundColor: COLORS.BACKGROUND.WHITE,
    borderColor: COLORS.BORDER.DEFAULT,
    borderWidth: SPACING.STROKE_WIDTH.DEFAULT,
    lineType: 'solid' as const,
    shapeType: 'rectangle' as const,
    textColor: COLORS.TEXT.PRIMARY,
    fontSize: TYPOGRAPHY.FONT_SIZE.DEFAULT,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT.NORMAL,
    borderRadius: SPACING.BORDER_RADIUS.DEFAULT,
  },
} as const;

// 端口默认配置
export const PORT_DEFAULTS = {
  RADIUS: SPACING.PORT_RADIUS,
  STROKE_COLOR: COLORS.PORT.STROKE,
  FILL_COLOR: COLORS.PORT.FILL,
  OPACITY: {
    HIDDEN: 0,
    VISIBLE: 1,
  },
  MAGNET: true,
} as const;



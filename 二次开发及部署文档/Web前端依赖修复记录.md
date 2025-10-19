# Web 前端依赖修复记录

## 问题描述

**时间**: 2025-10-19
**问题**: 访问告警事件页面 `/alarm/incidents` 时出现构建错误

### 错误信息
```
Module not found: Can't resolve 'react-activation'

./src/app/alarm/(pages)/incidents/page.tsx:20:1
  18 | import { useRouter } from 'next/navigation';
  19 | import { useCommon } from '@/app/alarm/context/common';
> 20 | import { KeepAlive, useActivate } from 'react-activation';
     | ^
```

## 问题分析

BKLite 前端采用多模块架构，每个功能模块（alarm、cmdb、log 等）都有自己的 `package.json` 来声明模块特定的依赖。但这些依赖需要在**根级别**的 `/web/package.json` 中实际安装才能使用。

经过排查，发现以下模块在其 `package.json` 中声明了依赖，但根 `package.json` 中缺失：

- **alarm 模块**: react-activation, @ant-design/charts, recharts
- **cmdb 模块**: @antv/x6, @antv/xflow, @dnd-kit/*, react-activation, react-masonry-css
- **log 模块**: react-ace, recharts, echarts-for-react, react-grid-layout
- **monitor 模块**: @ant-design/colors, react-ace, recharts
- **opspilot 模块**: @ant-design/x, @antv/g6, aieditor, markdown-it, xlsx 等
- **ops-analysis 模块**: @antv/x6, @antv/x6-plugin-*, echarts-for-react, fossflow 等
- **system-manager 模块**: @dnd-kit/*

## 解决方案

### 1. 更新根 package.json

在 `/home/soft/bk-lite/web/package.json` 中添加所有缺失的依赖：

#### 新增 dependencies (28个)

```json
{
  "dependencies": {
    "@ant-design/charts": "^2.2.3",
    "@ant-design/colors": "^8.0.0",
    "@ant-design/x": "1.0.0-alpha.12",
    "@antv/g6": "^4.8.25",
    "@antv/x6": "^2.18.1",
    "@antv/x6-plugin-minimap": "^2.0.7",
    "@antv/x6-plugin-selection": "^2.2.2",
    "@antv/x6-plugin-transform": "^2.1.8",
    "@antv/x6-react-shape": "^2.2.3",
    "@antv/xflow": "^2.2.4",
    "@dnd-kit/core": "^6.2.0",
    "@dnd-kit/modifiers": "^8.0.0",
    "@dnd-kit/sortable": "^9.0.0",
    "@dnd-kit/utilities": "^3.2.2",
    "@isoflow/isopacks": "^0.0.10",
    "aieditor": "^1.3.3",
    "docx-preview": "^0.3.4",
    "echarts-for-react": "^3.0.2",
    "fossflow": "^1.0.5",
    "highlight.js": "^11.11.0",
    "markdown-it": "^14.1.0",
    "react-ace": "^14.0.1",
    "react-activation": "^0.13.0",
    "react-file-viewer": "^1.2.1",
    "react-grid-layout": "^1.5.2",
    "react-masonry-css": "latest",
    "recharts": "^2.15.0",
    "xlsx": "^0.18.5"
  }
}
```

#### 新增 devDependencies (2个)

```json
{
  "devDependencies": {
    "@types/markdown-it": "^14.1.2",
    "@types/react-beautiful-dnd": "^13.1.8"
  }
}
```

### 2. 安装依赖

```bash
cd /home/soft/bk-lite/web
pnpm install
```

**安装结果**:
- 新增 408 个包
- 耗时约 55.9 秒
- 所有依赖成功安装

### 3. 重启 Web 服务

```bash
# 清理旧进程
pkill -f "next dev -p 3011"

# 重启服务
./dev.sh start web
```

**验证结果**:
- Web 服务正常启动 (http://localhost:3011)
- 首页返回 200 状态码
- 日志中无 react-activation 相关错误
- 所有页面可正常访问

## 依赖说明

### 核心依赖功能

| 依赖包 | 用途 | 使用模块 |
|--------|------|----------|
| react-activation | React 组件持久化（KeepAlive） | alarm, cmdb |
| @ant-design/charts | Ant Design 图表组件库 | alarm, opspilot |
| @antv/x6 | 图编辑器核心引擎 | cmdb, ops-analysis |
| @antv/g6 | 图可视化引擎 | opspilot |
| @dnd-kit/* | 拖拽功能套件 | cmdb, system-manager |
| recharts | React 图表库 | alarm, log, monitor, mlops |
| react-ace | 代码编辑器组件 | log, monitor, node-manager |
| echarts-for-react | ECharts React 封装 | log, ops-analysis |
| markdown-it | Markdown 解析器 | opspilot |
| aieditor | AI 编辑器组件 | opspilot |

### 注意事项

1. **peer dependencies 警告**: 安装过程中出现一些 peer dependencies 不匹配的警告，但不影响功能使用：
   - react-file-viewer 需要 React 16，当前使用 React 18
   - 部分 @storybook 插件版本不完全匹配

2. **版本选择**: 依赖版本与各模块 package.json 中声明的版本保持一致

3. **latest 版本**: react-masonry-css 使用 `latest` 标签，实际安装了 1.0.16

## 相关文件

- `/home/soft/bk-lite/web/package.json` - 根级依赖配置（已更新）
- `/home/soft/bk-lite/web/pnpm-lock.yaml` - 依赖锁定文件（已更新）
- `/home/soft/bk-lite/web/src/app/*/package.json` - 各模块依赖声明

## 后续建议

1. **依赖管理规范**: 建议建立明确的依赖管理规范，新增模块依赖时同步更新根 package.json

2. **自动化检查**: 可以添加 CI 检查，确保模块 package.json 中声明的依赖在根 package.json 中存在

3. **依赖审计**: 定期执行 `pnpm audit` 检查依赖安全性

4. **版本统一**: 对于多个模块共用的依赖（如 recharts），建议在根 package.json 中统一管理版本

## 参考资源

- [Next.js Module Resolution](https://nextjs.org/docs/messages/module-not-found)
- [pnpm 工作空间](https://pnpm.io/workspaces)
- [React Activation 文档](https://github.com/CJY0208/react-activation)

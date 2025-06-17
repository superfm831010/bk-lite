# BK-Lite Web 项目代码架构

## 项目概述

BK-Lite Web 是一个基于 Next.js 14 的企业级 IT 运维管理平台前端项目，采用 TypeScript 开发，集成了多个业务模块，包括资产管理、监控集成、节点管理、运维助手等核心功能。

## 技术栈

### 核心框架
- **Next.js 14.2.25** - React全栈框架，支持App Router
- **React 18.2.0** - UI框架
- **TypeScript 5** - 类型安全的JavaScript

### UI组件库
- **Ant Design 5.21.5** - 企业级UI组件库
- **Tailwind CSS 3.4.1** - 原子化CSS框架
- **Sass 1.81.0** - CSS预处理器

### 状态管理与数据处理
- **React Context** - 全局状态管理
- **Next-Auth 4.24.10** - 身份认证
- **Axios 1.7.7** - HTTP客户端
- **React-Intl 7.0.1** - 国际化支持

### 开发工具
- **Storybook 8.4.6** - 组件开发和文档
- **ESLint** - 代码规范检查
- **pnpm** - 包管理器

## 项目结构

```
src/
├── app/                          # Next.js App Router 路由目录
│   ├── layout.tsx               # 根布局组件
│   ├── page.tsx                 # 首页
│   ├── not-found.tsx           # 404页面
│   ├── (core)/                 # 核心功能模块
│   ├── cmdb/                   # 配置管理数据库模块
│   ├── monitor/                # 监控模块
│   ├── node-manager/           # 节点管理模块
│   ├── ops-console/            # 运维控制台
│   ├── opspilot/               # 运维助手模块
│   └── system-manager/         # 系统管理模块
├── components/                  # 公共组件库
│   ├── custom-table/           # 自定义表格组件
│   ├── dynamic-form/           # 动态表单组件
│   ├── page-layout/            # 页面布局组件
│   ├── permission/             # 权限控制组件
│   ├── top-menu/               # 顶部菜单组件
│   └── ...                     # 其他通用组件
├── context/                     # React Context 状态管理
│   ├── auth.tsx                # 认证状态
│   ├── locale.tsx              # 国际化状态
│   ├── theme.tsx               # 主题状态
│   ├── menus.tsx               # 菜单状态
│   ├── permissions.tsx         # 权限状态
│   └── userInfo.tsx            # 用户信息状态
├── hooks/                       # 自定义Hooks
│   ├── useLocalizedTime.ts     # 本地化时间Hook
│   ├── usePermissions.ts       # 权限Hook
│   └── useRedirectFirstChild.ts # 重定向Hook
├── lib/                         # 工具库
│   ├── auth.ts                 # 认证相关工具
│   └── wechatProvider.ts       # 微信登录提供者
├── locales/                     # 国际化文件
│   ├── en.json                 # 英文语言包
│   └── zh.json                 # 中文语言包
├── types/                       # TypeScript 类型定义
├── utils/                       # 工具函数
└── styles/                      # 全局样式
    └── globals.css             # 全局CSS样式
```

## 架构设计模式

### 1. 模块化架构
项目采用模块化设计，每个业务模块独立管理：

```typescript
// 模块结构示例 (以monitor模块为例)
app/monitor/
├── (pages)/                    # 页面组件
│   ├── intergration/          # 集成管理页面
│   └── ...
├── api/                       # API接口层
├── components/                # 模块专用组件
├── constants/                 # 模块常量
├── context/                   # 模块状态管理
├── hooks/                     # 模块专用Hooks
├── types/                     # 模块类型定义
└── utils/                     # 模块工具函数
```

### 2. 分层架构

#### 表现层 (Presentation Layer)
- **页面组件**: 负责UI渲染和用户交互
- **布局组件**: 提供页面结构和导航
- **通用组件**: 可复用的UI组件

#### 业务逻辑层 (Business Logic Layer)
- **自定义Hooks**: 封装业务逻辑和状态管理
- **Context Providers**: 全局状态管理
- **工具函数**: 业务相关的纯函数

#### 数据访问层 (Data Access Layer)
- **API客户端**: HTTP请求封装
- **类型定义**: 数据模型和接口定义

### 3. 权限控制架构

```typescript
// 权限控制流程
app/layout.tsx → PermissionsProvider → 权限验证 → 页面渲染

// 权限组件示例
<Permission requiredPermissions={['Setting']}>
  <Button>设置</Button>
</Permission>
```

### 4. 国际化架构

```typescript
// 国际化支持
LocaleProvider → React-Intl → 多语言渲染

// 使用示例
const { t } = useTranslation();
const title = t('common.title');
```

## 核心功能模块

### 1. CMDB (配置管理数据库)
- **资产管理**: 设备、软件资产的生命周期管理
- **自动发现**: 网络设备和服务的自动发现
- **关系映射**: 资产间的依赖关系管理

### 2. Monitor (监控模块)
- **集成管理**: 第三方监控工具集成
- **指标配置**: 监控指标的配置和管理
- **告警处理**: 告警规则和通知管理

### 3. Node Manager (节点管理)
- **云区域管理**: 多云环境的统一管理
- **采集器管理**: 数据采集器的部署和配置
- **节点监控**: 节点状态和性能监控

### 4. OpsPilot (运维助手)
- **智能问答**: AI驱动的运维问题解答
- **工具集成**: 常用运维工具的集成
- **知识库**: 运维知识的存储和检索

### 5. System Manager (系统管理)
- **用户管理**: 用户账户和角色管理
- **权限控制**: 细粒度的权限配置
- **应用管理**: 系统应用的配置和管理

## 状态管理策略

### Global State (全局状态)
使用React Context管理全局状态：

```typescript
// 认证状态
interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
}

// 用户信息状态
interface UserInfoContextType {
  loading: boolean;
  roles: string[];
  groups: Group[];
  selectedGroup: Group | null;
  setSelectedGroup: (group: Group) => void;
}
```

### Local State (本地状态)
页面级状态使用React Hooks管理：

```typescript
// 表格数据状态
const [tableData, setTableData] = useState<TableDataItem[]>([]);
const [pagination, setPagination] = useState<Pagination>({
  current: 1,
  total: 0,
  pageSize: 20,
});
```

## 组件设计原则

### 1. 可复用性
组件设计遵循单一职责原则，提高复用性：

```typescript
// 通用表格组件
interface CustomTableProps<T> {
  columns: ColumnItem[];
  dataSource: T[];
  pagination?: Pagination;
  loading?: boolean;
  onPageChange?: (page: number, pageSize: number) => void;
}
```

### 2. 类型安全
严格的TypeScript类型定义：

```typescript
// 监控类型定义
export interface MonitorItem {
  id: number;
  name: string;
  type: 'host' | 'service' | 'application';
  status: 'active' | 'inactive' | 'error';
  metrics: MetricItem[];
}
```

### 3. 配置驱动
使用配置对象驱动组件行为：

```typescript
// 动态表单配置
interface FormConfig {
  fields: FormFieldConfig[];
  layout: 'horizontal' | 'vertical';
  validation: ValidationRules;
}
```

## API设计模式

### 1. 统一的HTTP客户端
```typescript
// API客户端封装
const useApiClient = () => {
  const { get, post, put, del } = useHttpClient();
  
  return {
    get: (url: string, params?: any) => get(url, params),
    post: (url: string, data?: any) => post(url, data),
    put: (url: string, data?: any) => put(url, data),
    delete: (url: string) => del(url),
    isLoading: boolean
  };
};
```

### 2. 模块化API接口
```typescript
// 监控API示例
const useMonitorApi = () => {
  const { get, post } = useApiClient();
  
  return {
    getMonitorList: (params: QueryParams) => get('/monitor/list', params),
    createMonitor: (data: CreateMonitorData) => post('/monitor/create', data),
    updateMonitor: (id: string, data: UpdateMonitorData) => 
      put(`/monitor/${id}`, data)
  };
};
```

## 性能优化策略

### 1. 代码分割
- 使用Next.js动态导入实现路由级代码分割
- 组件级懒加载减少初始包大小

### 2. 数据获取优化
- 使用SWR或React Query缓存API请求
- 实现分页和虚拟滚动处理大数据集

### 3. 构建优化
- 使用Bundle Analyzer分析包大小
- 配置Webpack优化构建产物

## 开发规范

### 1. 代码规范
- 使用ESLint和Prettier保证代码质量
- 遵循TypeScript严格模式
- 使用Husky进行Git提交前检查

### 2. 组件规范
- 组件文件使用PascalCase命名
- Props接口以组件名+Props结尾
- 导出方式统一使用default export

### 3. 样式规范
- 优先使用Tailwind CSS类名
- 复杂样式使用CSS Modules
- 保持样式与组件的就近原则

## 测试策略

### 1. 组件测试
使用Storybook进行组件开发和测试：

```typescript
// 组件Story示例
export default {
  title: 'Components/CustomTable',
  component: CustomTable,
  parameters: {
    docs: {
      description: {
        component: '自定义表格组件，支持分页、排序、筛选等功能'
      }
    }
  }
} as Meta;
```

### 2. 类型检查
使用TypeScript进行编译时类型检查：

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "noImplicitReturns": true
  }
}
```

## 部署架构

### 1. 构建配置
```javascript
// next.config.mjs
const nextConfig = {
  reactStrictMode: true,
  sassOptions: {
    implementation: 'sass-embedded',
  },
  staticPageGenerationTimeout: 300
};
```

### 2. 环境配置
- 开发环境：支持热重载和调试工具
- 生产环境：优化构建和性能监控
- 容器化部署：Docker镜像和Kubernetes配置

## 安全考虑

### 1. 认证授权
- JWT Token管理
- 路由级权限控制
- API接口鉴权

### 2. 数据安全
- 输入验证和XSS防护
- CSRF保护
- 敏感数据加密传输

这个架构设计确保了项目的可维护性、可扩展性和性能，为企业级IT运维管理提供了坚实的技术基础。
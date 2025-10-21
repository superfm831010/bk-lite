# BKLite API 接口架构分析报告

## 执行摘要

BKLite 项目采用 **Django REST Framework (DRF)** 架构，基于模块化的 ViewSet 设计模式，提供了超过 120 个注册路由。系统支持多种认证方式，包括 Token 认证、API 密钥认证和 Session 认证。

---

## 1. API 整体架构

### 1.1 核心技术栈

| 技术组件 | 版本/说明 |
|--------|---------|
| 框架 | Django REST Framework (DRF) |
| 基础框架 | Django 4.2 |
| 认证方式 | Token + API Secret + Session |
| API 文档 | CoreAPI AutoSchema (无 Swagger/OpenAPI 配置) |
| 分页方式 | 自定义 PageNumberPagination |
| 响应格式 | 统一的自定义 JSON 格式 |

### 1.2 主要文件位置

```
/home/user/bk-lite/server/
├── urls.py                              # 主 URL 配置 (动态路由加载)
├── settings.py                          # Django 设置入口
├── config/
│   ├── default.py                       # 配置集合入口
│   ├── components/
│   │   ├── app.py                       # 应用配置 (INSTALLED_APPS, MIDDLEWARE)
│   │   └── drf.py                       # DRF 配置
│   ├── drf/
│   │   ├── viewsets.py                  # 自定义 ModelViewSet
│   │   ├── pagination.py                # 自定义分页器
│   │   ├── renderers.py                 # 自定义响应渲染器
│   │   └── filters.py                   # 自定义过滤器
│   └── context_processors/
└── apps/
    ├── base/                            # 基础应用 (用户模型)
    ├── core/                            # 核心应用
    │   ├── backends.py                  # 认证后端
    │   ├── decorators/api_permission.py # 权限装饰器
    │   └── middlewares/                 # 中间件
    └── [其他应用]/
        └── urls.py                      # 应用级 URL 配置
```

---

## 2. API 路由配置

### 2.1 动态路由加载机制

**文件**: `/home/user/bk-lite/server/urls.py`

```python
# 主 URL 配置采用动态加载，所有 apps.* 应用的 urls.py 自动注册
for app_config in apps.get_app_configs():
    app_name = app_config.name
    if app_name.startswith("apps."):
        # 动态导入 urls.py
        urls_module = __import__(f"{app_name}.urls", fromlist=["urlpatterns"])
        url_path = app_name.split("apps.")[-1]
        # 统一前缀: /api/v1/{app_name}/
        urlpatterns.append(path(f"api/v1/{url_path}/", include(urls_module)))
```

**API 版本控制**: `/api/v1/`

**关键点**:
- 所有应用的路由自动注册到 `/api/v1/{app_name}/` 下
- 应用名称从 `apps.` 后开始提取

### 2.2 已注册应用及其 API 端点 (120+ 个注册)

#### 2.2.1 核心应用 (Core)

**路由前缀**: `/api/v1/core/`

**登录相关接口** (`apps/core/urls.py`):
```
POST   /api/login/                    # 用户登录
POST   /api/bk_lite_login/            # BK Lite 域登录
GET    /api/get_domain_list/          # 获取域名列表
GET    /api/get_wechat_settings/      # 获取微信设置
GET    /api/get_bk_settings/          # 获取 BK 设置
POST   /api/wechat_user_register/     # 微信用户注册
POST   /api/generate_qr_code/         # 生成二维码
POST   /api/verify_otp_code/          # 验证 OTP 码
POST   /api/reset_pwd/                # 重置密码
GET    /api/login_info/               # 获取登录信息
GET    /api/get_client/               # 获取客户端信息
GET    /api/get_my_client/            # 获取我的客户端
GET    /api/get_client_detail/        # 获取客户端详情
GET    /api/get_user_menus/           # 获取用户菜单
GET    /api/get_all_groups/           # 获取所有分组
```

**用户分组管理** (ViewSet):
```
GET    /user_group/                   # 列表
POST   /user_group/                   # 创建
GET    /user_group/{id}/              # 详情
PUT    /user_group/{id}/              # 更新
DELETE /user_group/{id}/              # 删除
```

**认证豁免路径**:
- `/swagger/`
- `/admin/`
- `/accounts/`

#### 2.2.2 系统管理应用 (System Management)

**路由前缀**: `/api/v1/system_mgmt/`

**ViewSet 注册** (`apps/system_mgmt/urls.py`):
```
group                    # 用户组管理
user                     # 用户管理
role                     # 角色管理
channel                  # 渠道管理
group_data_rule          # 组数据规则
system_settings          # 系统设置
app                      # 应用管理
login_module             # 登录模块
```

**示例端点**:
```
GET    /api/v1/system_mgmt/user/                # 用户列表
POST   /api/v1/system_mgmt/user/                # 创建用户
GET    /api/v1/system_mgmt/user/{id}/           # 用户详情
PUT    /api/v1/system_mgmt/user/{id}/           # 更新用户
DELETE /api/v1/system_mgmt/user/{id}/           # 删除用户
GET    /api/v1/system_mgmt/user/search_user_list/  # 搜索用户
GET    /api/v1/system_mgmt/user/user_all/      # 获取所有用户
GET    /api/v1/system_mgmt/user/get_user_detail/   # 获取用户详情
```

#### 2.2.3 节点管理应用 (Node Management)

**路由前缀**: `/api/v1/node_mgmt/`

**ViewSet 注册** (`apps/node_mgmt/urls.py`):
```
api/node                         # 节点管理
api/cloud_region                 # 云区域
api/sidecar_env                  # Sidecar 环境变量
api/collector                    # 采集器
api/controller                   # 控制器
api/configuration                # 采集配置
api/child_config                 # 子配置
api/installer                    # 安装程序
api/package                      # 包管理
open_api                         # 开放 API (特殊路由)
```

**特殊说明**: `open_api` 使用 `trailing_slash=False` 配置

#### 2.2.4 CMDB 应用 (Configuration Management Database)

**路由前缀**: `/api/v1/cmdb/`

**ViewSet 注册** (`apps/cmdb/urls.py`):
```
api/classification       # 分类管理
api/model                # 模型管理
api/instance             # 实例管理
api/change_record        # 变更记录
api/collect              # 采集模型
api/oid                  # OID 管理
```

#### 2.2.5 监控应用 (Monitor)

**路由前缀**: `/api/v1/monitor/`

**ViewSet 注册** (`apps/monitor/urls.py`, 共 14 个):
```
api/monitor_object                      # 监控对象
api/metrics_group                       # 指标组
api/metrics                             # 指标
api/metrics_instance                    # 指标实例
api/organization_rule                   # 组织规则
api/monitor_instance                    # 监控实例
api/monitor_policy                      # 监控策略
api/monitor_plugin                      # 监控插件
api/monitor_alert                       # 监控告警
api/monitor_event                       # 监控事件
api/monitor_alert_metric_snapshot       # 告警指标快照
api/system_mgmt                         # 系统管理
api/node_mgmt                           # 节点管理
```

#### 2.2.6 告警应用 (Alerts)

**路由前缀**: `/api/v1/alerts/`

**API 端点** (`apps/alerts/urls.py`):
```
GET/POST  /api/test/                          # 测试端点
POST      /api/receiver_data/                 # 接收告警数据

ViewSet 注册:
api/alert_source                        # 告警源
api/alerts                              # 告警
api/events                              # 事件
api/level                               # 告警级别
api/settings                            # 系统设置
api/assignment                          # 告警分配
api/shield                              # 告警屏蔽
api/incident                            # 事件
api/correlation_rule                    # 关联规则
api/aggregation_rule                    # 聚合规则
api/log                                 # 日志
```

**特点**: 支持 Webhook 告警接收 (`/api/receiver_data/`)

#### 2.2.7 日志应用 (Log)

**路由前缀**: `/api/v1/log/`

**ViewSet 注册** (`apps/log/urls.py`):
```
collect_types            # 采集类型
collect_instances        # 采集实例
collect_configs          # 采集配置
node_mgmt                # 节点管理
log_group                # 日志分组
search                   # 日志搜索
search_conditions        # 搜索条件
policy                   # 策略
alert                    # 告警
event                    # 事件
event_raw_data           # 原始数据
system_mgmt              # 系统管理
```

#### 2.2.8 OpsPilot 应用 (AI 助手)

**路由前缀**: `/api/v1/opspilot/`

**主要模块** (`apps/opspilot/urls.py`):
- 模型提供商管理 (Model Provider)
- 机器人管理 (Bot Management)
- 渠道管理 (Channel Management)
- 知识管理 (Knowledge Management)
- 配额规则管理 (Quota Rule)

**模型提供商**:
```
model_provider_mgmt/embed_provider      # 嵌入模型提供商
model_provider_mgmt/rerank_provider     # 重排序提供商
model_provider_mgmt/ocr_provider        # OCR 提供商
model_provider_mgmt/llm                 # LLM 模型
model_provider_mgmt/rule                # 规则
model_provider_mgmt/llm_model           # LLM 模型管理
model_provider_mgmt/skill_tools         # 技能工具
model_provider_mgmt/skill_log           # 技能日志
model_provider_mgmt/model_type          # 模型类型
```

**机器人管理**:
```
bot_mgmt/bot                            # 机器人
bot_mgmt/rasa_model                     # Rasa 模型
bot_mgmt/history                        # 对话历史
bot_mgmt/workflow_task_result           # 工作流任务结果

bot_mgmt/bot/{bot_id}/get_detail/       # 获取机器人详情
bot_mgmt/rasa_model_download/           # 下载 Rasa 模型
bot_mgmt/skill_execute/                 # 执行技能
bot_mgmt/v1/chat/completions            # OpenAI 兼容端点
bot_mgmt/lobe_chat/v1/chat/completions  # Lobe Chat 端点
bot_mgmt/get_active_users_line_data/    # 活跃用户统计
bot_mgmt/get_conversations_line_data/   # 对话统计
bot_mgmt/get_total_token_consumption/   # 总 Token 消耗
bot_mgmt/get_token_consumption_overview/ # Token 消耗概览
bot_mgmt/execute_chat_flow/{bot_id}/{node_id}/  # 执行对话流
```

**知识管理**:
```
knowledge_mgmt/knowledge_base            # 知识库
knowledge_mgmt/file_knowledge            # 文件知识
knowledge_mgmt/knowledge_document        # 知识文档
knowledge_mgmt/web_page_knowledge        # 网页知识
knowledge_mgmt/manual_knowledge          # 手动知识
knowledge_mgmt/qa_pairs                  # QA 对
knowledge_mgmt/knowledge_graph           # 知识图谱
```

#### 2.2.9 MLOps 应用

**路由前缀**: `/api/v1/mlops/`

**功能模块**:
```
异常检测 (Anomaly Detection):
- anomaly_detection_datasets
- anomaly_detection_train_data
- anomaly_detection_train_jobs
- anomaly_detection_servings

时间序列预测 (TimeSeries Predict):
- timeseries_predict_datasets
- timeseries_predict_train_data
- timeseries_predict_train_jobs
- timeseries_predict_train_history
- timeseries_predict_servings

日志聚类 (Log Clustering):
- log_clustering_datasets
- log_clustering_train_data
- log_clustering_train_jobs
- log_clustering_train_history
- log_clustering_servings

Rasa 管理:
- rasa_datasets
- rasa_intent
- rasa_response
- rasa_rule
- rasa_story
- rasa_entity
- rasa_slot
- rasa_form
- rasa_action
- rasa_pipelines
```

#### 2.2.10 API 密钥管理 (Base App)

**路由前缀**: `/api/v1/base/`

**端点** (`apps/base/urls.py`):
```
POST   /api/v1/base/user_api_secret/             # 创建 API 密钥
GET    /api/v1/base/user_api_secret/             # 列表 API 密钥
POST   /api/v1/base/user_api_secret/generate_api_secret/  # 生成 API 密钥
DELETE /api/v1/base/user_api_secret/{id}/        # 删除 API 密钥
```

---

## 3. 认证机制

### 3.1 认证架构

**文件**: `/home/user/bk-lite/server/config/components/app.py`

```python
AUTHENTICATION_BACKENDS = (
    "apps.core.backends.AuthBackend",           # 标准 Token 认证
    "apps.core.backends.APISecretAuthBackend",  # API 密钥认证
    "django.contrib.auth.backends.ModelBackend", # Django 默认认证
)

# DRF 配置
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        # BasicAuthentication 已注释
    ],
}

# 认证令牌头部配置
AUTH_TOKEN_HEADER_NAME = "HTTP_AUTHORIZATION"
API_TOKEN_HEADER_NAME = "HTTP_API_AUTHORIZATION"
```

### 3.2 认证后端详解

#### 3.2.1 标准 Token 认证 (AuthBackend)

**文件**: `/home/user/bk-lite/server/apps/core/backends.py`

```python
class AuthBackend(ModelBackend):
    def authenticate(self, request=None, username=None, password=None, token=None):
        """使用 token 进行用户认证"""
        if not token:
            return None
        
        # 1. 通过 SystemMgmt RPC 验证 token
        result = self._verify_token_with_system_mgmt(token)
        
        # 2. 获取用户信息
        user_info = result.get("data")
        
        # 3. 处理用户 locale
        self._handle_user_locale(user_info)
        
        # 4. 获取用户权限规则
        rules = self._get_user_rules(request, user_info)
        
        # 5. 设置用户信息
        return self.set_user_info(request, user_info, rules)
```

**用户属性设置**:
```python
user.email = user_info.get("email", "")
user.is_superuser = is_superuser
user.is_staff = user.is_superuser
user.is_active = True
user.group_list = user_info.get("group_list", [])
user.roles = user_info.get("roles", [])
user.locale = user_info.get("locale", DEFAULT_LOCALE)
user.rules = rules                              # 运行时属性
user.permission = {key: set(value) for ...}   # 运行时属性
user.role_ids = user_info.get("role_ids", [])
user.display_name = user_info.get("display_name", "")
user.group_tree = user_info.get("group_tree", [])
```

#### 3.2.2 API 密钥认证 (APISecretAuthBackend)

**文件**: `/home/user/bk-lite/server/apps/core/backends.py`

```python
class APISecretAuthBackend(ModelBackend):
    def authenticate(self, request=None, username=None, password=None, api_token=None):
        """使用 API token 进行用户认证"""
        if not api_token:
            return None
        
        # 1. 查询数据库 UserAPISecret 表
        user_secret = UserAPISecret.objects.filter(api_secret=api_token).first()
        
        # 2. 获取关联用户
        user = User.objects.get(username=user_secret.username)
        
        # 3. 设置用户分组
        user.group_list = [user_secret.team]
        
        return user
```

**模型定义** (`apps/base/models/user.py`):
```python
class UserAPISecret(TimeInfo):
    username = models.CharField(max_length=255)
    api_secret = models.CharField(max_length=64)
    team = models.IntegerField(default=0)
    
    @staticmethod
    def generate_api_secret():
        return binascii.hexlify(os.urandom(32)).decode()  # 64 字符十六进制
    
    class Meta:
        unique_together = ("username", "team")
```

### 3.3 认证中间件

#### 3.3.1 AuthMiddleware

**文件**: `/home/user/bk-lite/server/apps/core/middlewares/auth_middleware.py`

**功能**: 
- 从 HTTP 请求头提取 Token
- 验证用户身份
- 支持 Bearer 格式

**豁免条件**:
```python
EXEMPT_PATHS = [
    "/swagger/",
    "/admin/",
    "/accounts/",
]

# 或者在视图上添加装饰器:
@api_exempt  # 标记为豁免认证
def login(request):
    ...
```

**提取 Token 逻辑**:
```python
token_header = request.META.get(settings.AUTH_TOKEN_HEADER_NAME)
# 支持 "Bearer token_value" 格式
if token_header.startswith("Bearer "):
    token = token_header[7:].strip()
else:
    token = token_header.strip()
```

#### 3.3.2 APISecretMiddleware

**文件**: `/home/user/bk-lite/server/apps/core/middlewares/api_middleware.py`

**功能**:
- 检查 API 令牌 (来自 `HTTP_API_AUTHORIZATION` 头)
- 验证并登录用户
- 设置 `request.api_pass = True` 标志

**流程**:
```python
# 1. 提取 API token
token = request.META.get("HTTP_API_AUTHORIZATION")

# 2. 认证用户
user = auth.authenticate(request=request, api_token=token)

# 3. 登录用户
auth.login(request, user)
setattr(request, "api_pass", True)
```

### 3.4 中间件执行顺序

**文件**: `/home/user/bk-lite/server/config/components/app.py`

```python
MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "apps.core.middlewares.app_exception_middleware.AppExceptionMiddleware",
    "apps.core.middlewares.drf_middleware.DisableCSRFMiddleware",      # CSRF 禁用
    "apps.core.middlewares.api_middleware.APISecretMiddleware",         # API 令牌检查
    "apps.core.middlewares.auth_middleware.AuthMiddleware",             # Token 认证
    "better_exceptions.integrations.django.BetterExceptionsMiddleware",
)
```

---

## 4. 权限控制机制

### 4.1 权限装饰器

**文件**: `/home/user/bk-lite/server/apps/core/decorators/api_permission.py`

#### 4.1.1 HasRole 装饰器

**用途**: 基于角色的访问控制

```python
@HasRole(roles="admin")  # 需要 admin 角色
@HasRole(roles=["admin", "manager"])  # 需要 admin 或 manager 角色
def some_view(request):
    pass
```

**特殊处理**:
```python
if roles == "admin":
    # 自动添加 CLIENT_ID_admin 角色
    client_id = os.getenv("CLIENT_ID", "")
    roles = ["admin", f"{client_id}_admin"] if client_id else ["admin"]
```

**豁免条件**:
- 如果 `request.api_pass = True`，则允许通过
- 如果没有指定角色要求，则直接通过
- 如果用户是超级用户，则允许通过

#### 4.1.2 HasPermission 装饰器

**用途**: 基于细粒度权限的访问控制

```python
@HasPermission(permission="user_group-View", app_name="system_mgmt")
def list_users(request):
    pass

@HasPermission(permission="user_group-View,user_group-Add")
def create_user(request):
    pass
```

**权限格式**: `{resource}-{action}` (如: `user_group-View`, `api_secret_key-Delete`)

**权限映射** (app_name):
```python
app_name_map = {
    "system_mgmt": "system-manager",
    "node_mgmt": "node",
    "console_mgmt": "ops-console",
    "alerts": "alarm"
}
```

**用户权限结构**:
```python
# 新格式 (字典)
user.permission = {
    "system-manager": {"user_group-View", "user_group-Add"},
    "node": {"node-View"},
    ...
}

# 旧格式 (集合)
user.permission = {"user_group-View", "user_group-Add"}
```

**豁免条件**:
- `request.api_pass = True`
- 用户是超级用户
- 用户权限与要求权限有交集

### 4.2 权限使用示例

**文件**: `/home/user/bk-lite/server/apps/system_mgmt/viewset/user_viewset.py`

```python
@action(detail=False, methods=["GET"])
@HasPermission("user_group-View")
def search_user_list(self, request):
    # 搜索用户
    pass

@action(detail=False, methods=["POST"])
@HasPermission("user_group-View")
def get_user_detail(self, request):
    # 获取用户详情
    pass
```

**文件**: `/home/user/bk-lite/server/apps/base/user_api_secret_mgmt/views.py`

```python
@HasPermission("api_secret_key-View", "opspilot")
def list(self, request, *args, **kwargs):
    pass

@action(detail=False, methods=["POST"])
@HasPermission("api_secret_key-Add", "opspilot")
def generate_api_secret(self, request):
    pass
```

---

## 5. 响应格式标准化

### 5.1 统一响应格式

**文件**: `/home/user/bk-lite/server/config/drf/renderers.py`

所有 API 响应遵循统一的 JSON 格式:

**成功响应** (2xx):
```json
{
    "result": true,
    "code": "20000",
    "message": "success",
    "data": {
        // 实际数据
    }
}
```

**失败响应** (4xx/5xx):
```json
{
    "result": false,
    "code": "40000",
    "message": "错误信息",
    "data": null
}
```

**验证错误响应**:
```json
{
    "result": false,
    "code": "40000",
    "message": "username:不能为空;email:邮箱格式不正确",
    "data": null
}
```

### 5.2 自定义渲染器实现

```python
class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        request = renderer_context.get("request")
        response = renderer_context.get("response")
        
        # DELETE 操作状态码: 204 -> 200
        if response.status_code == 204 and request.method == "DELETE":
            response.status_code = 200
        
        # 重新构建响应
        if status.is_success(response.status_code):
            ret = {
                "result": True,
                "code": str(response.status_code * 100),
                "message": "success",
                "data": data,
            }
        else:
            ret = {
                "result": False,
                "code": str((response.status_code if response else 500) * 100),
                "message": self._format_validation_message(data.get("detail", "")),
                "data": data.get("data"),
            }
        
        return super().render(ret, accepted_media_type, renderer_context)
```

---

## 6. 分页与过滤

### 6.1 分页配置

**文件**: `/home/user/bk-lite/server/config/drf/pagination.py`

```python
class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 10000
    
    def paginate_queryset(self, queryset, request, view=None):
        page_size = request.GET.get("page_size")
        # 如果 page_size 为 0 或 -1，则返回所有结果 (不分页)
        if page_size is None or page_size in ["0", "-1"]:
            return None
        return super().paginate_queryset(queryset, request, view)
    
    def get_paginated_response(self, data):
        return Response({
            "count": self.page.paginator.count,
            "items": data,
        })
```

**查询参数**:
```
GET /api/v1/system_mgmt/user/?page=1&page_size=20
GET /api/v1/system_mgmt/user/?page=1&page_size=-1  # 返回所有
GET /api/v1/system_mgmt/user/?page=1&page_size=0   # 返回所有
```

### 6.2 过滤配置

**文件**: `/home/user/bk-lite/server/config/components/drf.py`

```python
"DEFAULT_FILTER_BACKENDS": [
    "django_filters.rest_framework.DjangoFilterBackend",  # 字段过滤
    "rest_framework.filters.SearchFilter",                # 搜索过滤
    "rest_framework.filters.OrderingFilter",              # 排序
],
```

**示例**:
```
GET /api/v1/system_mgmt/user/?search=admin           # 搜索
GET /api/v1/system_mgmt/user/?ordering=-id           # 反向排序
GET /api/v1/system_mgmt/user/?username=admin         # 字段过滤
```

---

## 7. ModelViewSet 自定义

**文件**: `/home/user/bk-lite/server/config/drf/viewsets.py`

```python
class ModelViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        """创建时自动添加创建者和更新者"""
        user = serializer.context.get("request").user
        username = getattr(user, "username", "admin")
        if hasattr(serializer.Meta.model, "created_by"):
            serializer.save(created_by=username, updated_by=username)
        else:
            serializer.save()
    
    def perform_update(self, serializer):
        """更新时自动添加更新者"""
        user = serializer.context.get("request").user
        username = getattr(user, "username", "admin")
        if hasattr(serializer.Meta.model, "updated_by"):
            serializer.save(updated_by=username)
        else:
            serializer.save()
```

---

## 8. 外部集成与调用可能性

### 8.1 开放 API 端点

#### 8.1.1 OpsPilot 开放接口

**文件**: `/home/user/bk-lite/server/apps/opspilot/views.py`

```python
# OpenAI 兼容接口
POST /api/v1/opspilot/bot_mgmt/v1/chat/completions

# Lobe Chat 兼容接口
POST /api/v1/opspilot/bot_mgmt/lobe_chat/v1/chat/completions

# 技能执行接口
POST /api/v1/opspilot/bot_mgmt/skill_execute/

# 获取机器人详情
GET  /api/v1/opspilot/bot_mgmt/bot/{bot_id}/get_detail/
```

**认证方式**:
```python
# 从 Authorization 头提取 API Token
api_token = request.META.get("HTTP_AUTHORIZATION").split("TOKEN")[-1].strip()
bot = Bot.objects.filter(id=bot_id, api_token=api_token).first()
```

#### 8.1.2 告警 Webhook 接收

**文件**: `/home/user/bk-lite/server/apps/alerts/urls.py`

```python
POST /api/v1/alerts/api/receiver_data/   # 接收告警数据

POST /api/v1/alerts/api/test/            # 测试端点
```

**特点**: 支持第三方告警源推送

#### 8.1.3 节点管理开放 API

**文件**: `/home/user/bk-lite/server/apps/node_mgmt/urls.py`

```python
# 开放 API (无 trailing slash)
/api/v1/node_mgmt/open_api
```

### 8.2 API 密钥管理

**文件**: `/home/user/bk-lite/server/apps/base/user_api_secret_mgmt/views.py`

```python
# 生成 API 密钥
POST /api/v1/base/user_api_secret/generate_api_secret/

# 创建 API 密钥
POST /api/v1/base/user_api_secret/

# 列表
GET  /api/v1/base/user_api_secret/

# 删除
DELETE /api/v1/base/user_api_secret/{id}/
```

**API 密钥格式**: 64 字符十六进制字符串

### 8.3 RPC 调用架构

**文件**: `/home/user/bk-lite/server/apps/rpc/base.py`

```python
class RpcClient(object):
    """NATS 消息队列 RPC 客户端"""
    def __init__(self, namespace=None):
        namespace = os.getenv("NATS_NAMESPACE", "bk_lite")
        self.namespace = namespace
    
    def run(self, method_name, *args, **kwargs):
        return asyncio.run(nats_client.request(self.namespace, method_name, ...))
```

**支持的 RPC 客户端**:
- `SystemMgmt()` - 系统管理 RPC
- `NodeMgmt()` - 节点管理 RPC
- `StarGazer()` - 资源采集 RPC
- `Monitor()` - 监控 RPC
- `Alerts()` - 告警 RPC
- `OpsPilot()` - AI 助手 RPC

### 8.4 WebSocket 支持

**说明**: 项目中未发现 WebSocket 配置，所有通信基于 HTTP REST

---

## 9. API 文档状态

### 9.1 文档配置

**当前状态**: 
- API 文档文件为空: `/home/user/bk-lite/docs/overview/api_doc.md`
- 使用 CoreAPI AutoSchema，未配置 Swagger/OpenAPI

**配置信息**:
```python
# DRF 配置
"DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
```

### 9.2 模块级 API 文档

**OpsPilot 模块级文档** (`/home/user/bk-lite/web/src/app/opspilot/public/module_api/`):
```
zh/knowledge_api.md      # 中文知识库 API 文档
zh/skill_api.md          # 中文技能 API 文档
zh/studio_api.md         # 中文工作室 API 文档
en/knowledge_api.md      # 英文知识库 API 文档
en/skill_api.md          # 英文技能 API 文档
en/studio_api.md         # 英文工作室 API 文档
```

---

## 10. 特殊功能与扩展点

### 10.1 国际化 (i18n)

**配置**:
```python
# Django i18n URLs
path("i18n/", include("django.conf.urls.i18n")),

# 用户 locale 自动设置
user.locale = user_info.get("locale", DEFAULT_LOCALE)

# locale 映射
CHINESE_LOCALE_MAPPING = {"zh-CN": "zh-Hans"}
```

### 10.2 CORS 跨域支持

**调试模式配置** (`DEBUG=True`):
```python
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "api-authorization",  # API 密钥认证头
    "debug",
]
```

### 10.3 CSRF 保护禁用

**说明**: 在中间件中禁用 CSRF 检查 (用于 API 兼容性)

```python
class DisableCSRFMiddleware(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, "_dont_enforce_csrf_checks", True)
```

### 10.4 调试工具

**可用工具** (DEBUG=True):
```python
# django-debug-toolbar
# better-exceptions 更好的异常显示
# django-extensions (shell_plus)
```

---

## 11. 安全配置

### 11.1 认证检查

| 检查项 | 状态 | 说明 |
|------|------|------|
| CSRF 检查 | 禁用 | 在中间件中禁用 |
| Session 认证 | 启用 | 支持 Session 认证 |
| Token 认证 | 启用 | Authorization 头 |
| API 密钥认证 | 启用 | API-Authorization 头 |
| 权限检查 | 启用 | 装饰器级权限检查 |
| 豁免路径 | 启用 | `/swagger/`, `/admin/`, `/accounts/` |

### 11.2 用户模型

**文件**: `/home/user/bk-lite/server/apps/base/models/user.py`

```python
class User(AbstractUser):
    username = models.CharField(max_length=150, unique=False)
    group_list = models.JSONField(default=list)
    roles = models.JSONField(default=list)
    locale = models.CharField(max_length=32, default="zh-CN")
    domain = models.CharField(max_length=100, default="domain.com")
    
    class Meta:
        unique_together = ("username", "domain")  # 用户名与域名组合唯一
```

---

## 12. 调用示例

### 12.1 Token 认证调用

```bash
curl -X GET "http://localhost:8001/api/v1/system_mgmt/user/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

### 12.2 API 密钥调用

```bash
curl -X GET "http://localhost:8001/api/v1/system_mgmt/user/" \
  -H "API-Authorization: YOUR_API_SECRET" \
  -H "Content-Type: application/json"
```

### 12.3 登录获取 Token

```bash
curl -X POST "http://localhost:8001/api/login/" \
  -H "Content-Type: application/json" \
  -d "{
    \"username\": \"admin\",
    \"password\": \"password\",
    \"domain\": \"domain.com\"
  }"
```

### 12.4 创建 API 密钥

```bash
# 生成 API 密钥
curl -X POST "http://localhost:8001/api/v1/base/user_api_secret/generate_api_secret/" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 创建 API 密钥
curl -X POST "http://localhost:8001/api/v1/base/user_api_secret/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"api_secret\": \"GENERATED_SECRET\"
  }"
```

### 12.5 OpenAI 兼容调用

```bash
curl -X POST "http://localhost:8001/api/v1/opspilot/bot_mgmt/v1/chat/completions" \
  -H "Authorization: TOKEN YOUR_BOT_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"messages\": [{\"role\": \"user\", \"content\": \"Hello\"}],
    \"model\": \"bot-1\"
  }"
```

---

## 13. API 限制与配置

### 13.1 分页限制

| 参数 | 值 |
|-----|-----|
| 默认页面大小 | 10 |
| 最大页面大小 | 10000 |
| 支持全量获取 | 是 (page_size=-1 或 0) |

### 13.2 文件上传限制

```python
DATA_UPLOAD_MAX_NUMBER_FILES = 100  # 最多 100 个文件
```

### 13.3 时间格式

```python
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"  # ISO 8601 格式
```

---

## 14. 总结与建议

### 14.1 架构优点

1. **模块化设计**: 每个应用独立管理 URL 路由
2. **统一认证**: 支持多种认证方式 (Token、API 密钥、Session)
3. **细粒度权限**: 支持角色和权限的组合控制
4. **响应标准化**: 所有 API 返回统一的 JSON 格式
5. **可扩展性**: 新应用自动注册到路由系统

### 14.2 改进建议

1. **API 文档**: 
   - 建议配置 drf-spectacular 以支持 OpenAPI 3.0
   - 补充 `/docs/overview/api_doc.md` 的内容

2. **速率限制**:
   - 建议添加 API 速率限制中间件
   - 防止滥用和 DDoS 攻击

3. **API 版本控制**:
   - 考虑支持多版本 API (`/api/v1/`, `/api/v2/`)
   - 便于逐步升级

4. **API 日志**:
   - 建议添加详细的 API 访问日志
   - 便于审计和调试

5. **Webhook 签名验证**:
   - 建议在告警 Webhook 中添加签名验证
   - 增强安全性

---

## 附录 A: 环境变量

| 变量名 | 说明 | 示例 |
|------|------|------|
| CLIENT_ID | 客户端 ID | "myapp" |
| NATS_NAMESPACE | NATS 命名空间 | "bk_lite" |
| INSTALL_APPS | 安装应用列表 | "system_mgmt,monitor,alerts" |
| DEBUG | 调试模式 | "True" / "False" |

---

## 附录 B: 常见错误码

| 错误码 | 描述 |
|------|------|
| 20000 | 成功 (2xx 状态码 × 100) |
| 40000 | 客户端错误 (4xx 状态码 × 100) |
| 50000 | 服务器错误 (5xx 状态码 × 100) |

---

**文档生成日期**: 2025-10-21
**版本**: 1.0
**作者**: Claude Code Analysis


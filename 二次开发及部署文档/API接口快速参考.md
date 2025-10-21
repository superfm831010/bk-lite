# BKLite API 快速参考指南

## 一、API 基本信息

| 项目 | 内容 |
|------|------|
| API 基础URL | `http://localhost:8001/api/v1/` |
| API 版本 | v1 |
| 框架 | Django REST Framework (DRF) |
| 默认端口 | 8001 |

---

## 二、认证方式

### 方式 1: Token 认证 (标准方式)

**头部名称**: `Authorization`
**格式**: `Bearer YOUR_TOKEN` 或直接使用 Token

```bash
curl -H "Authorization: Bearer token123..." http://localhost:8001/api/v1/system_mgmt/user/
```

### 方式 2: API 密钥认证 (机器人调用)

**头部名称**: `API-Authorization`
**格式**: 直接使用 64 字符十六进制字符串

```bash
curl -H "API-Authorization: api_secret_key..." http://localhost:8001/api/v1/system_mgmt/user/
```

### 方式 3: OpsPilot 机器人认证

**头部名称**: `Authorization`
**格式**: `TOKEN bot_api_token`

```bash
curl -H "Authorization: TOKEN bot_api_token..." http://localhost:8001/api/v1/opspilot/bot_mgmt/v1/chat/completions
```

---

## 三、核心 API 端点速查表

### 认证与登录

| 端点 | 方法 | 说明 | 需要认证 |
|------|------|------|---------|
| `/api/login/` | POST | 用户登录 | 否 |
| `/api/bk_lite_login/` | POST | BK 域名登录 | 否 |
| `/api/reset_pwd/` | POST | 重置密码 | 否 |
| `/api/verify_otp_code/` | POST | 验证 OTP | 否 |
| `/api/login_info/` | GET | 获取登录信息 | 是 |

### 用户与权限管理

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/system_mgmt/user/` | GET | 列出用户 |
| `/api/v1/system_mgmt/user/` | POST | 创建用户 |
| `/api/v1/system_mgmt/user/{id}/` | GET | 获取用户详情 |
| `/api/v1/system_mgmt/user/{id}/` | PUT | 更新用户 |
| `/api/v1/system_mgmt/user/{id}/` | DELETE | 删除用户 |
| `/api/v1/system_mgmt/user/search_user_list/` | GET | 搜索用户 |
| `/api/v1/system_mgmt/role/` | GET | 列出角色 |
| `/api/v1/system_mgmt/group/` | GET | 列出分组 |

### API 密钥管理

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/base/user_api_secret/` | GET | 列出 API 密钥 |
| `/api/v1/base/user_api_secret/` | POST | 创建 API 密钥 |
| `/api/v1/base/user_api_secret/generate_api_secret/` | POST | 生成新的 API 密钥 |
| `/api/v1/base/user_api_secret/{id}/` | DELETE | 删除 API 密钥 |

### 节点管理

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/node_mgmt/api/node/` | GET | 列出节点 |
| `/api/v1/node_mgmt/api/node/` | POST | 创建节点 |
| `/api/v1/node_mgmt/api/collector/` | GET | 列出采集器 |
| `/api/v1/node_mgmt/api/package/` | GET | 列出包 |

### 告警管理

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/alerts/api/receiver_data/` | POST | 接收告警数据 (Webhook) |
| `/api/v1/alerts/api/alert_source/` | GET | 列出告警源 |
| `/api/v1/alerts/api/alerts/` | GET | 列出告警 |
| `/api/v1/alerts/api/events/` | GET | 列出事件 |

### 监控系统

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/monitor/api/monitor_object/` | GET | 列出监控对象 |
| `/api/v1/monitor/api/metrics/` | GET | 列出指标 |
| `/api/v1/monitor/api/monitor_alert/` | GET | 列出监控告警 |
| `/api/v1/monitor/api/monitor_policy/` | GET | 列出监控策略 |

### CMDB 管理

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/cmdb/api/model/` | GET | 列出模型 |
| `/api/v1/cmdb/api/instance/` | GET | 列出实例 |
| `/api/v1/cmdb/api/classification/` | GET | 列出分类 |

### OpsPilot AI 助手

| 端点 | 方法 | 说明 | 特殊认证 |
|------|------|------|---------|
| `/api/v1/opspilot/bot_mgmt/v1/chat/completions` | POST | OpenAI 兼容接口 | Bot Token |
| `/api/v1/opspilot/bot_mgmt/lobe_chat/v1/chat/completions` | POST | Lobe Chat 兼容接口 | Bot Token |
| `/api/v1/opspilot/bot_mgmt/skill_execute/` | POST | 执行技能 | Bot Token |
| `/api/v1/opspilot/knowledge_mgmt/knowledge_base/` | GET | 列出知识库 | - |
| `/api/v1/opspilot/bot_mgmt/bot/` | GET | 列出机器人 | - |

### 日志管理

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/log/collect_types/` | GET | 列出采集类型 |
| `/api/v1/log/search/` | GET | 搜索日志 |
| `/api/v1/log/log_group/` | GET | 列出日志分组 |

### MLOps

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/mlops/anomaly_detection_datasets/` | GET | 异常检测数据集 |
| `/api/v1/mlops/timeseries_predict_datasets/` | GET | 时间序列预测数据集 |
| `/api/v1/mlops/log_clustering_datasets/` | GET | 日志聚类数据集 |

---

## 四、通用查询参数

### 分页参数

```
?page=1                    # 页码 (默认为 1)
?page_size=20             # 每页数量 (默认为 10，最大 10000)
?page_size=-1             # 返回所有结果 (不分页)
```

### 搜索与排序

```
?search=keyword           # 搜索关键词
?ordering=-id             # 排序 (- 表示反向)
?ordering=username        # 按用户名排序
```

### 字段过滤

```
?username=admin           # 精确匹配用户名
?email__icontains=test    # 邮箱包含 "test"
```

---

## 五、响应格式

### 成功响应 (200-299)

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

### 失败响应 (400-599)

```json
{
    "result": false,
    "code": "40000",
    "message": "错误描述",
    "data": null
}
```

### 分页响应示例

```json
{
    "result": true,
    "code": "20000",
    "message": "success",
    "data": {
        "count": 100,
        "items": [
            { "id": 1, "username": "admin" },
            { "id": 2, "username": "user" }
        ]
    }
}
```

---

## 六、常见操作示例

### 登录获取 Token

```bash
curl -X POST http://localhost:8001/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "password",
    "domain": "domain.com"
  }'
```

**响应**:
```json
{
    "result": true,
    "code": "20000",
    "message": "success",
    "data": {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
}
```

### 使用 Token 调用 API

```bash
curl -X GET http://localhost:8001/api/v1/system_mgmt/user/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -H "Content-Type: application/json"
```

### 创建 API 密钥

```bash
# 第一步: 生成密钥
curl -X POST http://localhost:8001/api/v1/base/user_api_secret/generate_api_secret/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# 第二步: 使用生成的密钥
curl -X POST http://localhost:8001/api/v1/base/user_api_secret/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "api_secret": "生成的密钥"
  }'

# 第三步: 使用 API 密钥调用接口
curl -X GET http://localhost:8001/api/v1/system_mgmt/user/ \
  -H "API-Authorization: 生成的密钥"
```

### 搜索用户

```bash
curl -X GET "http://localhost:8001/api/v1/system_mgmt/user/search_user_list/?search=admin" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 分页获取用户列表

```bash
# 获取第 1 页，每页 10 条
curl -X GET "http://localhost:8001/api/v1/system_mgmt/user/?page=1&page_size=10" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 获取所有用户 (不分页)
curl -X GET "http://localhost:8001/api/v1/system_mgmt/user/?page_size=-1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 创建用户

```bash
curl -X POST http://localhost:8001/api/v1/system_mgmt/user/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "display_name": "New User"
  }'
```

### 更新用户

```bash
curl -X PUT http://localhost:8001/api/v1/system_mgmt/user/1/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newemail@example.com",
    "display_name": "Updated Name"
  }'
```

### 删除用户

```bash
curl -X DELETE http://localhost:8001/api/v1/system_mgmt/user/1/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 获取告警列表

```bash
curl -X GET "http://localhost:8001/api/v1/alerts/api/alerts/?page=1&page_size=20" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 推送告警 (Webhook)

```bash
curl -X POST http://localhost:8001/api/v1/alerts/api/receiver_data/ \
  -H "Content-Type: application/json" \
  -d '{
    "alert_name": "CPU High",
    "alert_level": "critical",
    "timestamp": "2025-10-21T10:00:00+00:00"
  }'
```

### OpenAI 兼容调用

```bash
curl -X POST http://localhost:8001/api/v1/opspilot/bot_mgmt/v1/chat/completions \
  -H "Authorization: TOKEN YOUR_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "model": "default",
    "temperature": 0.7
  }'
```

---

## 七、权限控制

### 权限装饰器使用

系统采用两种权限检查方式:

#### 1. 基于角色 (HasRole)

```python
@HasRole(roles="admin")        # 需要 admin 角色
@HasRole(roles=["admin", "manager"])  # 需要任意一个角色
```

#### 2. 基于权限 (HasPermission)

```python
@HasPermission(permission="user_group-View")         # 单个权限
@HasPermission(permission="user_group-View,user_group-Add")  # 多个权限
@HasPermission(permission="user_group-View", app_name="system_mgmt")
```

### 权限豁免

以下情况会跳过权限检查:

1. API 密钥认证 (`request.api_pass = True`)
2. 超级用户 (`is_superuser = True`)
3. 用户权限与要求权限有交集

---

## 八、HTTP 状态码与错误码对应

| HTTP 状态码 | API 错误码 | 说明 |
|------------|----------|------|
| 200 | 20000 | 成功 |
| 201 | 20100 | 创建成功 |
| 204 | 20400 | 删除成功 (自动转为 200) |
| 400 | 40000 | 请求参数错误 |
| 401 | 40100 | 未认证 (缺少认证) |
| 403 | 40300 | 权限不足 |
| 404 | 40400 | 资源不存在 |
| 500 | 50000 | 服务器错误 |

---

## 九、常见错误及解决方案

### 错误 1: "Token Required"

**原因**: 缺少认证令牌

**解决**:
```bash
# 添加 Authorization 头
curl -H "Authorization: Bearer YOUR_TOKEN" ...
```

### 错误 2: "insufficient permissions"

**原因**: 用户权限不足

**解决**:
- 检查用户是否拥有所需权限
- 为用户分配相应角色或权限

### 错误 3: "api_secret_key-View: api_secret_key-View"

**原因**: 创建 API 密钥时缺少权限

**解决**:
```bash
# 使用有权限的用户账号创建
curl -X POST http://localhost:8001/api/v1/base/user_api_secret/ \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  ...
```

### 错误 4: 504 Gateway Timeout

**原因**: 后端服务无响应或超时

**解决**:
- 检查后端服务是否运行
- 检查网络连接
- 增加请求超时时间

---

## 十、应用隐射关系

| 应用名称 | 前缀 | 主要功能 | ViewSet 数 |
|--------|------|--------|----------|
| core | /api/v1/core/ | 认证、登录、菜单 | 1 |
| system_mgmt | /api/v1/system_mgmt/ | 系统管理 | 8 |
| node_mgmt | /api/v1/node_mgmt/ | 节点管理 | 10 |
| cmdb | /api/v1/cmdb/ | CMDB | 6 |
| monitor | /api/v1/monitor/ | 监控 | 14 |
| alerts | /api/v1/alerts/ | 告警 | 11 |
| log | /api/v1/log/ | 日志 | 12 |
| opspilot | /api/v1/opspilot/ | AI 助手 | 20+ |
| mlops | /api/v1/mlops/ | 机器学习 | 20+ |
| base | /api/v1/base/ | 基础应用 | 1 |
| playground | /api/v1/playground/ | 测试室 | 3 |
| operation_analysis | /api/v1/operation_analysis/ | 运维分析 | 2 |
| lab | /api/v1/lab/ | 实验室 | - |
| console_mgmt | /api/v1/console_mgmt/ | 控制台 | - |

**总计**: 120+ 个注册路由

---

## 十一、开发快速启动

### 启动开发服务

```bash
cd /home/user/bk-lite/server
make dev
```

### 创建超级用户

```bash
cd /home/user/bk-lite/server
make shell
# 在 shell 中执行
User.objects.create_superuser('admin', 'admin@example.com', 'password')
```

### 迁移数据库

```bash
cd /home/user/bk-lite/server
make migrate
```

### 运行测试

```bash
cd /home/user/bk-lite/server
make test
```

---

## 十二、配置文件位置

| 配置项 | 文件路径 |
|------|--------|
| 主配置 | `/home/user/bk-lite/server/config/default.py` |
| DRF 配置 | `/home/user/bk-lite/server/config/components/drf.py` |
| 应用配置 | `/home/user/bk-lite/server/config/components/app.py` |
| 认证后端 | `/home/user/bk-lite/server/apps/core/backends.py` |
| 中间件 | `/home/user/bk-lite/server/apps/core/middlewares/` |
| 权限装饰器 | `/home/user/bk-lite/server/apps/core/decorators/api_permission.py` |

---

## 十三、环境变量

| 变量 | 说明 | 示例 |
|-----|------|------|
| `CLIENT_ID` | 客户端 ID | `myapp` |
| `NATS_NAMESPACE` | NATS 命名空间 | `bk_lite` |
| `INSTALL_APPS` | 要安装的应用 | `system_mgmt,monitor` |
| `DEBUG` | 调试模式 | `True` / `False` |

---

## 十四、常用 HTTP 方法

| 方法 | 用途 | 示例 |
|-----|------|------|
| GET | 获取资源列表或详情 | `GET /api/v1/user/` |
| POST | 创建资源 | `POST /api/v1/user/` |
| PUT | 完全更新资源 | `PUT /api/v1/user/1/` |
| PATCH | 部分更新资源 | `PATCH /api/v1/user/1/` |
| DELETE | 删除资源 | `DELETE /api/v1/user/1/` |

---

## 十五、请求与响应示例

### 创建用户请求

```http
POST /api/v1/system_mgmt/user/ HTTP/1.1
Host: localhost:8001
Authorization: Bearer token123
Content-Type: application/json

{
    "username": "testuser",
    "email": "test@example.com",
    "display_name": "Test User",
    "password": "secure_password"
}
```

### 创建用户响应

```json
{
    "result": true,
    "code": "20100",
    "message": "success",
    "data": {
        "id": 5,
        "username": "testuser",
        "email": "test@example.com",
        "display_name": "Test User",
        "created_at": "2025-10-21T10:00:00+00:00",
        "created_by": "admin"
    }
}
```

---

**最后更新**: 2025-10-21
**文档版本**: 1.0


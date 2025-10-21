# 修复探针安装NATS通信问题

## 问题描述

在黄埔海关智能运维平台内网生产环境中，尝试安装Linux探针时报错：

```
download: nats: no responders available for request
```

探针安装失败，无法完成文件下载步骤。

## 问题分析

### 1. 系统架构背景

探针安装功能使用NATS消息队列进行通信：

- **Server（Django后端）**：发送安装指令到NATS
- **nats-executor（Go服务）**：订阅NATS消息，执行文件下载、SSH命令等操作
- **通信机制**：基于NATS的请求-响应模式

### 2. NATS Subject命名规则

NATS使用subject来路由消息，格式为：`<operation>.<method>.<instance_id>`

例如：
- `download.remote.default` - 向default实例发送远程下载请求
- `ssh.execute.管理网` - 向管理网实例发送SSH执行请求

### 3. 问题根源

通过日志和代码分析发现：

**nats-executor订阅的subjects（修复前）**：
```
download.remote.default
ssh.execute.default
local.execute.default
upload.remote.default
```

**探针安装发送的subject**：
```
download.remote.管理网  # 使用云区域名称作为instance_id
```

**原因**：
1. nats-executor的实例ID配置为 `default`
2. 探针安装使用云区域的 `work_node` 字段（值为"管理网"）作为实例ID
3. 消息路由不匹配，导致无订阅者响应

### 4. 相关代码位置

**nats-executor订阅配置**：
- `deploy-huangpu/docker-compose.yml:230` - 环境变量 `NATS_INSTANCE_ID`
- `agents/nats-executor/main.go:170-176` - 订阅逻辑

**探针安装发送逻辑**：
- `server/apps/node_mgmt/tasks/installer.py:134` - 使用 `task_obj.work_node` 作为实例ID
- `server/apps/rpc/executor.py:10-21` - Executor类使用实例ID发送消息

**数据库记录**：
```sql
SELECT work_node FROM node_mgmt_controllertask;
-- 结果: 管理网
```

## 解决方案

### 修复步骤

#### 1. 修改docker-compose配置

文件：`/home/soft/bk-lite/deploy-huangpu/docker-compose.yml`

```yaml
# 修改前
  nats-executor:
    environment:
      - NATS_INSTANCE_ID=default

# 修改后
  nats-executor:
    environment:
      - NATS_INSTANCE_ID=管理网
```

#### 2. 重新创建容器

```bash
cd /home/soft/bk-lite/deploy-huangpu
docker compose up -d nats-executor
```

**注意**：必须使用 `docker compose up -d` 重新创建容器，单纯 `docker restart` 不会更新环境变量。

#### 3. 验证修复

查看容器日志：
```bash
docker logs bklite-nats-executor-prod --tail 20
```

预期输出：
```
2025/10/21 13:06:33 [Local Subscribe] Instance: 管理网, Subscribing to subject: local.execute.管理网
2025/10/21 13:06:33 [SSH Subscribe] Instance: 管理网, Subscribing to subject: ssh.execute.管理网
2025/10/21 13:06:33 [Download Subscribe] Instance: 管理网, Subscribing to subject: download.remote.管理网
2025/10/21 13:06:33 [Upload Subscribe] Instance: 管理网, Subscribing to subject: upload.remote.管理网
```

确认环境变量：
```bash
docker exec bklite-nats-executor-prod env | grep NATS_INSTANCE
```

预期输出：
```
NATS_INSTANCE_ID=管理网
```

## 测试验证

修复后，重新尝试安装探针：

1. 登录前端界面
2. 进入"节点管理" -> "云区域" -> "管理网"
3. 点击"安装控制器"
4. 填写目标主机信息：
   - IP: 192.168.31.10
   - 用户名: root
   - 密码: 1qaz2wsx@
5. 执行安装

预期结果：
- ✅ 文件下载步骤成功
- ✅ 文件传输步骤成功
- ✅ 安装命令执行成功
- ✅ 探针正常注册到系统

## 技术细节

### NATS消息路由流程

```
[Server] --> NATS Request --> [NATS Server] --> Route by Subject --> [nats-executor]
                                                                              |
                                                                              v
                                                                       Execute & Response
```

### Instance ID的作用

1. **隔离性**：不同云区域可以有独立的executor实例
2. **路由性**：确保消息发送到正确的执行器
3. **扩展性**：支持多区域、多环境部署

### 相关配置项

**Server环境变量**：
- `NATS_NAMESPACE=bklite` - NATS命名空间前缀
- `NATS_SERVERS` - NATS服务器地址

**nats-executor环境变量**：
- `NATS_INSTANCE_ID` - 实例标识（必须与云区域的work_node一致）
- `NATS_URLS` - NATS连接地址
- `NATS_CA_FILE` - TLS证书路径

## 长期优化建议

### 方案1：统一使用"default"

修改系统设计，所有云区域统一使用 `default` 作为work_node。

**优点**：
- 简化配置
- 单一executor实例即可

**缺点**：
- 无法支持多云区域隔离
- 扩展性受限

### 方案2：增强executor支持多实例

修改nats-executor代码，支持通配符订阅或多实例配置。

```go
// 支持通配符订阅
subjects := []string{
    "download.remote.*",
    "ssh.execute.*",
    // ...
}

// 或支持多实例配置
instanceIDs := []string{"default", "管理网", "业务网"}
```

**优点**：
- 最灵活的方案
- 支持多云区域、多环境
- 无需为每个云区域配置独立executor

**缺点**：
- 需要修改Go代码
- 需要重新编译和测试

### 方案3：前端配置化

在云区域管理界面增加"工作节点ID"配置项，与executor实例ID对应。

**优点**：
- 灵活配置
- 支持多executor部署

**缺点**：
- 增加配置复杂度
- 需要修改前后端代码

## 注意事项

1. **生产环境操作**：修改配置前建议备份，选择业务低峰期操作
2. **多云区域支持**：如有多个云区域，每个云区域需要独立的executor实例或使用通配符订阅
3. **环境变量更新**：修改docker-compose环境变量后，必须重新创建容器才能生效
4. **监控验证**：修复后持续监控NATS和executor日志，确保通信正常

## 相关文件清单

- ✅ `deploy-huangpu/docker-compose.yml` - 修改实例ID配置
- 📝 `server/apps/node_mgmt/tasks/installer.py` - 探针安装任务逻辑
- 📝 `server/apps/rpc/executor.py` - NATS RPC客户端
- 📝 `agents/nats-executor/main.go` - executor主程序

## 修复时间

- **发现时间**：2025-10-21
- **修复时间**：2025-10-21
- **影响范围**：黄埔海关智能运维平台内网生产环境
- **修复状态**：✅ 已完成

## 参考资料

- [NATS Documentation](https://docs.nats.io/)
- [NATS Request-Reply Pattern](https://docs.nats.io/nats-concepts/core-nats/reqreply)
- BKLite项目架构文档（CLAUDE.md）

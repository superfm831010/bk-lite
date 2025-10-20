# BlueKing Lite 日志采集实现方案

> **技术研究文档**
> 文档版本：v1.0
> 创建日期：2025-10-20
> 研究目标：了解 BlueKing Lite 系统如何实现对 Windows 和 Linux 目标服务器的日志采集

---

## 一、系统架构概览

### 1.1 整体架构

BlueKing Lite 采用分布式日志采集架构，数据流如下：

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────────┐     ┌──────────────┐
│  目标服务器      │ --> │  采集代理     │ --> │ NATS 消息队列│ --> │  Vector 转换处理  │ --> │ VictoriaLogs │
│ (Windows/Linux) │     │ (多种采集器)  │     │             │     │                  │     │   日志存储    │
└─────────────────┘     └──────────────┘     └─────────────┘     └──────────────────┘     └──────────────┘
                                                                                                    │
                                                                                                    ▼
                                                                                          ┌──────────────────┐
                                                                                          │  Web 查询展示     │
                                                                                          │  (日志检索/告警)  │
                                                                                          └──────────────────┘
```

### 1.2 核心组件

1. **采集代理（Collector）**
   - 部署在目标服务器上
   - 负责读取日志文件或接收日志流
   - 支持多种采集器：Vector, Filebeat, Auditbeat, Metricbeat, Packetbeat

2. **NATS 消息队列**
   - 作为数据传输管道
   - 解耦采集端和存储端
   - 支持高并发和可靠传输

3. **Vector 转换器**
   - 从 NATS 订阅日志数据
   - 将日志解析为 JSON 格式
   - 转发到 VictoriaLogs
   - 配置文件：`deploy/docker-compose/conf/vector/vector.yaml`

4. **VictoriaLogs 存储**
   - 高性能日志存储引擎
   - 支持 LogSQL 查询语言
   - 提供 Elasticsearch 兼容接口

5. **Django 后端服务**
   - 管理采集配置（`server/apps/log/`）
   - 提供日志查询 API
   - 支持告警策略管理

6. **Next.js Web 前端**
   - 日志检索界面（`web/src/app/log/`）
   - 采集配置管理
   - 可视化展示和分析

---

## 二、操作系统支持

### 2.1 支持的操作系统

**✅ 完全支持 Windows 和 Linux**

系统在节点模型中定义了操作系统类型（`server/apps/node_mgmt/models/sidecar.py:10-13`）：

```python
OS_TYPE = (
    ("linux", "Linux"),
    ("windows", "Windows"),
)
```

### 2.2 跨平台兼容性

- **Vector**：原生支持 Windows 和 Linux
- **Filebeat**：Elastic Beat 系列支持多平台
- **Auditbeat**：仅支持 Linux（系统审计特性）
- **Metricbeat/Packetbeat**：跨平台支持

---

## 三、可用采集器详解

### 3.1 Vector（推荐）

Vector 是高性能的日志和指标采集工具，适用于文件日志采集。

#### 支持的采集类型

| 采集类型 | 说明 | 适用场景 | 配置文件模板 |
|---------|------|---------|------------|
| **file** | 文件日志采集 | 应用日志、服务日志 | `Vector/file/file.child.toml.j2` |
| **syslog** | Syslog 日志采集 | 系统日志、网络设备日志 | `Vector/syslog/syslog.child.toml.j2` |
| **docker** | Docker 容器日志 | 容器化应用日志 | `Vector/docker/docker.child.toml.j2` |
| **exec** | 命令执行输出 | 脚本输出、定期任务 | `Vector/exec/exec.child.toml.j2` |

#### Vector File 采集器配置示例

**位置**：`server/apps/log/plugins/Vector/file/file.child.toml.j2`

```toml
# ====================================
# file 日志源（含字段映射）
# ====================================
[sources.file_{{ instance_id }}]
type = "file"
include = ["{{ file_path }}"]  # 支持 Windows (C:\logs\*.log) 和 Linux (/var/log/*.log)
data_dir = "/opt/fusion-collectors"  # Linux 路径，Windows 需调整
ignore_older = 86400  # 忽略24小时以前的日志

{% if multiline %}
# ====================================
# 多行日志处理
# ====================================
multiline.condition_pattern = '{{ multiline.condition_pattern }}'
multiline.mode = "{{ multiline.mode }}"
multiline.start_pattern = '{{ multiline.start_pattern }}'
multiline.timeout_ms = {{ multiline.timeout_ms }}
{% endif %}

# ====================================
# enrich（字段补全）
# ====================================
[transforms.file_enrich_{{ instance_id }}]
type = "remap"
inputs = ["file_{{ instance_id }}"]
source = '''
.collector = "Vector"
.collect_type = "file"
.instance_id = "{{ instance_id }}"
'''

# ====================================
# sinks - 发送到 NATS
# ====================================
[sinks.vmlogs_{{ instance_id }}]
type = "nats"
inputs = ["file_enrich_{{ instance_id }}"]
subject = "vector"
url = "${NATS_PROTOCOL}://${NATS_SERVERS}"

[sinks.vmlogs_{{ instance_id }}.auth]
strategy = "user_password"
user = "${NATS_USERNAME}"
password = "${NATS_PASSWORD}"

[sinks.vmlogs_{{ instance_id }}.encoding]
codec = "json"
```

### 3.2 Filebeat

Elastic Filebeat 是轻量级日志采集工具。

#### 支持的采集类型

| 采集类型 | 说明 | 配置文件模板 |
|---------|------|------------|
| **filestream** | 文件流日志采集 | `Filebeat/filestream/filestream.child.yaml.j2` |

#### Filebeat Filestream 配置示例

**位置**：`server/apps/log/plugins/Filebeat/filestream/filestream.child.yaml.j2`

```yaml
# ================================== Filestream Input 配置 ==================================
- type: filestream
  id: {{ instance_id }}

  # ================================== 文件路径配置 ==================================
  paths:
    {% for path in paths %}
    - {{ path }}  # 支持 Windows 和 Linux 路径
    {% endfor %}

  # 文件编码（默认: utf-8）
  encoding: {{ encoding | default('utf-8') }}

  # ================================== 文件扫描配置 ==================================
  prospector.scanner.check_interval: {{ scan_frequency | default('10s') }}

  {% if ignore_older %}
  ignore_older: {{ ignore_older }}
  {% endif %}

  # ================================== 文件处理配置 ==================================
  max_bytes: {{ max_bytes | default('10MB') }}
  harvester_buffer_size: {{ harvester_buffer_size | default(16384) }}
  close_inactive: {{ close_inactive | default('5m') }}

  # ================================== 多行日志处理 ==================================
  {% if multiline %}
  parsers:
    - multiline:
        type: pattern
        pattern: '{{ multiline.pattern }}'
        negate: {{ multiline.negate | default(false) | lower }}
        match: {{ multiline.match | default('after') }}
        timeout: {{ multiline.timeout | default(5) }}s
        max_lines: {{ multiline.max_lines | default(500) }}
  {% endif %}

  # ================================== 字段标识配置 ==================================
  fields:
    collector: "Filebeat"
    collect_type: "filestream"
    instance_id: "{{ instance_id }}"
  fields_under_root: {{ fields_under_root | default(true) | lower }}
```

### 3.3 Auditbeat（仅 Linux）

用于 Linux 系统审计和安全监控。

#### 支持的采集类型

| 采集类型 | 说明 | 适用场景 | 配置文件模板 |
|---------|------|---------|------------|
| **auditd** | Linux 审计日志 | 安全审计、合规监控 | `Auditbeat/auditd/auditd.child.yaml.j2` |
| **file_integrity** | 文件完整性监控 | 关键文件变更检测 | `Auditbeat/file_integrity/file_integrity.child.yaml.j2` |

#### Auditbeat Auditd 功能说明

**位置**：`server/apps/log/plugins/Auditbeat/auditd/README.md`

**预设规则类别**：

- **security**：安全监控（身份管理 + 权限提升）
  - 监控 `/etc/passwd`, `/etc/shadow`, `/etc/sudoers`
  - 监控 `sudo`, `su` 命令执行

- **system**：系统监控（关键文件变更）
  - 监控 `/bin/`, `/sbin/`, `/boot/` 目录

- **network**：网络监控（连接活动）
  - 监控 socket 系统调用

### 3.4 Metricbeat

系统和服务指标采集。

| 采集类型 | 说明 | 配置文件模板 |
|---------|------|------------|
| **system** | 系统指标采集 | `Metricbeat/system/system.child.yaml.j2` |
| **docker** | Docker 指标采集 | `Metricbeat/docker/docker.child.yaml.j2` |

### 3.5 Packetbeat

网络数据包分析。

| 采集类型 | 说明 | 配置文件模板 |
|---------|------|------------|
| **http** | HTTP 流量分析 | `Packetbeat/http/http.child.yaml.j2` |
| **dns** | DNS 查询分析 | `Packetbeat/dns/dns.child.yaml.j2` |
| **dhcp** | DHCP 流量分析 | `Packetbeat/dhcp/dhcp.child.yaml.j2` |
| **icmp** | ICMP 流量分析 | `Packetbeat/icmp/icmp.child.yaml.j2` |
| **flows** | 网络流量分析 | `Packetbeat/flows/flows.child.yaml.j2` |

---

## 四、日志格式要求

### 4.1 格式灵活性

**BlueKing Lite 对日志内容格式要求非常灵活**，支持多种格式：

1. **纯文本日志**
   ```
   2025-10-20 10:30:45 INFO Application started successfully
   2025-10-20 10:31:12 ERROR Failed to connect to database
   ```

2. **JSON 格式日志**
   ```json
   {"timestamp":"2025-10-20T10:30:45Z","level":"INFO","message":"Application started"}
   {"timestamp":"2025-10-20T10:31:12Z","level":"ERROR","message":"Database error"}
   ```

3. **多行日志（如 Java 堆栈跟踪）**
   ```
   ERROR [2025-10-20 10:32:00] Exception occurred
   java.lang.NullPointerException: Cannot invoke method
       at com.example.Service.process(Service.java:45)
       at com.example.Controller.handle(Controller.java:23)
   ```

### 4.2 自动添加的元数据字段

系统会自动为每条日志添加以下元数据（无需在原始日志中包含）：

| 字段 | 说明 | 示例值 |
|-----|------|--------|
| `collector` | 采集器名称 | `Vector`, `Filebeat` |
| `collect_type` | 采集类型 | `file`, `syslog`, `docker` |
| `instance_id` | 采集实例 ID | `uuid-1234-5678` |
| `host` / `hostname` | 主机信息 | `web-server-01` |
| `timestamp` | 时间戳 | `2025-10-20T10:30:45Z` |
| `message` | 日志消息内容 | 原始日志内容 |
| `file` | 日志文件路径 | `/var/log/app/app.log` |
| `source_type` | 来源类型 | `file`, `syslog` |

### 4.3 多行日志处理配置

#### Vector 多行配置示例

**位置**：`web/src/app/log/hooks/integration/collectors/vector/file.tsx:30-36`

```javascript
multiline: {
  enabled: true,
  mode: 'continue_through',  // 继续模式
  start_pattern: '^(ERROR|WARN|INFO|DEBUG|TRACE|FATAL)\\s\\[',  // 日志起始模式
  timeout_ms: 3000,  // 超时时间
  condition_pattern: '^(\\s+|Traceback|File\\s+)',  // 继续条件
}
```

**常见多行模式**：

1. **Java 异常堆栈**
   ```toml
   multiline.start_pattern = '^\d{4}-\d{2}-\d{2}'
   multiline.mode = "continue_through"
   multiline.condition_pattern = '^\s+'
   ```

2. **Python Traceback**
   ```toml
   multiline.start_pattern = '^Traceback'
   multiline.mode = "halt_with"
   ```

3. **日志级别开头**
   ```toml
   multiline.start_pattern = '^(ERROR|WARN|INFO|DEBUG)'
   multiline.mode = "continue_through"
   ```

### 4.4 日志过滤和处理

#### 内容过滤（Filebeat）

```yaml
# 仅包含匹配的日志行
include_lines: ['ERROR', 'WARN', 'FATAL']

# 排除匹配的日志行
exclude_lines: ['DEBUG', 'TRACE']
```

#### 文件过滤

```yaml
# 排除文件模式
prospector.scanner.exclude_files: ['.gz$', '.zip$']

# 忽略过旧文件
ignore_older: 24h
```

---

## 五、实现步骤

### 5.1 Windows 服务器日志采集

#### 步骤 1：准备目标服务器

1. **确认日志文件位置**
   ```
   例如：C:\logs\app\application.log
         C:\inetpub\logs\LogFiles\*.log
   ```

2. **确认服务器网络连通性**
   - 能够访问 BlueKing Lite 的 NATS 服务（默认端口 4222）

#### 步骤 2：在 Web 界面添加 Windows 节点

1. 访问「节点管理」模块
2. 点击「添加节点」
3. 填写节点信息：
   - **节点名称**：`windows-web-01`
   - **IP 地址**：`192.168.1.100`
   - **操作系统类型**：选择 `Windows`
   - **采集器配置目录**：`C:\fusion-collectors`
4. 保存节点信息

#### 步骤 3：部署采集器

**方式一：使用 Vector（推荐）**

1. 在 Windows 服务器上下载 Vector：
   ```powershell
   # 下载 Vector Windows 版本
   # https://github.com/vectordotdev/vector/releases
   ```

2. 安装 Vector 为 Windows 服务

3. 配置 Vector 连接到 NATS（环境变量）：
   ```
   NATS_PROTOCOL=nats
   NATS_SERVERS=192.168.1.10:4222
   NATS_USERNAME=admin
   NATS_PASSWORD=password
   ```

**方式二：使用 Filebeat**

1. 下载 Filebeat Windows 版本
2. 配置 Filebeat 连接到 BlueKing Lite

#### 步骤 4：在 Web 界面配置日志采集

1. 访问「日志管理」→「集成」→「接入」
2. 点击「新建接入」
3. 选择采集器和类型：
   - **采集器**：`Vector`
   - **采集类型**：`file`（文件日志）
4. 配置采集参数：
   - **实例名称**：`windows-app-logs`
   - **日志文件路径**：`C:\logs\app\*.log`
   - **目标节点**：选择 `windows-web-01`
5. （可选）配置多行日志：
   - 启用多行处理
   - 配置起始模式正则表达式
6. 保存配置

#### 步骤 5：验证采集

1. 访问「日志管理」→「集成」→「列表」
2. 查看采集实例状态是否为「正常」
3. 访问「日志管理」→「检索」
4. 使用 LogSQL 查询日志：
   ```sql
   instance_id: "实例ID" | limit 100
   ```

### 5.2 Linux 服务器日志采集

#### 步骤 1：准备目标服务器

1. **确认日志文件位置**
   ```bash
   # 应用日志
   /var/log/app/application.log

   # 系统日志
   /var/log/syslog
   /var/log/messages

   # Nginx 日志
   /var/log/nginx/access.log
   /var/log/nginx/error.log
   ```

2. **确认网络连通性**
   ```bash
   nc -zv bklite-server 4222
   ```

#### 步骤 2：在 Web 界面添加 Linux 节点

1. 访问「节点管理」→「添加节点」
2. 填写节点信息：
   - **节点名称**：`linux-app-01`
   - **IP 地址**：`192.168.1.101`
   - **操作系统类型**：选择 `Linux`
   - **采集器配置目录**：`/opt/fusion-collectors`
3. 保存节点信息

#### 步骤 3：部署采集器

**方式一：使用 Vector（推荐）**

```bash
# 下载 Vector
curl -o /tmp/vector.tar.gz https://packages.timber.io/vector/0.xx.x/vector-0.xx.x-x86_64-unknown-linux-gnu.tar.gz

# 解压安装
tar -xzf /tmp/vector.tar.gz -C /opt/

# 配置环境变量
export NATS_PROTOCOL=nats
export NATS_SERVERS=192.168.1.10:4222
export NATS_USERNAME=admin
export NATS_PASSWORD=password

# 启动 Vector（配置文件由 BKLite 管理）
/opt/vector/bin/vector --config /opt/fusion-collectors/vector.toml
```

**方式二：使用 Filebeat**

```bash
# 安装 Filebeat
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.x.x-linux-x86_64.tar.gz
tar xzvf filebeat-8.x.x-linux-x86_64.tar.gz

# 启动 Filebeat（配置文件由 BKLite 管理）
./filebeat -c /opt/fusion-collectors/filebeat.yml
```

#### 步骤 4：在 Web 界面配置日志采集

**场景一：采集应用日志**

1. 访问「日志管理」→「集成」→「接入」
2. 配置：
   - **采集器**：`Vector`
   - **采集类型**：`file`
   - **实例名称**：`app-logs`
   - **日志文件路径**：`/var/log/app/*.log`
   - **目标节点**：`linux-app-01`

**场景二：采集系统审计日志（需要 root 权限）**

1. 配置：
   - **采集器**：`Auditbeat`
   - **采集类型**：`auditd`
   - **实例名称**：`system-audit`
   - **目标节点**：`linux-app-01`
   - **规则类别**：选择 `security` 和 `system`

**场景三：采集 Syslog**

1. 配置：
   - **采集器**：`Vector`
   - **采集类型**：`syslog`
   - **实例名称**：`syslog-collector`
   - **监听端口**：`514`
   - **目标节点**：`linux-app-01`

#### 步骤 5：验证采集

```bash
# 方式一：在 Linux 服务器上验证采集器运行状态
ps aux | grep vector
# 或
ps aux | grep filebeat

# 方式二：查看采集器日志
tail -f /var/log/vector.log

# 方式三：在 Web 界面检索日志
# 访问「日志管理」→「检索」
# 使用 LogSQL 查询
```

---

## 六、配置示例和最佳实践

### 6.1 Windows IIS 日志采集

```yaml
# Filebeat 配置示例
采集器: Filebeat
采集类型: filestream
实例名称: iis-logs
文件路径:
  - C:\inetpub\logs\LogFiles\W3SVC1\*.log
编码: utf-8
忽略旧文件: 7d
最大字节数: 10MB
```

### 6.2 Linux Nginx 日志采集（JSON 格式）

```toml
# Vector 配置示例
采集器: Vector
采集类型: file
实例名称: nginx-json-logs
文件路径: /var/log/nginx/access.json.log
```

Nginx JSON 格式配置：
```nginx
log_format json_combined escape=json
  '{'
    '"timestamp":"$time_iso8601",'
    '"remote_addr":"$remote_addr",'
    '"request":"$request",'
    '"status":$status,'
    '"body_bytes_sent":$body_bytes_sent,'
    '"http_referer":"$http_referer",'
    '"http_user_agent":"$http_user_agent"'
  '}';

access_log /var/log/nginx/access.json.log json_combined;
```

### 6.3 Java 应用日志（多行堆栈）

```javascript
// Vector file 采集配置
{
  file_path: "/var/log/tomcat/catalina.out",
  multiline: {
    enabled: true,
    mode: "continue_through",
    start_pattern: "^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}",
    condition_pattern: "^\\s+",
    timeout_ms: 5000
  }
}
```

### 6.4 Docker 容器日志采集

```yaml
采集器: Vector
采集类型: docker
实例名称: docker-app-logs
容器名称: app-container
包含容器: ["app-*", "web-*"]
排除容器: ["sidecar-*"]
```

### 6.5 Windows 事件日志采集

虽然系统主要面向文件日志，但可以通过以下方式采集 Windows 事件日志：

1. 使用 Vector 的 `exec` 类型
2. 编写 PowerShell 脚本定期导出事件日志为文件
3. 使用 Vector file 采集导出的日志文件

---

## 七、数据模型和查询

### 7.1 数据库模型

**位置**：`server/apps/log/models/`

#### 采集类型模型（CollectType）

```python
# server/apps/log/models/collect_type.py
class CollectType(TimeInfo, MaintainerInfo):
    name = models.CharField(max_length=100, verbose_name='采集方式')
    collector = models.CharField(max_length=100, verbose_name='采集器')
    icon = models.CharField(max_length=100, verbose_name='图标')
    description = models.TextField(blank=True, verbose_name='描述')
    default_query = models.TextField(blank=True, verbose_name='默认查询语句')
    attrs = models.JSONField(default=list, verbose_name='属性列表')
```

#### 采集实例模型（CollectInstance）

```python
# server/apps/log/models/instance.py
class CollectInstance(TimeInfo, MaintainerInfo):
    id = models.CharField(primary_key=True, max_length=200, verbose_name='采集方式实例ID')
    name = models.CharField(max_length=200, verbose_name='采集方式实例名称')
    collect_type = models.ForeignKey(CollectType, on_delete=models.CASCADE)
    node_id = models.CharField(max_length=100, verbose_name='Node ID')
```

#### 日志分组模型（LogGroup）

```python
# server/apps/log/models/log_group.py
class LogGroup(TimeInfo, MaintainerInfo):
    id = models.CharField(primary_key=True, max_length=200, verbose_name='日志分组ID')
    name = models.CharField(max_length=200, verbose_name='日志分组名称')
    rule = models.JSONField(default=dict, verbose_name='规则')
    description = models.TextField(blank=True, verbose_name='描述')
```

#### 告警策略模型（Policy）

```python
# server/apps/log/models/policy.py
class Policy(TimeInfo, MaintainerInfo):
    name = models.CharField(max_length=255, verbose_name="策略名称")
    collect_type = models.ForeignKey(CollectType, on_delete=models.CASCADE)
    log_groups = models.JSONField(default=list, verbose_name="日志分组范围")
    alert_type = models.CharField(max_length=50, verbose_name="告警类型")
    alert_condition = models.JSONField(default=dict, verbose_name="告警条件")
    notice_users = models.JSONField(default=list, verbose_name="通知人")
```

### 7.2 日志查询（VictoriaLogs）

**位置**：`server/apps/log/utils/query_log.py`

#### VictoriaMetrics API 封装

```python
class VictoriaMetricsAPI:
    def __init__(self):
        self.host = VICTORIALOGS_HOST
        self.username = VICTORIALOGS_USER
        self.password = VICTORIALOGS_PWD

    def query(self, query, start, end, limit=10):
        """查询日志"""
        data = {"query": query, "start": start, "end": end, "limit": limit}
        response = requests.post(
            f"{self.host}/select/logsql/query",
            params=data,
            auth=(self.username, self.password),
        )
        return response.json()

    def hits(self, query, start, end, field, fields_limit=5, step="5m"):
        """查询日志命中数（用于统计图表）"""
        # ...

    async def tail_async(self, query):
        """异步实时日志流"""
        # ...
```

### 7.3 LogSQL 查询语法示例

```sql
-- 查询特定实例的日志
instance_id: "uuid-1234" | limit 100

-- 查询特定采集类型
collect_type: file | limit 50

-- 查询包含错误的日志
message: *error* OR message: *exception* | limit 100

-- 按字段分组统计
collect_type: file | stats count by host | sort by count desc

-- 时间范围查询（在 Web 界面通过时间选择器控制）
-- 由 start 和 end 参数控制

-- 多条件查询
collect_type: file AND host: "web-01" AND message: *error*

-- 分区查询（获取每个实例的最新日志）
collect_type: file | last 1 by (_time) partition by (instance_id)
```

---

## 八、配置管理和部署流程

### 8.1 插件式配置管理

**位置**：`server/apps/log/plugins/`

系统采用插件式架构管理采集配置：

```
plugins/
├── Vector/
│   ├── file/
│   │   ├── collect_type.json      # 采集类型定义
│   │   └── file.child.toml.j2     # Jinja2 模板
│   ├── syslog/
│   ├── docker/
│   └── exec/
├── Filebeat/
│   └── filestream/
│       ├── collect_type.json
│       └── filestream.child.yaml.j2
├── Auditbeat/
│   ├── auditd/
│   └── file_integrity/
├── Metricbeat/
│   ├── system/
│   └── docker/
└── Packetbeat/
    ├── http/
    ├── dns/
    └── ...
```

### 8.2 配置模板渲染流程

**位置**：`server/apps/log/plugins/controller.py`

```python
class Controller:
    def controller(self):
        """生成并部署采集配置"""
        configs = self.format_configs()
        for config_info in configs:
            # 1. 查找模板
            template_dir = os.path.join(
                PLUGIN_DIRECTORY,
                config_info["collector"],
                config_info["collect_type"]
            )

            # 2. 渲染模板（Jinja2）
            template_config = self.render_template(
                template_dir,
                f"{type}.{config_type}.{file_type}.j2",
                context={**config_info, "instance_id": instance_id}
            )

            # 3. 通过 NodeMgmt RPC 下发配置到目标节点
            NodeMgmt().batch_add_node_config(node_configs)
            NodeMgmt().batch_add_node_child_config(node_child_configs)

            # 4. 记录配置关系到数据库
            CollectConfig.objects.bulk_create(collect_configs)
```

### 8.3 配置下发流程

```
Web 界面配置
     │
     ▼
Django 后端接收
     │
     ▼
Controller 渲染 Jinja2 模板
     │
     ▼
NodeMgmt RPC 调用
     │
     ▼
配置文件写入目标节点
     │
     ▼
采集器读取配置并重新加载
     │
     ▼
开始采集日志
```

### 8.4 初始化和迁移

**位置**：`server/apps/log/management/commands/log_init.py`

```python
class Command(BaseCommand):
    help = "日志插件初始化命令"

    def handle(self, *args, **options):
        # 1. 迁移采集类型（从 JSON 配置文件导入到数据库）
        migrate_collect_type()

        # 2. 初始化默认日志分组
        init_stream()
```

初始化命令：
```bash
cd server
uv run python manage.py log_init
```

---

## 九、告警和通知

### 9.1 告警策略配置

**位置**：`server/apps/log/models/policy.py`

告警策略支持：

1. **关键字告警**：日志中包含特定关键字时触发
2. **聚合告警**：基于日志数量、频率等指标
3. **周期执行**：按配置的时间间隔检查
4. **通知方式**：支持多种通知渠道

```python
class Policy(TimeInfo, MaintainerInfo):
    name = models.CharField(verbose_name="策略名称")
    collect_type = models.ForeignKey(CollectType, ...)
    log_groups = models.JSONField(verbose_name="日志分组范围")

    # 告警条件
    alert_type = models.CharField(verbose_name="告警类型")
    alert_level = models.CharField(verbose_name="告警等级")
    alert_condition = models.JSONField(verbose_name="告警条件")
    schedule = models.JSONField(verbose_name="策略执行周期")
    period = models.JSONField(verbose_name="数据检测周期")

    # 通知配置
    notice = models.BooleanField(default=True)
    notice_type = models.CharField(verbose_name="通知方式")
    notice_users = models.JSONField(verbose_name="通知人")
```

### 9.2 告警流程

```
定时任务检查策略
     │
     ▼
查询 VictoriaLogs（根据告警条件）
     │
     ▼
判断是否满足告警条件
     │
     ▼ (满足)
创建告警记录（Alert）
     │
     ▼
创建事件记录（Event）
     │
     ▼
发送通知（根据 notice_type）
     │
     ▼
记录通知结果
```

---

## 十、性能和容量规划

### 10.1 VictoriaLogs 性能特点

- **高压缩率**：比 Elasticsearch 节省 70% 存储空间
- **高查询性能**：LogSQL 查询速度快
- **低资源占用**：单机可处理大量日志

### 10.2 NATS 消息队列

- **高吞吐**：支持百万级消息/秒
- **轻量级**：低延迟、低资源占用
- **可靠性**：支持持久化和 ACK 机制

### 10.3 容量规划建议

| 日志量级 | 推荐配置 | 备注 |
|---------|---------|------|
| < 1GB/天 | 单机部署 | VictoriaLogs + NATS + Vector |
| 1-10GB/天 | 标准配置 | 4核8G，SSD 存储 |
| 10-100GB/天 | 增强配置 | 8核16G，NVMe 存储，考虑集群 |
| > 100GB/天 | 集群部署 | 多节点 VictoriaLogs 集群 |

### 10.4 采集器性能优化

1. **Vector**
   - 调整 `buffer.max_events` 缓冲区大小
   - 使用 `batch.timeout_secs` 批量发送

2. **Filebeat**
   - 调整 `harvester_buffer_size`
   - 控制 `max_procs` 并发数

3. **网络优化**
   - 使用 NATS TLS 加密（生产环境）
   - 配置 NATS JetStream 持久化（高可靠性需求）

---

## 十一、故障排查

### 11.1 常见问题

#### 问题 1：日志未采集

**排查步骤**：

1. 检查采集器进程是否运行
   ```bash
   ps aux | grep vector
   # 或
   Get-Process | Where-Object {$_.Name -like "*vector*"}  # Windows
   ```

2. 检查配置文件是否正确
   ```bash
   cat /opt/fusion-collectors/vector.toml
   ```

3. 检查采集器日志
   ```bash
   tail -f /var/log/vector.log
   ```

4. 检查 NATS 连接
   ```bash
   nc -zv <bklite-server> 4222
   ```

5. 检查文件路径和权限
   ```bash
   ls -la /var/log/app/*.log
   # 确保采集器有读取权限
   ```

#### 问题 2：日志延迟高

**可能原因**：

1. NATS 队列积压
2. VictoriaLogs 写入慢
3. 采集器缓冲区配置过小
4. 网络带宽不足

**解决方案**：

1. 检查 NATS 监控指标
2. 检查 VictoriaLogs 资源使用
3. 调整采集器批量发送配置
4. 增加网络带宽或压缩传输

#### 问题 3：多行日志未正确合并

**解决方案**：

1. 检查 `multiline.start_pattern` 正则表达式
2. 调整 `multiline.timeout_ms` 超时时间
3. 使用 `multiline.mode` 正确模式：
   - `continue_through`: 继续直到不匹配
   - `halt_with`: 遇到模式停止
   - `halt_before`: 在模式前停止

#### 问题 4：Windows 路径问题

**注意事项**：

1. Windows 路径使用反斜杠或双反斜杠
   ```toml
   include = ["C:\\logs\\app\\*.log"]
   # 或
   include = ["C:/logs/app/*.log"]
   ```

2. 确保路径存在且采集器有权限访问

### 11.2 调试技巧

1. **启用 Vector 详细日志**
   ```bash
   VECTOR_LOG=debug /opt/vector/bin/vector --config config.toml
   ```

2. **使用 LogSQL 验证数据**
   ```sql
   -- 检查最近的日志
   * | limit 10

   -- 检查特定实例
   instance_id: "uuid" | limit 10

   -- 检查字段映射
   collect_type: file | fields collector, instance_id, host | limit 10
   ```

3. **查看 VictoriaLogs 原始数据**
   ```bash
   curl -u admin:password "http://localhost:9428/select/logsql/query?query=*&limit=10"
   ```

---

## 十二、安全最佳实践

### 12.1 传输安全

1. **使用 NATS TLS**
   ```toml
   [sinks.vmlogs.tls]
   enabled = true
   verify_certificate = true
   ca_file = "/path/to/ca.pem"
   ```

2. **使用强密码**
   - NATS 用户密码
   - VictoriaLogs 认证密码

### 12.2 访问控制

1. **节点权限管理**
   - 通过组织（Organization）隔离不同团队的日志
   - 使用 `NodeOrganization` 和 `LogGroupOrganization` 模型

2. **日志敏感信息脱敏**
   - 在采集器端使用 `remap` 转换脱敏
   - 过滤敏感字段

```toml
[transforms.sanitize]
type = "remap"
inputs = ["file_source"]
source = '''
.message = replace(.message, r'\d{16}', "****CARD****")  # 脱敏信用卡号
.message = replace(.message, r'\b[\w\.-]+@[\w\.-]+\.\w+\b', "****EMAIL****")  # 脱敏邮箱
'''
```

### 12.3 审计日志

使用 Auditbeat 采集系统审计日志，确保合规性：

```yaml
采集器: Auditbeat
采集类型: auditd
规则类别:
  - security  # 监控安全相关操作
  - system    # 监控系统文件变更
```

---

## 十三、总结

### 13.1 核心优势

1. **跨平台支持**：完全支持 Windows 和 Linux
2. **灵活的采集方式**：多种采集器适应不同场景
3. **无格式限制**：支持纯文本、JSON、多行日志等多种格式
4. **高性能存储**：基于 VictoriaLogs 的高效日志存储
5. **强大的查询能力**：LogSQL 提供灵活的日志检索
6. **完善的告警机制**：支持关键字和聚合告警

### 13.2 技术架构亮点

1. **解耦设计**：采集端、传输层、存储层分离
2. **插件化管理**：采集配置通过插件模板管理
3. **自动化部署**：配置自动下发和生效
4. **可扩展性**：支持水平扩展

### 13.3 适用场景

- ✅ 应用日志采集和分析
- ✅ 系统审计和安全监控
- ✅ 容器日志采集
- ✅ 网络流量分析
- ✅ 多环境日志统一管理
- ✅ 混合操作系统环境

---

## 附录

### A. 相关代码文件索引

| 功能模块 | 关键文件路径 |
|---------|------------|
| 日志模型 | `server/apps/log/models/` |
| 采集插件 | `server/apps/log/plugins/` |
| 配置控制器 | `server/apps/log/plugins/controller.py` |
| 日志查询 | `server/apps/log/utils/query_log.py` |
| NATS 接口 | `server/apps/log/nats/log.py` |
| Web 前端 | `web/src/app/log/` |
| Vector 配置 | `deploy/docker-compose/conf/vector/vector.yaml` |
| 节点管理 | `server/apps/node_mgmt/models/sidecar.py` |

### B. 参考链接

- [BlueKing Lite 开发文档](../DEVELOPMENT.md)
- [Vector 官方文档](https://vector.dev/docs/)
- [Filebeat 官方文档](https://www.elastic.co/guide/en/beats/filebeat/current/index.html)
- [VictoriaLogs 文档](https://docs.victoriametrics.com/VictoriaLogs/)
- [NATS 文档](https://docs.nats.io/)

### C. 下一步研究方向

1. 日志采集性能优化和压测
2. 大规模集群部署方案
3. 日志数据生命周期管理
4. 自定义采集器插件开发
5. 日志数据可视化和分析

---

**文档结束**

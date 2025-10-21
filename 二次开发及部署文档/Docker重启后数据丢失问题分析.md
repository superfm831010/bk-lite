# Docker 重启后探针数据丢失问题分析与解决

## 文档信息

- **问题日期**: 2025-10-21
- **严重程度**: 🔴 高危（导致生产数据丢失）
- **影响范围**: 手动上传的探针包、节点安装记录
- **版本**: 1.0.0

---

## 一、问题现象

### 1.1 问题描述

执行 `docker-compose down -v` 重启服务后，发现：

1. ❌ **探针包列表为空** - 之前上传的控制器包和采集器包都不见了
2. ❌ **已安装的节点记录丢失** - 之前安装探针的服务器记录消失
3. ❌ **安装历史记录清空** - 所有安装任务和日志都不见了
4. ✅ **系统预置数据仍在** - 采集器定义、控制器定义等自动初始化的数据还在

### 1.2 数据库状态对比

#### 重启前（预期状态）
```sql
SELECT COUNT(*) FROM node_mgmt_packageversion;
-- 预期: 8 条（1个控制器 + 7个采集器）

SELECT COUNT(*) FROM node_mgmt_node;
-- 预期: N 条（已安装探针的节点）

SELECT COUNT(*) FROM node_mgmt_nodecollectorinstallstatus;
-- 预期: M 条（采集器安装状态）
```

#### 重启后（实际状态）
```sql
SELECT COUNT(*) FROM node_mgmt_packageversion;
-- 结果: 0 条 ❌

SELECT COUNT(*) FROM node_mgmt_node;
-- 结果: 0 条 ❌

SELECT COUNT(*) FROM node_mgmt_nodecollectorinstallstatus;
-- 结果: 0 条 ❌

-- 但是系统预置数据还在：
SELECT COUNT(*) FROM node_mgmt_collector;
-- 结果: 28 条 ✅（采集器定义）

SELECT COUNT(*) FROM node_mgmt_controller;
-- 结果: 2 条 ✅（控制器定义）
```

---

## 二、根本原因分析

### 2.1 命令对比

#### ❌ 错误的重启方式
```bash
docker-compose down -v
```

**`-v` 参数的作用**：
- 删除 `docker-compose.yml` 中定义的所有**命名卷（named volumes）**
- 删除容器自动创建的匿名卷
- **这会永久删除所有数据！**

#### ✅ 正确的重启方式

```bash
# 方式 1: 只重启容器（最安全）
docker-compose restart

# 方式 2: 停止并重新创建容器（保留数据卷）
docker-compose down
docker-compose up -d

# 方式 3: 重启单个服务
docker-compose restart server
```

### 2.2 数据丢失机制

当执行 `docker-compose down -v` 时：

```
1. 停止所有容器
   ↓
2. 删除所有容器
   ↓
3. 删除所有命名卷 (-v 参数)
   ├─ huangpu_postgres  ← PostgreSQL 数据 ❌
   ├─ huangpu_minio     ← MinIO 文件 ❌
   ├─ huangpu_nats      ← NATS 数据 ❌
   └─ ... (其他卷)
   ↓
4. 重新启动时，数据卷被重新创建（空的）
   ↓
5. 系统自动初始化预置数据
   ├─ 采集器定义 ✅
   ├─ 控制器定义 ✅
   └─ 云区域配置 ✅
   ↓
6. 但手动上传的数据不会恢复
   ├─ PackageVersion ❌
   ├─ Node ❌
   └─ 安装记录 ❌
```

### 2.3 为什么有些数据还在？

**系统预置数据还在的原因**：

这些数据是通过 Django 的初始化命令（management commands）自动创建的，在容器启动时会自动执行：

```python
# server/config/settings.py
INSTALLED_APPS = [
    'apps.node_mgmt',  # 会执行 node_init 命令
    'apps.monitor',    # 会执行 plugin_init 命令
    # ...
]
```

服务启动流程：
1. 容器启动
2. 运行数据库迁移（migrate）
3. 执行初始化命令（如 `node_init`）← 这里重建了系统预置数据
4. 启动 Web 服务

**手动上传的数据丢失的原因**：

这些数据是用户操作产生的，不在自动初始化范围内：
- 探针包上传（通过 API 或脚本）
- 节点安装（通过界面操作）
- 配置修改（用户自定义配置）

---

## 三、影响评估

### 3.1 数据丢失范围

| 数据类型 | 丢失状态 | 影响 | 恢复方式 |
|---------|---------|------|---------|
| 探针包版本 | ❌ 完全丢失 | 无法安装探针 | 重新上传 |
| 已安装节点 | ❌ 完全丢失 | 节点列表为空 | 重新安装 |
| 安装历史 | ❌ 完全丢失 | 无法追溯 | 无法恢复 |
| 采集器配置 | ❌ 完全丢失 | 配置重置 | 重新配置 |
| 监控数据 | ❌ 完全丢失 | 历史数据消失 | 无法恢复 |
| 系统配置 | ❌ 部分丢失 | 需重新配置 | 重新配置 |
| 用户数据 | ❌ 完全丢失 | 账号消失 | 重新创建 |

### 3.2 业务影响

1. **监控中断** - 所有已安装的探针失联
2. **数据断层** - 历史监控数据全部丢失
3. **重复工作** - 需要重新配置和安装
4. **用户体验** - 所有自定义配置丢失

---

## 四、解决方案

### 4.1 快速恢复步骤

#### 步骤 1: 重新上传探针包

```bash
cd /home/soft/bk-lite/deploy-huangpu/

# 1. 初始化控制器包
./init-probe-packages.sh --auto

# 2. 初始化采集器包
./init-collector-packages.sh
```

#### 步骤 2: 验证恢复结果

```bash
# 检查包版本记录
docker exec bklite-postgres-prod env PGPASSWORD=bklite psql -U postgres -d bklite -c \
  "SELECT COUNT(*) as total, type FROM node_mgmt_packageversion GROUP BY type;"

# 预期输出：
#  total |    type
# -------+------------
#      1 | controller
#      7 | collector
```

#### 步骤 3: 重新配置系统（如需要）

1. **重置管理员密码**（如果丢失）：
   ```bash
   docker exec bklite-server-prod bash -c \
     "cd /apps && source .venv/bin/activate && \
      python manage.py createsuperuser"
   ```

2. **重新配置云区域**（如需要）
3. **重新安装探针到目标节点**
4. **重新配置采集器**

### 4.2 完整恢复脚本

为方便恢复，可以创建一个一键恢复脚本：

```bash
#!/bin/bash
# restore-after-down-v.sh

echo "检测到数据可能丢失，开始恢复..."

# 1. 恢复探针包
cd /home/soft/bk-lite/deploy-huangpu/
./init-probe-packages.sh --auto
./init-collector-packages.sh

# 2. 验证
echo "验证恢复结果："
docker exec bklite-postgres-prod env PGPASSWORD=bklite psql -U postgres -d bklite -c \
  "SELECT type, COUNT(*) FROM node_mgmt_packageversion GROUP BY type;"

echo "恢复完成！请手动重新安装探针到目标节点。"
```

---

## 五、预防措施

### 5.1 正确的运维操作规范

#### 日常重启操作

```bash
# ✅ 推荐：只重启容器
docker-compose restart

# ✅ 可以：重新创建容器但保留数据
docker-compose down
docker-compose up -d

# ⚠️ 谨慎：只在需要时使用
docker-compose stop
docker-compose start
```

#### 需要清理数据时

```bash
# ⚠️ 危险操作：删除所有数据
# 仅在以下情况使用：
# 1. 测试环境重置
# 2. 确认不需要任何数据
# 3. 已做好数据备份

# 删除前提示
echo "警告：此操作将删除所有数据！"
read -p "确认继续？(yes/no) " confirm

if [ "$confirm" = "yes" ]; then
    docker-compose down -v
else
    echo "已取消"
fi
```

### 5.2 数据备份策略

#### 自动备份脚本

```bash
#!/bin/bash
# backup-bklite-data.sh

BACKUP_DIR="/backup/bklite/$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

# 1. 备份数据库
docker exec bklite-postgres-prod pg_dump -U postgres bklite > \
  "$BACKUP_DIR/database.sql"

# 2. 备份 MinIO 数据（如果使用）
# docker exec bklite-minio-prod tar czf - /data > \
#   "$BACKUP_DIR/minio-data.tar.gz"

# 3. 备份配置文件
cp -r /home/soft/bk-lite/deploy-huangpu/conf "$BACKUP_DIR/"
cp /home/soft/bk-lite/deploy-huangpu/.secrets "$BACKUP_DIR/"

echo "备份完成: $BACKUP_DIR"
```

#### 定时备份（Cron）

```bash
# 添加到 crontab
# 每天凌晨 2 点备份
0 2 * * * /home/soft/bk-lite/deploy-huangpu/backup-bklite-data.sh
```

### 5.3 持久化验证清单

在部署后检查持久化配置：

```bash
# 1. 检查数据卷配置
docker-compose config | grep -A 5 "volumes:"

# 2. 检查数据卷是否创建
docker volume ls | grep huangpu

# 3. 检查数据卷挂载
docker inspect bklite-postgres-prod | grep -A 10 "Mounts"

# 4. 测试重启后数据保留
# 4.1 添加测试数据
# 4.2 执行 docker-compose restart
# 4.3 验证数据仍然存在
```

---

## 六、改进建议

### 6.1 系统层面改进

#### 方案 1: 自动检测和恢复

在 `deploy.sh` 中添加数据丢失检测：

```bash
# deploy.sh 中添加
check_and_restore_data() {
    echo "检查数据完整性..."

    # 检查探针包数量
    pkg_count=$(docker exec bklite-postgres-prod env PGPASSWORD=bklite \
        psql -U postgres -d bklite -t -c \
        "SELECT COUNT(*) FROM node_mgmt_packageversion;" | tr -d ' ')

    if [ "$pkg_count" -eq 0 ]; then
        echo "检测到探针包数据丢失，自动恢复..."
        ./init-probe-packages.sh --auto
        ./init-collector-packages.sh
    else
        echo "数据完整，探针包数量: $pkg_count"
    fi
}

# 在服务启动后调用
check_and_restore_data
```

#### 方案 2: 启动时自动初始化

修改 Server 容器的启动脚本，在服务启动后自动检查并初始化探针包。

### 6.2 运维层面改进

#### 建立操作规范文档

1. **操作手册**
   - 日常运维命令清单
   - 危险操作警告
   - 回滚步骤

2. **应急预案**
   - 数据丢失快速恢复流程
   - 服务故障处理流程
   - 联系人和升级机制

3. **变更管理**
   - 变更前备份
   - 变更审批流程
   - 变更回滚计划

#### 监控和告警

设置数据完整性监控：
```bash
# 监控脚本：check-data-integrity.sh
#!/bin/bash

pkg_count=$(docker exec bklite-postgres-prod env PGPASSWORD=bklite \
    psql -U postgres -d bklite -t -c \
    "SELECT COUNT(*) FROM node_mgmt_packageversion;" | tr -d ' ')

if [ "$pkg_count" -eq 0 ]; then
    echo "告警：探针包数据为空！"
    # 发送告警通知
fi
```

---

## 七、经验教训

### 7.1 关键要点

1. ⚠️ **永远不要在生产环境使用 `docker-compose down -v`**
2. ✅ **使用 `docker-compose restart` 进行日常重启**
3. ✅ **任何重大操作前都要备份数据**
4. ✅ **建立数据恢复预案和脚本**
5. ✅ **定期测试备份和恢复流程**

### 7.2 Docker Compose 命令安全等级

| 命令 | 安全等级 | 数据影响 | 使用场景 |
|------|---------|---------|---------|
| `docker-compose restart` | 🟢 安全 | 无影响 | 日常重启 |
| `docker-compose stop/start` | 🟢 安全 | 无影响 | 临时停止 |
| `docker-compose down && up -d` | 🟡 注意 | 无影响 | 更新配置 |
| `docker-compose down -v` | 🔴 危险 | **删除所有数据** | 仅测试环境 |
| `docker volume rm` | 🔴 危险 | **删除指定数据** | 谨慎操作 |

---

## 八、快速参考

### 8.1 常用命令

```bash
# 查看数据卷
docker volume ls

# 检查探针包数量
docker exec bklite-postgres-prod env PGPASSWORD=bklite psql -U postgres -d bklite -c \
  "SELECT COUNT(*) FROM node_mgmt_packageversion;"

# 重新初始化探针包
cd /home/soft/bk-lite/deploy-huangpu/
./init-probe-packages.sh --auto
./init-collector-packages.sh

# 备份数据库
docker exec bklite-postgres-prod pg_dump -U postgres bklite > backup.sql

# 恢复数据库
docker exec -i bklite-postgres-prod psql -U postgres bklite < backup.sql
```

### 8.2 故障排查流程

```
1. 发现问题
   ↓
2. 检查数据是否丢失
   SELECT COUNT(*) FROM node_mgmt_packageversion;
   ↓
3. 确认是否执行过 docker-compose down -v
   ↓
4. 运行恢复脚本
   ./init-probe-packages.sh --auto
   ./init-collector-packages.sh
   ↓
5. 验证恢复结果
   ↓
6. 重新配置和安装探针
```

---

## 九、相关文档

- [探针包初始化配置指南](./探针包初始化配置指南.md)
- [已上传插件功能说明](./已上传插件功能说明.md)
- [内网离线部署方案](./内网离线部署方案.md)

---

## 十、总结

这次数据丢失事件的根本原因是误用了 `docker-compose down -v` 命令。该命令会删除所有数据卷，导致包括探针包、节点记录在内的所有手动数据丢失。

**关键教训**：
1. 生产环境禁用 `-v` 参数
2. 建立完善的备份机制
3. 制定明确的操作规范
4. 准备数据恢复预案

**预防措施**：
1. 使用正确的重启命令
2. 定期自动备份数据
3. 建立数据完整性监控
4. 编写自动恢复脚本

通过这些措施，可以有效避免类似问题再次发生，并在问题发生时快速恢复。

---

**文档维护**：运维团队
**最后更新**：2025-10-21
**版本**：1.0.0

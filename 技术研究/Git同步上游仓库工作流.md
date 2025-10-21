# Git 同步上游仓库工作流

## 概述

本文档介绍如何在保持二次开发内容的同时，持续同步上游仓库（TencentBlueKing/bk-lite）的更新。

## 仓库配置

### 远程仓库

当前配置了两个远程仓库：

```bash
# 查看远程仓库配置
git remote -v
```

- **origin**: `https://github.com/TencentBlueKing/bk-lite` - 上游官方仓库
- **myfork**: `https://github.com/superfm831010/bk-lite.git` - 个人 fork 仓库

## 分支策略

采用**功能分支工作流**进行管理：

### 分支说明

| 分支名称 | 用途 | 说明 |
|---------|------|------|
| `master` | 跟踪上游 | 始终保持与上游 origin/master 同步，不在此分支直接开发 |
| `huangpu-dev` | 黄埔定制开发 | 所有黄埔海关的定制化功能都在此分支开发和维护 |

### 分支工作流程图

```
origin/master (上游)
    ↓ (定期同步)
master (本地纯净分支)
    ↓ (合并更新)
huangpu-dev (开发分支)
    ↓ (日常开发)
feature/* (特性分支，可选)
```

## 初始设置（已完成）

以下是初始设置的步骤记录（已执行完成）：

### 1. 创建开发分支

```bash
# 从当前 master 创建 huangpu-dev 分支保存所有定制化内容
git branch huangpu-dev

# 确认分支创建
git branch -v
```

### 2. 重置 master 到上游

```bash
# 将 master 分支重置为上游最新版本
git reset --hard origin/master

# 确认同步状态
git log --oneline -5
```

### 3. 推送到个人仓库

```bash
# 强制推送 master（因为做了 reset）
git push myfork master --force

# 推送新的 huangpu-dev 分支
git push myfork huangpu-dev
```

### 4. 合并上游更新到开发分支

```bash
# 切换到开发分支
git checkout huangpu-dev

# 合并 master 的最新更新
git merge master --no-edit
```

## 日常工作流程

### 同步上游更新

定期（建议每周或每月）同步上游更新：

```bash
# 1. 切换到 master 分支
git checkout master

# 2. 获取上游最新更新
git fetch origin

# 3. 查看有哪些新提交
git log --oneline master..origin/master

# 4. 将 master 更新到上游最新版本
git reset --hard origin/master

# 5. 推送到个人仓库
git push myfork master --force

# 6. 切换到开发分支
git checkout huangpu-dev

# 7. 合并 master 的更新到开发分支
git merge master

# 8. 如果有冲突，解决冲突后提交
# git add .
# git commit -m "merge: 合并上游更新"

# 9. 推送更新后的开发分支
git push myfork huangpu-dev
```

### 日常开发

在 `huangpu-dev` 分支或其特性分支上进行开发：

```bash
# 切换到开发分支
git checkout huangpu-dev

# 进行开发工作
# ... 修改代码 ...

# 提交更改
git add .
git commit -m "feat: 添加新功能"

# 推送到个人仓库
git push myfork huangpu-dev
```

### 创建特性分支（可选）

对于大型功能，建议创建独立的特性分支：

```bash
# 从 huangpu-dev 创建特性分支
git checkout -b feature/new-feature huangpu-dev

# 开发完成后合并回 huangpu-dev
git checkout huangpu-dev
git merge feature/new-feature

# 删除特性分支
git branch -d feature/new-feature
```

## 部署发布

### 生产部署

```bash
# 从 huangpu-dev 分支构建和部署
git checkout huangpu-dev

# 拉取最新代码
git pull myfork huangpu-dev

# 执行部署脚本
# ./deploy-huangpu/xxx
```

### 创建发布标签

```bash
# 在 huangpu-dev 分支上创建标签
git checkout huangpu-dev
git tag -a v1.0.0-huangpu -m "黄埔海关版本 v1.0.0"
git push myfork v1.0.0-huangpu
```

## 冲突处理

### 常见冲突场景

1. **配置文件冲突**：黄埔定制的配置 vs 上游新增配置
2. **代码逻辑冲突**：黄埔修改的代码被上游也修改了
3. **依赖版本冲突**：package.json、pyproject.toml 等

### 冲突解决流程

```bash
# 1. 合并时遇到冲突
git merge master
# Auto-merging xxx
# CONFLICT (content): Merge conflict in xxx

# 2. 查看冲突文件
git status

# 3. 手动编辑冲突文件，保留需要的内容
# 冲突标记：
# <<<<<<< HEAD
# 当前分支的内容（huangpu-dev）
# =======
# 要合并的内容（master）
# >>>>>>> master

# 4. 标记冲突已解决
git add <冲突文件>

# 5. 完成合并
git commit -m "merge: 解决合并冲突"

# 6. 推送
git push myfork huangpu-dev
```

### 冲突解决策略

- **优先保留黄埔定制化内容**：涉及黄埔特定配置和功能
- **接受上游修复**：安全补丁、bug 修复
- **合并功能**：新功能可以两者结合
- **测试验证**：解决冲突后务必进行完整测试

## 最佳实践

### 1. 定期同步

- 建议每周检查一次上游更新
- 重要安全更新应立即同步

### 2. 保持提交清晰

```bash
# 好的提交消息示例
git commit -m "feat: 添加黄埔海关登录页面定制"
git commit -m "fix: 修复端口冲突问题"
git commit -m "merge: 同步上游 v1.2.0 更新"
```

### 3. 文档同步

- 在 `二次开发及部署文档/` 目录记录所有定制化修改
- 在 `技术研究/` 目录记录技术方案和调研

### 4. 代码审查

- 同步上游更新后，检查变更日志
- 测试关键功能是否正常
- 验证黄埔定制功能未受影响

### 5. 备份策略

```bash
# 在重大操作前创建备份分支
git branch backup-$(date +%Y%m%d) huangpu-dev
```

## 快速参考命令

### 查看状态

```bash
# 查看当前分支
git branch

# 查看远程仓库
git remote -v

# 查看上游新提交
git fetch origin && git log --oneline master..origin/master

# 查看本地新提交
git log --oneline origin/master..master
```

### 同步流程

```bash
# 一键同步上游（无冲突情况）
git checkout master && \
git fetch origin && \
git reset --hard origin/master && \
git push myfork master --force && \
git checkout huangpu-dev && \
git merge master && \
git push myfork huangpu-dev
```

## 故障排除

### 问题：推送被拒绝

```bash
# 错误：! [rejected] master -> master (non-fast-forward)
# 解决：使用 --force 强制推送（仅限 master 分支）
git push myfork master --force
```

### 问题：合并冲突太多

```bash
# 取消合并，重新评估
git merge --abort

# 考虑使用 rebase 或手动迁移定制内容
```

### 问题：误操作恢复

```bash
# 查看操作历史
git reflog

# 恢复到指定版本
git reset --hard HEAD@{n}
```

## 实施记录

### 首次实施时间

- **日期**: 2025-10-21
- **上游版本**: d329ee44 (Merge pull request #1204)
- **本地提交数**: 15 个黄埔定制化提交
- **上游新增提交**: 37 个
- **合并冲突**: 无

### 同步内容

本次同步包含的主要上游更新：

1. **NATS 功能增强**
   - 支持 TLS 加密连接
   - JetStream TLS 支持
   - NATS 核心代码重构

2. **移动端改进**
   - Android 构建脚本优化
   - MainActivity 全屏布局支持
   - 新增跨平台构建工具

3. **安全修复**
   - Sidecar API 认证漏洞修复
   - 节点管理 token 认证增强

4. **功能优化**
   - 安装控制器添加操作系统类型检测
   - 代理执行无限循环检测和缓解
   - 组件代码重构（密码组件统一）

5. **文档和工具**
   - 代码审查流程文档
   - 多语言支持优化

## 相关资源

- [上游仓库](https://github.com/TencentBlueKing/bk-lite)
- [个人 Fork](https://github.com/superfm831010/bk-lite)
- [Git 分支策略](https://git-scm.com/book/zh/v2/Git-分支-分支的新建与合并)
- [解决合并冲突](https://git-scm.com/book/zh/v2/Git-分支-分支的新建与合并#_基本的合并冲突)

---

**维护者**: 黄埔海关开发团队
**最后更新**: 2025-10-21

# Git 远程仓库配置说明

## 远程仓库配置

本项目配置了两个远程仓库：

### 1. origin - 上游原始仓库
- **URL**: `https://github.com/TencentBlueKing/bk-lite`
- **用途**: 上游原始仓库，用于拉取最新代码和同步更新
- **权限**: 只读，无推送权限

### 2. myfork - 个人 fork 仓库
- **URL**: `https://github.com/superfm831010/bk-lite.git`
- **用途**: 个人开发仓库，用于推送开发分支
- **权限**: 完全控制

## 查看远程仓库配置

```bash
git remote -v
```

输出：
```
myfork	https://github.com/superfm831010/bk-lite.git (fetch)
myfork	https://github.com/superfm831010/bk-lite.git (push)
origin	https://github.com/TencentBlueKing/bk-lite (fetch)
origin	https://github.com/TencentBlueKing/bk-lite (push)
```

## 推送代码到个人仓库

### 首次推送新分支

```bash
git push --set-upstream myfork <分支名>
```

例如推送 `huangpu-dev` 分支：
```bash
git push --set-upstream myfork huangpu-dev
```

### 后续推送

设置上游跟踪后，可以直接使用：
```bash
git push
```

## 同步上游代码

从上游仓库获取最新代码：

```bash
# 获取上游更新
git fetch origin

# 查看差异
git log HEAD..origin/master

# 合并到当前分支
git merge origin/master

# 或者变基（推荐用于个人开发分支）
git rebase origin/master
```

## 工作流程建议

1. **开发新功能**
   ```bash
   # 基于 master 创建新分支
   git checkout -b feature-xxx master

   # 开发并提交
   git add .
   git commit -m "feat: 添加新功能"

   # 推送到个人仓库
   git push --set-upstream myfork feature-xxx
   ```

2. **保持与上游同步**
   ```bash
   # 切换到 master 分支
   git checkout master

   # 拉取上游更新
   git pull origin master

   # 推送到个人仓库
   git push myfork master
   ```

3. **更新开发分支**
   ```bash
   # 在开发分支上
   git checkout feature-xxx

   # 变基到最新的 master
   git rebase master

   # 强制推送（因为变基改变了历史）
   git push --force-with-lease myfork feature-xxx
   ```

## 常见问题

### Q: 执行 git push 时提示 403 错误
**A**: 这是因为 git 默认推送到 origin 仓库，而你没有权限。应该明确指定推送到 myfork：
```bash
git push myfork <分支名>
```

或者设置上游跟踪：
```bash
git push --set-upstream myfork <分支名>
```

### Q: 如何修改默认推送仓库？
**A**: 可以修改默认的 push 远程仓库：
```bash
# 设置当前分支的默认推送仓库
git config branch.<分支名>.remote myfork

# 或者全局设置默认推送到 myfork
git config push.default current
```

### Q: 如何添加新的远程仓库？
**A**:
```bash
# 添加远程仓库
git remote add <名称> <URL>

# 例如
git remote add myfork https://github.com/superfm831010/bk-lite.git
```

## huangpu-dev 分支说明

- **分支名称**: `huangpu-dev`
- **用途**: 黄埔海关定制化开发分支
- **推送位置**: `myfork/huangpu-dev`
- **上游跟踪**: 已设置为 `myfork/huangpu-dev`

当前状态：
```bash
$ git push
# 会自动推送到 myfork/huangpu-dev
```

## 参考资料

- [Git Remote 官方文档](https://git-scm.com/docs/git-remote)
- [GitHub Fork 工作流](https://docs.github.com/en/get-started/quickstart/fork-a-repo)

# Git 配置说明

## 配置日期
2025-10-19

## 仓库 Remote 配置

### 当前配置

项目配置了两个 remote 仓库：

```bash
# 查看 remote 配置
git remote -v
```

输出：
```
myfork  https://github.com/superfm831010/bk-lite.git (fetch)
myfork  https://github.com/superfm831010/bk-lite.git (push)
origin  https://github.com/TencentBlueKing/bk-lite (fetch)
origin  https://github.com/TencentBlueKing/bk-lite (push)
```

### Remote 说明

| Remote 名称 | 用途 | URL |
|------------|------|-----|
| **origin** | 官方上游仓库（腾讯蓝鲸） | https://github.com/TencentBlueKing/bk-lite |
| **myfork** | 个人 fork 仓库（默认推送） | https://github.com/superfm831010/bk-lite.git |

## 推送代码到个人仓库

### 方式一：使用 Personal Access Token（推荐）

由于项目使用 HTTPS 协议，需要使用 GitHub Personal Access Token 进行认证。

#### 1. 创建 Personal Access Token

1. 登录 GitHub
2. 进入 Settings → Developer settings → Personal access tokens → Tokens (classic)
3. 点击 "Generate new token (classic)"
4. 选择权限：勾选 `repo` (Full control of private repositories)
5. 生成并复制 token（只显示一次，请妥善保存）

#### 2. 推送代码

首次推送到个人仓库：

```bash
git push -u myfork master
```

系统会提示输入用户名和密码：
- **Username**: `superfm831010` (您的 GitHub 用户名)
- **Password**: 粘贴您的 Personal Access Token（不是 GitHub 密码）

> **注意**：密码处输入的是 Token，不是 GitHub 账户密码

#### 3. 配置 Git 凭证存储

**✅ 已配置**：当前系统已配置凭证永久存储

为避免每次都输入 token，已配置凭证永久存储：

```bash
# 当前配置：永久存储凭证到本地文件
git config --global credential.helper store
```

**工作原理**：
- 首次推送时输入用户名和 Personal Access Token
- 凭证会以明文形式保存到 `~/.git-credentials` 文件
- 后续所有 Git 操作自动使用保存的凭证，无需重新输入
- 系统重启后凭证依然有效

**凭证文件位置**：`~/.git-credentials`

**安全提示**：
- ⚠️ 凭证以明文形式存储，请确保系统安全
- ⚠️ 不要将 `~/.git-credentials` 文件分享给他人
- ⚠️ 如果 token 泄露，请立即在 GitHub 上撤销并重新生成

**其他可选配置**：
```bash
# 内存缓存凭证 1 小时（更安全）
git config --global credential.helper 'cache --timeout=3600'

# 内存缓存凭证 24 小时
git config --global credential.helper 'cache --timeout=86400'

# 内存缓存凭证 7 天
git config --global credential.helper 'cache --timeout=604800'
```

### 方式二：使用 SSH（需要配置 SSH Key）

如果网络环境允许 SSH 连接，可以切换到 SSH 协议：

```bash
# 修改 myfork 为 SSH URL
git remote set-url myfork git@github.com:superfm831010/bk-lite.git

# 配置 SSH Key 后推送
git push -u myfork master
```

**SSH Key 配置步骤**：
1. 生成 SSH key：`ssh-keygen -t ed25519 -C "your_email@example.com"`
2. 将公钥添加到 GitHub：Settings → SSH and GPG keys → New SSH key
3. 测试连接：`ssh -T git@github.com`

## 日常开发工作流

### 推送本地更改

设置完成后，直接使用 `git push` 会推送到个人 fork：

```bash
# 查看当前更改
git status

# 添加更改
git add .

# 提交更改
git commit -m "描述您的更改"

# 推送到个人 fork（已设置 upstream 后）
git push
```

### 同步上游官方仓库

定期从官方仓库同步最新代码：

```bash
# 拉取官方仓库的更新
git fetch origin

# 合并官方仓库的 master 分支到本地
git merge origin/master

# 或者使用 rebase
git rebase origin/master

# 推送更新到个人 fork
git push myfork master
```

### 提交 Pull Request 到官方仓库

1. 推送代码到个人 fork：`git push myfork master`
2. 访问 https://github.com/superfm831010/bk-lite
3. 点击 "Contribute" → "Open pull request"
4. 填写 PR 描述并提交

## 常用命令参考

```bash
# 查看 remote 配置
git remote -v

# 查看当前分支状态
git status

# 查看分支跟踪关系
git branch -vv

# 修改 remote URL
git remote set-url <remote-name> <new-url>

# 拉取并合并远程分支
git pull origin master

# 推送到指定 remote
git push myfork master

# 设置分支的上游
git branch --set-upstream-to=myfork/master master
```

## 故障排查

### 问题 1：Permission denied

**错误信息**：
```
remote: Permission to TencentBlueKing/bk-lite.git denied to superfm831010.
fatal: unable to access 'https://github.com/TencentBlueKing/bk-lite/': The requested URL returned error: 403
```

**原因**：尝试推送到官方仓库，但没有写入权限。

**解决**：推送到个人 fork：
```bash
git push myfork master
```

### 问题 2：SSH 连接失败

**错误信息**：
```
kex_exchange_identification: Connection closed by remote host
Connection closed by 20.205.243.166 port 22
```

**原因**：SSH 端口被防火墙阻止或网络环境不支持。

**解决**：切换到 HTTPS 协议并使用 Personal Access Token（见上文）。

### 问题 3：每次推送都要输入密码

**解决**：配置 Git 凭证缓存：
```bash
git config --global credential.helper cache
```

## 配置历史记录

- **2025-10-19 06:00**：初始配置，设置 myfork 指向 https://github.com/superfm831010/bk-lite.git
- **2025-10-19 06:15**：尝试 SSH 失败，改用 HTTPS + Personal Access Token 方式
- **2025-10-19 06:30**：配置 Git 凭证缓存 24 小时（后改为永久存储）
- **2025-10-19 06:35**：改为凭证永久存储（credential.helper store），明文保存到 ~/.git-credentials

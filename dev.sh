#!/bin/bash
# Blueking Lite - 本地开发环境管理脚本
# 用途：一键启动/停止/管理本地开发环境

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

# PID 文件目录
PID_DIR="$PROJECT_ROOT/.dev-pids"
mkdir -p "$PID_DIR"

# 日志目录
LOG_DIR="$PROJECT_ROOT/.dev-logs"
mkdir -p "$LOG_DIR"

#=============================================================================
# 日志函数
#=============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${MAGENTA}[STEP]${NC} $1"
}

#=============================================================================
# 工具检查函数
#=============================================================================

check_command() {
    local cmd=$1
    local install_msg=$2

    if ! command -v "$cmd" &> /dev/null; then
        log_error "$cmd 未安装"
        log_info "$install_msg"
        return 1
    fi
    return 0
}

check_environment() {
    log_step "检查开发环境..."

    local all_ok=true

    # 检查 Docker
    if ! check_command docker "请安装 Docker: https://docs.docker.com/get-docker/"; then
        all_ok=false
    else
        docker_version=$(docker --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
        log_success "Docker 版本: $docker_version"
    fi

    # 检查 Docker Compose
    if ! docker compose version &> /dev/null; then
        log_error "Docker Compose 未安装或版本过低"
        log_info "请升级 Docker 到最新版本"
        all_ok=false
    else
        compose_version=$(docker compose version --short)
        log_success "Docker Compose 版本: $compose_version"
    fi

    # 检查 Python (3.12+ required for server)
    if ! check_command python3 "请安装 Python 3.12+"; then
        all_ok=false
    else
        python_version=$(python3 --version | grep -oE '[0-9]+\.[0-9]+')
        log_info "Python 版本: $python_version"
        if [[ "${python_version//./}" -lt "312" ]]; then
            log_warn "Server 需要 Python 3.12+，当前版本: $python_version"
            log_info "建议使用 pyenv 安装: https://github.com/pyenv/pyenv"
        fi
    fi

    # 检查 uv (Python package manager)
    if ! check_command uv "请安装 uv: curl -LsSf https://astral.sh/uv/install.sh | sh"; then
        log_warn "uv 未安装，将无法管理 Python 依赖"
        log_info "安装命令: curl -LsSf https://astral.sh/uv/install.sh | sh"
    else
        uv_version=$(uv --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
        log_success "uv 版本: $uv_version"
    fi

    # 检查 Node.js
    if ! check_command node "请安装 Node.js 18+: https://nodejs.org/"; then
        all_ok=false
    else
        node_version=$(node --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
        log_success "Node.js 版本: v$node_version"
    fi

    # 检查 pnpm
    if ! check_command pnpm "请安装 pnpm: npm install -g pnpm"; then
        log_warn "pnpm 未安装，将无法管理前端依赖"
        log_info "安装命令: npm install -g pnpm"
    else
        pnpm_version=$(pnpm --version)
        log_success "pnpm 版本: $pnpm_version"
    fi

    if [ "$all_ok" = true ]; then
        log_success "环境检查通过！"
        return 0
    else
        log_error "环境检查失败，请安装缺失的工具后重试"
        return 1
    fi
}

#=============================================================================
# Docker 基础设施管理
#=============================================================================

start_infra() {
    log_step "启动基础设施服务 (Docker Compose)..."

    if ! docker compose -f docker-compose.dev.yml ps | grep -q "Up"; then
        docker compose -f docker-compose.dev.yml up -d
        log_info "等待服务健康检查..."
        sleep 10

        # 检查服务状态
        docker compose -f docker-compose.dev.yml ps
        log_success "基础设施服务已启动"
    else
        log_info "基础设施服务已在运行中"
    fi
}

stop_infra() {
    log_step "停止基础设施服务..."
    docker compose -f docker-compose.dev.yml stop
    log_success "基础设施服务已停止"
}

restart_infra() {
    log_step "重启基础设施服务..."
    docker compose -f docker-compose.dev.yml restart
    log_success "基础设施服务已重启"
}

status_infra() {
    log_step "基础设施服务状态:"
    docker compose -f docker-compose.dev.yml ps
}

logs_infra() {
    local service=${1:-}
    if [ -n "$service" ]; then
        docker compose -f docker-compose.dev.yml logs -f "$service"
    else
        docker compose -f docker-compose.dev.yml logs -f
    fi
}

#=============================================================================
# Server (Django) 管理
#=============================================================================

install_server() {
    log_step "安装 Server 依赖..."
    cd "$PROJECT_ROOT/server"

    if command -v uv &> /dev/null; then
        log_info "使用 uv 安装依赖..."
        uv sync --all-groups --all-extras
    else
        log_error "uv 未安装，无法安装依赖"
        log_info "请先安装 uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
        return 1
    fi

    # 复制环境变量文件
    if [ ! -f .env ]; then
        log_info "创建 .env 配置文件..."
        cp "$PROJECT_ROOT/server/.env.dev" .env
        log_success ".env 文件已创建"
    fi

    cd "$PROJECT_ROOT"
    log_success "Server 依赖安装完成"
}

init_server_db() {
    log_step "初始化 Server 数据库..."
    cd "$PROJECT_ROOT/server"

    # 运行迁移
    log_info "运行数据库迁移..."
    uv run python manage.py makemigrations
    uv run python manage.py migrate
    uv run python manage.py createcachetable django_cache

    # 初始化服务器数据
    log_info "初始化服务器数据..."
    uv run python manage.py init_realm_resource || true
    uv run python manage.py init_login_settings || true
    uv run python manage.py create_user admin password --email=admin@bklite.net --is_superuser || true
    uv run python manage.py model_init || true
    uv run python manage.py plugin_init || true
    uv run python manage.py node_init || true
    uv run python manage.py log_init || true
    uv run python manage.py init_bot || true
    uv run python manage.py init_channel || true
    uv run python manage.py init_llm || true
    uv run python manage.py create_builtin_rules --update || true

    cd "$PROJECT_ROOT"
    log_success "Server 数据库初始化完成"
    log_info "管理员账户: admin / password"
}

start_server() {
    log_step "启动 Server 开发服务器..."

    if [ -f "$PID_DIR/server.pid" ] && kill -0 $(cat "$PID_DIR/server.pid") 2>/dev/null; then
        log_warn "Server 已在运行中 (PID: $(cat $PID_DIR/server.pid))"
        return 0
    fi

    cd "$PROJECT_ROOT/server"
    nohup uv run uvicorn asgi:application --host 0.0.0.0 --port 8001 --reload > "$LOG_DIR/server.log" 2>&1 &
    echo $! > "$PID_DIR/server.pid"
    cd "$PROJECT_ROOT"

    log_success "Server 已启动 (PID: $(cat $PID_DIR/server.pid))"
    log_info "访问地址: http://localhost:8001"
    log_info "日志文件: $LOG_DIR/server.log"
}

stop_server() {
    log_step "停止 Server..."

    if [ -f "$PID_DIR/server.pid" ]; then
        local pid=$(cat "$PID_DIR/server.pid")
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid"
            rm "$PID_DIR/server.pid"
            log_success "Server 已停止"
        else
            log_warn "Server 进程不存在"
            rm "$PID_DIR/server.pid"
        fi
    else
        log_warn "Server 未在运行"
    fi
}

logs_server() {
    if [ -f "$LOG_DIR/server.log" ]; then
        tail -f "$LOG_DIR/server.log"
    else
        log_error "日志文件不存在: $LOG_DIR/server.log"
    fi
}

#=============================================================================
# Web (Next.js) 管理
#=============================================================================

install_web() {
    log_step "安装 Web 依赖..."
    cd "$PROJECT_ROOT/web"

    if command -v pnpm &> /dev/null; then
        log_info "使用 pnpm 安装依赖..."
        pnpm install
    else
        log_error "pnpm 未安装，无法安装依赖"
        log_info "请先安装 pnpm: npm install -g pnpm"
        return 1
    fi

    # 复制环境变量文件
    if [ ! -f .env.local ]; then
        log_info "创建 .env.local 配置文件..."
        cp "$PROJECT_ROOT/web/.env.local.dev" .env.local
        log_success ".env.local 文件已创建"
    fi

    cd "$PROJECT_ROOT"
    log_success "Web 依赖安装完成"
}

start_web() {
    log_step "启动 Web 开发服务器..."

    if [ -f "$PID_DIR/web.pid" ] && kill -0 $(cat "$PID_DIR/web.pid") 2>/dev/null; then
        log_warn "Web 已在运行中 (PID: $(cat $PID_DIR/web.pid))"
        return 0
    fi

    cd "$PROJECT_ROOT/web"
    nohup pnpm dev > "$LOG_DIR/web.log" 2>&1 &
    echo $! > "$PID_DIR/web.pid"
    cd "$PROJECT_ROOT"

    log_success "Web 已启动 (PID: $(cat $PID_DIR/web.pid))"
    log_info "访问地址: http://localhost:3000"
    log_info "日志文件: $LOG_DIR/web.log"
}

stop_web() {
    log_step "停止 Web..."

    if [ -f "$PID_DIR/web.pid" ]; then
        local pid=$(cat "$PID_DIR/web.pid")
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid"
            rm "$PID_DIR/web.pid"
            log_success "Web 已停止"
        else
            log_warn "Web 进程不存在"
            rm "$PID_DIR/web.pid"
        fi
    else
        log_warn "Web 未在运行"
    fi
}

logs_web() {
    if [ -f "$LOG_DIR/web.log" ]; then
        tail -f "$LOG_DIR/web.log"
    else
        log_error "日志文件不存在: $LOG_DIR/web.log"
    fi
}

#=============================================================================
# 综合管理命令
#=============================================================================

install_all() {
    log_step "安装所有依赖..."
    install_server
    install_web
    log_success "所有依赖安装完成"
}

start_all() {
    log_step "启动所有服务..."
    start_infra
    sleep 5
    start_server
    sleep 3
    start_web
    log_success "所有服务已启动"
    show_status
}

stop_all() {
    log_step "停止所有服务..."
    stop_web
    stop_server
    stop_infra
    log_success "所有服务已停止"
}

restart_all() {
    log_step "重启所有服务..."
    stop_all
    sleep 2
    start_all
}

show_status() {
    echo ""
    log_step "=== 服务状态 ==="
    echo ""

    # Docker 服务状态
    echo -e "${CYAN}基础设施服务:${NC}"
    docker compose -f docker-compose.dev.yml ps
    echo ""

    # Server 状态
    echo -e "${CYAN}Server 状态:${NC}"
    if [ -f "$PID_DIR/server.pid" ] && kill -0 $(cat "$PID_DIR/server.pid") 2>/dev/null; then
        echo -e "${GREEN}● 运行中${NC} (PID: $(cat $PID_DIR/server.pid)) - http://localhost:8001"
    else
        echo -e "${RED}● 已停止${NC}"
    fi
    echo ""

    # Web 状态
    echo -e "${CYAN}Web 状态:${NC}"
    if [ -f "$PID_DIR/web.pid" ] && kill -0 $(cat "$PID_DIR/web.pid") 2>/dev/null; then
        echo -e "${GREEN}● 运行中${NC} (PID: $(cat $PID_DIR/web.pid)) - http://localhost:3000"
    else
        echo -e "${RED}● 已停止${NC}"
    fi
    echo ""
}

#=============================================================================
# 数据库管理
#=============================================================================

db_reset() {
    log_warn "这将删除所有数据库数据！"
    read -p "确定要继续吗? (yes/no): " confirm

    if [ "$confirm" = "yes" ]; then
        log_step "重置数据库..."
        stop_server

        # 删除 PostgreSQL 容器和卷
        docker compose -f docker-compose.dev.yml stop postgres
        docker compose -f docker-compose.dev.yml rm -f postgres
        docker volume rm bk-lite_postgres_dev 2>/dev/null || true

        # 重新启动
        start_infra
        sleep 10

        # 重新初始化
        init_server_db

        log_success "数据库已重置"
    else
        log_info "操作已取消"
    fi
}

db_shell() {
    log_step "打开数据库 Shell..."
    docker compose -f docker-compose.dev.yml exec postgres psql -U postgres -d bklite
}

db_migrate() {
    log_step "运行数据库迁移..."
    cd "$PROJECT_ROOT/server"
    uv run python manage.py makemigrations
    uv run python manage.py migrate
    cd "$PROJECT_ROOT"
    log_success "迁移完成"
}

#=============================================================================
# Git 配置
#=============================================================================

git_setup() {
    log_step "配置 Git 凭证..."

    # 检查 Git 配置
    if ! git config user.name &> /dev/null; then
        read -p "请输入 Git 用户名: " git_username
        git config user.name "$git_username"
    fi

    if ! git config user.email &> /dev/null; then
        read -p "请输入 Git 邮箱: " git_email
        git config user.email "$git_email"
    fi

    log_info "当前 Git 配置:"
    echo "  用户名: $(git config user.name)"
    echo "  邮箱: $(git config user.email)"
    echo ""

    # 配置 credential helper
    log_info "配置 Git credential helper..."
    git config credential.helper store

    # GitHub 推送配置
    read -p "是否配置 GitHub 推送? (y/n): " setup_github
    if [ "$setup_github" = "y" ]; then
        read -p "请输入您的 GitHub 用户名: " github_user

        log_warn "请安全地输入您的 GitHub Personal Access Token (输入时不会显示):"
        read -s github_token
        echo ""

        # 配置远程仓库
        if git remote | grep -q "^myfork$"; then
            git remote set-url myfork "https://${github_user}:${github_token}@github.com/${github_user}/bk-lite.git"
        else
            git remote add myfork "https://${github_user}:${github_token}@github.com/${github_user}/bk-lite.git"
        fi

        log_success "GitHub 远程仓库已配置为 'myfork'"
        log_info "推送命令: git push myfork master"
    fi
}

git_push() {
    log_step "推送代码到 GitHub..."

    # 检查是否有未提交的更改
    if ! git diff-index --quiet HEAD --; then
        log_info "检测到未提交的更改，创建提交..."
        git add .
        read -p "请输入提交信息: " commit_msg
        git commit -m "$commit_msg"
    fi

    # 推送
    if git remote | grep -q "^myfork$"; then
        git push myfork master
        log_success "代码已推送到 GitHub"
    else
        log_error "未配置 GitHub 远程仓库"
        log_info "请先运行: ./dev.sh git-setup"
    fi
}

#=============================================================================
# 帮助信息
#=============================================================================

show_help() {
    cat << EOF
${CYAN}Blueking Lite 本地开发环境管理工具${NC}

用法:
    $0 <command> [options]

${YELLOW}环境管理:${NC}
    check               检查开发环境是否就绪
    install             安装所有依赖 (Server + Web)

${YELLOW}服务管理:${NC}
    start <service>     启动服务 [all|infra|server|web]
    stop <service>      停止服务 [all|infra|server|web]
    restart <service>   重启服务 [all|infra|server|web]
    status              查看所有服务状态
    logs <service>      查看日志 [infra|server|web]

${YELLOW}数据库管理:${NC}
    db migrate          运行数据库迁移
    db reset            重置数据库 (删除所有数据)
    db shell            打开数据库 Shell
    db init             初始化数据库

${YELLOW}Git 管理:${NC}
    git-setup           配置 Git 凭证和远程仓库
    git-push            提交并推送代码到 GitHub

${YELLOW}示例:${NC}
    $0 check            # 检查环境
    $0 install          # 安装依赖
    $0 start all        # 启动所有服务
    $0 status           # 查看状态
    $0 logs server      # 查看 Server 日志
    $0 db reset         # 重置数据库
    $0 git-setup        # 配置 Git

${YELLOW}快速开始:${NC}
    1. $0 check
    2. $0 install
    3. $0 start infra
    4. $0 db init
    5. $0 start all

${GREEN}访问地址:${NC}
    - Web 前端: http://localhost:3000
    - Server API: http://localhost:8001
    - MinIO 控制台: http://localhost:9001
    - MLflow: http://localhost:5000

EOF
}

#=============================================================================
# 主命令路由
#=============================================================================

main() {
    case "${1:-help}" in
        check)
            check_environment
            ;;
        install)
            check_environment && install_all
            ;;
        start)
            case "${2:-all}" in
                all) start_all ;;
                infra) start_infra ;;
                server) start_server ;;
                web) start_web ;;
                *) log_error "未知服务: $2"; show_help ;;
            esac
            ;;
        stop)
            case "${2:-all}" in
                all) stop_all ;;
                infra) stop_infra ;;
                server) stop_server ;;
                web) stop_web ;;
                *) log_error "未知服务: $2"; show_help ;;
            esac
            ;;
        restart)
            case "${2:-all}" in
                all) restart_all ;;
                infra) restart_infra ;;
                server) stop_server && sleep 2 && start_server ;;
                web) stop_web && sleep 2 && start_web ;;
                *) log_error "未知服务: $2"; show_help ;;
            esac
            ;;
        status)
            show_status
            ;;
        logs)
            case "${2:-infra}" in
                infra) logs_infra "${3:-}" ;;
                server) logs_server ;;
                web) logs_web ;;
                *) log_error "未知服务: $2"; show_help ;;
            esac
            ;;
        db)
            case "${2:-}" in
                migrate) db_migrate ;;
                reset) db_reset ;;
                shell) db_shell ;;
                init) init_server_db ;;
                *) log_error "未知数据库命令: $2"; show_help ;;
            esac
            ;;
        git-setup)
            git_setup
            ;;
        git-push)
            git_push
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "未知命令: $1"
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"

#!/bin/bash
set -euo pipefail

# ============================================================
# 黄埔海关智能运维平台 - 部署脚本
# 版本: v1.0
# 功能: 智能检测首次部署，自动初始化或直接启动
# ============================================================

# ANSI 颜色代码
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log() {
    local level="$1"
    local message="$2"
    local color=""

    case "$level" in
        "INFO")
            color="$BLUE"
            ;;
        "WARNING")
            color="$YELLOW"
            ;;
        "ERROR")
            color="$RED"
            ;;
        "SUCCESS")
            color="$GREEN"
            ;;
        *)
            color="$NC"
            ;;
    esac

    echo -e "${color}[$(date +'%Y-%m-%d %H:%M:%S')] [$level] $message${NC}"
}

# 检查 Docker 是否安装
check_docker() {
    if ! command -v docker >/dev/null 2>&1; then
        log "ERROR" "未找到 docker 命令，请先安装 Docker"
        exit 1
    fi
    log "SUCCESS" "Docker 已安装: $(docker --version)"
}

# 检查 Docker Compose 是否安装
check_docker_compose() {
    if command -v docker-compose >/dev/null 2>&1; then
        DOCKER_COMPOSE_CMD="docker-compose"
    elif docker compose version >/dev/null 2>&1; then
        DOCKER_COMPOSE_CMD="docker compose"
    else
        log "ERROR" "未找到 docker-compose，请先安装"
        exit 1
    fi
    log "SUCCESS" "Docker Compose 已安装: $($DOCKER_COMPOSE_CMD version)"
}

# 生成随机密码
generate_password() {
    local length=$1
    cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c $length
}

# 生成自签名 TLS 证书
generate_tls_certs() {
    local dir=./conf/certs
    local san="DNS:nats,DNS:localhost,IP:127.0.0.1,IP:${HOST_IP}"
    local cn="HuangpuCustoms"

    # 当证书已存在时跳过
    if [ -f "$dir/server.crt" ] && [ -f "$dir/server.key" ] && [ -f "$dir/ca.crt" ]; then
        log "SUCCESS" "TLS 证书已存在，跳过生成步骤"
        return
    fi

    log "INFO" "生成自签名 TLS 证书..."
    mkdir -p ${dir}
    local abs_dir=$(cd "$dir" && pwd)

    # CA 私钥生成
    docker run --rm -v "${abs_dir}:/certs" alpine/openssl:3.5.4 \
        genrsa -out "/certs/ca.key" 2048

    # CA 证书生成
    docker run --rm -v "${abs_dir}:/certs" alpine/openssl:3.5.4 \
        req -x509 -new -nodes -key "/certs/ca.key" -sha256 -days 3650 \
        -subj "/CN=Huangpu Customs CA" -out "/certs/ca.crt"

    # Server 私钥生成
    docker run --rm -v "${abs_dir}:/certs" alpine/openssl:3.5.4 \
        genrsa -out "/certs/server.key" 2048

    # 创建 OpenSSL 配置文件
    cat > "${dir}/openssl.conf" << EOF
[req]
distinguished_name = req
req_extensions = req_ext
prompt = no

[req_ext]
subjectAltName = ${san}

[v3_ext]
subjectAltName = ${san}
basicConstraints = CA:FALSE
keyUsage = digitalSignature,keyEncipherment,keyAgreement
extendedKeyUsage = serverAuth
EOF

    # 生成证书签名请求 (CSR)
    docker run --rm -v "${abs_dir}:/certs" alpine/openssl:3.5.4 \
        req -new -key "/certs/server.key" -out "/certs/server.csr" \
        -config "/certs/openssl.conf" -subj "/CN=${cn}"

    # 使用 CA 签名生成服务器证书
    docker run --rm -v "${abs_dir}:/certs" alpine/openssl:3.5.4 \
        x509 -req -in "/certs/server.csr" -CA "/certs/ca.crt" -CAkey "/certs/ca.key" \
        -CAcreateserial -days 825 -sha256 -out "/certs/server.crt" \
        -extensions v3_ext -extfile "/certs/openssl.conf"

    # 清理临时文件
    rm -f "${dir}/server.csr" "${dir}/openssl.conf"
    log "SUCCESS" "TLS 证书生成完成"
}

# 生成 NATS 配置文件
generate_nats_config() {
    if [ -f ./conf/nats/nats.conf ]; then
        log "SUCCESS" "NATS 配置文件已存在"
        return
    fi

    log "INFO" "创建 NATS 配置文件..."
    mkdir -p ./conf/nats
    cat > ./conf/nats/nats.conf <<EOF
port: 4222
monitor_port: 8222
trace: true
debug: false
logtime: false
allow_non_tls: true

jetstream {
  store_dir: /data/jetstream
  max_mem: 1G
  max_file: 10G
}

tls {
  cert_file: "/etc/nats/certs/server.crt"
  key_file: "/etc/nats/certs/server.key"
  ca_file: "/etc/nats/certs/ca.crt"
  timeout: 3
  verify: false
}

accounts {
  ADMIN: {
    users: [
      { user: "${NATS_ADMIN_USERNAME}", password: "${NATS_ADMIN_PASSWORD}" }
    ]
    jetstream: enabled
  }
}
EOF
    log "SUCCESS" "NATS 配置文件创建完成"
}

# 生成 Traefik 配置文件
generate_traefik_config() {
    if [ -f ./conf/traefik/dynamic.yml ] && [ -s ./conf/traefik/dynamic.yml ]; then
        log "SUCCESS" "Traefik 配置文件已存在"
        return
    fi

    log "INFO" "创建 Traefik 配置文件..."
    mkdir -p ./conf/traefik
    cat > ./conf/traefik/dynamic.yml <<'EOF'
http:
  routers:
    # Web 前端路由
    web-router:
      rule: "PathPrefix(`/`)"
      service: web-service
      priority: 1

  services:
    # Web 服务
    web-service:
      loadBalancer:
        servers:
          - url: "http://web:3000"
EOF
    log "SUCCESS" "Traefik 配置文件创建完成"
}

# 初始化或加载配置
initialize_config() {
    local config_file=".env"
    local secrets_file=".secrets"

    # 获取本机 IP
    if command -v hostname >/dev/null 2>&1 && hostname -I >/dev/null 2>&1; then
        DEFAULT_IP=$(hostname -I | awk '{print $1}')
    elif command -v ifconfig >/dev/null 2>&1; then
        DEFAULT_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)
    else
        DEFAULT_IP="127.0.0.1"
    fi

    # 检查是否存在 secrets 文件
    if [ -f "$secrets_file" ]; then
        log "SUCCESS" "发现已保存的密码配置，加载中..."
        . "./$secrets_file"
    else
        log "INFO" "首次部署，生成随机密码..."
        export POSTGRES_PASSWORD=$(generate_password 32)
        export REDIS_PASSWORD=$(generate_password 32)
        export SECRET_KEY=$(generate_password 32)
        export NEXTAUTH_SECRET=$(generate_password 12)
        export NATS_ADMIN_USERNAME=admin
        export NATS_ADMIN_PASSWORD=$(generate_password 32)
        export MINIO_ROOT_USER=minio
        export MINIO_ROOT_PASSWORD=$(generate_password 32)
        export FALKORDB_PASSWORD=$(generate_password 32)

        # 保存密码到 secrets 文件
        cat > "$secrets_file" <<EOF
# 黄埔海关智能运维平台 - 密码配置
# 生成日期: $(date +'%Y-%m-%d %H:%M:%S')
# 警告: 请妥善保管此文件，不要泄露!
export POSTGRES_PASSWORD=$POSTGRES_PASSWORD
export REDIS_PASSWORD=$REDIS_PASSWORD
export SECRET_KEY=$SECRET_KEY
export NEXTAUTH_SECRET=$NEXTAUTH_SECRET
export NATS_ADMIN_USERNAME=$NATS_ADMIN_USERNAME
export NATS_ADMIN_PASSWORD=$NATS_ADMIN_PASSWORD
export MINIO_ROOT_USER=$MINIO_ROOT_USER
export MINIO_ROOT_PASSWORD=$MINIO_ROOT_PASSWORD
export FALKORDB_PASSWORD=$FALKORDB_PASSWORD
EOF
        chmod 600 "$secrets_file"
        log "SUCCESS" "密码已生成并保存到 $secrets_file"
        log "WARNING" "请妥善保管 $secrets_file 文件！"
    fi

    # 设置 HOST_IP（如果没有 .env 文件）
    if [ ! -f "$config_file" ]; then
        # 尝试读取用户输入，如果失败则使用默认值
        if [ -t 0 ]; then
            # 交互模式
            read -p "请输入对外访问的IP地址，默认为 [$DEFAULT_IP]: " HOST_IP || true
        fi
        export HOST_IP=${HOST_IP:-$DEFAULT_IP}
        log "INFO" "使用 IP 地址: $HOST_IP"
    else
        . "./$config_file"
    fi

    # 生成 .env 文件
    cat > "$config_file" <<EOF
# 黄埔海关智能运维平台 - 环境配置
HOST_IP=${HOST_IP}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
REDIS_PASSWORD=${REDIS_PASSWORD}
SECRET_KEY=${SECRET_KEY}
NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
NATS_ADMIN_USERNAME=${NATS_ADMIN_USERNAME}
NATS_ADMIN_PASSWORD=${NATS_ADMIN_PASSWORD}
MINIO_ROOT_USER=${MINIO_ROOT_USER}
MINIO_ROOT_PASSWORD=${MINIO_ROOT_PASSWORD}
FALKORDB_PASSWORD=${FALKORDB_PASSWORD}
EOF

    log "SUCCESS" "环境配置已保存到 $config_file"
}

# 创建 JetStream
create_jetstream() {
    log "INFO" "创建 NATS JetStream..."
    docker run --rm --network=bklite-prod-huangpu \
        natsio/nats-box:latest nats -s nats://nats:4222 \
        --user $NATS_ADMIN_USERNAME --password $NATS_ADMIN_PASSWORD \
        stream add metrics --subjects=metrics.* --storage=file \
        --replicas=1 --retention=limits --discard=old \
        --max-age=20m --max-bytes=104857600 --max-consumers=-1 \
        --max-msg-size=-1 --max-msgs=-1 --max-msgs-per-subject=1000000 \
        --dupe-window=5m --no-allow-rollup --no-deny-delete --no-deny-purge || true
    log "SUCCESS" "JetStream 创建完成"
}

# 主部署流程
main() {
    log "INFO" "=========================================="
    log "INFO" "黄埔海关智能运维平台 - 部署程序"
    log "INFO" "=========================================="

    # 检查依赖
    check_docker
    check_docker_compose

    # 初始化配置
    initialize_config

    # 生成证书和配置
    generate_tls_certs
    generate_nats_config
    generate_traefik_config

    # 检查是否首次部署
    if [ ! -f ".initialized" ]; then
        log "INFO" "检测到首次部署，将执行完整初始化流程..."
        FIRST_DEPLOY=true
    else
        log "INFO" "检测到已初始化的环境，跳过初始化步骤..."
        FIRST_DEPLOY=false
    fi

    # 启动服务
    log "INFO" "启动基础设施服务..."
    ${DOCKER_COMPOSE_CMD} up -d traefik postgres redis nats victoria-metrics victoria-logs minio falkordb mlflow nats-executor

    log "INFO" "等待基础服务健康检查..."
    sleep 20

    # 首次部署需要创建 JetStream
    if [ "$FIRST_DEPLOY" = true ]; then
        create_jetstream
    fi

    # 启动应用服务
    log "INFO" "启动应用服务（Server + Web）..."
    ${DOCKER_COMPOSE_CMD} up -d server web

    # 等待服务启动
    log "INFO" "等待应用服务启动（这可能需要1-2分钟）..."
    sleep 30

    # 标记已初始化
    if [ "$FIRST_DEPLOY" = true ]; then
        touch .initialized
        log "SUCCESS" "初始化完成，已创建标记文件 .initialized"
    fi

    # 显示部署结果
    echo ""
    log "SUCCESS" "=========================================="
    log "SUCCESS" "部署完成！"
    log "SUCCESS" "=========================================="
    log "INFO" "访问地址: http://${HOST_IP}:8080"
    log "INFO" "默认账号: admin"
    log "INFO" "默认密码: password"
    log "INFO" ""
    log "INFO" "查看服务状态: ${DOCKER_COMPOSE_CMD} ps"
    log "INFO" "查看服务日志: ${DOCKER_COMPOSE_CMD} logs -f [service-name]"
    log "INFO" "停止所有服务: ${DOCKER_COMPOSE_CMD} down"
    log "WARNING" "密码配置保存在: .secrets (请妥善保管!)"
    echo ""
}

# 运行主程序
main

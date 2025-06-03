#!/bin/bash
set -euo pipefail
# ANSI escape codes for colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to log messages with colored output
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

# Function to validate environment variables
validate_env_var() {
    local var_name="$1"
    if [ -z "${!var_name}" ]; then
        log "ERROR" "Environment variable $var_name is not set."
        exit 1
    fi
}

# 生成随机密码 - 进一步优化，完全避免任何可能在YAML中引起问题的特殊字符
generate_password() {
    local length=$1
    # 只使用字母和数字，避免任何特殊字符，确保在YAML文件中不会出现解析问题
    cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c $length
}

# 等待容器健康状态函数
wait_container_health() {
    local container_name="$1"
    local service_name="$2"
    log "INFO" "等待 $service_name 启动..."
    until [ "$(docker-compose ps $container_name --format "{{.Health}}" 2>/dev/null)" == "healthy" ]; do
        log "INFO" "等待 $service_name 启动..."
        sleep 5
    done
    log "SUCCESS" "$service_name 已成功启动"
}

# 检查容器是否响应 HTTP 请求
check_http_response() {
    local url="$1"
    local expected_code="$2"
    local service_name="$3"
    local max_attempts="$4"
    local attempt=0

    log "INFO" "正在检查 $service_name 是否可访问..."
    
    while [ $attempt -lt $max_attempts ]; do
        response_code=$(curl -s -o /dev/null -w "%{http_code}" $url)
        if [ "$response_code" == "$expected_code" ]; then
            log "SUCCESS" "$service_name 已成功启动并可访问"
            return 0
        else
            log "INFO" "$service_name 尚未完全启动，第 $((attempt + 1)) 次尝试，等待 5 秒后继续检查..."
            sleep 5
        fi
        attempt=$((attempt + 1))
    done

    log "ERROR" "经过 $max_attempts 次尝试，$service_name 仍未成功启动"
    return 1
}
if [ -f port.env ]; then
    log "SUCCESS" "port.env文件已存在，跳过文件生成步骤..."
    source port.env
else
        # 获取本地的第一个ip为默认ip
    DEFAULT_IP=$(hostname -I | awk '{print $1}')

    # 从命令行读取HOST_IP环境变量
    read -p "输入对外访问的IP地址，默认为 [$DEFAULT_IP] " HOST_IP
    export HOST_IP=${HOST_IP:-$DEFAULT_IP}

    DEFAULT_TRAEFIK_CMDB_PORT=20000
    read -p "输入CMDB端口，默认为 [$DEFAULT_TRAEFIK_CMDB_PORT] " TRAEFIK_CMDB_PORT
    export TRAEFIK_CMDB_PORT=${TRAEFIK_CMDB_PORT:-$DEFAULT_TRAEFIK_CMDB_PORT}

    DEFAULT_TRAEFIK_SYSTEM_MANAGER_PORT=20001
    read -p "输入系统管理端口，默认为 [$DEFAULT_TRAEFIK_SYSTEM_MANAGER_PORT] " TRAEFIK_SYSTEM_MANAGER_PORT
    export TRAEFIK_SYSTEM_MANAGER_PORT=${TRAEFIK_SYSTEM_MANAGER_PORT:-$DEFAULT_TRAEFIK_SYSTEM_MANAGER_PORT}

    DEFAULT_TRAEFIK_NODE_MANAGER_PORT=20002
    read -p "输入节点管理端口，默认为 [$DEFAULT_TRAEFIK_NODE_MANAGER_PORT] " TRAEFIK_NODE_MANAGER_PORT
    export TRAEFIK_NODE_MANAGER_PORT=${TRAEFIK_NODE_MANAGER_PORT:-$DEFAULT_TRAEFIK_NODE_MANAGER_PORT}

    DEFAULT_TRAEFIK_MONITOR_PORT=20003
    read -p "输入监控端口，默认为 [$DEFAULT_TRAEFIK_MONITOR_PORT] " TRAEFIK_MONITOR_PORT
    export TRAEFIK_MONITOR_PORT=${TRAEFIK_MONITOR_PORT:-$DEFAULT_TRAEFIK_MONITOR_PORT}

    DEFAULT_TRAEFIK_CONSOLE_PORT=20004
    read -p "输入控制台端口，默认为 [$DEFAULT_TRAEFIK_CONSOLE_PORT] " TRAEFIK_CONSOLE_PORT
    export TRAEFIK_CONSOLE_PORT=${TRAEFIK_CONSOLE_PORT:-$DEFAULT_TRAEFIK_CONSOLE_PORT}

    DEFAULT_NODE_MANAGER_API_PORT=20005
    read -p "输入节点管理API端口，默认为 [$DEFAULT_NODE_MANAGER_API_PORT] " NODE_MANAGER_API_PORT
    export NODE_MANAGER_API_PORT=${NODE_MANAGER_API_PORT:-$DEFAULT_NODE_MANAGER_API_PORT}

    # 将输入的配置写入port.env
    cat > port.env <<EOF
HOST_IP=${HOST_IP}
TRAEFIK_CMDB_PORT=${TRAEFIK_CMDB_PORT}
TRAEFIK_SYSTEM_MANAGER_PORT=${TRAEFIK_SYSTEM_MANAGER_PORT}
TRAEFIK_NODE_MANAGER_PORT=${TRAEFIK_NODE_MANAGER_PORT}
TRAEFIK_MONITOR_PORT=${TRAEFIK_MONITOR_PORT}
TRAEFIK_CONSOLE_PORT=${TRAEFIK_CONSOLE_PORT}
NODE_MANAGER_API_PORT=${NODE_MANAGER_API_PORT}
EOF
fi

# 检查common.env文件是否存在，存在则加载，不存在则生成
COMMON_ENV_FILE="common.env"
if [ -f "$COMMON_ENV_FILE" ]; then
    log "SUCCESS" "发现 $COMMON_ENV_FILE 配置文件，加载已保存的环境变量..."
    source $COMMON_ENV_FILE
else
    log "INFO" "未发现 $COMMON_ENV_FILE 配置文件，生成随机环境变量..."
    # 生成随机密码
    export POSTGRES_PASSWORD=$(generate_password 32)
    export REDIS_PASSWORD=$(generate_password 32)
    export SECRET_KEY=$(generate_password 32)
    export NEXTAUTH_SECRET=$(generate_password 12)
    export SIDECAR_INIT_TOKEN=$(generate_password 64)
    export NATS_ADMIN_USERNAME=admin
    export NATS_ADMIN_PASSWORD=$(generate_password 32)
    export NATS_MONITOR_USERNAME=monitor
    export NATS_MONITOR_PASSWORD=$(generate_password 32)
    export NEO4J_USERNAME=neo4j
    export NEO4J_PASSWORD=$(generate_password 32)
    export NEO4J_AUTH="${NEO4J_USERNAME}/${NEO4J_PASSWORD}"
    
    # 保存到common.env文件
    cat > $COMMON_ENV_FILE <<EOF
# 自动生成的环境变量配置，用于确保脚本幂等性
# 生成日期: $(date +'%Y-%m-%d %H:%M:%S')
export POSTGRES_PASSWORD=$POSTGRES_PASSWORD
export REDIS_PASSWORD=$REDIS_PASSWORD
export SECRET_KEY=$SECRET_KEY
export NEXTAUTH_SECRET=$NEXTAUTH_SECRET
export SIDECAR_INIT_TOKEN=$SIDECAR_INIT_TOKEN
export NATS_ADMIN_USERNAME=$NATS_ADMIN_USERNAME
export NATS_ADMIN_PASSWORD=$NATS_ADMIN_PASSWORD
export NATS_MONITOR_USERNAME=$NATS_MONITOR_USERNAME
export NATS_MONITOR_PASSWORD=$NATS_MONITOR_PASSWORD
export NEO4J_USERNAME=$NEO4J_USERNAME
export NEO4J_PASSWORD=$NEO4J_PASSWORD
export NEO4J_AUTH=$NEO4J_AUTH
EOF
    log "SUCCESS" "环境变量已生成并保存到 $COMMON_ENV_FILE 文件"
fi

# 固定的环境变量
DOCKER_IMAGE_TRAEFIK=traefik:3.3.3
DOCKER_IMAGE_REDIS=redis:5.0.14
DOCKER_IMAGE_NATS=nats:2.10.25
DOCKER_IMAGE_NATS_CLI=bitnami/natscli:0.1.6
DOCKER_IMAGE_VICTORIA_METRICS=victoriametrics/victoria-metrics:v1.106.1
DOCKER_IMAGE_POSTGRES=postgres:15
DOCKER_IMAGE_SYSTEM_MANAGER=bklite/system-manager
DOCKER_IMAGE_SYSTEM_MANAGER_WEB=bklite/system-manager-web
DOCKER_IMAGE_NODE_MANAGER=bklite/node-manager
DOCKER_IMAGE_NODE_MANAGER_WEB=bklite/node-manager-web
DOCKER_IMAGE_MONITOR=bklite/monitor
DOCKER_IMAGE_MONITOR_WEB=bklite/monitor-web
DOCKER_NETWORK=prod
DIST_ARCH=arm64
POSTGRES_USERNAME=postgres
TRAEFIK_ENABLE_DASHBOARD=false
DEFAULT_REQUEST_TIMEOUT=10
DOCKER_IMAGE_OPSCONSOLE=bklite/ops-console
DOCKER_IMAGE_OPSCONSOLE_WEB=bklite/opsconsole-web
DOCKER_IMAGE_STARGAZER=bklite/stargazer
DOCKER_IMAGE_CMDB=bklite/cmdb
DOCKER_IMAGE_CMDB_WEB=bklite/cmdb-web
DOCKER_NEO4J_IMAGE=neo4j:4.4.43

# 采集器镜像
# TODO: 不同OS/架构支持
export DOCKER_IMAGE_FUSION_COLLECTOR=bklite/fusion-collector:linux-amd64

# 从镜像生成控制器&采集器包
log "INFO" "开始生成控制器和采集器包..."
# 获取当前cpu架构
CPU_ARCH=$(uname -m)
if [[ "$CPU_ARCH" == "x86_64" ]]; then
    [ -d pkgs ] && rm -rvf pkgs
    mkdir -p pkgs/controller
    mkdir -p pkgs/collector
    docker run --rm -v $PWD/pkgs:/pkgs --entrypoint=/bin/bash $DOCKER_IMAGE_FUSION_COLLECTOR -c "tar -czvf /pkgs/controller/lite_controller_linux_amd64.tar.gz . ;cp -av bin/* /pkgs/collector/"
elif [[ "$CPU_ARCH" == "aarch64" ]]; then
    log "WARNING" "当前CPU架构为arm64，暂时无内置采集器"
else
    log "ERROR" "不支持的CPU架构: $CPU_ARCH"
    exit 1
fi

# 检查nats.conf文件是否存在
if [ -f ./conf/nats/nats.conf ]; then
    log "WARNING" "nats.conf文件已存在，文件将被覆盖..."
else
    log "INFO" "创建 nats.conf 文件..."
    mkdir -p ./conf/nats
fi

cat > ./conf/nats/nats.conf <<EOF
port: 4222

monitor_port: 8222

trace: true
debug: false
logtime: false

jetstream: enabled
jetstream {
  store_dir=/nats/storage
}

server_name=nats-server
authorization {  
  default_permissions = {
    publish =[]
    subscribe = []
  }
  users = [
    {
      user: "${NATS_ADMIN_USERNAME}"
      password: "${NATS_ADMIN_PASSWORD}"
      permissions: {
        publish = [">"]
        subscribe = [">"]
      }
    },
    {
      user: "${NATS_MONITOR_USERNAME}"
      password: "${NATS_MONITOR_PASSWORD}"
      permissions: {
        publish = ["metrics.>"]
        subscribe = []
      }
    }
  ]
}
EOF

# 检查docker-compose.yml文件是否已存在
if [ -f docker-compose.yml ]; then
    log "INFO" "docker-compose.yml文件已存在，跳过文件生成步骤..."
else
    # 创建 docker-compose.yml 文件
    log "INFO" "创建 docker-compose.yml 文件..."
    cat > docker-compose.yml <<EOF
networks:
  prod:
    driver: bridge

volumes:
  redis:
  nats:
  victoria-metrics:
  postgres:
  neo4j:

services:

  traefik:
    image: ${DOCKER_IMAGE_TRAEFIK}
    restart: always
    ports:
      - "${TRAEFIK_CMDB_PORT}:${TRAEFIK_CMDB_PORT}"
      - "${TRAEFIK_SYSTEM_MANAGER_PORT}:${TRAEFIK_SYSTEM_MANAGER_PORT}"
      - "${TRAEFIK_NODE_MANAGER_PORT}:${TRAEFIK_NODE_MANAGER_PORT}"
      - "${TRAEFIK_MONITOR_PORT}:${TRAEFIK_MONITOR_PORT}"
      - "${TRAEFIK_CONSOLE_PORT}:${TRAEFIK_CONSOLE_PORT}"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./conf/traefik/dynamic.yml:/etc/traefik/dynamic.yml
    labels:
      - "traefik.enable=true"
      - "traefik.http.services.traefik-dashboard.loadbalancer.server.port=8080"
    command:
      - "--log.level=INFO"
      - "--api.insecure=true"
      - "--api.dashboard=${TRAEFIK_ENABLE_DASHBOARD}"
      - "--providers.docker.endpoint=unix:///var/run/docker.sock"
      - "--providers.docker.exposedByDefault=false"
      - "--providers.file.filename=/etc/traefik/dynamic.yml"
      - "--providers.file.watch=true"
      - "--accesslog"
      - "--entrypoints.cmdb-web.address=:${TRAEFIK_CMDB_PORT}"
      - "--entrypoints.system-manager-web.address=:${TRAEFIK_SYSTEM_MANAGER_PORT}"
      - "--entrypoints.node-manager-web.address=:${TRAEFIK_NODE_MANAGER_PORT}"
      - "--entrypoints.monitor-web.address=:${TRAEFIK_MONITOR_PORT}"
      - "--entrypoints.opsconsole.address=:${TRAEFIK_CONSOLE_PORT}"
    networks:
      - prod

  redis:
    image: ${DOCKER_IMAGE_REDIS}
    restart: always
    volumes:
      - redis:/data
    command:
      - "redis-server"
      - "--requirepass"
      - "${REDIS_PASSWORD}"
    ports:
      - "6379:6379"
    networks:
      - prod

  nats:
    image: ${DOCKER_IMAGE_NATS}
    restart: always
    volumes:
      - ./conf/nats/nats.conf:/etc/nats/nats.conf
      - nats:/nats
    ports:
      - "4222:4222"
    command:
      - "-c"
      - "/etc/nats/nats.conf"
    networks:
      - prod

  victoria-metrics:
    image: ${DOCKER_IMAGE_VICTORIA_METRICS}
    restart: always
    volumes:
      - victoria-metrics:/victoria-metrics-data
    ports:
      - "8428:8428"
    command:
      - "--storageDataPath=/victoria-metrics-data"
      - "--httpListenAddr=0.0.0.0:8428"
      - "--retentionPeriod=168h"
      - "-maxLabelsPerTimeseries=300"
    networks:
      - prod
    depends_on:
      - nats

  neo4j:
    image: ${DOCKER_NEO4J_IMAGE}
    container_name: neo4j
    restart: always
    ports:
      - "7474:7474"
      - "7687:7687"
      - "7473:7473"
    networks:
      - prod
    environment:
      - NEO4J_AUTH=${NEO4J_AUTH}
    volumes:
      - neo4j:/data

  postgres:
    container_name: postgres
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      PGDATA: /data/postgres
    volumes:
      - postgres:/data/postgres
      - ./conf/postgres/initdb.sql:/docker-entrypoint-initdb.d/initdb.sql
    networks:
      - prod
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "${POSTGRES_USERNAME}"]
      interval: 10s
      timeout: 5s
      retries: 3
    restart: always

  system-manager:
    image: ${DOCKER_IMAGE_SYSTEM_MANAGER}
    restart: always
    environment:
      NATS_SERVERS: nats://${NATS_ADMIN_USERNAME}:${NATS_ADMIN_PASSWORD}@nats:4222
      NATS_NAMESPACE: bk-lite
      DEFAULT_REQUEST_TIMEOUT: ${DEFAULT_REQUEST_TIMEOUT}
      DB_NAME: system_mgmt
      CLIENT_ID: system-manager
      DEBUG: "0"
      SECRET_KEY: ${SECRET_KEY}
      ENABLE_CELERY: "True"
      DB_USER: ${POSTGRES_USERNAME}
      DB_HOST: postgres
      DB_PASSWORD: ${POSTGRES_PASSWORD}
      DB_PORT: "5432"
      DB_ENGINE: postgresql
      INSTALL_APPS: system_mgmt
      JWT_ALGORITHM: HS256
    depends_on:
      postgres:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-s", "-o", "/dev/null", "-w", "'%{http_code}'", "http://127.0.0.1:8000/"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 10s
    networks:
      - prod

  system-manager-web:
    image: ${DOCKER_IMAGE_SYSTEM_MANAGER_WEB}
    restart: always
    environment:
      NEXTAUTH_URL: http://${HOST_IP}:${TRAEFIK_SYSTEM_MANAGER_PORT}
      NEXTAUTH_SECRET: ${NEXTAUTH_SECRET}
      NEXTAPI_URL: http://system-manager:8000
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.system-manager-web.rule=Host(\`${HOST_IP}\`)"
      - "traefik.http.routers.system-manager-web.entrypoints=system-manager-web"
      - "traefik.http.services.system-manager-web.loadbalancer.server.port=3000"
    networks:
      - prod

    depends_on:
      - system-manager
    healthcheck:
      test: ["CMD", "node", "-e", "fetch('http://system-manager-web:3000/healthcheck').then(res => res.status === 200)"]
      start_period: 5s

  node-manager:
    image: ${DOCKER_IMAGE_NODE_MANAGER}
    restart: always
    ports:
      - "${NODE_MANAGER_API_PORT}:8000"
    environment:
      NATS_SERVERS: nats://${NATS_ADMIN_USERNAME}:${NATS_ADMIN_PASSWORD}@nats:4222
      NATS_NAMESPACE: bk-lite
      DB_NAME: node_mgmt
      CLIENT_ID: node_mgmt
      SIDECAR_INIT_TOKEN: ${SIDECAR_INIT_TOKEN}
      DEFAULT_ZONE_VAR_NATS_SERVERS: ${HOST_IP}:4222
      DEFAULT_ZONE_VAR_NATS_USERNAME: ${NATS_MONITOR_USERNAME}
      DEFAULT_ZONE_VAR_NATS_PASSWORD: ${NATS_MONITOR_PASSWORD}
      DEFAULT_ZONE_VAR_NODE_SERVER_URL: http://${HOST_IP}:${NODE_MANAGER_API_PORT}
      DEFAULT_ZONE_VAR_STARGAZER_URL: http://stargazer:8083
      SIDECAR_INPUT_MODE: nats
      DEBUG: "0"
      SECRET_KEY: ${SECRET_KEY}
      ENABLE_CELERY: "False"
      DB_USER: ${POSTGRES_USERNAME}
      DB_HOST: postgres
      DB_PASSWORD: ${POSTGRES_PASSWORD}
      DB_PORT: "5432"
      DB_ENGINE: postgresql
      INSTALL_APPS: node_mgmt
    volumes:
      - ./pkgs:/pkgs
    healthcheck:
      test: ["CMD", "curl", "-s", "-o", "/dev/null", "-w", "'%{http_code}'", "http://127.0.0.1:8000/"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 10s
    networks:
      - prod

    depends_on:
      system-manager:
        condition: service_healthy

  node-manager-web:
    image: ${DOCKER_IMAGE_NODE_MANAGER_WEB}
    restart: always
    environment:
      NEXTAUTH_URL: http://${HOST_IP}:${TRAEFIK_NODE_MANAGER_PORT}
      NEXTAUTH_SECRET: ${NEXTAUTH_SECRET}
      NEXTAPI_URL: http://node-manager:8000
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.node-manager-web.rule=Host(\`${HOST_IP}\`)"
      - "traefik.http.routers.node-manager-web.entrypoints=node-manager-web"
      - "traefik.http.services.node-manager-web.loadbalancer.server.port=3000"
    networks:
      - prod

    depends_on:
      - node-manager
    healthcheck:
      test: ["CMD", "node", "-e", "fetch('http://node-manager-web:3000/healthcheck').then(res => res.status === 200)"]
      start_period: 5s

  monitor:
    image: ${DOCKER_IMAGE_MONITOR}
    restart: always
    environment:
      NATS_SERVERS: nats://${NATS_ADMIN_USERNAME}:${NATS_ADMIN_PASSWORD}@nats:4222
      NATS_NAMESPACE: bk-lite
      CLIENT_ID: monitor
      DB_NAME: monitor
      VICTORIAMETRICS_HOST: http://victoria-metrics:8428
      ENABLE_CELERY: "True"
      BROKER_URL: redis://:${REDIS_PASSWORD}@redis:6379/10
      CELERY_BROKER_URL: redis://:${REDIS_PASSWORD}@redis:6379/10
      CELERY_RESULT_BACKEND: redis://:${REDIS_PASSWORD}@redis:6379/10
      DEBUG: "0"
      SECRET_KEY: ${SECRET_KEY}
      DB_ENGINE: postgresql
      DB_USER: ${POSTGRES_USERNAME}
      DB_HOST: postgres
      DB_PASSWORD: ${POSTGRES_PASSWORD}
      DB_PORT: "5432"
      INSTALL_APPS: monitor
    healthcheck:
      test: ["CMD", "curl", "-s", "-o", "/dev/null", "-w", "'%{http_code}'", "http://127.0.0.1:8000/"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 10s
    depends_on:
      system-manager:
        condition: service_healthy
    networks:
      - prod

  monitor-web:
    image: ${DOCKER_IMAGE_MONITOR_WEB}
    restart: always
    environment:
      NEXTAUTH_URL: http://${HOST_IP}:${TRAEFIK_MONITOR_PORT}
      NEXTAUTH_SECRET: ${NEXTAUTH_SECRET}
      NEXTAPI_URL: http://monitor:8000
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.monitor-web.rule=Host(\`${HOST_IP}\`)"
      - "traefik.http.routers.monitor-web.entrypoints=monitor-web"
      - "traefik.http.services.monitor-web.loadbalancer.server.port=3000"
    networks:
      - prod

    depends_on:
      - monitor
    healthcheck:
      test: ["CMD", "node", "-e", "fetch('http://monitor-web:3000/healthcheck').then(res => res.status === 200)"]
      start_period: 5s
  
  cmdb:
    image: ${DOCKER_IMAGE_CMDB}
    restart: always
    environment:
      DEBUG: 0
      INSTALL_APPS: cmdb
      SECRET_KEY: ${SECRET_KEY}
      DB_ENGINE: postgresql
      DB_USER: ${POSTGRES_USERNAME}
      DB_HOST: postgres
      DB_PASSWORD: ${POSTGRES_PASSWORD}
      DB_PORT: "5432"
      NATS_SERVERS: nats://${NATS_ADMIN_USERNAME}:${NATS_ADMIN_PASSWORD}@nats:4222
      NATS_NAMESPACE: bk-lite
      CLIENT_ID: cmdb
      DB_NAME: cmdb
      NEO4J_URI: bolt://neo4j:7687
      NEO4J_USER: ${NEO4J_USERNAME}
      NEO4J_PASSWORD: ${NEO4J_PASSWORD}
      VICTORIAMETRICS_HOST: http://victoria-metrics:8428
      ENABLE_CELERY: True
      BROKER_URL: redis://:${REDIS_PASSWORD}@redis:6379/11
      CELERY_BROKER_URL: redis://:${REDIS_PASSWORD}@redis:6379/11
      CELERY_RESULT_BACKEND: redis://:${REDIS_PASSWORD}@redis:6379/11
      REDIS_CACHE_URL: redis://:${REDIS_PASSWORD}@redis:6379/11
      CELERY_WORKER_CONCURRENCY: 1
    networks:
      - prod

    depends_on:
      system-manager:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-s", "-o", "/dev/null", "-w", "'%{http_code}'", "http://cmdb:8000/healthcheck"]
  
  cmdb-web:
    image: ${DOCKER_IMAGE_CMDB_WEB}
    restart: always
    environment:
      NEXTAUTH_URL: http://${HOST_IP}:${TRAEFIK_CMDB_PORT}
      NEXTAUTH_SECRET: ${NEXTAUTH_SECRET}
      NEXTAPI_URL: http://cmdb:8000
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.cmdb-web.rule=Host(\`${HOST_IP}\`)"
      - "traefik.http.routers.cmdb-web.entrypoints=cmdb-web"
      - "traefik.http.services.cmdb-web.loadbalancer.server.port=3000"
    networks:
      - prod

    depends_on:
      - cmdb
    healthcheck:
      test: ["CMD", "node", "-e", "fetch('http://cmdb-web:3000/healthcheck').then(res => res.status === 200)"]
      start_period: 5s

  telegraf:
    image: bklite/telegraf
    container_name: telegraf
    environment:
      - METRIC_NATS_USERNAME=${NATS_ADMIN_USERNAME}
      - METRIC_NATS_PASSWORD=${NATS_ADMIN_PASSWORD}
      - METRIC_OUTPUT_URL=http://victoria-metrics:8428
      - METRIC_NATS_SERVERS=nats://nats:4222
    volumes:
      - ./conf/telegraf/telegraf.conf:/etc/telegraf/telegraf.conf
    networks:
      - prod

    restart: always

  fusion-collector:
    image: bklite/fusion-collector:latest
    container_name: fusion-collector
    hostname: fusion-collector-default
    environment:
      - SERVER_URL=http://node-manager:8000/node_mgmt/open_api/node
      - SERVER_API_TOKEN=${SIDECAR_INIT_TOKEN}
      - SIDECAR_ZONE=1
      - SIDECAR_GROUP=1
      - SIDECAR_NODEID=1
      - SIDECAR_NODENAME=fusion-collector
    networks:
      - prod
    restart: always

  ops-console:
    image: ${DOCKER_IMAGE_OPSCONSOLE}
    restart: always
    environment:
      NATS_SERVERS: nats://${NATS_ADMIN_USERNAME}:${NATS_ADMIN_PASSWORD}@nats:4222
      NATS_NAMESPACE: bk-lite
      CLIENT_ID: ops-console
      DB_NAME: ops-console
      DB_USER: ${POSTGRES_USERNAME}
      DB_HOST: postgres
      DB_PASSWORD: ${POSTGRES_PASSWORD}
      DB_ENGINE: postgresql
      DB_PORT: "5432"
      DEBUG: "0"
      SECRET_KEY: ${SECRET_KEY}
    networks:
      - prod
    healthcheck:
      test: ["CMD", "curl", "-s", "-o", "/dev/null", "-w", "'%{http_code}'", "http://127.0.0.1:8000/"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 10s

    depends_on:
      system-manager:
        condition: service_healthy
    
  ops-console-web:
    image: bklite/ops-console-web
    container_name: ops-console-web
    environment:
      - NEXTAPI_URL=http://ops-console:8000
      - NEXTAUTH_URL=http://${HOST_IP}:${TRAEFIK_CONSOLE_PORT}
      - NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
      - NEXTAPI_URL=http://ops-console:8000
    restart: always
    networks:
      - prod
    labels:
      - traefik.enable=true
      - traefik.http.routers.ops-console-web.rule=Host(\`${HOST_IP}\`)
      - traefik.http.routers.ops-console-web.entrypoints=opsconsole
      - traefik.http.services.ops-console-web.loadbalancer.server.port=3000
    healthcheck:
      test: ["CMD", "node", "-e", "fetch('http://ops-console-web:3000/healthcheck').then(res => res.status === 200)"]
      start_period: 5s
    depends_on:
      - ops-console

  stargazer:
    image: ${DOCKER_IMAGE_STARGAZER}
    container_name: stargazer
    networks:
      - prod

EOF
fi

# 按照特定顺序启动服务
log "INFO" "启动基础服务 (Traefik, Redis, NATS, VictoriaMetrics, Neo4j)..."
docker-compose up -d traefik redis nats victoria-metrics neo4j

# 获取 Docker Compose 创建的网络名称
PROJECT_NAME=$(basename $(pwd))
COMPOSE_NETWORK=${PROJECT_NAME}_prod

# 创建 JetStream - 使用正确的网络名称
log "INFO" "创建JetStream..."
docker run --rm --network=${COMPOSE_NETWORK} \
    $DOCKER_IMAGE_NATS_CLI -s nats://nats:4222 \
    --user $NATS_ADMIN_USERNAME --password $NATS_ADMIN_PASSWORD \
    stream add metrics --subjects=metrics.* --storage=file \
    --replicas=1 --retention=limits  --discard=old \
    --max-age=20m --max-bytes=104857600 --max-consumers=-1 \
    --max-msg-size=-1 --max-msgs=-1 --max-msgs-per-subject=1000000 \
    --dupe-window=5m --no-allow-rollup --no-deny-delete --no-deny-purge

# 启动 Postgres 并等待服务就绪
log "INFO" "启动 Postgres..."
docker-compose up -d postgres
wait_container_health postgres "Postgres"

# 启动服务
log "INFO" "启动系统管理服务..."
docker-compose up -d system-manager

log "INFO" "启动所有服务"
docker-compose up -d
sleep 10
wait_container_health cmdb-web "CMDB"
wait_container_health monitor-web "MONITOR"
wait_container_health system-manager-web "SYSTEM_MGMT"
wait_container_health ops-console-web "OPS_CONSOLE"
wait_container_health node-manager-web "NODE_MGMT"
log "SUCCESS" "部署成功，访问 http://$HOST_IP:$TRAEFIK_MONITOR_PORT 访问系统"
log "SUCCESS" "初始用户名: admin, 初始密码: password"
log "SUCCESS" "控制器安装信息："
log "SUCCESS" "Token: ${SIDECAR_INIT_TOKEN}"
log "SUCCESS" "API_URL: http://$HOST_IP:$NODE_MANAGER_API_PORT"

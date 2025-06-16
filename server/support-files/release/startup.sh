python manage.py migrate || true
python manage.py createcachetable django_cache
python manage.py collectstatic --noinput

# 初始化函数定义
init_system_mgmt() {
    echo "系统管理资源初始化..."
    python manage.py init_realm_resource || true
    python manage.py init_login_settings || true
    python manage.py create_user admin password --email=admin@bklite.net --is_superuser || true
}

init_cmdb() {
    echo "CMDB资源初始化..."
    python manage.py model_init || true
}

init_console_mgmt() {
    echo "控制台管理资源初始化..."
    # 如果有控制台管理相关的初始化命令，在这里添加
}

init_monitor() {
    echo "初始化监控资源..."
    python manage.py plugin_init || true
}

init_node_mgmt() {
    echo "初始化节点管理..."
    python manage.py node_init || true
}

init_opspilot() {
    echo "OpsPilot资源初始化..."
    python manage.py init_bot || true
    python manage.py init_channel || true
    python manage.py init_llm || true
}

# 读取 INSTALL_APPS 环境变量
INSTALL_APPS=${INSTALL_APPS:-""}

# 去除空白字符
INSTALL_APPS=$(echo "$INSTALL_APPS" | tr -d ' ')

# 如果 INSTALL_APPS 为空，执行所有初始化
if [ -z "$INSTALL_APPS" ]; then
    init_system_mgmt
    init_cmdb
    init_monitor
    init_node_mgmt
    init_opspilot
else
    # 按逗号分割 INSTALL_APPS
    IFS=',' read -ra APPS <<< "$INSTALL_APPS"
    
    for app in "${APPS[@]}"; do
        case "$app" in
            "system_mgmt")
                init_system_mgmt
                ;;
            "cmdb")
                init_cmdb
                ;;
            "console_mgmt")
                init_console_mgmt
                ;;
            "monitor")
                init_monitor
                ;;
            "node_mgmt")
                init_node_mgmt
                ;;
            "opspilot")
                init_opspilot
                ;;
            *)
                echo "未知模块: $app"
                ;;
        esac
    done
fi

supervisord -n
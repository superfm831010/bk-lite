#! /bin/bash

get_host_ip() {
    hostname -I | awk '{print $1}'
}

get_tomcat_home() {
    ps -ef | grep Bootstrap | grep -vE "grep|openjdk" | awk -F"Dcatalina.home=" '{print $2}' | awk '{print $1}'
}

get_tomcat_context() {
    local tomcat_server="${1}/conf/server.xml"
    cat "$tomcat_server" | sed 's/<!--/\n<!--\n/' | sed 's/-->/\n-->/' | sed '/<!--/,/-->/ d' | sed '/-->/ d' | sed '/^\s*$/d'
}

get_tomcat_port() {
    local context="$1"
    echo "$context" | tr '\r' ' ' | tr '\n' ' ' | grep -Eo '<Connector[^>]*>' | grep port | grep -vEi "Define|support|Server|apache|SSLEnabled|AJP" | grep -v "<!" | awk -F "port=" '{print $2}' | awk '{print $1}' | awk -F'"' '{print $2}' | uniq
}

get_jvm_options() {
    local pid=$(ps -ef | grep -v grep | grep Bootstrap | awk '{print $2}')
    if [ -z "$pid" ]; then
        echo ""
        return
    fi

    if [ -f "/proc/$pid/cmdline" ]; then
        tr '\0' ' ' < "/proc/$pid/cmdline"
    else
        ps -ef | grep -v grep | grep "$pid" | sed 's/^[^ ]* [^ ]* [^ ]* [^ ]* //'
    fi
}

get_tomcat_version() {
    "$1/bin/version.sh" 2>/dev/null | grep -oP 'Apache Tomcat/\K[^\s]+'
}

get_jdk_version() {
    unset JDK_JAVA_OPTIONS 2>/dev/null
    java -version 2>&1 | grep -oP 'version\s+"\K[^"]+'
}

get_init_heap() {
    local opts="$1"
    echo "$opts" | grep -oP '-Xms[[:space:]]+\K[0-9]+[kKmMgG]*' | xargs
}

get_max_heap() {
    local opts="$1"
    echo "$opts" | grep -oP '-Xmx[[:space:]]+\K[0-9]+[kKmMgG]*' | xargs
}

get_max_non_heap() {
    local opts="$1"
    echo "$opts" | grep -oP '(-XX:MaxMetaspaceSize|MaxPermSize)=[[:space:]]+\K[0-9]+[kKmMgG]*' | xargs
}

get_init_non_heap() {
    local opts="$1"
    echo "$opts" | grep -oP '(-XX:MetaspaceSize|PermSize)=[[:space:]]+\K[0-9]+[kKmMgG]*' | xargs
}

get_log_path() {
    local base="$1"
    local default_log="${base}/logs/catalina.out"
    if [ -f "$default_log" ]; then
        echo "$default_log"
    else
        find "${base}/logs" -name "catalina.out" 2>/dev/null | head -1
    fi
}

discover_tomcat() {
    local host_ip=$(get_host_ip)
    local tomcat_home=$(get_tomcat_home)

    for b in $tomcat_home; do
        local tomcat_context=$(get_tomcat_context "$b")
        local tomcat_port=$(get_tomcat_port "$tomcat_context")

        if [[ ! "$tomcat_port" =~ ^[0-9]+$ ]]; then
            continue
        fi

        local jvm_opts=$(get_jvm_options)
        echo "jvm_opts: $jvm_opts"

        local version=$(get_tomcat_version "$b")
        local java_version=$(get_jdk_version)
        local xms=$(get_init_heap "$jvm_opts")
        local xmx=$(get_max_heap "$jvm_opts")
        local max_perm_size=$(get_max_non_heap "$jvm_opts")
        local permsize=$(get_init_non_heap "$jvm_opts")
        local log_path=$(get_log_path "$b")

        cat <<EOF
{
    "inst_name": "${host_ip}-tomcat-${tomcat_port}",
    "obj_id": "tomcat",
    "ip_addr": "${host_ip}",
    "port": "${tomcat_port}",
    "catalina_path": "${b}/bin/catalina.sh",
    "version": "${version}",
    "xms": "${xms}",
    "xmx": "${xmx}",
    "max_perm_size": "${max_perm_size}",
    "permsize": "${permsize}",
    "log_path": "${log_path}",
    "java_version": "${java_version}"
}
EOF
    done
}

discover_tomcat

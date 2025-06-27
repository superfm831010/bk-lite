#!/bin/bash

host_innerip=$(hostname -I | awk '{print $1}')

get_rabbitmq_status() {
    rabbitmqctl status
}

get_rabbitmq_version() {
    echo "$1" | grep "RabbitMQ version:" | awk -F': ' '{print $2}'
}

get_erlang_version() {
    echo "$1" | grep "Erlang configuration:" | awk -F' ' '{print $4}'
}

get_enabled_plugin_file() {
    echo "$1" | grep "Enabled plugin file:" | awk -F': ' '{print $2}'
}

get_node_name() {
    echo "$1" | grep "Node name:" | awk -F': ' '{print $2}'
}

get_log_files() {
    echo "$1" |  awk '/Log file\(s\)/,/Alarms/' | grep -v "Log file(s)" | grep -v "Alarms"  | grep -v '^$' | awk '{print $2}' | paste -sd,
}

get_config_files() {
    echo "$1" |  awk '/Config files/,/Log file\(s\)/' | grep -v "Config files" | grep -v "Log file(s)"  | grep -v '^$' | awk '{print $2}' | paste -sd,
}

get_main_port() {
    echo "$1" | grep "Interface: \[::\], port:" | grep "protocol: amqp" | awk -F', ' '{print $2}' | awk -F': ' '{print $2}'
}

get_all_ports() {
    echo "$1" | grep "Interface: \[::\], port:" | awk -F', ' '{print $2, $3}'|awk -F ' ' '{print $2 "("$4 ")"}' | paste -sd,
}

discover_rabbitmq() {
    status_output=$(get_rabbitmq_status)
    if [ $? -ne 0 ]; then
        echo "{}"
        exit 1
    fi
    rabbitmq_version=$(get_rabbitmq_version "$status_output")
    erlang_version=$(get_erlang_version "$status_output")
    enabled_plugin_file=$(get_enabled_plugin_file "$status_output")
    node_name=$(get_node_name "$status_output")
    log_files=$(get_log_files "$status_output")
    config_files=$(get_config_files "$status_output")
    # config_config为空时,给个默认值"/etc/rabbitmq/rabbitmq.conf"
    if [ -z "$config_files" ]; then
        config_files="/etc/rabbitmq/rabbitmq.conf"
    fi
    main_port=$(get_main_port "$status_output")
    all_ports=$(get_all_ports "$status_output")
    
    inst_name="$host_innerip-rabbitmq-$main_port"
    printf '{
    "inst_name": "%s",
    "obj_id":"rabbitmq",
    "port": "%s",
    "allport": "%s",
    "ip_addr": "%s",
    "node_name": "%s",
    "log_path": "%s",
    "conf_path": "%s",
    "version": "%s",
    "enabled_plugin_file": "%s",
    "erlang_version": "%s"
    }' \
    "$inst_name" "$main_port" "$all_ports" "$host_innerip" "$node_name" "$log_files" "$config_files" "$rabbitmq_version" "$enabled_plugin_file" "$erlang_version"
}

discover_rabbitmq


# -*- coding: utf-8 -*-
# @File：kafka_info.py
# @Time：2025/6/9 12:02
# @Author：bennie


import json

from core.nast_request import NATSClient
from plugins.base_utils import convert_to_prometheus_format
from sanic.log import logger


class KafkaInfo:
    """Class for collecting kafka information."""

    def __init__(self, params: dict):
        self.node_id = params["node_id"]
        self.host = params.get("host", "")
        self.username = params.get("username")
        self.password = params.get("password")
        self.time_out = int(params.get("execute_timeout", 60))
        self.command = params.get("command", self.script)
        self.port = int(params.get("port", 22))
        self.nats_client = NATSClient()

    @property
    def script(self) -> str:
        result = """
#!/bin/bash

# Function to get Java version
get_jdk_version() {
    jpath=$1
    version=$($jpath -version 2>&1 | grep 'version' | awk -F '\"' '{print $2}')
    echo $version
}

# Function to make command to dict
make_command() {
    command=$1
    declare -A ret_dict
    for i in $command; do
        if [[ $i == *=* ]]; then
            key=$(echo $i | cut -d '=' -f 1)
            value=$(echo $i | cut -d '=' -f 2-)
            ret_dict[$key]=$value
        fi
    done
    echo $(declare -p ret_dict)
}

# Function to get config content
get_config_content() {
    cfg_path=$1
    declare -A ret
    while IFS= read -r line; do
        if [[ $line == \\#* ]]; then
            continue
        fi
        if [[ $line == *=* ]]; then
            key=$(echo $line | cut -d '=' -f 1)
            value=$(echo $line | cut -d '=' -f 2-)
            ret[$key]=$value
        fi
    done < $cfg_path
    echo $(declare -p ret)
}

# Function to get Kafka version from JAR file (fallback: use version.properties)
get_kafka_version() {
    installpath=$1
    if [[ $installpath == */ ]]; then
        lib_path="${installpath}libs"
    else
        lib_path="${installpath}/libs"
    fi

    version=$(find ./ -name 'kafka_*.jar' | head -1 | grep -oP 'kafka_\K[^-]+\-[^-]+' | awk -F '/libs' '{print $1}')

    echo $version
}

# Main script
# Use /proc to find Kafka processes instead of ps -ef
pid_list=$(find /proc -maxdepth 1 -type d -name "[0-9]*" -exec bash -c '
  cmdline=$(tr "\0" " " < {}/cmdline 2>/dev/null)
  [[ $cmdline =~ kafka\.Kafka ]] && echo {}
' \; | cut -d '/' -f 3)
if [[ -z $pid_list ]]; then
    echo 'Not found process'
    exit 1
fi

for pid in $pid_list; do
    # Get command line arguments from /proc
    command=$(tr '\0' ' ' < /proc/$pid/cmdline 2>/dev/null)

    # Fallback to /proc/self if necessary
    if [[ -z $command ]]; then
        command=$(tr '\0' ' ' < /proc/self/cmdline 2>/dev/null)
    fi

    # Get working directory
    cwd=$(readlink -f /proc/$pid/cwd 2>/dev/null)

    # Get user and executable path
    user=$(ps -p $pid -o user= 2>/dev/null)
    exe=$(readlink -f /proc/$pid/exe 2>/dev/null)

    # Parse command line arguments
    eval $(make_command "$command")
    cfg_path=$(echo $command | awk '{print $NF}')

    # Handle relative paths
    if [[ $cwd == '/' ]]; then
        cfg_path="${cfg_path}"
    elif [[ $cwd == */ ]]; then
        cfg_path="${cwd}${cfg_path}"
    else
        cfg_path="${cwd}/${cfg_path}"
    fi

    # Parse configuration file
    eval $(get_config_content "$cfg_path")

    # Extract port information
    port=''
    if [[ -n ${ret[listeners]} ]]; then
        IFS=',' read -ra listeners <<< "${ret[listeners]}"
        for listener in "${listeners[@]}"; do
            if [[ $listener == *PLAINTEXT* ]]; then
                port=$(echo $listener | awk -F ':' '{print $NF}')
            elif [[ $listener == *INTERNAL* ]]; then
                port=$(echo $listener | awk -F ':' '{print $NF}')
            fi
        done
        if [[ -z $port ]]; then
            port=$(echo ${ret[listeners]} | awk -F ':' '{print $NF}')
        fi
    else
        if [[ -n ${ret[port]} ]]; then
            port=${ret[port]}
        else
            echo "Not found port"
            continue
        fi
    fi

    # Get inner IP
    host_innerip=$(hostname -I | awk '{print $1}')  # 获取第一个内网 IP 地址


    # Extract classpath and install path

    cmdline=$(cat /proc/1/cmdline | tr '\0' ' ')
        classpath=$(echo $cmdline | grep -oP '(?<=-cp\s)\S+')
        if [ -n \"$classpath\" ]; then
            install_path=$(echo $classpath | grep -oP '[^:]*(?=/libs)' | head -n 1 | xargs -I {} readlink -f {})
        fi
        if [ -z \"$install_path\" ]; then
            continue
        fi

    # Extract broker ID and other configurations
    broker_id=$(grep -oP '(?<=^broker.id=)\d+' "$cfg_path")

    io_threads=$(grep -oP '(?<=^num.io.threads=)\d+' "$cfg_path")

    network_threads=$(grep -oP '(?<=^num.network.threads=)\d+' "$cfg_path")

    socket_receive_buffer_bytes=$(grep -oP '(?<=^socket.receive.buffer.bytes=)\d+' "$cfg_path")

    socket_request_max_bytes=$(grep -oP '(?<=^socket.request.max.bytes=)\d+' "$cfg_path")

    socket_send_buffer_bytes=$(grep -oP '(?<=^socket.send.buffer.bytes=)\d+' "$cfg_path")

    log_path=$(echo $command | grep -oP '(?<=-Dkafka.logs.dir=)\S+')

    # Construct output data
    printdata="{
      \"host_name\":\"${host_innerip}-kafka-${port}\",
      \"obj_id\":\"kafka\",
      \"install_path\":\"$install_path\",
      \"port\":\"$port\",
      \"user\":\"$user\",
      \"log_path\":\"$(readlink -f $log_path)\",
      \"conf_path\":\"$cfg_path\",
      \"version\":\"$(get_kafka_version $install_path)\",
      \"java_path\":\"$exe\",
      \"ip_addr\":\"$host_innerip\",
      \"java_version\":\"$(get_jdk_version $exe)\",
      \"xms\":\"$(echo $command | grep -oP '(?<=-Xms)\S+')\",  #初始堆内存大小
      \"xmx\":\"$(echo $command | grep -oP '(?<=-Xmx)\S+')\", #最大堆内存大小
      \"broker_id\":\"$broker_id\", #broker id
      \"io_threads\":\"$io_threads\", #io线程数
      \"network_threads\":\"$network_threads\", #网络线程数
      \"socket_receive_buffer_bytes\":\"$socket_receive_buffer_bytes\", #socket接收缓冲区大小
      \"socket_request_max_bytes\":\"$socket_request_max_bytes\", #socket请求最大字节数
      \"socket_send_buffer_bytes\":\"$socket_send_buffer_bytes\" #socket发送缓冲区大小
    }"

    echo "$printdata" | jq .
done
    """
        return result

    async def connect_nats(self):
        """异步连接 NATS"""
        await self.nats_client.connect()

    async def close_nats(self):
        """异步关闭 NATS"""
        await self.nats_client.close()

    @property
    def nast_id(self):
        """
        生成NATS ID
        :return:
        """
        return "ssh.execute" if self.username else "local.execute"

    def format_params(self):
        """
        格式化参数
        :return:
        """
        script_params = {
            "command": self.command,
        }
        if self.username:
            script_params["username"] = self.username
            script_params["password"] = self.password
            script_params["host"] = self.host
        if self.time_out:
            script_params["execute_timeout"] = self.time_out
        return script_params

    async def exec_script(self):
        """
        调用 NATS 执行脚本
        """
        exec_params = {
            "args": [self.format_params()],
            "kwargs": {}
        }
        subject = f"{self.nast_id}.{self.node_id}"
        response = await self.nats_client.request(subject=subject, params=exec_params)  # 使用 await 调用异步方法
        return json.loads(response["result"])

    async def list_all_resources(self):
        """
        Convert collected data to a standard format.
        """
        try:
            await self.connect_nats()  # 异步连接 NATS
            data = await self.exec_script()  # 使用 await 获取执行结果
            prometheus_data = convert_to_prometheus_format({"kafka": [data]})
            return prometheus_data
        except Exception as err:
            import traceback
            logger.error(f"kafka_info main error! {traceback.format_exc()}")
        finally:
            await self.close_nats()

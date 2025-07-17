
### Vector Syslog简介

- &zwnj;**基本功能**&zwnj;
  - ​​实时接收日志流
  - ​​结构化协议解析

- &zwnj;**主要特点**&zwnj;
  - 高效处理​
  - 连接保持
  - ​​结构化提取​​
  - ​​编码安全​​

### Vector Syslog 输出字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| * | required、string、literal | 原始日志行内容 |`hello world`|
| appname | required、string、literal | 本地主机名（等效于 gethostname 命令） |`app-name`|
| client_metadata | optional、object | 客户端 TLS 元数据（启用 TLS 时）	 |`tls_data`|
| facility | required、string、literal | 设施代码/名称 |`1`|
| host | required、string、literal | 主机名或客户端 IP	 |`127.0.0.1`|
| hostname | required、string、literal | 日志中的主机名字段		 |`my.host.com`|
| message | required、string、literal | 日志消息正文	 |`Hello world`|
| msgid | required、string、literal | 消息 ID  |`ID47`|
| procid | required、string、literal | 进程 ID  |`8710`|
| severity | required、string、literal | 日志严重级别  |`notice`|
| source_ip | required、string、literal | 客户端 IP 或 UDS 路径  |`127.0.0.1`|
| source_type | required、string、literal | 固定为 "syslog"  |`syslog`|
| timestamp | required、timestamp | 日志时间戳（解析失败用当前时间）  |`2020-10-10T17:07:36.452332Z`|
| version | required、uint | Syslog 版本  |`1`|


### Vector Syslog 输出样例

```json
{
  "appname": "non",
  "exampleSDID@32473": {
    "eventID": "1011",
    "eventSource": "Application",
    "iut": "3"
  },
  "facility": "user",
  "host": "my-host.local",
  "hostname": "dynamicwireless.name",
  "message": "Try to override the THX port, maybe it will reboot the neural interface!",
  "msgid": "ID931",
  "procid": "2426",
  "severity": "notice",
  "source_ip": "34.33.222.212",
  "source_type": "syslog",
  "timestamp": "2020-03-13T20:45:38.119Z"
}

### Vector Exec简介

- &zwnj;**基本功能**&zwnj;
  - ​​​​执行外部命令
  - 生成结构化事件

- &zwnj;**主要特点**&zwnj;
  - 高效处理​
  - ​​断点续传
  - ​​​多流合并
  - ​​​环境控制

### Vector Exec 输出字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| command | required、string | 生成此事件的完整命令及参数 |`ping`|
| data_stream | optional、string、literal | 数据来源流标识（stdout/stderr）	 |`stdout`|
| host | required、string、literal | 执行命令的主机名（自动获取）	 |`my-host.local`|
| message | required、string、literal | 核心字段​​：命令输出的原始内容 |`2019-02-13T19:48:34+00:00 [info] Started GET "/" for 127.0.0.1`|
| pid | required、uint | 命令进程的 PID	 |`60085`|
| source_type | required、string、literal | 固定值 "exec"（标识事件来源）		 |`source_type`|
| timestamp | required、timestamp | 事件被 Vector 捕获的时间（ISO 8601格式）	 |`2020-10-10T17:07:36.452332Z`|


### Vector Exec 输出样例

```json
{
  "data_stream": "stdout",
  "host": "my-host.local",
  "message": "64 bytes from 127.0.0.1: icmp_seq=0 ttl=64 time=0.060 ms",
  "pid": 5678,
  "source_type": "exec",
  "timestamp": "2020-03-13T20:45:38.119Z"
}
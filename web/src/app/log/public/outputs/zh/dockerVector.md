
### Vector Docker_logs简介

- &zwnj;**基本功能**&zwnj;
  - ​​​​​实时收集容器日志
  - ​​结构化容器元数据

- &zwnj;**主要特点**&zwnj;
  - 高效处理​
  - ​​智能续传​​
  - ​​多行日志合并​​
  - ​​容器智能过滤​​

### Vector Docker_logs 输出字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| container_created_at | required、timestamp | 容器创建时间（UTC）	 |`2020-10-10T17:07:36.452332Z`|
| container_id | required、string、literal | 容器完整 ID		 |`9b6247364a03`|
| container_name | required、string、literal | 容器名称		 |`evil_ptolemy`|
| host | required、string、literal | 宿主机主机名	 |`my-host.local`|
| image | required、string、literal |  容器使用的镜像名称		 |`ubuntu:latest`|
| label | required、object | 容器所有标签（键值对）			 |`{"mylabel": "myvalue"}`|
| message | required、string、literal | 原始日志内容​	 |`Started GET / for 127.0.0.1 at 2012-03-10 14:28:14 +0100`|
| source_type | required、string、literal | 固定值 "docker"		 |`docker`|
| stream | required、string、literal | 日志流类型（stdout/stderr）	 |`stdout`|
| timestamp | required、literal | 日志时间戳（从 Docker 日志中提取） |`2020-10-10T17:07:36.452332Z`|


### Vector Docker_logs 输出样例

```json
{
  "container_created_at": "2020-10-03T16:11:29.443232Z",
  "container_id": "fecc98177eca7fb75a2b2186c418bf9a0cd3a05a1169f2e2293bf8987a9d96ab",
  "container_name": "flog",
  "host": "my-host.local",
  "image": "mingrammer/flog",
  "message": "150.75.72.205 - - [03/Oct/2020:16:11:29 +0000] \"HEAD /initiatives HTTP/1.1\" 504 117",
  "source_type": "docker",
  "stream": "stdout"
}

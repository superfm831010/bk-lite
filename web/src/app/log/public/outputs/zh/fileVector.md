
### Vector File简介

- &zwnj;**基本功能**&zwnj;
  - 实时监控文件变化
  - 结构化日志事件

- &zwnj;**主要特点**&zwnj;
  - 高效处理
  - 断点续传
  - 多行日志合并
  - 字符编码转换

### Vector File 输出字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| file | required、string、literal | 原始文件的绝对路径 | `/var/log/apache/access.log` |
| host | required、string、literal | 本地主机名（等效于 gethostname 命令） | `my-host.local` |
| message | required、string、literal | 文件的原始行内容 | `53.126.150.246 - - [01/Oct/2020:11:25:58...` |
| source_type | required、string、literal | 数据源类型标识（固定为 file） | `file` |
| timestamp | required、timestamp | 事件被 Vector 摄入的时间戳 | `2020-10-10T17:07:36.452332Z` |

### Vector File 输出样例

```json
{
  "file": "/var/log/apache/access.log",
  "host": "my-host.local",
  "message": "53.126.150.246 - - [01/Oct/2020:11:25:58 -0400] \"GET /disintermediate HTTP/2.0\" 401 20308",
  "source_type": "file",
  "timestamp": "2020-10-10T17:07:36.452332Z"
}

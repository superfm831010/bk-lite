
### Vector File Introduction

- &zwnj;**Basic Functions**&zwnj;
  - Real-time file change monitoring
  - Structured log events

- &zwnj;**Key Features**&zwnj;
  - Efficient processing
  - Resume from breakpoint
  - Multi-line log merging
  - Character encoding conversion

### Vector File Output Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| file | required、string、literal | Absolute path of the original file | `/var/log/apache/access.log` |
| host | required、string、literal | Local hostname (equivalent to gethostname command) | `my-host.local` |
| message | required、string、literal | Original line content from the file | `53.126.150.246 - - [01/Oct/2020:11:25:58...` |
| source_type | required、string、literal | Data source type identifier (fixed as file) | `file` |
| timestamp | required、timestamp | Timestamp when event was ingested by Vector | `2020-10-10T17:07:36.452332Z` |

### Vector File Output Example

```json
{
  "file": "/var/log/apache/access.log",
  "host": "my-host.local",
  "message": "53.126.150.246 - - [01/Oct/2020:11:25:58 -0400] \"GET /disintermediate HTTP/2.0\" 401 20308",
  "source_type": "file",
  "timestamp": "2020-10-10T17:07:36.452332Z"
}

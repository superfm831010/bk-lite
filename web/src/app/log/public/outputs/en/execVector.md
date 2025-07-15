
### Vector Exec Introduction

- &zwnj;**Basic Functions**&zwnj;
  - Execute external commands
  - Generate structured events

- &zwnj;**Key Features**&zwnj;
  - Efficient processing
  - Resume from breakpoint
  - Multi-stream merging
  - Environment control

### Vector Exec Output Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| command | required、string | Complete command and arguments that generated this event |`ping`|
| data_stream | optional、string、literal | Data source stream identifier (stdout/stderr) |`stdout`|
| host | required、string、literal | Hostname where command was executed (auto-detected) |`my-host.local`|
| message | required、string、literal | Core field: raw output content from command |`2019-02-13T19:48:34+00:00 [info] Started GET "/" for 127.0.0.1`|
| pid | required、uint | Process ID of the command |`60085`|
| source_type | required、string、literal | Fixed value "exec" (identifies event source) |`source_type`|
| timestamp | required、timestamp | Time when event was captured by Vector (ISO 8601 format) |`2020-10-10T17:07:36.452332Z`|


### Vector Exec Output Example

```json
{
  "data_stream": "stdout",
  "host": "my-host.local",
  "message": "64 bytes from 127.0.0.1: icmp_seq=0 ttl=64 time=0.060 ms",
  "pid": 5678,
  "source_type": "exec",
  "timestamp": "2020-03-13T20:45:38.119Z"
}
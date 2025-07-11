
### Vector Syslog Introduction

- &zwnj;**Basic Functions**&zwnj;
  - Real-time log stream receiving
  - Structured protocol parsing

- &zwnj;**Key Features**&zwnj;
  - Efficient processing
  - Connection maintenance
  - Structured extraction
  - Encoding security

### Vector Syslog Output Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| * | required、string、literal | Original log line content |`hello world`|
| appname | required、string、literal | Application name from syslog message |`app-name`|
| client_metadata | optional、object | Client TLS metadata (when TLS enabled) |`tls_data`|
| facility | required、string、literal | Facility code/name |`1`|
| host | required、string、literal | Hostname or client IP |`127.0.0.1`|
| hostname | required、string、literal | Hostname field from log |`my.host.com`|
| message | required、string、literal | Log message body |`Hello world`|
| msgid | required、string、literal | Message ID |`ID47`|
| procid | required、string、literal | Process ID |`8710`|
| severity | required、string、literal | Log severity level |`notice`|
| source_ip | required、string、literal | Client IP or UDS path |`127.0.0.1`|
| source_type | required、string、literal | Fixed as "syslog" |`syslog`|
| timestamp | required、timestamp | Log timestamp (current time if parsing fails) |`2020-10-10T17:07:36.452332Z`|
| version | required、uint | Syslog version |`1`|


### Vector Syslog Output Example

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
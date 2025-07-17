
### Vector Docker_logs Introduction

- &zwnj;**Basic Functions**&zwnj;
  - Real-time container log collection
  - Structured container metadata

- &zwnj;**Key Features**&zwnj;
  - Efficient processing
  - Intelligent resume
  - Multi-line log merging
  - Container smart filtering

### Vector Docker_logs Output Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| container_created_at | required、timestamp | Container creation time (UTC) |`2020-10-10T17:07:36.452332Z`|
| container_id | required、string、literal | Full container ID |`9b6247364a03`|
| container_name | required、string、literal | Container name |`evil_ptolemy`|
| host | required、string、literal | Host machine hostname |`my-host.local`|
| image | required、string、literal | Container image name |`ubuntu:latest`|
| label | required、object | All container labels (key-value pairs) |`{"mylabel": "myvalue"}`|
| message | required、string、literal | Original log content |`Started GET / for 127.0.0.1 at 2012-03-10 14:28:14 +0100`|
| source_type | required、string、literal | Fixed value "docker" |`docker`|
| stream | required、string、literal | Log stream type (stdout/stderr) |`stdout`|
| timestamp | required、literal | Log timestamp (extracted from Docker logs) |`2020-10-10T17:07:36.452332Z`|


### Vector Docker_logs Output Example

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

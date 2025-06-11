# 使用compose部署bk-lite

## 部署要求

* docker >= 20.10.23
* docker-compose >=v2.27.0 

**如要体验ops-pilot相关特性，推荐服务器单台内存>16GB**

## 安装部署

> bootstrap.sh是幂等的，多次运行不会对当前部署造成影响
> 部署bk-lite
```bash
git clone https://github.com/TencentBlueKing/bk-lite.git
cd deploy/docker-compose
bash bootstrap.sh
```

> 如需体验ops-pilot, 执行下述动作
```bash
docker-compose --profile opspilot up -d
```

#### 端口映射说明

| 端口号 | 用途                                |
| ------ | ----------------------------------- |
| 20000  | CMDB访问端口    |
| 20001  | 系统管理访问端口                    |
| 20002  | 节点管理访问端口                    |
| 20003  | 监控页面访问端口                    |
| 20004  | 控制台页面访问端口                  |
| 20005  | 节点管理API端口，用于外部控制器通讯 |
| 20006  | ops-pilot端口,用于AI相关特性 |
#### 如何干净卸载

> 需在deploy/compose目录下执行

```bash
#!/bin/bash
# 清除现有的容器，卷和网络
docker-compose --profile opspilot down --volumes
# 清除生成的安装包，环境变量和compose文件
rm -rvf pkgs *.env docker-compose.yaml .env
```


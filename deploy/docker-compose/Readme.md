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
bash bootstrap.sh --opspilot
docker-compose --profile opspilot up -d
# 当使用plugin形式安装compose时
# docker compose --profile opspilot up -d
```

## 卸载
> 需在deploy/docker-compose目录下执行

```bash
#!/bin/bash
# 清除现有的容器，卷和网络
docker-compose --profile opspilot down --volumes
# 当使用plugin形式安装compose时
# docker compose --profile opspilot down --volumes
# 清除生成的安装包，环境变量和compose文件
rm -rvf pkgs *.env docker-compose.yaml .env
```


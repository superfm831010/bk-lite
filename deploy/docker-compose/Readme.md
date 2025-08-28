# 使用compose部署bk-lite

## 部署要求

* docker >= 20.10.23
* docker-compose >=v2.27.0 

**如要体验ops-pilot相关特性，建议服务器单台内存>16GB**

## 快速体验

> install.run和bootstrap.sh是幂等的，多次运行不会对当前部署造成影响
> 一键部署
```bash
# bk-lite基础套餐
curl -sSL https://bklite.ai/install.run| bash -
# 带ops-ilot体验
curl -sSL https://bklite.ai/install.run| bash -s - --opspilot
```
> 快速卸载
```
curl -sSL https://bklite.ai/uninstall.sh| bash -
```

> 从源码部署
```bash
git clone https://github.com/TencentBlueKing/bk-lite.git
cd deploy/docker-compose
# bk-lite基础套餐
bash bootstrap.sh
# 带ops-ilot体验
bash bootstrap.sh --opspilot
```

> 手动卸载，在deploy/docker-compose或/opt/bk-lite目录下执行
```bash
#!/bin/bash
# 清除现有的容器，卷和网络
docker-compose down --volumes
# 当使用plugin形式安装compose时
docker compose down --volumes
# 清除生成的安装包，环境变量和compose文件
rm -rvf pkgs *.env docker-compose.yaml .env
```


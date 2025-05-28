# CMDB 目录结构与文件说明

本目录为蓝鲸 Lite 版 CMDB（配置管理数据库）后端核心代码，基于 Django 框架开发，主要负责资产模型、采集、实例、权限、等功能的实现。

项目技术栈：

```
Django+ pgsql + neo4j + celery + celery beat
pgsql
	存储采集任务，模型实例操作日志等
neo4j
	存储模型，模型分组，模型实例数据
celery/beat
	异步任务和周期任务
```

以下为详细的目录与文件说明：

## 目录结构

```
cmdb/
├── __init__.py
├── admin.py
├── apps.py
├── celery_tasks.py
├── config.py
├── constants.py
├── filters.py
├── management/
│   └── commands/
│       └── model_init.py 初始化模型命令
├── migrations/
│   └── ...（数据库迁移脚本）
├── models/
│   ├── __init__.py
│   ├── asset.py
│   ├── change.py
│   ├── collect.py
│   ├── display.py
│   └── ...（其他数据模型）
├── serializers/
│   ├── __init__.py
│   ├── asset.py
│   ├── collect.py
│   ├── display.py
│   └── ...（数据序列化与校验）
├── services/
│   ├── __init__.py
│   ├── asset.py
│   ├── collect.py
│   ├── migrate.py
│   └── ...（业务逻辑实现）
├── collection/
│   └── ...（采集相关逻辑）
├── utils/
│   ├── __init__.py
│   ├── auth.py
│   ├── change.py
│   ├── export.py
│   └── ...（工具函数）
├── language/
│   ├── __init__.py
│   ├── fields.py
│   ├── models.py
│   └── ...（多语言支持）
├── oid/
│   ├── __init__.py
│   └── snmp.py
├── graph/
│   ├── __init__.py
│   ├── types.py
│   └── ...（图数据库相关）
├── model_migrate/
│   ├── __init__.py
│   └── ...（模型迁移相关）
├── tests.py
├── urls.py
└── views/
    ├── __init__.py
    ├── asset.py
    ├── collect.py
    ├── display.py
    └── ...（接口实现）
```

## 主要文件与文件夹说明

- **admin.py**  
  Django 后台管理站点配置。
- **apps.py**  
  Django 应用配置。
- **celery_tasks.py**  
  定义 celery 异步任务。
- **config.py**  
  应用配置项。
- **constants.py**  
  全局常量定义。
- **filters.py**  
  过滤器定义，用于数据筛选。
- **management/**  
  Django 自定义管理命令目录。
- **migrations/**  
  Django ORM 的数据库迁移脚本。
- **models/**  
  ORM 数据模型定义，如资产、采集、变更、展示字段等。
- **serializers/**  
  数据序列化与校验，配合 views 层使用。
- **services/**  
  业务逻辑实现，如资产管理、采集任务、模型迁移等。
- **collection/**  
  采集相关逻辑，包括 K8S、网络、VMware 等采集实现。
  - base.py 采集基类
  - common.py 数据纳管类
  - constants.py 采集指标
  - service.py 具体采集实现方式
  
- **utils/**  
  工具函数，如权限、导入导出、变更记录等。
- **language/**  
  多语言支持，包含字段、模型、属性等翻译。
- **oid/**  
  OID 静态数据，如 SNMP 设备 OID 映射。
- **graph/**  
  图数据库相关操作和类型定义。
- **model_migrate/**  
  资产模型迁移相关逻辑及配置。
- **tests.py**  
  单元测试入口。
- **urls.py**  
  Django 路由配置。
- **views/**  
  视图层，API 接口实现。

---

如需详细了解每个模块的功能和用法，请参考各子目录下的代码和注释。


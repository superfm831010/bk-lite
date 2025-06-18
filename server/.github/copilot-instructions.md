# Copilot 使用说明
1、语法精简
2、重复代码超过5行的可以提取成独立方法
3、不添加多余变量
4、补充必要注释，多余的注释删除
5、必要地方添加日志，引用的logger 为各个代码模块所属APP的logger
如：opspilot使用 from apps.core.logger import opspilot_logger as logger
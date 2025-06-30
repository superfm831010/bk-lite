import nats_client
from apps.monitor.models import MonitorInstance, MonitorObject


@nats_client.register
def get_monitor_module_data(module, child_module, page, page_size, group_id):
    """
        获取监控模块数据
    """
    queryset = MonitorInstance.objects.filter(
        monitor_object_id=child_module,
        monitorinstanceorganization__organization=group_id
    ).distinct("id")
    # 计算总数
    total_count = queryset.count()
    # 计算分页
    start = (page - 1) * page_size
    end = page * page_size
    # 获取当前页的数据
    data_list = queryset.values("id", "name")[start:end]
    return {"count": total_count,"items": list(data_list)}


@nats_client.register
def get_module_list():
    """
        获取监控模块列表
    """
    objs = MonitorObject.objects.all().values("id", "type", "name")
    return [
        {
            "name": "instance",
            "display_name": "Instance",
            "children": list(objs),
        },
    ]

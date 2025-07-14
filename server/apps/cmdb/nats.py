import nats_client
from apps.cmdb.services.model import ModelManage
from apps.cmdb.services.classification import ClassificationManage
from apps.cmdb.models.collect_model import CollectModels
from apps.cmdb.services.instance import InstanceManage
from apps.cmdb.constants import PERMISSION_MODEL,PERMISSION_INSTANCES,PERMISSION_TASK
@nats_client.register
def get_cmdb_module_data(module, child_module, page, page_size, group_id):
    """
        获取cmdb模块实例数据
    """
    if module == PERMISSION_TASK:
        # 计算分页
        start = (page - 1) * page_size
        end = page * page_size
        instances = CollectModels.objects.filter(model_id=child_module).values("id","name", "model_id")[start:end]
        count = instances.count()
        queryset= [{"id":i['id'], "name":f"{i['model_id']}_{i['name']}"} for i in instances]
    elif module == PERMISSION_INSTANCES or module == PERMISSION_MODEL:
        instances, count = InstanceManage.instance_list(
            user_groups=[group_id],  # 改为列表
            roles=[],  # 空列表
            model_id=child_module,  # 使用实际模型ID
            params=[],  # 空查询条件（或按需添加）
            page=page,
            page_size=page_size,
            order="",
            check_permission=False  # 关闭权限检查
        )
        queryset = []
        for instance in instances:
            queryset.append({
                "name": instance["inst_name"],
                "id": instance["inst_name"]
            })
    else:
        raise ValueError("Invalid module type")
    return [
        {
            "count": count,
            "items": list(queryset)
        }
    ]

@nats_client.register
def get_cmdb_module_list():
    """
        获取cmdb模块列表
    """
    classifications = ClassificationManage.search_model_classification()
    classification_map = {}
    for classification in classifications:
        if classification["classification_id"] not in classification_map:
            classification_map[classification["classification_id"]] = []
        classification_map[classification["classification_id"]].append({
            "name": classification["classification_id"],
            "display_name": classification["classification_name"],
        })
    """
        根据模型分类id进行数据封装
    """
    models = ModelManage.search_model()
    model_map = {}
    for model in models:
        if model["classification_id"] not in model_map:
            model_map[model["classification_id"]] = []
        model_map[model["classification_id"]].append({
            "name": model["model_id"],
            "display_name": model["model_name"],
        })
        classification_map[model["classification_id"]].append({
            "name": model["model_id"],
            "display_name": model["model_name"],
        })
    cls_list = []
    for cls_id,item in classification_map.items():
        cls_list.append({
            "name": cls_id,
            "display_name": cls_id,
            "children": item,
        })
    model_list = []
    for cls_id,item in model_map.items():
        model_list.append({
            "name": cls_id,
            "display_name": cls_id,
            "children": item,
        })
    tasks = CollectModels.objects.all().values("name","task_type","task_id")
    task_map = {}
    for task in tasks:
        if task["task_type"] not in task_map:
            task_map[task["task_type"]] = []
        task_map[task["task_type"]].append({"name": task["task_id"], "display_name": task["name"]})
    type_list = []
    for task_type,item in task_map.items():
        type_list.append({
            "name": task_type,
            "display_name": task_type,
            "children": item,
        })
    result = [
        {"name": PERMISSION_INSTANCES,"display_name": "Instance","children":cls_list},
        {"name": PERMISSION_MODEL, "display_name": "Model", "children":model_list},
        {"name": PERMISSION_TASK,"display_name": "Task","children":type_list},
    ]
    return result
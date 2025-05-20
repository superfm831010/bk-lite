# -- coding: utf-8 --
# @File: nats_server.py
# @Time: 2025/4/25 17:04
# @Author: windyzhao
import json
from sanic.log import logger
from service.collect_service import CollectService
from core.nats_instance import register_handler


# 注册 list_regions 处理器
@register_handler("list_regions")
async def list_regions(data):
    logger.info(f"list_regions Received data: {data}")
    kwargs = data["kwargs"]
    collect_service = CollectService(kwargs)
    regions = collect_service.list_regions()
    logger.info(f"list_regions regions data: {regions}")
    return regions


async def test_connection(request):
    data = request.json
    return json.dumps({"result": True, "data": data})

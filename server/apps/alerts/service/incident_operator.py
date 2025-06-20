# -- coding: utf-8 --
# @File: incident_operator.py
# @Time: 2025/6/19 14:38
# @Author: windyzhao

from django.db import transaction
from django.utils import timezone

from apps.alerts.models import Incident
from apps.core.logger import alert_logger as logger
from apps.alerts.constants import IncidentStatus, IncidentOperate


class IncidentOperator:
    """
    事故操作类
    未分派--> 待响应 --> 处理中 --> 已关闭--> 重新打开到处理中
    """

    def __init__(self, user):
        self.user = user

    def operate(self, action: str, incident_id: str, data: dict) -> dict:
        """
        执行事故操作
        """
        logger.info(f"用户 {self.user} 开始执行事故操作: action={action}, incident_id={incident_id}")

        func = getattr(self, f"_{action}_incident", None)
        if not func:
            logger.error(f"不支持的操作类型: {action}")
            return {
                "result": False,
                "message": f"不支持的操作类型: {action}",
                "data": {}
            }

        try:
            result = func(incident_id, data)
            logger.info(f"事故操作执行成功: action={action}, incident_id={incident_id}")
            return result
        except Exception as e:
            logger.error(f"事故操作执行失败: action={action}, incident_id={incident_id}, error={str(e)}")
            return {
                "result": False,
                "message": str(e),
                "data": {}
            }

    @staticmethod
    def get_incident(incident_id):
        """获取事故对象并加锁"""
        try:
            incident = Incident.objects.select_for_update().get(incident_id=incident_id)
            return incident
        except Incident.DoesNotExist:
            logger.error(f"事故不存在: incident_id={incident_id}")
            return {
                "result": False,
                "message": "事故不存在",
                "data": {}
            }

    def _acknowledge_incident(self, incident_id: str, data: dict) -> dict:
        """确认事故 - 从待响应变为处理中"""
        with transaction.atomic():
            incident = self.get_incident(incident_id)
            if not isinstance(incident, Incident):
                return incident

            if incident.status != IncidentStatus.PENDING:
                return {
                    "result": False,
                    "message": f"事故当前状态为{incident.get_status_display()}，无法确认",
                    "data": {}
                }

            incident.status = IncidentStatus.PROCESSING
            incident.operate = IncidentOperate.ACKNOWLEDGE
            incident.updated_at = timezone.now()
            incident.updated_by = self.user
            incident.save()

            return {
                "result": True,
                "message": "事故确认成功",
                "data": {
                    "incident_id": incident_id,
                    "status": incident.status,
                    "operator": incident.operator,
                    "updated_at": incident.updated_at.isoformat()
                }
            }

    def _close_incident(self, incident_id: str, data: dict) -> dict:
        """关闭事故 - 从处理中变为已关闭"""
        with transaction.atomic():
            incident = self.get_incident(incident_id)
            if not isinstance(incident, Incident):
                return incident

            if incident.status != IncidentStatus.PROCESSING:
                return {
                    "result": False,
                    "message": f"事故当前状态为{incident.get_status_display()}，无法关闭",
                    "data": {}
                }

            incident.status = IncidentStatus.CLOSED
            incident.operate = IncidentOperate.CLOSE
            incident.updated_at = timezone.now()
            incident.updated_by = self.user
            incident.save()

            return {
                "result": True,
                "message": "事故关闭成功",
                "data": {
                    "incident_id": incident_id,
                    "status": incident.status,
                    "operator": incident.operator,
                    "updated_at": incident.updated_at.isoformat()
                }
            }

    def _reopen_incident(self, incident_id: str, data: dict) -> dict:
        """重新打开事故 - 从已关闭变为处理中"""
        with transaction.atomic():
            incident = self.get_incident(incident_id)
            if not isinstance(incident, Incident):
                return incident

            if incident.status != IncidentStatus.CLOSED:
                return {
                    "result": False,
                    "message": f"事故当前状态为{incident.get_status_display()}，无法重新打开",
                    "data": {}
                }

            incident.status = IncidentStatus.PROCESSING
            incident.operate = IncidentOperate.REASSIGN
            incident.updated_at = timezone.now()
            incident.updated_by = self.user
            incident.save()

            return {
                "result": True,
                "message": "事故重新打开成功",
                "data": {
                    "incident_id": incident_id,
                    "status": incident.status,
                    "operator": incident.operator,
                    "updated_at": incident.updated_at.isoformat()
                }
            }

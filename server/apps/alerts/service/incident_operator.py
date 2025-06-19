# -- coding: utf-8 --
# @File: incident_operator.py
# @Time: 2025/6/19 14:38
# @Author: windyzhao

from apps.alerts.models import Incident
from apps.core.logger import logger
from apps.alerts.constants import IncidentStatus, IncidentOperate


class IncidentOperator:
    """
    事故操作类
    类型：待响应，处理中，已关闭 但是可以重新打开，就会变成处理中
    """

    def __init__(self, user):
        self.user = user

    def operate(self, action: str, incident_id: str, data: dict) -> dict:
        """
        执行事故操作
        :param incident_id: 事故ID
        :param action: 操作类型
        :param data: 附加数据
        :return: 操作结果
        """
        logger.info(f"用户 {self.user} 开始执行事故操作: action={action}, incident_id={incident_id}")

        # 查找对应的操作方法
        func = getattr(self, f"_{action}_incident", None)
        if not func:
            logger.error(f"不支持的操作类型: {action}")
            raise ValueError(f"Unsupported action: {action}")

        try:
            result = func(incident_id, data)
            logger.info(f"事故操作执行成功: action={action}, incident_id={incident_id}, result={result}")
            return result
        except Exception as e:
            logger.error(f"事故操作执行失败: action={action}, incident_id={incident_id}, error={str(e)}")
            raise

    def _acknowledge_incident(self, incident_id: str, data: dict) -> dict:
        """
        确认事故 - 从待响应变为处理中
        """
        incident = Incident.objects.get(incident_id=incident_id)

        if incident.status != IncidentStatus.PENDING:
            raise ValueError(f"事故 {incident_id} 当前状态为 {incident.status}，无法确认")

        # 更新状态和操作人
        incident.status = IncidentStatus.PROCESSING
        incident.operate = IncidentOperate.ACKNOWLEDGE

        # 添加操作人到列表
        operator_list = incident.operator or []
        if self.user not in operator_list:
            operator_list.append(self.user)
        incident.operator = operator_list

        # 更新备注
        if data.get('note'):
            incident.note = data.get('note')

        incident.updated_by = self.user
        incident.save()

        return {
            'incident_id': incident_id,
            'status': incident.status,
            'operator': incident.operator,
            'message': '事故确认成功'
        }

    def _close_incident(self, incident_id: str, data: dict) -> dict:
        """
        关闭事故 - 从处理中变为已关闭
        """
        incident = Incident.objects.get(incident_id=incident_id)

        if incident.status not in [IncidentStatus.PROCESSING, IncidentStatus.PENDING]:
            raise ValueError(f"事故 {incident_id} 当前状态为 {incident.status}，无法关闭")

        # 更新状态
        incident.status = IncidentStatus.CLOSED
        incident.operate = 'close'

        # 添加操作人到列表
        operator_list = incident.operator or []
        if self.user not in operator_list:
            operator_list.append(self.user)
        incident.operator = operator_list

        # 更新备注
        if data.get('note'):
            incident.note = data.get('note')

        incident.updated_by = self.user
        incident.save()

        return {
            'incident_id': incident_id,
            'status': incident.status,
            'operator': incident.operator,
            'message': '事故关闭成功'
        }

    def _reopen_incident(self, incident_id: str, data: dict) -> dict:
        """
        重新打开事故 - 从已关闭变为处理中
        """
        incident = Incident.objects.get(incident_id=incident_id)

        if incident.status != IncidentStatus.CLOSED:
            raise ValueError(f"事故 {incident_id} 当前状态为 {incident.status}，无法重新打开")

        # 更新状态
        incident.status = IncidentStatus.PROCESSING
        incident.operate = 'reopen'

        # 添加操作人到列表
        operator_list = incident.operator or []
        if self.user not in operator_list:
            operator_list.append(self.user)
        incident.operator = operator_list

        # 更新备注
        if data.get('note'):
            incident.note = data.get('note')

        incident.updated_by = self.user
        incident.save()

        return {
            'incident_id': incident_id,
            'status': incident.status,
            'operator': incident.operator,
            'message': '事故重新打开成功'
        }

    def _assign_incident(self, incident_id: str, data: dict) -> dict:
        """
        分派事故 - 分派给指定用户
        """
        incident = Incident.objects.get(incident_id=incident_id)
        assignees = data.get('assignees', [])

        if not assignees:
            raise ValueError("分派人员不能为空")

        # 更新操作人列表
        incident.operator = assignees
        incident.operate = 'assign'

        # 如果是待响应状态，自动变为处理中
        if incident.status == IncidentStatus.PENDING:
            incident.status = IncidentStatus.PROCESSING

        # 更新备注
        if data.get('note'):
            incident.note = data.get('note')

        incident.updated_by = self.user
        incident.save()

        return {
            'incident_id': incident_id,
            'status': incident.status,
            'operator': incident.operator,
            'message': '事故分派成功'
        }

    def _update_incident(self, incident_id: str, data: dict) -> dict:
        """
        更新事故信息
        """
        incident = Incident.objects.get(incident_id=incident_id)

        # 可更新的字段
        updatable_fields = ['title', 'content', 'level', 'note']
        updated_fields = []

        for field in updatable_fields:
            if field in data:
                setattr(incident, field, data[field])
                updated_fields.append(field)

        if updated_fields:
            incident.updated_by = self.user
            incident.save()

        return {
            'incident_id': incident_id,
            'updated_fields': updated_fields,
            'message': '事故信息更新成功'
        }
